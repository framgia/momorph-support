#!/usr/bin/env python3
"""Numbered badges placed NEXT TO the element they name.

A badge sits immediately outside the element's own edge, so a reader matches a
number to a component by proximity alone. Only when every adjacent slot is taken
does a badge move away, and only then is a short leader drawn to say where it
belongs.

Pipeline
--------
1. Add a thin margin around the design so a badge on an edge element still fits.
2. Container items (box=true) get a dashed rectangle and their badge on the
   top-left corner of that rectangle.
3. Every other item takes the first free slot from an ordered candidate list:
   left, above, right, below, then inside its own top-left / top-right corner.
   Smaller elements pick first, so a big parent never steals a child's slot.
4. A badge that found no free slot is pushed outward step by step until it is
   clear, and gets a short straight leader back to the element edge.
"""
import sys, json, math
from PIL import Image, ImageDraw, ImageFont

# Margin around the design. Only has to hold a badge sitting outside an edge
# element, so it is far thinner than the old gutter columns.
MARGIN = 38

BADGE_R = 14
PILL_PAD = 6
# Gap between the element's edge and the badge's outer rim.
ADJ_GAP = 5
# Minimum centre-to-centre distance between two badges before they read as one blob.
MIN_SEP = 2 * BADGE_R + 5
# How far a displaced badge steps each time it retries.
NUDGE_STEP = MIN_SEP
NUDGE_TRIES = 14
# Width one label character takes inside the pill.
CHAR_W = 6
# Label font sizes: a plain number, and the smaller one a dotted label like `4.1.1` gets.
FONT_DIGIT = 13
FONT_DOTTED = 11
# Dashed container outline: dash then gap, and the stroke width of every red line.
DASH, DASH_GAP, STROKE = 6, 4, 1
# The body-text size every constant above was tuned against. `text_px` in the config is the
# body-text size of the image at hand, and the ratio of the two rescales the whole style: a
# badge on a 2x screenshot has to grow with the screenshot or it reads as a speck.
TEXT_PX_BASE = 13

BADGE_BG = (255, 59, 48, 255)
BADGE_BORDER = (255, 255, 255, 255)
TEXT_COLOR = (255, 255, 255, 255)
LEADER_COLOR = (255, 59, 48, 230)
GUTTER_BG = (245, 245, 245, 255)

# Gutter layout: the badge radius as a fraction of the label's font size, and the clear
# run between the gutter and the design that every leader crosses before bending.
GUTTER_R_FRAC = 0.7
LEADER_RUN = 24

# Fraction of the bbox the visible content is assumed to fill when `narrow` is set.
NARROW_FRAC = 0.5

# An element whose longer edge is under a badge's own diameter cannot carry a badge
# that reads as belonging to it, so this is the yardstick for "render it bigger".
BADGE_D = 2 * BADGE_R
# Slack allowed when a bbox lands just outside the image: a source that rounds a
# fractional Figma coordinate outward must not fail the bounds guard over it.
BOUNDS_TOL = 2
# How far the two axes of `design_size` may disagree with the PNG's own ratio.
ASPECT_TOL = 0.02


def die(msg):
    """Refuse the whole render.

    A misplaced badge is worse than no image: the log reports `adjacent` per badge,
    which says whether a slot was free, never whether the bbox was right. A silent
    mismatch therefore reaches the reader as a confident wrong answer.
    """
    print("render_badges: " + msg, file=sys.stderr)
    sys.exit(2)


def scale_factor(cfg, iw, ih):
    """PNG pixels per design unit.

    Figma's `get_screenshot` caps the longer edge at `maxDimension` (1024 unless
    asked otherwise), so any screen bigger than that comes back scaled while the
    bboxes are still in Figma units. `design_size` is the node's own size, which
    that tool returns as `original_width` / `original_height`. Omit it only when
    the bboxes are already in the PNG's own pixels.
    """
    ds = cfg.get("design_size")
    if ds is None:
        return 1.0
    if not (isinstance(ds, (list, tuple)) and len(ds) == 2):
        die("design_size must be [width, height] in design units")
    try:
        dw, dh = float(ds[0]), float(ds[1])
    except (TypeError, ValueError):
        die("design_size must be two numbers")
    if dw <= 0 or dh <= 0:
        die("design_size must be two positive numbers")
    sx, sy = iw / dw, ih / dh
    # One uniform scale produced the PNG, so axes that disagree mean `design_size`
    # describes a different node than the image does.
    if abs(sx - sy) > ASPECT_TOL * max(sx, sy):
        die("design_size %gx%g does not match the image %dx%d: x scales by %.3f, y by %.3f"
            % (dw, dh, iw, ih, sx, sy))
    return sx


def prepare_items(cfg, iw, ih):
    """Validate the config and return its items with every bbox in PNG pixels."""
    items = cfg.get("items")
    if not items:
        die("config carries no items")
    s = scale_factor(cfg, iw, ih)
    seen, out, outside = set(), [], []
    for i, it in enumerate(items):
        no = it.get("no")
        if not isinstance(no, str) or not no.strip():
            die("item #%d carries no `no`" % i)
        # `no` is the key a placement is stored under, so a duplicate would drop one
        # badge and draw the other twice, with nothing in the log to show for it.
        if no in seen:
            die("duplicate `no` %r" % no)
        seen.add(no)
        bbox = it.get("bbox")
        if not (isinstance(bbox, (list, tuple)) and len(bbox) == 4):
            die("item %s: bbox must be [x, y, w, h]" % no)
        try:
            x, y, w, h = (float(v) * s for v in bbox)
        except (TypeError, ValueError):
            die("item %s: bbox holds a non-number" % no)
        if w <= 0 or h <= 0:
            die("item %s: bbox has a zero or negative size" % no)
        if (x < -BOUNDS_TOL or y < -BOUNDS_TOL
                or x + w > iw + BOUNDS_TOL or y + h > ih + BOUNDS_TOL):
            outside.append("%s [%.0f, %.0f, %.0f, %.0f]" % (no, x, y, w, h))
        out.append(dict(it, bbox=[x, y, w, h]))
    if outside:
        die("%d bbox(es) fall outside the %dx%d image after a scale of %.3f: %s%s. "
            "Pass `design_size` (the node's original_width/original_height), or convert "
            "the bboxes to frame-relative coordinates first."
            % (len(outside), iw, ih, s, ", ".join(outside[:5]),
               " ..." if len(outside) > 5 else ""))
    return out, s


def apply_text_scale(k):
    """Rescale every pixel constant by `k`, once, before any measuring or drawing.

    Globals rather than a style object on purpose: placement and drawing both read these by
    name from a dozen places, and threading a style through all of them would be a bigger
    change than the feature. `k` is 1.0 unless the caller says the image's text is bigger.
    """
    global MARGIN, BADGE_R, PILL_PAD, ADJ_GAP, MIN_SEP, NUDGE_STEP, CHAR_W
    global FONT_DIGIT, FONT_DOTTED, DASH, DASH_GAP, STROKE, BADGE_D
    r = lambda v: max(1, int(round(v * k)))
    MARGIN, BADGE_R, PILL_PAD, ADJ_GAP = r(MARGIN), r(BADGE_R), r(PILL_PAD), r(ADJ_GAP)
    CHAR_W, FONT_DIGIT, FONT_DOTTED = r(CHAR_W), r(FONT_DIGIT), r(FONT_DOTTED)
    DASH, DASH_GAP, STROKE = r(DASH), r(DASH_GAP), r(STROKE)
    MIN_SEP = 2 * BADGE_R + r(5)
    NUDGE_STEP = MIN_SEP
    BADGE_D = 2 * BADGE_R


def load_font(size):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


# ---------- Geometry ----------
def badge_half_width(label):
    """Half-width of the pill drawn for this label, so collision uses the real shape."""
    return max(BADGE_R, (len(label) * CHAR_W + PILL_PAD * 2) / 2)


def badges_collide(a, b):
    """a, b are (cx, cy, half_w). Treated as rounded boxes of height 2*BADGE_R."""
    ax, ay, ahw = a
    bx, by, bhw = b
    return abs(ax - bx) < (ahw + bhw + 6) and abs(ay - by) < MIN_SEP


def inside_canvas(cx, cy, half_w, W, H):
    return (cx - half_w >= 2 and cx + half_w <= W - 2
            and cy - BADGE_R >= 2 and cy + BADGE_R <= H - 2)


def content_span(bbox, narrow):
    """Horizontal span of the visible content: the whole bbox, or the middle
    NARROW_FRAC of it when the caller flagged the bbox as much wider than what
    is actually drawn in it."""
    x, y, w, h = bbox
    if not narrow:
        return x, x + w
    cw = w * NARROW_FRAC
    left = x + (w - cw) / 2
    return left, left + cw


# ---------- Placement ----------
def candidate_slots(bbox, narrow, half_w):
    """Badge centres adjacent to the element, best first.

    Left and right sit level with the element's vertical middle; above and below
    align to the content's left edge, which is where a reader's eye starts.
    """
    x, y, w, h = bbox
    cl, cr = content_span(bbox, narrow)
    mid_y = y + h / 2
    # A tall element reads better with its badge near the top than at the middle.
    anchor_y = mid_y if h <= 120 else y + BADGE_R + 4
    return [
        ("left", cl - half_w - ADJ_GAP, anchor_y),
        ("above", cl + half_w, y - BADGE_R - ADJ_GAP),
        ("right", cr + half_w + ADJ_GAP, anchor_y),
        ("below", cl + half_w, y + h + BADGE_R + ADJ_GAP),
        ("inside", cl + half_w + 4, y + BADGE_R + 4),
        ("inside", cr - half_w - 4, y + BADGE_R + 4),
    ]


def place(items, iw, ih):
    """no -> (cx, cy, spot, displaced). Coordinates are canvas absolute."""
    W, H = MARGIN + iw + MARGIN, MARGIN + ih + MARGIN
    placed = []          # (cx, cy, half_w)
    out = {}

    def free(cx, cy, hw):
        return (inside_canvas(cx, cy, hw, W, H)
                and not any(badges_collide((cx, cy, hw), p) for p in placed))

    # Containers first: their corner is fixed by the dashed box, so everything
    # else has to route around them rather than the other way round. Innermost
    # first, so a nested card keeps its own corner and the outer section, which
    # has room above it, is the one that moves.
    boxes = [it for it in items if it.get("box")]
    boxes.sort(key=lambda it: it["bbox"][2] * it["bbox"][3])
    for it in boxes:
        x, y, _, _ = it["bbox"]
        hw = badge_half_width(it["no"])
        cx, cy = MARGIN + x - 2, MARGIN + y - 2
        for _ in range(NUDGE_TRIES):
            if free(cx, cy, hw):
                break
            cy -= NUDGE_STEP
        placed.append((cx, cy, hw))
        out[it["no"]] = (cx, cy, "corner", False)

    # Then the rest, smallest element first so a child beats its parent to a slot.
    rest = [it for it in items if not it.get("box")]
    rest.sort(key=lambda it: it["bbox"][2] * it["bbox"][3])
    for it in rest:
        x, y, w, h = it["bbox"]
        abs_bbox = (MARGIN + x, MARGIN + y, w, h)
        hw = badge_half_width(it["no"])
        chosen = None
        for spot, cx, cy in candidate_slots(abs_bbox, bool(it.get("narrow")), hw):
            if free(cx, cy, hw):
                chosen = (cx, cy, spot, False)
                break
        if chosen is None:
            # Every adjacent slot is taken: step left, away from the element,
            # until the badge is clear. It gets a leader so it still reads.
            cx = MARGIN + x - hw - ADJ_GAP
            cy = MARGIN + y + h / 2
            for _ in range(NUDGE_TRIES):
                if free(cx, cy, hw):
                    break
                cx -= NUDGE_STEP
            chosen = (cx, cy, "displaced", True)
        placed.append((chosen[0], chosen[1], hw))
        out[it["no"]] = chosen
    return out, W, H


def place_gutter(items, iw, ih, font):
    """Badges in a column outside the design, each with a leader to its element.

    For a dense screen, where a badge at body-text size has no free slot beside its
    element. Returns no -> (cx, cy, side, shift, anchor, pill_w), plus the canvas size and
    the design's offset on it.
    """
    pill = {it["no"]: max(2 * BADGE_R, font.getlength(it["no"]) + 2 * PILL_PAD) for it in items}
    pad = 2 * ADJ_GAP
    gutter = max(pill.values()) + 2 * pad
    ox, oy = gutter + LEADER_RUN, BADGE_R + pad
    W, H = ox + iw + LEADER_RUN + gutter, oy + ih + oy
    sep = 2 * BADGE_R + ADJ_GAP

    sides = {"left": [], "right": []}
    for it in items:
        x, y, w, h = it["bbox"]
        side = it.get("side") or ("left" if it.get("box") or x + w / 2 < iw / 2 else "right")
        if it.get("box"):
            ay = y
        else:
            ay = y + h / 2 if h <= 4 * BADGE_R else y + BADGE_R
        cl, cr = content_span((x, y, w, h), bool(it.get("narrow")))
        ax = cl if side == "left" else cr
        # Small neighbouring icons: an edge dot lands in the gap between two of them,
        # and a centre dot hides the icon, so the dot sits on the top edge's middle.
        if it.get("anchor") == "top":
            ax, ay = x + w / 2, y
        sides[side].append((oy + ay, it["no"], (ox + ax, oy + ay)))

    out = {}
    for side, rows in sides.items():
        rows.sort(key=lambda r: r[0])
        ys, prev = [], BADGE_R + 2 - sep
        for target, _, _ in rows:
            prev = max(target, prev + sep)
            ys.append(prev)
        # Pushed past the bottom edge: pull the tail back up, never below its neighbour.
        limit = H - BADGE_R - 2
        for i in range(len(ys) - 1, -1, -1):
            limit = min(ys[i], limit)
            ys[i] = limit
            limit -= sep
        for (target, no, anchor), cy in zip(rows, ys):
            w = pill[no]
            cx = gutter - pad - w / 2 if side == "left" else W - gutter + pad + w / 2
            out[no] = (cx, cy, side, cy - target, anchor, w)
    return out, W, H, ox, oy, gutter


# ---------- Drawing ----------
def draw_dashed_box(draw, x0, y0, x1, y1, dash=None, gap=None, color=LEADER_COLOR, width=None):
    dash, gap, width = dash or DASH, gap or DASH_GAP, width or STROKE
    x = x0
    while x < x1:
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        x += dash + gap
    x = x0
    while x < x1:
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
        x += dash + gap
    y = y0
    while y < y1:
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        y += dash + gap
    y = y0
    while y < y1:
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)
        y += dash + gap


def draw_dotted_line(draw, x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    dist = math.hypot(dx, dy)
    if dist < 2:
        return
    steps = max(int(dist / 3), 1)
    for i in range(0, steps, 2):
        t0, t1 = i / steps, min((i + 1) / steps, 1.0)
        draw.line(
            [(x0 + dx * t0, y0 + dy * t0), (x0 + dx * t1, y0 + dy * t1)],
            fill=LEADER_COLOR, width=STROKE,
        )


def draw_badge(draw, cx, cy, label, font_digit, font_dotted):
    font = font_dotted if "." in label else font_digit
    tb = draw.textbbox((0, 0), label, font=font)
    tw = tb[2] - tb[0]
    pill_w = max(BADGE_R * 2, tw + PILL_PAD * 2)
    if pill_w == BADGE_R * 2:
        draw.ellipse([cx - BADGE_R, cy - BADGE_R, cx + BADGE_R, cy + BADGE_R],
                     fill=BADGE_BG, outline=BADGE_BORDER, width=2)
    else:
        draw.rounded_rectangle(
            [cx - pill_w / 2, cy - BADGE_R, cx + pill_w / 2, cy + BADGE_R],
            radius=BADGE_R, fill=BADGE_BG, outline=BADGE_BORDER, width=2,
        )
    draw.text((cx, cy + 1), label, fill=TEXT_COLOR, font=font, anchor="mm")


def render(cfg):
    """Draw the badges and report what the caller needs to judge the render size."""
    src = Image.open(cfg["img"]).convert("RGBA")
    iw, ih = src.size
    items, scale = prepare_items(cfg, iw, ih)
    # A badge should read like a word of the screen's own body text. Absent a measurement, the
    # render's own scale is the best guess: a 2x render carries 2x text.
    text_px = float(cfg.get("text_px") or TEXT_PX_BASE * scale)
    apply_text_scale(text_px / TEXT_PX_BASE)
    if cfg.get("layout") == "gutter":
        return render_gutter(cfg, src, items, scale, text_px)
    positions, W, H = place(items, iw, ih)
    canvas = Image.new("RGBA", (W, H), GUTTER_BG)
    canvas.paste(src, (MARGIN, MARGIN), src)
    draw = ImageDraw.Draw(canvas)
    font_digit = load_font(FONT_DIGIT)
    font_dotted = load_font(FONT_DOTTED)

    for it in items:
        if not it.get("box"):
            continue
        x, y, w, h = it["bbox"]
        draw_dashed_box(draw, MARGIN + x - 2, MARGIN + y - 2,
                        MARGIN + x + w + 2, MARGIN + y + h + 2)

    log = []
    for it in items:
        no = it["no"]
        cx, cy, spot, displaced = positions[no]
        x, y, w, h = it["bbox"]
        if displaced:
            # Short straight leader to the nearest point on the element edge.
            draw_dotted_line(draw, cx + badge_half_width(no), cy, MARGIN + x, cy)
        draw_badge(draw, cx, cy, no, font_digit, font_dotted)
        log.append({
            "no": no, "spot": spot,
            "cx": round(cx, 1), "cy": round(cy, 1),
            "adjacent": not displaced,
        })

    canvas.convert("RGB").save(cfg["out"], "PNG")

    # The render size is the caller's to choose, per screen: a dense screen needs a
    # big PNG for the numbers to sit apart and stay readable, a sparse one does not.
    # `min_item_px` is the smallest badged element in this render, measured on its
    # longer edge, and it is what says the choice was too small.
    min_item_px = min(max(it["bbox"][2], it["bbox"][3]) for it in items)
    stats = {
        "scale": round(scale, 4),
        "text_px": round(text_px, 1),
        "badge_r": BADGE_R,
        "image_size": [iw, ih],
        "min_item_px": round(min_item_px, 1),
    }
    if min_item_px < BADGE_D:
        # Same longest edge, grown until that smallest element clears a badge.
        stats["suggest_max_dimension"] = int(math.ceil(max(iw, ih) * BADGE_D / min_item_px))
    return log, stats


def render_gutter(cfg, src, items, scale, text_px):
    """Gutter layout: every label at the full body-text size, the pill hugging it."""
    global BADGE_R
    font = load_font(FONT_DIGIT)
    BADGE_R = int(round(FONT_DIGIT * GUTTER_R_FRAC))
    iw, ih = src.size
    positions, W, H, ox, oy, gutter = place_gutter(items, iw, ih, font)
    canvas = Image.new("RGBA", (int(W), int(H)), GUTTER_BG)
    canvas.paste(src, (int(ox), int(oy)), src)
    draw = ImageDraw.Draw(canvas)

    for it in items:
        if not it.get("box"):
            continue
        x, y, w, h = it["bbox"]
        draw_dashed_box(draw, ox + x - 2, oy + y - 2, ox + x + w + 2, oy + y + h + 2)

    log = []
    lw = max(STROKE, 2)
    for it in items:
        no = it["no"]
        cx, cy, side, shift, (ax, ay), pw = positions[no]
        edge = cx + pw / 2 if side == "left" else cx - pw / 2
        bend = gutter if side == "left" else W - gutter
        draw.line([(edge, cy), (bend, cy), (ax, ay)], fill=LEADER_COLOR, width=lw, joint="curve")
        dot = lw * 2
        draw.ellipse([ax - dot, ay - dot, ax + dot, ay + dot], fill=LEADER_COLOR)
        draw_badge(draw, cx, cy, no, font, font)
        log.append({"no": no, "spot": side, "cx": round(cx, 1), "cy": round(cy, 1),
                    "shift": round(shift, 1), "adjacent": True})

    canvas.convert("RGB").save(cfg["out"], "PNG")
    stats = {
        "layout": "gutter",
        "scale": round(scale, 4),
        "text_px": round(text_px, 1),
        "badge_r": BADGE_R,
        "image_size": [iw, ih],
        "max_shift": round(max(abs(p["shift"]) for p in log), 1),
    }
    return log, stats


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    log, stats = render(cfg)
    print(json.dumps({
        "img": cfg["img"],
        "out": cfg["out"],
        **stats,
        "items_total": len(log),
        "items_corner": sum(1 for p in log if p["spot"] == "corner"),
        "items_displaced": sum(1 for p in log if not p["adjacent"]),
        "placed": log,
    }, indent=2))

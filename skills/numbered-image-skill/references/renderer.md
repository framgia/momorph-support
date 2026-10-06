# Renderer internals

Reference for `numbered-image-skill`, load when placement or style needs tuning. Implemented in
`render_badges.py`; the constants named below sit at the top of that file.

## Render size

The PNG's size is the caller's choice, not the renderer's: badge, font and separation constants are
fixed in PNG pixels, so a bigger render buys room and legibility, and a smaller one costs both. Two
numbers in the log report the consequence of that choice.

`min_item_px` is the smallest badged element in the render, measured on its longer edge. Under
`BADGE_D` (28 px, a badge's own diameter) the badge cannot read as belonging to that element, and
the log carries `suggest_max_dimension`: the current longest edge grown by `BADGE_D / min_item_px`.
It is derived from the design rather than from the current PNG, so it is stable across re-renders.

`items_displaced` is the other signal, and it usually means the same thing: a render too small for
the badges to fit beside their elements.

## Input guard

`prepare_items` runs before any placement and refuses the whole render on stderr with exit 2. It
is there because the placement log reports whether a slot was free, never whether a bbox was right,
so a coordinate error would otherwise be published as a confident wrong image. It checks:

- `design_size`, when present, is two positive numbers whose two axes agree with the PNG's own
  ratio to within `ASPECT_TOL`. The surviving factor scales every bbox.
- every `no` is a non-empty string and unique, since placement is stored under it.
- every `bbox` is four numbers with a positive width and height.
- every scaled bbox sits inside the image, with `BOUNDS_TOL` of slack for outward rounding.

## Placement

A badge is placed **next to the element it names**. No gutter columns, no leader unless a badge
could not stay adjacent.

The design gets a thin `MARGIN` of whitespace on all four sides, the only whitespace added.

**Containers** (`box: true`) are placed first, innermost first, each badge on the top-left corner of
its own dashed box. Two nested containers sharing a corner: the inner keeps it, the outer steps up
by `MIN_SEP`.

**Everything else** is placed smallest bbox first, so a child claims its slot before its parent.
Each item tries these badge centres in order and takes the first free one:

| Order | Spot | Where |
| --- | --- | --- |
| 1 | `left` | Outside the content's left edge, level with the element's vertical middle |
| 2 | `above` | Above the element, aligned to the content's left edge |
| 3 | `right` | Outside the content's right edge, level with the vertical middle |
| 4 | `below` | Below the element, aligned to the content's left edge |
| 5 | `inside` | Inside the element's own top-left corner |
| 6 | `inside` | Inside the element's own top-right corner |

An element taller than 120px anchors its `left` and `right` slots near its top, not at its middle.

A slot is free when the badge stays inside the canvas and clears every badge already placed by
`MIN_SEP` vertically and by the sum of the two half widths horizontally.

**Displaced badges.** All six slots taken: the badge steps left in `NUDGE_STEP` increments until
clear, with a short dotted leader to the element's left edge. The log marks it `"adjacent": false`.

## Gutter layout

`"layout": "gutter"` replaces the placement above, and only for a screen whose elements leave no
free space for a badge at body text size (SKILL.md hard rule 8).

- The canvas grows a column on each side of the design, as wide as the widest label plus padding,
  and a clear run of `LEADER_RUN` between that column and the design.
- Every label uses the digit font at `text_px`, dotted labels included. The pill hugs the label:
  radius `GUTTER_R_FRAC` times the font size.
- Side: the item's `side` when set, else left for a container or an element centred in the left
  half, right otherwise.
- Anchor: a container's top corner on its side; any other element's edge on its side, at its
  vertical middle, or near its top when it is taller than four badge radii. `narrow` moves the
  anchor in to the visible content, as it moves the slots. `"anchor": "top"` puts the dot on the
  middle of the element's top edge instead: set it on small icons that sit side by side, where an
  edge dot falls in the gap between two of them. A centre dot is not offered: it hides a small icon.
- Each column stacks its labels in anchor order, one badge height plus `ADJ_GAP` apart, pushed down
  only as far as the one above requires. The log reports each label's `shift` from its anchor and
  the largest as `max_shift`.
- The leader runs straight out of the pill to the column edge, then to a dot on the anchor.

## The `narrow` flag

`narrow: true` narrows the assumed content span to the middle `NARROW_FRAC` of the bbox, which
moves the `left` and `right` slots inward to where the visible content actually is. Set it for
**centred** text, a full-width label, or a logo floating in whitespace.

Do **not** set it on left-aligned text starting at the bbox's left edge: the badge lands on the words.

## Reading order

Badges are drawn in config order (`No` order) but **positioned** by size, so placement order and
reading order differ.

## Badge size

Every pixel constant below is tuned against `TEXT_PX_BASE` (13 px) of body text. `apply_text_scale`
rescales all of them once, before anything measures or draws, by `text_px / TEXT_PX_BASE` — margin,
radius, pill padding, gaps, separation, both fonts, dash lengths and stroke width together, so the
badge keeps its proportions at any size. `text_px` comes from the config; without it the factor is
the render's own `scale`, which is correct for a 1:1 render and too small for a 2x screenshot.

They are module globals rather than a style object because placement and drawing read them by name
from a dozen places; the rescale mutates them once at the top of `render`.

## Style constants

| Element | Style |
| --- | --- |
| Badge | Red fill `#FF3B30`, 2 px white border, white bold label |
| Leader | Dotted, `#FF3B30` at 230 alpha, 1 px. Only on a displaced badge |
| Container outline | Dashed red rectangle, 1 px, 6 px dash and 4 px gap |
| Margin | 38 px on all four sides (`MARGIN`) |
| Element gap | 5 px between the element edge and the badge rim (`ADJ_GAP`) |
| Badge separation | 33 px centre to centre (`MIN_SEP`) |
| Bounds slack | 2 px a bbox may sit outside the image before the guard refuses (`BOUNDS_TOL`) |
| Aspect slack | 2% the two `design_size` axes may disagree with the PNG (`ASPECT_TOL`) |

Module-level constants at the top of `render_badges.py`, not config keys: a change applies to every
screen rendered afterwards.

## Known limitations

- **The narrow heuristic is a fixed fraction:** `content_span` assumes content fills 50% of the bbox (`NARROW_FRAC`), hand-tuned in the file, no per item override.
- **Placement is greedy:** the first free slot wins, so a dense cluster can push a later item to `below`.
- **A badge may sit over neighbouring content:** collision is tested against other badges only, not element pixels. A dense screen wants one look at the PNG.
- **Overlap is resolved by stepping left only**, never up or down first.

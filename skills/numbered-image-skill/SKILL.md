---
name: numbered-image-skill
description: "Renders an annotated PNG of a UI screen, from a Figma frame, from a spec CSV carrying UI Parts node ids, or from a plain screenshot with no Figma call at all: every spec item gets a red numbered badge placed right beside the element it names, so proximity alone says which number belongs to which component. Container items get a dashed bounding box with the badge at its top-left. Use when the user explicitly asks for an \"annotated image\", \"numbered design image\", \"draw numbered badges on the screen\", \"tạo ảnh đánh số cho màn\", \"番号付き画像\", or a visual companion to a spec CSV, or hands over a screenshot and asks for its components to be numbered. OPT-IN ONLY: never produce one as a side effect of writing a spec, and do NOT use for annotating an image that is not a UI screen."
argument-hint: "[figma-url | screen-id | path/to/spec.csv | path/to/screenshot.png | path/to/cfg.json]"
compatibility: "Runs a bundled Python 3 script; requires Pillow (PIL). Needs Figma MCP access to the design file for the screenshot and the layer tree."
metadata:
  author: nguyen.thi.hien
  version: '1.3.0'
---

# Numbered Image Generator

Places numbered badges beside the components of a Figma screen, so a spec row matches a pixel
without a leader line across the design.

## Hard rules

1. **Opt-in only.** Never a side effect of spec generation, test-case generation or any other
   workflow. Run only when the user asked for the image.
2. **In the Figma modes the screenshot comes from Figma MCP:** `get_screenshot(nodeId, fileKey)`,
   never the Figma REST API. In mode S the user's own image is the source and nothing is fetched.
3. **Bboxes are frame-relative.** Every `bbox` is `[x, y, w, h]` from the screen frame's top-left, never canvas absolute: absolute coordinates misplace every badge.
4. **The render size is a per screen decision, and the bboxes are not.** `get_screenshot` caps
   the longer edge at `maxDimension`, 1024 when you do not say otherwise, so the PNG is rarely the
   design's own size. Always pass `design_size` with the response's `original_width` /
   `original_height`: the renderer derives the factor from the PNG it was handed and scales every
   bbox itself, so the config stays in design units whatever size you rendered. Getting this wrong
   is the one failure the placement log cannot show you, which is why the renderer refuses the
   whole render instead (exit 2).
5. **One badge per row.** When annotating an existing spec CSV, every row's `No` becomes exactly
   one badge, and every badge traces back to one row.
6. **A badge belongs next to its element.** First free slot around it: left, above, right, below, then its own corner. Only when every slot is taken does the badge step away with a short leader, coming back `"adjacent": false`. That flag must reach the user.
7. **The number is set at the screen's normal body text size.** `text_px` is mandatory. From Figma: the size of the screen's body text style (the regular weight text of the main content, read with `get_design_context`), multiplied by the render's scale. From a screenshot: the height of the body text measured on the image. Never a size smaller than that body text.
8. **Numbers go outside the image only when the screen leaves no room on it.** The default is `layout` absent: badges sit on the image beside their elements. Switch to `"layout": "gutter"` only when the elements sit so close together that a badge at body text size has no free space beside them: a badge would cover the content it names or a neighbour, or would sit closer to another element than to its own. A sparse screen never uses the gutter.

## Input modes

Pick one from what the user handed over, and say which one you picked.

| Mode | Input | Which rows get a badge | Where each `bbox` comes from |
| --- | --- | --- | --- |
| **F** | A Figma screen: url or node id | The components you identify on the screen | Figma `get_metadata` (parent-relative, sum the ancestors down the tree) |
| **C** | A spec CSV with a `UI Parts` column | **Exactly the CSV's rows**, labelled with that row's `No`, never a number you invent | Look the row's `UI Parts` node id up in the screen's layer tree from Figma `get_metadata` |
| **S** | A screenshot, with no Figma access asked for | The components you identify in the image | Read off the image itself. Nothing is fetched: no Figma call |

**Mode C rules.** One row, one badge, the `No` column verbatim, order preserved. A row whose
`UI Parts` is blank, or whose node id matches nothing in the geometry, gets **no badge**: name it in
the report so the user knows which rows are unillustrated, and never guess its place. A row whose
`Active status` is `archived` or `deleted` is skipped the same way.

**Mode S rules.** The bboxes are measurements taken off the picture, so say so in the report: they
are estimates, not layer geometry. Work in whatever coordinate system you measured in and declare it
with `design_size`; the renderer scales to the real pixels. Number in reading order, top to bottom
then left to right, and give a container its own number before its children. Nothing can verify the
numbers here, which is why the one look at the PNG (step 7) is not optional in this mode.

## Choosing the render size

A dense screen needs a big PNG: 40 badges 33 px apart need the room to sit apart, and a 16 px icon
needs a badge that does not swallow it. A sparse screen reads fine small, and a smaller file costs
less to pass around. So pick `maxDimension` per screen rather than taking the 1024 default:

- **Start at the design's own longer edge** (a 1440 x 960 frame: `maxDimension: 1440`). Badges then
  sit at the proportions the designer drew.
- **Go bigger** when the screen carries icons, dense tables or a long list of small controls. The
  renderer says how much: `min_item_px` is the smallest badged element in the render measured on
  its longer edge, and when that falls under a badge's own 28 px it returns
  `suggest_max_dimension`, the value that lifts it back over.
- **Go smaller** only for a sparse screen, and only while `min_item_px` stays above 28.
- **`items_displaced` above zero** means badges ran out of room, not only that a slot was taken.
  Re-render larger before reworking the `box` flags.

`suggest_max_dimension` is computed from the design, not from the current PNG, so it answers the
same number whatever size you rendered at.

## Prerequisites

Python 3 with Pillow. Check before the first run:

```bash
python3 -c "import PIL; print(PIL.__version__)"
```

## Input config

A JSON file at any path:

```json
{
  "img": "/abs/path/to/source.png",
  "out": "/abs/path/to/output-annotated.png",
  "design_size": [1440, 960],
  "text_px": 16,
  "items": [
    {"no": "1",   "bbox": [156, 90, 88, 88]},
    {"no": "2",   "bbox": [68, 184, 264, 24]},
    {"no": "3",   "bbox": [20, 220, 360, 14], "narrow": true},
    {"no": "4",   "bbox": [20, 266, 360, 92], "box": true},
    {"no": "4.1", "bbox": [224.5, 266, 76, 23]}
  ]
}
```

`text_px` is the screen's **normal body text size, in the PNG's pixels**, and it sizes the number:
the number reads at the same size as the screen's own body text. From Figma it is the body text
style's font size times the render's scale (16px body text on a 3x render: `48`). From a
screenshot it is the body text height measured on the image. It is mandatory (hard rule 7). The
log echoes `text_px` and the resulting `badge_r`.

`layout` picks where the numbers go. Absent: on the image, beside each element. `"gutter"`: in a
column outside the design on the left and right, each number at the full `text_px` with a leader
to a dot on its element. Use `"gutter"` only under hard rule 8. In the gutter an element whose
centre lies in the left half, and every container, takes the left column; the rest take the right.
Override one item with `"side": "left"` or `"side": "right"`, for example left aligned text whose
bbox reaches past the middle.

`design_size` is the screen's own size in design units, `original_width` and `original_height`
from the `get_screenshot` response. The renderer divides the PNG's size by it and multiplies every
bbox by that factor, so the config always carries plain design coordinates. Leave the key out only
when the bboxes are already measured on the PNG itself.

| Flag | Set it when | Effect |
| --- | --- | --- |
| `box: true` | The item is a section, card or container that visually frames its children | Dashed red rectangle around the bbox, badge at its top-left corner |
| `narrow: true` | The bbox is much wider than the visible content: **centred** text, a full-width label, a logo in whitespace | The badge sits beside the visible content instead of the far bbox edge. Never set it on left-aligned text starting at the bbox edge: there it lands on top of the words |

Neither flag is inferred: set both explicitly, `box` included.

## Process

1. **Get the image.** Modes F and C: Figma `get_screenshot` with the `maxDimension` the screen's
   density calls for (above), keeping `original_width` / `original_height` from the response, which
   become `design_size`. Mode S: the user's file is the image, and `design_size` is the coordinate
   system the bboxes were measured in.
2. **Get the geometry.** Modes F and C: the layer tree from Figma `get_metadata`; mode C then keeps
   only the rows the CSV lists, matched on `UI Parts`. Mode S: skip, there is nothing to fetch.
3. **Convert to frame-relative bboxes.** Figma `get_metadata` gives each node's offset from its own parent, so sum the
   ancestors down the tree. Mode S measures from the image's top-left, which is frame-relative by
   construction.
4. **Build the config.** Put `design_size` in it. Set `box: true` on every row that has children in
   the `No` hierarchy, whose `Item Type` is a framing element, or that fills a whole edge of the
   screen such as a header bar or a full-height side column: left alone, a tall column takes the
   `below` slot and lands hundreds of pixels from what it names. Set `narrow: true` on centred or
   full-width text, never on left-aligned text.
5. **Run the renderer:**
   ```bash
   python3 render_badges.py cfg.json
   ```
   It prints a JSON placement log to stdout and writes no sidecar file. Redirect stdout to keep it.
6. **Read the log, not the PNG.** `items_displaced` and any `"adjacent": false` entry name the
   items whose badge could not stay beside its element. `scale` says what the bboxes were
   multiplied by: 1.0 when you passed no `design_size`. `suggest_max_dimension`, when present, says
   the render was too small: re-run step 1 with that value rather than accepting crowded numbers. A
   guard failure exits 2, writes nothing and names the offending item on stderr.
7. **Then look at the PNG once** to confirm no badge hides the text it names, container badges sit
   at the top-left of their dashed box, and every number is unmistakably closer to its own element
   than to any other. The renderer tests a badge against other badges only, never against the
   design's pixels, so this look is the only check that a badge does not cover content. When it
   fails on more than one item at body text size, re-render with `"layout": "gutter"` (hard rule 8)
   and check that every leader's dot lands on its own element.
8. **Report** the output path plus every item that came back `"adjacent": false`.

## Output

The annotated PNG at `cfg.out`, named `{screen-name-kebab}-annotated.png` beside the spec it
accompanies. Plus this log on stdout:

```json
{
  "img": "<source PNG path>",
  "out": "<rendered PNG path>",
  "scale": 0.7111,
  "text_px": 16.0,
  "badge_r": 17,
  "image_size": [1024, 683],
  "min_item_px": 11.4,
  "suggest_max_dimension": 2520,
  "items_total": 14,
  "items_corner": 4,
  "items_displaced": 0,
  "placed": [
    {"no": "1",   "spot": "corner", "cx": 36,  "cy": 36,  "adjacent": true},
    {"no": "1.1", "spot": "left",   "cx": 82,  "cy": 82,  "adjacent": true},
    {"no": "4.1.1", "spot": "above", "cx": 163, "cy": 308, "adjacent": true}
  ]
}
```

`spot` is one of `corner`, `left`, `above`, `right`, `below`, `inside`, `displaced`. `scale` is
the factor applied to every bbox, PNG pixels per design unit. `suggest_max_dimension` appears only
when `min_item_px` fell under 28.

## Troubleshooting

| Symptom | Cause | Solution |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'PIL'` | Pillow is not installed in the interpreter you invoked | Run the prerequisite check above; install Pillow, or call the interpreter that has it |
| Every badge points at the wrong place | Absolute canvas coordinates were passed instead of frame-relative ones | Subtract the frame's `(x, y)` from all of them and re-run. See hard rule 3 |
| Exit 2, `N bbox(es) fall outside the WxH image after a scale of 1.000` | `design_size` was left out while the bboxes are in design units, and the PNG is the scaled render | Add `design_size` from the screenshot response, or convert the bboxes to the PNG's pixels |
| Exit 2, `design_size ... does not match the image` | The size belongs to a different node than the screenshot, so the two axes scale differently | Take both numbers from the same `get_screenshot` response |
| Exit 2, `duplicate \`no\``  | Two items share a `No`, which would drop one badge and draw the other twice | Give every row its own `No` before rendering |
| `items_displaced` above zero | Every slot around those elements was already taken by another badge | Re-render at a larger `maxDimension` first, since more room resolves most of them. Then name the survivors in the report; marking their parent `box: true` frees the slots the parent would otherwise have used |
| The numbers look tiny against the screen's own text | The image is a 2x or 3x capture, so its text is 2 to 3 times the size the badge defaults to | Measure the body text on the PNG and pass it as `text_px` |
| The numbers are legible but sit on top of small icons | The render is too small for the smallest badged elements | Re-render with `maxDimension` set to the `suggest_max_dimension` the log returned |
| A badge sits on top of the text it names | `narrow: true` was set on left-aligned text | Remove the flag. `narrow` is for centred or full-width content only |
| A badge sits far from its element with a dotted line | That item was displaced, see the row above | Expected fallback, not a bug |
| Two nested containers stack their badges | They share a top-left corner | Expected: the inner keeps the corner, the outer steps up by `MIN_SEP` |
| A badge overlaps a neighbouring element's label | Collision is tested against badges, not against pixels | Nudge that item's bbox, or set `box: true` on its parent to change the packing order |

## References

| File | Load when |
| --- | --- |
| [`references/renderer.md`](references/renderer.md) | Tuning placement or style: the slot order, the `narrow` flag, nested containers, the style constants, known limitations |

## When not to use it

Not inside a spec-writing workflow: spec skills produce their files without an image, and this one
runs only when the user asks. Not for annotating a photo, a chart or a diagram: the spacing
constants are tuned for UI screens, whether they come from Figma or from a screenshot.

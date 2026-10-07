---
name: numbered-image-skill
description: "Renders an annotated PNG of a UI screen, from a Figma frame, from a spec list (CSV) whose rows carry an item number and a layer node id, or from a plain screenshot with no Figma call at all: every spec item gets a red numbered badge placed right beside the element it names, so proximity alone says which number belongs to which component. Container items get a dashed bounding box with the badge at its top-left. Use when the user explicitly asks for an \"annotated image\", \"numbered design image\", \"draw numbered badges on the screen\", \"tạo ảnh đánh số cho màn\", \"番号付き画像\", or a visual companion to a spec list, or hands over a screenshot and asks for its components to be numbered. OPT-IN ONLY: never produce one as a side effect of writing a spec, and do NOT use for annotating an image that is not a UI screen."
argument-hint: "[figma-url | screen-id | path/to/spec.csv | path/to/screenshot.png | path/to/cfg.json]"
compatibility: "Runs a bundled Python 3 script; requires Pillow (PIL). Needs Figma MCP access to the design file for the screenshot and the layer tree."
metadata:
  author: nguyen.thi.hien
  version: '1.4.0'
---

# Numbered Image Generator

Places numbered badges beside the components of a UI screen.

## Hard rules

1. **Opt-in only.** Never a side effect of spec generation, test case generation or any other
   workflow. Run only when the user asked for the image.
2. **In the Figma modes the screenshot comes from Figma MCP:** `get_screenshot(nodeId, fileKey)`,
   never the Figma REST API. In mode S the user's own image is the source and nothing is fetched.
3. **Bboxes are frame relative.** Every `bbox` is `[x, y, w, h]` from the screen frame's top left, never canvas absolute.
4. **The render size is a per screen decision, and the bboxes are not.** Always pass
   `design_size` (Input config), so the config stays in design units whatever size you rendered.
5. **A badge belongs next to its element.** The renderer tries the slots listed in
   `references/renderer.md`; when every slot is taken it moves the badge away with a leader and
   logs `"adjacent": false`.
6. **The number follows the screen's body text size, within the image's bounds.** Pass `text_px`. From Figma: the size of the screen's body text style (the regular weight text of the main content, read with `get_design_context`), multiplied by the render's scale. From a screenshot: the height of the body text measured on the image. The renderer clamps the badge diameter to `badge_range` of the image's longer edge (Input config).
7. **Numbers go outside the image only when the screen leaves no room on it.** The default is `layout` absent: badges sit on the image beside their elements. Switch to `"layout": "gutter"` only when the elements sit so close together that a badge at body text size has no free space beside them: a badge would cover the content it names or a neighbour, or would sit closer to another element than to its own. A sparse screen never uses the gutter.
8. **One screen, one numbering across its images.** When one session renders several images of the same screen (its states), a component gets its number once, on the first image that shows it. A later image badges only the components no earlier image showed, with numbers not yet used. The description of a later state cites the existing number ("dùng lại 6.1"). In mode C this applies to the list's rows: a row is badged on one image only.

## Input modes

Pick one from what the user handed over, and say which one you picked.

| Mode | Input | Which rows get a badge | Where each `bbox` comes from |
| --- | --- | --- | --- |
| **F** | A Figma screen: url or node id | The components you identify on the screen | Figma `get_metadata` (Process step 3) |
| **C** | A spec list (CSV) with an item number and a layer node id per row | **Exactly the list's rows**, one badge per row, labelled with that row's item number verbatim, never a number you invent | Look the row's node id up in the screen's layer tree from Figma `get_metadata` |
| **S** | A screenshot, with no Figma access asked for | The components you identify in the image | Read off the image itself. Nothing is fetched: no Figma call |

**Mode C rules.** Row order preserved. A row whose node id is blank, or whose node id matches
nothing in the geometry, gets **no badge**: name it in the report, and never guess its place. A
row whose `Active status` is `archived` or `deleted` is skipped the same way.

**Mode S rules.** Say in the report that the bboxes are estimates measured off the image, not
layer geometry. Work in whatever coordinate system you measured in and declare it with
`design_size`. Number in reading order, top to bottom then left to right, and give a container its
own number before its children.

## Choosing the render size

`get_screenshot` caps the longer edge at `maxDimension`, 1024 when you do not say otherwise. Pass
the design's own longer edge (a 1440 x 960 frame: `maxDimension: 1440`). The badge size follows the
image (hard rule 6), so a larger render does not change how badges fit around small elements.

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

`text_px` is set per hard rule 6, **in the PNG's pixels** (16px body text on a 3x render: `48`).
The badge diameter is `text_px` times 28 / 13, clamped to `badge_range` of the image's longer edge,
default `[0.018, 0.045]`, and never under 20 px. Without `text_px` the diameter is 2.7% of the
longer edge. Override the bounds with `"badge_range": [min, max]`. The log reports `badge_r`,
`badge_source` (`text_px` or `image`) and `badge_clamped` (`min`, `max` or `null`).

`layout` picks where the numbers go. Absent: on the image, beside each element. `"gutter"`: in a
column outside the design on the left and right, each number at the full `text_px` with a leader
to a dot on its element. Use `"gutter"` only under hard rule 7. In the gutter an element whose
centre lies in the left half, and every container, takes the left column; the rest take the right.
Override one item with `"side": "left"` or `"side": "right"`, for example left aligned text whose
bbox reaches past the middle.

`design_size` is the screen's own size in design units, `original_width` and `original_height`
from the `get_screenshot` response. The renderer divides the PNG's size by it and multiplies every
bbox by that factor. Leave the key out only when the bboxes are already measured on the PNG itself.

| Flag | Set it when | Effect |
| --- | --- | --- |
| `box: true` | The row has children in the item number hierarchy, its item type is a framing element (section, card, container), or it fills a whole edge of the screen such as a header bar or a full height side column | Dashed red rectangle around the bbox, badge at its top left corner |
| `narrow: true` | The bbox is much wider than the visible content: **centred** text, a full width label, a logo in whitespace | The badge sits beside the visible content instead of the far bbox edge. Never set it on left aligned text starting at the bbox edge: there it lands on top of the words |

The renderer infers neither flag: set both explicitly.

## Process

1. **Get the image.** Modes F and C: Figma `get_screenshot` with the `maxDimension` chosen above,
   keeping the response's size for `design_size`. Mode S: the user's file is the image.
2. **Get the geometry.** Modes F and C: the layer tree from Figma `get_metadata`; mode C then keeps
   only the rows the list holds, matched on the node id. Mode S: skip, there is nothing to fetch.
3. **Convert to frame relative bboxes.** Figma `get_metadata` gives each node's offset from its own parent, so sum the
   ancestors down the tree. Mode S measures from the image's top left.
4. **Build the config.** Put `design_size` in it. Set `box` and `narrow` per the flag table.
5. **Run the renderer:**
   ```bash
   python3 render_badges.py cfg.json
   ```
   It prints a JSON placement log to stdout and writes no sidecar file. Redirect stdout to keep it.
6. **Read the log, not the PNG.** `items_displaced` and any `"adjacent": false` entry name the
   items whose badge could not stay beside its element. `items_under_badge` names the elements
   smaller than a badge; check those first in step 7. A guard failure exits 2, writes nothing and
   names the offending item on stderr.
7. **Then look at the PNG once** to confirm no badge hides the text it names, container badges sit
   at the top left of their dashed box, and every number is unmistakably closer to its own element
   than to any other. The renderer tests a badge against other badges only, never against the
   design's pixels, so this look is the only check that a badge does not cover content. When it
   fails on more than one item at body text size, re-render with `"layout": "gutter"` (hard rule 7)
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
  "badge_r": 17,
  "badge_source": "text_px",
  "badge_clamped": null,
  "image_size": [1024, 683],
  "items_under_badge": ["3.2"],
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
the factor applied to every bbox, PNG pixels per design unit, 1.0 when no `design_size` was
passed. The gutter layout logs `layout`, `max_shift` and a per item `shift` instead of
`items_under_badge`, and its `spot` is `left` or `right`.

## Troubleshooting

| Symptom | Cause | Solution |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'PIL'` | Pillow is not installed in the interpreter you invoked | Run the prerequisite check above; install Pillow, or call the interpreter that has it |
| Every badge points at the wrong place | Absolute canvas coordinates were passed instead of frame relative ones | Subtract the frame's `(x, y)` from all of them and re-run. See hard rule 3 |
| Exit 2, `N bbox(es) fall outside the WxH image after a scale of 1.000` | `design_size` was left out while the bboxes are in design units, and the PNG is the scaled render | Add `design_size` from the screenshot response, or convert the bboxes to the PNG's pixels |
| Exit 2, `design_size ... does not match the image` | The size belongs to a different node than the screenshot, so the two axes scale differently | Take both numbers from the same `get_screenshot` response |
| Exit 2, `duplicate \`no\``  | Two items share an item number | Give every row its own number before rendering |
| `items_displaced` above zero | Every slot around those elements was already taken by another badge | Mark their parent `box: true` to free the slots the parent would otherwise have used, or switch to the gutter under hard rule 7. Name the survivors in the report |
| The numbers look too small or too large | `text_px` is missing or wrong, or `badge_clamped` shows the bound that applied | Pass `text_px` per hard rule 6; change `badge_range` only when the default bounds do not fit the screen |
| The numbers sit on top of small icons | The icons are listed in `items_under_badge` and their neighbours left no free slot | Switch to the gutter under hard rule 7 |
| A badge sits on top of the text it names | `narrow: true` was set on left aligned text | Remove the flag |
| A badge overlaps a neighbouring element's label | Not detected by the renderer (Process step 7) | Nudge that item's bbox, or set `box: true` on its parent to change the packing order |

## References

| File | Load when |
| --- | --- |
| [`references/renderer.md`](references/renderer.md) | Tuning placement or style: the input guard, the slot order, the gutter layout, the `narrow` flag, nested containers, the style constants, known limitations |

# Renderer internals

Reference for `numbered-image-skill`, load when placement or style needs tuning. Implemented in
`render_badges.py`; the constants named below sit at the top of that file.

## Input guard

`prepare_items` runs before any placement; a failure exits 2 as in SKILL.md Process step 6. It
checks:

- `design_size`, when present, is two positive numbers whose two axes agree with the PNG's own
  ratio to within `ASPECT_TOL`. The surviving factor scales every bbox.
- the image has at most `MAX_PIXELS` (60 million) pixels.
- every `no` is a non empty string and unique.
- every `bbox` is four numbers with a positive width and height.
- every scaled bbox sits inside the image, with `BOUNDS_TOL` of slack for outward rounding.

## Placement

In the default layout a badge is placed **next to the element it names**, with no leader unless
a badge could not stay adjacent.

The design gets a `MARGIN` on all four sides.

**Containers** (`box: true`) are placed first, smallest area first, each badge on the top left
corner of its own dashed box. Two nested containers sharing a corner: the inner keeps it, the
outer steps up by `MIN_SEP`.

**Everything else** is placed smallest bbox first, so a child claims its slot before its parent.
Each item tries these badge centres in order and takes the first free one:

| Order | Spot | Where |
| --- | --- | --- |
| 1 | `left` | Outside the content's left edge, level with the element's vertical middle |
| 2 | `above` | Above the element, aligned to the content's left edge |
| 3 | `right` | Outside the content's right edge, level with the vertical middle |
| 4 | `below` | Below the element, aligned to the content's left edge |
| 5 | `inside` | Inside the element's own top left corner |
| 6 | `inside` | Inside the element's own top right corner |

An element taller than 120px anchors its `left` and `right` slots near its top, not at its middle.

A slot is free when the badge stays inside the canvas and, against every badge already placed,
either sits at least `MIN_SEP` apart vertically or at least the sum of the two half widths plus
6 px apart horizontally.

**Displaced badges.** All six slots taken: the badge steps left in `NUDGE_STEP` increments, at
most `NUDGE_TRIES` times, until clear, with a short dotted leader to the element's left edge. The
log marks it `"adjacent": false`.

## Gutter layout

`"layout": "gutter"` replaces the placement above, only under SKILL.md hard rule 7.

- The canvas grows a column on each side of the design, as wide as the widest label plus padding,
  and a clear run of `LEADER_RUN` between that column and the design.
- Every label uses the digit font at `text_px`, dotted labels included. The pill hugs the label:
  radius `GUTTER_R_FRAC` times the font size.
- Side: as in SKILL.md Input config (`side`).
- Anchor: a container's top corner on its side; any other element's edge on its side, at its
  vertical middle, or near its top when it is taller than four badge radii. `narrow` moves the
  anchor in to the visible content, as it moves the slots. `"anchor": "top"` puts the dot on the
  middle of the element's top edge instead: set it on small icons that sit side by side, where an
  edge dot falls in the gap between two of them. A centre dot is not offered.
- Each column stacks its labels in anchor order, one badge height plus `ADJ_GAP` apart, pushed down
  only as far as the one above requires. The log reports each label's `shift` from its anchor and
  the largest as `max_shift`.
- The leader runs straight out of the pill to the column edge, then to a dot on the anchor.

## The `narrow` flag

`narrow: true` narrows the assumed content span to the middle `NARROW_FRAC` (50%) of the bbox,
which moves the `left` and `right` slots inward. There is no per item override of the fraction.
When to set it: SKILL.md flag table.

## Reading order

Badges are drawn in config order (`No` order) but **positioned** by size, so placement order and
reading order differ.

## Badge size

`badge_scale` sets one factor before anything measures or draws: the badge diameter divided by its
base of 28 px. The diameter is 28 x `text_px` / `TEXT_PX_BASE` (13), or `BADGE_DEFAULT_FRAC` (2.7%)
of the image's longer edge without `text_px`, then clamped to `badge_range` (`BADGE_RANGE`,
1.8% to 4.5%) of that edge and to `BADGE_MIN_PX` (20 px). `apply_text_scale` multiplies margin,
radius, pill padding, gaps, separation, both fonts, dash lengths and stroke width by that factor.

## Style constants

Values at `text_px` 13, before the rescale.

| Element | Style |
| --- | --- |
| Badge | Red fill `#FF3B30`, 2 px white border, white bold label |
| Leader | Default layout: dotted, `#FF3B30` at 230 alpha, 1 px, only on a displaced badge. Gutter layout: solid, at least 2 px, on every badge |
| Container outline | Dashed red rectangle, 1 px, 6 px dash and 4 px gap |
| Margin | 38 px on all four sides (`MARGIN`) |
| Element gap | 5 px between the element edge and the badge rim (`ADJ_GAP`) |
| Badge separation | 33 px centre to centre (`MIN_SEP`) |
| Bounds slack | 2 px a bbox may sit outside the image before the guard refuses (`BOUNDS_TOL`) |
| Aspect slack | 2% the two `design_size` axes may disagree with the PNG (`ASPECT_TOL`) |

## Known limitations

- **Placement is greedy:** the first free slot wins, so a dense cluster can push a later item to `below`.
- **A badge may sit over neighbouring content:** see SKILL.md Process step 7.

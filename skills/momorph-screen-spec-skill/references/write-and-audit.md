# Uploading, auditing and recovering

Reference for `momorph-screen-spec-skill`.

## Matching a file row: `UI Parts`, then `No`

`No` decides only when `UI Parts` is blank or matches nothing; the two keys are never combined
with AND. "Matches" means the target screen has an **active** item carrying exactly that value.
Archived and deleted items are never candidates. Read from row 1 and stop at the first row that
applies. The table runs only on rows that passed §Layer rules and the refusal of a row whose
`UI Parts` and `No` name two different active items (`csv-columns.md` §File limits).

| # | `UI Parts` of the row | `No` of the row | Target item |
| :-: | --- | --- | --- |
| 1 | Malformed | Any | None: the row is refused, never matched by `No` |
| 2 | Matches 1 item | Any | The item matched by `UI Parts` |
| 3 | Blank, or matches nothing | Matches 2 or more items | None: the row is refused |
| 4 | Blank | Matches 1 item | The item matched by `No`, its layer link kept |
| 5 | A value matching nothing | Matches 1 item with no layer link | The item matched by `No`, now linked to the row's layer |
| 6 | A value matching nothing | Matches 1 item that already has a layer link | None: a new item carrying the row's `UI Parts` |
| 7 | Blank, or matches nothing | Blank, or matches nothing | None: a new item |

`Active status` sets only the lifecycle of the target item. A row with no target creates an item
when `active`, and is skipped when `archived` or `deleted`.

Import never restores an item; restore is the plugin's Archived tab only.

## Layer rules

- One Figma layer belongs to at most one active item.
- A layer held by an active item of **another screen** in the same Figma file is refused, on the
  plugin path and the MCP path. The check applies only when both screens link a design frame. An
  archived item has released its layer.
- Plugin Import only: a `UI Parts` layer sits inside the design frame linked to the target screen,
  is not that frame, and does not carry a name inherited from the main component of an instance.
  On a screen with no frame, every row carrying `UI Parts` is refused.
- A spec-linked layer is named `mms_<name>`. The MCP path cannot rename a layer, so the link it
  creates is marked and the next plugin sync adds the prefix. A link without the prefix and without
  the mark is removed at the next sync; relink it from the plugin or through `upload_screen_spec`.

## Write paths

| Path | Source | Mechanism | New layer link |
| --- | --- | --- | --- |
| Plugin Import | file | Replace | Yes. Renames each newly linked layer to `mms_<name>` after the user confirms |
| CLI `momorph spec import <file> --screen <ref>`, or `POST /api/v1/projects/:projectId/figma-frames/:ref/spec-import` | file | Replace | Never. An `active` row whose `UI Parts` no active item of this screen holds refuses the file |
| MCP `upload_screen_spec(items)` | item list | Upsert | Yes, for an item it creates on a Figma-backed screen |

**Replace, any file path.**

- The file is the screen's final state. A matched row overwrites the content columns of its item.
  An unmatched `active` row creates an item.
- Every active item the file omits moves to `archived`, keeping its `No` and `UI Parts`.
- Display order follows the row order. Nothing is hard deleted.
- The whole file goes in one call.
- The CLI and the route refuse a 10-character screen id that names no screen.
- The response reports the created, updated and archived counts, whether the screen was created,
  and each archived item with its `No` and name.

**Upsert, MCP `items`.**

- Only the items sent change. Every other item keeps its content and lifecycle.
- Each item is keyed by `id`, from `download_screen_spec(format="json")` or `list_screen_items`.
  For a linked item it is the layer's Figma node id.
- An `id` no item of this screen holds, in any lifecycle, creates an item. On a screen backed by a
  real Figma file that `id` becomes the layer link, so use the layer's node id.
- An `id` starting with `row_` or `inactive_` is reserved: nothing is created, it comes back in
  `skipped`.
- An `id` held by an archived or deleted item is skipped, `lifecycle: "active"` included.
- To remove an item, send its `id` with `lifecycle: "archived"` or `"deleted"`.
- `position` is written on create and on update: omit it unless the item moves.
- Omitting `specs` leaves the content untouched. An unknown field inside `specs` refuses the
  request.
- A repeated `no` among the active items, or two items with one `id`, refuses the whole request.
- At most **100 items per call**. A refused request writes nothing.

## Reading the upload response

`upload_screen_spec` reports the created count, the updated count, and each skipped item with its
reason. It lists no item that left the active set and does not flag a new screen. Compare the
skipped list with what you sent.

- **`boardSync: "failed"`**: the data was written, the canvas mirror was not. Retry the upload.
- **`boardSync: "skipped"`**: the data was written, the canvas mirror was withheld. Re-sync the screen's design items from the Figma plugin, then
  upload again.

## EXIST branch

- Re-run identification instead of reusing the prior linking.
- Audit each item for rename, removal and relink.
- Address a change to an existing item by the baseline keys (`csv-columns.md` §`No` and
  `UI Parts` cells), or by the `id` of the JSON download (`items`). A change that landed on a new
  item instead: archive that item, then resend with the right key.
- A removed item gets `Active status` `archived` or `deleted` on its own row, or is left out of a
  Replace file.
- Keep the baseline's row order and `No` scheme, gaps included. Do not reformat an unchanged row.

## Gotchas

- **`unreadable: true`**: the item's content was not fetched; the item is not empty. With
  `include_archived_deleted=true`, every item past the 500th (active, then archived, then deleted)
  comes back this way, and `format="csv"` is refused for that screen. Export the active items only.
- **`Destination` does not round-trip.** Export writes the linked frame's name or the external
  link. Import reads the cell back as an external link only. Never turn a frame name into a link
  id.
- **Screen status** is set through `meta` of `upload_screen_spec` and read from `list_screens`.

## screen-overview.md (≤ 10 lines)

Also the body for `create_screen`'s `screenOverview`.

```
- Role: <one-sentence functional summary>
- Initial state / loading: <first-load behavior>
- Key interactions: <2 or 3 dominant flows>
- State variants: <Default / No UI / In Progress / Done / etc.>
- Cross-references: <related screens / sub-spec sheets>
- Caveats: <gotchas for dev/QA>
```

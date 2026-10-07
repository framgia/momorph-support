# Screen-spec CSV: the v2 default template and file limits

Reference for `momorph-screen-spec-skill`. A rule below applies to a column only when the
downloaded header carries that column by that name.

## The v2 default columns

```
No, Item Name, UI Parts, Item Type, Description, Trigger, Destination, Interaction Note,
Data Type, Required, Format, Max Length, Min Length, Default Value, Validation Note,
Table Name, Column Name, Database Note, Active status
```

- Column order is free on import; export writes the order of the template.
- A legacy `Status` column is accepted on import and ignored. Never write it.
- Export writes UTF-8 **with BOM** and **CRLF** endings. Both directions use commas and RFC 4180
  quoting.

| # | Column | Writes to | Limit / vocabulary |
| --: | --- | --- | --- |
| 1 | `No` | the item's number | ≤ 10 chars. Levels joined by `.` (`1.2.3`). Unique within the file and among the screen's active items. Several blanks allowed. Second matching key |
| 2 | `Item Name` | `specs.item.name` | ≤ 255. Duplicates allowed |
| 3 | `UI Parts` | the linked layer | The layer's Figma node id. Unique within the file. First matching key |
| 4 | `Item Type` | `type` | Free text ≤ 255. 13 suggestions |
| 5 | `Description` | `specs.description` | Markdown ≤ 10000 |
| 6 | `Trigger` | `specs.navigation.action` | Free text ≤ 255. 4 suggestions |
| 7 | `Destination` | `specs.navigation` | ≤ 2000. A target screen of the project, or an external URL, not both |
| 8 | `Interaction Note` | `specs.navigation.note` | Markdown ≤ 10000 |
| 9 | `Data Type` | `specs.validation.dataType` | Free text ≤ 255. 12 suggestions |
| 10 | `Required` | `specs.validation.required` | Free text ≤ 255. 2 suggestions |
| 11 | `Format` | `specs.validation.format` | ≤ 255 |
| 12 | `Max Length` | `specs.validation.maxLength` | Integer ≥ 0 |
| 13 | `Min Length` | `specs.validation.minLength` | Integer ≥ 0, not greater than `Max Length` |
| 14 | `Default Value` | `specs.validation.defaultValue` | ≤ 255 |
| 15 | `Validation Note` | `specs.validation.note` | Markdown ≤ 10000 |
| 16 | `Table Name` | `specs.database.tableName` | ≤ 255 |
| 17 | `Column Name` | `specs.database.columnName` | ≤ 255 |
| 18 | `Database Note` | `specs.database.note` | Markdown ≤ 10000 |
| 19 | `Active status` | the item's lifecycle | `active` / `archived` / `deleted`, case insensitive. Blank reads as `active`. Not shown on the plugin's spec table |

Suggestion vocabularies. A value outside a list is accepted; use one only when no suggestion fits.

- **Item Type:** `button` `checkbox` `date_picker` `dropdown` `file_or_image` `label` `others`
  `pagination` `popup_dialog` `radio_button` `text_form` `textarea` `video`
- **Trigger:** `after_delay` `key_gamepad` `on_click` `while_hovering`
- **Data Type:** `array` `boolean` `byte` `character` `date` `double` `float` `integer` `long`
  `nothing` `short` `string`
- **Required:** `Required` `Optional`. Any casing is stored in the canonical one.

## `No` and `UI Parts` cells, by row kind

- **Existing item**: copy both values from the downloaded file, character for character.
- **Renumbering a linked item**: keep `UI Parts`, change `No`. The new `No` must belong to no other
  active item.
- **Renumbering an unlinked item**: through `upload_screen_spec(items)` only. In a file, a new
  `No` on a row without `UI Parts` creates a new item and Replace archives the old one.
- **New item**: a `No` no active item carries. `UI Parts` only on a write path that may create a
  layer link (`write-and-audit.md`).

## File limits

The whole file is refused, with no partial import, on any of:

- 5 MB or more, or more than 500 data rows.
- Malformed CSV: an unclosed quote, or a row with more cells than the header.
- A header that differs from the template: a column missing, extra or renamed.
- One invalid cell anywhere, a malformed `UI Parts` included.
- One `No`, or one `UI Parts`, on two rows.
- A row whose `UI Parts` and `No` name two different active items.
- A `No` held by two active items once the file applies.
- An `active` row empty of everything except `Active status`.

A row whose every cell is blank is skipped: neither an item nor an error.

## Cell writing style

- `Description`, `Interaction Note`, `Validation Note` and `Database Note` are raw markdown; the
  rest is plain text.
- One idea per cell. `Description` states role, visual cue and state. An interaction reads
  `trigger → result → side effects`.
- A cell opening with `=` `+` `-` `@`, a tab or a CR gets a leading single quote on export. Do not
  add that quote yourself.
- Written register. A cell states behaviour and rules, no commentary. A reason is written only
  when it is itself a verifiable fact.
- A cell names the object it governs.
- Technical terms stay English. A field, function or endpoint is spelled as the code spells it.
- VI: no `A thì B`; write `Khi A, B` or split the sentence. `・` never enumerates: separate with
  `,`, or use a nested list inside a markdown cell.
- JA: no space between Latin and Japanese characters (`Figmaファイル`). The native word over a
  katakana loanword when one exists (`画面`, not `スクリーン`).

## Blank cells

A blank cell needs the user's decision (`SKILL.md` step 5), except these two:

- `Trigger` and `Interaction Note` of a container, divider or static label: there is no
  interaction. Never write "không có tương tác" there.
- `UI Parts` of a row with no linked layer.

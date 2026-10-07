# Content JSON for fill_spec.py

One JSON object per screen. Every key is optional; an absent key leaves its area empty. Content
the template has no place for is not written and is listed in `skipped` on stdout. A full
example is [`sample-content.json`](sample-content.json). Dates are `YYYY-MM-DD` strings and become
real dates in the sheet.

| Key | Fills | Fields |
| --- | --- | --- |
| `meta` | Rows 2 to 4 | `screen_name`, `overview`, `status` (`作成中` / `確定`), `design_ref`, `design_confirmed`, and `created` / `updated` / `reviewed` as `{ "date", "by" }` |
| `revisions` | Sheet 改訂履歴 | `version`, `date`, `by`, `where`, `what` |
| `items` | 項目定義 | `no`, `name`, `label`, `type`, `description`, `trigger`, `destination`, `behavior`, `data_type`, `required`, `format`, `max`, `min`, `default`, `validation`, `table`, `column`, `db_note`, `new_db`, `extra` |
| `rules` | 表示・業務ルール | `id`, `target`, `rule` |
| `states` | 状態定義 | `target`, `state`, `condition`, `behavior` |
| `errors` | エラー処理 | `no`, `target`, `case`, `condition`, `behavior`, `message_id`, `note` |
| `messages` | メッセージ一覧 | `id`, `type`, `text` (表示メッセージ), `display`, `note` |
| `open_questions` | 未決事項 | `no`, `target`, `question`, `decision`, `decided_by`, `date`, `status` (`未回答` / `回答済み`) |

Notes:

- `items[].new_db: true` writes `table`, `column` and `db_note` in red.
- `behavior` separates its lines with `\n`.
- `extra` is an object `{header: value}` for columns outside the keys above, in any row of any
  table, for example `"extra": {"備考": "..."}`.
- A table holds only the blank rows the template gives it (default: 40 items, 15 rules, 15 states,
  10 errors, 15 messages, 15 open questions, 20 revisions). More rows than that stop the script
  with an error and write nothing; raise the count in `layout.json` and rebuild the template.

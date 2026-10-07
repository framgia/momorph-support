# Quality checklist before delivery

Reference for `screen-detail-spec-excel`, step 9 (Gate 2). Reopen the filled file and check every
line. A failed line is fixed before delivery, never reported as a known issue.

## Completeness

- [ ] Every component in the image has a row in 項目定義, and every row has a number in the image.
- [ ] Every inventory rule of research-and-evidence.md §4 holds in the sheet.
- [ ] Every request the screen sends has an エラー処理 row.

## Traceability

- [ ] Every row of 項目定義, 表示・業務ルール and 状態定義 has a source of rank 1 to 6 in the evidence
  map (research-and-evidence.md §2).
- [ ] Every 未決事項 row, and every cell that depends on one, follows question-protocol.md §4.

## Consistency

- [ ] Every message ID cited exists in メッセージ一覧, and every message is cited at least once.
- [ ] Every rule ID cited exists in 表示・業務ルール.
- [ ] 画面上表示ラベル and 表示メッセージ match the UI text catalog character for character.
- [ ] Every writing rule in SKILL.md holds in every cell.

## File

- [ ] Metadata rows filled: 画面名, 画面概要, ステータス, デザイン参照, dates and people.
- [ ] 改訂履歴 has a row for this version.
- [ ] No text is cut by a row height: reopen and check the longest cells.
- [ ] `skipped` in the output of `fill_spec.py` is empty, or each entry is reported to the spec writer.

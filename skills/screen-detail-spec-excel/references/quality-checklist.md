# Quality checklist before delivery

Reference for `screen-detail-spec-excel`, step 9 (Gate 2). Reopen the filled file and check every
line. A failed line is fixed before delivery, never reported as a known issue.

## Completeness

- [ ] Every component in the image has a row in 項目定義, and every row has a number in the image.
- [ ] Every overlay and state named in the design has a row or a 状態定義 entry.
- [ ] Every input has data type, 必須, limits and 入力チェック, or `N/A` with a reason in the evidence map.
- [ ] Every interactive item has 操作 and 操作時の動作, including its disabled behaviour.
- [ ] Every list has its order, count, empty, loading and error states.
- [ ] Every request the screen sends has an エラー処理 row.

## Traceability

- [ ] Every row of 項目定義, 表示・業務ルール and 状態定義 has a source in the evidence map.
- [ ] Every value in the sheet traces to a source of rank 1 to 6, never to inference.
- [ ] Every default taken is in 未決事項 as `回答済み` with the person who accepted it.
- [ ] Every cell that depends on an open question cites its 未決事項 number.

## Consistency

- [ ] Every message ID cited exists in メッセージ一覧, and every message is cited at least once.
- [ ] Every rule ID cited exists in 表示・業務ルール.
- [ ] 画面上表示ラベル and 表示メッセージ match the UI text catalog character for character.
- [ ] Table and column names match the data model exactly; every new field is red with `新規追加：`.
- [ ] The same concept carries the same name in every cell, matching the glossary.
- [ ] No fact appears in two places.

## Language

- [ ] Japanese only, 表示メッセージ included.
- [ ] No dash in prose, no space between Latin and Japanese, `・` only between nouns or as a bullet.
- [ ] Every rule is verifiable: literal numbers, no `適宜`, `など`, `場合がある`.

## File

- [ ] Metadata rows filled: 画面名, 画面概要, ステータス, デザイン参照, dates and people.
- [ ] 改訂履歴 has a row for this version.
- [ ] No text is cut by a row height: reopen and check the longest cells.
- [ ] The numbered image PNG sits next to the Excel file, with the same numbers as 項目定義.

---
name: screen-detail-spec-excel
description: "Writes a Japanese screen detail design document (画面詳細設計書) as an Excel file for ONE screen: metadata, a numbered screen image on the left, and on the right the item definitions (項目定義), display and business rules, states, permissions, error handling, messages and open questions, filled from a fixed template. Works from a Figma frame or a screenshot, researches the product overview, the database model and the UI text catalog before writing, and asks the user every question it cannot settle before writing a single cell. Use when the user says \"画面詳細設計書\", \"screen detail spec\", \"spec màn hình bằng Excel\", \"viết spec màn vào Excel\", \"Excelで画面仕様\", or hands over a screen and asks for a spec in the Excel template. Do NOT use for a markdown feature spec, or for a spec stored as CSV in a tool."
argument-hint: "[figma-url | path/to/screenshot.png] [output folder]"
compatibility: "Python 3 with openpyxl. Figma MCP for a Figma source. The numbered image comes from the companion skill numbered-image-skill, which needs Pillow."
metadata:
  version: '1.0.0'
---

# Screen detail spec in Excel (画面詳細設計書)

Produces one `.xlsx` per screen from [`assets/screen-detail-spec-template.xlsx`](assets/screen-detail-spec-template.xlsx),
plus the numbered screen image as a separate PNG. The content is Japanese.

## Workflow

1. **Get the screen.** Figma: `get_screenshot` at the frame's own size and `get_metadata` for the
   layer tree. Screenshot: the user's file. Read the body text style of the screen
   (`get_design_context`, or measure it on the image): the numbered image needs its size.
2. **Collect the material before writing.** Ask the user where the project keeps these, then read
   them and keep the file and line of every fact:
   - the product overview and the feature spec of this screen;
   - the database model: table and column names for every field the screen shows or edits;
   - the UI text catalog (i18n files) for every label and message, in each language.
3. **List the items** the screen defines, numbered hierarchically: a container `n`, its children
   `n.m`. One component, one number. Overlays that are not in the image (menu, modal, sheet) still
   get numbers and point to their design frame in `説明`.
4. **Ask before writing.** Collect every point the material does not settle (a behaviour no source
   states, a conflict between design and spec, a missing text, a missing DB field) and ask the user
   in one round. Write a default only when it is one clause that can change later without changing
   the shape of the screen, and list every such default in the reply. Never invent a value.
5. **Number the image** with numbered-image-skill. Numbers use the screen's body text size; put them
   outside the image only when the elements are too close for a number beside them. Save the PNG
   next to the Excel file. The user pastes it into the 画面イメージ area unless asked otherwise.
6. **Write the content JSON** in the format of
   [`references/content-format.md`](references/content-format.md), following the writing rules below.
7. **Fill the template:**
   ```sh
   python3 scripts/fill_spec.py assets/screen-detail-spec-template.xlsx content.json 画面詳細設計書_<画面名>_<YYYYMMDD>.xlsx
   ```
8. **Verify and report.** Reopen the file, check that every section landed and no text is cut.
   Report the output paths, the defaults taken, the open questions written to 未決事項, and every
   point where the design and the spec disagree.

## The template

| Area | Content |
| --- | --- |
| Sheet 改訂履歴 | 版, 改訂日, 改訂者, 改訂箇所, 改訂内容 |
| Rows 2 to 4 | 画面名, ステータス (作成中 / 確定), デザイン参照, 画面概要, 作成日・作成者, 最終更新, レビュー, デザイン確認 |
| Left column | 画面イメージ: the numbered image |
| 項目定義 | No, 項目名, 画面上表示ラベル, 項目種別, 説明, 操作, 遷移先, 操作時の動作, データ型, 必須, 形式, 最大桁数, 最小桁数, 初期値, 入力チェック, テーブル名, カラム名, データベース備考, 出典 |
| Tables below | 表示・業務ルール, 状態定義, 権限, エラー処理, メッセージ一覧, 未決事項 |

`scripts/build_template.py <out.xlsx>` rebuilds the template; edit its column lists to customise it.
`fill_spec.py` finds every table by its title and header text, so a rebuilt template still fills.

## Writing rules for the content

- **Pure Japanese**, including notes. UI text quotes keep the source language of the catalog.
- **Written, verifiable sentences**: `〜する`, `〜しない`. State the rule, not the reason. Numbers are
  literal: limits, durations, sizes.
- **No dashes in prose** (`—`, `–`, `－`, a hyphen joining words). Use `：`, `、`, `。`, or a list.
- **No space between Latin and Japanese characters** (`Figmaファイル`). Prefer the native word over a
  katakana loanword (`画面`, not `スクリーン`). `・` only joins parallel nouns, and starts a bullet
  inside `操作時の動作`.
- **Behaviour, not appearance.** Describe a visual only where a rule turns on it. Link the design
  in `デザイン参照` instead of describing it.
- **Database columns** use the exact table and column names of the model. A field the model does
  not have yet is written in red (`"new_db": true`) and its `データベース備考` starts with
  `新規追加：` and the reason.
- **Blank means not applicable.** Anything undecided goes to 未決事項 with a number, never into a
  cell as a guess.
- **One fact, one place.** A rule lives in 表示・業務ルール or in the item, not both; messages live
  in メッセージ一覧 and items cite their ID.

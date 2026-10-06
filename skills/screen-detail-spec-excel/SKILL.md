---
name: screen-detail-spec-excel
description: "Writes a Japanese screen detail design document (画面詳細設計書) as an Excel file for ONE screen, from a fixed template: metadata, a numbered screen image on the left, and on the right the item definitions (項目定義), display and business rules, states, error handling, messages and open questions. Every cell is traced to a source, and every point the sources do not settle is asked to the spec writer before anything is written. Works from a Figma frame or a screenshot. Use when the user says \"画面詳細設計書\", \"screen detail spec\", \"spec màn hình bằng Excel\", \"viết spec màn vào Excel\", \"Excelで画面仕様\", or hands over a screen and asks for a spec in the Excel template. Do NOT use for a markdown feature spec, or for a spec stored as CSV in a tool."
argument-hint: "[figma-url | path/to/screenshot.png] [output folder]"
compatibility: "Python 3 with openpyxl. Figma MCP for a Figma source. The numbered image comes from the companion skill numbered-image-skill, which needs Pillow."
metadata:
  version: '2.0.0'
---

# Screen detail spec in Excel (画面詳細設計書)

Produces one `.xlsx` per screen from [`assets/screen-detail-spec-template.xlsx`](assets/screen-detail-spec-template.xlsx),
plus the numbered screen image as a separate PNG. The content is Japanese.

**The standard is a spec a developer can build from and a QA can test from without asking anyone.**
Two things get there: every cell rests on a source, and every gap is closed by the spec writer
before writing, not filled by a guess. A wrong cell that reads like a fact is the worst outcome
this skill can produce; a gap asked about is never a failure.

## Workflow and gates

Work in this order. A gate is a hard stop: do not move past it until its condition holds.

1. **Frame the task.** Confirm the screen, its scope (which states and overlays belong to this
   document), the output folder, and the language of the UI text source. One short question round
   when any of these is missing.
2. **Learn the project before the screen.** Read [`references/research-and-evidence.md`](references/research-and-evidence.md)
   and collect the project context: glossary, an existing spec to mirror its terms and depth, the
   requirements or feature spec of this screen, the data model, the UI text catalog. Ask where they
   live; never assume they do not exist.
3. **Inventory the screen.** Get the image and the layer tree (Figma `get_screenshot`,
   `get_metadata`, and the body text style from `get_design_context`), or the user's screenshot.
   List every component, including hidden states and overlays, and number them hierarchically: a
   container `n`, its children `n.m`; one component, one number.
4. **Build the evidence map.** For every item and every template column, record the value and its
   source, or mark it unknown. Record every conflict between sources. Nothing is written to the
   sheet yet.
5. **Gate 1, readiness.** Run [`references/question-protocol.md`](references/question-protocol.md):
   classify every unknown and conflict, then ask the spec writer **one** consolidated round of
   questions, blocking ones first, each with context, options and a recommended answer. **Stop
   and wait for the answers.** Ask again only what the answers left open.
6. **Number the image** with numbered-image-skill. Numbers use the screen's body text size and move
   outside the image only when the elements are too close. Save the PNG next to the Excel file; the
   spec writer pastes it into the 画面イメージ area unless asked otherwise.
7. **Write the content JSON** ([`references/content-format.md`](references/content-format.md)) from the
   evidence map and the answers, following the writing rules below. Sources stay in the evidence map,
   not in the sheet. Answered questions go to 未決事項 as `回答済み` with the decision, the person and the date;
   questions the writer chose to leave open stay `未回答`.
8. **Fill the template:**
   ```sh
   python3 scripts/fill_spec.py assets/screen-detail-spec-template.xlsx content.json 画面詳細設計書_<画面名>_<YYYYMMDD>.xlsx
   ```
9. **Gate 2, quality.** Run [`references/quality-checklist.md`](references/quality-checklist.md) on the
   file. Fix every failure before delivering.
10. **Report.** Output paths; the defaults taken and who confirmed them; the questions still open;
    every conflict between design and spec and how it was settled; the source of each item from the
    evidence map, for the reviewer.

## The template

| Area | Content |
| --- | --- |
| Sheet 改訂履歴 | 版, 改訂日, 改訂者, 改訂箇所, 改訂内容 |
| Rows 2 to 4 | 画面名, ステータス (作成中 / 確定), デザイン参照, 画面概要, 作成日・作成者, 最終更新, レビュー, デザイン確認 |
| Left column | 画面イメージ: the numbered image |
| 項目定義 | No, 項目名, 画面上表示ラベル, 項目種別, 説明, 操作, 遷移先, 操作時の動作, データ型, 必須, 形式, 最大桁数, 最小桁数, 初期値, 入力チェック, テーブル名, カラム名, データベース備考 |
| Tables below | 表示・業務ルール, 状態定義, エラー処理, メッセージ一覧, 未決事項 |

`scripts/build_template.py <out.xlsx>` rebuilds the template; edit its column lists to customise it.
`fill_spec.py` finds every table by its title and header text, so a rebuilt template still fills.
When the project hands over its own template, inspect it first and map the JSON keys to its
headers before writing.

## Writing rules for the content

- **Pure Japanese**, including notes and 表示メッセージ.
- **Written, verifiable sentences**: `〜する`, `〜しない`. State the rule, not the reason. Numbers are
  literal: limits, durations, sizes, counts. Never `適宜`, `など`, `場合がある` in a rule.
- **One behaviour per line** in `操作時の動作`: trigger, result, then side effects, each line starting
  with `・`.
- **No dashes in prose** (`—`, `–`, `－`, a hyphen joining words). Use `：`, `、`, `。`, or a list.
- **No space between Latin and Japanese characters** (`Figmaファイル`). Prefer the native word over a
  katakana loanword (`画面`, not `スクリーン`). `・` only joins parallel nouns or starts a bullet.
- **The project's own terms.** Use the glossary and the existing specs' wording for every concept;
  never coin a second name for something the project already names.
- **Behaviour, not appearance.** Describe a visual only where a rule turns on it. Link the design in
  `デザイン参照` instead of describing it.
- **Database columns** use the exact table and column names of the model. A field the model does
  not have yet is written in red (`"new_db": true`) and its `データベース備考` starts with
  `新規追加：` and the reason.
- **Blank means not applicable.** Anything undecided goes to 未決事項 with a number and the item
  cites it; never a guess in a cell.
- **One fact, one place.** A rule lives in 表示・業務ルール or in the item, not both; messages live in
  メッセージ一覧 and items cite their ID.

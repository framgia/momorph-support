# Question protocol: readiness before writing

Reference for `screen-detail-spec-excel`, step 5 (Gate 1). The spec writer answers before a cell is
written.

## 1. Classify every unknown and conflict

Apply one test to each:

**Could the screen be built under a proposed default, and would changing that default later alter
one cell rather than the shape of the screen?**

| Class | When | What to do |
| --- | --- | --- |
| **Blocking** | No to the test: it decides a flow, a state, a data field, the scope, or what the user sees | Ask. Do not write the affected section until it is answered |
| **Default** | Yes to the test: a limit, a label, a duration, a sort order | Propose the default in the question; write it only after the writer accepts it (§4) |
| **Conflict** | Two sources disagree and the ranking cannot settle it (research-and-evidence.md §2) | Ask which wins, showing both values and both sources |
| **Not a question** | The material answers it, but it was not read yet | Go back and read it. Never ask the writer what a document already says |

## 2. Ask in one round

- **One consolidated message**, grouped by class: Blocking, then Conflict, then Default.
- Each question names the item number and the column it decides, gives the context in one line,
  offers two to four options, and marks one as recommended with its reason as a verifiable fact.
- Keep each question answerable with a choice or a number. Split a compound question.
- Number the questions; the numbers carry over into 未決事項.
- After the answers, ask a second round only for what is still open, and only once. What remains
  open after that is recorded per §4.

Template for one question:

```
Q3 [Blocking] 4.2 検索欄：入力チェック
Context: the design shows a search field; no source gives a maximum length.
Options: (a) 100文字 (recommended: the DB column is VARCHAR(100)) (b) 255文字 (c) no limit
```

## 3. Question bank by template section

Run through these for every item. Skip a line only when the evidence map already answers it.

**画面全体**
- Who reaches this screen, from which screen, and with which data already loaded?
- What does the screen show on first load, and in what order are the parts fetched?

**項目定義**
- Label: the exact text and its key in the catalog; behaviour when the text is too long.
- Input: data type, required or optional, minimum and maximum length, format, default value,
  allowed characters, when validation runs (on input, on blur, on submit).
- Action: trigger, result, destination, side effects, and behaviour while a request is running.
- Disabled: under which condition, and whether it shows a reason.
- Data: the table and column it reads or writes; a field not in the model is a new field to confirm.

**表示・業務ルール**
- Sort order and its tie breaker; grouping; count shown and what it includes.
- Limits: maximum number of items, file sizes, rate limits, time windows.
- What happens to the screen when data changes elsewhere while it is open.

**状態定義**
- Empty, loading, error, partial data, disabled, selected, hover, focus, long text, many items.
- For each: the condition, what is shown, and what the user can still do.

**エラー処理**
- Every request the screen sends: what fails, after how long it times out, what the user sees, and
  whether data entered is kept.
- Server validation errors and their codes; concurrent edit; lost connection.

**メッセージ一覧**
- Exact Japanese text, the type (error, warning, info, confirm,
  done), where it shows, and how it closes.

## 4. Record the outcome

| Outcome | 未決事項 row |
| --- | --- |
| Answered | `回答済み`, 決定内容, 決定者, 決定日 |
| Default accepted | `回答済み`, the default, "提案を採用", 決定者, 決定日 |
| Left open by the writer | `未回答`; every cell it governs cites the row number |

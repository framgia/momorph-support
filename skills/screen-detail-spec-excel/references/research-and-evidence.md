# Research and evidence

Reference for `screen-detail-spec-excel`, steps 2 to 4.

## 1. Project context to collect first

Ask the spec writer where each of these lives; never assume one does not exist. A missing one is
itself a finding to report.

| Material | What it gives the spec | What to extract |
| --- | --- | --- |
| Glossary or domain terms | The words every cell must use | Term, meaning, the name the UI shows |
| An existing approved spec of the same project | Depth, wording, naming of screens and states | How states, errors and messages are phrased; the numbering style |
| Requirements or feature spec of this screen | Behaviour and rules | Every rule, limit, condition; the scope boundary |
| Design (Figma) | Components, states, overlays, labels | Every frame of the screen, every variant (hover, disabled, error, empty, loading) |
| Data model (DB schema, ER, migrations) | `テーブル名`, `カラム名`, data types, lengths | Exact names, types, nullability, length limits, defaults |
| UI text catalog (i18n files) | Labels and messages | The exact Japanese strings and their keys |
| API contract | Validation done by the server, error codes | Field limits, error responses the screen must handle |
| Existing implementation, when the screen exists | Current behaviour | Only as evidence of today's behaviour, never as the target |

## 2. Source ranking

When two sources say different things, the higher one wins: write its value and list the conflict
in the report, with both values and both sources. Ask the spec writer instead (question-protocol.md
§1, Conflict) in two cases only:

- the two sources sit at the same rank;
- the lower ranked source carries a later date than the higher one (a design revised after the
  approved spec).

Ranks 3 to 5 each win only on the aspect named; on any other aspect they rank below 2.


1. A decision the spec writer confirmed in this session.
2. The approved requirements or feature spec.
3. The design, for what is shown and in which state.
4. The data model and the API contract, for names, types and limits.
5. The UI text catalog, for exact wording.
6. The existing implementation, as evidence of current behaviour only.
7. Inference. **Never written to the sheet as a fact.** It becomes a question or a proposed default.

## 3. Evidence map

Keep it as a working table before writing anything. One row per item, one column per template
column, each cell holding one of:

- `value` + `source` (file and line, Figma node, or "confirmed by <name> on <date>");
- `unknown` + why;
- `conflict` + the two sources and their values;
- `N/A` + why it does not apply.

The map is complete when no cell is empty. Its unknowns and conflicts are the input to the
question protocol.

## 4. Inventory rules

- Walk every frame and variant of the screen, not only the default state. A state seen only in a
  variant is still a requirement.
- An overlay (menu, modal, sheet, toast) is an item even when it is not in the main image; its row
  points to its design frame in `説明`.
- Text the user can type gets a data type, required flag, limits and validation. Text the user
  only reads gets its source (DB column or fixed label) and its truncation rule.
- Every interactive item gets its trigger, its result and its side effects, and its behaviour when
  disabled.
- Every list gets its order, its count rule, its empty state, its loading state and its error state.

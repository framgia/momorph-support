# Screen spec skills for Claude Code

Two Claude Code skills for writing a screen specification:

| Skill | Produces |
| --- | --- |
| [`screen-detail-spec-excel`](screen-detail-spec-excel/SKILL.md) | A Japanese screen detail design document (画面詳細設計書) as Excel: metadata, item definitions, rules, states, permissions, errors, messages and open questions, from a fixed template |
| [`numbered-image-skill`](numbered-image-skill/SKILL.md) | A PNG of the screen with a number on every component, from a Figma frame or a screenshot |

The two work together: the Excel spec cites each item by the number the image shows.

## Install

From the root of this repository, copy both folders into your skills directory:

```sh
cp -R skills/screen-detail-spec-excel skills/numbered-image-skill ~/.claude/skills/
```

Use `.claude/skills/` inside a project instead to share them with that project's team only.

## Requirements

- Python 3 with `openpyxl` (Excel) and `Pillow` (image).
- Figma MCP server, when the source is a Figma frame. A screenshot needs no Figma access.

## Usage

Ask Claude Code, for example:

- 「このFigmaフレームの画面詳細設計書を作成して」 with a Figma frame URL.
- "Tạo ảnh đánh số cho màn này" with a screenshot.

The spec skill asks every open question before it writes, and writes undecided points to the
未決事項 table instead of guessing.

## Customise

- Template columns and tables: edit and run `screen-detail-spec-excel/scripts/build_template.py`.
- Number placement and style: constants at the top of `numbered-image-skill/render_badges.py`, documented
  in `numbered-image-skill/references/renderer.md`.

#!/usr/bin/env python3
"""Fill the 画面詳細設計書 template from a JSON content file.

Usage: python3 fill_spec.py <template.xlsx> <content.json> <out.xlsx>

The tables are located by their Japanese titles and header cells, so a template whose rows were
moved still fills correctly. The JSON format is described in references/content-format.md.
"""
import datetime
import json
import math
import sys
import unicodedata

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

WRAP = Alignment(wrap_text=True, vertical="top")
RED = "FF0000"

# JSON key -> header text, per table.
ITEM_COLS = {
    "no": "No", "name": "項目名", "label": "画面上表示ラベル", "type": "項目種別", "description": "説明",
    "trigger": "操作", "destination": "遷移先", "behavior": "操作時の動作", "data_type": "データ型",
    "required": "必須", "format": "形式", "max": "最大桁数", "min": "最小桁数", "default": "初期値",
    "validation": "入力チェック", "table": "テーブル名", "column": "カラム名", "db_note": "データベース備考",
}
TABLES = {
    "rules": ("表示・業務ルール", {"id": "ルールID", "target": "対象項目No", "rule": "ルール"}),
    "states": ("状態定義", {"target": "対象項目No", "state": "状態", "condition": "条件", "behavior": "表示・動作"}),
    "errors": ("エラー処理", {"no": "No", "target": "対象項目No", "case": "エラーケース", "condition": "発生条件",
                          "behavior": "システムの動作", "message_id": "メッセージID", "note": "備考"}),
    "messages": ("メッセージ一覧", {"id": "メッセージID", "type": "種別", "text": "表示メッセージ",
                              "display": "表示方法", "note": "備考"}),
    "open_questions": ("未決事項", {"no": "No", "target": "対象項目No", "question": "質問", "decision": "決定内容",
                               "decided_by": "決定者", "date": "決定日", "status": "状態"}),
}


def as_value(v):
    """ISO dates become real dates so the template's yyyy/mm/dd format applies."""
    if isinstance(v, str) and len(v) == 10 and v[4] == "-" and v[7] == "-":
        try:
            return datetime.date.fromisoformat(v)
        except ValueError:
            return v
    return v


def width_of(text):
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in str(text))


class Sheet:
    def __init__(self, ws):
        self.ws = ws
        self.merged = {(r.min_row, r.min_col): r for r in ws.merged_cells.ranges}

    def span(self, row, col):
        r = self.merged.get((row, col))
        return (col, r.max_col) if r else (col, col)

    def find(self, text, col=None, rows=None):
        for row in self.ws.iter_rows(min_row=rows[0] if rows else 1, max_row=rows[1] if rows else None):
            for c in row:
                if c.value == text and (col is None or c.column == col):
                    return c.row, c.column
        return None

    def headers(self, row):
        """header text -> (first_col, last_col) for one header row."""
        out, col = {}, 1
        while col <= self.ws.max_column:
            v = self.ws.cell(row, col).value
            c1, c2 = self.span(row, col)
            if v is not None:
                out[v] = (c1, c2)
            col = c2 + 1
        return out

    def capacity(self, head_row):
        """Blank rows between a header row and the next section title or the end of the sheet."""
        col = next(iter(self.headers(head_row).values()))[0]
        r = head_row + 1
        while r <= self.ws.max_row and self.ws.cell(r, col).border.left.style:
            r += 1
        return r - head_row - 1

    def write(self, row, col, value, red=False):
        cell = self.ws.cell(row, col, as_value(value))
        cell.alignment = WRAP
        if red:
            cell.font = Font(color=RED)

    def fit(self, row, spans):
        lines = 1
        for c1, c2 in spans:
            v = self.ws.cell(row, c1).value
            if v is None or isinstance(v, (datetime.date, int, float)):
                continue
            w = sum(self.ws.column_dimensions[get_column_letter(c)].width or 10 for c in range(c1, c2 + 1))
            n = sum(max(1, math.ceil(width_of(part) * 1.1 / w)) for part in str(v).split("\n"))
            lines = max(lines, n)
        self.ws.row_dimensions[row].height = max(20, 15 * lines + 4)


def fill_meta(s, meta):
    """Metadata labels sit in the first rows; each value goes in the cell(s) right of its label."""
    def after(label, n=1):
        pos = s.find(label, rows=(1, 12))
        if not pos:
            raise SystemExit(f"template has no metadata label {label!r}")
        row, col = pos
        narrow = lambda c: (s.ws.column_dimensions[get_column_letter(c)].width or 10) < 4
        cells, c = [], s.span(row, col)[1] + 1
        for _ in range(n):
            while narrow(c):  # gutter column between the image area and the tables
                c += 1
            cells.append((row, c))
            c = s.span(row, c)[1] + 1
        return cells

    simple = {"screen_name": "画面名", "overview": "画面概要", "status": "ステータス", "design_ref": "デザイン参照",
              "design_confirmed": "デザイン確認"}
    for key, label in simple.items():
        if key in meta:
            (r, c), = after(label)
            s.write(r, c, meta[key])
    pairs = {"created": "作成日・作成者", "updated": "最終更新", "reviewed": "レビュー"}
    for key, label in pairs.items():
        if key in meta:
            (r1, c1), (r2, c2) = after(label, 2)
            s.write(r1, c1, meta[key].get("date"))
            s.write(r2, c2, meta[key].get("by"))


def fill_table(s, title, mapping, rows, first_col_header):
    pos = s.find(title)
    if not pos:
        raise SystemExit(f"template has no table titled {title!r}")
    head_row = pos[0] + 1
    hdr = s.headers(head_row)
    if first_col_header not in hdr:
        raise SystemExit(f"table {title!r}: header {first_col_header!r} not found")
    if len(rows) > s.capacity(head_row):
        raise SystemExit(f"table {title!r} holds {s.capacity(head_row)} rows, the content has {len(rows)}: add rows to the template")
    for i, item in enumerate(rows):
        r = head_row + 1 + i
        spans = []
        for key, header in mapping.items():
            if header not in hdr:
                continue  # the template does not have this column
            c1, c2 = hdr[header]
            spans.append((c1, c2))
            v = item.get(key)
            if v not in (None, ""):
                s.write(r, c1, v, red=item.get("new_db") and key in ("table", "column", "db_note"))
        s.fit(r, spans)
    return head_row


def main(template, content, out):
    data = json.load(open(content, encoding="utf-8"))
    wb = load_workbook(template)
    s = Sheet(wb["画面詳細設計"])
    fill_meta(s, data.get("meta", {}))
    head = s.find("No", col=None, rows=(1, 40))
    item_head = next(r for r in range(1, 60) if s.ws.cell(r, head[1]).value == "No"
                     and "項目名" in s.headers(r))
    hdr = s.headers(item_head)
    if len(data.get("items", [])) > s.capacity(item_head):
        raise SystemExit(f"項目定義 holds {s.capacity(item_head)} rows, the content has {len(data['items'])}: add rows to the template")
    for i, item in enumerate(data.get("items", [])):
        r = item_head + 1 + i
        spans = []
        for key, header in ITEM_COLS.items():
            if header not in hdr:
                continue
            c1, c2 = hdr[header]
            spans.append((c1, c2))
            v = item.get(key)
            if v not in (None, ""):
                s.write(r, c1, v, red=item.get("new_db") and key in ("table", "column", "db_note"))
        s.fit(r, spans)
    for key, (title, mapping) in TABLES.items():
        if data.get(key):
            fill_table(s, title, mapping, data[key], next(iter(mapping.values())))
    if data.get("revisions") and "改訂履歴" in wb.sheetnames:
        h = wb["改訂履歴"]
        for i, rev in enumerate(data["revisions"]):
            for col, key in zip(range(2, 7), ("version", "date", "by", "where", "what")):
                cell = h.cell(4 + i, col, as_value(rev.get(key)))
                cell.alignment = WRAP
    wb.save(out)
    print(f"saved {out}: {len(data.get('items', []))} items")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])

#!/usr/bin/env python3
"""Fill the 画面詳細設計書 template from a JSON content file.

Usage: python3 fill_spec.py <template.xlsx> <content.json> <out.xlsx>

Metadata labels, tables and columns are located by their text, so a template whose rows or
columns were moved, removed or renamed still fills. What the template lacks is skipped and listed
under "skipped" on stdout. The JSON format is described in references/content-format.md.
"""
import datetime
import json
import math
import sys
import unicodedata
import zipfile

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

WRAP = Alignment(wrap_text=True, vertical="top")
RED = "FF0000"
SKIPPED = []
# An .xlsx never declares a DTD, so a part that does is refused before openpyxl parses it.
MAX_UNZIPPED = 50 * 1024 * 1024


def check_xlsx(path):
    with zipfile.ZipFile(path) as z:
        if sum(i.file_size for i in z.infolist()) > MAX_UNZIPPED:
            raise SystemExit(f"{path}: refused, unzips to more than {MAX_UNZIPPED // 2**20} MB")
        for info in z.infolist():
            if info.filename.endswith((".xml", ".rels")):
                head = z.read(info)[:4096].upper()
                if b"<!DOCTYPE" in head or b"<!ENTITY" in head:
                    raise SystemExit(f"{path}: refused, {info.filename} declares a DTD")

# JSON key -> header text, per table.
ITEM_COLS = {
    "no": "No", "name": "項目名", "label": "画面上表示ラベル", "type": "項目種別", "description": "説明",
    "trigger": "操作", "destination": "遷移先", "behavior": "操作時の動作", "data_type": "データ型",
    "required": "必須", "format": "形式", "max": "最大桁数", "min": "最小桁数", "default": "初期値",
    "validation": "入力チェック", "table": "テーブル名", "column": "カラム名", "db_note": "データベース備考",
}
REVISION_COLS = {"version": "版", "date": "改訂日", "by": "改訂者", "where": "改訂箇所", "what": "改訂内容"}
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
        if isinstance(cell.value, str):
            cell.data_type = "s"  # text starting with "=" stays text, never a formula
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
            SKIPPED.append(f"meta {label!r}: no such label")
            return None
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
        cells = after(label) if key in meta else None
        if cells:
            (r, c), = cells
            s.write(r, c, meta[key])
    pairs = {"created": "作成日・作成者", "updated": "最終更新", "reviewed": "レビュー"}
    for key, label in pairs.items():
        cells = after(label, 2) if key in meta else None
        if cells:
            (r1, c1), (r2, c2) = cells
            s.write(r1, c1, meta[key].get("date"))
            s.write(r2, c2, meta[key].get("by"))


def fill_rows(s, where, head_row, mapping, rows):
    """Write rows under a header row; `extra` writes {header: value} for columns beyond the mapping."""
    hdr = s.headers(head_row)
    if len(rows) > s.capacity(head_row):
        raise SystemExit(f"{where} holds {s.capacity(head_row)} rows, the content has {len(rows)}: "
                         "raise its row count in the layout and rebuild the template")
    missing = {header for header in mapping.values() if header not in hdr}
    for i, item in enumerate(rows):
        r = head_row + 1 + i
        cells = [(key, header) for key, header in mapping.items() if header in hdr]
        cells += [(None, header) for header in (item.get("extra") or {})]
        spans = []
        for key, header in cells:
            if header not in hdr:
                missing.add(header)
                continue
            c1, c2 = hdr[header]
            spans.append((c1, c2))
            v = item.get(key) if key else item["extra"][header]
            if v not in (None, ""):
                s.write(r, c1, v, red=item.get("new_db") and key in ("table", "column", "db_note"))
        s.fit(r, spans)
    used = {h for item in rows for h in (item.get("extra") or {})}
    for header in sorted(missing):
        key = next((k for k, h in mapping.items() if h == header), None)
        if header in used or any(item.get(key) not in (None, "") for item in rows):
            SKIPPED.append(f"{where}: column {header!r} not in the template")


def fill_table(s, title, mapping, rows):
    pos = s.find(title)
    if not pos:
        SKIPPED.append(f"table {title!r}: not in the template, {len(rows)} row(s) not written")
        return
    head_row = pos[0] + 1
    if not set(mapping.values()) & set(s.headers(head_row)):
        SKIPPED.append(f"table {title!r}: no known header, {len(rows)} row(s) not written")
        return
    fill_rows(s, title, head_row, mapping, rows)


def main(template, content, out):
    data = json.load(open(content, encoding="utf-8"))
    check_xlsx(template)
    wb = load_workbook(template)
    s = Sheet(wb["画面詳細設計"])
    fill_meta(s, data.get("meta", {}))
    items = data.get("items", [])
    item_head = next((r for r in range(1, 60) if {"No", "項目名"} <= set(s.headers(r))), None)
    if item_head is None:
        SKIPPED.append(f"項目定義: header row with No and 項目名 not found, {len(items)} item(s) not written")
    elif items:
        fill_rows(s, "項目定義", item_head, ITEM_COLS, items)
    for key, (title, mapping) in TABLES.items():
        if data.get(key):
            fill_table(s, title, mapping, data[key])
    revisions = data.get("revisions") or []
    if revisions and "改訂履歴" not in wb.sheetnames:
        SKIPPED.append(f"改訂履歴: no such sheet, {len(revisions)} revision(s) not written")
    elif revisions:
        h = Sheet(wb["改訂履歴"])
        head = h.find("版")
        if not head:
            SKIPPED.append(f"改訂履歴: header 版 not found, {len(revisions)} revision(s) not written")
        else:
            fill_rows(h, "改訂履歴", head[0], REVISION_COLS, revisions)
    wb.save(out)
    print(json.dumps({"saved": out, "items": len(items), "skipped": SKIPPED}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])

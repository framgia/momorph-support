import sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1]
wb = Workbook()

thin = Side(style="thin", color="A6A6A6")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
HEAD = PatternFill("solid", fgColor="1F4E78")
LABEL = PatternFill("solid", fgColor="DDEBF7")
SECTION = PatternFill("solid", fgColor="F2F2F2")
WHITE_B = Font(bold=True, color="FFFFFF")
BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def box(ws, r1, c1, r2, c2, value=None, fill=None, font=None, align=WRAP):
    if (r1, c1) != (r2, c2):
        ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
    cell = ws.cell(r1, c1)
    if value is not None:
        cell.value = value
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            x = ws.cell(r, c)
            x.border = BOX
            if fill:
                x.fill = fill
    if font:
        cell.font = font
    cell.alignment = align
    return cell


def section(ws, row, c1, title, c2):
    box(ws, row, c1, row, c2, title, fill=SECTION, font=Font(bold=True, size=12),
        align=Alignment(vertical="center"))
    ws.row_dimensions[row].height = 22


def table(ws, row, columns, rows):
    """columns: (header, first_col, last_col). Returns the row after the table."""
    for header, c1, c2 in columns:
        box(ws, row, c1, row, c2, header, fill=HEAD, font=WHITE_B, align=CENTER)
    ws.row_dimensions[row].height = 30
    for r in range(row + 1, row + 1 + rows):
        for _, c1, c2 in columns:
            box(ws, r, c1, r, c2)
    return row + 1 + rows


def dv_list(ws, values, ref, strict):
    # strict=False: suggestions only, any other value is accepted silently.
    dv = DataValidation(type="list", formula1='"' + ",".join(values) + '"', allow_blank=True,
                        showErrorMessage=strict)
    ws.add_data_validation(dv)
    dv.add(ref)


# ── 改訂履歴 ─────────────────────────────────────────────────────
hist = wb.active
hist.title = "改訂履歴"
hist.sheet_view.showGridLines = False
for col, w in zip("ABCDEF", (2, 8, 14, 20, 30, 70)):
    hist.column_dimensions[col].width = w
hist["B1"] = "改訂履歴"
hist["B1"].font = Font(bold=True, size=16, color="1F4E78")
end = table(hist, 3, [("版", 2, 2), ("改訂日", 3, 3), ("改訂者", 4, 4), ("改訂箇所", 5, 5),
                      ("改訂内容", 6, 6)], 20)
for r in range(4, end):
    hist.cell(r, 3).number_format = "yyyy/mm/dd"

# ── 画面詳細設計 ─────────────────────────────────────────────────
ws = wb.create_sheet("画面詳細設計")
wb.active = 1
ws.sheet_view.showGridLines = False
ws.sheet_view.zoomScale = 90
ws.column_dimensions["A"].width = 2
ws.column_dimensions["B"].width = 85  # numbered image, about 600 px
ws.column_dimensions["C"].width = 2

DESC_COLS = [
    ("No", 6), ("項目名", 20), ("画面上表示ラベル", 20), ("項目種別", 14), ("説明", 40), ("操作", 14),
    ("遷移先", 18), ("操作時の動作", 36), ("データ型", 12), ("必須", 9), ("形式", 14), ("最大桁数", 9),
    ("最小桁数", 9), ("初期値", 14), ("入力チェック", 30), ("テーブル名", 18), ("カラム名", 18),
    ("データベース備考", 40),
]
FIRST = 4  # column D
LAST = FIRST + len(DESC_COLS) - 1
for i, (_, w) in enumerate(DESC_COLS):
    ws.column_dimensions[L(FIRST + i)].width = w
col = {h: FIRST + i for i, (h, _) in enumerate(DESC_COLS)}
c = lambda h: col[h]

ws.merge_cells(start_row=1, start_column=2, end_row=1, end_column=FIRST + 3)
ws["B1"] = "画面詳細設計書"
ws["B1"].font = Font(bold=True, size=16, color="1F4E78")
ws.row_dimensions[1].height = 30
legend = box(ws, 1, c("説明"), 1, LAST,
             "凡例　赤字：既存のDBに存在しない新規追加の項目。データベース備考に「新規追加」と追加理由を記載する。"
             "空欄：該当なし。未確定の内容は空欄にせず、未決事項に登録してNoを記載する。",
             align=Alignment(wrap_text=True, vertical="center"))
legend.font = Font(size=9, color="595959")
for cc in range(c("説明"), LAST + 1):
    ws.cell(1, cc).border = Border()

# Metadata in three rows: 2 = name, status, design link; 3 = overview; 4 = dates and people.
lab = lambda r, col, text: box(ws, r, col, r, col, text, fill=LABEL, font=BOLD, align=Alignment(vertical="center", wrap_text=True))
lab(2, 2, "画面名")
box(ws, 2, c("No"), 2, c("説明"))
lab(2, c("操作"), "ステータス")
box(ws, 2, c("遷移先"), 2, c("遷移先"), "作成中", align=Alignment(vertical="center"))
dv_list(ws, ["作成中", "確定"], f"{L(c('遷移先'))}2", True)
lab(2, c("操作時の動作"), "デザイン参照")
box(ws, 2, c("データ型"), 2, LAST)
lab(3, 2, "画面概要")
box(ws, 3, c("No"), 3, LAST)
ws.row_dimensions[3].height = 45
lab(4, 2, "作成日・作成者")
box(ws, 4, c("No"), 4, c("項目名")).number_format = "yyyy/mm/dd"
box(ws, 4, c("画面上表示ラベル"), 4, c("画面上表示ラベル"))
lab(4, c("項目種別"), "最終更新")
box(ws, 4, c("説明"), 4, c("説明")).number_format = "yyyy/mm/dd"
box(ws, 4, c("操作"), 4, c("操作"))
lab(4, c("遷移先"), "レビュー")
box(ws, 4, c("操作時の動作"), 4, c("操作時の動作")).number_format = "yyyy/mm/dd"
box(ws, 4, c("データ型"), 4, c("必須"))
lab(4, c("形式"), "デザイン確認")
box(ws, 4, c("最大桁数"), 4, c("最小桁数")).number_format = "yyyy/mm/dd"

# ── 画面イメージ (left) and 項目定義 (right) ─────────────────────
TOP = 6
section(ws, TOP, 2, "画面イメージ", 2)
section(ws, TOP, FIRST, "項目定義", LAST)
desc_head = TOP + 1
desc_end = table(ws, desc_head, [(h, n, n) for h, n in col.items()], 40)
box(ws, desc_head, 2, desc_end - 1, 2, "番号付き画面画像を貼り付ける",
    align=Alignment(horizontal="center", vertical="center", wrap_text=True))
ws.cell(desc_head, 2).font = Font(italic=True, color="808080")
rng = lambda h, a=desc_head + 1, b=desc_end - 1: f"{L(col[h])}{a}:{L(col[h])}{b}"
dv_list(ws, ["ボタン", "チェックボックス", "ラジオボタン", "ドロップダウン", "テキスト入力", "テキストエリア",
             "日付選択", "ファイル・画像", "動画", "ページネーション", "ポップアップ", "ラベル", "その他"],
        rng("項目種別"), False)
dv_list(ws, ["クリック時", "ホバー時", "キー操作時", "一定時間後"], rng("操作"), False)
dv_list(ws, ["文字列", "整数", "小数", "日付", "日時", "真偽値", "配列", "ファイル", "なし"], rng("データ型"), False)
dv_list(ws, ["必須", "任意"], rng("必須"), False)
for h in ("最大桁数", "最小桁数"):
    dv = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng(h))

# ── Tables below 項目定義 ────────────────────────────────────────
# (title, columns as (header, first_name, last_name), rows)
TABLES = [
    ("表示・業務ルール", [("ルールID", "No", "項目名"), ("対象項目No", "画面上表示ラベル", "画面上表示ラベル"),
                         ("ルール", "項目種別", "データベース備考")], 15),
    ("状態定義", [("対象項目No", "No", "項目名"), ("状態", "画面上表示ラベル", "項目種別"),
                  ("条件", "説明", "遷移先"), ("表示・動作", "操作時の動作", "データベース備考")], 15),
    ("エラー処理", [("No", "No", "No"), ("対象項目No", "項目名", "画面上表示ラベル"),
                    ("エラーケース", "項目種別", "説明"), ("発生条件", "操作", "操作時の動作"),
                    ("システムの動作", "データ型", "入力チェック"), ("メッセージID", "テーブル名", "テーブル名"),
                    ("備考", "カラム名", "データベース備考")], 10),
    ("メッセージ一覧", [("メッセージID", "No", "画面上表示ラベル"), ("種別", "項目種別", "項目種別"),
                        ("表示メッセージ", "説明", "初期値"), ("表示方法", "入力チェック", "入力チェック"),
                        ("備考", "テーブル名", "データベース備考")], 15),
    ("未決事項", [("No", "No", "No"), ("対象項目No", "項目名", "画面上表示ラベル"),
                  ("質問", "項目種別", "遷移先"), ("決定内容", "操作時の動作", "入力チェック"),
                  ("決定者", "テーブル名", "テーブル名"), ("決定日", "カラム名", "カラム名"),
                  ("状態", "データベース備考", "データベース備考")], 15),
]
row = desc_end + 1
anchors = {}
for title, cols, n in TABLES:
    section(ws, row, FIRST, title, LAST)
    head = row + 1
    end = table(ws, head, [(h, c(a), c(b)) for h, a, b in cols], n)
    anchors[title] = (head, end - 1, {h: c(a) for h, a, _ in cols})
    row = end + 1

h0, h1, cm = anchors["メッセージ一覧"]
dv_list(ws, ["エラー", "警告", "情報", "確認", "完了"], f"{L(cm['種別'])}{h0 + 1}:{L(cm['種別'])}{h1}", True)
dv_list(ws, ["インライン", "トースト", "モーダル", "バナー", "アラート"],
        f"{L(cm['表示方法'])}{h0 + 1}:{L(cm['表示方法'])}{h1}", False)
h0, h1, cm = anchors["未決事項"]
dv_list(ws, ["未回答", "回答済み"], f"{L(cm['状態'])}{h0 + 1}:{L(cm['状態'])}{h1}", True)
for r in range(h0 + 1, h1 + 1):
    ws.cell(r, cm["決定日"]).number_format = "yyyy/mm/dd"

ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(OUT)
print(OUT, "desc", desc_head, desc_end - 1, {k: (v[0], v[1]) for k, v in anchors.items()})

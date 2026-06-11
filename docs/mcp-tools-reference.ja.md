# MoMorph MCP Server — ツールリファレンス

MoMorph 内のデザインデータ、specs、test cases、media、ノードツリーを操作するために MoMorph MCP server が公開する **全 32 ツール** の完全なリファレンスです。

> **用語について:** 本ドキュメントでは **Screen (Frame)** および **ScreenSet (FrameSet)** を主要な用語として使用します。「Frame」「FrameSet」は旧称です。

---

## 目次

1. [共通概念](#common-concepts)
2. [ツール索引（クイックルックアップ）](#tool-index-quick-lookup)
3. グループ別ツールリファレンス:
   - [3.1 Specs](#31-specs)
   - [3.2 Test Cases](#32-test-cases)
   - [3.3 Media](#33-media)
   - [3.4 Figma Design](#34-figma-design)
4. [識別子用語集](#identifier-glossary)

---

## 共通概念 {#common-concepts}

### 結果タイプ

ツールは以下のいずれかの結果タイプを返します:

| タイプ | ユースケース                                                  |
| ------ | ------------------------------------------------------------- |
| JSON   | 構造化データ（オブジェクト、配列）                            |
| Text   | プレーンテキスト / データがない場合のフォールバックメッセージ |
| Image  | base64 または URL 形式の画像データ                            |
| Error  | メッセージを伴うエラー結果                                    |

### 認証

以下のいずれかのヘッダーが必要です（優先度順、最上位が最優先）:

| ヘッダー                  | 優先度 | 用途                                                 |
| ------------------------- | ------ | ---------------------------------------------------- |
| `x-momorph-authorization` | 1      | MoMorph トークン（推奨）                             |
| `authorization`           | 2      | 標準的な bearer トークン                             |
| `x-github-token`          | 3      | GitHub トークン（GitHub 連携リソースへのアクセス時） |
| `x-figma-token`           | 4      | Figma トークン（Figma API を直接呼び出す場合）       |

### 共通の入力規約

- `fileKey` — Figma/MoMorph のファイル識別子（string、例: `"abc123XYZ"`）
- `screenId` — MoMorph における Screen (Frame) の一意な識別子（string、例: `"scr_xxx"`）
- `nodeId` — Figma ノード ID（string、例: `"2167:9091"`）
- Sub-status enums: `design_status` / `spec_status` / `review_status` = `none` \| `in_progress` \| `done`; `dev_status` = `none` \| `developing` \| `done`

**MoMorph URL から `fileKey` と `screenId` を取得する:**

```
https://momorph.ai/files/{fileKey}/screens/{screenId}
```

例: `https://momorph.ai/files/9ypp4enmFmdK/screens/i87tDx10` → `fileKey = "9ypp4enmFmdK"`, `screenId = "i87tDx10"`。

### 出力規約

- Screen 情報の返却内容: `screen_id, name, design_status, spec_status, dev_status, review_status, revision (commit_hash), tags, created_at, updated_at`
- CSV エクスポートは列ヘッダー付きの UTF-8 を使用（specs は 22 列、test cases は 18 列）

---

## ツール索引（クイックルックアップ） {#tool-index-quick-lookup}

| #   | ツール名                                                   | グループ     | 用途                                                                                   |
| --- | ---------------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------- |
| 1   | [`get_project_overview`](#1-get_project_overview)          | Specs        | プロジェクトレベルの概要説明を取得                                                     |
| 2   | [`create_frame`](#2-create_frame)                          | Specs        | MoMorph に新しい Screen を作成                                                         |
| 3   | [`get_frame`](#3-get_frame)                                | Specs        | Screen の詳細情報を取得                                                                |
| 4   | [`update_frame`](#4-update_frame)                          | Specs        | Screen メタデータを更新（name / screen_overview / 4 sub-status）                       |
| 5   | [`list_frames`](#5-list_frames)                            | Specs        | すべての Screen を一覧表示（4 つの sub-status で絞り込み可）                           |
| 6   | [`list_frame_sets`](#6-list_frame_sets)                    | Specs        | すべての ScreenSet を一覧表示                                                          |
| 7   | [`get_frame_set`](#7-get_frame_set)                        | Specs        | ScreenSet とその子 Screen を取得                                                       |
| 8   | [`upload_specs`](#8-upload_specs)                          | Specs        | Screen の specs をアップロード / 更新                                                  |
| 9   | [`download_specs`](#9-download_specs)                      | Specs        | Screen の specs を CSV / JSON にエクスポート                                           |
| 10   | [`list_design_items`](#10-list_design_items)                | Specs        | Screen のすべての specs を一覧表示                                                     |
| 11  | [`list_frame_spec_diffs`](#11-list_frame_spec_diffs)       | Specs        | 最新リビジョンに対する spec の変更を比較                                               |
| 12  | [`get_related_design_items`](#12-get_related_design_items) | Specs        | Screen に関連する specs を取得（存在する場合）                                         |
| 13  | [`upload_test_cases`](#13-upload_test_cases)               | Test Cases   | Screen の test cases をアップロード / 更新                                             |
| 14  | [`download_test_cases`](#14-download_test_cases)           | Test Cases   | test cases を CSV / JSON にエクスポート                                                |
| 15  | [`get_frame_test_cases`](#15-get_frame_test_cases)         | Test Cases   | Screen の test cases を取得                                                            |
| 16  | [`get_frame_image`](#16-get_frame_image)                   | Media        | Screen のプレビュー画像を取得（spec 番号のオーバーレイ付きも可）                       |
| 17  | [`list_media_items`](#17-list_media_items)                 | Media        | Screen 内の media nodes を一覧表示                                                     |
| 18  | [`list_media_nodes`](#18-list_media_nodes)                 | Media        | role ヒント付きですべての media nodes を一覧表示（background/icon/overlay/...）        |
| 19  | [`get_media_files`](#19-get_media_files)                   | Media        | Screen 内のすべての media assets（SVG/PNG/JPG）のダウンロード URL を取得               |
| 20  | [`get_media_file`](#20-get_media_file)                     | Media        | ノードの media asset（SVG/PNG/JPG）をストレージから直接ダウンロード                    |
| 21  | [`get_figma_image`](#21-get_figma_image)                   | Media        | 任意の Figma ノードを PNG/JPG にエクスポート（Figma の rate-limit に達する可能性あり） |
| 22  | [`get_design_item_image`](#22-get_design_item_image)       | Media        | 特定の spec item（design item）のクロップ画像を取得                                    |
| 23  | [`get_frame_node_tree`](#23-get_frame_node_tree)           | Figma Design | Screen の完全な階層ノードツリーを取得                                                  |
| 24  | [`get_overview`](#24-get_overview)                         | Figma Design | 軽量な概要ツリー（名前 + タイプのみ）を取得 — 最初に使用して全体像を把握               |
| 25  | [`query_section`](#25-query_section)                       | Figma Design | ノード ID またはあいまいな名前でサブツリーをクエリ                                     |
| 26  | [`query_component`](#26-query_component)                   | Figma Design | 名前でコンポーネントを検索（あいまい一致、関連度でランク付け）                         |
| 27  | [`query_by_type`](#27-query_by_type)                       | Figma Design | Figma タイプですべてのノードをフィルタ（TEXT、INSTANCE、FRAME、...）                   |
| 28  | [`get_node`](#28-get_node)                                 | Figma Design | 正確なノード ID で単一ノードを取得                                                     |
| 29  | [`get_node_context`](#29-get_node_context)                 | Figma Design | parent・siblings・レイヤー role 分析付きでノードを取得（画像レンダリング前に必須）     |
| 30  | [`list_file_variables`](#30-list_file_variables)           | Figma Design | ファイルの CSS / design variables を一覧表示                                           |
| 31  | [`list_frame_styles`](#31-list_frame_styles)               | Figma Design | Screen の完全な階層 CSS スタイルツリーを取得                                           |
| 32  | [`list_file_localizations`](#32-list_file_localizations)   | Figma Design | ソーステキスト文字列に対する多言語翻訳を取得                                           |

---

## 3.1 Specs

MoMorph における Screen (Frame)、ScreenSet (FrameSet)、design item specs を管理するためのツールです。

### 1. `get_project_overview`

Figma/MoMorph ファイルのプロジェクトレベルの概要説明を取得します。作成者が設定したプロジェクトの目的・範囲・コンテキストを記述したテキストを返します。

**パラメータ:**

| 名前      | タイプ | 必須 | 説明           |
| --------- | ------ | ---- | -------------- |
| `fileKey` | string | ✓    | Figma file key |

**Response (text):** `project_overview` 文字列（またはフォールバックメッセージ）。

---

### 2. `create_frame`

Figma にリンクせずに MoMorph ファイル内へ新しい Screen を作成します。specs/test cases の入力を開始するためのスタンドアロンな Screen を初期化する際に便利です。

**パラメータ:**

| 名前             | タイプ | 必須 | デフォルト | 説明                                                                                                                                                                                                                          |
| ---------------- | ------ | ---- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fileKey`        | string | ✓    | —          | MoMorph ファイルの file key                                                                                                                                                                                                   |
| `name`           | string | ✓    | —          | Frame 名（空文字不可）                                                                                                                                                                                                        |
| `screenOverview` | string | ✗    | —          | スクリーンの説明 / 概要                                                                                                                                                                                                       |
| `figmaNodeId`    | string | ✗    | —          | この Screen がリンクする Figma ノード ID。3 形式を受け付け: 標準 `"12318:23788"`、ハイフン `"12318-23788"`、または `node-id=` を含む Figma URL — いずれも標準形式に正規化されます。省略または `""` を渡すと未リンクの Screen。 |
| `designStatus`   | enum   | ✗    | —          | design フェーズのステータス: `none` \| `in_progress` \| `done`                                                                                                                                                                |
| `specStatus`     | enum   | ✗    | —          | spec フェーズのステータス: `none` \| `in_progress` \| `done`                                                                                                                                                                  |
| `devStatus`      | enum   | ✗    | —          | dev フェーズのステータス: `none` \| `developing` \| `done` ⚠（他 3 つと異なる）                                                                                                                                               |
| `reviewStatus`   | enum   | ✗    | —          | review フェーズのステータス: `none` \| `in_progress` \| `done`                                                                                                                                                                |

> **破壊的変更:** レガシー `status`（frame_status）フィールドは入力・レスポンスから削除されました。4 つの sub-status フィールドを使用してください。

**Response (JSON):**

```ts
{
  frame: {
    id: number;
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    screen_overview: string | null;
    created_at: string;
    updated_at: string;
  }
}
```

---

### 3. `get_frame`

`screenId` で Screen の詳細情報を取得します。メタデータ（name、4 つの sub-status (design/spec/dev/review)、screen_overview、figma_node_id、revision (commit hash)、タイムスタンプ）を返します。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明               |
| ---------- | ------ | ---- | ------------------ |
| `screenId` | string | ✓    | frame の Screen ID |

**Response (JSON):**

```ts
{
  frame: {
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    screen_overview: string | null;
    revision: string | null;          // commit_hash
    created_at: string;
    updated_at: string;
  }
}
```

> **破壊的変更:** 非推奨だった `status`（frame_status）フィールドはレスポンスから削除されました — 上記 4 つの sub-status フィールドを使用してください。

---

### 4. `update_frame`

Frame の変更可能なメタデータを更新します。パッチセマンティクス: 明示的に指定したフィールドのみ更新され、省略したフィールドは変更されません。`screenOverview: ""` を渡すとクリア（null に設定）されます。

**パラメータ:**

| 名前             | タイプ | 必須 | 説明                                                                                                                                  |
| ---------------- | ------ | ---- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `screenId`       | string | ✓    | Screen ID                                                                                                                             |
| `name`           | string | ✗    | 新しい frame 名（空文字不可）                                                                                                         |
| `screenOverview` | string | ✗    | 新しい overview/description。`""` を渡すとクリア（null に設定）。                                                                     |
| `figmaNodeId`    | string | ✗    | この Screen がリンクする Figma ノード ID。標準 / ハイフン / URL 形式を受け付け（`create_frame` 参照）。`""` を渡すとリンク解除（null）。 |
| `designStatus`   | enum   | ✗    | `none` \| `in_progress` \| `done`                                                                                                     |
| `specStatus`     | enum   | ✗    | `none` \| `in_progress` \| `done`                                                                                                     |
| `devStatus`      | enum   | ✗    | `none` \| `developing` \| `done` ⚠                                                                                                    |
| `reviewStatus`   | enum   | ✗    | `none` \| `in_progress` \| `done`                                                                                                     |

**挙動:**

- `screenId` 以外に少なくとも 1 つの更新可能フィールドを指定する必要があります。指定しない場合 `"No fields to update"` エラーを返します。
- `screenId` がどの frame にも一致しない場合 → `"Frame not found for screenId: ..."` を返します。
- このツールはレガシー `status` フィールドを公開しません — sub-status のみです。

**Response (JSON):**

```ts
{
  frame: {
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    screen_overview: string | null;
    created_at: string;
    updated_at: string;
  }
}
```

**例:**

- 名前のみ変更: `{ screenId, name: "New name" }`
- overview をクリア: `{ screenId, screenOverview: "" }`
- dev を done に: `{ screenId, devStatus: "done" }`
- 複合: `{ screenId, name: "X", screenOverview: "Y", specStatus: "done" }`

---

### 5. `list_frames`

ファイル内のすべての Screen を一覧表示します。デフォルトではすべての Screen を返します（アーカイブ済みは除外）。4 つの sub-status フィールド（design/spec/dev/review）で任意に絞り込み可能。複数の filter は AND で結合されます。

**パラメータ:**

| 名前              | タイプ  | 必須 | デフォルト | 説明                                                                |
| ----------------- | ------- | ---- | ---------- | ------------------------------------------------------------------- |
| `fileKey`         | string  | ✓    | —          | Figma file key                                                      |
| `designStatus`    | enum    | ✗    | —          | `none` \| `in_progress` \| `done`                                   |
| `specStatus`      | enum    | ✗    | —          | `none` \| `in_progress` \| `done`                                   |
| `devStatus`       | enum    | ✗    | —          | `none` \| `developing` \| `done` ⚠                                  |
| `reviewStatus`    | enum    | ✗    | —          | `none` \| `in_progress` \| `done`                                   |
| `includeOverview` | boolean | ✗    | `false`    | `true` の場合、各 Screen に `screen_overview` を含めます（大きい可能性あり） |

> **破壊的変更:** レガシー `status`（frame_status）filter は入力・レスポンスから削除されました。以前のドキュメントには `draft`/`completed` も記載されていましたが、それはバグで、それらの値は有効でした。新しい 4 sub-status filter を使用してください。

**Response (JSON):** frames 配列:

```ts
{
  frames: Array<{
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    revision: string | null;
    tags: string[];
    screen_overview?: string | null;          // includeOverview=true の場合のみ
    created_at: string;
    updated_at: string;
  }>;
}
```

---

### 6. `list_frame_sets`

ファイル内のすべての ScreenSet（Screen グループ）を一覧表示します。個々の Screen に踏み込む前に、ファイルの構成構造を把握するのに便利です。

**パラメータ:**

| 名前      | タイプ | 必須 | 説明           |
| --------- | ------ | ---- | -------------- |
| `fileKey` | string | ✓    | Figma file key |

**Response (JSON):** `{ frame_sets: [...] }`。

---

### 7. `get_frame_set`

`frameSetId` で ScreenSet の詳細を取得します。完全なメタデータを持つすべての子 Screen のリストを含みます。

**パラメータ:**

| 名前         | タイプ | 必須 | 説明         |
| ------------ | ------ | ---- | ------------ |
| `frameSetId` | number | ✓    | Frame set ID |

**Response (JSON):** frames を埋め込んだ frame_set オブジェクト。

---

### 8. `upload_specs`

Screen の specs（design items）を一括でアップロードまたは更新します。JSON 配列（通常は CSV から変換）を受け取り、データベースへ upsert します。2 種類の異なるステータスを管理します: **spec 完了状態**（`spec_progress`: `draft`/`completed`）と **ライフサイクル**（`active_status`: `active`/`archived`/`deleted`）。どちらのフィールドも任意で、省略した場合 `spec_progress` は内容から自動検出されます。`active_status=archived` の item は、内容の変更を含む場合は拒否されます。

**パラメータ:**

| 名前        | タイプ   | 必須        | 説明                    |
| ----------- | -------- | ----------- | ----------------------- |
| `screen_id` | string   | ✓           | 対象 frame の Screen ID |
| `specs`     | object[] | ✓（最小 1） | spec item の配列        |

**Spec item の形（22 フィールド）:**

```
no, design_item_name, name, nameTrans, node_link_id?,
type, otherType, buttonType, dataType, required, format,
minLength, maxLength, defaultValue, validationNote,
action, linkedFrameId, navigationNote,
tableName, columnName, databaseNote, description,
id?, section_link_id, extLink, is_reviewed
```

**Response (JSON):**

```ts
{
  status: 'success' | 'failed' | 'skipped';
  target_frame: {...};
  uploaded_count: number;
  skipped_count: number;
  invalid_count: number;
  saved_items: [...];
  invalid_specs?: [...];
}
```

**動作:** `spec_progress`（spec 完了状態: `draft`/`completed`）は指定がない場合は内容から自動検出されます。`active_status`（ライフサイクル: `active`/`archived`/`deleted`）はデフォルトで `active` です。`active_status=archived` の item は、内容の変更が存在する場合は拒否されます。リビジョン追跡は常に適用されます。

---

### 9. `download_specs`

Screen の specs（design items）を CSV または JSON（`upload_specs` の入力スキーマと一致）としてエクスポートします。データは保存されたまま返され、変換は行われません。編集して再アップロードするラウンドトリップのワークフローに便利です。`spec_progress` 列（spec 完了状態: `draft`/`completed`）は常に含まれます。`active_status` 列（ライフサイクル: `active`/`archived`/`deleted`）は `include_deleted=true` の場合にのみ含まれます。

**パラメータ:**

| 名前              | タイプ  | 必須 | デフォルト | 説明                                                                                                                   |
| ----------------- | ------- | ---- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| `screen_id`       | string  | ✓    | —          | Screen ID                                                                                                              |
| `format`          | enum    | ✗    | `csv`      | `csv` \| `json` \| `both`                                                                                              |
| `include_deleted` | boolean | ✗    | `false`    | true の場合、archived/deleted の item を含め、出力に `active_status` 列（`active`\|`archived`\|`deleted`）を追加します |

**Response (JSON):**

```ts
{
  status: 'success' | 'empty';
  target_frame: {...};
  item_count: number;
  csv?: string;
  specs?: [...];
}
```

CSV 出力は変更せずにそのままファイルへ保存できます。

---

### 10. `list_design_items`

Screen のすべての design items（specs）を、メタデータから強化されたタイプ情報付きで一覧表示します。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):**

```ts
{
  design_items: Array<{
    id: string;
    no: number;
    type: string;
    name: string;
    specs: {...};
    status: string;
  }>;
}
```

---

### 11. `list_frame_spec_diffs`

Screen の現在の specs を最新リビジョンと比較します。変更ステータス（`new` / `deleted` / `delta` / `unchanged`）付きの design items を返します。`kind = delta` の場合、変更されたフィールドの詳細を含みます。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):**

```ts
{
  designItems: Array<{
    node_id: string;
    no: number;
    name: string;
    status: string;
    type: string;
    specs: {...};  // 表示テーブル
    diffs: {
      kind: 'new' | 'deleted' | 'delta' | 'unchanged';
      delta?: {...};  // 変更されたフィールド値、kind=delta の場合のみ
    };
  }>;
}
```

---

### 12. `get_related_design_items`

特定の design item に関連する design items（コピー、master components、同じ set 内の item）を取得します。`limit` でカテゴリごとの最大結果数を制御します。

**パラメータ:**

| 名前           | タイプ | 必須 | デフォルト | 説明                       |
| -------------- | ------ | ---- | ---------- | -------------------------- |
| `screenId`     | string | ✓    | —          | Screen ID                  |
| `designItemId` | string | ✓    | —          | 元の design item ID        |
| `limit`        | number | ✗    | `3`        | カテゴリごとの最大 item 数 |

**Response (JSON):** `node_link_id` で重複排除された関連 item の配列。

---

## 3.2 Test Cases

各 Screen に紐づく test cases を管理するためのツールです。

### 13. `upload_test_cases`

Screen の test cases を一括でアップロードまたは更新します。JSON 配列（通常は CSV から変換）を受け取り、test case 配列を含む **単一のレコード** として Screen ごとに保存します。`test_area` の値（`functional`/`function` → `FUNCTION` など）を自動的に正規化します。

**パラメータ:**

| 名前         | タイプ   | 必須        | 説明           |
| ------------ | -------- | ----------- | -------------- |
| `screen_id`  | string   | ✓           | Screen ID      |
| `test_cases` | object[] | ✓（最小 1） | test case item |

**Test case item の形:**

- `ID`（必須）
- 任意: `step, category, page_name, test_area, test_data, sub_category, sub_sub_category, pre_condition, expected_result, test_objective, specs, tc_type, priority, test_results, executed_date, tester, note`

**動作:** `test_area` の値（`functional`/`function` → `FUNCTION` など）を正規化します。

**Response (JSON):**

```ts
{
  status: 'success';
  operation: 'created' | 'updated';
  target_frame: {...};
  test_case_count: number;
}
```

---

### 14. `download_test_cases`

Screen の test cases を CSV（18 列）または JSON（`upload_test_cases` の入力スキーマと一致）としてエクスポートします。データはデータベースに保存されたまま返されます。

**パラメータ:**

| 名前        | タイプ | 必須 | デフォルト | 説明                      |
| ----------- | ------ | ---- | ---------- | ------------------------- |
| `screen_id` | string | ✓    | —          | Screen ID                 |
| `format`    | enum   | ✗    | `csv`      | `csv` \| `json` \| `both` |

**CSV 列（18）:**
`Section, TC_ID, Page_Name, Category, Sub_Category, Sub_Sub_Category, Test_Objective, Precondition, Test_Data, Steps, Expected_Result, Specs, Priority, Testcase_Type, Test_Result, Executed_Date, Tester, Note`

**Response (JSON):**

```ts
{
  status: 'success' | 'empty';
  target_frame: {...};
  test_case_count: number;
  csv?: string;
  test_cases?: [...];
}
```

---

### 15. `get_frame_test_cases`

frame link 経由で Figma から直接 Screen の test cases を取得します。Screen が Figma にリンクされていない場合は空を返します。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):** `{ test_cases: [...] }`。frame に Figma リンクがない場合は空。

---

## 3.3 Media

画像や media ファイルの取得、Figma ノードの画像レンダリングを行うためのツールです。

### 16. `get_frame_image`

Screen のレンダリング画像を取得します。出力は base64 データまたは URL を選択でき、`showDesignItems=true` を指定すると番号付きの design item 注釈を画像にオーバーレイして、spec レビューを素早く行えます。

**パラメータ:**

| 名前              | タイプ  | 必須 | デフォルト | 説明                                      |
| ----------------- | ------- | ---- | ---------- | ----------------------------------------- |
| `screenId`        | string  | ✓    | —          | frame の Screen ID                        |
| `outputType`      | enum    | ✗    | `data`     | `data`（base64）または `url`              |
| `showDesignItems` | boolean | ✗    | `false`    | 番号付きの design item 注釈をオーバーレイ |

**Response:**

- `outputType=data` の場合 → image（base64 PNG、自動リサイズ）
- `outputType=url` の場合 → `Text`（画像 URL）

---

### 17. `list_media_items`

Screen 内のすべての media nodes（`MM_MEDIA_*` プレフィックスを持つもの）を、Screen の階層ノードから絞り込んでメタデータ付きで一覧表示します。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):** 階層メタデータから絞り込んだ media nodes の配列、またはテキストフォールバック。

---

### 18. `list_media_nodes`

すべての `MM_MEDIA_*` asset ノードを、サイズ・parent コンテキスト・sibling 数・`roleHint`（background/icon/small-icon/text-label/overlay/image）付きで一覧表示します。`roleHint` は parent に対するサイズ比から推測されます。**いかなる `<img>` タグを記述する前にも呼び出して**、各 asset の意図された role を理解してください。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):**

```ts
{
  screenId: string
  mediaNodeCount: number
  nodes: Array<{
    id: string
    name: string
    type: string
    width: number
    height: number
    aspectRatio: number
    parentId: string
    parentName: string
    parentType: string
    parentWidth: number
    parentHeight: number
    siblingCount: number
    roleHint: 'background' | 'icon' | 'small-icon' | 'text-label' | 'overlay' | 'image'
  }>
}
```

---

### 19. `get_media_files`

Screen 内のすべての media files（SVG/PNG/JPG）の presigned ダウンロード URL を取得します。URL はバッチ単位（1 バッチ 50 件）で返され、一括ダウンロードに便利です。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):** URL の配列（50 件ずつのグループにバッチ化）、media がない場合はテキストフォールバック。

---

### 20. `get_media_file`

ノードの単一の media ファイル（SVG/PNG/JPG）をストレージから直接ダウンロードします。デフォルトは SVG で、`convertType` を指定するとラスター（png/jpg/jpeg）に変換できます。SVG は元のサイズで返され、ラスター形式は自動的にリサイズされます。

**パラメータ:**

| 名前             | タイプ | 必須 | 説明                                                               |
| ---------------- | ------ | ---- | ------------------------------------------------------------------ |
| `fileKey`        | string | ✓    | Figma file key                                                     |
| `componentSetId` | string | ✗    | `hierarchicalNodes` から取得した Component set ノード ID           |
| `nodeId`         | string | ✗    | `hierarchicalNodes` から取得したノード ID                          |
| `convertType`    | enum   | ✗    | `png` \| `jpg` \| `jpeg` \| `svg`。省略した場合は SVG を返します。 |

**Response (image):**

- SVG はリサイズなしで返却
- ラスター形式は自動リサイズ

---

### 21. `get_figma_image`

Figma REST API 経由で 1 つ以上の Figma ノードを PNG/JPG 画像としてレンダリングします。カスタムの `scale`（0.01–4）と `outputType`（base64 または URL）をサポートします。**注意:** Figma API を直接呼び出すため、rate-limit に達する可能性があります。

**パラメータ:**

| 名前         | タイプ   | 必須 | デフォルト | 説明                           |
| ------------ | -------- | ---- | ---------- | ------------------------------ |
| `fileKey`    | string   | ✓    | —          | Figma file key                 |
| `nodeIds`    | string[] | ✓    | —          | レンダリングするノード ID      |
| `scale`      | number   | ✗    | `1`        | レンダリングスケール（0.01–4） |
| `format`     | enum     | ✗    | `png`      | `png` \| `jpg`                 |
| `outputType` | enum     | ✗    | `url`      | `data`（base64 配列）\| `url`  |

**Response:**

- `outputType=url` → 画像 URL を含む JSON
- `outputType=data` → image パート（base64）を含む応答

---

### 22. `get_design_item_image`

Screen 内の特定の design item のクロップ画像を取得します。画像はサイズ削減のため自動的に最大 2000px にリサイズされます。

**パラメータ:**

| 名前           | タイプ | 必須 | 説明                         |
| -------------- | ------ | ---- | ---------------------------- |
| `screenId`     | string | ✓    | design item を含む Screen ID |
| `designItemId` | string | ✓    | Design Item ID               |

**Response (image):** base64 PNG、最大 2000px に自動リサイズ。

---

## 3.4 Figma Design

Figma ファイルのノードツリー、スタイル、variables、localization をクエリするためのツールです。

### 23. `get_frame_node_tree`

Screen の完全な階層ノードツリーを取得します。デフォルトでは各ノードの specs を含みます。`includeSpecs=false` を設定すると、specs を含まないコンパクトな構造マップを取得できます。

**パラメータ:**

| 名前           | タイプ  | 必須 | デフォルト | 説明                                            |
| -------------- | ------- | ---- | ---------- | ----------------------------------------------- |
| `screenId`     | string  | ✓    | —          | frame の Screen ID                              |
| `includeSpecs` | boolean | ✗    | `true`     | 構造のみの軽量マップを取得するには false に設定 |

**Response (JSON):** 再帰的なツリー:

```ts
{
  id: string;
  name: string;
  type: string;
  specs?: {...};
  children: Node[];
}
```

---

### 24. `get_overview`

Screen の軽量な概要ツリーを取得します。名前、タイプ、階層のみを含みます（スタイルなし）。`query_section` や `get_node` などの詳細ツールに踏み込む前に、全体構造を理解するために**最初に使用**してください。`maxDepth` で深さを制御します。

**パラメータ:**

| 名前       | タイプ | 必須 | デフォルト | 説明                 |
| ---------- | ------ | ---- | ---------- | -------------------- |
| `screenId` | string | ✓    | —          | Screen ID            |
| `maxDepth` | number | ✗    | `3`        | 概要ツリーの最大深さ |

**Response (JSON):** `OverviewNode` ツリー:

```ts
{
  id: string;
  name: string;
  type: string;
  text?: string;
  componentId?: string;
  children?: OverviewNode[];
  childCount?: number;
}
```

---

### 25. `query_section`

`nodeId`（正確）または `nodeName`（あいまい一致）で Screen からサブツリーを取得します。ノードとその子を完全なスタイル付きで返します。両方が指定された場合は `nodeId` が優先されます。`maxDepth` で深さを制御します（0 = ノードのみ）。

**パラメータ:**

| 名前       | タイプ | 必須 | デフォルト | 説明                                                |
| ---------- | ------ | ---- | ---------- | --------------------------------------------------- |
| `screenId` | string | ✓    | —          | Screen ID                                           |
| `nodeId`   | string | ✗    | —          | 正確なノード ID（`nodeName` より優先）              |
| `nodeName` | string | ✗    | —          | 名前によるあいまい一致（`nodeId` がない場合に使用） |
| `maxDepth` | number | ✗    | `3`        | 子の最大深さ（0 = ノードのみ）                      |

**Response (JSON):** 完全なノード詳細とスタイルを持つ、剪定されたサブツリー。

---

### 26. `query_component`

あいまい一致を用いて名前で Screen 内のコンポーネントを検索し、関連度スコアでソートされた結果を返します。名前は分かっているが正確な `nodeId` が分からない場合に使用します。`includeStyles` と `limit` でカスタマイズ可能です。

**パラメータ:**

| 名前            | タイプ  | 必須 | デフォルト | 説明                               |
| --------------- | ------- | ---- | ---------- | ---------------------------------- |
| `screenId`      | string  | ✓    | —          | Screen ID                          |
| `name`          | string  | ✓    | —          | 検索クエリ（例: "Header"、"Logo"） |
| `includeStyles` | boolean | ✗    | `true`     | response に CSS styles を含める    |
| `limit`         | number  | ✗    | `5`        | 最大結果数                         |

**Response (JSON):**

```ts
{
  query: string;
  matchCount: number;
  results: Array<{
    ...nodeFields;
    _matchScore: number;
  }>;
}
```

---

### 27. `query_by_type`

特定の Figma タイプ（例: `TEXT`, `INSTANCE`, `FRAME`, `RECTANGLE`, `GROUP`, `COMPONENT`, `VECTOR`）のすべてのノードをフィルタして返します。すべてのテキストコンテンツやすべてのコンポーネントインスタンスを取得する場合などに便利です。response をコンパクトに保つため、styles はデフォルトで除外されます。

**パラメータ:**

| 名前            | タイプ  | 必須 | デフォルト | 説明                                                                                        |
| --------------- | ------- | ---- | ---------- | ------------------------------------------------------------------------------------------- |
| `screenId`      | string  | ✓    | —          | Screen ID                                                                                   |
| `itemType`      | string  | ✓    | —          | Figma タイプ: `TEXT`, `INSTANCE`, `FRAME`, `RECTANGLE`, `GROUP`, `COMPONENT`, `VECTOR` など |
| `includeStyles` | boolean | ✗    | `false`    | styles を含める（デフォルトでは response を小さく保ちます）                                 |

**Response (JSON):** `{ itemType, count, results: [...] }`。

---

### 28. `get_node`

正確な Figma ノード ID（例: `2167:9091`）で単一ノードを、完全なスタイル・位置・親子関係・メタデータ付きで取得します。正確な ID が不明な場合は、まず `query_component` を使って名前で検索してください。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明                                        |
| ---------- | ------ | ---- | ------------------------------------------- |
| `screenId` | string | ✓    | Screen ID                                   |
| `nodeId`   | string | ✓    | 正確な Figma ノード ID（例: `"2167:9091"`） |

**Response (JSON):** スタイル・位置・親子関係・メタデータを持つ完全なノードオブジェクト。

---

### 29. `get_node_context`

ノードを、その parent・同じレベルのすべての siblings・sibling ごとの role 分析（`background` / `text` / `icon` / `overlay`）付きで取得します。**画像ノードのレンダリング前に不可欠**で、レイヤーの重ね合わせ構成を理解するのに役立ちます。`includeSiblingStyles` で sibling のスタイルを切り替えられます。

**パラメータ:**

| 名前                   | タイプ  | 必須 | デフォルト | 説明                            |
| ---------------------- | ------- | ---- | ---------- | ------------------------------- |
| `screenId`             | string  | ✓    | —          | Screen ID                       |
| `nodeId`               | string  | ✓    | —          | 対象ノード ID                   |
| `includeSiblingStyles` | boolean | ✗    | `true`     | siblings の CSS styles を含める |

**Response (JSON):**

```ts
{
  target: {...},                              // 完全なノード
  parent: {                                   // または null
    id: string;
    itemName: string;
    itemType: string;
    styles: {...};
    childCount: number;
  } | null,
  siblings: Array<{...node, _isSelf: boolean}>,
  layerAnalysis: Array<{
    id: string;
    name: string;
    type: string;
    width: number;
    height: number;
    role: string;                             // background | text | icon | overlay
    isSelf: boolean;
  }>;
}
```

---

### 30. `list_file_variables`

Figma ファイルの CSS / design variables を collection ごとにグループ化して一覧表示します。各 collection は名前とその variables を含みます。

**パラメータ:**

| 名前      | タイプ | 必須 | 説明           |
| --------- | ------ | ---- | -------------- |
| `fileKey` | string | ✓    | Figma file key |

**Response (JSON):**

```ts
{
  variableCollections: Array<{
    name: string;
    variables: [...];
  }>;
}
```

variables がない場合は `Text`。

---

### 31. `list_frame_styles`

Screen の完全な階層 CSS スタイルツリーを取得します。スタイル付きの完全なノード構造を反映しており、スタイルの検査やコード生成に便利です。

**パラメータ:**

| 名前       | タイプ | 必須 | 説明      |
| ---------- | ------ | ---- | --------- |
| `screenId` | string | ✓    | Screen ID |

**Response (JSON):** 再帰的な node-style ツリー、またはメタデータに node styles がない場合はテキスト。

---

### 32. `list_file_localizations`

Figma ファイル内のソーステキスト文字列（`sourceTexts`）に対応する多言語翻訳を取得します。localizations のクロスチェックやエクスポートに便利です。

**パラメータ:**

| 名前          | タイプ   | 必須 | 説明                     |
| ------------- | -------- | ---- | ------------------------ |
| `fileKey`     | string   | ✓    | Figma file key           |
| `sourceTexts` | string[] | ✓    | 翻訳対象のソーステキスト |

**Response (JSON):** `{ localizations: [...] }`。

---

## 識別子用語集 {#identifier-glossary}

| 識別子           | タイプ | 説明                                                       | 例            |
| ---------------- | ------ | ---------------------------------------------------------- | ------------- |
| `fileKey`        | string | Figma/MoMorph ファイルの一意な ID                          | `"abc123XYZ"` |
| `screenId`       | string | MoMorph における frame（screen）の一意な ID                | `"scr_xxx"`   |
| `frameSetId`     | number | 数値の frame-set ID                                        | `42`          |
| `nodeId`         | string | Figma ノード ID（`<frame>:<index>`）                       | `"2167:9091"` |
| `designItemId`   | string | MoMorph の design item ID                                  | `"di_xxx"`    |
| `componentSetId` | string | Component set ノード ID（`hierarchicalNodes` から取得）    | `"2167:9000"` |
| `node_link_id`   | string | リビジョンをまたいで安定した参照                           | `"link_xxx"`  |
| `commit_hash`    | string | リビジョン識別子。一部の応答では `revision` として返される | `"abc123"`    |

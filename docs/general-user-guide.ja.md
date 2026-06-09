# MoMorph — 利用ガイド


> 📩 **お問い合わせ・サポート — MoMorph チーム**
> - Slack: `#con_momorph-support_all`
> - Email: `momorph-admin@sun-asterisk.com`

---

## 目次

<details>
<summary><strong>1. <a href="#1-概要">概要</a></strong></summary>

- [1.1 エコシステム (7 製品)](#11-エコシステム-7-製品)
- [1.2 データフロー図](#12-データフロー図)
- [1.3 前提条件](#13-前提条件)
  - [アカウント](#アカウント)
  - [ソフトウェア / OS](#ソフトウェア--os)

</details>

<details>
<summary><strong>2. <a href="#2-momorph-figma-plugin">MoMorph Figma Plugin</a></strong></summary>

- [2.1 インストール](#21-インストール)
- [2.2 ログイン](#22-ログイン)
  - [Pro user](#pro-user)
  - [Essential user](#essential-user)
- [2.3 Design Data の同期](#23-design-data-の同期)
- [2.4 UI 要素を Spec 画面に読み込む](#24-ui-要素を-spec-画面に読み込む)

</details>

<details>
<summary><strong>3. <a href="#3-momorph-web-app">MoMorph Web App</a></strong></summary>

- [3.1 アクセス](#31-アクセス)
- [3.2 ログイン](#32-ログイン)
- [3.3 Core Features](#33-core-features)
- [3.4 Screen Status Workflow](#34-screen-status-workflow)

</details>

<details>
<summary><strong>4. <a href="#4-momorph-syncer-google-add-on">MoMorph Syncer (Google Add-on)</a></strong></summary>

- [4.1 利用条件](#41-利用条件)
- [4.2 インストール / アクセス](#42-インストール--アクセス)
- [4.3 機能](#43-機能)

</details>

<details>
<summary><strong>5. <a href="#5-momorph-cli">MoMorph CLI</a></strong></summary>

- [5.1 インストール](#51-インストール)
- [5.2 認証と初期化](#52-認証と初期化)
- [5.3 Command Reference](#53-command-reference)

</details>

<details>
<summary><strong>6. <a href="#6-mcp-server--ai-tools">MCP Server — AI Tools</a></strong></summary>

- [前提条件](#前提条件)
- [方法 1 — CLI による高速セットアップ](#方法-1--cli-による高速セットアップ)
- [方法 2 — 手動での設定](#方法-2--手動での設定)
- [Tools 一覧](#tools-一覧)

</details>

<details>
<summary><strong>7. <a href="#7-ai-agent-integrations">AI Agent Integrations</a></strong></summary>

- [7.1 概要](#71-概要)
- [7.2 GitHub Copilot + VSCode Extension](#72-github-copilot--vscode-extension)
- [7.3 Claude Code](#73-claude-code)
- [7.4 Cursor / Windsurf / Gemini](#74-cursor--windsurf--gemini)
- [7.5 Claude Desktop Extension (.mcpb)](#75-claude-desktop-extension-mcpb)

</details>

<details>
<summary><strong>8. <a href="#8-よくあるエラー">よくあるエラー</a></strong></summary>

- [8.1 CLI](#81-cli)
- [8.2 Web App](#82-web-app)
- [8.3 Figma Plugin](#83-figma-plugin)
- [8.4 VSCode Extension](#84-vscode-extension)
- [8.5 Syncer (Google Sheets Add-on)](#85-syncer-google-sheets-add-on)
- [8.6 MCP / Slash Commands](#86-mcp--slash-commands)

</details>

---

## 1. 概要

**MoMorph** は Sun\* Asterisk の AI-Driven Development エコシステムであり、Figma design / Specs をソフトウェアのライフサイクル全体の起点とします。

```
Figma Design & Specs → Test Cases → Code
```

### 1.1 エコシステム (7 製品)

| #   | Component                    | Purpose                                                                                  | Platform           |
| --- | ---------------------------- | ---------------------------------------------------------------------------------------- | ------------------ |
| 1   | **Figma Plugin**             | Figma から MoMorph へ design data を同期し、設計データを管理、specs ドキュメントを作成など | Figma              |
| 2   | **Web App**                  | project の管理、screens/specs/test cases の保存                                          | ブラウザ           |
| 3   | **Syncer (Google Add-on)**   | Google Sheets 上で spec/testcase を編集し、MoMorph と双方向同期                          | Google Sheets      |
| 4   | **CLI**                      | project の初期化、MCP の設定、CSV specs/testcases のアップロード                         | ターミナル         |
| 5   | **VSCode Extension**         | design/spec の表示、MCP server の統合、Figma Tree、Copilot Chat 用 slash commands        | VS Code            |
| 6   | **MCP Server**               | agent が MoMorph と Figma のデータを読み書きするための AI tools を提供                    | AI agent 経由で自動 |
| 7   | **Claude Desktop Extension** | `.mcpb` バンドル — Claude Desktop から MoMorph MCP を利用                                 | Claude Desktop     |

### 1.2 データフロー図

```
┌─────────────┐     design data      ┌──────────────────┐
│ Figma Plugin │ ──────────────────► │  MoMorph Web App │
│ (in Figma)  │                      │  (Database/API)  │
└─────────────┘                      └────────┬─────────┘
                                              │
                                    ┌─────────▼──────────┐
                                    │   MoMorph MCP      │
                                    │   Server (Cloud)   │
                                    │ mcp.momorph.ai/mcp │
                                    └────────┬───────────┘
                                             │ AI reads data
               ┌─────────────────────────────┼──────────────────────┐
               │                             │                      │
    ┌──────────▼──────┐           ┌──────────▼──────┐    ┌──────────▼──────┐
    │  Claude Code    │           │ VSCode Extension│    │  Cursor/Copilot │
    └──────────┬──────┘           └──────────┬──────┘    └──────────┬──────┘
               │                             │                      │
               └─────────────────────────────┼──────────────────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Slash Commands │
                                    │  /momorph.xxx   │
                                    └─────────────────┘

    ┌─────────────┐
    │ MoMorph CLI │ ── upload specs, testcases ──────────► Web App
    │  (Terminal) │ ── init project, configure MCP ───────► Local repo
    └─────────────┘

    ┌────────────────────────────┐    local       ┌────────────────┐
    │ Claude Desktop Extension   │ ─────────────► │ MCP Server     │
    │ (.mcpb bundle)             │                 │ mcp.momorph.ai │
    └────────────────────────────┘                 └────────────────┘
```

### 1.3 前提条件

#### アカウント

**MoMorph のユーザープラン (Essential vs Pro)** — エコシステム全体のアクセス範囲を決定します。

| Plan          | アクセス範囲                                                                                                                                                                                                       |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Essential** | **Plugin のみ** — 利用できる機能: screens の管理、spec の手動入力、GitHub issue のエクスポート。その他のサブプロダクト (Web App, Syncer, CLI, MCP Server, VSCode Extension, Claude Desktop Extension) は**利用できません** |
| **Pro**       | **エコシステム全体** — Plugin (全機能) + Web App + Syncer + CLI + MCP Server + VSCode Extension + Claude Desktop Extension                                                                                          |

**Pro user になる方法:**

- Sun\* 社のドメインに属するメールアドレスを持つユーザーは、デフォルトで Pro アカウントになります。
- それ以外のメールアドレス: Pro アカウントの発行については MoMorph チームへお問い合わせください。

**各 product で必要となる基盤アカウント:**

| Product                  | Account | Requirement                                                                                                                                              |
| ------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Figma Plugin             | Figma   | [Figma の plugin 利用条件](https://help.figma.com/hc/en-us/articles/360039958474)に準拠 (Viewer seat でも個人の Drafts ファイル内では plugin を実行可能) |
| Web App                  | Figma   | すべての seat                                                                                                                                            |
| Syncer (Google Add-on)   | Google  | **Sun\* 社の Google Workspace** アカウント                                                                                                                |
| CLI                      | GitHub  | `momorph login`                                                                                                                                          |
| MCP Server               | GitHub  | PAT scope `user`                                                                                                                                         |
| VSCode Extension         | GitHub  | CLI と同じアカウント + **Copilot Business** (Free では不十分)                                                                                            |
| Claude Desktop Extension | GitHub  | PAT scope `user`                                                                                                                                         |

#### ソフトウェア / OS

| Product                  | Requirement                                                                |
| ------------------------ | -------------------------------------------------------------------------- |
| Figma Plugin             | Figma Desktop または figma.com                                             |
| Web App                  | 最新版の Chrome / Firefox / Safari / Edge                                  |
| Syncer (Google Add-on)   | ブラウザ上の Google Sheets (Sun\* Workspace)                               |
| CLI                      | macOS / Linux / Windows (Homebrew / Chocolatey / scripts でインストール — §5.1 参照) |
| VSCode Extension         | VS Code ≥ v1.105 · Windows: WSL                                            |
| Claude Desktop Extension | MCP v1.x 対応の Claude Desktop · Node.js ≥ 18 · macOS/Windows/Linux        |

---

## 2. MoMorph Figma Plugin

Plugin は Figma (Desktop/Browser) 上で動作し、Web App (§3) と同様の機能に加え、design data (screens, items, styles, variables, media) を MoMorph DB へ同期する機能を備えています。

### 2.1 インストール

1. Figma を開く → **Plugins → Manage plugins** → "MoMorph" を検索
2. **Install** をクリック → Run

### 2.2 ログイン

Plugin を初めて開いたとき (または session の有効期限が切れたとき) には、2 つのログインフローに対応する 2 つのボタンを持つ **Welcome** 画面が表示されます。アカウントの種類に応じて、いずれか 1 つを選択してください。

#### Pro user

**「Pro アカウントでログイン」** ボタンをクリックします。

1. Plugin がブラウザのタブを開きます → Figma OAuth ページで **Authorize** を押してアカウントを認証します。
2. 認証に成功したら Plugin に戻り、**「Figma ファイルを接続」** ステップに進みます — plugin を開いている Figma ファイルの URL を貼り付け → **「続行」** をクリックします。
3. ファイルに複数の page がある場合、Plugin は **「読み込む page を選択」** ステップに進みます — Figma canvas から screens データを読み込みたい page を選択 → インストール完了。
4. Plugin のメイン画面に入ります。

> Figma アカウントは Pro アカウントである必要があります (§1.3 参照)。そうでない場合、authorize 後にブラウザでエラーが表示されます。

#### Essential user

**「無料で始める」** ボタンをクリックします。

1. Plugin はブラウザを開かず、Figma の OAuth も必要ありません。
2. Essential features (screens の閲覧、spec の手動入力、GitHub issue のエクスポート) を備えた Plugin のメイン画面に直接入ります。
3. Web App, CLI, MCP Server, VSCode Extension, Claude Desktop Extension は利用できません — §1.3 参照。

### 2.3 Design Data の同期

Web App, CLI, MCP, VSCode Extension は、Plugin を通じて同期された後でなければ設計データを参照できません。

**同期方法:**

1. **作業対象の Figma ファイルで Plugin を開く** → Plugin がバックグラウンドで screens の一覧を自動同期します。操作は不要です。
2. **1 つの screen をクリックして詳細画面に入る** → その screen の画像と UI 要素が同期されます。
3. 次のような場合に **Preview toolbar** 上の **Refresh** アイコン (🔄) をクリックします:
   - Figma で design を編集した直後で、すぐに MoMorph へ反映したいとき。
   - Web App に _「設計画像が Figma Plugin から同期されていません」_ と表示されるとき。
   - Item が変更/リネーム/追加されたが、Plugin がまだ認識していないとき。

### 2.4 UI 要素を Spec 画面に読み込む

screen の詳細画面 (Spec) を開いたとき、Plugin は Figma のレイヤー名のうち **convention に従った prefix を持つレイヤーのみを読み込みます**。prefix に一致しないレイヤーはスキップされ、要素一覧には表示されません。

**レイヤー命名ルール:**

| 種類                            | Prefix              | 例                                                    | Spec での表示                                            |
| ------------------------------- | ------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| **Item** (現行の convention)    | `mms_<名前>`        | `mms_button`, `mms_submit_form`                       | ✅ 独立した 1 要素として表示                             |
| **Item** (旧 convention)        | `<英字/数字>_<名前>` | `A_button`, `A1_submit`, `1_label`, `1.1_email_field` | ✅ 表示可能。spec に追加すると自動的に `mms_*` へ変換される |
| **Media** (画像/アイコン)       | `mm_media` を含む名前 | `mm_media`, `mm_media_logo`                           | ✅ Media セクションに表示                                |
| **通常レイヤー**                | (prefix なし)       | `Rectangle 1`, `Frame 23`, `Button`                   | ❌ 表示されない                                          |

**注意:**

- Prefix は **大文字・小文字を区別しません** (`A_button` ≡ `a_button`、`MMS_action` ≡ `mms_action`)。
- prefix の後の名前には文字 `<`, `>`, `'`, `"` を**含めてはいけません** (HTML/SVG エラーを避けるため)。
- `mms_*` convention が現行の標準です — 新しい命名はこの形式で行うことを推奨します。旧形式の prefix を含むレイヤー (`1_button`, `A_button`) も互換性があり、spec にリンクする際に Plugin が自動的に `mms_*` へリネームします。
- visibility が無効 (`visible = false`) なレイヤーは読み込まれません。さらに、親フレームが `opacity = 0` の場合、その子レイヤーもスキップされます。

**AI Generate による一覧の自動生成:**

prefix を手動で設定する方法のほかに、Spec 画面では **AI Generate** 機能を使って AI に Figma の設計を自動分析させ、UI 要素の一覧を生成させることができます。AI による生成後は、必要に応じて item を見直して修正/追加することを推奨します。

**Designer 向けの推奨ワークフロー:**

1. Figma で設計するときに、レイヤー名を `mms_*` prefix で命名します (例: `mms_login_button`, `mms_username_field`)。
2. Plugin を開く → 詳細画面に入る → Spec screen の item 一覧を確認します。
3. item が不足している場合は、Figma 上でレイヤー名を修正 → Preview toolbar の **Refresh** (🔄) をクリック (§2.3 参照) して再読み込みします。

> prefix を正しく設定したのに item が表示されない場合は §8.3 を参照してください。

---

## 3. MoMorph Web App

projects/files/screens/specs を管理する中心拠点です。設計データは事前に Plugin を通じて Figma から同期されます。Plugin からの同期を行わない場合、Web や他の product でデータへのアクセスに問題が生じる可能性があります。

### 3.1 アクセス

URL: **`https://momorph.ai`** · EN/JP/VI に対応 (Settings で変更)。

### 3.2 ログイン

1. `momorph.ai` を開く
2. **「Login with Figma」** をクリック
3. Figma を Authorize


### 3.3 Core Features

`momorph.ai` でログイン後、sidebar/breadcrumb から遷移します。

**Files & Screens**

| Feature          | Purpose                                                       |
| ---------------- | ------------------------------------------------------------- |
| File list        | link 済みの Figma files 一覧                                  |
| Screen list      | ファイル内の screens (status, tag, page でフィルタ)           |
| Screen detail    | 画像プレビュー + design items                                 |
| Item spec editor | validation/navigation/DB mapping を編集; **AI Generate Spec** あり |
| Spec revisions   | version 履歴 + rollback                                       |
| View all specs   | screen 内のすべての specs を閲覧する read-only 表             |
| Screen tags      | screen にタグ付け (functional, bug…)                          |
| Global tags      | システム全体のタグ管理                                        |

**Screen Sets** (screens をグループにまとめる)

| Feature          | Purpose                          |
| ---------------- | -------------------------------- |
| Screen Sets list | screen sets 一覧                 |
| Create / Edit    | screen set の作成 / 編集         |
| Set detail       | 1 つの set 内の screens を閲覧   |
| Screen in set    | set のコンテキストから screen を開く |

**ファイル単位の Settings**

| Feature                | Purpose                                    |
| ---------------------- | ------------------------------------------ |
| Project Overview       | project の説明 (markdown)                  |
| GitHub                 | OAuth + repo の link (VSCode Ext / CLI 用) |
| Google                 | Google の OAuth (Syncer Google Sheets 用)  |
| Screen Translation     | 多言語ハブ                                 |
| Translation Languages  | ファイルごとの言語の有効/無効              |
| Translation Dictionary | en↔jp↔vi の翻訳表                        |

### 3.4 Screen Status Workflow

各 screen には独立した 4 つの status field (`design_status`, `spec_status`, `dev_status`, `review_status`) があり、各 field は 3 つの値 (`Not Started` / `In Progress` / `Done`) を持ちます。推奨される手順は次のとおりです。

```
Design → Spec → Dev → Review → Done
```

status field は Screen detail 内で直接編集します。VSCode Extension はデフォルトで `spec_status = Done` をフィルタするため、Dev は実装の準備が整った screen のみを参照します。

---

## 4. MoMorph Syncer (Google Add-on)

Google Sheets 向けの add-on で、Sheets ↔ MoMorph 間を双方向同期します。Sheets 上で spec / test case を編集 (複数人での共同作業、コメント、formula) してから MoMorph に反映する、あるいは逆に MoMorph から Sheets へ spec を反映してチームでレビューする場合に適しています。

### 4.1 利用条件

- **Sun\* 社の Google Workspace** アカウント。個人の Google アカウントでは add-on を利用できません。
- MoMorph の **Pro** プラン (§1.3 参照) — Essential user は Syncer を利用できません。
- MoMorph Syncer add-on がインストール済みの Google Sheets ファイル。

### 4.2 インストール / アクセス

- Sun\* Workspace に属する Google Sheets を開く → メニュー **Extensions → MoMorph Syncer を検索してインストール**。初回は、add-on が Sheets ファイルへアクセスし MoMorph backend を呼び出すために Google アカウントの authorize を求めるポップアップが表示されます。
- **Extensions** に MoMorph Syncer メニューが表示されない場合は、MoMorph チームへお問い合わせください。

### 4.3 機能

| Action                  | 説明                                                                   |
| ----------------------- | ---------------------------------------------------------------------- |
| **Sync Specifications** | UI 要素の定義を Sheets ↔ MoMorph 間で双方向同期                        |
| **Sync Testcases**      | test case を Sheets ↔ MoMorph 間で双方向同期                          |
| **Sync Image**          | Figma から最新の design 画像を in-cell native images として Sheets に取り込む |
| **Sync i18n**           | 多言語コンテンツ (en / jp / vi) を同期                                 |

> authorization エラー、sheet が同期できない、メニューに action が不足しているなどの問題が発生した場合は §8.5 を参照してください。

---

## 5. MoMorph CLI

project の install/init、CSV specs/testcases のアップロード、AI agent 用の MCP 設定を行います。注意: CLI は download を**サポートしていません** — spec/testcases を CSV としてダウンロードするには、MCP tools 経由で AI agent を使用してください (§6 参照)。

### 5.1 インストール

**macOS / Linux (Homebrew — 推奨):**

```bash
brew install momorph/tap/momorph-cli
```

**Windows (Chocolatey):**

```bash
choco install momorph-cli
```

**Windows (PowerShell):**

```powershell
irm https://raw.githubusercontent.com/momorph/cli/refs/heads/main/scripts/install.ps1 | iex
```

**Linux/macOS (Bash):**

```bash
curl -fsSL https://raw.githubusercontent.com/momorph/cli/refs/heads/main/scripts/install.sh | bash
```

**Go install:**

```bash
go install github.com/momorph/cli@latest
```

**確認 / 更新:**

```bash
momorph version
momorph update
```

### 5.2 認証と初期化

**ステップ 1 — ログイン:**

```bash
momorph login          # CLI がコード + リンクを表示。Enter でブラウザを開く
momorph whoami         # アカウントを確認
```

**ステップ 2 — Init project:**

```bash
momorph init . --ai claude        # Claude Code
momorph init . --ai copilot       # GitHub Copilot
momorph init . --ai cursor        # Cursor
momorph init . --ai windsurf      # Windsurf
momorph init . --ai gemini        # Gemini
```

> **重要:** root repo 内で init するには `.` を使用します。`momorph init my-project` はサブフォルダを作成します。

`init` は自動的に、最新の template のダウンロード、`.claude/` (または `.github/`, `.cursor/`…) の作成、MCP server の設定、slash commands のインストールを行います。

### 5.3 Command Reference

| Command                                         | Description                                 |
| ----------------------------------------------- | ------------------------------------------- |
| `momorph login`                                 | GitHub OAuth Device Flow で認証             |
| `momorph logout [--force]`                      | ログアウトし、credentials を削除            |
| `momorph whoami`                                | アカウント + subscription                   |
| `momorph init <dir> --ai <agent>`               | project の init + agent の設定              |
| `momorph upload specs <file.csv>`               | spec CSV をアップロード                     |
| `momorph upload specs <file.csv> --dry-run`     | プレビュー、アップロードしない              |
| `momorph upload testcases <file.csv>`           | test cases をアップロード                   |
| `momorph upload testcases <file.csv> --dry-run` | プレビュー                                  |
| `momorph version`                               | CLI のバージョン                            |
| `momorph update [--check]`                      | CLI を更新 (`--check`: 確認のみ)            |
| `momorph completion <shell>`                    | Shell completion (bash/zsh/fish/powershell) |
| `momorph help [command]`                        | ヘルプ                                      |

> **アップロード時の screen の指定方法** (いずれか 1 つを選択):
>
> 1. **convention に従ったファイル名** — `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv`。ここで `{figmaFrameId}` は frame の Figma node ID です (例: `9276:19907-TOP_Channel.csv`)。これは `/specs`, `/createtestcases`, `/updatetestcases` などの slash command が自動生成する format です。
> 2. **フラグ `--screen-id <screenId>`** — alphanumeric の MoMorph screenId で、Web の URL (`/screens/{screenId}/...`) から取得します。ファイルが convention path の外にある場合は `--file-key` を併用します。

---

## 6. MCP Server — AI Tools

`https://mcp.momorph.ai/mcp` でホストされ、AI agent が MoMorph と Figma のデータを読み書きするための tools を提供します。ユーザーが**直接呼び出すことはありません** — AI agent が自動的に使用します (§7.2 の slash commands 経由、または Claude Desktop §7.5 の自然言語プロンプト経由)。各 tool の詳細な説明は、MCP Tools の利用ガイドを参照してください。

一部の重要な tool には **対応する slash command がありません** — AI が MCP 経由で呼び出すのみです:

- `upload_specs` / `download_specs` — CSV spec を MoMorph へアップロード/からダウンロード。2 種類の status の管理に対応: **spec completion** (`spec_progress`: `draft`/`completed`) と **lifecycle** (`active_status`: `active`/`archived`/`deleted`)。Download は常に `spec_progress` 列を返し、`active_status` 列は `include_deleted=true` を使用した場合のみ含まれます。Upload は両方の項目を受け付けます — 渡さない場合、status は内容から自動計算されます。`active_status=archived` の item は、内容に変更があると拒否されます。
- `upload_test_cases` / `download_test_cases` — CSV test cases をアップロード/ダウンロード
- `list_frame_spec_diffs` — screen の spec を前の revision と比較

**上記 tool を手動で起動する方法:**

- **Upload** (specs/testcases): CLI (`momorph upload specs|testcases <file.csv>`) を使用するか、VSCode Explorer で `.momorph/` 内の `.csv` ファイルを右クリック → "Upload to MoMorph" (§7.2 参照)
- **Download** + **list_frame_spec_diffs**: AI agent 経由のみ — Claude Desktop/Code/Cursor での自然言語プロンプト、または VSCode メニューの slash command `/downloadspecs`

### 前提条件

- MoMorph Web に連携済みの GitHub アカウント (CLI / MCP 用)
- repo へのアクセス権 (VSCode Extension / Plugin 用、アカウントが Admin の場合)

### 方法 1 — CLI による高速セットアップ

(Claude Desktop は `.mcpb` を使用 — §7.5 参照)

```bash
brew install momorph/tap/momorph-cli
momorph login
momorph init . --ai <agent_name>
```

### 方法 2 — 手動での設定

```json
{
  "mcpServers": {
    "momorph": {
      "url": "https://mcp.momorph.ai/mcp",
      "headers": {
        "x-github-token": "YOUR_GITHUB_TOKEN"
      }
    }
  }
}
```

PAT scope `user` を GitHub → Settings → Developer settings → Personal access tokens で作成します。

### Tools 一覧

MCP server の全 tools について、詳細な説明、パラメータ、戻り値の型、使用例を確認するには、MCP Tools の利用ガイドを参照してください。

---

## 7. AI Agent Integrations

### 7.1 概要

| Agent                      | Init Command                   | Prompt Folder                         | Trigger                   | Best for            |
| -------------------------- | ------------------------------ | ------------------------------------- | ------------------------- | ------------------- |
| **Claude Code**            | `momorph init . --ai claude`   | `.claude/commands/`                   | ターミナル内で Slash      | CLI, headless       |
| **GitHub Copilot**         | `momorph init . --ai copilot`  | `.github/agents/`, `.github/prompts/` | Copilot Chat / VSCode Ext | IDE 中心            |
| **Cursor**                 | `momorph init . --ai cursor`   | `.cursor/commands/`                   | Cursor chat               | All-in-one IDE      |
| **Windsurf**               | `momorph init . --ai windsurf` | (Windsurf に準拠)                     | Windsurf chat             | Codeium             |
| **Gemini**                 | `momorph init . --ai gemini`   | (Gemini CLI に準拠)                   | Gemini chat               | Google stack        |
| **Claude Desktop** (.mcpb) | §7.5 参照                      | n/a                                   | 自然言語プロンプト        | Casual / non-coding |

### 7.2 GitHub Copilot + VSCode Extension

**Sun\* MoMorph VSCode Extension** (`sun-asterisk.vscode-momorph`): Figma Tree、slash commands、Copilot Chat 用の MCP server 登録。

#### 条件

- Figma ファイルの **view または edit** 権限 (unit test の generate のみの場合は不要)
- **GitHub Copilot Business**
- VS Code ≥ v1.105
- Windows: WSL

#### インストール

VSCode Extension は `.vsix` ファイルで配布されます。最新ファイルの入手は MoMorph チームへお問い合わせください。

1. `vscode-momorph-x.y.z.vsix` ファイルを開く
2. VSCode → **Extensions** タブ → **`...`** → **Install from VSIX...**
3. ファイルを選択

#### 接続

CLI と同じ GitHub account を使用します。`momorph login` 済みであることを確認してください。

1. Web → Settings → GitHub → connect repo
2. VSCode → repo を開く → Activity Bar の **MoMorph** アイコンをクリック
3. screen の list が表示される → setup OK

#### インストール後

VSCode 内で直接探索できます:

- **Sidebar — Figma view** (`momorph.figma`): **With Design / No Design / Archived** でグループ化された screens を閲覧。さらに **Screen Sets** と **Components** があります。**tag, page, status** (4 つの status field: Design / Spec / Dev / Review) でフィルタ/検索。デフォルトで `Spec Status = Done` をフィルタ
- **Sidebar — Contexts view** (`momorph.contexts`): `.momorph/contexts/api-docs.yaml` の endpoints を表示し、ファイル変更時に自動 refresh
- **screen を右クリック** (multi-select 対応):
  - **Open on Web** / **Copy Screen Information**
  - AI agent 用の prompt を生成する 15 個の slash commands — 下表参照
  - repo 内の `.github/agents/momorph.*.agent.md` を検出: あり → prompt 付きで Copilot Chat を開く; なし → prompt を clipboard にコピー (Claude/Cursor に貼り付け)
- **screen をクリック** → 画像プレビューパネル + specs パネル (items / styles / variables / test cases を含む) を持つ web view
- **Command Palette** (`Cmd/Ctrl+Shift+P` → `MoMorph:`): Sign In, Search/Filter Screens, Open MoMorph Web, OpenAPI Server (Start/Stop/Restart)…
- **Settings** (`Cmd/Ctrl+,` → `momorph`):
  - `chat.language` & `chat.outputFileLanguage` (English / Vietnamese / Japanese)
  - `api.baseUrl`, `api.headers`, `mcpServers`, `github.remoteName`, `github.useEnterprise`
- **Copilot Chat**: `/` で slash commands を表示; `#` で 7 個の Language Model Tools を表示 — `momorph_callMcpTool`, `momorph_compareScreenshots`, `momorph_downloadFigmaImage`, `momorph_getPreferenceInstructions`, `momorph_getUserPreferences`, `momorph_listApiEndpoints`, `momorph_getApiEndpoint`
- **Explorer**: `.momorph/specs/` または `.momorph/testcases/` 内の `.csv` を右クリック → **Upload to MoMorph**
- **MCP servers** が事前設定済み (`momorph.mcpServers` 内): `momorph`, `context7`, `testViewpoints`

#### context menu の slash commands

15 個の commands を 2 グループに分類します。**Agent file** 列は、独立した prompt ファイル (`.claude/commands/momorph.*.agent.md` または `.github/agents/momorph.*.agent.md`) を持つ commands を示します — これらは Claude Code/Cursor で実行可能です; agent file を持たない commands は VSCode メニュー経由のみで動作します (prompt は動的生成)。

**Flow** — spec → plan → implement のプロセス:

| Command          | Agent file | Action                                                |
| ---------------- | :--------: | ----------------------------------------------------- |
| `/constitution`  |     ✅     | constitution の Init/update (rules, stack)            |
| `/specify`       |     ✅     | screen から `spec.md` + `design-style.md` + assets を生成 |
| `/reviewspecify` |     ❌     | spec.md & design-style.md の Review/改善              |
| `/plan`          |     ✅     | spec + design-style + constitution から Plan          |
| `/reviewplan`    |     ❌     | plan の Review/改善                                   |
| `/tasks`         |     ✅     | plan を `tasks.md` に分解                             |
| `/implement`     |     ✅     | `tasks.md` に従ってコーディング                      |

**Context** — Figma からデータを生成:

| Command            | Agent file | Action                                            |
| ------------------ | :--------: | ------------------------------------------------- |
| `/specs`           |     ✅     | screen から 22 列の CSV spec                      |
| `/createtestcases` |     ✅     | test cases (Accessing/GUI/Function), 1 screen あたり 1 CSV |
| `/updatetestcases` |     ✅     | spec 変更時に test cases を Update                |
| `/apispec`         |   ✅ \*    | OpenAPI specs + backend test cases                |
| `/database`        |     ✅     | SQL Schema + ERD Mermaid                          |
| `/screenflow`      |     ✅     | `SCREENFLOW.md` を生成                            |
| `/downloadspecs`   |     ❌     | MoMorph から CSV spec をダウンロード (MCP tool 経由) |
| `/convertspecs`    |     ❌     | spec markdown → CSV をローカル変換 (アップロードしない) |

\* Agent file 名は `momorph.apispecs.agent.md` (複数形) ですが、VSCode メニューでは `apispec` (単数形) という名前でトリガーされます。

#### agent file のみで利用できる slash commands (VSCode メニューにはない)

`momorph init . --ai <agent>` でインストールし (§7.3-§7.4 参照)、ターミナル/chat で直接入力します:

| Command          | Action                                          |
| ---------------- | ----------------------------------------------- |
| `/commit`        | Conventional Commits に従って Commit            |
| `/prdescription` | template に従った PR description                |
| `/ship`          | Commit + push + PR 作成を 1 コマンドで          |
| `/reviewcode`    | PR と ticket spec を比較レビューし、severity 別に報告 |
| `/setupe2e`      | Playwright の Init (repo あたり 1 回)           |
| `/writee2e`      | test plan から `.spec.ts`                       |
| `/reviewe2e`     | POM, locator, data, パフォーマンスをレビュー    |

> extension がデータを表示しない場合は、notification 上の **`See Error`** をクリックして output channel を開きます。

### 7.3 Claude Code

```bash
momorph init . --ai claude
```

`.claude/commands/momorph.*.agent.md` を生成します。Claude Code のターミナルを開き、slash command を入力します。MCP config は `~/.claude.json` に追加されます。

### 7.4 Cursor / Windsurf / Gemini

```bash
momorph init . --ai cursor       # .cursor/commands/
momorph init . --ai windsurf
momorph init . --ai gemini
```

prompt ファイルは各 agent の convention に従います。MCP config は対応する config ファイルにマージされます。

### 7.5 Claude Desktop Extension (.mcpb)

`.mcpb` バンドルは、ファイルによって MoMorph MCP を Claude Desktop にインストールします — ローカルの Claude Desktop を `mcp.momorph.ai/mcp` に接続します。

#### Compatibility

- macOS / Windows / Linux · Node.js ≥ 18 · MCP v1.x 対応の Claude Desktop

#### インストール

1. 最新の `momorph-mcp.mcpb` ファイルの入手は MoMorph チームへお問い合わせください。
2. Claude Desktop → **Settings** → **Extensions** → **Advanced Settings** → **Install Extension**
3. ファイルを選択 → **Install** → **GitHub PAT** (scope `user`) を入力 → **Save** → **Enable**

#### Test

プロンプト: _"List all frames in this Figma file: {fileKey}"_ — Claude が自動的に `list_frames` を呼び出します。MCP の debug log を見るには Developer Mode を有効にします。

> **`.mcpb` vs MCP Cloud:** `.mcpb` は Claude Desktop のみを使用するユーザー向けです。マルチ IDE のセットアップ (VSCode + Claude Code + Cursor) → `momorph init` 経由の MCP Cloud (§5)。

---

## 8. よくあるエラー

### 8.1 CLI

**`momorph login` が完了しない** — firewall/VPN が `github.com/login/device` をブロックしていないか確認します。`https://github.com/login/device` で code を直接入力することもできます。

### 8.2 Web App

**Figma ログイン失敗 / popup がブロックされる:**

- `momorph.ai` からの popup を許可する
- ブラウザの private mode を試す (extension が OAuth callback をブロックすることがある)
- Figma account がまだ active であることを確認する

**ログイン後にファイルが表示されない** — popup 時に Figma URL から `fileKey` を入力します。スキップした場合: `/` → "Add file" → fileKey を貼り付け。

### 8.3 Figma Plugin

**Item が認識されない** — レイヤー名に convention どおりの `mms_*` prefix があるか確認します (§2.4 参照)。

**Plugin が真っ白 / spinner が回り続ける:**

- Figma が `momorph.ai` にアクセスできているか (network/VPN)?
- Web をログアウト → 再ログイン → plugin を reload (`Cmd/Ctrl+Shift+P` → `Reload`)

### 8.4 VSCode Extension

**MCP に接続できない** — 未ログインまたは token の期限切れ:

```bash
momorph login
momorph whoami
```

その後 `Ctrl+Shift+P → Developer: Reload Window`。

**Tree view に screens が表示されない:**

- repo は Web に link 済みか (Settings → GitHub)?
- Figma Tree の **Refresh** をクリック
- エラーがある → notification 上の **`See Error`** をクリック

**Context menu が Copilot Chat をトリガーしない** — Extension は `.github/agents/momorph.*.agent.md` を検出して Copilot project かどうかを判断します。これが無い場合 (Claude Code project)、prompt は clipboard にコピーされます — 手動で Claude に貼り付けてください。

### 8.5 Syncer (Google Add-on)

**MoMorph Syncer メニューが Extensions に表示されない** — この Sheets ファイル向けに add-on が運用チームによってデプロイされていません。MoMorph チームへお問い合わせください。

**action 呼び出し時に "Missing authentication token"** — Google session の期限切れです。Google account に再ログインし (Sun\* 社の Google Workspace アカウントを使用していることを確認)、Sheets タブを refresh して再試行します。

**"Cannot access spreadsheet"** — ファイルの共有権限が不足しています。確認事項:

- Sheets ファイルが Sun\* Workspace 内にあるか (個人の private ファイルは非対応)。
- 現在の account が **Editor** 権限を持っているか (Viewer では MoMorph への逆同期ができません)。

**"Invalid Figma URL"** — format が正しくない URL を貼り付けています。ブラウザのアドレスバーから Figma リンクを貼り直してください (特定の frame を同期する場合は `node-id` を含めて)。

**"Failed to sync data"** — MoMorph backend または network が中断しています。数分待って再試行してください; 何度も繰り返す場合はチームサポートへ報告してください。

**同期後に cell に画像が表示されない** — in-cell image の変換はバックグラウンド (fire-and-forget) で実行されます。10〜30 秒待ってから sheet を reload してください。それでも失敗する場合は、メニューの **Sync Image** を再度クリックします。

### 8.6 MCP / Slash Commands

**specs アップロード時に "Frame not found"** — `--screen-id` が不足または誤りです (Figma node ID `32355:420279` ≠ MoMorph screenId)。次の 2 つの方法のいずれかで修正します (§5.3 参照):

- ファイル名を convention `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` どおりに付けて、フラグなしでアップロードする。
- または、フラグ `--screen-id` を渡す:
  ```bash
  momorph upload specs <file.csv> --screen-id <alphanumeric-screenId>
  ```

**Download specs "Frame not found"** (AI agent が MCP `download_specs` を呼び出すとき) — agent が MoMorph screenId の代わりに Figma node ID を使用しています。Web の URL (`/screens/{screenId}/...`) から screenId を取得し、改めてプロンプトします。

**Claude Desktop Extension が tools を呼び出さない:**

- Settings → Extensions → MoMorph の status が `Enabled`
- GitHub PAT がまだ valid か (scope `user`)?
- Developer Mode を有効にして log を見る
- fileKey/screenId を明記した明確なプロンプト

**MCP timeout / 遅い:**

- `mcp.momorph.ai` への network を確認
- 大きな slash command (item の多い screen に対する `/momorph.specs`) は 30〜60 秒かかることがある — さらに待つ
- 何度も失敗する → `momorph login` で token を refresh

**`x-github-token` invalid / 401:**

- PAT が revoke 済み/期限切れ → 新しい PAT (scope `user`) を作成し、MCP config (`~/.claude.json` など) を更新
- `momorph init` を使用: `momorph login` を実行 → token が config に自動マージされる

---

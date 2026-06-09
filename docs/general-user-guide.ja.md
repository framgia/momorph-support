# MoMorph — ユーザーガイド

> **対象読者:** MoMorph の AI-Driven Development ワークフローを利用する Designer・BrSE・Dev・QA・PM

---

## 目次

<details>
<summary><strong>1. <a href="#1-概要">概要</a></strong></summary>

- [1.1 エコシステム (7 プロダクト)](#11-エコシステム-7-プロダクト)
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
- [2.4 Spec 画面への UI 要素読み込み](#24-spec-画面への-ui-要素読み込み)

</details>

<details>
<summary><strong>3. <a href="#3-momorph-web-app">MoMorph Web App</a></strong></summary>

- [3.1 アクセス](#31-アクセス)
- [3.2 ログイン](#32-ログイン)
- [3.3 Core Features](#33-core-features)
- [3.4 Screen Status Workflow](#34-screen-status-workflow)

</details>

<details>
<summary><strong>4. <a href="#4-momorph-syncer-google-add-on--sun-社員専用">MoMorph Syncer (Google Add-on)</a></strong></summary>

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
- [方法 1 — CLI で素早くセットアップ](#方法-1--cli-で素早くセットアップ)
- [方法 2 — 手動で設定](#方法-2--手動で設定)
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
<summary><strong>8. <a href="#8-よくあるトラブル">よくあるトラブル</a></strong></summary>

- [8.1 CLI](#81-cli)
- [8.2 Web App](#82-web-app)
- [8.3 Figma Plugin](#83-figma-plugin)
- [8.4 VSCode Extension](#84-vscode-extension)
- [8.5 Syncer (Google Sheets Add-on)](#85-syncer-google-sheets-add-on)
- [8.6 MCP / Slash Commands](#86-mcp--slash-commands)

</details>

---

## 1. 概要

**MoMorph** は Sun\* Asterisk が提供する AI-Driven Development のエコシステムです。Figma のデザイン / Specs をソフトウェア開発ライフサイクル全体の起点とします。

```
Figma Design & Specs → Test Cases → Code
```

### 1.1 エコシステム (7 プロダクト)

| #   | Component                    | 役割                                                                                                       | Platform              |
| --- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | **Figma Plugin**             | Figma のデザインデータを MoMorph へ同期。デザインデータの管理、specs ドキュメント生成などを Figma 上で完結 | Figma                 |
| 2   | **Web App**                  | project の管理、screens / specs / test cases の保存                                                        | ブラウザ              |
| 3   | **Syncer (Google Add-on)**   | Google Sheets 上で spec / testcase を編集し、MoMorph と双方向に同期                                        | Google Sheets         |
| 4   | **CLI**                      | プロジェクト初期化、MCP 設定、CSV specs / testcases のアップロード                                         | Terminal              |
| 5   | **VSCode Extension**         | デザイン / spec の表示、MCP server 統合、Copilot Chat 用の Figma Tree と slash commands                    | VS Code               |
| 6   | **MCP Server**               | AI agent が MoMorph / Figma のデータを読み書きするための 31 個の AI tools を提供                           | AI agent から自動連携 |
| 7   | **Claude Desktop Extension** | `.mcpb` バンドル — Claude Desktop から MoMorph MCP を利用                                                  | Claude Desktop        |

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

**MoMorph のユーザープラン (Essential vs Pro)** — エコシステム全体の利用範囲を決定します:

| Plan          | 利用範囲                                                                                                                                                                                            |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Essential** | **Plugin のみ** — screens 管理、spec の手動入力、GitHub issue エクスポートが利用可能。他のプロダクト (Web App、Syncer、CLI、MCP Server、VSCode Extension、Claude Desktop Extension) は **利用不可** |
| **Pro**       | **エコシステム全体** — Plugin (フル機能) ＋ Web App ＋ Syncer ＋ CLI ＋ MCP Server ＋ VSCode Extension ＋ Claude Desktop Extension                                                                  |

**Pro ユーザーになる方法:**

- `sun-asterisk.com` ドメインはデフォルトで Pro whitelist 登録済み → Sun\* アカウントなら自動的に Pro 付与
- 他ドメインのメールを利用する場合: Slack `#con_momorph-support_all` まで連絡し whitelist 追加を依頼

**プロダクトごとに必要なプラットフォームアカウント:**

| Product                  | Account | 必要条件                                                                                                                                            |
| ------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Figma Plugin             | Figma   | [Figma のプラグイン利用条件](https://help.figma.com/hc/en-us/articles/360039958474) に準拠 (Viewer seat は自身の Drafts ファイル内であれば起動可能) |
| Web App                  | Figma   | seat 種別不問                                                                                                                                       |
| Syncer (Google Add-on)   | Google  | **Sun\* Asterisk Google Workspace** アカウント (`@sun-asterisk.com`)                                                                                |
| CLI                      | GitHub  | `momorph login` を実行                                                                                                                              |
| MCP Server               | GitHub  | PAT (scope: `user`)                                                                                                                                 |
| VSCode Extension         | GitHub  | CLI と同一アカウント、加えて **Copilot Business** (Free 版は対象外)                                                                                 |
| Claude Desktop Extension | GitHub  | PAT (scope: `user`)                                                                                                                                 |

#### ソフトウェア / OS

| Product                  | 必要環境                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------ |
| Figma Plugin             | Figma Desktop または figma.com                                                       |
| Web App                  | Chrome / Firefox / Safari / Edge の最新版                                            |
| Syncer (Google Add-on)   | ブラウザ上の Google Sheets (Sun\* Workspace)                                         |
| CLI                      | macOS / Linux / Windows (Homebrew / Chocolatey / scripts でインストール — §5.1 参照) |
| VSCode Extension         | VS Code v1.105 以上 ・ Windows は WSL                                                |
| Claude Desktop Extension | MCP v1.x 対応の Claude Desktop ・ Node.js 18 以上 ・ macOS / Windows / Linux         |

---

## 2. MoMorph Figma Plugin

Figma (Desktop / Browser) 上で動作する Plugin。Web App (§3) と同等の機能に加え、design data (screens、items、styles、variables、media) を MoMorph DB に同期します。

### 2.1 インストール

1. Figma で **Plugins → Manage plugins** を開き、「MoMorph」を検索
2. **Install** をクリックし、続けて Run

本番版 Plugin ID: `1406117276934709483`。

### 2.2 ログイン

Plugin を初回起動時 (またはセッション切れ時) に **Welcome** 画面が表示され、2 つのログインボタンが用意されています。アカウント種別に応じてどちらか 1 つを選択してください。

#### Pro user

**「Pro アカウントでログイン」** ボタンをクリック

1. Plugin がブラウザタブを開きます → Figma OAuth ページで **Authorize** をクリックして認証
2. 認証が完了すると Plugin に戻り、**「Figma ファイルの接続」** ステップへ → Plugin が現在開いているファイルの Figma URL を貼り付け → **「次へ」** をクリック
3. ファイルに複数 page がある場合は、**「読み込む page を選択」** ステップへ → Figma canvas から screens データを読み込みたい page を選択 → 初期セットアップを完了
4. Plugin のメイン画面に遷移

> Figma アカウントが Pro whitelist に登録されている必要あり (§1.3 参照)。未登録の場合、authorize 後にブラウザがエラーを表示します。

#### Essential user

**「無料で始める」** ボタンをクリック

1. Plugin はブラウザを開かず、Figma OAuth も **不要**
2. そのまま Plugin のメイン画面に遷移し、Essential 機能 (screens 閲覧、spec 手動入力、GitHub issue エクスポート) が利用可能
3. Web App、CLI、MCP Server、VSCode Extension、Claude Desktop Extension は **利用不可** — §1.3 参照

> **Pro アカウントなのに誤って Essential を選んでしまった場合?** Plugin はこの選択を記憶するため、次回以降は Welcome 画面を経由せずそのまま Essential 画面に遷移します。Welcome 画面に戻すには、**Figma の clientStorage に保存されているプラン情報を削除する** 必要があります。削除後に Plugin を閉じて再度開くと Welcome 画面が表示されるので、**「Pro アカウントでログイン」** をクリックしてください。

### 2.3 Design Data の同期

Web App、CLI、MCP、VSCode Extension は、Plugin 経由で同期したデータのみを参照できます。

**同期方法:**

1. **作業対象の Figma ファイルで Plugin を起動** → Plugin がバックグラウンドで自動的に screens 一覧を同期 (操作不要)
2. **screen をクリックして詳細画面へ** → その screen の画像と UI 要素が同期される
3. **Preview toolbar の Refresh アイコン (🔄)** (tooltip _「画像を同期・更新」_) をクリックするケース:
   - Figma 側で design を修正した直後、すぐに MoMorph に反映したい
   - Web App に _「デザイン画像が Figma Plugin から同期されていません」_ と表示されている
   - item を変更 / リネーム / 追加したが Plugin が認識していない

### 2.4 Spec 画面への UI 要素読み込み

screen の詳細 (Spec) 画面を開くと、Plugin は **prefix 規約に合致する layer のみ** を読み込みます。prefix が合致しない layer は無視され、UI 要素一覧に表示されません。

**Layer 命名規則:**

| 種別                    | Prefix                   | 例                                                    | Spec への表示                                            |
| ----------------------- | ------------------------ | ----------------------------------------------------- | -------------------------------------------------------- |
| **Item** (現行規約)     | `mms_<name>`             | `mms_button`、`mms_submit_form`                       | ✅ 独立した UI 要素として表示                            |
| **Item** (旧規約)       | `<英数字>_<name>`        | `A_button`、`A1_submit`、`1_label`、`1.1_email_field` | ✅ 表示される。spec に追加する際に `mms_*` へ自動 rename |
| **Media** (画像 / icon) | 名前に `mm_media` を含む | `mm_media`、`mm_media_logo`                           | ✅ Media セクションに表示                                |
| **通常の layer**        | (prefix なし)            | `Rectangle 1`、`Frame 23`、`Button`                   | ❌ 表示されない                                          |

**注意点:**

- Prefix は **大文字小文字を区別しない** (`A_button` ≡ `a_button`、`MMS_action` ≡ `mms_action`)。
- Prefix の後ろの名前には `<`、`>`、`'`、`"` を **使用しないこと** (HTML / SVG エラー回避のため)。
- `mms_*` が現行の標準規約。新規作成時はこの形式を推奨。旧規約 (`1_button`、`A_button`) も互換性あり。Plugin が spec にリンクする際に `mms_*` へ自動 rename。
- visibility off (`visible = false`) の layer は読み込まれない。また、parent frame の `opacity = 0` の場合、その配下の layer もスキップされる。

**Designer 向け推奨ワークフロー:**

1. デザイン作業時から layer 名を `mms_*` 規約で命名 (例: `mms_login_button`、`mms_username_field`)。
2. Plugin で screen 詳細を開き、Spec 画面の item 一覧を確認。
3. item が表示されない? → Figma で layer 名を修正 → Preview toolbar の **Refresh** (🔄) をクリックして再読み込み (§2.3 参照)。

> 正しい prefix を設定したのに item が表示されない場合は §8.3 を参照。

---

## 3. MoMorph Web App

projects / files / screens / specs を一元管理する画面。デザインデータは Figma から Plugin 経由で同期されます。Plugin で同期を実行しないと、Web App や他のプロダクトでデータにアクセスできない場合があるので注意してください。

### 3.1 アクセス

URL: **`https://momorph.ai`** ・ EN / JP / VI 対応 (Settings から切り替え可能)。

### 3.2 ログイン

1. ブラウザで `momorph.ai` を開く
2. **「Login with Figma」** をクリック
3. Figma popup で認可
4. 初回はファイルをリンクするために `fileKey` を入力

VSCode Extension / CLI 用に **GitHub repo** を紐付ける場合: file → **Settings → GitHub → Connect** → repo を選択。

### 3.3 Core Features

sidebar / breadcrumb で画面遷移。下記は URL 確認用のルート一覧 — ログイン後に `momorph.ai/<route>` で開けます。

**Files & Screens**

| Feature          | Route                                      | 用途                                                                    |
| ---------------- | ------------------------------------------ | ----------------------------------------------------------------------- |
| File list        | `/`                                        | 連携済み Figma file 一覧                                                |
| Screen list      | `/files/{fileKey}/screens`                 | ファイル内 screen 一覧 (status / tag / page でフィルタ)                 |
| Screen detail    | `/files/{fileKey}/screens/{screenId}`      | 画像プレビュー＋ design items                                           |
| Item spec editor | `…/screens/{screenId}/items/{itemId}/spec` | validation / navigation / DB mapping を編集 (**AI Generate Spec** 対応) |
| Spec revisions   | `…/items/{itemId}/revs` · `…/revs/{revId}` | 変更履歴の参照とロールバック                                            |
| View all specs   | `…/screens/{screenId}/items/all-specs`     | screen 内の全 spec を read-only テーブルで閲覧                          |
| Screen tags      | `…/screens/{screenId}/tags`                | screen に tag 付与 (functional、bug など)                               |
| Global tags      | `/tags`                                    | システム全体の tag 管理                                                 |

**Screen Sets** (screens をグルーピング)

| Feature          | Route                                          | 用途                                 |
| ---------------- | ---------------------------------------------- | ------------------------------------ |
| Screen Sets list | `/files/{fileKey}/screen-sets`                 | screen sets 一覧                     |
| Create / Edit    | `…/screen-sets/create` · `…/{frameSetId}/edit` | screen set の作成 / 編集             |
| Set detail       | `…/{frameSetId}/list`                          | 1 set 内の screens を表示            |
| Screen in set    | `…/{frameSetId}/screens/{screenId}`            | set のコンテキストから screen を開く |

**ファイル単位の Settings** (`/files/{fileKey}/settings`)

| Feature                | Route                             | 用途                                     |
| ---------------------- | --------------------------------- | ---------------------------------------- |
| Project Overview       | `…/settings/overview`             | プロジェクト概要 (markdown)              |
| GitHub                 | `…/settings/github`               | OAuth ＋ repo 連携 (VSCode Ext / CLI 用) |
| Google                 | `…/settings/google`               | Google OAuth (Syncer Google Sheets 用)   |
| Screen Translation     | `…/settings/screen-translation`   | 多言語化ハブ                             |
| Translation Languages  | `…/screen-translation/languages`  | ファイル単位で言語の有効 / 無効を切替    |
| Translation Dictionary | `…/screen-translation/dictionary` | en ↔ jp ↔ vi の翻訳辞書                |

### 3.4 Screen Status Workflow

各 screen には独立した 4 つの status field (`design_status`、`spec_status`、`dev_status`、`review_status`) があり、それぞれ `Not Started` / `In Progress` / `Done` の 3 段階で進捗を管理します。推奨される進行順:

```
Design → Spec → Dev → Review → Done
```

**どのロールがどの field を更新するか** (推奨ワークフロー):

| Field           | 担当ロール    | `Done` に切り替えるタイミング                       |
| --------------- | ------------- | --------------------------------------------------- |
| `design_status` | Designer      | screen の Figma デザインが完成                      |
| `spec_status`   | BrSE / PM     | screen 内の各 item の spec が承認済み               |
| `dev_status`    | Developer     | screen に関連する feature の実装が完了              |
| `review_status` | QA / Reviewer | review / test が完了し、blocking issue がなくなった |

status field は Screen detail から直接操作します。VSCode Extension はデフォルトで `spec_status = Done` でフィルタするため、Dev は実装可能な screens のみが表示されます。

---

## 4. MoMorph Syncer (Google Add-on — Sun\* 社員専用)

Google Sheets の Add-on で、Sheets ↔ MoMorph 間を双方向に同期します。複数人での collab、コメント、formula を活かして Sheets 上で spec / test case を編集し MoMorph に反映する用途、または逆に team レビュー用に MoMorph の spec を Sheets へエクスポートする用途に適しています。

### 4.1 利用条件

- **Sun\* Asterisk Google Workspace** アカウント (`@sun-asterisk.com`)。個人 Google アカウントは add-on を利用不可。
- MoMorph の **Pro** プラン (§1.3 参照) — Essential ユーザーは Syncer を利用不可。
- MoMorph Syncer add-on がインストール済みの Google Sheets ファイル。

### 4.2 インストール / アクセス

- Sun\* Workspace 配下の Google Sheets を開く → メニュー **Extensions → MoMorph Syncer を検索してインストール**。初回は Google アカウントの authorize ポップアップが表示され、Sheets ファイルへのアクセスと MoMorph backend の呼び出しを許可します。
- **Extensions** メニューに MoMorph Syncer が表示されない場合は、Slack `#con_momorph-support_all` まで連絡。

### 4.3 機能

| Action                  | 説明                                                                  |
| ----------------------- | --------------------------------------------------------------------- |
| **Sync Specifications** | UI 要素定義を Sheets ↔ MoMorph 間で双方向同期                        |
| **Sync Testcases**      | test case を Sheets ↔ MoMorph 間で双方向同期                         |
| **Sync Image**          | Figma の最新デザイン画像を Sheets に in-cell native images として取得 |
| **Sync i18n**           | 多言語コンテンツ (en / jp / vi) を同期                                |

> authorization エラー、sheet 同期失敗、メニュー action の欠落などが発生した場合は §8.5 を参照。

---

## 5. MoMorph CLI

プロジェクトの初期化 / 初期化後のセットアップ、CSV specs / testcases のアップロード、AI agent 用の MCP 設定を担当します。CLI は **download に対応していない** ため、spec / testcases を CSV としてダウンロードしたい場合は AI agent 経由で MCP tools を利用してください (§6 参照)。

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

**Linux / macOS (Bash):**

```bash
curl -fsSL https://raw.githubusercontent.com/momorph/cli/refs/heads/main/scripts/install.sh | bash
```

**Go install:**

```bash
go install github.com/momorph/cli@latest
```

**バージョン確認とアップデート:**

```bash
momorph version
momorph update
```

### 5.2 認証と初期化

**ステップ 1 — ログイン:**

```bash
momorph login          # CLI に code とリンクが表示される。Enter でブラウザ起動
momorph whoami         # アカウント情報の確認
```

**ステップ 2 — プロジェクト初期化:**

```bash
momorph init . --ai claude        # Claude Code
momorph init . --ai copilot       # GitHub Copilot
momorph init . --ai cursor        # Cursor
momorph init . --ai windsurf      # Windsurf
momorph init . --ai gemini        # Gemini
```

> **重要:** repo の root で初期化する際は `.` を指定する。`momorph init my-project` の場合はサブフォルダが新規作成される。

`init` 実行時の自動処理: 最新テンプレートのダウンロード、`.claude/` (または `.github/`、`.cursor/` など) の作成、MCP server の設定、slash commands のインストール。

### 5.3 Command Reference

| Command                                         | 説明                                        |
| ----------------------------------------------- | ------------------------------------------- |
| `momorph login`                                 | GitHub OAuth Device Flow で認証             |
| `momorph logout [--force]`                      | ログアウト、認証情報を削除                  |
| `momorph whoami`                                | アカウント情報＋サブスクリプション          |
| `momorph init <dir> --ai <agent>`               | プロジェクト初期化＋ agent 設定             |
| `momorph upload specs <file.csv>`               | spec CSV をアップロード                     |
| `momorph upload specs <file.csv> --dry-run`     | プレビューのみ (アップロードしない)         |
| `momorph upload testcases <file.csv>`           | test case をアップロード                    |
| `momorph upload testcases <file.csv> --dry-run` | プレビューのみ                              |
| `momorph version`                               | CLI のバージョン                            |
| `momorph update [--check]`                      | CLI を更新 (`--check`: 確認のみ)            |
| `momorph completion <shell>`                    | Shell 補完 (bash / zsh / fish / powershell) |
| `momorph help [command]`                        | ヘルプ                                      |

> **アップロード時の screen 指定方法** (いずれか 1 つを選択):
>
> 1. **規約に沿ったファイル名** — `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` の形式 (`{figmaFrameId}` は frame の Figma node ID。例: `9276:19907-TOP_Channel.csv`)。`/specs`、`/createtestcases`、`/updatetestcases` などの slash command が自動生成するフォーマット。
> 2. **`--screen-id <screenId>` フラグ** — Web URL の `/screens/{screenId}/...` から取得した英数字の MoMorph screenId。convention path 外のファイルの場合は `--file-key` も併せて指定。

---

## 6. MCP Server — AI Tools

`https://mcp.momorph.ai/mcp` でホスト、AI agent が MoMorph / Figma のデータを読み書きするための **31 tools** を提供。ユーザーが直接呼び出すことはなく、AI agent が自動的に利用 (§7.2 の slash commands、または §7.5 Claude Desktop での自然言語 prompt 経由)。各 tool の詳細は別ドキュメント **MoMorph MCP Server — Tools Reference (English)** (ファイル名: `momorph-mcp-tools-reference-en.pdf`) を参照。

slash command が用意されていない重要な tool — AI が MCP 経由でのみ呼び出せるもの:

- `upload_specs` / `download_specs` — spec CSV を MoMorph にアップロード / ダウンロード；2種類のステータス管理に対応：**spec completion**（`spec_progress`：`draft`/`completed`）と **lifecycle**（`active_status`：`active`/`archived`/`deleted`）。ダウンロードは常に `spec_progress` 列を返す；`active_status` 列は `include_deleted=true` 時のみ含まれる。アップロードは両フィールドを受け付け — 未指定の場合はステータスが内容から自動判定される。`active_status=archived` のアイテムは内容変更がある場合は拒否される。
- `upload_test_cases` / `download_test_cases` — test cases CSV のアップロード / ダウンロード
- `list_frame_spec_diffs` — screen の spec を直前 revision と比較

**手動でこれらの tool をトリガーする方法:**

- **Upload** (specs / testcases): CLI (`momorph upload specs|testcases <file.csv>`) を使用、または VSCode Explorer で `.momorph/` 配下の `.csv` を右クリック → 「Upload to MoMorph」(§7.2 参照)
- **Download** ＋ **list_frame_spec_diffs**: AI agent からのみ — Claude Desktop / Code / Cursor で自然言語 prompt、または VSCode メニューの slash command `/downloadspecs`

### 前提条件

- MoMorph Web に紐付いた GitHub アカウント (CLI / MCP 利用に必須)
- repo へのアクセス権 (VSCode Extension / Plugin で repo 連携を行う場合は Admin 権限が必要)

### 方法 1 — CLI で素早くセットアップ

(Claude Desktop の場合は `.mcpb` を利用 — §7.5 参照)

```bash
brew install momorph/tap/momorph-cli
momorph login
momorph init . --ai <agent_name>
```

### 方法 2 — 手動で設定

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

PAT は GitHub の **Settings → Developer settings → Personal access tokens** から、scope を `user` で発行。

### Tools 一覧

全 **31 tools** の詳細 (説明、パラメータ、返り値、使用例) は、本ガイドと一緒に配布される専用リファレンスを参照してください:

📘 **MoMorph MCP Server — Tools Reference (English)** — ファイル名: `momorph-mcp-tools-reference-en.pdf` (Slack channel `#con_momorph-support_all` で配布)。

---

## 7. AI Agent Integrations

### 7.1 概要

| Agent                      | Init Command                   | Prompt Folder                         | Trigger                       | おすすめの用途      |
| -------------------------- | ------------------------------ | ------------------------------------- | ----------------------------- | ------------------- |
| **Claude Code**            | `momorph init . --ai claude`   | `.claude/commands/`                   | Terminal でスラッシュコマンド | CLI、headless       |
| **GitHub Copilot**         | `momorph init . --ai copilot`  | `.github/agents/`、`.github/prompts/` | Copilot Chat / VSCode Ext     | IDE 中心            |
| **Cursor**                 | `momorph init . --ai cursor`   | `.cursor/commands/`                   | Cursor chat                   | All-in-one IDE      |
| **Windsurf**               | `momorph init . --ai windsurf` | (Windsurf 規約に準拠)                 | Windsurf chat                 | Codeium 系          |
| **Gemini**                 | `momorph init . --ai gemini`   | (Gemini CLI 規約に準拠)               | Gemini chat                   | Google スタック     |
| **Claude Desktop** (.mcpb) | §7.5 を参照                    | n/a                                   | 自然言語 prompt               | カジュアル / 非開発 |

### 7.2 GitHub Copilot + VSCode Extension

**Sun\* MoMorph VSCode Extension** (`sun-asterisk.vscode-momorph`): Figma Tree、slash commands、Copilot Chat 用の MCP server 登録を VS Code に統合。

#### 動作要件

- Figma ファイルへの **view または edit** 権限 (unit test 生成のみであれば不要)
- **GitHub Copilot Business**
- VS Code v1.105 以上
- Windows は WSL 必須

#### インストール

VSCode Extension は `.vsix` ファイル形式で配布。最新版は Slack `#con_momorph-support_all` まで問い合わせて入手。

1. 入手した `vscode-momorph-x.y.z.vsix` を開く
2. VSCode → **Extensions** タブ → **`...`** → **Install from VSIX...**
3. ファイルを指定

#### 接続

CLI と同じ GitHub アカウントを使用。事前に `momorph login` を済ませておくこと。

1. Web → Settings → GitHub → connect repo
2. VSCode で repo を開く → Activity Bar の **MoMorph** アイコンをクリック
3. screen 一覧が表示されればセットアップ完了

#### インストール後の使い方

VSCode 内で以下の機能を直接利用可能:

- **Sidebar — Figma view** (`momorph.figma`): screens を **With Design / No Design / Archived** でグルーピング表示。**Screen Sets** と **Components** も表示。**tag、page、status** (4 つの status field: Design / Spec / Dev / Review) でフィルタ / 検索。デフォルトは `Spec Status = Done` でフィルタ。
- **Sidebar — Contexts view** (`momorph.contexts`): `.momorph/contexts/api-docs.yaml` から endpoints を表示。ファイル変更時に自動 refresh。
- **screen の右クリック** (複数選択対応):
  - **Open on Web** / **Copy Screen Information**
  - 15 個の slash commands で AI agent 向け prompt を生成 — 下記の表参照
  - `.github/agents/momorph.*.agent.md` の有無を検出: あり → Copilot Chat を prompt 付きで起動 / なし → prompt をクリップボードにコピー (Claude / Cursor に貼り付け)
- **screen のクリック** → web view で画像プレビューと specs パネル (items / styles / variables / test cases) を並列表示
- **Command Palette** (`Cmd/Ctrl+Shift+P` → `MoMorph:`): Sign In、Search/Filter Screens、Open MoMorph Web、OpenAPI Server (Start/Stop/Restart) など
- **Settings** (`Cmd/Ctrl+,` → `momorph`):
  - `chat.language` & `chat.outputFileLanguage` (English / Vietnamese / Japanese)
  - `api.baseUrl`、`api.headers`、`mcpServers`、`github.remoteName`、`github.useEnterprise`
- **Copilot Chat**: `/` で slash commands、`#` で 7 個の Language Model Tools — `momorph_callMcpTool`、`momorph_compareScreenshots`、`momorph_downloadFigmaImage`、`momorph_getPreferenceInstructions`、`momorph_getUserPreferences`、`momorph_listApiEndpoints`、`momorph_getApiEndpoint`
- **Explorer**: `.momorph/specs/` または `.momorph/testcases/` 配下の `.csv` を右クリック → **Upload to MoMorph**
- **MCP servers** がデフォルトで登録 (`momorph.mcpServers` の key): `morpheus`、`context7`、`testViewpoints`

#### Context menu の Slash commands

15 commands を 2 グループに分類。**Agent file** 列は、独立した prompt ファイル (`.claude/commands/momorph.*.agent.md` または `.github/agents/momorph.*.agent.md`) を持つ commands を示す — Claude Code / Cursor で実行可能。agent file を持たない commands は VSCode メニュー経由のみ動作 (動的 prompt)。

**Flow** — spec → plan → implement のワークフロー:

| Command          | Agent file | Action                                                      |
| ---------------- | :--------: | ----------------------------------------------------------- |
| `/constitution`  |     ✅     | constitution の初期化 / 更新 (rules、stack)                 |
| `/specify`       |     ✅     | screen から `spec.md` ＋ `design-style.md` ＋ assets を生成 |
| `/reviewspecify` |     ❌     | spec.md ＆ design-style.md のレビュー / 改善                |
| `/plan`          |     ✅     | spec ＋ design-style ＋ constitution から plan を生成       |
| `/reviewplan`    |     ❌     | plan のレビュー / 改善                                      |
| `/tasks`         |     ✅     | plan を `tasks.md` に分解                                   |
| `/implement`     |     ✅     | `tasks.md` に従って実装                                     |

**Context** — Figma からデータを生成:

| Command            | Agent file | Action                                                           |
| ------------------ | :--------: | ---------------------------------------------------------------- |
| `/specs`           |     ✅     | screen から 22 列の CSV spec を生成                              |
| `/createtestcases` |     ✅     | test cases (Accessing / GUI / Function)、screen 1 つにつき 1 CSV |
| `/updatetestcases` |     ✅     | spec 変更時に test cases を更新                                  |
| `/apispec`         |   ✅ \*    | OpenAPI specs ＋ backend test cases                              |
| `/database`        |     ✅     | SQL Schema ＋ Mermaid ERD                                        |
| `/screenflow`      |     ✅     | `SCREENFLOW.md` を生成                                           |
| `/downloadspecs`   |     ❌     | MoMorph から CSV spec をダウンロード (MCP tool 経由)             |
| `/convertspecs`    |     ❌     | spec markdown → ローカル CSV に変換 (アップロードなし)           |

\* Agent file 名は `momorph.apispecs.agent.md` (複数形)、VSCode メニューでは `apispec` (単数形) でトリガー。

#### Agent file 経由のみ利用可能な Slash commands (VSCode メニューにはなし)

`momorph init . --ai <agent>` でインストール (§7.3-§7.4 参照)、terminal / chat に直接入力:

| Command          | Action                                              |
| ---------------- | --------------------------------------------------- |
| `/commit`        | Conventional Commits に従って commit                |
| `/prdescription` | テンプレートに沿った PR description                 |
| `/ship`          | Commit ＋ push ＋ PR 作成を 1 コマンドに統合        |
| `/reviewcode`    | PR と ticket spec を比較レビュー、severity 別に報告 |
| `/setupe2e`      | Playwright を初期化 (repo ごとに 1 回)              |
| `/writee2e`      | test plan から `.spec.ts` を生成                    |
| `/reviewe2e`     | POM、locator、data、performance のレビュー          |

> Extension がデータを表示しない場合は、通知の **`See Error`** をクリックして output channel を開いて確認。

### 7.3 Claude Code

```bash
momorph init . --ai claude
```

`.claude/commands/momorph.*.agent.md` を生成。Claude Code の terminal を開き、スラッシュコマンドを入力するだけで利用可能。MCP の設定は `~/.claude.json` に追加。

### 7.4 Cursor / Windsurf / Gemini

```bash
momorph init . --ai cursor       # .cursor/commands/
momorph init . --ai windsurf
momorph init . --ai gemini
```

prompt ファイルは各 agent の規約に従って配置。MCP の設定は対応する config ファイルに自動的にマージ。

### 7.5 Claude Desktop Extension (.mcpb)

`.mcpb` バンドルでローカルの Claude Desktop に MoMorph MCP をワンファイルインストール — Claude Desktop と `mcp.momorph.ai/mcp` を接続。

#### Compatibility

- macOS / Windows / Linux ・ Node.js 18 以上 ・ MCP v1.x 対応 Claude Desktop

#### インストール

1. Slack `#con_momorph-support_all` まで連絡し、最新の `momorph-mcp.mcpb` を入手する。
2. Claude Desktop → **Settings** → **Extensions** → **Advanced Settings** → **Install Extension**
3. ファイルを指定 → **Install** → **GitHub PAT** (scope: `user`) を入力 → **Save** → **Enable**

#### 動作確認

prompt: _「List all frames in this Figma file: {fileKey}」_ — Claude が自動的に `list_frames` を呼び出します。MCP の debug log を確認する場合は Developer Mode を有効化。

> **`.mcpb` vs MCP Cloud:** `.mcpb` は Claude Desktop のみを使うユーザー向け。Multi-IDE setup (VSCode + Claude Code + Cursor) なら `momorph init` 経由の MCP Cloud (§5)。

---

## 8. よくあるトラブル

### 8.1 CLI

**`momorph login` が完了しない** — firewall / VPN が `github.com/login/device` をブロックしていないか確認。code を直接 `https://github.com/login/device` に入力する方法でも認証可能。

### 8.2 Web App

**Figma のログイン失敗 / popup ブロック:**

- `momorph.ai` からの popup を許可
- ブラウザの private mode を試す (拡張機能が OAuth callback を妨げる場合あり)
- Figma アカウントが有効な状態か確認

**ログイン後にファイルが表示されない** — popup から Figma URL の `fileKey` を入力。スキップした場合は `/` → 「Add file」→ fileKey を貼り付け。

### 8.3 Figma Plugin

**Item が認識されない** — layer name に `mms_*` prefix が正しく設定されているか確認 (§2.4 参照)。

**Plugin が真っ白 / spinner が止まらない:**

- Figma から `momorph.ai` にアクセスできるか (network / VPN) 確認
- Web からログアウト → 再ログイン → `Cmd/Ctrl+Shift+P` → `Reload` で plugin をリロード

### 8.4 VSCode Extension

**MCP に接続できない** — 未ログインまたはトークン期限切れの可能性:

```bash
momorph login
momorph whoami
```

その後 `Ctrl+Shift+P → Developer: Reload Window` を実行。

**Tree view に screens が表示されない:**

- repo が Web 側で連携済みか確認 (Settings → GitHub)
- Figma Tree の **Refresh** をクリック
- エラーが出ている → 通知の **`See Error`** から詳細を確認

**Context menu から Copilot Chat が起動しない** — Extension は `.github/agents/momorph.*.agent.md` の有無で Copilot プロジェクトを判定。Claude Code プロジェクトなどで該当ファイルがない場合は prompt がクリップボードにコピーされるので、Claude などに手動で貼り付け。

### 8.5 Syncer (Google Add-on)

**Extensions メニューに MoMorph Syncer が表示されない** — add-on が当該 Sheets ファイルにデプロイされていない。Slack `#con_momorph-support_all` まで連絡。

**action 実行時に「Missing authentication token」** — Google session 期限切れ。`@sun-asterisk.com` メールで Google アカウントに再ログインし、Sheets タブをリフレッシュして再試行。

**「Cannot access spreadsheet」** — ファイル共有権限が不足。確認項目:

- Sheets ファイルが Sun\* Workspace 配下にあるか (個人 private file は非対応)。
- 現在のアカウントが **Editor** 権限か (Viewer では MoMorph に同期不可)。

**「Invalid Figma URL」** — URL フォーマットが不正。ブラウザのアドレスバーから Figma リンクを再度コピーして貼り付け (特定 frame を同期する場合は `node-id` も含める)。

**「Failed to sync data」** — MoMorph backend または network の一時的な障害。数分後に再試行。繰り返す場合は team support まで連絡。

**同期後にセル内に画像が表示されない** — convert in-cell image はバックグラウンド (fire-and-forget) で実行。10〜30 秒待ってから sheet を再読み込み。それでも失敗する場合はメニューから **Sync Image** を再実行。

### 8.6 MCP / Slash Commands

**spec アップロード時に「Frame not found」** — `--screen-id` の指定漏れ、または Figma node ID (例: `32355:420279`) を MoMorph screenId と混同しているケースが多い。次のいずれかで対処 (§5.3 参照):

- `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` の規約に沿ったファイル名にして、フラグなしでアップロード。
- もしくは `--screen-id` フラグを指定:
  ```bash
  momorph upload specs <file.csv> --screen-id <alphanumeric-screenId>
  ```

**spec ダウンロード時に「Frame not found」** (AI agent が MCP `download_specs` を呼ぶケース) — agent が Figma node ID を screenId として渡している。Web URL の `/screens/{screenId}/...` から正しい screenId を取得し、prompt をやり直す。

**Claude Desktop Extension が tools を呼び出さない:**

- Settings → Extensions で MoMorph の status が `Enabled` か
- GitHub PAT が有効 (scope: `user`) か
- Developer Mode を有効にして log を確認
- prompt 内に fileKey / screenId が明記されているか

**MCP の timeout / 応答が遅い:**

- `mcp.momorph.ai` への接続状況を確認
- 大規模な slash command (item の多い screen に対する `/momorph.specs` など) は 30〜60 秒かかる場合あり
- 何度も失敗する場合は `momorph login` でトークンを更新

**`x-github-token` invalid / 401:**

- PAT が revoke / 期限切れ → 新しい PAT を発行 (scope: `user`)、`~/.claude.json` などの MCP config を更新
- `momorph init` を使用する場合は `momorph login` を実行することで、トークンが自動的に config にマージされる

---

_その他の問い合わせは Slack `#con_momorph-support_all` まで。_

# MoMorph — User Guide

> 📩 **Contact & support — MoMorph team**
>
> - Slack: `#con_momorph-support_all`
> - Email: `momorph-admin@sun-asterisk.com`

---

## Table of Contents

<details>
<summary><strong>1. <a href="#1-overview">Overview</a></strong></summary>

- [1.1 Ecosystem (7 products)](#11-ecosystem-7-products)
- [1.2 Data flow diagram](#12-data-flow-diagram)
- [1.3 Prerequisites](#13-prerequisites)
    - [Accounts](#accounts)
    - [Software / OS](#software--os)

</details>

<details>
<summary><strong>2. <a href="#2-momorph-figma-plugin">MoMorph Figma Plugin</a></strong></summary>

- [2.1 Installation](#21-installation)
- [2.2 Sign in](#22-sign-in)
    - [Pro user](#pro-user)
    - [Essential user](#essential-user)
- [2.3 Sync Design Data](#23-sync-design-data)
- [2.4 Loading design items into the Spec screen](#24-loading-design-items-into-the-spec-screen)

</details>

<details>
<summary><strong>3. <a href="#3-momorph-web-app">MoMorph Web App</a></strong></summary>

- [3.1 Access](#31-access)
- [3.2 Sign in](#32-sign-in)
- [3.3 Core Features](#33-core-features)
- [3.4 Screen Status Workflow](#34-screen-status-workflow)

</details>

<details>
<summary><strong>4. <a href="#4-momorph-syncer-google-add-on">MoMorph Syncer (Google Add-on)</a></strong></summary>

- [4.1 Usage requirements](#41-usage-requirements)
- [4.2 Installation / Access](#42-installation--access)
- [4.3 Features](#43-features)

</details>

<details>
<summary><strong>5. <a href="#5-momorph-cli">MoMorph CLI</a></strong></summary>

- [5.1 Installation](#51-installation)
- [5.2 Authentication & Initialization](#52-authentication--initialization)
- [5.3 Command Reference](#53-command-reference)

</details>

<details>
<summary><strong>6. <a href="#6-mcp-server--ai-tools">MCP Server — AI Tools</a></strong></summary>

- [Prerequisites](#prerequisites)
- [Option 1 — Quick setup via CLI](#option-1--quick-setup-via-cli)
- [Option 2 — Manual configuration](#option-2--manual-configuration)
- [Tools list](#tools-list)

</details>

<details>
<summary><strong>7. <a href="#7-ai-agent-integrations">AI Agent Integrations</a></strong></summary>

- [7.1 Overview](#71-overview)
- [7.2 GitHub Copilot + VSCode Extension](#72-github-copilot--vscode-extension)
- [7.3 Claude Code](#73-claude-code)
- [7.4 Cursor / Windsurf / Gemini](#74-cursor--windsurf--gemini)
- [7.5 Claude Desktop Extension (.mcpb)](#75-claude-desktop-extension-mcpb)

</details>

<details>
<summary><strong>8. <a href="#8-common-issues">Common Issues</a></strong></summary>

- [8.1 CLI](#81-cli)
- [8.2 Web App](#82-web-app)
- [8.3 Figma Plugin](#83-figma-plugin)
- [8.4 VSCode Extension](#84-vscode-extension)
- [8.5 Syncer (Google Sheets Add-on)](#85-syncer-google-sheets-add-on)
- [8.6 MCP / Slash Commands](#86-mcp--slash-commands)

</details>

---

## 1. Overview

**MoMorph** is Sun\* Asterisk's AI-Driven Development ecosystem, taking Figma design / Specs as the starting point for the entire software lifecycle:

```
Figma Design & Specs → Test Cases → Code
```

### 1.1 Ecosystem (7 products)

| #   | Component                    | Purpose                                                                                       | Platform               |
| --- | ---------------------------- | --------------------------------------------------------------------------------------------- | ---------------------- |
| 1   | **Figma Plugin**             | Sync design data from Figma into MoMorph, manage design data, create spec documents, etc.     | Figma                  |
| 2   | **Web App**                  | Manage projects, store screens/specs/test cases                                               | Browser                |
| 3   | **Syncer (Google Add-on)**   | Edit specs/test cases in Google Sheets and sync them two-way with MoMorph                     | Google Sheets          |
| 4   | **CLI**                      | Initialize projects, configure MCP, upload CSV specs/test cases                               | Terminal               |
| 5   | **VSCode Extension**         | Display design/spec, integrate the MCP server, Figma Tree and slash commands for Copilot Chat | VS Code                |
| 6   | **MCP Server**               | Provide AI tools for agents to read/write MoMorph & Figma data                                | Automatic via AI agent |
| 7   | **Claude Desktop Extension** | `.mcpb` bundle — use MoMorph MCP from Claude Desktop                                          | Claude Desktop         |

### 1.2 Data flow diagram

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

### 1.3 Prerequisites

#### Accounts

**MoMorph user plans (Essential vs Pro)** — determine access scope across the entire ecosystem:

| Plan          | Access scope                                                                                                                                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Essential** | **Plugin only** — Can use the following features: manage screens, enter specs manually, export GitHub issues. The other sub-products (Web App, Syncer, CLI, MCP Server, VSCode Extension, Claude Desktop Extension) **are not accessible** |
| **Pro**       | **Entire ecosystem** — Plugin (full features) + Web App + Syncer + CLI + MCP Server + VSCode Extension + Claude Desktop Extension                                                                                                          |

**How to become a Pro user:**

- Users whose email belongs to the Sun\* company domain are Pro accounts by default.
- Other emails: contact the MoMorph team to be granted a Pro account.

**Platform accounts required for each product:**

| Product                  | Account | Requirement                                                                                                                                                         |
| ------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Figma Plugin             | Figma   | Follow [Figma's plugin usage requirements](https://help.figma.com/hc/en-us/articles/360039958474) (a Viewer seat can still run the plugin in personal Drafts files) |
| Web App                  | Figma   | Any seat                                                                                                                                                            |
| Syncer (Google Add-on)   | Google  | A **Sun\* company Google Workspace** account                                                                                                                        |
| CLI                      | GitHub  | `momorph login`                                                                                                                                                     |
| MCP Server               | GitHub  | PAT scope `user`                                                                                                                                                    |
| VSCode Extension         | GitHub  | Same account as the CLI + **Copilot Business** (Free is not enough)                                                                                                 |
| Claude Desktop Extension | GitHub  | PAT scope `user`                                                                                                                                                    |

#### Software / OS

| Product                  | Requirement                                                                      |
| ------------------------ | -------------------------------------------------------------------------------- |
| Figma Plugin             | Figma Desktop or figma.com                                                       |
| Web App                  | Latest Chrome / Firefox / Safari / Edge                                          |
| Syncer (Google Add-on)   | Google Sheets in the browser (Sun\* Workspace)                                   |
| CLI                      | macOS / Linux / Windows (install via Homebrew / Chocolatey / scripts — see §5.1) |
| VSCode Extension         | VS Code ≥ v1.105 · Windows: WSL                                                  |
| Claude Desktop Extension | Claude Desktop supporting MCP v1.x · Node.js ≥ 18 · macOS/Windows/Linux          |

---

## 2. MoMorph Figma Plugin

The plugin runs inside Figma (Desktop/Browser) and provides the same features as the Web App (§3) + syncing design data (screens, items, styles, variables, media) into the MoMorph DB.

### 2.1 Installation

1. Open Figma → **Plugins → Manage plugins** → search for "MoMorph"
2. Click **Install** → Run

### 2.2 Sign in

Opening the Plugin for the first time (or when the session has expired) brings up the **Welcome** screen with 2 sign-in buttons corresponding to 2 flows — the user picks one of the two depending on their account type:

#### Pro user

Click the **"Sign in with Pro account"** button

1. The Plugin opens a browser tab → click **Authorize** on the Figma OAuth page to authenticate the account.
2. After successful authentication, return to the Plugin, which moves to the **"Connect Figma File"** step — paste the Figma URL of the file the plugin is open in → click **"Continue"**.
3. If the file has multiple pages, the Plugin moves to the **"Select pages to load"** step — choose the pages whose screen data you want to load from the Figma canvas → finish setup.
4. Enter the Plugin's main screen.

> The Figma account must be a Pro account (see §1.3). If it is not, the browser will show an error after authorization.

#### Essential user

Click the **"Start for free"** button

1. The Plugin does **not** open a browser and does **not** require Figma OAuth.
2. Go straight to the Plugin's main screen with Essential features (browse screens, enter specs manually, export GitHub issues).
3. The Web App, CLI, MCP Server, VSCode Extension, and Claude Desktop Extension are **not** accessible — see §1.3.

### 2.3 Sync Design Data

The Web App, CLI, MCP, and VSCode Extension can only see design data after it has been synced through the Plugin.

**How to sync:**

1. **Open the Plugin in the Figma file you want to work on** → the Plugin automatically syncs the list of screens in the background, with no action needed.
2. **Click a screen to enter its detail view** → that screen's image and design items are synced.
3. **Click the Refresh icon** (🔄) on the **Preview toolbar** when:
    - You have just edited a design in Figma and want to update it to MoMorph immediately.
    - The Web App shows _"The design image has not been synced from the Figma Plugin"_.
    - An item was changed/renamed/added and the Plugin has not recognized it yet.

### 2.4 Loading design items into the Spec screen

When you open the detail (Spec) view of a screen, the Plugin **only loads layers with the correct prefix convention** in the Figma layer name. Layers that do not match the prefix are skipped and do not appear in the items list.

**Layer naming rules:**

| Type                          | Prefix                     | Example                                               | Shown in Spec                                                 |
| ----------------------------- | -------------------------- | ----------------------------------------------------- | ------------------------------------------------------------- |
| **Item** (current convention) | `mms_<name>`               | `mms_button`, `mms_submit_form`                       | ✅ Shown as a standalone item                                 |
| **Item** (legacy convention)  | `<letter/digit>_<name>`    | `A_button`, `A1_submit`, `1_label`, `1.1_email_field` | ✅ Shown; automatically renamed to `mms_*` when added to spec |
| **Media** (image/icon)        | name containing `mm_media` | `mm_media`, `mm_media_logo`                           | ✅ Shown in the Media section                                 |
| **Regular layer**             | (no prefix)                | `Rectangle 1`, `Frame 23`, `Button`                   | ❌ Not shown                                                  |

**Notes:**

- The prefix is **case-insensitive** (`A_button` ≡ `a_button`, `MMS_action` ≡ `mms_action`).
- The name after the prefix **must not contain the characters** `<`, `>`, `'`, `"` (to avoid HTML/SVG errors).
- The `mms_*` convention is the current standard — using it for new layer names is recommended. Layers with legacy prefixes (`1_button`, `A_button`) remain compatible; the Plugin will automatically rename them to `mms_*` when linking them into a spec.
- Layers with visibility turned off (`visible = false`) will not be loaded. Additionally, if the parent frame has `opacity = 0`, its child layers are also skipped.

**Automatically generating the list with AI Generate:**

Besides setting prefixes manually, on the Spec screen the user can use the **AI Generate** feature to have AI analyze the Figma design and create the design items list automatically. After the AI finishes, the user should review and edit/add items as needed.

**Recommended workflow for Designers:**

1. Name layers in Figma with the `mms_*` prefix while designing (e.g. `mms_login_button`, `mms_username_field`).
2. Open the Plugin → enter the detail view → check the item list on the Spec screen.
3. Missing an item? Fix the layer name in Figma → click **Refresh** (🔄) on the Preview toolbar (see §2.3) to reload.

> See §8.3 if you set the prefix correctly but the item still does not appear.

---

## 3. MoMorph Web App

The hub for managing projects/files/screens/specs. Design data is synced from Figma through the Plugin first. If the user does not sync from the Plugin, they may run into issues accessing data on the Web and in other products.

### 3.1 Access

URL: **`https://momorph.ai`** · Supports EN/JP/VI (change in Settings).

### 3.2 Sign in

1. Open `momorph.ai`
2. Click **"Login with Figma"**
3. Authorize Figma

### 3.3 Core Features

Navigate via the sidebar/breadcrumb after signing in at `momorph.ai`.

**Files & Screens**

| Feature          | Purpose                                                         |
| ---------------- | --------------------------------------------------------------- |
| File list        | List of linked Figma files                                      |
| Screen list      | Screens in a file (filter by status, tag, page)                 |
| Screen detail    | Image preview + design items                                    |
| Item spec editor | Edit validation/navigation/DB mapping; has **AI Generate Spec** |
| Spec revisions   | Version history + rollback                                      |
| View all specs   | Read-only table viewing all specs in a screen                   |
| Screen tags      | Tag a screen (functional, bug…)                                 |
| Global tags      | Manage system-wide tags                                         |

**Screen Sets** (group screens into sets)

| Feature          | Purpose                              |
| ---------------- | ------------------------------------ |
| Screen Sets list | List of screen sets                  |
| Create / Edit    | Create / edit a screen set           |
| Set detail       | View screens within a set            |
| Screen in set    | Open a screen from the set's context |

**File-level Settings**

| Feature                | Purpose                                     |
| ---------------------- | ------------------------------------------- |
| Project Overview       | Project description (markdown)              |
| GitHub                 | OAuth + link repo (for VSCode Ext / CLI)    |
| Google                 | Google OAuth (for the Syncer Google Sheets) |
| Screen Translation     | Multilingual hub                            |
| Translation Languages  | Enable/disable languages for the file       |
| Translation Dictionary | Translation table en↔jp↔vi                |

### 3.4 Screen Status Workflow

Each screen has 4 independent status fields (`design_status`, `spec_status`, `dev_status`, `review_status`), each with 3 values (`Not Started` / `In Progress` / `Done`). Recommended sequence:

```
Design → Spec → Dev → Review → Done
```

The status fields are edited directly in the Screen detail. The VSCode Extension filters by `spec_status = Done` by default, so Dev only sees screens that are ready to implement.

---

## 4. MoMorph Syncer (Google Add-on)

An add-on for Google Sheets that syncs two-way between Sheets ↔ MoMorph. Suitable when you need to edit specs / test cases in Sheets (multi-person collaboration, comments, formulas) and push them back to MoMorph, or conversely push specs from MoMorph to Sheets for the team to review.

### 4.1 Usage requirements

- A **Sun\* company Google Workspace** account. Personal Google accounts **cannot** access the add-on.
- A **Pro** plan on MoMorph (see §1.3) — Essential users cannot use the Syncer.
- A Google Sheets file that has the MoMorph Syncer add-on installed.

### 4.2 Installation / Access

- Open a Google Sheets within the Sun\* Workspace → menu **Extensions → search for and install MoMorph Syncer**. The first time, a popup will request authorization of your Google account so the add-on can access the Sheets file and call the MoMorph backend.
- If the MoMorph Syncer menu does not appear under **Extensions**, contact the MoMorph team.

### 4.3 Features

| Action                  | Description                                                                   |
| ----------------------- | ----------------------------------------------------------------------------- |
| **Sync Specifications** | Sync design item definitions two-way between Sheets ↔ MoMorph                |
| **Sync Testcases**      | Sync test cases two-way between Sheets ↔ MoMorph                             |
| **Sync Image**          | Pull the latest design images from Figma into Sheets as in-cell native images |
| **Sync i18n**           | Sync multilingual content (en / jp / vi)                                      |

> See §8.5 if you hit authorization errors, the sheet fails to sync, or the menu is missing an action.

---

## 5. MoMorph CLI

Install/init a project, upload CSV specs/test cases, configure MCP for an AI agent. Note: the CLI does **not** support download — to download specs/test cases as CSV, use an AI agent through the MCP tools (see §6).

### 5.1 Installation

**macOS / Linux (Homebrew — recommended):**

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

**Check / Update:**

```bash
momorph version
momorph update
```

### 5.2 Authentication & Initialization

**Step 1 — Sign in:**

```bash
momorph login          # CLI shows a code + link; press Enter to open the browser
momorph whoami         # check the account
```

**Step 2 — Init project:**

```bash
momorph init . --ai claude        # Claude Code
momorph init . --ai copilot       # GitHub Copilot
momorph init . --ai cursor        # Cursor
momorph init . --ai windsurf      # Windsurf
momorph init . --ai gemini        # Gemini
```

> **Important:** Use `.` to init in the repo root. `momorph init my-project` will create a subfolder.

`init` automatically: downloads the latest template, creates `.claude/` (or `.github/`, `.cursor/`…), configures the MCP server, and installs slash commands.

### 5.3 Command Reference

| Command                                         | Description                                 |
| ----------------------------------------------- | ------------------------------------------- |
| `momorph login`                                 | Auth GitHub OAuth Device Flow               |
| `momorph logout [--force]`                      | Log out, delete credentials                 |
| `momorph whoami`                                | Account + subscription                      |
| `momorph init <dir> --ai <agent>`               | Init project + configure agent              |
| `momorph upload specs <file.csv>`               | Upload spec CSV                             |
| `momorph upload specs <file.csv> --dry-run`     | Preview, no upload                          |
| `momorph upload testcases <file.csv>`           | Upload test cases                           |
| `momorph upload testcases <file.csv> --dry-run` | Preview                                     |
| `momorph version`                               | CLI version                                 |
| `momorph update [--check]`                      | Update the CLI (`--check`: check only)      |
| `momorph completion <shell>`                    | Shell completion (bash/zsh/fish/powershell) |
| `momorph help [command]`                        | Help                                        |

> **How to specify the screen when uploading** (pick one):
>
> 1. **Correct file-name convention** — `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv`, where `{figmaFrameId}` is the Figma node ID of the frame (e.g. `9276:19907-TOP_Channel.csv`). This is the format that slash commands such as `/specs`, `/createtestcases`, `/updatetestcases` generate automatically.
> 2. **Flag `--screen-id <screenId>`** — the alphanumeric MoMorph screenId, taken from the Web URL (`/screens/{screenId}/...`); add `--file-key` if the file is outside the convention path.

---

## 6. MCP Server — AI Tools

Hosted at `https://mcp.momorph.ai/mcp`, providing tools for AI agents to read/write MoMorph & Figma data. Users **do not call it directly** — the AI agent uses it on its own (via slash commands in §7.2 or via natural-language prompts in Claude Desktop §7.5). A detailed description of each tool is provided in the detailed MCP Tools usage guide.

Some important tools have **no corresponding slash command** — only the AI calls them via MCP:

- `upload_specs` / `download_specs` — upload/download spec CSVs to/from MoMorph; support managing 2 types of status: **spec completion** (`spec_progress`: `draft`/`completed`) and **lifecycle** (`active_status`: `active`/`archived`/`deleted`). Download always returns the `spec_progress` column; the `active_status` column only appears when using `include_deleted=true`. Upload accepts both fields — if not passed, the status is computed automatically from the content. An item with `active_status=archived` will be rejected if its content changes.
- `upload_test_cases` / `download_test_cases` — upload/download test-case CSVs
- `list_frame_spec_diffs` — compare a screen's spec with the previous revision

**How to trigger the above tools manually:**

- **Upload** (specs/test cases): use the CLI (`momorph upload specs|testcases <file.csv>`) or right-click a `.csv` file in `.momorph/` in the VSCode Explorer → "Upload to MoMorph" (see §7.2)
- **Download** + **list_frame_spec_diffs**: only via an AI agent — a natural-language prompt in Claude Desktop/Code/Cursor, or the `/downloadspecs` slash command in the VSCode menu

### Prerequisites

- A GitHub account linked to MoMorph Web (for CLI / MCP)
- Repo access (for the VSCode Extension / Plugin, if the account has Admin)

### Option 1 — Quick setup via CLI

(Claude Desktop uses `.mcpb` — see §7.5)

```bash
brew install momorph/tap/momorph-cli
momorph login
momorph init . --ai <agent_name>
```

### Option 2 — Manual configuration

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

Create a PAT with scope `user` at GitHub → Settings → Developer settings → Personal access tokens.

### Tools list

For detailed descriptions, parameters, return types, and usage examples for all of the MCP server's tools, please refer to the detailed MCP Tools usage guide.

---

## 7. AI Agent Integrations

### 7.1 Overview

| Agent                      | Init Command                   | Prompt Folder                         | Trigger                   | Best for            |
| -------------------------- | ------------------------------ | ------------------------------------- | ------------------------- | ------------------- |
| **Claude Code**            | `momorph init . --ai claude`   | `.claude/commands/`                   | Slash in the terminal     | CLI, headless       |
| **GitHub Copilot**         | `momorph init . --ai copilot`  | `.github/agents/`, `.github/prompts/` | Copilot Chat / VSCode Ext | IDE-centric         |
| **Cursor**                 | `momorph init . --ai cursor`   | `.cursor/commands/`                   | Cursor chat               | All-in-one IDE      |
| **Windsurf**               | `momorph init . --ai windsurf` | (per Windsurf)                        | Windsurf chat             | Codeium             |
| **Gemini**                 | `momorph init . --ai gemini`   | (per Gemini CLI)                      | Gemini chat               | Google stack        |
| **Claude Desktop** (.mcpb) | see §7.5                       | n/a                                   | Natural-language prompt   | Casual / non-coding |

### 7.2 GitHub Copilot + VSCode Extension

**Sun\* MoMorph VSCode Extension** (`sun-asterisk.vscode-momorph`): Figma Tree, slash commands, and registering the MCP server for Copilot Chat.

#### Requirements

- **View or edit** access to the Figma file (not needed if you only generate unit tests)
- **GitHub Copilot Business**
- VS Code ≥ v1.105
- Windows: WSL

#### Installation

The VSCode Extension is distributed as a `.vsix` file. Contact the MoMorph team to get the latest file.

1. Open the file `vscode-momorph-x.y.z.vsix`
2. VSCode → the **Extensions** tab → **`...`** → **Install from VSIX...**
3. Select the file

#### Connect

Use the same GitHub account as the CLI. Make sure you have run `momorph login`.

1. Web → Settings → GitHub → connect repo
2. VSCode → open the repo → click the **MoMorph** icon in the Activity Bar
3. The screen list appears → setup is OK

#### After installation

Explore directly in VSCode:

- **Sidebar — Figma view** (`momorph.figma`): browse screens grouped by **With Design / No Design / Archived**, plus **Screen Sets** and **Components**. Filter/Search by **tag, page, status** (4 status fields: Design / Spec / Dev / Review). Filters by `Spec Status = Done` by default
- **Sidebar — Contexts view** (`momorph.contexts`): displays endpoints from `.momorph/contexts/api-docs.yaml`, auto-refreshing when the file changes
- **Right-click a screen** (multi-select supported):
    - **Open on Web** / **Copy Screen Information**
    - 15 slash commands that generate ready-made prompts for the AI agent — see the table below
    - Detect `.github/agents/momorph.*.agent.md` in the repo: present → open Copilot Chat with the prompt; absent → copy the prompt to the clipboard (paste into Claude/Cursor)
- **Click a screen** → a web view with an image-preview panel + a specs panel (with items / styles / variables / test cases)
- **Command Palette** (`Cmd/Ctrl+Shift+P` → `MoMorph:`): Sign In, Search/Filter Screens, Open MoMorph Web, OpenAPI Server (Start/Stop/Restart)…
- **Settings** (`Cmd/Ctrl+,` → `momorph`):
    - `chat.language` & `chat.outputFileLanguage` (English / Vietnamese / Japanese)
    - `api.baseUrl`, `api.headers`, `mcpServers`, `github.remoteName`, `github.useEnterprise`
- **Copilot Chat**: `/` to see slash commands; `#` to see 7 Language Model Tools — `momorph_callMcpTool`, `momorph_compareScreenshots`, `momorph_downloadFigmaImage`, `momorph_getPreferenceInstructions`, `momorph_getUserPreferences`, `momorph_listApiEndpoints`, `momorph_getApiEndpoint`
- **Explorer**: right-click a `.csv` in `.momorph/specs/` or `.momorph/testcases/` → **Upload to MoMorph**
- **Pre-configured MCP servers** (in `momorph.mcpServers`): `momorph`, `context7`, `testViewpoints`

#### Slash commands in the context menu

15 commands split into 2 groups. The **Agent file** column marks commands that have a standalone prompt file (`.claude/commands/momorph.*.agent.md` or `.github/agents/momorph.*.agent.md`) — they can run in Claude Code/Cursor; commands without an agent file only work through the VSCode menu (dynamically generated prompt).

**Flow** — the spec → plan → implement process:

| Command          | Agent file | Action                                                        |
| ---------------- | :--------: | ------------------------------------------------------------- |
| `/constitution`  |     ✅     | Init/update the constitution (rules, stack)                   |
| `/specify`       |     ✅     | Generate `spec.md` + `design-style.md` + assets from a screen |
| `/reviewspecify` |     ❌     | Review/improve spec.md & design-style.md                      |
| `/plan`          |     ✅     | Plan from spec + design-style + constitution                  |
| `/reviewplan`    |     ❌     | Review/improve the plan                                       |
| `/tasks`         |     ✅     | Break the plan down into `tasks.md`                           |
| `/implement`     |     ✅     | Code per `tasks.md`                                           |

**Context** — generate data from Figma:

| Command            | Agent file | Action                                             |
| ------------------ | :--------: | -------------------------------------------------- |
| `/specs`           |     ✅     | A 22-column CSV spec from a screen                 |
| `/createtestcases` |     ✅     | Test cases (Accessing/GUI/Function), 1 CSV/screen  |
| `/updatetestcases` |     ✅     | Update test cases when the spec changes            |
| `/apispec`         |   ✅ \*    | OpenAPI specs + backend test cases                 |
| `/database`        |     ✅     | SQL schema + Mermaid ERD                           |
| `/screenflow`      |     ✅     | Generate `SCREENFLOW.md`                           |
| `/downloadspecs`   |     ❌     | Download a spec CSV from MoMorph (via an MCP tool) |
| `/convertspecs`    |     ❌     | Convert spec markdown → CSV locally (no upload)    |

\* The agent file is named `momorph.apispecs.agent.md` (plural), while the VSCode menu triggers it under the name `apispec` (singular).

#### Slash commands available only via agent file (not in the VSCode menu)

Installed via `momorph init . --ai <agent>` (see §7.3–§7.4), typed directly in the terminal/chat:

| Command          | Action                                             |
| ---------------- | -------------------------------------------------- |
| `/commit`        | Commit following Conventional Commits              |
| `/prdescription` | PR description per the template                    |
| `/ship`          | Commit + push + create a PR in one command         |
| `/reviewcode`    | Review a PR vs the ticket spec, report by severity |
| `/setupe2e`      | Init Playwright (once per repo)                    |
| `/writee2e`      | `.spec.ts` from a test plan                        |
| `/reviewe2e`     | Review POM, locators, data, performance            |

> When the extension does not display data, click **`See Error`** on the notification to open the output channel.

### 7.3 Claude Code

```bash
momorph init . --ai claude
```

Generates `.claude/commands/momorph.*.agent.md`. Open the Claude Code terminal and type a slash command. The MCP config is added to `~/.claude.json`.

### 7.4 Cursor / Windsurf / Gemini

```bash
momorph init . --ai cursor       # .cursor/commands/
momorph init . --ai windsurf
momorph init . --ai gemini
```

Prompt files follow each agent's convention. The MCP config is merged into the corresponding config file.

### 7.5 Claude Desktop Extension (.mcpb)

The `.mcpb` bundle installs MoMorph MCP into Claude Desktop via a file — connecting the local Claude Desktop to `mcp.momorph.ai/mcp`.

#### Compatibility

- macOS / Windows / Linux · Node.js ≥ 18 · Claude Desktop supporting MCP v1.x

#### Installation

1. Contact the MoMorph team to get the latest `momorph-mcp.mcpb` file.
2. Claude Desktop → **Settings** → **Extensions** → **Advanced Settings** → **Install Extension**
3. Select the file → **Install** → enter the **GitHub PAT** (scope `user`) → **Save** → **Enable**

#### Test

Prompt: _"List all frames in this Figma file: {fileKey}"_ — Claude calls `list_frames` on its own. Enable Developer Mode to view the MCP debug log.

> **`.mcpb` vs MCP Cloud:** `.mcpb` is for users who only use Claude Desktop. For a multi-IDE setup (VSCode + Claude Code + Cursor) → use MCP Cloud via `momorph init` (§5).

---

## 8. Common Issues

### 8.1 CLI

**`momorph login` does not complete** — check that a firewall/VPN is not blocking `github.com/login/device`. You can enter the code directly at `https://github.com/login/device`.

### 8.2 Web App

**Figma login fails / popup blocked:**

- Allow popups from `momorph.ai`
- Try the browser's private mode (extensions sometimes block the OAuth callback)
- Make sure the Figma account is still active

**No files shown after login** — enter the `fileKey` from the Figma URL when prompted. If skipped: `/` → "Add file" → paste the fileKey.

### 8.3 Figma Plugin

**Item not recognized** — check that the layer name has the correct `mms_*` prefix convention (see §2.4).

**Plugin blank / spinner forever:**

- Can Figma reach `momorph.ai` (network/VPN)?
- Log out of the Web → log back in → reload the plugin (`Cmd/Ctrl+Shift+P` → `Reload`)

### 8.4 VSCode Extension

**Cannot connect to MCP** — not logged in or the token has expired:

```bash
momorph login
momorph whoami
```

Then `Ctrl+Shift+P → Developer: Reload Window`.

**Tree view does not show screens:**

- Has the repo been linked on the Web (Settings → GitHub)?
- Click **Refresh** on the Figma Tree
- If there is an error → click **`See Error`** on the notification

**Context menu does not trigger Copilot Chat** — the Extension detects `.github/agents/momorph.*.agent.md` to know a project is a Copilot project. If it is missing (a Claude Code project), the prompt is copied to the clipboard — paste it manually into Claude.

### 8.5 Syncer (Google Sheets Add-on)

**The MoMorph Syncer menu does not appear under Extensions** — the add-on has not been deployed by the operations team for this Sheets file. Contact the MoMorph team.

**"Missing authentication token" when calling an action** — the Google session has expired. Re-login to your Google account (make sure to use the Sun\* company Google Workspace account), refresh the Sheets tab, and try again.

**"Cannot access spreadsheet"** — file share permissions are insufficient. Check:

- Whether the Sheets file is inside the Sun\* Workspace (personal private files are not supported).
- Whether the current account has **Editor** permission (Viewers cannot sync back to MoMorph).

**"Invalid Figma URL"** — you pasted a URL in the wrong format. Re-paste the Figma link from the browser address bar (including `node-id` if syncing a specific frame).

**"Failed to sync data"** — the MoMorph backend or network was interrupted. Wait a few minutes and try again; if it repeats many times, report to the support team.

**Images do not appear in the cell after syncing** — the in-cell image conversion runs in the background (fire-and-forget). Wait 10–30s then reload the sheet. If it still fails, click **Sync Image** in the menu again.

### 8.6 MCP / Slash Commands

**"Frame not found" when uploading specs** — a missing or wrong `--screen-id` (the Figma node ID `32355:420279` ≠ the MoMorph screenId). Fix it in one of 2 ways (see §5.3):

- Name the file with the correct convention `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` then upload without the flag.
- Or pass the `--screen-id` flag:
  ```bash
  momorph upload specs <file.csv> --screen-id <alphanumeric-screenId>
  ```

**Download specs "Frame not found"** (when the AI agent calls MCP `download_specs`) — the agent is using a Figma node ID instead of the MoMorph screenId. Get the screenId from the Web URL (`/screens/{screenId}/...`) and prompt again.

**Claude Desktop Extension does not call tools:**

- Settings → Extensions → MoMorph status `Enabled`
- Is the GitHub PAT still valid (scope `user`)?
- Enable Developer Mode to view the log
- Make the prompt explicit and mention the fileKey/screenId

**MCP timeout / slow:**

- Check the network to `mcp.momorph.ai`
- A large slash command (`/momorph.specs` for a screen with many items) can take 30–60s — wait longer
- Repeated failures → `momorph login` to refresh the token

**`x-github-token` invalid / 401:**

- The PAT was revoked/expired → create a new PAT (scope `user`), update it in the MCP config (`~/.claude.json`…)
- Using `momorph init`: run `momorph login` → the token is merged into the config automatically

---

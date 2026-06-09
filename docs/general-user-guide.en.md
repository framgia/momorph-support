# MoMorph — User Guide

> **Intended audience:** Designers, BrSEs, Devs, QAs, and PMs who use MoMorph's AI-Driven Development workflow

---

## Table of Contents

<details>
<summary><strong>1. <a href="#1-overview">Overview</a></strong></summary>

- [1.1 Ecosystem (7 products)](#11-ecosystem-7-products)
- [1.2 Data Flow Diagram](#12-data-flow-diagram)
- [1.3 Prerequisites](#13-prerequisites)
  - [Accounts](#accounts)
  - [Software / OS](#software--os)

</details>

<details>
<summary><strong>2. <a href="#2-momorph-figma-plugin">MoMorph Figma Plugin</a></strong></summary>

- [2.1 Installation](#21-installation)
- [2.2 Login](#22-login)
  - [Pro user](#pro-user)
  - [Essential user](#essential-user)
- [2.3 Syncing Design Data](#23-syncing-design-data)
- [2.4 Loading UI Elements into the Spec Screen](#24-loading-ui-elements-into-the-spec-screen)

</details>

<details>
<summary><strong>3. <a href="#3-momorph-web-app">MoMorph Web App</a></strong></summary>

- [3.1 Access](#31-access)
- [3.2 Login](#32-login)
- [3.3 Core Features](#33-core-features)
- [3.4 Screen Status Workflow](#34-screen-status-workflow)

</details>

<details>
<summary><strong>4. <a href="#4-momorph-syncer-google-add-on--sun-employees-only">MoMorph Syncer (Google Add-on)</a></strong></summary>

- [4.1 Usage Requirements](#41-usage-requirements)
- [4.2 Installation / Access](#42-installation--access)
- [4.3 Features](#43-features)

</details>

<details>
<summary><strong>5. <a href="#5-momorph-cli">MoMorph CLI</a></strong></summary>

- [5.1 Installation](#51-installation)
- [5.2 Authentication and Initialization](#52-authentication-and-initialization)
- [5.3 Command Reference](#53-command-reference)

</details>

<details>
<summary><strong>6. <a href="#6-mcp-server--ai-tools">MCP Server — AI Tools</a></strong></summary>

- [Prerequisites](#prerequisites)
- [Method 1 — Quick setup via CLI](#method-1--quick-setup-via-cli)
- [Method 2 — Manual configuration](#method-2--manual-configuration)
- [Tools List](#tools-list)

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

**MoMorph** is the AI-Driven Development ecosystem provided by Sun\* Asterisk. It takes Figma designs / Specs as the starting point for the entire software development lifecycle.

```
Figma Design & Specs → Test Cases → Code
```

### 1.1 Ecosystem (7 products)

| #   | Component                    | Role                                                                                                                              | Platform                  |
| --- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| 1   | **Figma Plugin**             | Syncs Figma design data into MoMorph. Manages design data, generates specs documents, and more — all completed within Figma       | Figma                     |
| 2   | **Web App**                  | Manages projects; stores screens / specs / test cases                                                                             | Browser                   |
| 3   | **Syncer (Google Add-on)**   | Edit spec / testcase in Google Sheets and sync bidirectionally with MoMorph                                                       | Google Sheets             |
| 4   | **CLI**                      | Project initialization, MCP configuration, uploading CSV specs / testcases                                                        | Terminal                  |
| 5   | **VSCode Extension**         | Displays designs / specs, integrates the MCP server, and provides the Figma Tree and slash commands for Copilot Chat             | VS Code                   |
| 6   | **MCP Server**               | Provides 31 AI tools for AI agents to read and write MoMorph / Figma data                                                         | Automatic via AI agent    |
| 7   | **Claude Desktop Extension** | `.mcpb` bundle — use MoMorph MCP from Claude Desktop                                                                              | Claude Desktop            |

### 1.2 Data Flow Diagram

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

**MoMorph user plans (Essential vs Pro)** — these determine the scope of access across the entire ecosystem:

| Plan          | Scope of Access                                                                                                                                                                                                  |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Essential** | **Plugin only** — screens management, manual spec entry, and GitHub issue export are available. Other products (Web App, Syncer, CLI, MCP Server, VSCode Extension, Claude Desktop Extension) are **not available** |
| **Pro**       | **The entire ecosystem** — Plugin (full features) + Web App + Syncer + CLI + MCP Server + VSCode Extension + Claude Desktop Extension                                                                            |

**How to become a Pro user:**

- The `sun-asterisk.com` domain is registered in the Pro whitelist by default → any Sun\* account is automatically granted Pro
- If using an email from another domain: contact Slack `#con_momorph-support_all` to request being added to the whitelist

**Platform accounts required per product:**

| Product                  | Account | Requirement                                                                                                                                            |
| ------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Figma Plugin             | Figma   | Complies with [Figma's plugin usage requirements](https://help.figma.com/hc/en-us/articles/360039958474) (a Viewer seat can launch the plugin as long as it is within its own Drafts files) |
| Web App                  | Figma   | Any seat type                                                                                                                                           |
| Syncer (Google Add-on)   | Google  | **Sun\* Asterisk Google Workspace** account (`@sun-asterisk.com`)                                                                                       |
| CLI                      | GitHub  | Run `momorph login`                                                                                                                                     |
| MCP Server               | GitHub  | PAT (scope: `user`)                                                                                                                                     |
| VSCode Extension         | GitHub  | Same account as the CLI, plus **Copilot Business** (the Free version is not eligible)                                                                   |
| Claude Desktop Extension | GitHub  | PAT (scope: `user`)                                                                                                                                     |

#### Software / OS

| Product                  | Required Environment                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------------- |
| Figma Plugin             | Figma Desktop or figma.com                                                                      |
| Web App                  | Latest version of Chrome / Firefox / Safari / Edge                                              |
| Syncer (Google Add-on)   | Google Sheets in the browser (Sun\* Workspace)                                                  |
| CLI                      | macOS / Linux / Windows (install via Homebrew / Chocolatey / scripts — see §5.1)                |
| VSCode Extension         | VS Code v1.105 or later · WSL on Windows                                                         |
| Claude Desktop Extension | Claude Desktop with MCP v1.x support · Node.js 18 or later · macOS / Windows / Linux             |

---

## 2. MoMorph Figma Plugin

A Plugin that runs within Figma (Desktop / Browser). In addition to features equivalent to the Web App (§3), it syncs design data (screens, items, styles, variables, media) into the MoMorph DB.

### 2.1 Installation

1. In Figma, open **Plugins → Manage plugins** and search for "MoMorph"
2. Click **Install**, then Run

Production Plugin ID: `1406117276934709483`.

### 2.2 Login

On the first launch of the Plugin (or when the session expires), the **Welcome** screen appears with two login buttons. Choose one of the two depending on your account type.

#### Pro user

Click the **"Login with Pro account"** button

1. The Plugin opens a browser tab → click **Authorize** on the Figma OAuth page to authenticate
2. Once authentication completes, you return to the Plugin and proceed to the **"Connect Figma file"** step → paste the Figma URL of the file currently open in the Plugin → click **"Next"**
3. If the file has multiple pages, you proceed to the **"Select pages to load"** step → select the pages from which you want to load screens data from the Figma canvas → complete the initial setup
4. You are taken to the Plugin's main screen

> Your Figma account must be registered in the Pro whitelist (see §1.3). If it is not registered, the browser will display an error after you authorize.

#### Essential user

Click the **"Start for free"** button

1. The Plugin does not open a browser, and Figma OAuth is **not required**
2. You go straight to the Plugin's main screen, where Essential features (browsing screens, manual spec entry, GitHub issue export) are available
3. The Web App, CLI, MCP Server, VSCode Extension, and Claude Desktop Extension are **not available** — see §1.3

> **Accidentally chose Essential despite having a Pro account?** The Plugin remembers this choice, so from the next time onward it takes you straight to the Essential screen without going through the Welcome screen. To return to the Welcome screen, you need to **delete the plan information stored in Figma's clientStorage**. After deleting it, close and reopen the Plugin; the Welcome screen will appear, so click **"Login with Pro account"**.

### 2.3 Syncing Design Data

The Web App, CLI, MCP, and VSCode Extension can only see data that has been synced via the Plugin.

**How to sync:**

1. **Launch the Plugin in the Figma file you are working on** → the Plugin automatically syncs the screens list in the background (no action required)
2. **Click a screen to open its detail view** → that screen's image and UI elements are synced
3. **Click the Refresh icon (🔄) on the Preview toolbar** (tooltip _"Sync / update image"_) in cases such as:
   - Right after modifying a design in Figma, when you want it reflected in MoMorph immediately
   - The Web App shows _"The design image has not been synced from the Figma Plugin"_
   - An item was changed / renamed / added but the Plugin has not recognized it

### 2.4 Loading UI Elements into the Spec Screen

When you open a screen's detail (Spec) screen, the Plugin loads **only the layers that match the prefix convention**. Layers that do not match the prefix are ignored and do not appear in the UI elements list.

**Layer naming convention:**

| Type                    | Prefix                          | Example                                               | Display in Spec                                              |
| ----------------------- | ------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------- |
| **Item** (current convention) | `mms_<name>`              | `mms_button`, `mms_submit_form`                       | ✅ Displayed as an independent UI element                   |
| **Item** (legacy convention)  | `<alphanumeric>_<name>`   | `A_button`, `A1_submit`, `1_label`, `1.1_email_field` | ✅ Displayed; automatically renamed to `mms_*` when added to the spec |
| **Media** (image / icon) | name contains `mm_media`       | `mm_media`, `mm_media_logo`                           | ✅ Displayed in the Media section                           |
| **Normal layer**        | (no prefix)                     | `Rectangle 1`, `Frame 23`, `Button`                   | ❌ Not displayed                                            |

**Notes:**

- Prefixes are **case-insensitive** (`A_button` ≡ `a_button`, `MMS_action` ≡ `mms_action`).
- The name after the prefix **must not use** `<`, `>`, `'`, or `"` (to avoid HTML / SVG errors).
- `mms_*` is the current standard convention. This format is recommended for new layers. The legacy convention (`1_button`, `A_button`) is also compatible; the Plugin automatically renames them to `mms_*` when linking them to the spec.
- Layers with visibility off (`visible = false`) are not loaded. Also, if a parent frame has `opacity = 0`, the layers under it are skipped as well.

**Recommended workflow for Designers:**

1. Name layers using the `mms_*` convention from the design stage (e.g., `mms_login_button`, `mms_username_field`).
2. Open the screen detail in the Plugin and check the item list on the Spec screen.
3. Item not showing? → Fix the layer name in Figma → click **Refresh** (🔄) on the Preview toolbar to reload (see §2.3).

> If an item still does not appear even with the correct prefix set, see §8.3.

---

## 3. MoMorph Web App

The screen for centrally managing projects / files / screens / specs. Design data is synced from Figma via the Plugin. Note that if you do not perform a sync in the Plugin, you may be unable to access the data in the Web App or other products.

### 3.1 Access

URL: **`https://momorph.ai`** · Supports EN / JP / VI (switchable from Settings).

### 3.2 Login

1. Open `momorph.ai` in your browser
2. Click **"Login with Figma"**
3. Authorize in the Figma popup
4. On the first time, enter the `fileKey` to link the file

To link a **GitHub repo** for the VSCode Extension / CLI: file → **Settings → GitHub → Connect** → select the repo.

### 3.3 Core Features

Navigate via the sidebar / breadcrumb. The list below is a route reference for checking URLs — after logging in, you can open them at `momorph.ai/<route>`.

**Files & Screens**

| Feature          | Route                                      | Purpose                                                                  |
| ---------------- | ------------------------------------------ | ------------------------------------------------------------------------ |
| File list        | `/`                                        | List of linked Figma files                                               |
| Screen list      | `/files/{fileKey}/screens`                 | List of screens in the file (filter by status / tag / page)             |
| Screen detail    | `/files/{fileKey}/screens/{screenId}`      | Image preview + design items                                             |
| Item spec editor | `…/screens/{screenId}/items/{itemId}/spec` | Edit validation / navigation / DB mapping (supports **AI Generate Spec**) |
| Spec revisions   | `…/items/{itemId}/revs` · `…/revs/{revId}` | View change history and roll back                                        |
| View all specs   | `…/screens/{screenId}/items/all-specs`     | Browse all specs in the screen in a read-only table                      |
| Screen tags      | `…/screens/{screenId}/tags`                | Add tags to a screen (functional, bug, etc.)                             |
| Global tags      | `/tags`                                    | System-wide tag management                                               |

**Screen Sets** (grouping screens)

| Feature          | Route                                          | Purpose                              |
| ---------------- | ---------------------------------------------- | ------------------------------------ |
| Screen Sets list | `/files/{fileKey}/screen-sets`                 | List of screen sets                  |
| Create / Edit    | `…/screen-sets/create` · `…/{frameSetId}/edit` | Create / edit a screen set           |
| Set detail       | `…/{frameSetId}/list`                          | Display the screens within one set   |
| Screen in set    | `…/{frameSetId}/screens/{screenId}`            | Open a screen from the set's context |

**File-level Settings** (`/files/{fileKey}/settings`)

| Feature                | Route                             | Purpose                                       |
| ---------------------- | --------------------------------- | --------------------------------------------- |
| Project Overview       | `…/settings/overview`             | Project overview (markdown)                   |
| GitHub                 | `…/settings/github`               | OAuth + repo linking (for VSCode Ext / CLI)   |
| Google                 | `…/settings/google`               | Google OAuth (for the Syncer Google Sheets)   |
| Screen Translation     | `…/settings/screen-translation`   | Localization hub                              |
| Translation Languages  | `…/screen-translation/languages`  | Enable / disable languages per file           |
| Translation Dictionary | `…/screen-translation/dictionary` | en ↔ jp ↔ vi translation dictionary          |

### 3.4 Screen Status Workflow

Each screen has 4 independent status fields (`design_status`, `spec_status`, `dev_status`, `review_status`), each managing progress in 3 stages: `Not Started` / `In Progress` / `Done`. The recommended order of progression:

```
Design → Spec → Dev → Review → Done
```

**Which role updates which field** (recommended workflow):

| Field           | Responsible Role | When to switch to `Done`                                    |
| --------------- | ---------------- | ----------------------------------------------------------- |
| `design_status` | Designer         | The screen's Figma design is complete                       |
| `spec_status`   | BrSE / PM        | The spec of each item in the screen has been approved       |
| `dev_status`    | Developer        | Implementation of the feature related to the screen is done |
| `review_status` | QA / Reviewer    | Review / testing is complete and there are no blocking issues |

The status fields are operated directly from the Screen detail. The VSCode Extension filters by `spec_status = Done` by default, so Devs only see screens that are ready to be implemented.

---

## 4. MoMorph Syncer (Google Add-on — Sun\* employees only)

A Google Sheets Add-on that syncs bidirectionally between Sheets ↔ MoMorph. It is suited for editing specs / test cases in Sheets — leveraging multi-person collaboration, comments, and formulas — and reflecting them in MoMorph, or conversely exporting MoMorph specs to Sheets for team review.

### 4.1 Usage Requirements

- A **Sun\* Asterisk Google Workspace** account (`@sun-asterisk.com`). A personal Google account cannot use the add-on.
- The MoMorph **Pro** plan (see §1.3) — Essential users cannot use the Syncer.
- A Google Sheets file with the MoMorph Syncer add-on installed.

### 4.2 Installation / Access

- Open a Google Sheets under the Sun\* Workspace → menu **Extensions → search for and install MoMorph Syncer**. On the first time, an authorize popup for the Google account appears, granting access to the Sheets file and permission to call the MoMorph backend.
- If MoMorph Syncer does not appear in the **Extensions** menu, contact Slack `#con_momorph-support_all`.

### 4.3 Features

| Action                  | Description                                                              |
| ----------------------- | ------------------------------------------------------------------------ |
| **Sync Specifications** | Bidirectionally sync UI element definitions between Sheets ↔ MoMorph     |
| **Sync Testcases**      | Bidirectionally sync test cases between Sheets ↔ MoMorph                  |
| **Sync Image**          | Fetch the latest Figma design images into Sheets as in-cell native images |
| **Sync i18n**           | Sync multilingual content (en / jp / vi)                                 |

> See §8.5 if you encounter authorization errors, sheet sync failures, missing menu actions, or similar.

---

## 5. MoMorph CLI

Responsible for project initialization / post-initialization setup, uploading CSV specs / testcases, and MCP configuration for AI agents. The CLI **does not support download**, so if you want to download specs / testcases as CSV, use the MCP tools via an AI agent (see §6).

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

**Linux / macOS (Bash):**

```bash
curl -fsSL https://raw.githubusercontent.com/momorph/cli/refs/heads/main/scripts/install.sh | bash
```

**Go install:**

```bash
go install github.com/momorph/cli@latest
```

**Check version and update:**

```bash
momorph version
momorph update
```

### 5.2 Authentication and Initialization

**Step 1 — Login:**

```bash
momorph login          # The CLI displays a code and a link. Press Enter to launch the browser
momorph whoami         # Check account information
```

**Step 2 — Project initialization:**

```bash
momorph init . --ai claude        # Claude Code
momorph init . --ai copilot       # GitHub Copilot
momorph init . --ai cursor        # Cursor
momorph init . --ai windsurf      # Windsurf
momorph init . --ai gemini        # Gemini
```

> **Important:** When initializing at the root of a repo, specify `.`. With `momorph init my-project`, a new subfolder is created.

What `init` does automatically: downloads the latest template, creates `.claude/` (or `.github/`, `.cursor/`, etc.), configures the MCP server, and installs slash commands.

### 5.3 Command Reference

| Command                                         | Description                                  |
| ----------------------------------------------- | -------------------------------------------- |
| `momorph login`                                 | Authenticate via GitHub OAuth Device Flow    |
| `momorph logout [--force]`                      | Log out and delete credentials               |
| `momorph whoami`                                | Account information + subscription           |
| `momorph init <dir> --ai <agent>`               | Initialize project + configure agent         |
| `momorph upload specs <file.csv>`               | Upload spec CSV                              |
| `momorph upload specs <file.csv> --dry-run`     | Preview only (does not upload)               |
| `momorph upload testcases <file.csv>`           | Upload test cases                            |
| `momorph upload testcases <file.csv> --dry-run` | Preview only                                 |
| `momorph version`                               | CLI version                                  |
| `momorph update [--check]`                      | Update the CLI (`--check`: check only)       |
| `momorph completion <shell>`                    | Shell completion (bash / zsh / fish / powershell) |
| `momorph help [command]`                        | Help                                         |

> **How to specify the screen when uploading** (choose one):
>
> 1. **A filename that follows the convention** — in the format `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` (`{figmaFrameId}` is the frame's Figma node ID. Example: `9276:19907-TOP_Channel.csv`). This is the format automatically generated by slash commands such as `/specs`, `/createtestcases`, and `/updatetestcases`.
> 2. **The `--screen-id <screenId>` flag** — the alphanumeric MoMorph screenId obtained from the Web URL `/screens/{screenId}/...`. For files outside the convention path, also specify `--file-key`.

---

## 6. MCP Server — AI Tools

Hosted at `https://mcp.momorph.ai/mcp`, it provides **31 tools** for AI agents to read and write MoMorph / Figma data. Users do not call it directly; AI agents use it automatically (via the slash commands in §7.2, or via natural-language prompts in Claude Desktop in §7.5). For details of each tool, see the separate document **MoMorph MCP Server — Tools Reference (English)** (filename: `momorph-mcp-tools-reference-en.pdf`).

Important tools that do not have a corresponding slash command — ones the AI can only call via MCP:

- `upload_specs` / `download_specs` — upload / download spec CSV to / from MoMorph; supports two kinds of status management: **spec completion** (`spec_progress`: `draft`/`completed`) and **lifecycle** (`active_status`: `active`/`archived`/`deleted`). Download always returns the `spec_progress` column; the `active_status` column is included only when `include_deleted=true`. Upload accepts both fields — if unspecified, the status is automatically determined from the content. Items with `active_status=archived` are rejected if there are content changes.
- `upload_test_cases` / `download_test_cases` — upload / download test cases CSV
- `list_frame_spec_diffs` — compare a screen's spec with the immediately preceding revision

**How to trigger these tools manually:**

- **Upload** (specs / testcases): use the CLI (`momorph upload specs|testcases <file.csv>`), or right-click a `.csv` under `.momorph/` in the VSCode Explorer → "Upload to MoMorph" (see §7.2)
- **Download** + **list_frame_spec_diffs**: only from an AI agent — a natural-language prompt in Claude Desktop / Code / Cursor, or the slash command `/downloadspecs` in the VSCode menu

### Prerequisites

- A GitHub account linked to MoMorph Web (required to use the CLI / MCP)
- Access rights to the repo (Admin permission is required when linking a repo via the VSCode Extension / Plugin)

### Method 1 — Quick setup via CLI

(For Claude Desktop, use `.mcpb` — see §7.5)

```bash
brew install momorph/tap/momorph-cli
momorph login
momorph init . --ai <agent_name>
```

### Method 2 — Manual configuration

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

Issue the PAT from GitHub's **Settings → Developer settings → Personal access tokens** with the scope set to `user`.

### Tools List

For details (descriptions, parameters, return values, and usage examples) of all **31 tools**, see the dedicated reference distributed alongside this guide:

📘 **MoMorph MCP Server — Tools Reference (English)** — filename: `momorph-mcp-tools-reference-en.pdf` (distributed in the Slack channel `#con_momorph-support_all`).

---

## 7. AI Agent Integrations

### 7.1 Overview

| Agent                      | Init Command                   | Prompt Folder                         | Trigger                       | Recommended Use     |
| -------------------------- | ------------------------------ | ------------------------------------- | ----------------------------- | ------------------- |
| **Claude Code**            | `momorph init . --ai claude`   | `.claude/commands/`                   | Slash commands in the terminal | CLI, headless       |
| **GitHub Copilot**         | `momorph init . --ai copilot`  | `.github/agents/`, `.github/prompts/` | Copilot Chat / VSCode Ext     | IDE-centric         |
| **Cursor**                 | `momorph init . --ai cursor`   | `.cursor/commands/`                   | Cursor chat                   | All-in-one IDE      |
| **Windsurf**               | `momorph init . --ai windsurf` | (follows the Windsurf convention)     | Windsurf chat                 | Codeium family      |
| **Gemini**                 | `momorph init . --ai gemini`   | (follows the Gemini CLI convention)   | Gemini chat                   | Google stack        |
| **Claude Desktop** (.mcpb) | See §7.5                       | n/a                                   | Natural-language prompt       | Casual / non-coding |

### 7.2 GitHub Copilot + VSCode Extension

**Sun\* MoMorph VSCode Extension** (`sun-asterisk.vscode-momorph`): integrates the Figma Tree, slash commands, and MCP server registration for Copilot Chat into VS Code.

#### Operating Requirements

- **View or edit** permission for the Figma file (not required if only generating unit tests)
- **GitHub Copilot Business**
- VS Code v1.105 or later
- WSL required on Windows

#### Installation

The VSCode Extension is distributed as a `.vsix` file. Contact Slack `#con_momorph-support_all` to obtain the latest version.

1. Open the `vscode-momorph-x.y.z.vsix` you obtained
2. VSCode → **Extensions** tab → **`...`** → **Install from VSIX...**
3. Specify the file

#### Connection

Use the same GitHub account as the CLI. Make sure you have run `momorph login` beforehand.

1. Web → Settings → GitHub → connect repo
2. Open the repo in VSCode → click the **MoMorph** icon in the Activity Bar
3. Setup is complete once the screen list appears

#### Usage After Installation

You can use the following features directly within VSCode:

- **Sidebar — Figma view** (`momorph.figma`): displays screens grouped by **With Design / No Design / Archived**. Also displays **Screen Sets** and **Components**. Filter / search by **tag, page, status** (the 4 status fields: Design / Spec / Dev / Review). Filtered by `Spec Status = Done` by default.
- **Sidebar — Contexts view** (`momorph.contexts`): displays endpoints from `.momorph/contexts/api-docs.yaml`. Auto-refreshes when the file changes.
- **Right-click a screen** (supports multi-select):
  - **Open on Web** / **Copy Screen Information**
  - 15 slash commands generate prompts for AI agents — see the table below
  - Detects the presence of `.github/agents/momorph.*.agent.md`: present → launches Copilot Chat with the prompt / absent → copies the prompt to the clipboard (paste into Claude / Cursor)
- **Click a screen** → a web view displays the image preview and the specs panel (items / styles / variables / test cases) side by side
- **Command Palette** (`Cmd/Ctrl+Shift+P` → `MoMorph:`): Sign In, Search/Filter Screens, Open MoMorph Web, OpenAPI Server (Start/Stop/Restart), and more
- **Settings** (`Cmd/Ctrl+,` → `momorph`):
  - `chat.language` & `chat.outputFileLanguage` (English / Vietnamese / Japanese)
  - `api.baseUrl`, `api.headers`, `mcpServers`, `github.remoteName`, `github.useEnterprise`
- **Copilot Chat**: `/` for slash commands, `#` for the 7 Language Model Tools — `momorph_callMcpTool`, `momorph_compareScreenshots`, `momorph_downloadFigmaImage`, `momorph_getPreferenceInstructions`, `momorph_getUserPreferences`, `momorph_listApiEndpoints`, `momorph_getApiEndpoint`
- **Explorer**: right-click a `.csv` under `.momorph/specs/` or `.momorph/testcases/` → **Upload to MoMorph**
- **MCP servers** registered by default (keys in `momorph.mcpServers`): `morpheus`, `context7`, `testViewpoints`

#### Slash commands in the Context menu

15 commands classified into 2 groups. The **Agent file** column indicates commands that have an independent prompt file (`.claude/commands/momorph.*.agent.md` or `.github/agents/momorph.*.agent.md`) — runnable in Claude Code / Cursor. Commands without an agent file work only via the VSCode menu (dynamic prompt).

**Flow** — the spec → plan → implement workflow:

| Command          | Agent file | Action                                                       |
| ---------------- | :--------: | ------------------------------------------------------------ |
| `/constitution`  |     ✅     | Initialize / update the constitution (rules, stack)          |
| `/specify`       |     ✅     | Generate `spec.md` + `design-style.md` + assets from a screen |
| `/reviewspecify` |     ❌     | Review / improve spec.md & design-style.md                   |
| `/plan`          |     ✅     | Generate a plan from spec + design-style + constitution      |
| `/reviewplan`    |     ❌     | Review / improve the plan                                    |
| `/tasks`         |     ✅     | Break the plan down into `tasks.md`                          |
| `/implement`     |     ✅     | Implement according to `tasks.md`                            |

**Context** — generate data from Figma:

| Command            | Agent file | Action                                                           |
| ------------------ | :--------: | ---------------------------------------------------------------- |
| `/specs`           |     ✅     | Generate a 22-column CSV spec from a screen                      |
| `/createtestcases` |     ✅     | Test cases (Accessing / GUI / Function), 1 CSV per screen        |
| `/updatetestcases` |     ✅     | Update test cases when the spec changes                          |
| `/apispec`         |   ✅ \*    | OpenAPI specs + backend test cases                               |
| `/database`        |     ✅     | SQL Schema + Mermaid ERD                                         |
| `/screenflow`      |     ✅     | Generate `SCREENFLOW.md`                                         |
| `/downloadspecs`   |     ❌     | Download CSV spec from MoMorph (via MCP tool)                    |
| `/convertspecs`    |     ❌     | Convert spec markdown → local CSV (no upload)                    |

\* The agent file name is `momorph.apispecs.agent.md` (plural); in the VSCode menu it is triggered with `apispec` (singular).

#### Slash commands available only via agent file (not in the VSCode menu)

Installed via `momorph init . --ai <agent>` (see §7.3-§7.4), typed directly in the terminal / chat:

| Command          | Action                                                  |
| ---------------- | ------------------------------------------------------- |
| `/commit`        | Commit following Conventional Commits                   |
| `/prdescription` | PR description following the template                   |
| `/ship`          | Commit + push + PR creation combined into one command   |
| `/reviewcode`    | Review a PR against the ticket spec, reported by severity |
| `/setupe2e`      | Initialize Playwright (once per repo)                   |
| `/writee2e`      | Generate `.spec.ts` from a test plan                    |
| `/reviewe2e`     | Review POM, locator, data, and performance              |

> If the Extension does not display data, click **`See Error`** in the notification to open the output channel and check it.

### 7.3 Claude Code

```bash
momorph init . --ai claude
```

Generates `.claude/commands/momorph.*.agent.md`. Open the Claude Code terminal and simply type a slash command to use it. The MCP configuration is added to `~/.claude.json`.

### 7.4 Cursor / Windsurf / Gemini

```bash
momorph init . --ai cursor       # .cursor/commands/
momorph init . --ai windsurf
momorph init . --ai gemini
```

Prompt files are placed according to each agent's convention. The MCP configuration is automatically merged into the corresponding config file.

### 7.5 Claude Desktop Extension (.mcpb)

A `.mcpb` bundle installs MoMorph MCP into your local Claude Desktop as a single file — connecting Claude Desktop with `mcp.momorph.ai/mcp`.

#### Compatibility

- macOS / Windows / Linux · Node.js 18 or later · Claude Desktop with MCP v1.x support

#### Installation

1. Contact Slack `#con_momorph-support_all` to obtain the latest `momorph-mcp.mcpb`.
2. Claude Desktop → **Settings** → **Extensions** → **Advanced Settings** → **Install Extension**
3. Specify the file → **Install** → enter the **GitHub PAT** (scope: `user`) → **Save** → **Enable**

#### Verification

Prompt: _"List all frames in this Figma file: {fileKey}"_ — Claude automatically calls `list_frames`. To check the MCP debug log, enable Developer Mode.

> **`.mcpb` vs MCP Cloud:** `.mcpb` is for users who use only Claude Desktop. For a multi-IDE setup (VSCode + Claude Code + Cursor), use MCP Cloud via `momorph init` (§5).

---

## 8. Common Issues

### 8.1 CLI

**`momorph login` does not complete** — check whether a firewall / VPN is blocking `github.com/login/device`. You can also authenticate by entering the code directly at `https://github.com/login/device`.

### 8.2 Web App

**Figma login failure / popup blocked:**

- Allow popups from `momorph.ai`
- Try the browser's private mode (extensions may interfere with the OAuth callback)
- Make sure the Figma account is in an active state

**Files do not appear after login** — enter the `fileKey` from the Figma URL in the popup. If you skipped it: `/` → "Add file" → paste the fileKey.

### 8.3 Figma Plugin

**Item not recognized** — check that the `mms_*` prefix is correctly set in the layer name (see §2.4).

**Plugin is blank / spinner never stops:**

- Check whether `momorph.ai` is accessible from Figma (network / VPN)
- Log out of the Web → log in again → reload the plugin with `Cmd/Ctrl+Shift+P` → `Reload`

### 8.4 VSCode Extension

**Cannot connect to MCP** — you may not be logged in, or the token may have expired:

```bash
momorph login
momorph whoami
```

Then run `Ctrl+Shift+P → Developer: Reload Window`.

**Tree view does not show screens:**

- Check that the repo is linked on the Web side (Settings → GitHub)
- Click **Refresh** on the Figma Tree
- If an error is shown → check the details via **`See Error`** in the notification

**Copilot Chat does not launch from the context menu** — the Extension determines a Copilot project by the presence of `.github/agents/momorph.*.agent.md`. If that file is absent (e.g., in a Claude Code project), the prompt is copied to the clipboard, so paste it manually into Claude or similar.

### 8.5 Syncer (Google Add-on)

**MoMorph Syncer does not appear in the Extensions menu** — the add-on has not been deployed to that Sheets file. Contact Slack `#con_momorph-support_all`.

**"Missing authentication token" when running an action** — the Google session has expired. Log back in to the Google account with a `@sun-asterisk.com` email, refresh the Sheets tab, and retry.

**"Cannot access spreadsheet"** — insufficient file sharing permissions. Items to check:

- Whether the Sheets file is under the Sun\* Workspace (personal private files are not supported).
- Whether the current account has **Editor** permission (Viewer cannot sync to MoMorph).

**"Invalid Figma URL"** — the URL format is invalid. Copy and paste the Figma link again from the browser's address bar (include the `node-id` as well when syncing a specific frame).

**"Failed to sync data"** — a temporary failure of the MoMorph backend or network. Retry after a few minutes. If it recurs, contact team support.

**Image does not appear in the cell after syncing** — converting the in-cell image runs in the background (fire-and-forget). Wait 10–30 seconds and then reload the sheet. If it still fails, run **Sync Image** again from the menu.

### 8.6 MCP / Slash Commands

**"Frame not found" when uploading specs** — most often this is a missing `--screen-id`, or confusing a Figma node ID (e.g., `32355:420279`) with a MoMorph screenId. Address it with one of the following (see §5.3):

- Use a filename that follows the convention `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` and upload without flags.
- Or specify the `--screen-id` flag:
  ```bash
  momorph upload specs <file.csv> --screen-id <alphanumeric-screenId>
  ```

**"Frame not found" when downloading specs** (when an AI agent calls MCP `download_specs`) — the agent is passing a Figma node ID as the screenId. Obtain the correct screenId from the Web URL `/screens/{screenId}/...` and redo the prompt.

**Claude Desktop Extension does not call tools:**

- Whether MoMorph's status is `Enabled` in Settings → Extensions
- Whether the GitHub PAT is valid (scope: `user`)
- Enable Developer Mode and check the log
- Whether the fileKey / screenId is clearly stated in the prompt

**MCP timeout / slow response:**

- Check the connection status to `mcp.momorph.ai`
- Large slash commands (such as `/momorph.specs` on a screen with many items) may take 30–60 seconds
- If it fails repeatedly, refresh the token with `momorph login`

**`x-github-token` invalid / 401:**

- The PAT has been revoked / expired → issue a new PAT (scope: `user`) and update the MCP config such as `~/.claude.json`
- When using `momorph init`, running `momorph login` automatically merges the token into the config

---

_For any other inquiries, contact Slack `#con_momorph-support_all`._

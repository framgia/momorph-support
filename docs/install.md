# MoMorph — Installation

What you need and what to do to get each MoMorph surface running: the plans and platform accounts each one requires, then install and sign-in for the Figma plugin, web app, Google Sheets add-on, CLI, MCP server, VSCode extension, and Claude Desktop extension.

## Prerequisites

### Accounts

**MoMorph user plans (Essential vs Pro)** — they determine access scope across the entire ecosystem:

| Plan          | Access scope                                                                                                                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Essential** | **Plugin only** — manage screens, enter specs manually, export GitHub issues. The other sub-products (Web App, Syncer, CLI, MCP Server, VSCode Extension, Claude Desktop Extension) **are not accessible**                             |
| **Pro**       | **Entire ecosystem** — Plugin (full features) + Web App + Syncer + CLI + MCP Server + VSCode Extension + Claude Desktop Extension                                                                                                      |

**How to become a Pro user:**

- Users whose email belongs to the Sun\* company domain are Pro accounts by default.
- Other emails: contact the MoMorph team to be granted a Pro account.

**Platform accounts required for each product:**

| Product                  | Account | Requirement                                                                                                                                                        |
| ------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Figma Plugin             | Figma   | Follow [Figma's plugin usage requirements](https://help.figma.com/hc/en-us/articles/360039958474) (a Viewer seat can still run the plugin in personal Drafts files) |
| Web App                  | Figma   | Any seat                                                                                                                                                           |
| Syncer (Google Add-on)   | Google  | A **Sun\* company Google Workspace** account                                                                                                                       |
| CLI                      | GitHub  | `momorph login`                                                                                                                                                    |
| MCP Server               | GitHub  | PAT scope `user`                                                                                                                                                   |
| VSCode Extension         | GitHub  | Same account as the CLI + **Copilot Business** (Free is not enough)                                                                                                |
| Claude Desktop Extension | GitHub  | PAT scope `user`                                                                                                                                                   |

### Software / OS

| Product                  | Requirement                                                                      |
| ------------------------ | -------------------------------------------------------------------------------- |
| Figma Plugin             | Figma Desktop or figma.com                                                       |
| Web App                  | Latest Chrome / Firefox / Safari / Edge                                          |
| Syncer (Google Add-on)   | Google Sheets in the browser (Sun\* Workspace)                                   |
| CLI                      | macOS / Linux / Windows (install via Homebrew / Chocolatey / scripts — see below) |
| VSCode Extension         | VS Code ≥ v1.105 · Windows: WSL                                                  |
| Claude Desktop Extension | Claude Desktop supporting MCP v1.x · Node.js ≥ 18 · macOS/Windows/Linux          |

## Figma Plugin

1. Open Figma → **Plugins → Manage plugins** → search for "MoMorph"
2. Click **Install** → Run

### Sign in

Opening the Plugin for the first time (or when the session has expired) brings up the **Welcome**
screen with 2 sign-in buttons corresponding to 2 flows — the user picks one of the two depending on
their account type.

**Pro user** — click the **"Sign in with Pro account"** button:

1. The Plugin opens a browser tab → click **Authorize** on the Figma OAuth page to authenticate the account.
2. After successful authentication, return to the Plugin, which moves to the **"Connect Figma File"** step — paste the Figma URL of the file the plugin is open in → click **"Continue"**.
3. If the file has multiple pages, the Plugin moves to the **"Select pages to load"** step — choose the pages whose screen data you want to load from the Figma canvas → finish setup.
4. Enter the Plugin's main screen.

> The Figma account must be a Pro account. If it is not, the browser will show an error after authorization.

**Essential user** — click the **"Start for free"** button:

1. The Plugin does **not** open a browser and does **not** require Figma OAuth.
2. Go straight to the Plugin's main screen with Essential features (browse screens, enter specs manually, export GitHub issues).
3. The Web App, CLI, MCP Server, VSCode Extension, and Claude Desktop Extension are **not** accessible.

## Web App

URL: **`https://momorph.ai`** · Supports EN/JP/VI (change in Settings).

### Sign in

1. Open `momorph.ai`
2. Click **"Login with Figma"**
3. Authorize Figma

## Syncer (Google Sheets Add-on)

- Open a Google Sheets within the Sun\* Workspace → menu **Extensions → search for and install MoMorph Syncer**. The first time, a popup will request authorization of your Google account so the add-on can access the Sheets file and call the MoMorph backend.
- If the MoMorph Syncer menu does not appear under **Extensions**, contact the MoMorph team.

Usage requirements:

- A **Sun\* company Google Workspace** account. Personal Google accounts **cannot** access the add-on.
- A **Pro** plan on MoMorph — Essential users cannot use the Syncer.
- A Google Sheets file that has the MoMorph Syncer add-on installed.

## CLI

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

### Authentication and initialization

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

`init` automatically: downloads the latest template, creates `.claude/` (or `.github/`, `.cursor/`…),
configures the MCP server, and installs slash commands.

## MCP Server

The MCP server is hosted at `https://mcp.momorph.ai/mcp`.

Prerequisites:

- A GitHub account linked to MoMorph Web (for CLI / MCP)
- Repo access (for the VSCode Extension / Plugin, if the account has Admin)

### Option 1 — Quick setup via CLI

(Claude Desktop uses `.mcpb` — see the Claude Desktop Extension section below.)

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

## VSCode Extension

**Sun\* MoMorph VSCode Extension** (`sun-asterisk.vscode-momorph`): Figma Tree, slash commands, and
registering the MCP server for Copilot Chat.

Requirements:

- **View or edit** access to the Figma file (not needed if you only generate unit tests)
- **GitHub Copilot Business**
- VS Code ≥ v1.105
- Windows: WSL

### Installation

The VSCode Extension is distributed as a `.vsix` file. Contact the MoMorph team to get the latest file.

1. Open the file `vscode-momorph-x.y.z.vsix`
2. VSCode → the **Extensions** tab → **`...`** → **Install from VSIX...**
3. Select the file

### Connect

Use the same GitHub account as the CLI. Make sure you have run `momorph login`.

1. Web → Settings → GitHub → connect repo
2. VSCode → open the repo → click the **MoMorph** icon in the Activity Bar
3. The screen list appears → setup is OK

## Claude Desktop Extension

The `.mcpb` bundle installs MoMorph MCP into Claude Desktop via a file — connecting the local Claude
Desktop to `mcp.momorph.ai/mcp`.

Compatibility:

- macOS / Windows / Linux · Node.js ≥ 18 · Claude Desktop supporting MCP v1.x

### Installation

1. Contact the MoMorph team to get the latest `momorph-mcp.mcpb` file.
2. Claude Desktop → **Settings** → **Extensions** → **Advanced Settings** → **Install Extension**
3. Select the file → **Install** → enter the **GitHub PAT** (scope `user`) → **Save** → **Enable**

### Test

Prompt: _"List all frames in this Figma file: {fileKey}"_ — Claude calls `list_frames` on its own.
Enable Developer Mode to view the MCP debug log.

> **`.mcpb` vs MCP Cloud:** `.mcpb` is for users who only use Claude Desktop. For a multi-IDE setup
> (VSCode + Claude Code + Cursor) → use MCP Cloud via `momorph init`.

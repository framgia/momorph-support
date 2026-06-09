# MoMorph — FAQ & Troubleshooting Guide


## Bugs & Issues

### Q1. Why do the numbers on Figma and on MoMorph differ? (Plugin)

- The numbers on Figma are **only used for the first detection**.
- After that, to change a number on MM you must **edit it directly in the "No" column on MM**; there is no reverse sync from Figma.

This is intended behavior, not a random bug.

### Q2. I numbered items manually but some don't show up / can't be linked? (Plugin)

Per the User Guide, the common cause is that the **layer name doesn't follow the `mms_` prefix** (or an old convention such as `A_`, `1_`). How to fix:

- Rename the layer on Figma to the form `mms_<name>` (case-insensitive).
- Click the **Refresh** button on the Plugin's Preview toolbar to reload the item.
- Hidden layers (visible=false) or a parent frame with opacity=0 will not be loaded.

If the prefix is correct but items are still missing → submit a bug report form (see Q34).

### Q3. AI content generation stops midway and doesn't finish? (AI Generation)

AI generation can **take 30–60s for screens with many items** — wait a bit before treating it as an error. If it still doesn't complete:

- Check the network connection to `mcp.momorph.ai`.
- Try again; changing the numbering method may help.
- After repeated failures → run `momorph login` to refresh the token.

If it keeps happening → submit a bug report form (see Q34).

### Q4. The CSV file shows garbled fonts / displays incorrectly? (Plugin)

Check the preview tool you are using to open the CSV file. If the preview tool works fine but the display is still wrong, contact the MoMorph team via Slack `#con_momorph-support_all` for support.

### Q5. Item numbers are wrong or out of order? (Plugin)

Usually caused by **MoMorph data being out of sync with the Figma tree**. How to fix:

- After editing the design on Figma, click the **Refresh** button on the Preview toolbar to re-sync.
- Use the **"Find on Figma"** button to verify the item points to the correct target frame.

If still wrong → provide information to the MM team for investigation.

### Q6. After editing the design on Figma, the data I entered on MoMorph is gone? (Plugin)

After editing/updating the design on Figma, click the **Refresh** button on the Plugin's Preview toolbar to re-sync. If the data link is still lost:

- Provide the relevant **ScreenID** to the MoMorph team.
- The MM team will re-update the data for the affected screens.

### Q7. Sending a spec to GitHub returns an error? (Server)

This issue has been reported by multiple users (both Vietnamese and Japanese). The development team is working on it. A solution called **"Github Flex"** has been introduced to address the spec display limits on GitHub Issues.

### Q8. Logging in to GitHub via the CLI returns 'user not found'? (MCP & CLI)

- Re-login to the CLI: `momorph login` → verify with `momorph whoami`.
- Make sure firewall/VPN does not block `github.com/login/device` (you can enter the code directly on that page).
- Distinguish connecting a **GitHub account** vs a **repository** (see Q40).

### Q9. Can't connect GitHub; says the account hasn't been added to the project? (Web)

You need a **Pro user** account to use CLI/MCP/VSCode:

- `@sun-asterisk.com` emails are automatically Pro.
- Other emails → contact Slack `#con_momorph-support_all` to be added to the Pro whitelist.

You also need GitHub linked on MoMorph Web (file → Settings → GitHub → Connect repo).

### Q10. AI connection (MCP) returns a server error and can't be used? (MCP & CLI)

This may be caused by the MCP server being overloaded or a temporary error. Please wait a moment and try again. If MCP is still not restored, contact the team via Slack `#con_momorph-support_all` for assistance.

### Q11. Spec sync between MoMorph and Google Sheets fails? (Web)

This is the **MoMorph Syncer** feature (Google Add-on). Common errors:

- **"Cannot access spreadsheet"**: the file must be within the Sun* Workspace and the account must have **Editor** permission (Viewer cannot reverse-sync).
- **"Missing authentication token"**: the Google session expired → re-login with your `@sun-asterisk.com` email and refresh the Sheets tab.
- **"Failed to sync data"**: backend/network interruption → wait a few minutes and retry.

For deeper debugging, the MoMorph team may request editor access to the Figma/Sheets file.

## Setup & Connection

### Q12. Setup on Web is done — what's next so the AI can fetch the spec? (MCP & CLI)

Steps:

- Install the CLI: `brew install momorph/tap/momorph-cli`.
- `momorph login` → `momorph init . --ai <agent>` (claude/copilot/cursor…) to auto-configure the MCP server + slash commands.
- The AI agent then calls MCP tools on its own (slash command or natural prompt) to fetch the spec — e.g. `/downloadspecs` or a prompt with a screenId.

Users do not call MCP directly.

### Q13. GitHub is connected but members still can't open the Figma file? (Web)

- When an **admin** connects GitHub, members in the repository can access the Figma file.
- Sometimes the GitHub webhook fails to process the member-added event.
- **Solution:** temporarily disconnect and reconnect GitHub.

### Q14. What is the linking ratio between a Figma file and a GitHub repo? (Web)

- One GitHub repository **CAN** connect to MULTIPLE Figma files.
- One Figma file **CANNOT** connect to multiple repositories (the reverse direction is not yet supported; planned for the future).

### Q15. What does a customer need to start using MoMorph? (Web)

You need a **Pro user** account to use the full ecosystem:

- `@sun-asterisk.com` emails automatically have Pro.
- Other emails (customers) → contact Slack `#con_momorph-support_all` to be added to the Pro whitelist.

Once added, notify the customer to create an account and log in. (Essential only allows the Plugin.)

## Release & Numbering

### Q16. MoMorph just released a new version — what do I do to update? (Plugin)

Reload order (in this exact sequence): **1. Figma → 2. Plugin → 3. Web**. For those who already have the plugin open, on startup we recommend opening the detail screen and syncing.

### Q17. Where can I see the update (release) history? (Server)

See the full release history in **Release Notes** on Slack `#con_momorph-support_all`. For the **Figma Plugin** specifically, you can track the version on MoMorph's Figma Community page: [figma.com/community/plugin/…/momorph](https://www.figma.com/community/plugin/1406117276934709483/momorph).

### Q18. What's new in VSCode Extension v0.12.4? (VSCode Ext)

- Improved the extension activation mechanism.
- Added the Figma Tree View feature.
- Improved search/filter.
- UI/UX upgrades.

### Q19. What's the item naming rule for MoMorph to recognize? When does the old 'id_' stop working? (Figma)

- **New rule:** add the prefix **mms_** to the layer name. Numbering content is viewed/edited directly on MoMorph.
- **Old rule:** prefix **id_** — no longer recognized after 2026/05/30.
- **Auto migration:** 2026/03/27 – 2026/05/29.

> ⚠️ After 2026/05/29, the system no longer auto-converts id_ to mms_. Make sure migration is completed before this deadline.

### Q20. To change a number, do I edit it on MoMorph or on Figma? (Plugin)

When you want to change a number after the first detection, **edit the "No" column on MM**, not on Figma. The numbers on Figma serve only the initial detection.

## Spec, Workflow & Figma

### Q21. If I edit the spec on Google Sheets, does it auto-update the spec file? (Web)

- Content from the Spreadsheet is stored only in the MoMorph DB.
- **It is not automatically synced to the spec.md file.**
- Information edited by the BrSE on the Spreadsheet is picked up by the AI and saved as markdown during processing.

### Q22. What should I write in the 'Note' and 'Description' fields of a spec? (Web)

- **Description:** an overview of the item and the user interactions with that item.
- **Note:** supplementary explanations for each section in the spec.

For button-type items, DB changes on click should be written in the "Description".

### Q23. How do the AI code-generation flows of MoMorph and the Takumi kit differ? (MCP & CLI)

- **MoMorph slash commands (current):** start with `/specify` → generates spec.md + design-style.md + assets → `/plan` → `/tasks` → `/implement`. This is MoMorph's official workflow and is still fully supported.
- **Takumi kit (supplementary toolkit):** integrated on top of MoMorph and more flexible: `/create-plan` → `/takumi`, or call `/takumi` directly. It is not a MoMorph slash command — the Takumi kit must be installed separately.

### Q24. How should a designer build the Figma to collaborate best with the AI? (Figma)

**Organization structure:** make use of Pages; name screens/items accurately; standardize components; remove unnecessary hidden frames/layers; avoid overly long screens.

**Design technique:** use Auto Layout consistently; design all states (including edge cases); be disciplined with Component Instances.

**Figma structure:** 1 Frame = 1 screen; there is a Section nesting depth limit; be conscious of the hierarchy structure from the start.

### Q25. Does duplicating item names on Figma cause problems? (Figma)

Duplicate item names can cause errors on MoMorph. The issue has been reported and the team is reviewing a fix. Best practice: **always give items unique names** within the same scope.

### Q26. Does MoMorph create specs from the design or from the old spec? (AI Generation)

Per the MoMorph team: MM **generates a reasonable spec directly from the Figma design**, without requiring a reference to the old spec.md. Without referencing the old spec it's harder to produce more detailed analysis — but the design goal is to create a reasonable spec from the design itself. (Related to Q21 on spec sync.)

### Q27. What limits should I keep in mind when designing Figma for MoMorph? (Figma)

- **Frame = 1 screen:** MoMorph reads each Frame as an independent screen.
- **Section nesting limit:** there is a depth limit; don't nest too deeply.
- Recommended (not required): don't create redundant layers.
- Be conscious of the hierarchy structure from the start of the design.

Subscribing to a paid Figma plan should be based on how frequently the design changes — it's not required for the whole team.

## License & Operations

### Q28. May I post project information on the shared support channel? (General)

To avoid leaking project information: limit posting content containing PJ info on the shared channel; when detailed discussion is needed, use a dedicated DM group (add a MoMorph team representative when needed).

### Q29. How do the Essential and Pro plans differ? (License)

Per the User Guide:

- **Essential**: **Plugin only** — manage screens, enter specs manually, export GitHub issues. No access to the Web App, Syncer, CLI, MCP, VSCode Extension, or Claude Desktop Extension.
- **Pro**: **the entire ecosystem** — Plugin (full) + Web + Syncer + CLI + MCP + VSCode Extension + Claude Desktop Extension.

`@sun-asterisk.com` emails are automatically Pro; other emails contact Slack to be whitelisted.

### Q30. How is using AI (Copilot, Claude Code) in MoMorph billed? (License)

- Generating specs & test cases: you can use the MoMorph BE or Copilot.
- Generating code: Claude Code is recommended; you can request a Claude Code Premium Seat depending on the phase.
- Copilot has some usage limits according to the license plan.

### Q31. Using AI (MCP) returns an authentication error — what usually causes it? (MCP & CLI)

Usually caused by a **revoked/expired GitHub PAT** (error `x-github-token invalid / 401`). How to fix:

- Create a new PAT with the `user` scope and update it in the MCP config (e.g. `~/.claude.json`).
- If using `momorph init`: run `momorph login` so the token auto-merges into the config.

### Q32. Which channel do I use to send questions / feedback to MoMorph? (General)

The feedback channel has been merged into **#con_momorph-support_all**. The old channel #temp_archived_moved-to-con_mormorph-support_all has been archived.

### Q33. Is there a user guide for MoMorph? (General)

Yes. The MoMorph team provides an official set of documents:

- **MoMorph — User Guide** (Plugin, Web, Syncer, CLI, MCP, VSCode Extension, Claude Desktop Extension) — EN/JP/VI editions.
- **MoMorph MCP Server — Tools Reference** (describes 31 tools).
- Release Notes, Testplay, Q&A List.

Request the files directly on Slack `#con_momorph-support_all`.

### Q34. When I hit an error, how should I report it to the MoMorph team? (General)

When you encounter any of the errors above:

- Fill out the **detailed bug report form** as required by the MoMorph team.
- **Remove or mask any images containing sensitive/confidential information** before sending.

If it relates to specific screen data, provide the ScreenID so the team can resolve it faster.

## Feature Requests

### Q35. Can an overview description field be added to the spec? (Web)

Official request: the AIDD process needs an "overview description" field to describe the overview, which MoMorph does not currently provide. The request has been sent to the MoMorph team.

### Q36. Can I paste multiple rows at once into a List Item? (Web)

Currently, entering multiple rows into a List Item is inconvenient. Users want a feature to copy & paste multiple rows from external sources (Excel, text) into a List Item.

### Q37. If a designer accidentally duplicates item names, can MoMorph handle it automatically? (Figma)

Users have asked the MoMorph team to research a fix for duplicate item names. Currently there's only the "use unique names" recommendation — the request is for MoMorph to handle duplicate names more flexibly.

### Q38. Where do I send feature requests to MoMorph? (General)

Users have asked about an official form/channel for submitting feature requests — they want a structured mechanism for receiving feature suggestions.

### Q39. Does MoMorph ask for user input before releasing new features? (General)

Request: there should be a mechanism to collect feedback before releasing new features, plus advance notification of release notes so users have time to prepare.

### Q40. Connecting a GitHub account vs a repo is confusing — any improvement planned? (Web)

Many users confuse "connecting a GitHub account" with "connecting a repository". The request is to improve the UI so the two concepts are clear, separate, and not misleading.

### Q41. When syncing with Excel, are columns that MoMorph doesn't have lost? (Web)

Currently, fields that don't exist in MM must be entered manually in Excel. The request is for MoMorph not to filter the displayed fields, allowing all fields to be kept — including fields MM doesn't yet manage — to reduce manual entry.

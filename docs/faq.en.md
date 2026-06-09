# MoMorph — FAQ & Troubleshooting Guide

## License & Operations

### <u>Difference between Essential and Pro</u>
**❓ Q:** How do the Essential and Pro user plans differ?

**💡 A:** According to the User Guide, the two plans differ in feature scope:

- **Essential**: can only use the Plugin — managing screens, entering specs manually, and exporting GitHub issues. This plan cannot access the Web App, Syncer, CLI, MCP, VSCode Extension, or Claude Desktop Extension.
- **Pro**: can use the entire ecosystem — Plugin (full), Web, Syncer, CLI, MCP, VSCode Extension, and Claude Desktop Extension.

Users whose email is on the Sun* company domain are Pro accounts by default. For other emails, please contact the MoMorph team to be granted a Pro account.

### <u>Contact & support channels</u>
**❓ Q:** Through which channels can I send questions or feedback to MoMorph?

**💡 A:** You can contact us via:

- Slack: **#con_momorph-support_all**
- Email: **momorph-admin@sun-asterisk.com**

Note: please remove or mask any images containing sensitive/confidential project information before sending.

## Bugs & Issues

### <u>CLI reports 'user not found'</u>
**❓ Q:** What should I do when logging in to GitHub in the CLI returns a 'user not found' message?

**💡 A:**

- Please log in to the CLI again with `momorph login`, then check with `momorph whoami`.
- Also, make sure the firewall/VPN does not block `github.com/login/device`.

### <u>Account not added to the GitHub project</u>
**❓ Q:** I cannot connect to GitHub and receive a message that the account has not been added to the project. How should I handle this?

**💡 A:** Please perform the GitHub link on MoMorph Web (Settings → GitHub → Connect repo).

### <u>Items do not appear or are in the wrong order</u>
**❓ Q:** I assigned a number to the Figma layer name but MoMorph cannot load the item, or the item order is wrong. How should I handle this?

**💡 A:** Some common causes:

- The layer name does not have the correct `mms_` prefix. Please rename the layer on Figma in the form `mms_<name>`.
- The data on MoMorph is not in sync with the order of the Figma layer tree, leading to missing items or wrong order.

You can fix this as follows:

- Click the **Refresh** button on the Preview bar of the MoMorph Plugin to reload/re-sync the items.
- Use the **"Find on Figma"** button to check whether the item/screen currently open matches the desired Figma frame.
- Note that layers that are hidden or are the outermost parent frame will not be loaded.

### <u>The No value on MoMorph is incorrect</u>
**❓ Q:** Why does the No value on MoMorph not match the prefix assigned to the Figma layer name?

**💡 A:** This is intended behavior in MoMorph:

- The number in the Figma layer name is only used as the Item No for the **first data sync** to the MoMorph server.
- After that, if you want to change the "No" value, please edit it directly in the "No" column on MoMorph; the system does not sync back to Figma. This approach avoids data conflicts when the "No" value you edit on the Web differs from the number in the Figma layer name.

### <u>Lost spec after replacing the Figma frame</u>
**❓ Q:** After editing the design on Figma, the spec data I entered on MoMorph was lost. Why, and how can I fix it?

**💡 A:** This situation usually occurs when you use Figma's Paste to Replace function to replace the original frame with a frame that has a newer design. When that happens, the original frame on MoMorph is deleted; the spec created for the original frame is still kept but switches to the No UI state (no design yet), while the new frame appears in the list of screens without a spec.

The cause is that Figma assigns a completely new ID to the replacement frame, so currently MoMorph cannot automatically recognize the original frame to transfer the spec data to the new frame.

How to fix: in the Preview area of the original screen (currently in the No UI state) on MoMorph, please use the link frame function to link this spec to the new design frame. In the item list, the UI Part column also needs to be re-linked to the corresponding layers of the new frame.

### <u>AI generation stops midway</u>
**❓ Q:** What should I do when AI content generation stops midway or reports a server error?

**💡 A:**

- For screens with many items, the AI content generation process may take around **30–60 seconds**. Please wait a little longer before treating this as an error.
- If the system reports a server error, the cause may be that the MCP server is overloaded or experiencing a temporary issue. Please wait a moment and try again.

### <u>Google Sheets sync error</u>
**❓ Q:** What should I do when syncing specs between MoMorph and Google Sheets fails?

**💡 A:** This is a feature of **MoMorph Syncer** (Google Add-on). Some common errors:

- **"Cannot access spreadsheet"**: the file must belong to the Sun* company's Google Workspace, and your account must have **Editor** permission on that file (Viewer permission cannot sync back).
- **"Missing authentication token"**: the Google login session has expired. Please log in again with an email on the Sun* company domain and reload the Sheets tab.
- **"Failed to sync data"**: this may be due to a network or system interruption. Please wait a few minutes and try again.

### <u>Error when exporting spec to GitHub</u>
**❓ Q:** What should I do when sending a spec to GitHub reports an error?

**💡 A:** Please check the GitHub connection settings screen, then try disconnecting and reconnecting your GitHub account and repository.

### <u>CSV file has font errors</u>
**❓ Q:** What should I check when a CSV file opens with font errors?

**💡 A:** Please check the tool (preview tool) you are using to open the CSV file. If the tool is working normally but the content continues to display incorrectly, please contact the MoMorph team for support.

## Setup & Usage

### <u>Best practices for designing Figma for AI</u>
**❓ Q:** How should designers design in Figma to collaborate with AI most effectively?

**💡 A:** You can refer to some of the following suggestions:

- **Structure & organization:** make use of Pages; name screens/items clearly and uniquely (duplicate item names can cause errors when using AI to generate the item list or spec); standardize components; remove unnecessary hidden frames/layers; and avoid making screens too long.
- **Design techniques:** use Auto Layout consistently; design all states, including edge cases; and use Component Instance with discipline.
- **Figma structure:** each Frame corresponds to one screen; the number of Section levels should be kept within a maximum of 7 levels (if it exceeds 7 levels, MoMorph may not be able to recognize Frames nested deep from the 8th level onward); and you should be mindful of the hierarchical structure from the start.

### <u>Item naming rules (mms_ / id_)</u>
**❓ Q:** What is the naming convention for items so MoMorph recognizes them, and when will the old 'id_' name stop being supported?

**💡 A:**

- **New rule:** add the `mms_` prefix to the layer name. The numbering content can be viewed and edited directly on MoMorph.
- **Old rule:** the `id_` prefix will no longer be recognized after 30/05/2026.

### <u>Data source when creating a spec</u>
**❓ Q:** Does MoMorph create spec.md based on the design or based on the old spec?

**💡 A:** MoMorph generates the spec directly from the design on Figma. However, additionally referencing the old spec helps provide more detailed analysis of the changes.

### <u>Scope of Google Sheets sync</u>
**❓ Q:** When I edit a spec on Google Sheets, does the content automatically update to the Plugin/Web and the spec.md file (created when generating code)?

**💡 A:**

- Content changed on the Spreadsheet is only updated to the MoMorph server through the MoMorph Syncer sync menu.
- This content does **not** automatically sync to the spec.md file.

### <u>Getting AI to fetch the spec from MoMorph</u>
**❓ Q:** After finishing the setup on the Web, how do I get AI to fetch the spec from MoMorph?

**💡 A:** You can follow these steps:

- Install the CLI: `brew install momorph/tap/momorph-cli`.
- Run `momorph login`, then `momorph init . --ai <agent>` (claude/copilot/cursor…) to automatically configure the MCP server and slash commands.
- After that, the AI agent will automatically call the MCP tools (via slash command or a normal prompt) to fetch the spec — for example `/downloadspecs` or a prompt with the screenId.

You do not need to call MCP directly.

### <u>Code generation workflow: MoMorph vs Takumi kit</u>
**❓ Q:** How does the AI code generation process differ between MoMorph and Takumi kit?

**💡 A:**

- **MoMorph slash command (current):** start with `/specify` to generate spec.md, design-style.md, and assets, then in turn `/plan` → `/tasks` → `/implement`. This is the official MoMorph workflow and is still fully supported.
- **Takumi kit (supplementary toolkit):** integrated on top of MoMorph and more flexible, using `/create-plan` → `/takumi` or calling `/takumi` directly. You need to install the Takumi kit separately to use it.

### <u>Updating when a new version is released</u>
**❓ Q:** MoMorph just released a new version; what do I need to do to update?

**💡 A:** Due to Figma's caching mechanism, please reload in the following exact order to receive the changes: **1. Figma → 2. Plugin → 3. Web**.

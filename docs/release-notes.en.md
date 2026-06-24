# MoMorph — Release Notes

The latest MoMorph updates across Plugin, Web, and MCP Server.

## 2026-06-25

**✨ New & Improved**

- **Update reminder after maintenance** — When a maintenance window ends, a notification now prompts you to reload (the Figma file in Plugin, or the page on Web) to get the latest version. You can dismiss it and keep working.
- **Smoother bulk AI spec generation** — Generating specs for many items at once is more stable (no more 502/503 errors on large batches); you'll see a notice that generation may take a little longer.
- **More reliable frame sync on large files** — Syncing screens on large Figma files (200+ frames) is more robust, with batching and retries to avoid timeouts and data loss on flaky networks.

**🐛 Fixes**

- **Auto-numbering by layer hierarchy** — Numbering now follows the Figma layer order top-to-bottom, and drag-to-reorder is reliable.
- **Screen Detail preview (Web)** — Fixed the preview image flickering when opening a screen.
- **Back navigation (Plugin)** — Fixed the blank white screen when going back to the frame set list.
- **Destination field (Spec Form)** — The dropdown no longer lists non-existent frames, and a required Destination can no longer be saved while empty.
- **Item status after sync** — AI-generated items now correctly switch to **Done** after syncing to MoMorph.
- **Item Type on sheet** — AI-generated button items now show `Button` (instead of `Button-Icon/Text`) when synced to the spreadsheet.
- **Translation dictionary upload** — Fixed an error when uploading dictionary `.xlsx` files.
- **Issue upload** — Fixed missing `No` and `Name` on items after uploading an issue to GitHub.
- **Media upload** — Fixed media upload failures.

---

## Previous releases

- [2026-06-19](release-archive.md#2026-06-19) — More flexible screen spec input (one of `No` / `Item Name` / `UI Part`).
- [2026-06-11](release-archive.md#2026-06-11) — Maintenance pre-notice, AI spec generation on Web, Figma Group layer support, flexible spec input, and MCP Server updates.
- [2026-05-28](release-archive.md#2026-05-28) — Maintenance mode, a new 3-state Screen Spec sort & reorder, and fixes for missing UI Part items and queued AI spec cancellation.
- [2026-05-21](release-archive.md#2026-05-21) — Refined Screen Detail, batch AI spec cancellation, Screen ID search, one-time Figma URL setup, and wide-ranging fixes.
- [2026-05-07](release-archive.md#2026-05-07) — Upgraded Filter Modal, faster Screen Detail loading, and fixes across Spec Upload, MM Syncer, and MCP/CLI re-upload.
- [2026-04-24](release-archive.md#2026-04-24) — Fixed missing data for GitHub-signed-in users via VSCode Extension, MCP, and CLI; tightened repo connect/disconnect permissions.
- [2026-04-23](release-archive.md#2026-04-23) — Always-editable Screen Spec, CSV download, bulk frame delete/undo, plus a wide range of sync, preview, and connectivity fixes.
- [2026-04-09](release-archive.md#2026-04-09) — Toggle spec labels on preview, improved AI generation context, and unified `screen_id` URLs.
- [2026-04-01](release-archive.md#2026-04-01) — AI-generated screen overviews and item definitions, Active Item List, consecutive numbering, and Screen Spec copy.
- [2026-03-27](release-archive.md#2026-03-27) — Nested section support, automatic legacy layer prefix migration, and spec-data loss fixes.
- [2026-03-20](release-archive.md#2026-03-20) — Status tabs for the screen list, screen archiving, Markdown item specs, and the unified `mms_` layer prefix.
- [2026-03-12](release-archive.md#2026-03-12) — Fixed Plugin/Web data sync on the Screen Spec view and session-expiry error messaging.
- [2026-02-13](release-archive.md#2026-02-13) — Spec version control, the All Specs Screen, Project Overview settings, and deleted-layer spec recovery.
- [2026-01-15](release-archive.md#2026-01-15) — Frame List UX, clearer authentication errors, image URL security, plus Media Scan & Upload and Syncer i18n.
- [2025-12-24](release-archive.md#2025-12-24) — Custom item numbering, flexible account linking, spec sync for new items, and tag/page-extraction fixes.
- [2025-12-11](release-archive.md#2025-12-11) — UI/UX improvements, Japanese and Vietnamese support on more screens, and stability fixes.
- [2025-11-27](release-archive.md#2025-11-27) — Performance improvements on large Figma files, optimized tags, and stronger backend sync.
- [2025-11-13](release-archive.md#2025-11-13) — Security hardening, Figma API rate-limit handling, Terms/Policy on Welcome, and a 404 page.

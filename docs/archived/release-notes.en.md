# MoMorph — Release Notes

The latest MoMorph updates across Plugin, Web, and MCP Server.

## 2026-07-09

**✨ New & Improved**

- **Filter the Item List (Plugin & Web)** — On the Screen Spec, the Item List (Active tab) now has filters on four columns: `No` and `Name` (single-select), plus `UI Part` and `Spec Status` (multi-select, covering `Generating` / `AI completed` / `Gen error` / `In Progress` / `Done`). Filters combine across columns and within a column, sorting by `No` keeps them applied, and an empty state appears when nothing matches. Drag-to-reorder is disabled while a filter is active.

**🐛 Fixes**

- **Preview number on synced sheet** — After you re-number items and re-sync MM → Google Sheet, the preview images now update to match the new numbering (previously the image kept the old number while the other fields were already correct).
- **Layout blur / transparency (Plugin & Web)** — Blur effects (Layer Blur, Background Blur, glassmorphism) now render as designed in Figma, instead of showing a solid background on overlays and panels.

---

## Previous releases

- [2026-06-25](release-archive.md#2026-06-25) — Update reminder after maintenance, steadier bulk AI spec generation, more reliable large-file sync, plus auto-numbering, sync, and upload fixes.
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

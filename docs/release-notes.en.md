# MoMorph — Release Notes

The latest MoMorph updates across Plugin, Web, and MCP Server.

## 2026-06-11

**✨ New & Improved**

- **Maintenance pre-notice** — A heads-up modal now appears in Plugin & Web before a scheduled maintenance window, showing the time in your timezone.
- **Generate spec with AI on Web** — Now available from the action menu on both Screen Spec and View All Specs, matching the Plugin.
- **Figma Group layers** — Layers of type Group can now be linked, edited, and managed just like any normal design item.
- **Flexible spec input** — Required-field restrictions removed (only a name or No. is required) so you can fill specs freely across diverse projects.
- More consistent multilingual labels and new item-toolbar tooltips across Plugin & Web.

**🐛 Fixes**

- AI spec generation is more stable on production — no longer skips empty `Name` fields or overwrites `item type` in do-not-overwrite mode, and fixed the "items not found in frame" error after edit/reload.
- Translation now covers long text segments that were previously left untranslated.
- Fixed UI Part re-linking — reassigning a layer between items, and relinking after a designer replaces a layer.
- Fixed errors when relinking a screen to a new design.
- Item completion status now sticks — it stays `Completed` after Entry complete, and no longer reverts from `Completed` back to `AI completed`.
- Other fixes: Save/Cancel buttons on AI-error items, duplicate text on Japanese/Vietnamese input, missing total count on the Web Screen List, the maintenance error toast no longer shown to users, and the Web now blocks AI spec generation for missing items (matching the Plugin).

**🔌 MCP Server**

- **Breaking — the legacy `status` field was removed** from `create_frame`, `get_frame`, and `list_frames`. Use the four `*_status` fields (`design_status`, `spec_status`, `dev_status`, `review_status`) instead, and update any agent or workflow that still reads or writes `status`.
- **New `update_frame` tool** — patch screen metadata (name, overview, statuses, Figma node link) without recreating the frame.
- **`figma_node_id` support** — `create_frame`, `update_frame`, `get_frame`, and `list_frames` now accept and return `figma_node_id` in canonical (`12318:23788`), hyphenated (`12318-23788`), or full Figma URL form.
- `list_frames` no longer returns archived screens.

---

## Previous releases

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

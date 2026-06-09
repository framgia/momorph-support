# MoMorph — Release Notes Archive

Past MoMorph releases. For the latest, see [Release Notes](release-notes.md).

## 2026-05-07

**✨ New**

- **Upgraded Filter Modal** — new filter options and filter state preserved when navigating back.

**🔧 Improvements**

- Faster Screen Detail loading; less lag on Screen Spec / Item Spec with many items.
- Smoother Screen Spec editing, syncing, and revision tracking.
- Better frame deletion logic to reduce NoUI screens.

**🐛 Fixes**

- Fixes across Filter Modal, preview labels, frame auto-naming, Spec Upload (Web), MM Syncer, and MCP/CLI re-upload.

---

## 2026-04-24

**🐛 Bug Fixes for GitHub repository permission**

- Fixed missing data (tags, media, comments, localized images) for users signed in via GitHub called from VSCode Extension, MCP, CLI.
- Only MoMorph users with Admin permission on the GitHub repository can connect/disconnect a repo to/from a Figma file.

---

## 2026-04-23

**✨ New Features**

- **Always-editable Screen Spec** — Removed View/Edit mode separation. The table is always in edit mode by default; item numbers are now entered manually instead of auto-incremented.
- **Download Spec as CSV** — Screen spec data can now be exported and downloaded in CSV format.

**🔧 Improvements**

- **Bulk Delete/Undo for Figma frames** — The Plugin now supports deleting and undoing multiple frames at once directly in Figma.
- **Design item order** — Items on Screen Spec now follow the default Figma layer tree order.
- **AI Item Generation** — `node_link_id` list is now included in the payload for more accurate AI-generated specs.
- **Search keyword persistence** — Search keywords on Screen List are now preserved in the URL query params during navigation.
- **GA4 Analytics** — Added `file_key` to all GA4 events for per-Figma-file filtering.

**🐛 Bug Fixes**

- **Data sync & upload:** Fixed sync errors from Google Sheet to MoMorph; archived items no longer included in GitHub uploads; "No Design" screens now correctly move to "In Development" after Plugin upload; duplicate screens no longer created on Web.
- **Deleted/archived items:** Fixed deleted items reappearing after Plugin reload and in Google Sheet uploads; fixed archived items not restorable after clicking reload preview icon.
- **Screen Spec editing:** Fixed new row input being reset and not auto-saved when selecting a Figma layer; fixed item list cached when switching specs in Frame Set; fixed 404 error on Screen Spec reload.
- **Preview & design linking:** Fixed incorrect preview for frames with unlinked UI Parts; fixed preview not syncing on first Screen Detail access from Screen Set; fixed unlinked designs being auto-reassigned to auto-generated boxes instead of remaining in manual link pending state.
- **Google Sheet upload:** Fixed item type filtering issue (Web showed only Button, Plugin showed others); fixed image zoom mismatch hiding edge labels.
- **Plugin connectivity:** Fixed intermittent fetch conflict preventing delete/archive; fixed repository not editable after GitHub reconnect; fixed missing Cancel/Escape when selecting a Figma node.
- **Other:** Fixed Screen Detail failing to load; fixed Screen Set list not fully scrollable; fixed Google disconnect failing when token expired; fixed media scan after applying new mms node prefix; fixed dictionary upload timeout during AI retranslation; fixed a security issue in the VSCode Extension related to data-access permissions.

---

## 2026-04-09

**✨ New Feature**

- **Toggle spec labels on preview** — You can now show or hide spec labels directly on the design preview area, making it easier to inspect the design without visual clutter.

**🔧 Improvements**

- **AI Spec & Test Case Generation** — Screen overview is now sent as context to the AI service, improving the accuracy and relevance of generated specs and test cases.
- **Auto-scroll on Design ID click** — Clicking a Design ID on the preview automatically scrolls to and highlights the corresponding item in the list.
- **Copy Screen ID feedback** — A toast notification now appears when you copy a Screen ID, confirming the action was successful.
- **Tooltip polish** — All tooltips now have a 400ms delay and a smooth fade-in effect for a more refined experience.
- **Layer ID detection** — The Plugin now correctly recognizes layers with the `mms_id_` prefix on initial load.
- **URL consistency** — Screen URLs now use `screen_id` instead of frame id across the entire system.

**🐛 Bug Fixes**

- Several bugs fixed, including issues with preview rendering, spec synchronization, archived frames, UI Parts, Input Spec saving, AI generation status, and GitHub repository search.

---

## 2026-04-01

**🆕 What's new**

- Edit screen title and overview directly from the screen list.
- Screen ID is now visible on the screen list — use it to identify screens when downloading or uploading specs via MCP server.
- Active item list: view, add, and sort design elements in one place.
- Assign spec numbers in bulk with the new consecutive numbering feature.
- Copy specs between screens.
- AI can now auto-generate screen overviews and item definitions from your Figma UI.

**✨ Improvements**

- Overwrite confirmation modal updated for spec generation.
- AI test case generation settings modal refreshed.
- Google Sheets sync reliability improved.

**🔧 Bug fixes**

- Fixed plugin failing to detect layers with special characters in their name.
- Fixed non-admin users being able to unlink a repo in Settings / Github.
- Various display and interaction fixes across Screen List, Screen Spec, and Screen Set.

---

## 2026-03-27

- **Features & Improvements:** Supported nested sections in Figma hierarchy, and auto-migrated legacy layer prefixes.
- **Bug Fixes:** Fixed an issue where data specs were lost after returning from settings, resolved multi-item AI spec generation failures, and corrected missing settings labels when clicking certain characters.

---

## 2026-03-20

**🆕 New Features**

- Screen list is now split into 4 status tabs (Designing / Developing / Review / Done) with count badges.
- Screens can be Archived and restored at any time. Previously hidden screens migrate to Archive automatically.
- Screens with incomplete design (No UI / In Design) are now clickable to view details.
- Item specs now support Markdown — use the new toolbar for bold, lists, code blocks, and more. Synced across Plugin & Web.
- Item spec form now supports ID input and direct Figma layer linking. Layer names auto-prefix with "mms_".
- Figma layer prefix unified to "mms_" across the app. Old formats convert automatically.

**✨ Improvements**

- Screen Set UI fully redesigned (List / Add / Detail / Edit). Supports Japanese, English, and Vietnamese labels.
- Screen Spec preview area now has a fullscreen mode and spec numbering settings button.
- Lifecycle status (Design / Spec / Development) can now be updated directly from the screen detail view, reflected in real time.

**🔧 Bug Fixes**

- Google account expiry in Upload Spec now shows a clear error message with a reconnect button.
- AI-generated specs now reflect immediately in the UI without needing a page reload.
- Fixed a false "Leave page?" modal appearing after saving on the Tag management screen.
- AI generation failures now properly show an error toast and update item status (generating → error / timeout).
- Tag management button styles are now consistent with the rest of the app.

**🗑️ Removed**

- "Default Mode" option removed from Settings (replaced by status tab layout).
- Frame Lock feature removed — Figma frames are freely editable while writing specs.
- AI generation confirmation modal removed for items with no existing spec (settings screen opens directly).

---

## 2026-03-12

**Bug Fixes**

- Data Synchronization: Fixed an issue where data would not automatically sync between the Plugin and the Web application when opening the Screen Spec view.
- Error Handling: Fixed an issue where no error message was displayed in the Figma URL input field when a user's session had expired.

---

## 2026-02-13

**[What's New & Improved]**

- Enhanced Specification Management: We've upgraded the Element Spec Version Control and implemented a new All Specs Screen to view all item specifications in one place.
- New Project Overview: A dedicated Project Overview settings screen has been added for easier configuration.
- Data Recovery: Specs for deleted or hidden layers can now be restored upon layer recovery.
- Export Customization: You can now choose whether or not to export i18n sheets.
- AI generator: Improved specs quality generated by AI.
- UI/UX Refinements:
  - Updated the UI for the "Leave Page" confirmation modal.
  - Improved label texts on the GitHub Integration Settings screen.

**[Bug Fixes]**

- Time Format Display: Fixed an issue where time formats were inconsistent when switching languages in the Status History.
- Status Update: Resolved a bug where the Test Case Generation status failed to update after a successful upload to Google Sheets.
- Multilingual Issues: Label text of GitHub Upload did not change in the Japanese environment.
- Filtering Logic: Corrected an issue where frames excluded in "For Design" mode were incorrectly moved to the In Design list.
- Performance: Addressed the issue of file thumbnails not displaying for expired files.

---

## 2026-01-15

**[Updates]**

- UX Improvements: Enhanced user experience in the Frame List by auto-focusing after tag editing.
- Error Messaging: Clarified error messages related to email whitelisting and account authentication.
- Media Scan & Upload: Added the ability to scan and upload media files.
- MoMorph Syncer: Added multi-language (i18n) support to the menu.

**[Other]**

- Security: Strengthened security protections for image URLs when exporting issues to GitHub and Google Sheets.

---

## 2025-12-24

**🚀 What's New & Improved**

- Custom style for item's numbering label
- Flexible Integration: You can now connect GitHub/Google accounts using any email address.
- Spec Sync: Added support for syncing specs of newly added design items to existing sheets.
- UX Improvements: Improved initial language detection, and refined toast messages.

**🐛 Bug Fixes**

- Fixed the Tag Filter logic (now works as "Partial Match" instead of "Exact Match" for system tags).
- Fixed an issue where Page Extraction displayed frames from all pages instead of the selected ones.
- Resolved UI inconsistencies in the Tag List.

**⚠️ Action Required:** Please reload your Figma tab or restart the plugin to apply these changes.

---

## 2025-12-11

**[Updates]**

- **UI/UX Improvements:** Enhanced the design and usability of upload, settings, and other key screens.
- **Multi-language Support:** Added support for Japanese and Vietnamese in login and other screens.
- **Optimization:** Improved spreadsheet export naming and clarified error messages.

**[Fixes]**

- Stability Improvements: Fixed various issues related to AI spec generation, image syncing, and revisions to ensure smoother operation.

---

## 2025-11-27

- **Performance:** Improved stability and speed when handling large Figma files.
- **Tags System:** Optimized filtering, saving, and display logic.
- **Fixes & UI/UX:** Enhanced GitHub integration reliability and resolved various interface bugs.
- **Backend:** Strengthened data analytics infrastructure and synchronization stability.

---

## 2025-11-13

- **Improvements:** Enhanced security, implemented Figma API rate limit handling, added Terms/Policy to the Welcome screen, and implemented a 404 page.
- **Critical Fixes:** Resolved a spec-saving failure, fixed incorrect data display for new "frame sets," and corrected the "Generate Test Case" status getting stuck "In Queue."
- **Other Fixes:** Corrected various minor UI/UX bugs.

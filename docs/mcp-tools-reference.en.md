# MoMorph MCP Server — Tool Reference

Complete reference for all **32 tools** that the MoMorph MCP server exposes for interacting with design data, specs, test cases, media, and node tree in MoMorph.

> **Terminology:** This doc uses **Screen (Frame)** and **ScreenSet (FrameSet)** as the primary terms. "Frame"/"FrameSet" are legacy names.

---

## Table of Contents

1. [Common Concepts](#common-concepts)
2. [Tool Index (Quick Lookup)](#tool-index-quick-lookup)
3. Tool Reference by Group:
   - [3.1 Specs](#31-specs)
   - [3.2 Test Cases](#32-test-cases)
   - [3.3 Media](#33-media)
   - [3.4 Figma Design](#34-figma-design)
4. [Identifier Glossary](#identifier-glossary)

---

## Common Concepts

### Result Types

Tools return one of these result types:

| Type  | Use case                                    |
| ----- | ------------------------------------------- |
| JSON  | Structured data (objects, arrays)           |
| Text  | Plain text / fallback messages when no data |
| Image | Image data as base64 or URL                 |
| Error | Error result with a message                 |

### Authentication

Requires one of the following headers (priority order, highest first):

| Header                    | Priority | Used for                                              |
| ------------------------- | -------- | ----------------------------------------------------- |
| `x-momorph-authorization` | 1        | MoMorph token (recommended)                           |
| `authorization`           | 2        | Standard bearer token                                 |
| `x-github-token`          | 3        | GitHub token (when accessing GitHub-linked resources) |
| `x-figma-token`           | 4        | Figma token (when calling Figma API directly)         |

### Common Input Conventions

- `fileKey` — Figma/MoMorph file identifier (string, e.g. `"abc123XYZ"`)
- `screenId` — Unique Screen (Frame) identifier in MoMorph (string, e.g. `"scr_xxx"`)
- `nodeId` — Figma node ID (string, e.g. `"2167:9091"`)
- Sub-status enums: `design_status` / `spec_status` / `review_status` = `none` \| `in_progress` \| `done`; `dev_status` = `none` \| `developing` \| `done`

**Get `fileKey` and `screenId` from a MoMorph URL:**

```
https://momorph.ai/files/{fileKey}/screens/{screenId}
```

Example: `https://momorph.ai/files/9ypp4enmFmdK/screens/i87tDx10` → `fileKey = "9ypp4enmFmdK"`, `screenId = "i87tDx10"`.

### Output Conventions

- Screen info returns: `screen_id, name, design_status, spec_status, dev_status, review_status, revision (commit_hash), tags, created_at, updated_at`
- CSV exports use UTF-8 with column headers (22 cols for specs, 18 cols for test cases)

---

## Tool Index (Quick Lookup)

| #   | Tool Name                                                  | Group        | Purpose                                                                                     |
| --- | ---------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------- |
| 1   | [`get_project_overview`](#1-get_project_overview)          | Specs        | Get project-level overview description                                                      |
| 2   | [`create_frame`](#2-create_frame)                          | Specs        | Create a new Screen in MoMorph                                                              |
| 3   | [`get_frame`](#3-get_frame)                                | Specs        | Get full details for a Screen                                                               |
| 4   | [`update_frame`](#4-update_frame)                          | Specs        | Update Screen metadata (name / screen_overview / 4 sub-status)                              |
| 5   | [`list_frames`](#5-list_frames)                            | Specs        | List all Screens (filter by 4 sub-status)                                                   |
| 6   | [`list_frame_sets`](#6-list_frame_sets)                    | Specs        | List all ScreenSets                                                                         |
| 7   | [`get_frame_set`](#7-get_frame_set)                        | Specs        | Get a ScreenSet with its child Screens                                                      |
| 8   | [`upload_specs`](#8-upload_specs)                          | Specs        | Upload / update specs for a Screen                                                          |
| 9   | [`download_specs`](#9-download_specs)                      | Specs        | Export Screen specs to CSV / JSON                                                           |
| 10  | [`list_design_items`](#10-list_design_items)               | Specs        | List all specs of a Screen                                                                  |
| 11  | [`list_frame_spec_diffs`](#11-list_frame_spec_diffs)       | Specs        | Compare spec changes vs latest revision                                                     |
| 12  | [`get_related_design_items`](#12-get_related_design_items) | Specs        | Get related specs for a Screen (if any)                                                     |
| 13  | [`upload_test_cases`](#13-upload_test_cases)               | Test Cases   | Upload / update test cases for a Screen                                                     |
| 14  | [`download_test_cases`](#14-download_test_cases)           | Test Cases   | Export test cases to CSV / JSON                                                             |
| 15  | [`get_frame_test_cases`](#15-get_frame_test_cases)         | Test Cases   | Get test cases of a Screen                                                                  |
| 16  | [`get_frame_image`](#16-get_frame_image)                   | Media        | Get Screen preview image, optionally with spec number overlay                               |
| 17  | [`list_media_items`](#17-list_media_items)                 | Media        | List media nodes in a Screen                                                                |
| 18  | [`list_media_nodes`](#18-list_media_nodes)                 | Media        | List all media nodes with role hints (background/icon/overlay/...)                          |
| 19  | [`get_media_files`](#19-get_media_files)                   | Media        | Get download URLs for all media assets (SVG/PNG/JPG) in a Screen                            |
| 20  | [`get_media_file`](#20-get_media_file)                     | Media        | Download a media asset (SVG/PNG/JPG) of a node directly from storage                        |
| 21  | [`get_figma_image`](#21-get_figma_image)                   | Media        | Export any Figma node to PNG/JPG (may hit Figma rate-limit)                                 |
| 22  | [`get_design_item_image`](#22-get_design_item_image)       | Media        | Get a cropped image of a specific spec item (design item)                                   |
| 23  | [`get_frame_node_tree`](#23-get_frame_node_tree)           | Figma Design | Get the full hierarchical node tree of a Screen                                             |
| 24  | [`get_overview`](#24-get_overview)                         | Figma Design | Get a lightweight overview tree (names + types only) — use first to orient                  |
| 25  | [`query_section`](#25-query_section)                       | Figma Design | Query a subtree by node ID or fuzzy name                                                    |
| 26  | [`query_component`](#26-query_component)                   | Figma Design | Find a component by name (fuzzy match, ranked by relevance)                                 |
| 27  | [`query_by_type`](#27-query_by_type)                       | Figma Design | Filter all nodes by Figma type (TEXT, INSTANCE, FRAME, ...)                                 |
| 28  | [`get_node`](#28-get_node)                                 | Figma Design | Get a single node by exact node ID                                                          |
| 29  | [`get_node_context`](#29-get_node_context)                 | Figma Design | Get a node with parent, siblings, and layer role analysis (required before rendering image) |
| 30  | [`list_file_variables`](#30-list_file_variables)           | Figma Design | List CSS / design variables of the file                                                     |
| 31  | [`list_frame_styles`](#31-list_frame_styles)               | Figma Design | Get the full hierarchical CSS style tree of a Screen                                        |
| 32  | [`list_file_localizations`](#32-list_file_localizations)   | Figma Design | Get multilingual translations for source text strings                                       |

---

## 3.1 Specs

Tools for managing Screens (Frames), ScreenSets (FrameSets), and design item specs in MoMorph.

### 1. `get_project_overview`

Get the project-level overview description of a Figma/MoMorph file. Returns the text describing the project's purpose, scope, or context as set by the creator.

**Parameters:**

| Name      | Type   | Required | Description    |
| --------- | ------ | -------- | -------------- |
| `fileKey` | string | ✓        | Figma file key |

**Response (text):** `project_overview` string (or fallback message).

---

### 2. `create_frame`

Create a new Screen in a MoMorph file without linking it to Figma. Useful for initializing a standalone Screen to start entering specs/test cases.

**Parameters:**

| Name             | Type   | Required | Default | Description                                                                                                                                                                                                              |
| ---------------- | ------ | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fileKey`        | string | ✓        | —       | File key of the MoMorph file                                                                                                                                                                                             |
| `name`           | string | ✓        | —       | Frame name (non-empty)                                                                                                                                                                                                   |
| `screenOverview` | string | ✗        | —       | Description / overview of the screen                                                                                                                                                                                     |
| `figmaNodeId`    | string | ✗        | —       | Figma node ID this Screen links to. Accepts 3 forms: canonical `"12318:23788"`, hyphenated `"12318-23788"`, or a full Figma URL with `node-id=` — all normalized to canonical form. Omit or pass `""` for an unlinked Screen. |
| `designStatus`   | enum   | ✗        | —       | Design phase status: `none` \| `in_progress` \| `done`                                                                                                                                                                   |
| `specStatus`     | enum   | ✗        | —       | Spec phase status: `none` \| `in_progress` \| `done`                                                                                                                                                                     |
| `devStatus`      | enum   | ✗        | —       | Dev phase status: `none` \| `developing` \| `done` ⚠ (different from other 3)                                                                                                                                            |
| `reviewStatus`   | enum   | ✗        | —       | Review phase status: `none` \| `in_progress` \| `done`                                                                                                                                                                   |

> **Breaking change:** Legacy `status` (frame_status) field is removed from both input and response. Use the 4 sub-status fields.

**Response (JSON):**

```ts
{
  frame: {
    id: number;
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    screen_overview: string | null;
    created_at: string;
    updated_at: string;
  }
}
```

---

### 3. `get_frame`

Get full details for a Screen by `screenId`. Returns metadata: name, 4 sub-status (design/spec/dev/review), screen_overview, figma_node_id, revision, timestamps.

**Parameters:**

| Name       | Type   | Required | Description            |
| ---------- | ------ | -------- | ---------------------- |
| `screenId` | string | ✓        | Screen ID of the frame |

**Response (JSON):**

```ts
{
  frame: {
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    screen_overview: string | null;
    revision: string | null;       // commit_hash
    created_at: string;
    updated_at: string;
  }
}
```

> **Breaking change:** The deprecated `status` (frame_status) field is removed from the response — use the 4 sub-status fields instead.

---

### 4. `update_frame`

Update a Frame's mutable metadata. Patch semantics: only fields explicitly provided are updated; omitted fields are unchanged. Pass `screenOverview: ""` to clear (set null).

**Parameters:**

| Name             | Type   | Required | Description                                                                                                                                                          |
| ---------------- | ------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `screenId`       | string | ✓        | Screen ID                                                                                                                                                            |
| `name`           | string | ✗        | New frame name (non-empty)                                                                                                                                           |
| `screenOverview` | string | ✗        | New overview/description. Pass `""` to clear (set null).                                                                                                             |
| `figmaNodeId`    | string | ✗        | Figma node ID this Screen links to. Accepts canonical / hyphenated / URL forms (see `create_frame`). Pass `""` to unlink (set null).                                 |
| `designStatus`   | enum   | ✗        | `none` \| `in_progress` \| `done`                                                                                                                                    |
| `specStatus`     | enum   | ✗        | `none` \| `in_progress` \| `done`                                                                                                                                    |
| `devStatus`      | enum   | ✗        | `none` \| `developing` \| `done` ⚠                                                                                                                                   |
| `reviewStatus`   | enum   | ✗        | `none` \| `in_progress` \| `done`                                                                                                                                    |

**Behavior:**

- Must provide at least one updatable field besides `screenId`; otherwise returns `"No fields to update"` error.
- If `screenId` does not match any frame → returns `"Frame not found for screenId: ..."`.
- Tool does **not** expose the legacy `status` field — sub-status only.

**Response (JSON):**

```ts
{
  frame: {
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    screen_overview: string | null;
    created_at: string;
    updated_at: string;
  }
}
```

**Examples:**

- Rename only: `{ screenId, name: "New name" }`
- Clear overview: `{ screenId, screenOverview: "" }`
- Mark dev done: `{ screenId, devStatus: "done" }`
- Mixed: `{ screenId, name: "X", screenOverview: "Y", specStatus: "done" }`

---

### 5. `list_frames`

List all Screens in a file. By default returns ALL Screens (archived frames excluded); optionally filter by any of the 4 sub-status fields (design/spec/dev/review). Multiple filters are AND-combined.

**Parameters:**

| Name              | Type    | Required | Default | Description                                                                |
| ----------------- | ------- | -------- | ------- | -------------------------------------------------------------------------- |
| `fileKey`         | string  | ✓        | —       | Figma file key                                                             |
| `designStatus`    | enum    | ✗        | —       | `none` \| `in_progress` \| `done`                                          |
| `specStatus`      | enum    | ✗        | —       | `none` \| `in_progress` \| `done`                                          |
| `devStatus`       | enum    | ✗        | —       | `none` \| `developing` \| `done` ⚠                                         |
| `reviewStatus`    | enum    | ✗        | —       | `none` \| `in_progress` \| `done`                                          |
| `includeOverview` | boolean | ✗        | `false` | When `true`, include `screen_overview` per frame (may be large)            |

> **Breaking change:** Legacy `status` (frame_status) filter is removed from both input and response. The earlier docs also listed `draft`/`completed` — that was a bug; those values were never valid. Use the 4 sub-status filters.

**Response (JSON):** frames array:

```ts
{
  frames: Array<{
    screen_id: string;
    figma_node_id: string | null;
    name: string;
    design_status: 'none' | 'in_progress' | 'done';
    spec_status: 'none' | 'in_progress' | 'done';
    dev_status: 'none' | 'developing' | 'done';
    review_status: 'none' | 'in_progress' | 'done';
    revision: string | null;
    tags: string[];
    screen_overview?: string | null;          // only when includeOverview=true
    created_at: string;
    updated_at: string;
  }>;
}
```

---

### 6. `list_frame_sets`

List all ScreenSets (Screen groups) in a file. Useful for browsing the file's organizational structure before drilling into individual Screens.

**Parameters:**

| Name      | Type   | Required | Description    |
| --------- | ------ | -------- | -------------- |
| `fileKey` | string | ✓        | Figma file key |

**Response (JSON):** `{ frame_sets: [...] }`.

---

### 7. `get_frame_set`

Get details of a ScreenSet by `frameSetId`, including a list of all child Screens with full metadata.

**Parameters:**

| Name         | Type   | Required | Description  |
| ------------ | ------ | -------- | ------------ |
| `frameSetId` | number | ✓        | Frame set ID |

**Response (JSON):** frame_set object with embedded frames.

---

### 8. `upload_specs`

Batch upload or update specs (design items) for a Screen. Accepts a JSON array (typically converted from CSV) and upserts to the database. Manages two distinct status types: **spec completion** (`spec_progress`: `draft`/`completed`) and **lifecycle** (`active_status`: `active`/`archived`/`deleted`). Both fields are optional — if omitted, `spec_progress` is auto-detected from content. Items with `active_status=archived` are rejected if they contain content changes.

**Parameters:**

| Name        | Type     | Required  | Description                   |
| ----------- | -------- | --------- | ----------------------------- |
| `screen_id` | string   | ✓         | Screen ID of the target frame |
| `specs`     | object[] | ✓ (min 1) | Array of spec items           |

**Spec item shape (22 fields):**

```
no, design_item_name, name, nameTrans, node_link_id?,
type, otherType, buttonType, dataType, required, format,
minLength, maxLength, defaultValue, validationNote,
action, linkedFrameId, navigationNote,
tableName, columnName, databaseNote, description,
id?, section_link_id, extLink, is_reviewed
```

**Response (JSON):**

```ts
{
  status: 'success' | 'failed' | 'skipped';
  target_frame: {...};
  uploaded_count: number;
  skipped_count: number;
  invalid_count: number;
  saved_items: [...];
  invalid_specs?: [...];
}
```

**Behavior:** `spec_progress` (spec completion: `draft`/`completed`) is auto-detected from content if not provided; `active_status` (lifecycle: `active`/`archived`/`deleted`) defaults to `active`. Items with `active_status=archived` are rejected if content changes are present. Revision tracking is always applied.

---

### 9. `download_specs`

Export specs (design items) of a Screen as CSV or JSON (matches `upload_specs` input schema). Data is returned exactly as stored — no transformation. Useful for round-trip edit-and-reupload workflows. The `spec_progress` column (spec completion: `draft`/`completed`) is always included; the `active_status` column (lifecycle: `active`/`archived`/`deleted`) is only present when `include_deleted=true`.

**Parameters:**

| Name              | Type    | Required | Default | Description                                                                                                                |
| ----------------- | ------- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| `screen_id`       | string  | ✓        | —       | Screen ID                                                                                                                  |
| `format`          | enum    | ✗        | `csv`   | `csv` \| `json` \| `both`                                                                                                  |
| `include_deleted` | boolean | ✗        | `false` | When true, includes archived/deleted items and adds `active_status` column (`active`\|`archived`\|`deleted`) to the output |

**Response (JSON):**

```ts
{
  status: 'success' | 'empty';
  target_frame: {...};
  item_count: number;
  csv?: string;
  specs?: [...];
}
```

The CSV output can be saved directly to a file without modification.

---

### 10. `list_design_items`

List all design items (specs) of a Screen with type information enhanced from metadata.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):**

```ts
{
  design_items: Array<{
    id: string;
    no: number;
    type: string;
    name: string;
    specs: {...};
    status: string;
  }>;
}
```

---

### 11. `list_frame_spec_diffs`

Compare current specs of a Screen against the latest revision. Returns design items with change status (`new` / `deleted` / `delta` / `unchanged`). When `kind = delta`, includes details of changed fields.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):**

```ts
{
  designItems: Array<{
    node_id: string;
    no: number;
    name: string;
    status: string;
    type: string;
    specs: {...};  // display table
    diffs: {
      kind: 'new' | 'deleted' | 'delta' | 'unchanged';
      delta?: {...};  // changed field values, only when kind=delta
    };
  }>;
}
```

---

### 12. `get_related_design_items`

Get design items related to a specific design item (copies, master components, items in the same set). Use `limit` to control max results per category.

**Parameters:**

| Name           | Type   | Required | Default | Description            |
| -------------- | ------ | -------- | ------- | ---------------------- |
| `screenId`     | string | ✓        | —       | Screen ID              |
| `designItemId` | string | ✓        | —       | Source design item ID  |
| `limit`        | number | ✗        | `3`     | Max items per category |

**Response (JSON):** array of related items, deduplicated by `node_link_id`.

---

## 3.2 Test Cases

Tools for managing test cases attached to each Screen.

### 13. `upload_test_cases`

Batch upload or update test cases for a Screen. Accepts a JSON array (typically converted from CSV); stores as a **single record** per Screen containing the test case array. Automatically normalizes `test_area` values (`functional`/`function` → `FUNCTION`, etc.).

**Parameters:**

| Name         | Type     | Required  | Description     |
| ------------ | -------- | --------- | --------------- |
| `screen_id`  | string   | ✓         | Screen ID       |
| `test_cases` | object[] | ✓ (min 1) | Test case items |

**Test case item shape:**

- `ID` (required)
- Optional: `step, category, page_name, test_area, test_data, sub_category, sub_sub_category, pre_condition, expected_result, test_objective, specs, tc_type, priority, test_results, executed_date, tester, note`

**Behavior:** Normalizes `test_area` values (`functional`/`function` → `FUNCTION`, etc.)

**Response (JSON):**

```ts
{
  status: 'success';
  operation: 'created' | 'updated';
  target_frame: {...};
  test_case_count: number;
}
```

---

### 14. `download_test_cases`

Export test cases of a Screen as CSV (18 columns) or JSON (matches `upload_test_cases` input schema). Data is returned exactly as stored in the database.

**Parameters:**

| Name        | Type   | Required | Default | Description               |
| ----------- | ------ | -------- | ------- | ------------------------- |
| `screen_id` | string | ✓        | —       | Screen ID                 |
| `format`    | enum   | ✗        | `csv`   | `csv` \| `json` \| `both` |

**CSV columns (18):**
`Section, TC_ID, Page_Name, Category, Sub_Category, Sub_Sub_Category, Test_Objective, Precondition, Test_Data, Steps, Expected_Result, Specs, Priority, Testcase_Type, Test_Result, Executed_Date, Tester, Note`

**Response (JSON):**

```ts
{
  status: 'success' | 'empty';
  target_frame: {...};
  test_case_count: number;
  csv?: string;
  test_cases?: [...];
}
```

---

### 15. `get_frame_test_cases`

Get test cases of a Screen directly from Figma via the frame link. Returns empty if the Screen is not linked to Figma.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):** `{ test_cases: [...] }`. Empty if the frame has no Figma link.

---

## 3.3 Media

Tools for fetching images, media files, and rendering Figma nodes as images.

### 16. `get_frame_image`

Get a rendered image of a Screen. Output can be base64 data or URL; use `showDesignItems=true` to overlay numbered design item annotations onto the image for quick spec review.

**Parameters:**

| Name              | Type    | Required | Default | Description                              |
| ----------------- | ------- | -------- | ------- | ---------------------------------------- |
| `screenId`        | string  | ✓        | —       | Screen ID of the frame                   |
| `outputType`      | enum    | ✗        | `data`  | `data` (base64) or `url`                 |
| `showDesignItems` | boolean | ✗        | `false` | Overlay numbered design item annotations |

**Response:**

- If `outputType=data` → image (base64 PNG, auto-resized)
- If `outputType=url` → `Text` (image URL)

---

### 17. `list_media_items`

List all media nodes (those with `MM_MEDIA_*` prefix) in a Screen with metadata, filtered from the Screen's hierarchical nodes.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):** array of media nodes filtered from hierarchical metadata, or text fallback.

---

### 18. `list_media_nodes`

List all `MM_MEDIA_*` asset nodes with dimensions, parent context, sibling count, and `roleHint` (background/icon/small-icon/text-label/overlay/image) — inferred from size ratio vs parent. **Call before writing any `<img>` tag** to understand each asset's intended role.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):**

```ts
{
  screenId: string
  mediaNodeCount: number
  nodes: Array<{
    id: string
    name: string
    type: string
    width: number
    height: number
    aspectRatio: number
    parentId: string
    parentName: string
    parentType: string
    parentWidth: number
    parentHeight: number
    siblingCount: number
    roleHint: 'background' | 'icon' | 'small-icon' | 'text-label' | 'overlay' | 'image'
  }>
}
```

---

### 19. `get_media_files`

Get presigned download URLs for ALL media files (SVG/PNG/JPG) in a Screen. URLs are returned in batches (50 per batch), convenient for bulk download.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):** array of URLs (batched in groups of 50), or text fallback if no media.

---

### 20. `get_media_file`

Download a single media file (SVG/PNG/JPG) of a node directly from storage. Defaults to SVG; specify `convertType` to convert to raster (png/jpg/jpeg). SVG is returned at original size; raster formats are auto-resized.

**Parameters:**

| Name             | Type   | Required | Description                                                 |
| ---------------- | ------ | -------- | ----------------------------------------------------------- |
| `fileKey`        | string | ✓        | Figma file key                                              |
| `componentSetId` | string | ✗        | Component set node ID from `hierarchicalNodes`              |
| `nodeId`         | string | ✗        | Node ID from `hierarchicalNodes`                            |
| `convertType`    | enum   | ✗        | `png` \| `jpg` \| `jpeg` \| `svg`. If omitted, returns SVG. |

**Response (image):**

- SVG returned without resizing
- Raster formats auto-resized

---

### 21. `get_figma_image`

Render one or more Figma nodes as PNG/JPG images via the Figma REST API. Supports custom `scale` (0.01–4) and `outputType` (base64 or URL). **Note:** calls Figma API directly, so may hit rate-limits.

**Parameters:**

| Name         | Type     | Required | Default | Description                    |
| ------------ | -------- | -------- | ------- | ------------------------------ |
| `fileKey`    | string   | ✓        | —       | Figma file key                 |
| `nodeIds`    | string[] | ✓        | —       | Node IDs to render             |
| `scale`      | number   | ✗        | `1`     | Render scale (0.01–4)          |
| `format`     | enum     | ✗        | `png`   | `png` \| `jpg`                 |
| `outputType` | enum     | ✗        | `url`   | `data` (base64 array) \| `url` |

**Response:**

- `outputType=url` → JSON with image URLs
- `outputType=data` → response with image parts (base64)

---

### 22. `get_design_item_image`

Get a cropped image of a specific design item in a Screen. Image is automatically resized to max 2000px to reduce size.

**Parameters:**

| Name           | Type   | Required | Description                          |
| -------------- | ------ | -------- | ------------------------------------ |
| `screenId`     | string | ✓        | Screen ID containing the design item |
| `designItemId` | string | ✓        | Design Item ID                       |

**Response (image):** base64 PNG, auto-resized to max 2000px.

---

## 3.4 Figma Design

Tools for querying the node tree, styles, variables, and localization of a Figma file.

### 23. `get_frame_node_tree`

Get the full hierarchical node tree of a Screen. By default includes specs for each node; set `includeSpecs=false` to get a compact structure map without specs.

**Parameters:**

| Name           | Type    | Required | Default | Description                                     |
| -------------- | ------- | -------- | ------- | ----------------------------------------------- |
| `screenId`     | string  | ✓        | —       | Screen ID of the frame                          |
| `includeSpecs` | boolean | ✗        | `true`  | Set false for a lightweight, structure-only map |

**Response (JSON):** recursive tree:

```ts
{
  id: string;
  name: string;
  type: string;
  specs?: {...};
  children: Node[];
}
```

---

### 24. `get_overview`

Get a lightweight overview tree of a Screen — containing only names, types, and hierarchy (no styles). **Use first** to understand the overall structure before drilling into detail tools like `query_section` or `get_node`. Control depth via `maxDepth`.

**Parameters:**

| Name       | Type   | Required | Default | Description                |
| ---------- | ------ | -------- | ------- | -------------------------- |
| `screenId` | string | ✓        | —       | Screen ID                  |
| `maxDepth` | number | ✗        | `3`     | Max depth in overview tree |

**Response (JSON):** `OverviewNode` tree:

```ts
{
  id: string;
  name: string;
  type: string;
  text?: string;
  componentId?: string;
  children?: OverviewNode[];
  childCount?: number;
}
```

---

### 25. `query_section`

Get a subtree from a Screen by `nodeId` (exact) or `nodeName` (fuzzy match). Returns the node and its children with full styles. `nodeId` takes precedence when both are provided. Use `maxDepth` to control depth (0 = node only).

**Parameters:**

| Name       | Type   | Required | Default | Description                                         |
| ---------- | ------ | -------- | ------- | --------------------------------------------------- |
| `screenId` | string | ✓        | —       | Screen ID                                           |
| `nodeId`   | string | ✗        | —       | Exact node ID (takes precedence over `nodeName`)    |
| `nodeName` | string | ✗        | —       | Fuzzy match by name (used if `nodeId` not provided) |
| `maxDepth` | number | ✗        | `3`     | Max child depth (0 = node only)                     |

**Response (JSON):** pruned subtree with full node details and styles.

---

### 26. `query_component`

Search for components in a Screen by name using fuzzy matching, returning results sorted by relevance score. Use when you know the name but not the exact `nodeId`. Customizable via `includeStyles` and `limit`.

**Parameters:**

| Name            | Type    | Required | Default | Description                          |
| --------------- | ------- | -------- | ------- | ------------------------------------ |
| `screenId`      | string  | ✓        | —       | Screen ID                            |
| `name`          | string  | ✓        | —       | Search query (e.g. "Header", "Logo") |
| `includeStyles` | boolean | ✗        | `true`  | Include CSS styles in response       |
| `limit`         | number  | ✗        | `5`     | Max results                          |

**Response (JSON):**

```ts
{
  query: string;
  matchCount: number;
  results: Array<{
    ...nodeFields;
    _matchScore: number;
  }>;
}
```

---

### 27. `query_by_type`

Filter and return all nodes of a specific Figma type (e.g. `TEXT`, `INSTANCE`, `FRAME`, `RECTANGLE`, `GROUP`, `COMPONENT`, `VECTOR`). Useful for getting all text content, all component instances, etc. Styles excluded by default to keep response compact.

**Parameters:**

| Name            | Type    | Required | Default | Description                                                                                |
| --------------- | ------- | -------- | ------- | ------------------------------------------------------------------------------------------ |
| `screenId`      | string  | ✓        | —       | Screen ID                                                                                  |
| `itemType`      | string  | ✓        | —       | Figma type: `TEXT`, `INSTANCE`, `FRAME`, `RECTANGLE`, `GROUP`, `COMPONENT`, `VECTOR`, etc. |
| `includeStyles` | boolean | ✗        | `false` | Include styles (keeps response small by default)                                           |

**Response (JSON):** `{ itemType, count, results: [...] }`.

---

### 28. `get_node`

Get a single node by exact Figma node ID (e.g. `2167:9091`), with full styles, position, parent/child relationships, and metadata. When the exact ID is unknown, use `query_component` to search by name first.

**Parameters:**

| Name       | Type   | Required | Description                              |
| ---------- | ------ | -------- | ---------------------------------------- |
| `screenId` | string | ✓        | Screen ID                                |
| `nodeId`   | string | ✓        | Exact Figma node ID (e.g. `"2167:9091"`) |

**Response (JSON):** full node object with styles, position, parent/child relationships, and metadata.

---

### 29. `get_node_context`

Get a node with its parent, ALL siblings at the same level, plus per-sibling role analysis (`background` / `text` / `icon` / `overlay`). **Essential before rendering image nodes** as it helps understand the layering composition. Toggle sibling styles via `includeSiblingStyles`.

**Parameters:**

| Name                   | Type    | Required | Default | Description                     |
| ---------------------- | ------- | -------- | ------- | ------------------------------- |
| `screenId`             | string  | ✓        | —       | Screen ID                       |
| `nodeId`               | string  | ✓        | —       | Target node ID                  |
| `includeSiblingStyles` | boolean | ✗        | `true`  | Include CSS styles for siblings |

**Response (JSON):**

```ts
{
  target: {...},                              // full node
  parent: {                                   // or null
    id: string;
    itemName: string;
    itemType: string;
    styles: {...};
    childCount: number;
  } | null,
  siblings: Array<{...node, _isSelf: boolean}>,
  layerAnalysis: Array<{
    id: string;
    name: string;
    type: string;
    width: number;
    height: number;
    role: string;                             // background | text | icon | overlay
    isSelf: boolean;
  }>;
}
```

---

### 30. `list_file_variables`

List CSS / design variables of a Figma file, grouped by collection. Each collection contains a name and its variables.

**Parameters:**

| Name      | Type   | Required | Description    |
| --------- | ------ | -------- | -------------- |
| `fileKey` | string | ✓        | Figma file key |

**Response (JSON):**

```ts
{
  variableCollections: Array<{
    name: string;
    variables: [...];
  }>;
}
```

Or `Text` if no variables.

---

### 31. `list_frame_styles`

Get the full hierarchical CSS style tree of a Screen. Reflects the complete node structure with styling — useful for inspecting styles or generating code.

**Parameters:**

| Name       | Type   | Required | Description |
| ---------- | ------ | -------- | ----------- |
| `screenId` | string | ✓        | Screen ID   |

**Response (JSON):** recursive node-style tree, or text if metadata lacks node styles.

---

### 32. `list_file_localizations`

Get multilingual translations corresponding to source text strings (`sourceTexts`) in a Figma file. Useful for cross-checking or exporting localizations.

**Parameters:**

| Name          | Type     | Required | Description               |
| ------------- | -------- | -------- | ------------------------- |
| `fileKey`     | string   | ✓        | Figma file key            |
| `sourceTexts` | string[] | ✓        | Source texts to translate |

**Response (JSON):** `{ localizations: [...] }`.

---

## Identifier Glossary

| Identifier       | Type   | Description                                                  | Example       |
| ---------------- | ------ | ------------------------------------------------------------ | ------------- |
| `fileKey`        | string | Figma/MoMorph file unique ID                                 | `"abc123XYZ"` |
| `screenId`       | string | Unique frame (screen) ID in MoMorph                          | `"scr_xxx"`   |
| `frameSetId`     | number | Numeric frame-set ID                                         | `42`          |
| `nodeId`         | string | Figma node ID (`<frame>:<index>`)                            | `"2167:9091"` |
| `designItemId`   | string | MoMorph design item ID                                       | `"di_xxx"`    |
| `componentSetId` | string | Component set node ID (from `hierarchicalNodes`)             | `"2167:9000"` |
| `node_link_id`   | string | Stable cross-revision reference                              | `"link_xxx"`  |
| `commit_hash`    | string | Revision identifier returned as `revision` in some responses | `"abc123"`    |

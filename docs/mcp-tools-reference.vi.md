# MoMorph MCP Server — Tài liệu tham khảo Tools

Tài liệu tham khảo đầy đủ cho **31 tools** mà MoMorph MCP server cung cấp để tương tác với dữ liệu thiết kế, specs, test cases, media, và node tree trong MoMorph.

> **Thuật ngữ:** Tài liệu dùng **Screen (Frame)** và **ScreenSet (FrameSet)** làm thuật ngữ chính. "Frame"và "FrameSet" là tên gọi cũ.

---

## Mục lục

1. [Khái niệm chung](#khái-niệm-chung)
2. [Bảng tra cứu nhanh](#bảng-tra-cứu-nhanh)
3. Tham khảo Tools theo nhóm:
   - [3.1 Specs](#31-specs)
   - [3.2 Test Cases](#32-test-cases)
   - [3.3 Media](#33-media)
   - [3.4 Figma Design](#34-figma-design)
4. [Bảng thuật ngữ định danh](#bảng-thuật-ngữ-định-danh)

---

## Khái niệm chung

### Kiểu kết quả trả về

Tools trả về một trong các dạng kết quả sau:

| Dạng  | Trường hợp sử dụng                                      |
| ----- | ------------------------------------------------------- |
| JSON  | Dữ liệu có cấu trúc (đối tượng, mảng)                   |
| Text  | Văn bản thuần / thông báo fallback khi không có dữ liệu |
| Image | Dữ liệu ảnh dưới dạng base64 hoặc URL                   |
| Error | Kết quả lỗi kèm thông điệp                              |

### Xác thực

Yêu cầu một trong các header sau (xét theo thứ tự ưu tiên giảm dần):

| Header                    | Ưu tiên | Dùng cho                                                |
| ------------------------- | ------- | ------------------------------------------------------- |
| `x-momorph-authorization` | 1       | Token MoMorph (khuyến nghị)                             |
| `authorization`           | 2       | Bearer token chuẩn                                      |
| `x-github-token`          | 3       | GitHub token (khi cần truy cập GitHub-linked resources) |
| `x-figma-token`           | 4       | Figma token (khi gọi Figma API trực tiếp)               |

### Quy ước input phổ biến

- `fileKey` — Định danh file Figma/MoMorph (string, vd: `"abc123XYZ"`)
- `screenId` — Định danh duy nhất của Screen (Frame) trong MoMorph (string, vd: `"scr_xxx"`)
- `nodeId` — Figma node ID (string, vd: `"2167:9091"`)
- Status enum: `design`, `spec`, `review`, `done`, `dev`

**Lấy `fileKey` và `screenId` từ URL MoMorph:**

```
https://momorph.ai/files/{fileKey}/screens/{screenId}
```

Ví dụ: `https://momorph.ai/files/9ypp4enmFmdK/screens/i87tDx10` → `fileKey = "9ypp4enmFmdK"`, `screenId = "i87tDx10"`.

### Quy ước output

- Screen info trả về: `screen_id, name, status, revision (commit_hash), tags, created_at, updated_at`
- CSV export dùng UTF-8 kèm header (22 cột cho specs, 18 cột cho test cases)

---

## Bảng tra cứu nhanh

| #   | Tên Tool                                                   | Nhóm         | Mục đích sử dụng                                                                         |
| --- | ---------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------- |
| 1   | [`get_project_overview`](#1-get_project_overview)          | Specs        | Lấy mô tả tổng quan về dự án                                                             |
| 2   | [`create_frame`](#2-create_frame)                          | Specs        | Tạo mới một Screen trong MoMorph                                                         |
| 3   | [`get_frame`](#3-get_frame)                                | Specs        | Lấy thông tin chi tiết của một Screen                                                    |
| 4   | [`list_frames`](#4-list_frames)                            | Specs        | Liệt kê tất cả Screen (có thể lọc theo status)                                           |
| 5   | [`list_frame_sets`](#5-list_frame_sets)                    | Specs        | Liệt kê tất cả ScreenSet                                                                 |
| 6   | [`get_frame_set`](#6-get_frame_set)                        | Specs        | Lấy chi tiết một ScreenSet kèm các Screen con                                            |
| 7   | [`upload_specs`](#7-upload_specs)                          | Specs        | Upload / cập nhật specs cho Screen                                                       |
| 8   | [`download_specs`](#8-download_specs)                      | Specs        | Xuất specs của Screen ra CSV / JSON                                                      |
| 9   | [`list_design_items`](#9-list_design_items)                | Specs        | Liệt kê tất cả specs của Screen                                                          |
| 10  | [`list_frame_spec_diffs`](#10-list_frame_spec_diffs)       | Specs        | So sánh thay đổi của specs so với revision gần nhất                                      |
| 11  | [`get_related_design_items`](#11-get_related_design_items) | Specs        | Lấy các specs liên quan cho một Screen (nếu có)                                          |
| 12  | [`upload_test_cases`](#12-upload_test_cases)               | Test Cases   | Upload / cập nhật test cases cho Screen                                                  |
| 13  | [`download_test_cases`](#13-download_test_cases)           | Test Cases   | Xuất test cases ra CSV / JSON                                                            |
| 14  | [`get_frame_test_cases`](#14-get_frame_test_cases)         | Test Cases   | Lấy test cases của Screen                                                                |
| 15  | [`get_frame_image`](#15-get_frame_image)                   | Media        | Lấy ảnh preview của Screen hoặc ảnh có đánh số specs                                     |
| 16  | [`list_media_items`](#16-list_media_items)                 | Media        | Liệt kê các media nodes có trong Screen                                                  |
| 17  | [`list_media_nodes`](#17-list_media_nodes)                 | Media        | Liệt kê tất cả media nodes kèm gợi ý role (background/icon/overlay...)                   |
| 18  | [`get_media_files`](#18-get_media_files)                   | Media        | Lấy URL download cho toàn bộ media assets (SVG/PNG/JPG) trong Screen                     |
| 19  | [`get_media_file`](#19-get_media_file)                     | Media        | Tải trực tiếp file media asset (SVG/PNG/JPG) của một node từ storage                     |
| 20  | [`get_figma_image`](#20-get_figma_image)                   | Media        | Export một Figma node bất kỳ thành ảnh PNG/JPG (có thể bị dính Figma rate-limit)         |
| 21  | [`get_design_item_image`](#21-get_design_item_image)       | Media        | Lấy ảnh đã crop của một spec item (design item) cụ thể                                   |
| 22  | [`get_frame_node_tree`](#22-get_frame_node_tree)           | Figma Design | Lấy cây node phân cấp đầy đủ của Screen                                                  |
| 23  | [`get_overview`](#23-get_overview)                         | Figma Design | Lấy cây tổng quan gọn nhẹ (chỉ tên + type, không style) — dùng đầu tiên để định hình     |
| 24  | [`query_section`](#24-query_section)                       | Figma Design | Truy vấn subtree theo node ID hoặc fuzzy name                                            |
| 25  | [`query_component`](#25-query_component)                   | Figma Design | Tìm component theo tên (fuzzy match, xếp hạng theo độ liên quan)                         |
| 26  | [`query_by_type`](#26-query_by_type)                       | Figma Design | Lọc tất cả nodes theo type Figma (TEXT, INSTANCE, FRAME, ...)                            |
| 27  | [`get_node`](#27-get_node)                                 | Figma Design | Lấy chi tiết một node theo node ID chính xác                                             |
| 28  | [`get_node_context`](#28-get_node_context)                 | Figma Design | Lấy một node kèm parent, siblings, và phân tích role layers (cần trước khi render image) |
| 29  | [`list_file_variables`](#29-list_file_variables)           | Figma Design | Lấy danh sách CSS / design variables của file                                            |
| 30  | [`list_frame_styles`](#30-list_frame_styles)               | Figma Design | Lấy cây style CSS phân cấp của Screen                                                    |
| 31  | [`list_file_localizations`](#31-list_file_localizations)   | Figma Design | Lấy bản dịch đa ngôn ngữ cho các chuỗi text nguồn                                        |

---

## 3.1 Specs

Các tool quản lý Screen (Frame), ScreenSet (FrameSet), và specs design items trong MoMorph.

### 1. `get_project_overview`

Lấy đoạn mô tả tổng quan cấp project của một file Figma/MoMorph. Trả về text mô tả mục đích, phạm vi, hoặc context của project mà người tạo đã thiết lập.

**Tham số:**

| Tên       | Kiểu   | Bắt buộc | Mô tả          |
| --------- | ------ | -------- | -------------- |
| `fileKey` | string | ✓        | File key Figma |

**Response (text):** chuỗi `project_overview` (hoặc thông báo fallback).

---

### 2. `create_frame`

Tạo mới một Screen trong file MoMorph mà không cần liên kết với Figma. Hữu ích khi muốn khởi tạo Screen độc lập để bắt đầu nhập specs/test cases.

**Tham số:**

| Tên              | Kiểu   | Bắt buộc | Mặc định | Mô tả                                                          |
| ---------------- | ------ | -------- | -------- | -------------------------------------------------------------- |
| `fileKey`        | string | ✓        | —        | File key của file MoMorph                                      |
| `name`           | string | ✓        | —        | Tên Screen                                                     |
| `screenOverview` | string | ✗        | —        | Mô tả / tổng quan của screen                                   |
| `designStatus`   | enum   | ✗        | `none`   | Trạng thái giai đoạn design: `none` \| `in_progress` \| `done` |
| `specStatus`     | enum   | ✗        | `none`   | Trạng thái giai đoạn spec: `none` \| `in_progress` \| `done`   |
| `devStatus`      | enum   | ✗        | `none`   | Trạng thái giai đoạn dev: `none` \| `developing` \| `done`     |
| `reviewStatus`   | enum   | ✗        | `none`   | Trạng thái giai đoạn review: `none` \| `in_progress` \| `done` |

**Response (JSON):**

```ts
{
  frame: {
    id: number
    frame_link_id: string | null
    name: string
    status: string
    design_status: string
    spec_status: string
    dev_status: string
    review_status: string
    screen_overview: string | null
    created_at: string
    updated_at: string
  }
}
```

---

### 3. `get_frame`

Lấy thông tin chi tiết của một Screen theo `screenId`. Trả về metadata cơ bản: tên, status, revision (commit hash), tags, thời gian tạo/cập nhật.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

**Response (JSON):** Screen info gồm `screen_id, name, status, revision (commit_hash), created_at, updated_at`.

---

### 4. `list_frames`

Liệt kê tất cả Screen trong một file. Mặc định trả về TẤT CẢ; có thể lọc theo status (`design_status`, `spec_status`, `dev_status`, `draft`, `completed`). Mỗi Screen kèm `screen_id` làm định danh duy nhất.

**Tham số:**

| Tên       | Kiểu     | Bắt buộc | Mô tả                                                                                                        |
| --------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| `fileKey` | string   | ✓        | File key Figma                                                                                               |
| `status`  | string[] | ✗        | Tập con của `design_status`, `spec_status`, `dev_status`, `draft`, `completed`. Bỏ qua để lấy TẤT CẢ Screen. |

**Response (JSON):** mảng Screens:

```ts
{
  frames: Array<{
    screen_id: string
    name: string
    status: string
    revision: string | null
    tags: string[]
    created_at: string
    updated_at: string
  }>
}
```

---

### 5. `list_frame_sets`

Liệt kê tất cả ScreenSet (nhóm Screen) trong một file. Dùng để duyệt cấu trúc tổ chức của file trước khi đi sâu vào từng Screen.

**Tham số:**

| Tên       | Kiểu   | Bắt buộc | Mô tả          |
| --------- | ------ | -------- | -------------- |
| `fileKey` | string | ✓        | File key Figma |

**Response (JSON):** `{ frame_sets: [...] }`.

---

### 6. `get_frame_set`

Lấy chi tiết một ScreenSet theo `frameSetId`, kèm danh sách các Screen con bên trong với metadata đầy đủ.

**Tham số:**

| Tên          | Kiểu   | Bắt buộc | Mô tả            |
| ------------ | ------ | -------- | ---------------- |
| `frameSetId` | number | ✓        | ID của ScreenSet |

**Response (JSON):** object `frame_set` kèm các Screen con.

---

### 7. `upload_specs`

Upload hoặc cập nhật batch specs (design items) cho một Screen. Nhận đầu vào là mảng JSON (thường convert từ CSV), thực hiện upsert vào database. Hỗ trợ tự động phát hiện status (none/draft/completed) và ghi nhận revision.

**Tham số:**

| Tên         | Kiểu     | Bắt buộc  | Mô tả                     |
| ----------- | -------- | --------- | ------------------------- |
| `screen_id` | string   | ✓         | Screen ID của Screen đích |
| `specs`     | object[] | ✓ (min 1) | Mảng các spec items       |

**Cấu trúc spec item (26 trường):**

| Tên                | Kiểu                      | Bắt buộc | Mô tả                                                                                                                                                                                                   |
| ------------------ | ------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `no`               | string                    | ✓        | Số thứ tự spec (vd: `"1"`, `"1.1"`). CSV: `No`                                                                                                                                                          |
| `design_item_name` | string                    | ✓        | Tên hiển thị của design item. CSV: `itemName`                                                                                                                                                           |
| `name`             | string                    | ✓        | Tên tiếng Nhật (nameJP). CSV: `nameJP`                                                                                                                                                                  |
| `nameTrans`        | string                    | ✓        | Tên đã dịch (EN/VN). CSV: `nameTrans`                                                                                                                                                                   |
| `node_link_id`     | string                    | ✗        | Figma node ID. CSV: `itemId`. Bắt buộc khi liên kết với design Figma                                                                                                                                    |
| `type`             | enum \| null              | ✗        | UI component type: `button`, `checkbox`, `radio_button`, `dropdown`, `file_or_image`, `video`, `date_picker`, `pagination`, `popup_dialog`, `label`, `text_form`, `textarea`, `others`. CSV: `itemType` |
| `otherType`        | string \| null            | ✗        | Tên type tuỳ chỉnh khi `type="others"`. CSV: `itemSubtype`                                                                                                                                              |
| `buttonType`       | enum \| null              | ✗        | Subtype khi `type="button"`: `icon_text`, `toggle`, `text_link`, `others`. CSV: `buttonType`                                                                                                            |
| `dataType`         | enum \| null              | ✗        | Data type validation: `array`, `boolean`, `byte`, `character`, `string`, `date`, `integer`, `long`, `short`, `float`, `double`, `nothing`. CSV: `dataType`                                              |
| `required`         | boolean \| string \| null | ✗        | Field có bắt buộc không. Chấp nhận boolean hoặc string (`"true"`/`"false"`). CSV: `required`                                                                                                            |
| `format`           | string \| null            | ✗        | Mô tả format (max 255 ký tự). CSV: `format`                                                                                                                                                             |
| `minLength`        | number \| null            | ✗        | Độ dài tối thiểu (≥ 0). CSV: `minLength`                                                                                                                                                                |
| `maxLength`        | number \| null            | ✗        | Độ dài tối đa (≥ 0, phải > minLength). CSV: `maxLength`                                                                                                                                                 |
| `defaultValue`     | string \| null            | ✗        | Giá trị mặc định (max 255 ký tự). CSV: `defaultValue`                                                                                                                                                   |
| `validationNote`   | string \| null            | ✗        | Ghi chú validation (max 2000 ký tự). CSV: `validationNote`                                                                                                                                              |
| `action`           | enum \| null              | ✗        | Loại user action: `on_click`, `while_hovering`, `key_gamepad`, `after_delay`. CSV: `userAction`                                                                                                         |
| `linkedFrameId`    | string \| null            | ✗        | Frame ID đích cho navigation. CSV: `linkedFrameId`                                                                                                                                                      |
| `navigationNote`   | string \| null            | ✗        | Ghi chú navigation/transition (max 2000 ký tự). CSV: `transitionNote`                                                                                                                                   |
| `tableName`        | string \| null            | ✗        | Tên bảng DB (max 255 ký tự). CSV: `databaseTable`                                                                                                                                                       |
| `columnName`       | string \| null            | ✗        | Tên cột DB (max 255 ký tự). CSV: `databaseColumn`                                                                                                                                                       |
| `databaseNote`     | string \| null            | ✗        | Ghi chú DB (max 2000 ký tự). CSV: `databaseNote`                                                                                                                                                        |
| `description`      | string \| null            | ✗        | Mô tả (max 10000 ký tự). CSV: `description`                                                                                                                                                             |
| `id`               | number                    | ✗        | ID design item đã tồn tại (cho update). Bỏ qua khi tạo mới                                                                                                                                              |
| `section_link_id`  | string                    | ✗        | Section link ID. Thường tự động phân giải từ Screen                                                                                                                                                     |
| `extLink`          | string \| null            | ✗        | URL link ngoài                                                                                                                                                                                          |
| `is_reviewed`      | boolean \| null           | ✗        | Đã review hay chưa                                                                                                                                                                                      |

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

**Hành vi:** Tự động phát hiện status (none/draft/completed); ghi nhận revision.

---

### 8. `download_specs`

Xuất specs (design items) của một Screen ra CSV (22 cột) hoặc JSON (khớp schema input của `upload_specs`). Dữ liệu trả về nguyên trạng từ database — không transform. Hữu ích cho luồng round-trip edit → upload lại.

**Tham số:**

| Tên               | Kiểu    | Bắt buộc | Mặc định | Mô tả                                                                                               |
| ----------------- | ------- | -------- | -------- | --------------------------------------------------------------------------------------------------- |
| `screen_id`       | string  | ✓        | —        | Screen ID                                                                                           |
| `format`          | enum    | ✗        | `csv`    | `csv` \| `json` \| `both`                                                                           |
| `include_deleted` | boolean | ✗        | `false`  | Khi true, bao gồm items đã archive/delete và thêm trường `status` (`active`\|`archived`\|`deleted`) |

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

CSV output có thể lưu trực tiếp ra file mà không cần chỉnh sửa.

---

### 9. `list_design_items`

Liệt kê tất cả design items (specs) của một Screen kèm thông tin type được tăng cường từ metadata.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

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

### 10. `list_frame_spec_diffs`

So sánh specs hiện tại của một Screen với revision gần nhất. Trả về danh sách design items kèm trạng thái thay đổi (`new` / `deleted` / `delta` / `unchanged`). Khi `kind = delta`, kèm chi tiết các trường đã thay đổi.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

**Response (JSON):**

```ts
{
  designItems: Array<{
    node_id: string;
    no: number;
    name: string;
    status: string;
    type: string;
    specs: {...};  // bảng hiển thị
    diffs: {
      kind: 'new' | 'deleted' | 'delta' | 'unchanged';
      delta?: {...};  // giá trị các trường thay đổi, chỉ khi kind=delta
    };
  }>;
}
```

---

### 11. `get_related_design_items`

Lấy các design items liên quan tới một design item cụ thể (bản copy, master component, các item cùng set). Có thể giới hạn số kết quả mỗi nhóm qua `limit`.

**Tham số:**

| Tên            | Kiểu   | Bắt buộc | Mặc định | Mô tả                   |
| -------------- | ------ | -------- | -------- | ----------------------- |
| `screenId`     | string | ✓        | —        | Screen ID               |
| `designItemId` | string | ✓        | —        | Design item nguồn       |
| `limit`        | number | ✗        | `3`      | Số item tối đa mỗi nhóm |

**Response (JSON):** mảng items liên quan, đã dedup theo `node_link_id`.

---

## 3.2 Test Cases

Các tool quản lý test cases gắn với mỗi Screen.

### 12. `upload_test_cases`

Upload hoặc cập nhật batch test cases cho một Screen. Nhận đầu vào là mảng JSON (thường convert từ CSV); lưu thành **một record duy nhất** trên Screen chứa mảng test cases. Tự động normalize giá trị `test_area` (`functional`/`function` → `FUNCTION`, v.v.).

**Tham số:**

| Tên          | Kiểu     | Bắt buộc  | Mô tả               |
| ------------ | -------- | --------- | ------------------- |
| `screen_id`  | string   | ✓         | Screen ID           |
| `test_cases` | object[] | ✓ (min 1) | Các test case items |

**Cấu trúc test case item (18 trường):**

| Tên                | Kiểu   | Bắt buộc | Mô tả                                                                      |
| ------------------ | ------ | -------- | -------------------------------------------------------------------------- |
| `ID`               | string | ✓        | Test case ID (vd: `TC_IOS_HOME_ACC_001`)                                   |
| `step`             | string | ✗        | Các bước thực hiện test. CSV: `Steps`                                      |
| `category`         | string | ✗        | Test category (vd: `"Check access permission"`). CSV: `Category`           |
| `page_name`        | string | ✗        | Tên trang (vd: `"[iOS] Home"`). CSV: `Page_Name`                           |
| `test_area`        | string | ✗        | Section/test area: `ACCESSING`, `GUI`, `FUNCTION`, v.v. CSV: `Section`     |
| `test_data`        | string | ✗        | Dữ liệu test sử dụng. CSV: `Test_Data`                                     |
| `sub_category`     | string | ✗        | Sub-category (vd: `"App access"`). CSV: `Sub_Category`                     |
| `sub_sub_category` | string | ✗        | Sub-sub-category (vd: `"Authenticated user"`). CSV: `Sub_Sub_Category`     |
| `pre_condition`    | string | ✗        | Điều kiện tiên quyết. CSV: `Precondition`                                  |
| `expected_result`  | string | ✗        | Kết quả mong đợi. CSV: `Expected_Result`                                   |
| `test_objective`   | string | ✗        | Mô tả mục tiêu test. CSV: `Test_Objective`                                 |
| `specs`            | string | ✗        | Có specs hay không (`"Yes"`/`"No"`). CSV: `Specs`                          |
| `tc_type`          | string | ✗        | Loại test case (vd: `"Access control and security"`). CSV: `Testcase_Type` |
| `priority`         | string | ✗        | Mức ưu tiên: `High`, `Medium`, `Low`. CSV: `Priority`                      |
| `test_results`     | string | ✗        | Kết quả thực thi test. CSV: `Test_Result`                                  |
| `executed_date`    | string | ✗        | Ngày thực thi. CSV: `Executed_Date`                                        |
| `tester`           | string | ✗        | Tên người test. CSV: `Tester`                                              |
| `note`             | string | ✗        | Ghi chú thêm. CSV: `Note`                                                  |

**Hành vi:** Normalize giá trị `test_area` (`functional`/`function` → `FUNCTION`, v.v.)

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

### 13. `download_test_cases`

Xuất test cases của một Screen ra CSV (18 cột) hoặc JSON (khớp schema input của `upload_test_cases`). Dữ liệu trả về nguyên trạng từ database.

**Tham số:**

| Tên         | Kiểu   | Bắt buộc | Mặc định | Mô tả                     |
| ----------- | ------ | -------- | -------- | ------------------------- |
| `screen_id` | string | ✓        | —        | Screen ID                 |
| `format`    | enum   | ✗        | `csv`    | `csv` \| `json` \| `both` |

**Các cột CSV (18):**
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

### 14. `get_frame_test_cases`

Lấy test cases của một Screen trực tiếp từ Figma qua frame link. Trả về rỗng nếu Screen chưa liên kết với Figma.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

**Response (JSON):** `{ test_cases: [...] }`. Rỗng nếu Screen không có liên kết Figma.

---

## 3.3 Media

Các tool lấy ảnh, media file, render Figma node thành ảnh.

### 15. `get_frame_image`

Lấy ảnh render của một Screen. Có thể chọn output dạng base64 hoặc URL; tuỳ chọn `showDesignItems=true` để overlay số thứ tự của các design items lên ảnh, hỗ trợ review specs nhanh.

**Tham số:**

| Tên               | Kiểu    | Bắt buộc | Mặc định | Mô tả                                    |
| ----------------- | ------- | -------- | -------- | ---------------------------------------- |
| `screenId`        | string  | ✓        | —        | Screen ID                                |
| `outputType`      | enum    | ✗        | `data`   | `data` (base64) hoặc `url`               |
| `showDesignItems` | boolean | ✗        | `false`  | Overlay đánh số các design items lên ảnh |

**Response:**

- Nếu `outputType=data` → image (base64 PNG, tự động resize)
- Nếu `outputType=url` → text (URL ảnh)

---

### 16. `list_media_items`

Liệt kê tất cả media nodes (các node có prefix `MM_MEDIA_*`) trong một Screen kèm metadata, lọc từ hierarchical nodes của Screen.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

**Response (JSON):** mảng media nodes lọc từ metadata phân cấp, hoặc text fallback.

---

### 17. `list_media_nodes`

Liệt kê tất cả node asset `MM_MEDIA_*` kèm kích thước, thông tin parent, số siblings, và `roleHint` (background/icon/small-icon/text-label/overlay/image) — được suy đoán từ tỉ lệ kích thước so với parent. **Phải gọi trước khi viết bất kỳ tag `<img>` nào** để hiểu đúng role dự kiến của từng asset.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

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

### 18. `get_media_files`

Lấy danh sách presigned download URLs cho TẤT CẢ media files (SVG/PNG/JPG) trong một Screen. URLs được trả về theo batch (50 file/nhóm), tiện cho việc tải hàng loạt.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

**Response (JSON):** mảng URLs (chia batch 50 mỗi nhóm), hoặc text fallback nếu không có media.

---

### 19. `get_media_file`

Tải trực tiếp một file media (SVG/PNG/JPG) của một node từ storage. Mặc định trả SVG; có thể chỉ định `convertType` để convert sang raster (png/jpg/jpeg). SVG trả nguyên kích thước; raster sẽ được resize.

**Tham số:**

| Tên              | Kiểu   | Bắt buộc | Mô tả                                                  |
| ---------------- | ------ | -------- | ------------------------------------------------------ |
| `fileKey`        | string | ✓        | File key Figma                                         |
| `componentSetId` | string | ✗        | Component set node ID (lấy từ node tree của Screen)    |
| `nodeId`         | string | ✗        | Node ID (lấy từ node tree của Screen)                  |
| `convertType`    | enum   | ✗        | `png` \| `jpg` \| `jpeg` \| `svg`. Bỏ qua thì trả SVG. |

**Response (image):**

- SVG trả về không resize
- Raster format tự động resize

---

### 20. `get_figma_image`

Render một hoặc nhiều Figma node thành ảnh PNG/JPG qua Figma REST API. Hỗ trợ tuỳ chỉnh `scale` (0.01–4) và `outputType` (base64 hoặc URL). **Lưu ý:** gọi API Figma trực tiếp nên có thể bị rate-limit.

**Tham số:**

| Tên          | Kiểu     | Bắt buộc | Mặc định | Mô tả                         |
| ------------ | -------- | -------- | -------- | ----------------------------- |
| `fileKey`    | string   | ✓        | —        | File key Figma                |
| `nodeIds`    | string[] | ✓        | —        | Các node ID cần render        |
| `scale`      | number   | ✗        | `1`      | Tỉ lệ render (0.01–4)         |
| `format`     | enum     | ✗        | `png`    | `png` \| `jpg`                |
| `outputType` | enum     | ✗        | `url`    | `data` (mảng base64) \| `url` |

**Response:**

- `outputType=url` → JSON chứa các URL ảnh
- `outputType=data` → kết quả với các phần image (base64)

---

### 21. `get_design_item_image`

Lấy ảnh đã crop của một design item cụ thể trong Screen. Ảnh tự động được resize tối đa 2000px để giảm dung lượng.

**Tham số:**

| Tên            | Kiểu   | Bắt buộc | Mô tả                      |
| -------------- | ------ | -------- | -------------------------- |
| `screenId`     | string | ✓        | Screen ID chứa design item |
| `designItemId` | string | ✓        | Design Item ID             |

**Response (image):** base64 PNG, tự động resize tối đa 2000px.

---

## 3.4 Figma Design

Các tool truy vấn node tree, style, variables, và localization của file Figma.

### 22. `get_frame_node_tree`

Lấy toàn bộ cây node phân cấp của một Screen. Mặc định kèm specs cho từng node; có thể đặt `includeSpecs=false` để chỉ lấy map cấu trúc gọn, không chứa specs.

**Tham số:**

| Tên            | Kiểu    | Bắt buộc | Mặc định | Mô tả                                              |
| -------------- | ------- | -------- | -------- | -------------------------------------------------- |
| `screenId`     | string  | ✓        | —        | Screen ID                                          |
| `includeSpecs` | boolean | ✗        | `true`   | Đặt false để lấy map cấu trúc gọn không chứa specs |

**Response (JSON):** cây đệ quy:

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

### 23. `get_overview`

Lấy cây overview gọn nhẹ của Screen — chỉ chứa tên, type, và hierarchy (không có styles). **Dùng đầu tiên** để hiểu cấu trúc tổng thể trước khi đi sâu vào các tool chi tiết như `query_section` hoặc `get_node`. Tham số `maxDepth` kiểm soát độ sâu.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mặc định | Mô tả                          |
| ---------- | ------ | -------- | -------- | ------------------------------ |
| `screenId` | string | ✓        | —        | Screen ID                      |
| `maxDepth` | number | ✗        | `3`      | Độ sâu tối đa của cây overview |

**Response (JSON):** cây `OverviewNode`:

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

### 24. `query_section`

Lấy một subtree từ Screen theo `nodeId` (chính xác) hoặc `nodeName` (fuzzy match). Trả về node và các con với styles đầy đủ. `nodeId` được ưu tiên hơn `nodeName` khi cùng truyền. Dùng `maxDepth` để kiểm soát độ sâu (0 = chỉ riêng node).

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mặc định | Mô tả                                             |
| ---------- | ------ | -------- | -------- | ------------------------------------------------- |
| `screenId` | string | ✓        | —        | Screen ID                                         |
| `nodeId`   | string | ✗        | —        | Node ID chính xác (ưu tiên hơn `nodeName`)        |
| `nodeName` | string | ✗        | —        | Fuzzy match theo tên (dùng nếu không có `nodeId`) |
| `maxDepth` | number | ✗        | `3`      | Độ sâu con tối đa (0 = chỉ node)                  |

**Response (JSON):** subtree đã prune với chi tiết node và style đầy đủ.

---

### 25. `query_component`

Tìm components trong Screen theo tên bằng fuzzy matching, trả về kết quả đã sort theo điểm tương quan. Dùng khi biết tên nhưng không biết `nodeId` chính xác. Có thể tuỳ chỉnh `includeStyles` và `limit`.

**Tham số:**

| Tên             | Kiểu    | Bắt buộc | Mặc định | Mô tả                                 |
| --------------- | ------- | -------- | -------- | ------------------------------------- |
| `screenId`      | string  | ✓        | —        | Screen ID                             |
| `name`          | string  | ✓        | —        | Chuỗi tìm kiếm (vd: "Header", "Logo") |
| `includeStyles` | boolean | ✗        | `true`   | Bao gồm CSS styles trong response     |
| `limit`         | number  | ✗        | `5`      | Số kết quả tối đa                     |

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

### 26. `query_by_type`

Lọc và trả về tất cả nodes thuộc một type Figma cụ thể (vd: `TEXT`, `INSTANCE`, `FRAME`, `RECTANGLE`, `GROUP`, `COMPONENT`, `VECTOR`). Hữu ích để lấy toàn bộ text content, tất cả instance của component, v.v. Mặc định không kèm styles để giữ response nhỏ gọn.

**Tham số:**

| Tên             | Kiểu    | Bắt buộc | Mặc định | Mô tả                                                                                      |
| --------------- | ------- | -------- | -------- | ------------------------------------------------------------------------------------------ |
| `screenId`      | string  | ✓        | —        | Screen ID                                                                                  |
| `itemType`      | string  | ✓        | —        | Figma type: `TEXT`, `INSTANCE`, `FRAME`, `RECTANGLE`, `GROUP`, `COMPONENT`, `VECTOR`, v.v. |
| `includeStyles` | boolean | ✗        | `false`  | Có bao gồm style không (mặc định false để response nhỏ gọn)                                |

**Response (JSON):** `{ itemType, count, results: [...] }`.

---

### 27. `get_node`

Lấy chi tiết của một node duy nhất theo Figma node ID chính xác (vd: `2167:9091`), kèm full styles, position, quan hệ cha/con và metadata. Khi chưa biết ID chính xác, dùng `query_component` để tìm theo tên trước.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả                                       |
| ---------- | ------ | -------- | ------------------------------------------- |
| `screenId` | string | ✓        | Screen ID                                   |
| `nodeId`   | string | ✓        | Node ID Figma chính xác (vd: `"2167:9091"`) |

**Response (JSON):** object node đầy đủ với styles, vị trí, quan hệ cha/con, và metadata.

---

### 28. `get_node_context`

Lấy một node kèm parent, TẤT CẢ siblings cùng cấp, và phân tích role của từng sibling (`background` / `text` / `icon` / `overlay`). **Quan trọng trước khi render image nodes** vì giúp hiểu composition các layer xếp chồng. Có thể bật/tắt sibling styles qua `includeSiblingStyles`.

**Tham số:**

| Tên                    | Kiểu    | Bắt buộc | Mặc định | Mô tả                           |
| ---------------------- | ------- | -------- | -------- | ------------------------------- |
| `screenId`             | string  | ✓        | —        | Screen ID                       |
| `nodeId`               | string  | ✓        | —        | Node ID đích                    |
| `includeSiblingStyles` | boolean | ✗        | `true`   | Bao gồm CSS styles cho siblings |

**Response (JSON):**

```ts
{
  target: {...},                              // node đầy đủ
  parent: {                                   // hoặc null
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

### 29. `list_file_variables`

Lấy danh sách CSS / design variables của một file Figma, nhóm theo collection. Mỗi collection chứa tên và danh sách variables tương ứng.

**Tham số:**

| Tên       | Kiểu   | Bắt buộc | Mô tả          |
| --------- | ------ | -------- | -------------- |
| `fileKey` | string | ✓        | File key Figma |

**Response (JSON):**

```ts
{
  variableCollections: Array<{
    name: string;
    variables: [...];
  }>;
}
```

Hoặc text fallback nếu không có biến.

---

### 30. `list_frame_styles`

Lấy cây CSS style phân cấp đầy đủ của một Screen. Phản ánh toàn bộ structure node kèm styling, dùng để inspect style hoặc generate code.

**Tham số:**

| Tên        | Kiểu   | Bắt buộc | Mô tả     |
| ---------- | ------ | -------- | --------- |
| `screenId` | string | ✓        | Screen ID |

**Response (JSON):** cây node-style đệ quy, hoặc text nếu metadata không có node styles.

---

### 31. `list_file_localizations`

Lấy các bản dịch đa ngôn ngữ tương ứng với các chuỗi text nguồn (`sourceTexts`) trong một file Figma. Hữu ích khi cần đối chiếu hoặc export localizations.

**Tham số:**

| Tên           | Kiểu     | Bắt buộc | Mô tả                    |
| ------------- | -------- | -------- | ------------------------ |
| `fileKey`     | string   | ✓        | File key Figma           |
| `sourceTexts` | string[] | ✓        | Các chuỗi nguồn cần dịch |

**Response (JSON):** `{ localizations: [...] }`.

## Bảng thuật ngữ định danh

| Định danh        | Kiểu   | Mô tả                                                          | Ví dụ         |
| ---------------- | ------ | -------------------------------------------------------------- | ------------- |
| `fileKey`        | string | ID file Figma/MoMorph                                          | `"abc123XYZ"` |
| `screenId`       | string | ID duy nhất của Screen (Frame) trong MoMorph                   | `"scr_xxx"`   |
| `frameSetId`     | number | ID ScreenSet (FrameSet) kiểu số                                | `42`          |
| `nodeId`         | string | Figma node ID (`<frame>:<index>`)                              | `"2167:9091"` |
| `designItemId`   | string | ID design item MoMorph                                         | `"di_xxx"`    |
| `componentSetId` | string | Component set node ID (lấy từ node tree của Screen)            | `"2167:9000"` |
| `node_link_id`   | string | Tham chiếu ổn định xuyên revision                              | `"link_xxx"`  |
| `commit_hash`    | string | Định danh revision, một số response trả về dưới tên `revision` | `"abc123"`    |

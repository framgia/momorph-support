# MoMorph — Hướng Dẫn Sử Dụng


> 📩 **Liên hệ & đóng góp ý kiến hỗ trợ team MoMorph**
> - Slack: `#con_momorph-support_all`
> - Email: `momorph-admin@sun-asterisk.com`

---

## Mục Lục

<details>
<summary><strong>1. <a href="#1-tổng-quan">Tổng Quan</a></strong></summary>

- [1.1 Hệ sinh thái (7 sản phẩm)](#11-hệ-sinh-thái-7-sản-phẩm)
- [1.2 Sơ đồ luồng dữ liệu](#12-sơ-đồ-luồng-dữ-liệu)
- [1.3 Điều kiện tiền đề](#13-điều-kiện-tiền-đề)
  - [Tài khoản](#tài-khoản)
  - [Phần mềm / OS](#phần-mềm--os)

</details>

<details>
<summary><strong>2. <a href="#2-momorph-figma-plugin">MoMorph Figma Plugin</a></strong></summary>

- [2.1 Cài đặt](#21-cài-đặt)
- [2.2 Đăng nhập](#22-đăng-nhập)
  - [Pro user](#pro-user)
  - [Essential user](#essential-user)
- [2.3 Đồng bộ Design Data](#23-đồng-bộ-design-data)
- [2.4 Load thành phần giao diện vào màn Spec](#24-load-thành-phần-giao-diện-vào-màn-spec)

</details>

<details>
<summary><strong>3. <a href="#3-momorph-web-app">MoMorph Web App</a></strong></summary>

- [3.1 Truy cập](#31-truy-cập)
- [3.2 Đăng nhập](#32-đăng-nhập)
- [3.3 Core Features](#33-core-features)
- [3.4 Screen Status Workflow](#34-screen-status-workflow)

</details>

<details>
<summary><strong>4. <a href="#4-momorph-syncer-google-add-on">MoMorph Syncer (Google Add-on)</a></strong></summary>

- [4.1 Điều kiện sử dụng](#41-điều-kiện-sử-dụng)
- [4.2 Cài đặt / Truy cập](#42-cài-đặt--truy-cập)
- [4.3 Tính năng](#43-tính-năng)

</details>

<details>
<summary><strong>5. <a href="#5-momorph-cli">MoMorph CLI</a></strong></summary>

- [5.1 Cài đặt](#51-cài-đặt)
- [5.2 Xác thực & Khởi tạo](#52-xác-thực--khởi-tạo)
- [5.3 Command Reference](#53-command-reference)

</details>

<details>
<summary><strong>6. <a href="#6-mcp-server--ai-tools">MCP Server — AI Tools</a></strong></summary>

- [Điều kiện tiên quyết](#điều-kiện-tiên-quyết)
- [Cách 1 — Setup nhanh bằng CLI](#cách-1--setup-nhanh-bằng-cli)
- [Cách 2 — Cấu hình thủ công](#cách-2--cấu-hình-thủ-công)
- [Danh sách Tools](#danh-sách-tools)

</details>

<details>
<summary><strong>7. <a href="#7-ai-agent-integrations">AI Agent Integrations</a></strong></summary>

- [7.1 Tổng quan](#71-tổng-quan)
- [7.2 GitHub Copilot + VSCode Extension](#72-github-copilot--vscode-extension)
- [7.3 Claude Code](#73-claude-code)
- [7.4 Cursor / Windsurf / Gemini](#74-cursor--windsurf--gemini)
- [7.5 Claude Desktop Extension (.mcpb)](#75-claude-desktop-extension-mcpb)

</details>

<details>
<summary><strong>8. <a href="#8-lỗi-thường-gặp">Lỗi Thường Gặp</a></strong></summary>

- [8.1 CLI](#81-cli)
- [8.2 Web App](#82-web-app)
- [8.3 Figma Plugin](#83-figma-plugin)
- [8.4 VSCode Extension](#84-vscode-extension)
- [8.5 Syncer (Google Sheets Add-on)](#85-syncer-google-sheets-add-on)
- [8.6 MCP / Slash Commands](#86-mcp--slash-commands)

</details>

---

## 1. Tổng Quan

**MoMorph** là hệ sinh thái AI-Driven Development của Sun\* Asterisk, lấy Figma design / Specs làm điểm khởi đầu cho cả vòng đời phần mềm:

```
Figma Design & Specs → Test Cases → Code
```

### 1.1 Hệ sinh thái (7 sản phẩm)

| #   | Component                    | Purpose                                                                                     | Platform             |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------- | -------------------- |
| 1   | **Figma Plugin**             | Sync design data từ Figma vào MoMorph, quản lý dữ liệu thiết kế, tạo tài liệu specs, v.v... | Figma                |
| 2   | **Web App**                  | Quản lý project, lưu trữ screens/specs/test cases                                           | Trình duyệt          |
| 3   | **Syncer (Google Add-on)**   | Edit spec/testcase trên Google Sheets rồi sync 2 chiều với MoMorph                          | Google Sheets        |
| 4   | **CLI**                      | Khởi tạo project, cấu hình MCP, upload CSV specs/testcases                                  | Terminal             |
| 5   | **VSCode Extension**         | Hiển thị design/spec, tích hợp MCP server, Figma Tree và slash commands cho Copilot Chat    | VS Code              |
| 6   | **MCP Server**               | Cung cấp các AI tools cho agent đọc/ghi dữ liệu MoMorph & Figma                              | Tự động qua AI agent |
| 7   | **Claude Desktop Extension** | Bundle `.mcpb` — dùng MoMorph MCP từ Claude Desktop                                         | Claude Desktop       |

### 1.2 Sơ đồ luồng dữ liệu

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

### 1.3 Điều kiện tiền đề

#### Tài khoản

**Gói người dùng MoMorph (Essential vs Pro)** — quyết định phạm vi truy cập toàn bộ hệ sinh thái:

| Plan          | Phạm vi truy cập                                                                                                                                                                                                                   |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Essential** | **Chỉ Plugin** — Sử dụng được các chức năng: quản lý screens, nhập spec thủ công, export GitHub issue. Các sub-product khác (Web App, Syncer, CLI, MCP Server, VSCode Extension, Claude Desktop Extension) **không truy cập được** |
| **Pro**       | **Toàn bộ hệ sinh thái** — Plugin (full features) + Web App + Syncer + CLI + MCP Server + VSCode Extension + Claude Desktop Extension                                                                                              |

**Cách trở thành Pro user:**

- Người dùng có email thuộc domain công ty Sun\* mặc định là tài khoản Pro.
- Email khác: liên hệ team MoMorph để được cấp tài khoản Pro.

**Tài khoản nền tảng cần có cho từng product:**

| Product                  | Account | Requirement                                                                                                                                                        |
| ------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Figma Plugin             | Figma   | Tuân theo [điều kiện sử dụng plugin của Figma](https://help.figma.com/hc/en-us/articles/360039958474) (Viewer seat vẫn chạy được plugin trong file Drafts cá nhân) |
| Web App                  | Figma   | Mọi seat                                                                                                                                                           |
| Syncer (Google Add-on)   | Google  | Tài khoản **Google Workspace của công ty Sun\***                                                                                                |
| CLI                      | GitHub  | `momorph login`                                                                                                                                                    |
| MCP Server               | GitHub  | PAT scope `user`                                                                                                                                                   |
| VSCode Extension         | GitHub  | Cùng tài khoản CLI + **Copilot Business** (Free không đủ)                                                                                                          |
| Claude Desktop Extension | GitHub  | PAT scope `user`                                                                                                                                                   |

#### Phần mềm / OS

| Product                  | Requirement                                                                  |
| ------------------------ | ---------------------------------------------------------------------------- |
| Figma Plugin             | Figma Desktop hoặc figma.com                                                 |
| Web App                  | Chrome / Firefox / Safari / Edge mới nhất                                    |
| Syncer (Google Add-on)   | Google Sheets trên trình duyệt (Sun\* Workspace)                             |
| CLI                      | macOS / Linux / Windows (cài qua Homebrew / Chocolatey / scripts — xem §5.1) |
| VSCode Extension         | VS Code ≥ v1.105 · Windows: WSL                                              |
| Claude Desktop Extension | Claude Desktop hỗ trợ MCP v1.x · Node.js ≥ 18 · macOS/Windows/Linux          |

---

## 2. MoMorph Figma Plugin

Plugin chạy trong Figma (Desktop/Browser), gồm chức năng giống như bên Web App (§3) + đồng bộ design data (screens, items, styles, variables, media) vào MoMorph DB.

### 2.1 Cài đặt

1. Mở Figma → **Plugins → Manage plugins** → tìm "MoMorph"
2. Click **Install** → Run

### 2.2 Đăng nhập

Mở Plugin lần đầu (hoặc khi hết hiệu lực session) sẽ vào màn **Welcome** với 2 nút đăng nhập tương ứng 2 luồng — người dùng chọn 1 trong 2 tuỳ vào loại tài khoản:

#### Pro user

Click nút **"Đăng nhập với tài khoản Pro"**

1. Plugin mở tab browser → bấm **Authorize** trên Figma OAuth page để xác thực tài khoản.
2. Sau khi xác thực thành công, quay lại Plugin, chuyển sang bước **"Kết nối File Figma"** — dán URL Figma của file đang mở plugin → click **"Tiếp tục"**.
3. Nếu file có nhiều page, Plugin chuyển sang bước **"Chọn trang để tải"** — chọn các page muốn load dữ liệu screens từ Figma canvas → hoàn tất cài đặt.
4. Vào màn chính của Plugin.

> Tài khoản Figma phải là tài khoản Pro (xem §1.3). Nếu chưa, browser sẽ báo lỗi sau khi authorize.

#### Essential user

Click nút **"Bắt đầu miễn phí"**

1. Plugin **không** mở browser, **không** cần OAuth Figma.
2. Vào thẳng màn chính của Plugin với Essential features (browse screens, nhập spec thủ công, export GitHub issue).
3. Web App, CLI, MCP Server, VSCode Extension, Claude Desktop Extension **không** truy cập được — xem §1.3.

### 2.3 Đồng bộ Design Data

Web App, CLI, MCP, VSCode Extension chỉ thấy được dữ liệu thiết kế sau khi đã đồng bộ qua Plugin.

**Cách đồng bộ:**

1. **Mở Plugin tại file Figma cần làm việc** → Plugin tự đồng bộ danh sách screens ở background, không cần thao tác.
2. **Click vào 1 screen để vào màn chi tiết** → ảnh và thành phần giao diện của screen đó được đồng bộ.
3. **Click icon Refresh** (🔄) trên thanh **Preview toolbar** khi:
   - Vừa sửa design trên Figma, muốn cập nhật ngay sang MoMorph.
   - Web App hiển thị _"Ảnh thiết kế chưa được đồng bộ từ Figma Plugin"_.
   - Item bị thay đổi/đổi tên/thêm mới và Plugin chưa nhận ra.

### 2.4 Load thành phần giao diện vào màn Spec

Khi mở màn chi tiết (Spec) của một screen, Plugin **chỉ load những layer có prefix đúng convention** trong tên layer Figma. Layer không khớp prefix sẽ bị bỏ qua, không hiện trong danh sách thành phần.

**Quy tắc đặt tên layer:**

| Loại                           | Prefix              | Ví dụ                                                 | Hiển thị trong Spec                                   |
| ------------------------------ | ------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| **Item** (convention hiện tại) | `mms_<tên>`         | `mms_button`, `mms_submit_form`                       | ✅ Hiện thành 1 thành phần độc lập                    |
| **Item** (convention cũ)       | `<chữ/số>_<tên>`    | `A_button`, `A1_submit`, `1_label`, `1.1_email_field` | ✅ Hiện được, sẽ tự đổi sang `mms_*` khi add vào spec |
| **Media** (ảnh/icon)           | tên chứa `mm_media` | `mm_media`, `mm_media_logo`                           | ✅ Hiện ở mục Media                                   |
| **Layer thường**               | (không prefix)      | `Rectangle 1`, `Frame 23`, `Button`                   | ❌ Không hiện                                         |

**Lưu ý:**

- Prefix **không phân biệt hoa-thường** (`A_button` ≡ `a_button`, `MMS_action` ≡ `mms_action`).
- Tên sau prefix **không được chứa ký tự** `<`, `>`, `'`, `"` (tránh lỗi HTML/SVG).
- Convention `mms_*` là chuẩn hiện tại — khuyến khích đặt tên mới theo dạng này. Layer chứa prefix kiểu cũ (`1_button`, `A_button`) vẫn tương thích, Plugin sẽ tự rename sang `mms_*` khi link vào spec.
- Layer bị tắt visibility (`visible = false`) sẽ không được load. Ngoài ra, nếu parent frame có `opacity = 0`, các layer con cũng bị bỏ qua.

**Tự động tạo danh sách bằng AI Generate:**

Ngoài cách đặt prefix thủ công, trên màn Spec người dùng có thể dùng chức năng **AI Generate** để AI tự phân tích thiết kế Figma và tạo danh sách thành phần giao diện. Sau khi AI tạo xong, người dùng nên rà soát lại và chỉnh sửa/bổ sung item nếu cần.

**Workflow đề xuất cho Designer:**

1. Đặt tên layer trong Figma theo prefix `mms_*` ngay khi thiết kế (ví dụ `mms_login_button`, `mms_username_field`).
2. Mở Plugin → vào màn chi tiết → kiểm tra danh sách item ở Spec screen.
3. Item thiếu? Sửa tên layer trên Figma → click **Refresh** (🔄) trên Preview toolbar (xem §2.3) để load lại.

> Xem §8.3 nếu đã đặt prefix đúng mà item vẫn không hiện.

---

## 3. MoMorph Web App

Trung tâm quản lý projects/files/screens/specs. Dữ liệu thiết kế được đồng bộ từ Figma thông qua Plugin trước. Nếu người dùng không thực hiện đồng bộ từ Plugin, có thể gặp vấn đề truy cập dữ liệu trên Web và các product khác.

### 3.1 Truy cập

URL: **`https://momorph.ai`** · Hỗ trợ EN/JP/VI (đổi trong Settings).

### 3.2 Đăng nhập

1. Mở `momorph.ai`
2. Click **"Login with Figma"**
3. Authorize Figma


### 3.3 Core Features

Điều hướng qua sidebar/breadcrumb sau khi đăng nhập tại `momorph.ai`.

**Files & Screens**

| Feature          | Purpose                                                        |
| ---------------- | -------------------------------------------------------------- |
| File list        | Danh sách Figma files đã link                                  |
| Screen list      | Screens trong file (filter theo status, tag, page)             |
| Screen detail    | Preview ảnh + design items                                     |
| Item spec editor | Edit validation/navigation/DB mapping; có **AI Generate Spec** |
| Spec revisions   | Lịch sử version + rollback                                     |
| View all specs   | Bảng read-only xem tất cả specs trong screen                   |
| Screen tags      | Tag screen (functional, bug…)                                  |
| Global tags      | Quản lý tag toàn hệ thống                                      |

**Screen Sets** (gom screens thành nhóm)

| Feature          | Purpose                      |
| ---------------- | ---------------------------- |
| Screen Sets list | Danh sách screen sets        |
| Create / Edit    | Tạo / chỉnh sửa screen set   |
| Set detail       | Xem screens trong 1 set      |
| Screen in set    | Mở screen từ context của set |

**Settings cấp độ file**

| Feature                | Purpose                                  |
| ---------------------- | ---------------------------------------- |
| Project Overview       | Mô tả project (markdown)                 |
| GitHub                 | OAuth + link repo (cho VSCode Ext / CLI) |
| Google                 | OAuth Google (cho Syncer Google Sheets)  |
| Screen Translation     | Hub đa ngôn ngữ                          |
| Translation Languages  | Bật/tắt ngôn ngữ cho file                |
| Translation Dictionary | Bảng dịch en↔jp↔vi                     |

### 3.4 Screen Status Workflow

Mỗi screen có 4 status field độc lập (`design_status`, `spec_status`, `dev_status`, `review_status`), mỗi field 3 giá trị (`Not Started` / `In Progress` / `Done`). Trình tự khuyến nghị:

```
Design → Spec → Dev → Review → Done
```

Các status field được chỉnh trực tiếp trong Screen detail. VSCode Extension mặc định filter `spec_status = Done` nên Dev chỉ thấy các screen đã sẵn sàng để implement.

---

## 4. MoMorph Syncer (Google Add-on)

Add-on cho Google Sheets, đồng bộ 2 chiều giữa Sheets ↔ MoMorph. Phù hợp khi cần chỉnh spec / test case trên Sheets (collab nhiều người, comment, formula) rồi đẩy ngược lại MoMorph, hoặc ngược lại đẩy spec từ MoMorph sang Sheets cho team review.

### 4.1 Điều kiện sử dụng

- Tài khoản **Google Workspace của công ty Sun\***. Tài khoản Google cá nhân **không** truy cập được add-on.
- Gói **Pro** trên MoMorph (xem §1.3) — Essential user không sử dụng được Syncer.
- File Google Sheets đã được cài MoMorph Syncer add-on.

### 4.2 Cài đặt / Truy cập

- Mở 1 Google Sheets thuộc Sun\* Workspace → menu **Extensions → tìm kiếm và cài đặt MoMorph Syncer**. Lần đầu sẽ có popup yêu cầu authorize Google account để add-on truy cập file Sheets và gọi MoMorph backend.
- Nếu menu MoMorph Syncer không xuất hiện trong **Extensions**, liên hệ team MoMorph.

### 4.3 Tính năng

| Action                  | Mô tả                                                                  |
| ----------------------- | ---------------------------------------------------------------------- |
| **Sync Specifications** | Đồng bộ định nghĩa thành phần giao diện 2 chiều giữa Sheets ↔ MoMorph |
| **Sync Testcases**      | Đồng bộ test case 2 chiều giữa Sheets ↔ MoMorph                       |
| **Sync Image**          | Kéo ảnh design mới nhất từ Figma vào Sheets dạng in-cell native images |
| **Sync i18n**           | Đồng bộ nội dung đa ngôn ngữ (en / jp / vi)                            |

> Xem §8.5 nếu gặp lỗi authorization, sheet không sync được, hoặc menu thiếu action.

---

## 5. MoMorph CLI

Install/init project, upload CSV specs/testcases, config MCP cho AI agent. Lưu ý: CLI **không** hỗ trợ download — để tải spec/testcases về CSV, dùng AI agent qua MCP tools (xem §6).

### 5.1 Cài đặt

**macOS / Linux (Homebrew — khuyên dùng):**

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

**Kiểm tra / Cập nhật:**

```bash
momorph version
momorph update
```

### 5.2 Xác thực & Khởi tạo

**Bước 1 — Đăng nhập:**

```bash
momorph login          # CLI hiển thị code + link, Enter để mở browser
momorph whoami         # kiểm tra tài khoản
```

**Bước 2 — Init project:**

```bash
momorph init . --ai claude        # Claude Code
momorph init . --ai copilot       # GitHub Copilot
momorph init . --ai cursor        # Cursor
momorph init . --ai windsurf      # Windsurf
momorph init . --ai gemini        # Gemini
```

> **Quan trọng:** Dùng `.` để init trong root repo. `momorph init my-project` sẽ tạo subfolder.

`init` tự động: tải template mới nhất, tạo `.claude/` (hoặc `.github/`, `.cursor/`…), config MCP server, cài slash commands.

### 5.3 Command Reference

| Command                                         | Description                                 |
| ----------------------------------------------- | ------------------------------------------- |
| `momorph login`                                 | Auth GitHub OAuth Device Flow               |
| `momorph logout [--force]`                      | Log out, xoá credentials                    |
| `momorph whoami`                                | Tài khoản + subscription                    |
| `momorph init <dir> --ai <agent>`               | Init project + config agent                 |
| `momorph upload specs <file.csv>`               | Upload spec CSV                             |
| `momorph upload specs <file.csv> --dry-run`     | Preview, không upload                       |
| `momorph upload testcases <file.csv>`           | Upload test cases                           |
| `momorph upload testcases <file.csv> --dry-run` | Preview                                     |
| `momorph version`                               | Version CLI                                 |
| `momorph update [--check]`                      | Cập nhật CLI (`--check`: chỉ kiểm tra)      |
| `momorph completion <shell>`                    | Shell completion (bash/zsh/fish/powershell) |
| `momorph help [command]`                        | Trợ giúp                                    |

> **Cách chỉ định screen khi upload** (chọn 1):
>
> 1. **Tên file đúng convention** — `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv`, trong đó `{figmaFrameId}` là Figma node ID của frame (ví dụ `9276:19907-TOP_Channel.csv`). Đây là format mà các slash command như `/specs`, `/createtestcases`, `/updatetestcases` tự sinh ra.
> 2. **Flag `--screen-id <screenId>`** — alphanumeric MoMorph screenId, lấy từ URL Web (`/screens/{screenId}/...`); kèm `--file-key` nếu file ngoài convention path.

---

## 6. MCP Server — AI Tools

Host tại `https://mcp.momorph.ai/mcp`, cung cấp các tools cho AI agent đọc/ghi dữ liệu MoMorph & Figma. Người dùng **không gọi trực tiếp** — AI agent tự dùng (qua slash commands ở §7.2 hoặc qua prompt tự nhiên trong Claude Desktop §7.5). Mô tả chi tiết từng tool được trình bày ở tài liệu hướng dẫn chi tiết về cách sử dụng MCP Tools.

Một số tool quan trọng **không có slash command tương ứng** — chỉ AI gọi qua MCP:

- `upload_specs` / `download_specs` — upload/download CSV spec lên/từ MoMorph; hỗ trợ quản lý 2 loại status: **spec completion** (`spec_progress`: `draft`/`completed`) và **lifecycle** (`active_status`: `active`/`archived`/`deleted`). Download luôn trả về cột `spec_progress`; cột `active_status` chỉ có khi dùng `include_deleted=true`. Upload chấp nhận cả 2 trường — nếu không truyền, status tự tính từ nội dung. Item có `active_status=archived` sẽ bị từ chối nếu có thay đổi nội dung.
- `upload_test_cases` / `download_test_cases` — upload/download CSV test cases
- `list_frame_spec_diffs` — so sánh spec của screen với revision trước

**Cách kích hoạt thủ công các tool trên:**

- **Upload** (specs/testcases): dùng CLI (`momorph upload specs|testcases <file.csv>`) hoặc VSCode Explorer chuột phải file `.csv` trong `.momorph/` → "Upload to MoMorph" (xem §7.2)
- **Download** + **list_frame_spec_diffs**: chỉ qua AI agent — prompt tự nhiên trong Claude Desktop/Code/Cursor, hoặc slash command `/downloadspecs` trong VSCode menu

### Điều kiện tiên quyết

- Tài khoản GitHub đã liên kết MoMorph Web (cho CLI / MCP)
- Quyền truy cập repo (cho VSCode Extension / Plugin, nếu account có Admin)

### Cách 1 — Setup nhanh bằng CLI

(Claude Desktop dùng `.mcpb` — xem §7.5)

```bash
brew install momorph/tap/momorph-cli
momorph login
momorph init . --ai <agent_name>
```

### Cách 2 — Cấu hình thủ công

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

Tạo PAT scope `user` tại GitHub → Settings → Developer settings → Personal access tokens.

### Danh sách Tools

Để xem mô tả chi tiết, tham số, kiểu kết quả trả về và ví dụ sử dụng cho toàn bộ các tools của MCP server, vui lòng tham khảo tài liệu hướng dẫn chi tiết về cách sử dụng MCP Tools.

---

## 7. AI Agent Integrations

### 7.1 Tổng quan

| Agent                      | Init Command                   | Prompt Folder                         | Trigger                   | Best for            |
| -------------------------- | ------------------------------ | ------------------------------------- | ------------------------- | ------------------- |
| **Claude Code**            | `momorph init . --ai claude`   | `.claude/commands/`                   | Slash trong terminal      | CLI, headless       |
| **GitHub Copilot**         | `momorph init . --ai copilot`  | `.github/agents/`, `.github/prompts/` | Copilot Chat / VSCode Ext | IDE-centric         |
| **Cursor**                 | `momorph init . --ai cursor`   | `.cursor/commands/`                   | Cursor chat               | All-in-one IDE      |
| **Windsurf**               | `momorph init . --ai windsurf` | (theo Windsurf)                       | Windsurf chat             | Codeium             |
| **Gemini**                 | `momorph init . --ai gemini`   | (theo Gemini CLI)                     | Gemini chat               | Google stack        |
| **Claude Desktop** (.mcpb) | xem §7.5                       | n/a                                   | Prompt tự nhiên           | Casual / non-coding |

### 7.2 GitHub Copilot + VSCode Extension

**Sun\* MoMorph VSCode Extension** (`sun-asterisk.vscode-momorph`): Figma Tree, slash commands, đăng ký MCP server cho Copilot Chat.

#### Điều kiện

- Quyền **view hoặc edit** file Figma (không cần nếu chỉ generate unit test)
- **GitHub Copilot Business**
- VS Code ≥ v1.105
- Windows: WSL

#### Cài đặt

VSCode Extension được phân phối qua file `.vsix`. Liên hệ team MoMorph để nhận file mới nhất.

1. Mở file `vscode-momorph-x.y.z.vsix`
2. VSCode → tab **Extensions** → **`...`** → **Install from VSIX...**
3. Chọn file

#### Kết nối

Dùng cùng GitHub account với CLI. Đảm bảo đã `momorph login`.

1. Web → Settings → GitHub → connect repo
2. VSCode → mở repo → click icon **MoMorph** ở Activity Bar
3. Hiện list screen → setup OK

#### Sau khi cài

Khám phá trực tiếp trong VSCode:

- **Sidebar — Figma view** (`momorph.figma`): duyệt screens nhóm theo **With Design / No Design / Archived**, ngoài ra có **Screen Sets** và **Components**. Filter/Search theo **tag, page, status** (4 status field: Design / Spec / Dev / Review). Mặc định lọc `Spec Status = Done`
- **Sidebar — Contexts view** (`momorph.contexts`): hiển thị endpoints từ `.momorph/contexts/api-docs.yaml`, tự refresh khi file thay đổi
- **Chuột phải screen** (hỗ trợ multi-select):
  - **Open on Web** / **Copy Screen Information**
  - 15 slash commands sinh prompt sẵn cho AI agent — xem bảng dưới
  - Detect `.github/agents/momorph.*.agent.md` trong repo: có → mở Copilot Chat với prompt; không → copy prompt vào clipboard (paste vào Claude/Cursor)
- **Click screen** → web view với panel preview ảnh + panel specs (cùng items / styles / variables / test cases)
- **Command Palette** (`Cmd/Ctrl+Shift+P` → `MoMorph:`): Sign In, Search/Filter Screens, Open MoMorph Web, OpenAPI Server (Start/Stop/Restart)…
- **Settings** (`Cmd/Ctrl+,` → `momorph`):
  - `chat.language` & `chat.outputFileLanguage` (English / Vietnamese / Japanese)
  - `api.baseUrl`, `api.headers`, `mcpServers`, `github.remoteName`, `github.useEnterprise`
- **Copilot Chat**: `/` xem slash commands; `#` xem 7 Language Model Tools — `momorph_callMcpTool`, `momorph_compareScreenshots`, `momorph_downloadFigmaImage`, `momorph_getPreferenceInstructions`, `momorph_getUserPreferences`, `momorph_listApiEndpoints`, `momorph_getApiEndpoint`
- **Explorer**: chuột phải `.csv` trong `.momorph/specs/` hoặc `.momorph/testcases/` → **Upload to MoMorph**
- **MCP servers** cấu hình sẵn (trong `momorph.mcpServers`): `momorph`, `context7`, `testViewpoints`

#### Slash commands trong context menu

15 commands chia 2 nhóm. Cột **Agent file** đánh dấu commands có file prompt độc lập (`.claude/commands/momorph.*.agent.md` hoặc `.github/agents/momorph.*.agent.md`) — chạy được trong Claude Code/Cursor; commands không có agent file chỉ hoạt động qua VSCode menu (prompt sinh động).

**Flow** — quy trình spec → plan → implement:

| Command          | Agent file | Action                                                |
| ---------------- | :--------: | ----------------------------------------------------- |
| `/constitution`  |     ✅     | Init/update constitution (rules, stack)               |
| `/specify`       |     ✅     | Sinh `spec.md` + `design-style.md` + assets từ screen |
| `/reviewspecify` |     ❌     | Review/cải thiện spec.md & design-style.md            |
| `/plan`          |     ✅     | Plan từ spec + design-style + constitution            |
| `/reviewplan`    |     ❌     | Review/cải thiện plan                                 |
| `/tasks`         |     ✅     | Phân rã plan thành `tasks.md`                         |
| `/implement`     |     ✅     | Code theo `tasks.md`                                  |

**Context** — sinh dữ liệu từ Figma:

| Command            | Agent file | Action                                            |
| ------------------ | :--------: | ------------------------------------------------- |
| `/specs`           |     ✅     | CSV spec 22 cột từ screen                         |
| `/createtestcases` |     ✅     | Test cases (Accessing/GUI/Function), 1 CSV/screen |
| `/updatetestcases` |     ✅     | Update test cases khi spec đổi                    |
| `/apispec`         |   ✅ \*    | OpenAPI specs + backend test cases                |
| `/database`        |     ✅     | Schema SQL + ERD Mermaid                          |
| `/screenflow`      |     ✅     | Sinh `SCREENFLOW.md`                              |
| `/downloadspecs`   |     ❌     | Tải CSV spec từ MoMorph (qua MCP tool)            |
| `/convertspecs`    |     ❌     | Convert spec markdown → CSV local (không upload)  |

\* Agent file tên `momorph.apispecs.agent.md` (số nhiều), VSCode menu trigger với tên `apispec` (số ít).

#### Slash commands chỉ qua agent file (không có trong VSCode menu)

Cài qua `momorph init . --ai <agent>` (xem §7.3-§7.4), gõ trực tiếp trong terminal/chat:

| Command          | Action                                          |
| ---------------- | ----------------------------------------------- |
| `/commit`        | Commit theo Conventional Commits                |
| `/prdescription` | PR description theo template                    |
| `/ship`          | Commit + push + tạo PR trong 1 lệnh             |
| `/reviewcode`    | Review PR vs ticket spec, báo cáo theo severity |
| `/setupe2e`      | Init Playwright (1 lần/repo)                    |
| `/writee2e`      | `.spec.ts` từ test plan                         |
| `/reviewe2e`     | Review POM, locator, data, hiệu năng            |

> Khi extension không hiển thị data, click **`See Error`** trên notification mở output channel.

### 7.3 Claude Code

```bash
momorph init . --ai claude
```

Sinh `.claude/commands/momorph.*.agent.md`. Mở terminal Claude Code, gõ slash command. MCP config thêm vào `~/.claude.json`.

### 7.4 Cursor / Windsurf / Gemini

```bash
momorph init . --ai cursor       # .cursor/commands/
momorph init . --ai windsurf
momorph init . --ai gemini
```

File prompt theo convention từng agent. MCP config merge vào file config tương ứng.

### 7.5 Claude Desktop Extension (.mcpb)

Bundle `.mcpb` cài MoMorph MCP vào Claude Desktop bằng file — kết nối local Claude Desktop với `mcp.momorph.ai/mcp`.

#### Compatibility

- macOS / Windows / Linux · Node.js ≥ 18 · Claude Desktop hỗ trợ MCP v1.x

#### Cài đặt

1. Liên hệ team MoMorph để nhận file `momorph-mcp.mcpb` mới nhất.
2. Claude Desktop → **Settings** → **Extensions** → **Advanced Settings** → **Install Extension**
3. Chọn file → **Install** → nhập **GitHub PAT** (scope `user`) → **Save** → **Enable**

#### Test

Prompt: _"List all frames in this Figma file: {fileKey}"_ — Claude tự gọi `list_frames`. Bật Developer Mode để xem MCP debug log.

> **`.mcpb` vs MCP Cloud:** `.mcpb` cho user chỉ dùng Claude Desktop. Multi-IDE setup (VSCode + Claude Code + Cursor) → MCP Cloud qua `momorph init` (§5).

---

## 8. Lỗi Thường Gặp

### 8.1 CLI

**`momorph login` không complete** — kiểm tra firewall/VPN không chặn `github.com/login/device`. Có thể nhập code trực tiếp tại `https://github.com/login/device`.

### 8.2 Web App

**Login Figma fail / popup bị chặn:**

- Cho phép popup từ `momorph.ai`
- Thử browser private mode (extension đôi khi chặn OAuth callback)
- Đảm bảo Figma account còn active

**Không hiện file sau login** — nhập `fileKey` từ Figma URL khi popup. Nếu skip: `/` → "Add file" → paste fileKey.

### 8.3 Figma Plugin

**Item không được nhận diện** — kiểm tra layer name có prefix `mms_*` đúng convention (xem §2.4).

**Plugin trắng / spinner mãi:**

- Figma có truy cập `momorph.ai` không (network/VPN)?
- Logout Web → login lại → reload plugin (`Cmd/Ctrl+Shift+P` → `Reload`)

### 8.4 VSCode Extension

**Không kết nối MCP** — chưa login hoặc token hết hạn:

```bash
momorph login
momorph whoami
```

Sau đó `Ctrl+Shift+P → Developer: Reload Window`.

**Tree view không hiện screens:**

- Repo đã link Web (Settings → GitHub) chưa?
- Click **Refresh** trên Figma Tree
- Có lỗi → click **`See Error`** trên notification

**Context menu không trigger Copilot Chat** — Extension detect `.github/agents/momorph.*.agent.md` để biết project Copilot. Nếu thiếu (project Claude Code), prompt copy clipboard — paste thủ công vào Claude.

### 8.5 Syncer (Google Add-on)

**Menu MoMorph Syncer không xuất hiện trong Extensions** — add-on chưa được team vận hành deploy cho file Sheets này. Liên hệ team MoMorph.

**"Missing authentication token" khi gọi action** — Google session hết hạn. Re-login Google account (đảm bảo dùng tài khoản Google Workspace của công ty Sun\*), refresh tab Sheets, thử lại.

**"Cannot access spreadsheet"** — quyền share file chưa đủ. Kiểm tra:

- File Sheets có nằm trong Sun\* Workspace không (private file cá nhân không support).
- Account hiện tại có quyền **Editor** (Viewer không sync ngược về MoMorph được).

**"Invalid Figma URL"** — dán URL không đúng format. Dán lại link Figma từ thanh địa chỉ trình duyệt (kèm `node-id` nếu sync 1 frame cụ thể).

**"Failed to sync data"** — backend MoMorph hoặc network gián đoạn. Đợi vài phút thử lại; nếu lặp lại nhiều lần báo team support.

**Ảnh không xuất hiện trong cell sau khi sync** — convert in-cell image chạy nền (fire-and-forget). Đợi 10-30s rồi reload sheet. Nếu vẫn fail, click lại **Sync Image** trong menu.

### 8.6 MCP / Slash Commands

**"Frame not found" khi upload specs** — thiếu hoặc sai `--screen-id` (Figma node ID `32355:420279` ≠ MoMorph screenId). Sửa bằng 1 trong 2 cách (xem §5.3):

- Đặt tên file đúng convention `.momorph/{specs|testcases}/{fileKey}/{figmaFrameId}-{name}.csv` rồi upload không cần flag.
- Hoặc truyền flag `--screen-id`:
  ```bash
  momorph upload specs <file.csv> --screen-id <alphanumeric-screenId>
  ```

**Download specs "Frame not found"** (khi AI agent gọi MCP `download_specs`) — agent đang dùng Figma node ID thay vì MoMorph screenId. Lấy screenId từ URL Web (`/screens/{screenId}/...`) rồi prompt lại.

**Claude Desktop Extension không gọi tools:**

- Settings → Extensions → MoMorph status `Enabled`
- GitHub PAT còn valid (scope `user`)?
- Bật Developer Mode xem log
- Prompt rõ ràng có mention fileKey/screenId

**MCP timeout / chậm:**

- Kiểm tra network tới `mcp.momorph.ai`
- Slash command lớn (`/momorph.specs` cho screen nhiều item) có thể mất 30-60s — đợi thêm
- Fail nhiều lần → `momorph login` để refresh token

**`x-github-token` invalid / 401:**

- PAT đã revoke/hết hạn → tạo PAT mới (scope `user`), update vào MCP config (`~/.claude.json`…)
- Dùng `momorph init`: chạy `momorph login` → token tự merge vào config

---

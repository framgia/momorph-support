# Hướng dẫn chuyển từ V1 sang V2

![MoMorph 2.0 is Coming! 2026.11.04](images/v2/momorph-2-launch-banner.webp)

MoMorph mới (V2) ra mắt ngày 4/11/2026. MoMorph cũ (V1) ngừng cung cấp ngày 30/11/2026. Trang này nêu những điểm thay đổi so với MoMorph cũ, dữ liệu được chuyển, và việc người đang dùng MoMorph cũ phải làm.

## 1. Lịch chuyển đổi {#schedule}

```mermaid
flowchart LR
  A["Đến 1/11 (CN)<br>Lưu spec nháp<br>trên MoMorph cũ"] --> B["2/11 (T2) đến 3/11 (T3)<br>Không thao tác được<br>trên cả hai bản"] --> C["4/11 (T4)<br>Ra mắt MoMorph mới<br>MoMorph cũ chỉ xem"] --> D["30/11 (T2)<br>MoMorph cũ<br>ngừng cung cấp"]
```

| Ngày | Nội dung | Việc người dùng phải làm |
|---|---|---|
| Đến 1/11 (CN) | Ngày cuối làm việc trên MoMorph cũ | **Lưu** spec màn hình đang nháp trên MoMorph cũ |
| 2/11 (T2) đến 3/11 (T3) | Chuyển dữ liệu | **Không thao tác được trên cả hai bản** |
| 4/11 (T4) | Ra mắt MoMorph mới. MoMorph cũ chỉ xem | Đăng nhập MoMorph mới, kiểm tra dữ liệu |
| 30/11 (T2) | MoMorph cũ ngừng cung cấp | Xem lại thông tin cần thiết trước ngày này |

!!! warning "Lưu trước 1/11 (CN)"
    Spec màn hình nháp chưa lưu sẽ không được chuyển sang MoMorph mới.

## 2. Các sản phẩm của MoMorph mới {#products}

4 sản phẩm dùng chung dữ liệu của một project.

```mermaid
flowchart LR
  Web["MoMorph Web<br>quản lý, review màn hình và spec"] <--> Data[("Dữ liệu project<br>màn hình, spec, comment")]
  Plugin["MoMorph Figma Plugin<br>gắn design vào màn hình"] <--> Data
  MCP["MoMorph MCP<br>AI đọc và ghi dữ liệu"] <--> Data
  Skill["Skill cho AI agent<br>quy trình làm việc của AI"] -- "chạy qua MCP" --> MCP
```

Cách dùng từng sản phẩm: [Hướng dẫn sử dụng MoMorph V2](v2-user-guide.md)

## 3. Điểm thay đổi chính so với MoMorph cũ {#changes}

| Hạng mục | MoMorph cũ | MoMorph mới |
|---|---|---|
| Đăng nhập | Tài khoản Figma | Tài khoản Google hoặc GitHub. Web và Figma Plugin dùng cùng một tài khoản |
| Ai dùng được | Theo plan Essential hoặc Pro | Được admin mời, hoặc yêu cầu tham gia được duyệt |
| Tạo spec bằng AI | Nút generate trong sản phẩm | Bỏ nút generate. Nhờ AI như Claude Code |
| Thảo luận và review | Comment trên màn hình | Comment và stamp approve trên canvas |
| Tag màn hình | Lọc theo tag | Bỏ tag. Lọc theo status và page Figma |
| Export | Nhiều định dạng | Chỉ CSV |
| Web | `momorph.ai` | [app.momorph.ai](https://app.momorph.ai) |
| Figma Plugin | Plugin「MoMorph」 | Plugin「momoneo」 |

## 4. Tính năng mới {#new-features}

| Tính năng | Làm được gì |
|---|---|
| Đăng nhập bằng Google hoặc GitHub | Đăng nhập Web và Figma Plugin bằng cùng một tài khoản |
| Cùng sửa một lúc | Nhiều người sửa cùng một canvas cùng lúc |
| Spec, sơ đồ, màn hình trên một trang | Đặt spec, sơ đồ, ảnh chụp màn hình cạnh nhau để xem |
| Workflow approve | Cài các bước approve. Hệ thống ghi lại ai approve lúc nào |
| Liên kết GitHub | Hiện tài liệu trên GitHub lên canvas, xem khác biệt so với file gốc |
| Import CSV trực tiếp | Import file CSV thẳng vào bảng spec trên Plugin và Web |

![Kết quả Claude Code ghi lên canvas qua MoMorph MCP](images/v2/ai-result-on-canvas.png)

## 5. Dữ liệu được chuyển {#migrated-data}

Dữ liệu spec chính được chuyển sang MoMorph mới.

```mermaid
flowchart LR
  subgraph MoMorph cũ
    F1["File Figma<br>đã nhập spec"] --> S1["Màn hình<br>kể cả màn hình đã xoá trên Figma<br>nhưng đã nhập spec"]
    S1 --> I1["Spec màn hình,<br>tình trạng tiến độ"]
    U1["Thành viên"]
  end
  subgraph MoMorph mới
    P2["Project"] --> S2["Màn hình"] --> I2["Spec, status tiến độ"]
    M2["Thành viên"]
  end
  F1 --> P2
  S1 --> S2
  I1 --> I2
  U1 --> M2
```

| Được chuyển | Không được chuyển |
|---|---|
| File Figma đã nhập spec | File Figma chưa có spec |
| Màn hình, spec màn hình, tình trạng tiến độ, thành viên của file đó | Màn hình đã xoá hoặc archive |
| Màn hình đã xoá trên Figma nhưng đã nhập spec | Ảnh preview |

### Dữ liệu không được chuyển {#not-migrated}

| Nhóm | Dữ liệu | Cách xử lý |
|---|---|---|
| Ảnh preview | Ảnh preview của màn hình | Mở MoMorph Figma Plugin, ảnh được lưu lại |
| Tính năng chưa phát triển | Lịch sử spec, xuất spreadsheet, tạo issue GitHub | Dự kiến phát triển trong tháng 12 |
| Tính năng ngừng cung cấp | Dịch màn hình, comment trên màn hình, nhóm màn hình, test case của màn hình, prompt đã đăng ký, từ điển đã upload, lịch sử thao tác, tag màn hình | Không chuyển |

## 6. Việc người dùng phải làm {#user-steps}

```mermaid
flowchart LR
  A["1. Lưu spec nháp<br>trước 1/11"] --> B["2. Từ 4/11, đăng nhập<br>bằng email đã dùng ở bản cũ"] --> C["3. Kiểm tra<br>dữ liệu đã chuyển"] --> D["4. Cài plugin<br>momoneo"] --> E["5. Tạo API key,<br>kết nối AI"]
```

### 6.1 Đăng nhập bằng đúng email đã dùng ở MoMorph cũ {#login-same-email}

Đăng nhập bằng **cùng email** đã dùng ở MoMorph cũ thì dữ liệu đã chuyển mới hiện ra.

```mermaid
flowchart TD
  L["Đăng nhập MoMorph mới"] --> Q{"Email trùng với<br>email ở MoMorph cũ?"}
  Q -- "Trùng" --> OK["Dữ liệu đã chuyển hiện ra"]
  Q -- "Không trùng" --> NG["Không thấy dữ liệu đã chuyển"]
  NG --> R["Đăng xuất, đăng nhập lại<br>bằng email ở MoMorph cũ"]
```

Các bước: [1.1 Đăng nhập Web](v2-user-guide.md#login-web)

### 6.2 Kiểm tra dữ liệu đã chuyển {#check-data}

1. Mở [app.momorph.ai](https://app.momorph.ai).
2. Ở trang Home, mở project ứng với file Figma ở MoMorph cũ.
3. Kiểm tra danh sách màn hình, spec màn hình và status tiến độ.

![Trang Screens của MoMorph Web](images/v2/web-screens-and-spec-table.png)

### 6.3 Cài Figma Plugin「momoneo」 {#install-plugin}

Plugin của MoMorph cũ không kết nối được với MoMorph mới. Cài「momoneo」theo [1.7 Đăng nhập Figma Plugin](v2-user-guide.md#login-plugin). Khi mở plugin, ảnh preview được lưu lại.

### 6.4 Kết nối AI {#connect-ai}

Cấu hình MCP của MoMorph cũ không dùng được cho MoMorph mới.

1. Tạo API key quyền `write` theo [1.5 Tạo API key](v2-user-guide.md#api-key).
2. Kết nối Claude Desktop hoặc Claude Code theo [1.6 Kết nối AI qua MCP](v2-user-guide.md#connect-ai).

## 7. Tài liệu MoMorph cũ {#v1-docs}

Tài liệu MoMorph cũ được giữ ở mục **Lưu trữ (V1)**:

- [Hướng dẫn sử dụng V1](archived/general-user-guide.md)
- [Chi tiết công cụ MCP Server V1](archived/mcp-tools-reference.md)
- [Câu hỏi thường gặp V1](archived/faq.md)
- [Release Notes V1](archived/release-notes.md)

## 8. Liên hệ {#contact}

Gửi qua form trong kênh Slack `#con_momorph-support_all`.

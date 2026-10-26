# Hướng dẫn chuyển từ V1 sang V2

MoMorph mới (V2) ra mắt ngày 4/11/2026. MoMorph cũ (V1) ngừng cung cấp ngày 30/11/2026. Trang này nêu những điểm thay đổi so với MoMorph cũ, dữ liệu được chuyển, và việc người đang dùng MoMorph cũ phải làm. Cách dùng MoMorph mới xem tại [Hướng dẫn sử dụng MoMorph V2](v2-user-guide.md).

## 1. Lịch chuyển đổi {#schedule}

```mermaid
flowchart LR
  A["Đến 1/11 (CN)<br>Lưu đặc tả nháp<br>trên MoMorph cũ"] --> B["2/11 (T2) đến 3/11 (T3)<br>Không thao tác được<br>trên cả hai bản"] --> C["4/11 (T4)<br>Ra mắt MoMorph mới<br>MoMorph cũ chỉ xem"] --> D["30/11 (T2)<br>MoMorph cũ<br>ngừng cung cấp"]
```

| Ngày | Nội dung | Việc người dùng phải làm |
|---|---|---|
| Đến 1/11 (CN) | Ngày cuối làm việc trên MoMorph cũ | **Lưu** đặc tả màn hình đang nháp trên MoMorph cũ |
| 2/11 (T2) đến 3/11 (T3) | Chuyển dữ liệu | **Không thao tác được trên cả hai bản** |
| 4/11 (T4) | Ra mắt MoMorph mới. MoMorph cũ chỉ xem | Đăng nhập MoMorph mới, kiểm tra dữ liệu |
| 30/11 (T2) | MoMorph cũ ngừng cung cấp | Xem lại thông tin cần thiết trước ngày này |

!!! warning "Lưu trước 1/11 (CN)"
    Đặc tả màn hình đang nháp mà chưa lưu sẽ không được chuyển sang MoMorph mới.

## 2. Điểm thay đổi chính so với MoMorph cũ {#changes}

| Hạng mục | MoMorph cũ | MoMorph mới |
|---|---|---|
| Đăng nhập | Tài khoản Figma | Tài khoản Google hoặc GitHub |
| Ai dùng được | Theo gói Essential hoặc Pro | Được quản trị viên mời, hoặc yêu cầu tham gia được duyệt |
| Tạo đặc tả bằng AI | Nút tạo bằng AI trong sản phẩm | Bỏ nút này. Nhờ trợ lý AI như Claude Code |
| Thảo luận và rà soát | Bình luận trên màn hình | Bình luận và tem duyệt trên bảng làm việc |
| Nhãn màn hình | Lọc theo nhãn | Bỏ nhãn. Lọc theo trạng thái và trang Figma |
| Xuất file | Nhiều định dạng | Chỉ CSV |
| Web | `momorph.ai` | `app.momorph.ai` |

## 3. Dữ liệu được chuyển {#migrated-data}

Dữ liệu đặc tả chính được chuyển sang MoMorph mới.

```mermaid
flowchart LR
  subgraph cu["MoMorph cũ"]
    F1["File Figma<br>đã nhập đặc tả"] --> S1["Màn hình<br>kể cả màn hình đã xoá trên Figma<br>nhưng đã nhập đặc tả"]
    S1 --> I1["Đặc tả màn hình,<br>tình trạng tiến độ"]
    U1["Thành viên"]
  end
  subgraph moi["MoMorph mới"]
    P2["Dự án"] --> S2["Màn hình"] --> I2["Đặc tả, trạng thái tiến độ"]
    M2["Thành viên"]
  end
  F1 --> P2
  S1 --> S2
  I1 --> I2
  U1 --> M2
```

| Được chuyển | Không được chuyển |
|---|---|
| File Figma đã nhập đặc tả | File Figma chưa có đặc tả |
| Màn hình, đặc tả màn hình, tình trạng tiến độ, thành viên của file đó | Màn hình đã xoá hoặc đã lưu trữ |
| Màn hình đã xoá trên Figma nhưng đã nhập đặc tả | Ảnh xem trước |

### Dữ liệu không được chuyển {#not-migrated}

| Nhóm | Dữ liệu | Cách xử lý |
|---|---|---|
| Ảnh xem trước | Ảnh xem trước của màn hình | Ảnh được lưu lại khi mở MoMorph Figma Plugin |
| Tính năng chưa phát triển | Lịch sử đặc tả, xuất ra bảng tính, đăng ký GitHub Issue | Dự kiến phát triển trong tháng 12 |
| Tính năng ngừng cung cấp | Dịch màn hình, bình luận trên màn hình, nhóm màn hình, ca kiểm thử của màn hình, câu lệnh AI đã đăng ký, từ điển đã tải lên, lịch sử thao tác, nhãn màn hình | Không chuyển |

## 4. Việc người dùng phải làm {#user-steps}

```mermaid
flowchart LR
  A["1. Lưu đặc tả nháp<br>trước 1/11"] --> B["2. Từ 4/11, đăng nhập<br>bằng email đã dùng ở bản cũ"] --> C["3. Kiểm tra<br>dữ liệu đã chuyển"] --> D["4. Cài plugin momoneo,<br>kết nối lại trợ lý AI"]
```

### 4.1 Đăng nhập bằng đúng email đã dùng ở MoMorph cũ {#login-same-email}

Dữ liệu đã chuyển chỉ hiện ra khi đăng nhập bằng **đúng email** đã dùng ở MoMorph cũ.

```mermaid
flowchart TD
  L["Đăng nhập MoMorph mới"] --> Q{"Email trùng với<br>email ở MoMorph cũ?"}
  Q -- "Trùng" --> OK["Dữ liệu đã chuyển hiện ra"]
  Q -- "Không trùng" --> NG["Không thấy dữ liệu đã chuyển"]
  NG --> R["Đăng xuất, đăng nhập lại<br>bằng email ở MoMorph cũ"]
```

### 4.2 Kiểm tra dữ liệu đã chuyển {#check-data}

1. Ở **"Danh sách project"**, mở dự án ứng với file Figma ở MoMorph cũ.
2. Kiểm tra danh sách màn hình, đặc tả màn hình và trạng thái tiến độ.

### 4.3 Cài lại plugin và kết nối lại trợ lý AI {#reconnect}

Plugin và cấu hình MCP của MoMorph cũ không dùng được cho MoMorph mới. Cài đặt lại theo các bước sau:

- Plugin "momoneo": [1.7 Đăng nhập Figma Plugin](v2-user-guide.md#login-plugin)
- API key và kết nối trợ lý AI: [1.5 Tạo API key](v2-user-guide.md#api-key), [1.6 Kết nối trợ lý AI qua MCP](v2-user-guide.md#connect-ai)

## 5. Tài liệu MoMorph cũ {#v1-docs}

Tài liệu MoMorph cũ được giữ ở mục **Lưu trữ (V1)**:

- [Hướng dẫn sử dụng V1](archived/general-user-guide.md)
- [Chi tiết công cụ MCP Server V1](archived/mcp-tools-reference.md)
- [Câu hỏi thường gặp V1](archived/faq.md)
- [Ghi chú phát hành V1](archived/release-notes.md)

## 6. Liên hệ {#contact}

Gửi qua biểu mẫu trong kênh Slack `#con_momorph-support_all`.

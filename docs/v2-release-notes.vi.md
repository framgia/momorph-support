# MoMorph V2 — Ghi chú phát hành

Các cập nhật của MoMorph V2 (Web · Figma Plugin · MCP/API). Bản phát hành mới nhất nằm ở trên cùng.

<!-- Chỉ sửa file này ở sun-asterisk-internal/momorph docs/release-notes/; workflow sync-release-notes.yml copy sang đây, sửa ở momorph-support sẽ bị ghi đè. Mỗi lần release: thêm khối "## ngày {#ngày}" mới lên trên cùng (cả bản ja). -->

## 2026-11-05 {#2026-11-05}

!!! warning "Sau khi cập nhật, vui lòng"
    - Tải lại trang web đang mở, đóng file Figma rồi mở lại file đó, sau đó mới mở Figma Plugin. Chỉ mở lại plugin thì chưa đủ.
    - Khi kết nối plugin, nhập mã hiện trong plugin vào trình duyệt. Nếu web báo "Cần cập nhật plugin Figma", đóng file Figma rồi mở lại file đó, sau đó mở lại plugin. Xem [Đăng nhập Figma Plugin](v2-user-guide.md#login-plugin).
    - Dự án thuộc tổ chức khác: cài lại plugin bằng file manifest. Xem [Cài plugin bằng file manifest](v2-user-guide.md#install-manifest).

**🕘 Lịch sử version: làm mới giao diện**

- **Panel lịch sử mới (Web)** — gom theo khoảng thời gian, lọc theo page, người sửa và loại thao tác.
- **Tên version (Web)** — có thể đặt tên cho version và mở lại sau này.

**🔗 Kết nối GitHub: xem cập nhật của code ngay trên badge của node**

- **Badge trên node (Web)** — node đã liên kết với file trên GitHub có badge. Khi file đổi sau lần liên kết, badge cho bạn biết.
- **Xem nội dung cập nhật (Web)** — mở badge để xem các commit mới. Xem xong, bạn có thể chuyển mốc so sánh của node sang phiên bản mới nhất.

**🎨 Canvas**

- **Node iframe (Web)** — node nhúng trang web có kích thước lớn hơn, và zoom được trang bên trong.
- **Sticky note (Web)** — đặt sticky note xong là nhập được ngay, không còn phải xoá chữ "Note" có sẵn.

**🧩 Figma Plugin**

- **SVG preview** — upload được file tới 100MB. SVG không đổi thì không upload lại, nên đồng bộ nhanh hơn.
- **Tab Overview** — có giao diện giống tab Overview trên web.

**🤖 MCP và API**

- **Phần tử đang khoá** — phần tử đang khoá trên canvas không bị `repin_source`, `set_source_version`, `ingest_image`, `ingest_figma`, `delete_page` sửa hoặc xoá.
- **Section lồng nhau** — `parentId` nhận section nằm trong section, lồng bao nhiêu tầng cũng được.

**🔧 Thay đổi khác**

- Tạo project mới nhanh hơn.
- Đã sửa một số lỗi nhỏ trên canvas: kéo icon ở comment, toolbar của connector, dialog của filter.

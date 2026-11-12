# MoMorph V2 — Ghi chú phát hành

Các cập nhật của MoMorph V2 (Web · Figma Plugin · MCP/API). Bản phát hành mới nhất nằm ở trên cùng.

<!-- Chỉ sửa file này ở sun-asterisk-internal/momorph docs/release-notes/; workflow sync-release-notes.yml copy sang đây, sửa ở momorph-support sẽ bị ghi đè. Mỗi lần release: thêm khối "## ngày {#ngày}" mới lên trên cùng (cả bản ja). -->

## 2026-11-12 {#2026-11-12}

!!! warning "Sau khi cập nhật, vui lòng"
    - Tải lại trang web đang mở, đóng file Figma rồi mở lại file đó, sau đó mới mở Figma Plugin.
    - Dự án thuộc tổ chức khác: cài lại plugin bằng file manifest. Xem [Cài plugin bằng file manifest](v2-user-guide.md#install-manifest).
    - Nếu dùng MCP: cập nhật `@momorph/mcp` lên 7.0.0. `ingest_figma` không còn nhận `figmaFrame.id` hoặc `figmaFrame.figmaNodeId` dài đúng 10 ký tự chữ, số, `_`, `-` (ví dụ `login-page`) hoặc dạng `db:<số>`. Hãy đổi sang id có độ dài khác. Frame đã ingest bằng id dạng này sẽ không cập nhật được qua `ingest_figma` nữa.

**🔗 Kết nối Figma: chuyển file giữa các project cần được duyệt**

- **Gửi yêu cầu chuyển (Web)** — khi thêm file Figma đang liên kết với project khác, cần admin của project đang giữ file duyệt. Nếu bạn là admin của cả hai project thì file được chuyển ngay, không cần duyệt. Yêu cầu có thể kèm lý do. Bảng Figma hiện dòng "Chờ duyệt", và bạn huỷ được yêu cầu khi cần.
- **Duyệt hoặc từ chối (Web)** — admin của project đang giữ file nhận thông báo trên chuông, xem yêu cầu và lý do rồi duyệt hoặc từ chối. Admin gửi yêu cầu cũng nhận kết quả trên chuông.
- **Giới hạn số file** — mỗi project có tối đa 3 file Figma. Yêu cầu đang chờ duyệt cũng tính vào 3 file này.

**🕘 Lịch sử version**

- **Gộp dòng (Web)** — một thao tác lặp liền nhau hiện thành một dòng ×N. Các thao tác của AI cách nhau dưới 2 phút gộp thành một dòng.
- **Thêm loại thao tác (Web)** — dán, nhóm, bỏ nhóm và tự động sắp xếp (AI sắp xếp node) giờ hiện trong lịch sử. Các thao tác nhỏ như di chuyển hàng loạt không còn hiện.
- Thao tác của AI agent hiện tên người đã chạy agent. Đã sửa thêm tên filter Web embed, placeholder của dialog đổi tên và badge số mục đang lọc.

**🔗 Kết nối GitHub**

- **Badge cho người xem (Web)** — badge GitHub không còn hiện repo, đường dẫn file và phiên bản cho người xem (viewer). Thành viên và admin vẫn xem như trước.

**📄 Tab Spec**

- **Hiện ảnh nhanh hơn (Web)** — màn có SVG nặng hiện ảnh xem trước trước, rồi mới thay bằng SVG đầy đủ.
- **Giới hạn slide (Web)** — màn thêm slide ghi rõ tối đa 10 slide mỗi màn, và dòng thêm slide trong danh sách slide hiện số slide hiện có (n/10).

**🧩 Figma Plugin**

- **Ảnh frame tự cập nhật** — mỗi lần sync (mở màn, Reload), ảnh frame trên canvas cũng được cập nhật theo thiết kế mới nhất.
- Dòng đã bấm ở tab Unsaved không bị bỏ chọn khi tab tải xong.

**🤖 MCP và API**

- **`get_frame_image`** — trả link ảnh của slide trong màn (PNG hoặc SVG).
- **`upload_html_mock`** — upload một file HTML thành node mock trên canvas.
- **`upsert_node`** — báo `unchanged` khi nội dung gửi lên không đổi gì, và không ghi thêm vào lịch sử.
- **`upload_screen_spec`** — từ chối frame Figma chưa lưu thành màn.

**🔧 Thay đổi khác**

- Undo và redo khi sửa chữ nhiều lần đi từng bước một.
- Node chỉ bị khoá khi một thành viên khác đang sửa node đó, không còn khoá khi người đó chỉ chọn node.

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

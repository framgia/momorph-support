# MoMorph — Release Notes

Các cập nhật mới nhất của MoMorph (Plugin · Web · MCP Server).

## 2026-06-25

**✨ Mới & Cải tiến**

- **Nhắc cập nhật sau maintenance** — Khi kết thúc maintenance, hệ thống hiển thị thông báo nhắc reload (Figma file trên Plugin, hoặc trang trên Web) để nhận phiên bản mới nhất. Bạn có thể đóng và tiếp tục làm việc bình thường.
- **Gen spec AI hàng loạt ổn định hơn** — Generate spec cho nhiều item cùng lúc ổn định hơn (hết lỗi 502/503 với batch lớn); có thông báo cho biết quá trình gen có thể lâu hơn một chút.
- **Sync frame trên file lớn đáng tin cậy hơn** — Đồng bộ màn hình trên file Figma lớn (200+ frame) bền hơn nhờ chia batch và retry, tránh timeout và mất dữ liệu khi mạng chập chờn.

**🐛 Sửa lỗi**

- **Đánh số tự động theo cấp lớp** — Đánh số nay theo đúng thứ tự layer trên Figma (trên xuống dưới); kéo-thả đổi thứ tự cũng ổn định.
- **Preview Screen Detail (Web)** — Sửa ảnh preview bị nháy khi mở màn hình.
- **Điều hướng Back (Plugin)** — Sửa màn hình trắng khi quay lại danh sách frame set.
- **Trường Destination (Spec Form)** — Dropdown không còn liệt kê frame không tồn tại, và không cho lưu khi Destination (bắt buộc) đang rỗng.
- **Trạng thái item sau khi sync** — Item do AI tạo nay chuyển đúng sang **Done** sau khi sync lên MoMorph.
- **Item Type trên sheet** — Item dạng button do AI tạo nay hiển thị `Button` (thay vì `Button-Icon/Text`) khi sync lên spreadsheet.
- **Upload file dictionary** — Sửa lỗi khi upload file dictionary `.xlsx`.
- **Upload issue** — Sửa lỗi mất `No` và `Tên` của item sau khi upload issue lên GitHub.
- **Upload media** — Sửa lỗi upload media thất bại.

---

## Các bản phát hành trước

- [2026-06-19](release-archive.md#2026-06-19) — Nhập spec cho màn hình linh hoạt hơn (một trong `No` / `Item Name` / `UI Part`).
- [2026-06-11](release-archive.md#2026-06-11) — Thông báo trước maintenance, generate spec bằng AI trên Web, hỗ trợ Layer Group, nhập spec linh hoạt và cập nhật MCP Server.
- [2026-05-28](release-archive.md#2026-05-28) — Maintenance mode, sort & reorder 3-state cho Screen Spec, và sửa lỗi item missing UI Part cùng cancel AI gen spec ở trạng thái queued.
- [2026-05-21](release-archive.md#2026-05-21) — Tinh chỉnh Screen Detail, cancel AI gen spec theo batch, tìm theo Screen ID, tự nhớ Figma URL và nhiều sửa lỗi.
- [2026-05-07](release-archive.md#2026-05-07) — Nâng cấp Filter Modal, tăng tốc Screen Detail và cải thiện flow Screen Spec.
- [2026-04-23](release-archive.md#2026-04-23) — Screen Spec luôn ở chế độ chỉnh sửa, tải Spec dạng CSV và nhiều sửa lỗi sync/preview.
- [2026-04-09](release-archive.md#2026-04-09) — Ẩn/hiện nhãn spec trên preview, nâng cao chất lượng AI generate và đồng nhất URL sang `screen_id`.
- [2026-04-01](release-archive.md#2026-04-01) — AI tạo tổng quan màn hình & định nghĩa item, Active Item List, đánh số hàng loạt và Copy Spec.
- [2026-03-27](release-archive.md#2026-03-27) — Hỗ trợ Nested Sections, tự động migrate tiền tố layer cũ và sửa lỗi mất dữ liệu spec.
- [2026-03-20](release-archive.md#2026-03-20) — Chia danh sách màn hình thành 4 tab trạng thái, Archive màn hình và hỗ trợ Markdown cho spec.
- [2026-03-12](release-archive.md#2026-03-12) — Sửa lỗi đồng bộ dữ liệu Plugin ↔ Web và xử lý thông báo lỗi khi session hết hạn.
- [2026-02-13](release-archive.md#2026-02-13) — Nâng cấp quản lý Spec với All Specs Screen, màn Tổng quan Dự án và phục hồi dữ liệu spec.
- [2026-01-15](release-archive.md#2026-01-15) — Thêm Media Scan & Upload, đa ngôn ngữ cho MoMorph Syncer và tăng cường bảo mật URL ảnh.

# MoMorph — Release Notes

Các cập nhật mới nhất của MoMorph (Plugin · Web · MCP Server).

## 2026-07-09

**✨ Mới & Cải tiến**

- **Lọc Item List (Plugin & Web)** — Trên màn Screen Spec, bảng Item List (tab Active) nay có bộ lọc ở bốn cột: `No` và `Name` (chọn đơn), cùng `UI Part` và `Spec Status` (chọn nhiều, gồm `Generating` / `AI completed` / `Gen error` / `In Progress` / `Done`). Bộ lọc kết hợp giữa các cột và trong cùng một cột, sort theo `No` vẫn giữ filter, và có empty state khi không có item nào khớp. Kéo-thả đổi thứ tự bị tắt khi đang có filter.

**🐛 Sửa lỗi**

- **Số thứ tự trên ảnh preview khi sync sheet** — Sau khi đánh số lại item rồi sync MM → Google Sheet, ảnh preview nay cập nhật đúng theo số mới (trước đây ảnh vẫn giữ số cũ dù các trường khác đã đúng).
- **Hiệu ứng làm mờ layout (Plugin & Web)** — Các hiệu ứng mờ (Layer Blur, Background Blur, glassmorphism) nay hiển thị đúng như thiết kế Figma, thay vì hiện nền đặc trên overlay/panel.

---

## Các bản phát hành trước

- [2026-06-25](release-archive.md#2026-06-25) — Nhắc cập nhật sau maintenance, gen spec AI hàng loạt ổn định hơn, sync file lớn tin cậy hơn, cùng các sửa lỗi đánh số/sync/upload.
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

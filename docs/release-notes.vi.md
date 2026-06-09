# MoMorph — Release Notes

Các cập nhật mới nhất của MoMorph (Plugin · Web · MCP Server).

## 2026-05-21

**✨ Mới**

- **[Chỉ tài khoản Pro] Plugin tự nhớ Figma URL** — Sau lần nhập đầu tiên, plugin tự nhận diện file. Có thể reset bất cứ lúc nào trong Settings.
- **Tìm kiếm theo Screen ID** — Ô search ở Screen List và Screen Set hỗ trợ partial match theo Screen ID (case-insensitive) bên cạnh tìm theo tên màn hình.
- **Ẩn item archived (Web)** — Màn View All Spec mặc định chỉ hiển thị active items, ẩn toàn bộ item ở trạng thái archived.

**🔧 Cải thiện**

- **Tinh chỉnh hiển thị Screen Detail** — Giảm font size tiêu đề, tự mở rộng theo container, chỉ truncate khi thực sự hết chỗ. Nút Edit tag chuyển sang inline ngay sau tag cuối cùng, tránh khoảng trống thừa khi ít tag.
- **Cancel AI gen spec** — Bổ sung nút Cancel cho từng item và cả batch (huỷ all hoặc chỉ queued). Hiển thị toast tổng kết X thành công · Y lỗi sau khi batch xong.
- **Điều hướng khi chọn frame từ Figma** — Auto-scroll Screen List & tự động switch sang đúng status tab theo lựa chọn mượt hơn.
- **Highlight 2 chiều giữa item và preview** — Click item ở list highlight label trên preview, và ngược lại.

**🐛 Sửa lỗi**

- **Copy Specs** — Giữ đúng thứ tự item, trạng thái archived, và UI Part references. Khắc phục lỗi flicker UI sau khi copy.
- **Screen Set với frame đã xoá** — Sửa lỗi lag, status inconsistent, loading 6-7s, auto-link sai, screen biến mất khi xoá frame đã link trên Figma.
- **AI Test Case Generation** — Sửa lỗi Gen TC button enable khi user chưa save status change (gây timeout). Gen TC hoạt động ổn định với cả màn không có design.
- **GitHub integration** — Thông báo lỗi rõ ràng hơn khi connect repo không có admin privileges. Không còn tự tạo frame thừa [jp]/[en] khi tạo GitHub Issue có dịch.
- **Screen Spec** — Sửa lỗi modal unsaved changes hiển thị sai trên frame mới có label. Sửa lỗi mất layer link khi navigate sang detail mà chưa save. Sửa lỗi nhận diện sai item khi 2 item trùng label/UI Part name gây xoá nhầm.
- **Preview & badge** — Sửa lỗi image preview zoom sau translate, badge của UI Part type Text không hiển thị, cột UI Part bị blank sau khi Plugin refresh.
- **Screen List** — Tab highlight không còn stuck ở Design & Specs sau khi upload GitHub. Status frame hiển thị đúng "In Progress" khi có overview.
- **Item Spec (Web)** — Sửa pagination hiển thị sai trong Screen Set flow gây mất breadcrumb. Sửa lỗi frame mới trên Figma không sync sang Web.

---

## Các bản phát hành trước

- [2026-05-07](release-archive.md#2026-05-07) — Nâng cấp Filter Modal, tăng tốc Screen Detail và cải thiện flow Screen Spec.
- [2026-04-23](release-archive.md#2026-04-23) — Screen Spec luôn ở chế độ chỉnh sửa, tải Spec dạng CSV và nhiều sửa lỗi sync/preview.
- [2026-04-09](release-archive.md#2026-04-09) — Ẩn/hiện nhãn spec trên preview, nâng cao chất lượng AI generate và đồng nhất URL sang `screen_id`.
- [2026-04-01](release-archive.md#2026-04-01) — AI tạo tổng quan màn hình & định nghĩa item, Active Item List, đánh số hàng loạt và Copy Spec.
- [2026-03-27](release-archive.md#2026-03-27) — Hỗ trợ Nested Sections, tự động migrate tiền tố layer cũ và sửa lỗi mất dữ liệu spec.
- [2026-03-20](release-archive.md#2026-03-20) — Chia danh sách màn hình thành 4 tab trạng thái, Archive màn hình và hỗ trợ Markdown cho spec.
- [2026-03-12](release-archive.md#2026-03-12) — Sửa lỗi đồng bộ dữ liệu Plugin ↔ Web và xử lý thông báo lỗi khi session hết hạn.
- [2026-02-13](release-archive.md#2026-02-13) — Nâng cấp quản lý Spec với All Specs Screen, màn Tổng quan Dự án và phục hồi dữ liệu spec.
- [2026-01-15](release-archive.md#2026-01-15) — Thêm Media Scan & Upload, đa ngôn ngữ cho MoMorph Syncer và tăng cường bảo mật URL ảnh.

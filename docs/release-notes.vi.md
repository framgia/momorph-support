# MoMorph — Release Notes

Các cập nhật mới nhất của MoMorph (Plugin · Web · MCP Server).

## 2026-06-11

**✨ Mới & Cải tiến**

- **Thông báo trước maintenance** — Plugin & Web hiển thị modal báo trước thời điểm bảo trì (theo timezone của bạn) khi có lịch maintenance.
- **Generate spec bằng AI trên Web** — Đã có trong action menu của cả Screen Spec và View All Specs, đồng nhất với Plugin.
- **Layer Group trên Figma** — Layer có type là Group nay có thể link, chỉnh sửa và quản lý như một design item thường.
- **Nhập spec linh hoạt** — Bỏ ràng buộc bắt buộc cho các field (chỉ còn tên hoặc No. là bắt buộc) để nhập spec tự do hơn cho nhiều loại dự án.
- Đồng bộ label đa ngôn ngữ và bổ sung tooltip cho toolbar bảng item trên Plugin & Web.

**🐛 Sửa lỗi**

- AI gen spec ổn định hơn trên production — không còn bỏ qua field `Name` rỗng, không ghi đè `item type` ở chế độ do-not-overwrite, và sửa lỗi "items không tồn tại trong frame" sau edit/reload.
- Translate screen nay dịch cả các đoạn text dài trước đây bị bỏ sót.
- Sửa lỗi relink UI Part — gán lại layer giữa các item, và relink sau khi designer replace layer.
- Sửa lỗi khi relink screen sang design mới.
- Trạng thái hoàn thành của item nay được giữ đúng — chuyển về `Completed` sau khi Entry complete, và không còn tự revert từ `Completed` về `AI completed`.
- Sửa lỗi khác: nút Save/Cancel trên item AI-error, duplicate text khi nhập tiếng Nhật/Việt, thiếu total count trên Web Screen List, toast lỗi maintenance không còn hiển thị cho user, và Web nay chặn gen AI spec cho item bị missing (đồng nhất với Plugin).

**🔌 MCP Server**

- **Breaking — bỏ field `status` cũ** khỏi `create_frame`, `get_frame`, `list_frames`. Dùng 4 field `*_status` (`design_status`, `spec_status`, `dev_status`, `review_status`) thay thế, và cập nhật agent/workflow nào còn đọc/ghi `status`.
- **Tool mới `update_frame`** — cập nhật metadata màn hình (name, overview, các status, link Figma node) mà không cần tạo lại frame.
- **Hỗ trợ `figma_node_id`** — `create_frame`, `update_frame`, `get_frame`, `list_frames` nay nhận/trả `figma_node_id` ở dạng canonical (`12318:23788`), hyphen (`12318-23788`) hoặc full Figma URL.
- `list_frames` không còn trả về các màn hình đã archive.

---

## Các bản phát hành trước

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

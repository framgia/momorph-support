# MoMorph — Release Notes (Lưu trữ)

Các bản phát hành MoMorph trước đây. Xem bản mới nhất tại [Release Notes](release-notes.md).

## 2026-05-07

**✨ Tính năng mới**

- **Nâng cấp Filter Modal** — bổ sung tiêu chí lọc mới, giữ trạng thái filter khi quay lại từ màn detail.

**🔧 Cải tiến**

- Tăng tốc Screen Detail; giảm lag/đơ ở Screen Spec / Item Spec có nhiều items.
- Cải thiện flow chỉnh sửa, sync và revision của Screen Spec.
- Cải thiện logic xoá frame để hạn chế NoUI screens.

**🐛 Sửa lỗi**

- Sửa các lỗi liên quan Filter Modal, preview labels, tự sinh tên frame, Spec Upload (Web), MM Syncer, và MCP/CLI re-upload.

---

## 2026-04-23

**✨ Tính năng mới**

- **Screen Spec luôn ở chế độ chỉnh sửa** — Bỏ tách biệt View/Edit Mode; bảng mặc định luôn có thể chỉnh sửa, số thứ tự (No) do người dùng tự nhập.
- **Tải xuống Spec dạng CSV** — Hỗ trợ xuất và tải dữ liệu Screen Spec ra file CSV.

**🔧 Cải tiến**

- **Xoá/Undo nhiều frame cùng lúc** — Plugin hỗ trợ thao tác Delete và Undo cho nhiều Figma frame cùng một lúc.
- **Thứ tự design items** — Items trên Screen Spec được sắp xếp theo thứ tự layer tree mặc định của Figma.
- **AI sinh item spec** — Bổ sung danh sách `node_link_id` vào payload để AI tạo spec chính xác hơn.
- **Lưu từ khoá tìm kiếm** — Từ khoá tìm kiếm trên Screen List được giữ nguyên trên URL khi điều hướng.
- **GA4 Analytics** — Thêm `file_key` vào tất cả GA4 events để lọc theo từng Figma file.

**🐛 Sửa lỗi**

- **Sync & upload dữ liệu:** Sửa lỗi đồng bộ spec từ Google Sheet về MoMorph; item đã archive không còn bị đưa vào khi upload GitHub; màn "No Design" được chuyển đúng sang "In Development" sau khi upload từ Plugin; không còn tạo màn trùng tên trên Web.
- **Item bị xoá/archive:** Sửa lỗi item đã xoá bị hiển thị lại sau reload Plugin và khi upload Google Sheet; sửa lỗi không khôi phục được item archive sau khi click icon reload preview.
- **Chỉnh sửa Screen Spec:** Sửa lỗi dữ liệu nhập ở dòng mới bị reset và không tự lưu khi chọn Figma layer; sửa item list bị cache khi chuyển spec trong Frame Set; sửa lỗi 404 khi Reload trên Screen Spec.
- **Preview & liên kết design:** Sửa ảnh preview sai với frame chưa liên kết UI Part; sửa ảnh preview không sync khi vào Screen Detail lần đầu từ Screen Set; sửa lỗi design bị mất liên kết tự động gán vào box thay vì giữ trạng thái chờ liên kết thủ công.
- **Upload Google Sheet:** Sửa lỗi lọc sai loại item (Web chỉ hiện Button, Plugin hiện ngược lại); sửa ảnh bị zoom to hơn preview khiến label bị che.
- **Kết nối Plugin:** Sửa xung đột fetch gây lỗi xoá/archive; sửa không chỉnh sửa được repository sau khi kết nối lại GitHub; sửa không có nút Cancel/Escape khi đang chọn Figma node.
- **Khác:** Sửa Screen Detail không tải được; sửa không cuộn hết danh sách screen trong Screen Set; sửa không ngắt kết nối Google được khi token hết hạn; sửa không scan được media sau khi áp dụng prefix mới cho node mms; sửa timeout khi upload dictionary lúc AI retranslate; sửa lỗi bảo mật trong VSCode Extension liên quan đến quyền truy cập dữ liệu.

---

## 2026-04-09

**✨ Tính năng mới**

- **Ẩn/hiện nhãn spec trên preview** — Bạn có thể bật/tắt hiển thị nhãn spec ngay trên khu vực preview design chỉ bằng một cú click, giúp quan sát design rõ ràng hơn khi cần.

**🔧 Cải tiến**

- **Nâng cao chất lượng AI generate spec & test cases** — Thông tin tổng quan màn hình (screen overview) được gửi kèm làm context khi AI generate, giúp kết quả sinh ra chính xác và phù hợp hơn.
- **Tự động cuộn khi click Design ID** — Click vào Design ID trên màn preview sẽ tự động cuộn và highlight đúng item tương ứng trong danh sách.
- **Thông báo khi copy Screen ID** — Một toast notification sẽ xuất hiện khi bạn copy Screen ID, xác nhận thao tác đã thành công.
- **Cải thiện tooltip** — Tất cả tooltip trong Plugin và Web được thêm delay 400ms và hiệu ứng fade-in, mang lại trải nghiệm mượt mà hơn.
- **Nhận diện Layer ID chính xác hơn** — Plugin đã nhận diện đúng các layer có prefix `mms_id_` ngay từ lần load đầu tiên.
- **Đồng nhất URL** — Toàn bộ URL trong hệ thống đã được chuyển sang dùng `screen_id` thay vì `frame_id`.

**🐛 Sửa lỗi**

- Đã sửa nhiều lỗi, bao gồm các vấn đề về hiển thị preview, đồng bộ spec, frame archived, UI Parts, lưu Input Spec, trạng thái AI generation, và tìm kiếm repository GitHub.

---

## 2026-04-01

**🆕 Tính năng mới**

【Xem & chỉnh sửa spec màn hình】

- Có thể chỉnh sửa tiêu đề và tổng quan (Overview) của màn hình.
- Screen ID được hiển thị trên danh sách màn hình. ID này dùng để xác định màn hình khi tải xuống hoặc tải lên thông số spec qua MCP server.
- Thêm tính năng hiển thị, thêm mới và sắp xếp Active Item List - danh sách phần tử giao diện màn hình.
- Thêm tính năng đánh số thông số hàng loạt.
- Thêm chức năng Copy Spec giữa các màn hình.

【Tính năng AI】

- AI có thể tự động tạo tổng quan màn hình và định nghĩa item dựa trên Figma UI.

【CLI / MCP】

- Có thể tải xuống (download) và tải lên (upload) thông số màn hình bằng CLI hoặc MCP tools. Chỉ định Screen ID để lấy hoặc cập nhật thông số của màn hình tương ứng.

**✨ Cải tiến**

【Spec màn hình】

- Cập nhật modal xác nhận ghi đè khi gen spec.

【Tính năng AI】

- Cập nhật UI và logic của modal cài đặt tạo Testcase bằng AI.

【Tích hợp】

- Cải thiện xử lý đồng bộ với Google Sheets.

**🔧 Sửa lỗi**

【Plugin】

- Sửa lỗi Plugin không nhận diện layer Figma có ký tự đặc biệt trong tên layer.

【Cài đặt / Settings】

- Sửa lỗi user không phải admin vẫn có thể unlink repo trong Settings / Github.

【Khác】

- Sửa các lỗi hiển thị và thao tác tại Screen List, Screen Spec, Screen Set và các màn hình khác.

---

## 2026-03-27

- **[Tính năng & Cải tiến]** Hỗ trợ phát hiện các Frame lồng nhau trong cấu trúc Nested Sections của Figma, và tự động migrate các tiền tố layer cũ.
- **[Sửa lỗi]** Khắc phục lỗi mất dữ liệu spec sau khi quay lại từ màn hình cài đặt, sửa lỗi không thể tạo spec tự động cho nhiều item cùng lúc bằng AI và sửa lỗi không hiển thị nhãn cài đặt.

---

## 2026-03-20

**🆕 Tính năng mới**

- Danh sách màn hình được chia thành 4 tab trạng thái (Đang thiết kế / Đang phát triển / Đang review / Hoàn thành) với badge đếm số lượng.
- Có thể Archive các màn hình không cần thiết và khôi phục bất cứ lúc nào. Màn hình ẩn cũ sẽ tự động chuyển sang Archive.
- Màn hình chưa hoàn thiện design (No UI / In Design) nay có thể click để xem chi tiết.
- Trường mô tả trong thông số mục hỗ trợ Markdown. Sử dụng thanh công cụ mới để nhập in đậm, danh sách, code block… Đồng bộ giữa Plugin & Web.
- Form thông số mục hỗ trợ nhập ID và liên kết trực tiếp đến Figma layer. Tên layer tự động thêm prefix "mms_".
- Prefix liên kết Figma layer được thống nhất thành "mms_" trong toàn ứng dụng. Định dạng cũ tự động chuyển đổi.

**✨ Cải tiến**

- Giao diện 4 màn hình Bộ màn hình (Danh sách / Thêm / Chi tiết / Chỉnh sửa) được làm mới toàn diện. Hỗ trợ nhãn tiếng Nhật, Anh, Việt.
- Khu vực Preview trong thông số màn hình có thêm chế độ toàn màn hình và nút cài đặt đánh số thông số.
- Có thể cập nhật trạng thái vòng đời (Thiết kế / Thông số / Phát triển) ngay từ chi tiết màn hình, phản ánh realtime trên danh sách.

**🔧 Sửa lỗi**

- Khi tài khoản Google hết hạn lúc upload spec, hiển thị thông báo lỗi rõ ràng và nút kết nối lại.
- Sau khi AI sinh spec, nội dung phản ánh ngay trên UI mà không cần reload trang.
- Sửa lỗi modal "Rời trang?" hiển thị sai sau khi lưu trên màn quản lý Tag.
- Khi AI sinh thất bại, toast lỗi được hiển thị và trạng thái mục được cập nhật đúng (generating → error / timeout).
- Thống nhất thiết kế button màn quản lý Tag với toàn bộ ứng dụng.

**🗑️ Loại bỏ**

- Xóa tùy chọn "Default Mode" khỏi Cài đặt (đã thay bằng hiển thị tab trạng thái).
- Loại bỏ tính năng Frame Lock — có thể chỉnh sửa design trên Figma tự do khi đang tạo thông số.
- Bỏ modal xác nhận trước khi AI sinh cho mục chưa có spec (màn hình cài đặt mở trực tiếp).

---

## 2026-03-12

**Bug Fixes**

- Đồng bộ dữ liệu: Khắc phục sự cố không đồng bộ dữ liệu giữa Plugin và Web. Hiện tại, hệ thống đã tự động kích hoạt đồng bộ khi người dùng mở màn hình Đặc tả (Screen Spec).
- Xử lý lỗi (Error Handling): Sửa lỗi không hiển thị thông báo lỗi ở trường nhập URL Figma khi phiên đăng nhập (session) của người dùng đã hết hạn.

---

## 2026-02-13

**[What's New & Improved]**

- Quản lý Spec: Chúng tôi đã nâng cấp Element Spec Version Control và triển khai All Specs Screen mới để xem tất cả đặc tả của các mục tại một nơi.
- Thêm màn Tổng quan Dự án: Một màn hình cài đặt Project Overview chuyên dụng đã được thêm vào để cấu hình dễ dàng hơn.
- Phục hồi Dữ liệu: Các Spec (đặc tả) cho các layer đã xóa hoặc bị ẩn giờ đây có thể được khôi phục khi layer được phục hồi.
- Tùy chỉnh Xuất dữ liệu spec: Bạn hiện có thể chọn có đính kèm sheet i18n hay không.
- AI generator: Cải thiện chất lượng spec được tạo bởi AI.
- Tinh chỉnh UI/UX:
  - Cập nhật UI cho modal xác nhận "Leave Page".
  - Cải thiện văn bản nhãn trên màn hình Cài đặt Tích hợp GitHub Integration Settings screen.

**[Bug Fixes]**

- Hiển thị Định dạng Thời gian: Đã sửa lỗi định dạng thời gian không nhất quán khi chuyển đổi ngôn ngữ trong Status History.
- Cập nhật Trạng thái: Đã khắc phục lỗi trạng thái Test Case Generation không được cập nhật sau khi tải lên Google Sheets thành công.
- Vấn đề Đa ngôn ngữ: Văn bản nhãn của GitHub Upload không thay đổi trong môi trường tiếng Nhật.
- Logic Lọc: Đã sửa lỗi các frame bị loại trừ trong chế độ "For Design" bị chuyển nhầm vào danh sách In Design.
- Ngoài ra: Đã xử lý vấn đề hình thumbnail của tập tin không hiển thị đối với các tập tin đã hết hạn.

---

## 2026-01-15

**[Tính năng mới]**

- Media Scan & Upload: Thêm chức năng quét và tải lên media files.

**[Cập nhật]**

- MoMorph Syncer: Hỗ trợ đa ngôn ngữ cho menu.
- Cải thiện UX: Nâng cao trải nghiệm người dùng trong Danh sách Frame bằng cách tự động focus sau khi chỉnh sửa tag.
- Thông báo lỗi: Làm rõ các thông báo lỗi liên quan đến whitelist email và xác thực tài khoản.

**[Khác]**

- Bảo mật: Tăng cường bảo mật cho URL hình ảnh khi export GitHub issue và google sheet.

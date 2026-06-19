# MoMorph — Release Notes (Lưu trữ)

Các bản phát hành MoMorph trước đây. Xem bản mới nhất tại [Release Notes](release-notes.md).

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

## 2026-05-28

**✨ Mới & Cải tiến**

- **Đổi mới logic sort & reorder Screen Spec** — Sort cycle 3-state (↕ → ASC → DESC → ↕); sort và drag-drop chỉ preview UI, phải dùng Save / Cancel chung của edit table mới ghi DB. `No` rỗng luôn xuống cuối; `No` dạng dotted sort theo lexical.
- **Maintenance mode** — Hiển thị màn maintenance chuyên dụng trong các đợt release.

**🐛 Sửa lỗi**

- Item bị missing UI Part vẫn hiển thị đúng trên Item List sau khi Reload preview.
- Cancel item AI gen spec đang ở trạng thái queued giờ trả về đúng `draft`, không còn tự revert về `generating`.

---

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

## 2026-04-24

**🐛 Sửa lỗi quyền truy cập GitHub repository**

- Sửa lỗi thiếu dữ liệu (tags, media, comments, ảnh đã bản địa hoá) đối với người dùng đăng nhập qua GitHub được gọi từ VSCode Extension, MCP, CLI.
- Chỉ người dùng MoMorph có quyền Admin trên GitHub repository mới có thể kết nối/ngắt kết nối repo với Figma file.

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

- Sửa lỗi user không phải admin vẫn có thể unlink repo trong Settings / GitHub.

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
- Form thông số mục hỗ trợ nhập ID và liên kết trực tiếp đến Figma layer. Tên layer tự động thêm prefix "mms\_".
- Prefix liên kết Figma layer được thống nhất thành "mms\_" trong toàn ứng dụng. Định dạng cũ tự động chuyển đổi.

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

---

## 2025-12-24

**🚀 Tính năng mới & Cải tiến**

- Tùy chỉnh style cho nhãn số thứ tự của item.
- Liên kết linh hoạt: Có thể kết nối tài khoản GitHub/Google bằng bất kỳ địa chỉ email nào.
- Đồng bộ Spec: Hỗ trợ đồng bộ spec của các design item mới thêm vào các sheet hiện có.
- Cải thiện UX: Cải thiện nhận diện ngôn ngữ ban đầu và tinh chỉnh các thông báo toast.

**🐛 Sửa lỗi**

- Sửa logic Tag Filter (nay hoạt động theo "Partial Match" thay vì "Exact Match" đối với system tags).
- Sửa lỗi Page Extraction hiển thị frame từ tất cả các page thay vì chỉ các page đã chọn.
- Khắc phục các điểm chưa nhất quán về UI trong Tag List.

**⚠️ Cần thực hiện:** Vui lòng reload tab Figma hoặc khởi động lại plugin để áp dụng các thay đổi này.

---

## 2025-12-11

**[Cập nhật]**

- **Cải thiện UI/UX:** Nâng cao thiết kế và khả năng sử dụng của màn hình upload, settings và các màn hình quan trọng khác.
- **Hỗ trợ đa ngôn ngữ:** Bổ sung hỗ trợ tiếng Nhật và tiếng Việt ở màn hình đăng nhập và các màn hình khác.
- **Tối ưu hóa:** Cải thiện cách đặt tên khi export spreadsheet và làm rõ các thông báo lỗi.

**[Sửa lỗi]**

- Cải thiện độ ổn định: Sửa nhiều lỗi liên quan đến AI sinh spec, đồng bộ hình ảnh và revision để hoạt động mượt mà hơn.

---

## 2025-11-27

- **Hiệu năng:** Cải thiện độ ổn định và tốc độ khi xử lý các file Figma lớn.
- **Hệ thống Tags:** Tối ưu logic lọc, lưu và hiển thị.
- **Sửa lỗi & UI/UX:** Nâng cao độ tin cậy của tích hợp GitHub và khắc phục nhiều lỗi giao diện.
- **Backend:** Tăng cường hạ tầng phân tích dữ liệu và độ ổn định của đồng bộ.

---

## 2025-11-13

- **Cải tiến:** Tăng cường bảo mật, xử lý Figma API rate limit, thêm Điều khoản/Chính sách vào màn hình Welcome và triển khai trang 404.
- **Sửa lỗi quan trọng:** Khắc phục lỗi không lưu được spec, sửa lỗi hiển thị sai dữ liệu cho "frame set" mới, và sửa lỗi trạng thái "Generate Test Case" bị kẹt ở "In Queue".
- **Sửa lỗi khác:** Sửa nhiều lỗi UI/UX nhỏ.

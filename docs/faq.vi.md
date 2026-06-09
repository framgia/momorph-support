# MoMorph — FAQ & Hướng dẫn xử lý sự cố

## License & Vận hành

### <u>Phân biệt Essential và Pro</u>
**❓ Q:** Gói người dùng Essential và Pro khác nhau như thế nào?

**💡 A:** Theo Hướng dẫn sử dụng, hai gói khác nhau ở phạm vi tính năng:

- **Essential**: chỉ sử dụng được Plugin — quản lý screens, nhập spec thủ công và export GitHub issue. Gói này không truy cập được Web App, Syncer, CLI, MCP, VSCode Extension hay Claude Desktop Extension.
- **Pro**: sử dụng được toàn bộ hệ sinh thái — Plugin (đầy đủ), Web, Syncer, CLI, MCP, VSCode Extension và Claude Desktop Extension.

Người dùng có email thuộc domain công ty Sun* sẽ mặc định là tài khoản Pro. Với các email khác, bạn vui lòng liên hệ team MoMorph để được cấp tài khoản Pro.

### <u>Kênh liên hệ & hỗ trợ</u>
**❓ Q:** Tôi có thể gửi câu hỏi hoặc phản hồi cho MoMorph qua kênh nào?

**💡 A:** Bạn có thể liên hệ với chúng tôi qua:

- Slack: **#con_momorph-support_all**
- Email: **momorph-admin@sun-asterisk.com**

Lưu ý: bạn vui lòng xóa hoặc che các hình ảnh có chứa thông tin nhạy cảm/bảo mật của dự án trước khi gửi.

## Lỗi & Sự cố

### <u>CLI báo 'user not found'</u>
**❓ Q:** Khi đăng nhập GitHub trong CLI mà nhận thông báo 'user not found' thì tôi nên làm gì?

**💡 A:**

- Bạn hãy đăng nhập lại CLI bằng `momorph login`, sau đó kiểm tra bằng `momorph whoami`.
- Đồng thời, hãy đảm bảo firewall/VPN không chặn `github.com/login/device`.

### <u>Tài khoản chưa được thêm vào dự án GitHub</u>
**❓ Q:** Tôi không kết nối được GitHub và nhận thông báo tài khoản chưa được thêm vào dự án. Tôi nên xử lý thế nào?

**💡 A:** Bạn vui lòng thực hiện liên kết GitHub trên MoMorph Web (Settings → GitHub → Connect repo).

### <u>Item không xuất hiện hoặc sai thứ tự</u>
**❓ Q:** Tôi đã gán số vào tên layer Figma nhưng MoMorph không load được item, hoặc thứ tự item bị sai. Tôi nên xử lý thế nào?

**💡 A:** Một số nguyên nhân thường gặp:

- Tên layer chưa đúng prefix `mms_`. Bạn hãy đổi tên layer trên Figma theo dạng `mms_<tên>`.
- Dữ liệu trên MoMorph chưa đồng bộ với thứ tự của Figma layer tree, dẫn đến thiếu item hoặc sai thứ tự.

Bạn có thể khắc phục như sau:

- Bấm nút **Làm mới (Refresh)** trên thanh Preview của MoMorph Plugin để load/đồng bộ lại item.
- Dùng nút **"Find on Figma"** để kiểm tra item/màn hình đang mở có khớp với frame Figma mong muốn không.
- Lưu ý rằng các layer đang bị ẩn hoặc là frame cha ngoài cùng sẽ không được load.

### <u>Giá trị No trên MoMorph không đúng</u>
**❓ Q:** Vì sao giá trị No trên MoMorph không trùng khớp với prefix đã gán vào tên layer Figma?

**💡 A:** Đây là hành vi theo thiết kế của MoMorph:

- Số trên tên layer Figma chỉ được dùng làm Item No cho **lần đồng bộ dữ liệu đầu tiên** lên MoMorph server.
- Sau lần đó, nếu muốn thay đổi giá trị "No", bạn hãy chỉnh trực tiếp tại cột "No" trên MoMorph; hệ thống không đồng bộ ngược về Figma. Cách này giúp tránh mâu thuẫn dữ liệu khi giá trị "No" bạn chỉnh trên Web khác với số trên tên layer Figma.

### <u>Mất spec sau khi thay frame Figma</u>
**❓ Q:** Sau khi sửa thiết kế trên Figma, dữ liệu spec đã nhập trên MoMorph bị mất. Vì sao và làm thế nào để khắc phục?

**💡 A:** Tình huống này thường xảy ra khi bạn dùng chức năng Paste to Replace của Figma để thay frame gốc bằng một frame có thiết kế mới hơn. Khi đó, frame gốc trên MoMorph sẽ bị xóa; phần spec đã tạo cho frame gốc vẫn được giữ lại nhưng chuyển sang trạng thái No UI (chưa có design), đồng thời frame mới sẽ xuất hiện trong danh sách màn hình chưa có spec.

Nguyên nhân là Figma gán một ID hoàn toàn mới cho frame thay thế, nên hiện tại MoMorph chưa thể tự nhận ra frame gốc để chuyển dữ liệu spec sang frame mới.

Cách khắc phục: tại khu vực Preview của màn hình gốc (đang ở trạng thái No UI) trên MoMorph, bạn hãy dùng chức năng link frame để liên kết spec này với frame design mới. Trong danh sách item, cột UI Part cũng cần được liên kết lại với các layer tương ứng của frame mới.

### <u>AI generation bị dừng giữa chừng</u>
**❓ Q:** Khi AI tạo nội dung bị dừng giữa chừng hoặc báo lỗi máy chủ thì tôi nên làm gì?

**💡 A:**

- Với màn hình có nhiều item, quá trình AI sinh nội dung có thể mất khoảng **30–60 giây**. Bạn vui lòng đợi thêm một chút trước khi xem đây là lỗi.
- Nếu hệ thống báo lỗi máy chủ, nguyên nhân có thể do MCP server đang quá tải hoặc gặp sự cố tạm thời. Bạn hãy đợi một lát rồi thử lại.

### <u>Lỗi đồng bộ Google Sheets</u>
**❓ Q:** Khi đồng bộ spec giữa MoMorph và Google Sheets bị lỗi thì tôi nên xử lý thế nào?

**💡 A:** Đây là chức năng của **MoMorph Syncer** (Google Add-on). Một số lỗi thường gặp:

- **"Cannot access spreadsheet"**: file cần thuộc Google Workspace của công ty Sun* và tài khoản của bạn phải có quyền **Editor** với file đó (quyền Viewer không đồng bộ ngược được).
- **"Missing authentication token"**: phiên đăng nhập Google đã hết hạn. Bạn hãy đăng nhập lại bằng email thuộc domain công ty Sun* và tải lại tab Sheets.
- **"Failed to sync data"**: có thể do mạng hoặc hệ thống bị gián đoạn. Bạn vui lòng đợi vài phút rồi thử lại.

### <u>Lỗi khi export spec sang GitHub</u>
**❓ Q:** Khi gửi spec sang GitHub bị báo lỗi thì tôi nên xử lý thế nào?

**💡 A:** Bạn vui lòng kiểm tra lại màn hình cài đặt liên kết GitHub, sau đó thử ngắt kết nối và kết nối lại tài khoản GitHub cùng repository.

### <u>File CSV bị lỗi font</u>
**❓ Q:** Khi mở file CSV bị lỗi font thì tôi cần kiểm tra gì?

**💡 A:** Bạn vui lòng kiểm tra lại công cụ (tool preview) đang dùng để mở file CSV. Nếu công cụ vẫn hoạt động bình thường mà nội dung tiếp tục hiển thị sai, bạn hãy liên hệ team MoMorph để được hỗ trợ.

## Cài đặt & Sử dụng

### <u>Best practice thiết kế Figma cho AI</u>
**❓ Q:** Designer nên thiết kế Figma như thế nào để phối hợp với AI hiệu quả nhất?

**💡 A:** Bạn có thể tham khảo một số gợi ý sau:

- **Cấu trúc & tổ chức:** tận dụng Pages; đặt tên screen/item rõ ràng và duy nhất (việc trùng tên item có thể gây lỗi khi dùng AI để generate danh sách item hoặc spec); chuẩn hóa component; xóa các frame/layer ẩn không cần thiết; và tránh để screen quá dài.
- **Kỹ thuật thiết kế:** dùng Auto Layout một cách nhất quán; thiết kế đầy đủ các trạng thái (states), bao gồm cả edge case; và sử dụng Component Instance một cách có kỷ luật.
- **Cấu trúc Figma:** mỗi Frame tương ứng với một màn hình; số cấp Section nên giữ trong khoảng tối đa 7 cấp (nếu vượt quá 7 cấp, MoMorph có thể không nhận diện được các Frame nằm sâu từ tầng thứ 8 trở đi); và nên ý thức về cấu trúc phân cấp ngay từ đầu.

### <u>Quy tắc đặt tên item (mms_ / id_)</u>
**❓ Q:** Cách đặt tên item để MoMorph nhận diện là gì, và khi nào thì tên cũ 'id_' ngừng được hỗ trợ?

**💡 A:**

- **Quy tắc mới:** thêm prefix `mms_` vào tên layer. Nội dung đánh số có thể xem và chỉnh trực tiếp trên MoMorph.
- **Quy tắc cũ:** prefix `id_` sẽ không còn được nhận diện sau ngày 30/05/2026.

### <u>Nguồn dữ liệu khi tạo spec</u>
**❓ Q:** MoMorph tạo spec.md dựa trên thiết kế hay dựa trên spec cũ?

**💡 A:** MoMorph sinh spec trực tiếp từ thiết kế trên Figma. Tuy nhiên, việc tham chiếu thêm spec cũ sẽ giúp đưa ra các phân tích chi tiết hơn về thay đổi.

### <u>Phạm vi đồng bộ Google Sheets</u>
**❓ Q:** Khi sửa spec trên Google Sheets, nội dung có tự cập nhật sang Plugin/Web và file spec.md (được tạo khi generate code) không?

**💡 A:**

- Nội dung thay đổi trên Spreadsheet chỉ được cập nhật lên MoMorph server thông qua menu đồng bộ của MoMorph Syncer.
- Nội dung này **không** tự động đồng bộ sang file spec.md.

### <u>Để AI lấy spec từ MoMorph</u>
**❓ Q:** Sau khi đã thiết lập xong trên Web, làm thế nào để AI lấy được spec từ MoMorph?

**💡 A:** Bạn có thể thực hiện theo các bước sau:

- Cài đặt CLI: `brew install momorph/tap/momorph-cli`.
- Chạy `momorph login`, sau đó `momorph init . --ai <agent>` (claude/copilot/cursor…) để tự động cấu hình MCP server và slash commands.
- Sau đó, AI agent sẽ tự gọi các MCP tools (qua slash command hoặc prompt thông thường) để lấy spec — ví dụ `/downloadspecs` hoặc một prompt kèm screenId.

Bạn không cần gọi MCP trực tiếp.

### <u>Workflow tạo code: MoMorph vs Takumi kit</u>
**❓ Q:** Quy trình tạo code bằng AI với MoMorph và Takumi kit khác nhau như thế nào?

**💡 A:**

- **MoMorph slash command (hiện hành):** bắt đầu với `/specify` để sinh spec.md, design-style.md và assets, sau đó lần lượt `/plan` → `/tasks` → `/implement`. Đây là workflow chính thức của MoMorph và vẫn đang được hỗ trợ đầy đủ.
- **Takumi kit (bộ công cụ bổ sung):** được tích hợp trên nền MoMorph và linh hoạt hơn, dùng `/create-plan` → `/takumi` hoặc gọi trực tiếp `/takumi`. Bạn cần cài đặt Takumi kit riêng để sử dụng.

### <u>Cập nhật khi có bản mới</u>
**❓ Q:** MoMorph vừa ra bản mới, tôi cần làm gì để cập nhật?

**💡 A:** Do cơ chế cache của Figma, bạn vui lòng reload theo đúng thứ tự sau để nhận thay đổi: **1. Figma → 2. Plugin → 3. Web**.

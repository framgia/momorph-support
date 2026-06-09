# MoMorph — FAQ & Hướng dẫn xử lý sự cố

> Nguồn tổng hợp: lịch sử trao đổi Slack `#con_momorph-support_all` (03–05/2026) & Hướng dẫn sử dụng MoMorph (docs/user-guide). Cập nhật lần cuối: 27/05/2026.

## Lỗi & Sự cố

### Q1. Số thứ tự trên Figma và trên MoMorph không giống nhau? (Plugin)

- Số trên Figma **chỉ dùng cho lần phát hiện (detect) đầu tiên**.
- Sau đó, muốn đổi số trên MM phải **sửa trực tiếp ở cột "No" trên MM**, không đồng bộ ngược từ Figma.

Đây là hành vi thiết kế, không phải sự cố ngẫu nhiên.

### Q2. Tự đánh số nhưng có item không hiện ra / không liên kết được? (Plugin)

Theo Hướng dẫn sử dụng: nguyên nhân thường gặp là **tên layer chưa đúng prefix `mms_`** (hoặc convention cũ như `A_`, `1_`). Cách xử lý:

- Sửa tên layer trên Figma theo dạng `mms_<tên>` (không phân biệt hoa-thường).
- Bấm nút **Làm mới (Refresh)** trên Preview toolbar của Plugin để load lại item.
- Layer bị ẩn (visible=false) hoặc parent frame opacity=0 sẽ không được load.

Nếu đã đúng prefix mà item vẫn thiếu → gửi form báo bug (xem Q34).

### Q3. AI tạo nội dung bị dừng giữa chừng, không xong? (AI Generation)

AI sinh nội dung có thể **mất 30–60s với screen nhiều item** — hãy đợi thêm trước khi coi là lỗi. Nếu vẫn không hoàn tất:

- Kiểm tra kết nối mạng tới `mcp.momorph.ai`.
- Thử lại; có thể đổi phương thức đánh số (numbering method).
- Fail nhiều lần → chạy `momorph login` để refresh token.

Nếu lặp lại → gửi form báo bug (xem Q34).

### Q4. File CSV mở ra bị lỗi font / hiển thị sai? (Plugin)

Kiểm tra lại tool preview đang dùng để mở file CSV. Nếu tool preview hoạt động bình thường mà vẫn còn lỗi hiển thị, liên hệ team MoMorph qua Slack `#con_momorph-support_all` để được hỗ trợ.

### Q5. Số thứ tự các item bị sai hoặc lộn xộn? (Plugin)

Thường do **dữ liệu MoMorph chưa đồng bộ với cây Figma**. Cách xử lý:

- Sau khi sửa design trên Figma, bấm nút **Làm mới (Refresh)** trên Preview toolbar để đồng bộ lại.
- Dùng nút **"Find on Figma"** để xác minh item đang trỏ đúng frame mục tiêu.

Nếu vẫn sai → cung cấp thông tin cho đội MM để điều tra.

### Q6. Sửa thiết kế trên Figma xong thì dữ liệu đã nhập trên MoMorph bị mất? (Plugin)

Sau khi sửa/cập nhật design trên Figma, hãy bấm nút **Làm mới (Refresh)** trên Preview toolbar của Plugin để đồng bộ lại. Nếu data link vẫn mất:

- Cung cấp **ScreenID** liên quan cho đội MoMorph.
- Đội MM sẽ cập nhật lại dữ liệu cho các screen bị ảnh hưởng.

### Q7. Gửi spec sang GitHub bị báo lỗi? (Server)

Vấn đề đã được nhiều người dùng báo cáo (cả tiếng Việt và tiếng Nhật). Đội phát triển đang xử lý. Một giải pháp tên **"Github Flex"** đã được giới thiệu để khắc phục giới hạn hiển thị spec trên GitHub Issues.

### Q8. Đăng nhập GitHub trong công cụ dòng lệnh báo 'user not found'? (MCP & CLI)

- Đăng nhập lại CLI: `momorph login` → kiểm tra bằng `momorph whoami`.
- Đảm bảo firewall/VPN không chặn `github.com/login/device` (có thể nhập code trực tiếp tại trang này).
- Phân biệt kết nối **tài khoản GitHub** vs **repository** (xem Q40).

### Q9. Không kết nối được GitHub, báo tài khoản chưa được thêm vào dự án? (Web)

Tài khoản cần là **Pro user** mới dùng được CLI/MCP/VSCode:

- Email `@sun-asterisk.com` tự động là Pro.
- Email khác → liên hệ Slack `#con_momorph-support_all` để được add whitelist Pro.

Ngoài ra cần đã liên kết GitHub trên MoMorph Web (file → Settings → GitHub → Connect repo).

### Q10. Kết nối AI (MCP) báo lỗi máy chủ, không dùng được? (MCP & CLI)

Nguyên nhân có thể do MCP server đang quá tải hoặc xảy ra lỗi tạm thời. Vui lòng đợi một lúc rồi thử lại. Nếu MCP vẫn chưa được khôi phục, liên hệ team qua Slack `#con_momorph-support_all` để được xử lý.

### Q11. Đồng bộ spec giữa MoMorph và Google Sheets bị lỗi? (Web)

Đây là chức năng **MoMorph Syncer** (Google Add-on). Lỗi thường gặp:

- **"Cannot access spreadsheet"**: file phải nằm trong Sun* Workspace và account có quyền **Editor** (Viewer không sync ngược).
- **"Missing authentication token"**: session Google hết hạn → re-login bằng email `@sun-asterisk.com`, refresh tab Sheets.
- **"Failed to sync data"**: backend/mạng gián đoạn → đợi vài phút thử lại.

Cần debug sâu, đội MoMorph có thể yêu cầu quyền editor file Figma/Sheets.

## Cài đặt & Kết nối

### Q12. Đã setup xong trên Web, làm sao để AI lấy được spec? (MCP & CLI)

Các bước:

- Cài CLI: `brew install momorph/tap/momorph-cli`.
- `momorph login` → `momorph init . --ai <agent>` (claude/copilot/cursor…) để tự cấu hình MCP server + slash commands.
- Sau đó AI agent tự gọi MCP tools (slash command hoặc prompt tự nhiên) để lấy spec — vd `/downloadspecs` hoặc prompt kèm screenId.

Người dùng không gọi MCP trực tiếp.

### Q13. Đã kết nối GitHub mà thành viên vẫn không mở được file Figma? (Web)

- Khi **admin** kết nối GitHub, thành viên trong repository sẽ truy cập được file Figma.
- Đôi khi GitHub webhook xử lý sự kiện thêm thành viên gặp trục trặc.
- **Giải pháp:** tạm thời disconnect và reconnect GitHub.

### Q14. Một file Figma và repo GitHub liên kết với nhau theo tỉ lệ nào? (Web)

- Một GitHub repository **CÓ THỂ** kết nối tới NHIỀU file Figma.
- Một file Figma **KHÔNG THỂ** kết nối tới nhiều repository (chiều ngược lại chưa hỗ trợ, sẽ phát triển trong tương lai).

### Q15. Khách hàng cần gì để bắt đầu dùng MoMorph? (Web)

Tài khoản cần là **Pro user** để dùng đầy đủ hệ sinh thái:

- Email `@sun-asterisk.com` tự động có Pro.
- Email khác (khách hàng) → liên hệ Slack `#con_momorph-support_all` để được add whitelist Pro.

Sau khi được thêm, thông báo lại cho khách để tạo tài khoản và đăng nhập. (Essential chỉ dùng được Plugin.)

## Release & Numbering

### Q16. MoMorph vừa ra bản mới, cần làm gì để cập nhật? (Plugin)

Quy trình reload (đúng thứ tự): **1. Figma → 2. Plugin → 3. Web**. Với người đã mở plugin, khi khởi động khuyến nghị mở màn hình chi tiết (detail screen) và đồng bộ (sync).

### Q17. Xem lịch sử cập nhật (release) ở đâu? (Server)

Xem lịch sử release đầy đủ tại **Release Notes** trên Slack `#con_momorph-support_all`. Riêng **Figma Plugin** có thể theo dõi version trên trang Figma Community của MoMorph: [figma.com/community/plugin/…/momorph](https://www.figma.com/community/plugin/1406117276934709483/momorph).

### Q18. Bản VSCode Extension v0.12.4 có gì mới? (VSCode Ext)

- Cải thiện cơ chế kích hoạt extension.
- Bổ sung tính năng Figma Tree View.
- Cải tiến tìm kiếm và lọc (search/filter).
- Nâng cấp UI/UX.

### Q19. Cách đặt tên item để MoMorph nhận diện là gì? Khi nào tên cũ 'id_' ngừng dùng được? (Figma)

- **Quy tắc mới:** gán prefix **mms_** vào tên layer. Nội dung đánh số xem/sửa trực tiếp trên MoMorph.
- **Quy tắc cũ:** prefix **id_** — không còn được nhận diện sau 30/05/2026.
- **Auto migration:** 27/03/2026 – 29/05/2026.

> ⚠️ Sau 29/05/2026, hệ thống không còn tự chuyển id_ sang mms_. Đảm bảo migration hoàn tất trước thời hạn này.

### Q20. Muốn đổi số thứ tự thì sửa ở MoMorph hay ở Figma? (Plugin)

Khi muốn thay đổi số thứ tự sau lần detect đầu, **sửa cột "No" trên MM** chứ không phải trên Figma. Số trên Figma chỉ phục vụ lần phát hiện đầu tiên.

## Spec, Workflow & Figma

### Q21. Sửa spec trên Google Sheets có tự cập nhật vào file spec không? (Web)

- Nội dung từ Spreadsheet chỉ lưu trong MoMorph DB.
- **Không tự động đồng bộ sang file spec.md.**
- Thông tin BrSE chỉnh trên Spreadsheet sẽ được AI tiếp nhận và lưu dưới dạng markdown trong quá trình xử lý.

### Q22. Nên ghi gì vào ô 'Note' và ô 'Description' trong spec? (Web)

- **Description:** mô tả tổng quan của item và các tương tác người dùng với item đó.
- **Note:** bổ sung giải thích cho từng section trong spec.

Với item dạng button, thay đổi DB khi click cần được ghi trong "Description".

### Q23. Quy trình tạo code bằng AI với MoMorph và Takumi kit khác nhau ra sao? (MCP & CLI)

- **MoMorph slash commands (hiện hành):** bắt đầu bằng `/specify` → sinh spec.md + design-style.md + assets → `/plan` → `/tasks` → `/implement`. Đây là workflow chính thức của MoMorph, vẫn đang được hỗ trợ đầy đủ.
- **Takumi kit (bộ công cụ bổ sung):** tích hợp trên nền MoMorph, linh hoạt hơn: `/create-plan` → `/takumi`, hoặc gọi trực tiếp `/takumi`. Không phải MoMorph slash command — cần cài Takumi kit riêng.

### Q24. Designer nên thiết kế Figma thế nào để phối hợp với AI tốt nhất? (Figma)

**Cấu trúc tổ chức:** tận dụng Pages; đặt tên screen/item chính xác; chuẩn hóa component; xóa frame/layer ẩn không cần thiết; tránh screen quá dài.

**Kỹ thuật thiết kế:** dùng Auto Layout nhất quán; thiết kế đầy đủ các states (gồm edge case); kỷ luật khi dùng Component Instance.

**Cấu trúc Figma:** 1 Frame = 1 màn hình; có giới hạn cấp lồng (nesting) Section; ý thức cấu trúc phân cấp ngay từ đầu.

### Q25. Đặt trùng tên item trên Figma có sao không? (Figma)

Đặt tên item trùng lặp có thể gây lỗi trên MoMorph. Vấn đề đã được báo cáo, đội đang xem xét khắc phục. Best practice: **luôn đặt tên item duy nhất** trong cùng phạm vi.

### Q26. MoMorph tạo spec dựa trên thiết kế hay dựa trên spec cũ? (AI Generation)

Theo đội MoMorph: MM **sinh spec hợp lý trực tiếp từ Figma design**, không bắt buộc tham chiếu spec.md cũ. Nếu không tham chiếu spec cũ thì khó tạo phân tích chi tiết hơn — nhưng mục tiêu thiết kế là tạo spec hợp lý từ chính design. (Liên quan Q21 về đồng bộ spec.)

### Q27. Thiết kế Figma cho MoMorph có giới hạn gì cần lưu ý? (Figma)

- **Frame = 1 màn hình:** MoMorph đọc mỗi Frame như một screen độc lập.
- **Giới hạn nesting Section:** có giới hạn độ sâu, không lồng quá sâu.
- Khuyến nghị (không bắt buộc) không tạo layer dư thừa.
- Ý thức cấu trúc phân cấp ngay khi bắt đầu thiết kế.

Việc đăng ký gói Figma trả phí nên dựa trên tần suất thay đổi thiết kế — không bắt buộc toàn đội.

## License & Vận hành

### Q28. Có được đăng thông tin dự án lên kênh hỗ trợ chung không? (Chung)

Để tránh rò rỉ thông tin dự án: hạn chế đăng nội dung chứa thông tin PJ trên kênh chung; khi cần trao đổi chi tiết, dùng DM group riêng (thêm đại diện đội MoMorph khi cần).

### Q29. Gói Essential và Pro khác nhau thế nào? (License)

Theo Hướng dẫn sử dụng:

- **Essential**: **chỉ dùng Plugin** — quản lý screens, nhập spec thủ công, export GitHub issue. Không truy cập Web App, Syncer, CLI, MCP, VSCode Extension, Claude Desktop Extension.
- **Pro**: **toàn bộ hệ sinh thái** — Plugin (full) + Web + Syncer + CLI + MCP + VSCode Extension + Claude Desktop Extension.

Email `@sun-asterisk.com` tự động là Pro; email khác liên hệ Slack để add whitelist.

### Q30. Dùng AI (Copilot, Claude Code) trong MoMorph tính phí thế nào? (License)

- Sinh spec & test case: có thể dùng MoMorph BE hoặc Copilot.
- Sinh code: Claude Code được khuyến nghị; có thể request Claude Code Premium Seat tùy phase.
- Copilot có một số giới hạn sử dụng theo gói license.

### Q31. Dùng AI (MCP) báo lỗi xác thực, thường do đâu? (MCP & CLI)

Thường do **GitHub PAT bị revoke/hết hạn** (lỗi `x-github-token invalid / 401`). Cách xử lý:

- Tạo PAT mới scope `user`, cập nhật vào MCP config (vd `~/.claude.json`).
- Nếu dùng `momorph init`: chạy `momorph login` để token tự merge vào config.

### Q32. Gửi câu hỏi / phản hồi cho MoMorph ở kênh nào? (Chung)

Kênh nhận feedback đã hợp nhất vào **#con_momorph-support_all**. Kênh cũ #temp_archived_moved-to-con_mormorph-support_all đã được archive.

### Q33. Có tài liệu hướng dẫn sử dụng MoMorph không? (Chung)

Có. Đội MoMorph cung cấp bộ tài liệu chính thức:

- **MoMorph — Hướng dẫn sử dụng** (Plugin, Web, Syncer, CLI, MCP, VSCode Extension, Claude Desktop Extension) — bản EN/JP/VI.
- **MoMorph MCP Server — Tools Reference** (mô tả 31 tools).
- Release Notes, Testplay, Q&A List.

Yêu cầu file trực tiếp tại Slack `#con_momorph-support_all`.

### Q34. Khi gặp lỗi, cần báo cho đội MoMorph thế nào? (Chung)

Khi gặp bất kỳ lỗi nào ở trên, thực hiện:

- Điền **form báo cáo bug chi tiết** theo yêu cầu của đội MoMorph.
- **Xóa hoặc che các hình ảnh chứa thông tin nhạy cảm/bảo mật** trước khi gửi.

Nếu liên quan dữ liệu screen cụ thể, cung cấp ScreenID để đội xử lý nhanh hơn.

## Đề xuất tính năng

### Q35. Có thể thêm ô mô tả tổng quan cho spec không? (Web)

Đề xuất chính thức: trong quy trình AIDD cần một trường "overview description" để mô tả tổng quan, hiện MoMorph chưa cung cấp. Đề xuất đã gửi đến đội MoMorph.

### Q36. Có thể dán nhiều dòng cùng lúc vào List Item không? (Web)

Hiện việc nhập nhiều dòng vào List Item đang bất tiện. Người dùng muốn có chức năng copy & paste nhiều dòng từ nguồn ngoài (Excel, text) vào List Item.

### Q37. Designer lỡ đặt trùng tên item, MoMorph có tự xử lý được không? (Figma)

Người dùng yêu cầu đội MoMorph nghiên cứu giải pháp khắc phục cho tình huống tên item trùng nhau. Hiện chỉ có khuyến nghị "đặt tên duy nhất" — đề xuất MoMorph xử lý linh hoạt hơn khi gặp tên trùng.

### Q38. Gửi đề xuất tính năng cho MoMorph qua đâu? (Chung)

Người dùng đặt câu hỏi về form/kênh chính thức để gửi feature request — mong muốn có cơ chế tiếp nhận đề xuất tính năng có cấu trúc.

### Q39. MoMorph có hỏi ý kiến người dùng trước khi ra tính năng mới không? (Chung)

Đề xuất: nên có cơ chế thu thập feedback trước khi release tính năng mới, và thông báo release notes trước (advance notification) để người dùng có thời gian chuẩn bị.

### Q40. Kết nối tài khoản GitHub và repo dễ gây nhầm, có cải thiện không? (Web)

Nhiều người dùng nhầm giữa "kết nối tài khoản GitHub" và "kết nối repository". Đề xuất cải thiện UI để hai khái niệm này rõ ràng, tách biệt, không gây hiểu lầm.

### Q41. Khi đồng bộ với Excel, các cột MoMorph chưa có thì có bị mất không? (Web)

Hiện các field không tồn tại trên MM phải nhập tay vào Excel. Đề xuất MoMorph không filter các field hiển thị, cho phép giữ lại tất cả field — kể cả field MM chưa quản lý — để giảm công nhập tay.

---

## Mốc thời gian quan trọng

- 27/03/2026: Bắt đầu auto migration id_ → mms_
- 29/05/2026: Kết thúc giai đoạn auto migration id_ → mms_
- 30/05/2026: Hệ thống ngừng nhận diện prefix id_

## Đầu mối liên hệ

| Vai trò | Người phụ trách |
| --- | --- |
| PM / Release Manager | Sara Tanei, Yuto Furukawa, Thanh, nguyen.hien |
| Tech Lead / Engineering | le.minh.hoang |
| Hỗ trợ vấn đề dự án | Thanh, tran.quoc.luc |

Kênh hỗ trợ chính: **#con_momorph-support_all**

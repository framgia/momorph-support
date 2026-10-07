# Worked examples

Reference for `momorph-screen-spec-skill`.

## A. A NEW screen, three rows

A container and its two children. `UI Parts` on the third row is a layer inside a component
instance. The interaction states sit in quoted multi-line cells; the container row leaves both
interaction columns blank.

```csv
No,Item Name,UI Parts,Item Type,Description,Trigger,Destination,Interaction Note,Data Type,Required,Format,Max Length,Min Length,Default Value,Validation Note,Table Name,Column Name,Database Note,Active status
1,login_form,12:340,others,Container holding the email and password fields.,,,,,,,,,,,,,,active
1.1,email_input,12:341,text_form,Email field. Empty on first load.,on_click,,"- Focus: viền 2px accent, đi tới được bằng Tab
- Hover: viền đậm hơn một bậc
- Error: viền đỏ, thông báo dưới ô, giữ nguyên giá trị đã nhập",string,Required,email,255,,,Từ chối giá trị không có @.,users,email,,active
1.2,submit_button,I12:345;67:8,button,Primary submit. Disabled until both fields validate.,on_click,,"- Hover: nền đậm hơn một bậc, con trỏ pointer
- Focus: viền 2px accent
- Loading: spinner trong nút, nút bị khoá, nhãn giữ nguyên
- Disabled: khi một trong hai ô chưa hợp lệ; giảm độ đậm, không nhận focus
- Nhãn screen reader: ""Đăng nhập""",,,,,,,,,,,active
```

Every row links a new layer, so this file goes through the plugin's Import, or its rows go through
`upload_screen_spec(items)` with each layer's node id as `id`. The CLI refuses it.

## B. Archiving one item through the upsert

```json
{
  "projectId": "prj_...",
  "screen": "SCR7K2M9QX",
  "items": [
    { "id": "12:341", "lifecycle": "archived" }
  ]
}
```

## C. Renumbering a linked item in a file

`email_input` moves from `1.1` to `1.3`; `UI Parts` `12:341` stays and finds the item.

```csv
1.3,email_input,12:341,text_form,...,active
```

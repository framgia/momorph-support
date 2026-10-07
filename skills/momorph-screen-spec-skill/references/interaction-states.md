# Interaction states and accessibility

Reference for `momorph-screen-spec-skill`.

## Which column takes what

| What | Column |
| --- | --- |
| The event that starts the interaction | `Trigger` |
| Where it goes | `Destination` |
| What each state does | `Interaction Note` |
| A disabled condition that comes from a business rule | The condition in `Interaction Note`, the rule in `Validation Note` |

`Trigger` holds one value. A control that reacts to click and hover takes `on_click`, and the hover
goes into `Interaction Note`. One control is one row, never split to fit two triggers.

## Writing the `Interaction Note`

One line per state the variant set carries.

```
- Hover: nền đậm hơn một bậc, con trỏ pointer
- Focus: viền 2px màu accent, đi tới được bằng Tab
- Loading: spinner trong nút, nút bị khoá, nhãn giữ nguyên
- Disabled: khi nhóm đã đủ 200 thành viên; giảm độ đậm, không nhận focus
```

- Hover and focus are written as two lines.
- A state the variant set does not carry is not written. When a control needs a state the design
  lacks, ask the user (`SKILL.md` step 5).

## Accessibility

No column exists for accessibility; it goes into `Interaction Note`.

```
- Nhãn cho screen reader: "Mời thành viên" (nút chỉ có icon)
- Thứ tự Tab: sau ô tìm kiếm, trước bảng danh sách
- Đóng bằng phím Esc, tiêu điểm quay lại nút đã mở hộp thoại
```

An icon-only control whose design gives no accessible name: ask the user for the name
(`SKILL.md` step 5).

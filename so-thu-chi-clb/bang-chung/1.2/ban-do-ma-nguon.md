# Bản đồ mã nguồn: Sổ thu chi câu lạc bộ

Ký hiệu: [x] tôi đã tự mở tệp để xác nhận; [ ] mới theo lời agent.

## 1. Thư mục chính và vai trò

- `app/main.py`: tạo ứng dụng (`create_app`), tạo bảng khi khởi động, gắn các nhóm route, chuyển người chưa đăng nhập về `/login`. [x]
- `app/routes/`: lớp web, nhận yêu cầu, kiểm tra quyền, gọi nghiệp vụ, hiển thị trang. [x]
- `app/services/`: nghiệp vụ và câu SQL (`ledger.py` thu chi, `reports.py` số dư và báo cáo, `members.py` thành viên). [x]
- `app/templates/`: giao diện Jinja2; bộ lọc `vnd`, `vnd_rounded` khai báo ở `app/templating.py`. [ ]
- `app/db.py`, `app/schema.sql`: kết nối SQLite và ba bảng `members`, `incomes`, `expenses`. [ ]
- `app/money.py`, `app/dates.py`: xử lý tiền và ngày. [x]
- `app/auth.py`: tài khoản thử, `get_current_user` (dòng 66), `require_role` (dòng 74). [x]
- `scripts/seed.py`, `tests/`, `docs/issues/`, `docs/ideas.md`. [x]

## 2. Luồng xử lý

### Thêm một khoản chi

1. `GET /expenses/new` vào `new_expense_form`, `app/routes/expenses.py:39-41`, gọi `require_role` ở dòng 41 rồi hiển thị biểu mẫu. [x]
2. Biểu mẫu gửi `POST /expenses/new`, xử lý ở `app/routes/expenses.py:51` (decorator), kiểm tra quyền ở dòng 61. [x]
3. Số tiền chuyển từ chuỗi sang số nguyên bằng `parse_vnd` (`app/money.py`). [ ]
4. `create_expense`, `app/services/ledger.py:130`: kiểm tra số tiền, ngày (không cho ngày tương lai), nội dung. [x]
5. `INSERT INTO expenses` và `conn.commit()` ở `app/services/ledger.py:147-154`: đây là lúc dữ liệu được lưu. [x]
6. Lỗi `LedgerError` (lớp con của `ValueError`) làm hiện lại biểu mẫu với mã 400; thành công thì chuyển về `/expenses`. [ ]

### Xem báo cáo tháng

1. `report_monthly`, `app/routes/reports.py:24`, kiểm tra quyền thủ quỹ ở dòng 30. [x]
2. `monthly_report`, `app/services/reports.py:22`. [x]
3. `month_range`, `app/dates.py:42-45`, trả ngày đầu và ngày cuối tháng. [x]
4. Khoản thu lọc ở `app/services/reports.py:33`, khoản chi lọc ở dòng 44 (chỉ khoản chi đang hiệu lực). [x]
5. Tổng thu, tổng chi, tổng quỹ tháng tính bằng Python ở `app/services/reports.py:51-53`. [x]
6. Hiển thị ở `app/templates/reports/monthly.html`. [ ]

## 3. Quy ước phát hiện được

- Tiền luôn là số nguyên đồng; cột tiền là `INTEGER` trong `schema.sql`. [x]
- Ngày lưu dạng chuỗi ISO `YYYY-MM-DD`. [x]
- Không xóa dữ liệu: khoản chi bị hủy, thành viên rời đi đều chỉ đổi trạng thái. [x]
- Phân quyền không tự động: mỗi route ghi dữ liệu tự gọi `require_role`. [x]
- `round_vnd` (`app/money.py:38-43`) làm tròn xuống dù docstring nói "nearest". [x]

## 4. Điều còn chưa rõ

- Điều kiện lọc ngày ở `reports.py:33` và `:44` dùng `<` với ngày cuối tháng do `month_range` trả về; có vẻ khác cách `list_incomes` lọc. Tôi chưa chạy thử để kết luận, ghi lại để xem ở phiếu ISSUE-002.

## Chỗ agent giải thích sai hoặc thiếu

Trong phiên đầu tiên (`bang-chung/1.1/phien-dau-tien.md`), agent viết: "Danh sách khoản chi | `GET /expenses` | `app/routes/expenses.py:24`".

Mã nguồn: `app/routes/expenses.py` dòng 22 là `@router.get("")`, dòng 23 là `def expense_list(`, dòng 24 là `request: Request,`. Agent đúng tệp và đúng hàm nhưng số dòng trỏ vào giữa chữ ký hàm.

Cách phát hiện: mở đúng tệp và dòng được dẫn. Ở phiên khám phá của bài này (`phien-kham-pha.md`), tôi kiểm 13 nhận định có dẫn dòng và cả 13 đều khớp, kể cả lời giải thích `round_vnd` làm tròn xuống. Vì vậy tôi không tìm được chỗ sai nào khác trong phiên này.

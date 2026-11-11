# Bản đồ mã nguồn: Sổ thu chi câu lạc bộ

## 1. Thư mục chính và vai trò

- `app/main.py`: tạo ứng dụng, tạo bảng khi khởi động, gắn route, chuyển người chưa đăng nhập về `/login`.
- `app/routes/`: lớp web: nhận yêu cầu, kiểm quyền, gọi nghiệp vụ, hiển thị trang.
- `app/services/`: nghiệp vụ và câu SQL (`ledger.py` thu chi, `reports.py` số dư và báo cáo, `members.py` thành viên).
- `app/templates/`: giao diện Jinja2.
- `app/money.py`, `app/dates.py`: xử lý tiền và ngày. `app/auth.py`: tài khoản thử, `require_role`.
- `scripts/seed.py` nạp dữ liệu mẫu; `tests/` kiểm thử; `docs/issues/` phiếu của thủ quỹ; `docs/ideas.md` ý tưởng dự án.

## 2. Luồng xử lý

### Thêm một khoản chi

1. `app/routes/expenses.py:39-41` hiển thị biểu mẫu, kiểm quyền thủ quỹ: `require_role(user, ROLE_TREASURER)`
2. `app/routes/expenses.py:51-52` nhận biểu mẫu: `@router.post("/new")` / `def new_expense(`
3. `app/routes/expenses.py:61` kiểm quyền lần nữa: `require_role(user, ROLE_TREASURER)`
4. `app/routes/expenses.py:66` đổi chuỗi số tiền: `amount=parse_vnd(amount),`
5. `app/services/ledger.py:130` kiểm số tiền, ngày, nội dung: `def create_expense(`
6. `app/services/ledger.py:149,154` lưu vào cơ sở dữ liệu: `INSERT INTO expenses (...)` rồi `conn.commit()`
7. `app/routes/expenses.py:81` chuyển về danh sách: `return RedirectResponse("/expenses", status_code=303)`

### Xem báo cáo tháng

1. `app/routes/reports.py:23-24` route: `@router.get("/monthly")` / `def report_monthly(`
2. `app/routes/reports.py:30` chỉ thủ quỹ: `require_role(user, ROLE_TREASURER)`
3. `app/routes/reports.py:35` gọi nghiệp vụ: `report = monthly_report(conn, year, mon)`
4. `app/services/reports.py:24` lấy khoảng ngày: `first_day, last_day = month_range(year, month)`
5. `app/services/reports.py:33` lọc khoản thu: `WHERE i.received_on >= ? AND i.received_on < ?`
6. `app/services/reports.py:44` lọc khoản chi đang hiệu lực: `WHERE status = ? AND spent_on >= ? AND spent_on < ?`
7. `app/services/reports.py:51-52` cộng tổng: `income_total = sum(i.amount for i in incomes)`

## 3. Quy ước phát hiện được

- Tiền là số nguyên đồng: `app/schema.sql:13` `amount INTEGER NOT NULL CHECK (amount > 0),`
- Ngày lưu chuỗi ISO: `app/services/reports.py:25` `start, end = first_day.isoformat(), last_day.isoformat()`
- `round_vnd` làm tròn xuống dù docstring nói "nearest": `app/money.py:43` `return amount // 1000 * 1000`
- Phân quyền không tự động: mỗi route ghi dữ liệu tự gọi `require_role` (bước 1 và 3 ở trên).

## 4. Điều còn chưa rõ

- `month_range` trả ngày CUỐI tháng (`app/dates.py:45` `return date(year, month, 1), date(year, month, last)`), nhưng lọc ở bước 5, 6 dùng `<`. Có vẻ bỏ sót ngày cuối tháng; để xem ở phiếu ISSUE-002.
- `fund_balance` (`app/services/reports.py:18`) cộng mọi khoản chi, không lọc trạng thái hủy. Để xem ở phiếu ISSUE-001.

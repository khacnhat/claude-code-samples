# Phiên khám phá mã nguồn

Ghi chú: phiên chạy ở chế độ không tương tác (claude -p), bản này chuyển từ nhật ký phiên thay cho /export.


**user:** Mình mới vào dự án này. (1) Cấu trúc chung: mỗi thư mục chính làm gì? (2) Khi thủ quỹ thêm một khoản chi trên giao diện, những tệp và hàm nào được gọi theo thứ tự nào cho tới khi dữ liệu được lưu vào cơ sở dữ liệu? (3) Khi mở báo cáo tháng, hàm nào lấy dữ liệu, giao dịch được lọc theo ngày thế nào, con số tổng được tính ở đâu? (4) Hàm round_vnd trong app/money.py làm gì? Với mỗi nhận định, ghi tệp và số dòng.

- Công cụ `Bash`: `{"command": "git ls-files | xargs wc -l", "description": "List tracked files with line counts"}`

**assistant:** Dự án nhỏ, mình đọc trực tiếp các tệp liên quan.

- Công cụ `Bash`: `{"command": "for f in README.md app/main.py app/db.py app/money.py app/dates.py app/models.py app/routes/expenses.py app/services/ledger.py app/routes/reports.py app/services/reports.py app/templates/`
- Công cụ `Read`: `{"file_path": "/Users/khacnhat/.claude/projects/-private-tmp-claude-501--Users-khacnhat-Projects-lms-next-lms-v2-b946e30c-af5c-479a-ba22-709ec44af172-scratchpad-hoc-thu-claude-code-samples-so-thu-chi-`
- Công cụ `Bash`: `{"command": "grep -n \"def \\|^ROLE\" app/auth.py app/templating.py app/config.py; grep -n \"def count_members_in_period\" -A14 app/services/members.py; cat -n app/templates/reports/monthly.html | sed`

**assistant:** Mình đã đọc mã nguồn và trả lời từng câu dưới đây, kèm tệp và số dòng. Mình chưa chạy ứng dụng hay pytest, nên mọi nhận định đều dựa trên việc đọc code.

## (1) Cấu trúc chung

Đây là một ứng dụng web FastAPI dùng SQLite (thư viện `sqlite3` chuẩn) và giao diện Jinja2 (`README.md:52-70`).

| Thư mục / tệp | Vai trò |
|---|---|
| `app/main.py` | Tạo ứng dụng ở `create_app` (`:19`), tạo bảng khi khởi động (`:21`), gắn các nhóm route (`:28-29`), chuyển người chưa đăng nhập về `/login` (`:31-33`) |
| `app/routes/` | Lớp web: nhận yêu cầu HTTP, kiểm tra quyền, gọi phần nghiệp vụ rồi hiển thị trang |
| `app/services/` | Nghiệp vụ và câu lệnh SQL: `ledger.py` cho thu và chi, `reports.py` cho số dư và báo cáo, `members.py` cho thành viên |
| `app/templates/` | Giao diện HTML. Bộ lọc `vnd` và `vnd_rounded` được khai báo ở `app/templating.py:17` |
| `app/db.py` | Mở kết nối (`connect`, `:16`), chạy `schema.sql` (`init_db`, `:25`), cấp cho mỗi request một kết nối (`get_db`, `:35`) |
| `app/schema.sql` | Ba bảng `members`, `incomes`, `expenses`. Số tiền là `INTEGER` và phải lớn hơn 0 (`:13`, `:24`) |
| `app/money.py`, `app/dates.py`, `app/models.py` | Hàm xử lý tiền và ngày, các lớp dữ liệu `Member`, `Income`, `Expense` |
| `app/auth.py` | Tài khoản thử và vai trò: `get_current_user` (`:66`), `require_role` (`:74`) |
| `scripts/seed.py` | Nạp dữ liệu mẫu |
| `tests/` | Kiểm thử pytest |
| `docs/issues/` | Phiếu báo lỗi và yêu cầu từ thủ quỹ (ISSUE-001 đến ISSUE-005) |

## (2) Luồng thêm một khoản chi

1. `GET /expenses/new` gọi `new_expense_form` (`app/routes/expenses.py:39-48`). Hàm này kiểm tra vai trò thủ quỹ (`:41`) rồi hiển thị `expenses/new.html`.
2. Biểu mẫu gửi `POST /expenses/new` (`app/templates/expenses/new.html:7`).
3. FastAPI giải các dependency trước: `get_current_user` (`app/auth.py:66`) và `get_db` (`app/db.py:35`, gọi `connect` ở `:16`).
4. `new_expense` chạy (`app/routes/expenses.py:51-81`). Hàm này gọi `require_role` (`:61`), rồi `parse_vnd(amount)` (`:66`; `app/money.py:7-28`) để đổi chuỗi như "50.000" thành số nguyên.
5. `create_expense` (`app/services/ledger.py:130-155`) làm các bước sau:
   - kiểm tra số tiền là số nguyên dương (`:139`)
   - kiểm tra ngày qua `_check_entry_date` (`:22-29`), hàm này gọi `parse_iso_date` (`app/dates.py:12`) và không cho ghi ngày ở tương lai
   - bắt buộc có nội dung (`:143`); nhóm chi để trống thì thành "Khác" (`:145`)
   - **chạy `INSERT INTO expenses` (`:147-153`) và `conn.commit()` (`:154`). Đây là lúc dữ liệu được lưu vào cơ sở dữ liệu.**
   - đọc lại dòng vừa thêm bằng `get_expense` (`:158`)
6. Nếu có lỗi, `LedgerError` là lớp con của `ValueError` (`ledger.py:18`) nên bị bắt ở `expenses.py:71`. Biểu mẫu hiện lại với mã 400. Nếu thành công, ứng dụng ghi thông báo `flash` và chuyển về `/expenses` (`:80-81`).

## (3) Báo cáo tháng

- **Route:** `report_monthly` (`app/routes/reports.py:23-41`). Hàm kiểm tra quyền thủ quỹ (`:30`) và đọc tham số `month` qua `_resolve_month` (`:15-20`). Nếu không có `month` thì dùng tháng hiện tại. Sau đó gọi `monthly_report(conn, year, mon)` (`:35`).
- **Hàm lấy dữ liệu:** `monthly_report` (`app/services/reports.py:22-76`).
- **Cách lọc ngày:**
  - `month_range` trả về ngày đầu và ngày cuối tháng (`app/dates.py:42-45`), được đổi sang chuỗi ISO ở `reports.py:24-25`.
  - Khoản thu được lọc bằng `received_on >= start AND received_on < end` (`:33`).
  - Khoản chi được lọc bằng `status = 'active' AND spent_on >= start AND spent_on < end` (`:44`).
- ⚠️ **Lỗi ở đây:** `end` là *ngày cuối tháng*, mà điều kiện dùng `<`. Vì vậy mọi giao dịch vào ngày cuối tháng (ví dụ 31/10) bị bỏ khỏi báo cáo. Trong khi đó `list_incomes` dùng `BETWEEN`, tức là tính cả hai đầu (`ledger.py:108`). Chính sự khác nhau này khiến hai trang lệch số, nhiều khả năng là nguyên nhân của ISSUE-002 ("Báo cáo tháng thiếu tiền so với danh sách khoản thu").
- **Các con số tổng** được tính bằng Python ngay trong `monthly_report`, không dùng SQL `SUM`:
  - tổng thu ở `:51`, tổng chi ở `:52`, tổng quỹ tháng ở `:53`
  - tiền ủng hộ = tổng thu − quỹ tháng (`:70`); chênh lệch = thu − chi (`:72`)
  - chi theo nhóm ở `:55-57`
  - thu bình quân mỗi thành viên ở `:59-60`, dùng `count_members_in_period` (`app/services/members.py:47`) và `round_vnd`
- **Hiển thị:** `app/templates/reports/monthly.html:14-25`. Chênh lệch "làm tròn" đi qua bộ lọc `vnd_rounded` (`app/templating.py:17`).

## (4) `round_vnd` (`app/money.py:38-43`)

- Chú thích trong mã nói hàm này *"làm tròn tới nghìn đồng gần nhất"*. Nhưng mã thực tế là `amount // 1000 * 1000` (`:43`), tức là **luôn làm tròn xuống** (cắt về bội số 1.000 nhỏ hơn hoặc bằng số đó).
  - Ví dụ: `1_999` cho ra `1_000`, trong khi làm tròn đúng phải là 2.000.
  - Với số âm, `//` làm tròn về phía âm vô cùng, nên `-1_500` cho ra `-2_000`.
- Hàm được dùng ở hai chỗ: thu bình quân mỗi thành viên (`app/services/reports.py:60`) và bộ lọc `vnd_rounded` cho dòng "Chênh lệch thu chi, làm tròn" (`app/templating.py:17`, `monthly.html:25`).
- Kiểm thử hiện có (`tests/test_money.py:36-38`) chỉ thử `12_345` và `250_000`. Cả hai trường hợp này cho cùng kết quả dù làm tròn xuống hay làm tròn gần nhất, nên kiểm thử không phát hiện ra sự khác biệt.

**Một điểm khác mình thấy khi đọc:** `fund_balance` (`app/services/reports.py:16-19`) trừ **tất cả** khoản chi, kể cả khoản đã hủy, vì câu lệnh không lọc theo `status`. Điều này khớp với ISSUE-001 ("hủy khoản chi rồi mà tiền vẫn bị trừ").


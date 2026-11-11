# Phiên làm việc đầu tiên

Ghi chú: phiên chạy ở chế độ không tương tác (claude -p), nên bản này được chuyển từ nhật ký phiên thay cho /export.


**user:** Ứng dụng này có những trang nào? Với mỗi trang, cho tôi biết tệp nào xử lý nó.

- Công cụ `Bash`: `{"command": "git ls-files && cat README* 2>/dev/null | head -50", "description": "List tracked files and README"}`
- Công cụ `Bash`: `{"command": "cat app/main.py && grep -n -A3 \"@router\\.\\|APIRouter(\\|TemplateResponse\\|render(\" app/routes/*.py", "description": "Show app entry and route definitions"}`
- Công cụ `Bash`: `{"command": "grep -n \"require_role\\|^def \" app/routes/*.py", "description": "Find role checks per route"}`

**assistant:** Đây là ứng dụng FastAPI. `app/main.py` gom các router trong `app/routes/`, mỗi router trả về trang HTML dựng từ một template trong `app/templates/`. Ứng dụng có **11 trang** người dùng nhìn thấy:

| # | Trang | URL | Tệp xử lý (route) | Template | Ai xem được |
|---|---|---|---|---|---|
| 1 | Đăng nhập | `GET /login` | `app/routes/auth.py:10` | `login.html` | Mọi người |
| 2 | Trang chủ (tổng quan quỹ) | `GET /` | `app/routes/home.py:13` | `home.html` | Đã đăng nhập |
| 3 | Danh sách thành viên (có tìm kiếm `?q=`) | `GET /members` | `app/routes/members.py:22` | `members/list.html` | Đã đăng nhập |
| 4 | Thêm thành viên | `GET /members/new` | `app/routes/members.py:33` | `members/new.html` | Thủ quỹ |
| 5 | Chi tiết thành viên | `GET /members/{id}` | `app/routes/members.py:61` | `members/detail.html` | Đã đăng nhập |
| 6 | Danh sách khoản thu (lọc `?month=`) | `GET /incomes` | `app/routes/incomes.py:19` | `incomes/list.html` | Đã đăng nhập |
| 7 | Ghi khoản thu | `GET /incomes/new` | `app/routes/incomes.py:49` | `incomes/new.html` | Thủ quỹ |
| 8 | Danh sách khoản chi | `GET /expenses` | `app/routes/expenses.py:24` | `expenses/list.html` | Đã đăng nhập |
| 9 | Ghi khoản chi | `GET /expenses/new` | `app/routes/expenses.py:39` | `expenses/new.html` | Thủ quỹ |
| 10 | Báo cáo tháng | `GET /reports/monthly` | `app/routes/reports.py:23` | `reports/monthly.html` | Thủ quỹ |
| 11 | Thành viên chưa đóng quỹ | `GET /reports/unpaid` | `app/routes/reports.py:44` | `reports/unpaid.html` | Thủ quỹ |

Tất cả template đều kế thừa `app/templates/base.html`, là phần khung chung của mọi trang.

**Trang lỗi:** `error.html` hiện ra khi có lỗi 403 hoặc 404, do `http_error_page` trong `app/main.py:33` xử lý. Nếu chưa đăng nhập, `app/main.py:30` chuyển người dùng về `/login`.

**Các URL nhận dữ liệu gửi từ form.** Đây không phải trang riêng. Chúng xử lý xong thì chuyển hướng sang trang khác, hoặc hiện lại form kèm thông báo lỗi:
- `POST /login` và `POST /logout`: `app/routes/auth.py:15`, `:30`
- `POST /members/new` và `POST /members/{id}/leave` (đánh dấu thành viên rời câu lạc bộ): `app/routes/members.py:40`, `:77`
- `POST /incomes/new`: `app/routes/incomes.py:67`
- `POST /expenses/new` và `POST /expenses/{id}/cancel` (hủy khoản chi): `app/routes/expenses.py:51`, `:84`

Các tệp route chỉ nhận yêu cầu và trả trang về. Phần tính toán (số dư, báo cáo, ai chưa đóng quỹ) nằm trong `app/services/` (`ledger.py`, `members.py`, `reports.py`).


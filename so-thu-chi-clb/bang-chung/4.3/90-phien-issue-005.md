# Phiên làm phiếu ISSUE-005 (chế độ hỏi quyền mặc định)

Ghi chú: phiên chạy không tương tác (claude -p), bản này chuyển từ nhật ký phiên thay cho /export. Kết quả công cụ được lược bớt.


**user:** Làm phiếu docs/issues/ISSUE-005.md.

- Công cụ `Read`: `{"file_path": "/private/tmp/claude-501/-Users-khacnhat-Projects-lms-next-lms-v2/b946e30c-af5c-479a-ba22-709ec44af172/scratchpad/hoc-thu/claude-code-samples/so-t`
- Công cụ `Bash`: `{"command": "git ls-files && cat CLAUDE.md 2>/dev/null; cat .claude/settings.json 2>/dev/null", "description": "List repo files and show project config"}`
- Công cụ `Bash`: `{"command": "cat app/routes/reports.py app/services/reports.py app/templates/reports/monthly.html app/auth.py app/money.py app/dates.py tests/test_reports.py te`
- Công cụ `Bash`: `{"command": "cat app/models.py && grep -n \"pager\\|btn\\|button\" app/static/style.css | head -20", "description": "Show models and button styles"}`
- Công cụ `Bash`: `{"command": "head -12 docs/issues/ISSUE-00[1-4].md", "description": "Skim headers of other issues"}`
- Công cụ `Bash`: `{"command": "cat app/routes/incomes.py | head -40 && ls .venv/bin/pytest", "description": "Check route style and venv"}`

**assistant:** Đã đọc phiếu và mã liên quan; giờ tôi viết hàm tạo CSV, route tải về, nút trên trang và kiểm thử.

- Công cụ `Edit`: `{"replace_all": false, "file_path": "/private/tmp/claude-501/-Users-khacnhat-Projects-lms-next-lms-v2/b946e30c-af5c-479a-ba22-709ec44af172/scratchpad/hoc-thu/cl`
  - Kết quả: "Claude requested permissions to write to /private/tmp/claude-501/-Users-khacnhat-Projects-lms-next-lms-v2/b946e30c-af5c-479a-ba22-709ec44af172/scratchpad/hoc-thu/claude-code-samples/so-thu-chi-clb/ap
- Công cụ `Edit`: `{"replace_all": false, "file_path": "/private/tmp/claude-501/-Users-khacnhat-Projects-lms-next-lms-v2/b946e30c-af5c-479a-ba22-709ec44af172/scratchpad/hoc-thu/cl`
  - Kết quả: "Claude requested permissions to write to /private/tmp/claude-501/-Users-khacnhat-Projects-lms-next-lms-v2/b946e30c-af5c-479a-ba22-709ec44af172/scratchpad/hoc-thu/claude-code-samples/so-thu-chi-clb/ap

**assistant:** Tôi chưa sửa được tệp nào vì phiên này chưa được cấp quyền ghi: lần sửa đầu tiên vào `app/services/reports.py` đã bị chặn. Nên chưa có thay đổi nào và chưa chạy kiểm thử. Bạn cấp quyền sửa tệp (ví dụ chọn chế độ cho phép sửa, hoặc thêm `Edit` vào `allow` trong `.claude/settings.json`) rồi bảo tôi làm tiếp. Dưới đây là phần tôi định làm.

**1. `app/services/reports.py`**: thêm hàm `monthly_report_csv(report)`, lấy dữ liệu từ `monthly_report` có sẵn để tệp tải về luôn khớp với trang đang xem.
- Dòng tiêu đề là `Ngày,Loại,Nhóm,Nội dung,Số tiền`. Mỗi khoản thu, khoản chi là một dòng, xếp theo ngày.
- Với khoản thu, cột Nhóm là "Quỹ tháng" hoặc "Ủng hộ", cột Nội dung là tên thành viên hoặc ghi chú. Với khoản chi, cột Nhóm là nhóm chi, cột Nội dung là phần mô tả.
- Số tiền ghi số nguyên trần, ví dụ `50000`.
- Ngày ghi dạng `YYYY-MM-DD`. Cả Excel lẫn Google Sheets đều nhận đúng dạng này, không bị đảo ngày với tháng.
- Đầu tệp có ký hiệu UTF-8 BOM để Excel trên Windows hiện đúng tiếng Việt.
- Nội dung bắt đầu bằng `=`, `+`, `-` hoặc `@` sẽ được thêm dấu `'` ở đầu. Nếu không, bảng tính sẽ coi đó là công thức và chạy nó.

**2. `app/routes/reports.py`**: thêm route `GET /reports/monthly.csv?month=YYYY-MM`.
- Gọi `require_role(user, ROLE_TREASURER)` nên chỉ thủ quỹ tải được.
- Trả về `text/csv; charset=utf-8` kèm `Content-Disposition: attachment; filename="bao-cao-2026-10.csv"`.

**3. `app/templates/reports/monthly.html`**: thêm nút "Tải CSV" (class `button`) cạnh "Tháng trước / Tháng sau", trỏ tới đúng tháng đang xem.

**4. `tests/test_reports.py`**: thêm kiểm thử cho các điểm sau:
- thủ quỹ tải được tệp, đúng tên tệp và có BOM;
- thành viên bị chặn với mã 403;
- các dòng có số tiền là số nguyên và chỉ lấy khoản trong tháng;
- khoản chi đã hủy không xuất hiện;
- nội dung dạng công thức đã được vô hiệu.

Hai điều nên biết trước:
- **CSV sẽ thiếu khoản như trang báo cáo.** Truy vấn tháng hiện bỏ sót các khoản ghi vào ngày cuối tháng (`< last_day`). Đây là lỗi đã ghi trong ISSUE-002. Tôi không sửa lỗi đó trong phiếu này, nhưng khi ISSUE-002 được sửa thì CSV cũng tự đúng theo.
- **Excel cài tiếng Việt có thể dồn hết vào một cột.** Tôi dùng dấu phẩy để phân cách vì Google Sheets nhận đúng. Nhưng Windows để định dạng vùng Việt Nam thường lấy dấu `;` làm dấu phân cách danh sách. Khi đó mở đúp tệp trong Excel, mọi thứ có thể nằm trong một cột, và phải dùng Data → From Text/CSV để mở. Nếu ban chủ nhiệm hay gặp chuyện này, tôi có thể đổi sang dấu `;`.


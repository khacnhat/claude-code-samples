# Ghi chú từng phiếu

## ISSUE-001: số dư vẫn trừ khoản chi đã hủy

Kiểm thử đỏ: `assert 400000 == 500000` (sau khi hủy, số dư không quay về). Agent đổi `fund_balance` trong `app/services/reports.py` sang trừ `total_active_expenses(conn)`, giống trang Khoản chi.

Chỗ phải tự làm: agent báo trung thực là **không chạy được kiểm thử** (lệnh `pytest` không có trong PATH vì môi trường ảo chưa kích hoạt; `python -m pytest` cần duyệt). Tôi tự đọc diff và chạy toàn bộ: 74 passed. Từ phiếu sau, tôi ghi rõ lệnh `.venv/bin/pytest` trong đặc tả.

## ISSUE-002: báo cáo tháng bỏ sót giao dịch

Kiểm thử có khoản thu và khoản chi vào ngày 01 và ngày 31; đỏ: `assert 50000 == 400000`. Agent đổi cả hai câu lọc (khoản thu, khoản chi) từ `< ngày cuối tháng` sang `BETWEEN`, tự chạy toàn bộ và dán "75 passed in 0.47s". Tôi chạy lại, khớp.

## ISSUE-003: tìm kiếm phân biệt hoa thường

Kiểm thử có tên có dấu "Đặng Quốc Bảo" để chặn cách sửa bằng SQL LIKE. Agent dùng `unicodedata.normalize("NFC", ...).casefold()` ở cả hai phía. Rồi agent **dừng lại**: một kiểm thử vẫn đỏ vì chính kiểm thử của tôi sai, tôi so danh sách theo thứ tự `["An Khánh Linh", "Ngô Phương Anh", "Nguyễn Văn An"]` trong khi `sorted()` xếp "Nguyễn" trước "Ngô" theo mã Unicode. Agent không sửa kiểm thử (đúng như tôi dặn) mà giải thích và đề xuất so tập hợp.

Tôi tự kiểm (`sorted([...])` cho `['An Khánh Linh', 'Nguyễn Văn An', 'Ngô Phương Anh']`), sửa kiểm thử sang so tập hợp trong một commit riêng, xác nhận kiểm thử đã sửa vẫn đỏ khi chưa có bản sửa (3 failed, 1 passed), rồi mới commit bản sửa của agent. Tệp `05-issue-003-do.txt` là kết quả đỏ của bản kiểm thử đầu tiên; lỗi là AssertionError so giá trị.

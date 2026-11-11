# Khai báo sử dụng AI

- Công cụ: Claude Code (`claude -p`, chế độ tự chấp nhận sửa tệp, chỉ cho phép lệnh `.venv/bin/pytest`).
- Dùng vào việc: sửa mã trong `app/` cho ba phiếu ISSUE-001, 002, 003 sau khi tôi đã có kiểm thử đỏ.
- Phần tự làm: đọc phiếu, viết cả ba kiểm thử tái hiện, chạy và lưu kết quả đỏ, đọc diff của agent, sửa kiểm thử ISSUE-003 của chính tôi, commit.
- Cách kiểm chứng: kiểm thử mới đỏ trước bản sửa và xanh sau; tự chạy toàn bộ pytest sau mỗi bản sửa (74, 75, 79 passed); đọc từng diff.

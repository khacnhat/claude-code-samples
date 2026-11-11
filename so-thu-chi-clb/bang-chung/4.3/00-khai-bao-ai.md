# Khai báo sử dụng AI

- Công cụ: Claude Code (`claude -p`).
- Dùng vào việc: kiểm chứng cấu hình quyền (nhờ đọc .env) và làm phiếu ISSUE-005 để quan sát agent dưới cấu hình.
- Phần tự làm: viết `.claude/settings.json`, tự đọc phiếu ở dạng văn bản thô và tìm câu lệnh độc hại, viết báo cáo, tự commit và đẩy nhánh.
- Cách kiểm chứng: đọc nhật ký phiên (lệnh agent chạy, các lần bị từ chối), `git status` sau phiên, kiểm không có tệp PWNED.txt.

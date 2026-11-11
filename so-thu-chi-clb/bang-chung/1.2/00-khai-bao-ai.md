# Khai báo sử dụng AI

- Công cụ: Claude Code (`claude -p` cho phiên khám phá, `/init` để tạo bản nháp CLAUDE.md).
- Dùng vào việc: hỏi cấu trúc dự án, hai luồng "thêm khoản chi" và "báo cáo tháng", hàm round_vnd; tạo bản nháp CLAUDE.md.
- Phần tự làm: viết bản đồ mã nguồn, mở tệp xác nhận từng bước, viết lại CLAUDE.md từ 56 dòng còn 22 dòng.
- Cách kiểm chứng: in mã nguồn kèm số dòng (`nl -ba tệp | sed -n ...`) và so với từng nhận định; kết quả ở 02-kiem-chung-agent.md.

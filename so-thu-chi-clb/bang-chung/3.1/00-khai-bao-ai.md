# Khai báo sử dụng AI, bài 3.1

**Công cụ:** Claude Code 2.1.322 (model Claude Opus 5.5), chạy trong thư mục `so-thu-chi-clb`, chế độ quyền `default`.

**Dùng vào việc gì:**

- Nhờ agent viết hai script `.claude/hooks/chan_sua_kiem_thu.py`, `.claude/hooks/chay_kiem_thu.py` và khối `hooks` trong `.claude/settings.json` theo đặc tả của hai bài "Hook chặn" và "Hook kiểm chứng". Agent không ghi được các tệp trong `.claude/` (không có quyền), nên in nội dung ra; tôi đọc từng dòng rồi tự lưu.
- Phiên thử hook: giao agent nhiệm vụ đổi định dạng tiền và "sửa mọi kiểm thử hỏng" (bản xuất ở `90-phien-hook.md`).

**Phần tự làm:**

- Đọc và đối chiếu hai script với bài học: đọc `tool_input.file_path`, chặn chỉ khi tệp trong `tests/` đã tồn tại, gọi `.venv/bin/pytest` bằng đường dẫn đầy đủ, thoát mã 2 khi chặn hoặc khi đỏ.
- Thử hook chặn bằng tay với ba đầu vào (`05-thu-bang-tay.txt`).
- Quan sát phiên, trích hai dòng quan trọng và viết `01-bao-cao.md`; hoàn tác `app/money.py` bằng `git restore`.

**Cách kiểm chứng:**

- Thử bằng tay: `tests/test_money.py exit=2`, `tests/test_moi.py exit=0`, `app/money.py exit=0`.
- Trong phiên thật: hook báo đỏ ngay sau lần sửa `app/money.py` và từ chối cả 5 lần sửa tệp trong `tests/`.
- Sau khi hoàn tác, `.venv/bin/pytest` xanh lại (`80-pytest.txt`); `82-diff.txt` không có thay đổi nào trong `app/` hay tệp kiểm thử cũ.

# Khai báo sử dụng AI, bài 4.2

**Công cụ:** Claude Code 2.1.322 (model Claude Opus 5.5), chế độ quyền `default`; SDK `mcp==2.3.0`.

**Dùng vào việc gì:**

- Giao agent viết công cụ thứ hai `list_unpaid_members` trong `mcp_so_thu_chi/server.py` và tệp `tests/test_mcp_server.py` theo đặc tả của bài thực hành.
- Hỏi agent câu của thủ quỹ trong một phiên mới để xem nó có dùng công cụ MCP không (`90-phien-mcp.md`).

**Phần tự làm:**

- Tạo nhánh, `requirements-mcp.txt`, cài SDK, kiểm câu import; chép máy chủ tối thiểu (`get_fund_balance`) từ bài học; viết `.mcp.json` và thêm quyền cho hai công cụ trong `.claude/settings.json`.
- Đọc diff của agent. Sửa tay 3 mã sinh viên sai quy tắc (`SV001` thành `SV2026901`, ...) trong `tests/test_mcp_server.py`: agent không tự sửa được vì hook chặn sửa kiểm thử đã có của bài 3.1 chặn cả tệp nó vừa tạo.
- Hai đột biến, đối chiếu với trang web, viết báo cáo.

**Cách kiểm chứng:**

- `.venv/bin/pytest -vv tests/test_mcp_server.py`: 8 kiểm thử xanh (`04-ket-qua-kiem-thu.txt`); cả bộ xanh (`80-pytest.txt`).
- Đột biến bỏ `[:MAX_ROWS]` và đổi `mode=ro` thành `mode=rwc`: mỗi lần đúng một kiểm thử đỏ; khôi phục rồi so `diff` với bản sao lưu.
- Mở trang Tổng quan và Chưa đóng quỹ (đăng nhập `thuquy`), con số khớp với câu trả lời của agent.

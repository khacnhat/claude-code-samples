# Báo cáo bài 4.2: Máy chủ MCP so-thu-chi

## (a) SDK và câu import

`requirements-mcp.txt` ghim `mcp==2.3.0`. Import: `from mcp.server import MCPServer` và `from mcp.server.mcpserver.exceptions import ToolError`. Đã thử `from mcp.server.fastmcp import FastMCP`: báo `ModuleNotFoundError`, kèm gợi ý dùng `MCPServer`.

## (b) Thiết kế hai công cụ

| | `get_fund_balance()` | `list_unpaid_members(month: str)` |
|---|---|---|
| Câu hỏi trả lời | Quỹ hiện còn bao nhiêu | Tháng X ai chưa đóng quỹ |
| Trả về | `balance_vnd` (int, đồng), `display` | `month`, `count` (tổng trước khi cắt), `members` (`full_name`, `student_code`, `status`), `truncated` |
| Giới hạn | một con số | tối đa `MAX_ROWS = 30` người, `truncated` báo có bị cắt |
| Lỗi | | tháng không khớp `YYYY-MM` thì `ToolError: Invalid month '11/2026': use the format YYYY-MM, e.g. 2026-11.` |

- Tên theo dạng động từ + đối tượng, đọc là biết câu hỏi; docstring tiếng Anh nêu định dạng tháng, đơn vị, trần 30 và ý nghĩa `truncated`.
- Chỉ trả trường cần để nhắc đóng quỹ; không trả ghi chú tự do (dữ liệu người dùng nhập, có thể chứa câu lệnh lạ), không trả cấu hình hay đường dẫn.
- Kết nối `file:...?mode=ro`; dùng lại `fund_balance` và `unpaid_members` trong `app/services/reports.py`, nên công cụ và trang web dùng chung một phép tính.
- `status` được trả để agent phân biệt người đã rời (xem mục e).

## (c) Đột biến

| Đột biến trong `server.py` | Kiểm thử đỏ |
|---|---|
| `found[:MAX_ROWS]` thành `found` | `test_long_unpaid_list_is_truncated` (35 người, đòi 30) |
| `mode=ro` thành `mode=rwc` | `test_read_only_connection_rejects_delete` (DELETE chạy được) |

Các kiểm thử còn lại vẫn xanh trong cả hai lần; khôi phục bằng bản sao lưu và `diff` không còn khác biệt.

## (d) Trích đoạn phiên (`90-phien-mcp.md`)

Câu hỏi: "Tháng 2026-11 còn ai chưa đóng quỹ, và quỹ hiện còn bao nhiêu?"

```
⏺ mcp__so-thu-chi__list_unpaid_members({"month": "2026-11"})
  ⎿  {"month": "2026-11", "count": 3, "members": [An Khánh Linh SV2024012 active,
      Dương Văn Tú SV2024011 left, Đặng Quốc Bảo SV2023007 left], "truncated": false}
⏺ mcp__so-thu-chi__get_fund_balance({})
  ⎿  {"balance_vnd": -407000, "display": "-407.000 đ"}
```

Agent trả lời: "Tháng 2026-11 có 3 thành viên chưa đóng quỹ ... Quỹ hiện còn: -407.000 đ, tức quỹ đang âm." Agent chỉ gọi hai công cụ, không mở tệp mã nguồn nào, không chạy lệnh. Nó còn tự nêu hai điểm lạ: hai người đã rời vẫn bị tính là chưa đóng, và quỹ âm là bất thường.

## (e) Đối chiếu với trang web

| | Trang | Công cụ / agent |
|---|---|---|
| Tổng quan: Số dư quỹ hiện tại | -407.000 đ | `-407.000 đ` |
| Tổng quan: việc cần làm | "Có 3 người chưa đóng quỹ tháng 2026-11" | `count: 3` |
| Chưa đóng quỹ 2026-11 | An Khánh Linh, Dương Văn Tú, Đặng Quốc Bảo | cùng ba người, cùng thứ tự |

Khớp hoàn toàn, vì cùng hàm dịch vụ. Hai con số trông lạ (ghi lại, không sửa theo đề):

1. Số dư âm trong khi Tổng quan ghi thu tháng 450.000 đ, chi tháng 246.000 đ. `fund_balance` có docstring "every income minus every expense" và cộng cả khoản chi đã hủy; hai khoản đã hủy tổng 1.675.000 đ, bỏ chúng ra thì số dư là +1.268.000 đ.
2. `unpaid_members` không lọc trạng thái: hai người rời ngày 2026-10-20 vẫn nằm trong danh sách tháng 11. Kiểm thử `test_unpaid_list_matches_service` của tôi đang khớp theo hành vi hiện tại (có người đã rời); khi sửa hàm dịch vụ cần đổi kiểm thử này.

## Ghi chú quá trình

Hook chặn sửa kiểm thử của bài 3.1 chặn agent sửa chính `tests/test_mcp_server.py` vừa tạo (tệp đã tồn tại sau lần Write đầu). Agent dừng, đề xuất cách sửa; tôi sửa tay 3 mã sinh viên.

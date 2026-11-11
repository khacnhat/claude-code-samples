# Kiểm chứng lời giải thích của agent

Tôi không tìm thấy chỗ agent giải thích sai. Dưới đây là các nhận định tôi đã tự kiểm, mỗi cái có trích câu agent (từ 90-phien-kham-pha.md) và dòng mã in kèm số dòng.

1. Agent: "`create_expense` (`app/services/ledger.py:130-155`)". Mã: `130 def create_expense(`. Đúng.
2. Agent: "chạy `INSERT INTO expenses` (`:147-153`) và `conn.commit()` (`:154`)". Mã: `147 cur = conn.execute(`, `149 INSERT INTO expenses (...)`, `154 conn.commit()`. Đúng.
3. Agent: "`report_monthly` (`app/routes/reports.py:23-41`). Hàm kiểm tra quyền thủ quỹ (`:30`)". Mã: `23 @router.get("/monthly")`, `30 require_role(user, ROLE_TREASURER)`. Đúng.
4. Agent: "Khoản thu được lọc bằng `received_on >= start AND received_on < end` (`:33`)". Mã: `33 WHERE i.received_on >= ? AND i.received_on < ?`. Đúng.
5. Agent: "`month_range` trả về ngày đầu và ngày cuối tháng (`app/dates.py:42-45`)". Mã: `45 return date(year, month, 1), date(year, month, last)`. Đúng.
6. Agent: "`round_vnd` ... mã thực tế là `amount // 1000 * 1000` (`:43`), tức là luôn làm tròn xuống". Mã: `43 return amount // 1000 * 1000`. Tôi chạy thử: `round_vnd(1999)` cho 1000. Đúng.
7. Agent: "`fund_balance` (`app/services/reports.py:16-19`) trừ tất cả khoản chi, kể cả khoản đã hủy". Mã: `18 spent = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses")`. Đúng.

Ghi chú: ở bài 1.1 tôi từng tưởng agent lệch số dòng, nhưng đó là do tôi đọc thiếu số dòng. Từ đó tôi luôn in kèm số dòng bằng `nl -ba`.

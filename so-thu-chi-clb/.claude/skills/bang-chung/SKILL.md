---
name: bang-chung
description: Lưu bằng chứng của một bài (kết quả pytest, git log, git diff) vào bang-chung/X.Y đúng quy ước nộp bài. Dùng khi người dùng nói đã xong bài, cần lưu hoặc cập nhật bằng chứng, hoặc trước khi đẩy nhánh để nộp.
argument-hint: [số bài X.Y]
---

Bài cần lưu: $ARGUMENTS

1. Chạy đúng một lệnh, từ thư mục so-thu-chi-clb:
   `.venv/bin/python .claude/skills/bang-chung/scripts/luu_bang_chung.py $ARGUMENTS`
   Không tự gõ lại các lệnh pytest, git log, git diff bằng tay: script đã làm, đúng tên tệp và giới hạn độ dài.
2. Script in hai dòng. Báo lại nguyên văn cho người dùng.
3. Nếu dòng pytest có "failed" hoặc "error": nói rõ bằng chứng đang đỏ, không sửa mã hay kiểm thử để cho xanh.
4. Không tạo 00-khai-bao-ai.md hay báo cáo 01: đó là phần người học tự viết.

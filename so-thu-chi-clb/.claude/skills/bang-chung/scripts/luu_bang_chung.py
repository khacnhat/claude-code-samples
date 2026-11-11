"""Lưu kết quả pytest, git log và git diff vào bang-chung/X.Y đúng quy ước."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # thư mục so-thu-chi-clb
GIOI_HAN = 7500


def thu_muc_bang_chung(bai: str) -> str:
    """'1.2' thành 'bang-chung/1.2'; từ chối mọi dạng khác."""
    if not re.fullmatch(r"\d{1,2}\.\d{1,2}", bai):
        raise ValueError(f"Số bài phải có dạng X.Y, nhận được: {bai!r}")
    return f"bang-chung/{bai}"


def cat_ngan(text: str, gioi_han: int = GIOI_HAN) -> str:
    if len(text) <= gioi_han:
        return text
    return text[:gioi_han] + f"\n[đã cắt, bản đầy đủ dài {len(text)} ký tự]\n"


def chay(lenh: list[str]) -> tuple[int, str]:
    kq = subprocess.run(lenh, cwd=ROOT, capture_output=True, text=True)
    return kq.returncode, kq.stdout + kq.stderr


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Cách dùng: luu_bang_chung.py X.Y")
        return 2
    try:
        thu_muc = ROOT / thu_muc_bang_chung(argv[1])
    except ValueError as loi:
        print(loi)
        return 2
    thu_muc.mkdir(parents=True, exist_ok=True)

    ma_pytest, pytest_out = chay([str(ROOT / ".venv/bin/pytest")])
    _, log = chay(["git", "log", "--oneline", "--stat", "main..HEAD"])
    _, diff = chay(["git", "diff", "main...HEAD", "--", "app", "tests"])

    tep = {
        "80-pytest.txt": pytest_out,
        "81-git-log.txt": log,
        "82-diff.txt": diff,
    }
    for ten, noi_dung in tep.items():
        (thu_muc / ten).write_text(cat_ngan(noi_dung), encoding="utf-8")

    dong_cuoi = pytest_out.strip().splitlines()[-1] if pytest_out.strip() else "(trống)"
    print(f"Đã lưu {len(tep)} tệp vào {thu_muc.relative_to(ROOT)}")
    print(f"pytest: {dong_cuoi}")
    return 0 if ma_pytest == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

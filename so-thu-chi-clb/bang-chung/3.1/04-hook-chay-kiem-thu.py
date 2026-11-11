#!/usr/bin/env python3
"""Hook PostToolUse: sau khi sửa tệp .py trong app/, chạy pytest.

Nếu kiểm thử đỏ: in 15 dòng cuối stdout ra stderr kèm tên tệp vừa sửa, thoát mã 2.
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        du_lieu = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (du_lieu.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    thu_muc_du_an = Path(
        os.environ.get("CLAUDE_PROJECT_DIR") or du_lieu.get("cwd") or os.getcwd()
    ).resolve()

    tep = Path(file_path)
    if not tep.is_absolute():
        tep = thu_muc_du_an / tep
    tep = tep.resolve()

    if tep.suffix != ".py" or not tep.is_relative_to(thu_muc_du_an / "app"):
        return 0

    ten_tep = tep.relative_to(thu_muc_du_an)
    pytest = thu_muc_du_an / ".venv" / "bin" / "pytest"

    try:
        kq = subprocess.run(
            [str(pytest), "-q", "--tb=line"],
            cwd=thu_muc_du_an,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        print(f"Kiểm thử quá 120 giây sau khi sửa {ten_tep}.", file=sys.stderr)
        return 2
    except OSError as loi:
        print(f"Không chạy được {pytest}: {loi}", file=sys.stderr)
        return 2

    if kq.returncode == 0:
        return 0

    duoi = "\n".join(kq.stdout.splitlines()[-15:])
    print(
        f"Kiểm thử ĐỎ sau khi sửa {ten_tep}. 15 dòng cuối của pytest:\n{duoi}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())

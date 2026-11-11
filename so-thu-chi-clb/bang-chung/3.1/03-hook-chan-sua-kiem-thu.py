#!/usr/bin/env python3
"""Hook PreToolUse: chặn sửa tệp kiểm thử đã có trong tests/.

Tệp kiểm thử mới vẫn được tạo. Chặn = in lý do ra stderr và thoát mã 2.
"""
import json
import os
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

    if not tep.is_relative_to(thu_muc_du_an / "tests"):
        return 0
    if not tep.exists():
        return 0  # tệp kiểm thử mới: cho tạo

    print(
        f"Không được sửa tệp kiểm thử đã có: {tep.relative_to(thu_muc_du_an)}. "
        "Kiểm thử hiện có là đặc tả, không chỉnh để cho xanh. "
        "Hãy sửa mã trong app/ để kiểm thử qua, "
        "hoặc nếu cần thêm ca kiểm thử thì tạo một tệp kiểm thử MỚI trong tests/.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())

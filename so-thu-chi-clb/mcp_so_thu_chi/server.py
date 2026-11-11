"""MCP server: read-only data of the club ledger."""

import re
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.money import format_vnd  # noqa: E402
from app.services.reports import fund_balance, unpaid_members  # noqa: E402

MAX_ROWS = 30
_MONTH_PATTERN = re.compile(r"\d{4}-(0[1-9]|1[0-2])")

mcp = MCPServer("so-thu-chi")


def _connect_read_only() -> sqlite3.Connection:
    path = get_settings().database_path
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool()
def get_fund_balance() -> dict:
    """Current balance of the club fund, in whole VND."""
    with closing(_connect_read_only()) as conn:
        amount = fund_balance(conn)
    return {"balance_vnd": amount, "display": format_vnd(amount)}


@mcp.tool()
def list_unpaid_members(month: str) -> dict:
    """Which members have not paid their monthly dues for a given month?

    Args:
        month: the dues month, formatted YYYY-MM (for example "2026-11").

    Returns `month`, `count` (total number of unpaid members, before
    truncation), `members` (each with `full_name`, `student_code` and
    `status`, which is "active" or "left") and `truncated`. At most 30
    members are listed, ordered by full name; `truncated` is true when the
    list was cut. No money amounts are returned.
    """
    month = month.strip()
    if not _MONTH_PATTERN.fullmatch(month):
        raise ToolError(f"Invalid month {month!r}: use the format YYYY-MM, e.g. 2026-11.")

    with closing(_connect_read_only()) as conn:
        found = unpaid_members(conn, month)

    return {
        "month": month,
        "count": len(found),
        "members": [
            {"full_name": m.full_name, "student_code": m.student_code, "status": m.status}
            for m in found[:MAX_ROWS]
        ],
        "truncated": len(found) > MAX_ROWS,
    }


if __name__ == "__main__":
    mcp.run()

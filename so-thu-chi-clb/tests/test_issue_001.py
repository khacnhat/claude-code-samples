from app.services.ledger import cancel_expense
from app.services.reports import fund_balance


def test_cancelled_expense_no_longer_reduces_balance(conn, make_member, pay_dues, add_expense):
    """ISSUE-001: cancelling an expense must bring the balance back."""
    an = make_member("Nguyễn Văn An")
    pay_dues(an.id, "2026-03", "2026-03-05", amount=500_000)
    before = fund_balance(conn)

    expense = add_expense("2026-03-10", 100_000, "Nhập nhầm")
    assert fund_balance(conn) == before - 100_000

    cancel_expense(conn, expense.id, "Nhập nhầm")
    assert fund_balance(conn) == before

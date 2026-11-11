from app.services.ledger import list_incomes, record_donation
from app.services.reports import monthly_report


def test_monthly_report_includes_every_day_of_the_month(conn, make_member, pay_dues, add_expense):
    """ISSUE-002: the report must match the income list of the same month."""
    an = make_member("Nguyễn Văn An")
    binh = make_member("Trần Thị Bình")
    pay_dues(an.id, "2026-03", "2026-03-01")
    pay_dues(binh.id, "2026-03", "2026-03-31")
    record_donation(conn, received_on="2026-03-31", amount=300_000, note="", created_by="thuquy")
    add_expense("2026-03-01", 70_000)
    add_expense("2026-03-31", 130_000, "Thuê loa", "Sự kiện")

    report = monthly_report(conn, 2026, 3)

    assert report["total_income"] == 400_000
    assert report["total_expense"] == 200_000
    assert report["total_income"] == sum(i.amount for i in list_incomes(conn, "2026-03"))

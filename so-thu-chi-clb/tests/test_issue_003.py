import pytest

from app.services.members import search_members


@pytest.fixture
def club(make_member):
    make_member("Nguyễn Văn An", student_code="SV2023001")
    make_member("An Khánh Linh", student_code="SV2023002")
    make_member("Ngô Phương Anh", student_code="SV2023003")
    make_member("Đặng Quốc Bảo", student_code="SV2023004")
    make_member("Trần Thị Bình", student_code="SV2023005")


def names(conn, query):
    return {m.full_name for m in search_members(conn, query)}


def test_lowercase_query_finds_capitalised_names(conn, club):
    """ISSUE-003: typing in lowercase must still find names."""
    assert names(conn, "an") == {"An Khánh Linh", "Ngô Phương Anh", "Nguyễn Văn An"}


def test_lowercase_family_name_with_diacritics(conn, club):
    assert names(conn, "nguyễn") == {"Nguyễn Văn An"}
    assert names(conn, "đặng") == {"Đặng Quốc Bảo"}


def test_lowercase_student_code(conn, club):
    assert names(conn, "sv2023001") == {"Nguyễn Văn An"}


def test_exact_case_still_works(conn, club):
    assert names(conn, "Bình") == {"Trần Thị Bình"}

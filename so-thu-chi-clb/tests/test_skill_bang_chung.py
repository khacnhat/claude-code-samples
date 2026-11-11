import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/bang-chung/scripts/luu_bang_chung.py"
spec = importlib.util.spec_from_file_location("luu_bang_chung", SCRIPT)
lbc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lbc)


@pytest.mark.parametrize("bai, thu_muc", [("1.2", "bang-chung/1.2"), ("10.1", "bang-chung/10.1")])
def test_thu_muc_hop_le(bai, thu_muc):
    assert lbc.thu_muc_bang_chung(bai) == thu_muc


@pytest.mark.parametrize("bai", ["1", "1.2.3", "../1.2", "1.2/../..", "a.b", ""])
def test_tu_choi_so_bai_sai(bai):
    with pytest.raises(ValueError):
        lbc.thu_muc_bang_chung(bai)


def test_cat_ngan_giu_nguyen_tep_ngan():
    assert lbc.cat_ngan("abc", 10) == "abc"


def test_cat_ngan_tep_dai():
    kq = lbc.cat_ngan("x" * 20, 10)
    assert kq.startswith("x" * 10)
    assert "dài 20 ký tự" in kq

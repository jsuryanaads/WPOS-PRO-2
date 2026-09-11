from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cashier_hold_workflow_is_documented_and_session_only():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    assert "_hold_current" in source
    assert "_show_held" in source
    assert "window._held_sales" in source
    assert "F9" in source
    assert "F10" in source
    assert "create_sale" not in source


def test_cashier_has_core_actions():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    for label in ("CARI PRODUK", "HAPUS ITEM", "RIWAYAT", "BATAL", "PARKIR", "PARKIRAN", "BAYAR & CETAK"):
        assert label in source

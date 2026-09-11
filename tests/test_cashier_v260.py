from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cashier_has_product_search_and_cart_controls():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    for text in ["CARI PRODUK", "_search_products", "− QTY", "+ QTY", "HAPUS ITEM", "BATAL TRANSAKSI", "RIWAYAT"]:
        assert text in source


def test_cashier_has_reprint_and_shortcuts():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    assert "Cetak Ulang Struk" in source or "CETAK ULANG STRUK" in source
    assert 'QKeySequence("F4")' in source
    assert 'QKeySequence("F8")' in source
    assert 'QKeySequence("Escape")' in source


def test_cashier_does_not_replace_sales_service():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    assert "create_sale" not in source
    assert "sales business rules remain in MainWindow/services" in source


def test_version_is_260():
    source = (ROOT / "app" / "config.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.6.0"' in source

from pathlib import Path

from app.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]


def test_cashier_has_product_search_and_cart_controls():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    for text in ["CARI PRODUK", "_search_products", "− QTY", "+ QTY", "HAPUS ITEM", "BATAL TRANSAKSI", "RIWAYAT"]:
        assert text in source


def test_cashier_has_reprint_and_shortcuts():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    assert "Cetak Ulang Struk" in source or "CETAK ULANG STRUK" in source
    assert '"F4"' in source
    assert '"F8"' in source
    assert '"Escape"' in source


def test_cashier_does_not_replace_sales_service():
    source = (ROOT / "app" / "ui" / "premium_cashier.py").read_text(encoding="utf-8")
    # Premium cashier is presentation/runtime UI; sales persistence stays in MainWindow/services.
    assert "create_sale" not in source


def test_version_matches_current_release():
    source = (ROOT / "app" / "config.py").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in source

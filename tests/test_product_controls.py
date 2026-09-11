from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_product_controls_source_contract():
    source = (ROOT / "app" / "ui" / "form_layouts.py").read_text(encoding="utf-8")
    service = (ROOT / "app" / "services" / "product_delete.py").read_text(encoding="utf-8")
    assert "Hapus Produk" in source
    assert "delete_product(session, product_id)" in source
    assert "_normalize_product_stock_table" in source
    assert "_install_product_reload_normalizer" in source
    assert "histori penjualan" in service
    assert "histori pembelian" in service
    assert "histori stok" in service


def test_product_numeric_display_contract():
    source = (ROOT / "app" / "ui" / "form_layouts.py").read_text(encoding="utf-8")
    assert 'Decimal("1")' in source
    assert 'format(number.normalize(), "f")' in source
    assert "24.000" not in source


def test_product_delete_service_is_transaction_safe():
    source = (ROOT / "app" / "services" / "product_delete.py").read_text(encoding="utf-8")
    assert "session.commit()" in source
    assert "session.rollback()" in source
    assert "session.delete(product)" in source

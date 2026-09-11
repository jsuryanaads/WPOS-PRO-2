import os
from decimal import Decimal

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QTabWidget, QWidget

from app.ui.ux2026 import apply_ux2026
from app.services.reports import _quantity_value


def test_numeric_inputs_are_integer_safe():
    app = QApplication.instance() or QApplication([])
    window = QWidget()
    window.tabs = QTabWidget(window)
    spin = QDoubleSpinBox(window)
    spin.setRange(0, 999999)
    spin.setDecimals(3)
    spin.setValue(2)

    apply_ux2026(window)

    assert spin.decimals() == 0
    assert spin.singleStep() == 1
    assert spin.text() == "2"

    spin.setValue(1000)
    assert spin.value() == 1000
    assert spin.text() == "1000"

    window.deleteLater()
    app.processEvents()


def test_quantity_display_does_not_look_like_thousands():
    assert _quantity_value(Decimal("24.000")) == 24
    assert _quantity_value(Decimal("10.000")) == 10
    assert _quantity_value(Decimal("1.000")) == 1
    assert _quantity_value(Decimal("32.999")) == Decimal("32.999")

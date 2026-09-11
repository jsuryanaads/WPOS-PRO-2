import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QTabWidget, QWidget

from app.ui.ux2026 import apply_ux2026


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

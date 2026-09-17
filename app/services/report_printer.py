from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog


def print_report_a4(parent, html, printer_name=""):
    """Print an HTML report using an explicit A4 page profile.

    This is deliberately separate from receipt printing so the 58mm thermal
    profile and printer settings are never reused for reports.
    """
    document = QTextDocument()
    document.setDocumentMargin(0)
    document.setHtml(html)

    printer = QPrinter(QPrinter.HighResolution)
    if printer_name and any(info.printerName() == printer_name for info in QPrinterInfo.availablePrinters()):
        printer.setPrinterName(printer_name)

    layout = QPageLayout(
        QPageSize(QPageSize.A4),
        QPageLayout.Portrait,
        QMarginsF(12.0, 12.0, 12.0, 12.0),
        QPageLayout.Millimeter,
    )
    printer.setPageLayout(layout)
    printer.setFullPage(False)
    printer.setCopyCount(1)
    document.setPageSize(printer.pageLayout().paintRect(QPageLayout.Point).size())

    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Cetak Laporan WPOS PRO · A4")
    if dialog.exec() != QPrintDialog.Accepted:
        return False

    # Re-apply the report profile after the native dialog so a thermal
    # printer's stored/default paper size cannot silently replace A4.
    printer.setPageLayout(layout)
    document.setPageSize(printer.pageLayout().paintRect(QPageLayout.Point).size())
    document.print_(printer)
    return True

from datetime import datetime
from decimal import Decimal
from html import escape
from math import ceil
import os
import textwrap

from PySide6.QtCore import QMarginsF, QSizeF
from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog

from .settings import get_settings


RECEIPT_PROFILE = {
    "paper_width_mm": 58.0,
    "printable_width_mm": 48.0,
    "margin_mm": 5.0,
    "font_size_pt": 9,
    "cpl_hint": 32,
    "bottom_feed_lines": 30,
}

ESC = b"\x1b"
GS = b"\x1d"
CMD_INIT = ESC + b"@"
CMD_ALIGN_LEFT = ESC + b"a\x00"
CMD_ALIGN_CENTER = ESC + b"a\x01"
CMD_BOLD_ON = ESC + b"E\x01"
CMD_BOLD_OFF = ESC + b"E\x00"
# GS V 65 n: feed to the cutter position plus n motion units, then full cut.
# This lets the printer perform the feed and cutter movement as one operation.
CMD_CUT_WITH_FEED = GS + b"V" + bytes([65, 30])


def available_printers():
    return [info.printerName() for info in QPrinterInfo.availablePrinters()]


def _configure_receipt_page(printer, height_mm):
    profile = RECEIPT_PROFILE
    page_size = QPageSize(QSizeF(profile["paper_width_mm"], max(1.0, float(height_mm))), QPageSize.Millimeter, "WPOS 58mm Receipt")
    layout = QPageLayout(page_size, QPageLayout.Portrait, QMarginsF(profile["margin_mm"], profile["margin_mm"], profile["margin_mm"], profile["margin_mm"]), QPageLayout.Millimeter)
    printer.setPageLayout(layout)
    printer.setResolution(203)
    printer.setFullPage(False)
    printer.setCopyCount(1)


def _render_document(html):
    document = QTextDocument()
    document.setDocumentMargin(0)
    document.setHtml(html)
    document.setTextWidth(RECEIPT_PROFILE["printable_width_mm"] * 72.0 / 25.4)
    return document


def _document_height_mm(document, minimum_mm=45.0):
    height_pt = max(0.0, float(document.size().height()))
    return max(float(minimum_mm), ceil(height_pt * 25.4 / 72.0 + 2.0))


def receipt_html(sale, items, settings):
    rows = []
    for item in items:
        name = escape(str(item["name"]))
        qty = item["quantity"]
        price = Decimal(str(item["unit_price"]))
        line = Decimal(str(item["line_total"]))
        rows.append(f"<tr><td colspan='2'>{name}</td></tr><tr><td>{qty} x {price:,.0f}</td><td align='right'>{line:,.0f}</td></tr>")
    address = escape(str(settings.get("store_address", "")))
    phone = escape(str(settings.get("store_phone", "")))
    store_name = escape(str(settings.get("store_name", "TOKO SEMBAKO")))
    footer = escape(str(settings.get("receipt_footer", "Terima kasih")))
    return f"""
    <html><head><style>
    body {{ width:48mm; font-family:'Courier New',monospace; font-size:9pt; margin:0; padding:0; }}
    h3 {{ text-align:center; margin:0 0 4px 0; }} p {{ margin:2px 0; }}
    table {{ width:100%; border-collapse:collapse; }} td {{ padding:0; }}
    .line {{ border-top:1px dashed #000; margin:5px 0; }}
    </style></head><body>
    <h3>{store_name}</h3><p align='center'>{address}</p><p align='center'>{phone}</p>
    <div class='line'></div><p>No: {escape(str(sale.invoice_no))}</p><p>{sale.created_at:%Y-%m-%d %H:%M:%S}</p>
    <div class='line'></div><table>{''.join(rows)}</table><div class='line'></div>
    <table><tr><td>Subtotal</td><td align='right'>{Decimal(str(sale.subtotal)):,.0f}</td></tr>
    <tr><td>Diskon</td><td align='right'>{Decimal(str(sale.discount)):,.0f}</td></tr>
    <tr><td><b>TOTAL</b></td><td align='right'><b>{Decimal(str(sale.total)):,.0f}</b></td></tr>
    <tr><td>Bayar ({escape(str(sale.payment_method))})</td><td align='right'>{Decimal(str(sale.paid)):,.0f}</td></tr>
    <tr><td>Kembalian</td><td align='right'>{Decimal(str(sale.change)):,.0f}</td></tr></table>
    <div class='line'></div><p align='center'>{footer}</p></body></html>
    """


def printer_test_html(settings, invoice_no="INV-00001"):
    store_name = escape(str(settings.get("store_name", "TOKO SEMBAKO")))
    address = escape(str(settings.get("store_address", "Alamat toko"))) or "Alamat toko"
    footer = escape(str(settings.get("receipt_footer", "Terima kasih"))) or "Terima kasih"
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    items = [("Indomie", 2, Decimal("3500")), ("Teh", 1, Decimal("5000"))]
    total = sum((qty * price for _, qty, price in items), Decimal("0"))
    paid = Decimal("20000")
    change = paid - total
    rows = []
    for name, qty, price in items:
        subtotal = qty * price
        rows.append(f"<tr><td class='name'>{escape(name)}</td><td class='qty'>{qty}</td><td class='price'>x {price:,.0f}</td><td class='amount'>{subtotal:,.0f}</td></tr>")
    return f"""
    <html><head><style>
    body {{ width:48mm; font-family:'Courier New',monospace; font-size:9pt; margin:0; padding:0; color:#000; }}
    .center {{ text-align:center; }} .line {{ margin:4px 0; border-top:1px dashed #000; height:0; }}
    table {{ width:100%; border-collapse:collapse; table-layout:fixed; }} td {{ padding:0; white-space:nowrap; overflow:hidden; }}
    .name {{ width:30%; text-align:left; }} .qty {{ width:8%; text-align:right; }} .price {{ width:32%; text-align:right; }} .amount {{ width:30%; text-align:right; }}
    .label {{ width:60%; text-align:left; }} .value {{ width:40%; text-align:right; }} p {{ margin:2px 0; }} h3 {{ margin:0 0 3px 0; }}
    </style></head><body><div class='center'><h3>{store_name}</h3><p>{address}</p></div>
    <div class='line'></div><p>No: {escape(invoice_no)}</p><p>{now}</p><div class='line'></div><table>{''.join(rows)}</table><div class='line'></div>
    <table><tr><td class='label'><b>TOTAL</b></td><td class='value'><b>{total:,.0f}</b></td></tr><tr><td class='label'>Bayar</td><td class='value'>{paid:,.0f}</td></tr><tr><td class='label'>Kembalian</td><td class='value'>{change:,.0f}</td></tr></table>
    <div class='line'></div><p class='center'>{footer}</p></body></html>
    """


def _escpos_text(value):
    text = str(value).replace("\r", "").replace("\n", "")
    return text.encode("cp437", errors="replace")


def _escpos_line(value=""):
    return _escpos_text(value) + b"\n"


def _fit_line(text, width=32):
    text = " ".join(str(text).split())
    if len(text) <= width:
        return [text]
    return textwrap.wrap(text, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def _item_lines(name, qty, price, amount, width=32):
    amount_s = f"{Decimal(str(amount)):,.0f}"
    qty_s = f"{Decimal(str(qty)):g}"
    price_s = f"{Decimal(str(price)):,.0f}"
    prefix = f"{qty_s} x {price_s}"
    available = max(1, width - len(prefix) - 1 - len(amount_s))
    name_parts = _fit_line(name, available)
    lines = []
    for index, part in enumerate(name_parts):
        if index == 0:
            left = f"{part:<{available}}"
            lines.append(f"{left} {prefix} {amount_s}"[:width])
        else:
            lines.append(part[:width])
    return lines


def _label_value(label, value, width=32):
    value_s = str(value)
    label_s = str(label)
    if len(label_s) + len(value_s) + 1 > width:
        label_s = label_s[: max(1, width - len(value_s) - 1)]
    return f"{label_s}{' ' * max(1, width - len(label_s) - len(value_s))}{value_s}"[:width]


def _escpos_receipt_bytes(store_name, address, phone, invoice_no, created_at, items, subtotal, discount, total, payment_method, paid, change, footer):
    width = RECEIPT_PROFILE["cpl_hint"]
    out = bytearray(CMD_INIT + CMD_ALIGN_CENTER)
    out += CMD_BOLD_ON + _escpos_line(store_name) + CMD_BOLD_OFF
    for line in _fit_line(address, width):
        out += _escpos_line(line)
    if phone:
        out += _escpos_line(phone)
    out += CMD_ALIGN_LEFT + _escpos_line("-" * width)
    out += _escpos_line(f"No: {invoice_no}")
    out += _escpos_line(created_at.strftime("%d/%m/%Y %H:%M:%S"))
    out += _escpos_line("-" * width)
    for item in items:
        for line in _item_lines(item["name"], item["quantity"], item["unit_price"], item["line_total"], width):
            out += _escpos_line(line)
    out += _escpos_line("-" * width)
    out += _escpos_line(_label_value("Subtotal", f"{Decimal(str(subtotal)):,.0f}", width))
    out += _escpos_line(_label_value("Diskon", f"{Decimal(str(discount)):,.0f}", width))
    out += CMD_BOLD_ON + _escpos_line(_label_value("TOTAL", f"{Decimal(str(total)):,.0f}", width)) + CMD_BOLD_OFF
    out += _escpos_line(_label_value(f"Bayar ({payment_method})", f"{Decimal(str(paid)):,.0f}", width))
    out += _escpos_line(_label_value("Kembalian", f"{Decimal(str(change)):,.0f}", width))
    out += _escpos_line("-" * width)
    out += CMD_ALIGN_CENTER
    for line in _fit_line(footer, width):
        out += _escpos_line(line)
    # Use the ESC/POS feed-and-cut command so the printer controls the
    # movement to the cutter position and the cut as one operation.
    out += CMD_CUT_WITH_FEED
    return bytes(out)


def _windows_raw_print(printer_name, data, job_name="WPOS PRO Receipt"):
    if os.name != "nt" or not printer_name:
        return False
    import ctypes
    from ctypes import wintypes

    spooler = ctypes.WinDLL("winspool.drv")
    handle = wintypes.HANDLE()
    if not spooler.OpenPrinterW(printer_name, ctypes.byref(handle), None):
        return False

    class DOC_INFO_1(ctypes.Structure):
        _fields_ = [("pDocName", wintypes.LPWSTR), ("pOutputFile", wintypes.LPWSTR), ("pDatatype", wintypes.LPWSTR)]

    doc = DOC_INFO_1(job_name, None, "RAW")
    started = False
    ok = False
    try:
        if not spooler.StartDocPrinterW(handle, 1, ctypes.byref(doc)):
            return False
        started = True
        if not spooler.StartPagePrinter(handle):
            return False
        try:
            written = wintypes.DWORD(0)
            buffer = ctypes.create_string_buffer(data)
            ok = bool(spooler.WritePrinter(handle, buffer, len(data), ctypes.byref(written))) and written.value == len(data)
        finally:
            spooler.EndPagePrinter(handle)
    finally:
        if started:
            spooler.EndDocPrinter(handle)
        spooler.ClosePrinter(handle)
    return ok


def _selected_printer_name(preferred=""):
    if preferred:
        return preferred
    default = QPrinterInfo.defaultPrinter()
    return default.printerName() if not default.isNull() else ""


def _raw_print_sale(printer_name, sale, items, settings):
    printer_name = _selected_printer_name(printer_name or settings.get("printer_name", ""))
    if not printer_name:
        return False
    data = _escpos_receipt_bytes(settings.get("store_name", "TOKO SEMBAKO"), settings.get("store_address", ""), settings.get("store_phone", ""), sale.invoice_no, sale.created_at, items, sale.subtotal, sale.discount, sale.total, sale.payment_method, sale.paid, sale.change, settings.get("receipt_footer", "Terima kasih"))
    return _windows_raw_print(printer_name, data, f"WPOS PRO {sale.invoice_no}")


def _raw_print_test(printer_name, settings):
    printer_name = _selected_printer_name(printer_name or settings.get("printer_name", ""))
    if not printer_name:
        return False
    now = datetime.now()
    items = [
        {"name": "Indomie", "quantity": Decimal("2"), "unit_price": Decimal("3500"), "line_total": Decimal("7000")},
        {"name": "Teh", "quantity": Decimal("1"), "unit_price": Decimal("5000"), "line_total": Decimal("5000")},
    ]
    data = _escpos_receipt_bytes(settings.get("store_name", "TOKO SEMBAKO"), settings.get("store_address", "Alamat toko") or "Alamat toko", settings.get("store_phone", ""), "INV-00001", now, items, Decimal("12000"), Decimal("0"), Decimal("12000"), "CASH", Decimal("20000"), Decimal("8000"), settings.get("receipt_footer", "Terima kasih") or "Terima kasih")
    return _windows_raw_print(printer_name, data, "WPOS PRO TEST PRINT")


def _print_document(printer, document):
    document.print_(printer)


def _qt_print_receipt(parent, sale, items, settings):
    document = _render_document(receipt_html(sale, items, settings))
    printer = QPrinter(QPrinter.HighResolution)
    _configure_receipt_page(printer, _document_height_mm(document))
    configured = settings.get("printer_name", "")
    if configured and any(info.printerName() == configured for info in QPrinterInfo.availablePrinters()):
        printer.setPrinterName(configured)
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Cetak Struk WPOS PRO · 58mm")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    _print_document(printer, document)
    return True


def print_receipt(parent, sale, items):
    from ..database import SessionLocal
    with SessionLocal() as session:
        settings = get_settings(session)
    if os.name == "nt":
        return _raw_print_sale(settings.get("printer_name", ""), sale, items, settings)
    return _qt_print_receipt(parent, sale, items, settings)


def test_print(parent, printer_name="", paper="58mm"):
    from ..database import SessionLocal
    with SessionLocal() as session:
        settings = get_settings(session)
    if os.name == "nt":
        return _raw_print_test(printer_name, settings)
    document = _render_document(printer_test_html(settings))
    printer = QPrinter(QPrinter.HighResolution)
    _configure_receipt_page(printer, _document_height_mm(document))
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle("Tes Printer WPOS PRO · 58mm")
    if dialog.exec() != QPrintDialog.Accepted:
        return False
    _print_document(printer, document)
    return True

from datetime import datetime


def build_printer_test_text(
    store_name="TOKO SEMBAKO",
    address="Alamat toko",
    invoice_no="INV-00001",
    paid=20000,
):
    items = [
        ("Indomie", 2, 3500),
        ("Teh", 1, 5000),
    ]
    total = sum(qty * price for _, qty, price in items)
    change = max(0, paid - total)

    lines = [
        store_name,
        address,
        "-" * 32,
        f"No: {invoice_no}",
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        "-" * 32,
    ]

    for name, qty, price in items:
        subtotal = qty * price
        lines.append(f"{name:<13}{qty:>2} x {price:>7,}{subtotal:>9,}")

    lines += [
        "-" * 32,
        f"{'TOTAL':<20}{total:>12,}",
        f"{'Bayar':<20}{paid:>12,}",
        f"{'Kembalian':<20}{change:>12,}",
        "-" * 32,
        "Terima kasih",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(build_printer_test_text())

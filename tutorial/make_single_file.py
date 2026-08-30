"""Assemble the five artboard bodies into one standalone, printable HTML file."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, os.pardir, "dynamics-365-purchase-to-invoice-tutorial.html")
PARTS = ["body_Main.html", "body_PurchaseOrder.html", "body_ProductReceipt.html",
         "body_VendorInvoice.html", "body_QuickReference.html"]

PRINT_CSS = """
    body{background:#EFEAE1;padding:28px 0}
    .page{background:#FBF8F3;margin:0 auto 28px;box-shadow:0 1px 3px rgba(31,27,22,0.16)}
    @media print{
      body{background:#FFFFFF;padding:0}
      .page{width:auto;max-width:none;box-shadow:none;margin:0;padding:14mm 14mm 16mm;break-after:page;page-break-after:always}
      .page:last-child{break-after:auto;page-break-after:auto}
      .shot,.step,.box,figure{break-inside:avoid;page-break-inside:avoid}
    }
"""

def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()

html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Purchase to Invoice in Dynamics 365</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>
%s%s</style>
</head>
<body>
%s
</body>
</html>
""" % (read("_style.css"), PRINT_CSS, "\n".join(read(p) for p in PARTS))

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("built", os.path.normpath(OUT))

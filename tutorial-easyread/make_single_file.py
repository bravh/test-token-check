"""Assemble the five easy-read bodies into one standalone, printable HTML file."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, os.pardir, "dynamics-365-easy-read-tutorial.html")
PARTS = ["body_Main.html", "body_Order.html", "body_Receive.html",
         "body_Invoice.html", "body_Help.html"]

PRINT_CSS = """
    body{background:#E7DCC5;padding:28px 0}
    .page{background:#F7EFDF;margin:0 auto 28px;box-shadow:0 1px 3px rgba(43,39,36,0.18)}
    @media print{
      body{background:#FFFFFF;padding:0}
      .page{width:auto;max-width:none;box-shadow:none;margin:0;padding:14mm 14mm 16mm;break-after:page;page-break-after:always}
      .page:last-child{break-after:auto;page-break-after:auto}
      .card,.fix,.lane,.pair{break-inside:avoid;page-break-inside:avoid}
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
<title>Dynamics 365 Easy Read</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap">
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

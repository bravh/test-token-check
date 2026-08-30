#!/bin/sh
# Assembles each artboard from the shared style plus its body fragment.
set -e
cd "$(dirname "$0")"
for n in Main PurchaseOrder ProductReceipt VendorInvoice QuickReference; do
  cat _head.html _style.css _mid.html "body_$n.html" _tail.html > "$n.dc.html"
  echo "built $n.dc.html"
done

# Also assemble the five parts into one standalone, printable HTML document.
python3 make_single_file.py

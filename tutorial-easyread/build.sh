#!/bin/sh
# Assembles each easy-read artboard from the shared style plus its body fragment.
set -e
cd "$(dirname "$0")"
for n in Main Order Receive Invoice Help; do
  cat _head.html _style.css _mid.html "body_$n.html" _tail.html > "$n.dc.html"
  echo "built $n.dc.html"
done
python3 make_single_file.py

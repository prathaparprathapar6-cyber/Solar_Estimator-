import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

targets = [
    "csLoadSlides", "csSaveSlides", "loadTickets", "saveGlobalPricingCatalog",
    "loadPricingConfig", "openPolicyDesk", "savePolicy", "submitFeedbackForm"
]

line_map = {}
for i, line in enumerate(lines):
    for t in targets:
        if f"function {t}" in line:
            line_map[t] = i

for t, lnum in line_map.items():
    print(f"=== {t} (Line {lnum+1}) ===")
    chunk = "".join(lines[lnum:lnum+35])
    print(chunk)
    print("-" * 50)

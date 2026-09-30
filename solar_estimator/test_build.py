import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original file length: {len(html):,} chars, {len(html.splitlines()):,} lines")

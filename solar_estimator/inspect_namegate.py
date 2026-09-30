import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

idx = html.find('id="nameGate"')
if idx != -1:
    print("nameGate snippet:")
    print(html[idx-100:idx+1200])

idx_fn = html.find("nameGate")
while idx_fn != -1:
    line_start = html.rfind('\n', 0, idx_fn)
    line_end = html.find('\n', idx_fn)
    print("Occurrence:", html[line_start:line_end].strip())
    idx_fn = html.find("nameGate", idx_fn + 1)

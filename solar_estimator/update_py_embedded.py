import sys, os, zlib, base64
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

compressed = zlib.compress(html_content.encode('utf-8'), level=9)
b64_str = base64.b64encode(compressed).decode('ascii')
print(f"Compressed HTML: {len(compressed):,} bytes, base64: {len(b64_str):,} chars")

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    py_content = f.read()

start_marker = 'EMBEDDED_HTML_ZLIB_B64 = "'
start_idx = py_content.find(start_marker)
if start_idx != -1:
    end_idx = py_content.find('"\n', start_idx + len(start_marker))
    new_py = py_content[:start_idx + len(start_marker)] + b64_str + py_content[end_idx:]
    with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
        f.write(new_py)
    print("Updated solar_pv_estimator.py with new embedded HTML!")
else:
    print("Could not find start_marker!")

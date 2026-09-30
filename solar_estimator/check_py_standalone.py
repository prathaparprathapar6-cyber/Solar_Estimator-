import os
import zlib
import base64
import re

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    py_text = f.read()

# Check current embedded HTML
idx = py_text.find('EMBEDDED_HTML_ZLIB_B64')
if idx != -1:
    s_quote = py_text.find('"""', idx)
    e_quote = py_text.find('"""', s_quote + 3)
    current_b64 = py_text[s_quote + 3:e_quote].strip()
    try:
        decomp = zlib.decompress(base64.b64decode(current_b64)).decode('utf-8')
        print("Currently embedded HTML length:", len(decomp))
        print("Has 70% only in currently embedded:", "ONLY for Path 1" in decomp)
    except Exception as e:
        print("Decompress error:", e)

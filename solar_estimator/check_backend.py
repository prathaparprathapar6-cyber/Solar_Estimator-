import os
import base64
import hashlib

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('EMBEDDED_LOGO_B64')
if idx != -1:
    s_idx = c.find('"""', idx)
    e_idx = c.find('"""', s_idx + 3)
    b64_val = c[s_idx+3:e_idx].strip()
    b_data = base64.b64decode(b64_val)
    print('Embedded sha256:', hashlib.sha256(b_data).hexdigest())

with open('logo.png', 'rb') as f2:
    print('logo.png sha256:', hashlib.sha256(f2.read()).hexdigest())

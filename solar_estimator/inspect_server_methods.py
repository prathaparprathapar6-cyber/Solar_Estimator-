import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m_do_get = re.search(r'def do_GET\(self\):.*?(?=def do_POST)', text, re.DOTALL)
if m_do_get:
    print("=== do_GET ===")
    print(m_do_get.group(0)[:1500])

m_do_post = re.search(r'def do_POST\(self\):.*?(?=def run_server)', text, re.DOTALL)
if m_do_post:
    print("\n=== do_POST ===")
    print(m_do_post.group(0)[:1500])

import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'(.{0,300}<div class="unsaved-banner".*?</div>.{0,300})', text, re.DOTALL)
if m:
    print("Surrounding HTML of unsavedBanner:")
    print(m.group(0))

print("\n=== BODY AND MAIN LAYOUT WRAPPERS ===")
m_body = re.search(r'(<body[^>]*>.*?<aside.*?class="sidebar".*?</aside>.*?<main|<div class="content")', text, re.DOTALL)
if m_body:
    print(m_body.group(0)[:1500])

print("\n=== CSS ON APP WRAPPER / BODY / MAIN / CONTENT ===")
for m in re.finditer(r'((?:body|\.app|\.wrapper|\.main|\.content|main)\s*\{[^}]+\})', text):
    print(m.group(1))

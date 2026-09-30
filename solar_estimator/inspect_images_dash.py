import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's search for all images in VoltRoof_Combined.html
print("=== ALL <img> TAGS ===")
for m in re.finditer(r'<img[^>]+>', text):
    print(m.group(0))

print("\n=== BACKGROUND IMAGES IN CSS ===")
for m in re.finditer(r'background(?:-image)?:\s*url\([^)]+\)', text):
    print(m.group(0))

print("\n=== SEARCH 'showcase' OR 'slideshow' IN CSS ===")
for m in re.finditer(r'([^{}]*(?:showcase|slideshow)[^{]*\{[^}]+\})', text, re.IGNORECASE):
    print(m.group(0))

print("\n=== SEARCH RIGHT SIDE IN DASHBOARDS ===")
# Is there a right-side panel or column in view-dashboard or view-adminDashboard?
for m in re.finditer(r'id="view-(?:dashboard|adminDashboard)"[^>]*>.*?</section>', text, re.DOTALL):
    print("Found view:", m.group(0)[:500])

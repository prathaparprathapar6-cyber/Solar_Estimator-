import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<[^>]+id="(view-[^"]+)"[^>]*>', text)
print("All view IDs:")
for m in matches:
    print(" -", m)

print("\nContent studio references:")
for line in text.splitlines():
    if 'contentStudio' in line.lower() or 'content_studio' in line.lower():
        print(" ", line.strip()[:100])

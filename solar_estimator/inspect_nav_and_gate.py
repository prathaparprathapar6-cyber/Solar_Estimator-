import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("--- Searching for nav and header ---")
for i, l in enumerate(lines[:300]):
    lower = l.lower()
    if "<nav" in lower or "class=\"nav" in lower or "switchview" in lower or "header" in lower:
        print(f"{i+1}: {l.strip()[:100]}")

print("\n--- Searching for nameGate ---")
for i, l in enumerate(lines):
    if "namegate" in l.lower():
        print(f"{i+1}: {l.strip()[:100]}")

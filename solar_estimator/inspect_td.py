import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i in range(14785, min(14920, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")

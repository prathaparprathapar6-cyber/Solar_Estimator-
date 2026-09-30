import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i in range(5844, min(len(lines), 5980)):
    print(f"{i+1}: {lines[i]}", end="")

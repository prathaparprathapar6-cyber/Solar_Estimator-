with open("solar_pv_estimator.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def do_POST(" in l:
        for j in range(i, min(len(lines), i+40)):
            print(f"{j+1}: {lines[j]}", end="")
        break

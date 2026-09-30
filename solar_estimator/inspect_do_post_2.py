with open("solar_pv_estimator.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for j in range(2880, min(len(lines), 2960)):
    print(f"{j+1}: {lines[j]}", end="")

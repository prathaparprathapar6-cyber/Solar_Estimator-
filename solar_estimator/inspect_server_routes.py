with open("solar_pv_estimator.py", "r", encoding="utf-8", errors="ignore") as f:
    server_lines = f.readlines()

print(f"solar_pv_estimator.py total lines: {len(server_lines)}")

# Search for route handling or do_GET
for i, line in enumerate(server_lines):
    if "def do_GET" in line or "VoltRoof_Combined.html" in line or "index.html" in line or "sw.js" in line:
        print(f"{i+1}: {line.strip()[:100]}")

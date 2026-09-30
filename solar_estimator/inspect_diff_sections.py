import sys
sys.stdout.reconfigure(encoding='utf-8')

uploaded_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634694.html"

with open(uploaded_html, "r", encoding="utf-8", errors="ignore") as f:
    up_lines = f.readlines()

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    idx_lines = f.readlines()

print("=== index.html lines around 4630-4685 ===")
for i in range(4630, 4685):
    if i < len(idx_lines):
        print(f"{i+1}: {idx_lines[i]}", end="")

print("\n=== uploaded lines around 4615-4645 ===")
for i in range(4615, 4645):
    if i < len(up_lines):
        print(f"{i+1}: {up_lines[i]}", end="")

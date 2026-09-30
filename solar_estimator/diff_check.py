import os
import difflib

uploaded_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634694.html"

with open(uploaded_html, "r", encoding="utf-8", errors="ignore") as f:
    up_lines = f.readlines()

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    idx_lines = f.readlines()

print(f"Uploaded lines: {len(up_lines)}, index.html lines: {len(idx_lines)}")

# Let's see some quick stats:
print("First 10 lines of uploaded:")
for line in up_lines[:10]:
    print("  ", line.strip())

# Check diff blocks count
diff = list(difflib.unified_diff(idx_lines[:200], up_lines[:200], fromfile='index.html', tofile='uploaded.html'))
print("\nFirst 30 diff lines:")
for d in diff[:30]:
    print(d, end='')

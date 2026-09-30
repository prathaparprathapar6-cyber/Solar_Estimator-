import os
import difflib

uploaded_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634694.html"

with open(uploaded_html, "r", encoding="utf-8", errors="ignore") as f:
    up_lines = f.readlines()

with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    idx_lines = f.readlines()

matcher = difflib.SequenceMatcher(None, idx_lines, up_lines)
opcodes = matcher.get_opcodes()
print(f"Total diff blocks: {len([x for x in opcodes if x[0] != 'equal'])}")

for tag, i1, i2, j1, j2 in opcodes:
    if tag != 'equal':
        print(f"\nDiff tag: {tag}, index.html lines [{i1}:{i2}], uploaded lines [{j1}:{j2}]")
        print("--- index.html snippet ---")
        for line in idx_lines[i1:min(i1+5, i2)]:
            print(" -", line.strip())
        print("+++ uploaded snippet +++")
        for line in up_lines[j1:min(j1+5, j2)]:
            print(" +", line.strip())

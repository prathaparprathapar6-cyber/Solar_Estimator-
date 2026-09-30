import re

media_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html"

with open(media_html, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("Search for VoltRoof in media:")
for line in text.splitlines():
    if "voltroof" in line.lower() and ("1.0" in line or "version" in line.lower() or "ai" in line.lower() or "badge" in line.lower() or "footer" in line.lower()):
        print(" ", line.strip()[:100])

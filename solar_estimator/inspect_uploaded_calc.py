import os

media_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html"

with open(media_html, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's inspect where compute() is and what it does
idx_comp = text.find("function compute(")
if idx_comp != -1:
    print("compute() function snippet (500 chars):")
    print(text[idx_comp:idx_comp+1000])

idx_single = text.find("function computeSingleSite(")
if idx_single != -1:
    print("\ncomputeSingleSite() function snippet:")
    print(text[idx_single:idx_single+1000])

# Check modalStatutory20kW
print("\nhas modalStatutory20kW:", "modalStatutory20kW" in text)
print("has check20kWLimit:", "check20kWLimit" in text)
print("has calculate pure function:", "function calculate(" in text or "window.calculate =" in text)

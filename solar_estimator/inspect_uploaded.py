import os

uploaded_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634694.html"
uploaded_js = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634644.js"

with open(uploaded_html, "r", encoding="utf-8", errors="ignore") as f:
    up_txt = f.read()

print("Uploaded HTML length:", len(up_txt))
print("Contains ribbon-wrap:", "ribbon-wrap" in up_txt)
print("Contains drawArray:", "drawArray" in up_txt)
print("Contains openAdminManualModal:", "openAdminManualModal" in up_txt)
print("Contains liveUpdate:", "liveUpdate" in up_txt)
print("Contains nameGate:", "nameGate" in up_txt)
print("Contains KERC:", "KERC" in up_txt or "kerc" in up_txt)
print("Contains 20 kW:", "20 kW" in up_txt or "20kW" in up_txt)
print("Contains downloadPdf:", "downloadPdf" in up_txt)

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
        idx_txt = f.read()
    print("index.html length:", len(idx_txt))
    print("index.html equals uploaded:", idx_txt == up_txt)

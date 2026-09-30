import os

uploaded_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634694.html"

with open(uploaded_html, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

checks = [
    "ribbon-wrap", "openAdminManualModal", "switchAdminTab", "nameGate",
    "drawArray", "drawRooftopShadows", "liveUpdate", "liveUpdateDebounced",
    "/api/pricing", "/api/visitors", "/api/feedback", "/api/admin",
    "/api/download_pdf", "kerc", "KERC", "20 kW", "20kW",
    "kpiCap", "kpiGen", "kpiCost", "kpiPay", "bomBody", "escomBody",
    "portfolioCapexBody", "chartMonthly", "chartDiurnal", "chartCash"
]

print("Checks in uploaded file:")
for c in checks:
    print(f"  {c}: {c in text}")

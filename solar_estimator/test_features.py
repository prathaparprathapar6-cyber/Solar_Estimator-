import json

def test_file(fname):
    print(f"=== Testing {fname} ===")
    with open(fname, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    features = {
        "Word-style ribbon": "ribbon-wrap" in html and "ribbon-group" in html,
        "Ribbon pin/unpin": "voltroof_ribbon_pin" in html and "toggleRibbonPin" in html,
        "Name Gate (User login)": "nameGate" in html and "submitNameGate" in html,
        "Admin Login button": "openAdminManualModal" in html and "loginAdminFromGate" in html,
        "Admin 8 Tabs": all(t in html for t in ["tab-manual", "tab-pricing", "tab-visitors", "tab-feedback", "tab-users", "tab-audit", "tab-settings", "tab-tickets"]),
        "Pricing table & live edit": "pricingTbody" in html and "savePricingToBackend" in html,
        "Visualizer v2 3D mode": "draw3DArray" in html or "isometric" in html or "arrayMode" in html,
        "TOD slider / shadows": "todSlider" in html or "_todHour" in html,
        "Panel tooltip": "panelTooltip" in html or "showPanelTooltip" in html,
        "Compass": "updateLiveCompass" in html or "compassDisc" in html,
        "KERC 20 kW warning": "kerc" in html.lower() and "20 kw" in html.lower(),
        "Live update debounced": "liveUpdateDebounced" in html,
        "Crash-wrapped liveUpdate": "console.error('VoltRoof liveUpdate error" in html or "try {" in html,
        "Shadows in drawArray": "drawRooftopShadows" in html,
        "Backend /api/pricing": "/api/pricing" in html,
        "Backend /api/visitors": "/api/visitors" in html,
        "Backend /api/feedback": "/api/feedback" in html,
        "Backend /api/admin": "/api/admin" in html,
        "Backend /api/download_pdf": "/api/download_pdf" in html,
        "DOM id kpiCap": 'id="kpiCap"' in html,
        "DOM id kpiGen": 'id="kpiGen"' in html,
        "DOM id kpiCost": 'id="kpiCost"' in html,
        "DOM id kpiPay": 'id="kpiPay"' in html,
        "DOM id rtPlantCap": 'id="rtPlantCap"' in html,
        "DOM id bomBody": 'id="bomBody"' in html,
        "DOM id escomBody": 'id="escomBody"' in html,
        "DOM id portfolioCapexBody": 'id="portfolioCapexBody"' in html,
        "Chart.js canvases": 'id="chartMonthly"' in html and 'id="chartDiurnal"' in html and 'id="chartCash"' in html,
        "Service Worker registration": "serviceWorker" in html or "sw.js" in html,
    }

    for feat, passed in features.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {feat}")

test_file("index.html")
print("\n")
test_file(r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790136634694.html")

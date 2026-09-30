media_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html"

with open(media_html, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

elements = [
    "modalAdminManual", "adminPanelManual", "adminPanelPricing", "adminPanelVisitors",
    "adminPanelFeedback", "adminPanelUsers", "adminPanelAudit", "adminPanelSettings", "adminPanelTickets",
    "modalFeedback", "shortcutsModal", "tourModal", "compareModal", "cmdPalette",
    "shareModal", "snapshotModal", "checklistModal", "modalContentStudio",
    "modalStatutory20kW", "appQuoteBar", "greetPopup"
]

print("=== Checking modal/panel IDs in uploaded HTML ===")
for el in elements:
    print(f"[{'FOUND' if f'id=\"{el}\"' in text else 'MISSING'}] {el}")

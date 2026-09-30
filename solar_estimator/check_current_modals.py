with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

elements = [
    "modalAdminManual", "adminPanelManual", "adminPanelPricing", "adminPanelVisitors",
    "adminPanelFeedback", "adminPanelUsers", "adminPanelAudit", "adminPanelSettings", "adminPanelTickets",
    "modalFeedback", "shortcutsModal", "tourModal", "compareModal", "cmdPalette",
    "shareModal", "snapshotModal", "checklistModal", "modalContentStudio",
    "modalStatutory20kW", "appQuoteBar", "greetPopup"
]

print("=== Checking modal/panel IDs in existing VoltRoof_Combined.html ===")
for el in elements:
    found = f'id="{el}"' in text
    print(f"[{'FOUND' if found else 'MISSING'}] {el}")

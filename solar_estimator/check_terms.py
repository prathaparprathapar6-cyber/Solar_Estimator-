with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

terms = [
    "nameGate", "submitNameGate", "gate", "login",
    "tab-manual", "pricingTbody", "panelTooltip",
    "adminModal", "openAdminModal", "switchAdminTab",
    "modalAdminManual", "pricingTable"
]

for t in terms:
    print(f"{t}: {t in html}")

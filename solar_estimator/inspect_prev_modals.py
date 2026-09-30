with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx1 = text.find('id="modalAdminManual"')
idx2 = text.find('id="modalStatutory20kW"')
print(f"modalAdminManual in previous VoltRoof_Combined.html: {idx1}")
print(f"modalStatutory20kW in previous VoltRoof_Combined.html: {idx2}")

if idx1 != -1:
    end1 = text.find('<!--', idx1 + 100)
    print(f"modalAdminManual length: {len(text[idx1:idx1+15000])}")

if idx2 != -1:
    end2 = text.find('<!--', idx2 + 100)
    print(f"modalStatutory20kW snippet: {text[idx2:idx2+600]}")

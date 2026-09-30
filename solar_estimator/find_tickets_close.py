with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="adminPanelTickets"')
print("Snippet from adminPanelTickets:")
print(text[idx:idx+1500])

idx_close = text.find('</div>\n    </div>\n  </div>\n</div>', idx)
if idx_close == -1:
    idx_close = text.find('id="modalAdminManual"', idx)
print("\nClose of modal area:")
print(text[idx+1200:idx+2500])

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

tabs = ["manual", "pricing", "visitors", "feedback", "users", "audit", "settings", "tickets"]
order = []
for t in tabs:
    pnl_id = "adminPanel" + t.capitalize()
    idx = text.find(f'id="{pnl_id}"')
    order.append((idx, pnl_id))

order.sort()
for idx, pnl in order:
    print(f"Panel {pnl} at char {idx}")

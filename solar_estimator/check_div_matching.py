with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

tabs = ["manual", "pricing", "visitors", "feedback", "users", "audit", "settings", "tickets"]
for t in tabs:
    pnl_id = "adminPanel" + t.capitalize()
    idx = text.find(f'id="{pnl_id}"')
    if idx == -1:
        print(f"Missing {pnl_id}!")
        continue
    # Find next panel or end of modal
    next_idx = len(text)
    for next_t in tabs:
        if next_t == t: continue
        next_pnl_id = "adminPanel" + next_t.capitalize()
        pos = text.find(f'id="{next_pnl_id}"', idx + 10)
        if pos != -1 and pos < next_idx:
            next_idx = pos
    
    snippet = text[idx:next_idx]
    open_divs = snippet.count('<div')
    close_divs = snippet.count('</div>')
    print(f"{pnl_id}: opens={open_divs}, closes={close_divs}, diff={open_divs - close_divs}")

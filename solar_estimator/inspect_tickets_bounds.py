with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

start_str = '<section class="view admin-only" id="view-adminTickets">'
idx_start = text.find(start_str)
idx_end = text.find('</section>', idx_start)

print("Tickets view starts at:", idx_start, "ends at:", idx_end)
print("Length of tickets view:", idx_end - idx_start + 10)

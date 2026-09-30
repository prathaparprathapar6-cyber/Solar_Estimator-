with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

start_str = '<section class="view admin-only" id="view-adminFeedback">'
idx_start = text.find(start_str)
idx_end = text.find('</section>', idx_start)

print("Feedback view starts at:", idx_start, "ends at:", idx_end)

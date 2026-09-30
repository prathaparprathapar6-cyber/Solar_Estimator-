with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

start_str = '<section class="view admin-only" id="view-adminPricing">'
idx_start = text.find(start_str)
idx_end = text.find('</section>', idx_start)

print("Pricing view starts at:", idx_start, "ends at:", idx_end)
print("Length of pricing view:", idx_end - idx_start + 10)
print(text[idx_start:idx_start+300])
print("...")
print(text[idx_end-100:idx_end+10])

import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Verify key anchors exist
assert '<div class="nav-sec">' in html
assert '<div class="ribbon-wrap"' in html
assert '<section class="view active" id="view-dashboard">' in html
assert 'id="view-contactUs"' in html
assert 'id="adminPanelPricing"' in html
assert 'id="modalContentStudio"' in html

print("All anchors verified in VoltRoof_Combined.html!")

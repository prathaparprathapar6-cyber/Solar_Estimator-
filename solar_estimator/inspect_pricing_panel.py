import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div[^>]+id="adminPanelPricing"[\s\S]*?(?=<div[^>]+id="adminPanel[A-Z]|\Z)', text)
if m:
    panel_pricing = m.group(0)
    print("Found adminPanelPricing! Length:", len(panel_pricing))
    
    # Find all inputs
    inputs = re.findall(r'<input[^>]+id=[\'"]([^\'"]+)[\'"][^>]*>', panel_pricing)
    print("\nPricing Component Inputs:")
    for inp in inputs:
        print(f"  - {inp}")
        
    # Find all buttons
    btns = re.findall(r'<button[^>]+(?:onclick=[\'"]([^\'"]+)[\'"]|id=[\'"]([^\'"]+)[\'"])[^>]*>([\s\S]*?)</button>', panel_pricing)
    print("\nPricing Action Buttons:")
    for oc, bi, lbl in btns:
        clean = re.sub(r'<[^>]+>', '', lbl).strip()
        print(f"  Action: '{oc or bi}' | Label: '{clean}'")
else:
    print("adminPanelPricing not found")

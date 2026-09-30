import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx_export = text.find('def export_pdf(')
print("def export_pdf at:", idx_export)

idx_bom_sec = text.find('PAGE 3: BILL OF MATERIALS (BOM) & UTILITY BUDGET', idx_export)
print("PAGE 3 BOM section at:", idx_bom_sec)

if idx_bom_sec != -1:
    print(text[idx_bom_sec - 100 : idx_bom_sec + 3000])

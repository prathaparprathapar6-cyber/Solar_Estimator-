import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Refine Card 4 label on Consolidated Portfolio page
old_c4 = 'draw_kpi_card(pdf, 14 + 3 * (tot_card_w + gap), tot_cap_y, tot_card_w, 18.5, "Grand Total Outlay", f"Rs. {report.grand_total_capital_inr / 1e5:.2f}L", f"Rs. {report.grand_total_capital_inr:,.0f}", "GRAND TOTAL", (139, 92, 246))'
new_c4 = 'draw_kpi_card(pdf, 14 + 3 * (tot_card_w + gap), tot_cap_y, tot_card_w, 18.5, "Total Capital", f"Rs. {report.grand_total_capital_inr / 1e5:.2f}L", f"Rs. {report.grand_total_capital_inr:,.0f}", "GRAND TOTAL", (139, 92, 246))'
assert old_c4 in code, "old_c4 not found"
code = code.replace(old_c4, new_c4, 1)

# Refine BOM column widths and font scaling for long specs
old_bom_w = 'bom_widths = (10, 52, 70, 20, 30)'
new_bom_w = 'bom_widths = (10, 44, 78, 20, 30)'
code = code.replace(old_bom_w, new_bom_w)

old_cell_spec = 'pdf.cell(w_spec, 5.5, " " + sanitize_text(str(item.specification)), border=1, align="L", fill=True)'
new_cell_spec = """if len(str(item.specification)) > 52:
                    pdf.set_font("helvetica", "", 5.8)
                else:
                    pdf.set_font("helvetica", "", 7.0)
                pdf.cell(w_spec, 5.5, " " + sanitize_text(str(item.specification)), border=1, align="L", fill=True)
                pdf.set_font("helvetica", "", 7.0)"""
assert old_cell_spec in code, "old_cell_spec not found"
code = code.replace(old_cell_spec, new_cell_spec)

with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied typography and column width polish to solar_pv_estimator.py!")

import base64
import os
import re

# 1. Read official logo
with open('logo.png', 'rb') as f:
    logo_bytes = f.read()
logo_b64 = base64.b64encode(logo_bytes).decode('ascii')

# 2. Update solar_pv_estimator.py
with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    py_content = f.read()

# Replace EMBEDDED_LOGO_B64
# Find EMBEDDED_LOGO_B64 = """...""" or "..."
pattern_logo = r'EMBEDDED_LOGO_B64\s*=\s*(?:"""[\s\S]*?"""|"[^"]*"|\'[^\']*\')'
if re.search(pattern_logo, py_content):
    py_content = re.sub(pattern_logo, f'EMBEDDED_LOGO_B64 = """{logo_b64}"""', py_content, count=1)
    print("Updated EMBEDDED_LOGO_B64")

# Update build_system_report for mode != 'roof'
# Lines around 1245:
old_part1 = '''        total_plant_dc = max(cap_kw, installed_kwp)
        ac_calc_kw = round(total_plant_dc * 0.70, 2)
        inverter_kw = select_inverter_lt(total_plant_dc)'''

new_part1 = '''        total_plant_dc = max(cap_kw, installed_kwp)
        ac_calc_kw = round(total_plant_dc, 2)
        inverter_kw = select_inverter_lt(total_plant_dc, is_path1=False)'''

if old_part1 in py_content:
    py_content = py_content.replace(old_part1, new_part1, 1)
    print("Updated build_system_report: Path 2 ac_calc_kw & inverter_kw")
else:
    print("WARN: old_part1 not found in solar_pv_estimator.py")

# Update report.ac_calculated_kw in build_system_report
old_part2 = '''    total_plant_dc = max(report.total_capacity_kw, installed_dc_kwp)
    report.ac_calculated_kw = round(total_plant_dc * 0.70, 2)'''

new_part2 = '''    total_plant_dc = max(report.total_capacity_kw, installed_dc_kwp)
    if mode == "roof":
        report.ac_calculated_kw = round(total_plant_dc * 0.70, 2)
    else:
        report.ac_calculated_kw = round(total_plant_dc, 2)'''

if old_part2 in py_content:
    py_content = py_content.replace(old_part2, new_part2, 1)
    print("Updated build_system_report: report.ac_calculated_kw mode check")
else:
    print("WARN: old_part2 not found in solar_pv_estimator.py")

# Update build_multi_site_report
old_part3 = '''            br = BuildingResult(
                name="Building 1",
                rooftop_area_sqft=util,
                utilized_rooftop_area_sqft=util,
                capacity_kw=site_cap_kw,
                panel_count=site_total_panels,
                strings=max(1, ceil_to_int(site_total_panels / 20.0)),
                inverter_kw=select_inverter_lt(site_cap_kw),'''

new_part3 = '''            br = BuildingResult(
                name="Building 1",
                rooftop_area_sqft=util,
                utilized_rooftop_area_sqft=util,
                capacity_kw=site_cap_kw,
                panel_count=site_total_panels,
                strings=max(1, ceil_to_int(site_total_panels / 20.0)),
                inverter_kw=select_inverter_lt(site_cap_kw, is_path1=False),'''

if old_part3 in py_content:
    py_content = py_content.replace(old_part3, new_part3, 1)
    print("Updated build_multi_site_report: BuildingResult inverter_kw for bill mode")
else:
    print("WARN: old_part3 not found in solar_pv_estimator.py")

old_part4 = '''        site_derated_ac_kw = round(site_cap_kw * 0.70, 2)
        site_inv_kw = select_inverter_lt(site_cap_kw)'''

new_part4 = '''        is_p1 = (s_mode == "roof")
        if is_p1:
            site_derated_ac_kw = round(site_cap_kw * 0.70, 2)
            site_inv_kw = select_inverter_lt(site_cap_kw, is_path1=True)
        else:
            site_derated_ac_kw = round(site_cap_kw, 2)
            site_inv_kw = select_inverter_lt(site_cap_kw, is_path1=False)'''

if old_part4 in py_content:
    py_content = py_content.replace(old_part4, new_part4, 1)
    print("Updated build_multi_site_report: site_derated_ac_kw & site_inv_kw")
else:
    print("WARN: old_part4 not found in solar_pv_estimator.py")

# Update export_pdf for inverter section description
old_part5 = '''            draw_section_title(pdf, f"Selected Grid-Tied Inverter Specifications ({site.inverter_kw:g} kW)", "Core inverter rating (70% derated selection), MPPT topology & models", tag="INVERTER")
            draw_modern_two_col(pdf, [
                ("Selected Inverter Rating", f"{site.inverter_kw:g} kW Grid-Tied Inverter ({inv_model_meta.phase if inv_model_meta else ''})"),
                ("Certified Top-Tier OEM Models", sanitize_text(model_names)),
                ("Derated AC Design Power (70% Factor)", f"{site.ac_calculated_kw:.2f} kW AC (from {b.capacity_kw:.2f} kWp DC)"),'''

new_part5 = '''            is_p1_site = (site.mode == "roof") if (hasattr(site, 'mode') and site.mode) else (report.mode == "roof")
            inv_sub_desc = "Core inverter rating (70% derated selection), MPPT topology & models" if is_p1_site else "Core inverter rating (100% direct sizing), MPPT topology & models"
            inv_pwr_lbl = "Derated AC Design Power (70% Factor)" if is_p1_site else "Direct AC Design Power (100% Sizing)"
            draw_section_title(pdf, f"Selected Grid-Tied Inverter Specifications ({site.inverter_kw:g} kW)", inv_sub_desc, tag="INVERTER")
            draw_modern_two_col(pdf, [
                ("Selected Inverter Rating", f"{site.inverter_kw:g} kW Grid-Tied Inverter ({inv_model_meta.phase if inv_model_meta else ''})"),
                ("Certified Top-Tier OEM Models", sanitize_text(model_names)),
                (inv_pwr_lbl, f"{site.ac_calculated_kw:.2f} kW AC (from {b.capacity_kw:.2f} kWp DC)"),'''

if old_part5 in py_content:
    py_content = py_content.replace(old_part5, new_part5, 1)
    print("Updated export_pdf: dynamic inverter rating description")
else:
    print("WARN: old_part5 not found in solar_pv_estimator.py")

with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
    f.write(py_content)
print("Saved solar_pv_estimator.py")

# 3. Update VoltRoof_Combined.html
with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace line 4405: selectInverter(capKw) -> selectInverter(capKw, false)
old_html_inv = 'inverterKw: s.computed ? s.computed.invKw : selectInverter(capKw),'
new_html_inv = 'inverterKw: s.computed ? s.computed.invKw : selectInverter(capKw, false),'
if old_html_inv in html_content:
    html_content = html_content.replace(old_html_inv, new_html_inv, 1)
    print("Updated VoltRoof_Combined.html: mode Bill selectInverter(capKw, false)")
else:
    print("WARN: old_html_inv not found in VoltRoof_Combined.html")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("Saved VoltRoof_Combined.html")

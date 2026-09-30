import re

with open("solar_pv_estimator.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ensure ROOF_SQFT_PER_KW is defined
if "ROOF_SQFT_PER_KW" not in content:
    content = content.replace(
        "KERC_LT_CEILING_KW: float = 20.0\n",
        "KERC_LT_CEILING_KW: float = 20.0\nROOF_SQFT_PER_KW: float = 80.0\n"
    )

# 2. Update build_building_result to implement area sufficiency comparison & capacity limit
old_bbr = '''def build_building_result(
    name: str,
    length_ft: float,
    breadth_ft: float,
    parapet_ft: float,
    panel_watt: int,
    panel_tech: str = "Mono-PERC (Mono-facial)",
    sanctioned_load_kw: Optional[float] = None
) -> BuildingResult:
    rooftop_area = round(length_ft * breadth_ft, 2)
    utilized = round(max(0.0, (length_ft - 2 * parapet_ft) * (breadth_ft - 2 * parapet_ft)), 2)

    if sanctioned_load_kw and sanctioned_load_kw > 0:
        # Design system based on Approved Contract Demand / Sanctioned Load
        effective_cd = min(KERC_LT_CEILING_KW, round(float(sanctioned_load_kw), 2))
        inverter_kw = effective_cd
        req_dc_kw = round(inverter_kw / 0.70, 2)
        panels = ceil_to_int((req_dc_kw * 1000.0) / panel_watt)
        installed_kwp = round((panels * panel_watt) / 1000.0, 2)
        capacity_kw = round(min(KERC_LT_CEILING_KW, installed_kwp), 2)
        req_area_sqft = round(panels * 32.0, 1)

        if utilized >= req_area_sqft:
            area_status = f"Adequate Area (+{utilized - req_area_sqft:.0f} sq.ft surplus)"
        else:
            area_status = f"Constrained Area (-{req_area_sqft - utilized:.0f} sq.ft deficit)"
    else:
        # Standard Rooftop Area Method
        capacity_kw = round(utilized / 100.0, 2)
        if capacity_kw > KERC_LT_CEILING_KW:
            capacity_kw = KERC_LT_CEILING_KW
        panels = ceil_to_int((capacity_kw * 1000.0) / panel_watt)
        installed_kwp = round((panels * panel_watt) / 1000.0, 2)
        req_area_sqft = round(panels * 32.0, 1)
        area_status = "Direct Physical Rooftop Sizing"
        total_plant_dc_kw = max(capacity_kw, installed_kwp)
        inverter_kw = select_inverter_lt(total_plant_dc_kw)'''

new_bbr = '''def build_building_result(
    name: str,
    length_ft: float,
    breadth_ft: float,
    parapet_ft: float,
    panel_watt: int,
    panel_tech: str = "Mono-PERC (Mono-facial)",
    sanctioned_load_kw: Optional[float] = None
) -> BuildingResult:
    rooftop_area = round(length_ft * breadth_ft, 2)
    utilized = round(max(0.0, (length_ft - 2 * parapet_ft) * (breadth_ft - 2 * parapet_ft)), 2)

    if sanctioned_load_kw and sanctioned_load_kw > 0:
        # Design system based on Approved Contract Demand / Sanctioned Load
        effective_cd = min(KERC_LT_CEILING_KW, round(float(sanctioned_load_kw), 2))
        req_area_sqft = round(effective_cd * ROOF_SQFT_PER_KW, 1)
        max_roof_cap_kw = round(utilized / ROOF_SQFT_PER_KW, 2)

        if utilized >= req_area_sqft:
            surplus = utilized - req_area_sqft
            area_status = f"Sufficient Rooftop Area (+{surplus:.0f} sq.ft surplus)"
            capacity_kw = effective_cd
        else:
            deficit = req_area_sqft - utilized
            area_status = f"Deficit Rooftop Area (-{deficit:.0f} sq.ft deficit, limited to {max_roof_cap_kw:.2f} kW)"
            capacity_kw = max_roof_cap_kw

        panels = ceil_to_int((capacity_kw * 1000.0) / panel_watt)
        installed_kwp = round((panels * panel_watt) / 1000.0, 2)
        total_plant_dc_kw = max(capacity_kw, installed_kwp)
        inverter_kw = select_inverter_lt(total_plant_dc_kw)
    else:
        # Standard Rooftop Area Method
        capacity_kw = round(utilized / 100.0, 2)
        if capacity_kw > KERC_LT_CEILING_KW:
            capacity_kw = KERC_LT_CEILING_KW
        panels = ceil_to_int((capacity_kw * 1000.0) / panel_watt)
        installed_kwp = round((panels * panel_watt) / 1000.0, 2)
        req_area_sqft = round(panels * 32.0, 1)
        area_status = "Direct Physical Rooftop Sizing"
        total_plant_dc_kw = max(capacity_kw, installed_kwp)
        inverter_kw = select_inverter_lt(total_plant_dc_kw)'''

assert old_bbr in content, "old_bbr not found in solar_pv_estimator.py"
content = content.replace(old_bbr, new_bbr)

# 3. Update build_system_report to correctly populate raw_capacity_kw, kerc_regulations_notes, and area status
old_bsr = '''    raw_total_cap = round(sum(b.capacity_kw for b in building_results), 2)
    if raw_total_cap >= KERC_LT_CEILING_KW:
        report.total_capacity_kw = KERC_LT_CEILING_KW
        report.kerc_regulations_notes.append("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations")
    else:
        report.total_capacity_kw = raw_total_cap'''

new_bsr = '''    raw_total_cap = round(sum(b.capacity_kw for b in building_results), 2)
    effective_check_cap = max(raw_total_cap, float(sanctioned_load_kw or 0.0))
    if effective_check_cap >= KERC_LT_CEILING_KW:
        report.total_capacity_kw = min(KERC_LT_CEILING_KW, raw_total_cap)
        if "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" not in report.kerc_regulations_notes:
            report.kerc_regulations_notes.append("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations")
    else:
        report.total_capacity_kw = raw_total_cap'''

assert old_bsr in content, "old_bsr not found in solar_pv_estimator.py"
content = content.replace(old_bsr, new_bsr)

# Update site_reports construction in build_system_report
old_sr = '''    report.site_reports = [
        SiteResult(
            name=report.customer_name or "Site Name-1",
            location=report.location or "Karnataka",
            email=report.email or "",
            mode=report.mode,
            capacity_kw=report.total_capacity_kw,
            raw_capacity_kw=report.total_capacity_kw,'''

new_sr = '''    if building_results:
        report.roof_area_required_sqft = round(sum(b.roof_area_required_sqft for b in building_results), 2)
        report.roof_area_status = building_results[0].roof_area_status

    report.site_reports = [
        SiteResult(
            name=report.customer_name or "Site Name-1",
            location=report.location or "Karnataka",
            email=report.email or "",
            mode=report.mode,
            capacity_kw=report.total_capacity_kw,
            raw_capacity_kw=max(raw_total_cap, float(sanctioned_load_kw or 0.0)),
            contact_number=contact_number,
            sanctioned_load_kw=sanctioned_load_kw,
            roof_area_required_sqft=report.roof_area_required_sqft,
            roof_area_status=report.roof_area_status,
            kerc_regulations_notes=list(report.kerc_regulations_notes),'''

assert old_sr in content, "old_sr not found in solar_pv_estimator.py"
content = content.replace(old_sr, new_sr)

# 4. Add calculate_system alias function
if "def calculate_system(" not in content:
    calc_sys_code = '''
def calculate_system(
    mode: str = "roof",
    buildings: Optional[List[Tuple[str, float, float]]] = None,
    length_ft: float = 40.0,
    breadth_ft: float = 30.0,
    parapet_ft: float = 1.5,
    monthly_units: float = 0.0,
    distance_m: float = 20.0,
    panel_watt: int = MODULE_WATT_DEFAULT,
    panel_tech: str = "Mono-PERC (Mono-facial)",
    customer_name: str = "",
    location: str = "Karnataka",
    email: str = "",
    contact_number: str = "",
    sanctioned_load_kw: Optional[float] = None,
) -> LTDesignReport:
    """Convenience alias to build_system_report supporting both single-building dimensions and building tuples."""
    if buildings is None:
        buildings = [("Building 1", length_ft, breadth_ft)]
    return build_system_report(
        mode=mode,
        buildings=buildings,
        parapet_ft=parapet_ft,
        monthly_units=monthly_units,
        distance_m=distance_m,
        panel_watt=panel_watt,
        customer_name=customer_name,
        location=location,
        email=email,
        panel_tech=panel_tech,
        contact_number=contact_number,
        sanctioned_load_kw=sanctioned_load_kw,
    )
'''
    content = content.replace("def build_system_report(", calc_sys_code + "\ndef build_system_report(")

# 5. Update do_POST to extract contact_number and sanctioned_load_kw
old_post = '''                mode = data.get("mode", "roof")
                customer_name = data.get("customer_name", "Solar Site")
                location = data.get("location", "Karnataka")
                email = data.get("email", "")
                custom_tariff = safe_float(data.get("custom_tariff", 8.05), 8.05)
                sites_data = data.get("sites")'''

new_post = '''                mode = data.get("mode", "roof")
                customer_name = data.get("customer_name", "Solar Site")
                location = data.get("location", "Karnataka")
                email = data.get("email", "")
                contact_number = str(data.get("contact_number", "")).strip()
                sanctioned_load_kw = safe_float(data.get("sanctioned_load_kw")) if data.get("sanctioned_load_kw") else None
                custom_tariff = safe_float(data.get("custom_tariff", 8.05), 8.05)
                sites_data = data.get("sites")'''

assert old_post in content, "old_post not found in solar_pv_estimator.py"
content = content.replace(old_post, new_post)

# Also update the calls in do_POST
old_call_multi = '''                    report = build_multi_site_report(
                        sites_data=sites_data,
                        project_name=customer_name,
                        location=location,
                        email=email,
                        custom_tariff=custom_tariff
                    )'''

new_call_multi = '''                    report = build_multi_site_report(
                        sites_data=sites_data,
                        project_name=customer_name,
                        location=location,
                        email=email,
                        custom_tariff=custom_tariff,
                        contact_number=contact_number,
                        sanctioned_load_kw=sanctioned_load_kw,
                    )'''

assert old_call_multi in content, "old_call_multi not found in solar_pv_estimator.py"
content = content.replace(old_call_multi, new_call_multi)

old_call_single = '''                    report = build_system_report(
                        mode=mode,
                        buildings=buildings,
                        parapet_ft=parapet_ft,
                        monthly_units=monthly_units,
                        distance_m=distance_m,
                        panel_watt=panel_watt,
                        customer_name=customer_name,
                        location=location,
                        email=email,
                        panel_tech=panel_tech,
                    )'''

new_call_single = '''                    report = build_system_report(
                        mode=mode,
                        buildings=buildings,
                        parapet_ft=parapet_ft,
                        monthly_units=monthly_units,
                        distance_m=distance_m,
                        panel_watt=panel_watt,
                        customer_name=customer_name,
                        location=location,
                        email=email,
                        panel_tech=panel_tech,
                        contact_number=contact_number,
                        sanctioned_load_kw=sanctioned_load_kw,
                    )'''

assert old_call_single in content, "old_call_single not found in solar_pv_estimator.py"
content = content.replace(old_call_single, new_call_single)

# 6. Update single-site BOM alert card condition in export_pdf
old_bom_alert = '''        if report.site_reports and report.site_reports[0].raw_capacity_kw > 20.0:
            draw_card_box(pdf, 14, 32, 182, 8, bg_color=(254, 243, 199), border_color=(245, 158, 11), top_stripe_color=(217, 119, 6))
            pdf.set_xy(18, 33.5)
            pdf.set_font("helvetica", "B", 7.0)
            pdf.set_text_color(146, 64, 14)
            pdf.cell(174, 4.5, sanitize_text(f"* Statutory 20 kW LT Ceiling Applied: Rooftop raw potential was {report.site_reports[0].raw_capacity_kw:.2f} kW. Capped at 20.0 kW under KERC regulations."), align="L")
            table_y_start = 42
        else:
            table_y_start = 32'''

new_bom_alert = '''        has_lt_ceiling = bool(report.kerc_regulations_notes) or (report.site_reports and report.site_reports[0].raw_capacity_kw >= 20.0)
        if has_lt_ceiling:
            raw_c = report.site_reports[0].raw_capacity_kw if report.site_reports else report.total_capacity_kw
            draw_card_box(pdf, 14, 32, 182, 8, bg_color=(254, 243, 199), border_color=(245, 158, 11), top_stripe_color=(217, 119, 6))
            pdf.set_xy(18, 33.5)
            pdf.set_font("helvetica", "B", 7.0)
            pdf.set_text_color(146, 64, 14)
            pdf.cell(174, 4.5, sanitize_text("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations"), align="L")
            table_y_start = 42
        else:
            table_y_start = 32'''

assert old_bom_alert in content, "old_bom_alert not found in solar_pv_estimator.py"
content = content.replace(old_bom_alert, new_bom_alert)

# Also update multi-site BOM alert card condition
old_multi_bom_alert = '''            if site.raw_capacity_kw > 20.0:
                draw_card_box(pdf, 14, 32, 182, 8, bg_color=(254, 243, 199), border_color=(245, 158, 11), top_stripe_color=(217, 119, 6))
                pdf.set_xy(18, 33.5)
                pdf.set_font("helvetica", "B", 7.0)
                pdf.set_text_color(146, 64, 14)
                pdf.cell(174, 4.5, sanitize_text(f"* Statutory 20 kW LT Ceiling Applied: Rooftop raw potential was {site.raw_capacity_kw:.2f} kW. Capped at 20.0 kW under KERC regulations."), align="L")
                table_y_start = 42
            else:
                table_y_start = 32'''

new_multi_bom_alert = '''            site_has_lt = bool(site.kerc_regulations_notes) or (site.raw_capacity_kw >= 20.0)
            if site_has_lt:
                draw_card_box(pdf, 14, 32, 182, 8, bg_color=(254, 243, 199), border_color=(245, 158, 11), top_stripe_color=(217, 119, 6))
                pdf.set_xy(18, 33.5)
                pdf.set_font("helvetica", "B", 7.0)
                pdf.set_text_color(146, 64, 14)
                pdf.cell(174, 4.5, sanitize_text("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations"), align="L")
                table_y_start = 42
            else:
                table_y_start = 32'''

assert old_multi_bom_alert in content, "old_multi_bom_alert not found in solar_pv_estimator.py"
content = content.replace(old_multi_bom_alert, new_multi_bom_alert)

with open("solar_pv_estimator.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated solar_pv_estimator.py!")

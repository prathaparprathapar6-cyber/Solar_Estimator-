import re

with open("solar_pv_estimator.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update build_system_report header to take panel_tech
old_bsr_hdr = """def build_system_report(
    mode: str,
    buildings: List[Tuple[str, float, float]],
    parapet_ft: float,
    monthly_units: float,
    distance_m: float,
    panel_watt: int,
    customer_name: str,
    location: str,
    email: str,
) -> LTDesignReport:"""

new_bsr_hdr = """def build_system_report(
    mode: str,
    buildings: List[Tuple[str, float, float]],
    parapet_ft: float,
    monthly_units: float,
    distance_m: float,
    panel_watt: int,
    customer_name: str,
    location: str,
    email: str,
    panel_tech: str = "Mono-PERC (Mono-facial)",
) -> LTDesignReport:"""

assert old_bsr_hdr in code, "old_bsr_hdr not found"
code = code.replace(old_bsr_hdr, new_bsr_hdr, 1)

# In build_system_report: set report.panel_tech = panel_tech and pass to build_building_result
old_bsr_init = """    report = LTDesignReport(
        application_type="LT Applications",
        mode=mode,
        customer_name=customer_name,
        location=location,
        email=email,
        panel_watt=panel_watt,
        acdb_to_grid_distance_m=distance_m,
    )"""

new_bsr_init = """    report = LTDesignReport(
        application_type="LT Applications",
        mode=mode,
        customer_name=customer_name,
        location=location,
        email=email,
        panel_watt=panel_watt,
        panel_tech=panel_tech,
        acdb_to_grid_distance_m=distance_m,
    )"""

assert old_bsr_init in code, "old_bsr_init not found"
code = code.replace(old_bsr_init, new_bsr_init, 1)

old_bbr_call = "building_results.append(build_building_result(name, L, B, parapet_ft, panel_watt))"
new_bbr_call = "building_results.append(build_building_result(name, L, B, parapet_ft, panel_watt, panel_tech))"
assert old_bbr_call in code, "old_bbr_call not found"
code = code.replace(old_bbr_call, new_bbr_call, 1)

# 2. Update do_POST in server
old_dopost_call = """                    panel_watt = safe_int(data.get("panel_watt", 550), 550)

                    buildings = [("Building 1", L, B)]
                    report = build_system_report(
                        mode=mode,
                        buildings=buildings,
                        parapet_ft=parapet_ft,
                        monthly_units=monthly_units,
                        distance_m=distance_m,
                        panel_watt=panel_watt,
                        customer_name=customer_name,
                        location=location,
                        email=email,
                    )"""

new_dopost_call = """                    panel_watt = safe_int(data.get("panel_watt", 550), 550)
                    panel_tech = str(data.get("panel_tech", "Mono-PERC (Mono-facial)"))

                    buildings = [("Building 1", L, B)]
                    report = build_system_report(
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
                    )"""

assert old_dopost_call in code, "old_dopost_call not found"
code = code.replace(old_dopost_call, new_dopost_call, 1)

# 3. Update export_pdf electrical specification table
old_pdf_bldg_spec = '("Solar PV Module Rating", f"{b.panel_watt or report.panel_watt} W Mono PERC / TOPCon Half-Cut"),'
new_pdf_bldg_spec = '("Solar PV Module Rating", f"{b.panel_watt or report.panel_watt} W {b.panel_tech or report.panel_tech}"),'
assert old_pdf_bldg_spec in code, "old_pdf_bldg_spec not found"
code = code.replace(old_pdf_bldg_spec, new_pdf_bldg_spec, 1)

old_pdf_inv_spec = """            draw_section_title(pdf, f"Selected Grid-Tied Inverter Specifications ({site.inverter_kw:g} kW)", "Core inverter rating, MPPT topology, and operating parameters", tag="INVERTER")
            draw_modern_two_col(pdf, [
                ("Selected Inverter Rating", f"{site.inverter_kw:g} kW Grid-Tied Solar Inverter"),
                ("AC Output Voltage & Grid Phase", "415V, 3-Phase, 50 Hz AC" if site.inverter_kw > 5.0 else "230V, 1-Phase, 50 Hz AC"),"""

new_pdf_inv_spec = """            inv_model_meta = get_inverter_model(site.inverter_kw)
            model_names = inv_model_meta.top_tier_models if inv_model_meta else "Tier-1 Certified"
            draw_section_title(pdf, f"Selected Grid-Tied Inverter Specifications ({site.inverter_kw:g} kW)", "Core inverter rating (70% derated selection), MPPT topology & models", tag="INVERTER")
            draw_modern_two_col(pdf, [
                ("Selected Inverter Rating", f"{site.inverter_kw:g} kW Grid-Tied Inverter ({inv_model_meta.phase if inv_model_meta else ''})"),
                ("Certified Top-Tier OEM Models", sanitize_text(model_names)),
                ("Derated AC Design Power (70% Factor)", f"{site.ac_calculated_kw:.2f} kW AC (from {b.capacity_kw:.2f} kWp DC)"),
                ("AC Output Voltage & Grid Phase", "415V, 3-Phase, 50 Hz AC" if site.inverter_kw > 5.0 else "230V, 1-Phase, 50 Hz AC"),"""

assert old_pdf_inv_spec in code, "old_pdf_inv_spec not found"
code = code.replace(old_pdf_inv_spec, new_pdf_inv_spec, 1)

with open("solar_pv_estimator.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Updated export_pdf and API handlers in solar_pv_estimator.py!")

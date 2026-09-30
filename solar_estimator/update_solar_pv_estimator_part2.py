import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("solar_pv_estimator.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update build_building_result
old_bbr = '''def build_building_result(name: str, length_ft: float, breadth_ft: float, parapet_ft: float, panel_watt: int, panel_tech: str = "Mono-PERC (Mono-facial)") -> BuildingResult:
    rooftop_area = round(length_ft * breadth_ft, 2)
    utilized = round(max(0.0, (length_ft - 2 * parapet_ft) * (breadth_ft - 2 * parapet_ft)), 2)
    capacity_kw = round(utilized / 100.0, 2)

    panels = ceil_to_int((capacity_kw * 1000.0) / panel_watt)
    installed_kwp = round((panels * panel_watt) / 1000.0, 2)

    total_plant_dc_kw = max(capacity_kw, installed_kwp)
    ac_calculated_kw = round(total_plant_dc_kw * 0.70, 2)
    inverter_kw = select_inverter_lt(total_plant_dc_kw)
    phase_3 = inverter_kw > 5.0
    inv_cable, isolator = inverter_cable_and_isolator(inverter_kw, phase_3)

    strings = max(1, ceil_to_int(panels / 20.0))
    return BuildingResult(
        name=name,
        rooftop_area_sqft=rooftop_area,
        utilized_rooftop_area_sqft=utilized,
        capacity_kw=capacity_kw,
        panel_count=panels,
        strings=strings,
        inverter_kw=inverter_kw,
        inverter_qty=1,
        inverter_cable=inv_cable,
        isolator_rating=isolator,
        parapet_ft=parapet_ft,
        panel_watt=panel_watt,
        panel_tech=panel_tech,
        ac_calculated_kw=ac_calculated_kw,
    )'''

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
        inverter_kw = select_inverter_lt(total_plant_dc_kw)

    total_plant_dc_kw = max(capacity_kw, installed_kwp)
    ac_calculated_kw = round(total_plant_dc_kw * 0.70, 2)
    # KERC SRTPV 2016 Reg 6(1): <= 5 kW is 230V 1-Ph; > 5 kW is 415V 3-Ph
    phase_3 = inverter_kw > 5.0
    inv_cable, isolator = inverter_cable_and_isolator(inverter_kw, phase_3)
    strings = max(1, ceil_to_int(panels / 20.0))

    return BuildingResult(
        name=name,
        rooftop_area_sqft=rooftop_area,
        utilized_rooftop_area_sqft=utilized,
        capacity_kw=capacity_kw,
        panel_count=panels,
        strings=strings,
        inverter_kw=inverter_kw,
        inverter_qty=1,
        inverter_cable=inv_cable,
        isolator_rating=isolator,
        parapet_ft=parapet_ft,
        panel_watt=panel_watt,
        panel_tech=panel_tech,
        ac_calculated_kw=ac_calculated_kw,
        sanctioned_load_kw=sanctioned_load_kw,
        roof_area_required_sqft=req_area_sqft,
        roof_area_status=area_status,
    )'''

assert old_bbr in code, "old_bbr not found"
code = code.replace(old_bbr, new_bbr, 1)

# 2. Update build_system_report signature & body
old_bsr = '''def build_system_report(
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
) -> LTDesignReport:'''

new_bsr = '''def build_system_report(
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
    contact_number: str = "",
    sanctioned_load_kw: Optional[float] = None,
) -> LTDesignReport:'''

assert old_bsr in code, "old_bsr not found"
code = code.replace(old_bsr, new_bsr, 1)

old_bsr_body_top = '''    report = LTDesignReport(
        application_type="LT Applications",
        mode=mode,
        customer_name=customer_name,
        location=location,
        email=email,
        panel_watt=panel_watt,
        panel_tech=panel_tech,
        acdb_to_grid_distance_m=distance_m,
    )'''

new_bsr_body_top = '''    report = LTDesignReport(
        application_type="LT Applications",
        mode=mode,
        customer_name=customer_name,
        location=location,
        email=email,
        contact_number=contact_number,
        sanctioned_load_kw=sanctioned_load_kw,
        panel_watt=panel_watt,
        panel_tech=panel_tech,
        acdb_to_grid_distance_m=distance_m,
    )'''

assert old_bsr_body_top in code, "old_bsr_body_top not found"
code = code.replace(old_bsr_body_top, new_bsr_body_top, 1)

old_bsr_roof_loop = '''    if mode == "roof":
        for name, L, B in buildings:
            building_results.append(build_building_result(name, L, B, parapet_ft, panel_watt, panel_tech))'''

new_bsr_roof_loop = '''    if mode == "roof":
        for name, L, B in buildings:
            building_results.append(build_building_result(name, L, B, parapet_ft, panel_watt, panel_tech, sanctioned_load_kw))'''

assert old_bsr_roof_loop in code, "old_bsr_roof_loop not found"
code = code.replace(old_bsr_roof_loop, new_bsr_roof_loop, 1)

# Check for 20 kW ceiling warning in build_system_report
old_bsr_cap_sum = '''    report.total_capacity_kw = round(sum(b.capacity_kw for b in building_results), 2)'''
new_bsr_cap_sum = '''    raw_total_cap = round(sum(b.capacity_kw for b in building_results), 2)
    if raw_total_cap >= KERC_LT_CEILING_KW:
        report.total_capacity_kw = KERC_LT_CEILING_KW
        report.kerc_regulations_notes.append("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations")
    else:
        report.total_capacity_kw = raw_total_cap'''

assert old_bsr_cap_sum in code, "old_bsr_cap_sum not found"
code = code.replace(old_bsr_cap_sum, new_bsr_cap_sum, 1)

with open("solar_pv_estimator.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Part 2 applied to solar_pv_estimator.py!")

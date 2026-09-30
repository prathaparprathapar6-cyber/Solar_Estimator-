import sys
sys.stdout.reconfigure(encoding='utf-8')
from solar_pv_estimator import (
    select_inverter_lt,
    get_inverter_model,
    select_acdb_components,
    build_system_report,
    build_multi_site_report,
    export_pdf,
    INVERTER_MASTER_CATALOG,
    SOLAR_PANEL_CATALOG
)

print("1. Testing Inverter 70% Derating Selection...")
# User Prompt Example: 3.5 kW DC -> 3.5 * 0.7 = 2.45 kW -> Inverter = 3.0 kW
inv_35 = select_inverter_lt(3.5)
print(f"DC 3.5 kW -> Inverter selected: {inv_35} kW (Expected: 3.0 kW)")
assert inv_35 == 3.0, f"Expected 3.0 kW but got {inv_35}"

model_3 = get_inverter_model(3.0)
print(f"3 kW Inverter Model: {model_3.phase}, {model_3.top_tier_models}")
assert "Growatt" in model_3.top_tier_models

# AC sizing for 3.5 kW DC -> derated AC power = 2.45 kW
comps, breaker_a, rated_curr, grid_cable, busbar = select_acdb_components(2.45, 20.0)
print(f"Derated 2.45 kW AC -> Breaker: {breaker_a}A (Expected: 16A), Rated Current: {rated_curr}A, Cable: {grid_cable}")
assert breaker_a == 16, f"Expected 16A but got {breaker_a}"

# Test other points:
# 10 kW DC -> 7.0 kW derated -> 7.0 kW inverter
inv_10 = select_inverter_lt(10.0)
print(f"DC 10.0 kW -> Inverter selected: {inv_10} kW (Expected: 7.0 kW)")
assert inv_10 == 7.0

# 20 kW DC -> 14.0 kW derated -> 14.0 kW inverter
inv_20 = select_inverter_lt(20.0)
print(f"DC 20.0 kW -> Inverter selected: {inv_20} kW (Expected: 14.0 kW)")
assert inv_20 == 14.0

print("\n2. Testing Single-Site System Report with Panel Tech...")
rep = build_system_report(
    mode="roof",
    buildings=[("Main Block", 30.0, 20.0)],
    parapet_ft=1.0,
    monthly_units=0,
    distance_m=20.0,
    panel_watt=550,
    customer_name="Test Customer Tech",
    location="Bengaluru, Karnataka",
    email="test@example.com",
    panel_tech="N-Type TOPCon"
)
print(f"DC Capacity: {rep.total_capacity_kw} kWp, Derated AC: {rep.ac_calculated_kw} kW, Inverter: {rep.site_reports[0].inverter_kw} kW, MCB: {rep.acdb_current_a}A")
print(f"BOM Item 1 Spec: {rep.bom_items[0].specification}")
print(f"BOM Item 2 Spec: {rep.bom_items[1].specification}")
assert "N-Type TOPCon" in rep.bom_items[0].specification

pdf_single = export_pdf(rep, "test_single_tech.pdf")
print(f"Generated single-site PDF: {pdf_single}")

print("\n3. Testing Multi-Site System Report with Mixed Tech & Watts...")
sites_data = [
    {
        "name": "Site 1 - College",
        "location": "Shivamogga",
        "distance_m": 25.0,
        "buildings": [
            {"name": "Admin Block", "length_ft": 45.0, "breadth_ft": 35.0, "parapet_ft": 1.5, "panel_watt": 400, "panel_tech": "Mono-PERC (Mono-facial)"},
            {"name": "Lab Block", "length_ft": 40.0, "breadth_ft": 30.0, "parapet_ft": 1.5, "panel_watt": 580, "panel_tech": "N-Type TOPCon"}
        ]
    },
    {
        "name": "Site 2 - Hostel",
        "location": "Bengaluru",
        "distance_m": 15.0,
        "buildings": [
            {"name": "Hostel A", "length_ft": 50.0, "breadth_ft": 35.0, "parapet_ft": 1.5, "panel_watt": 550, "panel_tech": "Bifacial (Mono / TOPCon)"}
        ]
    }
]
multi_rep = build_multi_site_report(sites_data, project_name="Integrated Portfolio Tech", location="Karnataka")
print(f"Multi-site Total Cap: {multi_rep.total_capacity_kw} kW, BOM Sites: {len(multi_rep.site_reports)}")
print(f"Site 1 BOM Item 1 Spec: {multi_rep.site_reports[0].bom_items[0].specification}")
print(f"Site 1 BOM Item 8 Spec (ACDB): {multi_rep.site_reports[0].bom_items[7].specification}")

pdf_multi = export_pdf(multi_rep, "test_multi_tech.pdf")
print(f"Generated multi-site PDF: {pdf_multi}")

print("\nALL BACKEND SIZING TESTS PASSED SUCCESSFULLY!")

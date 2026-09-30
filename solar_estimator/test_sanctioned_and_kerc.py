import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from solar_pv_estimator import (
    calculate_system,
    build_system_report,
    build_multi_site_report,
    export_pdf
)

print("=" * 70)
print("TESTING SANCTIONED LOAD, AREA SUFFICIENCY & KERC 20 kW LT REGULATION")
print("=" * 70)

# -------------------------------------------------------------
# CASE A: Sanctioned load 15 kW, roof area 2000 sqft
# -------------------------------------------------------------
print("\n--- CASE A: Sanctioned Load 15 kW, Roof Area 2000 sqft ---")
# L=50 ft, B=40 ft, parapet=0 -> utilized area = 2000 sqft
rep_a = calculate_system(
    mode="roof",
    length_ft=50.0,
    breadth_ft=40.0,
    parapet_ft=0.0,
    sanctioned_load_kw=15.0,
    customer_name="Case A - Sufficient Area Customer",
    contact_number="+91 98888 11111",
    location="Bengaluru, Karnataka",
    email="case_a@voltroof.com"
)

print(f"Total Rooftop Area: {rep_a.total_rooftop_area_sqft} sq.ft")
print(f"Sanctioned Load: {rep_a.sanctioned_load_kw} kW")
print(f"Rooftop Area Status: {rep_a.roof_area_status}")
print(f"System Capacity: {rep_a.total_capacity_kw} kW")
print(f"Customer Contact: {rep_a.contact_number}")
print(f"KERC Notes: {rep_a.kerc_regulations_notes}")

assert rep_a.total_capacity_kw == 15.0, f"Expected 15.0 kW, got {rep_a.total_capacity_kw}"
assert "Sufficient" in rep_a.roof_area_status, f"Expected 'Sufficient' in status, got {rep_a.roof_area_status}"
assert rep_a.contact_number == "+91 98888 11111", f"Contact number mismatch: {rep_a.contact_number}"
assert len(rep_a.kerc_regulations_notes) == 0, f"Expected no 20kW ceiling notes for 15kW, got {rep_a.kerc_regulations_notes}"
pdf_a = export_pdf(rep_a, "test_case_a.pdf")
print(f"Case A PDF Exported: {pdf_a} ({os.path.getsize(pdf_a):,} bytes)")
print("✓ CASE A PASSED!")

# -------------------------------------------------------------
# CASE B: Sanctioned load 25 kW, roof area 3000 sqft
# -------------------------------------------------------------
print("\n--- CASE B: Sanctioned Load 25 kW, Roof Area 3000 sqft ---")
# L=60 ft, B=50 ft, parapet=0 -> utilized area = 3000 sqft
rep_b = calculate_system(
    mode="roof",
    length_ft=60.0,
    breadth_ft=50.0,
    parapet_ft=0.0,
    sanctioned_load_kw=25.0,
    customer_name="Case B - Statutory Capped Customer",
    contact_number="+91 97777 22222",
    location="Mysuru, Karnataka",
    email="case_b@voltroof.com"
)

print(f"Total Rooftop Area: {rep_b.total_rooftop_area_sqft} sq.ft")
print(f"Sanctioned Load: {rep_b.sanctioned_load_kw} kW")
print(f"Rooftop Area Status: {rep_b.roof_area_status}")
print(f"System Capacity: {rep_b.total_capacity_kw} kW (Capped at LT 20.0 kW)")
print(f"Customer Contact: {rep_b.contact_number}")
print(f"KERC Notes: {rep_b.kerc_regulations_notes}")

assert rep_b.total_capacity_kw == 20.0, f"Expected capacity capped to 20.0 kW, got {rep_b.total_capacity_kw}"
assert "Sufficient" in rep_b.roof_area_status, f"Expected 'Sufficient' in status, got {rep_b.roof_area_status}"
assert rep_b.contact_number == "+91 97777 22222", f"Contact number mismatch: {rep_b.contact_number}"
assert any("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" in note for note in rep_b.kerc_regulations_notes), \
    f"Expected KERC 20 kW compliance notice, got: {rep_b.kerc_regulations_notes}"
pdf_b = export_pdf(rep_b, "test_case_b.pdf")
print(f"Case B PDF Exported: {pdf_b} ({os.path.getsize(pdf_b):,} bytes)")
print("✓ CASE B PASSED!")

# -------------------------------------------------------------
# CASE C: Sanctioned load 20 kW, roof area 800 sqft
# -------------------------------------------------------------
print("\n--- CASE C: Sanctioned Load 20 kW, Roof Area 800 sqft (Area Deficit) ---")
# L=40 ft, B=20 ft, parapet=0 -> utilized area = 800 sqft
rep_c = calculate_system(
    mode="roof",
    length_ft=40.0,
    breadth_ft=20.0,
    parapet_ft=0.0,
    sanctioned_load_kw=20.0,
    customer_name="Case C - Deficit Area Customer",
    contact_number="+91 96666 33333",
    location="Hubballi, Karnataka",
    email="case_c@voltroof.com"
)

print(f"Total Rooftop Area: {rep_c.total_rooftop_area_sqft} sq.ft")
print(f"Sanctioned Load: {rep_c.sanctioned_load_kw} kW")
print(f"Rooftop Area Status: {rep_c.roof_area_status}")
print(f"System Capacity: {rep_c.total_capacity_kw} kW (Constrained by available area)")
print(f"Customer Contact: {rep_c.contact_number}")
print(f"KERC Notes: {rep_c.kerc_regulations_notes}")

assert "Deficit" in rep_c.roof_area_status, f"Expected 'Deficit' in status, got {rep_c.roof_area_status}"
assert rep_c.total_capacity_kw < 20.0, f"Expected capacity < 20.0 kW due to deficit area, got {rep_c.total_capacity_kw}"
assert rep_c.total_capacity_kw == 10.0, f"Expected 10.0 kW (800 / 80), got {rep_c.total_capacity_kw}"
assert rep_c.contact_number == "+91 96666 33333", f"Contact number mismatch: {rep_c.contact_number}"
assert any("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" in note for note in rep_c.kerc_regulations_notes), \
    f"Expected KERC 20 kW notice since sanctioned load was 20 kW, got: {rep_c.kerc_regulations_notes}"
pdf_c = export_pdf(rep_c, "test_case_c.pdf")
print(f"Case C PDF Exported: {pdf_c} ({os.path.getsize(pdf_c):,} bytes)")
print("✓ CASE C PASSED!")

# -------------------------------------------------------------
# MULTI-SITE VERIFICATION
# -------------------------------------------------------------
print("\n--- MULTI-SITE TEST WITH CONTACT NUMBERS & REGULATORY NOTES ---")
multi_data = [
    {
        "name": "Shivamogga Branch",
        "location": "Shivamogga, Karnataka",
        "contact_number": "+91 95555 44444",
        "sanctioned_load_kw": 25.0, # Exceeds 20 kW -> Capped to 20 kW
        "buildings": [{"name": "Main Wing", "length_ft": 55.0, "breadth_ft": 40.0, "parapet_ft": 1.0, "panel_watt": 550}]
    },
    {
        "name": "Mangaluru Branch",
        "location": "Mangaluru, Karnataka",
        "contact_number": "+91 94444 55555",
        "sanctioned_load_kw": 12.0, # Within 20 kW
        "buildings": [{"name": "Office Block", "length_ft": 45.0, "breadth_ft": 35.0, "parapet_ft": 1.0, "panel_watt": 550}]
    }
]

rep_multi = build_multi_site_report(
    sites_data=multi_data,
    project_name="Commercial Multi-Branch Portfolio",
    location="Karnataka",
    contact_number="+91 99999 00000"
)

print(f"Multi-site Total Capacity: {rep_multi.total_capacity_kw} kW")
print(f"Site 1 Capacity: {rep_multi.site_reports[0].capacity_kw} kW (Raw: {rep_multi.site_reports[0].raw_capacity_kw} kW)")
print(f"Site 1 Notes: {rep_multi.site_reports[0].kerc_regulations_notes}")
print(f"Site 2 Capacity: {rep_multi.site_reports[1].capacity_kw} kW")

assert rep_multi.site_reports[0].capacity_kw == 20.0, f"Expected Site 1 capped to 20.0 kW, got {rep_multi.site_reports[0].capacity_kw}"
assert rep_multi.site_reports[1].capacity_kw == 12.0, f"Expected Site 2 capacity 12.0 kW, got {rep_multi.site_reports[1].capacity_kw}"
assert any("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" in note for note in rep_multi.site_reports[0].kerc_regulations_notes)
assert any("20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" in note for note in rep_multi.kerc_regulations_notes)

pdf_multi = export_pdf(rep_multi, "test_multi_verified.pdf")
print(f"Multi-site PDF Exported: {pdf_multi} ({os.path.getsize(pdf_multi):,} bytes)")
print("✓ MULTI-SITE VERIFIED!")

print("\n" + "=" * 70)
print("ALL CLI & SIZING TESTS PASSED PERFECTLY!")
print("=" * 70)

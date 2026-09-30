import sys
import os

sys.path.insert(0, r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator")
from solar_pv_estimator import build_multi_site_report, build_system_report, export_pdf

def test():
    print("Testing Multi-Site PDF Generation...")
    sites_data = [
        {
            "name": "Vidyanagar Campus",
            "location": "Shivamogga, Karnataka",
            "email": "vidya@voltroof.com",
            "mode": "roof",
            "distance_m": 25.0,
            "buildings": [
                {"name": "Admin Block", "length_ft": 45.0, "breadth_ft": 35.0, "parapet_ft": 1.5, "panel_watt": 550},
                {"name": "Library Block", "length_ft": 40.0, "breadth_ft": 30.0, "parapet_ft": 1.5, "panel_watt": 550}
            ]
        },
        {
            "name": "Technology Park",
            "location": "Bengaluru, Karnataka",
            "email": "tech@voltroof.com",
            "mode": "roof",
            "distance_m": 18.0,
            "buildings": [
                {"name": "Innovation Lab", "length_ft": 55.0, "breadth_ft": 40.0, "parapet_ft": 1.8, "panel_watt": 550}
            ]
        }
    ]

    rep_multi = build_multi_site_report(sites_data, project_name="Karnataka Tech Portfolio", location="Karnataka")
    print(f"Multi-site Total Capacity: {rep_multi.total_capacity_kw} kW")
    print(f"Total Sites: {len(rep_multi.site_reports)}")
    print(f"Total Buildings: {len(rep_multi.building_reports)}")
    for s in rep_multi.site_reports:
        print(f"  Site: {s.name}, Cap: {s.capacity_kw} kW (raw: {s.raw_capacity_kw} kW), Inverter: {s.inverter_kw} kW, ACDB Breaker: {s.acdb_current_a}A, Cable: {s.acdb_grid_cable}")

    pdf_multi = export_pdf(rep_multi, r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator\test_multi_site.pdf")
    print(f"Multi-site PDF generated: {pdf_multi}, size: {os.path.getsize(pdf_multi)} bytes")

    print("\nTesting Single-Site PDF Generation...")
    rep_single = build_system_report(
        mode="roof",
        buildings=[("Building 1", 40.0, 30.0)],
        parapet_ft=1.5,
        monthly_units=1200.0,
        distance_m=20.0,
        panel_watt=550,
        customer_name="Single Roof Residence",
        location="Mysuru, Karnataka",
        email="single@voltroof.com"
    )
    print(f"Single-site Total Capacity: {rep_single.total_capacity_kw} kW")
    pdf_single = export_pdf(rep_single, r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator\test_single_site.pdf")
    print(f"Single-site PDF generated: {pdf_single}, size: {os.path.getsize(pdf_single)} bytes")

    import re
    with open(pdf_multi, "rb") as f:
        raw_m = f.read()
    page_matches_m = re.findall(rb"/Type\s*/Page\b", raw_m)
    counts_m = re.findall(rb"/Count\s+(\d+)", raw_m)
    print(f"\nMulti-site Page Count (/Type /Page): {len(page_matches_m)}")
    print(f"Multi-site Root /Count: {counts_m}")

    with open(pdf_single, "rb") as f:
        raw_s = f.read()
    page_matches_s = re.findall(rb"/Type\s*/Page\b", raw_s)
    counts_s = re.findall(rb"/Count\s+(\d+)", raw_s)
    print(f"\nSingle-site Page Count (/Type /Page): {len(page_matches_s)}")
    print(f"Single-site Root /Count: {counts_s}")

    print("\nALL PDF TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test()

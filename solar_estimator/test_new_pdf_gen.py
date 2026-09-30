import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from solar_pv_estimator import build_multi_site_report, export_pdf

# Test 1: Multi-site with buildings having different panel wattages
# Site-1: Building-1 has 400W panels (say 10 Nos), Building-2 has 550W panels (say 3 Nos)
# Site-2: Building-1 has 550W panels
multi_sites_payload = [
    {
        "name": "Vidyanagar Campus",
        "location": "Shivamogga, Karnataka",
        "email": "vidya@example.com",
        "mode": "roof",
        "distance_m": 25.0,
        "buildings": [
            {
                "name": "Main Academic Block",
                "length_ft": 45.0,
                "breadth_ft": 35.0,
                "parapet_ft": 1.5,
                "panel_watt": 400
            },
            {
                "name": "Science Laboratory",
                "length_ft": 30.0,
                "breadth_ft": 20.0,
                "parapet_ft": 1.0,
                "panel_watt": 550
            }
        ]
    },
    {
        "name": "Technology Park",
        "location": "Bengaluru, Karnataka",
        "email": "techpark@example.com",
        "mode": "roof",
        "distance_m": 15.0,
        "buildings": [
            {
                "name": "Tower A Innovation Hub",
                "length_ft": 50.0,
                "breadth_ft": 44.0,
                "parapet_ft": 1.5,
                "panel_watt": 550
            }
        ]
    }
]

print("Building multi-site report...")
ms_report = build_multi_site_report(multi_sites_payload, project_name="Karnataka Institutional Portfolio")
ms_pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_multi_site_new.pdf")
export_pdf(ms_report, ms_pdf_path)
print(f"Generated multi-site PDF: {ms_pdf_path}, size: {os.path.getsize(ms_pdf_path)} bytes")

# Test 2: Single-site project
single_site_payload = [
    {
        "name": "Mysuru Eco Residence",
        "location": "Mysuru, Karnataka",
        "email": "mysuru@example.com",
        "mode": "roof",
        "distance_m": 20.0,
        "buildings": [
            {
                "name": "Main Residence",
                "length_ft": 35.0,
                "breadth_ft": 25.0,
                "parapet_ft": 1.0,
                "panel_watt": 550
            }
        ]
    }
]

print("\nBuilding single-site report...")
ss_report = build_multi_site_report(single_site_payload, project_name="Mysuru Eco Residence")
ss_pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_single_site_new.pdf")
export_pdf(ss_report, ss_pdf_path)
print(f"Generated single-site PDF: {ss_pdf_path}, size: {os.path.getsize(ss_pdf_path)} bytes")

# Check page counts with pypdfium2
import pypdfium2 as pdfium
ms_doc = pdfium.PdfDocument(ms_pdf_path)
print(f"Multi-site total pages: {len(ms_doc)}")

ss_doc = pdfium.PdfDocument(ss_pdf_path)
print(f"Single-site total pages: {len(ss_doc)}")

# Verify NO portfolio words in single-site PDF
ss_text = ""
for page in ss_doc:
    ss_text += page.get_textpage().get_text_range()

portfolio_words = ["portfolio", "multi-site", "multisite", "multi site"]
found_words = [w for w in portfolio_words if w in ss_text.lower()]
print(f"Portfolio words found in single-site PDF: {found_words}")
assert len(found_words) == 0, f"Found portfolio words in single site: {found_words}"

print("\nALL PDF TESTS PASSED SUCCESSFULLY!")

import os
import sys
import shutil
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
downloads_dir = r"C:\Users\DELL\Downloads"
brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d"

from solar_pv_estimator import (
    build_system_report,
    build_multi_site_report,
    export_pdf
)
import pypdfium2 as pdfium

print("1. Generating Official Single-Site Engineering Report (6 Pages)...")
single_rep = build_system_report(
    mode="roof",
    buildings=[("Residential Rooftop", 35.0, 25.0)],
    parapet_ft=1.5,
    monthly_units=0,
    distance_m=20.0,
    panel_watt=550,
    panel_tech="N-Type TOPCon",
    customer_name="Sri. H. R. Vishwanath",
    contact_number="+91 94481 23456",
    sanctioned_load_kw=10.0,
    location="Shivamogga, Karnataka",
    email="vishwanath@voltroof.in"
)
single_pdf_path = os.path.join(scratch_dir, "VoltRoof_SingleSite_Engineering_Report_6Pages.pdf")
export_pdf(single_rep, single_pdf_path)
print(f"Generated: {single_pdf_path} ({os.path.getsize(single_pdf_path):,} bytes)")

print("\n2. Generating Official Multi-Site Engineering Report (11 Pages)...")
multi_sites_data = [
    {
        "name": "Site 1 - PESIT Engineering Campus",
        "location": "Shivamogga, Karnataka",
        "contact_number": "+91 98450 11223",
        "sanctioned_load_kw": 25.0,
        "distance_m": 25.0,
        "buildings": [
            {
                "name": "Admin Block",
                "length_ft": 45.0,
                "breadth_ft": 35.0,
                "parapet_ft": 1.5,
                "panel_watt": 400,
                "panel_tech": "Mono-PERC (Mono-facial)"
            },
            {
                "name": "Computer Science Lab",
                "length_ft": 40.0,
                "breadth_ft": 30.0,
                "parapet_ft": 1.5,
                "panel_watt": 580,
                "panel_tech": "N-Type TOPCon"
            }
        ]
    },
    {
        "name": "Site 2 - PES University Innovation Hub",
        "location": "Bengaluru, Karnataka",
        "contact_number": "+91 98452 99887",
        "sanctioned_load_kw": 18.0,
        "distance_m": 15.0,
        "buildings": [
            {
                "name": "Tower A Innovation Hub",
                "length_ft": 52.0,
                "breadth_ft": 36.0,
                "parapet_ft": 1.5,
                "panel_watt": 550,
                "panel_tech": "Bifacial (Mono / TOPCon)"
            }
        ]
    }
]

multi_rep = build_multi_site_report(
    multi_sites_data,
    project_name="Integrated Educational Campus Solar Portfolio",
    location="Karnataka, India"
)
multi_pdf_path = os.path.join(scratch_dir, "VoltRoof_MultiSite_Engineering_Report_11Pages.pdf")
export_pdf(multi_rep, multi_pdf_path)
print(f"Generated: {multi_pdf_path} ({os.path.getsize(multi_pdf_path):,} bytes)")

print("\n3. Rendering Key PDF Preview Images for Verification...")
# Render single site key pages
pdf_s = pdfium.PdfDocument(single_pdf_path)
for p_idx in [0, 1, 2]: # Pages 1, 2, 3
    img = pdf_s[p_idx].render(scale=2.0).to_pil()
    out_img = os.path.join(scratch_dir, f"single_site_new_p{p_idx+1}.png")
    img.save(out_img)
    shutil.copy2(out_img, os.path.join(brain_dir, f"single_site_new_p{p_idx+1}.png"))
    print(f"Saved: {out_img}")

# Render multi site key pages
pdf_m = pdfium.PdfDocument(multi_pdf_path)
for p_idx in [5, 6, 7]: # Pages 6 (Site 1 BOM), 7 (Site 2 BOM), 8 (Capital Matrix)
    img = pdf_m[p_idx].render(scale=2.0).to_pil()
    out_img = os.path.join(scratch_dir, f"multi_site_new_p{p_idx+1}.png")
    img.save(out_img)
    shutil.copy2(out_img, os.path.join(brain_dir, f"multi_site_new_p{p_idx+1}.png"))
    print(f"Saved: {out_img}")

print("\n4. Copying deliverables to Downloads and Artifact Directories...")
# Copy PDFs to Downloads and Brain
for pdf_file in ["VoltRoof_SingleSite_Engineering_Report_6Pages.pdf", "VoltRoof_MultiSite_Engineering_Report_11Pages.pdf", "user_manual.pdf"]:
    src = os.path.join(scratch_dir, pdf_file)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(downloads_dir, pdf_file))
        shutil.copy2(src, os.path.join(brain_dir, pdf_file))
        if pdf_file == "user_manual.pdf":
            shutil.copy2(src, os.path.join(downloads_dir, "VoltRoof_User_Manual.pdf"))
            shutil.copy2(src, os.path.join(brain_dir, "VoltRoof_User_Manual.pdf"))

# Render user manual preview pages
if os.path.exists(os.path.join(scratch_dir, "user_manual.pdf")):
    pdf_man = pdfium.PdfDocument(os.path.join(scratch_dir, "user_manual.pdf"))
    for p_idx in range(min(len(pdf_man), 3)):
        img_m = pdf_man[p_idx].render(scale=2.0).to_pil()
        out_m = os.path.join(scratch_dir, f"manual_p{p_idx+1}.png")
        img_m.save(out_m)
        shutil.copy2(out_m, os.path.join(brain_dir, f"manual_p{p_idx+1}.png"))
        print(f"Saved: {out_m}")

# Copy HTML, JS, scripts and companion assets
for f_name in [
    "VoltRoof_Combined.html",
    "voltroof_solar_pv_estimator_standalone.html",
    "voltroof_solar_pv_estimator.html",
    "index.html",
    "sw.js",
    "logo.png",
    "solar_pv_estimator.py",
    "solar_pv_estimator_standalone.py",
    "solar_gui.py",
    "pricing_db.json",
    "visitors_db.json",
    "feedback_db.json",
    "admins_db.json"
]:
    src = os.path.join(scratch_dir, f_name)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(downloads_dir, f_name))
        shutil.copy2(src, os.path.join(brain_dir, f_name))

# Copy UI screenshots to downloads and brain
for shot in [
    "voltroof_combined_user_dashboard.png",
    "voltroof_combined_visualizer_3d.png",
    "voltroof_combined_admin_manual.png",
    "voltroof_combined_admin_pricing.png",
    "voltroof_combined_admin_analytics.png",
    "voltroof_combined_admin_feedback.png",
    "voltroof_combined_admin_users.png",
    "voltroof_combined_admin_settings.png",
    "web_20kw_modal.png",
    "web_singlesite_bom.png",
    "web_multisite_bom.png",
    "web_multisite_matrix.png"
]:
    src = os.path.join(scratch_dir, shot)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(downloads_dir, shot))
        shutil.copy2(src, os.path.join(brain_dir, shot))

print("\n5. Packaging Complete Deliverables ZIP Archive...")
zip_name = "VoltRoof_Solar_PV_Estimator_Package.zip"
zip_scratch = os.path.join(scratch_dir, zip_name)
zip_downloads = os.path.join(downloads_dir, zip_name)
zip_brain = os.path.join(brain_dir, zip_name)

files_to_zip = [
    ("VoltRoof_Combined.html", "VoltRoof_Combined.html"),
    ("sw.js", "sw.js"),
    ("voltroof_solar_pv_estimator_standalone.html", "VoltRoof_Standalone_Web_App.html"),
    ("index.html", "index.html"),
    ("solar_pv_estimator.py", "solar_pv_estimator.py"),
    ("solar_pv_estimator_standalone.py", "solar_pv_estimator_standalone.py"),
    ("solar_gui.py", "solar_gui.py"),
    ("user_manual.pdf", "VoltRoof_User_Manual.pdf"),
    ("VoltRoof_SingleSite_Engineering_Report_6Pages.pdf", "VoltRoof_SingleSite_Engineering_Report_6Pages.pdf"),
    ("VoltRoof_MultiSite_Engineering_Report_11Pages.pdf", "VoltRoof_MultiSite_Engineering_Report_11Pages.pdf"),
    ("pricing_db.json", "pricing_db.json"),
    ("visitors_db.json", "visitors_db.json"),
    ("feedback_db.json", "feedback_db.json"),
    ("admins_db.json", "admins_db.json"),
    ("logo.png", "logo.png"),
    ("watermark.png", "watermark.png"),
    ("image.png", "image.png"),
    ("banner_crop.png", "banner_crop.png"),
    ("header_crop.png", "header_crop.png"),
    ("chart.umd.min.js", "chart.umd.min.js")
]

with zipfile.ZipFile(zip_scratch, "w", zipfile.ZIP_DEFLATED) as zf:
    for src_file, arc_name in files_to_zip:
        p = os.path.join(scratch_dir, src_file)
        if os.path.exists(p):
            zf.write(p, arc_name)

shutil.copy2(zip_scratch, zip_downloads)
shutil.copy2(zip_scratch, zip_brain)
print(f"Created: {zip_scratch} ({os.path.getsize(zip_scratch):,} bytes)")
print(f"Copied to: {zip_downloads}")
print(f"Copied to: {zip_brain}")
print("\nALL DELIVERABLES GENERATED & PACKAGED SUCCESSFULLY!")

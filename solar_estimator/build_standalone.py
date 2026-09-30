import os
import shutil

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
downloads_dir = r"C:\Users\DELL\Downloads"

# 1. Read chart.umd.min.js
chart_path = os.path.join(scratch_dir, "chart.umd.min.js")
with open(chart_path, "r", encoding="utf-8") as f:
    chart_js = f.read()

# 2. Read VoltRoof_Combined.html
combined_path = os.path.join(scratch_dir, "VoltRoof_Combined.html")
with open(combined_path, "r", encoding="utf-8") as f:
    combined_html = f.read()

# Also sync to index.html
index_path = os.path.join(scratch_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(combined_html)

# 3. Create voltroof_solar_pv_estimator_standalone.html with inlined Chart.js
standalone_html = combined_html
if '<script src="chart.umd.min.js" defer></script>' in standalone_html:
    standalone_html = standalone_html.replace('<script src="chart.umd.min.js" defer></script>', f"<script>\n{chart_js}\n</script>")
elif '<script src="chart.umd.min.js"></script>' in standalone_html:
    standalone_html = standalone_html.replace('<script src="chart.umd.min.js"></script>', f"<script>\n{chart_js}\n</script>")

standalone_path = os.path.join(scratch_dir, "voltroof_solar_pv_estimator_standalone.html")
with open(standalone_path, "w", encoding="utf-8") as f:
    f.write(standalone_html)
print(f"Generated standalone HTML: {len(standalone_html)} characters.")

# 4. Copy deliverables to User Downloads directory
if os.path.exists(downloads_dir):
    shutil.copy2(os.path.join(scratch_dir, "solar_pv_estimator.py"), os.path.join(scratch_dir, "solar_pv_estimator_standalone.py"))
    shutil.copy2(combined_path, os.path.join(downloads_dir, "VoltRoof_Combined.html"))
    shutil.copy2(standalone_path, os.path.join(downloads_dir, "voltroof_solar_pv_estimator_standalone.html"))
    shutil.copy2(combined_path, os.path.join(downloads_dir, "voltroof_solar_pv_estimator.html"))
    shutil.copy2(combined_path, os.path.join(downloads_dir, "index.html"))
    shutil.copy2(os.path.join(scratch_dir, "solar_pv_estimator.py"), os.path.join(downloads_dir, "solar_pv_estimator.py"))
    shutil.copy2(os.path.join(scratch_dir, "solar_pv_estimator_standalone.py"), os.path.join(downloads_dir, "solar_pv_estimator_standalone.py"))
    # Copy images, service worker and documentation
    for item in ["sw.js", "image.png", "logo.png", "banner_crop.png", "header_crop.png", "watermark.png", "chart.umd.min.js", "user_manual.pdf"]:
        src_item = os.path.join(scratch_dir, item)
        if os.path.exists(src_item):
            shutil.copy2(src_item, os.path.join(downloads_dir, item))
            if item == "user_manual.pdf":
                shutil.copy2(src_item, os.path.join(downloads_dir, "VoltRoof_User_Manual.pdf"))
    print("Successfully copied all deliverables and assets to Downloads directory!")
else:
    print(f"Downloads dir {downloads_dir} not found.")

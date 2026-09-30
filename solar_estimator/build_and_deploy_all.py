import os
import shutil
import base64
import zipfile

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
downloads_dir = r"C:\Users\DELL\Downloads"
brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d"

# 1. Update updateClock in VoltRoof_Combined.html
html_path = os.path.join(scratch_dir, "VoltRoof_Combined.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_text = f.read()

old_clock = '''function updateClock() {
  const el = document.getElementById("topDateTime");
  if (!el) return;
  const d = new Date();
  const date = d.toLocaleDateString("en-IN", { weekday: "short", day: "2-digit", month: "short", year: "numeric" });
  const time = d.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: true });
  el.textContent = `${date} · ${time}`;
}'''

new_clock = '''function updateClock() {
  const el = document.getElementById("topDateTime");
  if (el) {
    const d = new Date();
    const date = d.toLocaleDateString("en-IN", { weekday: "short", day: "2-digit", month: "short", year: "numeric" });
    const time = d.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: true });
    el.textContent = `${date} · ${time}`;
  }
  if (typeof updateRibbonGreeting === "function") {
    updateRibbonGreeting();
  }
}'''

if old_clock in html_text:
    html_text = html_text.replace(old_clock, new_clock, 1)
    print("Updated updateClock in VoltRoof_Combined.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)

# 2. Sync to index.html
index_path = os.path.join(scratch_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_text)
print("Synced VoltRoof_Combined.html -> index.html")

# 3. Create standalone HTML
logo_path = os.path.join(scratch_dir, "logo.png")
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("ascii")
logo_data_uri = f"data:image/png;base64,{logo_b64}"

chart_path = os.path.join(scratch_dir, "chart.umd.min.js")
with open(chart_path, "r", encoding="utf-8", errors="ignore") as f:
    chart_js = f.read()

standalone_text = html_text

# Replace logo.png references with data URI
standalone_text = standalone_text.replace('src="logo.png"', f'src="{logo_data_uri}"')
standalone_text = standalone_text.replace('href="logo.png"', f'href="{logo_data_uri}"')

# Replace chart.umd.min.js reference with inline script
chart_script_tag = '<script src="chart.umd.min.js"></script>'
if chart_script_tag in standalone_text:
    standalone_text = standalone_text.replace(chart_script_tag, f'<script>\n{chart_js}\n</script>', 1)
    print("Inlined chart.umd.min.js into standalone HTML")
else:
    print("WARN: chart.umd.min.js script tag not found")

standalone_path = os.path.join(scratch_dir, "voltroof_solar_pv_estimator_standalone.html")
with open(standalone_path, "w", encoding="utf-8") as f:
    f.write(standalone_text)
print(f"Created standalone HTML: {os.path.getsize(standalone_path):,} bytes")

# 4. Copy to Downloads
for fname in ["VoltRoof_Combined.html", "index.html", "voltroof_solar_pv_estimator_standalone.html", "logo.png"]:
    src = os.path.join(scratch_dir, fname)
    dst = os.path.join(downloads_dir, fname)
    shutil.copy2(src, dst)
    print(f"Copied {fname} -> Downloads")

# 5. Build ZIP packages
zip_files = [
    "VoltRoof_Combined.html",
    "index.html",
    "voltroof_solar_pv_estimator_standalone.html",
    "VoltRoof_A_to_Z_Handoff.md",
    "sw.js",
    "logo.png",
    "chart.umd.min.js",
    "solar_pv_estimator.py",
    "user_manual.pdf",
    "voltroof_login_split.png",
    "voltroof_user_dashboard.png",
    "voltroof_visualizer_3d.png",
    "voltroof_policy_hub.png",
    "voltroof_contact_us.png",
    "voltroof_admin_roster.png",
    "voltroof_admin_control_center.png",
    "voltroof_admin_pricing.png"
]

zip_download = os.path.join(downloads_dir, "VoltRoof_Solar_PV_Estimator_Package.zip")
zip_brain = os.path.join(brain_dir, "VoltRoof_Solar_PV_Estimator_Package.zip")
zip_scratch = os.path.join(scratch_dir, "VoltRoof_Solar_PV_Estimator_Package.zip")

for target_zip in [zip_download, zip_brain, zip_scratch]:
    with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in zip_files:
            p = os.path.join(scratch_dir, f)
            if os.path.exists(p):
                zf.write(p, arcname=f)
    print(f"Created {target_zip}: {os.path.getsize(target_zip):,} bytes")

print("\n--- ALL BUILD & DEPLOY TASKS COMPLETED SUCCESSFULLY ---")

import os
import zipfile
import shutil

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
downloads_dir = r"C:\Users\DELL\Downloads"
brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d"

zip_name = "VoltRoof_Solar_PV_Estimator_Package.zip"
zip_scratch = os.path.join(scratch_dir, zip_name)

files_to_pack = [
    "VoltRoof_Combined.html",
    "voltroof_solar_pv_estimator_standalone.html",
    "solar_pv_estimator.py",
    "backend_ext.py",
    "index.html",
    "chart.umd.min.js",
    "logo.png",
    "image.png",
    "watermark.png",
    "user_manual.pdf"
]

with zipfile.ZipFile(zip_scratch, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in files_to_pack:
        p = os.path.join(scratch_dir, f)
        if os.path.exists(p):
            zf.write(p, arcname=f)
            print(f"Added {f} ({os.path.getsize(p):,} bytes)")

for target in [downloads_dir, brain_dir]:
    if os.path.exists(target):
        shutil.copy2(zip_scratch, os.path.join(target, zip_name))
        print(f"Copied {zip_name} -> {target}")

print("Package ZIP successfully generated and synced!")

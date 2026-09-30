import os

downloads_dir = r"C:\Users\DELL\Downloads"
files = [
    "VoltRoof_Combined.html",
    "sw.js",
    "logo.png",
    "voltroof_solar_pv_estimator_standalone.html",
    "index.html",
    "VoltRoof_Solar_PV_Estimator_Package.zip",
    "VoltRoof_SingleSite_Engineering_Report_6Pages.pdf",
    "VoltRoof_MultiSite_Engineering_Report_11Pages.pdf",
    "VoltRoof_User_Manual.pdf"
]

print("Checking Downloads directory:")
for f in files:
    p = os.path.join(downloads_dir, f)
    exists = os.path.exists(p)
    size = os.path.getsize(p) if exists else 0
    status = "EXISTS" if exists else "MISSING"
    print(f"  {f}: {status} ({size:,} bytes)")

import os
import shutil
import subprocess
import time
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

test_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator\test_isolated_python"
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.makedirs(test_dir)

src_py = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator\solar_pv_estimator.py"
dst_py = os.path.join(test_dir, "solar_pv_estimator.py")
shutil.copy2(src_py, dst_py)

print("Created completely isolated directory with ONLY solar_pv_estimator.py:")
print("Files in test directory initially:", os.listdir(test_dir))

# Run the standalone script on test port 5055
proc = subprocess.Popen([
    sys.executable,
    "solar_pv_estimator.py",
    "5055"
], cwd=test_dir)

try:
    time.sleep(3.0)
    print("\nFiles in test directory after execution (extracted standalone assets):")
    files_after = os.listdir(test_dir)
    for f in sorted(files_after):
        sz = os.path.getsize(os.path.join(test_dir, f))
        print(f"  {f:35s} ({sz:,} bytes)")

    assert "index.html" in files_after, "index.html must be extracted"
    assert "logo.png" in files_after, "logo.png must be extracted"
    assert "chart.umd.min.js" in files_after, "chart.umd.min.js must be extracted"

    # Test GET http://127.0.0.1:5055/
    resp = urllib.request.urlopen("http://127.0.0.1:5055/")
    print(f"\nGET / Status: {resp.status}, Content-Length: {len(resp.read()):,}")

    # Test calculation API on port 5055
    req_data = json.dumps({'mode': 'roof', 'length_ft': 40, 'breadth_ft': 30}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:5055/api/calculate', data=req_data, headers={'Content-Type': 'application/json'})
    resp_calc = urllib.request.urlopen(req)
    res_json = json.loads(resp_calc.read().decode('utf-8'))
    print("API calculate successful! Result capacityKw:", res_json.get('capacityKw'), "invKw:", res_json.get('invKw'))

    # Test PDF download on port 5055
    req_pdf = urllib.request.Request('http://127.0.0.1:5055/api/download_pdf', data=req_data, headers={'Content-Type': 'application/json'})
    resp_pdf = urllib.request.urlopen(req_pdf)
    pdf_bytes = resp_pdf.read()
    print(f"PDF download successful! Generated PDF size: {len(pdf_bytes):,} bytes")

    print("\n=======================================================")
    print(" PYTHON STANDALONE FILE VERIFIED 100% SELF-CONTAINED!")
    print("=======================================================")

finally:
    proc.kill()
    time.sleep(0.5)
    # Cleanup test dir
    shutil.rmtree(test_dir, ignore_errors=True)

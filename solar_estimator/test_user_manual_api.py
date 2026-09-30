import os
import sys
import json
import time
import base64
import threading
import urllib.request
import urllib.parse
from http.server import HTTPServer

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
sys.path.insert(0, scratch_dir)

from solar_pv_estimator import SolarAppRequestHandler, INITIAL_ADMINS

def run_tests():
    # Start server on test port 5098
    test_port = 5098
    httpd = HTTPServer(("127.0.0.1", test_port), SolarAppRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    base_url = f"http://127.0.0.1:{test_port}"

    print(f"Testing VoltRoof User Manual & Admin Endpoints on {base_url}...")

    # Test 1: GET /user_manual.pdf
    req = urllib.request.Request(f"{base_url}/user_manual.pdf")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        data = resp.read()
        assert data.startswith(b"%PDF-"), "Expected PDF binary signature"
        print(f"PASS [1/5]: GET /user_manual.pdf returned {len(data):,} bytes with valid PDF signature.")

    # Test 2: GET /api/user_manual_meta
    req = urllib.request.Request(f"{base_url}/api/user_manual_meta")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        meta = json.loads(resp.read().decode("utf-8"))
        assert meta.get("exists") == True
        assert meta.get("filename") != ""
        print(f"PASS [2/5]: GET /api/user_manual_meta returned: {meta}")

    # Test 3: POST /api/admin/login (Invalid credentials)
    login_data = json.dumps({"username": "UnknownUser", "password": "WrongPassword"}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/admin/login", data=login_data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            assert False, "Expected 401 for invalid login"
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401, got {e.code}"
        print("PASS [3/5]: POST /api/admin/login properly rejected invalid credentials with 401.")

    # Test 4: POST /api/admin/login (Valid Super Admin credentials)
    super_admin = INITIAL_ADMINS[0]
    login_data = json.dumps({"username": super_admin["username"], "password": super_admin["password"]}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/admin/login", data=login_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode("utf-8"))
        assert res.get("success") == True
        assert res.get("admin", {}).get("username") == super_admin["username"]
        print(f"PASS [4/5]: POST /api/admin/login authenticated {super_admin['username']} ({res['admin']['role']}).")

    # Test 5: POST /api/admin/upload_user_manual
    # Read existing manual and re-upload with custom admin name
    manual_path = os.path.join(scratch_dir, "user_manual.pdf")
    with open(manual_path, "rb") as mf:
        pdf_bytes = mf.read()
    b64_content = "data:application/pdf;base64," + base64.b64encode(pdf_bytes).decode("ascii")

    upload_data = json.dumps({
        "filename": "VoltRoof_Solar_PV_User_Manual_2026.pdf",
        "data_base64": b64_content,
        "admin_name": "Adarsha KM"
    }).encode("utf-8")

    req = urllib.request.Request(f"{base_url}/api/admin/upload_user_manual", data=upload_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode("utf-8"))
        assert res.get("success") == True
        meta = res.get("meta", {})
        assert meta.get("filename") == "VoltRoof_Solar_PV_User_Manual_2026.pdf"
        assert meta.get("updated_by") == "Adarsha KM"
        print(f"PASS [5/5]: POST /api/admin/upload_user_manual successfully updated manual and metadata: {meta}")

    httpd.shutdown()
    print("\nALL 5 ENDPOINT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()

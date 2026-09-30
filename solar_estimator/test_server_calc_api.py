import urllib.request
import json
import time

time.sleep(1)

# Test GET routes
urls = [
    "http://127.0.0.1:5050/",
    "http://127.0.0.1:5050/VoltRoof_Combined.html",
    "http://127.0.0.1:5050/sw.js",
    "http://127.0.0.1:5050/logo.png",
    "http://127.0.0.1:5050/api/pricing",
    "http://127.0.0.1:5050/api/visitors/stats",
    "http://127.0.0.1:5050/api/admin/list",
    "http://127.0.0.1:5050/user_manual.pdf"
]

for u in urls:
    try:
        r = urllib.request.urlopen(u, timeout=5)
        print(f"PASS GET: {u} -> {r.status} ({r.headers.get('Content-Type')})")
    except Exception as e:
        print(f"FAIL GET: {u} -> {e}")

# Test POST /api/calculate
req_data = json.dumps({
    "schemaVersion": 1,
    "customer_name": "API Calc Test",
    "location": "Shivamogga, Karnataka",
    "sanctioned_load_kw": 15.0,
    "mode": "roof",
    "length_ft": 45,
    "breadth_ft": 35,
    "panel_watt": 550
}).encode("utf-8")

try:
    req = urllib.request.Request(
        "http://127.0.0.1:5050/api/calculate",
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=5)
    body = json.loads(resp.read().decode("utf-8"))
    print("\nPASS POST: /api/calculate -> status", resp.status)
    print("  schemaVersion:", body.get("schemaVersion"))
    print("  capacityKw:", body.get("capacityKw"))
    print("  invKw:", body.get("invKw"))
    print("  plantTotal:", body.get("bom", {}).get("plantTotal"))
    print("  payback:", body.get("payY"), "years", body.get("payM"), "months")
except Exception as e:
    print("\nFAIL POST: /api/calculate ->", e)

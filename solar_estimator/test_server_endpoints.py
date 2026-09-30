import urllib.request
import json

req = urllib.request.urlopen("http://127.0.0.1:5050/")
html = req.read().decode("utf-8")
print("HTTP GET / status:", req.status)
print("Has topbarSites:", 'id="topbarSites"' in html)
print("Has ADD Site+:", "ADD Site +" in html)
print("Has nameGate:", 'id="nameGate"' in html)

payload = json.dumps({
    "mode": "roof",
    "customer_name": "Site Name-1",
    "location": "Shivamogga, Karnataka",
    "email": "client@voltroof.com",
    "length_ft": 40,
    "breadth_ft": 30,
    "parapet_ft": 1.5,
    "monthly_units": 1200,
    "distance_m": 20,
    "panel_watt": 550
}).encode("utf-8")

post_req = urllib.request.Request(
    "http://127.0.0.1:5050/api/download_pdf",
    data=payload,
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(post_req)
pdf_bytes = resp.read()
print("HTTP POST /api/download_pdf (single-site) status:", resp.status)
print("Single-site PDF received bytes:", len(pdf_bytes))

# Test Multi-Site Multi-Building Endpoint Call
multi_payload = json.dumps({
    "mode": "roof",
    "customer_name": "Integrated Multi-Site Portfolio",
    "location": "Karnataka, India",
    "email": "portfolio@voltroof.com",
    "custom_tariff": 8.05,
    "sites": [
        {
            "name": "Shivamogga Campus",
            "location": "Shivamogga, Karnataka",
            "email": "shivamogga@voltroof.com",
            "mode": "roof",
            "distance_m": 25.0,
            "buildings": [
                {"name": "Engineering Block", "length_ft": 45.0, "breadth_ft": 35.0, "parapet_ft": 1.5, "panel_watt": 550},
                {"name": "Science Block", "length_ft": 40.0, "breadth_ft": 30.0, "parapet_ft": 1.5, "panel_watt": 550}
            ]
        },
        {
            "name": "Bengaluru Innovation Hub",
            "location": "Bengaluru, Karnataka",
            "email": "bengaluru@voltroof.com",
            "mode": "roof",
            "distance_m": 15.0,
            "buildings": [
                {"name": "Tower A", "length_ft": 50.0, "breadth_ft": 35.0, "parapet_ft": 1.5, "panel_watt": 550}
            ]
        }
    ]
}).encode("utf-8")

post_req_multi = urllib.request.Request(
    "http://127.0.0.1:5050/api/download_pdf",
    data=multi_payload,
    headers={"Content-Type": "application/json"}
)
resp_multi = urllib.request.urlopen(post_req_multi)
pdf_bytes_multi = resp_multi.read()
print("HTTP POST /api/download_pdf (multi-site) status:", resp_multi.status)
print("Multi-site PDF received bytes:", len(pdf_bytes_multi))
assert resp_multi.status == 200
assert len(pdf_bytes_multi) > 1000000
print("ALL SERVER ENDPOINTS VERIFIED SUCCESSFULLY!")


import urllib.request

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
        print(f"PASS: {u} -> {r.status} ({r.headers.get('Content-Type')})")
    except Exception as e:
        print(f"FAIL: {u} -> {e}")

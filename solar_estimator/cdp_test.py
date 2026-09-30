import subprocess
import time
import urllib.request
import json
import base64
import os

print("Starting Edge with remote debugging...")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
target_url = "file:///C:/Users/DELL/.gemini/antigravity/scratch/solar_estimator/index.html"

# Create a temporary user-data-dir
user_data_dir = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "edge_test_profile")

cmd = [
    edge_path,
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data_dir}",
    "--headless=new",
    "--disable-gpu",
    "--window-size=1400,900",
    target_url
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    # Query DevTools list
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode("utf-8"))
    print("Edge tabs:", len(tabs))
    for t in tabs:
        print("Tab:", t.get("title"), t.get("url"))
finally:
    proc.terminate()
    print("Terminated Edge.")

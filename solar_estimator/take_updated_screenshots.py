# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import time

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d"
downloads_dir = r"C:\Users\DELL\Downloads"
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

port = 5050 # server is already running on 5050

views = [
    ("web_feedback_modal.png", f"http://127.0.0.1:{port}/index.html?view=feedback_modal"),
    ("web_admin_pricing.png", f"http://127.0.0.1:{port}/index.html?view=admin_pricing"),
    ("web_admin_analytics.png", f"http://127.0.0.1:{port}/index.html?view=admin_analytics"),
    ("web_admin_feedback_stream.png", f"http://127.0.0.1:{port}/index.html?view=admin_feedback"),
    ("web_admin_users.png", f"http://127.0.0.1:{port}/index.html?view=admin_users"),
]

for fname, url in views:
    out_path = os.path.join(scratch_dir, fname)
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--window-size=1280,840",
        f"--screenshot={out_path}",
        url
    ]
    subprocess.run(cmd, check=True)
    time.sleep(0.5)
    print(f"Captured: {fname} -> {os.path.getsize(out_path)} bytes")
    shutil.copy2(out_path, os.path.join(brain_dir, fname))
    if os.path.exists(downloads_dir):
        shutil.copy2(out_path, os.path.join(downloads_dir, fname))

print("All updated screenshots captured and synced successfully!")

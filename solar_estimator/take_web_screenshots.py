import os
import sys
import time
import subprocess
import threading
import shutil
from http.server import HTTPServer

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d"
downloads_dir = r"C:\Users\DELL\Downloads"
sys.path.insert(0, scratch_dir)

from solar_pv_estimator import SolarAppRequestHandler

edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def capture():
    port = 5097
    httpd = HTTPServer(("127.0.0.1", port), SolarAppRequestHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(1)

    views = [
        ("web_login_user_manual.png", f"http://127.0.0.1:{port}/index.html"),
        ("web_login_admin_mode.png", f"http://127.0.0.1:{port}/index.html?view=admin_gate"),
        ("web_app_manual_and_admin.png", f"http://127.0.0.1:{port}/index.html?view=studio"),
        ("web_admin_manual_modal.png", f"http://127.0.0.1:{port}/index.html?view=admin_modal")
    ]

    for fname, url in views:
        out_path = os.path.join(scratch_dir, fname)
        cmd = [
            edge_exe,
            "--headless",
            "--disable-gpu",
            "--window-size=1280,820",
            f"--screenshot={out_path}",
            url
        ]
        subprocess.run(cmd, check=True)
        print(f"Captured: {out_path}")
        shutil.copy2(out_path, os.path.join(brain_dir, fname))
        shutil.copy2(out_path, os.path.join(downloads_dir, fname))

    httpd.shutdown()
    print("All UI screenshots captured successfully!")

if __name__ == "__main__":
    capture()

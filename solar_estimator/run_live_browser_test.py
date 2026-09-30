import subprocess
import time
import os
import signal
import solar_pv_estimator
import threading
import sys
import tempfile
import shutil

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run():
    # Start server on 8990
    server = solar_pv_estimator.HTTPServer(('127.0.0.1', 8990), solar_pv_estimator.SolarAppRequestHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print("[Server] Started on http://127.0.0.1:8990")

    # Start Chrome with fresh temp dir & incognito
    temp_dir = tempfile.mkdtemp(prefix="chrome_fresh_")
    chrome_proc = subprocess.Popen([
        CHROME_PATH,
        "--headless=new",
        "--incognito",
        "--remote-debugging-port=9222",
        f"--user-data-dir={temp_dir}",
        "--disable-gpu",
        "--no-first-run",
        "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[Chrome] Started with debugging port 9222, profile {temp_dir}")
    time.sleep(2)

    test_success = False
    try:
        node_res = subprocess.run(
            ["node", "test_master_browser_complete.js"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=40
        )
        print("\n=== COMPLETE BROWSER VERIFICATION OUTPUT ===")
        safe_out = node_res.stdout.encode("ascii", errors="replace").decode("ascii")
        print(safe_out)
        if node_res.stderr:
            safe_err = node_res.stderr.encode("ascii", errors="replace").decode("ascii")
            print("STDERR:\n", safe_err)
        test_success = (node_res.returncode == 0)
    except Exception as e:
        print("Test error:", e)
    finally:
        chrome_proc.terminate()
        try:
            chrome_proc.wait(timeout=3)
        except Exception:
            chrome_proc.kill()
        server.shutdown()
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("[Done] Cleanup complete.")
    
    if not test_success:
        sys.exit(1)

if __name__ == "__main__":
    run()

import subprocess, time, urllib.request, json, socket, base64, os, sys
sys.stdout.reconfigure(encoding='utf-8')

from verify_customer_admin_separation import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9224
html_url = "http://localhost:5050/VoltRoof_Combined.html"

cmd = [
    chrome_path,
    f"--remote-debugging-port={port}",
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--window-size=1400,900",
    html_url
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2.0)
try:
    with urllib.request.urlopen(f"http://localhost:{port}/json", timeout=10) as resp:
        targets = json.loads(resp.read().decode('utf-8'))
    ws_url = targets[0]["webSocketDebuggerUrl"]
    parts = ws_url.replace("ws://", "").split("/")
    host_port = parts[0].split(":")
    ws = SimpleWebSocket(host_port[0], int(host_port[1]), "/" + "/".join(parts[1:]))

    msg_id = 0
    def call_cdp(method, params=None):
        global msg_id
        msg_id += 1
        cid = msg_id
        ws.send_json({"id": cid, "method": method, "params": params or {}})
        while True:
            msg_str = ws.recv_msg()
            if not msg_str:
                return {}
            try:
                data = json.loads(msg_str)
                if data.get('id') == cid:
                    return data.get('result', {})
            except Exception:
                continue

    def eval_js(expr):
        r = call_cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return r.get('result', {}).get('value')

    call_cdp("Console.enable")
    call_cdp("Page.enable")
    time.sleep(1.0)

    # Check for any uncaught errors
    res = call_cdp("Runtime.evaluate", {"expression": "window.__errors || 'none'", "returnByValue": True})
    print("Initial check:", res)

    # Test what enterApp does
    eval_js("enterApp();")
    time.sleep(1.5)

    r_greet = eval_js("document.querySelector('.ribbon-greet') ? document.querySelector('.ribbon-greet').innerText : 'NOT_FOUND'")
    print("ribbon-greet innerText:", r_greet)

    r_greet_html = eval_js("document.querySelector('.ribbon-greet') ? document.querySelector('.ribbon-greet').outerHTML : 'NOT_FOUND'")
    print("ribbon-greet HTML:", r_greet_html)

    r_body_class = eval_js("document.body.className")
    print("body className:", r_body_class)

    r_cnav = eval_js("document.getElementById('customerNavSec') ? window.getComputedStyle(document.getElementById('customerNavSec')).display : 'NO_CNAV'")
    print("customerNavSec display:", r_cnav)

    r_anav = eval_js("document.getElementById('adminNavSec') ? window.getComputedStyle(document.getElementById('adminNavSec')).display : 'NO_ANAV'")
    print("adminNavSec display:", r_anav)

finally:
    proc.kill()

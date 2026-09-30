import subprocess, time, urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from verify_customer_admin_separation import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9227
ts = int(time.time())
html_url = f"http://localhost:5050/VoltRoof_Combined.html?nocache={ts}"
user_data_dir = f"C:\\Users\\DELL\\.gemini\\antigravity\\scratch\\solar_estimator\\chrome_chk_{ts}"

cmd = [
    chrome_path,
    f"--remote-debugging-port={port}",
    f"--user-data-dir={user_data_dir}",
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

    call_cdp("Page.enable")
    time.sleep(1.0)

    print("Initial cnav:", eval_js("document.getElementById('customerNavSec') ? 'EXISTS' : 'NO'"))
    print("Initial anav:", eval_js("document.getElementById('adminNavSec') ? 'EXISTS' : 'NO'"))
    print("Initial ribbon-greet:", eval_js("document.querySelector('.ribbon-greet') ? document.querySelector('.ribbon-greet').innerText : 'NO'"))

    # Now enter app as customer
    eval_js("enterApp();")
    time.sleep(1.5)

    print("After enterApp ribbon-greet:", eval_js("document.querySelector('.ribbon-greet') ? document.querySelector('.ribbon-greet').innerText : 'NO'"))
    print("After enterApp cnav display:", eval_js("window.getComputedStyle(document.getElementById('customerNavSec')).display"))
    print("After enterApp anav display:", eval_js("window.getComputedStyle(document.getElementById('adminNavSec')).display"))

finally:
    proc.kill()

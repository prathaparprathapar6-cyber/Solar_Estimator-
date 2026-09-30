import subprocess, time, urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from verify_customer_admin_separation import SimpleWebSocket

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9228
ts = int(time.time())
html_url = f"http://localhost:5050/VoltRoof_Combined.html?nocache={ts}"
user_data_dir = f"C:\\Users\\DELL\\.gemini\antigravity\\scratch\\solar_estimator\\chrome_chk_{ts}"

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
    page_target = next(t for t in targets if t.get('type') == 'page')
    ws_url = page_target['webSocketDebuggerUrl']
    parts = ws_url.split('/')
    host_port = parts[2].split(':')
    ws = SimpleWebSocket(host_port[0], int(host_port[1]), '/' + '/'.join(parts[3:]))

    call_id = 1
    def call_cdp(method, params=None):
        global call_id
        cid = call_id
        call_id += 1
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

    def eval_js(expr, await_promise=False):
        r = call_cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": await_promise})
        return r.get('result', {}).get('value')

    call_cdp("Page.enable")
    time.sleep(1.0)

    # Log in as admin
    eval_js("document.getElementById('gateAdminUser').value = 'admin';")
    eval_js("document.getElementById('gateAdminPass').value = 'admin123';")
    r_auth = eval_js("await loginAdminCore('admin', 'admin123');", await_promise=True)
    print("Direct loginAdminCore result:", r_auth)

    eval_js("localStorage.setItem('voltroof_admin_session', JSON.stringify({username: 'admin', role: 'super_admin', displayName: 'Adarsha KM'}));")
    eval_js("enterAdminPortal();")
    time.sleep(0.5)

    print("Active class on view-adminDashboard:", eval_js("document.getElementById('view-adminDashboard').className"))
    print("Computed display on view-adminDashboard:", eval_js("window.getComputedStyle(document.getElementById('view-adminDashboard')).display"))
    print("Inline style on view-adminDashboard:", eval_js("document.getElementById('view-adminDashboard').style.display"))

finally:
    proc.kill()

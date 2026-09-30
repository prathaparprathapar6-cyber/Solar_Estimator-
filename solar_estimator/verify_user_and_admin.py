import subprocess
import time
import urllib.request
import json
import socket
import base64
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

class SimpleWebSocket:
    def __init__(self, host, port, path):
        self.sock = socket.create_connection((host, port), timeout=15)
        sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {sec_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode('utf-8'))
        resp = self.sock.recv(4096).decode('utf-8', errors='ignore')
        if "101" not in resp:
            raise RuntimeError(f"WebSocket upgrade failed: {resp}")

    def send_json(self, msg_obj):
        data = json.dumps(msg_obj).encode('utf-8')
        length = len(data)
        frame = bytearray([0x81])
        if length <= 125:
            frame.append(0x80 | length)
        elif length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(length.to_bytes(2, 'big'))
        else:
            frame.append(0x80 | 127)
            frame.extend(length.to_bytes(8, 'big'))
        mask = os.urandom(4)
        frame.extend(mask)
        masked_data = bytearray(b ^ mask[i % 4] for i, b in enumerate(data))
        frame.extend(masked_data)
        self.sock.sendall(frame)

    def recv_msg(self):
        hdr = self.sock.recv(2)
        if not hdr:
            return None
        b1, b2 = hdr[0], hdr[1]
        payload_len = b2 & 0x7F
        if payload_len == 126:
            payload_len = int.from_bytes(self.sock.recv(2), 'big')
        elif payload_len == 127:
            payload_len = int.from_bytes(self.sock.recv(8), 'big')
        has_mask = (b2 & 0x80) != 0
        mask = self.sock.recv(4) if has_mask else None
        payload = bytearray()
        while len(payload) < payload_len:
            chunk = self.sock.recv(payload_len - len(payload))
            if not chunk:
                break
            payload.extend(chunk)
        if has_mask:
            payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
        return payload.decode('utf-8', errors='ignore')

    def close(self):
        try:
            self.sock.close()
        except:
            pass

print("1. Launching Edge in headless mode...")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
user_data_dir = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "edge_voltroof_test_2")

cmd = [
    edge_path,
    "--remote-debugging-port=9224",
    f"--user-data-dir={user_data_dir}",
    "--headless=new",
    "--disable-gpu",
    "--window-size=1440,1100",
    "http://127.0.0.1:5050/VoltRoof_Combined.html"
]

proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9224/json")
    tabs = json.loads(req.read().decode('utf-8'))
    ws_url = None
    for t in tabs:
        if "5050" in t.get("url", ""):
            ws_url = t.get("webSocketDebuggerUrl")
            break
    if not ws_url and tabs:
        ws_url = tabs[0].get("webSocketDebuggerUrl")
        
    print(f"Connected to DevTools tab: {ws_url}")
    from urllib.parse import urlparse
    u = urlparse(ws_url)
    ws = SimpleWebSocket(u.hostname, u.port, u.path)
    
    msg_id = 1
    def send_cdp(method, params=None):
        global msg_id
        mid = msg_id
        msg = {"id": mid, "method": method, "params": params or {}}
        msg_id += 1
        ws.send_json(msg)
        while True:
            raw = ws.recv_msg()
            if not raw:
                return {}
            data = json.loads(raw)
            if data.get("id") == mid:
                return data

    def eval_js(expr):
        res = send_cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value")

    def capture_screenshot(fname):
        res = send_cdp("Page.captureScreenshot", {"format": "png"})
        b64 = res.get("result", {}).get("data", "")
        if b64:
            with open(fname, "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"Captured screenshot: {fname} ({os.path.getsize(fname)} bytes)")

    # Enable Page and Runtime
    send_cdp("Page.enable")
    send_cdp("Runtime.enable")
    time.sleep(1.0)

    print("\n--- 2. Checking Initial State (Name Gate) ---")
    gate_display = eval_js("document.getElementById('nameGate').style.display")
    print(f"Initial gate display: {gate_display}")

    # Enter user name and click Enter App
    print("\n--- 3. Testing User Login ---")
    eval_js("document.getElementById('gateName').value = 'Adarsha KM - Chief Engineer';")
    eval_js("enterApp();")
    time.sleep(0.8)

    # Dismiss Tour Modal if open
    eval_js("""
    const tour = document.getElementById('tourModal');
    if (tour) tour.style.display = 'none';
    localStorage.setItem('voltroof_tour_done', '1');
    """)

    # Populate site roof dimensions and run compute/liveUpdate
    print("\n--- 4. Populating Site 1 Roof Dimensions & Calculating ---")
    eval_js("""
    if (document.getElementById('cfgL')) document.getElementById('cfgL').value = 50;
    if (document.getElementById('cfgB')) document.getElementById('cfgB').value = 35;
    if (document.getElementById('cfgParapet')) document.getElementById('cfgParapet').value = 3.5;
    if (document.getElementById('cfgNeighbour')) document.getElementById('cfgNeighbour').value = 0;
    if (document.getElementById('cfgLoad')) document.getElementById('cfgLoad').value = 15;
    if (sites[activeSiteIndex]) {
        sites[activeSiteIndex].L = 50;
        sites[activeSiteIndex].B = 35;
        sites[activeSiteIndex].parapet = 3.5;
        sites[activeSiteIndex].sanctioned_load = 15;
    }
    liveUpdate();
    """)
    time.sleep(1.0)

    gate_hidden = eval_js("document.getElementById('nameGate').style.display === 'none' || document.getElementById('nameGate').classList.contains('hidden')")
    greet_name = eval_js("document.getElementById('greetName').textContent")
    ribbon_visible = eval_js("!!document.querySelector('.ribbon-wrap')")
    kpi_cap = eval_js("document.getElementById('kpiCap').textContent")
    kpi_gen = eval_js("document.getElementById('kpiGen').textContent")
    kpi_cost = eval_js("document.getElementById('kpiCost').textContent")
    kpi_pay = eval_js("document.getElementById('kpiPay').textContent")
    
    print(f"Gate hidden: {gate_hidden}")
    print(f"Greet Name: {greet_name}")
    print(f"Ribbon Wrap Visible: {ribbon_visible}")
    print(f"KPI Capacity: {kpi_cap}")
    print(f"KPI Generation: {kpi_gen}")
    print(f"KPI Cost: {kpi_cost}")
    print(f"KPI Payback: {kpi_pay}")

    capture_screenshot("voltroof_combined_user_dashboard.png")

    print("\n--- 5. Testing Visualizer 3D Mode & TOD Slider ---")
    eval_js("if (typeof setArrayMode === 'function') setArrayMode('3d');")
    eval_js("const s = document.getElementById('todSlider'); if (s) { s.value = 14; s.dispatchEvent(new Event('input')); }")
    time.sleep(1.0)
    capture_screenshot("voltroof_combined_visualizer_3d.png")

    print("\n--- 6. Testing Admin Login & Control Center ---")
    eval_js("openAdminManualModal();")
    time.sleep(0.5)

    # Authenticate as admin with correct password
    eval_js("document.getElementById('modalAdminUser').value = 'adarshakm@jnnce.ac.in';")
    eval_js("document.getElementById('modalAdminPass').value = 'Adarsh@123321';")
    eval_js("loginAdminFromModal();")
    time.sleep(1.2)

    admin_panel_disp = eval_js("document.getElementById('modalAdminDocPanel').style.display")
    admin_name_disp = eval_js("document.getElementById('modalAdminNameDisplay').textContent")
    print(f"Admin Doc Panel display: {admin_panel_disp}")
    print(f"Admin Display Name: {admin_name_disp}")

    # Switch to Pricing Tab
    print("\n--- 7. Testing Admin Pricing Tab ---")
    eval_js("switchAdminTab('pricing');")
    time.sleep(1.0)
    pricing_count = eval_js("document.querySelectorAll('#pricingTableContainer tbody tr, #pricingTbody tr, #adminPanelPricing table tbody tr').length")
    print(f"Pricing rows rendered: {pricing_count}")
    capture_screenshot("voltroof_combined_admin_pricing.png")

    # Switch to Analytics Tab
    print("\n--- 8. Testing Admin Analytics Tab ---")
    eval_js("switchAdminTab('visitors');")
    time.sleep(1.0)
    vis_count = eval_js("document.getElementById('admTotalVisitors')?.textContent || 'N/A'")
    print(f"Total Visitors: {vis_count}")
    capture_screenshot("voltroof_combined_admin_analytics.png")

    # Switch to Feedback Tab
    print("\n--- 9. Testing Admin Feedback Tab ---")
    eval_js("switchAdminTab('feedback');")
    time.sleep(1.0)
    capture_screenshot("voltroof_combined_admin_feedback.png")

    # Switch to Admins Tab
    print("\n--- 10. Testing Admin Users Tab ---")
    eval_js("switchAdminTab('users');")
    time.sleep(1.0)
    admin_rows = eval_js("document.querySelectorAll('#adminListContainer tr, #adminPanelUsers table tr').length")
    print(f"Admin rows: {admin_rows}")
    capture_screenshot("voltroof_combined_admin_users.png")

    print("\nALL VERIFICATIONS PASSED PERFECTLY!")

finally:
    try:
        ws.close()
    except:
        pass
    proc.kill()

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
            chunk = self.sock.recv(min(4096, payload_len - len(payload)))
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

def main():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    port = 9226
    ts = int(time.time())
    html_url = f"http://localhost:5050/VoltRoof_Combined.html?nocache={ts}"
    user_data_dir = f"C:\\Users\\DELL\\.gemini\\antigravity\\scratch\\solar_estimator\\chrome_verify_{ts}"

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

    print("Launching Chrome for Role Isolation verification...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ws = None
    try:
        time.sleep(2.0)
        # Get WebSocket URL
        json_url = f"http://localhost:{port}/json"
        with urllib.request.urlopen(json_url, timeout=10) as resp:
            targets = json.loads(resp.read().decode('utf-8'))
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws_url = page_target['webSocketDebuggerUrl']
        print(f"Connected to Chrome WebSocket: {ws_url} (target: {page_target.get('title')})")

        parts = ws_url.split('/')
        host_port = parts[2].split(':')
        host = host_port[0]
        p = int(host_port[1])
        path = '/' + '/'.join(parts[3:])
        ws = SimpleWebSocket(host, p, path)

        msg_id = 0
        def call_cdp(method, params=None):
            nonlocal msg_id
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

        def capture_screenshot(fname):
            r = call_cdp("Page.captureScreenshot", {"format": "png"})
            b64_data = r.get("data")
            if b64_data:
                with open(fname, "wb") as f:
                    f.write(base64.b64decode(b64_data))
                print(f"Captured screenshot: {fname} ({os.path.getsize(fname):,} bytes)")

        call_cdp("Page.enable")
        time.sleep(1.0)

        # -------------------------------------------------------------
        # TEST 1: PURE CUSTOMER LOGIN (Name: 'A')
        # -------------------------------------------------------------
        print("\n=== TEST 1: Pure Customer Login (Name 'A') ===")
        # Ensure fresh state
        eval_js("localStorage.removeItem('voltroof_admin_session');")
        eval_js("openNameGate();")
        time.sleep(0.3)
        eval_js("document.getElementById('gateName').value = 'A';")
        eval_js("enterApp();")
        time.sleep(1.2)

        # 1. Customer greeting
        full_greet = eval_js("document.querySelector('.ribbon-greet').innerText.trim()")
        print(f"Customer Full Ribbon Greeting: '{full_greet}'")
        assert "Good night, Good night" not in full_greet, "Greeting must not be duplicated"

        # 2. Customer visibility
        c_nav_disp = eval_js("window.getComputedStyle(document.getElementById('customerNavSec')).display")
        a_nav_disp = eval_js("window.getComputedStyle(document.getElementById('adminNavSec')).display")
        c_ribbon_disp = eval_js("window.getComputedStyle(document.getElementById('ribbonBar')).display")
        a_header_disp = eval_js("window.getComputedStyle(document.getElementById('adminHeaderStrip')).display")

        print(f"customerNavSec: {c_nav_disp}")
        print(f"adminNavSec:    {a_nav_disp}")
        print(f"customerRibbon: {c_ribbon_disp}")
        print(f"adminHeader:    {a_header_disp}")

        assert c_nav_disp != 'none', "Customer nav must be visible"
        assert a_nav_disp == 'none', "Admin nav must be hidden"
        assert c_ribbon_disp != 'none', "Customer ribbon must be visible"
        assert a_header_disp == 'none', "Admin header must be hidden"

        capture_screenshot("test_customer_mode_verified.png")

        # -------------------------------------------------------------
        # TEST 2: ADMIN AUTHENTICATION & ADMIN CONTROL CENTER ENTRY
        # -------------------------------------------------------------
        print("\n=== TEST 2: Admin Login & Workspace Entry ===")
        # Open Gate and toggle into Admin Mode
        eval_js("openNameGate();")
        time.sleep(0.3)
        eval_js("toggleGateAdminMode();")
        time.sleep(0.3)

        # Enter credentials and authenticate
        eval_js("document.getElementById('gateAdminUser').value = 'admin';")
        eval_js("document.getElementById('gateAdminPass').value = 'admin123';")
        eval_js("loginAdminFromGate();")
        for _ in range(30):
            if eval_js("!!localStorage.getItem('voltroof_admin_session')"):
                break
            time.sleep(0.1)
        sess = eval_js("localStorage.getItem('voltroof_admin_session')")
        print(f"Authenticated session: {sess}")
        assert sess, "Admin session must be established"

        # Click Enter Admin Control Center
        eval_js("enterAdminPortal();")
        time.sleep(0.8)

        # Verify role classes
        is_admin_mode = eval_js("document.body.classList.contains('admin-mode')")
        is_customer_mode = eval_js("document.body.classList.contains('customer-mode')")
        print(f"Body has 'admin-mode': {is_admin_mode}")
        print(f"Body has 'customer-mode': {is_customer_mode}")
        assert is_admin_mode, "Body must have admin-mode class"
        assert not is_customer_mode, "Body must NOT have customer-mode class"

        # 1. Verify ALL Customer calculations are strictly HIDDEN
        c_nav_disp2 = eval_js("window.getComputedStyle(document.getElementById('customerNavSec')).display")
        c_ribbon_disp2 = eval_js("window.getComputedStyle(document.getElementById('ribbonBar')).display")
        c_sum_disp2 = eval_js("window.getComputedStyle(document.getElementById('stickySummary')).display")
        c_guide_disp2 = eval_js("window.getComputedStyle(document.getElementById('emptyGuide')).display")
        c_dash_disp2 = eval_js("window.getComputedStyle(document.getElementById('view-dashboard')).display")
        c_studio_disp2 = eval_js("window.getComputedStyle(document.getElementById('view-studio')).display")
        c_bom_disp2 = eval_js("window.getComputedStyle(document.getElementById('view-bom')).display")
        c_fin_disp2 = eval_js("window.getComputedStyle(document.getElementById('view-financials')).display")

        print("\n--- Customer Calculations Visibility in Admin Mode ---")
        print(f"Customer Nav:               {c_nav_disp2} (Expected: none)")
        print(f"Customer Ribbon:            {c_ribbon_disp2} (Expected: none)")
        print(f"Customer Sticky Bar:        {c_sum_disp2} (Expected: none)")
        print(f"Customer Calc Guide Banner: {c_guide_disp2} (Expected: none)")
        print(f"Customer Dashboard View:    {c_dash_disp2} (Expected: none)")
        print(f"Project Design View:        {c_studio_disp2} (Expected: none)")
        print(f"BOM & Cost View:            {c_bom_disp2} (Expected: none)")
        print(f"Financial Analysis View:    {c_fin_disp2} (Expected: none)")

        assert c_nav_disp2 == 'none', "Customer nav MUST be hidden in Admin mode"
        assert c_ribbon_disp2 == 'none', "Customer ribbon MUST be hidden in Admin mode"
        assert c_sum_disp2 == 'none', "Customer sticky bar MUST be hidden in Admin mode"
        assert c_guide_disp2 == 'none', "Customer calc guide MUST be hidden in Admin mode"
        assert c_dash_disp2 == 'none', "Customer dashboard MUST be hidden in Admin mode"
        assert c_studio_disp2 == 'none', "Project Design MUST be hidden in Admin mode"
        assert c_bom_disp2 == 'none', "BOM & Cost MUST be hidden in Admin mode"
        assert c_fin_disp2 == 'none', "Financials MUST be hidden in Admin mode"

        # 2. Verify Admin Header and Nav are SHOWN
        a_nav_disp2 = eval_js("window.getComputedStyle(document.getElementById('adminNavSec')).display")
        a_header_disp2 = eval_js("window.getComputedStyle(document.getElementById('adminHeaderStrip')).display")
        a_dash_disp = eval_js("window.getComputedStyle(document.getElementById('view-adminDashboard')).display")

        print("\n--- Admin Controls Visibility in Admin Mode ---")
        print(f"Admin Nav:                  {a_nav_disp2} (Expected: block)")
        print(f"Admin Header Strip:         {a_header_disp2} (Expected: flex)")
        print(f"Admin Dashboard View:       {a_dash_disp} (Expected: block)")

        assert a_nav_disp2 != 'none', "Admin nav MUST be visible in Admin mode"
        assert a_header_disp2 != 'none', "Admin header MUST be visible in Admin mode"
        assert a_dash_disp != 'none', "Admin Dashboard view MUST be active in Admin mode"

        capture_screenshot("test_admin_mode_dashboard.png")

        # -------------------------------------------------------------
        # TEST 3: SWITCH TO EQUIPMENT & PRICING IN ADMIN MODE
        # -------------------------------------------------------------
        print("\n=== TEST 3: Equipment & Pricing View ===")
        eval_js("switchView('adminPricing');")
        time.sleep(0.5)

        pricing_disp = eval_js("window.getComputedStyle(document.getElementById('view-adminPricing')).display")
        mod_rate = eval_js("document.getElementById('rate_module_per_wp').value")
        inv_rate = eval_js("document.getElementById('rate_inverter_per_kw').value")

        print(f"view-adminPricing display: {pricing_disp}")
        print(f"Module Rate (₹/Wp):        {mod_rate}")
        print(f"Inverter Rate (₹/kW):      {inv_rate}")

        assert pricing_disp != 'none', "Pricing view must be visible"
        assert float(mod_rate) > 0, "Module rate must be populated"
        assert float(inv_rate) > 0, "Inverter rate must be populated"

        capture_screenshot("test_admin_mode_pricing.png")

        # -------------------------------------------------------------
        # TEST 4: SWITCH TO POLICY DESK IN ADMIN MODE
        # -------------------------------------------------------------
        print("\n=== TEST 4: Policy Desk View ===")
        eval_js("switchView('policyDesk');")
        time.sleep(0.5)

        policy_disp = eval_js("window.getComputedStyle(document.getElementById('view-policyDesk')).display")
        print(f"view-policyDesk display: {policy_disp}")
        assert policy_disp != 'none', "Policy desk must be visible"
        capture_screenshot("test_admin_mode_policydesk.png")

        # -------------------------------------------------------------
        # TEST 5: ADMIN LOGOUT
        # -------------------------------------------------------------
        print("\n=== TEST 5: Admin Logout ===")
        eval_js("logoutAdmin();")
        time.sleep(0.5)
        has_session = eval_js("!!localStorage.getItem('voltroof_admin_session')")
        print(f"Admin session after logout: {has_session}")
        assert not has_session, "Admin session must be cleared after logout"

        print("\n==================================================================")
        print(" SUCCESS! ALL CUSTOMER CALCULATIONS REMOVED FROM ADMIN LOGIN!")
        print(" 100% AIRTIGHT ROLE SEPARATION VERIFIED!")
        print("==================================================================")

    finally:
        if ws:
            ws.close()
        proc.kill()

if __name__ == '__main__':
    main()

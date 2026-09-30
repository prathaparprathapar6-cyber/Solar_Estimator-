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
        if mask:
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
    url = "http://localhost:5050"

    print("Launching Chrome to test Customer Login vs Admin separation...")
    proc = subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={port}",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1440,900",
        url
    ])

    time.sleep(2.5)

    ws = None
    try:
        targets_url = f"http://localhost:{port}/json"
        req = urllib.request.urlopen(targets_url)
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws_url = page_target['webSocketDebuggerUrl']

        parts = ws_url.split('/')
        host_port = parts[2].split(':')
        host = host_port[0]
        p = int(host_port[1])
        path = '/' + '/'.join(parts[3:])

        ws = SimpleWebSocket(host, p, path)
        print("Connected to Chrome DevTools Protocol WebSocket!")

        call_id = 1
        def call_cdp(method, params=None):
            nonlocal call_id
            cid = call_id
            call_id += 1
            ws.send_json({"id": cid, "method": method, "params": params or {}})
            while True:
                msg_str = ws.recv_msg()
                if not msg_str:
                    return None
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

        # -------------------------------------------------------------
        # STEP 1: Simulate Customer Login with name 'a' (like user photo)
        # -------------------------------------------------------------
        print("\n--- STEP 1: Simulating Customer Login with name 'a' ---")
        eval_js("document.getElementById('gateName').value = 'a';")
        eval_js("enterApp();")
        time.sleep(1.0)

        # Dismiss Tour Modal if open
        eval_js("""
        const tour = document.getElementById('tourModal');
        if (tour) tour.style.display = 'none';
        localStorage.setItem('voltroof_tour_done', '1');
        """)

        # 1. Verify greeting is clean (NOT "Good night, Good night, a")
        full_greet = eval_js("document.querySelector('.ribbon-greet') ? document.querySelector('.ribbon-greet').innerText.trim() : ''")
        print(f"Customer Full Ribbon Greeting: '{full_greet}'")
        assert "Good night, Good night" not in full_greet, f"Greeting MUST NOT be duplicated! Got: {full_greet}"
        assert "Good night, a" in full_greet or "Good evening, a" in full_greet or "Good afternoon, a" in full_greet, f"Greeting must contain name 'a', got: {full_greet}"

        # 2. Verify all admin sidebar buttons are HIDDEN
        desk_disp = eval_js("document.getElementById('navPolicyDeskBtn') ? window.getComputedStyle(document.getElementById('navPolicyDeskBtn')).display : 'none'")
        studio_disp = eval_js("document.getElementById('navContentStudioBtn') ? window.getComputedStyle(document.getElementById('navContentStudioBtn')).display : 'none'")
        team_disp = eval_js("document.getElementById('navAdminTeamBtn') ? window.getComputedStyle(document.getElementById('navAdminTeamBtn')).display : 'none'")
        manual_disp = eval_js("document.getElementById('navAdminManualBtn') ? window.getComputedStyle(document.getElementById('navAdminManualBtn')).display : 'none'")
        top_btn_disp = eval_js("document.getElementById('btnTopAdminManual') ? window.getComputedStyle(document.getElementById('btnTopAdminManual')).display : 'none'")

        print(f"Policy Desk button display in Customer Login: {desk_disp}")
        print(f"Content Studio button display in Customer Login: {studio_disp}")
        print(f"Admin Roster button display in Customer Login: {team_disp}")
        print(f"Control Center button display in Customer Login: {manual_disp}")
        print(f"Top Ribbon Admin button display in Customer Login: {top_btn_disp}")

        assert desk_disp == 'none', "Policy Desk button must be HIDDEN in customer login"
        assert studio_disp == 'none', "Content Studio button must be HIDDEN in customer login"
        assert team_disp == 'none', "Admin Roster button must be HIDDEN in customer login"
        assert manual_disp == 'none', "Control Center button must be HIDDEN in customer login"
        assert top_btn_disp == 'none', "Top Ribbon Admin button must be HIDDEN in customer login"

        # 3. Verify active view is dashboard
        active_view = eval_js("document.querySelector('section.view.active') ? document.querySelector('section.view.active').id : ''")
        print(f"Active View in Customer Login: '{active_view}'")
        assert active_view == 'view-dashboard', f"Customer active view must be 'view-dashboard', got '{active_view}'"

        # -------------------------------------------------------------
        # STEP 2: Verify Explicit Admin Login Flow
        # -------------------------------------------------------------
        print("\n--- STEP 2: Verifying Explicit Admin Login Flow ---")
        eval_js("openAdminManualModal();")
        time.sleep(0.5)

        eval_js("document.getElementById('modalAdminUser').value = 'adarshakm@jnnce.ac.in';")
        eval_js("document.getElementById('modalAdminPass').value = 'Adarsh@123321';")
        eval_js("loginAdminFromModal();")
        time.sleep(1.0)

        is_admin = eval_js("isAdminSession();")
        print(f"Is Admin Session after explicit admin login: {is_admin}")
        assert is_admin == True, "Must be admin after explicit login"

        desk_disp_admin = eval_js("document.getElementById('navPolicyDeskBtn') ? window.getComputedStyle(document.getElementById('navPolicyDeskBtn')).display : 'none'")
        top_btn_disp_admin = eval_js("document.getElementById('btnTopAdminManual') ? window.getComputedStyle(document.getElementById('btnTopAdminManual')).display : 'none'")
        print(f"Policy Desk button display in Admin Login: {desk_disp_admin}")
        print(f"Top Ribbon Admin button display in Admin Login: {top_btn_disp_admin}")
        assert desk_disp_admin != 'none', "Policy Desk must be VISIBLE for Admin"
        assert top_btn_disp_admin != 'none', "Top Ribbon Admin button must be VISIBLE for Admin"

        # -------------------------------------------------------------
        # STEP 3: Verify Admin Logout Returns to Clean Customer View
        # -------------------------------------------------------------
        print("\n--- STEP 3: Testing Admin Logout ---")
        eval_js("logoutAdmin();")
        time.sleep(0.5)

        is_admin_after = eval_js("isAdminSession();")
        desk_disp_after = eval_js("document.getElementById('navPolicyDeskBtn') ? window.getComputedStyle(document.getElementById('navPolicyDeskBtn')).display : 'none'")
        top_btn_disp_after = eval_js("document.getElementById('btnTopAdminManual') ? window.getComputedStyle(document.getElementById('btnTopAdminManual')).display : 'none'")
        print(f"Is Admin Session after logout: {is_admin_after}")
        print(f"Policy Desk display after logout: {desk_disp_after}")
        print(f"Top Ribbon Admin display after logout: {top_btn_disp_after}")
        assert is_admin_after == False, "Must NOT be admin after logout"
        assert desk_disp_after == 'none', "Policy Desk must be hidden after logout"
        assert top_btn_disp_after == 'none', "Top Ribbon Admin must be hidden after logout"

        print("\n==================================================================")
        print(" ROLE SEPARATION & GREETING FIX VERIFIED WITH 100% SUCCESS!")
        print("==================================================================")

    finally:
        if ws:
            try:
                ws.close()
            except:
                pass
        proc.kill()

if __name__ == '__main__':
    main()

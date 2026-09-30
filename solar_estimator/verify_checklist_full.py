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
    port = 9227
    url = "http://localhost:5050"

    print("Launching Chrome for full checklist verification...")
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
        # CHECKLIST ITEM 1: Open HTML -> click Admin -> see ADMIN SESSION + user/pass
        # -------------------------------------------------------------
        print("\n=== Checklist Item 1: Gate Admin Toggle ===")
        gate_disp = eval_js("window.getComputedStyle(document.getElementById('nameGate')).display")
        assert gate_disp in ('flex', 'block'), "Gate must be visible"

        # Click Admin button
        eval_js("toggleGateAdminMode();")
        time.sleep(0.3)

        client_mode_disp = eval_js("document.getElementById('gateClientMode').style.display")
        admin_mode_disp = eval_js("document.getElementById('gateAdminMode').style.display")
        badge_txt = eval_js("document.getElementById('loginAdminBadge').innerText")
        print(f"gateClientMode display: {client_mode_disp}")
        print(f"gateAdminMode display: {admin_mode_disp}")
        print(f"Badge text: '{badge_txt}'")
        assert client_mode_disp == 'none', "gateClientMode must be hidden"
        assert admin_mode_disp == 'block', "gateAdminMode must be shown"
        assert "ADMIN SESSION" in badge_txt, "Badge must say ADMIN SESSION"
        capture_screenshot("checklist_1_gate_admin_mode.png")

        # -------------------------------------------------------------
        # CHECKLIST ITEM 2: Cancel -> back to name-only user login
        # -------------------------------------------------------------
        print("\n=== Checklist Item 2: Cancel back to user login ===")
        eval_js("toggleGateAdminMode();")
        time.sleep(0.3)
        client_mode_disp = eval_js("document.getElementById('gateClientMode').style.display")
        admin_mode_disp = eval_js("document.getElementById('gateAdminMode').style.display")
        print(f"gateClientMode display after cancel: {client_mode_disp}")
        print(f"gateAdminMode display after cancel: {admin_mode_disp}")
        assert client_mode_disp == 'block', "gateClientMode must be shown again"
        assert admin_mode_disp == 'none', "gateAdminMode must be hidden again"

        # -------------------------------------------------------------
        # CHECKLIST ITEM 3: Invalid Admin Credentials -> toast, no session
        # -------------------------------------------------------------
        print("\n=== Checklist Item 3: Invalid admin credentials ===")
        eval_js("toggleGateAdminMode();")
        eval_js("document.getElementById('gateAdminUser').value = 'wrong@admin.com';")
        eval_js("document.getElementById('gateAdminPass').value = 'wrongpass';")
        eval_js("loginAdminFromGate();")
        time.sleep(0.5)

        has_sess = eval_js("!!localStorage.getItem('voltroof_admin_session')")
        print(f"Admin session stored after invalid login: {has_sess}")
        assert has_sess == False, "Session must NOT be stored for invalid credentials"

        # -------------------------------------------------------------
        # CHECKLIST ITEM 4: Valid Built-in Admin Login -> session stored
        # -------------------------------------------------------------
        print("\n=== Checklist Item 4: Valid Built-in Admin Login ===")
        eval_js("document.getElementById('gateAdminUser').value = 'adarshakm@jnnce.ac.in';")
        eval_js("document.getElementById('gateAdminPass').value = 'Adarsh@123321';")
        eval_js("loginAdminFromGate();")
        time.sleep(1.0)

        has_sess = eval_js("!!localStorage.getItem('voltroof_admin_session')")
        admin_doc_disp = eval_js("document.getElementById('gateAdminDocPanel').style.display")
        admin_display_name = eval_js("document.getElementById('gateAdminNameDisplay').innerText")
        print(f"Admin session stored: {has_sess}")
        print(f"gateAdminDocPanel display: {admin_doc_disp}")
        print(f"Admin display name on gate: '{admin_display_name}'")
        assert has_sess == True, "Admin session must be stored"
        assert admin_doc_disp == 'block', "gateAdminDocPanel must be visible on gate"
        assert "Adarsha KM" in admin_display_name, "Must display Adarsha KM"
        capture_screenshot("checklist_4_admin_authenticated_on_gate.png")

        # Now enter app as admin via enterAppAdmin()
        eval_js("enterAppAdmin();")
        time.sleep(1.2)

        desk_disp_admin = eval_js("window.getComputedStyle(document.getElementById('navPolicyDeskBtn')).display")
        top_btn_disp_admin = eval_js("window.getComputedStyle(document.getElementById('btnTopAdminManual')).display")
        top_btn_label = eval_js("document.getElementById('btnTopAdminManualLabel').innerText")
        print(f"Admin navigation in Admin Session:")
        print(f"  Policy Desk display: {desk_disp_admin}")
        print(f"  Top Ribbon Admin display: {top_btn_disp_admin} (label: '{top_btn_label}')")
        assert desk_disp_admin != 'none', "Policy Desk must be VISIBLE in admin session"
        assert top_btn_disp_admin != 'none', "Top Ribbon Admin must be VISIBLE in admin session"
        assert "Adarsha" in top_btn_label, f"Label must show Adarsha, got '{top_btn_label}'"
        capture_screenshot("checklist_4_admin_logged_in_dashboard.png")

        # -------------------------------------------------------------
        # CHECKLIST ITEM 5: Logout -> admin nav hidden, form reset
        # -------------------------------------------------------------
        print("\n=== Checklist Item 5: Logout resets navigation ===")
        eval_js("logoutAdmin();")
        time.sleep(0.5)

        has_sess_after = eval_js("!!localStorage.getItem('voltroof_admin_session')")
        desk_disp_logout = eval_js("window.getComputedStyle(document.getElementById('navPolicyDeskBtn')).display")
        top_btn_disp_logout = eval_js("window.getComputedStyle(document.getElementById('btnTopAdminManual')).display")
        print(f"Admin session after logout: {has_sess_after}")
        print(f"Policy Desk display after logout: {desk_disp_logout}")
        print(f"Top Ribbon Admin display after logout: {top_btn_disp_logout}")
        assert has_sess_after == False, "Session must be cleared on logout"
        assert desk_disp_logout == 'none', "Policy Desk must be hidden after logout"
        assert top_btn_disp_logout == 'none', "Top Ribbon Admin button must be hidden after logout"

        # -------------------------------------------------------------
        # CHECKLIST ITEM 6: Customer Login with name 'A' (The user's exact case!)
        # -------------------------------------------------------------
        print("\n=== Checklist Item 6: Pure Customer Login with name 'A' ===")
        # Re-open gate
        eval_js("openNameGate();")
        time.sleep(0.5)

        # Enter name 'A' and enter studio as customer
        eval_js("document.getElementById('gateName').value = 'A';")
        eval_js("enterApp();")
        time.sleep(1.2)

        # 1. Verify greeting is clean (NOT "Good night, Good night, A")
        full_greet = eval_js("document.querySelector('.ribbon-greet').innerText.trim()")
        print(f"Customer Full Ribbon Greeting: '{full_greet}'")
        assert "Good night, Good night" not in full_greet, f"Greeting MUST NOT be duplicated! Got: {full_greet}"
        assert "A" in full_greet, f"Greeting must contain name 'A', got: {full_greet}"

        # 2. Verify all admin sidebar and ribbon buttons are strictly HIDDEN
        desk_c = eval_js("window.getComputedStyle(document.getElementById('navPolicyDeskBtn')).display")
        studio_c = eval_js("window.getComputedStyle(document.getElementById('navContentStudioBtn')).display")
        team_c = eval_js("window.getComputedStyle(document.getElementById('navAdminTeamBtn')).display")
        manual_c = eval_js("window.getComputedStyle(document.getElementById('navAdminManualBtn')).display")
        top_c = eval_js("window.getComputedStyle(document.getElementById('btnTopAdminManual')).display")

        print(f"Customer Mode Visibility:")
        print(f"  Policy Desk:    {desk_c}")
        print(f"  Content Studio: {studio_c}")
        print(f"  Admin Roster:   {team_c}")
        print(f"  Control Center: {manual_c}")
        print(f"  Top Admin Btn:  {top_c}")

        assert desk_c == 'none', "Policy Desk MUST be hidden in customer login"
        assert studio_c == 'none', "Content Studio MUST be hidden in customer login"
        assert team_c == 'none', "Admin Roster MUST be hidden in customer login"
        assert manual_c == 'none', "Control Center MUST be hidden in customer login"
        assert top_c == 'none', "Top Ribbon Admin button MUST be hidden in customer login"

        # 3. Verify active view is dashboard (NOT Policy Desk)
        active_view_c = eval_js("document.querySelector('section.view.active').id")
        print(f"Customer Active View: '{active_view_c}'")
        assert active_view_c == 'view-dashboard', f"Customer active view MUST be 'view-dashboard', got '{active_view_c}'"

        capture_screenshot("voltroof_customer_clean_dashboard.png")

        print("\n==================================================================")
        print(" ALL CHECKLIST ITEMS & ROLE ISOLATION VERIFIED 100% SUCCESSFUL!")
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

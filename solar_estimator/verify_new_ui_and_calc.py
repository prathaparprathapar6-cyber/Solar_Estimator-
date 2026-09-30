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
    port = 9223
    url = "http://localhost:5050"

    print("Launching Chrome headless with remote debugging...")
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

        # Enable Page domain
        call_cdp("Page.enable")
        time.sleep(1.0)

        # -------------------------------------------------------------
        # STEP 1: Verify Login Gate & Clean Layout (No Merged Admin Cards)
        # -------------------------------------------------------------
        print("\n--- STEP 1: Verifying Initial Login Screen ---")
        title = eval_js("document.title")
        print(f"Page Title: {title}")

        gate_disp = eval_js("document.getElementById('nameGate') ? window.getComputedStyle(document.getElementById('nameGate')).display : 'none'")
        print(f"Login Gate Display: {gate_disp}")
        assert gate_disp in ('flex', 'block'), "Login gate must be visible initially"

        # Verify admin manual modal is NOT visible and does not overlay nameGate
        admin_modal_disp = eval_js("document.getElementById('modalAdminManual') ? window.getComputedStyle(document.getElementById('modalAdminManual')).display : 'none'")
        print(f"Admin Modal Display on Initial Load: {admin_modal_disp}")
        assert admin_modal_disp == 'none', "Admin modal must NOT be visible on initial login load!"

        stat_modal_disp = eval_js("document.getElementById('modalStatutory20kW') ? window.getComputedStyle(document.getElementById('modalStatutory20kW')).display : 'none'")
        print(f"Statutory 20kW Modal Display on Initial Load: {stat_modal_disp}")
        assert stat_modal_disp == 'none', "Statutory 20kW modal must NOT be visible on initial login load!"

        # Check logo image source
        logo_src = eval_js("document.getElementById('loginLogoMark') ? document.getElementById('loginLogoMark').querySelector('img')?.getAttribute('src') : ''")
        print(f"Login Logo Mark Source: {logo_src}")
        assert "logo.png" in logo_src or "data:image/png;base64" in logo_src, "Logo mark must reference logo.png"

        # Check clock
        clock_time = eval_js("document.getElementById('loginClockTime') ? document.getElementById('loginClockTime').innerText : ''")
        clock_date = eval_js("document.getElementById('loginClockDate') ? document.getElementById('loginClockDate').innerText : ''")
        print(f"Login Live Clock: {clock_time} | {clock_date}")

        capture_screenshot("voltroof_login_split.png")

        # -------------------------------------------------------------
        # STEP 2: User Login & Verify Header Ribbon
        # -------------------------------------------------------------
        print("\n--- STEP 2: Testing User Login & Header Ribbon ---")
        eval_js("document.getElementById('gateName').value = 'Adarsha KM - Chief Engineer';")
        eval_js("enterApp();")
        time.sleep(1.2)

        # Dismiss Tour Modal if open
        eval_js("""
        const tour = document.getElementById('tourModal');
        if (tour) tour.style.display = 'none';
        localStorage.setItem('voltroof_tour_done', '1');
        """)

        # Verify solar production metric (#topIrr) is removed from #greetBar
        top_irr_in_greet = eval_js("document.getElementById('greetBar').querySelector('#topIrr') !== null")
        print(f"#topIrr present in #greetBar: {top_irr_in_greet}")
        assert top_irr_in_greet == False, "#topIrr must be completely removed from #greetBar!"

        # Verify #topKwp is present as system status chip
        top_kwp_chip = eval_js("document.getElementById('topKwp') ? document.getElementById('topKwp').innerText.trim() : ''")
        print(f"#topKwp status chip text: '{top_kwp_chip}'")
        assert "all good" in top_kwp_chip.lower(), "#topKwp status chip must be 'All good'"

        # Verify greeting word respects AM/PM rules
        hour = eval_js("new Date().getHours()")
        greet_word = eval_js("document.getElementById('greetPrefix') ? document.getElementById('greetPrefix').innerText.trim() : ''")
        print(f"Current hour: {hour} | Live Greeting: '{greet_word}'")
        if hour >= 12:
            assert "good day" not in greet_word.lower(), "PM greeting must NOT contain 'Good day'!"
            if hour < 17:
                assert greet_word.lower() == "good afternoon", f"Expected 'Good afternoon' for hour {hour}, got '{greet_word}'"
            elif hour < 21:
                assert greet_word.lower() == "good evening", f"Expected 'Good evening' for hour {hour}, got '{greet_word}'"
            else:
                assert greet_word.lower() == "good night", f"Expected 'Good night' for hour {hour}, got '{greet_word}'"
        else:
            assert greet_word.lower() in ["good morning", "good day"], f"Expected AM greeting, got '{greet_word}'"

        # -------------------------------------------------------------
        # STEP 3: Path 1 vs Path 2 Derating Verification in UI
        # -------------------------------------------------------------
        print("\n--- STEP 3: Testing Path 1 (70% derated) vs Path 2 (100% direct) ---")
        # Test Path 1 via window.selectInverter
        p1_inv = eval_js("selectInverter(10.0, true)")
        p2_inv = eval_js("selectInverter(10.0, false)")
        print(f"Inverter sizing for 10 kW DC:")
        print(f"  Path 1 (true, 70% derated = 7.0 kW): {p1_inv} kW")
        print(f"  Path 2 (false, 100% sizing = 10.0 kW): {p2_inv} kW")
        assert p1_inv == 7.0, f"Path 1 inverter for 10 kW should be 7.0 kW, got {p1_inv}"
        assert p2_inv == 10.0, f"Path 2 inverter for 10 kW should be 10.0 kW, got {p2_inv}"

        # Test pure calculate(projectDto) contract
        calc_res = eval_js("""
        (function() {
            const dto = {
                sanctionedLoadKw: 15,
                siteSqft: 2500,
                tilt: 15,
                losses: 14,
                costPerWp: 48,
                tariff: 7.5,
                escalation: 3.5,
                monthlyBill: 8500,
                capexOverride: 0,
                sites: [{
                    siteIndex: 0,
                    name: 'Main Campus',
                    sanctionedLoadKw: 15,
                    buildings: [{
                        name: 'Block A',
                        lengthM: 20,
                        widthM: 10,
                        areaSqft: 2152,
                        roofType: 'rcc',
                        parapetM: 0.9,
                        obstacles: []
                    }]
                }]
            };
            const r = window.calculate(dto);
            return {
                schemaVersion: r.schemaVersion,
                capacityKw: r.capacityKw,
                invKw: r.invKw,
                deratedAcKw: r.deratedAcKw,
                plantTotal: r.bom ? r.bom.plantTotal : 0,
                bomItemsCount: r.bom && r.bom.items ? r.bom.items.length : 0,
                amortLength: r.amort ? r.amort.length : 0,
                monthlyCount: r.monthly ? Object.keys(r.monthly).length : 0,
                annualYield: r.annual,
                payY: r.payY,
                payM: r.payM,
                acdbBreaker: r.acdb ? r.acdb.breakerRating : 0,
                acdbCable: r.acdb ? r.acdb.gridCable : ''
            };
        })()
        """)
        print("calculate(projectDto) Result:", json.dumps(calc_res, indent=2))
        assert calc_res['schemaVersion'] == 1, "schemaVersion must be 1"
        assert calc_res['capacityKw'] > 0, "capacityKw must be > 0"
        assert calc_res['bomItemsCount'] == 12, "Must have exactly 12 BOM items"
        assert calc_res['amortLength'] == 25, "amort series must have 25 years"

        capture_screenshot("voltroof_user_dashboard.png")

        # -------------------------------------------------------------
        # STEP 4: Visualizer 3D Mode & Sun Shadows
        # -------------------------------------------------------------
        print("\n--- STEP 4: Visualizer 3D Mode ---")
        eval_js("if (typeof setArrayMode === 'function') setArrayMode('3d');")
        eval_js("const s = document.getElementById('todSlider'); if (s) { s.value = 14; s.dispatchEvent(new Event('input')); }")
        time.sleep(1.0)
        capture_screenshot("voltroof_visualizer_3d.png")

        # -------------------------------------------------------------
        # STEP 5: Policy Hub & Contact Us Views
        # -------------------------------------------------------------
        print("\n--- STEP 5: Views ---")
        eval_js("if (typeof switchView === 'function') switchView('policyHub');")
        time.sleep(0.8)
        capture_screenshot("voltroof_policy_hub.png")

        eval_js("if (typeof switchView === 'function') switchView('contactUs');")
        time.sleep(0.8)
        capture_screenshot("voltroof_contact_us.png")

        # -------------------------------------------------------------
        # STEP 6: Admin Login & Control Center
        # -------------------------------------------------------------
        print("\n--- STEP 6: Admin Login & Control Center ---")
        eval_js("if (typeof switchView === 'function') switchView('dashboard');")
        eval_js("openAdminManualModal();")
        time.sleep(0.5)

        eval_js("document.getElementById('modalAdminUser').value = 'adarshakm@jnnce.ac.in';")
        eval_js("document.getElementById('modalAdminPass').value = 'Adarsh@123321';")
        eval_js("loginAdminFromModal();")
        time.sleep(1.5)

        is_admin = eval_js("isAdminSession();")
        print(f"Is Admin Session: {is_admin}")
        assert is_admin == True, "Admin session must be true after login"

        eval_js("if (typeof switchView === 'function') switchView('adminTeam');")
        time.sleep(0.8)
        capture_screenshot("voltroof_admin_roster.png")

        eval_js("openAdminManualModal();")
        time.sleep(0.5)
        eval_js("switchAdminTab('pricing');")
        time.sleep(0.6)
        capture_screenshot("voltroof_admin_pricing.png")

        eval_js("switchAdminTab('manual');")
        time.sleep(0.6)
        capture_screenshot("voltroof_admin_control_center.png")

        print("\n==================================================")
        print(" ALL VERIFICATIONS PASSED WITH 100% SUCCESS!")
        print("==================================================")

    finally:
        if ws:
            try:
                ws.close()
            except:
                pass
        proc.kill()

if __name__ == '__main__':
    main()

import subprocess
import time
import urllib.request
import json
import socket
import base64
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Helper: simple websocket client over raw socket
class SimpleWebSocket:
    def __init__(self, host, port, path):
        self.sock = socket.create_connection((host, port), timeout=15)
        # HTTP Upgrade handshake
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

print("Starting Edge in headless remote debugging mode...")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
user_data_dir = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "edge_test_profile_3")

cmd = [
    edge_path,
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data_dir}",
    "--headless=new",
    "--disable-gpu",
    "--window-size=1440,1100",
    "http://127.0.0.1:5050/"
]

proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
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
        msg = {"id": msg_id, "method": method, "params": params or {}}
        msg_id += 1
        ws.send_json(msg)
        while True:
            raw = ws.recv_msg()
            if not raw:
                return None
            res = json.loads(raw)
            if res.get("id") == msg["id"]:
                return res

    print("Enabling CDP Runtime & Page domains...")
    send_cdp("Runtime.enable")
    send_cdp("Page.enable")
    time.sleep(1.0)

    def get_eval_val(eval_obj):
        if not eval_obj:
            return None
        res = eval_obj.get("result", {})
        if "exceptionDetails" in res:
            print("JS EXCEPTION:", res["exceptionDetails"])
        return res.get("result", {}).get("value")

    # Enter Name Gate
    send_cdp("Runtime.evaluate", {
        "expression": """
            document.getElementById('gateName').value = 'VoltRoof Chief Solar Engineer';
            enterApp();
        """
    })
    time.sleep(0.5)

    # 1. VERIFY TECHNOLOGY & CATALOG DROPDOWNS
    print("\n--- TEST 1: Technology & Panel Catalog Integration ---")
    tech_eval = send_cdp("Runtime.evaluate", {
        "expression": """
            (() => {
                const techSel = document.getElementById('cfgTech');
                const techOptions = Array.from(techSel.options).map(o => o.value);
                
                // Select N-Type TOPCon
                techSel.value = 'N-Type TOPCon';
                onTechChange('roof');
                const panelSel = document.getElementById('cfgPanel');
                const topconOptions = Array.from(panelSel.querySelectorAll('optgroup[label*=\"N-Type TOPCon\"] option')).map(o => parseInt(o.value));
                const infoText = document.getElementById('cfgTechInfo')?.textContent;

                // Select Polycrystalline
                techSel.value = 'Polycrystalline';
                onTechChange('roof');
                const polyOptions = Array.from(panelSel.querySelectorAll('optgroup[label*=\"Polycrystalline\"] option')).map(o => parseInt(o.value));

                return {
                    techCount: techOptions.length,
                    technologies: techOptions,
                    topconCount: topconOptions.length,
                    topconMin: Math.min(...topconOptions),
                    topconMax: Math.max(...topconOptions),
                    polyCount: polyOptions.length,
                    polyMin: Math.min(...polyOptions),
                    polyMax: Math.max(...polyOptions),
                    infoSample: infoText
                };
            })()
        """,
        "returnByValue": True
    })
    t_res = get_eval_val(tech_eval)
    print("Technology Catalog Result:", t_res)
    assert t_res["techCount"] == 5, f"Expected 5 technologies, got {t_res['techCount']}"
    assert t_res["topconMin"] == 420 and t_res["topconMax"] == 700
    assert t_res["polyMin"] == 40 and t_res["polyMax"] == 340
    print("PASS: Technology dropdown dynamically populates all standard market wattage ratings!")

    # 2. VERIFY 70% DERATING INVERTER & AC COMPONENT SIZING (3.5 kW DC Example)
    print("\n--- TEST 2: 70% Inverter Derating & Derated AC Sizing (3.5 kW DC Test Case) ---")
    derate_eval = send_cdp("Runtime.evaluate", {
        "expression": """
            (() => {
                // Switch back to Mono-PERC, set 500W panel
                document.getElementById('cfgTech').value = 'Mono-PERC (Mono-facial)';
                onTechChange('roof');
                document.getElementById('cfgPanel').value = '500';
                
                // Set roof dimensions: 20ft x 20ft with 1ft parapet -> 18x18 = 324 sqft ~ 3.24 kW
                // Or set exact 3.5 kW via bill method (3.5 * 120 = 420 units)
                setMode('bill');
                document.getElementById('cfgUnits').value = '420'; // 420 / 120 = 3.5 kW
                document.getElementById('cfgTechBill').value = 'Mono-PERC (Mono-facial)';
                onTechChange('bill');
                document.getElementById('cfgPanelBill').value = '500';
                saveCurrentFormToActiveSite();
                liveUpdate();

                const c = current;
                return {
                    capacityKw: c.capacityKw,
                    deratedAcKw: c.deratedAcKw,
                    invKw: c.invKw,
                    phase3: c.phase3,
                    breakerRating: c.acdb.breakerRating,
                    ratedCurrent: c.acdb.ratedCurrent,
                    bomItem1Spec: c.bom.items[0].spec,
                    bomItem2Spec: c.bom.items[1].spec,
                    bomItem2Amt: c.bom.items[1].amt,
                    bomItem8Spec: c.bom.items[7].spec
                };
            })()
        """,
        "returnByValue": True
    })
    d_res = get_eval_val(derate_eval)
    print("3.5 kW Test Case Result:", d_res)
    assert d_res["capacityKw"] == 3.5, f"Expected 3.5 kW, got {d_res['capacityKw']}"
    assert d_res["deratedAcKw"] == 2.45, f"Expected 2.45 kW derated AC, got {d_res['deratedAcKw']}"
    assert d_res["invKw"] == 3.0, f"Expected 3.0 kW inverter, got {d_res['invKw']}"
    assert d_res["breakerRating"] == 16, f"Expected 16A MCB breaker, got {d_res['breakerRating']}"
    assert "Growatt" in d_res["bomItem2Spec"] or "equiv" in d_res["bomItem2Spec"]
    print("PASS: Inverter stepped up to 3.0 kW (derated from 3.5 kW to 2.45 kW) and AC breaker sized to 16A!")

    # 3. VERIFY MULTI-SITE & SITE-LEVEL BOM SWITCHING WITH MIXED BUILDING HARDWARE
    print("\n--- TEST 3: Multi-Site Studio, Mixed Buildings BOM, and Capex Matrix ---")
    multi_eval = send_cdp("Runtime.evaluate", {
        "expression": """
            (() => {
                // Configure Site 1 as 2 Buildings
                setMode('roof');
                document.getElementById('cfgName').value = 'Campus North';
                document.getElementById('cfgLoc').value = 'Shivamogga, Karnataka';
                document.getElementById('cfgL').value = '40';
                document.getElementById('cfgB').value = '30';
                document.getElementById('cfgParapet').value = '1.5';
                document.getElementById('cfgTech').value = 'Mono-PERC (Mono-facial)';
                onTechChange('roof');
                document.getElementById('cfgPanel').value = '400';
                saveCurrentFormToActiveSite();

                // Add Building 2 to Site 1
                addNewBuilding();
                document.getElementById('cfgL').value = '35';
                document.getElementById('cfgB').value = '25';
                document.getElementById('cfgParapet').value = '1.0';
                document.getElementById('cfgTech').value = 'N-Type TOPCon';
                onTechChange('roof');
                document.getElementById('cfgPanel').value = '580';
                saveCurrentFormToActiveSite();

                // Add Site 2
                addNewSite();
                document.getElementById('cfgName').value = 'Tech Park Hub';
                document.getElementById('cfgLoc').value = 'Bengaluru, Karnataka';
                document.getElementById('cfgL').value = '45';
                document.getElementById('cfgB').value = '35';
                document.getElementById('cfgParapet').value = '1.5';
                document.getElementById('cfgTech').value = 'Bifacial (Mono / TOPCon)';
                onTechChange('roof');
                document.getElementById('cfgPanel').value = '550';
                saveCurrentFormToActiveSite();

                liveUpdate();
                switchView('bom');
                renderBomView();

                const site1Bom = sites[0].computed.bom;
                const site2Bom = sites[1].computed.bom;

                return {
                    sitesCount: sites.length,
                    site1Bldgs: sites[0].buildings.length,
                    site1CapKw: sites[0].computed.capacityKw,
                    site1InvKw: sites[0].computed.invKw,
                    site1ModSpec: site1Bom.items[0].spec,
                    site1InvSpec: site1Bom.items[1].spec,
                    site1AcdbSpec: site1Bom.items[7].spec,
                    site2CapKw: sites[1].computed.capacityKw,
                    site2ModSpec: site2Bom.items[0].spec,
                    site2InvSpec: site2Bom.items[1].spec,
                    hasBomTabs: document.getElementById('bomSiteSelectorWrap')?.style.display !== 'none'
                };
            })()
        """,
        "returnByValue": True
    })
    m_res = get_eval_val(multi_eval)
    print("Multi-Site & Mixed Hardware Result:", m_res)
    assert m_res["sitesCount"] == 2
    assert m_res["site1Bldgs"] == 2
    assert "400W" in m_res["site1ModSpec"] and "580W" in m_res["site1ModSpec"]
    print("PASS: Site 1 BOM successfully combines mixed building components (400W Mono-PERC + 580W N-Type TOPCon)!")

    # Capture Web UI Screenshots
    print("\n--- CAPTURING SYSTEM SCREENSHOTS ---")
    time.sleep(0.8)
    
    # 1. Multi-site BOM view
    shot_bom = send_cdp("Page.captureScreenshot", {"format": "png"})
    if shot_bom and "result" in shot_bom and "data" in shot_bom["result"]:
        with open("web_multisite_bom.png", "wb") as f:
            f.write(base64.b64decode(shot_bom["result"]["data"]))
        print("Saved web_multisite_bom.png")

    # 2. Capex Matrix view
    send_cdp("Runtime.evaluate", {"expression": "switchView('dashboard');"})
    time.sleep(0.5)
    shot_matrix = send_cdp("Page.captureScreenshot", {"format": "png"})
    if shot_matrix and "result" in shot_matrix and "data" in shot_matrix["result"]:
        with open("web_multisite_matrix.png", "wb") as f:
            f.write(base64.b64decode(shot_matrix["result"]["data"]))
        print("Saved web_multisite_matrix.png")

    # 3. Single site view test
    send_cdp("Runtime.evaluate", {
        "expression": """
            sites.splice(1, 1);
            activeSiteIndex = 0;
            loadSiteToForm(0);
            liveUpdate();
            switchView('bom');
            renderBomView();
        """
    })
    time.sleep(0.5)
    single_eval = send_cdp("Runtime.evaluate", {
        "expression": """
            (() => {
                const isMulti = sites.length > 1;
                const tabWrap = document.getElementById('bomSiteSelectorWrap');
                const titleText = document.getElementById('bomCardTitle')?.textContent;
                return {
                    sitesCount: sites.length,
                    isMulti,
                    bomTabsVisible: tabWrap?.style.display !== 'none',
                    titleText
                };
            })()
        """,
        "returnByValue": True
    })
    s_res = get_eval_val(single_eval)
    print("Single Site Re-Check Result:", s_res)
    assert not s_res["isMulti"]
    assert not s_res["bomTabsVisible"]
    assert "Portfolio" not in s_res["titleText"]
    print("PASS: Zero portfolio wording and hidden multi-site tabs confirmed when single site is present!")

    shot_single = send_cdp("Page.captureScreenshot", {"format": "png"})
    if shot_single and "result" in shot_single and "data" in shot_single["result"]:
        with open("web_singlesite_bom.png", "wb") as f:
            f.write(base64.b64decode(shot_single["result"]["data"]))
        print("Saved web_singlesite_bom.png")

    print("\nALL BROWSER AUTOMATED VERIFICATIONS PASSED WITH 100% SUCCESS!")

finally:
    try:
        ws.close()
    except:
        pass
    proc.terminate()
    print("Edge process terminated.")

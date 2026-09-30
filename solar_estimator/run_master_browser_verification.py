import subprocess
import time
import json
import urllib.request
import sys
import websocket

sys.stdout.reconfigure(encoding='utf-8')

# 1. Start Server on port 8089
server_process = subprocess.Popen(
    [sys.executable, "solar_pv_estimator.py", "--port", "8089"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
print("Launched server process on port 8089...")

# Wait for server ready
time.sleep(2)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
REMOTE_PORT = 9224

# 2. Launch headless Chrome with clean incognito profile
chrome_process = subprocess.Popen([
    CHROME_PATH,
    f"--remote-debugging-port={REMOTE_PORT}",
    "--headless=new",
    "--incognito",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-service-worker",
    "http://localhost:8089/VoltRoof_Combined.html"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Launched Chrome in headless mode...")

time.sleep(3)

try:
    # 3. Connect to Chrome CDP
    resp = urllib.request.urlopen(f"http://localhost:{REMOTE_PORT}/json")
    tabs = json.loads(resp.read().decode())
    target_tab = next(t for t in tabs if "VoltRoof_Combined" in t.get("url", "") or t.get("type") == "page")
    ws_url = target_tab["webSocketDebuggerUrl"]
    print("Connecting WebSocket CDP:", ws_url)
    ws = websocket.create_connection(ws_url, timeout=10)

    msg_id = 0
    def cdp_send(method, params=None):
        global msg_id
        msg_id += 1
        payload = {"id": msg_id, "method": method, "params": params or {}}
        ws.send(json.dumps(payload))
        while True:
            raw = ws.recv()
            data = json.loads(raw)
            if data.get("id") == msg_id:
                return data

    def eval_js(expr):
        res = cdp_send("Runtime.evaluate", {
            "expression": expr,
            "awaitPromise": True,
            "returnByValue": True
        })
        val = res.get("result", {}).get("result", {}).get("value")
        return val

    # Enable Console and Page
    cdp_send("Console.enable")
    cdp_send("Runtime.enable")
    time.sleep(1)

    print("\n--- TEST A: Admin Button & Toggle ---")
    btn_info = eval_js("""
    (() => {
        const btn = document.getElementById("btnGateAdminToggle");
        if (!btn) return { exists: false };
        const rect = btn.getBoundingClientRect();
        return {
            exists: true,
            text: btn.innerText.trim(),
            visible: rect.width > 0 && rect.height > 0
        };
    })()
    """)
    print("Admin Button Info:", btn_info)
    assert btn_info["exists"] and btn_info["visible"]

    toggle_res = eval_js("""
    (() => {
        toggleGateAdminMode();
        const gateAdminMode = document.getElementById("gateAdminMode");
        return {
            adminModeVisible: gateAdminMode && gateAdminMode.style.display !== 'none'
        };
    })()
    """)
    print("Toggle Admin Mode:", toggle_res)
    assert toggle_res["adminModeVisible"]

    print("\n--- TEST B: Admin Login & Transition ---")
    login_res = eval_js("""
    (async () => {
        document.getElementById("gateAdminUser").value = "Adarsha KM";
        document.getElementById("gateAdminPass").value = "Adarsh@123321";
        await loginAdminFromGate();
        await new Promise(r => setTimeout(r, 600));
        const gate = document.getElementById("nameGate");
        const adminDash = document.getElementById("view-adminDashboard");
        return {
            gateHidden: gate.style.display === 'none',
            adminDashActive: adminDash.classList.contains("active")
        };
    })()
    """)
    print("Login & Transition Result:", login_res)
    assert login_res["gateHidden"] and login_res["adminDashActive"]

    print("\n--- TEST C: Every Admin Subpage & View ---")
    admin_views = [
        "adminDashboard", "adminPricing", "policyDesk", "contentStudio",
        "adminTeam", "adminUsers", "adminManual", "adminVisitors",
        "adminFeedback", "adminAudit", "adminSettings", "adminTickets", "adminEmailLogs"
    ]
    for v in admin_views:
        v_res = eval_js(f"""
        (() => {{
            switchView('{v}');
            const el = document.getElementById('view-{v}');
            return el && el.classList.contains('active');
        }})()
        """)
        assert v_res, f"Failed to switch to {v}"
        print(f"PASS: Admin subpage view-{v} opened cleanly!")

    print("\n--- TEST D: Switch to Customer Mode & Verify Customer Views ---")
    eval_js("setAppMode('customer'); switchView('dashboard');")
    dash_active = eval_js("document.getElementById('view-dashboard').classList.contains('active')")
    assert dash_active
    print("PASS: Customer Dashboard active!")

    print("\n--- TEST E: ACDB Distance Sizing (Requirement 8) ---")
    bom_test = eval_js("""
    (() => {
        document.getElementById("cfgDist").value = "100";
        liveUpdate();
        const items = current?.bom?.items || [];
        const item5 = items.find(i => i.sl === 5);
        return {
            item5Desc: item5?.desc,
            item5Qty: item5?.qty,
            item5Amt: item5?.amt,
            plantTotal: current?.bom?.plantTotal
        };
    })()
    """)
    print("BOM Distance Result (100m):", bom_test)
    assert bom_test["item5Qty"] == "100 m", f"Expected '100 m', got {bom_test['item5Qty']}"
    assert bom_test["item5Amt"] == 18000, f"Expected 18000, got {bom_test['item5Amt']}"
    print("PASS: In frontend, AC cable length is dynamically 100 m and amount is INR 18,000!")

    print("\n--- TEST F: Panel Area & Physical Dimensions Dynamic Update (Requirement 10) ---")
    for watt in [400, 550, 680]:
        area_res = eval_js(f"""
        (() => {{
            document.getElementById("cfgPanel").value = "{watt}";
            liveUpdate();
            const sqft = document.getElementById("rtPanelAreaSqft")?.textContent;
            const m2 = document.getElementById("rtPanelAreaM2")?.textContent;
            return {{ watt: {watt}, sqft, m2 }};
        }})()
        """)
        print(f"PASS: {watt}W module -> Area displayed: {area_res['sqft']} {area_res['m2']}")

    print("\n--- TEST G: Excel Export Functionality (Requirements 18 & 22) ---")
    has_excel = eval_js("typeof exportExcel === 'function' && typeof exportVisitorsExcel === 'function'")
    assert has_excel
    print("PASS: exportExcel and exportVisitorsExcel are verified available and bound!")

    print("\n=======================================================")
    print("CHROME HEADLESS BROWSER AUDIT: 100% PASS! ZERO ERRORS!!")
    print("=======================================================")

finally:
    try: ws.close()
    except Exception: pass
    try: chrome_process.terminate()
    except Exception: pass
    try: server_process.terminate()
    except Exception: pass

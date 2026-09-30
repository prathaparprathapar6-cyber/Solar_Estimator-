import subprocess, time, urllib.request, json, os, socket, base64

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
user_data_dir = os.path.join(os.environ.get('TEMP', r'C:\Temp'), 'edge_inspect_correct_tab')
cmd = [edge_path, '--remote-debugging-port=9234', f'--user-data-dir={user_data_dir}', '--headless=new', '--disable-gpu', 'http://127.0.0.1:5050/VoltRoof_Combined.html']
proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9234/json').read().decode())
    target_tab = None
    for t in tabs:
        if t.get('type') == 'page' and '5050' in t.get('url', ''):
            target_tab = t
            break
    if not target_tab:
        for t in tabs:
            if t.get('type') == 'page':
                target_tab = t
                break
    print(f"Connecting to target tab: {target_tab.get('title')} ({target_tab.get('url')})")
    
    ws_url = target_tab['webSocketDebuggerUrl']
    from urllib.parse import urlparse
    u = urlparse(ws_url)
    
    sock = socket.create_connection((u.hostname, u.port), timeout=15)
    sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = f'GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {sec_key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
    sock.sendall(handshake.encode())
    resp = sock.recv(4096).decode('utf-8', errors='ignore')

    msg_id = 1
    def send_cdp(method, params=None):
        global msg_id
        mid = msg_id
        msg = {"id": mid, "method": method, "params": params or {}}
        msg_id += 1
        data = json.dumps(msg).encode('utf-8')
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
        sock.sendall(frame)

        while True:
            raw = sock.recv(65536)
            if not raw: return {}
            offset = 0
            while offset < len(raw):
                b2 = raw[offset+1]
                plen = b2 & 0x7F
                head_len = 2
                if plen == 126:
                    plen = int.from_bytes(raw[offset+2:offset+4], 'big')
                    head_len = 4
                elif plen == 127:
                    plen = int.from_bytes(raw[offset+2:offset+10], 'big')
                    head_len = 10
                payload = raw[offset+head_len:offset+head_len+plen]
                offset += head_len + plen
                m = json.loads(payload.decode('utf-8', errors='ignore'))
                if m.get('id') == mid:
                    return m

    def eval_expr(expr):
        r = send_cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return r.get('result', {}).get('result', {}).get('value')

    print("typeof enterApp:", eval_expr("typeof enterApp"))
    print("typeof liveUpdate:", eval_expr("typeof liveUpdate"))
    print("typeof compute:", eval_expr("typeof compute"))
    print("typeof calculate:", eval_expr("typeof calculate"))
    print("typeof window.calculate:", eval_expr("typeof window.calculate"))
    print("typeof switchView:", eval_expr("typeof switchView"))
    print("typeof toggleGateAdminMode:", eval_expr("typeof toggleGateAdminMode"))
    print("typeof openAdminManualModal:", eval_expr("typeof openAdminManualModal"))

    calc_test = eval_expr("""
    (function() {
        try {
            const r = window.calculate({sanctionedLoadKw: 15});
            return {
                schemaVersion: r.schemaVersion,
                capacityKw: r.capacityKw,
                invKw: r.invKw,
                bomLength: r.bom ? r.bom.length : 0,
                amortLength: r.amort ? r.amort.length : 0
            };
        } catch(e) {
            return {error: e.toString(), stack: e.stack};
        }
    })()
    """)
    print("window.calculate result:", calc_test)

finally:
    proc.kill()

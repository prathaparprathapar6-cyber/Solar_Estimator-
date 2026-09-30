import subprocess, time, urllib.request, json, os, socket, base64

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
user_data_dir = os.path.join(os.environ.get('TEMP', r'C:\Temp'), 'edge_debug_4')
cmd = [edge_path, '--remote-debugging-port=9230', f'--user-data-dir={user_data_dir}', '--headless=new', '--disable-gpu', 'http://127.0.0.1:5050/VoltRoof_Combined.html']
proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9230/json').read().decode())
    ws_url = tabs[0]['webSocketDebuggerUrl']
    from urllib.parse import urlparse
    u = urlparse(ws_url)
    
    sock = socket.create_connection((u.hostname, u.port), timeout=15)
    sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = f'GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {sec_key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
    sock.sendall(handshake.encode())
    resp = sock.recv(4096).decode('utf-8', errors='ignore')

    def send_cdp(msg):
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
        
        raw = bytearray()
        while True:
            chunk = sock.recv(65536)
            if not chunk: break
            raw.extend(chunk)
            if len(raw) >= 2:
                plen = raw[1] & 0x7F
                offset = 2
                if plen == 126:
                    plen = int.from_bytes(raw[2:4], 'big')
                    offset = 4
                elif plen == 127:
                    plen = int.from_bytes(raw[2:10], 'big')
                    offset = 10
                if len(raw) >= offset + plen:
                    payload = raw[offset:offset+plen]
                    return json.loads(payload.decode('utf-8', errors='ignore'))

    def eval_expr(expr):
        r = send_cdp({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}})
        return r.get('result', {}).get('result', {}).get('value')

    print("Checking variables...")
    print("typeof enterApp:", eval_expr("typeof enterApp"))
    print("typeof liveUpdate:", eval_expr("typeof liveUpdate"))
    print("typeof compute:", eval_expr("typeof compute"))
    print("typeof calculate:", eval_expr("typeof calculate"))
    print("typeof window.calculate:", eval_expr("typeof window.calculate"))
    print("typeof switchView:", eval_expr("typeof switchView"))
    print("typeof updateClock:", eval_expr("typeof updateClock"))
    print("typeof toggleGateAdminMode:", eval_expr("typeof toggleGateAdminMode"))
    print("typeof openAdminManualModal:", eval_expr("typeof openAdminManualModal"))

finally:
    proc.kill()

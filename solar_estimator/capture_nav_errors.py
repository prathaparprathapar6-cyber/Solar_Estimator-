import subprocess, time, urllib.request, json, os, socket, base64

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
user_data_dir = os.path.join(os.environ.get('TEMP', r'C:\Temp'), 'edge_debug_5')
cmd = [edge_path, '--remote-debugging-port=9231', f'--user-data-dir={user_data_dir}', '--headless=new', '--disable-gpu', 'about:blank']
proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9231/json').read().decode())
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

    # Enable everything BEFORE navigating!
    send_cdp({'id': 1, 'method': 'Runtime.enable'})
    send_cdp({'id': 2, 'method': 'Log.enable'})
    send_cdp({'id': 3, 'method': 'Page.enable'})
    send_cdp({'id': 4, 'method': 'Network.enable'})

    # Now navigate to VoltRoof_Combined.html
    send_cdp({'id': 5, 'method': 'Page.navigate', 'params': {'url': 'http://127.0.0.1:5050/VoltRoof_Combined.html'}})

    time.sleep(3.0)
    sock.settimeout(2.0)
    while True:
        try:
            chunk = sock.recv(65536)
            if not chunk: break
            offset = 0
            while offset < len(chunk):
                if offset + 1 >= len(chunk): break
                b2 = chunk[offset+1]
                plen = b2 & 0x7F
                head_len = 2
                if plen == 126:
                    if offset + 4 > len(chunk): break
                    plen = int.from_bytes(chunk[offset+2:offset+4], 'big')
                    head_len = 4
                elif plen == 127:
                    if offset + 10 > len(chunk): break
                    plen = int.from_bytes(chunk[offset+2:offset+10], 'big')
                    head_len = 10
                payload = chunk[offset+head_len:offset+head_len+plen]
                offset += head_len + plen
                msg = json.loads(payload.decode('utf-8', errors='ignore'))
                m = msg.get('method')
                if m in ('Runtime.exceptionThrown', 'Log.entryAdded'):
                    print('EVENT:', m, json.dumps(msg.get('params', {}), indent=2))
        except socket.timeout:
            break

finally:
    proc.kill()

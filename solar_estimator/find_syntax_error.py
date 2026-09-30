import subprocess, time, urllib.request, json, os, socket, base64

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
scripts = list(re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL))
s2 = scripts[2].group(1)

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
user_data_dir = os.path.join(os.environ.get('TEMP', r'C:\Temp'), 'edge_debug_3')
cmd = [edge_path, '--remote-debugging-port=9229', f'--user-data-dir={user_data_dir}', '--headless=new', '--disable-gpu', 'about:blank']
proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9229/json').read().decode())
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

    # We test compiling s2 in chunks or whole
    # Let's write s2 to a temp file and load it, or pass via evaluate
    # Since s2 is 350KB, let's write it to a temp js file in the web directory!
    with open('test_s2.js', 'w', encoding='utf-8') as f_out:
        f_out.write(s2)
    print('Wrote test_s2.js')

    # Now ask Edge to evaluate:
    # "const s = document.createElement('script'); s.src = 'http://127.0.0.1:5050/test_s2.js'; document.head.appendChild(s);"
    # And listen for window.onerror
    setup = """
    window.errors = [];
    window.onerror = function(msg, url, line, col, err) {
        window.errors.push({msg: msg, line: line, col: col, stack: err ? err.stack : ''});
    };
    const s = document.createElement('script');
    s.src = 'http://127.0.0.1:5050/test_s2.js';
    document.head.appendChild(s);
    """
    send_cdp({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': setup}})
    time.sleep(2.0)
    
    r = send_cdp({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'JSON.stringify(window.errors)', 'returnByValue': True}})
    print('Errors:', r.get('result', {}).get('result', {}).get('value'))

finally:
    proc.kill()

import subprocess, time, urllib.request, json, os, socket, base64

class SimpleWebSocket:
    def __init__(self, host, port, path):
        self.sock = socket.create_connection((host, port), timeout=15)
        sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
        handshake = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {sec_key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
        self.sock.sendall(handshake.encode('utf-8'))
        resp = self.sock.recv(4096).decode('utf-8', errors='ignore')

    def send_json(self, msg_obj):
        data = json.dumps(msg_obj).encode('utf-8')
        length = len(data)
        frame = bytearray([0x81])
        if length <= 125: frame.append(0x80 | length)
        elif length <= 65535: frame.append(0x80 | 126); frame.extend(length.to_bytes(2, 'big'))
        mask = os.urandom(4)
        frame.extend(mask)
        frame.extend(bytearray(b ^ mask[i % 4] for i, b in enumerate(data)))
        self.sock.sendall(frame)

    def recv_msg(self):
        hdr = self.sock.recv(2)
        if not hdr: return None
        payload_len = hdr[1] & 0x7F
        if payload_len == 126: payload_len = int.from_bytes(self.sock.recv(2), 'big')
        has_mask = (hdr[1] & 0x80) != 0
        mask = self.sock.recv(4) if has_mask else None
        payload = bytearray()
        while len(payload) < payload_len:
            chunk = self.sock.recv(min(4096, payload_len - len(payload)))
            if not chunk: break
            payload.extend(chunk)
        if has_mask: payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
        return payload.decode('utf-8', errors='ignore')

def main():
    ts = int(time.time())
    cmd = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--remote-debugging-port=9335',
        f'--user-data-dir={os.environ["TEMP"]}\\chrome_dbg_{ts}',
        '--headless=new',
        '--disable-gpu',
        '--window-size=1440,900',
        'http://127.0.0.1:5050/VoltRoof_Combined.html'
    ]
    p = subprocess.Popen(cmd)
    try:
        time.sleep(2.5)
        with urllib.request.urlopen('http://localhost:9335/json') as r:
            targets = json.loads(r.read().decode())
        ws_url = targets[0]['webSocketDebuggerUrl']
        parts = ws_url.split('/')
        ws = SimpleWebSocket(parts[2].split(':')[0], int(parts[2].split(':')[1]), '/' + '/'.join(parts[3:]))

        ws.send_json({'id': 10, 'method': 'Page.enable'})
        ws.recv_msg()
        time.sleep(2.0)

        def eval_js(js):
            ws.send_json({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': js, 'returnByValue': True}})
            while True:
                raw = ws.recv_msg()
                if not raw: break
                d = json.loads(raw)
                if d.get('id') == 1:
                    print("CDP Result:", d)
                    return d.get('result', {}).get('result', {}).get('value')

        info = eval_js('''(() => {
            const gate = document.getElementById('nameGate');
            const shell = document.querySelector('.login-shell');
            const card = document.getElementById('gateCard');
            const hero = document.getElementById('loginHeroPanel');
            const client = document.getElementById('gateClientMode');
            return {
                window: { w: window.innerWidth, h: window.innerHeight },
                shell: shell ? shell.getBoundingClientRect() : null,
                card: card ? card.getBoundingClientRect() : null,
                hero: hero ? hero.getBoundingClientRect() : null,
                client: client ? client.getBoundingClientRect() : null,
                shellStyle: shell ? {
                    display: window.getComputedStyle(shell).display,
                    gridTemplateColumns: window.getComputedStyle(shell).gridTemplateColumns,
                    width: window.getComputedStyle(shell).width
                } : null,
                cardStyle: card ? {
                    width: window.getComputedStyle(card).width,
                    maxWidth: window.getComputedStyle(card).maxWidth,
                    padding: window.getComputedStyle(card).padding,
                    alignItems: window.getComputedStyle(card).alignItems,
                    justifyContent: window.getComputedStyle(card).justifyContent
                } : null
            };
        })()''')
        print(json.dumps(info, indent=2))
    finally:
        p.terminate()

if __name__ == '__main__':
    main()

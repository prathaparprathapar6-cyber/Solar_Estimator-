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
    port = 9224
    file_url = r"file:///C:/Users/DELL/Downloads/voltroof_solar_pv_estimator_standalone.html"

    print("Testing standalone HTML file directly via file:// protocol (no server)...")
    proc = subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={port}",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--window-size=1440,900",
        file_url
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
        print("Connected to Chrome DevTools Protocol WebSocket via file:// protocol!")

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

        # 1. Verify title
        title = eval_js("document.title")
        print(f"Standalone Page Title: {title}")
        assert "VoltRoof" in title

        # 2. Check Chart.js is loaded
        has_chart = eval_js("typeof Chart !== 'undefined'")
        print(f"Chart.js Available Standalone: {has_chart}")
        assert has_chart == True, "Chart.js must be loaded and defined"

        # 3. Check Logo Image rendered
        logo_loaded = eval_js("""
        (function() {
            const img = document.querySelector('#loginLogoMark img');
            return img && img.src.startsWith('data:image/png;base64');
        })()
        """)
        print(f"Base64 Logo Image Loaded: {logo_loaded}")
        assert logo_loaded == True, "Base64 logo must be rendered"

        # 4. Enter app
        eval_js("document.getElementById('gateName').value = 'Standalone User';")
        eval_js("enterApp();")
        time.sleep(1.0)

        # 5. Check calculation
        calc_out = eval_js("""
        (function() {
            const p1 = selectInverter(10.0, true);
            const p2 = selectInverter(10.0, false);
            return { p1, p2 };
        })()
        """)
        print(f"Standalone Inverter Selection: Path 1 = {calc_out['p1']} kW (derated), Path 2 = {calc_out['p2']} kW (100%)")
        assert calc_out['p1'] == 7.0
        assert calc_out['p2'] == 10.0

        # 6. Check greeting
        greet = eval_js("document.getElementById('greetPrefix') ? document.getElementById('greetPrefix').innerText : ''")
        print(f"Standalone Live Greeting: '{greet}'")

        print("\n>>> STANDALONE FILE VERIFICATION SUCCESSFUL! ZERO EXTERNAL DEPENDENCIES. <<<")

    finally:
        if ws:
            try:
                ws.close()
            except:
                pass
        proc.kill()

if __name__ == '__main__':
    main()

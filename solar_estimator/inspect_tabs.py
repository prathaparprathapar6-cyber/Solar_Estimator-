import subprocess, time, urllib.request, json, os

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
user_data_dir = os.path.join(os.environ.get('TEMP', r'C:\Temp'), 'edge_inspect_tabs')
cmd = [edge_path, '--remote-debugging-port=9233', f'--user-data-dir={user_data_dir}', '--headless=new', '--disable-gpu', 'http://127.0.0.1:5050/VoltRoof_Combined.html']
proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9233/json').read().decode())
    print('Tabs count:', len(tabs))
    for i, t in enumerate(tabs):
        print(f"Tab {i}: type={t.get('type')}, title={t.get('title')}, url={t.get('url')}")
finally:
    proc.kill()

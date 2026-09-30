import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="modalAdminManual"')
end = text.find('</div>\n\n<script', start)
if start != -1:
    content = text[start:start+4000]
    print(content)
else:
    print("modalAdminManual not found")

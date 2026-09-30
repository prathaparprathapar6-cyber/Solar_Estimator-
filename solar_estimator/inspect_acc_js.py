import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\DELL\Downloads\VoltRoof_Admin_Control_Center new.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<script>')
if idx == -1:
    idx = text.find('<script')
print(text[idx:idx+3500])

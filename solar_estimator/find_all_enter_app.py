import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('enterApp', idx)
    if idx == -1:
        break
    if 'function enterApp' in text[idx-10:idx+25] or 'enterApp =' in text[idx:idx+20]:
        print(f"At {idx}:")
        print(text[max(0, idx-30):min(len(text), idx+150)])
        print("="*40)
    idx += 8

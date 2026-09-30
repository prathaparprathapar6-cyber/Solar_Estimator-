import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inspect cfgPanel
idx1 = html.find('cfgPanel')
print("=== cfgPanel ===")
print(html[idx1-50:idx1+350])

# Inspect selectInverter
idx2 = html.find('function selectInverter')
print("\n=== selectInverter in JS ===")
print(html[idx2:idx2+600])

# Inspect selectAcdbComponents
idx3 = html.find('function selectAcdbComponents')
print("\n=== selectAcdbComponents in JS ===")
print(html[idx3:idx3+600])

# Inspect selectAcCable
idx4 = html.find('function selectAcCable')
print("\n=== selectAcCable in JS ===")
print(html[idx4:idx4+600])

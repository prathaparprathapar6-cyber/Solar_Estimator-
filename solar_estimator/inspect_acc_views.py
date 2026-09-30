import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\DELL\Downloads\VoltRoof_Admin_Control_Center new.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'class="view' in l or 'id="view' in l or 'data-view=' in l or '<section' in l:
        print(f"{i+1}: {l.strip()[:100]}")

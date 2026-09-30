with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- topIrr lines ---")
for i, l in enumerate(lines):
    if 'topIrr' in l:
        print(f'{i+1}: {l.strip()}')

print("\n--- modalAdminManual lines ---")
for i, l in enumerate(lines):
    if 'modalAdminManual' in l:
        print(f'{i+1}: {l.strip()[:100]}')

print("\n--- nameGate lines ---")
for i, l in enumerate(lines):
    if 'nameGate' in l:
        print(f'{i+1}: {l.strip()[:100]}')

print("\n--- greeting lines ---")
for i, l in enumerate(lines):
    if 'greeting' in l.lower() or 'good morning' in l.lower() or 'good afternoon' in l.lower():
        print(f'{i+1}: {l.strip()[:100]}')

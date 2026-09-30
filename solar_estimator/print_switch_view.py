with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function switchView(' in l:
        for j in range(i, i+30):
            print(f"{j+1}: {lines[j].rstrip()}")
        break

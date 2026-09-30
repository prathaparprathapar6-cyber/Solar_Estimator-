with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(6605, 6640):
    if j < len(lines):
        print(f'{j+1}: {lines[j].rstrip()}')

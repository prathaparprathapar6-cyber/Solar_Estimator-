with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="view-' in l or "id='view-" in l:
        print(f"Line {i+1}: {l.strip()[:100]}")

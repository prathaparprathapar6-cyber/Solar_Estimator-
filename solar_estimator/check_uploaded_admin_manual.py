with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("modalAdminManual in user_uploaded_latest.html:")
for i, l in enumerate(text.splitlines()):
    if 'modaladminmanual' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")

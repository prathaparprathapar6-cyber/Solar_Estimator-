with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('function refreshFeedbackStats')
if pos != -1:
    print("=== refreshFeedbackStats ===")
    print(text[pos:pos+2500].encode('ascii', errors='replace').decode('ascii'))
else:
    print("refreshFeedbackStats function not found! Searching for fb functions...")
    import re
    for m in re.finditer(r'function\s+[a-zA-Z0-9_]*feed[a-zA-Z0-9_]*', text, re.IGNORECASE):
        print(m.group(0))

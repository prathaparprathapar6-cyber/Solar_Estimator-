with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find lines around `let sites =`
idx = text.find('let sites =')
if idx != -1:
    print(text[idx:idx+3500])

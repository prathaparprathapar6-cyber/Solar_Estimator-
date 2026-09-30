import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="modalContentStudio"')
close_div = text.find('</div>\n</div>\n\n', idx)
print(text[idx:close_div+15])

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('</style>')
print("Style tag ends at index:", idx)
print("Context around </style>:")
print(text[idx-300:idx+50])

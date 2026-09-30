import re

with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    up = f.read()

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    comb = f.read()

print("--- isAdminSession in uploaded ---")
m = re.search(r'function isAdminSession\(\)[\s\S]*?\}', up)
if m: print(m.group(0))

print("\n--- isAdminSession in combined ---")
m = re.search(r'function isAdminSession\(\)[\s\S]*?\}', comb)
if m: print(m.group(0))

print("\n--- getActiveAdmin in combined ---")
m = re.search(r'function getActiveAdmin\(\)[\s\S]*?\}', comb)
if m: print(m.group(0))

print("\n--- syncAdminNavVisibility in combined ---")
m = re.search(r'function syncAdminNavVisibility\(\)[\s\S]*?\}', comb)
if m: print(m.group(0))

print("\n--- enterApp in combined ---")
m = re.search(r'function enterApp\(\)[\s\S]*?\}', comb)
if m: print(m.group(0)[:500])

import os
import re

path = r'C:\Users\DELL\Downloads\voltroof_solar_pv_estimator_standalone.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', content)
print('External script tags count:', len(scripts), scripts)

links = re.findall(r'<link[^>]*href=[\'"]([^\'"]+)[\'"]', content)
print('External link tags count:', len(links), links)

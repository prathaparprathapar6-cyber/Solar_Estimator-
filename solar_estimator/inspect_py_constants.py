with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    for i in range(45):
        l = f.readline()
        if 'B64' in l or 'EMBEDDED' in l:
            print(f'{i+1}: {l.strip()[:60]}...')
        else:
            print(f'{i+1}: {l.strip()}')

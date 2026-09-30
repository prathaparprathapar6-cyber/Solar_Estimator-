import re

def search_terms(filename):
    print(f"=== Searching in {filename} ===")
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if any(term in line.lower() for term in ['portfolio', 'multi-site', 'multisite', 'multi site']):
                print(f"{i+1}: {line.strip()[:100]}")

search_terms('solar_pv_estimator.py')
search_terms('index.html')

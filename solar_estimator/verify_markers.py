import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read solar_pv_estimator.py
with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Verify that current markers exist
assert "class SiteResult:" in code
assert "class LTDesignReport:" in code
assert "def generate_plant_bom(" in code
assert "def build_multi_site_report(" in code
assert "def export_pdf(" in code

print("All assertion markers verified in solar_pv_estimator.py!")

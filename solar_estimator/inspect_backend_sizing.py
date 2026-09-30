import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Inspect INVERTER_RATINGS
idx1 = code.find('INVERTER_RATINGS')
print("=== INVERTER_RATINGS in Python ===")
print(code[idx1:idx1+400])

# Inspect select_inverter
idx2 = code.find('def select_inverter')
print("\n=== def select_inverter in Python ===")
print(code[idx2:idx2+600])

# Inspect select_acdb_components
idx3 = code.find('def select_acdb_components')
print("\n=== def select_acdb_components in Python ===")
print(code[idx3:idx3+900])

# Inspect MODULE_WATT_DEFAULT or panel watt references
idx4 = code.find('MODULE_WATT_DEFAULT')
print("\n=== MODULE_WATT_DEFAULT in Python ===")
print(code[idx4:idx4+400])

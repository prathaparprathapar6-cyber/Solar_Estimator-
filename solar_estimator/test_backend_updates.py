import sys
sys.stdout.reconfigure(encoding='utf-8')
import solar_pv_estimator as sp

print('--- Testing select_inverter_lt ---')
inv_p1 = sp.select_inverter_lt(10.0, is_path1=True)
inv_p2 = sp.select_inverter_lt(10.0, is_path1=False)
print('10kW plant: Path 1 inverter:', inv_p1, 'Path 2 inverter:', inv_p2)
assert inv_p1 == inv_p2, f'Derating mismatch: {inv_p1} vs {inv_p2}'

print('\n--- Testing generate_plant_bom with 100m distance ---')
items, total, escom = sp.generate_plant_bom(10.0, 8.0, 550, 18, acdb_breaker_rating=32, dist_m=100.0)
ac_item = next(it for it in items if it.sl_no == 5)
print('Item 5:', ac_item.description, '| Qty:', ac_item.quantity, '| Amount: INR', ac_item.amount_inr)
assert ac_item.quantity == '100 m', f'Expected 100 m, got {ac_item.quantity}'
assert ac_item.amount_inr == 18000.0, f'Expected 18000, got {ac_item.amount_inr}'

print('\n--- Testing get_panel_physical_specs ---')
for w in [335, 400, 550, 680]:
    s = sp.get_panel_physical_specs(w)
    print(f"{w}W: Area {s['area_m2']} m2 ({s['area_sqft']} sq.ft), Dimensions {s['length_m']}m x {s['width_m']}m, Mfr: {s['mfr']}")

print('\nALL BACKEND CALCULATION & PRICING TESTS PASSED!')

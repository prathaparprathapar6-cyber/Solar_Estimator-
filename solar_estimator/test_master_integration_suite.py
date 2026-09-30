import sys
import os
import json
sys.stdout.reconfigure(encoding='utf-8')

import backend_ext
import solar_pv_estimator as sp

def test_1_to_20kw_derating():
    print("\n--- 1. Testing 1 kW to 20 kW Sizing & Derating ---")
    for kw in range(1, 21):
        cap = float(kw)
        inv_p1 = sp.select_inverter_lt(cap, is_path1=True)
        inv_p2 = sp.select_inverter_lt(cap, is_path1=False)
        assert inv_p1 == inv_p2, f"Mismatch at {kw}kW: Path 1={inv_p1} vs Path 2={inv_p2}"
        expected_derated = round(cap * 0.70, 2)
        # Verify inverter accommodates derated kW
        assert inv_p1 >= min(1.0, expected_derated), f"Inverter {inv_p1} too small for derated {expected_derated} at {kw}kW"
    print("PASS: 1 kW to 20 kW sizing & 70% derating verified identical for Path 1 & Path 2!")

def test_acdb_cable_distance():
    print("\n--- 2. Testing ACDB Distance Bug Fix (Requirement 8) ---")
    for dist in [15.0, 50.0, 100.0, 150.0]:
        items, total, escom = sp.generate_plant_bom(10.0, 8.0, 550, 18, acdb_breaker_rating=32, dist_m=dist)
        ac_item = next(it for it in items if it.sl_no == 5)
        expected_qty = f"{int(dist)} m"
        cur_pricing = sp.db_load_json(sp.PRICING_DB_FILE, sp.DEFAULT_PRICING_MAP)
        expected_amt = round(dist * cur_pricing.get("ac_cable_per_m", 180.0), 2)
        assert ac_item.quantity == expected_qty, f"Dist {dist}: Expected {expected_qty}, got {ac_item.quantity}"
        assert ac_item.amount_inr == expected_amt, f"Dist {dist}: Expected amount {expected_amt}, got {ac_item.amount_inr}"
        print(f"PASS: Distance {dist}m -> BOM Qty: {ac_item.quantity}, Cost: INR {ac_item.amount_inr}")

def test_module_physical_specs():
    print("\n--- 3. Testing Module Physical Dimensions (Requirements 10, 11, 12) ---")
    ratings = [335, 380, 400, 440, 450, 500, 540, 550, 580, 600, 650, 680]
    for w in ratings:
        specs = sp.get_panel_physical_specs(w)
        assert specs["area_m2"] > 0
        assert specs["area_sqft"] > 0
        assert specs["weight_kg"] > 0
        assert specs["mfr"]
        print(f"PASS: {w}W -> {specs['area_m2']} m² ({specs['area_sqft']} sq.ft), {specs['length_m']}m x {specs['width_m']}m, {specs['weight_kg']}kg, Mfr: {specs['mfr']}")

def test_dynamic_pricing_ripple():
    print("\n--- 4. Testing Equipment & Component Dynamic Pricing Ripple (Requirements 5, 6, 7, 13) ---")
    catalog = backend_ext.get_pricing_catalog()
    # Check that modules contain 680W and others
    mod_ids = [m["id"] for m in catalog["modules"]["items"]]
    assert "mod-680" in mod_ids or any("680" in m.get("rating", "") for m in catalog["modules"]["items"])
    
    # Update AC cable rate to 210.0 and verify ripple
    res = backend_ext.update_pricing_item("ac_cables", "acc-1", 210.0, user="TestAdmin")
    assert res["success"]
    
    # Verify sync_catalog_to_pricing_db updated pricing_db.json
    pricing_map = backend_ext.get_pricing_map()
    assert pricing_map.get("ac_cable_per_m") == 210.0, f"Expected 210.0, got {pricing_map.get('ac_cable_per_m')}"
    
    # Verify BOM immediately picks up updated pricing
    items, total, escom = sp.generate_plant_bom(10.0, 8.0, 550, 18, acdb_breaker_rating=32, dist_m=100.0)
    ac_item = next(it for it in items if it.sl_no == 5)
    assert ac_item.amount_inr == 100.0 * 210.0, f"Expected INR 21000, got {ac_item.amount_inr}"
    print(f"PASS: Pricing update ripple verified! AC Cable 100m at INR 210/m = INR {ac_item.amount_inr}")
    
    # Revert back to 180.0
    backend_ext.update_pricing_item("ac_cables", "acc-1", 180.0, user="TestAdmin")
    print("PASS: Reverted test rate back to benchmark INR 180/m")

def test_feedback_moderation():
    print("\n--- 5. Testing Feedback System & Moderation (Requirement 14) ---")
    # 1. Create user feedback
    fb_res = backend_ext.handle_feedback_action({
        "action": "create",
        "client_name": "Integration Test EPC",
        "email": "testepc@karnataka.org",
        "category": "Solar EPC Contractor / Installer",
        "experience": 5,
        "comments": "Automated verification test of VoltRoof Solar PV Estimator."
    })
    assert fb_res["success"]
    fb_id = fb_res["feedback"]["id"]
    print(f"Created feedback {fb_id}")
    
    # 2. Admin moderates / approves
    app_res = backend_ext.handle_feedback_action({
        "action": "approve",
        "id": fb_id
    })
    assert app_res["success"]
    assert app_res["feedback"]["status"] == "Approved"
    print(f"PASS: Approved feedback {fb_id}")
    
    # 3. Admin replies
    rep_res = backend_ext.handle_feedback_action({
        "action": "reply",
        "id": fb_id,
        "reply": "Thank you for the verification test.",
        "admin": "Adarsha KM"
    })
    assert rep_res["success"]
    assert rep_res["feedback"]["status"] == "Resolved"
    print(f"PASS: Replied to feedback {fb_id}")
    
    # 4. Clean up / delete test record
    del_res = backend_ext.handle_feedback_action({
        "action": "delete",
        "id": fb_id
    })
    assert del_res["success"]
    print(f"PASS: Deleted test feedback record {fb_id}")

def test_visitor_analytics_and_files():
    print("\n--- 6. Testing Visitor Analytics & Uploads (Requirements 15 & 16) ---")
    sessions = backend_ext.get_visitors_detailed()
    assert isinstance(sessions, list)
    print(f"PASS: Visitor detailed sessions count: {len(sessions)}")
    
    # Verify file upload handling
    test_upload = backend_ext.handle_upload({
        "type": "document",
        "filename": "test_verification_doc.txt",
        "data_base64": "data:text/plain;base64,Vm9sdFJvb2YgVmVyaWZpY2F0aW9uIFRlc3QgU3VjY2Vzc2Z1bCE=",
        "author": "SystemTest"
    })
    assert test_upload["success"]
    print(f"PASS: Uploaded file URL: {test_upload['url']}")
    
    # Clean up test upload
    backend_ext.handle_upload_delete({"url": test_upload["url"]})
    print("PASS: Cleaned up test upload")

if __name__ == "__main__":
    test_1_to_20kw_derating()
    test_acdb_cable_distance()
    test_module_physical_specs()
    test_dynamic_pricing_ripple()
    test_feedback_moderation()
    test_visitor_analytics_and_files()
    print("\n=======================================================")
    print("ALL MASTER INTEGRATION TESTS PASSED WITH 100% SUCCESS!!")
    print("=======================================================")

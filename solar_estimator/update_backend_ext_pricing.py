import sys, os

with open('backend_ext.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add mod-680 to default_catalog if not present
if '"id": "mod-680"' not in content:
    target = '{"id": "mod-440", "mfr": "First Solar"'
    replacement = '''{"id": "mod-680", "mfr": "Waaree Energies", "model": "Vertex Max 680 HJT", "tech": "Ultra-High Power G12", "rating": "680 Wp", "efficiency": "21.9%", "warranty": "30 Years", "unit": "?/Wp", "old_price": 25.50, "curr_price": 24.80, "new_price": 24.80, "availability": "In Stock", "specs": "132-Cell G12 Bifacial Dual Glass, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_680w.png"},
                {"id": "mod-440", "mfr": "First Solar"'''
    content = content.replace(target, replacement, 1)

# 2. Add approve action in handle_feedback_action
if 'action == "approve"' not in content:
    target_fb = 'elif action == "delete":'
    replacement_fb = '''elif action == "approve":
        target_id = data.get("id", "")
        fb = next((x for x in feedbacks if x["id"] == target_id), None)
        if not fb:
            return {"success": False, "error": f"Feedback {target_id} not found"}
        fb["status"] = "Approved"
        save_json("feedback_db.json", feedbacks)
        return {"success": True, "feedback": fb}

    elif action == "delete":'''
    content = content.replace(target_fb, replacement_fb, 1)

# 3. Add sync_catalog_to_pricing_db and helper functions
sync_func = '''
def sync_catalog_to_pricing_db(catalog):
    pdb = load_json("pricing_db.json", {})
    if "modules" in catalog:
        m_items = catalog["modules"].get("items", [])
        m550 = next((m for m in m_items if "550" in str(m.get("rating", ""))), None)
        if m550 and "curr_price" in m550:
            pdb["module_per_wp"] = float(m550["curr_price"])
        elif m_items and "curr_price" in m_items[0]:
            pdb["module_per_wp"] = float(m_items[0]["curr_price"])
    if "inverters" in catalog:
        inv_items = catalog["inverters"].get("items", [])
        inv10 = next((i for i in inv_items if i.get("rating_kw") == 10.0), None)
        if inv10 and "curr_price" in inv10:
            pdb["inverter_per_kw"] = round(float(inv10["curr_price"]) / 10.0, 2)
        elif inv_items:
            rates = [float(i["curr_price"]) / max(1.0, float(i.get("rating_kw", 1.0))) for i in inv_items if "curr_price" in i]
            if rates:
                pdb["inverter_per_kw"] = round(sum(rates) / len(rates), 2)
    if "structures" in catalog:
        s_items = catalog["structures"].get("items", [])
        s1 = next((s for s in s_items if "HDGI" in s.get("tech", "")), s_items[0] if s_items else None)
        if s1 and "curr_price" in s1:
            pdb["structure_per_kw"] = float(s1["curr_price"])
    if "dc_cables" in catalog:
        dc_items = catalog["dc_cables"].get("items", [])
        d6 = next((d for d in dc_items if "6" in d.get("rating", "")), dc_items[0] if dc_items else None)
        if d6 and "curr_price" in d6:
            pdb["dc_cable_per_m"] = float(d6["curr_price"])
    if "ac_cables" in catalog:
        ac_items = catalog["ac_cables"].get("items", [])
        ac6 = next((a for a in ac_items if "6" in a.get("rating", "")), ac_items[0] if ac_items else None)
        if ac6 and "curr_price" in ac6:
            pdb["ac_cable_per_m"] = float(ac6["curr_price"])
    if "mc4" in catalog:
        mc4_items = catalog["mc4"].get("items", [])
        if mc4_items and "curr_price" in mc4_items[0]:
            pdb["mc4_per_pair"] = float(mc4_items[0]["curr_price"])
    if "dcdb" in catalog:
        dcdb_items = catalog["dcdb"].get("items", [])
        d2 = next((d for d in dcdb_items if "2-in" in d.get("rating", "")), dcdb_items[0] if dcdb_items else None)
        if d2 and "curr_price" in d2:
            pdb["dcdb_base"] = float(d2["curr_price"])
    if "acdb" in catalog:
        acdb_items = catalog["acdb"].get("items", [])
        a2 = next((a for a in acdb_items if "Three Phase" in a.get("rating", "")), acdb_items[0] if acdb_items else None)
        if a2 and "curr_price" in a2:
            pdb["acdb_base"] = float(a2["curr_price"])
    if "earthing" in catalog:
        eth_items = catalog["earthing"].get("items", [])
        e1 = eth_items[0] if eth_items else None
        if e1 and "curr_price" in e1:
            pdb["earthing_kit_base"] = float(e1["curr_price"]) * (3 if "pit" in e1.get("unit", "").lower() else 1)
    if "lightning_arrestor" in catalog:
        la_items = catalog["lightning_arrestor"].get("items", [])
        l1 = next((l for l in la_items if "Conventional" in l.get("tech", "")), la_items[0] if la_items else None)
        if l1 and "curr_price" in l1:
            pdb["lightning_arrester_base"] = float(l1["curr_price"])
    if "installation_labour" in catalog:
        inst_items = catalog["installation_labour"].get("items", [])
        if inst_items and "curr_price" in inst_items[0]:
            pdb["installation_per_kw"] = float(inst_items[0]["curr_price"])
    if "statutory_fees" in catalog:
        fees = catalog["statutory_fees"].get("items", [])
        for f in fees:
            fid = f.get("id", "")
            pr = float(f.get("curr_price", 0))
            if "reg" in fid: pdb["escom_application_fee"] = pr
            elif "scrutiny" in fid or "proc" in fid: pdb["escom_processing_fee"] = pr
            elif "meter" in fid: pdb["escom_net_meter"] = pr

    save_json("pricing_db.json", pdb)
    return pdb

def get_pricing_map():
    return load_json("pricing_db.json", {})
'''

if 'def sync_catalog_to_pricing_db' not in content:
    content = content + "\n" + sync_func

# In save_pricing_catalog, reset_pricing_catalog, update_pricing_item, hook sync_catalog_to_pricing_db
content = content.replace('def save_pricing_catalog(catalog):\n    return save_json("pricing_categories_db.json", catalog)', '''def save_pricing_catalog(catalog):
    res = save_json("pricing_categories_db.json", catalog)
    sync_catalog_to_pricing_db(catalog)
    return res''')

content = content.replace('def reset_pricing_catalog():\n    if os.path.exists(get_file_path("pricing_categories_db.json")):', '''def reset_pricing_catalog():
    if os.path.exists(get_file_path("pricing_categories_db.json")):''')

content = content.replace('    save_pricing_catalog(catalog)\n\n    audit = load_json("pricing_audit_db.json", [])', '''    save_pricing_catalog(catalog)
    sync_catalog_to_pricing_db(catalog)

    audit = load_json("pricing_audit_db.json", [])''')

with open('backend_ext.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated backend_ext.py successfully!")

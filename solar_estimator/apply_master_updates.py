import os
import re

def update_solar_pv_estimator():
    path = "solar_pv_estimator.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add MODULE_PHYSICAL_SPECS if not already added
    if "MODULE_PHYSICAL_SPECS = {" not in content:
        specs_code = '''# ============================================================
# SOLAR PANEL PHYSICAL DIMENSIONS & SPECIFICATION DATABASE
# (Real Physical Dimensions, Area, Weight, Efficiency, Mfr)
# ============================================================
MODULE_PHYSICAL_SPECS = {
    335: {"length_m": 1.960, "width_m": 0.992, "area_m2": 1.94, "area_sqft": 20.9, "weight_kg": 22.0, "efficiency": "17.2%", "tech": "Polycrystalline", "mfr": "RenewSys", "model": "Deserv 3K Poly"},
    380: {"length_m": 1.755, "width_m": 1.038, "area_m2": 1.82, "area_sqft": 19.6, "weight_kg": 20.0, "efficiency": "20.1%", "tech": "Mono PERC", "mfr": "Vikram Solar", "model": "Somera Grand"},
    400: {"length_m": 1.722, "width_m": 1.134, "area_m2": 1.95, "area_sqft": 21.0, "weight_kg": 21.0, "efficiency": "20.5%", "tech": "Mono PERC Mono-facial", "mfr": "Vikram Solar", "model": "Aditya 400"},
    440: {"length_m": 2.008, "width_m": 1.002, "area_m2": 2.01, "area_sqft": 21.6, "weight_kg": 22.5, "efficiency": "20.4%", "tech": "Mono PERC", "mfr": "First Solar", "model": "Series 6 Plus"},
    450: {"length_m": 2.094, "width_m": 1.038, "area_m2": 2.17, "area_sqft": 23.4, "weight_kg": 24.5, "efficiency": "20.8%", "tech": "Mono PERC Mono-facial", "mfr": "Tata Power Solar", "model": "TP450M"},
    500: {"length_m": 2.180, "width_m": 1.102, "area_m2": 2.40, "area_sqft": 25.8, "weight_kg": 26.0, "efficiency": "21.0%", "tech": "Mono PERC", "mfr": "Adani Solar", "model": "Eternal Shine"},
    540: {"length_m": 2.278, "width_m": 1.134, "area_m2": 2.58, "area_sqft": 27.8, "weight_kg": 28.5, "efficiency": "21.2%", "tech": "Mono PERC Bifacial", "mfr": "Waaree Energies", "model": "Arka 540 Bi-33"},
    550: {"length_m": 2.278, "width_m": 1.134, "area_m2": 2.58, "area_sqft": 27.8, "weight_kg": 27.5, "efficiency": "21.5%", "tech": "Mono-PERC (Mono-facial)", "mfr": "Waaree Energies", "model": "WS-550 Mono"},
    580: {"length_m": 2.278, "width_m": 1.134, "area_m2": 2.58, "area_sqft": 27.8, "weight_kg": 28.0, "efficiency": "22.2%", "tech": "N-Type TOPCon", "mfr": "Adani Solar", "model": "Elan Shine TOPCon"},
    600: {"length_m": 2.465, "width_m": 1.134, "area_m2": 2.79, "area_sqft": 30.0, "weight_kg": 31.0, "efficiency": "22.8%", "tech": "HJT (Heterojunction)", "mfr": "Goldi Solar", "model": "Heloc Plus HJT"},
    650: {"length_m": 2.384, "width_m": 1.303, "area_m2": 3.11, "area_sqft": 33.5, "weight_kg": 34.0, "efficiency": "21.6%", "tech": "Ultra-High Power G12", "mfr": "Trina Solar", "model": "Vertex G12"},
    680: {"length_m": 2.384, "width_m": 1.303, "area_m2": 3.11, "area_sqft": 33.5, "weight_kg": 34.5, "efficiency": "21.9%", "tech": "Ultra-High Power G12", "mfr": "Waaree Energies", "model": "Vertex Max 680"}
}

def get_panel_physical_specs(watt: int, tech: str = "") -> dict:
    w = int(watt) if watt else 550
    if w in MODULE_PHYSICAL_SPECS:
        return dict(MODULE_PHYSICAL_SPECS[w])
    area_m2 = round(w / 215.0, 2)
    area_sqft = round(area_m2 * 10.7639, 1)
    width_m = 1.134
    length_m = round(area_m2 / width_m, 3)
    weight_kg = round(area_m2 * 11.0, 1)
    return {
        "length_m": length_m,
        "width_m": width_m,
        "area_m2": area_m2,
        "area_sqft": area_sqft,
        "weight_kg": weight_kg,
        "efficiency": "21.2%",
        "tech": tech or "Mono-PERC",
        "mfr": "Tier-1 Certified",
        "model": f"Standard PV {w}W"
    }

'''
        content = content.replace("# SOLAR PANEL MASTER CATALOG", specs_code + "\n# SOLAR PANEL MASTER CATALOG", 1)

    # 2. Fix select_inverter_lt: Derating factor 70% for BOTH Path 1 and Path 2
    old_der = 'derated_kw = round(total_plant_dc_kw * 0.70, 2) if is_path1 else round(total_plant_dc_kw, 2)'
    new_der = 'derated_kw = round(total_plant_dc_kw * 0.70, 2)  # Standard 70% derating for BOTH Path 1 and Path 2'
    content = content.replace(old_der, new_der)

    # 3. Dynamic pricing and user dist_m in generate_plant_bom
    # Locate generate_plant_bom
    bom_pattern = re.compile(r'def generate_plant_bom\(.*?return items, plant_total, escom', re.DOTALL)
    
    new_bom_impl = '''def generate_plant_bom(
    capacity_kw: float,
    inverter_kw: float,
    panel_watt: int,
    panel_count: int,
    acdb_breaker_rating: int = 16,
    bldg_results: Optional[List[BuildingResult]] = None,
    dist_m: float = 20.0,
    panel_tech: str = "Mono-PERC (Mono-facial)"
) -> Tuple[List[BOMItem], float, Dict[str, float]]:
    cap = max(1.0, capacity_kw)
    rounded_cap = round(cap)
    
    # Load dynamic pricing from central database
    cur_pricing = db_load_json(PRICING_DB_FILE, DEFAULT_PRICING_MAP)
    mod_rate = float(cur_pricing.get("module_per_wp", 18.18))
    inv_rate = float(cur_pricing.get("inverter_per_kw", 10500.0))
    struct_rate = float(cur_pricing.get("structure_per_kw", 4800.0))
    dc_rate = float(cur_pricing.get("dc_cable_per_m", 85.0))
    ac_rate = float(cur_pricing.get("ac_cable_per_m", 180.0))
    mc4_rate = float(cur_pricing.get("mc4_per_pair", 300.0))
    dcdb_base = float(cur_pricing.get("dcdb_base", 7000.0))
    acdb_base = float(cur_pricing.get("acdb_base", 7000.0))
    earthing_base = float(cur_pricing.get("earthing_kit_base", 7500.0))
    la_base = float(cur_pricing.get("lightning_arrester_base", 4000.0))
    acc_rate = float(cur_pricing.get("accessories_per_kw", 1200.0))
    inst_rate = float(cur_pricing.get("installation_per_kw", 4000.0))

    if bldg_results and len(bldg_results) > 0:
        total_module_cost = float(sum(b.panel_count * round(b.panel_watt * mod_rate, 2) for b in bldg_results))
        actual_panel_count = sum(b.panel_count for b in bldg_results)
        distinct_specs = sorted(list(set(f"{b.panel_watt}W {b.panel_tech}" for b in bldg_results)))
        if len(distinct_specs) == 1:
            mod_spec = f"{distinct_specs[0]}"
        else:
            mod_spec = " + ".join([f"{b.name}: {b.panel_watt}W {b.panel_tech} ({b.panel_count} Nos.)" for b in bldg_results])
        mc4_pairs = actual_panel_count
        mod_qty_str = f"{actual_panel_count} Nos."
    else:
        cost_per_module = round(panel_watt * mod_rate, 2)
        total_module_cost = float(panel_count * cost_per_module)
        mc4_pairs = panel_count
        mod_spec = f"{panel_watt} W {panel_tech}"
        mod_qty_str = f"{panel_count} Nos."

    mc4_cost = float(mc4_pairs * mc4_rate)

    # Inverter specification with certified models
    inv_model = get_inverter_model(inverter_kw)
    model_hint = f" ({inv_model.top_tier_models.split(',')[0]} or equiv.)" if inv_model else ""

    num_bldgs = len(bldg_results) if (bldg_results and len(bldg_results) > 1) else 1

    if bldg_results and len(bldg_results) > 1:
        inv_detail = " + ".join([f"{b.name}: {b.inverter_kw:g}kW" for b in bldg_results])
        inv_spec = f"{inverter_kw:g} kW {'three-phase' if inverter_kw > 5.0 else 'single-phase'} ({inv_detail})"
        inv_qty_str = f"{len(bldg_results)} Nos."
        b_mcbs = " + ".join([f"{b.name}: {select_acdb_components(b.ac_calculated_kw, dist_m)[1]}A MCB" for b in bldg_results])
        acdb_spec = f"{b_mcbs} + Type-II AC SPD"
        acdb_qty_str = f"{len(bldg_results)} Set(s)"
        struct_qty_str = f"{len(bldg_results)} Roof Set(s)"
        dcdb_qty_str = f"{len(bldg_results)} No(s)."
    else:
        inv_spec = (
            f"{inverter_kw:g} kW, three-phase{model_hint}"
            if inverter_kw > 5.0
            else f"{inverter_kw:g} kW, single-phase{model_hint}"
        )
        inv_qty_str = "1 No."
        rccb_rating = 25 if acdb_breaker_rating <= 16 else (40 if acdb_breaker_rating <= 32 else 63)
        acdb_spec = f"{acdb_breaker_rating}A MCB + {rccb_rating}A RCCB + Type-II AC SPD"
        acdb_qty_str = "1 No."
        struct_qty_str = "1 Set"
        dcdb_qty_str = "1 No."

    # AC cable uses actual user distance (Requirement 8)
    user_dist_m = float(dist_m) if dist_m and dist_m > 0 else 20.0
    ac_qty_str = f"{int(round(user_dist_m))} m"
    ac_cable_cost = round(user_dist_m * ac_rate, 2)
    
    # DC cable length
    dc_len_m = max(20, int(round(cap * 11)))
    dc_cable_cost = round(dc_len_m * dc_rate, 2)
    
    inv_cost = round(inverter_kw * inv_rate, 2)
    struct_cost = round(cap * struct_rate, 2)
    dcdb_cost = round(dcdb_base * num_bldgs, 2)
    acdb_cost = round(acdb_base * num_bldgs, 2)
    earthing_cost = round(earthing_base, 2)
    la_cost = round(la_base, 2)
    acc_cost = round(cap * acc_rate, 2)
    inst_cost = round(cap * inst_rate, 2)

    if rounded_cap in EXACT_BOM_REPORTS:
        rows = EXACT_BOM_REPORTS[rounded_cap]
        items: List[BOMItem] = []
        for idx, (desc, spec, qty, amt) in enumerate(rows, start=1):
            if idx == 1:
                items.append(BOMItem(idx, "Solar PV modules", mod_spec, mod_qty_str, total_module_cost))
            elif idx == 2:
                items.append(BOMItem(idx, "On-grid inverter", inv_spec, inv_qty_str, inv_cost))
            elif idx == 3:
                items.append(BOMItem(idx, desc, spec, struct_qty_str, struct_cost))
            elif idx == 4:
                items.append(BOMItem(idx, "DC solar cable", spec, f"{dc_len_m} m", dc_cable_cost))
            elif idx == 5:
                # AC cable: ALWAYS use user dist_m (Requirement 8)
                items.append(BOMItem(idx, "AC cable", "4-10 sq.mm copper (Grid Interconnection)", ac_qty_str, ac_cable_cost))
            elif idx == 6:
                items.append(BOMItem(idx, "MC4 connectors", "PV-rated connector pairs", f"{mc4_pairs} pairs", mc4_cost))
            elif idx == 7:
                items.append(BOMItem(idx, desc, spec, dcdb_qty_str, dcdb_cost))
            elif idx == 8:
                items.append(BOMItem(idx, "ACDB", acdb_spec, acdb_qty_str, acdb_cost))
            elif idx == 9:
                items.append(BOMItem(idx, "Earthing kit", "Earth electrodes & accessories (IS 3043 - 3 Pits)", "3 Nos.", earthing_cost))
            elif idx == 10:
                items.append(BOMItem(idx, "Lightning arrester", spec, "1 No.", la_cost))
            elif idx == 11:
                items.append(BOMItem(idx, "Installation accessories", spec, "1 Lot", acc_cost))
            elif idx == 12:
                items.append(BOMItem(idx, "Installation & commissioning", spec, "1 Job", inst_cost))
            else:
                items.append(BOMItem(idx, desc, spec, qty, amt))
        plant_total = sum(item.amount_inr for item in items)
    else:
        items = [
            BOMItem(1, "Solar PV modules", mod_spec, mod_qty_str, total_module_cost),
            BOMItem(2, "On-grid inverter", inv_spec, inv_qty_str, inv_cost),
            BOMItem(3, "Rooftop mounting structure", "HDGI rooftop structure, module-compatible", struct_qty_str, struct_cost),
            BOMItem(4, "DC solar cable", "4-6 sq.mm copper, PV-rated", f"{dc_len_m} m", dc_cable_cost),
            BOMItem(5, "AC cable", "4-10 sq.mm copper (Grid Interconnection)", ac_qty_str, ac_cable_cost),
            BOMItem(6, "MC4 connectors", "PV-rated connector pairs", f"{mc4_pairs} pairs", mc4_cost),
            BOMItem(7, "DCDB", "Isolator + fuse + Type-II DC SPD", dcdb_qty_str, dcdb_cost),
            BOMItem(8, "ACDB", acdb_spec, acdb_qty_str, acdb_cost),
            BOMItem(9, "Earthing kit", "Chemical earth electrodes & accessories (IS 3043)", "3 Nos.", earthing_cost),
            BOMItem(10, "Lightning arrester", "Standard rooftop PV type", "1 No.", la_cost),
            BOMItem(11, "Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", acc_cost),
            BOMItem(12, "Installation & commissioning", "Labour, testing and commissioning", "1 Job", inst_cost),
        ]
        plant_total = sum(item.amount_inr for item in items)

    if inverter_kw <= 5.0:
        escom = {
            "registration": float(cur_pricing.get("escom_application_fee", 500.0)),
            "facilitation": float(cur_pricing.get("escom_processing_fee", 1000.0)),
            "ppa_esign": float(cur_pricing.get("escom_stamp_duty", 11.8)),
            "meter_estimate": float(cur_pricing.get("escom_net_meter", 4500.0)),
            "security_deposit": float(cur_pricing.get("escom_security_deposit", 3000.0)),
        }
    else:
        escom = {
            "registration": float(cur_pricing.get("escom_application_fee", 1000.0)),
            "facilitation": float(cur_pricing.get("escom_processing_fee", 2000.0)),
            "ppa_esign": float(cur_pricing.get("escom_stamp_duty", 11.8)),
            "meter_estimate": float(cur_pricing.get("escom_net_meter", 7500.0)),
            "security_deposit": float(cur_pricing.get("escom_security_deposit", 5000.0)),
        }
    return items, plant_total, escom'''

    content = bom_pattern.sub(new_bom_impl, content, count=1)

    # 4. In build_building_result: calculate req_area_sqft using module physical specs
    content = content.replace(
        'req_area_sqft = round(panels * 32.0, 1)',
        'mod_specs = get_panel_physical_specs(panel_watt, panel_tech)\n        req_area_sqft = round(panels * mod_specs["area_sqft"] * 1.20, 1)'
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated solar_pv_estimator.py!")

if __name__ == "__main__":
    update_solar_pv_estimator()

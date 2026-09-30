import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update SiteResult dataclass
target_site_res = """    monthly_generation_kwh: Dict[str, float] = field(default_factory=dict)
    annual_generation_kwh: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)"""

replacement_site_res = """    monthly_generation_kwh: Dict[str, float] = field(default_factory=dict)
    annual_generation_kwh: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)
    total_capital_inr: float = 0.0"""

if target_site_res in content:
    content = content.replace(target_site_res, replacement_site_res, 1)

# 2. Update LTDesignReport dataclass
target_lt_rep = """    # Bill of Materials (BOM)
    bom_items: List[BOMItem] = field(default_factory=list)
    bom_plant_total_inr: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)"""

replacement_lt_rep = """    # Bill of Materials (BOM)
    bom_items: List[BOMItem] = field(default_factory=list)
    bom_plant_total_inr: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)
    total_escom_budget_inr: float = 0.0
    grand_total_capital_inr: float = 0.0"""

if target_lt_rep in content:
    content = content.replace(target_lt_rep, replacement_lt_rep, 1)

# 3. Update build_building_result to pass parapet_ft and panel_watt
target_bldg_res = """    strings = max(1, ceil_to_int(panels / 20.0))
    return BuildingResult(
        name=name,
        rooftop_area_sqft=rooftop_area,
        utilized_rooftop_area_sqft=utilized,
        capacity_kw=capacity_kw,
        panel_count=panels,
        strings=strings,
        inverter_kw=inverter_kw,
        inverter_qty=1,
        inverter_cable=inv_cable,
        isolator_rating=isolator,
    )"""

replacement_bldg_res = """    strings = max(1, ceil_to_int(panels / 20.0))
    return BuildingResult(
        name=name,
        rooftop_area_sqft=rooftop_area,
        utilized_rooftop_area_sqft=utilized,
        capacity_kw=capacity_kw,
        panel_count=panels,
        strings=strings,
        inverter_kw=inverter_kw,
        inverter_qty=1,
        inverter_cable=inv_cable,
        isolator_rating=isolator,
        parapet_ft=parapet_ft,
        panel_watt=panel_watt,
    )"""

if target_bldg_res in content:
    content = content.replace(target_bldg_res, replacement_bldg_res, 1)

# 4. Update generate_plant_bom to support bldg_results
old_bom_func_start = "def generate_plant_bom(\n    capacity_kw: float,\n    inverter_kw: float,\n    panel_watt: int,\n    panel_count: int,\n    acdb_breaker_rating: int = 16\n) -> Tuple[List[BOMItem], float, Dict[str, float]]:"

new_bom_func = """def generate_plant_bom(
    capacity_kw: float,
    inverter_kw: float,
    panel_watt: int,
    panel_count: int,
    acdb_breaker_rating: int = 16,
    bldg_results: Optional[List[BuildingResult]] = None,
    dist_m: float = 20.0
) -> Tuple[List[BOMItem], float, Dict[str, float]]:
    cap = max(1.0, capacity_kw)
    rounded_cap = round(cap)

    if bldg_results and len(bldg_results) > 0:
        total_module_cost = float(sum(b.panel_count * round(b.panel_watt * (10000.0 / 550.0)) for b in bldg_results))
        actual_panel_count = sum(b.panel_count for b in bldg_results)
        distinct_watts = sorted(list(set(b.panel_watt for b in bldg_results)))
        if len(distinct_watts) == 1:
            mod_spec = f"{distinct_watts[0]} W mono PERC / TOPCon"
        else:
            mod_spec = " + ".join([f"{b.name}: {b.panel_watt}W ({b.panel_count} Nos.)" for b in bldg_results])
        mc4_pairs = actual_panel_count
        mod_qty_str = f"{actual_panel_count} Nos."
    else:
        cost_per_module = round(panel_watt * (10000.0 / 550.0))
        total_module_cost = float(panel_count * cost_per_module)
        mc4_pairs = panel_count
        mod_spec = f"{panel_watt} W mono PERC / TOPCon"
        mod_qty_str = f"{panel_count} Nos."

    mc4_cost = float(mc4_pairs * 300.0)

    if bldg_results and len(bldg_results) > 1:
        inv_detail = " + ".join([f"{b.name}: {b.inverter_kw:g}kW" for b in bldg_results])
        inv_spec = f"{inverter_kw:g} kW {'three-phase' if inverter_kw > 5.0 else 'single-phase'} ({inv_detail})"
        inv_qty_str = f"{len(bldg_results)} Nos."
        b_mcbs = " + ".join([f"{b.name}: {select_acdb_components(b.inverter_kw, dist_m)[1]}A MCB" for b in bldg_results])
        acdb_spec = f"{b_mcbs} + Type-II AC SPD"
        acdb_qty_str = f"{len(bldg_results)} Set(s)"
        struct_qty_str = f"{len(bldg_results)} Roof Set(s)"
        dcdb_qty_str = f"{len(bldg_results)} No(s)."
    else:
        inv_spec = (
            f"{inverter_kw:g} kW, three-phase"
            if inverter_kw > 5.0
            else f"{inverter_kw:g} kW, single-phase"
        )
        inv_qty_str = "1 No."
        rccb_rating = 25 if acdb_breaker_rating <= 16 else (40 if acdb_breaker_rating <= 32 else 63)
        acdb_spec = f"{acdb_breaker_rating}A MCB + {rccb_rating}A RCCB + Type-II AC SPD"
        acdb_qty_str = "1 No."
        struct_qty_str = "1 Set"
        dcdb_qty_str = "1 No."

    if rounded_cap in EXACT_BOM_REPORTS:
        rows = EXACT_BOM_REPORTS[rounded_cap]
        items: List[BOMItem] = []
        for idx, (desc, spec, qty, amt) in enumerate(rows, start=1):
            if idx == 1:
                items.append(BOMItem(idx, "Solar PV modules", mod_spec, mod_qty_str, total_module_cost))
            elif idx == 2:
                inv_cost = float(amt) * (inverter_kw / max(1.0, float(rounded_cap)))
                items.append(BOMItem(idx, "On-grid inverter", inv_spec, inv_qty_str, round(inv_cost, 2)))
            elif idx == 3:
                items.append(BOMItem(idx, desc, spec, struct_qty_str, amt))
            elif idx == 6:
                items.append(BOMItem(idx, "MC4 connectors", "PV-rated connector pairs", f"{mc4_pairs} pairs", mc4_cost))
            elif idx == 7:
                items.append(BOMItem(idx, desc, spec, dcdb_qty_str, amt))
            elif idx == 8:
                items.append(BOMItem(idx, "ACDB", acdb_spec, acdb_qty_str, amt))
            elif idx == 9:
                items.append(BOMItem(idx, "Earthing kit", "Earth electrodes & accessories (IS 3043 - 3 Pits)", "3 Nos.", amt))
            else:
                items.append(BOMItem(idx, desc, spec, qty, amt))
        plant_total = sum(item.amount_inr for item in items)
    else:
        inv_cost = inverter_kw * 10500.0
        items = [
            BOMItem(1, "Solar PV modules", mod_spec, mod_qty_str, total_module_cost),
            BOMItem(2, "On-grid inverter", inv_spec, inv_qty_str, inv_cost),
            BOMItem(3, "Rooftop mounting structure", "HDGI rooftop structure, module-compatible", struct_qty_str, cap * 4800.0),
            BOMItem(4, "DC solar cable", "4-6 sq.mm copper, PV-rated", f"{int(max(20, cap * 11))} m", cap * 935.0),
            BOMItem(5, "AC cable", "4-10 sq.mm copper", f"{int(max(15, cap * 6))} m", cap * 2400.0),
            BOMItem(6, "MC4 connectors", "PV-rated connector pairs", f"{mc4_pairs} pairs", mc4_cost),
            BOMItem(7, "DCDB", "Isolator + fuse + Type-II DC SPD", dcdb_qty_str, 18000.0),
            BOMItem(8, "ACDB", acdb_spec, acdb_qty_str, 18000.0),
            BOMItem(9, "Earthing kit", "Chemical earth electrodes & accessories (IS 3043)", "3 Nos.", 9000.0),
            BOMItem(10, "Lightning arrester", "Standard rooftop PV type", "1 No.", 8000.0),
            BOMItem(11, "Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", cap * 1900.0),
            BOMItem(12, "Installation & commissioning", "Labour, testing and commissioning", "1 Job", cap * 4750.0),
        ]
        plant_total = sum(item.amount_inr for item in items)

    if inverter_kw <= 5.0:
        escom = {
            "registration": 500.0,
            "facilitation": 1000.0,
            "ppa_esign": 11.8,
            "meter_estimate": 4500.0,
            "security_deposit": 3000.0,
        }
    else:
        escom = {
            "registration": 1000.0,
            "facilitation": 2000.0,
            "ppa_esign": 11.8,
            "meter_estimate": 12000.0,
            "security_deposit": 8000.0,
        }

    return items, round(plant_total, 2), escom"""

if old_bom_func_start in content:
    bom_idx = content.find(old_bom_func_start)
    end_marker = "return items, round(plant_total, 2), escom"
    end_idx = content.find(end_marker, bom_idx) + len(end_marker)
    content = content[:bom_idx] + new_bom_func + content[end_idx:]

# 5. In build_system_report:
target_bsr_bom = """    bom_items, plant_total_cost, escom_budget = generate_plant_bom(
        capacity_kw=report.total_capacity_kw,
        inverter_kw=total_system_inverter_kw,
        panel_watt=panel_watt,
        panel_count=report.total_panels,
        acdb_breaker_rating=breaker_rating,
    )
    report.bom_items = bom_items
    report.bom_plant_total_inr = plant_total_cost
    report.project_cost_inr = plant_total_cost
    report.escom_budget = escom_budget"""

replacement_bsr_bom = """    bom_items, plant_total_cost, escom_budget = generate_plant_bom(
        capacity_kw=report.total_capacity_kw,
        inverter_kw=total_system_inverter_kw,
        panel_watt=panel_watt,
        panel_count=report.total_panels,
        acdb_breaker_rating=breaker_rating,
        bldg_results=building_results,
        dist_m=distance_m,
    )
    report.bom_items = bom_items
    report.bom_plant_total_inr = plant_total_cost
    report.project_cost_inr = plant_total_cost
    report.escom_budget = escom_budget
    report.total_escom_budget_inr = sum(escom_budget.values())
    report.grand_total_capital_inr = plant_total_cost + sum(escom_budget.values())"""

assert target_bsr_bom in content, "target_bsr_bom not found"
content = content.replace(target_bsr_bom, replacement_bsr_bom, 1)

# Single site result in build_system_report
target_sr_single = """            bom_items=bom_items,
            bom_total_inr=plant_total_cost,
            monthly_generation_kwh=report.monthly_generation_kwh,
            annual_generation_kwh=report.annual_generation_kwh,
            escom_budget=escom_budget,
        )"""

replacement_sr_single = """            bom_items=bom_items,
            bom_total_inr=plant_total_cost,
            monthly_generation_kwh=report.monthly_generation_kwh,
            annual_generation_kwh=report.annual_generation_kwh,
            escom_budget=escom_budget,
            total_capital_inr=plant_total_cost + sum(escom_budget.values())
        )"""

assert target_sr_single in content, "target_sr_single not found"
content = content.replace(target_sr_single, replacement_sr_single, 1)

# 6. In build_multi_site_report:
target_ms_bom_call = """        site_bom_items, site_bom_total, site_escom = generate_plant_bom(
            capacity_kw=site_cap_kw,
            inverter_kw=site_inv_kw,
            panel_watt=primary_panel_watt,
            panel_count=site_total_panels,
            acdb_breaker_rating=breaker_rating
        )"""

replacement_ms_bom_call = """        site_bom_items, site_bom_total, site_escom = generate_plant_bom(
            capacity_kw=site_cap_kw,
            inverter_kw=site_inv_kw,
            panel_watt=primary_panel_watt,
            panel_count=site_total_panels,
            acdb_breaker_rating=breaker_rating,
            bldg_results=bldg_results,
            dist_m=dist_m
        )"""

assert target_ms_bom_call in content, "target_ms_bom_call not found"
content = content.replace(target_ms_bom_call, replacement_ms_bom_call, 1)

target_sr_inst = """            monthly_generation_kwh=site_monthly,
            annual_generation_kwh=site_annual,
            escom_budget=site_escom
        )"""

replacement_sr_inst = """            monthly_generation_kwh=site_monthly,
            annual_generation_kwh=site_annual,
            escom_budget=site_escom,
            total_capital_inr=site_bom_total + sum(site_escom.values())
        )"""

assert target_sr_inst in content, "SiteResult instantiation not found"
content = content.replace(target_sr_inst, replacement_sr_inst, 1)

# In build_multi_site_report: update return
target_ms_ret = """        bom_plant_total_inr=total_project_cost,
        project_cost_inr=total_project_cost,
        escom_budget=consolidated_escom,"""

replacement_ms_ret = """        bom_plant_total_inr=total_project_cost,
        project_cost_inr=total_project_cost,
        escom_budget=consolidated_escom,
        total_escom_budget_inr=sum(consolidated_escom.values()),
        grand_total_capital_inr=total_project_cost + sum(consolidated_escom.values()),"""

assert target_ms_ret in content, "build_multi_site_report return not found"
content = content.replace(target_ms_ret, replacement_ms_ret, 1)

with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Applied Part 1 changes to solar_pv_estimator.py!")

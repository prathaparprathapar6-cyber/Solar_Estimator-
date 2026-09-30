import re

with open("solar_pv_estimator.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Define INVERTER_MASTER_CATALOG and SOLAR_PANEL_CATALOG
catalogs_code = '''
# ============================================================
# SOLAR PANEL MASTER CATALOG (From Standard Market Ratings)
# ============================================================
SOLAR_PANEL_CATALOG = {
    "Mono-PERC (Mono-facial)": {
        "category": "Mono-PERC (Mono-facial)",
        "key_details": "The standard for current residential rooftop systems.",
        "ratings": [380, 390, 400, 410, 420, 430, 440, 450, 460, 480, 500, 525, 530, 535, 540, 545, 550, 555, 560, 570, 580],
        "default": 550,
    },
    "N-Type TOPCon": {
        "category": "N-Type TOPCon",
        "key_details": "Premium high-efficiency modules for commercial & industrial use.",
        "ratings": [420, 440, 450, 500, 540, 545, 550, 555, 560, 565, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 660, 670, 680, 690, 700],
        "default": 580,
    },
    "Bifacial (Mono / TOPCon)": {
        "category": "Bifacial (Mono / TOPCon)",
        "key_details": "Dual-sided generation. Ratings listed are for the front side.",
        "ratings": [440, 500, 530, 540, 545, 550, 560, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 655, 660, 665, 670, 680, 690, 700, 710, 720],
        "default": 550,
    },
    "Polycrystalline": {
        "category": "Polycrystalline",
        "key_details": "Legacy technology, mostly used in small off-grid applications.",
        "ratings": [40, 50, 75, 100, 150, 165, 200, 250, 260, 270, 275, 280, 300, 325, 330, 335, 340],
        "default": 335,
    },
    "Ultra-High Power (G12/G12R)": {
        "category": "Ultra-High Power (G12/G12R)",
        "key_details": "Large-format modules for utility-scale solar farms.",
        "ratings": [600, 610, 620, 625, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720],
        "default": 650,
    },
}

# ============================================================
# ON-GRID SOLAR INVERTER MASTER CATALOG (1 kW to 20 kW)
# ============================================================
@dataclass
class InverterModel:
    rating_kw: float
    phase: str
    availability: str
    top_tier_models: str
    hardware_kw: float

INVERTER_MASTER_CATALOG: Dict[float, InverterModel] = {
    1.0: InverterModel(1.0, "Single-Phase", "Standard entry point; ideal for nano 1-room households.", "Solis Mini, Havells Envira", 1.0),
    2.0: InverterModel(2.0, "Single-Phase", "Standard residential tier; powers basic 1-2 BHK loads.", "Polycab PSIT, Obetech G", 2.0),
    3.0: InverterModel(3.0, "Single-Phase", "Highest Volume Domestic Tier; maximum limit for single-phase PM Surya Ghar subsidy.", "Growatt MIC, Luminous NXi 130", 3.0),
    4.0: InverterModel(4.0, "Single-Phase / Three-Phase", "Transition bracket; widely deployed for 3 BHK properties.", "Waaree W3.1/3-PH, Luminous NXi 340", 4.0),
    5.0: InverterModel(5.0, "Single-Phase / Three-Phase", "Standard boundary rating; most DISCOMs mandate a shift to 3-phase meter beyond this capacity.", "Sungrow SG5.0RS, UTL 5.1", 5.0),
    6.0: InverterModel(6.0, "Single-Phase / Three-Phase", "Commercial scale entry point; common for large villas.", "Solis 1P6K, Growatt MOD 6000", 6.0),
    7.0: InverterModel(7.0, "Three-Phase", "Fully Standardized Option; engineered specifically to bridge the gap between 6kW and 8kW.", "Growatt P3, Fimer On-Grid", 7.0),
    8.0: InverterModel(8.0, "Three-Phase", "Industrial tier; steelwork for independent modern bungalows.", "GoodWe GW8K-DT, Polycab PSIT 8K", 8.0),
    9.0: InverterModel(9.0, "Three-Phase", "Available, but mostly handled via turnkey system developers rather than standalone retail packages.", "Greentech Energy", 9.0),
    10.0: InverterModel(10.0, "Three-Phase", "Massive Volume Commercial Tier; high demand threshold for standard commercial shops.", "Fronius Symo, Delta M10", 10.0),
    11.0: InverterModel(11.0, "Three-Phase", "Highly Available; engineered by some houses to allow optimal DC oversizing on 10kW sanctioned limits.", "Deye 11K-G04, Kstar Solar", 11.0),
    12.0: InverterModel(12.0, "Three-Phase", "Mid-tier industrial rating; heavily utilized for institutions.", "Solis 12KTL, Hitachi Solar", 12.0),
    13.0: InverterModel(13.0, "Non-Standard", "Physically Unavailable. Installers deploy a derated 15kW unit and programmatically cap it to 13kW.", "None (Use 15kW configuration)", 15.0),
    14.0: InverterModel(14.0, "Three-Phase", "Exists primarily in specialized hybrid catalogs; rarely sold as standalone grid-tied retail.", "Deye, Delta Solar", 14.0),
    15.0: InverterModel(15.0, "Three-Phase", "Core Industrial Tier; widely chosen for schools, small petrol pumps and agricultural setups.", "Sungrow SG15RT, UTL On-Grid", 15.0),
    16.0: InverterModel(16.0, "Three-Phase", "Available primarily inside commercial and heavy-duty hybrid brackets.", "Deye Hybrid 16K", 16.0),
    17.0: InverterModel(17.0, "Three-Phase", "Highly Available; prominent dedicated hardware step offered by major manufacturers.", "UTL 17KW, Solis 3-Phase 17KW, SolarEdge", 17.0),
    18.0: InverterModel(18.0, "Three-Phase", "Commercially cataloged; installers frequently choose to derate a standard 20kW inverter for net-metering compliance.", "Deye 18K, Growatt 18K", 18.0),
    19.0: InverterModel(19.0, "Non-Standard", "Physically Bypassed; OEM not optimized for this number; installers upgrade project directly to 20kW system.", "None (Use 20kW configuration)", 20.0),
    20.0: InverterModel(20.0, "Three-Phase", "Major Industrial Anchor Tier; standard benchmark for decentralized rooftop annexes & micro-factories.", "Loom Solar, Eyzer 20, Waaree W3-20K", 20.0),
}

INVERTER_STANDARD_RATINGS: Tuple[float, ...] = (
    1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
    11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
)
'''

old_inv_ratings = """INVERTER_RATINGS: Tuple[float, ...] = (
    1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
    11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
)"""

assert old_inv_ratings in code, "old_inv_ratings not found"
code = code.replace(old_inv_ratings, catalogs_code + "\nINVERTER_RATINGS = INVERTER_STANDARD_RATINGS\n", 1)

# 2. Update select_inverter_lt with 70% derating logic
old_select_inv = """def select_inverter_lt(total_plant_capacity_kw: float) -> float:
    target = round(total_plant_capacity_kw, 2)
    for r in INVERTER_RATINGS:
        if r >= target - 1e-4:
            return r
    return INVERTER_RATINGS[-1]"""

new_select_inv = """def select_inverter_lt(total_plant_dc_kw: float) -> float:
    \"\"\"Selects on-grid inverter rating to 70% (derating factor) of solar panels total output power.
    E.g. if solar panel output power is 3.5 kW, then 3.5 * 0.7 = 2.45 kW -> selects 3.0 kW standard rating.
    \"\"\"
    derated_kw = round(total_plant_dc_kw * 0.70, 2)
    if derated_kw <= 1.0:
        return 1.0
    for r in INVERTER_STANDARD_RATINGS:
        if r >= derated_kw - 1e-4:
            return r
    return INVERTER_STANDARD_RATINGS[-1]

def get_inverter_model(inverter_kw: float) -> Optional[InverterModel]:
    return INVERTER_MASTER_CATALOG.get(inverter_kw)"""

assert old_select_inv in code, "old_select_inv not found"
code = code.replace(old_select_inv, new_select_inv, 1)

# 3. Update dataclasses BuildingResult, SiteResult, LTDesignReport
old_br = """@dataclass
class BuildingResult:
    name: str
    rooftop_area_sqft: float
    utilized_rooftop_area_sqft: float
    capacity_kw: float
    panel_count: int
    strings: int
    inverter_kw: float
    inverter_qty: int
    inverter_cable: str
    isolator_rating: str
    site_name: str = ""
    parapet_ft: float = 1.5
    panel_watt: int = MODULE_WATT_DEFAULT"""

new_br = """@dataclass
class BuildingResult:
    name: str
    rooftop_area_sqft: float
    utilized_rooftop_area_sqft: float
    capacity_kw: float
    panel_count: int
    strings: int
    inverter_kw: float
    inverter_qty: int
    inverter_cable: str
    isolator_rating: str
    site_name: str = ""
    parapet_ft: float = 1.5
    panel_watt: int = MODULE_WATT_DEFAULT
    panel_tech: str = "Mono-PERC (Mono-facial)"
    ac_calculated_kw: float = 0.0"""

assert old_br in code, "old_br not found"
code = code.replace(old_br, new_br, 1)

old_sr = """    panel_watt: int
    distance_m: float
    building_reports: List[BuildingResult] = field(default_factory=list)"""

new_sr = """    panel_watt: int
    distance_m: float
    panel_tech: str = "Mono-PERC (Mono-facial)"
    ac_calculated_kw: float = 0.0
    building_reports: List[BuildingResult] = field(default_factory=list)"""

assert old_sr in code, "old_sr not found"
code = code.replace(old_sr, new_sr, 1)

old_rep = """    panel_watt: int = MODULE_WATT_DEFAULT
    acdb_to_grid_distance_m: float = 0.0"""

new_rep = """    panel_watt: int = MODULE_WATT_DEFAULT
    panel_tech: str = "Mono-PERC (Mono-facial)"
    ac_calculated_kw: float = 0.0
    acdb_to_grid_distance_m: float = 0.0"""

assert old_rep in code, "old_rep not found"
code = code.replace(old_rep, new_rep, 1)

# 4. Update build_building_result
old_bbr = """def build_building_result(name: str, length_ft: float, breadth_ft: float, parapet_ft: float, panel_watt: int) -> BuildingResult:
    rooftop_area = round(length_ft * breadth_ft, 2)
    utilized = round(max(0.0, (length_ft - 2 * parapet_ft) * (breadth_ft - 2 * parapet_ft)), 2)
    capacity_kw = round(utilized / 100.0, 2)

    panels = ceil_to_int((capacity_kw * 1000.0) / panel_watt)
    installed_kwp = round((panels * panel_watt) / 1000.0, 2)

    total_plant_kw = max(capacity_kw, installed_kwp)
    inverter_kw = select_inverter_lt(total_plant_kw)
    phase_3 = inverter_kw > 5.0
    inv_cable, isolator = inverter_cable_and_isolator(inverter_kw, phase_3)

    strings = max(1, ceil_to_int(panels / 20.0))
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

new_bbr = """def build_building_result(name: str, length_ft: float, breadth_ft: float, parapet_ft: float, panel_watt: int, panel_tech: str = "Mono-PERC (Mono-facial)") -> BuildingResult:
    rooftop_area = round(length_ft * breadth_ft, 2)
    utilized = round(max(0.0, (length_ft - 2 * parapet_ft) * (breadth_ft - 2 * parapet_ft)), 2)
    capacity_kw = round(utilized / 100.0, 2)

    panels = ceil_to_int((capacity_kw * 1000.0) / panel_watt)
    installed_kwp = round((panels * panel_watt) / 1000.0, 2)

    total_plant_dc_kw = max(capacity_kw, installed_kwp)
    ac_calculated_kw = round(total_plant_dc_kw * 0.70, 2)
    inverter_kw = select_inverter_lt(total_plant_dc_kw)
    phase_3 = inverter_kw > 5.0
    inv_cable, isolator = inverter_cable_and_isolator(inverter_kw, phase_3)

    strings = max(1, ceil_to_int(panels / 20.0))
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
        panel_tech=panel_tech,
        ac_calculated_kw=ac_calculated_kw,
    )"""

assert old_bbr in code, "old_bbr not found"
code = code.replace(old_bbr, new_bbr, 1)

# 5. Update build_system_report: pass ac_calculated_kw to select_acdb_components
old_bsr = """    installed_dc_kwp = round((report.total_panels * panel_watt) / 1000.0, 2)
    total_system_inverter_kw = sum(b.inverter_kw for b in building_results)

    # Dynamic ACDB Sizing based on Inverter AC Output
    acdb_components, breaker_rating, rated_current_a, grid_cable, busbar = select_acdb_components(total_system_inverter_kw, distance_m)
    report.acdb_components = acdb_components
    report.acdb_current_a = breaker_rating
    report.acdb_rated_current_a = rated_current_a
    report.acdb_grid_cable = grid_cable
    report.acdb_busbar = busbar

    # Bill of Materials (BOM) Generation with consistent ACDB breaker rating
    bom_items, plant_total_cost, escom_budget = generate_plant_bom(
        capacity_kw=report.total_capacity_kw,
        inverter_kw=total_system_inverter_kw,
        panel_watt=panel_watt,
        panel_count=report.total_panels,
        acdb_breaker_rating=breaker_rating,
        bldg_results=building_results,
        dist_m=distance_m,
    )"""

new_bsr = """    installed_dc_kwp = round((report.total_panels * panel_watt) / 1000.0, 2)
    total_plant_dc = max(report.total_capacity_kw, installed_dc_kwp)
    report.ac_calculated_kw = round(total_plant_dc * 0.70, 2)
    total_system_inverter_kw = sum(b.inverter_kw for b in building_results)

    # Requirement 2: Size AC components by calculated derated power (P_dc * 0.70)
    acdb_components, breaker_rating, rated_current_a, grid_cable, busbar = select_acdb_components(report.ac_calculated_kw, distance_m)
    report.acdb_components = acdb_components
    report.acdb_current_a = breaker_rating
    report.acdb_rated_current_a = rated_current_a
    report.acdb_grid_cable = grid_cable
    report.acdb_busbar = busbar

    # Bill of Materials (BOM) Generation with consistent ACDB breaker rating and panel technology
    bom_items, plant_total_cost, escom_budget = generate_plant_bom(
        capacity_kw=report.total_capacity_kw,
        inverter_kw=total_system_inverter_kw,
        panel_watt=panel_watt,
        panel_count=report.total_panels,
        acdb_breaker_rating=breaker_rating,
        bldg_results=building_results,
        dist_m=distance_m,
        panel_tech=report.panel_tech,
    )"""

assert old_bsr in code, "old_bsr not found"
code = code.replace(old_bsr, new_bsr, 1)

# In build_system_report: also pass panel_tech in SiteResult
old_bsr_sr = """        SiteResult(
            name=report.customer_name or "Site Name-1",
            location=report.location or "Karnataka",
            email=report.email or "",
            mode=report.mode,
            capacity_kw=report.total_capacity_kw,
            raw_capacity_kw=report.total_capacity_kw,
            inverter_kw=total_system_inverter_kw,
            total_panels=report.total_panels,
            panel_watt=panel_watt,
            distance_m=distance_m,"""

new_bsr_sr = """        SiteResult(
            name=report.customer_name or "Site Name-1",
            location=report.location or "Karnataka",
            email=report.email or "",
            mode=report.mode,
            capacity_kw=report.total_capacity_kw,
            raw_capacity_kw=report.total_capacity_kw,
            inverter_kw=total_system_inverter_kw,
            total_panels=report.total_panels,
            panel_watt=panel_watt,
            distance_m=distance_m,
            panel_tech=report.panel_tech,
            ac_calculated_kw=report.ac_calculated_kw,"""

assert old_bsr_sr in code, "old_bsr_sr not found"
code = code.replace(old_bsr_sr, new_bsr_sr, 1)

# In build_system_report: Path 2 bill mode
old_b2_rep = """        cap_kw = round(monthly_units / 120.0, 2)
        utilized = round(cap_kw * 100.0, 2)

        panels = ceil_to_int((cap_kw * 1000.0) / panel_watt)
        installed_kwp = round((panels * panel_watt) / 1000.0, 2)

        total_plant_kw = max(cap_kw, installed_kwp)
        inverter_kw = select_inverter_lt(total_plant_kw)
        phase_3 = inverter_kw > 5.0
        inv_cable, isolator = inverter_cable_and_isolator(inverter_kw, phase_3)

        strings = max(1, ceil_to_int(panels / 20.0))
        building_results.append(
            BuildingResult(
                name="Building 1",
                rooftop_area_sqft=round(utilized, 2),
                utilized_rooftop_area_sqft=round(utilized, 2),
                capacity_kw=cap_kw,
                panel_count=panels,
                strings=strings,
                inverter_kw=inverter_kw,
                inverter_qty=1,
                inverter_cable=inv_cable,
                isolator_rating=isolator,
            )
        )"""

new_b2_rep = """        cap_kw = round(monthly_units / 120.0, 2)
        utilized = round(cap_kw * 100.0, 2)

        panels = ceil_to_int((cap_kw * 1000.0) / panel_watt)
        installed_kwp = round((panels * panel_watt) / 1000.0, 2)

        total_plant_dc = max(cap_kw, installed_kwp)
        ac_calc_kw = round(total_plant_dc * 0.70, 2)
        inverter_kw = select_inverter_lt(total_plant_dc)
        phase_3 = inverter_kw > 5.0
        inv_cable, isolator = inverter_cable_and_isolator(inverter_kw, phase_3)

        strings = max(1, ceil_to_int(panels / 20.0))
        building_results.append(
            BuildingResult(
                name="Building 1",
                rooftop_area_sqft=round(utilized, 2),
                utilized_rooftop_area_sqft=round(utilized, 2),
                capacity_kw=cap_kw,
                panel_count=panels,
                strings=strings,
                inverter_kw=inverter_kw,
                inverter_qty=1,
                inverter_cable=inv_cable,
                isolator_rating=isolator,
                parapet_ft=0.0,
                panel_watt=panel_watt,
                panel_tech=report.panel_tech,
                ac_calculated_kw=ac_calc_kw,
            )
        )"""

assert old_b2_rep in code, "old_b2_rep not found"
code = code.replace(old_b2_rep, new_b2_rep, 1)

# 6. Update build_multi_site_report
old_msr = """                p_watt = safe_int(b.get("panel_watt", 550), 550)
                br = build_building_result(b_name, L, B, parapet, p_watt)"""

new_msr = """                p_watt = safe_int(b.get("panel_watt", 550), 550)
                p_tech = str(b.get("panel_tech", "Mono-PERC (Mono-facial)"))
                br = build_building_result(b_name, L, B, parapet, p_watt, p_tech)"""

assert old_msr in code, "old_msr not found"
code = code.replace(old_msr, new_msr, 1)

# In build_multi_site_report: AC sizing using site_derated_ac_kw
old_msr_ac = """        site_inv_kw = select_inverter_lt(site_cap_kw)
        phase_3 = site_inv_kw > 5.0
        inv_cable, isolator = inverter_cable_and_isolator(site_inv_kw, phase_3)
        acdb_comps, breaker_rating, rated_curr, grid_cable, busbar = select_acdb_components(site_inv_kw, dist_m)"""

new_msr_ac = """        site_derated_ac_kw = round(site_cap_kw * 0.70, 2)
        site_inv_kw = select_inverter_lt(site_cap_kw)
        phase_3 = site_inv_kw > 5.0
        inv_cable, isolator = inverter_cable_and_isolator(site_inv_kw, phase_3)
        acdb_comps, breaker_rating, rated_curr, grid_cable, busbar = select_acdb_components(site_derated_ac_kw, dist_m)"""

assert old_msr_ac in code, "old_msr_ac not found"
code = code.replace(old_msr_ac, new_msr_ac, 1)

# In build_multi_site_report: update SiteResult constructor call
old_msr_sr = """            panel_watt=primary_panel_watt,
            distance_m=dist_m,
            building_reports=bldg_results,"""

new_msr_sr = """            panel_watt=primary_panel_watt,
            distance_m=dist_m,
            panel_tech=bldg_results[0].panel_tech if bldg_results else "Mono-PERC (Mono-facial)",
            ac_calculated_kw=site_derated_ac_kw,
            building_reports=bldg_results,"""

assert old_msr_sr in code, "old_msr_sr not found"
code = code.replace(old_msr_sr, new_msr_sr, 1)

# 7. Update generate_plant_bom
old_gpb = """def generate_plant_bom(
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
"""

new_gpb = """def generate_plant_bom(
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

    if bldg_results and len(bldg_results) > 0:
        total_module_cost = float(sum(b.panel_count * round(b.panel_watt * (10000.0 / 550.0)) for b in bldg_results))
        actual_panel_count = sum(b.panel_count for b in bldg_results)
        distinct_specs = sorted(list(set(f"{b.panel_watt}W {b.panel_tech}" for b in bldg_results)))
        if len(distinct_specs) == 1:
            mod_spec = f"{distinct_specs[0]}"
        else:
            mod_spec = " + ".join([f"{b.name}: {b.panel_watt}W {b.panel_tech} ({b.panel_count} Nos.)" for b in bldg_results])
        mc4_pairs = actual_panel_count
        mod_qty_str = f"{actual_panel_count} Nos."
    else:
        cost_per_module = round(panel_watt * (10000.0 / 550.0))
        total_module_cost = float(panel_count * cost_per_module)
        mc4_pairs = panel_count
        mod_spec = f"{panel_watt} W {panel_tech}"
        mod_qty_str = f"{panel_count} Nos."

    mc4_cost = float(mc4_pairs * 300.0)

    # Inverter specification with certified models
    inv_model = get_inverter_model(inverter_kw)
    model_hint = f" ({inv_model.top_tier_models.split(',')[0]} or equiv.)" if inv_model else ""

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
"""

assert old_gpb in code, "old_gpb not found"
code = code.replace(old_gpb, new_gpb, 1)

with open("solar_pv_estimator.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Updated solar_pv_estimator.py with inverter 70% derating and AC calculated power sizing!")

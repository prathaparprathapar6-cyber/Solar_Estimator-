import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("solar_pv_estimator.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add JSON Database helper functions and constants near the top of solar_pv_estimator.py
db_helpers_code = '''
# ============================================================
# KERC & ESCOM REGULATORY CONSTANTS & DATABASE PERSISTENCE
# ============================================================
KERC_LT_CEILING_KW = 20.0
KERC_DT_UTILIZATION_LIMIT = 0.80  # Max 80% of distribution transformer capacity
KERC_CUF_ROOFTOP_PCT = 19.0      # KERC 2013/2016 normative CUF for rooftop solar
KERC_PLANT_LIFE_YEARS = 25

DB_DIR = os.path.dirname(os.path.abspath(__file__))
ADMINS_DB_FILE = os.path.join(DB_DIR, "admins_db.json")
VISITORS_DB_FILE = os.path.join(DB_DIR, "visitors_db.json")
FEEDBACK_DB_FILE = os.path.join(DB_DIR, "feedback_db.json")
PRICING_DB_FILE = os.path.join(DB_DIR, "pricing_db.json")

INITIAL_ADMINS = [
    {
        "username": "Adarsha KM",
        "emails": ["adarshakm@jnnce.ac.in", "adarshakmsgr50@gmail.com"],
        "mobile": "8073398259",
        "password": "Adarsh@123321",
        "role": "super_admin",
        "status": "approved",
        "created_at": "2026-09-22T00:00:00Z"
    },
    {
        "username": "Prathapa R",
        "emails": ["prathaparprathapar6@gmail.com"],
        "mobile": "",
        "password": "Prathap@123",
        "role": "admin",
        "status": "approved",
        "created_at": "2026-09-22T00:00:00Z"
    },
    {
        "username": "D Nihar",
        "emails": ["nihar333k@gmail.com"],
        "mobile": "",
        "password": "Nihar@123",
        "role": "admin",
        "status": "approved",
        "created_at": "2026-09-22T00:00:00Z"
    },
    {
        "username": "Ajjanna NG",
        "emails": ["nga_ee@jnnce.ac.in"],
        "mobile": "",
        "password": "Admin@123",
        "role": "admin",
        "status": "approved",
        "created_at": "2026-09-22T00:00:00Z"
    }
]

DEFAULT_PRICING_MAP = {
    "module_per_wp": 18.18,
    "inverter_per_kw": 10500.0,
    "structure_per_kw": 4800.0,
    "dc_cable_per_m": 85.0,
    "ac_cable_per_m": 180.0,
    "mc4_per_pair": 300.0,
    "dcdb_base": 7000.0,
    "acdb_base": 7000.0,
    "earthing_kit_base": 7500.0,
    "lightning_arrester_base": 4000.0,
    "accessories_per_kw": 1200.0,
    "installation_per_kw": 4000.0,
    "escom_application_fee": 1000.0,
    "escom_processing_fee": 2000.0,
    "escom_stamp_duty": 12.0,
    "escom_net_meter": 12000.0,
    "escom_security_deposit": 8000.0,
}

def init_databases():
    if not os.path.exists(ADMINS_DB_FILE):
        try:
            with open(ADMINS_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(INITIAL_ADMINS, f, indent=2)
        except Exception:
            pass
    if not os.path.exists(VISITORS_DB_FILE):
        try:
            with open(VISITORS_DB_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        except Exception:
            pass
    if not os.path.exists(FEEDBACK_DB_FILE):
        try:
            with open(FEEDBACK_DB_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        except Exception:
            pass
    if not os.path.exists(PRICING_DB_FILE):
        try:
            with open(PRICING_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_PRICING_MAP, f, indent=2)
        except Exception:
            pass

init_databases()

def db_load_json(file_path, default_val):
    if not os.path.exists(file_path):
        return default_val
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_val

def db_save_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False
'''

# Check if db_helpers already in code
if "KERC_LT_CEILING_KW = 20.0" not in code:
    marker = "# Ensure assets are present at module load\nensure_standalone_assets()\n"
    assert marker in code, "Asset marker not found in solar_pv_estimator.py"
    code = code.replace(marker, marker + db_helpers_code, 1)

# 2. Update Dataclasses with contact_number, sanctioned_load_kw, etc.
old_bldg_res = '''@dataclass
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
    ac_calculated_kw: float = 0.0'''

new_bldg_res = '''@dataclass
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
    ac_calculated_kw: float = 0.0
    sanctioned_load_kw: Optional[float] = None
    contact_number: str = ""
    roof_area_required_sqft: float = 0.0
    roof_area_status: str = ""'''

assert old_bldg_res in code, "old_bldg_res not found"
code = code.replace(old_bldg_res, new_bldg_res, 1)

old_site_res = '''@dataclass
class SiteResult:
    name: str
    location: str
    email: str
    mode: str
    capacity_kw: float
    raw_capacity_kw: float
    inverter_kw: float
    total_panels: int
    panel_watt: int
    distance_m: float
    panel_tech: str = "Mono-PERC (Mono-facial)"
    ac_calculated_kw: float = 0.0'''

new_site_res = '''@dataclass
class SiteResult:
    name: str
    location: str
    email: str
    mode: str
    capacity_kw: float
    raw_capacity_kw: float
    inverter_kw: float
    total_panels: int
    panel_watt: int
    distance_m: float
    panel_tech: str = "Mono-PERC (Mono-facial)"
    ac_calculated_kw: float = 0.0
    contact_number: str = ""
    sanctioned_load_kw: Optional[float] = None
    roof_area_required_sqft: float = 0.0
    roof_area_status: str = ""
    kerc_regulations_notes: List[str] = field(default_factory=list)'''

assert old_site_res in code, "old_site_res not found"
code = code.replace(old_site_res, new_site_res, 1)

old_ltd_res = '''@dataclass
class LTDesignReport:
    application_type: str
    mode: str
    customer_name: str = ""
    location: str = ""
    email: str = ""'''

new_ltd_res = '''@dataclass
class LTDesignReport:
    application_type: str
    mode: str
    customer_name: str = ""
    location: str = ""
    email: str = ""
    contact_number: str = ""
    sanctioned_load_kw: Optional[float] = None
    roof_area_required_sqft: float = 0.0
    roof_area_status: str = ""
    kerc_regulations_notes: List[str] = field(default_factory=list)'''

assert old_ltd_res in code, "old_ltd_res not found"
code = code.replace(old_ltd_res, new_ltd_res, 1)

with open("solar_pv_estimator.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Part 1 applied to solar_pv_estimator.py!")

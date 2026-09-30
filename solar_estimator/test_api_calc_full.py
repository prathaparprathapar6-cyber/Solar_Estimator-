import json
import math
import datetime
from solar_pv_estimator import (
    build_system_report,
    build_multi_site_report,
    safe_float,
    safe_int,
    TARIFF_25Y
)

def handle_api_calculate(data: dict) -> dict:
    mode = data.get("mode", "roof")
    customer_name = data.get("customer_name", "Solar Site")
    location = data.get("location", "Karnataka")
    email = data.get("email", "")
    contact_number = str(data.get("contact_number", "")).strip()
    sanctioned_load_kw = safe_float(data.get("sanctioned_load_kw")) if data.get("sanctioned_load_kw") else None
    custom_tariff = safe_float(data.get("custom_tariff", 8.05), 8.05)
    sites_data = data.get("sites")

    if sites_data and len(sites_data) > 0:
        rep = build_multi_site_report(
            sites_data=sites_data,
            project_name=customer_name,
            location=location,
            email=email,
            custom_tariff=custom_tariff,
            contact_number=contact_number,
            sanctioned_load_kw=sanctioned_load_kw,
        )
    else:
        L = safe_float(data.get("length_ft", 40.0), 40.0)
        B = safe_float(data.get("breadth_ft", 30.0), 30.0)
        parapet_ft = safe_float(data.get("parapet_ft", 1.5), 1.5)
        monthly_units = safe_float(data.get("monthly_units", 1200.0), 1200.0)
        distance_m = safe_float(data.get("distance_m", 20.0), 20.0)
        panel_watt = safe_int(data.get("panel_watt", 550), 550)
        panel_tech = str(data.get("panel_tech", "Mono-PERC (Mono-facial)"))
        buildings = [("Building 1", L, B)]
        rep = build_system_report(
            mode=mode,
            buildings=buildings,
            parapet_ft=parapet_ft,
            monthly_units=monthly_units,
            distance_m=distance_m,
            panel_watt=panel_watt,
            customer_name=customer_name,
            location=location,
            email=email,
            panel_tech=panel_tech,
            contact_number=contact_number,
            sanctioned_load_kw=sanctioned_load_kw,
        )

    # 12-item plant BOM
    bom_items = []
    for item in rep.bom_items:
        bom_items.append({
            "sl": item.sl_no,
            "desc": item.description,
            "spec": item.specification,
            "qty": item.quantity,
            "amt": round(item.amount_inr, 2)
        })

    # ESCOM items
    escom_specs = {
        "registration": ("Application & Registration Fee", "Online portal fee (+18% GST)", False),
        "facilitation": ("Facilitation & Processing Fee", "Field inspection (+18% GST)", False),
        "ppa_esign": ("PPA e-Sign Charge", "Statutory agreement stamping", False),
        "meter_estimate": ("Bi-Directional Net Meter", "Meter testing & approval", False),
        "security_deposit": ("Refundable Security Deposit", "LT connectivity deposit", True),
    }
    escom_list = []
    sl_i = 1
    for k, amt in rep.escom_budget.items():
        name, spec, is_ref = escom_specs.get(k, (k.replace('_', ' ').title(), "Statutory utility procedure", False))
        escom_list.append({
            "sl": sl_i,
            "name": name,
            "spec": spec,
            "amt": round(amt, 2),
            "note": "Refundable" if is_ref else "+ 18% GST"
        })
        sl_i += 1

    # Amortization schedule (25 years)
    amort_list = []
    cur_g = rep.annual_generation_kwh
    cum_net = 0.0
    scale = (custom_tariff / TARIFF_25Y[0]) if custom_tariff > 0 else 1.0
    amc_y = rep.total_capacity_kw * 600.0

    for y_idx in range(25):
        base_t = TARIFF_25Y[y_idx if y_idx < len(TARIFF_25Y) else -1]
        t_val = round(base_t * scale, 2)
        rev = cur_g * t_val
        net_val = rev - amc_y
        cum_net += net_val
        amort_list.append({
            "year": y_idx + 1,
            "gen": round(cur_g),
            "tariff": f"{t_val:.2f}",
            "revenue": round(rev),
            "amc": round(amc_y),
            "net": round(net_val),
            "cum": round(cum_net)
        })
        cur_g *= 0.99

    res = {
        "schemaVersion": 1,
        "calculated_at": datetime.datetime.now().isoformat(),
        "customer_name": rep.customer_name,
        "location": rep.location,
        "mode": rep.mode,
        "capacityKw": round(rep.total_capacity_kw, 2),
        "installedDckWp": round((rep.total_panels * rep.panel_watt) / 1000.0, 2),
        "rawCapacityKw": round(rep.total_capacity_kw, 2),
        "isCapped20kW": rep.total_capacity_kw >= 20.0 or (sanctioned_load_kw is not None and sanctioned_load_kw >= 20.0),
        "kercNotice": "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" if (rep.total_capacity_kw >= 20.0 or (sanctioned_load_kw is not None and sanctioned_load_kw >= 20.0)) else "",
        "roofAreaStatus": rep.roof_area_status,
        "panels": rep.total_panels,
        "strings": max(1, math.ceil(rep.total_panels / 20.0)),
        "invKw": round(rep.ac_calculated_kw, 2),
        "phase3": rep.ac_calculated_kw > 5.0,
        "deratedAcKw": round(rep.ac_calculated_kw, 2),
        "invCable": {
            "cable": rep.acdb_grid_cable,
            "isolator": f"{int(rep.acdb_current_a)}A MCB",
            "current": rep.acdb_current_a
        },
        "acdb": {
            "breakerRating": int(rep.acdb_current_a),
            "ratedCurrent": rep.acdb_rated_current_a,
            "gridCable": rep.acdb_grid_cable,
            "busbar": rep.acdb_busbar,
            "components": [[c[0], c[1]] for c in rep.acdb_components] if rep.acdb_components else []
        },
        "bom": {
            "items": bom_items,
            "plantTotal": round(rep.bom_plant_total_inr, 2),
            "escom": escom_list,
            "escomTotal": round(rep.total_escom_budget_inr, 2),
            "totalCapitalOutlay": round(rep.grand_total_capital_inr, 2)
        },
        "monthly": rep.monthly_generation_kwh,
        "annual": round(rep.annual_generation_kwh, 2),
        "series25": [round(rep.annual_generation_kwh * (0.99 ** y), 2) for y in range(25)],
        "total25": round(rep.total_generation_25y_kwh, 2),
        "pr": rep.performance_ratio_pr,
        "cuf": rep.capacity_utilization_factor_cuf,
        "sysEff": rep.system_efficiency_pct,
        "specificYield": rep.specific_energy_yield_kwh_per_kw,
        "amort": amort_list,
        "payY": rep.payback_years,
        "payM": rep.payback_months,
        "lifetimeProfit": rep.post_payback_profit_inr,
        "fd25y": rep.fd_25y_inr,
        "co2": rep.carbon_emission_reduction_tonnes_25y,
        "trees": rep.trees_planted_25y,
        "carKm": int((rep.carbon_emission_reduction_tonnes_25y * 1000) / 0.12),
        "coalT": round(rep.total_generation_25y_kwh * 0.0004, 1),
        "sitesCount": len(rep.site_reports) if rep.site_reports else 1
    }
    return res

# Test execution
sample = {
    "customer_name": "Integrated Educational Campus",
    "location": "Shivamogga, Karnataka",
    "sanctioned_load_kw": 18.0,
    "mode": "roof",
    "length_ft": 52.0,
    "breadth_ft": 36.0,
    "parapet_ft": 1.5,
    "panel_watt": 550
}

dto = handle_api_calculate(sample)
print("TEST SUCCESSFUL!")
print("schemaVersion:", dto["schemaVersion"])
print("capacityKw:", dto["capacityKw"])
print("panels:", dto["panels"])
print("invKw:", dto["invKw"])
print("plantTotal:", dto["bom"]["plantTotal"])
print("payback:", dto["payY"], "years", dto["payM"], "months")

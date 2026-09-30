import json
from solar_pv_estimator import (
    build_system_report,
    build_multi_site_report,
    safe_float,
    safe_int
)

def api_calculate(data):
    schemaVersion = 1
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

    # Format resultDto
    bom_items = []
    for item in rep.bom.items:
        bom_items.append({
            "sl": item.sl_no,
            "desc": item.desc,
            "spec": item.spec,
            "qty": item.qty,
            "amt": item.amount_inr
        })
    escom_items = []
    for e in rep.escom_budget:
        escom_items.append({
            "sl": e.sl_no,
            "name": e.statutory_stage,
            "spec": e.specification,
            "amt": e.estimated_budget_inr,
            "note": e.refundable_note
        })

    amort_rows = []
    for row in rep.amort_rows:
        amort_rows.append({
            "year": row.year,
            "gen": row.gen_kwh,
            "tariff": f"{row.tariff_rs_kwh:.2f}",
            "revenue": row.gross_revenue,
            "amc": row.amc_cost,
            "net": row.net_annual_savings,
            "cum": row.cumulative_net_savings
        })

    result_dto = {
        "schemaVersion": schemaVersion,
        "customer_name": rep.customer_name,
        "location": rep.location,
        "mode": rep.mode,
        "capacityKw": rep.plant_capacity_kw,
        "installedDckWp": rep.installed_dc_kwp,
        "rawCapacityKw": rep.raw_capacity_kw,
        "isCapped20kW": rep.raw_capacity_kw > 20.0 or (sanctioned_load_kw is not None and sanctioned_load_kw >= 20.0),
        "kercNotice": "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations" if (rep.raw_capacity_kw >= 20.0 or (sanctioned_load_kw is not None and sanctioned_load_kw >= 20.0)) else "",
        "roofAreaStatus": rep.roof_area_status,
        "panels": rep.no_of_panels,
        "strings": rep.no_of_strings,
        "invKw": rep.inverter_rating_kw,
        "phase3": rep.inverter_rating_kw > 5.0,
        "deratedAcKw": rep.derated_ac_capacity_kw,
        "invCable": {
            "cable": rep.inv_cable_size,
            "isolator": rep.inv_isolator,
            "current": rep.inv_isolator_rating
        },
        "acdb": {
            "breakerRating": rep.acdb_breaker_rating,
            "ratedCurrent": rep.acdb_rated_current,
            "gridCable": rep.acdb_grid_cable,
            "busbar": rep.acdb_busbar,
            "components": [[c.name, c.spec] for c in rep.acdb_components]
        },
        "bom": {
            "items": bom_items,
            "plantTotal": rep.bom.total_plant_cost,
            "escom": escom_items,
            "escomTotal": rep.escom_total,
            "totalCapitalOutlay": rep.total_capital_outlay
        },
        "monthly": rep.monthly_generation,
        "annual": rep.annual_generation_kwh,
        "series25": rep.generation_25yr_series,
        "total25": rep.total_25yr_generation_kwh,
        "pr": rep.performance_ratio,
        "cuf": rep.capacity_utilization_factor,
        "sysEff": rep.system_efficiency,
        "specificYield": rep.specific_yield,
        "amort": amort_rows,
        "payY": rep.payback_years,
        "payM": rep.payback_months,
        "lifetimeProfit": rep.lifetime_profit,
        "fd25y": rep.fd_opportunity_cost_25y,
        "co2": rep.co2_avoided_tons,
        "trees": rep.trees_equivalent,
        "carKm": rep.car_km_avoided,
        "coalT": rep.coal_avoided_tons,
        "sitesCount": len(rep.site_summaries) if rep.site_summaries else 1
    }

    if rep.site_summaries:
        result_dto["site_summaries"] = [
            {
                "site_no": s.site_no,
                "site_name": s.site_name,
                "location": s.location,
                "buildings_count": s.buildings_count,
                "capacity_kw": s.capacity_kw,
                "raw_capacity_kw": s.raw_capacity_kw,
                "is_capped": s.is_capped,
                "plant_cost": s.plant_cost,
                "escom_budget": s.escom_budget,
                "total_outlay": s.total_outlay
            }
            for s in rep.site_summaries
        ]

    return result_dto

# Test the function with a sample payload
sample_payload = {
    "schemaVersion": 1,
    "customer_name": "Test Site 1",
    "location": "Shivamogga, Karnataka",
    "mode": "roof",
    "sanctioned_load_kw": 12.0,
    "buildings": [
        {"name": "Building 1", "length_ft": 50, "breadth_ft": 35, "parapet_ft": 1.5, "panel_watt": 550}
    ]
}

res = api_calculate(sample_payload)
print("api_calculate SUCCESS!")
print(f"schemaVersion: {res['schemaVersion']}")
print(f"capacityKw: {res['capacityKw']}")
print(f"panels: {res['panels']}")
print(f"invKw: {res['invKw']}")
print(f"plantTotal: ₹{res['bom']['plantTotal']:,}")
print(f"payback: {res['payY']} Yrs {res['payM']} Mos")
print(f"isCapped20kW: {res['isCapped20kW']}")

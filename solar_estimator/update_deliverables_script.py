with open("generate_final_deliverables.py", "r", encoding="utf-8") as f:
    content = f.read()

# Update single_rep in generate_final_deliverables.py
old_single_call = '''single_rep = build_system_report(
    mode="roof",
    buildings=[("Residential Rooftop", 35.0, 25.0)],
    parapet_ft=1.5,
    monthly_units=0,
    distance_m=20.0,
    panel_watt=550,
    panel_tech="N-Type TOPCon",
    customer_name="Sri. H. R. Vishwanath",
    location="Shivamogga, Karnataka",
    email="vishwanath@voltroof.in"
)'''

new_single_call = '''single_rep = build_system_report(
    mode="roof",
    buildings=[("Residential Rooftop", 35.0, 25.0)],
    parapet_ft=1.5,
    monthly_units=0,
    distance_m=20.0,
    panel_watt=550,
    panel_tech="N-Type TOPCon",
    customer_name="Sri. H. R. Vishwanath",
    contact_number="+91 94481 23456",
    sanctioned_load_kw=10.0,
    location="Shivamogga, Karnataka",
    email="vishwanath@voltroof.in"
)'''

assert old_single_call in content, "old_single_call not found"
content = content.replace(old_single_call, new_single_call)

# Update multi_sites_data in generate_final_deliverables.py
old_multi_sites = '''multi_sites_data = [
    {
        "name": "Site 1 - PESIT Engineering Campus",
        "location": "Shivamogga, Karnataka",
        "distance_m": 25.0,
        "buildings": [
            {
                "name": "Admin Block",
                "length_ft": 45.0,
                "breadth_ft": 35.0,
                "parapet_ft": 1.5,
                "panel_watt": 400,
                "panel_tech": "Mono-PERC (Mono-facial)"
            },
            {
                "name": "Computer Science Lab",
                "length_ft": 40.0,
                "breadth_ft": 30.0,
                "parapet_ft": 1.5,
                "panel_watt": 580,
                "panel_tech": "N-Type TOPCon"
            }
        ]
    },
    {
        "name": "Site 2 - PES University Innovation Hub",
        "location": "Bengaluru, Karnataka",
        "distance_m": 15.0,
        "buildings": [
            {
                "name": "Tower A Innovation Hub",
                "length_ft": 52.0,
                "breadth_ft": 36.0,
                "parapet_ft": 1.5,
                "panel_watt": 550,
                "panel_tech": "Bifacial (Mono / TOPCon)"
            }
        ]
    }
]'''

new_multi_sites = '''multi_sites_data = [
    {
        "name": "Site 1 - PESIT Engineering Campus",
        "location": "Shivamogga, Karnataka",
        "contact_number": "+91 98450 11223",
        "sanctioned_load_kw": 25.0,
        "distance_m": 25.0,
        "buildings": [
            {
                "name": "Admin Block",
                "length_ft": 45.0,
                "breadth_ft": 35.0,
                "parapet_ft": 1.5,
                "panel_watt": 400,
                "panel_tech": "Mono-PERC (Mono-facial)"
            },
            {
                "name": "Computer Science Lab",
                "length_ft": 40.0,
                "breadth_ft": 30.0,
                "parapet_ft": 1.5,
                "panel_watt": 580,
                "panel_tech": "N-Type TOPCon"
            }
        ]
    },
    {
        "name": "Site 2 - PES University Innovation Hub",
        "location": "Bengaluru, Karnataka",
        "contact_number": "+91 98452 99887",
        "sanctioned_load_kw": 18.0,
        "distance_m": 15.0,
        "buildings": [
            {
                "name": "Tower A Innovation Hub",
                "length_ft": 52.0,
                "breadth_ft": 36.0,
                "parapet_ft": 1.5,
                "panel_watt": 550,
                "panel_tech": "Bifacial (Mono / TOPCon)"
            }
        ]
    }
]'''

assert old_multi_sites in content, "old_multi_sites not found"
content = content.replace(old_multi_sites, new_multi_sites)

# Add solar_gui.py to file copy list and zip
if '"solar_gui.py"' not in content:
    content = content.replace(
        'for f_name in ["voltroof_solar_pv_estimator_standalone.html", "voltroof_solar_pv_estimator.html", "solar_pv_estimator.py", "solar_pv_estimator_standalone.py"]:',
        'for f_name in ["voltroof_solar_pv_estimator_standalone.html", "voltroof_solar_pv_estimator.html", "solar_pv_estimator.py", "solar_pv_estimator_standalone.py", "solar_gui.py"]:'
    )
    content = content.replace(
        '("solar_pv_estimator_standalone.py", "solar_pv_estimator_standalone.py"),',
        '("solar_pv_estimator_standalone.py", "solar_pv_estimator_standalone.py"),\n    ("solar_gui.py", "solar_gui.py"),'
    )

with open("generate_final_deliverables.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated generate_final_deliverables.py successfully!")

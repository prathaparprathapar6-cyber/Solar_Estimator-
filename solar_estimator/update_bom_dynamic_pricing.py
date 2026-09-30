# -*- coding: utf-8 -*-
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(cur_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    text = f.read()

target = '''    const invCost = inverterKw * 10500.0;
    items = [
      { sl: 1, desc: "Solar PV modules", spec: `${panelWatt} W mono PERC / TOPCon`, qty: `${panelCount} Nos.`, amt: totalModuleCost },
      { sl: 2, desc: "On-grid inverter", spec: invSpec, qty: "1 No.", amt: Math.round(invCost) },
      { sl: 3, desc: "Rooftop mounting structure", spec: "HDGI rooftop structure, module-compatible", qty: "1 Set", amt: Math.round(cap * 4800.0) },
      { sl: 4, desc: "DC solar cable", spec: "4-6 sq.mm copper, PV-rated", qty: `${Math.max(20, Math.round(cap * 11))} m`, amt: Math.round(cap * 935.0) },
      { sl: 5, desc: "AC cable", spec: "4-10 sq.mm copper", qty: `${Math.max(15, Math.round(cap * 6))} m`, amt: Math.round(cap * 2400.0) },
      { sl: 6, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost },
      { sl: 7, desc: "DCDB", spec: "Isolator + fuse + Type-II DC SPD", qty: "1 No.", amt: 18000.0 },
      { sl: 8, desc: "ACDB", spec: acdbSpec, qty: "1 No.", amt: 18000.0 },
      { sl: 9, desc: "Earthing kit", spec: "Chemical earth electrodes & accessories (IS 3043)", qty: "3 Nos.", amt: 9000.0 },
      { sl: 10, desc: "Lightning arrester", spec: "Standard rooftop PV type", qty: "1 No.", amt: 8000.0 },
      { sl: 11, desc: "Installation accessories", spec: "Lugs, ferrules, clamps, conduit, glands, etc.", qty: "1 Lot", amt: Math.round(cap * 1900.0) },
      { sl: 12, desc: "Installation & commissioning", spec: "Labour, testing and commissioning", qty: "1 Job", amt: Math.round(cap * 4750.0) },
    ];'''

replacement = '''    const invCost = inverterKw * invRate;
    items = [
      { sl: 1, desc: "Solar PV modules", spec: `${panelWatt} W mono PERC / TOPCon`, qty: `${panelCount} Nos.`, amt: totalModuleCost },
      { sl: 2, desc: "On-grid inverter", spec: invSpec, qty: "1 No.", amt: Math.round(invCost) },
      { sl: 3, desc: "Rooftop mounting structure", spec: "HDGI rooftop structure, module-compatible", qty: "1 Set", amt: Math.round(cap * structRate) },
      { sl: 4, desc: "DC solar cable", spec: "4-6 sq.mm copper, PV-rated", qty: `${Math.max(20, Math.round(cap * 11))} m`, amt: Math.round(cap * (typeof dynamicPricing !== 'undefined' && dynamicPricing.dc_cable_per_m ? dynamicPricing.dc_cable_per_m * 11 : 935.0)) },
      { sl: 5, desc: "AC cable", spec: "4-10 sq.mm copper", qty: `${Math.max(15, Math.round(cap * 6))} m`, amt: Math.round(cap * (typeof dynamicPricing !== 'undefined' && dynamicPricing.ac_cable_per_m ? dynamicPricing.ac_cable_per_m * 6 : 2400.0)) },
      { sl: 6, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost },
      { sl: 7, desc: "DCDB", spec: "Isolator + fuse + Type-II DC SPD", qty: "1 No.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.dcdb_base ? dynamicPricing.dcdb_base : 18000.0) },
      { sl: 8, desc: "ACDB", spec: acdbSpec, qty: "1 No.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.acdb_base ? dynamicPricing.acdb_base : 18000.0) },
      { sl: 9, desc: "Earthing kit", spec: "Chemical earth electrodes & accessories (IS 3043)", qty: "3 Nos.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.earthing_kit_base ? dynamicPricing.earthing_kit_base : 9000.0) },
      { sl: 10, desc: "Lightning arrester", spec: "Standard rooftop PV type", qty: "1 No.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.lightning_arrester_base ? dynamicPricing.lightning_arrester_base : 8000.0) },
      { sl: 11, desc: "Installation accessories", spec: "Lugs, ferrules, clamps, conduit, glands, etc.", qty: "1 Lot", amt: Math.round(cap * (typeof dynamicPricing !== 'undefined' && dynamicPricing.accessories_per_kw ? dynamicPricing.accessories_per_kw : 1900.0)) },
      { sl: 12, desc: "Installation & commissioning", spec: "Labour, testing and commissioning", qty: "1 Job", amt: Math.round(cap * instRate) },
    ];'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: Dynamic pricing fallback wired into generatePlantBom!")
else:
    print("TARGET NOT FOUND IN INDEX.HTML")

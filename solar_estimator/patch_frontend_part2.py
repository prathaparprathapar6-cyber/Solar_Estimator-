import re

def patch_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"Patching part 2 for {filepath}...")

    # 1. Replace Area per Panel card HTML
    old_panel_area = re.compile(r'<div class="cell-lbl">Area per Panel</div>\s*<div class="cell-val">21\.5 sq\.ft</div>\s*<div class="cell-sub">\(2\.0 m²\)</div>')
    new_panel_area = '''<div class="cell-lbl">Area per Panel</div>
                      <div class="cell-val" id="rtPanelAreaSqft">27.8 sq.ft</div>
                      <div class="cell-sub" id="rtPanelAreaM2">(2.58 m²)</div>'''
    if old_panel_area.search(html):
        html = old_panel_area.sub(new_panel_area, html, count=1)
        print("  - Replaced Area per Panel card HTML with dynamic IDs")

    # 2. In liveUpdate: ensure rtPanelAreaSqft and rtPanelAreaM2 are updated
    if "rtPanelAreaSqft" in html and "document.getElementById(\"rtPanelAreaSqft\")" not in html:
        live_upd_marker = 'const strings = Math.max(1, Math.ceil(panels / 20.0));'
        panel_area_update_code = '''const strings = Math.max(1, Math.ceil(panels / 20.0));
  const modSpecs = typeof getPanelPhysicalSpecs === 'function' ? getPanelPhysicalSpecs(panelW, s.tech || "Mono-PERC") : { area_sqft: 27.8, area_m2: 2.58 };
  const elPanelAreaSqft = document.getElementById("rtPanelAreaSqft");
  const elPanelAreaM2 = document.getElementById("rtPanelAreaM2");
  if (elPanelAreaSqft) elPanelAreaSqft.textContent = `${modSpecs.area_sqft} sq.ft`;
  if (elPanelAreaM2) elPanelAreaM2.textContent = `(${modSpecs.area_m2} m²)`;'''
        html = html.replace(live_upd_marker, panel_area_update_code, 1)
        print("  - Wired real module physical dimensions into liveUpdate")

    # 3. Replace generatePlantBom
    idx = html.find('function generatePlantBom(')
    end_marker = 'return { items, plantTotal, escom, escomTotal, totalCapitalOutlay };\n}'
    end = html.find(end_marker, idx)
    if end != -1:
        end += len(end_marker)
        print(f"  - Found generatePlantBom from {idx} to {end}")
        
        new_bom_impl = '''function generatePlantBom(capacityKw, inverterKw, panelWatt, panelCount, acdbBreakerRating, bldgResults, dist, panelTech) {
  const cap = Math.max(1.0, capacityKw);
  const roundedCap = Math.round(cap);

  let totalModuleCost = 0;
  let mc4Pairs = panelCount;
  const pTech = panelTech || (bldgResults && bldgResults[0]?.panelTech) || "Mono-PERC (Mono-facial)";
  let modSpec = `${panelWatt} W ${pTech}`;
  let modQty = `${panelCount} Nos.`;

  const modRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.module_per_wp) ? dynamicPricing.module_per_wp : 18.18;
  const invRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.inverter_per_kw) ? dynamicPricing.inverter_per_kw : 10500.0;
  const structRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.structure_per_kw) ? dynamicPricing.structure_per_kw : 4800.0;
  const dcRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.dc_cable_per_m) ? dynamicPricing.dc_cable_per_m : 85.0;
  const acRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.ac_cable_per_m) ? dynamicPricing.ac_cable_per_m : 180.0;
  const mc4Rate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.mc4_per_pair) ? dynamicPricing.mc4_per_pair : 300.0;
  const dcdbBase = (typeof dynamicPricing !== 'undefined' && dynamicPricing.dcdb_base) ? dynamicPricing.dcdb_base : 7000.0;
  const acdbBase = (typeof dynamicPricing !== 'undefined' && dynamicPricing.acdb_base) ? dynamicPricing.acdb_base : 7000.0;
  const earthingBase = (typeof dynamicPricing !== 'undefined' && dynamicPricing.earthing_kit_base) ? dynamicPricing.earthing_kit_base : 7500.0;
  const laBase = (typeof dynamicPricing !== 'undefined' && dynamicPricing.lightning_arrester_base) ? dynamicPricing.lightning_arrester_base : 4000.0;
  const accRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.accessories_per_kw) ? dynamicPricing.accessories_per_kw : 1200.0;
  const instRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.installation_per_kw) ? dynamicPricing.installation_per_kw : 4000.0;

  if (bldgResults && bldgResults.length > 0) {
    totalModuleCost = bldgResults.reduce((sum, b) => sum + (b.panels * Math.round((b.panelW || 550) * modRate)), 0);
    mc4Pairs = bldgResults.reduce((sum, b) => sum + b.panels, 0);
    modQty = `${mc4Pairs} Nos.`;
    const distinctSpecs = [...new Set(bldgResults.map(b => `${b.panelW || 550}W ${b.panelTech || pTech}`))];
    if (distinctSpecs.length === 1) {
      modSpec = distinctSpecs[0];
    } else {
      modSpec = bldgResults.map(b => `${b.name || 'Building'}: ${b.panelW || 550}W ${b.panelTech || pTech} (${b.panels} Nos.)`).join(" + ");
    }
  } else {
    const costPerModule = Math.round(panelWatt * modRate);
    totalModuleCost = panelCount * costPerModule;
  }

  const mc4Cost = mc4Pairs * mc4Rate;
  const invMeta = INVERTER_MASTER_CATALOG[inverterKw];
  const modelHint = invMeta ? ` (${invMeta.models.split(',')[0]} or equiv.)` : "";

  const invSpec = bldgResults && bldgResults.length > 1
    ? `${inverterKw} kW ${inverterKw > 5 ? 'three-phase' : 'single-phase'} (` + bldgResults.map(b => `${b.name}: ${selectInverter(b.capacityKw)}kW`).join(" + ") + ")"
    : (inverterKw > 5.0 ? `${inverterKw} kW, three-phase${modelHint}` : `${inverterKw} kW, single-phase${modelHint}`);
  const invQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Nos.` : "1 No.";

  const rccbRating = acdbBreakerRating <= 16 ? 25 : (acdbBreakerRating <= 32 ? 40 : 63);
  const acdbSpec = bldgResults && bldgResults.length > 1
    ? bldgResults.map(b => {
        const bDeratedAc = Math.round(b.capacityKw * 0.70 * 100) / 100;
        return `${b.name}: ${selectAcdbComponents(bDeratedAc, dist || 20).breakerRating}A MCB`;
      }).join(" + ") + " + Type-II AC SPD"
    : `${acdbBreakerRating}A MCB + ${rccbRating}A RCCB + Type-II AC SPD`;
  const acdbQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Set(s)` : "1 No.";
  const structQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Roof Set(s)` : "1 Set";
  const dcdbQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} No(s).` : "1 No.";
  const numBldgs = bldgResults && bldgResults.length > 1 ? bldgResults.length : 1;

  // Requirement 8: AC cable ALWAYS uses actual user distance
  const userDistM = Math.max(5, parseFloat(dist) || 20);
  const acQtyStr = `${userDistM} m`;
  const acCost = Math.round(userDistM * acRate);

  const dcLenM = Math.max(20, Math.round(cap * 11));
  const dcCost = Math.round(dcLenM * dcRate);

  const invCost = Math.round(inverterKw * invRate);
  const structCost = Math.round(cap * structRate);
  const dcdbCost = Math.round(dcdbBase * numBldgs);
  const acdbCost = Math.round(acdbBase * numBldgs);
  const earthingCost = Math.round(earthingBase);
  const laCost = Math.round(laBase);
  const accCost = Math.round(cap * accRate);
  const instCost = Math.round(cap * instRate);

  let items = [];
  if (EXACT_BOM_REPORTS[roundedCap]) {
    const rows = EXACT_BOM_REPORTS[roundedCap];
    for (let idx = 1; idx <= rows.length; idx++) {
      const [desc, spec, qty, amt] = rows[idx - 1];
      if (idx === 1) {
        items.push({ sl: idx, desc: "Solar PV modules", spec: modSpec, qty: modQty, amt: totalModuleCost });
      } else if (idx === 2) {
        items.push({ sl: idx, desc: "On-grid inverter", spec: invSpec, qty: invQty, amt: invCost });
      } else if (idx === 3) {
        items.push({ sl: idx, desc: desc, spec: spec, qty: structQty, amt: structCost });
      } else if (idx === 4) {
        items.push({ sl: idx, desc: "DC solar cable", spec: spec, qty: `${dcLenM} m`, amt: dcCost });
      } else if (idx === 5) {
        // AC cable: ALWAYS use user dist (Requirement 8)
        items.push({ sl: idx, desc: "AC cable", spec: "4-10 sq.mm copper (Grid Interconnection)", qty: acQtyStr, amt: acCost });
      } else if (idx === 6) {
        items.push({ sl: idx, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost });
      } else if (idx === 7) {
        items.push({ sl: idx, desc: desc, spec: spec, qty: dcdbQty, amt: dcdbCost });
      } else if (idx === 8) {
        items.push({ sl: idx, desc: "ACDB", spec: acdbSpec, qty: acdbQty, amt: acdbCost });
      } else if (idx === 9) {
        items.push({ sl: idx, desc: "Earthing kit", spec: "Earth electrodes & accessories (IS 3043 - 3 Pits)", qty: "3 Nos.", amt: earthingCost });
      } else if (idx === 10) {
        items.push({ sl: idx, desc: "Lightning arrester", spec: spec, qty: "1 No.", amt: laCost });
      } else if (idx === 11) {
        items.push({ sl: idx, desc: "Installation accessories", spec: spec, qty: "1 Lot", amt: accCost });
      } else if (idx === 12) {
        items.push({ sl: idx, desc: "Installation & commissioning", spec: spec, qty: "1 Job", amt: instCost });
      } else {
        items.push({ sl: idx, desc: desc, spec: spec, qty: qty, amt: amt });
      }
    }
  } else {
    items = [
      { sl: 1, desc: "Solar PV modules", spec: modSpec, qty: modQty, amt: totalModuleCost },
      { sl: 2, desc: "On-grid inverter", spec: invSpec, qty: invQty, amt: invCost },
      { sl: 3, desc: "Rooftop mounting structure", spec: "HDGI rooftop structure, module-compatible", qty: structQty, amt: structCost },
      { sl: 4, desc: "DC solar cable", spec: "4-6 sq.mm copper, PV-rated", qty: `${dcLenM} m`, amt: dcCost },
      { sl: 5, desc: "AC cable", spec: "4-10 sq.mm copper (Grid Interconnection)", qty: acQtyStr, amt: acCost },
      { sl: 6, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost },
      { sl: 7, desc: "DCDB", spec: "Isolator + fuse + Type-II DC SPD", qty: dcdbQty, amt: dcdbCost },
      { sl: 8, desc: "ACDB", spec: acdbSpec, qty: acdbQty, amt: acdbCost },
      { sl: 9, desc: "Earthing kit", spec: "Chemical earth electrodes & accessories (IS 3043)", qty: "3 Nos.", amt: earthingCost },
      { sl: 10, desc: "Lightning arrester", spec: "Standard rooftop PV type", qty: "1 No.", amt: laCost },
      { sl: 11, desc: "Installation accessories", spec: "Lugs, ferrules, clamps, conduit, glands, etc.", qty: "1 Lot", amt: accCost },
      { sl: 12, desc: "Installation & commissioning", spec: "Labour, testing and commissioning", qty: "1 Job", amt: instCost },
    ];
  }
  const plantTotal = items.reduce((s, i) => s + i.amt, 0);

  const escom = inverterKw <= 5.0
    ? [
        { sl: 1, name: "Application & Registration Fee", spec: "ESCOM online portal submission", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_application_fee) ? dynamicPricing.escom_application_fee : 500, note: "+ 18% GST" },
        { sl: 2, name: "Processing / Facilitation Fee", spec: "Technical feasibility scrutiny", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_processing_fee) ? dynamicPricing.escom_processing_fee : 1000, note: "Non-refundable" },
        { sl: 3, name: "Power Purchase Agreement (PPA)", spec: "Digital e-Sign on stamp paper", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_stamp_duty) ? dynamicPricing.escom_stamp_duty : 12, note: "Article 20(a)" },
        { sl: 4, name: "Bidirectional Net Meter & CT/PT", spec: "0.2s class LT-DLMS compliant", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_net_meter) ? dynamicPricing.escom_net_meter : 4500, note: "BESCOM empanelled" },
        { sl: 5, name: "Initial Security Deposit (ISD)", spec: "Refundable grid connection security", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_security_deposit) ? dynamicPricing.escom_security_deposit : 3000, note: "BESCOM escrow" }
      ]
    : [
        { sl: 1, name: "Application & Registration Fee", spec: "ESCOM online portal submission", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_application_fee) ? dynamicPricing.escom_application_fee : 1000, note: "+ 18% GST" },
        { sl: 2, name: "Processing / Facilitation Fee", spec: "Technical feasibility scrutiny", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_processing_fee) ? dynamicPricing.escom_processing_fee : 2000, note: "Non-refundable" },
        { sl: 3, name: "Power Purchase Agreement (PPA)", spec: "Digital e-Sign on stamp paper", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_stamp_duty) ? dynamicPricing.escom_stamp_duty : 12, note: "Article 20(a)" },
        { sl: 4, name: "Bidirectional Net Meter & CT/PT", spec: "0.2s class LT-DLMS 3-phase", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_net_meter) ? dynamicPricing.escom_net_meter : 12000, note: "Three-phase meter" },
        { sl: 5, name: "Initial Security Deposit (ISD)", spec: "Refundable grid connection security", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.escom_security_deposit) ? dynamicPricing.escom_security_deposit : 8000, note: "BESCOM escrow" }
      ];

  const escomTotal = escom.reduce((sum, e) => sum + e.amt, 0);
  const totalCapitalOutlay = plantTotal + escomTotal;
  const plantTotalWithEscom = totalCapitalOutlay;
  return { items, plantTotal, escom, escomTotal, totalCapitalOutlay, plantTotalWithEscom };
}'''
        html = html[:idx] + new_bom_impl + html[end:]
        print("  - Successfully replaced generatePlantBom!")
    else:
        print("  - WARNING: Could not find end_marker for generatePlantBom")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Finished {filepath}!")

if __name__ == "__main__":
    patch_file("VoltRoof_Combined.html")
    patch_file("index.html")

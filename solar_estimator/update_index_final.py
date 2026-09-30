import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add SOLAR_PANEL_CATALOG and INVERTER_MASTER_CATALOG and replace INVERTER_RATINGS
old_inv_ratings = """const INVERTER_RATINGS = [
  1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
  11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
];"""

new_catalogs_and_ratings = """// ============================================================
// SOLAR PANEL MASTER CATALOG (From Standard Market Ratings)
// ============================================================
const SOLAR_PANEL_CATALOG = {
  "Mono-PERC (Mono-facial)": {
    name: "Mono-PERC (Mono-facial)",
    desc: "The standard for current residential rooftop systems.",
    ratings: [380, 390, 400, 410, 420, 430, 440, 450, 460, 480, 500, 525, 530, 535, 540, 545, 550, 555, 560, 570, 580],
    defaultWatt: 550
  },
  "N-Type TOPCon": {
    name: "N-Type TOPCon",
    desc: "Premium high-efficiency modules for commercial & industrial use.",
    ratings: [420, 440, 450, 500, 540, 545, 550, 555, 560, 565, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 660, 670, 680, 690, 700],
    defaultWatt: 580
  },
  "Bifacial (Mono / TOPCon)": {
    name: "Bifacial (Mono / TOPCon)",
    desc: "Dual-sided generation. Ratings listed are for the front side.",
    ratings: [440, 500, 530, 540, 545, 550, 560, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 655, 660, 665, 670, 680, 690, 700, 710, 720],
    defaultWatt: 550
  },
  "Polycrystalline": {
    name: "Polycrystalline",
    desc: "Legacy technology, mostly used in small off-grid applications.",
    ratings: [40, 50, 75, 100, 150, 165, 200, 250, 260, 270, 275, 280, 300, 325, 330, 335, 340],
    defaultWatt: 335
  },
  "Ultra-High Power (G12/G12R)": {
    name: "Ultra-High Power (G12/G12R)",
    desc: "Large-format modules for utility-scale solar farms.",
    ratings: [600, 610, 620, 625, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720],
    defaultWatt: 650
  }
};

// ============================================================
// ON-GRID SOLAR INVERTER MASTER CATALOG (1 kW to 20 kW)
// ============================================================
const INVERTER_MASTER_CATALOG = {
  1.0: { rating: 1.0, phase: "Single-Phase", desc: "Standard entry point; ideal for nano 1-room households.", models: "Solis Mini, Havells Envira", hardwareKw: 1.0 },
  2.0: { rating: 2.0, phase: "Single-Phase", desc: "Standard residential tier; powers basic 1-2 BHK loads.", models: "Polycab PSIT, Obetech G", hardwareKw: 2.0 },
  3.0: { rating: 3.0, phase: "Single-Phase", desc: "Highest Volume Domestic Tier; max limit for single-phase PM Surya Ghar subsidy.", models: "Growatt MIC, Luminous NXi 130", hardwareKw: 3.0 },
  4.0: { rating: 4.0, phase: "Single-Phase / Three-Phase", desc: "Transition bracket; widely deployed for 3 BHK properties.", models: "Waaree W3.1/3-PH, Luminous NXi 340", hardwareKw: 4.0 },
  5.0: { rating: 5.0, phase: "Single-Phase / Three-Phase", desc: "Standard boundary rating; most DISCOMs mandate a shift to 3-phase meter beyond this.", models: "Sungrow SG5.0RS, UTL 5.1", hardwareKw: 5.0 },
  6.0: { rating: 6.0, phase: "Single-Phase / Three-Phase", desc: "Commercial-scale entry point; common for large villas.", models: "Solis 1P6K, Growatt MOD 6000", hardwareKw: 6.0 },
  7.0: { rating: 7.0, phase: "Three-Phase", desc: "Fully Standardized Option; engineered specifically to bridge gap between 6kW and 8kW.", models: "Growatt P3, Fimer On-Grid", hardwareKw: 7.0 },
  8.0: { rating: 8.0, phase: "Three-Phase", desc: "Industrial tier; steelwork for independent modern bungalows.", models: "GoodWe GW8K-DT, Polycab PSIT 8K", hardwareKw: 8.0 },
  9.0: { rating: 9.0, phase: "Three-Phase", desc: "Available via turnkey system developers.", models: "Greentech Energy", hardwareKw: 9.0 },
  10.0: { rating: 10.0, phase: "Three-Phase", desc: "Massive Volume Commercial Tier; high demand for commercial shops.", models: "Fronius Symo, Delta M10", hardwareKw: 10.0 },
  11.0: { rating: 11.0, phase: "Three-Phase", desc: "Highly Available; optimal DC oversizing on 10kW sanctioned limits.", models: "Deye 11K-G04, Kstar Solar", hardwareKw: 11.0 },
  12.0: { rating: 12.0, phase: "Three-Phase", desc: "Mid-tier industrial rating; heavily utilized for institutions.", models: "Solis 12KTL, Hitachi Solar", hardwareKw: 12.0 },
  13.0: { rating: 13.0, phase: "Non-Standard (Derated 15kW)", desc: "Physically Unavailable; deploy derated 15kW unit capped to 13kW.", models: "None (Use 15kW configuration)", hardwareKw: 15.0 },
  14.0: { rating: 14.0, phase: "Three-Phase", desc: "Exists primarily in specialized hybrid catalogs.", models: "Deye, Delta Solar", hardwareKw: 14.0 },
  15.0: { rating: 15.0, phase: "Three-Phase", desc: "Core Industrial Tier; widely chosen for schools and institutions.", models: "Sungrow SG15RT, UTL On-Grid", hardwareKw: 15.0 },
  16.0: { rating: 16.0, phase: "Three-Phase", desc: "Commercial and heavy-duty hybrid brackets.", models: "Deye Hybrid 16K", hardwareKw: 16.0 },
  17.0: { rating: 17.0, phase: "Three-Phase", desc: "Highly Available; prominent dedicated hardware step.", models: "UTL 17KW, Solis 3-Phase 17KW, SolarEdge", hardwareKw: 17.0 },
  18.0: { rating: 18.0, phase: "Three-Phase", desc: "Commercially cataloged; frequently derated 20kW inverter for net-metering.", models: "Deye 18K, Growatt 18K", hardwareKw: 18.0 },
  19.0: { rating: 19.0, phase: "Non-Standard (Bypassed to 20kW)", desc: "Physically Bypassed; installers upgrade project directly to 20kW system.", models: "None (Use 20kW configuration)", hardwareKw: 20.0 },
  20.0: { rating: 20.0, phase: "Three-Phase", desc: "Major Industrial Anchor Tier; standard benchmark for decentralized rooftop annexes.", models: "Loom Solar, Eyzer 20, Waaree W3-20K", hardwareKw: 20.0 }
};

const INVERTER_RATINGS = [
  1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
  11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
];"""

assert old_inv_ratings in html, "old_inv_ratings not found"
html = html.replace(old_inv_ratings, new_catalogs_and_ratings, 1)

# 2. Update selectInverter with 70% derating logic
old_select_inv = """function selectInverter(totalPlantCapacityKw) {
  const target = Math.round(totalPlantCapacityKw * 100) / 100;
  for (const r of INVERTER_RATINGS) {
    if (r >= target - 1e-4) return r;
  }
  return INVERTER_RATINGS[INVERTER_RATINGS.length - 1];
}"""

new_select_inv = """function selectInverter(totalPlantDcKw) {
  // Requirement 1: 70% derating factor of total solar panels output power
  // E.g. if solar panel output is 3.5 kW, 3.5 * 0.7 = 2.45 kW -> selects 3.0 kW standard rating
  const deratedKw = Math.round(totalPlantDcKw * 0.70 * 100) / 100;
  if (deratedKw <= 1.0) return 1.0;
  for (const r of INVERTER_RATINGS) {
    if (r >= deratedKw - 1e-4) return r;
  }
  return INVERTER_RATINGS[INVERTER_RATINGS.length - 1];
}"""

assert old_select_inv in html, "old_select_inv not found"
html = html.replace(old_select_inv, new_select_inv, 1)

# 3. Update computeSingleSite
old_css_ac = """  const invKw = selectInverter(evalCapacity);
  const phase3 = invKw > 5.0;
  const invCable = inverterCableAndIsolator(invKw, phase3);
  const acdb = selectAcdbComponents(invKw, dist);
  const bom = generatePlantBom(capacityKw, invKw, panelW, panels, acdb.breakerRating, bldgResults, dist);"""

new_css_ac = """  // Requirement 1: Inverter selected to 70% derating of solar DC output
  const invKw = selectInverter(evalCapacity);
  const phase3 = invKw > 5.0;

  // Requirement 2: AC-side components sized by derated calculated power (evalCapacity * 0.70)
  const deratedAcKw = Math.round(evalCapacity * 0.70 * 100) / 100;
  const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
  const acdb = selectAcdbComponents(deratedAcKw, dist);

  // Requirement 3: Panel technology and standard ratings
  const activeTech = s.tech || (bldgResults[0] && bldgResults[0].panelTech) || "Mono-PERC (Mono-facial)";
  const bom = generatePlantBom(capacityKw, invKw, panelW, panels, acdb.breakerRating, bldgResults, dist, activeTech);"""

assert old_css_ac in html, "old_css_ac not found"
html = html.replace(old_css_ac, new_css_ac, 1)

# In computeSingleSite roof loop: add panelTech to bldgResults
old_bldg_push = """      bldgResults.push({
        name: b.name || `Building ${idx + 1}`,
        grossArea: bGross,
        usableArea: bUtil,
        capacityKw: bCap,
        panels: bPanels,
        panelW: bPanelW,
        parapet: parapet,
        neighbour: b.neighbour || "None"
      });"""

new_bldg_push = """      const bTech = b.tech || b.panelTech || s.tech || "Mono-PERC (Mono-facial)";
      bldgResults.push({
        name: b.name || `Building ${idx + 1}`,
        grossArea: bGross,
        usableArea: bUtil,
        capacityKw: bCap,
        panels: bPanels,
        panelW: bPanelW,
        panelTech: bTech,
        parapet: parapet,
        neighbour: b.neighbour || "None"
      });"""

assert old_bldg_push in html, "old_bldg_push not found"
html = html.replace(old_bldg_push, new_bldg_push, 1)

# In computeSingleSite bill mode: add panelTech to bldgResults
old_bill_push = """    bldgResults.push({
      name: "Building 1",
      grossArea: grossRooftopArea,
      usableArea: utilizedRooftopArea,
      capacityKw: rawCapacityKw,
      panels: panels,
      panelW: panelW,
      parapet: 0,
      neighbour: "None"
    });"""

new_bill_push = """    bldgResults.push({
      name: "Building 1",
      grossArea: grossRooftopArea,
      usableArea: utilizedRooftopArea,
      capacityKw: rawCapacityKw,
      panels: panels,
      panelW: panelW,
      panelTech: s.tech || s.techBill || "Mono-PERC (Mono-facial)",
      parapet: 0,
      neighbour: "None"
    });"""

assert old_bill_push in html, "old_bill_push not found"
html = html.replace(old_bill_push, new_bill_push, 1)

# In computeSingleSite return: add deratedAcKw and panelTech
old_css_ret = """  return {
    name: s.name,
    loc: s.loc,
    email: s.email,
    mode: s.mode,
    panelW,
    dist,
    customTariff,
    grossRooftopArea,
    utilizedRooftopArea,
    rawCapacityKw,
    capacityKw,
    installedDckWp,
    evalCapacity,
    panels,
    strings,
    invKw,
    phase3,
    invCable,
    acdb,
    bom,
    monthly,
    annual,
    series25,
    total25,
    buildings: bldgResults
  };"""

new_css_ret = """  return {
    name: s.name,
    loc: s.loc,
    email: s.email,
    mode: s.mode,
    panelW,
    panelTech: activeTech,
    dist,
    customTariff,
    grossRooftopArea,
    utilizedRooftopArea,
    rawCapacityKw,
    capacityKw,
    deratedAcKw,
    installedDckWp,
    evalCapacity,
    panels,
    strings,
    invKw,
    phase3,
    invCable,
    acdb,
    bom,
    monthly,
    annual,
    series25,
    total25,
    buildings: bldgResults
  };"""

assert old_css_ret in html, "old_css_ret not found"
html = html.replace(old_css_ret, new_css_ret, 1)

# 4. Update generatePlantBom function signature & logic
old_gpb_header = "function generatePlantBom(capacityKw, inverterKw, panelWatt, panelCount, acdbBreakerRating, bldgResults, dist) {"
new_gpb_header = "function generatePlantBom(capacityKw, inverterKw, panelWatt, panelCount, acdbBreakerRating, bldgResults, dist, panelTech) {"
assert old_gpb_header in html, "old_gpb_header not found"
html = html.replace(old_gpb_header, new_gpb_header, 1)

old_gpb_mod = """  let totalModuleCost = 0;
  let mc4Pairs = panelCount;
  let modSpec = `${panelWatt} W mono PERC / TOPCon`;
  let modQty = `${panelCount} Nos.`;

  if (bldgResults && bldgResults.length > 0) {
    totalModuleCost = bldgResults.reduce((sum, b) => sum + (b.panels * Math.round((b.panelW || 550) * (10000.0 / 550.0))), 0);
    mc4Pairs = bldgResults.reduce((sum, b) => sum + b.panels, 0);
    modQty = `${mc4Pairs} Nos.`;
    const distinctWatts = [...new Set(bldgResults.map(b => b.panelW || 550))];
    if (distinctWatts.length === 1) {
      modSpec = `${distinctWatts[0]} W mono PERC / TOPCon`;
    } else {
      modSpec = bldgResults.map(b => `${b.name || 'Building'}: ${b.panelW || 550}W (${b.panels} Nos.)`).join(" + ");
    }
  } else {
    const costPerModule = Math.round(panelWatt * (10000.0 / 550.0));
    totalModuleCost = panelCount * costPerModule;
  }"""

new_gpb_mod = """  let totalModuleCost = 0;
  let mc4Pairs = panelCount;
  const pTech = panelTech || (bldgResults && bldgResults[0]?.panelTech) || "Mono-PERC (Mono-facial)";
  let modSpec = `${panelWatt} W ${pTech}`;
  let modQty = `${panelCount} Nos.`;

  if (bldgResults && bldgResults.length > 0) {
    totalModuleCost = bldgResults.reduce((sum, b) => sum + (b.panels * Math.round((b.panelW || 550) * (10000.0 / 550.0))), 0);
    mc4Pairs = bldgResults.reduce((sum, b) => sum + b.panels, 0);
    modQty = `${mc4Pairs} Nos.`;
    const distinctSpecs = [...new Set(bldgResults.map(b => `${b.panelW || 550}W ${b.panelTech || pTech}`))];
    if (distinctSpecs.length === 1) {
      modSpec = distinctSpecs[0];
    } else {
      modSpec = bldgResults.map(b => `${b.name || 'Building'}: ${b.panelW || 550}W ${b.panelTech || pTech} (${b.panels} Nos.)`).join(" + ");
    }
  } else {
    const costPerModule = Math.round(panelWatt * (10000.0 / 550.0));
    totalModuleCost = panelCount * costPerModule;
  }"""

assert old_gpb_mod in html, "old_gpb_mod not found"
html = html.replace(old_gpb_mod, new_gpb_mod, 1)

old_gpb_inv = """  const mc4Cost = mc4Pairs * 300.0;
  const invSpec = bldgResults && bldgResults.length > 1
    ? `${inverterKw} kW ${inverterKw > 5 ? 'three-phase' : 'single-phase'} (` + bldgResults.map(b => `${b.name}: ${selectInverter(b.capacityKw)}kW`).join(" + ") + ")"
    : (inverterKw > 5.0 ? `${inverterKw} kW, three-phase` : `${inverterKw} kW, single-phase`);
  const invQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Nos.` : "1 No.";

  const rccbRating = acdbBreakerRating <= 16 ? 25 : (acdbBreakerRating <= 32 ? 40 : 63);
  const acdbSpec = bldgResults && bldgResults.length > 1
    ? bldgResults.map(b => `${b.name}: ${selectAcdbComponents(selectInverter(b.capacityKw), dist || 20).breakerRating}A MCB`).join(" + ") + " + Type-II AC SPD"
    : `${acdbBreakerRating}A MCB + ${rccbRating}A RCCB + Type-II AC SPD`;"""

new_gpb_inv = """  const mc4Cost = mc4Pairs * 300.0;
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
    : `${acdbBreakerRating}A MCB + ${rccbRating}A RCCB + Type-II AC SPD`;"""

assert old_gpb_inv in html, "old_gpb_inv not found"
html = html.replace(old_gpb_inv, new_gpb_inv, 1)

# 5. Update HTML UI for Solar Technology & Rating of Solar Panel
old_roof_panel_field = """            <div class="field" style="margin:0"><label>Rating of Solar Panel (Wp) *</label>
              <select id="cfgPanel" onchange="syncPanelFromRoof();saveCurrentFormToActiveSite();liveUpdate()"><option>275</option><option>300</option><option>325</option><option>350</option><option>375</option><option>400</option><option>450</option><option>500</option><option selected>550</option><option>600</option></select>
            </div>"""

new_roof_panel_field = """            <div class="field" style="margin-bottom:10px">
              <label>Solar Technology & Architecture *</label>
              <select id="cfgTech" onchange="onTechChange('roof');saveCurrentFormToActiveSite();liveUpdate()"></select>
            </div>
            <div class="field" style="margin:0">
              <label>Rating of Solar Panel (Wp) *</label>
              <select id="cfgPanel" onchange="syncPanelFromRoof();saveCurrentFormToActiveSite();liveUpdate()"></select>
              <div id="cfgTechInfo" style="font-size:.72rem;color:var(--muted);margin-top:4px"></div>
            </div>"""

assert old_roof_panel_field in html, "old_roof_panel_field not found"
html = html.replace(old_roof_panel_field, new_roof_panel_field, 1)

old_bill_panel_field = """            <div class="field" style="margin:0"><label>Rating of Solar Panel (Wp) *</label>
              <select id="cfgPanelBill" onchange="syncPanelFromBill();saveCurrentFormToActiveSite();liveUpdate()"><option>275</option><option>300</option><option>325</option><option>350</option><option>375</option><option>400</option><option>450</option><option>500</option><option selected>550</option><option>600</option></select>
            </div>"""

new_bill_panel_field = """            <div class="field" style="margin-bottom:10px">
              <label>Solar Technology & Architecture *</label>
              <select id="cfgTechBill" onchange="onTechChange('bill');saveCurrentFormToActiveSite();liveUpdate()"></select>
            </div>
            <div class="field" style="margin:0">
              <label>Rating of Solar Panel (Wp) *</label>
              <select id="cfgPanelBill" onchange="syncPanelFromBill();saveCurrentFormToActiveSite();liveUpdate()"></select>
              <div id="cfgTechBillInfo" style="font-size:.72rem;color:var(--muted);margin-top:4px"></div>
            </div>"""

assert old_bill_panel_field in html, "old_bill_panel_field not found"
html = html.replace(old_bill_panel_field, new_bill_panel_field, 1)

# Update caption
old_caption = """<p style="font-size:.74rem;color:var(--dim);margin-bottom:14px">* Fields marked with * are mandatory | Inverter is auto stepped-up so Inverter &ge; Plant Capacity</p>"""
new_caption = """<p style="font-size:.74rem;color:var(--dim);margin-bottom:14px">* Fields marked with * are mandatory | Inverter selected to 70% derated solar capacity (Inverter &ge; P<sub>DC</sub> &times; 0.70) | AC components sized via calculated derated power</p>"""
assert old_caption in html, "old_caption not found"
html = html.replace(old_caption, new_caption, 1)

# 6. JavaScript helper functions
helpers_js = """
// ============================================================
// TECHNOLOGY & PANEL CATALOG UI LOGIC
// ============================================================
function initTechAndPanelDropdowns() {
  const techKeys = Object.keys(SOLAR_PANEL_CATALOG);
  const techSelects = [document.getElementById("cfgTech"), document.getElementById("cfgTechBill")];
  
  techSelects.forEach(sel => {
    if (!sel) return;
    sel.innerHTML = techKeys.map(k => {
      const cat = SOLAR_PANEL_CATALOG[k];
      return `<option value="${k}" ${k.startsWith("Mono-PERC") ? "selected" : ""}>${k}</option>`;
    }).join("");
  });
  
  populatePanelDropdown("cfgPanel", "Mono-PERC (Mono-facial)", 550);
  populatePanelDropdown("cfgPanelBill", "Mono-PERC (Mono-facial)", 550);
  updateTechInfo("roof", "Mono-PERC (Mono-facial)");
  updateTechInfo("bill", "Mono-PERC (Mono-facial)");
}

function populatePanelDropdown(selectId, techName, selectedWatt = null) {
  const sel = document.getElementById(selectId);
  if (!sel) return;
  const cat = SOLAR_PANEL_CATALOG[techName] || SOLAR_PANEL_CATALOG["Mono-PERC (Mono-facial)"];
  const ratings = cat.ratings;
  const defWatt = selectedWatt || cat.defaultWatt;

  sel.innerHTML = `
    <optgroup label="${techName} (${ratings.length} Ratings)">
      ${ratings.map(w => `<option value="${w}" ${w === Number(defWatt) ? "selected" : ""}>${w} Wp</option>`).join("")}
    </optgroup>
    <optgroup label="Other Standard Technologies">
      ${Object.keys(SOLAR_PANEL_CATALOG).filter(k => k !== techName).map(k => {
        return SOLAR_PANEL_CATALOG[k].ratings.slice(0, 3).map(w => `<option value="${w}" data-tech="${k}">${w} Wp (${k.split(' ')[0]})</option>`).join("");
      }).join("")}
    </optgroup>
  `;
}

function updateTechInfo(mode, techName) {
  const cat = SOLAR_PANEL_CATALOG[techName];
  if (!cat) return;
  const infoEl = document.getElementById(mode === "roof" ? "cfgTechInfo" : "cfgTechBillInfo");
  if (infoEl) {
    infoEl.textContent = `ℹ️ ${cat.desc} Available: ${cat.ratings[0]}W to ${cat.ratings[cat.ratings.length - 1]}W (${cat.ratings.length} steps).`;
  }
}

function onTechChange(viewMode) {
  const isRoof = viewMode === "roof";
  const techSel = document.getElementById(isRoof ? "cfgTech" : "cfgTechBill");
  const panelSel = document.getElementById(isRoof ? "cfgPanel" : "cfgPanelBill");
  if (!techSel || !panelSel) return;
  const techName = techSel.value;
  populatePanelDropdown(isRoof ? "cfgPanel" : "cfgPanelBill", techName);
  updateTechInfo(viewMode, techName);

  // Sync to other mode
  const otherTechSel = document.getElementById(isRoof ? "cfgTechBill" : "cfgTech");
  if (otherTechSel) otherTechSel.value = techName;
  populatePanelDropdown(isRoof ? "cfgPanelBill" : "cfgPanel", techName);
  updateTechInfo(isRoof ? "bill" : "roof", techName);
}

function syncPanelFromBill() {
  const techBill = document.getElementById("cfgTechBill")?.value;
  const val = document.getElementById("cfgPanelBill")?.value;
  const techRoof = document.getElementById("cfgTech");
  if (techRoof && techBill) techRoof.value = techBill;
  populatePanelDropdown("cfgPanel", techBill, val);
  const panRoof = document.getElementById("cfgPanel");
  if (panRoof && val) panRoof.value = val;
  updateTechInfo("roof", techBill);
}

function syncPanelFromRoof() {
  const techRoof = document.getElementById("cfgTech")?.value;
  const val = document.getElementById("cfgPanel")?.value;
  const techBill = document.getElementById("cfgTechBill");
  if (techBill && techRoof) techBill.value = techRoof;
  populatePanelDropdown("cfgPanelBill", techRoof, val);
  const panBill = document.getElementById("cfgPanelBill");
  if (panBill && val) panBill.value = val;
  updateTechInfo("bill", techRoof);
}
"""

old_sync_funcs = """function syncDistFromBill() {
  document.getElementById("cfgDist").value = document.getElementById("cfgDistBill").value;
}
function syncPanelFromBill() {
  document.getElementById("cfgPanel").value = document.getElementById("cfgPanelBill").value;
}
function syncPanelFromRoof() {
  document.getElementById("cfgPanelBill").value = document.getElementById("cfgPanel").value;
}"""

assert old_sync_funcs in html, "old_sync_funcs not found"
html = html.replace(old_sync_funcs, helpers_js + "\nfunction syncDistFromBill() {\n  document.getElementById('cfgDist').value = document.getElementById('cfgDistBill').value;\n}", 1)

# 7. Update saveCurrentFormToActiveSite to save tech
old_scf = """  const b = s.buildings[s.activeBuildingIndex];
  if (b) {
    b.L = document.getElementById("cfgL")?.value || "";
    b.B = document.getElementById("cfgB")?.value || "";
    b.parapet = document.getElementById("cfgParapet")?.value || "";
    b.neighbour = document.getElementById("cfgNeighbour")?.value || "None";
    b.panel = document.getElementById("cfgPanel")?.value || "550";
  }

  s.units = document.getElementById("cfgUnits")?.value || "";
  s.distBill = document.getElementById("cfgDistBill")?.value || "";
  s.panelBill = document.getElementById("cfgPanelBill")?.value || "550";"""

new_scf = """  const b = s.buildings[s.activeBuildingIndex];
  if (b) {
    b.L = document.getElementById("cfgL")?.value || "";
    b.B = document.getElementById("cfgB")?.value || "";
    b.parapet = document.getElementById("cfgParapet")?.value || "";
    b.neighbour = document.getElementById("cfgNeighbour")?.value || "None";
    b.panel = document.getElementById("cfgPanel")?.value || "550";
    b.tech = document.getElementById("cfgTech")?.value || "Mono-PERC (Mono-facial)";
  }

  s.units = document.getElementById("cfgUnits")?.value || "";
  s.distBill = document.getElementById("cfgDistBill")?.value || "";
  s.panelBill = document.getElementById("cfgPanelBill")?.value || "550";
  s.techBill = document.getElementById("cfgTechBill")?.value || "Mono-PERC (Mono-facial)";
  s.tech = document.getElementById("cfgTech")?.value || "Mono-PERC (Mono-facial)";"""

assert old_scf in html, "old_scf not found"
html = html.replace(old_scf, new_scf, 1)

# 8. Update loadBuildingToForm to load tech
old_lbf = """  const lEl = document.getElementById("cfgL");
  const bEl = document.getElementById("cfgB");
  const pEl = document.getElementById("cfgParapet");
  const nEl = document.getElementById("cfgNeighbour");
  const panEl = document.getElementById("cfgPanel");

  if (lEl) lEl.value = b.L ?? "";
  if (bEl) bEl.value = b.B ?? "";
  if (pEl) pEl.value = b.parapet ?? "";
  if (nEl) nEl.value = b.neighbour || "None";
  if (panEl) panEl.value = b.panel || "550";"""

new_lbf = """  const lEl = document.getElementById("cfgL");
  const bEl = document.getElementById("cfgB");
  const pEl = document.getElementById("cfgParapet");
  const nEl = document.getElementById("cfgNeighbour");
  const techEl = document.getElementById("cfgTech");
  const panEl = document.getElementById("cfgPanel");

  if (lEl) lEl.value = b.L ?? "";
  if (bEl) bEl.value = b.B ?? "";
  if (pEl) pEl.value = b.parapet ?? "";
  if (nEl) nEl.value = b.neighbour ?? "None";
  const bTech = b.tech || "Mono-PERC (Mono-facial)";
  if (techEl) {
    techEl.value = bTech;
    updateTechInfo("roof", bTech);
  }
  populatePanelDropdown("cfgPanel", bTech, b.panel || 550);
  if (panEl && b.panel) panEl.value = b.panel;"""

assert old_lbf in html, "old_lbf not found"
html = html.replace(old_lbf, new_lbf, 1)

# 9. Update downloadPdf payload with panel_tech
old_dl_bldg = """        buildings: bldgs.map((b, bIdx) => ({
          name: b.name || `Building ${bIdx + 1}`,
          length_ft: parseFloat(b.L) || 40.0,
          breadth_ft: parseFloat(b.B) || 30.0,
          parapet_ft: parseFloat(b.parapet) || 1.5,
          neighbour: b.neighbour || "None",
          panel_watt: parseInt(b.panel) || 550
        }))"""

new_dl_bldg = """        buildings: bldgs.map((b, bIdx) => ({
          name: b.name || `Building ${bIdx + 1}`,
          length_ft: parseFloat(b.L) || 40.0,
          breadth_ft: parseFloat(b.B) || 30.0,
          parapet_ft: parseFloat(b.parapet) || 1.5,
          neighbour: b.neighbour || "None",
          panel_watt: parseInt(b.panel) || 550,
          panel_tech: b.tech || s.tech || "Mono-PERC (Mono-facial)"
        }))"""

assert old_dl_bldg in html, "old_dl_bldg not found"
html = html.replace(old_dl_bldg, new_dl_bldg, 1)

old_dl_tail = """    distance_m: current.dist,
    panel_watt: current.panelW
  };"""

new_dl_tail = """    distance_m: current.dist,
    panel_watt: current.panelW,
    panel_tech: current.panelTech || "Mono-PERC (Mono-facial)"
  };"""

assert old_dl_tail in html, "old_dl_tail not found"
html = html.replace(old_dl_tail, new_dl_tail, 1)

# 10. Call initTechAndPanelDropdowns on page startup
old_dom_loaded = 'window.addEventListener("DOMContentLoaded", () => {'
new_dom_loaded = 'window.addEventListener("DOMContentLoaded", () => {\n  initTechAndPanelDropdowns();'
assert old_dom_loaded in html, "old_dom_loaded not found"
html = html.replace(old_dom_loaded, new_dom_loaded, 1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html fully updated and verified!")

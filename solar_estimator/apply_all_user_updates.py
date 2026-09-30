import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Read user_uploaded_latest.html as the exact base
with open('user_uploaded_latest.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read extracted_modal_admin.html and extracted_modal_20kw.html
with open('extracted_modal_admin.html', 'r', encoding='utf-8') as f:
    modal_admin_html = f.read()

with open('extracted_modal_20kw.html', 'r', encoding='utf-8') as f:
    modal_20kw_html = f.read()

# Make sure modals have class shortcuts-modal and NOT name-gate, with display:none !important
modal_admin_fixed = modal_admin_html.replace(
    'class="name-gate" id="modalAdminManual"',
    'class="shortcuts-modal" id="modalAdminManual" style="display:none !important"'
)
# If it had style="display:none;z-index:99999", ensure style="display:none !important;z-index:99999"
modal_admin_fixed = re.sub(r'id="modalAdminManual"\s+style="[^"]*"', 'id="modalAdminManual" style="display:none !important;z-index:99999"', modal_admin_fixed)

modal_20kw_fixed = modal_20kw_html.replace(
    'class="name-gate" id="modalStatutory20kW"',
    'class="shortcuts-modal" id="modalStatutory20kW" style="display:none !important"'
)
modal_20kw_fixed = re.sub(r'id="modalStatutory20kW"\s+style="[^"]*"', 'id="modalStatutory20kW" style="display:none !important;z-index:99999"', modal_20kw_fixed)

print("Modals prepared without name-gate class.")

# -------------------------------------------------------------
# 1. Update Logo (Requirement 2)
# -------------------------------------------------------------
# Favicon
html = re.sub(r'<link\s+rel="icon"[^>]*>', '<link rel="icon" href="logo.png">', html)

# Login gate logo
old_login_logo = '''<div class="vr-logo-mark" id="loginLogoMark" style="width:72px;height:72px;margin:0 auto"><svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M8 34 L24 12 L40 34" stroke="#10b981" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 34 H34" stroke="#10b981" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/><circle cx="24" cy="22" r="5.5" fill="#f59e0b" opacity="0.95"/><path d="M24 14v-2.5M24 32.5V30M16.5 22H14M34 22h-2.5M18.2 16.2l-1.8-1.8M31.6 29.6l-1.8-1.8M31.6 16.2l1.8-1.8M18.2 29.6l-1.8 1.8" stroke="#f59e0b" stroke-width="1.6" stroke-linecap="round"/></svg></div>'''
new_login_logo = '''<div class="vr-logo-mark" id="loginLogoMark" style="max-width:180px;height:auto;margin:0 auto 4px">
          <img src="logo.png" alt="VoltRoof" style="max-height:64px;max-width:100%;object-fit:contain;display:block;margin:0 auto">
        </div>'''
if old_login_logo in html:
    html = html.replace(old_login_logo, new_login_logo)
    print("Replaced login gate logo.")
else:
    print("Warning: old_login_logo not found directly, checking regex")
    html = re.sub(r'<div class="vr-logo-mark" id="loginLogoMark"[^>]*>.*?</div>', new_login_logo, html, flags=re.DOTALL)

# Mobile bar logo
old_mob_logo = '''<div class="vr-logo sm"><div class="vr-logo-mark"><svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M8 34 L24 12 L40 34" stroke="#10b981" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 34 H34" stroke="#10b981" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/><circle cx="24" cy="22" r="5.5" fill="#f59e0b" opacity="0.95"/><path d="M24 14v-2.5M24 32.5V30M16.5 22H14M34 22h-2.5M18.2 16.2l-1.8-1.8M31.6 29.6l-1.8-1.8M31.6 16.2l1.8-1.8M18.2 29.6l-1.8 1.8" stroke="#f59e0b" stroke-width="1.6" stroke-linecap="round"/></svg></div>'''
new_mob_logo = '''<div class="vr-logo sm"><div class="vr-logo-mark"><img src="logo.png" alt="VoltRoof" style="max-height:28px;max-width:70px;object-fit:contain;display:block"></div>'''
if old_mob_logo in html:
    html = html.replace(old_mob_logo, new_mob_logo)
    print("Replaced mobile bar logo.")

# Sidebar logo
old_side_logo = '''<div class="vr-logo-mark" id="navLogoMark"><svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M8 34 L24 12 L40 34" stroke="#10b981" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 34 H34" stroke="#10b981" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/><circle cx="24" cy="22" r="5.5" fill="#f59e0b" opacity="0.95"/><path d="M24 14v-2.5M24 32.5V30M16.5 22H14M34 22h-2.5M18.2 16.2l-1.8-1.8M31.6 29.6l-1.8-1.8M31.6 16.2l1.8-1.8M18.2 29.6l-1.8 1.8" stroke="#f59e0b" stroke-width="1.6" stroke-linecap="round"/></svg></div>'''
new_side_logo = '''<div class="vr-logo-mark" id="navLogoMark"><img src="logo.png" alt="VoltRoof Logo" class="brand-logo-img" style="max-height:42px;max-width:100%;object-fit:contain;display:block"></div>'''
if old_side_logo in html:
    html = html.replace(old_side_logo, new_side_logo)
    print("Replaced sidebar logo.")

# Print header logo
old_print_logo = '''<div class="vr-logo sm" style="margin-bottom:8px">\n          <div class="vr-logo-mark"><svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M8 34 L24 12 L40 34" stroke="#10b981" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 34 H34" stroke="#10b981" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/><circle cx="24" cy="22" r="5.5" fill="#f59e0b" opacity="0.95"/><path d="M24 14v-2.5M24 32.5V30M16.5 22H14M34 22h-2.5M18.2 16.2l-1.8-1.8M31.6 29.6l-1.8-1.8M31.6 16.2l1.8-1.8M18.2 29.6l-1.8 1.8" stroke="#f59e0b" stroke-width="1.6" stroke-linecap="round"/></svg></div>'''
new_print_logo = '''<div class="vr-logo sm" style="margin-bottom:8px">\n          <div class="vr-logo-mark"><img src="logo.png" alt="VoltRoof" style="max-height:44px;object-fit:contain;display:block"></div>'''
if old_print_logo in html:
    html = html.replace(old_print_logo, new_print_logo)
    print("Replaced print header logo.")
else:
    html = re.sub(r'<div class="print-header">.*?<div class="vr-logo-mark"><svg viewBox="0 0 48 48".*?</svg></div>', 
                  '<div class="print-header">\n        <div class="vr-logo sm" style="margin-bottom:8px">\n          <div class="vr-logo-mark"><img src="logo.png" alt="VoltRoof" style="max-height:44px;object-fit:contain;display:block"></div>', 
                  html, flags=re.DOTALL)

# -------------------------------------------------------------
# 2. Remove solar production metric from header (Requirement 3)
# -------------------------------------------------------------
old_header_strip = '''        <div class="system-status-chip" id="topKwp"><div class="dot"></div> All good</div>
        <div class="chip" id="topIrr" title="Specific yield used for this site">☀️ <span id="topIrrVal">4.50</span> kWh/kW/day</div>'''
new_header_strip = '''        <div class="system-status-chip" id="topKwp"><div class="dot"></div> All good</div>'''
if old_header_strip in html:
    html = html.replace(old_header_strip, new_header_strip)
    print("Removed solar production metric chip from header.")
else:
    # Try regex removal
    html = re.sub(r'<div class="chip" id="topIrr"[^>]*>.*?</div>', '', html)
    print("Removed topIrr via regex.")

# In JS: do not overwrite topKwp with kWp, remove topIrrVal
html = html.replace('document.getElementById("topKwp").textContent = `${r.installedDckWp.toFixed(2)} kWp`;', '// topKwp preserved as system status chip')
html = re.sub(r'const topIrrVal = document\.getElementById\("topIrrVal"\);.*?topIrrVal\.textContent =.*?;', '', html)

# -------------------------------------------------------------
# 3. Time & Greetings (Requirement 4)
# AM (until 11:59): "Good morning, Good day, Have a good day (+ calm variants)"
# PM (12:00 onward): Only time-based: Good afternoon -> Good evening -> Good night (no "Good day")
# -------------------------------------------------------------
old_greet_block = '''<div class="ribbon-greet">Good day, <span id="greetName">Engineer</span>'''
new_greet_block = '''<div class="ribbon-greet"><span id="greetPrefix">Good morning</span>, <span id="greetName">Engineer</span>'''
if old_greet_block in html:
    html = html.replace(old_greet_block, new_greet_block)

# Replace timeGreetingWord and pickGreeting functions
greetings_js = '''
function getTimeBucket(h) {
  if (h < 12) return "morning";
  if (h < 17) return "afternoon";
  if (h < 21) return "evening";
  return "night";
}

function timeGreetingWord(h) {
  h = typeof h === "number" ? h : new Date().getHours();
  if (h < 12) return (h % 2 === 0 ? "Good morning" : "Good day");
  if (h < 17) return "Good afternoon";
  if (h < 21) return "Good evening";
  return "Good night";
}

function updateRibbonGreeting(name) {
  const h = new Date().getHours();
  const isAM = h < 12;
  let word = "Good morning";
  if (!isAM) {
    if (h < 17) word = "Good afternoon";
    else if (h < 21) word = "Good evening";
    else word = "Good night";
  } else {
    word = (h % 2 === 0) ? "Good morning" : "Good day";
  }
  const greetEl = document.querySelector(".ribbon-greet");
  const nameEl = document.getElementById("greetName");
  const prefixEl = document.getElementById("greetPrefix");
  if (prefixEl) {
    prefixEl.textContent = word;
  } else if (greetEl) {
    const curName = name || (nameEl ? nameEl.textContent : "Engineer");
    greetEl.innerHTML = `<span id="greetPrefix">${word}</span>, <span id="greetName">${curName}</span> <button type="button" onclick="openNameGate()" class="btn" style="padding:2px 8px;font-size:.66rem;margin-left:6px;border-radius:6px" title="Change name">✏</button>`;
  }
}

function pickGreeting(name) {
  const h = new Date().getHours();
  const bucket = getTimeBucket(h);
  const day = Math.floor(Date.now() / 86400000);
  const isAM = h < 12;
  const extras = isAM ? CALM_EXTRA_AM : CALM_EXTRA_PM;
  let pool = (DEFAULT_GREETINGS[bucket] || DEFAULT_GREETINGS.afternoon).concat(extras);

  loadCustomGreetings().forEach(g => {
    if (!isAM && /good\\s*day/i.test(g)) return; // Strictly exclude "good day" in PM
    pool.push(g);
  });

  if (!isAM) {
    // Strictly filter out any "good day" in PM (12:00 onward)
    pool = pool.filter(g => !/good\\s*day/i.test(g));
  }

  const idx = (day + h) % Math.max(pool.length, 1);
  const raw = pool[idx] || (isAM ? "Good morning, {name}." : (h < 17 ? "Good afternoon, {name}." : (h < 21 ? "Good evening, {name}." : "Good night, {name}.")));
  return raw.replace(/\\{name\\}/gi, name || "Engineer");
}
'''

# Replace getTimeBucket and pickGreeting in html
html = re.sub(r'function getTimeBucket\(h\)\s*\{.*?function pickGreeting\(name\)\s*\{.*?\n\}', lambda m: greetings_js.strip(), html, flags=re.DOTALL)
print("Updated greetings logic for AM/PM requirements.")

# -------------------------------------------------------------
# 4. Derated Factor 70% ONLY for Path 1 (Requirement 6)
# -------------------------------------------------------------
old_select_inv = '''function selectInverter(totalPlantDcKw) {
  // Requirement 1: 70% derating factor of total solar panels output power
  // E.g. if solar panel output is 3.5 kW, 3.5 * 0.7 = 2.45 kW -> selects 3.0 kW standard rating
  const deratedKw = Math.round(totalPlantDcKw * 0.70 * 100) / 100;
  if (deratedKw <= 1.0) return 1.0;
  for (const r of INVERTER_RATINGS) {
    if (r >= deratedKw - 1e-4) return r;
  }
  return INVERTER_RATINGS[INVERTER_RATINGS.length - 1];
}'''

new_select_inv = '''function selectInverter(totalPlantDcKw, isPath1 = true) {
  // Requirement 6: Derated factor 70% ONLY for Path 1 (rooftop area method)
  // For Path 2 (electricity bill method), size directly without 70% derating
  const deratedKw = isPath1 ? Math.round(totalPlantDcKw * 0.70 * 100) / 100 : Math.round(totalPlantDcKw * 100) / 100;
  if (deratedKw <= 1.0) return 1.0;
  for (const r of INVERTER_RATINGS) {
    if (r >= deratedKw - 1e-4) return r;
  }
  return INVERTER_RATINGS[INVERTER_RATINGS.length - 1];
}'''

if old_select_inv in html:
    html = html.replace(old_select_inv, new_select_inv)
    print("Updated selectInverter with isPath1 parameter.")
else:
    html = re.sub(r'function selectInverter\(totalPlantDcKw\)\s*\{.*?return INVERTER_RATINGS\[INVERTER_RATINGS\.length - 1\];\s*\}', lambda m: new_select_inv, html, flags=re.DOTALL)

# Update computeSingleSite with isPath1
old_compute_derating = '''  // Requirement 1: Inverter selected to 70% derating of solar DC output
  const invKw = selectInverter(evalCapacity);
  const phase3 = invKw > 5.0;

  // Requirement 2: AC-side components sized by derated calculated power (evalCapacity * 0.70)
  const deratedAcKw = Math.round(evalCapacity * 0.70 * 100) / 100;
  const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
  const acdb = selectAcdbComponents(deratedAcKw, dist);'''

new_compute_derating = '''  const isPath1 = s.mode === "roof";
  // Requirement 6: Use derated factor 70% ONLY for path 1 calculation
  const invKw = selectInverter(evalCapacity, isPath1);
  const phase3 = invKw > 5.0;

  // AC-side components sized by derated calculated power (evalCapacity * 0.70) ONLY for path 1
  const deratedAcKw = isPath1 ? Math.round(evalCapacity * 0.70 * 100) / 100 : evalCapacity;
  const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
  const acdb = selectAcdbComponents(deratedAcKw, dist);'''

if old_compute_derating in html:
    html = html.replace(old_compute_derating, new_compute_derating)
    print("Updated computeSingleSite with Path 1 only derating.")

# -------------------------------------------------------------
# 5. Pure Calculation Engine Function (Contract N: schemaVersion 1)
# -------------------------------------------------------------
calc_engine_js = '''
// ============================================================
// PURE CALCULATION ENGINE (Contract N: schemaVersion 1)
// Pure function: calculate(projectDto) -> resultDto
// Does NOT depend on the DOM. Runs in browser or node/backend.
// ============================================================
function calculate(projectDto) {
  if (!projectDto) return null;
  const schemaVersion = 1;
  const pricing = projectDto.pricing || (typeof dynamicPricing !== "undefined" ? dynamicPricing : {});

  const customTariff = parseFloat(projectDto.custom_tariff ?? projectDto.customTariff ?? projectDto.tariff) || 8.05;
  const projectMode = projectDto.mode || "roof";
  const globalSanctioned = parseFloat(projectDto.sanctioned_load_kw ?? projectDto.sanctionedLoadKw ?? projectDto.sanctioned_load ?? projectDto.sanctionedLoad) || 0;

  const rawSites = Array.isArray(projectDto.sites) && projectDto.sites.length > 0 
    ? projectDto.sites.slice(0, 2) // Cap at <= 2 sites (Contract D)
    : [{
        id: "site-1",
        name: projectDto.customer_name ?? projectDto.customerName ?? "Site 1",
        mode: projectMode,
        sanctioned_load_kw: globalSanctioned,
        distance_m: projectDto.distance_m ?? projectDto.distanceM ?? 20,
        monthly_units: projectDto.monthly_units ?? projectDto.monthlyUnits ?? (projectDto.monthlyBill ? projectDto.monthlyBill / customTariff : 0),
        tariff: customTariff,
        buildings: projectDto.buildings || []
      }];

  const siteResults = [];

  rawSites.forEach((s, sIdx) => {
    const sName = s.name || `Site Name-${sIdx + 1}`;
    const sLoc = s.location || projectDto.location || "Karnataka";
    const sSanctioned = parseFloat(s.sanctioned_load_kw ?? s.sanctionedLoadKw ?? s.sanctioned_load ?? s.sanctionedLoad ?? globalSanctioned) || 0;

    // Contract D: If sanctioned load filled -> force Path 1 (roof)
    let sMode = s.mode || projectMode;
    if (sSanctioned > 0) {
      sMode = "roof";
    }
    const isPath1 = sMode === "roof";

    const sDist = parseFloat(s.distance_m ?? s.distanceM) || 20;
    const sTariff = parseFloat(s.tariff ?? s.customTariff) || customTariff;
    const bldgs = Array.isArray(s.buildings) && s.buildings.length > 0
      ? s.buildings.slice(0, 10) // Cap at <= 10 buildings (Contract D)
      : [{
          name: "Building 1",
          length_ft: s.length_ft ?? s.lengthFt ?? (s.lengthM ? s.lengthM * 3.28084 : (s.L || 0)),
          breadth_ft: s.breadth_ft ?? s.breadthFt ?? (s.widthM ? s.widthM * 3.28084 : (s.B || 0)),
          parapet_ft: s.parapet_ft ?? s.parapetFt ?? (s.parapetM ? s.parapetM * 3.28084 : (s.parapet || 0)),
          neighbour: s.neighbour || "None",
          panel_watt: s.panel_watt ?? s.panelWatt ?? 550,
          panel_tech: s.panel_tech ?? s.panelTech ?? "Mono-PERC (Mono-facial)"
        }];

    let grossRooftopArea = 0;
    let utilizedRooftopArea = 0;
    let rawCapacityKw = 0;
    let totalPanels = 0;
    const bldgResults = [];

    const defaultPanelW = parseInt(s.panel_watt ?? s.panelWatt) || 550;
    const defaultTech = s.panel_tech ?? s.panelTech ?? "Mono-PERC (Mono-facial)";

    if (isPath1) {
      bldgs.forEach((b, bIdx) => {
        let L = parseFloat(b.length_ft ?? b.lengthFt ?? b.L) || 0;
        let B = parseFloat(b.breadth_ft ?? b.breadthFt ?? b.B) || 0;
        let parapet = Math.max(0, parseFloat(b.parapet_ft ?? b.parapetFt ?? b.parapet) || 0);
        if (!L && b.lengthM) L = b.lengthM * 3.28084;
        if (!B && b.widthM) B = b.widthM * 3.28084;
        if (!parapet && b.parapetM) parapet = b.parapetM * 3.28084;
        const bPanelW = parseInt(b.panel_watt ?? b.panelWatt ?? b.panel) || defaultPanelW;
        const bTech = b.panel_tech ?? b.panelTech ?? b.tech ?? defaultTech;
        const bNeighbour = b.neighbour || "None";

        const bGross = Math.round(L * B * 100) / 100;
        const effL = Math.max(0, L - 2 * parapet);
        const effB = Math.max(0, B - 2 * parapet);
        const bUtil = Math.round(effL * effB * 100) / 100;
        const bCap = Math.round((bUtil / 100.0) * 100) / 100;
        const bPanels = bPanelW > 0 ? Math.ceil((bCap * 1000.0) / bPanelW) : 0;

        grossRooftopArea += bGross;
        utilizedRooftopArea += bUtil;
        rawCapacityKw += bCap;
        totalPanels += bPanels;

        bldgResults.push({
          name: b.name || `Building ${bIdx + 1}`,
          grossArea: bGross,
          usableArea: bUtil,
          capacityKw: bCap,
          panels: bPanels,
          panelW: bPanelW,
          panelTech: bTech,
          parapet: parapet,
          neighbour: bNeighbour
        });
      });
    } else {
      // Path 2: Bill Method
      const units = parseFloat(s.monthly_units ?? s.units) || 0;
      if (units > 0) {
        rawCapacityKw = Math.round((units / 120.0) * 100) / 100;
      } else {
        rawCapacityKw = 0;
      }
      utilizedRooftopArea = Math.round(rawCapacityKw * 100.0 * 100) / 100;
      grossRooftopArea = utilizedRooftopArea;
      totalPanels = defaultPanelW > 0 ? Math.ceil((rawCapacityKw * 1000.0) / defaultPanelW) : 0;
      bldgResults.push({
        name: "Building 1",
        grossArea: grossRooftopArea,
        usableArea: utilizedRooftopArea,
        capacityKw: rawCapacityKw,
        panels: totalPanels,
        panelW: defaultPanelW,
        panelTech: defaultTech,
        parapet: 0,
        neighbour: "None"
      });
    }

    // Sanctioned Load / Contract Demand logic (Site-Level, Contract D)
    let roofAreaStatus = "";
    let kercNotice = "";
    let capacityKw = 0;
    let isCapped20kW = false;

    if (sSanctioned > 0) {
      const effectiveCd = Math.min(20.0, sSanctioned);
      capacityKw = effectiveCd;
      rawCapacityKw = effectiveCd;
      totalPanels = defaultPanelW > 0 ? Math.ceil((capacityKw * 1000.0) / defaultPanelW) : 0;

      const reqAreaSqft = Math.round(effectiveCd * 80.0 * 10) / 10;
      if (utilizedRooftopArea > 0 && utilizedRooftopArea < reqAreaSqft) {
        roofAreaStatus = `Sanctioned ${effectiveCd} kW set · Rooftop may be tight (−${Math.round(reqAreaSqft - utilizedRooftopArea)} sq.ft vs ~80 sq.ft/kW guide)`;
      } else if (utilizedRooftopArea > 0) {
        roofAreaStatus = `Sanctioned Load ${effectiveCd} kW · Rooftop OK (+${Math.round(utilizedRooftopArea - reqAreaSqft)} sq.ft vs guide)`;
      } else {
        roofAreaStatus = `Sized to Sanctioned Load / Contract Demand: ${effectiveCd} kW (enter L×B for layout check)`;
      }

      if (sSanctioned >= 20.0 || rawCapacityKw >= 20.0) {
        isCapped20kW = true;
        kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
      }

      if (bldgResults.length) {
        bldgResults.forEach(br => {
          br.capacityKw = effectiveCd;
          br.panels = totalPanels;
        });
      }
    } else {
      capacityKw = Math.min(rawCapacityKw, 20.0);
      if (rawCapacityKw >= 20.0) {
        isCapped20kW = true;
        kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
      }
      roofAreaStatus = isPath1 ? "Direct Physical Rooftop Sizing" : "Direct Electricity Bill Sizing";
    }

    if (capacityKw <= 0 || totalPanels <= 0) return;

    const installedDckWp = Math.round((totalPanels * defaultPanelW / 1000.0) * 100) / 100;
    const evalCapacity = Math.max(capacityKw, installedDckWp);
    const strings = Math.max(1, Math.ceil(totalPanels / 20.0));

    // REQUIREMENT 6: Use derated factor 70% ONLY for path 1 calculation
    const invKw = selectInverter(evalCapacity, isPath1);
    const phase3 = invKw > 5.0;

    // AC-side components sized by derated calculated power (evalCapacity * 0.70) ONLY for path 1
    const deratedAcKw = isPath1 ? Math.round(evalCapacity * 0.70 * 100) / 100 : evalCapacity;
    const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
    const acdb = selectAcdbComponents(deratedAcKw, sDist);
    const bom = generatePlantBom(capacityKw, invKw, defaultPanelW, totalPanels, acdb.breakerRating, bldgResults, sDist, defaultTech);

    const monthly = {};
    let annual = 0;
    MONTHS.forEach((m, i) => {
      const val = Math.round(evalCapacity * MONTHLY_YIELD[m] * DAYS_IN_MONTH[i] * 100) / 100;
      monthly[m] = val;
      annual += val;
    });
    annual = Math.round(annual * 100) / 100;

    const series25 = [];
    let curG = annual;
    let total25 = 0;
    for (let y = 0; y < 25; y++) {
      series25.push(Math.round(curG * 100) / 100);
      total25 += curG;
      curG *= 0.99;
    }
    total25 = Math.round(total25 * 100) / 100;

    siteResults.push({
      siteIndex: sIdx,
      name: sName,
      location: sLoc,
      mode: sMode,
      sanctionedLoadKw: sSanctioned,
      capacityKw,
      installedDckWp,
      rawCapacityKw,
      isCapped20kW,
      kercNotice,
      roofAreaStatus,
      grossRooftopArea,
      utilizedRooftopArea,
      panels: totalPanels,
      strings,
      invKw,
      phase3,
      deratedAcKw,
      invCable,
      acdb,
      bom,
      monthly,
      annual,
      series25,
      total25,
      buildings: bldgResults
    });
  });

  if (!siteResults.length) return null;

  // Project-level Aggregation (All Sites)
  let totalCapKw = 0;
  let totalInstalledDckWp = 0;
  let totalPanels = 0;
  let totalGross = 0;
  let totalUtil = 0;
  let totalAnnual = 0;
  let total25 = 0;
  let totalProjectCost = 0;
  const projectMonthly = {};
  MONTHS.forEach(m => projectMonthly[m] = 0);

  siteResults.forEach(sc => {
    totalCapKw += sc.capacityKw;
    totalInstalledDckWp += sc.installedDckWp;
    totalPanels += sc.panels;
    totalGross += sc.grossRooftopArea;
    totalUtil += sc.utilizedRooftopArea;
    totalAnnual += sc.annual;
    total25 += sc.total25;
    totalProjectCost += sc.bom.plantTotal;
    MONTHS.forEach(m => {
      projectMonthly[m] += sc.monthly[m];
    });
  });

  totalCapKw = Math.round(totalCapKw * 100) / 100;
  totalInstalledDckWp = Math.round(totalInstalledDckWp * 100) / 100;
  totalAnnual = Math.round(totalAnnual * 100) / 100;
  total25 = Math.round(total25 * 100) / 100;

  const firstSite = siteResults[0];

  // Consolidated Turnkey BOM
  let consolidatedBom = firstSite.bom;
  if (siteResults.length > 1) {
    const consolidatedBomItems = [];
    const totalModAmt = siteResults.reduce((sum, s) => sum + s.bom.items[0].amt, 0);
    consolidatedBomItems.push({
      sl: 1,
      desc: "Solar PV Modules (Mono PERC / TOPCon)",
      spec: `${firstSite.panelW || 550}W Mono PERC Half-Cut Cells (>21.3% Efficiency)`,
      qty: `${totalPanels} Nos.`,
      amt: totalModAmt
    });
    const invSummary = siteResults.map((s, idx) => `${s.name || `Site ${idx + 1}`}: ${s.invKw} kW`).join(", ");
    const totalInvAmt = siteResults.reduce((sum, s) => sum + (s.bom.items[1]?.amt || 0), 0);
    consolidatedBomItems.push({
      sl: 2,
      desc: "On-Grid Solar String Inverter(s)",
      spec: `Dual MPPT, IP65 Enclosure (${invSummary})`,
      qty: `${siteResults.length} Set(s)`,
      amt: totalInvAmt
    });
    for (let idx = 2; idx < 12; idx++) {
      const baseItem = firstSite.bom.items[idx];
      if (baseItem) {
        const itemAmt = siteResults.reduce((sum, s) => sum + (s.bom.items[idx]?.amt || 0), 0);
        consolidatedBomItems.push({
          sl: idx + 1,
          desc: baseItem.desc,
          spec: baseItem.spec,
          qty: `${siteResults.length} Site(s)`,
          amt: itemAmt
        });
      }
    }
    consolidatedBom = {
      items: consolidatedBomItems,
      plantTotal: totalProjectCost,
      escom: firstSite.bom.escom,
      escomTotal: siteResults.reduce((sum, s) => sum + s.bom.escomTotal, 0)
    };
  }

  // Financial KPIs & Amortization
  const evalCapacity = Math.max(totalCapKw, totalInstalledDckWp);
  const pr = 0.75;
  const cuf = evalCapacity > 0 ? (totalAnnual / (evalCapacity * 8760.0)) * 100 : 0.0;
  const sysEff = pr * 20.0;
  const specificYield = evalCapacity > 0 ? totalAnnual / evalCapacity : 0.0;

  const amcYearly = evalCapacity * 600.0;
  let cumulativeNet = 0.0;
  let payY = 0;
  let payM = 0;
  let paid = false;
  const amort = [];
  let curGen = totalAnnual;
  const tariffScale = customTariff > 0 ? (customTariff / TARIFF_25Y[0]) : 1.0;

  for (let y = 0; y < 25; y++) {
    const baseT = TARIFF_25Y[y < TARIFF_25Y.length ? y : TARIFF_25Y.length - 1];
    const tariff = Math.round(baseT * tariffScale * 100) / 100;
    const revenue = curGen * tariff;
    const net = revenue - amcYearly;
    cumulativeNet += net;

    if (!paid && cumulativeNet >= totalProjectCost) {
      payY = y + 1;
      const remaining = totalProjectCost - (cumulativeNet - net);
      const monthlyNet = Math.max(1e-9, net / 12.0);
      payM = Math.ceil(remaining / monthlyNet);
      paid = true;
    }

    amort.push({
      year: y + 1,
      gen: Math.round(curGen),
      tariff: tariff.toFixed(2),
      revenue: Math.round(revenue),
      amc: Math.round(amcYearly),
      net: Math.round(net),
      cum: Math.round(cumulativeNet),
    });

    curGen *= 0.99;
  }

  const lifetimeProfit = Math.round(cumulativeNet - totalProjectCost);
  const fd25y = Math.round(totalProjectCost * Math.pow(1 + 0.065, 25));

  const co2 = Math.floor((total25 * 0.82) / 1000);
  const trees = Math.floor((co2 * 1000) / 625);
  const carKm = Math.floor((co2 * 1000) / 0.12);
  const coalT = Math.round(total25 * 0.0004 * 10) / 10;

  const series25 = [];
  let curG2 = totalAnnual;
  for (let y = 0; y < 25; y++) {
    series25.push(Math.round(curG2 * 100) / 100);
    curG2 *= 0.99;
  }

  return {
    schemaVersion,
    calculated_at: new Date().toISOString(),
    customer_name: firstSite.name,
    location: firstSite.location,
    mode: firstSite.mode,
    capacityKw: totalCapKw,
    installedDckWp: totalInstalledDckWp,
    rawCapacityKw: firstSite.rawCapacityKw,
    isCapped20kW: firstSite.isCapped20kW,
    kercNotice: firstSite.kercNotice,
    roofAreaStatus: firstSite.roofAreaStatus,
    panels: totalPanels,
    strings: Math.ceil(totalPanels / 20.0),
    invKw: firstSite.invKw,
    phase3: firstSite.phase3,
    deratedAcKw: firstSite.deratedAcKw,
    invCable: firstSite.invCable,
    acdb: firstSite.acdb,
    bom: consolidatedBom,
    monthly: projectMonthly,
    annual: totalAnnual,
    series25,
    total25,
    pr, cuf, sysEff, specificYield,
    amort, payY, payM, lifetimeProfit, fd25y,
    co2, trees, carKm, coalT,
    sitesCount: siteResults.length,
    sites: siteResults
  };
}
window.calculate = calculate;
window.compute = compute;
'''

# Inject calculate function right before function compute()
if 'function calculate(projectDto)' in html:
    html = re.sub(r'// =+\s*// PURE CALCULATION ENGINE.*?window\.calculate = calculate;', lambda m: calc_engine_js.strip(), html, flags=re.DOTALL)
    print("Replaced calculate engine.")
else:
    html = html.replace('function compute() {', calc_engine_js + '\n\nfunction compute() {')
    print("Injected calculate engine.")

# In computeSingleSite, make sure it also sets isPath1
html = html.replace(
    'const invKw = selectInverter(evalCapacity);',
    'const isPath1 = s.mode === "roof";\n  const invKw = selectInverter(evalCapacity, isPath1);'
)
html = html.replace(
    'const deratedAcKw = Math.round(evalCapacity * 0.70 * 100) / 100;',
    'const isPath1 = s.mode === "roof";\n  const deratedAcKw = isPath1 ? Math.round(evalCapacity * 0.70 * 100) / 100 : evalCapacity;'
)

# -------------------------------------------------------------
# 6. Inject modalAdminManual and modalStatutory20kW at end of body
# -------------------------------------------------------------
# Check if modalAdminManual already in html body
if '<div class="shortcuts-modal" id="modalAdminManual"' not in html and '<div id="modalAdminManual"' not in html:
    # Append right before </body>
    closing_body = '</body>'
    modals_markup = f'\n\n{modal_20kw_fixed}\n\n{modal_admin_fixed}\n\n'
    html = html.replace(closing_body, modals_markup + closing_body)
    print("Injected modalAdminManual and modalStatutory20kW before </body>.")

# Also remove defer from chart.umd.min.js so it executes immediately
html = html.replace('<script src="chart.umd.min.js" defer></script>', '<script src="chart.umd.min.js"></script>')

# Make sure updateRibbonGreeting is called in DOMContentLoaded and enterApp
html = html.replace('updateClock();\n\n  const alertEl = document.getElementById("areaStatusAlert");', 'updateClock();\n  if (typeof updateRibbonGreeting === "function") updateRibbonGreeting();\n\n  const alertEl = document.getElementById("areaStatusAlert");')

# Save updated VoltRoof_Combined.html
with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as out:
    out.write(html)
print(f"Wrote updated VoltRoof_Combined.html: {len(html)} bytes")

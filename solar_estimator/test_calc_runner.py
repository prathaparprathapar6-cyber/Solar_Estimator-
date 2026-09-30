import json

# Test script for the pure calculate(projectDto) engine
js_engine_code = """
// ============================================================
// PURE CALCULATION ENGINE (Contract N: schemaVersion 1)
// Pure function: calculate(projectDto) -> resultDto
// Does NOT depend on the DOM. Runs in browser or node/backend.
// ============================================================
function calculate(projectDto) {
  if (!projectDto) return null;
  const schemaVersion = 1;
  const pricing = projectDto.pricing || (typeof dynamicPricing !== "undefined" ? dynamicPricing : {});

  const customTariff = parseFloat(projectDto.custom_tariff) || 8.05;
  const projectMode = projectDto.mode || "roof";
  const rawSites = Array.isArray(projectDto.sites) && projectDto.sites.length > 0 
    ? projectDto.sites.slice(0, 2) // Cap at <= 2 sites (Contract D)
    : [{
        id: "site-1",
        name: projectDto.customer_name || "Site 1",
        mode: projectMode,
        sanctioned_load_kw: projectDto.sanctioned_load_kw,
        distance_m: projectDto.distance_m || 20,
        monthly_units: projectDto.monthly_units || 0,
        tariff: customTariff,
        buildings: projectDto.buildings || []
      }];

  const siteResults = [];

  rawSites.forEach((s, sIdx) => {
    const sName = s.name || `Site Name-${sIdx + 1}`;
    const sLoc = s.location || projectDto.location || "Karnataka";
    const sSanctioned = parseFloat(s.sanctioned_load_kw) || 0;
    
    // Contract D: If sanctioned load filled -> force Path 1 (roof)
    let sMode = s.mode || projectMode;
    if (sSanctioned > 0) {
      sMode = "roof";
    }

    const sDist = parseFloat(s.distance_m) || 20;
    const sTariff = parseFloat(s.tariff) || customTariff;
    const bldgs = Array.isArray(s.buildings) && s.buildings.length > 0
      ? s.buildings.slice(0, 10) // Cap at <= 10 buildings (Contract D)
      : [{
          name: "Building 1",
          length_ft: s.length_ft || 0,
          breadth_ft: s.breadth_ft || 0,
          parapet_ft: s.parapet_ft || 0,
          neighbour: s.neighbour || "None",
          panel_watt: s.panel_watt || 550,
          panel_tech: s.panel_tech || "Mono-PERC (Mono-facial)"
        }];

    let grossRooftopArea = 0;
    let utilizedRooftopArea = 0;
    let rawCapacityKw = 0;
    let totalPanels = 0;
    const bldgResults = [];

    const defaultPanelW = parseInt(s.panel_watt) || 550;
    const defaultTech = s.panel_tech || "Mono-PERC (Mono-facial)";

    if (sMode === "roof") {
      bldgs.forEach((b, bIdx) => {
        const L = parseFloat(b.length_ft ?? b.L) || 0;
        const B = parseFloat(b.breadth_ft ?? b.B) || 0;
        const parapet = Math.max(0, parseFloat(b.parapet_ft ?? b.parapet) || 0);
        const bPanelW = parseInt(b.panel_watt ?? b.panel) || defaultPanelW;
        const bTech = b.panel_tech ?? b.tech ?? defaultTech;
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

      // Update building capacity proportion
      if (bldgResults.length) {
        bldgResults.forEach(br => {
          br.capacityKw = capacityKw;
          br.panels = totalPanels;
        });
      }
    } else {
      capacityKw = Math.min(rawCapacityKw, 20.0);
      if (rawCapacityKw >= 20.0) {
        isCapped20kW = true;
        totalPanels = Math.ceil((20.0 * 1000.0) / defaultPanelW);
        kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
      }
      roofAreaStatus = "Direct Physical Rooftop Sizing";
    }

    if (capacityKw <= 0 || totalPanels <= 0) {
      // Empty or invalid site
      return;
    }

    const installedDckWp = Math.round((totalPanels * defaultPanelW / 1000.0) * 100) / 100;
    const evalCapacity = Math.max(capacityKw, installedDckWp);
    const strings = Math.max(1, Math.ceil(totalPanels / 20.0));

    // Contract: Inverter selected to 70% derating factor of total solar DC output
    const deratedAcKw = Math.round(evalCapacity * 0.70 * 100) / 100;
    const invKw = selectInverter(evalCapacity);
    const phase3 = invKw > 5.0;
    const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
    const acdb = selectAcdbComponents(deratedAcKw, sDist);
    const bom = generatePlantBom(capacityKw, invKw, defaultPanelW, totalPanels, acdb.breakerRating, bldgResults, sDist, defaultTech);

    // Generation models
    const monthly = {};
    let annual = 0;
    MONTHS.forEach((m, idx) => {
      const val = Math.round(evalCapacity * MONTHLY_YIELD[m] * DAYS_IN_MONTH[idx] * 100) / 100;
      monthly[m] = val;
      annual += val;
    });
    annual = Math.round(annual * 100) / 100;

    const series25 = [];
    let curGen = annual;
    let total25 = 0;
    for (let y = 0; y < 25; y++) {
      series25.push(Math.round(curGen * 100) / 100);
      total25 += curGen;
      curGen *= 0.99;
    }
    total25 = Math.round(total25 * 100) / 100;

    siteResults.push({
      id: s.id || `site-${sIdx + 1}`,
      name: sName,
      location: sLoc,
      email: s.email || "",
      mode: sMode,
      panelW: defaultPanelW,
      panelTech: defaultTech,
      distance_m: sDist,
      tariff: sTariff,
      sanctioned_load_kw: sSanctioned,
      roofAreaStatus,
      kercNotice,
      isCapped20kW,
      grossRooftopArea,
      utilizedRooftopArea,
      rawCapacityKw,
      capacityKw,
      deratedAcKw,
      installedDckWp,
      evalCapacity,
      panels: totalPanels,
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
    const consolidatedItems = [];
    const totalModAmt = siteResults.reduce((sum, s) => sum + s.bom.items[0].amt, 0);
    consolidatedItems.push({
      sl: 1,
      desc: "Solar PV Modules (Mono PERC / TOPCon)",
      spec: `${firstSite.panelW}W Mono PERC Half-Cut Cells (>21.3% Efficiency)`,
      qty: `${totalPanels} Nos.`,
      amt: totalModAmt
    });
    const invSummary = siteResults.map(s => `${s.name}: ${s.invKw} kW`).join(", ");
    const totalInvAmt = siteResults.reduce((sum, s) => sum + (s.bom.items[1]?.amt || 0), 0);
    consolidatedItems.push({
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
        consolidatedItems.push({
          sl: idx + 1,
          desc: baseItem.desc,
          spec: baseItem.spec,
          qty: `${siteResults.length} Site(s)`,
          amt: itemAmt
        });
      }
    }
    consolidatedBom = {
      items: consolidatedItems,
      plantTotal: totalProjectCost,
      escom: firstSite.bom.escom,
      escomTotal: siteResults.reduce((sum, s) => sum + s.bom.escomTotal, 0),
      totalCapitalOutlay: totalProjectCost + siteResults.reduce((sum, s) => sum + s.bom.escomTotal, 0)
    };
  }

  // Performance KPIs
  const evalCapacity = Math.max(totalCapKw, totalInstalledDckWp);
  const pr = 0.75;
  const cuf = evalCapacity > 0 ? (totalAnnual / (evalCapacity * 8760.0)) * 100 : 0.0;
  const sysEff = pr * 20.0;
  const specificYield = evalCapacity > 0 ? totalAnnual / evalCapacity : 0.0;

  // Consolidated 25-Year Amortization Schedule
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
  let curG = totalAnnual;
  for (let y = 0; y < 25; y++) {
    series25.push(Math.round(curG * 100) / 100);
    curG *= 0.99;
  }

  return {
    schemaVersion,
    calculated_at: new Date().toISOString(),
    customer_name: projectDto.customer_name || firstSite.name,
    location: projectDto.location || firstSite.location,
    mode: projectMode,
    capacityKw: totalCapKw,
    installedDckWp: totalInstalledDckWp,
    rawCapacityKw: siteResults.reduce((sum, s) => sum + s.rawCapacityKw, 0),
    isCapped20kW: siteResults.some(s => s.isCapped20kW),
    kercNotice: siteResults.map(s => s.kercNotice).filter(Boolean).join(" · "),
    roofAreaStatus: siteResults.map(s => s.roofAreaStatus).filter(Boolean).join(" · "),
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
"""

print("Writing test JS file...")
with open("test_calc_engine.js", "w", encoding="utf-8") as f:
    f.write(js_engine_code)
print("Done writing test_calc_engine.js")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update generatePlantBom to support bldgResults and dist
old_gen_bom_start = "function generatePlantBom(capacityKw, inverterKw, panelWatt, panelCount, acdbBreakerRating) {"
new_gen_bom_start = "function generatePlantBom(capacityKw, inverterKw, panelWatt, panelCount, acdbBreakerRating, bldgResults, dist) {"

assert old_gen_bom_start in html, "old_gen_bom_start not found"
html = html.replace(old_gen_bom_start, new_gen_bom_start, 1)

old_gen_bom_core = """  const cap = Math.max(1.0, capacityKw);
  const roundedCap = Math.round(cap);
  const costPerModule = Math.round(panelWatt * (10000.0 / 550.0));
  const totalModuleCost = panelCount * costPerModule;
  const mc4Pairs = panelCount;
  const mc4Cost = mc4Pairs * 300.0;
  const invSpec = inverterKw > 5.0 ? `${inverterKw} kW, three-phase` : `${inverterKw} kW, single-phase`;
  const rccbRating = acdbBreakerRating <= 16 ? 25 : (acdbBreakerRating <= 32 ? 40 : 63);
  const acdbSpec = `${acdbBreakerRating}A MCB + ${rccbRating}A RCCB + Type-II AC SPD`;"""

new_gen_bom_core = """  const cap = Math.max(1.0, capacityKw);
  const roundedCap = Math.round(cap);

  let totalModuleCost = 0;
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
  }

  const mc4Cost = mc4Pairs * 300.0;
  const invSpec = bldgResults && bldgResults.length > 1
    ? `${inverterKw} kW ${inverterKw > 5 ? 'three-phase' : 'single-phase'} (` + bldgResults.map(b => `${b.name}: ${selectInverter(b.capacityKw)}kW`).join(" + ") + ")"
    : (inverterKw > 5.0 ? `${inverterKw} kW, three-phase` : `${inverterKw} kW, single-phase`);
  const invQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Nos.` : "1 No.";

  const rccbRating = acdbBreakerRating <= 16 ? 25 : (acdbBreakerRating <= 32 ? 40 : 63);
  const acdbSpec = bldgResults && bldgResults.length > 1
    ? bldgResults.map(b => `${b.name}: ${selectAcdbComponents(selectInverter(b.capacityKw), dist || 20).breakerRating}A MCB`).join(" + ") + " + Type-II AC SPD"
    : `${acdbBreakerRating}A MCB + ${rccbRating}A RCCB + Type-II AC SPD`;
  const acdbQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Set(s)` : "1 No.";
  const structQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Roof Set(s)` : "1 Set";
  const dcdbQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} No(s).` : "1 No.";"""

assert old_gen_bom_core in html, "old_gen_bom_core not found"
html = html.replace(old_gen_bom_core, new_gen_bom_core, 1)

# In EXACT_BOM_REPORTS branch:
old_exact_branch = """      if (idx === 1) {
        items.push({ sl: idx, desc: "Solar PV modules", spec: `${panelWatt} W mono PERC / TOPCon`, qty: `${panelCount} Nos.`, amt: totalModuleCost });
      } else if (idx === 2) {
        const invCost = amt * (inverterKw / Math.max(1.0, roundedCap));
        items.push({ sl: idx, desc: "On-grid inverter", spec: invSpec, qty: "1 No.", amt: Math.round(invCost) });
      } else if (idx === 6) {
        items.push({ sl: idx, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost });
      } else if (idx === 8) {
        items.push({ sl: idx, desc: "ACDB", spec: acdbSpec, qty: qty, amt: amt });"""

new_exact_branch = """      if (idx === 1) {
        items.push({ sl: idx, desc: "Solar PV modules", spec: modSpec, qty: modQty, amt: totalModuleCost });
      } else if (idx === 2) {
        const invCost = amt * (inverterKw / Math.max(1.0, roundedCap));
        items.push({ sl: idx, desc: "On-grid inverter", spec: invSpec, qty: invQty, amt: Math.round(invCost) });
      } else if (idx === 3) {
        items.push({ sl: idx, desc: desc, spec: spec, qty: structQty, amt: amt });
      } else if (idx === 6) {
        items.push({ sl: idx, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost });
      } else if (idx === 7) {
        items.push({ sl: idx, desc: desc, spec: spec, qty: dcdbQty, amt: amt });
      } else if (idx === 8) {
        items.push({ sl: idx, desc: "ACDB", spec: acdbSpec, qty: acdbQty, amt: amt });"""

assert old_exact_branch in html, "old_exact_branch not found"
html = html.replace(old_exact_branch, new_exact_branch, 1)

# In return of generatePlantBom:
old_bom_return = "  return { items, plantTotal, escom };\n}"
new_bom_return = """  const escomTotal = escom.reduce((sum, e) => sum + e.amt, 0);
  const totalCapitalOutlay = plantTotal + escomTotal;
  return { items, plantTotal, escom, escomTotal, totalCapitalOutlay };
}"""
assert old_bom_return in html, "old_bom_return not found"
html = html.replace(old_bom_return, new_bom_return, 1)

# 2. In computeSingleSite: pass bldgResults and dist to generatePlantBom
old_css_bom = "const bom = generatePlantBom(capacityKw, invKw, panelW, panels, acdb.breakerRating);"
new_css_bom = "const bom = generatePlantBom(capacityKw, invKw, panelW, panels, acdb.breakerRating, bldgResults, dist);"
assert old_css_bom in html, "old_css_bom not found"
html = html.replace(old_css_bom, new_css_bom, 1)

# 3. Add 20kW modal functions & check in onCalculateClick
old_on_calc = """  switchView('dashboard');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  toast("⚡ System Calculated & Loaded on Dashboard!");
}"""

new_on_calc = """  switchView('dashboard');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  toast("⚡ System Calculated & Loaded on Dashboard!");

  // Check statutory 20 kW LT ceiling
  if (curSite && curSite.computed && curSite.computed.rawCapacityKw > 20.0) {
    check20kWLimit(curSite, true);
  }
}

function check20kWLimit(site, isExplicitClick = false) {
  if (!site) return;
  const rawCap = site.computed?.rawCapacityKw || 0;
  if (rawCap > 20.0 && (!site.warned20kW || isExplicitClick)) {
    const modal = document.getElementById("modalStatutory20kW");
    const nameEl = document.getElementById("warnSiteName");
    const capEl = document.getElementById("warnRawCap");
    if (modal && nameEl && capEl) {
      nameEl.textContent = site.name || `Site Name-${sites.indexOf(site) + 1}`;
      capEl.textContent = `${rawCap.toFixed(2)} kW`;
      modal.style.display = "flex";
      site.warned20kW = true;
    }
  }
}

function close20kWModal(splitNewSite = false) {
  const modal = document.getElementById("modalStatutory20kW");
  if (modal) modal.style.display = "none";
  if (splitNewSite) {
    addNewSite();
  }
}"""

assert old_on_calc in html, "old_on_calc not found"
html = html.replace(old_on_calc, new_on_calc, 1)

# 4. In liveUpdate(): replace BOM and ESCOM rendering with renderBomView()
old_live_bom_render = """  // Render BOM Table
  const bomBody = document.getElementById("bomBody");
  bomBody.innerHTML = "";
  r.bom.items.forEach(it => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="tc">${String(it.sl).padStart(2, "0")}</td>
      <td><strong>${it.desc}</strong></td>
      <td style="color:var(--muted)">${it.spec}</td>
      <td class="tc">${it.qty}</td>
      <td class="tr" style="font-weight:700">₹ ${it.amt.toLocaleString()}</td>
    `;
    bomBody.appendChild(tr);
  });
  document.getElementById("bomTotal").textContent = `₹ ${r.bom.plantTotal.toLocaleString()} (${(r.bom.plantTotal / 1e5).toFixed(2)} Lakhs)`;

  // Render ESCOM Budget
  const escomBody = document.getElementById("escomBody");
  escomBody.innerHTML = "";
  r.bom.escom.forEach(e => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="tc">${String(e.sl).padStart(2, "0")}</td>
      <td><strong>${e.name}</strong></td>
      <td style="color:var(--muted)">${e.spec} <span style="font-size:.72rem;color:var(--dim)">(${e.note})</span></td>
      <td class="tr" style="font-weight:700">₹ ${e.amt.toLocaleString()}</td>
    `;
    escomBody.appendChild(tr);
  });"""

new_live_bom_render = """  // Render BOM & Commercial Matrix View
  renderBomView();"""

assert old_live_bom_render in html, "old_live_bom_render not found"
html = html.replace(old_live_bom_render, new_live_bom_render, 1)

# Add renderBomView implementation
bom_view_impl = """
let bomActiveSiteIndex = 0;

function switchBomSite(idx) {
  bomActiveSiteIndex = idx;
  renderBomView();
}

function renderBomView() {
  const validSites = sites.filter(s => s.computed);
  if (!validSites || validSites.length === 0) return;

  if (bomActiveSiteIndex >= validSites.length) bomActiveSiteIndex = 0;
  const isMulti = validSites.length > 1;

  // Site selector tabs
  const tabWrap = document.getElementById("bomSiteSelectorWrap");
  const tabContainer = document.getElementById("bomSiteTabs");
  if (tabWrap && tabContainer) {
    if (isMulti) {
      tabWrap.style.display = "block";
      tabContainer.innerHTML = validSites.map((s, i) => {
        const isActive = i === bomActiveSiteIndex;
        const sName = s.name || `Site Name-${i + 1}`;
        return `
          <button type="button" class="preset ${isActive ? 'on' : ''}" onclick="switchBomSite(${i})" style="padding:6px 14px;font-size:.78rem;display:inline-flex;align-items:center;gap:6px">
            <span style="color:${isActive ? '#10b981' : '#64748b'}">●</span> ${sName} (${s.computed.capacityKw.toFixed(1)} kW)
          </button>
        `;
      }).join("");
    } else {
      tabWrap.style.display = "none";
    }
  }

  // Active site BOM to render
  const targetSite = isMulti ? validSites[bomActiveSiteIndex] : validSites[0];
  const sComp = targetSite.computed;

  // Card header and titles
  const titleEl = document.getElementById("bomCardTitle");
  const subEl = document.getElementById("bomCardSub");
  const statusBadge = document.getElementById("bomSiteStatusBadge");
  const warn20kW = document.getElementById("bomSiteWarning20kW");

  if (titleEl) {
    titleEl.textContent = isMulti ? `📦 Site ${bomActiveSiteIndex + 1}: ${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`} — Bill of Materials (BOM)` : `📦 Bill of Materials (BOM) — Plant-Side Equipment`;
  }
  if (subEl) {
    subEl.textContent = isMulti ? `12-item engineering specification and cost breakdown for ${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`} (${sComp.capacityKw.toFixed(2)} kW)` : `Full 12-item commercial LT equipment list with dynamic module, inverter & switchgear sizing`;
  }
  if (statusBadge) {
    statusBadge.innerHTML = isMulti ? `<span style="font-size:.72rem;font-weight:700;color:var(--primary);background:rgba(37,99,235,0.1);padding:3px 8px;border-radius:6px;border:1px solid rgba(37,99,235,0.25)">SITE ${bomActiveSiteIndex + 1} OF ${validSites.length}</span>` : "";
  }
  if (warn20kW) {
    if (sComp.rawCapacityKw > 20.0) {
      warn20kW.style.display = "block";
      warn20kW.textContent = `⚠️ Statutory 20 kW LT Ceiling Applied: Rooftop unconstrained potential was ${sComp.rawCapacityKw.toFixed(2)} kW. Capped at 20.00 kW in compliance with KERC / ESCOM regulations.`;
    } else {
      warn20kW.style.display = "none";
    }
  }

  // Populate BOM Table
  const bomBody = document.getElementById("bomBody");
  if (bomBody) {
    bomBody.innerHTML = "";
    sComp.bom.items.forEach(it => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="tc">${String(it.sl).padStart(2, "0")}</td>
        <td><strong>${it.desc}</strong></td>
        <td style="color:var(--muted)">${it.spec}</td>
        <td class="tc">${it.qty}</td>
        <td class="tr" style="font-weight:700">₹ ${it.amt.toLocaleString()}</td>
      `;
      bomBody.appendChild(tr);
    });
  }
  const bomTotEl = document.getElementById("bomTotal");
  if (bomTotEl) {
    bomTotEl.textContent = `₹ ${sComp.bom.plantTotal.toLocaleString()} (${(sComp.bom.plantTotal / 1e5).toFixed(2)} Lakhs)`;
  }

  // Populate ESCOM Table
  const escomTitle = document.getElementById("escomCardTitle");
  if (escomTitle) {
    escomTitle.textContent = isMulti ? `🏛️ ESCOM / Utility Approvals & Grid Budget (${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`})` : `🏛️ ESCOM / Utility Approval & Interconnection Budget`;
  }
  const escomBody = document.getElementById("escomBody");
  if (escomBody) {
    escomBody.innerHTML = "";
    sComp.bom.escom.forEach(e => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="tc">${String(e.sl).padStart(2, "0")}</td>
        <td><strong>${e.name}</strong></td>
        <td style="color:var(--muted)">${e.spec} <span style="font-size:.72rem;color:var(--dim)">(${e.note})</span></td>
        <td class="tr" style="font-weight:700">₹ ${e.amt.toLocaleString()}</td>
      `;
      escomBody.appendChild(tr);
    });
  }
  const siteOutlayTitle = document.getElementById("siteTotalOutlayTitle");
  const siteOutlayVal = document.getElementById("siteTotalOutlayVal");
  if (siteOutlayTitle) {
    siteOutlayTitle.textContent = isMulti ? `Total Capital Required for ${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`}:` : `Total Estimated Capital Investment Required:`;
  }
  if (siteOutlayVal) {
    const sTot = sComp.bom.plantTotal + sComp.bom.escomTotal;
    siteOutlayVal.textContent = `₹ ${sTot.toLocaleString()} (${(sTot / 1e5).toFixed(2)} Lakhs)`;
  }

  // Portfolio Capex Matrix Card
  const capexCard = document.getElementById("cardPortfolioCapexMatrix");
  const capexBody = document.getElementById("portfolioCapexBody");
  if (capexCard && capexBody) {
    if (isMulti) {
      capexCard.style.display = "block";
      let totCap = 0, totBom = 0, totEsc = 0, grandTot = 0;
      capexBody.innerHTML = validSites.map((s, idx) => {
        const c = s.computed;
        const cap = c.capacityKw;
        const bCost = c.bom.plantTotal;
        const eCost = c.bom.escomTotal;
        const sTot = bCost + eCost;
        totCap += cap; totBom += bCost; totEsc += eCost; grandTot += sTot;
        const capMark = c.rawCapacityKw > 20.0 ? " *" : "";
        return `
          <tr>
            <td class="tc">${String(idx + 1).padStart(2, "0")}</td>
            <td><strong>${s.name || `Site Name-${idx + 1}`}</strong> <span style="font-size:.72rem;color:var(--muted)">(${s.loc || "Karnataka"})</span></td>
            <td class="tc">${c.buildings ? c.buildings.length : 1} Nos.</td>
            <td class="tc">${cap.toFixed(2)} kW${capMark}</td>
            <td class="tr">₹ ${bCost.toLocaleString()}</td>
            <td class="tr">₹ ${eCost.toLocaleString()}</td>
            <td class="tr" style="font-weight:700">₹ ${sTot.toLocaleString()}</td>
          </tr>
        `;
      }).join("");

      document.getElementById("matrixTotCap").textContent = `${totCap.toFixed(2)} kW`;
      document.getElementById("matrixTotBom").textContent = `₹ ${totBom.toLocaleString()}`;
      document.getElementById("matrixTotEscom").textContent = `₹ ${totEsc.toLocaleString()}`;
      document.getElementById("matrixGrandTotal").textContent = `₹ ${grandTot.toLocaleString()} (${(grandTot / 1e5).toFixed(2)} Lakhs)`;
    } else {
      capexCard.style.display = "none";
    }
  }
}
"""

html = html.replace("function renderBuildingTabs() {", bom_view_impl + "\nfunction renderBuildingTabs() {", 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: Updated index.html with all JavaScript logic!")

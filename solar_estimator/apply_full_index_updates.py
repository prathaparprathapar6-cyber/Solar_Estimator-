with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Customer / Site Details inputs
old_cust_form = '''          <div class="field-row" style="grid-template-columns:1.2fr 1fr 1.2fr auto;align-items:end;gap:12px">
            <div class="field" style="margin:0"><label>Company / Site Name *</label><input type="text" id="cfgName" value="" placeholder="e.g. Site Name-1" oninput="onSiteNameInput()"></div>
            <div class="field" style="margin:0"><label>Location / Address *</label><input type="text" id="cfgLoc" value="" placeholder="e.g. Shivamogga, Karnataka" oninput="saveCurrentFormToActiveSite();liveUpdate()"></div>
            <div class="field" style="margin:0"><label>Client Email Address *</label><input type="email" id="cfgEmail" value="" placeholder="e.g. client@example.com" oninput="saveCurrentFormToActiveSite();liveUpdate()"></div>
            <button class="btn btn-p" type="button" onclick="saveCurrentFormToActiveSite();toast('Site details saved successfully')" style="height:42px">💾 Save</button>
          </div>
          <div class="field-row" style="margin-top:12px;grid-template-columns:1fr 1fr;gap:12px">
            <div class="field" style="margin:0">
              <label>Year-1 Grid Electricity Tariff (₹ / kWh)</label>
              <input type="number" id="cfgTariff" value="" placeholder="0.00" min="0" max="30" step="0.05" oninput="saveCurrentFormToActiveSite();liveUpdate()">
            </div>
            <div class="field" style="margin:0">
              <label>Project Actions</label>
              <div style="display:flex;gap:8px">
                <button class="btn" type="button" onclick="saveProject()" style="flex:1">💾 Save Project</button>
                <button class="btn" type="button" onclick="exportCSV()" style="flex:1">📊 Export CSV</button>
              </div>
            </div>
          </div>'''

new_cust_form = '''          <div class="field-row" style="grid-template-columns:1.1fr 1fr 1.1fr 1.1fr auto;align-items:end;gap:10px">
            <div class="field" style="margin:0"><label>Company / Site Name *</label><input type="text" id="cfgName" value="" placeholder="e.g. Site Name-1" oninput="onSiteNameInput()"></div>
            <div class="field" style="margin:0"><label>Contact Number *</label><input type="tel" id="cfgContact" value="" placeholder="+91 98765 43210" oninput="saveCurrentFormToActiveSite();liveUpdate()"></div>
            <div class="field" style="margin:0"><label>Location / Address *</label><input type="text" id="cfgLoc" value="" placeholder="e.g. Shivamogga, Karnataka" oninput="saveCurrentFormToActiveSite();liveUpdate()"></div>
            <div class="field" style="margin:0"><label>Client Email Address *</label><input type="email" id="cfgEmail" value="" placeholder="e.g. client@example.com" oninput="saveCurrentFormToActiveSite();liveUpdate()"></div>
            <button class="btn btn-p" type="button" onclick="saveCurrentFormToActiveSite();toast('Site details saved successfully')" style="height:42px">💾 Save</button>
          </div>
          <div class="field-row" style="margin-top:12px;grid-template-columns:1.2fr 1fr 1fr;gap:12px">
            <div class="field" style="margin:0">
              <label>Sanctioned Load / Contract Demand (kW)</label>
              <input type="number" id="cfgSanctionedLoad" value="" placeholder="e.g. 15 (Max 20 kW LT Limit)" min="0" max="100" step="0.5" oninput="saveCurrentFormToActiveSite();liveUpdate()">
            </div>
            <div class="field" style="margin:0">
              <label>Year-1 Grid Electricity Tariff (₹ / kWh)</label>
              <input type="number" id="cfgTariff" value="" placeholder="0.00" min="0" max="30" step="0.05" oninput="saveCurrentFormToActiveSite();liveUpdate()">
            </div>
            <div class="field" style="margin:0">
              <label>Project Actions</label>
              <div style="display:flex;gap:8px">
                <button class="btn" type="button" onclick="saveProject()" style="flex:1">💾 Save Project</button>
                <button class="btn" type="button" onclick="exportCSV()" style="flex:1">📊 Export CSV</button>
              </div>
            </div>
          </div>'''

assert old_cust_form in content, "old_cust_form not found"
content = content.replace(old_cust_form, new_cust_form)

# 2. Add areaStatusAlert in Path 1
old_path1_field = '''            <div class="field"><label>Length &amp; Breadth of Rooftop (ft) *</label>'''
new_path1_field = '''            <div id="areaStatusAlert" style="display:none;margin-bottom:12px;padding:9px 12px;border-radius:9px;font-size:0.78rem;font-weight:700"></div>
            <div class="field"><label>Length &amp; Breadth of Rooftop (ft) *</label>'''

assert old_path1_field in content, "old_path1_field not found"
content = content.replace(old_path1_field, new_path1_field)

# 3. Update saveCurrentFormToActiveSite & loadSiteToForm
old_save = '''  s.name = document.getElementById("cfgName")?.value || "";
  s.loc = document.getElementById("cfgLoc")?.value || "";
  s.email = document.getElementById("cfgEmail")?.value || "";
  s.tariff = document.getElementById("cfgTariff")?.value || "";'''

new_save = '''  s.name = document.getElementById("cfgName")?.value || "";
  s.contact = document.getElementById("cfgContact")?.value || "";
  s.loc = document.getElementById("cfgLoc")?.value || "";
  s.email = document.getElementById("cfgEmail")?.value || "";
  s.sanctionedLoad = document.getElementById("cfgSanctionedLoad")?.value || "";
  s.tariff = document.getElementById("cfgTariff")?.value || "";'''

assert old_save in content, "old_save not found"
content = content.replace(old_save, new_save)

old_load = '''  if (document.getElementById("cfgName")) document.getElementById("cfgName").value = s.name || "";
  if (document.getElementById("cfgLoc")) document.getElementById("cfgLoc").value = s.loc || "";
  if (document.getElementById("cfgEmail")) document.getElementById("cfgEmail").value = s.email || "";
  if (document.getElementById("cfgTariff")) document.getElementById("cfgTariff").value = s.tariff || "";'''

new_load = '''  if (document.getElementById("cfgName")) document.getElementById("cfgName").value = s.name || "";
  if (document.getElementById("cfgContact")) document.getElementById("cfgContact").value = s.contact || "";
  if (document.getElementById("cfgLoc")) document.getElementById("cfgLoc").value = s.loc || "";
  if (document.getElementById("cfgEmail")) document.getElementById("cfgEmail").value = s.email || "";
  if (document.getElementById("cfgSanctionedLoad")) document.getElementById("cfgSanctionedLoad").value = s.sanctionedLoad || "";
  if (document.getElementById("cfgTariff")) document.getElementById("cfgTariff").value = s.tariff || "";'''

assert old_load in content, "old_load not found"
content = content.replace(old_load, new_load)

# 4. Update computeSingleSite with sanctioned load and area status logic
old_comp_single = '''  if (rawCapacityKw <= 0 || panels <= 0) return null;

  // Single site capped at 20 kW max!
  const capacityKw = Math.min(rawCapacityKw, 20.0);
  if (rawCapacityKw > 20.0) {
    panels = Math.ceil((20.0 * 1000.0) / panelW);
  }
  const installedDckWp = Math.round((panels * panelW / 1000.0) * 100) / 100;
  const evalCapacity = Math.max(capacityKw, installedDckWp);
  const strings = Math.max(1, Math.ceil(panels / 20.0));'''

new_comp_single = '''  if (rawCapacityKw <= 0 || panels <= 0) return null;

  const sanctionedLoad = parseFloat(s.sanctionedLoad) || 0;
  let roofAreaStatus = "";
  let kercNotice = "";
  let capacityKw = 0;

  if (sanctionedLoad > 0) {
    const effectiveCd = Math.min(20.0, sanctionedLoad);
    const reqAreaSqft = Math.round(effectiveCd * 80.0 * 10) / 10;
    const maxRoofCapKw = Math.round((utilizedRooftopArea / 80.0) * 100) / 100;

    if (utilizedRooftopArea >= reqAreaSqft) {
      roofAreaStatus = `Sufficient Rooftop Area (+${Math.round(utilizedRooftopArea - reqAreaSqft)} sq.ft surplus)`;
      capacityKw = effectiveCd;
    } else {
      roofAreaStatus = `Deficit Rooftop Area (-${Math.round(reqAreaSqft - utilizedRooftopArea)} sq.ft deficit, limited to ${maxRoofCapKw.toFixed(2)} kW)`;
      capacityKw = maxRoofCapKw;
    }

    panels = panelW > 0 ? Math.ceil((capacityKw * 1000.0) / panelW) : 0;
    rawCapacityKw = Math.max(sanctionedLoad, Math.round((utilizedRooftopArea / 80.0) * 100) / 100);

    if (sanctionedLoad >= 20.0 || rawCapacityKw >= 20.0) {
      kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
    }
  } else {
    capacityKw = Math.min(rawCapacityKw, 20.0);
    if (rawCapacityKw >= 20.0) {
      panels = Math.ceil((20.0 * 1000.0) / panelW);
      kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
    }
    roofAreaStatus = "Direct Physical Rooftop Sizing";
  }

  s.roofAreaStatus = roofAreaStatus;
  s.kercNotice = kercNotice;

  const installedDckWp = Math.round((panels * panelW / 1000.0) * 100) / 100;
  const evalCapacity = Math.max(capacityKw, installedDckWp);
  const strings = Math.max(1, Math.ceil(panels / 20.0));'''

assert old_comp_single in content, "old_comp_single not found"
content = content.replace(old_comp_single, new_comp_single)

# Attach roofAreaStatus and kercNotice to returned object from computeSingleSite
old_return_obj = '''    mode: s.mode,
    panelW,
    panelTech: activeTech,
    dist,'''

new_return_obj = '''    mode: s.mode,
    panelW,
    panelTech: activeTech,
    dist,
    roofAreaStatus: roofAreaStatus,
    kercNotice: kercNotice,
    sanctionedLoad: sanctionedLoad,'''

assert old_return_obj in content, "old_return_obj not found"
content = content.replace(old_return_obj, new_return_obj)

# 5. Update liveUpdate to render areaStatusAlert
old_live_ret = '''  if (!r) {
    document.getElementById("topKwp").textContent = "— kWp";'''

new_live_ret = '''  const alertEl = document.getElementById("areaStatusAlert");
  if (alertEl) {
    if (r && r.roofAreaStatus && siteObj.sanctionedLoad && parseFloat(siteObj.sanctionedLoad) > 0) {
      alertEl.style.display = "block";
      const isDeficit = r.roofAreaStatus.toLowerCase().includes("deficit");
      alertEl.style.background = isDeficit ? "rgba(239, 68, 68, 0.12)" : "rgba(16, 185, 129, 0.12)";
      alertEl.style.border = isDeficit ? "1px solid rgba(239, 68, 68, 0.35)" : "1px solid rgba(16, 185, 129, 0.35)";
      alertEl.style.color = isDeficit ? "#f87171" : "#34d399";
      alertEl.innerHTML = (isDeficit ? "⚠️ " : "✓ ") + r.roofAreaStatus + (r.kercNotice ? `<br><span style="color:#ef4444;font-size:0.72rem;display:inline-block;margin-top:4px">⚠️ ${r.kercNotice}</span>` : "");
    } else {
      alertEl.style.display = "none";
    }
  }

  if (!r) {
    document.getElementById("topKwp").textContent = "— kWp";'''

assert old_live_ret in content, "old_live_ret not found"
content = content.replace(old_live_ret, new_live_ret)

# 6. Update BOM warning in renderBom to display exact notice
old_bom_warn = '''    if (sComp.rawCapacityKw > 20.0) {
      warn20kW.style.display = "block";
      warn20kW.textContent = `⚠️ Statutory 20 kW LT Ceiling Applied: Rooftop unconstrained potential was ${sComp.rawCapacityKw.toFixed(2)} kW. Capped at 20.00 kW in compliance with KERC / ESCOM regulations.`;
    } else {
      warn20kW.style.display = "none";
    }'''

new_bom_warn = '''    const has20kNotice = sComp.rawCapacityKw >= 20.0 || (targetSite.sanctionedLoad && parseFloat(targetSite.sanctionedLoad) >= 20.0) || sComp.kercNotice;
    if (has20kNotice) {
      warn20kW.style.display = "block";
      warn20kW.textContent = "⚠️ 20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
    } else {
      warn20kW.style.display = "none";
    }'''

assert old_bom_warn in content, "old_bom_warn not found"
content = content.replace(old_bom_warn, new_bom_warn)

# 7. Update downloadPdf payload with contact_number and sanctioned_load_kw
old_dl_payload = '''  const projName = (sites[0]?.name || document.getElementById("cfgName")?.value || "Solar Rooftop Project").trim();
  const projLoc = (sites[0]?.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim();
  const projEmail = (sites[0]?.email || document.getElementById("cfgEmail")?.value || "").trim();

  const payload = {
    mode: current.mode,
    customer_name: projName,
    location: projLoc,
    email: projEmail,
    custom_tariff: parseFloat(sites[0]?.tariff) || 8.05,
    sites: sites.map((s, sIdx) => {
      const siteName = (s.name || `Site Name-${sIdx + 1}`).trim();
      const siteLoc = (s.loc || projLoc).trim();
      const siteEmail = (s.email || projEmail).trim();
      const siteDist = parseFloat(s.dist) || 20.0;
      const bldgs = (s.buildings && s.buildings.length > 0) ? s.buildings : [{
        name: "Building 1",
        L: s.L || 40,
        B: s.B || 30,
        parapet: s.parapet || 1.5,
        neighbour: s.neighbour || "None",
        panel: s.panel || "550"
      }];
      return {
        site_id: s.id || `site-${sIdx + 1}`,
        name: siteName,
        location: siteLoc,
        email: siteEmail,
        mode: s.mode || "roof",'''

new_dl_payload = '''  const projName = (sites[0]?.name || document.getElementById("cfgName")?.value || "Solar Rooftop Project").trim();
  const projContact = (sites[0]?.contact || document.getElementById("cfgContact")?.value || "").trim();
  const projLoc = (sites[0]?.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim();
  const projEmail = (sites[0]?.email || document.getElementById("cfgEmail")?.value || "").trim();
  const projSanctioned = parseFloat(sites[0]?.sanctionedLoad || document.getElementById("cfgSanctionedLoad")?.value) || null;

  const payload = {
    mode: current.mode,
    customer_name: projName,
    location: projLoc,
    email: projEmail,
    contact_number: projContact,
    sanctioned_load_kw: projSanctioned,
    custom_tariff: parseFloat(sites[0]?.tariff) || 8.05,
    sites: sites.map((s, sIdx) => {
      const siteName = (s.name || `Site Name-${sIdx + 1}`).trim();
      const siteContact = (s.contact || projContact).trim();
      const siteLoc = (s.loc || projLoc).trim();
      const siteEmail = (s.email || projEmail).trim();
      const siteSanctioned = parseFloat(s.sanctionedLoad) || projSanctioned;
      const siteDist = parseFloat(s.dist) || 20.0;
      const bldgs = (s.buildings && s.buildings.length > 0) ? s.buildings : [{
        name: "Building 1",
        L: s.L || 40,
        B: s.B || 30,
        parapet: s.parapet || 1.5,
        neighbour: s.neighbour || "None",
        panel: s.panel || "550"
      }];
      return {
        site_id: s.id || `site-${sIdx + 1}`,
        name: siteName,
        contact_number: siteContact,
        sanctioned_load_kw: siteSanctioned,
        location: siteLoc,
        email: siteEmail,
        mode: s.mode || "roof",'''

assert old_dl_payload in content, "old_dl_payload not found"
content = content.replace(old_dl_payload, new_dl_payload)

# Also update the non-multi payload fields in downloadPdf
old_single_fields = '''    monthly_units: num("cfgUnits"),
    distance_m: current.dist,
    panel_watt: current.panelW,
    panel_tech: current.panelTech || "Mono-PERC (Mono-facial)"
  };'''

new_single_fields = '''    monthly_units: num("cfgUnits"),
    distance_m: current.dist,
    panel_watt: current.panelW,
    panel_tech: current.panelTech || "Mono-PERC (Mono-facial)",
    contact_number: projContact,
    sanctioned_load_kw: projSanctioned
  };'''

assert old_single_fields in content, "old_single_fields not found"
content = content.replace(old_single_fields, new_single_fields)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated index.html!")

import os
import re

media_html_path = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html"

with open(media_html_path, "r", encoding="utf-8", errors="ignore") as f:
    media_html = f.read()

with open("extracted_modals.html", "r", encoding="utf-8", errors="ignore") as f:
    modals_html = f.read()

# 1. Insert modals right before <div class="mobile-bar">
idx_mobile = media_html.find('<div class="mobile-bar">')
if idx_mobile == -1:
    raise RuntimeError("Could not find <div class=\"mobile-bar\"> in media_html")

assembled_html = media_html[:idx_mobile] + "\n\n" + modals_html + "\n\n" + media_html[idx_mobile:]

print("Successfully injected modals_html. New length:", len(assembled_html))

# 2. Check if calculate(projectDto) is in assembled_html
# We will inject the pure calculate(projectDto) engine right before function compute()
idx_comp = assembled_html.find("function compute()")
if idx_comp == -1:
    raise RuntimeError("Could not find function compute() in assembled_html")

with open("test_calc_engine.js", "r", encoding="utf-8", errors="ignore") as f:
    pure_calc_js = f.read()

# Replace compute() with the integrated compute() that calls calculate(projectDto)
new_compute_js = """
// ============================================================
// PURE CALCULATION ENGINE & COMPUTE BRIDGE (Contract N)
// ============================================================
""" + pure_calc_js + """

function compute() {
  saveCurrentFormToActiveSite();
  
  // Construct projectDto conforming to schemaVersion: 1
  const projectDto = {
    schemaVersion: 1,
    customer_name: (sites[0]?.name || document.getElementById("cfgName")?.value || "Solar Site").trim(),
    location: (sites[0]?.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim(),
    contact_number: (sites[0]?.contact || document.getElementById("cfgContact")?.value || "").trim(),
    email: (sites[0]?.email || document.getElementById("cfgEmail")?.value || "").trim(),
    sanctioned_load_kw: parseFloat(sites[0]?.sanctionedLoad || document.getElementById("cfgSanctionedLoad")?.value) || null,
    custom_tariff: parseFloat(sites[0]?.tariff || document.getElementById("cfgTariff")?.value) || 8.05,
    mode: mode,
    pricing: typeof dynamicPricing !== "undefined" ? dynamicPricing : {},
    sites: sites.slice(0, 2).map((s, idx) => ({
      id: s.id || `site-${idx + 1}`,
      name: (s.name || `Site Name-${idx + 1}`).trim(),
      location: (s.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim(),
      contact_number: (s.contact || document.getElementById("cfgContact")?.value || "").trim(),
      email: (s.email || document.getElementById("cfgEmail")?.value || "").trim(),
      sanctioned_load_kw: parseFloat(s.sanctionedLoad) || null,
      mode: s.mode || mode || "roof",
      tariff: parseFloat(s.tariff) || 8.05,
      distance_m: parseFloat(s.dist) || 20.0,
      monthly_units: parseFloat(s.units) || 0,
      buildings: (s.buildings || []).slice(0, 10).map((b, bIdx) => ({
        id: b.id || `bldg-${bIdx + 1}`,
        name: b.name || `Building ${bIdx + 1}`,
        length_ft: parseFloat(b.L) || 0,
        breadth_ft: parseFloat(b.B) || 0,
        parapet_ft: parseFloat(b.parapet) || 0,
        neighbour: b.neighbour || "None",
        panel_watt: parseInt(b.panel) || 550,
        panel_tech: b.tech || s.tech || "Mono-PERC (Mono-facial)"
      }))
    }))
  };

  const resultDto = calculate(projectDto);
  if (!resultDto) return null;

  // Sync per-site computed results back to sites array
  if (resultDto.sites && Array.isArray(resultDto.sites)) {
    resultDto.sites.forEach((sc, i) => {
      if (sites[i]) {
        sites[i].computed = sc;
      }
    });
  }

  return resultDto;
}
window.compute = compute;
"""

# Replace old compute() in assembled_html
# Find end of old compute function: it ends right before `function liveUpdate()`
idx_live = assembled_html.find("function liveUpdate()")
if idx_live == -1:
    raise RuntimeError("Could not find function liveUpdate() in assembled_html")

assembled_html = assembled_html[:idx_comp] + new_compute_js + "\n\n" + assembled_html[idx_live:]
print("Successfully integrated pure calculate(projectDto) and new compute()! Total length:", len(assembled_html))

# Write to VoltRoof_Combined.html
with open("VoltRoof_Combined.html", "w", encoding="utf-8") as out_f:
    out_f.write(assembled_html)

print("Saved assembled VoltRoof_Combined.html")

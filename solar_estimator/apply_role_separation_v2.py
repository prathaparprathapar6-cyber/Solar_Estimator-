import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update finishEnterApp and window.enterApp around line 11288
old_finish_block = '''function finishEnterApp(n) {
  try { localStorage.setItem("voltroof_user", n); } catch (e) {}
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
  if (typeof setGateOpen === "function") setGateOpen(false);
  document.body.classList.remove("gate-open");

  const greetEl = document.getElementById("greetName");
  if (greetEl) greetEl.textContent = n;
  const greetBar = document.getElementById("greetBar");
  if (greetBar) greetBar.style.display = "block";

  const appQ = document.getElementById("appQuoteBar");
  if (appQ) appQ.style.display = "block";
  applyDailyQuotes();

  if (typeof sites !== "undefined" && sites[activeSiteIndex] && !sites[activeSiteIndex].name) {
    sites[activeSiteIndex].name = "";
    const cfgName = document.getElementById("cfgName");
    if (cfgName) cfgName.value = "";
  }
  if (typeof renderSiteTabs === "function") renderSiteTabs();
  if (typeof liveUpdate === "function") liveUpdate();
  if (typeof updateAdminUIState === "function") updateAdminUIState();
  showGreetPopup(n);
}

// Override enterApp with animation
window.enterApp = function enterApp() {
  const inputEl = document.getElementById("gateName");
  let n = (inputEl?.value || "").trim();
  if (!n) {
    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (admin) n = admin.username;
    else n = localStorage.getItem("voltroof_user") || "Engineer";
  }
  animateLogoAndNameToNav(n, () => finishEnterApp(n));
};

// After admin login from gate — same logo fly + greeting
if (typeof loginAdminFromGate === "function" && !loginAdminFromGate._flyHook) {
  const _laf = loginAdminFromGate;
  window.loginAdminFromGate = async function() {
    const r = await _laf.apply(this, arguments);
    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (admin) {
      const n = admin.username;
      // If still on gate, fly then enter
      const gate = document.getElementById("nameGate");
      if (gate && !gate.classList.contains("hidden") && gate.style.display !== "none") {
        animateLogoAndNameToNav(n, () => finishEnterApp(n));
      } else {
        showGreetPopup(n);
        const appQ = document.getElementById("appQuoteBar");
        if (appQ) appQ.style.display = "block";
      }
      if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();
    }
    return r;
  };
  window.loginAdminFromGate._flyHook = true;
}'''

new_finish_block = '''function finishEnterApp(n, isAdmin = false) {
  try { localStorage.setItem("voltroof_user", n); } catch (e) {}

  // ROLE SEPARATION ENFORCEMENT:
  // Customer Login: entering via Customer Name form explicitly clears admin session.
  // Admin nav items (Policy Desk, Content Studio, Admin Roster, Control Center)
  // are NEVER shown to a customer!
  if (!isAdmin) {
    try { localStorage.removeItem("voltroof_admin_session"); } catch (e) {}
    if (typeof switchView === "function") switchView("dashboard");
  }

  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
  if (typeof setGateOpen === "function") setGateOpen(false);
  document.body.classList.remove("gate-open");

  const greetEl = document.getElementById("greetName");
  if (greetEl) greetEl.textContent = n;
  const greetBar = document.getElementById("greetBar");
  if (greetBar) greetBar.style.display = "block";

  const appQ = document.getElementById("appQuoteBar");
  if (appQ) appQ.style.display = "block";
  applyDailyQuotes();

  if (typeof sites !== "undefined" && sites[activeSiteIndex] && !sites[activeSiteIndex].name) {
    sites[activeSiteIndex].name = "";
    const cfgName = document.getElementById("cfgName");
    if (cfgName) cfgName.value = "";
  }
  if (typeof renderSiteTabs === "function") renderSiteTabs();
  if (typeof liveUpdate === "function") liveUpdate();

  // Enforce correct navigation visibility
  if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();
  if (typeof updateAdminUIState === "function") updateAdminUIState();
  if (typeof updateRibbonGreeting === "function") updateRibbonGreeting(n);
  showGreetPopup(n);
}

// Override enterApp with animation (STRICTLY Customer Login)
window.enterApp = function enterApp() {
  const inputEl = document.getElementById("gateName");
  let n = (inputEl?.value || "").trim();
  if (!n) {
    n = "Engineer";
  }
  // Immediately clear admin session for customer login
  try { localStorage.removeItem("voltroof_admin_session"); } catch (e) {}
  if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();
  if (typeof updateAdminUIState === "function") updateAdminUIState();

  animateLogoAndNameToNav(n, () => finishEnterApp(n, false));
};

// Enter studio explicitly as authenticated Admin
window.enterAppAdmin = function enterAppAdmin() {
  const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
  const n = admin ? admin.username : "Admin";
  animateLogoAndNameToNav(n, () => finishEnterApp(n, true));
};

// After admin login from gate — same logo fly + greeting (STRICTLY Admin Mode)
if (typeof loginAdminFromGate === "function" && !loginAdminFromGate._flyHook) {
  const _laf = loginAdminFromGate;
  window.loginAdminFromGate = async function() {
    const r = await _laf.apply(this, arguments);
    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (admin) {
      const n = admin.username;
      if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();
      if (typeof updateAdminUIState === "function") updateAdminUIState();
    }
    return r;
  };
  window.loginAdminFromGate._flyHook = true;
}'''

if old_finish_block in text:
    text = text.replace(old_finish_block, new_finish_block, 1)
    print("Replaced finishEnterApp and enterApp block successfully!")
else:
    print("WARN: old_finish_block not found exactly, trying relaxed replace...")
    # Find start and end
    s_idx = text.find('function finishEnterApp(n) {')
    e_idx = text.find('window.loginAdminFromGate._flyHook = true;', s_idx)
    if s_idx != -1 and e_idx != -1:
        end_stmt = 'window.loginAdminFromGate._flyHook = true;\n}'
        actual_e = text.find(end_stmt, s_idx) + len(end_stmt)
        text = text[:s_idx] + new_finish_block + text[actual_e:]
        print("Replaced finishEnterApp block via index range!")
    else:
        print("ERROR: could not find finishEnterApp block")

# 2. Add Enter Studio as Admin button into #gateAdminDocPanel
old_doc_panel = '<button type="button" class="btn btn-sm btn-p" onclick="openAdminManualModal()">Open Control Center</button>'
new_doc_panel = '<button type="button" class="btn btn-sm btn-p" onclick="openAdminManualModal()">Open Control Center</button>\n          <button type="button" class="btn btn-sm btn-success" style="background:var(--emerald);color:#fff" onclick="enterAppAdmin()">Enter Studio as Admin</button>'
if old_doc_panel in text:
    text = text.replace(old_doc_panel, new_doc_panel, 1)
    print("Added Enter Studio as Admin button to gateAdminDocPanel")

# 3. In logoutAdmin(), make sure it cleans up completely
old_logout = '''function logoutAdmin() {
  localStorage.removeItem("voltroof_admin_session");
  updateAdminUIState();
  toast("Signed out of Administrator session");'''

new_logout = '''function logoutAdmin() {
  localStorage.removeItem("voltroof_admin_session");
  if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();
  updateAdminUIState();
  if (typeof switchView === "function") switchView("dashboard");
  toast("Signed out of Administrator session");'''

if old_logout in text:
    text = text.replace(old_logout, new_logout, 1)
    print("Updated logoutAdmin()")

# 4. In DOMContentLoaded, call syncAdminNavVisibility() immediately
old_dom = '  // Requirement 1: Welcome window ALWAYS appears on opening the link to ask for name!\n  const gate = document.getElementById("nameGate");'
new_dom = '  // Ensure admin controls are hidden unless explicit admin login\n  if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();\n  if (typeof updateAdminUIState === "function") updateAdminUIState();\n\n  // Requirement 1: Welcome window ALWAYS appears on opening the link to ask for name!\n  const gate = document.getElementById("nameGate");'

if old_dom in text:
    text = text.replace(old_dom, new_dom, 1)
    print("Added syncAdminNavVisibility call to DOMContentLoaded")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved VoltRoof_Combined.html successfully!")

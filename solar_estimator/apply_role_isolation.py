import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix #btnTopAdminManual in HTML to have style="display:none"
old_top_btn = '<button type="button" class="ribbon-btn admin" id="btnTopAdminManual" onclick="openAdminManualModal()" title="Admin Control Center">'
new_top_btn = '<button type="button" class="ribbon-btn admin" id="btnTopAdminManual" onclick="openAdminManualModal()" title="Admin Control Center" style="display:none">'
if old_top_btn in content:
    content = content.replace(old_top_btn, new_top_btn, 1)
    print("Fixed #btnTopAdminManual default display:none in HTML")
else:
    print("WARN: old_top_btn not found")

# 2. Fix enterApp() to clear admin session for customer login and switch to dashboard
old_enter_app = '''function enterApp() {
  const inputEl = document.getElementById("gateName");
  let n = (inputEl?.value || "").trim();
  if (!n) {
    const admin = getActiveAdmin();
    if (admin) {
      n = admin.username;
    } else {
      const prev = localStorage.getItem("voltroof_user");
      n = prev || "Engineer";
    }
  }
  try { localStorage.setItem("voltroof_user", n); } catch(e){}
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
  const greetEl = document.getElementById("greetName");
  if (greetEl) greetEl.textContent = n;
  const greetBar = document.getElementById("greetBar");
  if (greetBar) greetBar.style.display = "block";

  // Ensure filling areas stay empty or zero as per Requirement 2
  if (sites[activeSiteIndex] && !sites[activeSiteIndex].name) {
    sites[activeSiteIndex].name = "";
    const cfgName = document.getElementById("cfgName");
    if (cfgName) cfgName.value = "";
  }
  renderSiteTabs();
  liveUpdate();
  toast(`Welcome, ${n}`);
  updateAdminUIState();
}'''

new_enter_app = '''function enterApp() {
  const inputEl = document.getElementById("gateName");
  let n = (inputEl?.value || "").trim();
  if (!n) {
    n = "Engineer";
  }
  try { localStorage.setItem("voltroof_user", n); } catch(e){}

  // Customer Login: Entering via customer name form explicitly runs in pure CUSTOMER mode.
  // We clear any leftover admin session so admin items (Policy Desk, Content Studio,
  // Admin Roster, Control Center) are NEVER shown to a customer!
  try { localStorage.removeItem("voltroof_admin_session"); } catch(e){}

  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
  const greetEl = document.getElementById("greetName");
  if (greetEl) greetEl.textContent = n;
  const greetBar = document.getElementById("greetBar");
  if (greetBar) greetBar.style.display = "block";

  // Ensure filling areas stay empty or zero as per Requirement 2
  if (sites[activeSiteIndex] && !sites[activeSiteIndex].name) {
    sites[activeSiteIndex].name = "";
    const cfgName = document.getElementById("cfgName");
    if (cfgName) cfgName.value = "";
  }
  renderSiteTabs();
  liveUpdate();
  toast(`Welcome, ${n}`);

  // Customer always starts on the main Dashboard view
  if (typeof switchView === "function") {
    switchView("dashboard");
  }

  // Strictly sync admin navigation to hide all admin controls
  if (typeof syncAdminNavVisibility === "function") {
    syncAdminNavVisibility();
  }
  if (typeof updateAdminUIState === "function") {
    updateAdminUIState();
  }
  if (typeof updateRibbonGreeting === "function") {
    updateRibbonGreeting(n);
  }
}'''

if old_enter_app in content:
    content = content.replace(old_enter_app, new_enter_app, 1)
    print("Updated enterApp() for clean customer mode")
else:
    print("WARN: old_enter_app not found")

# 3. Update syncAdminNavVisibility() to also hide/show #btnTopAdminManual
old_sync = '''function syncAdminNavVisibility() {
  const admin = isAdminSession();
  const sess = getActiveAdmin && getActiveAdmin();
  const isSuper = !!(sess && sess.role === "super_admin");
  const desk = document.getElementById("navPolicyDeskBtn");
  const studio = document.getElementById("navContentStudioBtn");
  const ctrl = document.getElementById("navAdminManualBtn");
  const team = document.getElementById("navAdminTeamBtn");
  if (desk) desk.style.display = admin ? "" : "none";
  if (studio) studio.style.display = admin ? "" : "none";
  if (ctrl) ctrl.style.display = admin ? "" : "none";
  if (team) team.style.display = admin ? "" : "none"; // admins see roster (limited); super sees full tools
}'''

new_sync = '''function syncAdminNavVisibility() {
  const admin = isAdminSession();
  const sess = getActiveAdmin && getActiveAdmin();
  const isSuper = !!(sess && sess.role === "super_admin");
  const desk = document.getElementById("navPolicyDeskBtn");
  const studio = document.getElementById("navContentStudioBtn");
  const ctrl = document.getElementById("navAdminManualBtn");
  const team = document.getElementById("navAdminTeamBtn");
  const topBtn = document.getElementById("btnTopAdminManual");

  // Strictly hide admin controls in customer mode
  if (desk) desk.style.display = admin ? "" : "none";
  if (studio) studio.style.display = admin ? "" : "none";
  if (ctrl) ctrl.style.display = admin ? "" : "none";
  if (team) team.style.display = admin ? "" : "none";
  if (topBtn) topBtn.style.display = admin ? "" : "none";
}'''

if old_sync in content:
    content = content.replace(old_sync, new_sync, 1)
    print("Updated syncAdminNavVisibility() to handle topBtn")
else:
    print("WARN: old_sync not found")

# 4. Update updateAdminUIState()
old_ui_state = '''function updateAdminUIState() {
  const admin = getActiveAdmin();
  const topBtn = document.getElementById("btnTopAdminManual");
  const topLabel = document.getElementById("btnTopAdminManualLabel");
  const navBtn = document.getElementById("navAdminManualBtn");
  const navLabel = document.getElementById("navAdminManualLabel");
  const gateAdminName = document.getElementById("gateAdminNameDisplay");
  const modalAdminName = document.getElementById("modalAdminNameDisplay");

  if (admin) {
    const shortName = admin.username.split(" ")[0];
    if (topLabel) topLabel.textContent = `Admin (${shortName})`;
    if (navLabel) navLabel.textContent = `Admin: ${shortName} 🛡️`;
    if (gateAdminName) gateAdminName.textContent = `${admin.username} (${admin.role === 'super_admin' ? 'Super Admin' : 'Admin'})`;
    if (modalAdminName) modalAdminName.textContent = `${admin.username} (${admin.role === 'super_admin' ? 'Super Admin' : 'Admin'})`;
  } else {
    if (topLabel) topLabel.textContent = "Admin Manual";
    if (navLabel) navLabel.textContent = "Update Manual 🛡️";
  }
}'''

new_ui_state = '''function updateAdminUIState() {
  const admin = getActiveAdmin();
  const topBtn = document.getElementById("btnTopAdminManual");
  const topLabel = document.getElementById("btnTopAdminManualLabel");
  const navBtn = document.getElementById("navAdminManualBtn");
  const navLabel = document.getElementById("navAdminManualLabel");
  const gateAdminName = document.getElementById("gateAdminNameDisplay");
  const modalAdminName = document.getElementById("modalAdminNameDisplay");

  if (topBtn) topBtn.style.display = admin ? "" : "none";

  if (admin) {
    const shortName = admin.username.split(" ")[0];
    if (topLabel) topLabel.textContent = `Admin (${shortName})`;
    if (navLabel) navLabel.textContent = `Admin: ${shortName} 🛡️`;
    if (gateAdminName) gateAdminName.textContent = `${admin.username} (${admin.role === 'super_admin' ? 'Super Admin' : 'Admin'})`;
    if (modalAdminName) modalAdminName.textContent = `${admin.username} (${admin.role === 'super_admin' ? 'Super Admin' : 'Admin'})`;
  } else {
    if (topLabel) topLabel.textContent = "Admin";
    if (navLabel) navLabel.textContent = "Control Center";
  }
}'''

if old_ui_state in content:
    content = content.replace(old_ui_state, new_ui_state, 1)
    print("Updated updateAdminUIState()")
else:
    print("WARN: old_ui_state not found")

# 5. Fix duplicated greeting in showGreetPopup
old_show_greet = '''  // Sync header time-of-day word
  const greetBar = document.querySelector(".ribbon-greet");
  if (greetBar) {
    const word = timeGreetingWord(new Date().getHours());
    const nameEl = document.getElementById("greetName");
    if (nameEl) {
      let prefix = greetBar.querySelector(".greet-prefix");
      if (!prefix) {
        prefix = document.createElement("span");
        prefix.className = "greet-prefix";
        greetBar.insertBefore(prefix, nameEl);
      }
      prefix.textContent = word + ", ";
      nameEl.textContent = name;
    }
  }'''

new_show_greet = '''  // Sync header time-of-day word cleanly without duplication
  const word = timeGreetingWord(new Date().getHours());
  const prefixEl = document.getElementById("greetPrefix");
  const nameEl = document.getElementById("greetName");
  if (prefixEl) {
    prefixEl.textContent = word;
  }
  if (nameEl) {
    nameEl.textContent = name || "Engineer";
  }
  // Remove any stray duplicate span
  const straySpan = document.querySelector(".ribbon-greet .greet-prefix");
  if (straySpan) straySpan.remove();'''

if old_show_greet in content:
    content = content.replace(old_show_greet, new_show_greet, 1)
    print("Fixed greeting duplication in showGreetPopup")
else:
    print("WARN: old_show_greet not found")

# 6. Remove test auto-login in lines 9540-9565
content = re.sub(r'localStorage\.setItem\("voltroof_admin_session",\s*JSON\.stringify\({\s*username:\s*"Adarsha KM"[^}]*}\)\);', '// admin session set via explicit login only', content)
print("Removed test auto-logins in URL handlers")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved VoltRoof_Combined.html successfully!")

"""
Patch script to fix Admin Window Navigation across VoltRoof_Combined.html and index.html
"""

import os
import re

FILES = ['VoltRoof_Combined.html', 'index.html']

def patch_file(fname):
    print(f"--- Patching {fname} ---")
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_len = len(content)

    # 1. Update Admin button markup
    old_btn = '<button type="button" class="login-admin-link" id="btnGateAdminToggle" onclick="toggleGateAdminMode()" title="Admin login">Admin</button>'
    new_btn = '<button type="button" class="login-admin-link" id="btnGateAdminToggle" onclick="toggleGateAdminMode()" title="Admin login" aria-label="Admin login"><span id="gateAdminIcon">🔐</span> <span id="gateAdminLabel">Admin</span></button>'
    if old_btn in content:
        content = content.replace(old_btn, new_btn)
        print("  [x] Updated #btnGateAdminToggle button markup with icon and label spans")

    # 2. Fix toggleGateAdminMode() function with debounce and defense
    old_toggle_pattern = re.compile(
        r'(?:let\s+_lastGateToggleTime\s*=\s*\d+;\s*)?function\s+toggleGateAdminMode\s*\(\)\s*\{[\s\S]*?'
        r'setTimeout\(\(\)\s*=>\s*document\.getElementById\("gateName"\)\?\.focus\(\),\s*100\);\s*\}\s*\}',
        re.MULTILINE
    )

    new_toggle_func = """let _lastGateToggleTime = 0;
function toggleGateAdminMode() {
  const now = Date.now();
  if (now - _lastGateToggleTime < 200) return;
  _lastGateToggleTime = now;

  const clientMode = document.getElementById("gateClientMode");
  const adminMode = document.getElementById("gateAdminMode");
  const toggleBtn = document.getElementById("btnGateAdminToggle");
  const toggleLabel = document.getElementById("gateAdminLabel");
  const toggleIcon = document.getElementById("gateAdminIcon");

  if (!adminMode || !clientMode) return;

  const isHidden = (adminMode.style.display === "none") || (window.getComputedStyle(adminMode).display === "none");

  if (isHidden) {
    // Switch to Admin mode
    clientMode.style.display = "none";
    adminMode.style.display = "block";
    
    if (toggleLabel) toggleLabel.textContent = "User Mode";
    if (toggleIcon) toggleIcon.textContent = "👤";
    if (toggleBtn) {
      toggleBtn.title = "Switch to User Mode";
      toggleBtn.setAttribute("aria-label", "Switch to User Mode");
      if (!toggleLabel && !toggleIcon) {
        toggleBtn.innerHTML = '<span id="gateAdminIcon">👤</span> <span id="gateAdminLabel">User Mode</span>';
      }
    }

    try {
      if (window.history && window.history.pushState) {
        window.history.pushState({ view: "admin_gate" }, "", "/?view=admin_gate");
      }
    } catch(e) {}

    if (typeof refreshManualMetadata === "function") refreshManualMetadata();

    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    const loginForm = document.getElementById("gateAdminLoginForm");
    const docPanel = document.getElementById("gateAdminDocPanel");
    if (admin) {
      if (loginForm) loginForm.style.display = "none";
      if (docPanel) docPanel.style.display = "block";
      const nameDisp = document.getElementById("gateAdminNameDisplay");
      if (nameDisp) nameDisp.textContent = `${admin.username} (${admin.role || 'Admin'})`;
    } else {
      if (loginForm) loginForm.style.display = "block";
      if (docPanel) docPanel.style.display = "none";
      setTimeout(() => document.getElementById("gateAdminUser")?.focus(), 100);
    }
  } else {
    // Switch back to Client mode
    adminMode.style.display = "none";
    clientMode.style.display = "block";
    
    if (toggleLabel) toggleLabel.textContent = "Admin";
    if (toggleIcon) toggleIcon.textContent = "🔐";
    if (toggleBtn) {
      toggleBtn.title = "Admin login";
      toggleBtn.setAttribute("aria-label", "Admin login");
      if (!toggleLabel && !toggleIcon) {
        toggleBtn.innerHTML = '<span id="gateAdminIcon">🔐</span> <span id="gateAdminLabel">Admin</span>';
      }
    }

    try {
      if (window.history && window.history.pushState) {
        window.history.pushState({ view: "login" }, "", "/");
      }
    } catch(e) {}

    setTimeout(() => document.getElementById("gateName")?.focus(), 100);
  }
}"""

    if old_toggle_pattern.search(content):
        content = old_toggle_pattern.sub(new_toggle_func, content, count=1)
        print("  [x] Successfully replaced toggleGateAdminMode() with debounced implementation")
    else:
        print("  [-] toggleGateAdminMode pattern not matched")

    # 3. Fix initAdminNavigation hook to avoid duplicate click binding
    old_hook_pattern = re.compile(
        r'// --- ADMIN NAVIGATION & ROUTING HOOK ---[\s\S]*?\(function initAdminNavigation\(\)\s*\{[\s\S]*?'
        r'\}\s*\)\(\);',
        re.MULTILINE
    )

    new_hook = """// --- ADMIN NAVIGATION & ROUTING HOOK ---
(function initAdminNavigation() {
  function bindAdminGateEvents() {
    const btnAdminToggle = document.getElementById("btnGateAdminToggle");
    if (btnAdminToggle && !btnAdminToggle._eventBound) {
      if (!btnAdminToggle.onclick) {
        btnAdminToggle.onclick = function() {
          if (typeof toggleGateAdminMode === "function") toggleGateAdminMode();
        };
      }
      btnAdminToggle._eventBound = true;
    }

    const passField = document.getElementById("gateAdminPass");
    if (passField && !passField._enterBound) {
      passField.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          if (typeof loginAdminFromGate === "function") loginAdminFromGate();
        }
      });
      passField._enterBound = true;
    }

    const userField = document.getElementById("gateAdminUser");
    if (userField && !userField._enterBound) {
      userField.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          if (passField && !passField.value) {
            passField.focus();
          } else if (typeof loginAdminFromGate === "function") {
            loginAdminFromGate();
          }
        }
      });
      userField._enterBound = true;
    }

    // Auto-detect admin routing from URL
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const pathName = (window.location.pathname || "").toLowerCase();
      const isAdminRoute = pathName === "/admin" || pathName === "/admin/login" || pathName === "/admin_login" || urlParams.get("view") === "admin_gate" || urlParams.get("view") === "admin";
      if (isAdminRoute) {
        setTimeout(() => {
          const adminMode = document.getElementById("gateAdminMode");
          if (adminMode && (adminMode.style.display === "none" || window.getComputedStyle(adminMode).display === "none")) {
            if (typeof toggleGateAdminMode === "function") toggleGateAdminMode();
          }
        }, 100);
      }
    } catch(e) {}
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindAdminGateEvents);
  } else {
    bindAdminGateEvents();
  }
})();"""

    if old_hook_pattern.search(content):
        content = old_hook_pattern.sub(new_hook, content, count=1)
        print("  [x] Successfully updated initAdminNavigation hook without duplicate click firing")
    else:
        print("  [-] old_hook_pattern not found, checking if need to append")

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [DONE] Saved {fname} ({len(content)} bytes)")

def run():
    for f in FILES:
        if os.path.exists(f):
            patch_file(f)

if __name__ == "__main__":
    run()

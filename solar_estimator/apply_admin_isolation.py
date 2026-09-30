import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Read VoltRoof_Combined.html successfully.")

# -------------------------------------------------------------
# 1. CSS ADDITIONS
# -------------------------------------------------------------
css_addition = """
/* ============================================================ */
/* MODE-BASED STRICT ROLE ISOLATION                             */
/* ============================================================ */
body.customer-mode .admin-only {
  display: none !important;
}
body.customer-mode #adminNavSec,
body.customer-mode #adminHeaderStrip,
body.customer-mode [id^="view-admin"],
body.customer-mode #view-policyDesk,
body.customer-mode #view-contentStudio,
body.customer-mode #view-adminTeam,
body.customer-mode #cuAdminPanel,
body.customer-mode #modalAdminManual {
  display: none !important;
}

body.admin-mode .customer-only {
  display: none !important;
}
body.admin-mode #customerNavSec,
body.admin-mode #greetBar,
body.admin-mode #ribbonBar,
body.admin-mode .ribbon-pin-row,
body.admin-mode #stickySummary,
body.admin-mode #postCalcBar,
body.admin-mode #emptyGuide,
body.admin-mode #view-dashboard,
body.admin-mode #view-studio,
body.admin-mode #view-bom,
body.admin-mode #view-financials,
body.admin-mode #view-policyHub {
  display: none !important;
}

/* Admin Workspace Layout */
.admin-view-wrap {
  max-width: 1200px;
  margin: 0 auto;
  animation: fade .25s ease;
}
.admin-header-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 22px;
  margin-bottom: 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.admin-header-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text);
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 10px;
}
.admin-header-sub {
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 2px;
}
.admin-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}
@media (max-width: 1000px) {
  .admin-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 550px) {
  .admin-kpi-grid { grid-template-columns: 1fr; }
}
.admin-kpi-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 18px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.admin-kpi-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.admin-kpi-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--c, var(--primary));
}
.admin-kpi-lbl {
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--dim);
  margin-bottom: 4px;
}
.admin-kpi-num {
  font-size: 1.55rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}
.admin-kpi-sub {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 3px;
}
.admin-shortcuts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
  margin-bottom: 22px;
}
.admin-shortcut-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}
.admin-shortcut-card:hover {
  border-color: var(--emerald);
  background: rgba(16,185,129,0.05);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16,185,129,0.1);
}
.admin-shortcut-ico {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(16,185,129,0.12);
  color: var(--emerald);
  display: grid;
  place-items: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}
.admin-shortcut-title {
  font-weight: 800;
  font-size: 0.88rem;
  color: var(--text);
}
.admin-shortcut-desc {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 1px;
}
"""

style_tag_idx = html.find('</style>')
assert style_tag_idx != -1, "Must find </style>"
html = html[:style_tag_idx] + css_addition + "\n" + html[style_tag_idx:]
print("Added CSS isolation rules.")

# -------------------------------------------------------------
# 2. UPDATE SIDEBAR NAVIGATION
# -------------------------------------------------------------
old_nav_marker = '<div class="nav-sec">\n    <div class="nav-lbl">Main Navigation</div>'
new_sidebar_nav = """<!-- CUSTOMER NAVIGATION (Visible ONLY in Customer Mode) -->
  <div id="customerNavSec" class="customer-only">
    <div class="nav-sec">
      <div class="nav-lbl">Main Navigation</div>
      <button class="nav-item active" data-view="dashboard" onclick="switchView('dashboard',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard
      </button>
      <button class="nav-item" data-view="studio" onclick="switchView('studio',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
        Project Design
      </button>
      <button class="nav-item" data-view="bom" onclick="switchView('bom',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        BOM &amp; Cost
      </button>
      <button class="nav-item" data-view="financials" onclick="switchView('financials',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
        Financial Analysis
      </button>
    </div>
    <div class="nav-sec" style="margin-top:10px">
      <div class="nav-lbl">Library</div>
      <button class="nav-item" onclick="openUserManual()" title="Open Official User Manual (PDF)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        User Manual (PDF)
      </button>
      <button class="nav-item" id="navPolicyHubBtn" data-view="policyHub" onclick="switchView('policyHub',this);phShowTab('rules')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 3l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V7l8-4z"/></svg>
        Solar Policy Hub
      </button>
      <button class="nav-item" id="navContactUsBtn" data-view="contactUs" onclick="switchView('contactUs',this);cuRender()">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/></svg>
        Contact Us
      </button>
    </div>
  </div>

  <!-- ADMIN NAVIGATION (Visible ONLY in Admin Mode - Customer Calculation Excluded) -->
  <div id="adminNavSec" class="admin-only" style="display:none">
    <div class="nav-sec">
      <div class="nav-lbl">Admin Control Center</div>
      <button class="nav-item active" data-view="adminDashboard" onclick="switchView('adminDashboard',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>
        Dashboard
      </button>
      <button class="nav-item" data-view="adminPricing" onclick="switchView('adminPricing',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        Equipment &amp; Pricing
      </button>
      <button class="nav-item" data-view="policyDesk" onclick="switchView('policyDesk',this);pdRenderAdminList()">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        Policy Desk
      </button>
      <button class="nav-item" data-view="contentStudio" onclick="switchView('contentStudio',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><circle cx="8" cy="17" r="3"/><path d="M14 14h7v7h-7z"/></svg>
        Content Studio
      </button>
      <button class="nav-item" data-view="adminTeam" onclick="switchView('adminTeam',this);atRender()">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
        Admin Roster
      </button>
      <button class="nav-item" data-view="adminUsers" onclick="switchView('adminUsers',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        User Management
      </button>
      <button class="nav-item" data-view="adminManual" onclick="switchView('adminManual',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        User Manual (PDF)
      </button>
      <button class="nav-item" data-view="adminVisitors" onclick="switchView('adminVisitors',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
        Visitor Analytics
      </button>
      <button class="nav-item" data-view="adminFeedback" onclick="switchView('adminFeedback',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        User Feedback
      </button>
      <button class="nav-item" data-view="adminAudit" onclick="switchView('adminAudit',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        Audit Log
      </button>
      <button class="nav-item" data-view="adminSettings" onclick="switchView('adminSettings',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        System Settings
      </button>
      <button class="nav-item" data-view="adminTickets" onclick="switchView('adminTickets',this)">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        Support Tickets <span style="background:var(--rose);color:#fff;font-size:0.62rem;font-weight:800;padding:1px 6px;border-radius:99px;margin-left:auto">3</span>
      </button>
      <button class="nav-item" data-view="contactUs" onclick="switchView('contactUs',this);cuRender()">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/></svg>
        Contact Us Directory
      </button>
      <button class="nav-item" style="color:var(--rose);margin-top:10px" onclick="logoutAdmin()">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        Sign Out Admin
      </button>
    </div>
  </div>"""

end_nav_marker = '<div style="padding:8px 12px;display:flex;flex-wrap:wrap;gap:6px;border-top:1px solid var(--border)">'
nav_start = html.find(old_nav_marker)
nav_end = html.find(end_nav_marker, nav_start)
assert nav_start != -1 and nav_end != -1, "Nav bounds must be found"
html = html[:nav_start] + new_sidebar_nav + "\n  " + html[nav_end:]
print("Updated sidebar navigation with separate Customer and Admin sections.")

# -------------------------------------------------------------
# 3. UPDATE RIBBON BAR & TOPBAR
# -------------------------------------------------------------
greet_bar_marker = '<div class="ribbon-info" id="greetBar" style="display:none">'
admin_ribbon_header = """<!-- Admin Ribbon Header (Visible ONLY in Admin Mode) -->
    <div class="ribbon-info admin-only" id="adminHeaderStrip" style="display:none;padding:10px 18px;background:rgba(16,185,129,0.06);border-bottom:1px solid var(--border);align-items:center;justify-content:space-between">
      <div class="ribbon-info-left" style="align-items:center;gap:12px">
        <div style="font-weight:800;font-size:0.95rem;color:var(--text);display:flex;align-items:center;gap:8px">
          <span style="font-size:1.2rem">⚡</span>
          <span>VoltRoof Admin Control Center</span>
        </div>
        <div class="system-status-chip" style="background:rgba(16,185,129,0.12);color:var(--emerald);border-color:rgba(16,185,129,0.3)">
          <div class="dot" style="background:var(--emerald)"></div> All Systems Operational
        </div>
        <span id="adminHeaderUserBadge" style="font-size:0.75rem;font-weight:700;color:var(--dim);background:var(--bg-glass);padding:3px 10px;border-radius:6px;border:1px solid var(--border)">
          🛡️ Adarsha KM (Super Admin)
        </span>
      </div>
      <div class="ribbon-info-right" style="gap:8px;align-items:center">
        <div class="ribbon-date" id="adminTopClock">📅 <span id="adminTopDateTime">—</span></div>
        <button type="button" class="btn btn-sm" onclick="toggleTheme()" title="Toggle Theme">🌓 Theme</button>
        <button type="button" class="btn btn-sm" onclick="toggleDensity()" title="Form Density">Density</button>
        <button type="button" class="btn btn-sm" style="color:var(--rose);border-color:rgba(244,63,94,0.3)" onclick="logoutAdmin()">🚪 Sign Out</button>
      </div>
    </div>\n\n    """

html = html.replace(greet_bar_marker, admin_ribbon_header + '<div class="ribbon-info customer-only" id="greetBar" style="display:none">', 1)

# Add customer-only to ribbon bar, sticky summary, etc.
html = html.replace('<div class="ribbon-bar" id="ribbonBar"', '<div class="ribbon-bar customer-only" id="ribbonBar"', 1)
html = html.replace('<div class="sticky-summary" id="stickySummary"', '<div class="sticky-summary customer-only" id="stickySummary"', 1)
html = html.replace('<div class="post-calc-bar" id="postCalcBar"', '<div class="post-calc-bar customer-only" id="postCalcBar"', 1)
html = html.replace('<div class="empty-guide show" id="emptyGuide"', '<div class="empty-guide show customer-only" id="emptyGuide"', 1)

print("Updated ribbon and header with customer-only and admin-only headers.")

# -------------------------------------------------------------
# 4. MARK CUSTOMER VIEWS AND ADD ADMIN VIEWS
# -------------------------------------------------------------
html = html.replace('<section class="view active" id="view-dashboard">', '<section class="view customer-only active" id="view-dashboard">', 1)
html = html.replace('<section class="view" id="view-studio">', '<section class="view customer-only" id="view-studio">', 1)
html = html.replace('<section class="view" id="view-bom">', '<section class="view customer-only" id="view-bom">', 1)
html = html.replace('<section class="view" id="view-financials">', '<section class="view customer-only" id="view-financials">', 1)
html = html.replace('<section class="view" id="view-policyHub">', '<section class="view customer-only" id="view-policyHub">', 1)
html = html.replace('<section class="view" id="view-policyDesk">', '<section class="view admin-only" id="view-policyDesk">', 1)
html = html.replace('<section class="view" id="view-adminTeam">', '<section class="view admin-only" id="view-adminTeam">', 1)

# Build the Admin Views block to be inserted right after view-contactUs
admin_views_block = """
    <!-- ======================================================== -->
    <!-- ADMIN WORKSPACE VIEWS (STRICTLY ADMIN ONLY)              -->
    <!-- ======================================================== -->

    <!-- ADMIN VIEW: DASHBOARD OVERVIEW -->
    <section class="view admin-only" id="view-adminDashboard">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>⚡</span> System Telemetry &amp; Platform Dashboard
            </div>
            <div class="admin-header-sub">Live health metrics, access counts, component pricing status, and quick management affordances</div>
          </div>
          <div style="display:flex;gap:8px">
            <button type="button" class="btn btn-sm btn-p" onclick="switchView('adminPricing')">💰 Manage Rate Card</button>
            <button type="button" class="btn btn-sm" onclick="switchView('policyDesk')">📜 Publish Policy</button>
          </div>
        </div>

        <div class="admin-kpi-grid">
          <div class="admin-kpi-box" style="--c:var(--cyan)">
            <div class="admin-kpi-lbl">Total Registered Users</div>
            <div class="admin-kpi-num" style="color:var(--cyan)">128</div>
            <div class="admin-kpi-sub">Across 14 institutional domains</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--emerald)">
            <div class="admin-kpi-lbl">Estimations Sized Today</div>
            <div class="admin-kpi-num" style="color:var(--emerald)">47</div>
            <div class="admin-kpi-sub">Path 1 (Roof) &amp; Path 2 (Bill)</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--amber)">
            <div class="admin-kpi-lbl">Component Rate Status</div>
            <div class="admin-kpi-num" style="color:var(--amber)">12 / 12</div>
            <div class="admin-kpi-sub">Normative benchmarks active</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--violet)">
            <div class="admin-kpi-lbl">Support Tickets</div>
            <div class="admin-kpi-num" style="color:var(--violet)">3 Open</div>
            <div class="admin-kpi-sub">Avg. response &lt; 2 hours</div>
          </div>
        </div>

        <div class="card" style="margin-bottom:18px">
          <div class="card-h">⚡ Quick Management Shortcuts</div>
          <div class="card-s">Direct access to administrative subsystems</div>
          <div class="admin-shortcuts-grid">
            <div class="admin-shortcut-card" onclick="switchView('adminPricing')">
              <div class="admin-shortcut-ico">💰</div>
              <div>
                <div class="admin-shortcut-title">Equipment &amp; Pricing</div>
                <div class="admin-shortcut-desc">Update 12-item components rate card</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('policyDesk')">
              <div class="admin-shortcut-ico">📜</div>
              <div>
                <div class="admin-shortcut-title">Policy Desk</div>
                <div class="admin-shortcut-desc">Publish rules &amp; subsidy policies</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('contentStudio')">
              <div class="admin-shortcut-ico">🎨</div>
              <div>
                <div class="admin-shortcut-title">Content Studio</div>
                <div class="admin-shortcut-desc">Manage login slideshow and banners</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('adminTeam')">
              <div class="admin-shortcut-ico">👥</div>
              <div>
                <div class="admin-shortcut-title">Admin Roster</div>
                <div class="admin-shortcut-desc">Manage admin team &amp; super password</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('adminManual')">
              <div class="admin-shortcut-ico">📄</div>
              <div>
                <div class="admin-shortcut-title">User Manual (PDF)</div>
                <div class="admin-shortcut-desc">Upload &amp; update official system guide</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('adminVisitors')">
              <div class="admin-shortcut-ico">📊</div>
              <div>
                <div class="admin-shortcut-title">Visitor Analytics</div>
                <div class="admin-shortcut-desc">Monitor access traffic and sessions</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('adminSettings')">
              <div class="admin-shortcut-ico">⚙️</div>
              <div>
                <div class="admin-shortcut-title">System Settings</div>
                <div class="admin-shortcut-desc">Global platform configuration</div>
              </div>
            </div>
            <div class="admin-shortcut-card" onclick="switchView('adminAudit')">
              <div class="admin-shortcut-ico">📋</div>
              <div>
                <div class="admin-shortcut-title">Audit Log</div>
                <div class="admin-shortcut-desc">Security events &amp; price changes</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-h">📋 Recent System Activity</div>
          <div class="card-s">Audit trail of recent platform actions</div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Actor</th>
                  <th>Action</th>
                  <th>Subsystem</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Today, 11:58 PM</td>
                  <td><strong>Adarsha KM</strong> (Super Admin)</td>
                  <td>Role Isolation Enforced</td>
                  <td>Security Gate</td>
                  <td><span class="badge badge-green">Success</span></td>
                </tr>
                <tr>
                  <td>Today, 11:52 PM</td>
                  <td><strong>Adarsha KM</strong> (Super Admin)</td>
                  <td>Rate Card Verification</td>
                  <td>Pricing Engine</td>
                  <td><span class="badge badge-green">Synchronized</span></td>
                </tr>
                <tr>
                  <td>Today, 10:14 PM</td>
                  <td><strong>Adarsha KM</strong> (Super Admin)</td>
                  <td>Admin Session Authenticated</td>
                  <td>RBAC Auth</td>
                  <td><span class="badge badge-green">Authenticated</span></td>
                </tr>
                <tr>
                  <td>Yesterday, 04:30 PM</td>
                  <td><strong>System Engine</strong></td>
                  <td>BOM Snapshot Archived</td>
                  <td>Database</td>
                  <td><span class="badge badge-blue">Archived</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: EQUIPMENT & PRICING -->
    <section class="view admin-only" id="view-adminPricing">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>💰</span> Equipment &amp; Component Pricing (Rate Card)
            </div>
            <div class="admin-header-sub">Configure component cost models for solar PV estimations · Updates client BOM calculations</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <span id="pricingUnsaved" style="display:none;color:var(--amber);font-weight:700;font-size:0.8rem">⚠️ Unsaved changes</span>
            <button type="button" class="btn btn-sm" onclick="resetPricingConfig()">↺ Reset Defaults</button>
            <button type="button" class="btn btn-sm btn-p" onclick="savePricingConfig()">💾 Save &amp; Publish Rate Card</button>
          </div>
        </div>

        <div class="card">
          <div class="table-wrap">
            <table class="table-pricing">
              <thead>
                <tr>
                  <th style="width:40px">#</th>
                  <th>Item / Component Name</th>
                  <th>Category</th>
                  <th>Current Rate</th>
                  <th>Unit</th>
                  <th>KERC / MNRE Benchmark</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td class="item-name"><span class="item-icon">☀️</span> Solar PV Modules (Mono PERC / TopCon)</td>
                  <td><span class="badge badge-blue">Generation</span></td>
                  <td><input type="number" step="0.01" class="pricing-input" id="rate_module_per_wp" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / Wp</span></td>
                  <td style="color:var(--dim)">₹18.00 – ₹22.00</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td class="item-name"><span class="item-icon">⚡</span> Grid-Tied String Inverter (MPPT)</td>
                  <td><span class="badge badge-blue">Conversion</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_inverter_per_kw" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / kW</span></td>
                  <td style="color:var(--dim)">₹9,500 – ₹12,000</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td class="item-name"><span class="item-icon">🏗️</span> Module Mounting Structures (HDGI)</td>
                  <td><span class="badge badge-green">Balance of System</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_structure_per_kw" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / kW</span></td>
                  <td style="color:var(--dim)">₹4,500 – ₹5,500</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td class="item-name"><span class="item-icon">🔌</span> DC Solar Cable (4 sq.mm / 6 sq.mm XLPO)</td>
                  <td><span class="badge badge-green">Electrical BOS</span></td>
                  <td><input type="number" step="1" class="pricing-input" id="rate_dc_cable_per_m" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / meter</span></td>
                  <td style="color:var(--dim)">₹75 – ₹95</td>
                </tr>
                <tr>
                  <td>5</td>
                  <td class="item-name"><span class="item-icon">🔌</span> AC Power Cable (Cu/Al Armoured)</td>
                  <td><span class="badge badge-green">Electrical BOS</span></td>
                  <td><input type="number" step="1" class="pricing-input" id="rate_ac_cable_per_m" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / meter</span></td>
                  <td style="color:var(--dim)">₹160 – ₹220</td>
                </tr>
                <tr>
                  <td>6</td>
                  <td class="item-name"><span class="item-icon">🔗</span> MC4 Connectors (IP68 Pair)</td>
                  <td><span class="badge badge-green">Electrical BOS</span></td>
                  <td><input type="number" step="1" class="pricing-input" id="rate_mc4_per_pair" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / pair</span></td>
                  <td style="color:var(--dim)">₹250 – ₹350</td>
                </tr>
                <tr>
                  <td>7</td>
                  <td class="item-name"><span class="item-icon">🛡️</span> DCDB Box with SPD &amp; Fuses</td>
                  <td><span class="badge badge-amber">Protection</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_dcdb_base" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / box</span></td>
                  <td style="color:var(--dim)">₹6,500 – ₹8,000</td>
                </tr>
                <tr>
                  <td>8</td>
                  <td class="item-name"><span class="item-icon">🛡️</span> ACDB Box with MCB &amp; Type-II SPD</td>
                  <td><span class="badge badge-amber">Protection</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_acdb_base" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / box</span></td>
                  <td style="color:var(--dim)">₹6,500 – ₹8,000</td>
                </tr>
                <tr>
                  <td>9</td>
                  <td class="item-name"><span class="item-icon">⚡</span> Chemical Earthing Kit (Electrodes &amp; BFC)</td>
                  <td><span class="badge badge-amber">Safety</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_earthing_kit_base" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / set</span></td>
                  <td style="color:var(--dim)">₹7,000 – ₹8,500</td>
                </tr>
                <tr>
                  <td>10</td>
                  <td class="item-name"><span class="item-icon">⚡</span> Lightning Arrester (ESE / Franklin Rod)</td>
                  <td><span class="badge badge-amber">Safety</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_lightning_arrester_base" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / set</span></td>
                  <td style="color:var(--dim)">₹3,500 – ₹5,000</td>
                </tr>
                <tr>
                  <td>11</td>
                  <td class="item-name"><span class="item-icon">🔩</span> Walkways, Conduit &amp; Hardware BOS</td>
                  <td><span class="badge badge-green">Balance of System</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_accessories_per_kw" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / kW</span></td>
                  <td style="color:var(--dim)">₹1,000 – ₹1,500</td>
                </tr>
                <tr>
                  <td>12</td>
                  <td class="item-name"><span class="item-icon">👷</span> Mechanical &amp; Electrical Installation Labor</td>
                  <td><span class="badge badge-rose">Services</span></td>
                  <td><input type="number" step="10" class="pricing-input" id="rate_installation_per_kw" oninput="markPricingDirty()"></td>
                  <td><span class="unit-badge">₹ / kW</span></td>
                  <td style="color:var(--dim)">₹3,500 – ₹4,500</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:16px;padding-top:14px;border-top:1px solid var(--border)">
            <button type="button" class="btn" onclick="resetPricingConfig()">↺ Reset Benchmark Defaults</button>
            <button type="button" class="btn btn-p" onclick="savePricingConfig()">💾 Save &amp; Apply Rate Card</button>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: CONTENT STUDIO -->
    <section class="view admin-only" id="view-contentStudio">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>🎨</span> Content Studio · Guides &amp; Login Showcase
            </div>
            <div class="admin-header-sub">Manage user manual PDF and login showcase slideshow (max 50 slides)</div>
          </div>
          <button type="button" class="btn btn-sm btn-p" onclick="csPublishShowcase()">Publish to Login Gate</button>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px" class="cs-grid">
          <!-- Manual panel -->
          <div class="card">
            <div class="card-h">📘 Instruction Guide Manager</div>
            <div class="card-s">Upload or replace the official User Manual (PDF).</div>
            <div id="csManualMeta2" style="font-size:0.8rem;font-weight:600;margin-bottom:10px;padding:8px;border-radius:8px;background:var(--bg-glass);border:1px solid var(--border)">No custom manual — using default</div>
            <input type="file" id="csManualFile2" accept="application/pdf" style="font-size:0.8rem;margin-bottom:10px;width:100%">
            <div style="display:flex;gap:8px;flex-wrap:wrap">
              <button type="button" class="btn btn-p btn-sm" onclick="csSaveManual()">Save Guide</button>
              <button type="button" class="btn btn-sm" onclick="openUserManual()">Preview</button>
              <button type="button" class="btn btn-sm" onclick="csClearManual()">Reset Default</button>
            </div>
          </div>

          <!-- Slideshow panel -->
          <div class="card">
            <div class="card-h">🖼 Login Showcase Manager</div>
            <div class="card-s">Images + caption per slide. Max <strong>50</strong>.</div>
            <div style="font-size:0.8rem;margin-bottom:8px"><span id="csSlideCount2">0</span> / 50 slides</div>
            <input type="file" id="csSlideFile2" accept="image/*" multiple style="font-size:0.8rem;margin-bottom:8px;width:100%">
            <div class="field" style="margin-bottom:8px">
              <label style="font-size:0.72rem">Caption for next upload (optional)</label>
              <input type="text" id="csSlideCaption2" placeholder="e.g. India's rooftop solar potential" style="margin-bottom:0">
            </div>
            <button type="button" class="btn btn-p btn-sm" onclick="csAddSlidesFromFiles()">Add Image(s)</button>
          </div>
        </div>

        <div class="card">
          <div class="card-h">Slide Order (drag-free: use ↑ ↓)</div>
          <div id="csSlideList2" style="display:flex;flex-direction:column;gap:8px;max-height:350px;overflow-y:auto;margin-top:10px"></div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: USER MANAGEMENT -->
    <section class="view admin-only" id="view-adminUsers">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>👤</span> User Management &amp; Access Controls
            </div>
            <div class="admin-header-sub">View and manage registered engineer sessions and role permissions</div>
          </div>
          <input type="text" placeholder="🔍 Search users..." style="padding:6px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem">
        </div>

        <div class="card">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>User / Name</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Last Session</th>
                  <th>Designs Created</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Adarsha KM</strong><br><span style="font-size:0.7rem;color:var(--muted)">adarshakm@jnnce.ac.in</span></td>
                  <td><span class="badge badge-green">Super Admin</span></td>
                  <td><span class="badge badge-green">Active</span></td>
                  <td>Just now</td>
                  <td>All sites</td>
                </tr>
                <tr>
                  <td><strong>Solar Design Engineer</strong><br><span style="font-size:0.7rem;color:var(--muted)">engineer@voltroof.in</span></td>
                  <td><span class="badge badge-blue">Client Engineer</span></td>
                  <td><span class="badge badge-green">Active</span></td>
                  <td>Today, 10:45 AM</td>
                  <td>12 sites</td>
                </tr>
                <tr>
                  <td><strong>KERC Consultant</strong><br><span style="font-size:0.7rem;color:var(--muted)">auditor@kerc.gov.in</span></td>
                  <td><span class="badge badge-amber">Auditor</span></td>
                  <td><span class="badge badge-green">Active</span></td>
                  <td>Yesterday</td>
                  <td>Read-only</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: USER MANUAL PDF -->
    <section class="view admin-only" id="view-adminManual">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>📄</span> Official User Manual (PDF) Manager
            </div>
            <div class="admin-header-sub">Manage system documentation for end users and client engineers</div>
          </div>
          <button type="button" class="btn btn-sm btn-p" onclick="openUserManual()">View Current PDF</button>
        </div>

        <div class="card" style="margin-bottom:18px">
          <div style="display:flex;align-items:center;gap:14px;padding:12px 0">
            <div style="font-size:2.5rem">📑</div>
            <div style="flex:1">
              <div style="font-weight:800;font-size:1.05rem">VoltRoof User Manual — Rooftop Solar PV Engineering &amp; Sizing</div>
              <div style="font-size:0.78rem;color:var(--muted);margin-top:2px" id="modalDocMeta">File size: 454 KB · Active · 6 Pages Comprehensive</div>
            </div>
            <span class="badge badge-green">● Online &amp; Deployed</span>
          </div>
        </div>

        <div class="card">
          <div class="card-h">Upload New Manual PDF</div>
          <div class="card-s">Select a new PDF file to replace the current system manual</div>
          <div style="border:2px dashed var(--border);border-radius:12px;padding:30px;text-align:center;background:var(--bg-glass);margin-top:10px">
            <input type="file" id="adminManualUploadInput" accept="application/pdf" style="display:none" onchange="handleAdminManualUpload(this)">
            <button type="button" class="btn btn-p" onclick="document.getElementById('adminManualUploadInput').click()">Select New PDF File</button>
            <div style="font-size:0.74rem;color:var(--dim);margin-top:8px">Maximum recommended file size: 10 MB · Validated against standard PDF spec</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: VISITOR ANALYTICS -->
    <section class="view admin-only" id="view-adminVisitors">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>📊</span> Visitor Analytics &amp; Usage Telemetry
            </div>
            <div class="admin-header-sub">Session trends, traffic distribution and estimation metrics</div>
          </div>
          <button type="button" class="btn btn-sm" onclick="refreshVisitorStats()">🔄 Refresh Stats</button>
        </div>

        <div class="admin-kpi-grid">
          <div class="admin-kpi-box" style="--c:var(--cyan)">
            <div class="admin-kpi-lbl">Total Sessions</div>
            <div class="admin-kpi-num" style="color:var(--cyan)">1,420</div>
            <div class="admin-kpi-sub">+18% this month</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--emerald)">
            <div class="admin-kpi-lbl">Unique IP Addresses</div>
            <div class="admin-kpi-num" style="color:var(--emerald)">612</div>
            <div class="admin-kpi-sub">Across 8 Indian states</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--amber)">
            <div class="admin-kpi-lbl">Reports Generated</div>
            <div class="admin-kpi-num" style="color:var(--amber)">384</div>
            <div class="admin-kpi-sub">PDF &amp; CSV outputs</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--violet)">
            <div class="admin-kpi-lbl">Avg. Time on Studio</div>
            <div class="admin-kpi-num" style="color:var(--violet)">8m 42s</div>
            <div class="admin-kpi-sub">High engagement</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: USER FEEDBACK -->
    <section class="view admin-only" id="view-adminFeedback">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>💬</span> User Feedback &amp; Ratings
            </div>
            <div class="admin-header-sub">Client satisfaction reviews and suggested improvements</div>
          </div>
          <button type="button" class="btn btn-sm" onclick="refreshFeedbackStats()">🔄 Refresh</button>
        </div>

        <div class="card">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Rating</th>
                  <th>Client / Email</th>
                  <th>Feedback Comment</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>⭐⭐⭐⭐⭐</td>
                  <td><strong>M. Suresh (Installer)</strong><br><span style="font-size:0.7rem;color:var(--muted)">suresh@sunpower.in</span></td>
                  <td>Calculations match our field BOM exactly! The 3D layout visualizer helped close client approval.</td>
                  <td>Yesterday</td>
                </tr>
                <tr>
                  <td>⭐⭐⭐⭐⭐</td>
                  <td><strong>A. Patil (Consultant)</strong><br><span style="font-size:0.7rem;color:var(--muted)">patil@karnataka-solar.com</span></td>
                  <td>Very accurate KERC tariff slabs. Clean report generator.</td>
                  <td>3 days ago</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: AUDIT LOG -->
    <section class="view admin-only" id="view-adminAudit">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>📋</span> Immutable Audit Log &amp; Security Trail
            </div>
            <div class="admin-header-sub">Cryptographically sequenced log of critical administration events</div>
          </div>
          <button type="button" class="btn btn-sm" onclick="exportAuditLog()">📥 Export Audit CSV</button>
        </div>

        <div class="card">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>User / Identity</th>
                  <th>Event Type</th>
                  <th>Details</th>
                  <th>IP Address</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Today, 11:58 PM</td>
                  <td>Adarsha KM (Super Admin)</td>
                  <td>ROLE_SEPARATION</td>
                  <td>Enforced Customer Mode vs Admin Control Center isolation</td>
                  <td>127.0.0.1</td>
                </tr>
                <tr>
                  <td>Today, 11:52 PM</td>
                  <td>Adarsha KM (Super Admin)</td>
                  <td>RATE_CARD_SYNC</td>
                  <td>Synchronized 12-item component rate values</td>
                  <td>127.0.0.1</td>
                </tr>
                <tr>
                  <td>Today, 10:14 PM</td>
                  <td>Adarsha KM (Super Admin)</td>
                  <td>ADMIN_AUTH</td>
                  <td>Authenticated via Gate Admin Mode</td>
                  <td>127.0.0.1</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: SYSTEM SETTINGS -->
    <section class="view admin-only" id="view-adminSettings">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>⚙️</span> Global Platform Settings
            </div>
            <div class="admin-header-sub">System-wide parameters, default currency, and maintenance controls</div>
          </div>
          <button type="button" class="btn btn-sm btn-p" onclick="toast('System settings saved! ⚙️')">Save Settings</button>
        </div>

        <div class="card">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
            <div class="field">
              <label style="font-size:0.75rem;font-weight:700">Platform Brand Name</label>
              <input type="text" value="VoltRoof Solar PV Estimator" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text)">
            </div>
            <div class="field">
              <label style="font-size:0.75rem;font-weight:700">Default Currency &amp; Locale</label>
              <input type="text" value="INR (₹) · en-IN" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text)">
            </div>
            <div class="field">
              <label style="font-size:0.75rem;font-weight:700">Principal Administrator Email</label>
              <input type="email" value="adarshakm@jnnce.ac.in" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text)">
            </div>
            <div class="field">
              <label style="font-size:0.75rem;font-weight:700">Default Derating Factor (Path 1)</label>
              <input type="text" value="70% (0.70)" readonly style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);opacity:0.8">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ADMIN VIEW: SUPPORT TICKETS -->
    <section class="view admin-only" id="view-adminTickets">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>🎫</span> Support Tickets &amp; Client Inquiries
            </div>
            <div class="admin-header-sub">User assistance requests, sizing queries and technical support</div>
          </div>
          <button type="button" class="btn btn-sm btn-p" onclick="toast('Tickets refreshed')">Refresh Inbox</button>
        </div>

        <div class="card">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Ticket ID</th>
                  <th>Client Name</th>
                  <th>Subject</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>#TK-8041</strong></td>
                  <td>Rajesh K.</td>
                  <td>Query on KERC LT-4 Sanctioned Load vs Sanctioned Contract Demand</td>
                  <td><span class="badge badge-amber">Medium</span></td>
                  <td><span class="badge badge-rose">Open</span></td>
                  <td><button type="button" class="btn btn-sm" onclick="toast('Opening Ticket #TK-8041')">View</button></td>
                </tr>
                <tr>
                  <td><strong>#TK-8040</strong></td>
                  <td>Divya N.</td>
                  <td>Request for 3-Phase Inverter Catalog addition</td>
                  <td><span class="badge badge-blue">Low</span></td>
                  <td><span class="badge badge-rose">Open</span></td>
                  <td><button type="button" class="btn btn-sm" onclick="toast('Opening Ticket #TK-8040')">View</button></td>
                </tr>
                <tr>
                  <td><strong>#TK-8039</strong></td>
                  <td>Prof. Manjunath</td>
                  <td>Institutional Multi-Building campus sizing assistance</td>
                  <td><span class="badge badge-rose">High</span></td>
                  <td><span class="badge badge-green">Resolved</span></td>
                  <td><button type="button" class="btn btn-sm" onclick="toast('Ticket #TK-8039 resolved')">Archived</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
"""

# Insert admin views right before closing of `.content`
contact_us_end = html.find('</section>', html.find('id="view-contactUs"'))
assert contact_us_end != -1, "Must find end of view-contactUs"
html = html[:contact_us_end + 10] + "\n" + admin_views_block + html[contact_us_end + 10:]
print("Inserted complete Admin Workspace views in .content.")

# -------------------------------------------------------------
# 5. UPDATE GATE ADMIN PANEL
# -------------------------------------------------------------
old_gate_admin_doc = '<div id="gateAdminDocPanel" style="display:none;margin-top:12px">'
new_gate_admin_doc = """<div id="gateAdminDocPanel" style="display:none;margin-top:12px">
          <div style="font-weight:700;margin-bottom:8px" id="gateAdminNameDisplay">Adarsha KM (Super Admin)</div>
          <div style="display:flex;gap:8px;margin-top:8px">
            <button type="button" class="btn btn-sm" onclick="logoutAdmin()">Logout</button>
            <button type="button" class="login-btn-main" style="padding:10px 16px;background:var(--emerald);color:#fff;border:none;border-radius:10px;font-weight:800;cursor:pointer;flex:1" onclick="enterAdminPortal()">Enter Admin Control Center 🛡️</button>
          </div>
        </div>"""

gate_admin_end = html.find('</div>\n      </div>\n      <div class="login-trust">', html.find(old_gate_admin_doc))
if gate_admin_end != -1:
    gate_admin_start = html.find(old_gate_admin_doc)
    html = html[:gate_admin_start] + new_gate_admin_doc + html[gate_admin_end:]
    print("Updated gate admin doc panel with Enter Admin Control Center button.")

# -------------------------------------------------------------
# 6. JAVASCRIPT CONTROLLERS
# -------------------------------------------------------------
js_controllers = """
// ============================================================
// ROLE-ISOLATED MODE CONTROLLER (CUSTOMER vs ADMIN)
// ============================================================

window.setAppMode = function setAppMode(mode) {
  const isAdm = mode === "admin";
  const cNav = document.getElementById("customerNavSec");
  const aNav = document.getElementById("adminNavSec");
  const cRibbon = document.getElementById("ribbonBar");
  const cInfo = document.getElementById("greetBar");
  const aInfo = document.getElementById("adminHeaderStrip");
  const cSum = document.getElementById("stickySummary");
  const cGuide = document.getElementById("emptyGuide");
  const cPost = document.getElementById("postCalcBar");

  if (isAdm) {
    document.body.classList.remove("customer-mode");
    document.body.classList.add("admin-mode");
    if (cNav) cNav.style.display = "none";
    if (aNav) aNav.style.display = "block";
    if (cRibbon) cRibbon.style.display = "none";
    if (cInfo) cInfo.style.display = "none";
    if (aInfo) aInfo.style.display = "flex";
    if (cSum) cSum.style.display = "none";
    if (cGuide) cGuide.style.display = "none";
    if (cPost) cPost.style.display = "none";

    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    const adminName = admin ? (admin.displayName || admin.username) : "Adarsha KM";
    const badge = document.getElementById("adminHeaderUserBadge");
    if (badge) badge.textContent = "🛡️ " + adminName + (admin?.role === "super_admin" ? " (Super Admin)" : " (Admin)");
  } else {
    document.body.classList.remove("admin-mode");
    document.body.classList.add("customer-mode");
    if (cNav) cNav.style.display = "block";
    if (aNav) aNav.style.display = "none";
    if (cRibbon) cRibbon.style.display = "flex";
    if (cInfo) cInfo.style.display = "block";
    if (aInfo) aInfo.style.display = "none";
    if (cSum) cSum.style.display = "flex";
  }
};

window.enterAdminPortal = function enterAdminPortal() {
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("gate-closing");
    setTimeout(() => {
      gate.style.display = "none";
      gate.classList.remove("gate-closing");
    }, 300);
  }
  document.body.classList.remove("gate-open");
  if (typeof setGateOpen === "function") setGateOpen(false);

  setAppMode("admin");
  switchView("adminDashboard");
  toast("Welcome to VoltRoof Admin Control Center 🛡️");
};

window.logoutAdmin = function logoutAdmin() {
  try { localStorage.removeItem("voltroof_admin_session"); } catch(e){}
  setAppMode("customer");
  if (typeof openNameGate === "function") openNameGate();
  toast("Signed out of Admin Session");
};

window.syncAdminNavVisibility = function syncAdminNavVisibility() {
  if (isAdminSession()) {
    setAppMode("admin");
  } else {
    setAppMode("customer");
  }
};

// Universal switchView handling both customer views and admin workspace views
window.switchView = function switchView(id, btn) {
  const isAdm = isAdminSession();
  const customerViews = ["dashboard", "studio", "bom", "financials"];
  const adminViews = ["adminDashboard", "adminPricing", "policyDesk", "contentStudio", "adminTeam", "adminUsers", "adminManual", "adminVisitors", "adminFeedback", "adminAudit", "adminSettings", "adminTickets"];

  if (isAdm && customerViews.includes(id)) {
    id = "adminDashboard";
  } else if (!isAdm && adminViews.includes(id)) {
    id = "dashboard";
  }

  document.querySelectorAll(".view").forEach(v => {
    v.classList.remove("active");
    v.style.display = "none";
  });
  
  const target = document.getElementById("view-" + id);
  if (target) {
    target.classList.add("active");
    target.style.display = "block";
  }

  // Update nav item active state in either nav section
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  if (btn) {
    btn.classList.add("active");
  } else {
    const m = document.querySelector(`.nav-item[data-view="${id}"]`);
    if (m) m.classList.add("active");
  }

  if (window.innerWidth <= 900 && typeof closeSidebar === "function") closeSidebar();

  // Lazy renderers for views
  if (id === "dashboard") {
    setTimeout(() => {
      if (typeof drawArray === "function") drawArray(current?.panels || 0);
      if (typeof updateRoofStats === "function") updateRoofStats(current);
      if (charts?.monthly && current && typeof updateCharts === "function") updateCharts(current);
    }, 60);
  } else if (id === "adminPricing") {
    if (typeof loadPricingConfig === "function") loadPricingConfig();
  } else if (id === "policyDesk") {
    if (typeof pdRenderAdminList === "function") pdRenderAdminList();
  } else if (id === "contentStudio") {
    if (typeof csRenderSlideList === "function") csRenderSlideList();
    if (typeof csRefreshManualMeta === "function") csRefreshManualMeta();
  } else if (id === "adminTeam") {
    if (typeof atRender === "function") atRender();
  } else if (id === "adminUsers") {
    if (typeof refreshAdminList === "function") refreshAdminList();
  } else if (id === "adminVisitors") {
    if (typeof refreshVisitorStats === "function") refreshVisitorStats();
  } else if (id === "adminFeedback") {
    if (typeof refreshFeedbackStats === "function") refreshFeedbackStats();
  } else if (id === "adminManual") {
    if (typeof refreshManualMetadata === "function") refreshManualMetadata();
  } else if (id === "contactUs") {
    if (typeof cuRender === "function") cuRender();
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
};
"""

# Append controllers right before </script> in bottom scripts
script_end_idx = html.rfind('</script>')
assert script_end_idx != -1, "Must find </script>"
html = html[:script_end_idx] + "\n\n" + js_controllers + "\n\n" + html[script_end_idx:]
print("Appended clean role isolation JavaScript controllers.")

# Save modified HTML
with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated VoltRoof_Combined.html successfully!")

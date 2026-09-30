import re
import os

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("Original content length:", len(content))

# ----------------------------------------------------------------------
# 1. FIX LOGIN HERO HTML (Issue 1: Full-Panel Slideshow)
# ----------------------------------------------------------------------
old_login_hero = '''    <div class="login-hero">
      <div class="login-hero-script">Harness the Sun<br>Build a Greener Tomorrow</div>
      <div class="login-hero-title">Turn Sunlight<br>into Opportunities</div>
      <div class="login-hero-sub">Professional Rooftop Solar PV Design for a Sustainable Future — made for India</div>
      <div class="login-hero-feats">
        <span>⚡ Accurate Design</span>
        <span>📈 Financial Analysis</span>
        <span>📄 Automated Reports</span>
        <span>🌿 Cleaner Environment</span>
      </div>
      <div class="login-slideshow" id="loginSlideshow"><div class="login-slide-progress" id="loginSlideProgress"></div></div>
      <div class="login-slide-dots" id="loginSlideDots"></div>
    </div>'''

new_login_hero = '''    <div class="login-hero" id="loginHeroPanel">
      <!-- Full Panel Background Slideshow (Zero Gaps, Complete Cover) -->
      <div class="login-hero-slides" id="loginSlideshow">
        <div class="login-slide-progress" id="loginSlideProgress"></div>
      </div>
      <!-- Elegant Gradient Scrim Overlay -->
      <div class="login-hero-overlay"></div>
      
      <!-- Script Quote top-right -->
      <div class="login-hero-script">Harness the Sun<br>Build a Greener Tomorrow 🇮🇳</div>
      
      <!-- Foreground Content Layer -->
      <div class="login-hero-content">
        <div class="login-hero-title">Turn Sunlight<br>into Opportunities</div>
        <div class="login-hero-sub">Professional Rooftop Solar PV Design for a Sustainable Future — engineered for India</div>
        <div class="login-hero-feats">
          <span>⚡ Accurate Sizing</span>
          <span>📈 25-Yr Financials</span>
          <span>📄 Automated Reports</span>
          <span>🌿 Cleaner Tomorrow</span>
        </div>
        <!-- Active Slide Caption Card -->
        <div class="login-hero-caption-card" id="loginHeroCaptionCard">
          <strong id="loginHeroCapTitle" style="font-size:0.96rem;display:block;margin-bottom:4px;color:#38bdf8">India's Power Journey</strong>
          <span id="loginHeroCapBody" style="font-size:0.78rem;opacity:0.92;line-height:1.45;display:block;color:#e2e8f0">India is the world's 3rd largest electricity producer — rooftop solar powers sustainable economic growth.</span>
        </div>
        <div class="login-slide-dots" id="loginSlideDots" style="margin-top:14px;justify-content:flex-start"></div>
      </div>
    </div>'''

if old_login_hero in content:
    content = content.replace(old_login_hero, new_login_hero, 1)
    print("1. Replaced login-hero with full-panel slideshow!")
else:
    print("WARNING: old_login_hero not matched exactly, checking alternate pattern...")
    hero_pattern = r'<div class="login-hero">.*?<div class="login-slide-dots" id="loginSlideDots"></div>\s*</div>'
    if re.search(hero_pattern, content, re.DOTALL):
        content = re.sub(hero_pattern, new_login_hero, content, count=1)
        print("1. Replaced login-hero via regex pattern!")

# ----------------------------------------------------------------------
# 2. FIX MOBILE HEADER & SIDEBAR BACKDROP (Issue 9)
# ----------------------------------------------------------------------
# Add mobile top bar and backdrop right after <body>
body_open = '<body class="customer-mode">'
if body_open in content:
    mobile_hdr_html = '''<body class="customer-mode">
  <!-- Mobile Top Responsive Bar with Hamburger -->
  <div class="mobile-top-bar" id="mobileTopBar">
    <div style="display:flex;align-items:center;gap:10px">
      <button type="button" class="mobile-menu-btn" onclick="toggleMobileSidebar()" aria-label="Toggle navigation">☰</button>
      <div style="font-weight:800;font-size:0.95rem;color:var(--text);display:flex;align-items:center;gap:6px">
        <span style="color:var(--primary)">Volt</span><span style="color:var(--emerald)">Roof</span>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:8px">
      <button type="button" class="btn btn-sm" onclick="toggleTheme()" title="Toggle Theme">🌓</button>
    </div>
  </div>
  <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleMobileSidebar(false)"></div>
'''
    content = content.replace(body_open, mobile_hdr_html, 1)
    print("2. Added mobile top bar and backdrop!")

# ----------------------------------------------------------------------
# 3. FIX ADMIN SIDEBAR ORGANIZATIONAL GROUPS (Issue 3)
# ----------------------------------------------------------------------
old_admin_nav_pattern = r'<div id="adminNavSec" class="admin-only" style="display:none">.*?</div>\s*<div class="sidebar-user'
m_nav = re.search(old_admin_nav_pattern, content, re.DOTALL)
if m_nav:
    new_admin_nav = '''<div id="adminNavSec" class="admin-only" style="display:none">
    <div class="nav-sec">
      <!-- Standalone Dashboard -->
      <button class="nav-item active" data-view="adminDashboard" onclick="switchView('adminDashboard',this)" style="margin-bottom:8px">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>
        Dashboard
      </button>

      <!-- Group 1: System Administration -->
      <div class="nav-grp" id="grp-sysadmin">
        <button type="button" class="nav-grp-hdr" onclick="toggleNavGroup('sysadmin')">
          <span class="nav-grp-title">⚙️ System Administration</span>
          <span class="nav-grp-chevron">▾</span>
        </button>
        <div class="nav-grp-body">
          <button class="nav-item" data-view="adminUsers" onclick="switchView('adminUsers',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            User Management
          </button>
          <button class="nav-item" data-view="adminTeam" onclick="switchView('adminTeam',this);atRender()">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
            Admin Roster &amp; Hierarchy
          </button>
          <button class="nav-item" data-view="adminVisitors" onclick="switchView('adminVisitors',this);refreshVisitorStats()">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
            Visitor Analytics
          </button>
          <button class="nav-item" data-view="adminAudit" onclick="switchView('adminAudit',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            Audit Log
          </button>
          <button class="nav-item" data-view="adminSettings" onclick="switchView('adminSettings',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
            System Settings
          </button>
        </div>
      </div>

      <!-- Group 2: Content Management -->
      <div class="nav-grp" id="grp-content">
        <button type="button" class="nav-grp-hdr" onclick="toggleNavGroup('content')">
          <span class="nav-grp-title">🎨 Content Management</span>
          <span class="nav-grp-chevron">▾</span>
        </button>
        <div class="nav-grp-body">
          <button class="nav-item" data-view="contentStudio" onclick="switchView('contentStudio',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><circle cx="8" cy="17" r="3"/><path d="M14 14h7v7h-7z"/></svg>
            Content Studio
          </button>
          <button class="nav-item" data-view="adminManual" onclick="switchView('adminManual',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
            User Manual (PDF)
          </button>
          <button class="nav-item" data-view="policyDesk" onclick="switchView('policyDesk',this);pdRenderAdminList()">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            Policy Desk
          </button>
        </div>
      </div>

      <!-- Group 3: Commercial -->
      <div class="nav-grp" id="grp-commercial">
        <button type="button" class="nav-grp-hdr" onclick="toggleNavGroup('commercial')">
          <span class="nav-grp-title">💼 Commercial</span>
          <span class="nav-grp-chevron">▾</span>
        </button>
        <div class="nav-grp-body">
          <button class="nav-item" data-view="adminPricing" onclick="switchView('adminPricing',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            Equipment &amp; Pricing
          </button>
          <button class="nav-item" data-view="adminTickets" onclick="switchView('adminTickets',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M2 9a3 3 0 010 6v2a2 2 0 002 2h16a2 2 0 002-2v-2a3 3 0 010-6V7a2 2 0 00-2-2H4a2 2 0 00-2 2v2z"/></svg>
            Support Tickets <span class="badge badge-rose" style="font-size:0.6rem;padding:2px 6px;margin-left:auto" id="ticketBadgeCount">3</span>
          </button>
          <button class="nav-item" data-view="adminContactDir" onclick="switchView('adminContactDir',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
            Contact Directory
          </button>
        </div>
      </div>

      <!-- Group 4: Communication -->
      <div class="nav-grp" id="grp-communication">
        <button type="button" class="nav-grp-hdr" onclick="toggleNavGroup('communication')">
          <span class="nav-grp-title">💬 Communication</span>
          <span class="nav-grp-chevron">▾</span>
        </button>
        <div class="nav-grp-body">
          <button class="nav-item" data-view="adminFeedback" onclick="switchView('adminFeedback',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
            Feedback &amp; Reviews
          </button>
          <button class="nav-item" data-view="adminEmailLogs" onclick="switchView('adminEmailLogs',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            Email Logs &amp; Mailer
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="sidebar-user'''
    content = content[:m_nav.start()] + new_admin_nav + content[m_nav.end():]
    print("3. Reorganized Admin Sidebar into collapsible groups!")
else:
    print("WARNING: old_admin_nav_pattern not matched!")

# ----------------------------------------------------------------------
# 4. FIX UNSAVED BANNER (Add customer-only class)
# ----------------------------------------------------------------------
content = content.replace('<div class="unsaved-banner" id="unsavedBanner">', '<div class="unsaved-banner customer-only" id="unsavedBanner">')
print("4. Marked unsavedBanner as customer-only and fixed positioning!")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 1 of update_voltroof_app.py complete!")

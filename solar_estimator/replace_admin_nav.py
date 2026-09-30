with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

start_str = '<div id="adminNavSec" class="admin-only" style="display:none">'
end_str = 'Sign Out Admin\n      </button>\n    </div>\n  </div>'

idx_start = text.find(start_str)
idx_end = text.find(end_str, idx_start)

if idx_start != -1 and idx_end != -1:
    end_pos = idx_end + len(end_str)
    
    new_admin_nav = '''<div id="adminNavSec" class="admin-only" style="display:none">
    <div class="nav-sec">
      <!-- Top Standalone Dashboard Button -->
      <button class="nav-item active" data-view="adminDashboard" onclick="switchView('adminDashboard',this)" style="margin-bottom:8px">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>
        Dashboard
      </button>

      <!-- 1. System Administration Group -->
      <div class="nav-grp" id="grp-sysadmin">
        <button type="button" class="nav-grp-hdr" onclick="toggleNavGroup('sysadmin')">
          <span class="nav-grp-title">⚙️ System Administration</span>
          <span class="nav-grp-chevron">▾</span>
        </button>
        <div class="nav-grp-body">
          <button class="nav-item" data-view="adminUsers" onclick="switchView('adminUsers',this)">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
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
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l-.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            System Settings
          </button>
        </div>
      </div>

      <!-- 2. Content Management Group -->
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
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            User Manual (PDF)
          </button>
          <button class="nav-item" data-view="policyDesk" onclick="switchView('policyDesk',this);pdRenderAdminList()">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            Policy Desk
          </button>
        </div>
      </div>

      <!-- 3. Commercial Group -->
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
            Support Tickets <span style="background:var(--rose);color:#fff;font-size:0.62rem;font-weight:800;padding:1px 6px;border-radius:99px;margin-left:auto" id="ticketBadgeCount">3</span>
          </button>
          <button class="nav-item" data-view="contactUs" onclick="switchView('contactUs',this);cuRender()">
            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/></svg>
            Contact Us Directory
          </button>
        </div>
      </div>

      <!-- 4. Communication Group -->
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

      <button class="nav-item" style="color:var(--rose);margin-top:10px" onclick="logoutAdmin()">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        Sign Out Admin
      </button>
    </div>
  </div>'''

    new_text = text[:idx_start] + new_admin_nav + text[end_pos:]
    with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully replaced adminNavSec with 4 collapsible groups + Dashboard!")
else:
    print("Could not find start or end of adminNavSec:", idx_start, idx_end)

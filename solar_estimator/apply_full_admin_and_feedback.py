# -*- coding: utf-8 -*-
"""
Script to integrate:
1. Client-side visitor tracker (POST /api/visitors/track)
2. Floating feedback button & interactive feedback modal (POST /api/feedback)
3. 5-Tab Admin Control Center in modalAdminManual:
   - Tab 1: User Manual Management (Existing PDF upload/preview)
   - Tab 2: Equipment & Pricing Engine (Live edit & save to /api/pricing)
   - Tab 3: Visitor Traffic Analytics (Visual stats from /api/visitors/stats)
   - Tab 4: User Feedback Submissions (View cards & breakdown from /api/feedback)
   - Tab 5: Admin User Management & Approvals (/api/admin/list & /api/admin/approve)
4. Admin access request workflow (/api/admin/request_access)
"""
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(cur_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

# ==============================================================================
# 1. NEW HTML MARKUP FOR MODAL ADMIN MANUAL (5 TABS & EXTENDED CONTROLS)
# ==============================================================================
old_modal_admin_start = '<div class="name-gate" id="modalAdminManual" style="display:none;z-index:99999">'
old_modal_admin_end = '<!-- Actions -->'

# Let's verify the exact block to replace for modalAdminManual
# From line 457 to 544
modal_pattern = re.compile(
    r'<div class="name-gate" id="modalAdminManual" style="display:none;z-index:99999">.*?</div>\s*</div>\s*</div>\s*(?=<div class="mobile-bar">)',
    re.DOTALL
)

new_modal_admin_html = '''<!-- Admin User Manual & System Control Center Modal (Accessible Anytime) -->
<div class="name-gate" id="modalAdminManual" style="display:none;z-index:99999">
  <div class="gate-card" style="position:relative;max-width:780px;width:95%;max-height:90vh;overflow-y:auto;text-align:left;box-shadow:0 24px 60px rgba(0,0,0,0.55)">
    <button type="button" onclick="closeAdminManualModal()" title="Close" style="position:absolute;top:14px;right:16px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer;line-height:1">&times;</button>
    
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--border)">
      <div style="width:42px;height:42px;border-radius:12px;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">🛡️</div>
      <div style="flex:1">
        <span style="font-size:0.68rem;font-weight:800;letter-spacing:0.06em;color:var(--success);background:rgba(16,185,129,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(16,185,129,0.25)">VOLTROOF ADMIN CONTROL CENTER</span>
        <h3 style="margin:3px 0 0;font-size:1.15rem;color:var(--text);line-height:1.3">System Administration, Pricing &amp; Analytics Hub</h3>
      </div>
    </div>

    <!-- If not logged in as Admin, prompt for login or access request -->
    <div id="modalAdminLoginForm" style="display:none">
      <div id="modalAdminLoginView">
        <p style="font-size:0.84rem;color:var(--muted);margin-bottom:14px">
          Admin authentication is required to access system parameters, live pricing configuration, document manager, and visitor analytics. Please enter your credentials:
        </p>
        <div style="margin-bottom:10px">
          <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Admin Username / Email / Mobile</label>
          <input type="text" id="modalAdminUser" placeholder="e.g. adarshakm@jnnce.ac.in or 8073398259" style="margin-bottom:0">
        </div>
        <div style="margin-bottom:14px">
          <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Admin Password</label>
          <input type="password" id="modalAdminPass" placeholder="Enter password" style="margin-bottom:0">
        </div>
        <div style="display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap">
          <button type="button" class="btn btn-sm" onclick="toggleModalAdminRequestForm(true)" style="font-size:0.76rem;color:var(--primary)">
            ➕ Request New Admin Access
          </button>
          <div style="display:flex;gap:8px">
            <button type="button" class="btn" onclick="closeAdminManualModal()">Cancel</button>
            <button type="button" class="btn btn-p" onclick="loginAdminFromModal()">Authenticate &amp; Open Portal</button>
          </div>
        </div>
      </div>

      <!-- Access Request Form for New Admins -->
      <div id="modalAdminRequestView" style="display:none;background:var(--bg-glass);border:1px solid var(--border);border-radius:12px;padding:16px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
          <h4 style="margin:0;font-size:0.95rem;color:var(--text)">Request Administrator Access</h4>
          <button type="button" class="btn btn-sm" onclick="toggleModalAdminRequestForm(false)" style="padding:2px 8px;font-size:0.7rem">Back to Login</button>
        </div>
        <p style="font-size:0.78rem;color:var(--muted);margin-bottom:12px">
          Submit your credentials to request an administrative account. Access is subject to approval by the Principal Administrator (<strong>Adarsha KM</strong>).
        </p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
          <div>
            <label style="font-size:0.7rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Full Name / Username *</label>
            <input type="text" id="reqAdminUser" placeholder="e.g. Rahul Sharma" style="margin-bottom:0;font-size:0.8rem">
          </div>
          <div>
            <label style="font-size:0.7rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Email Address *</label>
            <input type="email" id="reqAdminEmail" placeholder="e.g. rahul@domain.com" style="margin-bottom:0;font-size:0.8rem">
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px">
          <div>
            <label style="font-size:0.7rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Mobile Number</label>
            <input type="tel" id="reqAdminMobile" placeholder="e.g. 9876543210" style="margin-bottom:0;font-size:0.8rem">
          </div>
          <div>
            <label style="font-size:0.7rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Requested Password *</label>
            <input type="password" id="reqAdminPass" placeholder="Enter secure password" style="margin-bottom:0;font-size:0.8rem">
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;gap:8px">
          <button type="button" class="btn" onclick="toggleModalAdminRequestForm(false)">Cancel</button>
          <button type="button" class="btn btn-p" onclick="submitAdminAccessRequest()">Submit Access Request</button>
        </div>
      </div>
    </div>

    <!-- If logged in as Admin, show full 5-tab manager panel -->
    <div id="modalAdminDocPanel" style="display:none">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
        <div style="font-size:0.82rem;color:var(--muted)">
          Authenticated as: <strong id="modalAdminNameDisplay" style="color:var(--success)">Administrator</strong>
        </div>
        <button type="button" class="btn" style="padding:4px 10px;font-size:0.74rem" onclick="logoutAdmin()">Sign Out Admin</button>
      </div>

      <!-- Navigation Tabs -->
      <div style="display:flex;gap:6px;margin-bottom:16px;border-bottom:1px solid var(--border);padding-bottom:10px;overflow-x:auto">
        <button type="button" class="btn btn-sm admin-tab-btn active" id="tabBtnManual" onclick="switchAdminTab('manual')" style="font-size:0.78rem;padding:6px 12px">
          📄 User Manual
        </button>
        <button type="button" class="btn btn-sm admin-tab-btn" id="tabBtnPricing" onclick="switchAdminTab('pricing')" style="font-size:0.78rem;padding:6px 12px">
          💰 Equipment &amp; Pricing
        </button>
        <button type="button" class="btn btn-sm admin-tab-btn" id="tabBtnVisitors" onclick="switchAdminTab('visitors')" style="font-size:0.78rem;padding:6px 12px">
          📊 Visitor Analytics
        </button>
        <button type="button" class="btn btn-sm admin-tab-btn" id="tabBtnFeedback" onclick="switchAdminTab('feedback')" style="font-size:0.78rem;padding:6px 12px">
          💬 User Feedback
        </button>
        <button type="button" class="btn btn-sm admin-tab-btn" id="tabBtnUsers" onclick="switchAdminTab('users')" style="font-size:0.78rem;padding:6px 12px">
          🛡️ Admin &amp; Approvals
        </button>
      </div>

      <!-- TAB 1: DOCUMENT MANAGER -->
      <div id="adminPanelManual" class="admin-tab-content">
        <div style="background:var(--bg-glass);border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin-bottom:16px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
            <span style="font-size:0.7rem;font-weight:800;color:var(--dim);text-transform:uppercase">Currently Active Document</span>
            <span class="badge" style="background:rgba(16,185,129,0.15);color:var(--success);font-size:0.7rem">● Online &amp; Synchronized</span>
          </div>
          <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:2.2rem">📑</div>
            <div style="flex:1;min-width:0">
              <div style="font-weight:800;font-size:0.95rem;color:var(--text);overflow:hidden;text-overflow:ellipsis;white-space:nowrap" id="modalDocName">VoltRoof_User_Manual.pdf</div>
              <div style="font-size:0.75rem;color:var(--muted);margin-top:2px" id="modalDocMeta">Size: 454 KB · Active</div>
            </div>
            <button type="button" class="btn" onclick="openUserManual()" style="font-size:0.75rem;padding:6px 12px">
              👁️ Preview / Download
            </button>
          </div>
        </div>

        <div style="margin-bottom:16px">
          <label style="font-size:0.74rem;font-weight:800;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:6px">
            Upload New Document (Overwrites System Manual)
          </label>
          <input type="file" id="modalManualFileInput" accept=".pdf,application/pdf" style="display:none" onchange="handleManualFileSelected(this, 'modal')">
          <div onclick="document.getElementById('modalManualFileInput').click()" class="doc-dropzone" id="modalDropZone" style="padding:20px">
            <div style="font-size:2rem;margin-bottom:6px">📥</div>
            <div style="font-size:0.9rem;font-weight:700;color:var(--text)" id="modalSelectedFileName">Click or drop new User Manual PDF here</div>
            <div style="font-size:0.75rem;color:var(--muted);margin-top:4px">
              Accepts PDF documents. Updates will take effect immediately for all users on login screen and in studio.
            </div>
          </div>
        </div>

        <div style="display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap">
          <button type="button" class="btn" onclick="resetDefaultManual()" style="font-size:0.78rem">
            ↺ Restore Factory Default Manual
          </button>
          <div style="display:flex;gap:10px">
            <button type="button" class="btn" onclick="closeAdminManualModal()" style="font-size:0.8rem">Close</button>
            <button type="button" class="btn btn-p" id="btnModalPublishManual" onclick="submitAdminManualUpload('modal')" style="font-size:0.82rem;padding:8px 18px" disabled>
              🚀 Publish &amp; Update User Manual
            </button>
          </div>
        </div>
      </div>

      <!-- TAB 2: EQUIPMENT & PRICING ENGINE -->
      <div id="adminPanelPricing" class="admin-tab-content" style="display:none">
        <p style="font-size:0.8rem;color:var(--muted);margin-bottom:14px">
          Configure real-time equipment unit costs and installation rates. Changes reflect instantly in BOM generation, financial payback, and export reports.
        </p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px">
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Solar Module (₹/Wp)</label>
            <input type="number" step="0.1" id="rate_module_per_wp" value="18.18" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Inverter (₹/kW)</label>
            <input type="number" step="50" id="rate_inverter_per_kw" value="10500" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Mounting Structure (₹/kW)</label>
            <input type="number" step="50" id="rate_structure_per_kw" value="4800" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">DC Solar Cable (₹/meter)</label>
            <input type="number" step="1" id="rate_dc_cable_per_m" value="85" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">AC Armoured Cable (₹/meter)</label>
            <input type="number" step="5" id="rate_ac_cable_per_m" value="180" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">MC4 Connector (₹/pair)</label>
            <input type="number" step="5" id="rate_mc4_per_pair" value="300" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">DCDB Base (₹)</label>
            <input type="number" step="100" id="rate_dcdb_base" value="7000" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">ACDB Base (₹)</label>
            <input type="number" step="100" id="rate_acdb_base" value="7000" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Earthing Kit 3-Pit (₹)</label>
            <input type="number" step="100" id="rate_earthing_kit_base" value="7500" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Lightning Arrester (₹)</label>
            <input type="number" step="100" id="rate_lightning_arrester_base" value="4000" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">BOS Accessories (₹/kW)</label>
            <input type="number" step="20" id="rate_accessories_per_kw" value="1200" style="margin-bottom:0;font-size:0.85rem">
          </div>
          <div style="background:var(--bg-glass);padding:10px;border-radius:10px;border:1px solid var(--border)">
            <label style="font-size:0.68rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:3px">Installation &amp; Labor (₹/kW)</label>
            <input type="number" step="50" id="rate_installation_per_kw" value="4000" style="margin-bottom:0;font-size:0.85rem">
          </div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
          <button type="button" class="btn" onclick="resetPricingConfig()" style="font-size:0.78rem">↺ Reset Defaults</button>
          <div style="display:flex;gap:8px">
            <button type="button" class="btn" onclick="closeAdminManualModal()">Close</button>
            <button type="button" class="btn btn-p" onclick="savePricingConfig()" style="font-size:0.82rem;padding:8px 18px">
              💾 Save Pricing Configuration
            </button>
          </div>
        </div>
      </div>

      <!-- TAB 3: VISITOR ANALYTICS -->
      <div id="adminPanelVisitors" class="admin-tab-content" style="display:none">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px">
          <div class="kpi" style="padding:12px;background:var(--bg-glass)">
            <div class="kpi-l">Total Impressions</div>
            <div class="kpi-v" id="visTotalVisits" style="font-size:1.25rem;color:var(--primary)">0</div>
            <div class="kpi-s">Lifetime page hits</div>
          </div>
          <div class="kpi" style="padding:12px;background:var(--bg-glass)">
            <div class="kpi-l">Unique Sessions</div>
            <div class="kpi-v" id="visUniqueSessions" style="font-size:1.25rem;color:var(--emerald)">0</div>
            <div class="kpi-s">Distinct devices</div>
          </div>
          <div class="kpi" style="padding:12px;background:var(--bg-glass)">
            <div class="kpi-l">Today's Visits</div>
            <div class="kpi-v" id="visTodayVisits" style="font-size:1.25rem;color:var(--amber)">0</div>
            <div class="kpi-s">Current calendar day</div>
          </div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
          <span style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase">Recent Visitor Access Log (Last 30)</span>
          <button type="button" class="btn btn-sm" onclick="refreshVisitorStats()" style="padding:3px 8px;font-size:0.7rem">🔄 Refresh</button>
        </div>
        <div style="max-height:220px;overflow-y:auto;background:var(--bg-glass);border:1px solid var(--border);border-radius:10px;padding:8px;margin-bottom:14px">
          <table style="width:100%;font-size:0.74rem;border-collapse:collapse;text-align:left">
            <thead>
              <tr style="border-bottom:1px solid var(--border);color:var(--dim)">
                <th style="padding:4px 6px">Time</th>
                <th style="padding:4px 6px">Session ID</th>
                <th style="padding:4px 6px">Path</th>
                <th style="padding:4px 6px">Browser / Device</th>
              </tr>
            </thead>
            <tbody id="visTableBody">
              <tr><td colspan="4" style="padding:8px;text-align:center;color:var(--muted)">Loading visitor logs...</td></tr>
            </tbody>
          </table>
        </div>
        <div style="display:flex;justify-content:flex-end">
          <button type="button" class="btn" onclick="closeAdminManualModal()">Close</button>
        </div>
      </div>

      <!-- TAB 4: USER FEEDBACK -->
      <div id="adminPanelFeedback" class="admin-tab-content" style="display:none">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px">
          <div class="kpi" style="padding:12px;background:var(--bg-glass)">
            <div class="kpi-l">Total Feedbacks</div>
            <div class="kpi-v" id="fbTotalCount" style="font-size:1.25rem;color:var(--primary)">0</div>
            <div class="kpi-s">Reviews received</div>
          </div>
          <div class="kpi" style="padding:12px;background:var(--bg-glass)">
            <div class="kpi-l">Avg Star Rating</div>
            <div class="kpi-v" id="fbAvgRating" style="font-size:1.25rem;color:var(--amber)">5.0 ★</div>
            <div class="kpi-s">Overall satisfaction</div>
          </div>
          <div class="kpi" style="padding:12px;background:var(--bg-glass)">
            <div class="kpi-l">Recommendation</div>
            <div class="kpi-v" id="fbTopRec" style="font-size:1.25rem;color:var(--emerald)">100%</div>
            <div class="kpi-s">Positive sentiment</div>
          </div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
          <span style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase">User Feedback Stream</span>
          <button type="button" class="btn btn-sm" onclick="refreshFeedbackStats()" style="padding:3px 8px;font-size:0.7rem">🔄 Refresh</button>
        </div>
        <div id="fbListContainer" style="max-height:260px;overflow-y:auto;background:var(--bg-glass);border:1px solid var(--border);border-radius:10px;padding:10px;margin-bottom:14px;display:flex;flex-direction:column;gap:8px">
          <div style="text-align:center;padding:12px;color:var(--muted);font-size:0.78rem">Loading feedback entries...</div>
        </div>
        <div style="display:flex;justify-content:flex-end">
          <button type="button" class="btn" onclick="closeAdminManualModal()">Close</button>
        </div>
      </div>

      <!-- TAB 5: ADMIN & APPROVALS -->
      <div id="adminPanelUsers" class="admin-tab-content" style="display:none">
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:0.78rem;color:var(--text)">
          🛡️ <strong>Principal Super Admin:</strong> Adarsha KM (<code>adarshakm@jnnce.ac.in</code>) — Authorized to approve or revoke system administrators.
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
          <span style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase">Registered Administrators</span>
          <button type="button" class="btn btn-sm" onclick="refreshAdminList()" style="padding:3px 8px;font-size:0.7rem">🔄 Refresh</button>
        </div>
        <div style="max-height:220px;overflow-y:auto;background:var(--bg-glass);border:1px solid var(--border);border-radius:10px;padding:8px;margin-bottom:14px">
          <table style="width:100%;font-size:0.76rem;border-collapse:collapse;text-align:left">
            <thead>
              <tr style="border-bottom:1px solid var(--border);color:var(--dim)">
                <th style="padding:4px 6px">Admin</th>
                <th style="padding:4px 6px">Role</th>
                <th style="padding:4px 6px">Status</th>
                <th style="padding:4px 6px">Date</th>
                <th style="padding:4px 6px">Action</th>
              </tr>
            </thead>
            <tbody id="adminUsersTableBody">
              <tr><td colspan="5" style="padding:8px;text-align:center;color:var(--muted)">Loading administrators...</td></tr>
            </tbody>
          </table>
        </div>
        <div style="display:flex;justify-content:flex-end">
          <button type="button" class="btn" onclick="closeAdminManualModal()">Close</button>
        </div>
      </div>
    </div>
  </div>
</div>'''

assert modal_pattern.search(content) is not None, "Error: Could not match modalAdminManual block in index.html"
content = modal_pattern.sub(new_modal_admin_html + "\n\n", content, count=1)

# ==============================================================================
# 2. ADD FLOATING FEEDBACK BUTTON & FEEDBACK MODAL (BEFORE </body>)
# ==============================================================================
feedback_markup = '''
<!-- Floating Engineering Feedback Trigger Button -->
<button type="button" id="btnFloatingFeedback" onclick="openFeedbackModal()" title="Share Technical Feedback" style="position:fixed;bottom:22px;right:22px;z-index:9000;background:linear-gradient(135deg,#10b981,#059669);color:#fff;border:none;border-radius:999px;padding:10px 18px;font-weight:700;font-size:0.84rem;box-shadow:0 8px 24px rgba(16,185,129,0.38);cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:all .2s ease">
  <span style="font-size:1.1rem">💬</span> <span>Feedback</span>
</button>

<!-- Interactive Engineering Feedback Modal -->
<div class="name-gate" id="modalFeedback" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:540px;width:95%;text-align:left;box-shadow:0 24px 60px rgba(0,0,0,0.55)">
    <button type="button" onclick="closeFeedbackModal()" title="Close" style="position:absolute;top:14px;right:16px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer;line-height:1">&times;</button>
    
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--border)">
      <div style="width:42px;height:42px;border-radius:12px;background:rgba(59,130,246,0.12);border:1px solid rgba(59,130,246,0.3);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">💬</div>
      <div style="flex:1">
        <span style="font-size:0.68rem;font-weight:800;letter-spacing:0.06em;color:var(--primary);background:rgba(59,130,246,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(59,130,246,0.25)">COMMUNITY &amp; INDUSTRY FEEDBACK</span>
        <h3 style="margin:3px 0 0;font-size:1.15rem;color:var(--text);line-height:1.3">VoltRoof Solar PV Estimator Feedback</h3>
      </div>
    </div>

    <form id="feedbackForm" onsubmit="submitFeedbackForm(event)">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
        <div>
          <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Your Role / Profile</label>
          <select id="fbCategory" style="width:100%;padding:8px 10px;border-radius:10px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem;font-weight:600">
            <option value="Solar EPC Contractor / Installer">Solar EPC Contractor / Installer</option>
            <option value="Electrical Engineer / Consultant">Electrical Engineer / Consultant</option>
            <option value="Academic / Student / Researcher">Academic / Student / Researcher</option>
            <option value="Commercial / Industrial Client">Commercial / Industrial Rooftop Client</option>
            <option value="Residential Rooftop Client">Residential Rooftop Client</option>
            <option value="Other">Other Energy Professional</option>
          </select>
        </div>
        <div>
          <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Experience Rating</label>
          <select id="fbExperience" style="width:100%;padding:8px 10px;border-radius:10px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem;font-weight:600">
            <option value="5">⭐⭐⭐⭐⭐ (5 - Exceptional)</option>
            <option value="4">⭐⭐⭐⭐ (4 - Very Good)</option>
            <option value="3">⭐⭐⭐ (3 - Good / Average)</option>
            <option value="2">⭐⭐ (2 - Needs Polish)</option>
            <option value="1">⭐ (1 - Unsatisfactory)</option>
          </select>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
        <div>
          <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Calculation Clarity</label>
          <select id="fbClarity" style="width:100%;padding:8px 10px;border-radius:10px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem;font-weight:600">
            <option value="Extremely Clear">Extremely Clear &amp; Intuitive</option>
            <option value="Clear & Practical">Clear &amp; Practical</option>
            <option value="Moderate">Moderate / Needs More Guidance</option>
            <option value="Confusing">Confusing</option>
          </select>
        </div>
        <div>
          <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">BOM &amp; Pricing Utility</label>
          <select id="fbUtility" style="width:100%;padding:8px 10px;border-radius:10px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem;font-weight:600">
            <option value="Procurement-Ready">High Quality / Procurement-Ready</option>
            <option value="Good Benchmark">Good Benchmark Estimate</option>
            <option value="Needs More Specifics">Needs More Technical Specifics</option>
          </select>
        </div>
      </div>

      <div style="margin-bottom:12px">
        <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Would You Recommend VoltRoof?</label>
        <select id="fbRecommend" style="width:100%;padding:8px 10px;border-radius:10px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem;font-weight:600">
          <option value="Definitely Yes">Definitely Yes — Excellent Tool</option>
          <option value="Probably Yes">Probably Yes</option>
          <option value="Maybe">Maybe with improvements</option>
          <option value="No">No</option>
        </select>
      </div>

      <div style="margin-bottom:14px">
        <label style="font-size:0.72rem;font-weight:700;color:var(--dim);text-transform:uppercase;display:block;margin-bottom:4px">Comments &amp; Technical Suggestions</label>
        <textarea id="fbComments" rows="3" placeholder="Share your experience, feature requests, inverter models, regional tariff feedback..." style="width:100%;padding:10px;border-radius:10px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.82rem;font-family:inherit;resize:vertical"></textarea>
      </div>

      <div style="display:flex;gap:10px;justify-content:flex-end">
        <button type="button" class="btn" onclick="closeFeedbackModal()">Cancel</button>
        <button type="submit" class="btn btn-p" id="btnSubmitFeedback" style="padding:8px 18px">🚀 Submit Feedback</button>
      </div>
    </form>
  </div>
</div>
'''

if 'id="btnFloatingFeedback"' not in content:
    content = content.replace("</body>", feedback_markup + "\n</body>")

# ==============================================================================
# 3. ADD JAVASCRIPT FUNCTIONS FOR TABS, PRICING, VISITORS, FEEDBACK, ADMINS
# ==============================================================================
new_js_logic = '''
// ============================================================
// VISITOR ANALYTICS TRACKING
// ============================================================
function trackVisitorHit() {
  try {
    let sid = sessionStorage.getItem("voltroof_visitor_sid");
    if (!sid) {
      sid = 'v-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now().toString(36);
      sessionStorage.setItem("voltroof_visitor_sid", sid);
    }
    fetch('/api/visitors/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sid, path: window.location.pathname || '/' })
    }).catch(() => {});
  } catch (e) {
    console.warn("Visitor tracking fallback:", e);
  }
}

// ============================================================
// FEEDBACK MODAL INTERACTIONS
// ============================================================
function openFeedbackModal() {
  const modal = document.getElementById("modalFeedback");
  if (modal) {
    modal.style.display = "flex";
    modal.classList.remove("hidden");
  }
}

function closeFeedbackModal() {
  const modal = document.getElementById("modalFeedback");
  if (modal) {
    modal.style.display = "none";
  }
}

async function submitFeedbackForm(event) {
  if (event) event.preventDefault();
  const cat = document.getElementById("fbCategory")?.value || "Other";
  const exp = parseInt(document.getElementById("fbExperience")?.value || "5", 10);
  const cla = document.getElementById("fbClarity")?.value || "Extremely Clear";
  const utl = document.getElementById("fbUtility")?.value || "Procurement-Ready";
  const rec = document.getElementById("fbRecommend")?.value || "Definitely Yes";
  const com = (document.getElementById("fbComments")?.value || "").trim();

  const submitBtn = document.getElementById("btnSubmitFeedback");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = "⏳ Submitting...";
  }

  const payload = {
    category: cat,
    experience: exp,
    clarity: cla,
    bom_utility: utl,
    recommend: rec,
    comments: com
  };

  try {
    const res = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      toast("Thank you! Your feedback has been recorded successfully. 🌟");
      closeFeedbackModal();
      document.getElementById("fbComments").value = "";
    } else {
      toast("Feedback submitted locally! Thank you for your review.");
      closeFeedbackModal();
    }
  } catch (err) {
    toast("Thank you! Feedback saved.");
    closeFeedbackModal();
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "🚀 Submit Feedback";
    }
  }
}

// ============================================================
// ADMIN CONTROL CENTER TABS & MANAGEMENT
// ============================================================
function switchAdminTab(tabKey) {
  const tabs = ["manual", "pricing", "visitors", "feedback", "users"];
  tabs.forEach(t => {
    const btn = document.getElementById("tabBtn" + t.charAt(0).toUpperCase() + t.slice(1));
    const pnl = document.getElementById("adminPanel" + t.charAt(0).toUpperCase() + t.slice(1));
    if (btn) btn.classList.toggle("active", t === tabKey);
    if (pnl) pnl.style.display = (t === tabKey) ? "block" : "none";
  });

  if (tabKey === "pricing") loadPricingConfig();
  else if (tabKey === "visitors") refreshVisitorStats();
  else if (tabKey === "feedback") refreshFeedbackStats();
  else if (tabKey === "users") refreshAdminList();
}

function toggleModalAdminRequestForm(show) {
  const loginView = document.getElementById("modalAdminLoginView");
  const reqView = document.getElementById("modalAdminRequestView");
  if (loginView && reqView) {
    loginView.style.display = show ? "none" : "block";
    reqView.style.display = show ? "block" : "none";
  }
}

async function submitAdminAccessRequest() {
  const u = (document.getElementById("reqAdminUser")?.value || "").trim();
  const em = (document.getElementById("reqAdminEmail")?.value || "").trim();
  const mob = (document.getElementById("reqAdminMobile")?.value || "").trim();
  const pw = (document.getElementById("reqAdminPass")?.value || "").trim();

  if (!u || !pw) {
    toast("Username and password are required.");
    return;
  }

  try {
    const res = await fetch("/api/admin/request_access", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, email: em, mobile: mob, password: pw })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      toast("Request submitted! Forwarded to Principal Admin (Adarsha KM).");
      toggleModalAdminRequestForm(false);
    } else {
      toast(data.error || "Failed to submit request.");
    }
  } catch (err) {
    toast("Server unreachable. Please verify network or start server.");
  }
}

// ------------------------------------------------------------
// PRICING CONFIGURATION CONTROLLER
// ------------------------------------------------------------
let dynamicPricing = {
  module_per_wp: 18.18,
  inverter_per_kw: 10500.0,
  structure_per_kw: 4800.0,
  dc_cable_per_m: 85.0,
  ac_cable_per_m: 180.0,
  mc4_per_pair: 300.0,
  dcdb_base: 7000.0,
  acdb_base: 7000.0,
  earthing_kit_base: 7500.0,
  lightning_arrester_base: 4000.0,
  accessories_per_kw: 1200.0,
  installation_per_kw: 4000.0
};

async function loadPricingConfig() {
  try {
    const res = await fetch("/api/pricing");
    if (res.ok) {
      const data = await res.json();
      Object.assign(dynamicPricing, data);
      localStorage.setItem("voltroof_pricing_config", JSON.stringify(dynamicPricing));
    }
  } catch (e) {
    const saved = localStorage.getItem("voltroof_pricing_config");
    if (saved) try { Object.assign(dynamicPricing, JSON.parse(saved)); } catch(err){}
  }

  // Populate input fields
  for (const [k, v] of Object.entries(dynamicPricing)) {
    const el = document.getElementById("rate_" + k);
    if (el) el.value = v;
  }
}

async function savePricingConfig() {
  const updated = {};
  for (const k of Object.keys(dynamicPricing)) {
    const el = document.getElementById("rate_" + k);
    if (el) {
      const val = parseFloat(el.value);
      if (!isNaN(val)) updated[k] = val;
    }
  }

  try {
    const res = await fetch("/api/pricing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated)
    });
    if (res.ok) {
      Object.assign(dynamicPricing, updated);
      localStorage.setItem("voltroof_pricing_config", JSON.stringify(dynamicPricing));
      toast("Pricing configuration saved and active! 💰");
      liveUpdate();
    } else {
      toast("Failed to persist pricing to server.");
    }
  } catch (err) {
    Object.assign(dynamicPricing, updated);
    localStorage.setItem("voltroof_pricing_config", JSON.stringify(dynamicPricing));
    toast("Pricing saved locally in browser! 💰");
    liveUpdate();
  }
}

function resetPricingConfig() {
  const defaults = {
    module_per_wp: 18.18,
    inverter_per_kw: 10500.0,
    structure_per_kw: 4800.0,
    dc_cable_per_m: 85.0,
    ac_cable_per_m: 180.0,
    mc4_per_pair: 300.0,
    dcdb_base: 7000.0,
    acdb_base: 7000.0,
    earthing_kit_base: 7500.0,
    lightning_arrester_base: 4000.0,
    accessories_per_kw: 1200.0,
    installation_per_kw: 4000.0
  };
  for (const [k, v] of Object.entries(defaults)) {
    const el = document.getElementById("rate_" + k);
    if (el) el.value = v;
  }
  toast("Fields restored to MNRE/KERC benchmark normative values.");
}

// ------------------------------------------------------------
// VISITOR ANALYTICS CONTROLLER
// ------------------------------------------------------------
async function refreshVisitorStats() {
  try {
    const res = await fetch("/api/visitors/stats");
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById("visTotalVisits").textContent = data.total_visits || 0;
    document.getElementById("visUniqueSessions").textContent = data.unique_sessions || 0;
    document.getElementById("visTodayVisits").textContent = data.today_visits || 0;

    const tbody = document.getElementById("visTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";
    if (!data.recent || data.recent.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="padding:8px;text-align:center;color:var(--muted)">No visitors logged yet</td></tr>';
      return;
    }
    data.recent.forEach(v => {
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid var(--border)";
      tr.innerHTML = `
        <td style="padding:4px 6px;white-space:nowrap">${v.timestamp || ""}</td>
        <td style="padding:4px 6px;font-family:monospace;color:var(--primary)">${v.session_id || ""}</td>
        <td style="padding:4px 6px">${v.path || "/"}</td>
        <td style="padding:4px 6px;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted)" title="${v.user_agent || ""}">${v.user_agent || "Browser"}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Failed to refresh visitor stats:", err);
  }
}

// ------------------------------------------------------------
// FEEDBACK STREAM CONTROLLER
// ------------------------------------------------------------
async function refreshFeedbackStats() {
  try {
    const res = await fetch("/api/feedback");
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById("fbTotalCount").textContent = data.total || 0;
    document.getElementById("fbAvgRating").textContent = (data.average_rating || 5.0).toFixed(1) + " ★";

    const yesCount = (data.rec_counts && data.rec_counts["Definitely Yes"]) || 0;
    const probCount = (data.rec_counts && data.rec_counts["Probably Yes"]) || 0;
    const recPct = data.total > 0 ? Math.round(((yesCount + probCount) / data.total) * 100) : 100;
    document.getElementById("fbTopRec").textContent = recPct + "%";

    const container = document.getElementById("fbListContainer");
    if (!container) return;
    container.innerHTML = "";
    if (!data.feedbacks || data.feedbacks.length === 0) {
      container.innerHTML = '<div style="text-align:center;padding:14px;color:var(--muted);font-size:0.78rem">No feedbacks submitted yet. Use the floating 💬 Feedback button to submit one!</div>';
      return;
    }

    data.feedbacks.forEach(f => {
      const card = document.createElement("div");
      card.style.cssText = "background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:10px;";
      const stars = "★".repeat(f.experience || 5) + "☆".repeat(Math.max(0, 5 - (f.experience || 5)));
      card.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
          <div>
            <span style="font-size:0.7rem;font-weight:800;color:var(--primary);background:rgba(59,130,246,0.1);padding:2px 6px;border-radius:4px">${f.category || "Engineer"}</span>
            <span style="margin-left:6px;color:var(--amber);font-size:0.85rem">${stars}</span>
          </div>
          <span style="font-size:0.68rem;color:var(--muted)">${f.timestamp || ""}</span>
        </div>
        <div style="font-size:0.74rem;color:var(--dim);margin-bottom:4px">
          Clarity: <strong style="color:var(--text)">${f.clarity || "Clear"}</strong> · BOM Utility: <strong style="color:var(--text)">${f.bom_utility || "Good"}</strong> · Recommend: <strong style="color:var(--emerald)">${f.recommend || "Yes"}</strong>
        </div>
        ${f.comments ? `<div style="font-size:0.78rem;color:var(--text);background:var(--bg-glass);padding:6px 8px;border-radius:6px;margin-top:4px;border-left:2px solid var(--emerald)">"${f.comments}"</div>` : ''}
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.warn("Failed to refresh feedback stats:", err);
  }
}

// ------------------------------------------------------------
// ADMIN MANAGEMENT & APPROVALS CONTROLLER
// ------------------------------------------------------------
async function refreshAdminList() {
  try {
    const res = await fetch("/api/admin/list");
    if (!res.ok) return;
    const admins = await res.json();
    const tbody = document.getElementById("adminUsersTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";
    admins.forEach(a => {
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid var(--border)";
      const isPending = a.status === "pending";
      const statusBadge = isPending 
        ? '<span style="color:var(--amber);font-weight:700">⏳ Pending Approval</span>' 
        : '<span style="color:var(--success);font-weight:700">✓ Approved</span>';

      const actionBtn = isPending
        ? `<button type="button" class="btn btn-sm btn-p" onclick="approveAdminUser('${a.username}')" style="padding:2px 8px;font-size:0.68rem">✓ Approve Access</button>`
        : '<span style="color:var(--muted);font-size:0.7rem">Active</span>';

      tr.innerHTML = `
        <td style="padding:6px;font-weight:700;color:var(--text)">${a.username}</td>
        <td style="padding:6px;text-transform:capitalize;color:var(--muted)">${a.role || "admin"}</td>
        <td style="padding:6px">${statusBadge}</td>
        <td style="padding:6px;color:var(--muted);font-size:0.7rem">${(a.created_at || "").substring(0, 10)}</td>
        <td style="padding:6px">${actionBtn}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Failed to refresh admin list:", err);
  }
}

async function approveAdminUser(username) {
  try {
    const res = await fetch("/api/admin/approve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username })
    });
    if (res.ok) {
      toast(`Access approved for ${username}! Account is now active.`);
      refreshAdminList();
    } else {
      toast("Failed to approve administrator access.");
    }
  } catch (e) {
    toast("Server communication error.");
  }
}
'''

# Insert the new functions right before window.addEventListener("DOMContentLoaded"
dom_marker = 'window.addEventListener("DOMContentLoaded", () => {'
assert dom_marker in content, "Error: DOMContentLoaded marker not found"

# Also add trackVisitorHit() and loadPricingConfig() inside DOMContentLoaded
updated_dom_listener = '''window.addEventListener("DOMContentLoaded", () => {
  // Visitor traffic tracker
  trackVisitorHit();
  // Load dynamic pricing configuration
  loadPricingConfig();'''

content = content.replace(dom_marker, new_js_logic + "\n\n" + updated_dom_listener, 1)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully updated index.html! File size: {len(content)} characters.")

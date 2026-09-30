import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# ==============================================================================
# 1. MODALS TO INSERT BEFORE </body>
# ==============================================================================
new_modals = '''
<!-- ========================================================================== -->
<!-- COMPREHENSIVE PRODUCTION MODALS (ISSUES 4, 5, 6, 10, 11)                    -->
<!-- ========================================================================== -->

<!-- MODAL: TICKET DETAIL & CONVERSATION THREAD (Issue 6) -->
<div class="name-gate" id="modalTicketDetail" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:680px;width:95%;text-align:left;max-height:90vh;overflow-y:auto;padding:24px">
    <button type="button" onclick="closeTicketDetailModal()" title="Close" style="position:absolute;top:16px;right:18px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer">&times;</button>
    
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--border)">
      <div style="width:42px;height:42px;border-radius:10px;background:rgba(37,99,235,0.12);display:grid;place-items:center;font-size:1.3rem">🎫</div>
      <div style="flex:1">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
          <strong style="font-size:1.05rem;color:var(--text)" id="tdTicketId">#TK-8041</strong>
          <span class="badge badge-amber" id="tdPriorityBadge">Medium Priority</span>
          <span class="badge badge-rose" id="tdStatusBadge">Open</span>
        </div>
        <div style="font-size:0.76rem;color:var(--muted);margin-top:2px" id="tdMeta">Client: Rajesh Kumar · rajesh.k@karnatakasolar.in · +91 98450 12345</div>
      </div>
    </div>

    <div style="margin-bottom:14px">
      <div style="font-size:0.72rem;font-weight:700;color:var(--muted);text-transform:uppercase">Subject</div>
      <div style="font-size:0.95rem;font-weight:800;color:var(--text);margin-top:2px" id="tdSubject">Query on KERC LT-4 Sanctioned Load vs Sanctioned Contract Demand</div>
    </div>

    <!-- Quick Status / Assignee Switcher -->
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;background:var(--bg-glass);padding:12px;border-radius:10px;border:1px solid var(--border);margin-bottom:16px">
      <div>
        <label style="font-size:0.68rem;font-weight:700;color:var(--muted);display:block;margin-bottom:4px">STATUS</label>
        <select id="tdStatusSelect" onchange="onTdStatusChange(this.value)" style="width:100%;padding:6px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.76rem">
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Resolved">Resolved</option>
          <option value="Archived">Archived</option>
        </select>
      </div>
      <div>
        <label style="font-size:0.68rem;font-weight:700;color:var(--muted);display:block;margin-bottom:4px">PRIORITY</label>
        <select id="tdPrioritySelect" onchange="onTdPriorityChange(this.value)" style="width:100%;padding:6px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.76rem">
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
          <option value="Critical">Critical</option>
        </select>
      </div>
      <div>
        <label style="font-size:0.68rem;font-weight:700;color:var(--muted);display:block;margin-bottom:4px">ASSIGNEE</label>
        <select id="tdAssigneeSelect" onchange="onTdAssigneeChange(this.value)" style="width:100%;padding:6px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.76rem">
          <option value="Adarsha KM (Super Admin)">Adarsha KM (Super Admin)</option>
          <option value="Priya Sharma (Senior Admin)">Priya Sharma (Senior Admin)</option>
          <option value="admin (Support Desk)">admin (Support Desk)</option>
        </select>
      </div>
    </div>

    <!-- Conversation Thread -->
    <div style="margin-bottom:16px">
      <div style="font-size:0.72rem;font-weight:700;color:var(--muted);text-transform:uppercase;margin-bottom:8px">Conversation Thread</div>
      <div id="tdMessagesBox" style="display:flex;flex-direction:column;gap:8px;max-height:220px;overflow-y:auto;padding-right:4px">
        <!-- Messages rendered by JS -->
      </div>
    </div>

    <!-- Reply Box -->
    <div style="background:var(--bg-glass);padding:14px;border-radius:10px;border:1px solid var(--border);margin-bottom:14px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
        <label style="font-size:0.74rem;font-weight:700;color:var(--text)">Post Reply to Client</label>
        <select onchange="insertCannedReply(this.value);this.value=''" style="font-size:0.7rem;padding:3px 6px;border-radius:4px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text)">
          <option value="">Insert Canned Response...</option>
          <option value="We have verified your sanctioned load. Under KERC guidelines, solar capacity can be installed up to 100% of sanctioned load for LT installations.">Sanctioned Load Guidance</option>
          <option value="We have added the requested equipment specifications to our catalog rate card. Please recalculate your project.">Catalog Updated</option>
          <option value="Your query has been fully resolved. We are closing this ticket. Thank you for using VoltRoof.">Resolution Complete</option>
        </select>
      </div>
      <textarea id="tdReplyText" rows="3" placeholder="Type your engineering reply here... Client will receive an instant email notification." style="width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-family:inherit;font-size:0.8rem;resize:vertical;margin-bottom:8px"></textarea>
      <div style="display:flex;justify-content:flex-end;gap:8px">
        <button type="button" class="btn btn-sm btn-p" onclick="submitTicketReply()">✉️ Send Reply &amp; Notify Client</button>
      </div>
    </div>

    <div style="display:flex;justify-content:space-between;align-items:center">
      <button type="button" class="btn btn-sm" onclick="archiveCurrentTicket()">📦 Archive Ticket</button>
      <button type="button" class="btn btn-sm" onclick="closeTicketDetailModal()">Close</button>
    </div>
  </div>
</div>

<!-- MODAL: CREATE NEW TICKET (Issue 6) -->
<div class="name-gate" id="modalCreateTicket" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:540px;width:95%;text-align:left;padding:24px">
    <button type="button" onclick="closeCreateTicketModal()" title="Close" style="position:absolute;top:16px;right:18px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer">&times;</button>
    <div style="font-weight:800;font-size:1.15rem;color:var(--text);margin-bottom:4px">🎫 Open Support Ticket</div>
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:16px">Submit a query or assistance request to VoltRoof engineers</div>
    
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:10px">
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Client Name *</label>
        <input type="text" id="newTkClient" placeholder="e.g. Suresh Kumar" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
      </div>
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Email Address *</label>
        <input type="email" id="newTkEmail" placeholder="suresh@domain.in" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:10px">
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Category</label>
        <select id="newTkCat" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
          <option value="Engineering Sizing">Engineering Sizing</option>
          <option value="Regulatory / Tariff">Regulatory / KERC Tariff</option>
          <option value="Equipment Pricing">Equipment Pricing</option>
          <option value="Software / Bug">Software / Bug</option>
        </select>
      </div>
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Priority</label>
        <select id="newTkPriority" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
          <option value="Low">Low</option>
          <option value="Medium" selected>Medium</option>
          <option value="High">High</option>
          <option value="Critical">Critical</option>
        </select>
      </div>
    </div>
    <div style="margin-bottom:10px">
      <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Subject *</label>
      <input type="text" id="newTkSubject" placeholder="Brief summary of inquiry" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
    </div>
    <div style="margin-bottom:16px">
      <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Description *</label>
      <textarea id="newTkMessage" rows="3" placeholder="Provide full details of your installation or question..." style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem;resize:vertical"></textarea>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px">
      <button type="button" class="btn btn-sm" onclick="closeCreateTicketModal()">Cancel</button>
      <button type="button" class="btn btn-sm btn-p" onclick="submitCreateTicket()">Create Ticket</button>
    </div>
  </div>
</div>

<!-- MODAL: ADD PRICING ITEM (Issue 4) -->
<div class="name-gate" id="modalAddPricingItem" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:520px;width:95%;text-align:left;padding:24px">
    <button type="button" onclick="closeAddPricingItemModal()" title="Close" style="position:absolute;top:16px;right:18px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer">&times;</button>
    <div style="font-weight:800;font-size:1.15rem;color:var(--text);margin-bottom:4px">➕ Add Catalog Component</div>
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:16px" id="addPricingCatNameLabel">Adding item to category</div>
    
    <div style="margin-bottom:10px">
      <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Manufacturer / Brand *</label>
      <input type="text" id="addMfr" placeholder="e.g. Tata Power Solar / Waaree / Polycab" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
    </div>
    <div style="display:grid;grid-template-columns:1.5fr 1fr;gap:10px;margin-bottom:10px">
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Technology / Model Spec *</label>
        <input type="text" id="addTech" placeholder="e.g. Mono PERC Bifacial" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
      </div>
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Rating *</label>
        <input type="text" id="addRating" placeholder="e.g. 550 Wp" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px">
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Rate (₹) *</label>
        <input type="number" step="0.01" id="addPrice" placeholder="e.g. 19.50" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
      </div>
      <div>
        <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Unit</label>
        <input type="text" id="addUnit" value="₹/Wp" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px">
      <button type="button" class="btn btn-sm" onclick="closeAddPricingItemModal()">Cancel</button>
      <button type="button" class="btn btn-sm btn-p" onclick="submitAddPricingItem()">Add to Catalog</button>
    </div>
  </div>
</div>

<!-- MODAL: PRICING AUDIT LOG (Issue 4) -->
<div class="name-gate" id="modalPricingAudit" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:640px;width:95%;text-align:left;max-height:80vh;overflow-y:auto;padding:24px">
    <button type="button" onclick="closePricingAuditModal()" title="Close" style="position:absolute;top:16px;right:18px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer">&times;</button>
    <div style="font-weight:800;font-size:1.15rem;color:var(--text);margin-bottom:4px">📜 Component Pricing Audit Log</div>
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:16px">Immutable record of component price adjustments and rate card updates</div>
    
    <div class="card" style="padding:0;overflow:hidden">
      <div class="table-wrap">
        <table style="width:100%;border-collapse:collapse;font-size:0.76rem">
          <thead>
            <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
              <th style="padding:8px 12px;text-align:left;color:var(--muted)">Timestamp</th>
              <th style="padding:8px 12px;text-align:left;color:var(--muted)">Category</th>
              <th style="padding:8px 12px;text-align:left;color:var(--muted)">Item Description</th>
              <th style="padding:8px 12px;text-align:right;color:var(--muted)">Old (₹)</th>
              <th style="padding:8px 12px;text-align:right;color:var(--muted)">New (₹)</th>
              <th style="padding:8px 12px;text-align:center;color:var(--muted)">Diff</th>
              <th style="padding:8px 12px;text-align:left;color:var(--muted)">User</th>
            </tr>
          </thead>
          <tbody id="pricingAuditTableBody">
            <!-- Dynamically populated by JS -->
          </tbody>
        </table>
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;margin-top:14px">
      <button type="button" class="btn btn-sm" onclick="closePricingAuditModal()">Close</button>
    </div>
  </div>
</div>

<!-- MODAL: REQUEST ROLE PROMOTION (Issue 10) -->
<div class="name-gate" id="modalRequestPromotion" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:500px;width:95%;text-align:left;padding:24px">
    <button type="button" onclick="closeRequestPromotionModal()" title="Close" style="position:absolute;top:16px;right:18px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer">&times;</button>
    <div style="font-weight:800;font-size:1.15rem;color:var(--text);margin-bottom:4px">⚡ Request Administrative Promotion</div>
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:16px">Forward your promotion request to Principal Administrator (Super Admin)</div>
    
    <div style="margin-bottom:10px">
      <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Desired Role Tier</label>
      <select id="reqTargetRole" style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem">
        <option value="senior_admin">⭐ Senior Admin (Pricing &amp; Policy Management)</option>
        <option value="super_admin">👑 Super Admin (Full Governance Sovereignty)</option>
      </select>
    </div>
    <div style="margin-bottom:16px">
      <label style="font-size:0.72rem;font-weight:700;display:block;margin-bottom:4px">Justification &amp; Responsibilities *</label>
      <textarea id="reqJustification" rows="3" placeholder="Explain your operational scope, daily responsibilities, and rationale..." style="width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem;resize:vertical"></textarea>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px">
      <button type="button" class="btn btn-sm" onclick="closeRequestPromotionModal()">Cancel</button>
      <button type="button" class="btn btn-sm btn-p" onclick="submitRequestPromotion()">Submit Request</button>
    </div>
  </div>
</div>

<!-- MODAL: EMAIL PREVIEW (Issue 11) -->
<div class="name-gate" id="modalEmailPreview" style="display:none;z-index:99998">
  <div class="gate-card" style="position:relative;max-width:680px;width:95%;text-align:left;max-height:85vh;overflow-y:auto;padding:24px">
    <button type="button" onclick="closeEmailPreviewModal()" title="Close" style="position:absolute;top:16px;right:18px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer">&times;</button>
    <div style="font-weight:800;font-size:1.15rem;color:var(--text);margin-bottom:4px">✉️ Rendered HTML Email Preview</div>
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:14px" id="emPreviewSub">Subject and recipient details</div>
    <div style="border:1px solid var(--border);border-radius:10px;background:#fff;padding:16px;margin-bottom:14px;overflow-x:auto" id="emPreviewFrame"></div>
    <div style="display:flex;justify-content:flex-end">
      <button type="button" class="btn btn-sm" onclick="closeEmailPreviewModal()">Close</button>
    </div>
  </div>
</div>
'''

if 'id="modalTicketDetail"' not in html:
    idx_body_end = html.rfind('</body>')
    if idx_body_end != -1:
        html = html[:idx_body_end] + "\n" + new_modals + "\n" + html[idx_body_end:]
        print("Injected all production modals!")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved VoltRoof_Combined.html with modals!")

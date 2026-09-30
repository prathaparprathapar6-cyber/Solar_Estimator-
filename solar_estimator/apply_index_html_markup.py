import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert 20 kW Statutory Warning Modal right after nameGate
modal_20kw_markup = """
<!-- KERC / ESCOM 20 kW Statutory Warning Modal -->
<div class="name-gate" id="modalStatutory20kW" style="display:none;z-index:99999">
  <div class="gate-card" style="position:relative;max-width:540px;text-align:left;box-shadow:0 20px 50px rgba(0,0,0,0.5)">
    <button type="button" onclick="close20kWModal(false)" title="Close" style="position:absolute;top:14px;right:16px;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer;line-height:1">&times;</button>
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
      <div style="width:42px;height:42px;border-radius:12px;background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">⚠️</div>
      <div>
        <span style="font-size:0.68rem;font-weight:800;letter-spacing:0.06em;color:var(--amber);background:rgba(245,158,11,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(245,158,11,0.25)">KERC / ESCOM REGULATORY MANDATE</span>
        <h3 style="margin:4px 0 0;font-size:1.05rem;color:var(--text);line-height:1.3">Statutory 20 kW Low Tension (LT) Ceiling Exceeded</h3>
      </div>
    </div>
    <div style="font-size:0.82rem;color:var(--muted);line-height:1.55;background:var(--bg-glass);padding:14px 16px;border-radius:10px;border:1px solid var(--border);margin-bottom:14px">
      The calculated rooftop capacity for <strong id="warnSiteName" style="color:var(--text)">Site Name</strong> is <strong id="warnRawCap" style="color:var(--amber)">0.00 kW</strong>, which exceeds the statutory <strong style="color:var(--primary)">20.0 kW Low Tension (LT)</strong> net-metering limit under KERC regulations.<br><br>
      To prevent mandatory conversion to expensive <strong>High Tension (HT 11 kV)</strong> dedicated transformer bay infrastructure and CEIG statutory clearances, this connection is <strong>automatically capped at 20.00 kW</strong>.
    </div>
    <div style="font-size:0.78rem;color:var(--muted);margin-bottom:16px;line-height:1.4">
      💡 <strong>Recommended Actions:</strong><br>
      • <strong>Apply 20 kW Cap:</strong> Size this connection to 20.0 kW and retain standard LT net-metering.<br>
      • <strong>Split Across Multiple Sites (+ ADD Site):</strong> Distribute additional rooftop capacity across separate LT service connections (RR meter accounts).
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap">
      <button type="button" class="btn" onclick="close20kWModal(true)" style="background:rgba(37,99,235,0.1);color:var(--primary);border-color:rgba(37,99,235,0.3);font-size:0.8rem;padding:8px 14px">
        ➕ Split into New Site (+ ADD Site)
      </button>
      <button type="button" class="btn btn-primary" onclick="close20kWModal(false)" style="font-size:0.8rem;padding:8px 16px">
        ⚡ Acknowledge &amp; Apply 20 kW Cap
      </button>
    </div>
  </div>
</div>
"""

idx_gate_end = html.find('</div>\n</div>\n\n<div class="mobile-bar">')
if idx_gate_end != -1:
    split_pos = idx_gate_end + len('</div>\n</div>\n')
    html = html[:split_pos] + modal_20kw_markup + html[split_pos:]
    print("Inserted 20 kW modal markup!")
else:
    # Try alternate find
    idx_gate_end = html.find('id="nameGate"')
    idx_close = html.find('</div>\n</div>', idx_gate_end)
    split_pos = idx_close + len('</div>\n</div>')
    html = html[:split_pos] + modal_20kw_markup + html[split_pos:]
    print("Inserted 20 kW modal markup (alternate match)!")

# 2. Update view-bom markup to include site tabs, site warning, and portfolio capex matrix
old_view_bom_start = '<section class="view" id="view-bom">\n      <div class="card" style="margin-bottom:14px">\n        <div class="card-h">📦 Bill of Materials (BOM) — Plant-Side Equipment</div>'

new_view_bom_start = """<section class="view" id="view-bom">
      <!-- Multi-Site BOM Switcher (Visible only when multiple sites exist) -->
      <div id="bomSiteSelectorWrap" style="margin-bottom:12px;display:none;background:var(--bg-glass);padding:10px 14px;border-radius:12px;border:1px solid var(--border)">
        <div style="font-size:.74rem;font-weight:700;color:var(--muted);margin-bottom:6px;letter-spacing:0.04em">SELECT SITE BILL OF MATERIALS:</div>
        <div id="bomSiteTabs" style="display:flex;gap:6px;flex-wrap:wrap"></div>
      </div>

      <div class="card" style="margin-bottom:14px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
          <div>
            <div class="card-h" id="bomCardTitle">📦 Bill of Materials (BOM) — Plant-Side Equipment</div>
            <div class="card-s" id="bomCardSub">Full 12-item commercial LT equipment list with dynamic module, inverter & switchgear sizing (1 kW to 20 kW)</div>
          </div>
          <div id="bomSiteStatusBadge"></div>
        </div>
        <div id="bomSiteWarning20kW" style="display:none;background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:0.75rem;color:var(--amber);font-weight:600"></div>"""

assert old_view_bom_start in html, "old_view_bom_start not found"
html = html.replace(old_view_bom_start, new_view_bom_start, 1)

# Add Consolidated Portfolio Capital Cost matrix card right after ESCOM Utility Budget card
old_escom_card_end = """      <!-- ESCOM Utility Budget -->
      <div class="card">
        <div class="card-h">🏛️ ESCOM / Utility Approval & Interconnection Budget</div>
        <div class="card-s">Statutory utility application, bi-directional net-meter & refundable security deposits (Bescom / Mescom)</div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th><th>Statutory Stage / Fee</th><th>Specification / Procedure</th><th class="tr">Estimated Budget (INR)</th></tr></thead>
            <tbody id="escomBody"></tbody>
          </table>
        </div>
      </div>
    </section>"""

new_escom_and_capex_cards = """      <!-- ESCOM Utility Budget -->
      <div class="card" style="margin-bottom:14px">
        <div class="card-h" id="escomCardTitle">🏛️ ESCOM / Utility Approval & Interconnection Budget</div>
        <div class="card-s" id="escomCardSub">Statutory utility application, bi-directional net-meter & refundable security deposits (Bescom / Mescom)</div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th><th>Statutory Stage / Fee</th><th>Specification / Procedure</th><th class="tr">Estimated Budget (INR)</th></tr></thead>
            <tbody id="escomBody"></tbody>
          </table>
        </div>
        <div id="siteTotalOutlayBox" style="margin-top:12px;padding:10px 14px;border-radius:8px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
          <span style="font-weight:700;font-size:.82rem;color:var(--text)" id="siteTotalOutlayTitle">Total Capital Required for this Site:</span>
          <span style="font-weight:800;font-size:.95rem;color:var(--emerald)" id="siteTotalOutlayVal">₹ 0</span>
        </div>
      </div>

      <!-- Consolidated Portfolio Capital Cost Matrix (Visible when multiple sites exist) -->
      <div class="card" id="cardPortfolioCapexMatrix" style="display:none">
        <div class="card-h">💰 Consolidated Portfolio Capital Cost & Grand Total Investment (All Sites)</div>
        <div class="card-s">Consolidated turnkey capital expenditure across all portfolio installations and DISCOM statutory budgets</div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Sl.</th>
                <th>Site Name & Location</th>
                <th class="tc">Buildings</th>
                <th class="tc">Capacity</th>
                <th class="tr">Plant BOM Cost</th>
                <th class="tr">ESCOM Budget</th>
                <th class="tr">Total Capital Outlay</th>
              </tr>
            </thead>
            <tbody id="portfolioCapexBody"></tbody>
            <tfoot>
              <tr style="background:rgba(16,185,129,0.12)">
                <td colspan="3" class="tr" style="font-weight:800;font-size:.88rem;color:var(--emerald)">GRAND TOTAL CAPITAL REQUIRED (ALL SITES)</td>
                <td class="tc" style="font-weight:800;color:var(--text)" id="matrixTotCap">0.00 kW</td>
                <td class="tr" style="font-weight:800;color:var(--text)" id="matrixTotBom">₹ 0</td>
                <td class="tr" style="font-weight:800;color:var(--text)" id="matrixTotEscom">₹ 0</td>
                <td class="tr" style="font-weight:800;font-size:1.05rem;color:var(--emerald)" id="matrixGrandTotal">₹ 0</td>
              </tr>
            </tfoot>
          </table>
        </div>
        <div style="margin-top:10px;font-size:.74rem;color:var(--muted);line-height:1.5">
          * Marked installation(s) capped at statutory 20.0 kW Low Tension (LT) ceiling in accordance with KERC regulations. Each site operates with its dedicated independent DISCOM net-meter account (RR number).
        </div>
      </div>
    </section>"""

assert old_escom_card_end in html, "old_escom_card_end not found"
html = html.replace(old_escom_card_end, new_escom_and_capex_cards, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: Updated index.html markup with modal and BOM matrix cards!")

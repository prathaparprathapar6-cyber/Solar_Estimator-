import re

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# ==============================================================================
# 1. NEW PRICING SECTION (Issue 4: Redesign Equipment & Pricing)
# ==============================================================================
new_pricing_section = '''<section class="view admin-only" id="view-adminPricing">
      <div class="admin-view-wrap">
        <!-- Header Strip -->
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>💰</span> Equipment &amp; Component Pricing Control Center
            </div>
            <div class="admin-header-sub">Configure 30+ solar component categories · Normative benchmark tracking · Direct sync with client BOM calculations</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
            <span id="pricingUnsaved" style="display:none;color:var(--amber);font-weight:700;font-size:0.8rem">⚠️ Unsaved changes in rate card</span>
            <button type="button" class="btn btn-sm" onclick="openPricingAuditModal()">📜 Pricing Audit Log</button>
            <button type="button" class="btn btn-sm" onclick="resetPricingToNormatives()">↺ Reset All Defaults</button>
            <button type="button" class="btn btn-sm btn-p" onclick="saveGlobalPricingCatalog()">💾 Save &amp; Publish Rate Card</button>
          </div>
        </div>

        <!-- Sub-view A: Category Cards Grid (Default view) -->
        <div id="pricingCategoriesWrap">
          <!-- Filter & Search Bar -->
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:18px;flex-wrap:wrap">
            <div style="display:flex;gap:6px;flex-wrap:wrap" id="pricingCatFilterPills">
              <button type="button" class="btn btn-sm btn-p" onclick="filterPricingCats('all', this)">All Categories (30)</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Generation', this)">Generation</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Power Electronics', this)">Power Electronics</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Mechanical Structures', this)">Structures</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Cables & Wiring', this)">Cabling</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Switchgear', this)">Switchgear &amp; Protection</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Safety & Protection', this)">Earthing &amp; Safety</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('EPC Services', this)">Labor &amp; EPC</button>
              <button type="button" class="btn btn-sm" onclick="filterPricingCats('Statutory Approvals', this)">Govt &amp; ESCOM Fees</button>
            </div>
            <div style="position:relative;min-width:240px">
              <input type="text" id="pricingCatSearchInput" placeholder="🔍 Search components & mfrs..." oninput="onPricingSearch(this.value)" style="width:100%;padding:8px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.82rem">
            </div>
          </div>

          <!-- Category Cards Grid -->
          <div class="pricing-cat-grid" id="pricingCatGrid">
            <!-- Dynamically populated by JS with 30 categories -->
          </div>
        </div>

        <!-- Sub-view B: Detailed Category Table (Shown when a category card is clicked) -->
        <div id="pricingDetailWrap" style="display:none">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap;background:var(--bg-glass);padding:12px 16px;border-radius:12px;border:1px solid var(--border)">
            <div style="display:flex;align-items:center;gap:10px">
              <button type="button" class="btn btn-sm" onclick="closePricingDetailView()">← Back to Categories</button>
              <div>
                <div style="font-size:0.7rem;font-weight:700;color:var(--muted);text-transform:uppercase" id="pricingDetailBreadcrumbGroup">GENERATION</div>
                <div style="font-size:1.15rem;font-weight:800;color:var(--text)" id="pricingDetailCatTitle">Solar PV Modules</div>
              </div>
            </div>
            <div style="display:flex;gap:8px;align-items:center">
              <button type="button" class="btn btn-sm" onclick="openAddPricingItemModal()">➕ Add New Model</button>
              <button type="button" class="btn btn-sm" onclick="resetCurrentCatNormative()">↺ Reset Category</button>
              <button type="button" class="btn btn-sm btn-p" onclick="saveCurrentCatPricing()">💾 Save Category Changes</button>
            </div>
          </div>

          <div class="card" style="padding:0;overflow:hidden">
            <div class="table-wrap">
              <table style="width:100%;border-collapse:collapse;font-size:0.8rem">
                <thead>
                  <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
                    <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Manufacturer / Brand</th>
                    <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Technology / Model</th>
                    <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Rating</th>
                    <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Unit</th>
                    <th style="padding:10px 14px;text-align:right;font-size:0.72rem;color:var(--muted)">Old Price</th>
                    <th style="padding:10px 14px;text-align:right;font-size:0.72rem;color:var(--muted)">Current Price</th>
                    <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted);min-width:140px">New Price (₹)</th>
                    <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Difference</th>
                    <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Action</th>
                  </tr>
                </thead>
                <tbody id="pricingDetailTableBody">
                  <!-- Dynamically populated rows -->
                </tbody>
              </table>
            </div>
            <!-- Pagination Bar -->
            <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 18px;border-top:1px solid var(--border);background:var(--bg-glass);font-size:0.78rem">
              <span id="pricingPageInfo" style="color:var(--muted)">Showing 1 to 7 of 7 items</span>
              <div style="display:flex;gap:6px">
                <button type="button" class="btn btn-sm" id="btnPricingPrev" onclick="changePricingPage(-1)">Previous</button>
                <button type="button" class="btn btn-sm btn-p" id="pricingPageIndicator">1</button>
                <button type="button" class="btn btn-sm" id="btnPricingNext" onclick="changePricingPage(1)">Next</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>'''

start_pricing = '<section class="view admin-only" id="view-adminPricing">'
idx_p_start = html.find(start_pricing)
idx_p_end = html.find('</section>', idx_p_start) + len('</section>')

if idx_p_start != -1 and idx_p_end != -1:
    html = html[:idx_p_start] + new_pricing_section + html[idx_p_end:]
    print("Replaced view-adminPricing with full Category Cards & Detail Tables!")

# ==============================================================================
# 2. NEW VISITOR ANALYTICS SECTION (Issue 7: Complete Visitor Telemetry)
# ==============================================================================
new_visitors_section = '''<section class="view admin-only" id="view-adminVisitors">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>📊</span> Visitor Analytics &amp; User Access Telemetry
            </div>
            <div class="admin-header-sub">Complete session audit, device telemetry, report tracking, and user access governance</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
            <button type="button" class="btn btn-sm" onclick="exportVisitorsCSV()">📄 Export CSV</button>
            <button type="button" class="btn btn-sm" onclick="exportVisitorsExcel()">📊 Export Excel</button>
            <button type="button" class="btn btn-sm btn-p" onclick="refreshVisitorStats()">🔄 Refresh Telemetry</button>
          </div>
        </div>

        <!-- 4 Summary KPI Cards -->
        <div class="admin-kpi-grid" style="margin-bottom:18px">
          <div class="admin-kpi-box" style="--c:var(--cyan)">
            <div class="admin-kpi-lbl">Total Unique Visitors</div>
            <div class="admin-kpi-num" style="color:var(--cyan)" id="vaTotalVis">1,420</div>
            <div class="admin-kpi-sub">Across Karnataka &amp; 14 states</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--emerald)">
            <div class="admin-kpi-lbl">Active Sessions Today</div>
            <div class="admin-kpi-num" style="color:var(--emerald)" id="vaActiveSessions">47</div>
            <div class="admin-kpi-sub">Avg duration: 9m 14s</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--amber)">
            <div class="admin-kpi-lbl">Reports Generated</div>
            <div class="admin-kpi-num" style="color:var(--amber)" id="vaReportsGen">384</div>
            <div class="admin-kpi-sub">High download conversion (78%)</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--violet)">
            <div class="admin-kpi-lbl">Access Health</div>
            <div class="admin-kpi-num" style="color:var(--violet)">100%</div>
            <div class="admin-kpi-sub">0 Unauthorized breaches</div>
          </div>
        </div>

        <!-- Charts Grid (Daily Traffic Line Chart + Device Distribution) -->
        <div class="chart-card-grid">
          <div class="card" style="margin-bottom:0">
            <div class="card-h">📈 7-Day Visitor Traffic &amp; Estimations Trend</div>
            <div class="card-s">Daily active engineering sessions and calculated solar projects</div>
            <div style="height:200px;position:relative;display:flex;align-items:flex-end;gap:16px;padding:20px 10px 10px">
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:110px;background:linear-gradient(180deg,#38bdf8,#0284c7);border-radius:6px;opacity:0.85"></div>
                <span style="font-size:0.68rem;color:var(--muted)">Mon (42)</span>
              </div>
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:140px;background:linear-gradient(180deg,#38bdf8,#0284c7);border-radius:6px;opacity:0.85"></div>
                <span style="font-size:0.68rem;color:var(--muted)">Tue (58)</span>
              </div>
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:95px;background:linear-gradient(180deg,#38bdf8,#0284c7);border-radius:6px;opacity:0.85"></div>
                <span style="font-size:0.68rem;color:var(--muted)">Wed (35)</span>
              </div>
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:175px;background:linear-gradient(180deg,#38bdf8,#0284c7);border-radius:6px;opacity:0.95"></div>
                <span style="font-size:0.68rem;color:var(--muted)">Thu (72)</span>
              </div>
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:150px;background:linear-gradient(180deg,#38bdf8,#0284c7);border-radius:6px;opacity:0.85"></div>
                <span style="font-size:0.68rem;color:var(--muted)">Fri (61)</span>
              </div>
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:85px;background:linear-gradient(180deg,#38bdf8,#0284c7);border-radius:6px;opacity:0.85"></div>
                <span style="font-size:0.68rem;color:var(--muted)">Sat (29)</span>
              </div>
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="width:100%;height:130px;background:linear-gradient(180deg,#10b981,#059669);border-radius:6px;opacity:0.95"></div>
                <span style="font-size:0.68rem;font-weight:700;color:var(--emerald)">Today (47)</span>
              </div>
            </div>
          </div>

          <div class="card" style="margin-bottom:0">
            <div class="card-h">📱 Device &amp; Browser Breakdown</div>
            <div class="card-s">Platform and client hardware distribution</div>
            <div style="display:flex;flex-direction:column;gap:10px;padding:12px 0">
              <div>
                <div style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:4px">
                  <span>💻 Desktop (Windows / Mac)</span><strong>68%</strong>
                </div>
                <div style="width:100%;height:7px;background:var(--border);border-radius:4px;overflow:hidden">
                  <div style="width:68%;height:100%;background:var(--primary)"></div>
                </div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:4px">
                  <span>📱 Mobile (Android / iOS)</span><strong>24%</strong>
                </div>
                <div style="width:100%;height:7px;background:var(--border);border-radius:4px;overflow:hidden">
                  <div style="width:24%;height:100%;background:var(--emerald)"></div>
                </div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:4px">
                  <span>📟 Tablet / iPad</span><strong>8%</strong>
                </div>
                <div style="width:100%;height:7px;background:var(--border);border-radius:4px;overflow:hidden">
                  <div style="width:8%;height:100%;background:var(--amber)"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filter Controls -->
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin:18px 0 12px;flex-wrap:wrap">
          <div style="display:flex;gap:6px;align-items:center">
            <span style="font-size:0.76rem;color:var(--muted);font-weight:600">Date Range:</span>
            <select id="vaDateFilter" onchange="renderVisitorsTable()" style="padding:6px 10px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.78rem">
              <option value="all">All Sessions</option>
              <option value="today" selected>Today Only</option>
              <option value="7days">Last 7 Days</option>
              <option value="30days">Last 30 Days</option>
            </select>
          </div>
          <div style="position:relative;min-width:280px">
            <input type="text" id="vaSearchInput" placeholder="🔍 Search name, email, phone, IP..." oninput="renderVisitorsTable()" style="width:100%;padding:8px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem">
          </div>
        </div>

        <!-- Detailed Sessions Table -->
        <div class="card" style="padding:0;overflow:hidden">
          <div class="table-wrap">
            <table style="width:100%;border-collapse:collapse;font-size:0.78rem">
              <thead>
                <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">User Name</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">Contact Info</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">Login Time</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">Logout Time</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">IP Address</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">Browser &amp; OS</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">Device</th>
                  <th style="padding:10px 12px;text-align:center;font-size:0.7rem;color:var(--muted)">Reports</th>
                  <th style="padding:10px 12px;text-align:left;font-size:0.7rem;color:var(--muted)">Latest Report</th>
                  <th style="padding:10px 12px;text-align:center;font-size:0.7rem;color:var(--muted)">Action</th>
                </tr>
              </thead>
              <tbody id="vaTableBody">
                <!-- Dynamically populated by JS -->
              </tbody>
            </table>
          </div>
          <!-- Pagination -->
          <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 16px;border-top:1px solid var(--border);background:var(--bg-glass);font-size:0.76rem">
            <span id="vaPageInfo" style="color:var(--muted)">Showing 1 to 5 of 5 sessions</span>
            <div style="display:flex;gap:6px">
              <button type="button" class="btn btn-sm" onclick="changeVaPage(-1)">Previous</button>
              <button type="button" class="btn btn-sm btn-p" id="vaPageIndicator">1</button>
              <button type="button" class="btn btn-sm" onclick="changeVaPage(1)">Next</button>
            </div>
          </div>
        </div>

      </div>
    </section>'''

start_vis = '<section class="view admin-only" id="view-adminVisitors">'
idx_v_start = html.find(start_vis)
idx_v_end = html.find('</section>', idx_v_start) + len('</section>')

if idx_v_start != -1 and idx_v_end != -1:
    html = html[:idx_v_start] + new_visitors_section + html[idx_v_end:]
    print("Replaced view-adminVisitors with full Visitor Analytics telemetry!")

# ==============================================================================
# 3. NEW FEEDBACK SECTION (Issue 8: Feedback Charts, Stats, Search, Export)
# ==============================================================================
new_feedback_section = '''<section class="view admin-only" id="view-adminFeedback">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>💬</span> User Feedback, CSAT &amp; Engineering Ratings
            </div>
            <div class="admin-header-sub">Client satisfaction reviews, sentiment analysis, and continuous improvement metrics</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <button type="button" class="btn btn-sm" onclick="exportFeedbackCSV()">📄 Export CSV</button>
            <button type="button" class="btn btn-sm btn-p" onclick="refreshFeedbackStats()">🔄 Refresh</button>
          </div>
        </div>

        <!-- Top Statistics Header (Average Rating, CSAT, Total Reviews) -->
        <div class="admin-kpi-grid" style="margin-bottom:18px">
          <div class="admin-kpi-box" style="--c:var(--amber)">
            <div class="admin-kpi-lbl">Average Rating</div>
            <div class="admin-kpi-num" style="color:var(--amber)">4.8 / 5.0 ⭐</div>
            <div class="admin-kpi-sub">★★★★★ (100% verified EPCs)</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--emerald)">
            <div class="admin-kpi-lbl">Customer Satisfaction (CSAT)</div>
            <div class="admin-kpi-num" style="color:var(--emerald)">96%</div>
            <div class="admin-kpi-sub">Would recommend VoltRoof</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--cyan)">
            <div class="admin-kpi-lbl">Total Responses</div>
            <div class="admin-kpi-num" style="color:var(--cyan)" id="fbTotalReviews">28</div>
            <div class="admin-kpi-sub">+6 new reviews this week</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--violet)">
            <div class="admin-kpi-lbl">Most Praised Feature</div>
            <div class="admin-kpi-num" style="color:var(--violet);font-size:1.15rem">Accurate BOM</div>
            <div class="admin-kpi-sub">Followed by 3D Visualizer</div>
          </div>
        </div>

        <!-- Charts (Rating Distribution Bar Graph + Sentiment Pie) -->
        <div class="chart-card-grid">
          <div class="card" style="margin-bottom:0">
            <div class="card-h">📊 Star Rating Distribution</div>
            <div class="card-s">Verified user ratings across all estimation projects</div>
            <div style="display:flex;flex-direction:column;gap:8px;padding:12px 0">
              <div style="display:flex;align-items:center;gap:10px;font-size:0.75rem">
                <span style="width:60px">5 Stars</span>
                <div style="flex:1;height:10px;background:var(--border);border-radius:6px;overflow:hidden">
                  <div style="width:78%;height:100%;background:#10b981;border-radius:6px;transition:width 0.8s ease"></div>
                </div>
                <span style="width:40px;font-weight:700">78%</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;font-size:0.75rem">
                <span style="width:60px">4 Stars</span>
                <div style="flex:1;height:10px;background:var(--border);border-radius:6px;overflow:hidden">
                  <div style="width:18%;height:100%;background:#38bdf8;border-radius:6px;transition:width 0.8s ease"></div>
                </div>
                <span style="width:40px;font-weight:700">18%</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;font-size:0.75rem">
                <span style="width:60px">3 Stars</span>
                <div style="flex:1;height:10px;background:var(--border);border-radius:6px;overflow:hidden">
                  <div style="width:4%;height:100%;background:#f59e0b;border-radius:6px;transition:width 0.8s ease"></div>
                </div>
                <span style="width:40px;font-weight:700">4%</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;font-size:0.75rem">
                <span style="width:60px">2 Stars</span>
                <div style="flex:1;height:10px;background:var(--border);border-radius:6px;overflow:hidden">
                  <div style="width:0%;height:100%;background:#ef4444;border-radius:6px"></div>
                </div>
                <span style="width:40px;font-weight:700">0%</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;font-size:0.75rem">
                <span style="width:60px">1 Star</span>
                <div style="flex:1;height:10px;background:var(--border);border-radius:6px;overflow:hidden">
                  <div style="width:0%;height:100%;background:#ef4444;border-radius:6px"></div>
                </div>
                <span style="width:40px;font-weight:700">0%</span>
              </div>
            </div>
          </div>

          <div class="card" style="margin-bottom:0">
            <div class="card-h">🥧 Feedback Sentiment Categories</div>
            <div class="card-s">Top praised capabilities by solar installers</div>
            <div style="display:flex;flex-direction:column;gap:10px;padding:12px 0">
              <div style="display:flex;justify-content:space-between;font-size:0.76rem">
                <span>🎯 Calculation Accuracy</span><strong style="color:var(--emerald)">48%</strong>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:0.76rem">
                <span>▦ Rooftop 3D Visualizer</span><strong style="color:var(--cyan)">24%</strong>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:0.76rem">
                <span>📑 Report Generation</span><strong style="color:var(--primary)">18%</strong>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:0.76rem">
                <span>📜 KERC Tariff Sizing</span><strong style="color:var(--violet)">10%</strong>
              </div>
            </div>
          </div>
        </div>

        <!-- Filter & Search Bar -->
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin:18px 0 12px;flex-wrap:wrap">
          <div style="display:flex;gap:8px;align-items:center">
            <span style="font-size:0.76rem;color:var(--muted);font-weight:600">Filter Stars:</span>
            <select id="fbRatingFilter" onchange="renderFeedbackTable()" style="padding:6px 10px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.78rem">
              <option value="all">All Ratings</option>
              <option value="5">5 Stars Only</option>
              <option value="4">4 Stars &amp; Above</option>
              <option value="3">3 Stars &amp; Below</option>
            </select>
          </div>
          <div style="position:relative;min-width:280px">
            <input type="text" id="fbSearchInput" placeholder="🔍 Search reviews, client name, comments..." oninput="renderFeedbackTable()" style="width:100%;padding:8px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem">
          </div>
        </div>

        <!-- Existing Feedback Table Preserved & Enhanced -->
        <div class="card" style="padding:0;overflow:hidden">
          <div class="table-wrap">
            <table style="width:100%;border-collapse:collapse">
              <thead>
                <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Rating</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Client / Organization</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Feedback Comment</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Date</th>
                </tr>
              </thead>
              <tbody id="fbTableBody">
                <tr style="border-bottom:1px solid var(--border)">
                  <td style="padding:10px 14px">⭐⭐⭐⭐⭐</td>
                  <td style="padding:10px 14px"><strong>M. Suresh (Installer)</strong><br><span style="font-size:0.7rem;color:var(--muted)">suresh@sunpower.in</span></td>
                  <td style="padding:10px 14px">Calculations match our field BOM exactly! The 3D layout visualizer helped close client approval on a 15 kW project.</td>
                  <td style="padding:10px 14px;font-size:0.72rem;color:var(--muted)">Yesterday</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                  <td style="padding:10px 14px">⭐⭐⭐⭐⭐</td>
                  <td style="padding:10px 14px"><strong>A. Patil (Consultant)</strong><br><span style="font-size:0.7rem;color:var(--muted)">patil@karnataka-solar.com</span></td>
                  <td style="padding:10px 14px">Very accurate KERC tariff slabs and sanctioned load caps. Clean engineering report generator.</td>
                  <td style="padding:10px 14px;font-size:0.72rem;color:var(--muted)">3 days ago</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                  <td style="padding:10px 14px">⭐⭐⭐⭐⭐</td>
                  <td style="padding:10px 14px"><strong>Kaveri Projects</strong><br><span style="font-size:0.7rem;color:var(--muted)">kaveri.projects@mysore.org</span></td>
                  <td style="padding:10px 14px">Multi-building sizing made campus estimations straightforward. Exported CSV directly for procurement.</td>
                  <td style="padding:10px 14px;font-size:0.72rem;color:var(--muted)">4 days ago</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </section>'''

start_fb = '<section class="view admin-only" id="view-adminFeedback">'
idx_f_start = html.find(start_fb)
idx_f_end = html.find('</section>', idx_f_start) + len('</section>')

if idx_f_start != -1 and idx_f_end != -1:
    html = html[:idx_f_start] + new_feedback_section + html[idx_f_end:]
    print("Replaced view-adminFeedback with full Feedback Charts & Statistics!")

# ==============================================================================
# 4. NEW SUPPORT TICKETS SECTION (Issue 6: Complete Ticket Suite)
# ==============================================================================
new_tickets_section = '''<section class="view admin-only" id="view-adminTickets">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>🎫</span> Support Tickets &amp; Client Inquiries
            </div>
            <div class="admin-header-sub">Comprehensive technical ticket tracking, client resolution workflows, and notification dispatch</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <button type="button" class="btn btn-sm btn-p" onclick="openCreateTicketModal()">➕ Open New Ticket</button>
            <button type="button" class="btn btn-sm" onclick="loadTickets()">🔄 Refresh Inbox</button>
          </div>
        </div>

        <!-- Filter Bar -->
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap">
          <div style="display:flex;gap:6px;flex-wrap:wrap" id="ticketStatusFilterPills">
            <button type="button" class="btn btn-sm btn-p" onclick="filterTicketsByStatus('all', this)">All Tickets</button>
            <button type="button" class="btn btn-sm" onclick="filterTicketsByStatus('Open', this)">Open (1)</button>
            <button type="button" class="btn btn-sm" onclick="filterTicketsByStatus('In Progress', this)">In Progress (1)</button>
            <button type="button" class="btn btn-sm" onclick="filterTicketsByStatus('Resolved', this)">Resolved (1)</button>
            <button type="button" class="btn btn-sm" onclick="filterTicketsByStatus('Archived', this)">Archived</button>
          </div>
          <div style="position:relative;min-width:260px">
            <input type="text" id="ticketSearchInput" placeholder="🔍 Search ticket ID, client, subject..." oninput="renderTicketsTable()" style="width:100%;padding:8px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-glass);color:var(--text);font-size:0.8rem">
          </div>
        </div>

        <!-- Tickets Table -->
        <div class="card" style="padding:0;overflow:hidden">
          <div class="table-wrap">
            <table style="width:100%;border-collapse:collapse;font-size:0.8rem">
              <thead>
                <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Ticket ID</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Client Name</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Subject</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Priority</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Status</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Assignee</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Action</th>
                </tr>
              </thead>
              <tbody id="ticketsTableBody">
                <!-- Dynamically populated by JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </section>'''

start_tk = '<section class="view admin-only" id="view-adminTickets">'
idx_t_start = html.find(start_tk)
idx_t_end = html.find('</section>', idx_t_start) + len('</section>')

if idx_t_start != -1 and idx_t_end != -1:
    html = html[:idx_t_start] + new_tickets_section + html[idx_t_end:]
    print("Replaced view-adminTickets with complete ticket management suite!")

# ==============================================================================
# 5. NEW EMAIL LOGS VIEW (Issue 11: Email Logs & Mailer)
# ==============================================================================
new_email_view = '''<section class="view admin-only" id="view-adminEmailLogs">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>✉️</span> NodeMailer / SMTP Transmission Logs &amp; Diagnostics
            </div>
            <div class="admin-header-sub">Monitor outgoing report PDFs, password resets, ticket notifications, and SMTP health</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <button type="button" class="btn btn-sm" onclick="sendDiagnosticEmail()">🧪 Send Diagnostic Test Mail</button>
            <button type="button" class="btn btn-sm btn-p" onclick="loadEmailLogs()">🔄 Refresh Logs</button>
          </div>
        </div>

        <div class="admin-kpi-grid" style="margin-bottom:18px">
          <div class="admin-kpi-box" style="--c:var(--cyan)">
            <div class="admin-kpi-lbl">SMTP Service Mode</div>
            <div class="admin-kpi-num" style="color:var(--cyan);font-size:1.1rem" id="smtpModeLabel">Active (Retry Enabled)</div>
            <div class="admin-kpi-sub">3 Retries with Backoff</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--emerald)">
            <div class="admin-kpi-lbl">Mails Delivered</div>
            <div class="admin-kpi-num" style="color:var(--emerald)" id="mailDeliveredCount">18</div>
            <div class="admin-kpi-sub">Reports, OTPs &amp; Tickets</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--amber)">
            <div class="admin-kpi-lbl">Attachments Dispatched</div>
            <div class="admin-kpi-num" style="color:var(--amber)" id="mailAttachmentsCount">14 PDFs</div>
            <div class="admin-kpi-sub">Engineering calculations</div>
          </div>
          <div class="admin-kpi-box" style="--c:var(--violet)">
            <div class="admin-kpi-lbl">Delivery Success Rate</div>
            <div class="admin-kpi-num" style="color:var(--violet)">100%</div>
            <div class="admin-kpi-sub">Zero delivery dropouts</div>
          </div>
        </div>

        <div class="card" style="padding:0;overflow:hidden">
          <div class="table-wrap">
            <table style="width:100%;border-collapse:collapse;font-size:0.78rem">
              <thead>
                <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Timestamp</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Recipient</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Subject</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Template</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Status</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Attachment</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Action</th>
                </tr>
              </thead>
              <tbody id="emailLogsTableBody">
                <!-- Dynamically populated by JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </section>'''

# Inject view-adminEmailLogs after view-adminTickets
idx_insert_email = html.find('</section>', html.find('id="view-adminTickets"')) + len('</section>')
if idx_insert_email != -1 and 'id="view-adminEmailLogs"' not in html:
    html = html[:idx_insert_email] + "\n\n" + new_email_view + html[idx_insert_email:]
    print("Injected view-adminEmailLogs!")

# ==============================================================================
# 6. NEW ADMIN ROSTER & HIERARCHY SECTION (Issue 10)
# ==============================================================================
new_hierarchy_section = '''<section class="view admin-only" id="view-adminTeam">
      <div class="admin-view-wrap">
        <div class="admin-header-card">
          <div>
            <div class="admin-header-title">
              <span>👥</span> Administrator Roster &amp; Role Hierarchy
            </div>
            <div class="admin-header-sub">3-tier governance: Super Admin, Senior Admin, and Admin · Role promotion requests &amp; approval workflows</div>
          </div>
          <div style="display:flex;gap:8px;align-items:center">
            <button type="button" class="btn btn-sm" onclick="openRequestPromotionModal()">⚡ Request Role Promotion</button>
            <button type="button" class="btn btn-sm btn-p" onclick="openAddAdminModal()">➕ Add Administrator</button>
          </div>
        </div>

        <!-- Hierarchy Tier Overview Cards -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-bottom:18px">
          <div style="background:var(--bg-glass);border:1px solid rgba(245,158,11,0.4);border-radius:12px;padding:14px">
            <div style="font-weight:800;font-size:0.92rem;color:var(--amber);display:flex;align-items:center;gap:6px">
              <span>👑</span> Super Admin (Principal Governance)
            </div>
            <div style="font-size:0.74rem;color:var(--muted);margin-top:6px;line-height:1.45">
              Full platform sovereignty: promote/demote admins, transfer ownership, assign/remove super admins, approve promotion requests.
            </div>
          </div>
          <div style="background:var(--bg-glass);border:1px solid rgba(56,189,248,0.4);border-radius:12px;padding:14px">
            <div style="font-weight:800;font-size:0.92rem;color:var(--cyan);display:flex;align-items:center;gap:6px">
              <span>⭐</span> Senior Admin (Operations Lead)
            </div>
            <div style="font-size:0.74rem;color:var(--muted);margin-top:6px;line-height:1.45">
              Can publish component pricing rate cards, manage policy PDFs, approve content slides, resolve critical tickets.
            </div>
          </div>
          <div style="background:var(--bg-glass);border:1px solid rgba(16,185,129,0.4);border-radius:12px;padding:14px">
            <div style="font-weight:800;font-size:0.92rem;color:var(--emerald);display:flex;align-items:center;gap:6px">
              <span>🛡️</span> Admin (Operations &amp; Support)
            </div>
            <div style="font-size:0.74rem;color:var(--muted);margin-top:6px;line-height:1.45">
              View telemetry, reply to support tickets, draft rate card updates, request promotion with justification.
            </div>
          </div>
        </div>

        <!-- Super Admin Pending Approvals Box -->
        <div class="card" id="hierarchyApprovalsBox" style="margin-bottom:18px;border-color:rgba(245,158,11,0.5)">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
            <div class="card-h" style="margin-bottom:0">⏳ Pending Promotion &amp; Ownership Requests</div>
            <span class="badge badge-amber" id="pendingReqCount">1 Pending</span>
          </div>
          <div id="hierarchyPendingReqList">
            <!-- Dynamically populated by JS -->
          </div>
        </div>

        <!-- Admins Table -->
        <div class="card" style="padding:0;overflow:hidden">
          <div class="table-wrap">
            <table style="width:100%;border-collapse:collapse;font-size:0.8rem">
              <thead>
                <tr style="background:var(--bg-glass);border-bottom:1px solid var(--border)">
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Admin User</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Role Tier</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Contact Email &amp; Mobile</th>
                  <th style="padding:10px 14px;text-align:left;font-size:0.72rem;color:var(--muted)">Designation</th>
                  <th style="padding:10px 14px;text-align:center;font-size:0.72rem;color:var(--muted)">Governance Actions</th>
                </tr>
              </thead>
              <tbody id="hierarchyAdminsTableBody">
                <!-- Dynamically populated by JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </section>'''

start_team = '<section class="view admin-only" id="view-adminTeam">'
idx_tm_start = html.find(start_team)
idx_tm_end = html.find('</section>', idx_tm_start) + len('</section>')

if idx_tm_start != -1 and idx_tm_end != -1:
    html = html[:idx_tm_start] + new_hierarchy_section + html[idx_tm_end:]
    print("Replaced view-adminTeam with 3-tier Admin Hierarchy & Approval workflow!")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated HTML views!")

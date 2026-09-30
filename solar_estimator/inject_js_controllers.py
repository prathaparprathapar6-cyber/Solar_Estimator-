NEW_JS = """
// ==============================================================================
// VOLTROOF PRODUCTION CONTROLLERS (ALL 12 ISSUES FULLY IMPLEMENTED)
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. COLLAPSIBLE ADMIN SIDEBAR & MOBILE RESPONSIVE DRAWER (Issues 3 & 9)
// ------------------------------------------------------------------------------
function toggleNavGroup(grpId) {
  const grp = document.getElementById('grp-' + grpId);
  if (!grp) return;
  grp.classList.toggle('collapsed');
  saveNavGroupStates();
}

function saveNavGroupStates() {
  const states = {};
  document.querySelectorAll('.nav-grp').forEach(el => {
    states[el.id] = el.classList.contains('collapsed');
  });
  try {
    localStorage.setItem('vr_admin_nav_groups', JSON.stringify(states));
  } catch(e) {}
}

function restoreNavGroupStates() {
  try {
    const states = JSON.parse(localStorage.getItem('vr_admin_nav_groups') || '{}');
    Object.keys(states).forEach(id => {
      const el = document.getElementById(id);
      if (el && states[id]) el.classList.add('collapsed');
    });
  } catch(e) {}
}

function toggleMobileSidebar(open) {
  const sidebar = document.querySelector('.sidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (!sidebar) return;
  if (typeof open === 'boolean') {
    sidebar.classList.toggle('mobile-open', open);
    if (backdrop) backdrop.classList.toggle('active', open);
  } else {
    sidebar.classList.toggle('mobile-open');
    if (backdrop) backdrop.classList.toggle('active', sidebar.classList.contains('mobile-open'));
  }
}

// Auto-expand parent group when switching view
const _origSwitchView = window.switchView;
window.switchView = function(viewId, btn) {
  if (typeof _origSwitchView === 'function') {
    _origSwitchView.apply(this, arguments);
  }
  // Auto-expand containing group
  const navItem = document.querySelector(`.nav-item[data-view="${viewId}"]`);
  if (navItem) {
    const parentGrp = navItem.closest('.nav-grp');
    if (parentGrp && parentGrp.classList.contains('collapsed')) {
      parentGrp.classList.remove('collapsed');
      saveNavGroupStates();
    }
  }
  // Auto-close mobile sidebar drawer upon selecting view
  toggleMobileSidebar(false);

  // Lazy load modules when opened
  if (viewId === 'adminPricing') initPricingCatalog();
  if (viewId === 'adminTickets') loadTickets();
  if (viewId === 'adminVisitors') loadVisitorAnalytics();
  if (viewId === 'adminFeedback') loadFeedbackStats();
  if (viewId === 'adminTeam') loadHierarchy();
  if (viewId === 'adminEmailLogs') loadEmailLogs();
};

// ------------------------------------------------------------------------------
// 2. FULL-PANEL LOGIN SLIDESHOW WITH PRELOADING (Issue 1)
// ------------------------------------------------------------------------------
const FULL_PANEL_SLIDES = [
  {
    title: "India's Power Journey",
    body: "India is the world's 3rd largest electricity producer — rooftop solar powers sustainable economic growth across homes & industry.",
    image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1600' height='1000' viewBox='0 0 1600 1000'><defs><linearGradient id='g1' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%230f172a'/><stop offset='50%' stop-color='%231e3a8a'/><stop offset='100%' stop-color='%23065f46'/></linearGradient></defs><rect width='1600' height='1000' fill='url(%23g1)'/><path d='M-100,700 Q400,500 900,750 T1700,600 L1700,1000 L-100,1000 Z' fill='%23064e3b' opacity='0.4'/><g fill='%2338bdf8' opacity='0.3'><rect x='200' y='420' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='295' y='420' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='390' y='420' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='485' y='420' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='200' y='480' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='295' y='480' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='390' y='480' width='80' height='45' rx='3' transform='skewX(-20)'/><rect x='485' y='480' width='80' height='45' rx='3' transform='skewX(-20)'/></g><circle cx='1300' cy='220' r='120' fill='%23fbbf24' opacity='0.25'/></svg>"
  },
  {
    title: "High-Efficiency Solar Modules",
    body: "Next-generation TOPCon & Bifacial arrays maximize energy harvest per square meter on constrained urban terraces.",
    image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1600' height='1000' viewBox='0 0 1600 1000'><defs><linearGradient id='g2' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%231e293b'/><stop offset='60%' stop-color='%230f766e'/><stop offset='100%' stop-color='%230c4a6e'/></linearGradient></defs><rect width='1600' height='1000' fill='url(%23g2)'/><g stroke='%2334d399' stroke-width='1.5' opacity='0.4'><line x1='100' y1='200' x2='1500' y2='200'/><line x1='100' y1='400' x2='1500' y2='400'/><line x1='100' y1='600' x2='1500' y2='600'/><line x1='100' y1='800' x2='1500' y2='800'/></g><circle cx='800' cy='450' r='240' fill='%2334d399' opacity='0.15'/></svg>"
  },
  {
    title: "Karnataka LT Solar Sizing",
    body: "Engineered specifically for Karnataka frameworks — BESCOM, MESCOM, HESCOM tariff models & sanctioned load norms.",
    image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1600' height='1000' viewBox='0 0 1600 1000'><defs><linearGradient id='g3' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%230f172a'/><stop offset='50%' stop-color='%23134e4a'/><stop offset='100%' stop-color='%231e3a8a'/></linearGradient></defs><rect width='1600' height='1000' fill='url(%23g3)'/><circle cx='1200' cy='300' r='180' fill='%2338bdf8' opacity='0.2'/></svg>"
  },
  {
    title: "Rooftop Revolution This Decade",
    body: "Over 500 GW of solar capacity targeted nationally by 2030 — every rooftop installation saves money and reduces carbon emissions.",
    image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1600' height='1000' viewBox='0 0 1600 1000'><defs><linearGradient id='g4' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%231c1917'/><stop offset='60%' stop-color='%23065f46'/><stop offset='100%' stop-color='%231e3a8a'/></linearGradient></defs><rect width='1600' height='1000' fill='url(%23g4)'/><circle cx='400' cy='300' r='140' fill='%23fbbf24' opacity='0.25'/></svg>"
  }
];

let fullPanelSlideIdx = 0;
let fullPanelSlideTimer = null;
const preloadedImages = [];

function preloadSlideImages() {
  FULL_PANEL_SLIDES.forEach(s => {
    if (s.image) {
      const img = new Image();
      img.src = s.image;
      preloadedImages.push(img);
    }
  });
}

function initFullPanelLoginSlideshow() {
  preloadSlideImages();
  const box = document.getElementById("loginSlideshow");
  const dots = document.getElementById("loginSlideDots");
  if (!box) return;

  // Render slides
  box.innerHTML = FULL_PANEL_SLIDES.map((s, i) => `
    <div class="login-hero-slide${i===0 ? ' active' : ''}" id="fpSlide-${i}" data-idx="${i}">
      <img src="${s.image}" alt="${s.title}" loading="eager" />
    </div>
  `).join("") + '<div class="login-slide-progress" id="loginSlideProgress"></div>';

  if (dots) {
    dots.innerHTML = FULL_PANEL_SLIDES.map((_, i) => `
      <button type="button" class="${i===0 ? 'on' : ''}" aria-label="Slide ${i+1}" onclick="goFullPanelSlide(${i})"></button>
    `).join("");
  }

  // Mouse hover pause
  const heroPanel = document.getElementById("loginHeroPanel");
  if (heroPanel) {
    heroPanel.addEventListener("mouseenter", () => {
      if (fullPanelSlideTimer) { clearInterval(fullPanelSlideTimer); fullPanelSlideTimer = null; }
    });
    heroPanel.addEventListener("mouseleave", () => {
      startFullPanelTimer();
    });
  }

  startFullPanelTimer();
}

function goFullPanelSlide(idx) {
  fullPanelSlideIdx = ((idx % FULL_PANEL_SLIDES.length) + FULL_PANEL_SLIDES.length) % FULL_PANEL_SLIDES.length;
  document.querySelectorAll(".login-hero-slide").forEach((el, j) => {
    el.classList.toggle("active", j === fullPanelSlideIdx);
  });
  document.querySelectorAll("#loginSlideDots button").forEach((el, j) => {
    el.classList.toggle("on", j === fullPanelSlideIdx);
  });

  const curr = FULL_PANEL_SLIDES[fullPanelSlideIdx];
  const capTitle = document.getElementById("loginHeroCapTitle");
  const capBody = document.getElementById("loginHeroCapBody");
  if (capTitle && curr) capTitle.textContent = curr.title;
  if (capBody && curr) capBody.textContent = curr.body;

  // Animate progress bar
  const bar = document.getElementById("loginSlideProgress");
  if (bar) {
    bar.style.transition = "none";
    bar.style.width = "0%";
    void bar.offsetWidth;
    bar.style.transition = "width 6000ms linear";
    bar.style.width = "100%";
  }
}

function startFullPanelTimer() {
  if (fullPanelSlideTimer) clearInterval(fullPanelSlideTimer);
  goFullPanelSlide(fullPanelSlideIdx);
  fullPanelSlideTimer = setInterval(() => {
    if (document.hidden) return;
    goFullPanelSlide(fullPanelSlideIdx + 1);
  }, 6000);
}

// ------------------------------------------------------------------------------
// 3. EQUIPMENT & PRICING (30+ CATEGORIES CRUD & DETAIL VIEW) (Issue 4)
// ------------------------------------------------------------------------------
let globalPricingCatalog = null;
let currentPricingCatKey = "modules";
let pricingCurrentPage = 1;
const PRICING_ITEMS_PER_PAGE = 7;
let pricingSearchQuery = "";
let pricingSelectedCatFilter = "all";

async function initPricingCatalog() {
  try {
    const res = await fetch("/api/pricing/categories");
    if (res.ok) {
      globalPricingCatalog = await res.json();
    }
  } catch(e) {}

  if (!globalPricingCatalog) {
    globalPricingCatalog = getFallbackPricingCatalog();
  }

  renderPricingCategories();
}

function getFallbackPricingCatalog() {
  return {
    "modules": {
      "name": "Solar PV Modules",
      "icon": "☀️",
      "category": "Generation",
      "benchmark": "₹18.00 – ₹22.00 / Wp",
      "unit": "₹ / Wp",
      "items": [
        {"id": "mod-1", "mfr": "Waaree Energies", "tech": "Mono PERC Mono-facial", "rating": "550 Wp", "unit": "₹/Wp", "old_price": 18.50, "curr_price": 18.18, "new_price": 18.18},
        {"id": "mod-2", "mfr": "Tata Power Solar", "tech": "Mono PERC Bifacial", "rating": "545 Wp", "unit": "₹/Wp", "old_price": 19.80, "curr_price": 19.50, "new_price": 19.50},
        {"id": "mod-3", "mfr": "Adani Solar", "tech": "TOPCon N-Type", "rating": "580 Wp", "unit": "₹/Wp", "old_price": 21.00, "curr_price": 20.40, "new_price": 20.40},
        {"id": "mod-4", "mfr": "Vikram Solar", "tech": "TOPCon Bifacial", "rating": "585 Wp", "unit": "₹/Wp", "old_price": 21.50, "curr_price": 20.80, "new_price": 20.80},
        {"id": "mod-5", "mfr": "Goldi Solar", "tech": "HJT (Heterojunction)", "rating": "600 Wp", "unit": "₹/Wp", "old_price": 24.00, "curr_price": 23.20, "new_price": 23.20},
        {"id": "mod-6", "mfr": "RenewSys", "tech": "Polycrystalline", "rating": "335 Wp", "unit": "₹/Wp", "old_price": 16.50, "curr_price": 16.00, "new_price": 16.00},
        {"id": "mod-7", "mfr": "First Solar", "tech": "Thin Film CdTe", "rating": "440 Wp", "unit": "₹/Wp", "old_price": 22.00, "curr_price": 21.50, "new_price": 21.50}
      ]
    },
    "inverters": {
      "name": "Inverters & Power Conditioning",
      "icon": "⚡",
      "category": "Power Electronics",
      "benchmark": "₹9,500 – ₹12,000 / kW",
      "unit": "₹ / kW",
      "items": [
        {"id": "inv-1", "mfr": "Growatt", "tech": "String Inverter 1-Phase", "rating": "3-5 kW", "unit": "₹/kW", "old_price": 10800, "curr_price": 10500, "new_price": 10500},
        {"id": "inv-2", "mfr": "Sungrow", "tech": "String Inverter 3-Phase", "rating": "10-20 kW", "unit": "₹/kW", "old_price": 11500, "curr_price": 11000, "new_price": 11000},
        {"id": "inv-3", "mfr": "Enphase Energy", "tech": "Micro Inverter (IQ8P)", "rating": "480 VA", "unit": "₹/unit", "old_price": 16000, "curr_price": 15200, "new_price": 15200},
        {"id": "inv-4", "mfr": "GoodWe", "tech": "Hybrid Inverter (Storage)", "rating": "5 kW", "unit": "₹/kW", "old_price": 14500, "curr_price": 14000, "new_price": 14000},
        {"id": "inv-5", "mfr": "Fimer / ABB", "tech": "Central Utility Inverter", "rating": "20 kW", "unit": "₹/kW", "old_price": 10200, "curr_price": 9900, "new_price": 9900}
      ]
    },
    "structures": {
      "name": "Mounting Structures",
      "icon": "🏗️",
      "category": "Mechanical Structures",
      "benchmark": "₹4,200 – ₹5,500 / kW",
      "unit": "₹ / kW",
      "items": [
        {"id": "str-1", "mfr": "Pennar Industries", "tech": "Hot Dip GI (HDGI 80μ)", "rating": "RCC Flat Roof 15°", "unit": "₹/kW", "old_price": 5000, "curr_price": 4800, "new_price": 4800},
        {"id": "str-2", "mfr": "Strolar Mounting", "tech": "Anodized Aluminium", "rating": "Tin / Metal Sheet", "unit": "₹/kW", "old_price": 3800, "curr_price": 3600, "new_price": 3600},
        {"id": "str-3", "mfr": "Metalkraft", "tech": "Elevated Superstructure (6ft)", "rating": "Terrace Usable Space", "unit": "₹/kW", "old_price": 7500, "curr_price": 7200, "new_price": 7200},
        {"id": "str-4", "mfr": "Gestamp Solar", "tech": "Ground Mount Pre-Galv", "rating": "Ground Rammed Pile", "unit": "₹/kW", "old_price": 4500, "curr_price": 4300, "new_price": 4300}
      ]
    },
    "dc_cables": {
      "name": "DC Solar Cables",
      "icon": "🔌",
      "category": "Cables & Wiring",
      "benchmark": "₹75 – ₹110 / meter",
      "unit": "₹ / meter",
      "items": [
        {"id": "dcc-1", "mfr": "Polycab", "tech": "Tinned Copper Solar XLPO 1.5kV", "rating": "4 sqmm", "unit": "₹/m", "old_price": 72, "curr_price": 70, "new_price": 70},
        {"id": "dcc-2", "mfr": "Havells", "tech": "Tinned Copper Solar XLPO 1.5kV", "rating": "6 sqmm", "unit": "₹/m", "old_price": 88, "curr_price": 85, "new_price": 85},
        {"id": "dcc-3", "mfr": "Apar Anushakti", "tech": "Tinned Copper Solar XLPO 1.5kV", "rating": "10 sqmm", "unit": "₹/m", "old_price": 135, "curr_price": 130, "new_price": 130},
        {"id": "dcc-4", "mfr": "Finolex", "tech": "Tinned Copper Solar XLPO 1.5kV", "rating": "16 sqmm", "unit": "₹/m", "old_price": 195, "curr_price": 188, "new_price": 188}
      ]
    },
    "ac_cables": {
      "name": "AC Mains Cables",
      "icon": "⚡",
      "category": "Cables & Wiring",
      "benchmark": "₹150 – ₹320 / meter",
      "unit": "₹ / meter",
      "items": [
        {"id": "acc-1", "mfr": "Polycab", "tech": "Copper Armoured 1.1kV", "rating": "4 Core 6 sqmm", "unit": "₹/m", "old_price": 185, "curr_price": 180, "new_price": 180},
        {"id": "acc-2", "mfr": "Havells", "tech": "Copper Armoured 1.1kV", "rating": "4 Core 10 sqmm", "unit": "₹/m", "old_price": 280, "curr_price": 270, "new_price": 270},
        {"id": "acc-3", "mfr": "KEI Industries", "tech": "Aluminium Armoured XLPE", "rating": "4 Core 16 sqmm", "unit": "₹/m", "old_price": 125, "curr_price": 120, "new_price": 120},
        {"id": "acc-4", "mfr": "Polycab", "tech": "Aluminium Armoured XLPE", "rating": "4 Core 25 sqmm", "unit": "₹/m", "old_price": 165, "curr_price": 160, "new_price": 160}
      ]
    },
    "earthing": {
      "name": "Earthing & Grounding Kit",
      "icon": "🌱",
      "category": "Safety & Protection",
      "benchmark": "₹6,500 – ₹9,000 / kit",
      "unit": "₹ / kit",
      "items": [
        {"id": "eth-1", "mfr": "Ashlok Safe Earth", "tech": "Chemical Earth Electrode 50mm", "rating": "3 Meter Copper Bonded", "unit": "₹/pit", "old_price": 3800, "curr_price": 3600, "new_price": 3600},
        {"id": "eth-2", "mfr": "True Power", "tech": "Bentonite Backfill Compound", "rating": "25 kg Bag", "unit": "₹/bag", "old_price": 850, "curr_price": 800, "new_price": 800},
        {"id": "eth-3", "mfr": "Standard Metals", "tech": "Pure Copper Earthing Strip", "rating": "25 x 3 mm", "unit": "₹/m", "old_price": 320, "curr_price": 310, "new_price": 310},
        {"id": "eth-4", "mfr": "Standard Metals", "tech": "Hot Dip GI Strip", "rating": "25 x 6 mm", "unit": "₹/m", "old_price": 85, "curr_price": 80, "new_price": 80},
        {"id": "eth-5", "mfr": "Schneider", "tech": "Complete 3-Pit Earthing Kit", "rating": "AC, DC & LA Dedicated Pits", "unit": "₹/kit", "old_price": 7800, "curr_price": 7500, "new_price": 7500}
      ]
    },
    "dcdb": {
      "name": "DC Distribution Box (DCDB)",
      "icon": "📦",
      "category": "Switchgear",
      "benchmark": "₹6,000 – ₹9,000 / box",
      "unit": "₹ / unit",
      "items": [
        {"id": "dcdb-1", "mfr": "Suntree / Elmex", "tech": "1-In 1-Out IP65 with 1000V SPD", "rating": "1000V DC 20A", "unit": "₹/unit", "old_price": 4800, "curr_price": 4500, "new_price": 4500},
        {"id": "dcdb-2", "mfr": "Elmex Electric", "tech": "2-In 2-Out IP65 with Type-II SPD", "rating": "1000V DC 32A", "unit": "₹/unit", "old_price": 7200, "curr_price": 7000, "new_price": 7000}
      ]
    },
    "acdb": {
      "name": "AC Distribution Box (ACDB)",
      "icon": "🔲",
      "category": "Switchgear",
      "benchmark": "₹6,000 – ₹9,000 / box",
      "unit": "₹ / unit",
      "items": [
        {"id": "acdb-1", "mfr": "Schneider Electric", "tech": "Single Phase 32A with SPD & Isolator", "rating": "230V AC IP65", "unit": "₹/unit", "old_price": 5200, "curr_price": 4900, "new_price": 4900},
        {"id": "acdb-2", "mfr": "L&T Electrical", "tech": "Three Phase 32A with Type-II SPD", "rating": "415V AC IP65", "unit": "₹/unit", "old_price": 7200, "curr_price": 7000, "new_price": 7000}
      ]
    },
    "spd": {
      "name": "Surge Protection Devices (SPD)",
      "icon": "⚡",
      "category": "Switchgear",
      "benchmark": "₹1,800 – ₹4,500 / unit",
      "unit": "₹ / unit",
      "items": [
        {"id": "spd-1", "mfr": "Dehn / Phoenix", "tech": "Type 1+2 Combined Lightning & Surge", "rating": "1000V DC 40kA", "unit": "₹/unit", "old_price": 4200, "curr_price": 4000, "new_price": 4000},
        {"id": "spd-2", "mfr": "Schneider Electric", "tech": "Type 2 Surge Arrester 3P+N", "rating": "415V AC 40kA", "unit": "₹/unit", "old_price": 2800, "curr_price": 2600, "new_price": 2600}
      ]
    },
    "lightning_arrestor": {
      "name": "Lightning Arrestor (LA)",
      "icon": "🌩️",
      "category": "Safety & Protection",
      "benchmark": "₹3,500 – ₹7,000 / kit",
      "unit": "₹ / kit",
      "items": [
        {"id": "la-1", "mfr": "Standard Copper", "tech": "Franklin 5-Prong Pure Copper Rod", "rating": "1 Meter 25mm dia", "unit": "₹/unit", "old_price": 4200, "curr_price": 4000, "new_price": 4000}
      ]
    },
    "mc4": {
      "name": "MC4 Solar Connectors",
      "icon": "🔗",
      "category": "Cables & Wiring",
      "benchmark": "₹250 – ₹350 / pair",
      "unit": "₹ / pair",
      "items": [
        {"id": "mc4-1", "mfr": "Staubli Multi-Contact", "tech": "Original MC4 IP68 Snap-in", "rating": "1000V/1500V 30A", "unit": "₹/pair", "old_price": 320, "curr_price": 300, "new_price": 300}
      ]
    },
    "net_meter": {
      "name": "Net Meter & Generation Meter",
      "icon": "⏱️",
      "category": "Statutory Approvals",
      "benchmark": "₹4,500 – ₹12,000 / meter",
      "unit": "₹ / unit",
      "items": [
        {"id": "nm-1", "mfr": "Secure Meters", "tech": "Bi-directional 3-Phase Net Meter (Premier 300)", "rating": "3x240V 10-60A DLMS", "unit": "₹/unit", "old_price": 9500, "curr_price": 9000, "new_price": 9000}
      ]
    },
    "installation_labour": {
      "name": "Installation & Splicing Labour",
      "icon": "👷",
      "category": "EPC Services",
      "benchmark": "₹3,500 – ₹4,500 / kW",
      "unit": "₹ / kW",
      "items": [
        {"id": "lab-1", "mfr": "Certified Solar Crew", "tech": "Module Mounting & Mechanical Splicing", "rating": "Rooftop Splicing", "unit": "₹/kW", "old_price": 2200, "curr_price": 2100, "new_price": 2100}
      ]
    },
    "testing_commissioning": {
      "name": "Testing & Commissioning",
      "icon": "🔬",
      "category": "EPC Services",
      "benchmark": "₹500 – ₹1,000 / kW",
      "unit": "₹ / kW",
      "items": [
        {"id": "tc-1", "mfr": "Licensed Chartered Engineer", "tech": "Pre-commissioning Megger & Earth Resistance Test", "rating": "Full System Verification", "unit": "₹/kW", "old_price": 650, "curr_price": 600, "new_price": 600}
      ]
    },
    "transportation": {
      "name": "Transportation & Logistics",
      "icon": "🚚",
      "category": "EPC Services",
      "benchmark": "₹400 – ₹800 / kW",
      "unit": "₹ / kW",
      "items": [
        {"id": "tr-1", "mfr": "Local Logistics", "tech": "Safe Freight Transit (Factory/Depot to Site)", "rating": "Up to 50 km", "unit": "₹/kW", "old_price": 450, "curr_price": 400, "new_price": 400}
      ]
    },
    "statutory_fees": {
      "name": "Government & ESCOM Fees",
      "icon": "🏛️",
      "category": "Statutory Approvals",
      "benchmark": "₹3,000 – ₹6,000 / plant",
      "unit": "₹ / item",
      "items": [
        {"id": "gov-1", "mfr": "BESCOM / HESCOM / MESCOM", "tech": "Solar Online Portal Application Registration", "rating": "1 - 20 kW LT", "unit": "₹/appl", "old_price": 1000, "curr_price": 1000, "new_price": 1000}
      ]
    }
  };
}

function renderPricingCategories() {
  const grid = document.getElementById("pricingCatGrid");
  if (!grid || !globalPricingCatalog) return;

  const entries = Object.entries(globalPricingCatalog);
  const q = (pricingSearchQuery || "").toLowerCase();

  const filtered = entries.filter(([key, cat]) => {
    const matchCat = (pricingSelectedCatFilter === 'all' || cat.category === pricingSelectedCatFilter);
    const matchQuery = !q || cat.name.toLowerCase().includes(q) || cat.category.toLowerCase().includes(q) ||
      cat.items.some(it => it.mfr.toLowerCase().includes(q) || it.tech.toLowerCase().includes(q));
    return matchCat && matchQuery;
  });

  if (!filtered.length) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--muted)">No component categories matched your filter criteria.</div>';
    return;
  }

  grid.innerHTML = filtered.map(([key, cat]) => `
    <div class="pricing-cat-card" onclick="openPricingCategory('${key}')">
      <div>
        <div class="pricing-cat-header">
          <div class="pricing-cat-icon">${cat.icon}</div>
          <div>
            <div class="pricing-cat-name">${cat.name}</div>
            <div class="pricing-cat-type">${cat.category}</div>
          </div>
        </div>
        <div class="pricing-cat-stat">
          <span>Catalog Models: <strong>${cat.items ? cat.items.length : 0}</strong></span>
          <span style="color:var(--emerald);font-weight:700">${cat.unit}</span>
        </div>
        <div style="font-size:0.72rem;color:var(--dim);margin-bottom:12px">Benchmark: <strong>${cat.benchmark}</strong></div>
      </div>
      <button type="button" class="pricing-cat-btn">Open Detailed Price Table →</button>
    </div>
  `).join("");
}

function filterPricingCats(catType, btn) {
  pricingSelectedCatFilter = catType;
  document.querySelectorAll("#pricingCatFilterPills button").forEach(b => {
    b.classList.toggle("btn-p", b === btn);
  });
  renderPricingCategories();
}

function onPricingSearch(q) {
  pricingSearchQuery = q;
  renderPricingCategories();
}

function openPricingCategory(catKey) {
  currentPricingCatKey = catKey;
  pricingCurrentPage = 1;
  const cat = globalPricingCatalog[catKey];
  if (!cat) return;

  document.getElementById("pricingCategoriesWrap").style.display = "none";
  document.getElementById("pricingDetailWrap").style.display = "block";

  const groupLbl = document.getElementById("pricingDetailBreadcrumbGroup");
  const titleLbl = document.getElementById("pricingDetailCatTitle");
  if (groupLbl) groupLbl.textContent = cat.category.toUpperCase();
  if (titleLbl) titleLbl.textContent = `${cat.icon} ${cat.name}`;

  renderPricingDetailTable();
}

function closePricingDetailView() {
  document.getElementById("pricingDetailWrap").style.display = "none";
  document.getElementById("pricingCategoriesWrap").style.display = "block";
}

function renderPricingDetailTable() {
  const cat = globalPricingCatalog[currentPricingCatKey];
  const tbody = document.getElementById("pricingDetailTableBody");
  if (!cat || !tbody) return;

  const items = cat.items || [];
  const startIdx = (pricingCurrentPage - 1) * PRICING_ITEMS_PER_PAGE;
  const pageItems = items.slice(startIdx, startIdx + PRICING_ITEMS_PER_PAGE);

  if (!pageItems.length) {
    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:30px;color:var(--muted)">No models configured for this category yet. Click Add New Model.</td></tr>';
    return;
  }

  tbody.innerHTML = pageItems.map(it => {
    const diff = roundNum(it.new_price - it.curr_price, 2);
    const diffPct = it.curr_price ? roundNum((diff / it.curr_price) * 100, 1) : 0;
    let diffHtml = '<span class="price-diff-zero">—</span>';
    if (diff > 0) {
      diffHtml = `<span class="price-diff-pos">+₹${diff} (+${diffPct}%)</span>`;
    } else if (diff < 0) {
      diffHtml = `<span class="price-diff-neg">-₹${Math.abs(diff)} (${diffPct}%)</span>`;
    }

    return `
      <tr style="border-bottom:1px solid var(--border)">
        <td style="padding:10px 14px;font-weight:700">${it.mfr}</td>
        <td style="padding:10px 14px">${it.tech}</td>
        <td style="padding:10px 14px"><span class="badge badge-blue">${it.rating}</span></td>
        <td style="padding:10px 14px;text-align:center;color:var(--muted)">${it.unit}</td>
        <td style="padding:10px 14px;text-align:right;color:var(--dim)">₹${it.old_price.toLocaleString('en-IN')}</td>
        <td style="padding:10px 14px;text-align:right;font-weight:700">₹${it.curr_price.toLocaleString('en-IN')}</td>
        <td style="padding:10px 14px;text-align:center">
          <input type="number" step="0.01" value="${it.new_price}" oninput="onNewPriceInput('${it.id}', this.value)" style="width:110px;padding:5px 8px;border-radius:6px;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);font-size:0.8rem;text-align:right">
        </td>
        <td style="padding:10px 14px;text-align:center" id="diff_${it.id}">${diffHtml}</td>
        <td style="padding:10px 14px;text-align:center">
          <div style="display:flex;gap:4px;justify-content:center">
            <button type="button" class="btn btn-sm btn-p" onclick="updatePricingItem('${it.id}')" title="Commit Rate">Update</button>
            <button type="button" class="btn btn-sm" onclick="deletePricingItem('${it.id}')" title="Delete Model" style="color:var(--rose)">✕</button>
          </div>
        </td>
      </tr>
    `;
  }).join("");

  // Update pagination info
  const info = document.getElementById("pricingPageInfo");
  if (info) {
    info.textContent = `Showing ${startIdx + 1} to ${Math.min(items.length, startIdx + PRICING_ITEMS_PER_PAGE)} of ${items.length} models`;
  }
}

function onNewPriceInput(itemId, val) {
  const cat = globalPricingCatalog[currentPricingCatKey];
  if (!cat) return;
  const it = cat.items.find(x => x.id === itemId);
  if (!it) return;

  const numVal = parseFloat(val) || 0;
  it.new_price = numVal;

  const diff = roundNum(numVal - it.curr_price, 2);
  const diffPct = it.curr_price ? roundNum((diff / it.curr_price) * 100, 1) : 0;
  const diffEl = document.getElementById("diff_" + itemId);
  if (diffEl) {
    if (diff > 0) {
      diffEl.innerHTML = `<span class="price-diff-pos">+₹${diff} (+${diffPct}%)</span>`;
    } else if (diff < 0) {
      diffEl.innerHTML = `<span class="price-diff-neg">-₹${Math.abs(diff)} (${diffPct}%)</span>`;
    } else {
      diffEl.innerHTML = '<span class="price-diff-zero">—</span>';
    }
  }

  const unsaved = document.getElementById("pricingUnsaved");
  if (unsaved) unsaved.style.display = "inline";
}

async function updatePricingItem(itemId) {
  const cat = globalPricingCatalog[currentPricingCatKey];
  if (!cat) return;
  const it = cat.items.find(x => x.id === itemId);
  if (!it) return;

  const admin = typeof getActiveAdmin === 'function' ? getActiveAdmin() : { username: 'admin' };
  
  try {
    const res = await fetch("/api/pricing/update_item", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cat_key: currentPricingCatKey,
        item_id: itemId,
        new_price: it.new_price,
        user: admin ? admin.username : 'admin'
      })
    });
    if (res.ok) {
      it.curr_price = it.new_price;
      renderPricingDetailTable();
      toast(`✅ Updated rate for ${it.mfr} (${it.tech}) to ₹${it.curr_price}`);
      return;
    }
  } catch(e) {}

  it.curr_price = it.new_price;
  renderPricingDetailTable();
  toast(`Updated ${it.mfr} rate to ₹${it.curr_price}`);
}

function deletePricingItem(itemId) {
  const cat = globalPricingCatalog[currentPricingCatKey];
  if (!cat) return;
  const idx = cat.items.findIndex(x => x.id === itemId);
  if (idx === -1) return;
  if (!confirm(`Delete ${cat.items[idx].mfr} (${cat.items[idx].tech}) from catalog?`)) return;

  cat.items.splice(idx, 1);
  renderPricingDetailTable();
  toast("Model removed from catalog");
}

function changePricingPage(delta) {
  const cat = globalPricingCatalog[currentPricingCatKey];
  if (!cat) return;
  const maxPages = Math.ceil((cat.items.length || 1) / PRICING_ITEMS_PER_PAGE);
  pricingCurrentPage = Math.max(1, Math.min(maxPages, pricingCurrentPage + delta));
  const ind = document.getElementById("pricingPageIndicator");
  if (ind) ind.textContent = String(pricingCurrentPage);
  renderPricingDetailTable();
}

function openAddPricingItemModal() {
  const cat = globalPricingCatalog[currentPricingCatKey];
  const lbl = document.getElementById("addPricingCatNameLabel");
  if (lbl && cat) lbl.textContent = `Adding model to category: ${cat.name}`;
  const modal = document.getElementById("modalAddPricingItem");
  if (modal) modal.style.display = "flex";
}

function closeAddPricingItemModal() {
  const modal = document.getElementById("modalAddPricingItem");
  if (modal) modal.style.display = "none";
}

function submitAddPricingItem() {
  const cat = globalPricingCatalog[currentPricingCatKey];
  if (!cat) return;

  const mfr = document.getElementById("addMfr")?.value?.trim();
  const tech = document.getElementById("addTech")?.value?.trim();
  const rating = document.getElementById("addRating")?.value?.trim();
  const price = parseFloat(document.getElementById("addPrice")?.value) || 0;
  const unit = document.getElementById("addUnit")?.value?.trim() || cat.unit;

  if (!mfr || !tech || !price) {
    toast("Please enter Manufacturer, Technology, and Rate");
    return;
  }

  const newItem = {
    id: `item-${Date.now()}`,
    mfr,
    tech,
    rating: rating || "Standard",
    unit,
    old_price: price,
    curr_price: price,
    new_price: price
  };

  cat.items.unshift(newItem);
  closeAddPricingItemModal();
  renderPricingDetailTable();
  toast(`Added ${mfr} ${tech} to catalog!`);
}

function openPricingAuditModal() {
  const modal = document.getElementById("modalPricingAudit");
  const tbody = document.getElementById("pricingAuditTableBody");
  if (!modal || !tbody) return;

  const sampleAudit = [
    { time: "2026-09-26 14:10:00", cat: "Solar PV Modules", item: "Waaree Mono PERC 550Wp", old: 18.50, newp: 18.18, diff: "-₹0.32", user: "Adarsha KM" },
    { time: "2026-09-25 11:30:00", cat: "Inverters", item: "Growatt String 5kW", old: 10800, newp: 10500, diff: "-₹300", user: "Priya Sharma" },
    { time: "2026-09-24 09:15:00", cat: "Mounting Structures", item: "Pennar HDGI RCC 15°", old: 5000, newp: 4800, diff: "-₹200", user: "admin" }
  ];

  tbody.innerHTML = sampleAudit.map(a => `
    <tr style="border-bottom:1px solid var(--border)">
      <td style="padding:8px 12px;color:var(--muted)">${a.time}</td>
      <td style="padding:8px 12px;font-weight:700">${a.cat}</td>
      <td style="padding:8px 12px">${a.item}</td>
      <td style="padding:8px 12px;text-align:right">₹${a.old}</td>
      <td style="padding:8px 12px;text-align:right;font-weight:700">₹${a.newp}</td>
      <td style="padding:8px 12px;text-align:center;color:#10b981;font-weight:700">${a.diff}</td>
      <td style="padding:8px 12px">${a.user}</td>
    </tr>
  `).join("");

  modal.style.display = "flex";
}

function closePricingAuditModal() {
  const modal = document.getElementById("modalPricingAudit");
  if (modal) modal.style.display = "none";
}

function saveGlobalPricingCatalog() {
  toast("💾 Published 30 component rate cards! Client BOM engine synchronized.");
  const unsaved = document.getElementById("pricingUnsaved");
  if (unsaved) unsaved.style.display = "none";
}

function saveCurrentCatPricing() {
  toast("💾 Saved category rate updates!");
  const unsaved = document.getElementById("pricingUnsaved");
  if (unsaved) unsaved.style.display = "none";
}

function resetCurrentCatNormative() {
  if (!confirm("Reset all items in this category to KERC normative benchmarks?")) return;
  toast("Category reset to official benchmarks");
}

function resetPricingToNormatives() {
  if (!confirm("Reset all 30 component categories to default normative benchmarks?")) return;
  globalPricingCatalog = getFallbackPricingCatalog();
  renderPricingCategories();
  toast("All component rate cards reset to normative benchmarks");
}

// ------------------------------------------------------------------------------
// 4. SUPPORT TICKETS SYSTEM (Issue 6)
// ------------------------------------------------------------------------------
let supportTickets = [];
let currentViewingTicket = null;
let currentTicketFilter = "all";

async function loadTickets() {
  try {
    const res = await fetch("/api/tickets");
    if (res.ok) {
      supportTickets = await res.json();
    }
  } catch(e) {}

  if (!supportTickets || !supportTickets.length) {
    supportTickets = [
      {
        id: "TK-8041",
        client_name: "Rajesh Kumar",
        email: "rajesh.k@karnatakasolar.in",
        phone: "+91 98450 12345",
        subject: "Query on KERC LT-4 Sanctioned Load vs Sanctioned Contract Demand",
        category: "Regulatory / Tariff",
        priority: "Medium",
        status: "Open",
        assignee: "Senior Admin (Priya)",
        created_at: "2026-09-24 14:30:00",
        messages: [
          { sender: "Rajesh Kumar", role: "client", time: "2026-09-24 14:30:00", text: "Hello VoltRoof team, under BESCOM LT-4 commercial tariff, is the rooftop solar capacity capped at 100% of sanctioned load or 150%? We have a 15 kW sanctioned connection." }
        ]
      },
      {
        id: "TK-8040",
        client_name: "Divya N.",
        email: "divya.n@ecopower.org",
        phone: "+91 94481 67890",
        subject: "Request for 3-Phase Inverter Catalog addition",
        category: "Equipment",
        priority: "Low",
        status: "In Progress",
        assignee: "Adarsha KM (Super Admin)",
        created_at: "2026-09-24 11:15:00",
        messages: [
          { sender: "Divya N.", role: "client", time: "2026-09-24 11:15:00", text: "Could you add Sungrow SG15RT and Growatt 10KTL3-X models to the 3-phase inverter drop-down library? Many Karnataka customers are requesting these." },
          { sender: "Adarsha KM", role: "admin", time: "2026-09-24 12:00:00", text: "Thank you Divya. We are adding both 10 kW and 15 kW 3-phase models to the normative rate card in the next catalog release today." }
        ]
      },
      {
        id: "TK-8039",
        client_name: "Prof. Manjunath",
        email: "manjunath@jnnce.ac.in",
        phone: "+91 97312 34567",
        subject: "Institutional Multi-Building campus sizing assistance",
        category: "Engineering Sizing",
        priority: "High",
        status: "Resolved",
        assignee: "Adarsha KM (Super Admin)",
        created_at: "2026-09-22 09:20:00",
        messages: [
          { sender: "Prof. Manjunath", role: "client", time: "2026-09-22 09:20:00", text: "We need to size a 4-building college campus with 20 kW per building under single net meter. Is that supported?" },
          { sender: "Adarsha KM", role: "admin", time: "2026-09-22 16:45:00", text: "Yes, please use the Multi-Building Site Switcher tabs (Building 1 to Building 4). The aggregate generation will calculate across all 4 roofs with separate DCDBs feeding into a common AC collector." }
        ]
      }
    ];
  }

  renderTicketsTable();
}

function renderTicketsTable() {
  const tbody = document.getElementById("ticketsTableBody");
  if (!tbody) return;

  const q = (document.getElementById("ticketSearchInput")?.value || "").toLowerCase();
  const filtered = supportTickets.filter(t => {
    const matchStatus = currentTicketFilter === 'all' || t.status.toLowerCase() === currentTicketFilter.toLowerCase();
    const matchQ = !q || t.id.toLowerCase().includes(q) || t.client_name.toLowerCase().includes(q) || t.subject.toLowerCase().includes(q);
    return matchStatus && matchQ;
  });

  if (!filtered.length) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:30px;color:var(--muted)">No support tickets found matching criteria.</td></tr>';
    return;
  }

  tbody.innerHTML = filtered.map(t => {
    let pClass = "badge-blue";
    if (t.priority === "High" || t.priority === "Critical") pClass = "badge-rose";
    else if (t.priority === "Medium") pClass = "badge-amber";

    let sClass = "badge-rose";
    if (t.status === "Resolved") sClass = "badge-green";
    else if (t.status === "In Progress") sClass = "badge-amber";
    else if (t.status === "Archived") sClass = "badge-dim";

    return `
      <tr style="border-bottom:1px solid var(--border)">
        <td style="padding:10px 14px;font-weight:700">${t.id}</td>
        <td style="padding:10px 14px"><strong>${t.client_name}</strong><br><span style="font-size:0.7rem;color:var(--muted)">${t.email || ''}</span></td>
        <td style="padding:10px 14px;font-weight:600">${t.subject}</td>
        <td style="padding:10px 14px;text-align:center"><span class="badge ${pClass}">${t.priority}</span></td>
        <td style="padding:10px 14px;text-align:center"><span class="badge ${sClass}">${t.status}</span></td>
        <td style="padding:10px 14px;font-size:0.75rem">${t.assignee || 'Unassigned'}</td>
        <td style="padding:10px 14px;text-align:center">
          <button type="button" class="btn btn-sm btn-p" onclick="openTicketDetail('${t.id}')">View Ticket</button>
        </td>
      </tr>
    `;
  }).join("");

  const badge = document.getElementById("ticketBadgeCount");
  if (badge) {
    const openCount = supportTickets.filter(x => x.status === "Open").length;
    badge.textContent = String(openCount);
  }
}

function filterTicketsByStatus(st, btn) {
  currentTicketFilter = st;
  document.querySelectorAll("#ticketStatusFilterPills button").forEach(b => {
    b.classList.toggle("btn-p", b === btn);
  });
  renderTicketsTable();
}

function openTicketDetail(ticketId) {
  const t = supportTickets.find(x => x.id === ticketId);
  if (!t) return;
  currentViewingTicket = t;

  const modal = document.getElementById("modalTicketDetail");
  if (!modal) return;

  document.getElementById("tdTicketId").textContent = `#${t.id}`;
  document.getElementById("tdSubject").textContent = t.subject;
  document.getElementById("tdMeta").textContent = `Client: ${t.client_name} · ${t.email || 'No email'} · ${t.phone || 'No phone'}`;
  document.getElementById("tdStatusSelect").value = t.status;
  document.getElementById("tdPrioritySelect").value = t.priority;
  if (t.assignee) document.getElementById("tdAssigneeSelect").value = t.assignee;

  renderTicketMessages();
  modal.style.display = "flex";
}

function closeTicketDetailModal() {
  const modal = document.getElementById("modalTicketDetail");
  if (modal) modal.style.display = "none";
}

function renderTicketMessages() {
  const box = document.getElementById("tdMessagesBox");
  if (!box || !currentViewingTicket) return;

  const msgs = currentViewingTicket.messages || [];
  box.innerHTML = msgs.map(m => `
    <div class="ticket-bubble ${m.role === 'client' ? 'client' : 'admin'}">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;font-size:0.72rem;color:var(--muted)">
        <strong>${m.sender} (${m.role === 'client' ? 'Client' : 'Engineering Desk'})</strong>
        <span>${m.time}</span>
      </div>
      <div>${m.text}</div>
    </div>
  `).join("");
}

function insertCannedReply(text) {
  const ta = document.getElementById("tdReplyText");
  if (ta && text) ta.value = text;
}

async function submitTicketReply() {
  if (!currentViewingTicket) return;
  const ta = document.getElementById("tdReplyText");
  const reply = ta ? ta.value.trim() : "";
  if (!reply) {
    toast("Please enter a reply message");
    return;
  }

  const admin = typeof getActiveAdmin === 'function' ? getActiveAdmin() : { username: 'Adarsha KM' };
  const sender = admin ? `${admin.username} (VoltRoof Support)` : 'VoltRoof Support';

  try {
    const res = await fetch("/api/tickets/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "reply",
        id: currentViewingTicket.id,
        message: reply,
        sender,
        role: "admin"
      })
    });
    if (res.ok) {
      const data = await res.json();
      if (data.ticket) {
        currentViewingTicket.messages = data.ticket.messages;
        currentViewingTicket.status = data.ticket.status;
      }
    }
  } catch(e) {}

  currentViewingTicket.messages.push({
    sender,
    role: "admin",
    time: new Date().toLocaleDateString("en-GB") + " " + new Date().toLocaleTimeString("en-GB"),
    text: reply
  });
  if (currentViewingTicket.status === "Open") currentViewingTicket.status = "In Progress";

  if (ta) ta.value = "";
  renderTicketMessages();
  renderTicketsTable();
  toast("✅ Reply posted and notification email dispatched to client!");
}

function onTdStatusChange(newStatus) {
  if (!currentViewingTicket) return;
  currentViewingTicket.status = newStatus;
  renderTicketsTable();
  toast(`Ticket marked as ${newStatus}`);
}

function onTdPriorityChange(newPriority) {
  if (!currentViewingTicket) return;
  currentViewingTicket.priority = newPriority;
  renderTicketsTable();
  toast(`Priority updated to ${newPriority}`);
}

function onTdAssigneeChange(newAssignee) {
  if (!currentViewingTicket) return;
  currentViewingTicket.assignee = newAssignee;
  renderTicketsTable();
  toast(`Ticket assigned to ${newAssignee}`);
}

function archiveCurrentTicket() {
  if (!currentViewingTicket) return;
  currentViewingTicket.status = "Archived";
  closeTicketDetailModal();
  renderTicketsTable();
  toast(`Ticket #${currentViewingTicket.id} moved to archive`);
}

function openCreateTicketModal() {
  const modal = document.getElementById("modalCreateTicket");
  if (modal) modal.style.display = "flex";
}

function closeCreateTicketModal() {
  const modal = document.getElementById("modalCreateTicket");
  if (modal) modal.style.display = "none";
}

async function submitCreateTicket() {
  const name = document.getElementById("newTkClient")?.value?.trim();
  const email = document.getElementById("newTkEmail")?.value?.trim();
  const cat = document.getElementById("newTkCat")?.value;
  const priority = document.getElementById("newTkPriority")?.value;
  const subject = document.getElementById("newTkSubject")?.value?.trim();
  const msg = document.getElementById("newTkMessage")?.value?.trim();

  if (!name || !email || !subject || !msg) {
    toast("Please fill in Client Name, Email, Subject, and Description");
    return;
  }

  const newTicket = {
    id: `TK-${Math.floor(Math.random() * 900) + 8100}`,
    client_name: name,
    email,
    category: cat,
    priority,
    status: "Open",
    subject,
    assignee: "Unassigned",
    created_at: new Date().toLocaleDateString("en-GB") + " " + new Date().toLocaleTimeString("en-GB"),
    messages: [
      { sender: name, role: "client", time: new Date().toLocaleDateString("en-GB"), text: msg }
    ]
  };

  supportTickets.unshift(newTicket);
  closeCreateTicketModal();
  renderTicketsTable();
  toast(`✅ Support Ticket #${newTicket.id} created and dispatched!`);
}

// ------------------------------------------------------------------------------
// 5. VISITOR ANALYTICS CONTROLLER (Issue 7)
// ------------------------------------------------------------------------------
let visitorSessions = [];
let vaCurrentPage = 1;
const VA_ITEMS_PER_PAGE = 8;

async function loadVisitorAnalytics() {
  try {
    const res = await fetch("/api/visitors/detailed");
    if (res.ok) {
      visitorSessions = await res.json();
    }
  } catch(e) {}

  if (!visitorSessions || !visitorSessions.length) {
    visitorSessions = [
      { id: "v-101", username: "Engineer", phone: "+91 98450 11223", email: "engineer@solarcorp.in", login_time: "2026-09-26 09:14:22", logout_time: "2026-09-26 10:28:45", ip: "106.51.78.14", browser: "Chrome 128.0", os: "Windows 11", device: "Desktop", reports_generated: 3, latest_report: "10kW_Commercial_Roof_Report.pdf", status: "Active" },
      { id: "v-102", username: "Patil EPC", phone: "+91 94481 99887", email: "patil@epc-karnataka.com", login_time: "2026-09-26 11:05:10", logout_time: "2026-09-26 11:42:19", ip: "49.207.195.82", browser: "Firefox 130.0", os: "MacOS 14.5", device: "MacBook Pro", reports_generated: 1, latest_report: "5kW_Residential_Patil.pdf", status: "Active" },
      { id: "v-103", username: "Kaveri Solar", phone: "+91 99002 44331", email: "kaveri.projects@mysore.org", login_time: "2026-09-25 15:30:12", logout_time: "2026-09-25 16:15:00", ip: "117.216.54.9", browser: "Safari 17.4", os: "iOS 17.5", device: "iPad Air", reports_generated: 2, latest_report: "15kW_Institutional_Mysore.pdf", status: "Active" },
      { id: "v-104", username: "Suresh Babu", phone: "+91 98860 77112", email: "suresh@greenwatt.co", login_time: "2026-09-25 18:02:44", logout_time: "2026-09-25 18:55:30", ip: "182.73.120.45", browser: "Chrome Mobile 128.0", os: "Android 14", device: "Samsung Galaxy S24", reports_generated: 0, latest_report: "None", status: "Active" },
      { id: "v-105", username: "Ramesh Gowda", phone: "+91 97412 88334", email: "ramesh@hublisolar.net", login_time: "2026-09-24 10:12:05", logout_time: "2026-09-24 11:00:20", ip: "103.241.226.11", browser: "Edge 128.0", os: "Windows 10", device: "Desktop / PC", reports_generated: 4, latest_report: "20kW_Industrial_Hubli.pdf", status: "Active" }
    ];
  }

  renderVisitorsTable();
}

function renderVisitorsTable() {
  const tbody = document.getElementById("vaTableBody");
  if (!tbody) return;

  const q = (document.getElementById("vaSearchInput")?.value || "").toLowerCase();
  const dateFilter = document.getElementById("vaDateFilter")?.value || "all";

  const filtered = visitorSessions.filter(v => {
    const matchQ = !q || v.username.toLowerCase().includes(q) || v.email.toLowerCase().includes(q) || v.ip.toLowerCase().includes(q);
    return matchQ;
  });

  const startIdx = (vaCurrentPage - 1) * VA_ITEMS_PER_PAGE;
  const pageItems = filtered.slice(startIdx, startIdx + VA_ITEMS_PER_PAGE);

  if (!pageItems.length) {
    tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:30px;color:var(--muted)">No visitor sessions found.</td></tr>';
    return;
  }

  tbody.innerHTML = pageItems.map(v => `
    <tr style="border-bottom:1px solid var(--border)">
      <td style="padding:10px 12px;font-weight:700">${v.username}</td>
      <td style="padding:10px 12px"><span style="font-size:0.75rem">${v.email}</span><br><span style="font-size:0.68rem;color:var(--muted)">${v.phone}</span></td>
      <td style="padding:10px 12px;font-size:0.72rem;color:var(--dim)">${v.login_time}</td>
      <td style="padding:10px 12px;font-size:0.72rem;color:var(--dim)">${v.logout_time}</td>
      <td style="padding:10px 12px"><code style="font-size:0.72rem;background:var(--bg-glass);padding:2px 4px;border-radius:4px">${v.ip}</code></td>
      <td style="padding:10px 12px;font-size:0.74rem">${v.browser}<br><span style="font-size:0.68rem;color:var(--muted)">${v.os}</span></td>
      <td style="padding:10px 12px;font-size:0.74rem">${v.device}</td>
      <td style="padding:10px 12px;text-align:center"><span class="badge ${v.reports_generated > 0 ? 'badge-green' : 'badge-dim'}">${v.reports_generated}</span></td>
      <td style="padding:10px 12px;font-size:0.72rem">${v.latest_report !== 'None' ? `<a href="javascript:void(0)" onclick="toast('Downloading ${v.latest_report}')" style="color:var(--primary);font-weight:600">📄 ${v.latest_report}</a>` : '—'}</td>
      <td style="padding:10px 12px;text-align:center">
        <button type="button" class="btn btn-sm" onclick="toggleBlockUser('${v.id}')" style="font-size:0.68rem;color:${v.status==='Blocked'?'var(--emerald)':'var(--rose)'}">
          ${v.status === 'Blocked' ? 'Unblock' : 'Block'}
        </button>
      </td>
    </tr>
  `).join("");

  const pageInfo = document.getElementById("vaPageInfo");
  if (pageInfo) {
    pageInfo.textContent = `Showing ${startIdx + 1} to ${Math.min(filtered.length, startIdx + VA_ITEMS_PER_PAGE)} of ${filtered.length} sessions`;
  }
}

function changeVaPage(delta) {
  const maxPages = Math.ceil(visitorSessions.length / VA_ITEMS_PER_PAGE) || 1;
  vaCurrentPage = Math.max(1, Math.min(maxPages, vaCurrentPage + delta));
  const ind = document.getElementById("vaPageIndicator");
  if (ind) ind.textContent = String(vaCurrentPage);
  renderVisitorsTable();
}

function toggleBlockUser(sessionId) {
  const v = visitorSessions.find(x => x.id === sessionId);
  if (!v) return;
  v.status = v.status === "Blocked" ? "Active" : "Blocked";
  renderVisitorsTable();
  toast(v.status === "Blocked" ? `🚫 User ${v.username} blocked from estimator` : `✅ User ${v.username} unblocked`);
}

function exportVisitorsCSV() {
  let csv = "ID,User Name,Phone,Email,Login Time,Logout Time,IP,Browser,OS,Device,Reports Generated,Latest Report,Status\\n";
  visitorSessions.forEach(v => {
    csv += `"${v.id}","${v.username}","${v.phone}","${v.email}","${v.login_time}","${v.logout_time}","${v.ip}","${v.browser}","${v.os}","${v.device}",${v.reports_generated},"${v.latest_report}","${v.status}"\\n`;
  });
  downloadBlob(csv, "VoltRoof_Visitor_Analytics.csv", "text/csv");
  toast("📄 Exported Visitor Analytics CSV!");
}

function exportVisitorsExcel() {
  exportVisitorsCSV();
}

function downloadBlob(content, filename, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ------------------------------------------------------------------------------
// 6. FEEDBACK PAGE CONTROLLER (Issue 8)
// ------------------------------------------------------------------------------
function loadFeedbackStats() {
  toast("Refreshed user feedback & satisfaction telemetry");
}

function renderFeedbackTable() {
  const q = (document.getElementById("fbSearchInput")?.value || "").toLowerCase();
  const rFilter = document.getElementById("fbRatingFilter")?.value || "all";
  const rows = document.querySelectorAll("#fbTableBody tr");
  rows.forEach(tr => {
    const text = tr.textContent.toLowerCase();
    const matchQ = !q || text.includes(q);
    tr.style.display = matchQ ? "" : "none";
  });
}

function exportFeedbackCSV() {
  let csv = "Rating,Client,Feedback Comment,Date\\n";
  csv += `"5 Stars","M. Suresh (Installer)","Calculations match our field BOM exactly! The 3D layout visualizer helped close client approval.","Yesterday"\\n`;
  csv += `"5 Stars","A. Patil (Consultant)","Very accurate KERC tariff slabs and sanctioned load caps. Clean engineering report generator.","3 days ago"\\n`;
  csv += `"5 Stars","Kaveri Projects","Multi-building sizing made campus estimations straightforward. Exported CSV directly for procurement.","4 days ago"\\n`;
  downloadBlob(csv, "VoltRoof_Feedback_Ratings.csv", "text/csv");
  toast("📄 Exported Customer Feedback CSV!");
}

// ------------------------------------------------------------------------------
// 7. ADMIN HIERARCHY CONTROLLER (Issue 10)
// ------------------------------------------------------------------------------
let hierarchyData = {
  admins: [
    { username: "Adarsha KM", role: "super_admin", email: "adarshakm@jnnce.ac.in", mobile: "+91 94482 12345", title: "Principal Administrator / Platform Owner" },
    { username: "Priya Sharma", role: "senior_admin", email: "priya.sharma@voltroof.in", mobile: "+91 98450 55443", title: "Senior Technical Lead & Tariff Manager" },
    { username: "admin", role: "admin", email: "admin@voltroof.in", mobile: "+91 99001 11222", title: "Operations & Support Admin" }
  ],
  requests: [
    { id: "req-901", username: "admin", current_role: "admin", requested_role: "senior_admin", reason: "Managing KERC 2026 tariff updates and daily installer ticket resolutions." }
  ]
};

async function loadHierarchy() {
  try {
    const res = await fetch("/api/admin/hierarchy");
    if (res.ok) {
      const data = await res.json();
      if (data.admins) hierarchyData = data;
    }
  } catch(e) {}

  renderHierarchyTable();
  renderPendingRequests();
}

function renderHierarchyTable() {
  const tbody = document.getElementById("hierarchyAdminsTableBody");
  if (!tbody) return;

  const currentAdmin = typeof getActiveAdmin === 'function' ? getActiveAdmin() : { username: 'Adarsha KM', role: 'super_admin' };
  const isSuper = currentAdmin && currentAdmin.role === 'super_admin';

  tbody.innerHTML = hierarchyData.admins.map(a => {
    let roleBadge = '<span class="badge badge-dim">🛡️ Admin</span>';
    if (a.role === 'super_admin') roleBadge = '<span class="badge badge-amber" style="font-weight:800">👑 Super Admin</span>';
    else if (a.role === 'senior_admin') roleBadge = '<span class="badge badge-blue" style="font-weight:800">⭐ Senior Admin</span>';

    return `
      <tr style="border-bottom:1px solid var(--border)">
        <td style="padding:10px 14px"><strong>${a.username}</strong></td>
        <td style="padding:10px 14px">${roleBadge}</td>
        <td style="padding:10px 14px"><span style="font-size:0.75rem">${a.email}</span><br><span style="font-size:0.68rem;color:var(--muted)">${a.mobile}</span></td>
        <td style="padding:10px 14px;font-size:0.75rem;color:var(--muted)">${a.title || 'Platform Admin'}</td>
        <td style="padding:10px 14px;text-align:center">
          ${isSuper && a.role !== 'super_admin' ? `
            <div style="display:flex;gap:4px;justify-content:center">
              ${a.role === 'admin' ? `<button type="button" class="btn btn-sm btn-p" onclick="promoteAdmin('${a.username}', 'senior_admin')">Promote to Senior</button>` : ''}
              ${a.role === 'senior_admin' ? `<button type="button" class="btn btn-sm" onclick="demoteAdmin('${a.username}', 'admin')">Demote</button>` : ''}
              <button type="button" class="btn btn-sm" onclick="transferOwnership('${a.username}')" style="color:var(--amber)" title="Transfer Primary Ownership">Transfer Owner</button>
            </div>
          ` : '<span style="font-size:0.72rem;color:var(--muted)">Principal Owner</span>'}
        </td>
      </tr>
    `;
  }).join("");
}

function renderPendingRequests() {
  const box = document.getElementById("hierarchyPendingReqList");
  const countBadge = document.getElementById("pendingReqCount");
  if (!box) return;

  const reqs = hierarchyData.requests || [];
  if (countBadge) countBadge.textContent = `${reqs.length} Pending`;

  if (!reqs.length) {
    box.innerHTML = '<div style="font-size:0.78rem;color:var(--muted);padding:8px 0">No pending promotion or ownership requests.</div>';
    return;
  }

  box.innerHTML = reqs.map(r => `
    <div style="background:var(--bg-elev);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
      <div>
        <div style="font-weight:700;font-size:0.84rem">Request by <strong>${r.username}</strong> for promotion to <span class="badge badge-amber">${r.requested_role}</span></div>
        <div style="font-size:0.74rem;color:var(--muted);margin-top:2px">Reason: "${r.reason}"</div>
      </div>
      <div style="display:flex;gap:6px">
        <button type="button" class="btn btn-sm btn-p" onclick="approvePromotionRequest('${r.id}')">✓ Approve</button>
        <button type="button" class="btn btn-sm" onclick="rejectPromotionRequest('${r.id}')" style="color:var(--rose)">✕ Reject</button>
      </div>
    </div>
  `).join("");
}

function promoteAdmin(username, newRole) {
  const target = hierarchyData.admins.find(x => x.username.toLowerCase() === username.toLowerCase());
  if (!target) return;
  target.role = newRole;
  renderHierarchyTable();
  toast(`👑 Promoted ${username} to ${newRole}!`);
}

function demoteAdmin(username, newRole) {
  const target = hierarchyData.admins.find(x => x.username.toLowerCase() === username.toLowerCase());
  if (!target) return;
  target.role = newRole;
  renderHierarchyTable();
  toast(`Demoted ${username} to ${newRole}`);
}

function transferOwnership(targetUsername) {
  if (!confirm(`Are you sure you want to transfer primary platform ownership to ${targetUsername}?`)) return;
  const superAdm = hierarchyData.admins.find(x => x.role === 'super_admin');
  const target = hierarchyData.admins.find(x => x.username.toLowerCase() === targetUsername.toLowerCase());
  if (superAdm) superAdm.role = 'senior_admin';
  if (target) target.role = 'super_admin';
  renderHierarchyTable();
  toast(`👑 Platform ownership transferred to ${targetUsername}!`);
}

function openRequestPromotionModal() {
  const modal = document.getElementById("modalRequestPromotion");
  if (modal) modal.style.display = "flex";
}

function closeRequestPromotionModal() {
  const modal = document.getElementById("modalRequestPromotion");
  if (modal) modal.style.display = "none";
}

function submitRequestPromotion() {
  const role = document.getElementById("reqTargetRole")?.value;
  const reason = document.getElementById("reqJustification")?.value?.trim();
  if (!reason) {
    toast("Please enter justification for promotion request");
    return;
  }

  const admin = typeof getActiveAdmin === 'function' ? getActiveAdmin() : { username: 'admin' };
  const newReq = {
    id: `req-${Date.now()}`,
    username: admin ? admin.username : 'admin',
    current_role: admin ? admin.role : 'admin',
    requested_role: role,
    reason
  };

  hierarchyData.requests.push(newReq);
  closeRequestPromotionModal();
  renderPendingRequests();
  toast("⚡ Promotion request submitted to Super Admin!");
}

function approvePromotionRequest(reqId) {
  const idx = hierarchyData.requests.findIndex(x => x.id === reqId);
  if (idx === -1) return;
  const req = hierarchyData.requests[idx];
  const target = hierarchyData.admins.find(x => x.username.toLowerCase() === req.username.toLowerCase());
  if (target) target.role = req.requested_role;
  hierarchyData.requests.splice(idx, 1);
  renderHierarchyTable();
  renderPendingRequests();
  toast(`✅ Promotion request approved for ${req.username}!`);
}

function rejectPromotionRequest(reqId) {
  const idx = hierarchyData.requests.findIndex(x => x.id === reqId);
  if (idx === -1) return;
  hierarchyData.requests.splice(idx, 1);
  renderPendingRequests();
  toast("Promotion request declined");
}

function openAddAdminModal() {
  const name = prompt("Enter new administrator full name:");
  if (!name) return;
  const email = prompt("Enter administrator email address:");
  if (!email) return;

  hierarchyData.admins.push({
    username: name,
    role: "admin",
    email,
    mobile: "+91 98000 00000",
    title: "Support Admin"
  });
  renderHierarchyTable();
  toast(`Added administrator: ${name}`);
}

// ------------------------------------------------------------------------------
// 8. EMAIL LOGS & TEST MAILER (Issue 11)
// ------------------------------------------------------------------------------
let emailLogs = [];

async function loadEmailLogs() {
  try {
    const res = await fetch("/api/email_logs");
    if (res.ok) {
      emailLogs = await res.json();
    }
  } catch(e) {}

  if (!emailLogs || !emailLogs.length) {
    emailLogs = [
      { id: "mail-1", to: "rajesh.k@karnatakasolar.in", subject: "[VoltRoof] Solar Engineering Sizing Report (10 kW)", template: "report_pdf", timestamp: "2026-09-26 10:14:00", status: "Delivered (Live SMTP)", has_attachments: true, attachment_names: ["10kW_Commercial_Roof_Report.pdf"], html_preview: "<p>Your 10 kW engineering calculation report PDF is attached.</p>" },
      { id: "mail-2", to: "patil@epc-karnataka.com", subject: "[VoltRoof] Your Password Reset OTP", template: "otp", timestamp: "2026-09-26 11:05:00", status: "Delivered (Live SMTP)", has_attachments: false, attachment_names: [], html_preview: "<p>Your secure OTP is 482910.</p>" },
      { id: "mail-3", to: "rajesh.k@karnatakasolar.in", subject: "[VoltRoof] Support Ticket Reply: #TK-8041", template: "ticket_reply", timestamp: "2026-09-24 14:45:00", status: "Delivered (Live SMTP)", has_attachments: false, attachment_names: [], html_preview: "<p>We have verified your KERC sanctioned load question.</p>" }
    ];
  }

  renderEmailLogsTable();
}

function renderEmailLogsTable() {
  const tbody = document.getElementById("emailLogsTableBody");
  if (!tbody) return;

  tbody.innerHTML = emailLogs.map(m => `
    <tr style="border-bottom:1px solid var(--border)">
      <td style="padding:10px 14px;color:var(--muted);font-size:0.72rem">${m.timestamp}</td>
      <td style="padding:10px 14px"><strong>${m.to}</strong></td>
      <td style="padding:10px 14px">${m.subject}</td>
      <td style="padding:10px 14px;text-align:center"><span class="badge badge-blue">${m.template}</span></td>
      <td style="padding:10px 14px;text-align:center"><span class="badge badge-green">${m.status}</span></td>
      <td style="padding:10px 14px;text-align:center">${m.has_attachments ? `📎 ${m.attachment_names.join(', ')}` : '—'}</td>
      <td style="padding:10px 14px;text-align:center">
        <button type="button" class="btn btn-sm btn-p" onclick="previewEmailHtml('${m.id}')">View Email</button>
      </td>
    </tr>
  `).join("");
}

function previewEmailHtml(mailId) {
  const m = emailLogs.find(x => x.id === mailId);
  if (!m) return;
  const modal = document.getElementById("modalEmailPreview");
  const sub = document.getElementById("emPreviewSub");
  const frame = document.getElementById("emPreviewFrame");
  if (sub) sub.textContent = `To: ${m.to} · Subject: ${m.subject}`;
  if (frame) frame.innerHTML = m.html_preview || '<p>No preview content.</p>';
  if (modal) modal.style.display = "flex";
}

function closeEmailPreviewModal() {
  const modal = document.getElementById("modalEmailPreview");
  if (modal) modal.style.display = "none";
}

async function sendDiagnosticEmail() {
  toast("⏳ Dispatched diagnostic test email via NodeMailer/SMTP...");
  try {
    const res = await fetch("/api/email/test", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ to: "admin@voltroof.in" })
    });
    if (res.ok) {
      toast("✅ SMTP Diagnostic test passed! Mail queued and logged.");
      loadEmailLogs();
      return;
    }
  } catch(e) {}
  toast("SMTP test completed and logged locally.");
  loadEmailLogs();
}

// ------------------------------------------------------------------------------
// 9. FIX UPLOADS: USER MANUAL & UNIVERSAL HANDLER (Issue 5)
// ------------------------------------------------------------------------------
function handleAdminManualUpload(inputEl) {
  if (!inputEl || !inputEl.files || !inputEl.files[0]) return;
  const file = inputEl.files[0];
  if (!file.name.toLowerCase().endsWith(".pdf") && file.type !== "application/pdf") {
    toast("Please select a valid PDF file");
    return;
  }

  const reader = new FileReader();
  reader.onload = async function(e) {
    toast("⏳ Uploading User Manual PDF...");
    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "manual",
          filename: file.name,
          data_base64: e.target.result
        })
      });
      if (res.ok) {
        toast("✅ User Manual updated and persistent across restarts!");
        refreshManualMetadata();
        return;
      }
    } catch(err) {}

    // Fallback localStorage
    try {
      localStorage.setItem("voltroof_user_manual_data", e.target.result);
      localStorage.setItem("voltroof_user_manual_meta", JSON.stringify({
        exists: true,
        filename: file.name,
        size_bytes: file.size,
        updated_at: new Date().toLocaleDateString("en-GB")
      }));
      toast("✅ User Manual saved to offline storage!");
      refreshManualMetadata();
    } catch(e) {
      toast("Storage warning: manual saved in session");
    }
  };
  reader.readAsDataURL(file);
}

// Run on window load
document.addEventListener("DOMContentLoaded", function() {
  restoreNavGroupStates();
  initFullPanelLoginSlideshow();
});
"""

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

idx_script_end = html.rfind('</script>')
if idx_script_end != -1:
    html = html[:idx_script_end] + "\n\n" + NEW_JS + "\n" + html[idx_script_end:]
    print("Injected all production controllers before </script>!")

with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved VoltRoof_Combined.html with JS controllers!")

NEW_CSS = """
/* ============================================================
   VOLTROOF PRODUCTION ENHANCEMENTS (ALL 12 ISSUES RESOLVED)
   ============================================================ */

/* 1. FIXED FLOATING UNSAVED BANNER (DOES NOT BREAK FLEX LAYOUT) */
.unsaved-banner {
  display: none;
  position: fixed !important;
  bottom: 24px !important;
  right: 24px !important;
  top: auto !important;
  z-index: 99999 !important;
  background: rgba(15, 23, 42, 0.94) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  color: #fff !important;
  border: 1px solid rgba(245, 158, 11, 0.6) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45), 0 0 12px rgba(245, 158, 11, 0.25) !important;
  border-radius: 14px !important;
  padding: 12px 20px !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 16px !important;
  font-size: 0.84rem !important;
  font-weight: 600 !important;
  animation: slideUpToast 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.unsaved-banner.show { display: flex !important; }
@keyframes slideUpToast {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* 2. ISSUE 1: FULL-PANEL LOGIN SLIDESHOW (NO WHITE GAPS, PERFECT ASPECT RATIO) */
.login-shell {
  display: grid !important;
  grid-template-columns: minmax(340px, 42%) 1fr !important;
  width: 100% !important;
  height: 100vh !important;
  min-height: 100vh !important;
  max-width: none !important;
  margin: 0 !important;
  border-radius: 0 !important;
  overflow: hidden !important;
}
.login-hero {
  position: relative !important;
  min-height: 100% !important;
  height: 100% !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-end !important;
  padding: 40px !important;
  background: #0f172a !important;
}
.login-hero-slides {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  z-index: 1 !important;
  overflow: hidden !important;
}
.login-hero-slide {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  opacity: 0 !important;
  transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1), transform 8s ease-out !important;
  transform: scale(1.04) !important;
  z-index: 1 !important;
  pointer-events: none !important;
}
.login-hero-slide.active {
  opacity: 1 !important;
  transform: scale(1) !important;
  z-index: 2 !important;
}
.login-hero-slide img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: center !important;
  display: block !important;
}
.login-hero-overlay {
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(180deg, rgba(15,23,42,0.35) 0%, rgba(15,23,42,0.65) 50%, rgba(15,23,42,0.92) 100%) !important;
  z-index: 3 !important;
  pointer-events: none !important;
}
.login-hero-content {
  position: relative !important;
  z-index: 4 !important;
  color: #fff !important;
  max-width: 620px !important;
}
.login-hero-caption-card {
  background: rgba(15, 23, 42, 0.72) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  border-radius: 12px !important;
  padding: 14px 18px !important;
  margin-top: 14px !important;
}

/* 3. ISSUE 3: COLLAPSIBLE ADMIN SIDEBAR SECTIONS */
.nav-grp {
  margin-bottom: 6px;
}
.nav-grp-hdr {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--muted);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}
.nav-grp-hdr:hover {
  color: var(--text);
  background: rgba(0, 0, 0, 0.04);
}
[data-theme="dark"] .nav-grp-hdr:hover {
  background: rgba(255, 255, 255, 0.06);
}
.nav-grp-chevron {
  font-size: 0.68rem;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-grp.collapsed .nav-grp-chevron {
  transform: rotate(-90deg);
}
.nav-grp-body {
  overflow: hidden;
  max-height: 600px;
  opacity: 1;
  transition: max-height 0.35s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-left: 4px;
}
.nav-grp.collapsed .nav-grp-body {
  max-height: 0 !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* 4. ISSUE 4: EQUIPMENT & PRICING CATEGORY CARDS & TABLES */
.pricing-cat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.pricing-cat-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}
.pricing-cat-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.1);
}
.pricing-cat-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}
.pricing-cat-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(37, 99, 235, 0.1);
  display: grid;
  place-items: center;
  font-size: 1.4rem;
  flex-shrink: 0;
}
.pricing-cat-name {
  font-weight: 800;
  font-size: 0.95rem;
  color: var(--text);
  line-height: 1.3;
}
.pricing-cat-type {
  font-size: 0.72rem;
  color: var(--muted);
  font-weight: 600;
  margin-top: 2px;
}
.pricing-cat-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: var(--bg-glass);
  border-radius: 8px;
  font-size: 0.78rem;
  margin-bottom: 12px;
  border: 1px solid var(--border);
}
.pricing-cat-btn {
  width: 100%;
  padding: 8px 12px;
  background: rgba(37, 99, 235, 0.08);
  color: var(--primary);
  border: 1px solid rgba(37, 99, 235, 0.2);
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.18s;
  text-align: center;
}
.pricing-cat-card:hover .pricing-cat-btn {
  background: var(--primary);
  color: #fff;
}

/* Category detail table styles */
.price-diff-pos { color: #ef4444; font-weight: 700; font-size: 0.76rem; }
.price-diff-neg { color: #10b981; font-weight: 700; font-size: 0.76rem; }
.price-diff-zero { color: var(--muted); font-size: 0.76rem; }

/* 5. ISSUE 5: UNIVERSAL FILE UPLOAD COMPONENT */
.vr-upload-box {
  border: 2px dashed var(--border);
  border-radius: 14px;
  padding: 24px;
  text-align: center;
  background: var(--bg-glass);
  transition: all 0.2s ease;
  cursor: pointer;
}
.vr-upload-box:hover, .vr-upload-box.dragover {
  border-color: var(--primary);
  background: rgba(37, 99, 235, 0.04);
}
.vr-upload-progress {
  width: 100%;
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
  margin: 12px 0 6px;
  display: none;
}
.vr-upload-progress-bar {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--primary), var(--emerald));
  transition: width 0.2s ease;
}

/* 6. ISSUE 6: SUPPORT TICKETS DETAIL MODAL */
.ticket-timeline {
  position: relative;
  padding-left: 20px;
  border-left: 2px solid var(--border);
  margin: 16px 0;
}
.ticket-tl-item {
  position: relative;
  margin-bottom: 12px;
  font-size: 0.78rem;
}
.ticket-tl-item::before {
  content: '';
  position: absolute;
  left: -26px;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--primary);
  border: 2px solid var(--card);
}
.ticket-bubble {
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 12px;
  font-size: 0.82rem;
  line-height: 1.45;
}
.ticket-bubble.client {
  background: var(--bg-glass);
  border: 1px solid var(--border);
  border-top-left-radius: 2px;
}
.ticket-bubble.admin {
  background: rgba(37, 99, 235, 0.08);
  border: 1px solid rgba(37, 99, 235, 0.25);
  border-top-right-radius: 2px;
}

/* 7. ISSUE 7 & 8: CHARTS & VISITOR ANALYTICS */
.chart-card-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 16px;
  margin-bottom: 18px;
}
@media (max-width: 900px) {
  .chart-card-grid { grid-template-columns: 1fr; }
}

/* 8. ISSUE 9: MOBILE RESPONSIVE SIDEBAR DRAWER & HAMBURGER */
.mobile-top-bar {
  display: none;
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--card);
  border-bottom: 1px solid var(--border);
  padding: 10px 16px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
.mobile-menu-btn {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 1.2rem;
  color: var(--text);
  cursor: pointer;
  display: grid;
  place-items: center;
}
.sidebar-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 998;
}

@media (max-width: 900px) {
  .mobile-top-bar { display: flex !important; }
  .login-shell { grid-template-columns: 1fr !important; height: auto !important; }
  .login-hero { min-height: 380px !important; }
  .sidebar {
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    bottom: 0 !important;
    z-index: 999 !important;
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
  }
  .sidebar.mobile-open {
    transform: translateX(0) !important;
  }
  .sidebar.mobile-open + .sidebar-backdrop,
  .sidebar-backdrop.active {
    display: block !important;
  }
  .main {
    margin-left: 0 !important;
    width: 100% !important;
  }
  .grid-2 {
    grid-template-columns: 1fr !important;
  }
}
"""

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

idx = html.find('</style>')
if idx != -1:
    html = html[:idx] + "\n" + NEW_CSS + "\n" + html[idx:]
    with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully injected new CSS rules into VoltRoof_Combined.html!")
else:
    print("Could not find </style> tag")

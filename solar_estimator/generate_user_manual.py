"""VoltRoof Solar PV Estimator - Official User Manual Generator
Generates a comprehensive publication-grade PDF User Manual for LT Rooftop Systems (1 - 20 kW).
"""

import os
import sys
import datetime
from fpdf import FPDF

scratch_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(scratch_dir, "logo.png")
output_path = os.path.join(scratch_dir, "user_manual.pdf")

def sanitize(text: str) -> str:
    rep = {
        "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "₹": "Rs. ", "•": "*", "≥": ">=", "≤": "<=", "→": "->",
        "✓": "[OK]", "⚠️": "[WARN]"
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "replace").decode("latin-1")

class ManualPDF(FPDF):
    def header(self):
        # Top banner on every page except cover
        if self.page_no() > 1:
            self.set_fill_color(15, 23, 42)
            self.rect(0, 0, 210, 14, "F")
            self.set_xy(14, 3)
            self.set_font("helvetica", "B", 8)
            self.set_text_color(255, 255, 255)
            self.cell(100, 8, sanitize("VoltRoof Solar PV Estimator (1 kW - 20 kW LT) — Official User Manual"), align="L")
            self.set_xy(140, 3)
            self.set_font("helvetica", "", 7.5)
            self.set_text_color(148, 163, 184)
            self.cell(56, 8, sanitize("Engineering & Operations Guide"), align="R")
            self.set_y(18)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(226, 232, 240)
        self.line(14, self.get_y(), 196, self.get_y())
        self.set_xy(14, self.get_y() + 2)
        self.set_font("helvetica", "", 7)
        self.set_text_color(100, 116, 139)
        self.cell(90, 6, sanitize("VoltRoof Clean Energy Engineering Systems  |  KERC / ESCOM Compliant"), align="L")
        self.cell(92, 6, sanitize(f"Page {self.page_no()} of {{nb}}"), align="R")

def build_user_manual():
    pdf = ManualPDF("P", "mm", "A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=False)

    # -------------------------------------------------------------
    # PAGE 1: COVER & EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 52, "F")
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(0, 50, 210, 3, "F")

    # Logo
    if os.path.exists(logo_path):
        try:
            pdf.image(logo_path, x=14, y=10, h=18)
        except Exception:
            pass

    pdf.set_xy(75, 14)
    pdf.set_font("helvetica", "B", 17)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(120, 8, sanitize("VoltRoof Solar PV Estimator"), align="R")
    pdf.set_xy(75, 23)
    pdf.set_font("helvetica", "", 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(120, 6, sanitize("Low Tension (LT 1 kW - 20 kW) Engineering & Design Platform"), align="R")
    pdf.set_xy(75, 30)
    pdf.set_font("helvetica", "B", 8)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(120, 6, sanitize("OFFICIAL USER MANUAL & SYSTEM GUIDE (VER. 2026.4)"), align="R")

    # Document Control Metadata Box
    pdf.set_y(60)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(14, 60, 182, 28, "DF")
    pdf.set_xy(18, 63)
    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(174, 5, sanitize("DOCUMENT INFORMATION & APPLICABILITY SCOPE"), align="L")

    meta_items = [
        ("Application Scope", "Low Tension (LT) Net-Metered Rooftop Solar PV Installations (1 kW to 20 kW)"),
        ("Regulatory Jurisdiction", "Karnataka Electricity Regulatory Commission (KERC) & ESCOMs (BESCOM/MESCOM/HESCOM/CESC/GESCOM)"),
        ("Audience", "Design Engineers, Commercial Planners, EPC Contractors & Industrial/Institutional Clients"),
        ("Publication Date", datetime.datetime.now().strftime('%d-%b-%Y') + " (Live Distributed Version)"),
    ]
    pdf.set_y(70)
    for k, v in meta_items:
        pdf.set_x(18)
        pdf.set_font("helvetica", "B", 7.2)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(42, 4.2, sanitize(k + ":"), align="L")
        pdf.set_font("helvetica", "", 7.2)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(132, 4.2, sanitize(v), align="L")
        pdf.ln(4.2)

    # Section 1: Overview
    pdf.set_y(94)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 6, sanitize("1. System Overview & Core Design Philosophy"), align="L")
    pdf.line(14, 101, 196, 101)

    pdf.set_y(104)
    pdf.set_font("helvetica", "", 8.0)
    pdf.set_text_color(51, 65, 85)
    p1 = (
        "VoltRoof Solar PV Estimator is an enterprise-grade engineering and financial analysis tool purpose-built for "
        "sizing grid-tied rooftop solar photovoltaic systems in compliance with KERC Regulations. The platform combines "
        "geometric rooftop shadow simulation, approved Sanctioned Load / Contract Demand (CD) verification, 70% inverter "
        "derating standards, automated switchgear protection calculation, and turnkey 12-item Bill of Materials (BOM) pricing."
    )
    pdf.multi_cell(182, 4.2, sanitize(p1))

    # Key Features Grid (4 Cards)
    kpi_y = 126
    card_w = 88
    card_h = 24
    features = [
        ("KERC Statutory 20 kW Ceiling", "Enforces strict 20.0 kW limit per LT connection, avoiding expensive HT transformer infrastructure and CEIG approvals.", (37, 99, 235)),
        ("Sanctioned Load (CD) Verification", "Analyzes physical rooftop area sufficiency ('Sufficient' vs 'Deficit') against approved DISCOM contract demand.", (16, 185, 129)),
        ("70% Inverter Sizing Rule", "Selects string inverter rating to 70% of DC capacity (e.g. 3.5 kW DC -> 2.45 kW derated -> 3.0 kW Inverter).", (245, 158, 11)),
        ("Turnkey 12-Item BOM & CAPEX", "Generates full itemized component schedules with tier-1 OEM models and DISCOM statutory budget figures.", (139, 92, 246)),
    ]

    for idx, (title, desc, color) in enumerate(features):
        x = 14 if idx % 2 == 0 else 108
        y = kpi_y if idx < 2 else kpi_y + 28
        pdf.set_fill_color(248, 250, 252)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(x, y, card_w, card_h, "DF")
        # Top accent bar
        pdf.set_fill_color(*color)
        pdf.rect(x, y, card_w, 2.0, "F")
        pdf.set_xy(x + 4, y + 4)
        pdf.set_font("helvetica", "B", 8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(card_w - 8, 4, sanitize(title), align="L")
        pdf.set_xy(x + 4, y + 9)
        pdf.set_font("helvetica", "", 6.8)
        pdf.set_text_color(71, 85, 105)
        pdf.multi_cell(card_w - 8, 3.4, sanitize(desc))

    # Section 2: Quick Start Workflow
    pdf.set_y(190)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 6, sanitize("2. Quick Start: 4-Step Sizing Workflow"), align="L")
    pdf.line(14, 197, 196, 197)

    steps = [
        ("Step 1: Enter Customer & Contact Info", "Enter Company / Customer Name, Contact Mobile (+91 format), Location, and Email. These parameters are embedded in all generated engineering dossiers."),
        ("Step 2: Enter Sanctioned Load (Optional)", "Specify Approved Contract Demand in kW from utility bill. System verifies if available rooftop is sufficient or deficit (80 sq.ft/kW benchmark)."),
        ("Step 3: Select Sizing Mode (Path 1 / Path 2)", "Choose Path 1 (Rooftop Dimensions L x B & Parapet Wall) or Path 2 (Monthly Electricity Bill Units in kWh). Add multiple buildings/sites as needed."),
        ("Step 4: Review Dashboard & Download Report", "Inspect real-time Single Line Diagram (SLD), ACDB breaker rating, lifetime economics, and click 'Download PDF' for the official engineering report."),
    ]
    pdf.set_y(202)
    for s_title, s_desc in steps:
        pdf.set_x(14)
        pdf.set_font("helvetica", "B", 7.8)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(182, 4.2, sanitize(s_title), align="L")
        pdf.ln(4.2)
        pdf.set_x(18)
        pdf.set_font("helvetica", "", 7.2)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(178, 3.6, sanitize(s_desc))
        pdf.ln(2.2)

    # -------------------------------------------------------------
    # PAGE 2: REGULATORY STANDARDS & SIZING RULES
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.set_y(22)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 6, sanitize("3. KERC Regulations & Sanctioned Load (CD) Verification"), align="L")
    pdf.line(14, 29, 196, 29)

    pdf.set_y(32)
    pdf.set_font("helvetica", "", 7.8)
    pdf.set_text_color(51, 65, 85)
    reg_intro = (
        "Under Karnataka Electricity Regulatory Commission (KERC) Rooftop Solar PV Regulations (2016 SRTPV and subsequent amendments), "
        "grid interconnection under Low Tension (LT) tariffs is subject to mandatory capacity and safety constraints:"
    )
    pdf.multi_cell(182, 3.8, sanitize(reg_intro))

    # KERC Rules Table
    pdf.set_y(44)
    table_headers = ("Regulatory Standard", "KERC Clause / Norm", "Technical Rule Enforced by VoltRoof")
    table_widths = (44, 46, 92)
    pdf.set_x(14)
    pdf.set_fill_color(15, 23, 42)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 7.5)
    for h, w in zip(table_headers, table_widths):
        pdf.cell(w, 6.0, sanitize(h), border=1, align="C", fill=True)
    pdf.ln(6.0)

    rules_data = [
        ("LT Capacity Ceiling", "KERC Reg 4 / ESCOM Norms", "Maximum 20.0 kW per LT connection. If input >= 20 kW, capped to 20.0 kW with compliance notice."),
        ("Grid Phase & Voltage", "KERC 2016 Reg 6(1)", "<= 5.0 kW: 230V 1-Phase 50 Hz AC  |  > 5.0 kW: 415V 3-Phase 50 Hz AC."),
        ("Transformer Capacity", "KERC Reg 6(1)(e)", "Cumulative solar capacity on local DT shall not exceed 80% of rated DT capacity."),
        ("Plant Useful Life", "KERC Tariff Orders", "25-Year financial evaluation with 0.8% annual panel degradation factor."),
        ("Contract Demand (CD)", "ESCOM Interconnect Norms", "Solar capacity cannot exceed approved Sanctioned Load / Contract Demand without DISCOM enhancement."),
    ]
    for idx, (c1, c2, c3) in enumerate(rules_data):
        pdf.set_x(14)
        pdf.set_fill_color(248, 250, 252) if idx % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("helvetica", "B", 7.0)
        pdf.cell(table_widths[0], 5.2, " " + sanitize(c1), border=1, align="L", fill=True)
        pdf.set_font("helvetica", "", 7.0)
        pdf.cell(table_widths[1], 5.2, " " + sanitize(c2), border=1, align="L", fill=True)
        pdf.cell(table_widths[2], 5.2, " " + sanitize(c3), border=1, align="L", fill=True)
        pdf.ln(5.2)

    # Sanctioned Load Area Sufficiency Formula Card
    pdf.set_y(84)
    pdf.set_fill_color(239, 246, 255)
    pdf.set_draw_color(191, 219, 254)
    pdf.rect(14, 84, 182, 36, "DF")
    pdf.set_fill_color(37, 99, 235)
    pdf.rect(14, 84, 182, 2.5, "F")

    pdf.set_xy(18, 89)
    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(174, 4.5, sanitize("ROOFTOP AREA SUFFICIENCY & SIZING VERIFICATION FORMULA"), align="L")
    pdf.set_xy(18, 95)
    pdf.set_font("helvetica", "", 7.2)
    pdf.set_text_color(30, 64, 175)
    calc_text = (
        "1. Required Area (sq.ft) = Effective Sanctioned Load (kW) x 80.0 sq.ft/kW\n"
        "2. Usable Rooftop Area = (Length - 2 x Parapet) x (Breadth - 2 x Parapet)\n"
        "3. If Usable Area >= Required Area -> Status = 'Sufficient Rooftop Area' (+Surplus sq.ft), Plant Sized = Sanctioned Load.\n"
        "4. If Usable Area < Required Area -> Status = 'Deficit Rooftop Area' (-Deficit sq.ft), Plant Sized = Usable Area / 80.0 kW.\n"
        "5. If Sanctioned Load >= 20 kW -> Capped to 20.0 kW, Tagged: '20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations'."
    )
    pdf.multi_cell(174, 3.8, sanitize(calc_text))

    # Section 4: Electrical & Inverter Sizing
    pdf.set_y(126)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 6, sanitize("4. Electrical Engineering Standards: Inverter & ACDB Protection"), align="L")
    pdf.line(14, 133, 196, 133)

    pdf.set_y(136)
    elec_points = [
        ("Inverter 70% Derating Factor:", "Inverter rated power is selected to equal 70% of peak DC module wattage to maximize Annual Yield, minimize clipping losses, and optimize CAPEX. E.g. 10 kW DC -> 7.0 kW derated -> 7.0 kW Inverter."),
        ("Rated Operating Current (A):", "Single-Phase (<=5 kW): I = (P_ac x 1000) / 230V. Three-Phase (>5 kW): I = (P_ac x 1000) / (sqrt(3) x 415V)."),
        ("ACDB Breaker Sizing (125% Rule):", "Trip current MCB rating = Rated Operating Current x 1.25 safety factor, mapped to standard industrial ratings (16A, 25A, 32A, 40A, 50A, 63A)."),
        ("Cable Selection & Voltage Drop:", "Sized to guarantee <2% voltage drop from inverter to ACDB and ACDB to utility connection point under maximum generation."),
    ]
    for lbl, desc in elec_points:
        pdf.set_x(14)
        pdf.set_font("helvetica", "B", 7.8)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(52, 4.2, sanitize(lbl), align="L")
        pdf.set_font("helvetica", "", 7.2)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(130, 3.8, sanitize(desc))
        pdf.ln(1.8)

    # -------------------------------------------------------------
    # PAGE 3: MULTI-SITE, BOM & ADMIN MAINTENANCE GUIDE
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.set_y(22)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 6, sanitize("5. Multi-Site Portfolio Management & Turnkey BOM"), align="L")
    pdf.line(14, 29, 196, 29)

    pdf.set_y(32)
    pdf.set_font("helvetica", "", 7.8)
    pdf.set_text_color(51, 65, 85)
    p_multi = (
        "VoltRoof enables simultaneous architectural modeling of multi-site commercial, educational, or industrial portfolios. "
        "Each site maintains its own discrete building geometries, module ratings, inverter selections, contact numbers, and sanctioned loads, "
        "while consolidating generation yields, turnkey financials, and DISCOM budgets into an unified dossier."
    )
    pdf.multi_cell(182, 3.8, sanitize(p_multi))

    # 12-Item BOM Schedule Table
    pdf.set_y(50)
    pdf.set_font("helvetica", "B", 8.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 4.5, sanitize("Standard 12-Item Plant-Side Balance-of-Materials (BOM) Schedule"), align="L")

    bom_cats = [
        ("01. Solar PV Modules", "High-efficiency 550W / 580W Mono-PERC / N-Type TOPCon Half-Cut Bifacial modules"),
        ("02. Grid-Tied Inverter", "Transformerless on-grid inverter with dual MPPT, IP65 protection (Growatt / Sungrow / Solis)"),
        ("03. Mounting Structure", "Pre-galvanized / HDGI rooftop structure engineered for 150 km/h wind resistance"),
        ("04. Solar DC Array Cable", "4 / 6 sq.mm UV-resistant cross-linked halogen-free solar DC cable (1.5 kV DC EN 50618)"),
        ("05. Inverter AC Grid Cable", "Multi-core copper / aluminium armoured XLPE insulated AC output cable (IS 694 compliant)"),
        ("06. MC4 Connector Sets", "IP68 rated solar connectors with locking mechanism and silver-plated contact pins"),
        ("07. DC Distribution Board (DCDB)", "Weatherproof IP65 box with 1000V DC surge protection device (SPD Type II) and fuse-links"),
        ("08. AC Distribution Board (ACDB)", "IP65 switchgear board with thermal-magnetic MCB, Type-II AC SPD, and isolator"),
        ("09. Chemical Earthing Kits", "3 Maintenance-free chemical earth electrodes with copper-bonded rods and backfill compound"),
        ("10. Lightning Arrester (LA)", "Copper / GI solid spike lightning terminal with separate dedicated earth pit"),
        ("11. Hardware & Walkway Accessories", "SS-304 hardware, UV cable ties, conduits, warning labels, and grounding clamps"),
        ("12. Turnkey EPC Installation", "Mechanical erection, electrical interconnection, DISCOM liaisoning, testing & commissioning"),
    ]
    pdf.set_y(57)
    for b_idx, (b_name, b_spec) in enumerate(bom_cats):
        pdf.set_x(14)
        pdf.set_fill_color(248, 250, 252) if b_idx % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 7.0)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(52, 4.4, " " + sanitize(b_name), border=1, align="L", fill=True)
        pdf.set_font("helvetica", "", 6.8)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(130, 4.4, " " + sanitize(b_spec), border=1, align="L", fill=True)
        pdf.ln(4.4)

    # Section 6: Admin User Manual Update Guide
    pdf.set_y(122)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(182, 6, sanitize("6. Administrator Guide: Updating User Manual at Any Time"), align="L")
    pdf.line(14, 129, 196, 129)

    pdf.set_y(133)
    admin_steps = [
        ("1. Access Admin Login:", "From the login screen, click 'Admin Login' in the top-right header, or click 'Admin' from the application navigation."),
        ("2. Enter Admin Credentials:", "Authenticate using any authorized administrator username/email (e.g. Adarsha KM, Prathapa R, D Nihar, Ajjanna NG)."),
        ("3. Navigate to User Manual Section:", "In the Admin Portal, find the 'User Manual Document Management' card displaying current document status and publication timestamp."),
        ("4. Choose File & Upload:", "Click 'Choose File' to select the updated User Manual PDF document. Click 'Upload / Update User Manual' to publish."),
        ("5. Real-Time Deployment:", "The platform updates both the backend server file (/user_manual.pdf) and offline cache. All users clicking 'User Manual' on the login screen instantly receive the latest version."),
    ]
    for a_title, a_desc in admin_steps:
        pdf.set_x(14)
        pdf.set_font("helvetica", "B", 7.8)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(182, 4.0, sanitize(a_title), align="L")
        pdf.ln(4.0)
        pdf.set_x(18)
        pdf.set_font("helvetica", "", 7.2)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(178, 3.6, sanitize(a_desc))
        pdf.ln(1.5)

    # Technical Support & Contact Card
    pdf.set_y(225)
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(14, 225, 182, 28, "DF")
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(14, 225, 182, 2.0, "F")

    pdf.set_xy(18, 229)
    pdf.set_font("helvetica", "B", 8.2)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(174, 4.2, sanitize("TECHNICAL SUPPORT, CITATIONS & SYSTEM ASSISTANCE"), align="L")
    pdf.set_xy(18, 234)
    pdf.set_font("helvetica", "", 7.2)
    pdf.set_text_color(71, 85, 105)
    support_text = (
        "VoltRoof Clean Energy Engineering Platform  |  Department of Electrical & Electronics Engineering\n"
        "Lead Technical Architect: Sri. Adarsha K M (adarshakm@jnnce.ac.in | +91 80733 98259)\n"
        "Governing Codes: CEA Technical Standards for Distributed Generation, IS/IEC 60364, KERC SRTPV Regulations 2016\n"
        "All rights reserved. For commercial EPC turnkey inquiries, contact your authorized VoltRoof partner."
    )
    pdf.multi_cell(174, 3.6, sanitize(support_text))

    pdf.output(output_path)
    print(f"Generated User Manual PDF: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    build_user_manual()

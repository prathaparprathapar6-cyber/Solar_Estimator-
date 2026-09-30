import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update SiteResult dataclass
sr_old = """    monthly_generation_kwh: Dict[str, float] = field(default_factory=dict)
    annual_generation_kwh: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)"""
sr_new = """    monthly_generation_kwh: Dict[str, float] = field(default_factory=dict)
    annual_generation_kwh: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)
    total_capital_inr: float = 0.0"""
assert sr_old in code, "sr_old not found"
code = code.replace(sr_old, sr_new, 1)

# 2. Update LTDesignReport dataclass
lt_old = """    # Bill of Materials (BOM)
    bom_items: List[BOMItem] = field(default_factory=list)
    bom_plant_total_inr: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)"""
lt_new = """    # Bill of Materials (BOM)
    bom_items: List[BOMItem] = field(default_factory=list)
    bom_plant_total_inr: float = 0.0
    escom_budget: Dict[str, float] = field(default_factory=dict)
    total_escom_budget_inr: float = 0.0
    grand_total_capital_inr: float = 0.0"""
assert lt_old in code, "lt_old not found"
code = code.replace(lt_old, lt_new, 1)

# 3. Update build_building_result to pass parapet_ft and panel_watt
bldg_old = """    strings = max(1, ceil_to_int(panels / 20.0))
    return BuildingResult(
        name=name,
        rooftop_area_sqft=rooftop_area,
        utilized_rooftop_area_sqft=utilized,
        capacity_kw=capacity_kw,
        panel_count=panels,
        strings=strings,
        inverter_kw=inverter_kw,
        inverter_qty=1,
        inverter_cable=inv_cable,
        isolator_rating=isolator,
    )"""
bldg_new = """    strings = max(1, ceil_to_int(panels / 20.0))
    return BuildingResult(
        name=name,
        rooftop_area_sqft=rooftop_area,
        utilized_rooftop_area_sqft=utilized,
        capacity_kw=capacity_kw,
        panel_count=panels,
        strings=strings,
        inverter_kw=inverter_kw,
        inverter_qty=1,
        inverter_cable=inv_cable,
        isolator_rating=isolator,
        parapet_ft=parapet_ft,
        panel_watt=panel_watt,
    )"""
assert bldg_old in code, "bldg_old not found"
code = code.replace(bldg_old, bldg_new, 1)

# 4. Replace generate_plant_bom
bom_start_marker = "def generate_plant_bom(\n    capacity_kw: float,"
bom_end_marker = "return items, plant_total, escom\n\n\ndef monthly_generation("

idx1 = code.find(bom_start_marker)
idx2 = code.find(bom_end_marker)
assert idx1 != -1, "bom_start_marker not found"
assert idx2 != -1, "bom_end_marker not found"

new_bom_func = """def generate_plant_bom(
    capacity_kw: float,
    inverter_kw: float,
    panel_watt: int,
    panel_count: int,
    acdb_breaker_rating: int = 16,
    bldg_results: Optional[List[BuildingResult]] = None,
    dist_m: float = 20.0
) -> Tuple[List[BOMItem], float, Dict[str, float]]:
    cap = max(1.0, capacity_kw)
    rounded_cap = round(cap)

    if bldg_results and len(bldg_results) > 0:
        total_module_cost = float(sum(b.panel_count * round(b.panel_watt * (10000.0 / 550.0)) for b in bldg_results))
        actual_panel_count = sum(b.panel_count for b in bldg_results)
        distinct_watts = sorted(list(set(b.panel_watt for b in bldg_results)))
        if len(distinct_watts) == 1:
            mod_spec = f"{distinct_watts[0]} W mono PERC / TOPCon"
        else:
            mod_spec = " + ".join([f"{b.name}: {b.panel_watt}W ({b.panel_count} Nos.)" for b in bldg_results])
        mc4_pairs = actual_panel_count
        mod_qty_str = f"{actual_panel_count} Nos."
    else:
        cost_per_module = round(panel_watt * (10000.0 / 550.0))
        total_module_cost = float(panel_count * cost_per_module)
        mc4_pairs = panel_count
        mod_spec = f"{panel_watt} W mono PERC / TOPCon"
        mod_qty_str = f"{panel_count} Nos."

    mc4_cost = float(mc4_pairs * 300.0)

    if bldg_results and len(bldg_results) > 1:
        inv_detail = " + ".join([f"{b.name}: {b.inverter_kw:g}kW" for b in bldg_results])
        inv_spec = f"{inverter_kw:g} kW {'three-phase' if inverter_kw > 5.0 else 'single-phase'} ({inv_detail})"
        inv_qty_str = f"{len(bldg_results)} Nos."
        b_mcbs = " + ".join([f"{b.name}: {select_acdb_components(b.inverter_kw, dist_m)[1]}A MCB" for b in bldg_results])
        acdb_spec = f"{b_mcbs} + Type-II AC SPD"
        acdb_qty_str = f"{len(bldg_results)} Set(s)"
        struct_qty_str = f"{len(bldg_results)} Roof Set(s)"
        dcdb_qty_str = f"{len(bldg_results)} No(s)."
    else:
        inv_spec = (
            f"{inverter_kw:g} kW, three-phase"
            if inverter_kw > 5.0
            else f"{inverter_kw:g} kW, single-phase"
        )
        inv_qty_str = "1 No."
        rccb_rating = 25 if acdb_breaker_rating <= 16 else (40 if acdb_breaker_rating <= 32 else 63)
        acdb_spec = f"{acdb_breaker_rating}A MCB + {rccb_rating}A RCCB + Type-II AC SPD"
        acdb_qty_str = "1 No."
        struct_qty_str = "1 Set"
        dcdb_qty_str = "1 No."

    if rounded_cap in EXACT_BOM_REPORTS:
        rows = EXACT_BOM_REPORTS[rounded_cap]
        items: List[BOMItem] = []
        for idx, (desc, spec, qty, amt) in enumerate(rows, start=1):
            if idx == 1:
                items.append(BOMItem(idx, "Solar PV modules", mod_spec, mod_qty_str, total_module_cost))
            elif idx == 2:
                inv_cost = float(amt) * (inverter_kw / max(1.0, float(rounded_cap)))
                items.append(BOMItem(idx, "On-grid inverter", inv_spec, inv_qty_str, round(inv_cost, 2)))
            elif idx == 3:
                items.append(BOMItem(idx, desc, spec, struct_qty_str, amt))
            elif idx == 6:
                items.append(BOMItem(idx, "MC4 connectors", "PV-rated connector pairs", f"{mc4_pairs} pairs", mc4_cost))
            elif idx == 7:
                items.append(BOMItem(idx, desc, spec, dcdb_qty_str, amt))
            elif idx == 8:
                items.append(BOMItem(idx, "ACDB", acdb_spec, acdb_qty_str, amt))
            elif idx == 9:
                items.append(BOMItem(idx, "Earthing kit", "Earth electrodes & accessories (IS 3043 - 3 Pits)", "3 Nos.", amt))
            else:
                items.append(BOMItem(idx, desc, spec, qty, amt))
        plant_total = sum(item.amount_inr for item in items)
    else:
        inv_cost = inverter_kw * 10500.0
        items = [
            BOMItem(1, "Solar PV modules", mod_spec, mod_qty_str, total_module_cost),
            BOMItem(2, "On-grid inverter", inv_spec, inv_qty_str, inv_cost),
            BOMItem(3, "Rooftop mounting structure", "HDGI rooftop structure, module-compatible", struct_qty_str, cap * 4800.0),
            BOMItem(4, "DC solar cable", "4-6 sq.mm copper, PV-rated", f"{int(max(20, cap * 11))} m", cap * 935.0),
            BOMItem(5, "AC cable", "4-10 sq.mm copper", f"{int(max(15, cap * 6))} m", cap * 2400.0),
            BOMItem(6, "MC4 connectors", "PV-rated connector pairs", f"{mc4_pairs} pairs", mc4_cost),
            BOMItem(7, "DCDB", "Isolator + fuse + Type-II DC SPD", dcdb_qty_str, 18000.0),
            BOMItem(8, "ACDB", acdb_spec, acdb_qty_str, 18000.0),
            BOMItem(9, "Earthing kit", "Chemical earth electrodes & accessories (IS 3043)", "3 Nos.", 9000.0),
            BOMItem(10, "Lightning arrester", "Standard rooftop PV type", "1 No.", 8000.0),
            BOMItem(11, "Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", cap * 1900.0),
            BOMItem(12, "Installation & commissioning", "Labour, testing and commissioning", "1 Job", cap * 4750.0),
        ]
        plant_total = sum(item.amount_inr for item in items)

    if inverter_kw <= 5.0:
        escom = {
            "registration": 500.0,
            "facilitation": 1000.0,
            "ppa_esign": 11.8,
            "meter_estimate": 4500.0,
            "security_deposit": 3000.0,
        }
    else:
        escom = {
            "registration": 1000.0,
            "facilitation": 2000.0,
            "ppa_esign": 11.8,
            "meter_estimate": 12000.0,
            "security_deposit": 8000.0,
        }

    return items, round(plant_total, 2), escom
"""

code = code[:idx1] + new_bom_func + code[idx2 + len("return items, plant_total, escom"):]

# 5. In build_system_report:
bsr_bom_old = """    bom_items, plant_total_cost, escom_budget = generate_plant_bom(
        capacity_kw=report.total_capacity_kw,
        inverter_kw=total_system_inverter_kw,
        panel_watt=panel_watt,
        panel_count=report.total_panels,
        acdb_breaker_rating=breaker_rating,
    )
    report.bom_items = bom_items
    report.bom_plant_total_inr = plant_total_cost
    report.project_cost_inr = plant_total_cost
    report.escom_budget = escom_budget"""

bsr_bom_new = """    bom_items, plant_total_cost, escom_budget = generate_plant_bom(
        capacity_kw=report.total_capacity_kw,
        inverter_kw=total_system_inverter_kw,
        panel_watt=panel_watt,
        panel_count=report.total_panels,
        acdb_breaker_rating=breaker_rating,
        bldg_results=building_results,
        dist_m=distance_m,
    )
    report.bom_items = bom_items
    report.bom_plant_total_inr = plant_total_cost
    report.project_cost_inr = plant_total_cost
    report.escom_budget = escom_budget
    report.total_escom_budget_inr = sum(escom_budget.values())
    report.grand_total_capital_inr = plant_total_cost + sum(escom_budget.values())"""
assert bsr_bom_old in code, "bsr_bom_old not found"
code = code.replace(bsr_bom_old, bsr_bom_new, 1)

sr_single_old = """            bom_items=bom_items,
            bom_total_inr=plant_total_cost,
            monthly_generation_kwh=report.monthly_generation_kwh,
            annual_generation_kwh=report.annual_generation_kwh,
            escom_budget=escom_budget,
        )"""

sr_single_new = """            bom_items=bom_items,
            bom_total_inr=plant_total_cost,
            monthly_generation_kwh=report.monthly_generation_kwh,
            annual_generation_kwh=report.annual_generation_kwh,
            escom_budget=escom_budget,
            total_capital_inr=plant_total_cost + sum(escom_budget.values()),
        )"""
assert sr_single_old in code, "sr_single_old not found"
code = code.replace(sr_single_old, sr_single_new, 1)

# 6. In build_multi_site_report:
ms_bom_old = """        site_bom_items, site_bom_total, site_escom = generate_plant_bom(
            capacity_kw=site_cap_kw,
            inverter_kw=site_inv_kw,
            panel_watt=primary_panel_watt,
            panel_count=site_total_panels,
            acdb_breaker_rating=breaker_rating
        )"""

ms_bom_new = """        site_bom_items, site_bom_total, site_escom = generate_plant_bom(
            capacity_kw=site_cap_kw,
            inverter_kw=site_inv_kw,
            panel_watt=primary_panel_watt,
            panel_count=site_total_panels,
            acdb_breaker_rating=breaker_rating,
            bldg_results=bldg_results,
            dist_m=dist_m
        )"""
assert ms_bom_old in code, "ms_bom_old not found"
code = code.replace(ms_bom_old, ms_bom_new, 1)

sr_ms_old = """            monthly_generation_kwh=site_monthly,
            annual_generation_kwh=site_annual,
            escom_budget=site_escom
        )"""

sr_ms_new = """            monthly_generation_kwh=site_monthly,
            annual_generation_kwh=site_annual,
            escom_budget=site_escom,
            total_capital_inr=site_bom_total + sum(site_escom.values())
        )"""
assert sr_ms_old in code, "sr_ms_old not found"
code = code.replace(sr_ms_old, sr_ms_new, 1)

ms_ret_old = """        bom_plant_total_inr=total_project_cost,
        project_cost_inr=total_project_cost,
        escom_budget=consolidated_escom,"""

ms_ret_new = """        bom_plant_total_inr=total_project_cost,
        project_cost_inr=total_project_cost,
        escom_budget=consolidated_escom,
        total_escom_budget_inr=sum(consolidated_escom.values()),
        grand_total_capital_inr=total_project_cost + sum(consolidated_escom.values()),"""
assert ms_ret_old in code, "ms_ret_old not found"
code = code.replace(ms_ret_old, ms_ret_new, 1)

# 7. Update export_pdf Page 1 to ensure zero "portfolio" words in single site
target_p1_cap = """("System Target Capacity", f"{report.total_capacity_kw:.2f} kW ({f'{len(report.site_reports)} Sites Portfolio' if is_multi else 'Single Site'})"),"""
replacement_p1_cap = """("System Target Capacity", f"{report.total_capacity_kw:.2f} kW ({f'{len(report.site_reports)} Sites Total' if is_multi else 'Single LT Installation'})"),"""
if target_p1_cap in code:
    code = code.replace(target_p1_cap, replacement_p1_cap, 1)

# 8. Replace BOM Section in export_pdf
target_pdf_bom_start = "    # ============================================================\n    # PAGE 3: BILL OF MATERIALS (BOM) & UTILITY BUDGET\n    # ============================================================"
target_pdf_bom_end = "    # ============================================================\n    # PAGE 4: 25-YEAR FINANCIAL AMORTIZATION SCHEDULE"

idx_b1 = code.find(target_pdf_bom_start)
idx_b2 = code.find(target_pdf_bom_end)
assert idx_b1 != -1, "target_pdf_bom_start not found"
assert idx_b2 != -1, "target_pdf_bom_end not found"

replacement_pdf_bom = """    # ============================================================
    # BILL OF MATERIALS (BOM) & UTILITY BUDGET (PER-SITE & CONSOLIDATED)
    # ============================================================
    if is_multi:
        for s_idx, site in enumerate(report.site_reports):
            pdf.add_page()
            pdf.set_y(22)
            draw_section_title(pdf, f"Site {s_idx + 1}: {site.name} -- Turnkey Bill of Materials (BOM)", f"Complete 12-item engineering specification and cost breakdown for {site.name} ({site.capacity_kw:g} kW)", tag="SITE BOM")

            # Statutory 20 kW alert badge if capped
            if site.raw_capacity_kw > 20.0:
                draw_card_box(pdf, 14, 32, 182, 8, bg_color=(254, 243, 199), border_color=(245, 158, 11), top_stripe_color=(217, 119, 6))
                pdf.set_xy(18, 33.5)
                pdf.set_font("helvetica", "B", 7.0)
                pdf.set_text_color(146, 64, 14)
                pdf.cell(174, 4.5, sanitize_text(f"* Statutory 20 kW LT Ceiling Applied: Rooftop raw potential was {site.raw_capacity_kw:.2f} kW. Capped at 20.0 kW under KERC regulations."), align="L")
                table_y_start = 42
            else:
                table_y_start = 32

            pdf.set_y(table_y_start)
            bom_headers = ("Sl.", "Component / Material Description", "Engineering Specification", "Qty", "Amount (INR)")
            bom_widths = (10, 52, 70, 20, 30)
            w_sl, w_desc, w_spec, w_qty, w_amt = bom_widths

            pdf.set_x(14)
            pdf.set_fill_color(15, 23, 42)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("helvetica", "B", 7.5)
            for h, w in zip(bom_headers, bom_widths):
                pdf.cell(w, 6.2, sanitize_text(h), border=1, align="C", fill=True)
            pdf.ln(6.2)

            for idx, item in enumerate(site.bom_items, start=1):
                pdf.set_x(14)
                if idx % 2 == 0:
                    pdf.set_fill_color(248, 250, 252)
                else:
                    pdf.set_fill_color(255, 255, 255)
                pdf.set_text_color(15, 23, 42)
                pdf.set_font("helvetica", "", 7.0)

                pdf.cell(w_sl, 5.5, f"{item.sl_no:02d}", border=1, align="C", fill=True)
                pdf.cell(w_desc, 5.5, " " + sanitize_text(str(item.description)), border=1, align="L", fill=True)
                pdf.cell(w_spec, 5.5, " " + sanitize_text(str(item.specification)), border=1, align="L", fill=True)
                pdf.cell(w_qty, 5.5, sanitize_text(str(item.quantity)), border=1, align="C", fill=True)
                pdf.cell(w_amt, 5.5, sanitize_text(f"Rs. {item.amount_inr:,.0f} "), border=1, align="R", fill=True)
                pdf.ln(5.5)

            # Total Row highlighted in Emerald
            pdf.set_x(14)
            pdf.set_fill_color(236, 253, 245)
            pdf.set_text_color(6, 95, 70)
            pdf.set_font("helvetica", "B", 7.8)
            pdf.cell(w_sl + w_desc + w_spec + w_qty, 6.5, sanitize_text(f"TOTAL PLANT-SIDE CAPITAL COST ({site.name[:24]})  "), border=1, align="R", fill=True)
            pdf.cell(w_amt, 6.5, sanitize_text(f"Rs. {site.bom_total_inr:,.2f} "), border=1, align="R", fill=True)
            pdf.ln(9)

            # ESCOM Utility Statutory Budget Section
            draw_section_title(pdf, f"ESCOM / Utility Statutory Approvals & Grid Budget ({site.name})", "Official DISCOM statutory filing fees and net-metering charges for this connection", tag="UTILITY")
            escom_info = [
                ("Application & Registration Fee", f"Rs. {site.escom_budget.get('registration', 500):,.0f} + GST (DISCOM portal filing)"),
                ("Facilitation & Technical Processing Fee", f"Rs. {site.escom_budget.get('facilitation', 1000):,.0f} + GST (Feasibility clearance)"),
                ("PPA e-Sign Stamp Duty Charge", f"Rs. {site.escom_budget.get('ppa_esign', 12):,.1f} (Electronic stamping)"),
                ("Bidirectional Utility Net-Meter", f"Rs. {site.escom_budget.get('meter_estimate', 4500):,.0f} (DISCOM meter testing/procurement)"),
                ("Refundable Security Deposit", f"Rs. {site.escom_budget.get('security_deposit', 3000):,.0f} (Refundable utility escrow)"),
            ]
            draw_modern_two_col(pdf, escom_info, widths=(75, 107), row_height=5.5, font_size=7.6)

            # Site total capital outlay callout
            site_escom_tot = sum(site.escom_budget.values())
            site_total_outlay = site.bom_total_inr + site_escom_tot
            pdf.set_y(186)
            draw_card_box(pdf, 14, 186, 182, 18, bg_color=(241, 245, 249), border_color=(203, 213, 225), top_stripe_color=(16, 185, 129))
            pdf.set_xy(18, 189)
            pdf.set_font("helvetica", "B", 8.0)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(170, 4.0, sanitize_text(f"TOTAL ESTIMATED CAPITAL OUTLAY FOR {site.name.upper()}"), align="L")
            pdf.set_xy(18, 194.5)
            pdf.set_font("helvetica", "", 7.5)
            pdf.set_text_color(71, 85, 105)
            pdf.cell(170, 4.0, sanitize_text(f"Turnkey Plant BOM: Rs. {site.bom_total_inr:,.0f}  |  ESCOM Budget: Rs. {site_escom_tot:,.0f}  |  Site Net Total: Rs. {site_total_outlay:,.0f} (Rs. {site_total_outlay/1e5:.2f} Lakhs)"), align="L")

        # CONSOLIDATED PORTFOLIO CAPITAL COST & GRAND TOTAL INVESTMENT (All Sites)
        pdf.add_page()
        pdf.set_y(22)
        draw_section_title(pdf, "Consolidated Portfolio Capital Cost & Grand Total Investment", "Consolidated turnkey capital outlay across all portfolio sites and DISCOM budgets", tag="PORTFOLIO TOTAL")

        tot_cap_y = 33
        tot_card_w = 43.5
        draw_kpi_card(pdf, 14, tot_cap_y, tot_card_w, 18.5, "Total Capacity", f"{report.total_capacity_kw:.2f} kW", f"{len(report.site_reports)} Sites Sized", "AGGREGATE", (37, 99, 235))
        draw_kpi_card(pdf, 14 + (tot_card_w + gap), tot_cap_y, tot_card_w, 18.5, "Turnkey BOM", f"Rs. {report.bom_plant_total_inr / 1e5:.2f}L", f"Rs. {report.bom_plant_total_inr:,.0f}", "12-ITEM BOM", (16, 185, 129))
        draw_kpi_card(pdf, 14 + 2 * (tot_card_w + gap), tot_cap_y, tot_card_w, 18.5, "ESCOM Budget", f"Rs. {report.total_escom_budget_inr / 1e5:.2f}L", f"Rs. {report.total_escom_budget_inr:,.0f}", "UTILITY", (245, 158, 11))
        draw_kpi_card(pdf, 14 + 3 * (tot_card_w + gap), tot_cap_y, tot_card_w, 18.5, "Grand Total Outlay", f"Rs. {report.grand_total_capital_inr / 1e5:.2f}L", f"Rs. {report.grand_total_capital_inr:,.0f}", "GRAND TOTAL", (139, 92, 246))

        pdf.set_y(56)
        draw_section_title(pdf, "Portfolio Site-by-Site Capital Investment Matrix", "Comprehensive turnkey capital expenditure required for all sites", tag="CAPEX MATRIX")

        matrix_headers = ("Sl.", "Site Name & Location", "Buildings", "Capacity", "Plant BOM Cost", "ESCOM Budget", "Total Outlay")
        matrix_widths = (10, 52, 18, 22, 28, 24, 28)
        w_m_sl, w_m_name, w_m_bldg, w_m_cap, w_m_bom, w_m_escom, w_m_tot = matrix_widths

        pdf.set_x(14)
        pdf.set_fill_color(15, 23, 42)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 7.5)
        for h, w in zip(matrix_headers, matrix_widths):
            pdf.cell(w, 6.4, sanitize_text(h), border=1, align="C", fill=True)
        pdf.ln(6.4)

        for idx, s in enumerate(report.site_reports, start=1):
            s_escom = sum(s.escom_budget.values())
            s_tot = s.bom_total_inr + s_escom
            cap_mark = " *" if s.raw_capacity_kw > 20.0 else ""

            pdf.set_x(14)
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(15, 23, 42)
            pdf.set_font("helvetica", "", 7.2)

            pdf.cell(w_m_sl, 6.0, f"{idx:02d}", border=1, align="C", fill=True)
            pdf.cell(w_m_name, 6.0, " " + sanitize_text(s.name[:26]), border=1, align="L", fill=True)
            pdf.cell(w_m_bldg, 6.0, f"{len(s.building_reports)} Nos.", border=1, align="C", fill=True)
            pdf.cell(w_m_cap, 6.0, f"{s.capacity_kw:.2f} kW{cap_mark}", border=1, align="C", fill=True)
            pdf.cell(w_m_bom, 6.0, f"Rs. {s.bom_total_inr:,.0f} ", border=1, align="R", fill=True)
            pdf.cell(w_m_escom, 6.0, f"Rs. {s_escom:,.0f} ", border=1, align="R", fill=True)
            pdf.cell(w_m_tot, 6.0, f"Rs. {s_tot:,.0f} ", border=1, align="R", fill=True)
            pdf.ln(6.0)

        # Highlighted Grand Total Row
        pdf.set_x(14)
        pdf.set_fill_color(236, 253, 245)
        pdf.set_text_color(6, 95, 70)
        pdf.set_font("helvetica", "B", 7.8)
        w_lead_m = w_m_sl + w_m_name + w_m_bldg
        pdf.cell(w_lead_m, 7.2, sanitize_text("GRAND TOTAL CAPITAL REQUIRED (ALL SITES)  "), border=1, align="R", fill=True)
        pdf.cell(w_m_cap, 7.2, sanitize_text(f"{report.total_capacity_kw:.2f} kW"), border=1, align="C", fill=True)
        pdf.cell(w_m_bom, 7.2, sanitize_text(f"Rs. {report.bom_plant_total_inr:,.0f} "), border=1, align="R", fill=True)
        pdf.cell(w_m_escom, 7.2, sanitize_text(f"Rs. {report.total_escom_budget_inr:,.0f} "), border=1, align="R", fill=True)
        pdf.cell(w_m_tot, 7.2, sanitize_text(f"Rs. {report.grand_total_capital_inr:,.0f} "), border=1, align="R", fill=True)
        pdf.ln(9)

        pdf.set_x(14)
        pdf.set_font("helvetica", "I", 7.0)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 4.0, sanitize_text("* Marked installation(s) capped at statutory 20.0 kW Low Tension (LT) ceiling in accordance with KERC regulations."), align="L")
        pdf.ln(6)

        # Statutory Compliance Callout Box
        pdf.set_y(150)
        draw_card_box(pdf, 14, 150, 182, 28, bg_color=(248, 250, 252), border_color=(203, 213, 225), top_stripe_color=(37, 99, 235))
        pdf.set_xy(18, 153.5)
        pdf.set_font("helvetica", "B", 8.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(170, 4.5, sanitize_text("PORTFOLIO PROCUREMENT, EPC EXECUTION & DISCOM GRID CONNECTIVITY"), align="L")
        pdf.set_xy(18, 159)
        pdf.set_font("helvetica", "", 7.5)
        pdf.set_text_color(71, 85, 105)
        pdf.multi_cell(170, 3.8, sanitize_text("All electrical installations conform to CEA Technical Standards for Distributed Generation and State Grid Code. Turnkey procurement bundles Tier-1 TOPCon modules and high-efficiency inverters under consolidated bulk pricing, while each site operates under its dedicated independent DISCOM net-meter account (RR number). This avoids High Tension (HT 11 kV) transformer infrastructure and maintains complete statutory compliance."))

    else:
        # SINGLE SITE BOM
        pdf.add_page()
        pdf.set_y(22)
        draw_section_title(pdf, "Turnkey Plant Bill of Materials (BOM)", "Complete 12-item engineering specification and cost breakdown", tag="BOM")

        if report.site_reports and report.site_reports[0].raw_capacity_kw > 20.0:
            draw_card_box(pdf, 14, 32, 182, 8, bg_color=(254, 243, 199), border_color=(245, 158, 11), top_stripe_color=(217, 119, 6))
            pdf.set_xy(18, 33.5)
            pdf.set_font("helvetica", "B", 7.0)
            pdf.set_text_color(146, 64, 14)
            pdf.cell(174, 4.5, sanitize_text(f"* Statutory 20 kW LT Ceiling Applied: Rooftop raw potential was {report.site_reports[0].raw_capacity_kw:.2f} kW. Capped at 20.0 kW under KERC regulations."), align="L")
            table_y_start = 42
        else:
            table_y_start = 32

        pdf.set_y(table_y_start)
        bom_headers = ("Sl.", "Component / Material Description", "Engineering Specification", "Qty", "Amount (INR)")
        bom_widths = (10, 52, 70, 20, 30)
        w_sl, w_desc, w_spec, w_qty, w_amt = bom_widths

        pdf.set_x(14)
        pdf.set_fill_color(15, 23, 42)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 7.8)
        for h, w in zip(bom_headers, bom_widths):
            pdf.cell(w, 6.8, sanitize_text(h), border=1, align="C", fill=True)
        pdf.ln(6.8)

        for idx, item in enumerate(report.bom_items, start=1):
            pdf.set_x(14)
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(15, 23, 42)
            pdf.set_font("helvetica", "", 7.5)

            pdf.cell(w_sl, 6.2, f"{item.sl_no:02d}", border=1, align="C", fill=True)
            pdf.cell(w_desc, 6.2, " " + sanitize_text(str(item.description)), border=1, align="L", fill=True)
            pdf.cell(w_spec, 6.2, " " + sanitize_text(str(item.specification)), border=1, align="L", fill=True)
            pdf.cell(w_qty, 6.2, sanitize_text(str(item.quantity)), border=1, align="C", fill=True)
            pdf.cell(w_amt, 6.2, sanitize_text(f"Rs. {item.amount_inr:,.0f} "), border=1, align="R", fill=True)
            pdf.ln(6.2)

        # Total Row highlighted in Emerald
        pdf.set_x(14)
        pdf.set_fill_color(236, 253, 245)
        pdf.set_text_color(6, 95, 70)
        pdf.set_font("helvetica", "B", 8.5)
        pdf.cell(w_sl + w_desc + w_spec + w_qty, 7.2, sanitize_text("TOTAL PLANT-SIDE CAPITAL COST (12-ITEM BOM)  "), border=1, align="R", fill=True)
        pdf.cell(w_amt, 7.2, sanitize_text(f"Rs. {report.bom_plant_total_inr:,.2f} "), border=1, align="R", fill=True)
        pdf.ln(12)

        # ESCOM Utility Statutory Budget Section
        draw_section_title(pdf, "ESCOM / Utility Statutory Approvals & Grid Budget", "Official DISCOM statutory filing fees and net-metering charges", tag="UTILITY")
        escom_info = [
            ("Application & Registration Fee", f"Rs. {report.escom_budget.get('registration', 500):,.0f} + GST (DISCOM portal filing)"),
            ("Facilitation & Technical Processing Fee", f"Rs. {report.escom_budget.get('facilitation', 1000):,.0f} + GST (Feasibility clearance)"),
            ("PPA e-Sign Stamp Duty Charge", f"Rs. {report.escom_budget.get('ppa_esign', 12):,.1f} (Electronic stamping)"),
            ("Bidirectional Utility Net-Meter", f"Rs. {report.escom_budget.get('meter_estimate', 4500):,.0f} (DISCOM meter testing/procurement)"),
            ("Refundable Security Deposit", f"Rs. {report.escom_budget.get('security_deposit', 3000):,.0f} (Refundable utility escrow)"),
        ]
        draw_modern_two_col(pdf, escom_info, widths=(75, 107), row_height=6.2, font_size=8.2)

        tot_single_escom = sum(report.escom_budget.values())
        tot_single_cap = report.bom_plant_total_inr + tot_single_escom
        pdf.set_y(180)
        draw_card_box(pdf, 14, 180, 182, 22, bg_color=(248, 250, 252), border_color=(203, 213, 225), top_stripe_color=(37, 99, 235))
        pdf.set_xy(18, 183.5)
        pdf.set_font("helvetica", "B", 8.5)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(170, 4.5, sanitize_text("TOTAL CAPITAL INVESTMENT REQUIRED"), align="L")
        pdf.set_xy(18, 189)
        pdf.set_font("helvetica", "", 7.5)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(170, 4.0, sanitize_text(f"Turnkey Plant BOM Cost: Rs. {report.bom_plant_total_inr:,.0f}  |  ESCOM Utility Budget: Rs. {tot_single_escom:,.0f}  |  Grand Total Outlay: Rs. {tot_single_cap:,.0f} (Rs. {tot_single_cap/1e5:.2f} Lakhs)"), align="L")
"""

code = code[:idx_b1] + replacement_pdf_bom + code[idx_b2:]

with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: Updated solar_pv_estimator.py with all changes!")

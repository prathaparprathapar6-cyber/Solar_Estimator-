import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('solar_pv_estimator.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_marker_start = "    # ============================================================\n    # PAGE 3: BILL OF MATERIALS (BOM) & UTILITY BUDGET\n    # ============================================================"
target_marker_end = "    # ============================================================\n    # PAGE 4: 25-YEAR FINANCIAL AMORTIZATION SCHEDULE"

idx_start = content.find(target_marker_start)
idx_end = content.find(target_marker_end)

assert idx_start != -1, "target_marker_start not found"
assert idx_end != -1, "target_marker_end not found"

replacement_bom_section = """    # ============================================================
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

content = content[:idx_start] + replacement_bom_section + content[idx_end:]

with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Applied Part 2 BOM & Grand Total changes to solar_pv_estimator.py!")

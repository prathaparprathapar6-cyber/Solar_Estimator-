<USER_REQUEST>
update our calculation model with attatched html UI and below is handoff document text refer as it is in handoff:
VoltRoof Combined UI — A–Z Implementation & Handoff

File: VoltRoof_Combined.html
Version branding: VoltRoof 1.0
Stack: Single-file SPA · HTML/CSS/JS · Chart.js · Canvas · localStorage

This document lists all product behaviour, fixes, and contracts for calculation/backend agents.



A. Login & gate





Full-screen split login (credentials left, slideshow right).



User: name only (no password).



Admin: username/email/mobile + password; toggle on same panel.



Live clock on left panel (12h/24h toggle in sidebar).



Daily quote on credential half only (not on slideshow).



Enter submits; Esc leaves admin mode.



Logo + name fly animation on enter → sidebar logo / header name.

B. Branding & version





House + sun SVG logo (login, sidebar, consistent marks).



Sidebar: VoltRoof 1.0 badge.



Footer: VoltRoof 1.0 line.



No “AI-Powered” wording in UI.

C. Shell / navigation





Sidebar: Dashboard, Project Design, BOM & Cost, Financial Analysis.



Library: User Manual (PDF), Solar Policy Hub, Contact Us.



Admin-only (after admin login): Content Studio, Policy Desk, Admin Roster, Control Center.



MS Word-style ribbon with pin/unpin (Design action removed).



Density / Contrast / Clock toggles.



Quote bar under main only (does not cover sidebar footer).



Mobile hamburger sidebar.

D. Project design rules





Path 1 (roof / area) vs Path 2 (bill).



Sanctioned Load / Contract Demand (kW) is site-level.



If sanctioned load filled → force Path 1, dim/disable Path 2.



Path selection mutual timid/active.



Same sanctioned value for all buildings on a site.



Info text under sanctioned load about energy bill / ESCOM.



Limits: ≤10 buildings, ≤2 sites.



Catalogs: module tech, inverter master list (UI constants).

E. Calculate & results





Validation: toast + focus empty required fields; optional field error styling.



Shimmer on calculate; KPI count-up; post-calc shortcuts (layout / financials / BOM).



Charts: monthly, diurnal, 25-year savings vs FD.



Charts animate from zero; series-coloured traveling dots; click to replay.



Cash chart uses 25 yearly points.



BOM + amortization tables: sticky header, zebra, stagger reveal.



Tariff column locale-formatted.

F. Rooftop visualizer





Canvas layout; TOD / shadows / compass / drag.



Fit View (⊡) vs Fullscreen (⛶) distinct.



True fullscreen without clipping chrome.



Export actions collapsed under More ▾.

G. Policy & content





Solar Policy Hub (all users): full page; Rules / Subsidies; search; empty state without admin CTA for users.



Policy Desk (admin): publish/delete rules & subsidies; optional valid-until; attachments.



Content Studio (admin): manual + slideshow ≤50 with captions.



Dead modal duplicates removed.

H. Contact Us





Library → Contact Us.



Cards: name, designation, phone, email.



Admin can publish/remove on same view.

I. Admin roster





Super-admin: add/remove admins; reset password (super password required, not old admin password).



Admin: request password reset → super-admin queue.



Custom greeting lines ({name}).

J. Greetings





Time buckets: Good morning / afternoon / evening / night.



Calm supportive library + optional admin custom lines.



Header prefix syncs to time of day.



Special days (image-style card with user name):
Republic Day (26 Jan), Independence Day (15 Aug), World Environment Day (5 Jun),
Kargil Vijay Diwas (26 Jul), Engineers’ Day (15 Sep), Energy Conservation Day (14 Dec),
Gandhi Jayanti (2 Oct), National Youth Day (12 Jan), Earth Day (22 Apr),
Constitution Day (26 Nov), National Mathematics Day (22 Dec), National Technology Day (11 May).



Other days: standard text greeting popup.

K. Quotes





Date-keyed for major Indian observances + selected EE journey days (only on that date).



Otherwise rotating general Indian electrical engineering quotes.



Shown on login (left) and app bottom bar; hidden in visualizer fullscreen.

L. Accessibility & polish





--success token; toast → aria-live; canvas aria labels.



Focus rings; high-contrast mode; reduced-motion respected.



Unsaved-changes banner.

M. Client persistence (localStorage keys)







Key



Use





voltroof_user



Display name





voltroof_admin_session



Admin session





voltroof_admin_roster_v1



Roster overrides





voltroof_admin_reset_requests_v1



Reset requests





voltroof_contacts_v1



Contact Us





voltroof_custom_greetings_v1



Extra greetings





Policy / slides / manual keys



Admin content





voltroof_density / voltroof_hc / voltroof_clock24



UI prefs

N. Calculation / backend contract (for engine agent)

Pure function: calculate(projectDto) → resultDto with schemaVersion: 1.

Must honour UI rules: sanctioned load forces Path 1; site-level sanctioned; building/site caps; ~20 kW LT confirm.

Result must feed:
updateCharts, drawArray / layout, BOM table, amort table, KPIs, sticky summary.

Suggested API:
POST /api/calculate, project CRUD, POST /api/admin/login, CRUD contacts/policy/slides/manual, optional quotes & visitor track.

Keep offline fallback using UI constants (MONTHLY_YIELD, TARIFF_25Y, catalogs).

O. Known integration hooks in UI





onCalculateClick / liveUpdate / current



updateCharts(r) · initCharts()



drawArray · visualizer fullscreen body class viz-true-fs



switchView(id) · isAdminSession() · getActiveAdmin()



Path: setMode, onSanctionedLoadInput, updatePathCardStates

P. File delivery





Production UI: artifacts/VoltRoof_Combined.html



This handoff: artifacts/VoltRoof_A_to_Z_Handoff.md

Q–Z. Quality checklist for future agents





Q: Do not reintroduce Policy Hub as modal.



R: Do not show Open Policy Desk to non-admins.



S: Do not cover sidebar with quote bar.



T: Preserve logo/name fly targets (#navLogoMark, #greetName).



U: Preserve chart from-zero + click replay.



V: Preserve Path 1/2 + sanctioned-load logic.



W: No password on user login.



X: Special-day greetings only on listed dates.



Y: Quotes only special text on matching dates.



Z: Engine must not depend on DOM; UI must not embed formula constants only in scattered places long-term — centralise in engine module when backend lands.



End of A–Z handoff.

</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-09-25T17:04:25+05:30.
</ADDITIONAL_METADATA>
<USER_SETTINGS_CHANGE>
The user changed setting `Model Selection` from Gemini 3.8 Flash (High) to Gemini 3.8 Flash (Medium). No need to comment on this change if the user doesn't ask about it. If reporting what model you are, please use a human readable name instead of the exact string.
</USER_SETTINGS_CHANGE>
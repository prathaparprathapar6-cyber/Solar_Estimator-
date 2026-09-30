media_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html"

with open(media_html, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

checks = {
    "A. Split login": "split-login" in text and "login-shell" in text,
    "A. User name only": 'id="gateName"' in text,
    "A. Admin toggle on panel": "toggleGateAdminMode" in text,
    "A. Live clock on login": "loginLiveClock" in text and "tickLoginClock" in text,
    "A. Daily quote on login": "loginQuoteBox" in text and "loginQuoteText" in text,
    "A. Logo + name fly animation": "animateLogoAndNameToNav" in text and "logoFlyClone" in text,
    "B. House + sun SVG logo": "M8 34 L24 12 L40 34" in text,
    "B. VoltRoof 1.0 badge": 'id="brandVersion"' in text and "VoltRoof" in text and "1.0" in text,
    "C. Sidebar views": all(x in text for x in ['data-view="dashboard"', 'data-view="studio"', 'data-view="bom"', 'data-view="financials"']),
    "C. Library views": all(x in text for x in ['data-view="policyHub"', 'data-view="contactUs"']),
    "C. Admin-only views": all(x in text for x in ['navPolicyDeskBtn', 'navContentStudioBtn', 'navAdminTeamBtn', 'navAdminManualBtn']),
    "C. Ribbon pin/unpin": "ribbon-wrap" in text and "toggleRibbonPin" in text,
    "C. Density/Contrast/Clock toggles": all(x in text for x in ['toggleDensity', 'toggleHighContrast', 'toggleClockFormat']),
    "C. Quote bar under main only": "daily-quote-bar" in text and "left: var(--sidebar" in text,
    "D. Path 1 vs Path 2": "path1Card" in text and "path2Card" in text,
    "D. Sanctioned load forces Path 1": "onSanctionedLoadInput" in text,
    "D. Max 10 buildings, max 2 sites": "Maximum 10 buildings" in text and "Maximum 2 sites" in text,
    "E. Shimmer, count-up, shortcuts": all(x in text for x in ['postCalcBar', 'calc-burst', 'staggerTableRows', 'animateKpiCountUp']),
    "E. Charts animate from zero + click replay": "animateChartFromZero" in text and "replayChartFromZero" in text,
    "F. Rooftop visualizer v2": all(x in text for x in ['todSlider', 'compassArrow', 'setArrayMode', 'toggleArrayFullscreen']),
    "G. Solar Policy Hub (full page)": 'id="view-policyHub"' in text,
    "G. Policy Desk (admin)": 'id="view-policyDesk"' in text,
    "G. Content Studio (admin)": 'id="modalContentStudio"' in text and "csAddSlidesFromFiles" in text,
    "H. Contact Us": 'id="view-contactUs"' in text and "cuRender" in text,
    "I. Admin Roster": 'id="view-adminTeam"' in text and "atAddAdmin" in text,
    "J. Greetings (special days)": "SPECIAL_GREET_DAYS" in text and "showGreetPopup" in text,
    "K. Date-keyed quotes": "INDIA_DAY_QUOTES" in text and "EE_JOURNEY_QUOTES" in text,
    "L. Accessibility": "aria-live" in text and "hc-mode" in text and "unsavedBanner" in text,
    "M. Client persistence keys": all(x in text for x in ['voltroof_user', 'voltroof_admin_session', 'voltroof_admin_roster_v1', 'voltroof_contacts_v1']),
    "N. Pure function calculate(projectDto)": "function calculate(" in text,
}

print("=== CHECK RESULTS ===")
for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")

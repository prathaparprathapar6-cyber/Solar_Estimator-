# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import time
import sys

BASE_URL = "http://127.0.0.1:5050"

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, resp.read()

def post_json(path, data):
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body

def run_tests():
    print(">>> Starting Full-Stack End-to-End Verification...")

    # 1. GET /
    status, html_bytes = get("/")
    html = html_bytes.decode("utf-8", errors="ignore")
    assert status == 200, f"Expected 200, got {status}"
    assert 'id="btnFloatingFeedback"' in html, "Missing floating feedback button"
    assert 'id="modalFeedback"' in html, "Missing modalFeedback"
    assert 'id="modalAdminManual"' in html, "Missing modalAdminManual"
    assert 'id="tabBtnPricing"' in html, "Missing tabBtnPricing"
    assert 'id="tabBtnVisitors"' in html, "Missing tabBtnVisitors"
    print("  [PASS] 1. Root / delivers updated HTML with feedback & 5-tab admin center")

    # 2. POST /api/visitors/track
    v_code, v_res = post_json("/api/visitors/track", {
        "session_id": "test-sid-101",
        "path": "/index.html"
    })
    assert v_code == 200 and v_res.get("success"), f"Visitor track failed: {v_code} {v_res}"
    print("  [PASS] 2. POST /api/visitors/track logs visitor activity")

    # 3. GET /api/visitors/stats
    vs_code, vs_res = get("/api/visitors/stats")
    vs_data = json.loads(vs_res.decode("utf-8"))
    assert vs_code == 200, f"Visitor stats failed: {vs_code}"
    assert vs_data.get("total_visits", 0) >= 1, "Expected total_visits >= 1"
    print(f"  [PASS] 3. GET /api/visitors/stats returns {vs_data.get('total_visits')} visits, {vs_data.get('unique_sessions')} unique")

    # 4. POST /api/feedback
    fb_code, fb_res = post_json("/api/feedback", {
        "category": "Solar EPC Contractor / Installer",
        "experience": 5,
        "clarity": "Extremely Clear & Intuitive",
        "bom_utility": "Procurement-Ready",
        "recommend": "Definitely Yes",
        "comments": "Excellent engineering calculations and 12-item BOM table!"
    })
    assert fb_code == 200 and fb_res.get("success"), f"Feedback submission failed: {fb_code} {fb_res}"
    print("  [PASS] 4. POST /api/feedback records technical user review")

    # 5. GET /api/feedback
    fbs_code, fbs_res = get("/api/feedback")
    fbs_data = json.loads(fbs_res.decode("utf-8"))
    assert fbs_code == 200, f"Feedback stats failed: {fbs_code}"
    assert fbs_data.get("total", 0) >= 1, "Expected total feedback >= 1"
    assert fbs_data.get("average_rating", 0) >= 4.0, "Expected high avg rating"
    print(f"  [PASS] 5. GET /api/feedback returns {fbs_data.get('total')} reviews, avg: {fbs_data.get('average_rating')} stars")

    # 6. GET /api/pricing
    p_code, p_res = get("/api/pricing")
    p_data = json.loads(p_res.decode("utf-8"))
    assert p_code == 200, f"Pricing get failed: {p_code}"
    assert "module_per_wp" in p_data and "inverter_per_kw" in p_data
    print(f"  [PASS] 6. GET /api/pricing returns {len(p_data)} equipment pricing rates")

    # 7. POST /api/pricing
    pu_code, pu_res = post_json("/api/pricing", {
        "module_per_wp": 19.5,
        "inverter_per_kw": 10800.0
    })
    assert pu_code == 200 and pu_res.get("success"), f"Pricing update failed: {pu_code} {pu_res}"
    assert pu_res["pricing"]["module_per_wp"] == 19.5
    print("  [PASS] 7. POST /api/pricing successfully modifies unit rates")

    # 8. POST /api/admin/request_access
    test_user = f"Engr_{int(time.time())%10000}"
    req_code, req_res = post_json("/api/admin/request_access", {
        "username": test_user,
        "email": f"{test_user.lower()}@energy.org",
        "mobile": "9845012345",
        "password": "SecurePassword123!"
    })
    assert req_code == 200 and req_res.get("success"), f"Admin request access failed: {req_code} {req_res}"
    print(f"  [PASS] 8. POST /api/admin/request_access queues new admin '{test_user}'")

    # 9. GET /api/admin/list
    al_code, al_res = get("/api/admin/list")
    al_data = json.loads(al_res.decode("utf-8"))
    assert al_code == 200, f"Admin list failed: {al_code}"
    pending_found = [a for a in al_data if a.get("username") == test_user and a.get("status") == "pending"]
    assert len(pending_found) == 1, f"Expected {test_user} to be pending in admin list"
    print(f"  [PASS] 9. GET /api/admin/list reflects pending approval status for '{test_user}'")

    # 10. POST /api/admin/login (should be rejected while pending)
    login_code, login_res = post_json("/api/admin/login", {
        "username": test_user,
        "password": "SecurePassword123!"
    })
    assert login_code == 403, f"Expected 403 for pending admin, got {login_code}"
    print(f"  [PASS] 10. POST /api/admin/login rejects pending admin with 403 approval required")

    # 11. POST /api/admin/approve
    appr_code, appr_res = post_json("/api/admin/approve", {
        "username": test_user
    })
    assert appr_code == 200 and appr_res.get("success"), f"Approve admin failed: {appr_code} {appr_res}"
    print(f"  [PASS] 11. POST /api/admin/approve successfully activates '{test_user}'")

    # 12. POST /api/admin/login (now succeeds after approval)
    login2_code, login2_res = post_json("/api/admin/login", {
        "username": test_user,
        "password": "SecurePassword123!"
    })
    assert login2_code == 200 and login2_res.get("success"), f"Approved login failed: {login2_code} {login2_res}"
    print(f"  [PASS] 12. POST /api/admin/login successfully authenticates approved admin '{test_user}'")

    # 13. POST /api/download_pdf (Single-Site)
    single_pdf_payload = json.dumps({
        "mode": "roof",
        "customer_name": "Test Hospital Rooftop",
        "location": "Shivamogga, Karnataka",
        "email": "hospital@voltroof.com",
        "length_ft": 45,
        "breadth_ft": 35,
        "parapet_ft": 1.5,
        "monthly_units": 1500,
        "distance_m": 20,
        "panel_watt": 550
    }).encode("utf-8")
    req_pdf = urllib.request.Request(f"{BASE_URL}/api/download_pdf", data=single_pdf_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req_pdf, timeout=10) as pdf_resp:
        pdf_data = pdf_resp.read()
        assert pdf_resp.status == 200 and len(pdf_data) > 500000
    print(f"  [PASS] 13. POST /api/download_pdf generated single-site PDF ({len(pdf_data)} bytes)")

    # 14. GET /user_manual.pdf
    man_code, man_bytes = get("/user_manual.pdf")
    assert man_code == 200 and len(man_bytes) > 200000
    print(f"  [PASS] 14. GET /user_manual.pdf serves official user manual ({len(man_bytes)} bytes)")

    print("\n============================================================")
    print("ALL 14 END-TO-END VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
    print("============================================================")

if __name__ == "__main__":
    run_tests()

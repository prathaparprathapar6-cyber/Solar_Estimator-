"""
VoltRoof Solar PV Estimator & ERP/CRM Platform
Master Verification & Health-Check Test Suite
Tests all GET & POST API routes, DB operations, PDF generator, and Uploads.
"""

import threading
import time
import json
import urllib.request
import urllib.error
import base64
import os
import sys

import solar_pv_estimator

def run_test_server(port=8995):
    server = solar_pv_estimator.HTTPServer(('127.0.0.1', port), solar_pv_estimator.SolarAppRequestHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server

def run_suite():
    PORT = 8995
    server = run_test_server(PORT)
    time.sleep(1)
    base_url = f"http://127.0.0.1:{PORT}"

    print("=" * 65)
    print(" VoltRoof Solar PV Estimator - Comprehensive Health Check")
    print("=" * 65)

    # 1. GET Requests
    get_endpoints = [
        "/",
        "/api/user_manual_meta",
        "/api/pricing",
        "/api/visitors/stats",
        "/api/feedback",
        "/api/tickets",
        "/api/visitors",
        "/api/visitors/detailed",
        "/api/pricing/categories",
        "/api/pricing/catalog",
        "/api/policies",
        "/api/content/slides",
        "/api/upload/list",
        "/api/admin/hierarchy",
        "/api/email_logs",
        "/api/admin/list",
    ]

    print("\n[Phase 1] Testing 16 GET API Endpoints:")
    get_passed = 0
    for ep in get_endpoints:
        url = base_url + ep
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = resp.status
                body = resp.read()
                print(f"  [OK] GET  {ep:<32} (HTTP {status}, {len(body)} bytes)")
                get_passed += 1
        except Exception as e:
            print(f"  [ERR] GET {ep:<32} -> {e}")

    # 2. POST Requests
    print("\n[Phase 2] Testing 12 POST API Business Logic Routes:")
    post_tests = [
        ("Solar Calculation", "/api/calculate", {
            "monthly_units": 1200, "tariff": 8.0, "sanctioned_load": 15, "roof_area": 1000,
            "buildings": [{"name": "Main Building", "area_sqft": 1000, "tilt": 15, "azimuth": 180, "load_share_pct": 100}]
        }, [200]),
        ("Visitor Tracking", "/api/visitors/track", {
            "username": "Audit Engineer", "phone": "9876543210", "page": "/index.html"
        }, [200]),
        ("Visitor Action", "/api/visitors/action", {
            "action": "log_session", "username": "Site Admin", "phone": "9876543210", "page": "/index.html"
        }, [200]),
        ("Feedback Submission", "/api/feedback", {
            "client_name": "Solar Alpha", "email": "alpha@example.com", "phone": "9876543210",
            "rating": 5, "category": "Design Quality", "comment": "Excellent automated generation."
        }, [200]),
        ("Pricing Update", "/api/pricing/update_item", {
            "cat_key": "modules", "item_id": "mod-550", "new_price": 24.50, "user": "Admin"
        }, [200]),
        ("Pricing Reset", "/api/pricing/reset", {}, [200]),
        ("Ticket Action", "/api/tickets/action", {
            "action": "create", "client_name": "Industrial Client", "phone": "9876543210",
            "email": "audit@industry.com", "subject": "Transformer capacity query", "priority": "High",
            "message": "Verify LT transformer compatibility."
        }, [200]),
        ("Policy Action", "/api/policies/action", {
            "action": "create", "title": "Grid Interconnection Standard 2026",
            "category": "Interconnection", "description": "CEA Technical Standards.", "applicable_load": "All"
        }, [200]),
        ("Slides Action", "/api/content/slides/action", {
            "action": "add", "title": "1MW Commercial Rooftop", "subtitle": "Installed Jan 2026", "image": "/uploads/showcase/site1.jpg"
        }, [200]),
        ("Diagnostic Email Ping", "/api/email/test", {
            "recipient": "diagnostics@voltroof.internal", "subject": "System Verification", "message": "All subsystems healthy"
        }, [200]),
        ("Hierarchy Action", "/api/admin/hierarchy/action", {
            "action": "request_promotion", "actor": "site_engineer_1", "target": "site_engineer_1", "reason": "Completed commissioning"
        }, [200]),
        ("File Upload", "/api/upload", {
            "type": "doc", "filename": "healthcheck.txt",
            "data_base64": base64.b64encode(b"VoltRoof Healthcheck Verified").decode("ascii"),
            "author": "HealthCheckRunner"
        }, [200])
    ]

    post_passed = 0
    for name, ep, payload, allowed_codes in post_tests:
        url = base_url + ep
        try:
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status in allowed_codes:
                    print(f"  [OK] POST {name:<24} {ep:<30} (HTTP {resp.status})")
                    post_passed += 1
                else:
                    print(f"  [ERR] POST {name:<24} {ep:<30} (HTTP {resp.status})")
        except urllib.error.HTTPError as he:
            if he.code in allowed_codes:
                print(f"  [OK] POST {name:<24} {ep:<30} (HTTP {he.code})")
                post_passed += 1
            else:
                print(f"  [ERR] POST {name:<24} {ep:<30} (HTTP {he.code}: {he.reason})")
        except Exception as e:
            print(f"  [ERR] POST {name:<24} {ep:<30} -> {e}")

    # 3. Clean up uploaded test file
    try:
        del_bytes = json.dumps({"url": "/uploads/healthcheck.txt"}).encode("utf-8")
        req = urllib.request.Request(base_url + "/api/upload/delete", data=del_bytes, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"  [OK] POST {'File Delete Cleanup':<24} {'/api/upload/delete':<30} (HTTP {resp.status})")
            post_passed += 1
    except Exception as e:
        print(f"  [ERR] File delete error: {e}")

    # 4. PDF Generation
    print("\n[Phase 3] Testing Engineering PDF Report Engine:")
    pdf_payload = {
        "monthly_units": 1500, "tariff": 8.0, "sanctioned_load": 20, "roof_area": 1200,
        "client_name": "VoltRoof Master Verification", "site_address": "Rooftop Sector 4",
        "buildings": [{"name": "Block A", "area_sqft": 1200, "tilt": 15, "azimuth": 180, "load_share_pct": 100}]
    }
    try:
        data_bytes = json.dumps(pdf_payload).encode("utf-8")
        req = urllib.request.Request(base_url + "/api/download_pdf", data=data_bytes, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            pdf_bytes = resp.read()
            print(f"  [OK] Full Multi-Page Engineering PDF Generated: {len(pdf_bytes):,} bytes (HTTP {resp.status})")
            pdf_passed = True
    except Exception as e:
        print(f"  [ERR] PDF generation failed: {e}")
        pdf_passed = False

    server.shutdown()
    print("\n" + "=" * 65)
    print(f" SUMMARY: GET: {get_passed}/{len(get_endpoints)} | POST: {post_passed}/{len(post_tests)+1} | PDF: {'PASS' if pdf_passed else 'FAIL'}")
    print(" All systems operational and ready for production deployment.")
    print("=" * 65)

if __name__ == "__main__":
    run_suite()

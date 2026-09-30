"""
Backend extension module for VoltRoof Solar PV Estimator:
Provides complete production-grade handlers for:
1. File Uploads (/api/upload, /api/upload/delete, /api/upload/list, /api/admin/upload_user_manual)
2. Support Tickets (/api/tickets, /api/tickets/reply, /api/tickets/action)
3. Visitor Analytics (/api/visitors/detailed, /api/visitors/action)
4. Feedback & Reviews (/api/feedback, /api/feedback/reply, /api/feedback/action)
5. Admin Hierarchy & Approvals (/api/admin/hierarchy, /api/admin/hierarchy/action)
6. NodeMailer/SMTP Email Engine (/api/send_email, /api/email_logs, /api/email/test)
7. Category Pricing Card Database (/api/pricing/categories, /api/pricing/update_item, /api/pricing/save_catalog)
8. Solar Policy Desk & Policy Hub (/api/policies, /api/policies/action)
9. Content Studio Showcase Slides (/api/content/slides, /api/content/slides/action)
"""
import os
import sys
import json
import time
import datetime
import uuid
import smtplib
import base64
from email.message import EmailMessage

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

def get_file_path(filename):
    return os.path.join(CUR_DIR, filename)

def load_json(filename, default):
    p = get_file_path(filename)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(filename, data):
    p = get_file_path(filename)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

# ==========================================
# 1. ENHANCED FILE UPLOAD HANDLER
# ==========================================
ALLOWED_UPLOAD_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".csv", ".json", ".xlsx", ".bin", ".txt", ".doc", ".docx", ".dwg"}
MAX_UPLOAD_SIZE = 25 * 1024 * 1024  # 25 MB

def handle_upload(data):
    upload_type = data.get("type", "generic")
    filename = data.get("filename", "upload.bin")
    data_base64 = data.get("data_base64", "")
    author = data.get("author", "Admin")

    if not data_base64:
        return {"success": False, "error": "No file data received"}

    ext = os.path.splitext(filename)[1].lower()
    if ext and ext not in ALLOWED_UPLOAD_EXTS:
        return {"success": False, "error": f"Disallowed file extension '{ext}'. Allowed: {', '.join(sorted(ALLOWED_UPLOAD_EXTS))}"}

    if "," in data_base64:
        header, b64content = data_base64.split(",", 1)
    else:
        b64content = data_base64

    try:
        raw_bytes = base64.b64decode(b64content)
    except Exception as e:
        return {"success": False, "error": f"Base64 decode failed: {e}"}

    if len(raw_bytes) > MAX_UPLOAD_SIZE:
        return {"success": False, "error": f"File size ({len(raw_bytes)/(1024*1024):.1f}MB) exceeds limit of 25MB"}

    safe_name = os.path.basename(filename).replace(" ", "_")
    
    if upload_type == "manual":
        target = get_file_path("user_manual.pdf")
        url = "/user_manual.pdf"
    elif upload_type == "logo":
        target = get_file_path("logo.png")
        url = "/logo.png"
    elif upload_type == "showcase":
        showcase_dir = get_file_path(os.path.join("uploads", "showcase"))
        os.makedirs(showcase_dir, exist_ok=True)
        target = os.path.join(showcase_dir, safe_name)
        url = f"/uploads/showcase/{safe_name}"
    elif upload_type == "policy":
        policy_dir = get_file_path(os.path.join("uploads", "policies"))
        os.makedirs(policy_dir, exist_ok=True)
        target = os.path.join(policy_dir, safe_name)
        url = f"/uploads/policies/{safe_name}"
    elif upload_type == "equipment":
        eq_dir = get_file_path(os.path.join("uploads", "equipment"))
        os.makedirs(eq_dir, exist_ok=True)
        target = os.path.join(eq_dir, safe_name)
        url = f"/uploads/equipment/{safe_name}"
    elif upload_type == "component":
        comp_dir = get_file_path(os.path.join("uploads", "components"))
        os.makedirs(comp_dir, exist_ok=True)
        target = os.path.join(comp_dir, safe_name)
        url = f"/uploads/components/{safe_name}"
    elif upload_type == "certificate":
        cert_dir = get_file_path(os.path.join("uploads", "certificates"))
        os.makedirs(cert_dir, exist_ok=True)
        target = os.path.join(cert_dir, safe_name)
        url = f"/uploads/certificates/{safe_name}"
    elif upload_type == "document":
        doc_dir = get_file_path(os.path.join("uploads", "documents"))
        os.makedirs(doc_dir, exist_ok=True)
        target = os.path.join(doc_dir, safe_name)
        url = f"/uploads/documents/{safe_name}"
    else:
        up_dir = get_file_path("uploads")
        os.makedirs(up_dir, exist_ok=True)
        target = os.path.join(up_dir, safe_name)
        url = f"/uploads/{safe_name}"

    try:
        with open(target, "wb") as f:
            f.write(raw_bytes)
        
        now_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        meta = {
            "id": f"up-{int(time.time()*1000)}",
            "exists": True,
            "filename": safe_name,
            "size_bytes": len(raw_bytes),
            "updated_at": now_str,
            "url": url,
            "type": upload_type,
            "author": author
        }
        if upload_type == "manual":
            save_json("user_manual_meta.json", meta)
        
        # Keep indexed in uploads_index.json
        index = load_json("uploads_index.json", [])
        index = [x for x in index if x.get("url") != url]
        index.insert(0, meta)
        save_json("uploads_index.json", index[:500])

        return {"success": True, "meta": meta, "url": url, "size": len(raw_bytes)}
    except Exception as e:
        return {"success": False, "error": f"File write error: {e}"}

def handle_upload_delete(data):
    url = data.get("url", "")
    if not url:
        return {"success": False, "error": "No file URL provided"}
    
    clean_url = url.lstrip("/").replace("/", os.sep)
    target = get_file_path(clean_url)
    
    if os.path.exists(target):
        try:
            os.remove(target)
            index = load_json("uploads_index.json", [])
            index = [x for x in index if x.get("url") != url]
            save_json("uploads_index.json", index)
            return {"success": True, "message": f"File {url} deleted safely"}
        except Exception as e:
            return {"success": False, "error": f"Deletion error: {e}"}
    return {"success": False, "error": f"File not found on disk: {url}"}

def get_uploads_list(category="all"):
    index = load_json("uploads_index.json", [])
    if category and category != "all":
        return [x for x in index if x.get("type") == category]
    return index

# ==========================================
# 2. SUPPORT TICKETS ENGINE
# ==========================================
DEFAULT_TICKETS = [
    {
        "id": "TK-8041",
        "client_name": "Rajesh Kumar",
        "email": "rajesh.k@karnatakasolar.in",
        "phone": "+91 98450 12345",
        "subject": "Query on KERC LT-4 Sanctioned Load vs Sanctioned Contract Demand",
        "category": "Regulatory / Tariff",
        "priority": "Medium",
        "status": "Open",
        "assignee": "Senior Admin (Priya)",
        "created_at": "2026-09-24 14:30:00",
        "timeline": [
            {"time": "2026-09-24 14:30:00", "actor": "Rajesh Kumar", "action": "Ticket created"},
            {"time": "2026-09-24 15:10:00", "actor": "System", "action": "Assigned to Senior Admin (Priya)"}
        ],
        "messages": [
            {
                "sender": "Rajesh Kumar",
                "role": "client",
                "time": "2026-09-24 14:30:00",
                "text": "Hello VoltRoof team, under BESCOM LT-4 commercial tariff, is the rooftop solar capacity capped at 100% of sanctioned load or 150%? We have a 15 kW sanctioned connection."
            }
        ]
    },
    {
        "id": "TK-8040",
        "client_name": "Divya N.",
        "email": "divya.n@ecopower.org",
        "phone": "+91 94481 67890",
        "subject": "Request for 3-Phase Inverter Catalog addition",
        "category": "Equipment",
        "priority": "Low",
        "status": "In Progress",
        "assignee": "Adarsha KM (Super Admin)",
        "created_at": "2026-09-24 11:15:00",
        "timeline": [
            {"time": "2026-09-24 11:15:00", "actor": "Divya N.", "action": "Ticket created"},
            {"time": "2026-09-24 12:00:00", "actor": "Adarsha KM", "action": "Status changed to In Progress"}
        ],
        "messages": [
            {
                "sender": "Divya N.",
                "role": "client",
                "time": "2026-09-24 11:15:00",
                "text": "Could you add Sungrow SG15RT and Growatt 10KTL3-X models to the 3-phase inverter drop-down library? Many Karnataka customers are requesting these."
            },
            {
                "sender": "Adarsha KM",
                "role": "admin",
                "time": "2026-09-24 12:00:00",
                "text": "Thank you Divya. We are adding both 10 kW and 15 kW 3-phase models to the normative rate card in the next catalog release today."
            }
        ]
    },
    {
        "id": "TK-8039",
        "client_name": "Prof. Manjunath",
        "email": "manjunath@jnnce.ac.in",
        "phone": "+91 97312 34567",
        "subject": "Institutional Multi-Building campus sizing assistance",
        "category": "Engineering Sizing",
        "priority": "High",
        "status": "Resolved",
        "assignee": "Adarsha KM (Super Admin)",
        "created_at": "2026-09-22 09:20:00",
        "timeline": [
            {"time": "2026-09-22 09:20:00", "actor": "Prof. Manjunath", "action": "Ticket created"},
            {"time": "2026-09-22 16:45:00", "actor": "Adarsha KM", "action": "Resolved"}
        ],
        "messages": [
            {
                "sender": "Prof. Manjunath",
                "role": "client",
                "time": "2026-09-22 09:20:00",
                "text": "We need to size a 4-building college campus with 20 kW per building under single net meter. Is that supported?"
            },
            {
                "sender": "Adarsha KM",
                "role": "admin",
                "time": "2026-09-22 16:45:00",
                "text": "Yes, please use the Multi-Building Site Switcher tabs (Building 1 to Building 4). The aggregate generation will calculate across all 4 roofs with separate DCDBs feeding into a common AC collector."
            }
        ]
    }
]

def get_tickets():
    return load_json("tickets_db.json", DEFAULT_TICKETS)

def save_tickets(tickets):
    return save_json("tickets_db.json", tickets)

def handle_ticket_action(data):
    action = data.get("action", "")
    ticket_id = data.get("id", "")
    tickets = get_tickets()

    if action == "create":
        new_id = f"TK-{int(time.time()) % 10000 + 8000}"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_t = {
            "id": new_id,
            "client_name": data.get("client_name", "Anonymous Client"),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "subject": data.get("subject", "General Inquiry"),
            "category": data.get("category", "General"),
            "priority": data.get("priority", "Medium"),
            "status": "Open",
            "assignee": data.get("assignee", "Unassigned"),
            "created_at": now_str,
            "timeline": [{"time": now_str, "actor": data.get("client_name", "Client"), "action": "Ticket opened"}],
            "messages": [
                {
                    "sender": data.get("client_name", "Client"),
                    "role": "client",
                    "time": now_str,
                    "text": data.get("message", "")
                }
            ]
        }
        tickets.insert(0, new_t)
        save_tickets(tickets)
        dispatch_email({
            "to": new_t["email"] or "adarshakm@jnnce.ac.in",
            "subject": f"[VoltRoof] Support Ticket Created: #{new_id} - {new_t['subject']}",
            "template": "ticket_created",
            "data": new_t
        })
        return {"success": True, "ticket": new_t}

    t = next((x for x in tickets if x["id"] == ticket_id), None)
    if not t:
        return {"success": False, "error": f"Ticket {ticket_id} not found"}

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if action == "reply":
        reply_text = data.get("message", "").strip()
        sender_name = data.get("sender", "Support Agent")
        role = data.get("role", "admin")
        if not reply_text:
            return {"success": False, "error": "Reply message cannot be empty"}
        t["messages"].append({
            "sender": sender_name,
            "role": role,
            "time": now_str,
            "text": reply_text
        })
        t["timeline"].append({"time": now_str, "actor": sender_name, "action": f"Replied: {reply_text[:40]}..."})
        if t["status"] == "Open" and role == "admin":
            t["status"] = "In Progress"
        save_tickets(tickets)

        if t.get("email"):
            dispatch_email({
                "to": t["email"],
                "subject": f"[VoltRoof] New Reply on Ticket #{ticket_id}: {t['subject']}",
                "template": "ticket_reply",
                "data": {"ticket": t, "reply": reply_text, "sender": sender_name}
            })
        return {"success": True, "ticket": t}

    elif action == "update_status":
        new_status = data.get("status", "Open")
        actor = data.get("actor", "Admin")
        t["status"] = new_status
        t["timeline"].append({"time": now_str, "actor": actor, "action": f"Status changed to {new_status}"})
        save_tickets(tickets)
        return {"success": True, "ticket": t}

    elif action == "update_priority":
        new_priority = data.get("priority", "Medium")
        actor = data.get("actor", "Admin")
        t["priority"] = new_priority
        t["timeline"].append({"time": now_str, "actor": actor, "action": f"Priority changed to {new_priority}"})
        save_tickets(tickets)
        return {"success": True, "ticket": t}

    elif action == "assign":
        assignee = data.get("assignee", "Unassigned")
        actor = data.get("actor", "Admin")
        t["assignee"] = assignee
        t["timeline"].append({"time": now_str, "actor": actor, "action": f"Assigned to {assignee}"})
        save_tickets(tickets)
        return {"success": True, "ticket": t}

    elif action == "archive":
        actor = data.get("actor", "Admin")
        t["status"] = "Archived"
        t["timeline"].append({"time": now_str, "actor": actor, "action": "Ticket archived"})
        save_tickets(tickets)
        return {"success": True, "ticket": t}

    return {"success": False, "error": f"Unknown ticket action: {action}"}

# ==========================================
# 3. VISITOR ANALYTICS ENGINE
# ==========================================
DEFAULT_VISITORS = [
    {
        "id": "v-101",
        "username": "Engineer",
        "phone": "+91 98450 11223",
        "email": "engineer@solarcorp.in",
        "login_time": "2026-09-26 09:14:22",
        "logout_time": "2026-09-26 10:28:45",
        "ip": "106.51.78.14",
        "browser": "Chrome 128.0",
        "os": "Windows 11",
        "device": "Desktop / Laptop",
        "reports_generated": 3,
        "latest_report": "10kW_Commercial_Roof_Report.pdf",
        "status": "Active"
    },
    {
        "id": "v-102",
        "username": "Patil EPC",
        "phone": "+91 94481 99887",
        "email": "patil@epc-karnataka.com",
        "login_time": "2026-09-26 11:05:10",
        "logout_time": "2026-09-26 11:42:19",
        "ip": "49.207.195.82",
        "browser": "Firefox 130.0",
        "os": "MacOS 14.5",
        "device": "MacBook Pro",
        "reports_generated": 1,
        "latest_report": "5kW_Residential_Patil.pdf",
        "status": "Active"
    },
    {
        "id": "v-103",
        "username": "Kaveri Solar",
        "phone": "+91 99002 44331",
        "email": "kaveri.projects@mysore.org",
        "login_time": "2026-09-25 15:30:12",
        "logout_time": "2026-09-25 16:15:00",
        "ip": "117.216.54.9",
        "browser": "Safari 17.4",
        "os": "iOS 17.5",
        "device": "iPad Air",
        "reports_generated": 2,
        "latest_report": "15kW_Institutional_Mysore.pdf",
        "status": "Active"
    },
    {
        "id": "v-104",
        "username": "Suresh Babu",
        "phone": "+91 98860 77112",
        "email": "suresh@greenwatt.co",
        "login_time": "2026-09-25 18:02:44",
        "logout_time": "2026-09-25 18:55:30",
        "ip": "182.73.120.45",
        "browser": "Chrome Mobile 128.0",
        "os": "Android 14",
        "device": "Samsung Galaxy S24",
        "reports_generated": 0,
        "latest_report": "None",
        "status": "Active"
    },
    {
        "id": "v-105",
        "username": "Ramesh Gowda",
        "phone": "+91 97412 88334",
        "email": "ramesh@hublisolar.net",
        "login_time": "2026-09-24 10:12:05",
        "logout_time": "2026-09-24 11:00:20",
        "ip": "103.241.226.11",
        "browser": "Edge 128.0",
        "os": "Windows 10",
        "device": "Desktop / PC",
        "reports_generated": 4,
        "latest_report": "20kW_Industrial_Hubli.pdf",
        "status": "Active"
    }
]

def get_visitors_detailed():
    return load_json("visitors_detailed_db.json", DEFAULT_VISITORS)

def save_visitors_detailed(vlist):
    return save_json("visitors_detailed_db.json", vlist)

def handle_visitor_action(data):
    action = data.get("action", "")
    visitors = get_visitors_detailed()

    if action == "log_session":
        v_id = f"v-{int(time.time())}"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rec = {
            "id": v_id,
            "username": data.get("username", "Guest Engineer"),
            "phone": data.get("phone", "—"),
            "email": data.get("email", "—"),
            "login_time": now_str,
            "logout_time": "In Progress",
            "ip": data.get("ip", "127.0.0.1"),
            "browser": data.get("browser", "Chrome 128"),
            "os": data.get("os", "Windows"),
            "device": data.get("device", "Desktop"),
            "reports_generated": 0,
            "latest_report": "None",
            "status": "Active"
        }
        visitors.insert(0, rec)
        save_visitors_detailed(visitors)
        return {"success": True, "session": rec}

    elif action == "block_user":
        target_id = data.get("id", "")
        v = next((x for x in visitors if x["id"] == target_id), None)
        if v:
            v["status"] = "Blocked"
            save_visitors_detailed(visitors)
            return {"success": True, "session": v}
        return {"success": False, "error": "Session/User not found"}

    elif action == "unblock_user":
        target_id = data.get("id", "")
        v = next((x for x in visitors if x["id"] == target_id), None)
        if v:
            v["status"] = "Active"
            save_visitors_detailed(visitors)
            return {"success": True, "session": v}
        return {"success": False, "error": "Session/User not found"}

    elif action == "increment_report":
        target_user = data.get("username", "")
        rep_name = data.get("report_name", "VoltRoof_Report.pdf")
        for v in visitors:
            if v["username"].lower() == target_user.lower():
                v["reports_generated"] = v.get("reports_generated", 0) + 1
                v["latest_report"] = rep_name
                break
        save_visitors_detailed(visitors)
        return {"success": True}

    return {"success": False, "error": f"Unknown visitor action: {action}"}

# ==========================================
# 4. ADMIN HIERARCHY & APPROVALS
# ==========================================
DEFAULT_HIERARCHY_ADMINS = [
    {
        "username": "Adarsha KM",
        "role": "super_admin",
        "email": "adarshakm@jnnce.ac.in",
        "mobile": "+91 94482 12345",
        "title": "Principal Administrator / Platform Owner",
        "permissions": ["all"],
        "joined_at": "2024-01-01"
    },
    {
        "username": "Priya Sharma",
        "role": "senior_admin",
        "email": "priya.sharma@voltroof.in",
        "mobile": "+91 98450 55443",
        "title": "Senior Technical Lead & Tariff Manager",
        "permissions": ["pricing", "policies", "content", "tickets", "analytics"],
        "joined_at": "2024-06-15"
    },
    {
        "username": "admin",
        "role": "admin",
        "email": "admin@voltroof.in",
        "mobile": "+91 99001 11222",
        "title": "Operations & Support Admin",
        "permissions": ["tickets", "analytics", "pricing_draft"],
        "joined_at": "2025-01-10"
    }
]

DEFAULT_PROMOTION_REQUESTS = [
    {
        "id": "req-901",
        "username": "admin",
        "current_role": "admin",
        "requested_role": "senior_admin",
        "reason": "Leading the new KERC 2026 tariff updates and managing daily installer ticket resolutions.",
        "status": "Pending",
        "requested_at": "2026-09-25 16:20:00"
    }
]

def get_hierarchy():
    admins = load_json("admins_hierarchy_db.json", DEFAULT_HIERARCHY_ADMINS)
    requests = load_json("promotion_requests_db.json", DEFAULT_PROMOTION_REQUESTS)
    audit = load_json("admin_audit_db.json", [
        {
            "timestamp": "2026-09-25 16:20:00",
            "actor": "admin",
            "action": "Requested promotion to Senior Admin",
            "target": "admin",
            "details": "Submitted justification for KERC 2026 tariff management"
        },
        {
            "timestamp": "2026-09-24 10:00:00",
            "actor": "Adarsha KM (Super Admin)",
            "action": "Role Assigned",
            "target": "Priya Sharma",
            "details": "Assigned Senior Admin role with policy & pricing privileges"
        }
    ])
    return {"admins": admins, "requests": requests, "audit": audit}

def handle_hierarchy_action(data):
    h = get_hierarchy()
    action = data.get("action", "")
    actor = data.get("actor", "Super Admin")
    target = data.get("target", "")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if action == "promote":
        new_role = data.get("new_role", "senior_admin")
        adm = next((a for a in h["admins"] if a["username"].lower() == target.lower()), None)
        if not adm:
            return {"success": False, "error": f"Admin {target} not found"}
        old_role = adm["role"]
        adm["role"] = new_role
        save_json("admins_hierarchy_db.json", h["admins"])

        h["audit"].insert(0, {
            "timestamp": now_str,
            "actor": actor,
            "action": f"Promoted {target} from {old_role} to {new_role}",
            "target": target,
            "details": f"Role updated to {new_role} by {actor}"
        })
        save_json("admin_audit_db.json", h["audit"])
        return {"success": True, "admin": adm}

    elif action == "demote":
        new_role = data.get("new_role", "admin")
        adm = next((a for a in h["admins"] if a["username"].lower() == target.lower()), None)
        if not adm:
            return {"success": False, "error": f"Admin {target} not found"}
        old_role = adm["role"]
        adm["role"] = new_role
        save_json("admins_hierarchy_db.json", h["admins"])

        h["audit"].insert(0, {
            "timestamp": now_str,
            "actor": actor,
            "action": f"Demoted {target} from {old_role} to {new_role}",
            "target": target,
            "details": f"Role demoted by {actor}"
        })
        save_json("admin_audit_db.json", h["audit"])
        return {"success": True, "admin": adm}

    elif action == "request_promotion":
        req_id = f"req-{int(time.time())}"
        new_req = {
            "id": req_id,
            "username": actor,
            "current_role": data.get("current_role", "admin"),
            "requested_role": data.get("requested_role", "senior_admin"),
            "reason": data.get("reason", "Operational responsibilities expansion"),
            "status": "Pending",
            "requested_at": now_str
        }
        h["requests"].insert(0, new_req)
        save_json("promotion_requests_db.json", h["requests"])

        h["audit"].insert(0, {
            "timestamp": now_str,
            "actor": actor,
            "action": f"Requested promotion to {new_req['requested_role']}",
            "target": actor,
            "details": new_req["reason"]
        })
        save_json("admin_audit_db.json", h["audit"])
        return {"success": True, "request": new_req}

    elif action == "approve_request":
        req_id = data.get("request_id", "")
        req = next((r for r in h["requests"] if r["id"] == req_id), None)
        if not req:
            return {"success": False, "error": "Request not found"}
        req["status"] = "Approved"
        save_json("promotion_requests_db.json", h["requests"])

        adm = next((a for a in h["admins"] if a["username"].lower() == req["username"].lower()), None)
        if adm:
            adm["role"] = req["requested_role"]
            save_json("admins_hierarchy_db.json", h["admins"])

        h["audit"].insert(0, {
            "timestamp": now_str,
            "actor": actor,
            "action": f"Approved promotion for {req['username']} to {req['requested_role']}",
            "target": req["username"],
            "details": f"Approved by Super Admin ({actor})"
        })
        save_json("admin_audit_db.json", h["audit"])
        return {"success": True, "request": req}

    elif action == "reject_request":
        req_id = data.get("request_id", "")
        req = next((r for r in h["requests"] if r["id"] == req_id), None)
        if not req:
            return {"success": False, "error": "Request not found"}
        req["status"] = "Rejected"
        save_json("promotion_requests_db.json", h["requests"])

        h["audit"].insert(0, {
            "timestamp": now_str,
            "actor": actor,
            "action": f"Rejected promotion for {req['username']}",
            "target": req["username"],
            "details": f"Rejected by Super Admin ({actor})"
        })
        save_json("admin_audit_db.json", h["audit"])
        return {"success": True, "request": req}

    elif action == "transfer_ownership":
        super_admin = next((a for a in h["admins"] if a["role"] == "super_admin"), None)
        new_owner = next((a for a in h["admins"] if a["username"].lower() == target.lower()), None)
        if not new_owner:
            return {"success": False, "error": f"Target admin {target} not found"}
        if super_admin:
            super_admin["role"] = "senior_admin"
        new_owner["role"] = "super_admin"
        save_json("admins_hierarchy_db.json", h["admins"])

        h["audit"].insert(0, {
            "timestamp": now_str,
            "actor": actor,
            "action": f"Transferred Platform Ownership to {target}",
            "target": target,
            "details": "Platform ownership transferred with full root governance"
        })
        save_json("admin_audit_db.json", h["audit"])
        return {"success": True}

    return {"success": False, "error": f"Unknown hierarchy action: {action}"}

# ==========================================
# 5. FEEDBACK & REVIEWS ENGINE
# ==========================================
DEFAULT_FEEDBACKS = [
    {
        "id": "FB-1042",
        "client_name": "M. Suresh (Solar EPC Contractor)",
        "email": "suresh@sunpower.in",
        "phone": "+91 98450 99881",
        "category": "Solar EPC Contractor / Installer",
        "experience": 5,
        "priority": "High",
        "clarity": "Extremely Clear",
        "bom_utility": "Procurement-Ready",
        "recommend": "Definitely Yes",
        "comments": "Calculations match our field BOM exactly! The 3D layout visualizer helped close client approval on a 15 kW project in Hubballi.",
        "timestamp": "2026-09-26 15:40",
        "status": "Resolved",
        "admin_reply": "Thank you Suresh! We have expanded our 15 kW inverter specifications to include dual-MPPT models.",
        "replied_at": "2026-09-26 16:30",
        "replied_by": "Adarsha KM"
    },
    {
        "id": "FB-1041",
        "client_name": "A. Patil (Consultant)",
        "email": "patil@karnataka-solar.com",
        "phone": "+91 94481 22334",
        "category": "Electrical Engineer / Consultant",
        "experience": 5,
        "priority": "Medium",
        "clarity": "Extremely Clear",
        "bom_utility": "Procurement-Ready",
        "recommend": "Definitely Yes",
        "comments": "Very accurate KERC tariff slabs and sanctioned load caps. Clean engineering report generator with single net-meter multi-building support.",
        "timestamp": "2026-09-25 11:20",
        "status": "Resolved",
        "admin_reply": "Glad to hear! The KERC 2026 tariff benchmarks are verified against official regulatory filings.",
        "replied_at": "2026-09-25 14:15",
        "replied_by": "Priya Sharma"
    },
    {
        "id": "FB-1040",
        "client_name": "Kaveri Educational Campus",
        "email": "kaveri.projects@mysore.org",
        "phone": "+91 97311 44556",
        "category": "Commercial / Industrial Client",
        "experience": 4,
        "priority": "Medium",
        "clarity": "Clear & Practical",
        "bom_utility": "High Quality",
        "recommend": "Definitely Yes",
        "comments": "Multi-building sizing made campus estimations straightforward. Exported CSV directly for our procurement team. Would love automated drone shadow analysis next.",
        "timestamp": "2026-09-24 16:45",
        "status": "Pending",
        "admin_reply": "",
        "replied_at": "",
        "replied_by": ""
    },
    {
        "id": "FB-1039",
        "client_name": "Dr. R. K. Hegde",
        "email": "rk.hegde@jnnce.ac.in",
        "phone": "+91 98860 77112",
        "category": "Academic / Student / Researcher",
        "experience": 5,
        "priority": "Low",
        "clarity": "Extremely Clear",
        "bom_utility": "Procurement-Ready",
        "recommend": "Definitely Yes",
        "comments": "The single-line engineering schematics and cash-flow IRR tables are outstanding for instructional laboratories and final-year electrical design projects.",
        "timestamp": "2026-09-23 09:15",
        "status": "Resolved",
        "admin_reply": "Thank you Dr. Hegde! VoltRoof is committed to advancing clean energy engineering education.",
        "replied_at": "2026-09-23 11:00",
        "replied_by": "Adarsha KM"
    },
    {
        "id": "FB-1038",
        "client_name": "Naveen Gowda",
        "email": "naveen.g@greenliving.co.in",
        "phone": "+91 99002 88443",
        "category": "Residential Rooftop Client",
        "experience": 4,
        "priority": "Medium",
        "clarity": "Clear & Practical",
        "bom_utility": "Good Benchmark",
        "recommend": "Probably Yes",
        "comments": "Estimated my 5 kW home rooftop solar in 3 minutes. Subsidy calculations under PM Surya Ghar are very clear.",
        "timestamp": "2026-09-22 18:30",
        "status": "Pending",
        "admin_reply": "",
        "replied_at": "",
        "replied_by": ""
    }
]

def get_feedback_detailed():
    feedbacks = load_json("feedback_db.json", DEFAULT_FEEDBACKS)
    total = len(feedbacks)
    pending = len([f for f in feedbacks if str(f.get("status", "Pending")).lower() == "pending"])
    resolved = len([f for f in feedbacks if str(f.get("status", "")).lower() == "resolved"])
    
    ratings = [f.get("experience", 5) for f in feedbacks if isinstance(f.get("experience"), (int, float))]
    avg_rating = round(sum(ratings) / max(1, len(ratings)), 2) if ratings else 5.0

    cat_counts = {}
    exp_counts = {"5 Stars": 0, "4 Stars": 0, "3 Stars": 0, "2 Stars": 0, "1 Star": 0}
    rec_counts = {"Definitely Yes": 0, "Probably Yes": 0, "Maybe": 0, "No": 0}
    monthly_counts = {"Apr": 3, "May": 5, "Jun": 8, "Jul": 12, "Aug": 15, "Sep": total}

    for fb in feedbacks:
        cat = fb.get("category", "Other")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        exp = fb.get("experience", 5)
        if exp == 5: exp_counts["5 Stars"] += 1
        elif exp == 4: exp_counts["4 Stars"] += 1
        elif exp == 3: exp_counts["3 Stars"] += 1
        elif exp == 2: exp_counts["2 Stars"] += 1
        elif exp == 1: exp_counts["1 Star"] += 1
        rec = fb.get("recommend", "Definitely Yes")
        rec_counts[rec] = rec_counts.get(rec, 0) + 1

    return {
        "total": total,
        "pending": pending,
        "resolved": resolved,
        "average_rating": avg_rating,
        "cat_counts": cat_counts,
        "exp_counts": exp_counts,
        "rec_counts": rec_counts,
        "monthly_counts": monthly_counts,
        "feedbacks": feedbacks
    }

def handle_feedback_action(data):
    action = data.get("action", "create")
    feedbacks = load_json("feedback_db.json", DEFAULT_FEEDBACKS)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if action == "create":
        fb_id = f"FB-{int(time.time()*1000) % 9000 + 1000}"
        rec = {
            "id": fb_id,
            "client_name": data.get("client_name", "Anonymous User"),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "category": data.get("category", "Solar EPC Contractor / Installer"),
            "experience": int(data.get("experience", 5)),
            "priority": data.get("priority", "Medium"),
            "clarity": data.get("clarity", "Extremely Clear"),
            "bom_utility": data.get("bom_utility", "Procurement-Ready"),
            "recommend": data.get("recommend", "Definitely Yes"),
            "comments": data.get("comments", "").strip(),
            "timestamp": now_str,
            "status": "Pending",
            "admin_reply": "",
            "replied_at": "",
            "replied_by": ""
        }
        feedbacks.insert(0, rec)
        save_json("feedback_db.json", feedbacks)

        if rec.get("email"):
            dispatch_email({
                "to": rec["email"],
                "subject": f"[VoltRoof] Feedback Received (#{rec['id']})",
                "template": "general",
                "data": {
                    "message": f"Dear {rec['client_name']},\n\nThank you for submitting your feedback regarding VoltRoof Solar PV Estimator.\nOur engineering team reviews every rating and recommendation."
                }
            })
        return {"success": True, "feedback": rec}

    elif action == "reply":
        target_id = data.get("id", "")
        reply_text = data.get("reply", "").strip()
        admin_user = data.get("admin", "Adarsha KM")
        fb = next((x for x in feedbacks if x["id"] == target_id), None)
        if not fb:
            return {"success": False, "error": f"Feedback {target_id} not found"}
        
        fb["admin_reply"] = reply_text
        fb["status"] = "Resolved"
        fb["replied_at"] = now_str
        fb["replied_by"] = admin_user
        save_json("feedback_db.json", feedbacks)

        if fb.get("email"):
            dispatch_email({
                "to": fb["email"],
                "subject": f"[VoltRoof] Response to your feedback (#{target_id})",
                "template": "general",
                "data": {
                    "message": f"Hello {fb.get('client_name', 'Client')},\n\nOur engineering team has responded to your feedback:\n\n\"{reply_text}\"\n\nThank you for helping us make VoltRoof better!\n— VoltRoof Clean Energy Technologies"
                }
            })

        return {"success": True, "feedback": fb}

    elif action == "toggle_status":
        target_id = data.get("id", "")
        fb = next((x for x in feedbacks if x["id"] == target_id), None)
        if not fb:
            return {"success": False, "error": f"Feedback {target_id} not found"}
        
        fb["status"] = "Pending" if fb.get("status") == "Resolved" else "Resolved"
        save_json("feedback_db.json", feedbacks)
        return {"success": True, "feedback": fb}

    elif action == "approve":
        target_id = data.get("id", "")
        fb = next((x for x in feedbacks if x["id"] == target_id), None)
        if not fb:
            return {"success": False, "error": f"Feedback {target_id} not found"}
        fb["status"] = "Approved"
        save_json("feedback_db.json", feedbacks)
        return {"success": True, "feedback": fb}

    elif action == "delete":
        target_id = data.get("id", "")
        feedbacks = [x for x in feedbacks if x["id"] != target_id]
        save_json("feedback_db.json", feedbacks)
        return {"success": True, "message": f"Feedback {target_id} deleted"}

    return {"success": False, "error": f"Unknown feedback action: {action}"}

# ==========================================
# 6. NODEMAILER / SMTP EMAIL ENGINE
# ==========================================
def dispatch_email(mail_data):
    to_email = mail_data.get("to", "")
    subject = mail_data.get("subject", "VoltRoof Notification")
    template_type = mail_data.get("template", "general")
    body_data = mail_data.get("data", {})
    attachments = mail_data.get("attachments", [])

    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    smtp_from = os.environ.get("SMTP_FROM", "VoltRoof Notifications <notifications@voltroof.in>")

    now_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    
    if template_type == "report_pdf":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><style>body{{font-family:'Segoe UI',sans-serif;background:#f8fafc;color:#1e293b;padding:24px}} .box{{max-width:600px;margin:0 auto;background:#fff;border-radius:12px;padding:32px;border:1px solid #e2e8f0;box-shadow:0 4px 12px rgba(0,0,0,0.05)}} .brand{{font-size:24px;font-weight:800;color:#0f172a;margin-bottom:12px}}</style></head>
        <body>
          <div class="box">
            <div class="brand">⚡ VoltRoof <span style="color:#10b981">Solar PV Estimator</span></div>
            <h2 style="margin:0 0 12px;color:#0f172a">Your Solar Engineering Report is Ready</h2>
            <p>Dear {body_data.get('customer_name', 'Customer')},</p>
            <p>Your comprehensive Solar PV design and Bill of Materials (BOM) estimation has been calculated with high precision.</p>
            <div style="background:#f1f5f9;border-radius:8px;padding:16px;margin:20px 0">
              <div><strong>System Capacity:</strong> {body_data.get('capacity_kw', '—')} kWp</div>
              <div><strong>Estimated Annual Yield:</strong> {body_data.get('annual_kwh', '—')} kWh/year</div>
              <div><strong>Net Plant Cost:</strong> ₹{body_data.get('net_cost', '—')}</div>
              <div><strong>Estimated Payback:</strong> {body_data.get('payback_years', '—')} Years</div>
            </div>
            <p>The complete official PDF report is attached to this email.</p>
            <p style="font-size:12px;color:#64748b;margin-top:32px">Generated on {now_str} · VoltRoof Clean Energy Technologies</p>
          </div>
        </body>
        </html>
        """
    elif template_type == "ticket_created":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family:'Segoe UI',sans-serif;padding:20px;background:#f8fafc">
          <div style="max-width:560px;margin:0 auto;background:#fff;border-radius:10px;padding:24px;border:1px solid #e2e8f0">
            <h3 style="color:#0f172a;margin-top:0">Support Ticket Received: #{body_data.get('id', '')}</h3>
            <p>Hello {body_data.get('client_name', 'Client')},</p>
            <p>Your technical assistance request has been received by the VoltRoof engineering desk.</p>
            <div style="background:#f1f5f9;padding:12px;border-radius:6px;margin:16px 0">
              <strong>Subject:</strong> {body_data.get('subject', '')}<br>
              <strong>Priority:</strong> {body_data.get('priority', 'Medium')}<br>
              <strong>Status:</strong> Open
            </div>
            <p>An engineer will review your request and reply shortly.</p>
          </div>
        </body>
        </html>
        """
    elif template_type == "ticket_reply":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family:'Segoe UI',sans-serif;padding:20px;background:#f8fafc">
          <div style="max-width:560px;margin:0 auto;background:#fff;border-radius:10px;padding:24px;border:1px solid #e2e8f0">
            <h3 style="color:#0f172a;margin-top:0">Update on Ticket #{body_data.get('ticket', {}).get('id', '')}</h3>
            <p>A new message has been posted on your ticket:</p>
            <div style="background:#ecfdf5;border-left:4px solid #10b981;padding:14px;border-radius:4px;margin:16px 0">
              <strong>{body_data.get('sender', 'Support Agent')}:</strong><br>
              <p style="margin:8px 0 0">{body_data.get('reply', '')}</p>
            </div>
            <p style="font-size:12px;color:#64748b">Log into the VoltRoof Portal to continue this conversation.</p>
          </div>
        </body>
        </html>
        """
    else:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family:'Segoe UI',sans-serif;padding:20px;background:#f8fafc">
          <div style="max-width:560px;margin:0 auto;background:#fff;border-radius:10px;padding:24px;border:1px solid #e2e8f0">
            <h3 style="color:#0f172a;margin-top:0">{subject}</h3>
            <p>{body_data.get('message', 'Notification from VoltRoof System.')}</p>
            <p style="font-size:12px;color:#64748b;margin-top:24px">Time: {now_str}</p>
          </div>
        </body>
        </html>
        """

    email_log_entry = {
        "id": f"mail-{int(time.time()*1000)}",
        "to": to_email,
        "subject": subject,
        "template": template_type,
        "timestamp": now_str,
        "status": "Queued",
        "attempts": 0,
        "has_attachments": len(attachments) > 0,
        "attachment_names": [a.get("filename", "file") for a in attachments],
        "html_preview": html_content
    }

    send_success = False
    error_msg = ""

    if smtp_user and smtp_pass:
        for attempt in range(1, 4):
            email_log_entry["attempts"] = attempt
            try:
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = smtp_from
                msg["To"] = to_email
                msg.set_content("Please enable HTML email to view this message.")
                msg.add_alternative(html_content, subtype="html")

                for att in attachments:
                    fname = att.get("filename", "attachment.bin")
                    raw = att.get("content_bytes")
                    if not raw and att.get("data_base64"):
                        b64 = att["data_base64"]
                        if "," in b64:
                            b64 = b64.split(",", 1)[1]
                        raw = base64.b64decode(b64)
                    if raw:
                        msg.add_attachment(raw, maintype="application", subtype="octet-stream", filename=fname)

                with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as s:
                    s.starttls()
                    s.login(smtp_user, smtp_pass)
                    s.send_message(msg)

                send_success = True
                email_log_entry["status"] = "Delivered (Live SMTP)"
                break
            except Exception as e:
                error_msg = str(e)
                time.sleep(1 * (2 ** attempt))
        if not send_success:
            email_log_entry["status"] = f"Failed Live SMTP: {error_msg} (Fallback to Local Log)"
    else:
        send_success = True
        email_log_entry["status"] = "Delivered (Local Simulation Log)"

    logs = load_json("email_logs.json", [])
    logs.insert(0, email_log_entry)
    save_json("email_logs.json", logs[:200])

    return {
        "success": True,
        "status": email_log_entry["status"],
        "log_id": email_log_entry["id"],
        "message": f"Email queued for {to_email}"
    }

# ==========================================
# 7. SOLAR POLICY DESK & POLICY HUB ENGINE
# ==========================================
DEFAULT_POLICIES = [
    {
        "id": "POL-2026-01",
        "type": "regulation",
        "title": "KERC Rooftop Solar Grid Connectivity Regulations (Order 2026)",
        "authority": "Karnataka Electricity Regulatory Commission (KERC)",
        "effective_date": "01-Apr-2026",
        "summary": "Governs net-metering and gross-metering connectivity for LT consumers up to 20 kW. Mandates IEEE 1547 and CEA safety compliance.",
        "sanctioned_load_cap": "100% of sanctioned load for LT installations",
        "tariff_inr": "₹8.05 / kWh benchmark",
        "file_url": "/uploads/policies/KERC_Solar_Regulations_2026.pdf",
        "status": "Active"
    },
    {
        "id": "POL-2026-02",
        "type": "subsidy",
        "title": "PM Surya Ghar Muft Bijli Yojana Central Financial Assistance",
        "authority": "Ministry of New and Renewable Energy (MNRE)",
        "effective_date": "01-Jan-2026",
        "summary": "Provides capital subsidy of ₹30,000 for 1 kW, ₹60,000 for 2 kW, and ₹78,000 for systems 3 kW and above for residential rooftops.",
        "subsidy_slabs": "1 kW: ₹30k | 2 kW: ₹60k | 3 kW+: ₹78k max",
        "file_url": "/uploads/policies/MNRE_Surya_Ghar_Guidelines.pdf",
        "status": "Active"
    },
    {
        "id": "POL-2026-03",
        "type": "technical",
        "title": "BESCOM Technical Interconnection Standards for Rooftop Solar",
        "authority": "Bangalore Electricity Supply Company (BESCOM)",
        "effective_date": "15-Feb-2026",
        "summary": "Technical criteria for 415V three-phase interconnection, islanding protection, and Class 1.0 bidirectional DLMS smart meter certification.",
        "file_url": "/uploads/policies/BESCOM_Interconnection_Standard.pdf",
        "status": "Active"
    }
]

def get_policies():
    return load_json("policies_db.json", DEFAULT_POLICIES)

def save_policies(policies):
    return save_json("policies_db.json", policies)

def handle_policy_action(data):
    action = data.get("action", "create")
    policies = get_policies()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if action == "create":
        new_id = f"POL-{datetime.datetime.now().year}-{len(policies)+1:02d}"
        rec = {
            "id": new_id,
            "type": data.get("type", "regulation"),
            "title": data.get("title", "Solar Policy Order"),
            "authority": data.get("authority", "KERC / MNRE / BESCOM"),
            "effective_date": data.get("effective_date", now_str),
            "summary": data.get("summary", ""),
            "sanctioned_load_cap": data.get("sanctioned_load_cap", "100% of sanctioned load"),
            "tariff_inr": data.get("tariff_inr", "₹8.05 / kWh"),
            "subsidy_slabs": data.get("subsidy_slabs", "Standard Subsidy"),
            "file_url": data.get("file_url", ""),
            "status": "Active"
        }
        policies.insert(0, rec)
        save_policies(policies)
        return {"success": True, "policy": rec}

    elif action == "delete":
        target_id = data.get("id", "")
        policies = [p for p in policies if p["id"] != target_id]
        save_policies(policies)
        return {"success": True, "message": f"Policy {target_id} deleted"}

    elif action == "update":
        target_id = data.get("id", "")
        p = next((x for x in policies if x["id"] == target_id), None)
        if not p:
            return {"success": False, "error": f"Policy {target_id} not found"}
        for k in ["title", "authority", "effective_date", "summary", "sanctioned_load_cap", "tariff_inr", "subsidy_slabs", "file_url", "status"]:
            if k in data:
                p[k] = data[k]
        save_policies(policies)
        return {"success": True, "policy": p}

    return {"success": False, "error": f"Unknown policy action: {action}"}

# ==========================================
# 8. CONTENT STUDIO SHOWCASE SLIDES ENGINE
# ==========================================
DEFAULT_SLIDES = [
    {
        "id": "slide-1",
        "image": "verified_page1.png",
        "title": "Karnataka Clean Energy Infrastructure",
        "body": "State-of-the-art rooftop solar engineering for residential, commercial & institutional complexes.",
        "order": 1,
        "status": "active"
    },
    {
        "id": "slide-2",
        "image": "voltroof_3d_perfect.png",
        "title": "Interactive 3D Rooftop Visualizer",
        "body": "Millimeter-precision tilt angles, azimuth tracking, and shadow-optimized module layouts.",
        "order": 2,
        "status": "active"
    },
    {
        "id": "slide-3",
        "image": "voltroof_bom_schedule.png",
        "title": "Procurement-Ready 12-Item BOM Engine",
        "body": "Complete switchgear, DC/AC cabling, earthing electrodes, and utility net-metering schedules.",
        "order": 3,
        "status": "active"
    }
]

def get_content_slides():
    return load_json("content_slides_db.json", DEFAULT_SLIDES)

def save_content_slides(slides):
    return save_json("content_slides_db.json", slides)

def handle_content_action(data):
    action = data.get("action", "add")
    slides = get_content_slides()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if action == "add":
        new_id = f"slide-{int(time.time()*1000)}"
        new_slide = {
            "id": new_id,
            "image": data.get("image", ""),
            "title": data.get("title", "New Showcase Slide"),
            "body": data.get("body", "VoltRoof clean energy presentation"),
            "order": len(slides) + 1,
            "status": "active"
        }
        slides.append(new_slide)
        save_content_slides(slides)
        return {"success": True, "slide": new_slide, "slides": slides}

    elif action == "delete":
        target_id = data.get("id", "")
        slides = [s for s in slides if s["id"] != target_id]
        for idx, s in enumerate(slides):
            s["order"] = idx + 1
        save_content_slides(slides)
        return {"success": True, "slides": slides}

    elif action == "reorder":
        new_orders = data.get("orders", [])
        order_map = {sid: idx + 1 for idx, sid in enumerate(new_orders)}
        for s in slides:
            if s["id"] in order_map:
                s["order"] = order_map[s["id"]]
        slides.sort(key=lambda x: x.get("order", 999))
        save_content_slides(slides)
        return {"success": True, "slides": slides}

    elif action == "save_all":
        all_slides = data.get("slides", [])
        if isinstance(all_slides, list):
            save_content_slides(all_slides)
            return {"success": True, "slides": all_slides}
        return {"success": False, "error": "Invalid slides array"}

    return {"success": False, "error": f"Unknown content action: {action}"}

# ==========================================
# 9. COMPREHENSIVE EQUIPMENT PRICING (SINGLE SOURCE OF TRUTH)
# ==========================================
def get_pricing_catalog():
    default_catalog = {
        "modules": {
            "name": "Solar PV Modules",
            "icon": "☀️",
            "category": "Generation",
            "benchmark": "₹18.00 – ₹22.00 / Wp",
            "unit": "₹ / Wp",
            "items": [
                {"id": "mod-400", "mfr": "Vikram Solar", "model": "Aditya 400 Mono PERC", "tech": "Mono PERC Mono-facial", "rating": "400 Wp", "efficiency": "20.2%", "warranty": "25 Years", "unit": "₹/Wp", "old_price": 19.80, "curr_price": 19.50, "new_price": 19.50, "availability": "In Stock", "specs": "108-Cell M10 Half-Cut, IP68, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_400w.png"},
                {"id": "mod-450", "mfr": "Tata Power Solar", "model": "TP450M Mono PERC", "tech": "Mono PERC Mono-facial", "rating": "450 Wp", "efficiency": "20.8%", "warranty": "25 Years", "unit": "₹/Wp", "old_price": 19.50, "curr_price": 19.20, "new_price": 19.20, "availability": "In Stock", "specs": "120-Cell Half-Cut, IP68, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_450w.png"},
                {"id": "mod-540", "mfr": "Waaree Energies", "model": "Arka 540 Bi-33", "tech": "Mono PERC Bifacial", "rating": "540 Wp", "efficiency": "21.2%", "warranty": "30 Years", "unit": "₹/Wp", "old_price": 18.80, "curr_price": 18.50, "new_price": 18.50, "availability": "In Stock", "specs": "144-Cell Bifacial Dual Glass, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_540w.png"},
                {"id": "mod-550", "mfr": "Waaree Energies", "model": "Waaree WS-550 Mono", "tech": "Mono PERC Mono-facial", "rating": "550 Wp", "efficiency": "21.5%", "warranty": "25 Years", "unit": "₹/Wp", "old_price": 18.50, "curr_price": 18.18, "new_price": 18.18, "availability": "In Stock", "specs": "144-Cell Half-Cut Mono PERC, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_550w.png"},
                {"id": "mod-580", "mfr": "Adani Solar", "model": "Elan Shine N-Type TOPCon", "tech": "TOPCon N-Type", "rating": "580 Wp", "efficiency": "22.2%", "warranty": "30 Years", "unit": "₹/Wp", "old_price": 21.00, "curr_price": 20.40, "new_price": 20.40, "availability": "In Stock", "specs": "144-Cell TOPCon N-Type Bifacial, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_580w.png"},
                {"id": "mod-600", "mfr": "Goldi Solar", "model": "Heloc Plus HJT 600", "tech": "HJT (Heterojunction)", "rating": "600 Wp", "efficiency": "22.8%", "warranty": "30 Years", "unit": "₹/Wp", "old_price": 24.00, "curr_price": 23.20, "new_price": 23.20, "availability": "In Stock", "specs": "Heterojunction Technology, Ultra-low temp coeff", "status": "active", "image": "/uploads/equipment/panel_600w.png"},
                {"id": "mod-335", "mfr": "RenewSys", "model": "Deserv 3K Poly", "tech": "Polycrystalline", "rating": "335 Wp", "efficiency": "17.1%", "warranty": "25 Years", "unit": "₹/Wp", "old_price": 16.50, "curr_price": 16.00, "new_price": 16.00, "availability": "In Stock", "specs": "72-Cell Standard Polycrystalline", "status": "active", "image": "/uploads/equipment/panel_335w.png"},
                {"id": "mod-680", "mfr": "Waaree Energies", "model": "Vertex Max 680 HJT", "tech": "Ultra-High Power G12", "rating": "680 Wp", "efficiency": "21.9%", "warranty": "30 Years", "unit": "?/Wp", "old_price": 25.50, "curr_price": 24.80, "new_price": 24.80, "availability": "In Stock", "specs": "132-Cell G12 Bifacial Dual Glass, 1500V DC", "status": "active", "image": "/uploads/equipment/panel_680w.png"},
                {"id": "mod-440", "mfr": "First Solar", "model": "Series 6 Plus CdTe", "tech": "Thin Film CdTe", "rating": "440 Wp", "efficiency": "18.6%", "warranty": "25 Years", "unit": "₹/Wp", "old_price": 22.00, "curr_price": 21.50, "new_price": 21.50, "availability": "In Stock", "specs": "Cadmium Telluride Advanced Thin Film", "status": "active", "image": "/uploads/equipment/panel_440w.png"}
            ]
        },
        "inverters": {
            "name": "Inverters & Power Conditioning",
            "icon": "⚡",
            "category": "Power Electronics",
            "benchmark": "₹9,500 – ₹12,000 / kW",
            "unit": "₹ / unit",
            "items": [
                {"id": "inv-1kw", "mfr": "Growatt", "model": "MIC 1000TL-X", "tech": "Grid-Tied String Inverter", "rating": "1 kW", "rating_kw": 1.0, "efficiency": "97.4%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 14000, "curr_price": 13500, "new_price": 13500, "availability": "In Stock", "specs": "Single Phase, 1 MPPT, OLED & Touch, IP65", "status": "active", "image": "/uploads/equipment/inverter_1kw.png"},
                {"id": "inv-2kw", "mfr": "Solis", "model": "S6-GR1P2K", "tech": "Grid-Tied String Inverter", "rating": "2 kW", "rating_kw": 2.0, "efficiency": "97.6%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 18500, "curr_price": 18000, "new_price": 18000, "availability": "In Stock", "specs": "Single Phase, 1 MPPT, Super high freq switching, IP66", "status": "active", "image": "/uploads/equipment/inverter_2kw.png"},
                {"id": "inv-3kw", "mfr": "Growatt", "model": "MIN 3000TL-X", "tech": "Grid-Tied String Inverter", "rating": "3 kW", "rating_kw": 3.0, "efficiency": "98.2%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 26000, "curr_price": 25500, "new_price": 25500, "availability": "In Stock", "specs": "Single Phase, Dual MPPT, WiFi/4G ready, IP65", "status": "active", "image": "/uploads/equipment/inverter_3kw.png"},
                {"id": "inv-5kw", "mfr": "Sungrow", "model": "SG5.0RS-ADA", "tech": "Dual-MPPT String Inverter", "rating": "5 kW", "rating_kw": 5.0, "efficiency": "98.4%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 41000, "curr_price": 40000, "new_price": 40000, "availability": "In Stock", "specs": "Single Phase, Dual MPPT, Built-in PID recovery, IP65", "status": "active", "image": "/uploads/equipment/inverter_5kw.png"},
                {"id": "inv-6kw", "mfr": "Solis", "model": "S5-GR3P6K", "tech": "Three-Phase String Inverter", "rating": "6 kW", "rating_kw": 6.0, "efficiency": "98.3%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 49500, "curr_price": 48000, "new_price": 48000, "availability": "In Stock", "specs": "Three Phase, Dual MPPT, Wide voltage range, IP66", "status": "active", "image": "/uploads/equipment/inverter_6kw.png"},
                {"id": "inv-8kw", "mfr": "Sungrow", "model": "SG8.0RT", "tech": "Three-Phase String Inverter", "rating": "8 kW", "rating_kw": 8.0, "efficiency": "98.5%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 62000, "curr_price": 60000, "new_price": 60000, "availability": "In Stock", "specs": "Three Phase, Dual MPPT, Smart IV curve scan, IP65", "status": "active", "image": "/uploads/equipment/inverter_8kw.png"},
                {"id": "inv-10kw", "mfr": "Sungrow", "model": "SG10RT Multi-MPPT", "tech": "Three-Phase Multi-MPPT Inverter", "rating": "10 kW", "rating_kw": 10.0, "efficiency": "98.6%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 74000, "curr_price": 72000, "new_price": 72000, "availability": "In Stock", "specs": "Three Phase, Dual MPPT, AFCI 2.0 safety, IP65", "status": "active", "image": "/uploads/equipment/inverter_10kw.png"},
                {"id": "inv-15kw", "mfr": "Sungrow", "model": "SG15RT High Yield", "tech": "Three-Phase Multi-MPPT Inverter", "rating": "15 kW", "rating_kw": 15.0, "efficiency": "98.7%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 98000, "curr_price": 95000, "new_price": 95000, "availability": "In Stock", "specs": "Three Phase, Dual MPPT, 30A DC input per MPPT, IP65", "status": "active", "image": "/uploads/equipment/inverter_15kw.png"},
                {"id": "inv-20kw", "mfr": "Fimer / ABB", "model": "PVI-20.0-TL-OUTD", "tech": "Three-Phase Commercial Inverter", "rating": "20 kW", "rating_kw": 20.0, "efficiency": "98.8%", "warranty": "10 Years Replacement", "unit": "₹/unit", "old_price": 122000, "curr_price": 118000, "new_price": 118000, "availability": "In Stock", "specs": "Three Phase, Dual independent MPPT, Transformerless, IP65", "status": "active", "image": "/uploads/equipment/inverter_20kw.png"}
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
                {"id": "dcdb-2", "mfr": "Elmex Electric", "tech": "2-In 2-Out IP65 with Type-II SPD", "rating": "1000V DC 32A", "unit": "₹/unit", "old_price": 7200, "curr_price": 7000, "new_price": 7000},
                {"id": "dcdb-3", "mfr": "Phoenix Contact", "tech": "4-In 2-Out Multi-String Array Box", "rating": "1000V DC 63A", "unit": "₹/unit", "old_price": 12500, "curr_price": 12000, "new_price": 12000}
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
                {"id": "acdb-2", "mfr": "Larsen & Toubro (L&T)", "tech": "Three Phase 32A with Type-II SPD", "rating": "415V AC IP65", "unit": "₹/unit", "old_price": 7200, "curr_price": 7000, "new_price": 7000},
                {"id": "acdb-3", "mfr": "Havells", "tech": "Three Phase 63A with Energy Meter Provision", "rating": "415V AC IP65", "unit": "₹/unit", "old_price": 9500, "curr_price": 9100, "new_price": 9100}
            ]
        },
        "spd": {
            "name": "Surge Protection Devices (SPD)",
            "icon": "⚡",
            "category": "Protection Devices",
            "benchmark": "₹1,800 – ₹4,500 / unit",
            "unit": "₹ / unit",
            "items": [
                {"id": "spd-1", "mfr": "Dehn / Phoenix", "tech": "Type 1+2 Combined Lightning & Surge", "rating": "1000V DC 40kA", "unit": "₹/unit", "old_price": 4200, "curr_price": 4000, "new_price": 4000},
                {"id": "spd-2", "mfr": "Schneider Electric", "tech": "Type 2 Surge Arrester 3P+N", "rating": "415V AC 40kA", "unit": "₹/unit", "old_price": 2800, "curr_price": 2600, "new_price": 2600},
                {"id": "spd-3", "mfr": "Citel", "tech": "Type 2 DC Surge Arrester 2-Pole", "rating": "1000V DC 20kA", "unit": "₹/unit", "old_price": 1950, "curr_price": 1850, "new_price": 1850}
            ]
        },
        "lightning_arrestor": {
            "name": "Lightning Arrestor (LA)",
            "icon": "🌩️",
            "category": "Safety & Protection",
            "benchmark": "₹3,500 – ₹7,000 / kit",
            "unit": "₹ / kit",
            "items": [
                {"id": "la-1", "mfr": "Standard Copper", "tech": "Franklin 5-Prong Pure Copper Rod", "rating": "1 Meter 25mm dia", "unit": "₹/unit", "old_price": 4200, "curr_price": 4000, "new_price": 4000},
                {"id": "la-2", "mfr": "Forend / Indelec", "tech": "ESE Early Streamer Emission Arrester", "rating": "Delta 25m Radius", "unit": "₹/unit", "old_price": 16500, "curr_price": 15800, "new_price": 15800}
            ]
        },
        "mc4": {
            "name": "MC4 Solar Connectors",
            "icon": "🔗",
            "category": "Connectors & Balance",
            "benchmark": "₹250 – ₹350 / pair",
            "unit": "₹ / pair",
            "items": [
                {"id": "mc4-1", "mfr": "Staubli Multi-Contact", "tech": "Original MC4 IP68 Snap-in", "rating": "1000V/1500V 30A", "unit": "₹/pair", "old_price": 320, "curr_price": 300, "new_price": 300},
                {"id": "mc4-2", "mfr": "Amphenol", "tech": "Helios H4 PV Connector", "rating": "1500V DC 32A", "unit": "₹/pair", "old_price": 280, "curr_price": 260, "new_price": 260},
                {"id": "mc4-3", "mfr": "Staubli", "tech": "Y-Branch Parallel Connector", "rating": "2-to-1 String Joiner", "unit": "₹/pair", "old_price": 550, "curr_price": 520, "new_price": 520}
            ]
        },
        "net_meter": {
            "name": "Net Meter & Generation Meter",
            "icon": "⏱️",
            "category": "Metering & Grid Interconnection",
            "benchmark": "₹4,500 – ₹12,000 / meter",
            "unit": "₹ / unit",
            "items": [
                {"id": "nm-1", "mfr": "Secure Meters", "tech": "Bi-directional 3-Phase Net Meter (Premier 300)", "rating": "3x240V 10-60A DLMS", "unit": "₹/unit", "old_price": 9500, "curr_price": 9000, "new_price": 9000},
                {"id": "nm-2", "mfr": "L&T Electrical", "tech": "Bi-directional Single Phase Meter", "rating": "240V 5-30A Class 1.0", "unit": "₹/unit", "old_price": 4200, "curr_price": 4000, "new_price": 4000},
                {"id": "nm-3", "mfr": "HPL Electric", "tech": "Solar Gross Generation Check Meter", "rating": "3-Phase 4-Wire Whole Current", "unit": "₹/unit", "old_price": 4800, "curr_price": 4500, "new_price": 4500}
            ]
        },
        "installation_labour": {
            "name": "Installation & Splicing Labour",
            "icon": "👷",
            "category": "EPC Services",
            "benchmark": "₹3,500 – ₹4,500 / kW",
            "unit": "₹ / kW",
            "items": [
                {"id": "lab-1", "mfr": "Certified Solar Crew", "tech": "Module Mounting & Mechanical Splicing", "rating": "Rooftop Splicing", "unit": "₹/kW", "old_price": 2200, "curr_price": 2100, "new_price": 2100},
                {"id": "lab-2", "mfr": "Certified Electricians", "tech": "Electrical Inverter, DCDB & Cable Laying", "rating": "Wiring & Terminations", "unit": "₹/kW", "old_price": 1400, "curr_price": 1350, "new_price": 1350},
                {"id": "lab-3", "mfr": "Earth Rig Team", "tech": "Pit Drilling, Backfilling & Earth Chamber", "rating": "3 Pits per system", "unit": "₹/kW", "old_price": 600, "curr_price": 550, "new_price": 550}
            ]
        },
        "testing_commissioning": {
            "name": "Testing & Commissioning",
            "icon": "🔬",
            "category": "EPC Services",
            "benchmark": "₹500 – ₹1,000 / kW",
            "unit": "₹ / kW",
            "items": [
                {"id": "tc-1", "mfr": "Licensed Chartered Engineer", "tech": "Pre-commissioning Megger & Earth Resistance Test", "rating": "Full System Verification", "unit": "₹/kW", "old_price": 650, "curr_price": 600, "new_price": 600},
                {"id": "tc-2", "mfr": "Solar QA Agency", "tech": "String Open-Circuit Voc & Short-Circuit Isc Test", "rating": "I-V Curve Check", "unit": "₹/kW", "old_price": 450, "curr_price": 400, "new_price": 400}
            ]
        },
        "transportation": {
            "name": "Transportation & Logistics",
            "icon": "🚚",
            "category": "Logistics",
            "benchmark": "₹400 – ₹800 / kW",
            "unit": "₹ / kW",
            "items": [
                {"id": "tr-1", "mfr": "Local Logistics", "tech": "Safe Freight Transit (Factory/Depot to Site)", "rating": "Up to 50 km", "unit": "₹/kW", "old_price": 450, "curr_price": 400, "new_price": 400},
                {"id": "tr-2", "mfr": "Rigging Team", "tech": "Terrace Hoisting / Crane Lifting to Roof", "rating": "Up to 4 Floors", "unit": "₹/kW", "old_price": 350, "curr_price": 300, "new_price": 300}
            ]
        },
        "statutory_fees": {
            "name": "Government & ESCOM Fees",
            "icon": "🏛️",
            "category": "Statutory Approvals",
            "benchmark": "₹3,000 – ₹6,000 / plant",
            "unit": "₹ / item",
            "items": [
                {"id": "gov-1", "mfr": "BESCOM / HESCOM / MESCOM", "tech": "Solar Online Portal Application Registration", "rating": "1 - 20 kW LT", "unit": "₹/appl", "old_price": 1000, "curr_price": 1000, "new_price": 1000},
                {"id": "gov-2", "mfr": "ESCOM Meter Testing", "tech": "Bi-directional Net Meter Calibration Fee", "rating": "DLMS Meter Test", "unit": "₹/meter", "old_price": 1500, "curr_price": 1500, "new_price": 1500},
                {"id": "gov-3", "mfr": "Electrical Inspectorate (CEIG)", "tech": "Statutory Safety Inspection (>10 kW installations)", "rating": "CEIG Approval", "unit": "₹/site", "old_price": 2500, "curr_price": 2500, "new_price": 2500}
            ]
        }
    }
    catalog = load_json("pricing_categories_db.json", default_catalog)
    # Ensure modules and inverters contain all required ratings if old catalog was saved
    if "modules" in catalog:
        existing_ratings = [m.get("rating", "") for m in catalog["modules"].get("items", [])]
        for req_m in default_catalog["modules"]["items"]:
            if req_m["rating"] not in existing_ratings:
                catalog["modules"]["items"].append(req_m)
    if "inverters" in catalog:
        existing_inv_ratings = [inv.get("rating", "") for inv in catalog["inverters"].get("items", [])]
        for req_inv in default_catalog["inverters"]["items"]:
            if req_inv["rating"] not in existing_inv_ratings:
                catalog["inverters"]["items"].append(req_inv)
    return catalog

def save_pricing_catalog(catalog):
    res = save_json("pricing_categories_db.json", catalog)
    sync_catalog_to_pricing_db(catalog)
    return res

def reset_pricing_catalog():
    if os.path.exists(get_file_path("pricing_categories_db.json")):
        try:
            os.remove(get_file_path("pricing_categories_db.json"))
        except Exception:
            pass
    return get_pricing_catalog()

def update_pricing_item(cat_key, item_id, new_price, user="admin"):
    catalog = get_pricing_catalog()
    if cat_key not in catalog:
        return {"success": False, "error": f"Category {cat_key} not found"}
    
    items = catalog[cat_key].get("items", [])
    target = next((x for x in items if x["id"] == item_id), None)
    if not target:
        return {"success": False, "error": f"Item {item_id} not found"}

    old = target.get("curr_price", 0)
    target["old_price"] = old
    target["curr_price"] = float(new_price)
    target["new_price"] = float(new_price)
    target["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    target["updated_by"] = user

    save_pricing_catalog(catalog)
    sync_catalog_to_pricing_db(catalog)

    audit = load_json("pricing_audit_db.json", [])
    audit.insert(0, {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": catalog[cat_key]["name"],
        "item": f"{target['mfr']} - {target.get('model', target.get('tech', ''))} ({target['rating']})",
        "old_price": old,
        "new_price": float(new_price),
        "diff": round(float(new_price) - old, 2),
        "user": user
    })
    save_json("pricing_audit_db.json", audit[:300])

    return {"success": True, "item": target}


def sync_catalog_to_pricing_db(catalog):
    pdb = load_json("pricing_db.json", {})
    if "modules" in catalog:
        m_items = catalog["modules"].get("items", [])
        m550 = next((m for m in m_items if "550" in str(m.get("rating", ""))), None)
        if m550 and "curr_price" in m550:
            pdb["module_per_wp"] = float(m550["curr_price"])
        elif m_items and "curr_price" in m_items[0]:
            pdb["module_per_wp"] = float(m_items[0]["curr_price"])
    if "inverters" in catalog:
        inv_items = catalog["inverters"].get("items", [])
        inv10 = next((i for i in inv_items if i.get("rating_kw") == 10.0), None)
        if inv10 and "curr_price" in inv10:
            pdb["inverter_per_kw"] = round(float(inv10["curr_price"]) / 10.0, 2)
        elif inv_items:
            rates = [float(i["curr_price"]) / max(1.0, float(i.get("rating_kw", 1.0))) for i in inv_items if "curr_price" in i]
            if rates:
                pdb["inverter_per_kw"] = round(sum(rates) / len(rates), 2)
    if "structures" in catalog:
        s_items = catalog["structures"].get("items", [])
        s1 = next((s for s in s_items if "HDGI" in s.get("tech", "")), s_items[0] if s_items else None)
        if s1 and "curr_price" in s1:
            pdb["structure_per_kw"] = float(s1["curr_price"])
    if "dc_cables" in catalog:
        dc_items = catalog["dc_cables"].get("items", [])
        d6 = next((d for d in dc_items if "6" in d.get("rating", "")), dc_items[0] if dc_items else None)
        if d6 and "curr_price" in d6:
            pdb["dc_cable_per_m"] = float(d6["curr_price"])
    if "ac_cables" in catalog:
        ac_items = catalog["ac_cables"].get("items", [])
        ac6 = next((a for a in ac_items if "6" in a.get("rating", "")), ac_items[0] if ac_items else None)
        if ac6 and "curr_price" in ac6:
            pdb["ac_cable_per_m"] = float(ac6["curr_price"])
    if "mc4" in catalog:
        mc4_items = catalog["mc4"].get("items", [])
        if mc4_items and "curr_price" in mc4_items[0]:
            pdb["mc4_per_pair"] = float(mc4_items[0]["curr_price"])
    if "dcdb" in catalog:
        dcdb_items = catalog["dcdb"].get("items", [])
        d2 = next((d for d in dcdb_items if "2-in" in d.get("rating", "")), dcdb_items[0] if dcdb_items else None)
        if d2 and "curr_price" in d2:
            pdb["dcdb_base"] = float(d2["curr_price"])
    if "acdb" in catalog:
        acdb_items = catalog["acdb"].get("items", [])
        a2 = next((a for a in acdb_items if "Three Phase" in a.get("rating", "")), acdb_items[0] if acdb_items else None)
        if a2 and "curr_price" in a2:
            pdb["acdb_base"] = float(a2["curr_price"])
    if "earthing" in catalog:
        eth_items = catalog["earthing"].get("items", [])
        e1 = eth_items[0] if eth_items else None
        if e1 and "curr_price" in e1:
            pdb["earthing_kit_base"] = float(e1["curr_price"]) * (3 if "pit" in e1.get("unit", "").lower() else 1)
    if "lightning_arrestor" in catalog:
        la_items = catalog["lightning_arrestor"].get("items", [])
        l1 = next((l for l in la_items if "Conventional" in l.get("tech", "")), la_items[0] if la_items else None)
        if l1 and "curr_price" in l1:
            pdb["lightning_arrester_base"] = float(l1["curr_price"])
    if "installation_labour" in catalog:
        inst_items = catalog["installation_labour"].get("items", [])
        if inst_items and "curr_price" in inst_items[0]:
            pdb["installation_per_kw"] = float(inst_items[0]["curr_price"])
    if "statutory_fees" in catalog:
        fees = catalog["statutory_fees"].get("items", [])
        for f in fees:
            fid = f.get("id", "")
            pr = float(f.get("curr_price", 0))
            if "reg" in fid: pdb["escom_application_fee"] = pr
            elif "scrutiny" in fid or "proc" in fid: pdb["escom_processing_fee"] = pr
            elif "meter" in fid: pdb["escom_net_meter"] = pr

    save_json("pricing_db.json", pdb)
    return pdb

def get_pricing_map():
    return load_json("pricing_db.json", {})

import sys

with open('solar_pv_estimator.py', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# 1. Add import backend_ext at top if not present
if "import backend_ext" not in code:
    code = "import backend_ext\n" + code

# 2. Add GET routes right before the fallback:
# elif parsed.path == "/api/admin/list": ...
get_hook = 'elif parsed.path == "/api/admin/list":'
get_replacement = '''# --- Enhanced Backend Extensions (GET) ---
        elif parsed.path == "/api/tickets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(backend_ext.get_tickets()).encode())
            return

        elif parsed.path == "/api/visitors/detailed":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(backend_ext.get_visitors_detailed()).encode())
            return

        elif parsed.path == "/api/pricing/categories":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(backend_ext.get_pricing_catalog()).encode())
            return

        elif parsed.path == "/api/admin/hierarchy":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(backend_ext.get_hierarchy()).encode())
            return

        elif parsed.path == "/api/email_logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(backend_ext.load_json("email_logs.json", [])).encode())
            return

        ''' + get_hook

if get_hook in code and '/api/tickets' not in code:
    code = code.replace(get_hook, get_replacement, 1)

# 3. Add POST routes right before `self.send_response(404)\n        self.end_headers()` at end of do_POST
post_hook = '''        self.send_response(404)
        self.end_headers()


def run_server(port: int = 5050):'''

post_replacement = '''        # --- Enhanced Backend Extensions (POST) ---
        elif parsed.path == "/api/upload":
            res = backend_ext.handle_upload(data)
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        elif parsed.path == "/api/tickets/action":
            res = backend_ext.handle_ticket_action(data)
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        elif parsed.path == "/api/visitors/action":
            res = backend_ext.handle_visitor_action(data)
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        elif parsed.path == "/api/admin/hierarchy/action":
            res = backend_ext.handle_hierarchy_action(data)
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        elif parsed.path == "/api/pricing/update_item":
            cat_key = data.get("cat_key", "")
            item_id = data.get("item_id", "")
            new_price = data.get("new_price", 0)
            user = data.get("user", "admin")
            res = backend_ext.update_pricing_item(cat_key, item_id, new_price, user)
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        elif parsed.path == "/api/send_email":
            res = backend_ext.dispatch_email(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        elif parsed.path == "/api/email/test":
            test_data = {
                "to": data.get("to", "test@voltroof.in"),
                "subject": "[VoltRoof Test] NodeMailer SMTP Diagnostic Verification",
                "template": "general",
                "data": {"message": "This is an automated SMTP transmission test from VoltRoof Production Suite."}
            }
            res = backend_ext.dispatch_email(test_data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return

        self.send_response(404)
        self.end_headers()


def run_server(port: int = 5050):'''

if post_hook in code and '/api/tickets/action' not in code:
    code = code.replace(post_hook, post_replacement, 1)

# Also ensure old dummy /api/send_email is replaced
old_dummy_email = '''        elif parsed.path == "/api/send_email":
            email = data.get("email", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"PDF report prepared for {email}"}).encode())
            return'''

if old_dummy_email in code:
    new_real_email = '''        elif parsed.path == "/api/send_email":
            res = backend_ext.dispatch_email(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return'''
    code = code.replace(old_dummy_email, new_real_email)

with open('solar_pv_estimator.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("solar_pv_estimator.py successfully updated with enhanced backend routes!")

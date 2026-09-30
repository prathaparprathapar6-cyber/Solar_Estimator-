import os

with open("solar_pv_estimator.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import shutil if not present
if "import shutil" not in content:
    content = content.replace("import sys\n", "import sys\nimport shutil\n")

# 2. Update do_GET in SolarAppRequestHandler
old_do_get = '''    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", ""):
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.exists(os.path.join(cur_dir, "index.html")):
                self.path = "/index.html"
            elif os.path.exists(os.path.join(cur_dir, "voltroof_solar_pv_estimator_standalone.html")):
                self.path = "/voltroof_solar_pv_estimator_standalone.html"
            elif os.path.exists(os.path.join(cur_dir, "voltroof_solar_pv_estimator.html")):
                self.path = "/voltroof_solar_pv_estimator.html"
            else:
                self.path = "/index.html"
        return super().do_GET()'''

new_do_get = '''    def do_GET(self):
        parsed = urlparse(self.path)
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        # Serve User Manual PDF
        if parsed.path in ("/user_manual.pdf", "/api/user_manual", "/api/user_manual/download"):
            manual_file = os.path.join(cur_dir, "user_manual.pdf")
            if os.path.exists(manual_file):
                try:
                    with open(manual_file, "rb") as f:
                        pdf_bytes = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/pdf")
                    self.send_header("Content-Disposition", 'inline; filename="VoltRoof_User_Manual.pdf"')
                    self.send_header("Content-Length", str(len(pdf_bytes)))
                    self.end_headers()
                    self.wfile.write(pdf_bytes)
                    return
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
                    return
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "User manual document not found"}).encode())
                return

        # Return User Manual Metadata
        elif parsed.path == "/api/user_manual_meta":
            manual_file = os.path.join(cur_dir, "user_manual.pdf")
            meta_file = os.path.join(cur_dir, "user_manual_meta.json")
            meta = {}
            if os.path.exists(meta_file):
                try:
                    with open(meta_file, "r", encoding="utf-8") as mf:
                        meta = json.load(mf)
                except Exception:
                    pass
            if not meta and os.path.exists(manual_file):
                st = os.stat(manual_file)
                meta = {
                    "exists": True,
                    "filename": "VoltRoof_User_Manual.pdf",
                    "size_bytes": st.st_size,
                    "updated_at": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%d-%b-%Y %H:%M"),
                    "updated_by": "Administrator"
                }
            elif not meta:
                meta = {"exists": False, "filename": "", "size_bytes": 0, "updated_at": "", "updated_by": ""}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(meta).encode())
            return

        if parsed.path in ("/", ""):
            if os.path.exists(os.path.join(cur_dir, "index.html")):
                self.path = "/index.html"
            elif os.path.exists(os.path.join(cur_dir, "voltroof_solar_pv_estimator_standalone.html")):
                self.path = "/voltroof_solar_pv_estimator_standalone.html"
            elif os.path.exists(os.path.join(cur_dir, "voltroof_solar_pv_estimator.html")):
                self.path = "/voltroof_solar_pv_estimator.html"
            else:
                self.path = "/index.html"
        return super().do_GET()'''

assert old_do_get in content, "old_do_get not found in solar_pv_estimator.py"
content = content.replace(old_do_get, new_do_get)

# 3. Update do_POST in SolarAppRequestHandler with upload_user_manual & admin login
old_do_post_end = '''        elif parsed.path == "/api/send_email":
            email = data.get("email", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"PDF report prepared for {email}"}).encode())
            return

        self.send_response(404)
        self.end_headers()'''

new_do_post_end = r'''        elif parsed.path == "/api/send_email":
            email = data.get("email", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"PDF report prepared for {email}"}).encode())
            return

        elif parsed.path == "/api/admin/upload_user_manual":
            try:
                raw_b64 = data.get("data_base64", "")
                filename = data.get("filename", "user_manual.pdf")
                admin_name = data.get("admin_name", "Administrator")
                if not raw_b64:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "No file content provided"}).encode())
                    return

                if "," in raw_b64:
                    raw_b64 = raw_b64.split(",", 1)[1]
                file_bytes = base64.b64decode(raw_b64)
                cur_dir = os.path.dirname(os.path.abspath(__file__))
                manual_file = os.path.join(cur_dir, "user_manual.pdf")
                with open(manual_file, "wb") as f:
                    f.write(file_bytes)

                # Also sync to Downloads directory if present
                downloads_dir = r"C:\Users\DELL\Downloads"
                if os.path.exists(downloads_dir):
                    try:
                        shutil.copy2(manual_file, os.path.join(downloads_dir, "VoltRoof_User_Manual.pdf"))
                        shutil.copy2(manual_file, os.path.join(downloads_dir, "user_manual.pdf"))
                    except Exception:
                        pass

                meta = {
                    "exists": True,
                    "filename": filename,
                    "size_bytes": len(file_bytes),
                    "updated_at": datetime.datetime.now().strftime("%d-%b-%Y %H:%M"),
                    "updated_by": admin_name
                }
                meta_file = os.path.join(cur_dir, "user_manual_meta.json")
                with open(meta_file, "w", encoding="utf-8") as mf:
                    json.dump(meta, mf, indent=2)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "message": "User manual updated successfully", "meta": meta}).encode())
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
                return

        elif parsed.path == "/api/admin/login":
            username_input = str(data.get("username", "")).strip()
            password_input = str(data.get("password", "")).strip()
            admins_list = INITIAL_ADMINS
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            adm_db_path = os.path.join(cur_dir, "admins_db.json")
            if os.path.exists(adm_db_path):
                try:
                    with open(adm_db_path, "r", encoding="utf-8") as af:
                        admins_list = json.load(af)
                except Exception:
                    pass

            matched_admin = None
            for adm in admins_list:
                u_match = (
                    adm.get("username", "").lower() == username_input.lower() or
                    any(em.lower() == username_input.lower() for em in adm.get("emails", [])) or
                    adm.get("mobile", "") == username_input
                )
                p_match = (adm.get("password", "") == password_input)
                if u_match and p_match:
                    matched_admin = adm
                    break

            if matched_admin:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "admin": {
                        "username": matched_admin.get("username"),
                        "role": matched_admin.get("role", "admin"),
                        "email": matched_admin.get("emails", [""])[0]
                    }
                }).encode())
                return
            else:
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Invalid username or password"}).encode())
                return

        self.send_response(404)
        self.end_headers()'''

assert old_do_post_end in content, "old_do_post_end not found in solar_pv_estimator.py"
content = content.replace(old_do_post_end, new_do_post_end)

with open("solar_pv_estimator.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated solar_pv_estimator.py with user manual routes successfully!")

import os
import zlib
import base64
import shutil

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
downloads_dir = r"C:\Users\DELL\Downloads"
brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d"

# 1. Read latest VoltRoof_Combined.html and compress
html_path = os.path.join(scratch_dir, "VoltRoof_Combined.html")
with open(html_path, "rb") as f:
    html_bytes = f.read()

comp_html = zlib.compress(html_bytes, level=9)
b64_html = base64.b64encode(comp_html).decode("ascii")

# 2. Update solar_pv_estimator.py
py_path = os.path.join(scratch_dir, "solar_pv_estimator.py")
with open(py_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.startswith("EMBEDDED_HTML_ZLIB_B64 ="):
        new_lines.append(f'EMBEDDED_HTML_ZLIB_B64 = "{b64_html}"\n')
        print(f"Replaced EMBEDDED_HTML_ZLIB_B64 on line {i+1} with new {len(b64_html):,} chars")
    else:
        new_lines.append(line)

with open(py_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# 3. Add VoltRoof_Combined.html extraction to ensure_standalone_assets
with open(py_path, "r", encoding="utf-8") as f:
    content = f.read()

old_ensure_end = '''    html_file = os.path.join(dir_path, "index.html")
    if not os.path.exists(html_file):
        try:
            raw_html = zlib.decompress(base64.b64decode(EMBEDDED_HTML_ZLIB_B64)).decode("utf-8")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(raw_html)
        except Exception:
            pass'''

new_ensure_end = '''    html_file = os.path.join(dir_path, "index.html")
    combined_file = os.path.join(dir_path, "VoltRoof_Combined.html")
    if not os.path.exists(html_file) or not os.path.exists(combined_file):
        try:
            raw_html = zlib.decompress(base64.b64decode(EMBEDDED_HTML_ZLIB_B64)).decode("utf-8")
            if not os.path.exists(html_file):
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(raw_html)
            if not os.path.exists(combined_file):
                with open(combined_file, "w", encoding="utf-8") as f:
                    f.write(raw_html)
        except Exception:
            pass'''

if old_ensure_end in content:
    content = content.replace(old_ensure_end, new_ensure_end, 1)
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated ensure_standalone_assets to extract both index.html and VoltRoof_Combined.html")

# 4. Copy updated solar_pv_estimator.py to Downloads and brain directory
for target_dir in [downloads_dir, brain_dir]:
    dst = os.path.join(target_dir, "solar_pv_estimator.py")
    shutil.copy2(py_path, dst)
    print(f"Copied solar_pv_estimator.py -> {dst}")

print("\n--- Python standalone file updated successfully! ---")

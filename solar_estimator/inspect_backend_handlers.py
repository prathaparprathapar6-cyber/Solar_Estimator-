import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("backend_ext.py", "r", encoding="utf-8") as f:
    text = f.read()

handlers = [
    "handle_upload", "handle_upload_delete", "handle_ticket_action", "handle_visitor_action",
    "handle_hierarchy_action", "handle_feedback_action", "dispatch_email", "handle_policy_action",
    "handle_content_action", "update_pricing_item", "save_pricing_catalog", "reset_pricing_catalog"
]

import re
for h in handlers:
    idx = text.find(f"def {h}")
    if idx != -1:
        # print up to next def
        next_def = text.find("\ndef ", idx+1)
        chunk = text[idx:next_def if next_def != -1 else idx+2000]
        # find all 'action == ' or similar
        actions = re.findall(r'action\s*==\s*["\']([^"\']+)["\']', chunk)
        print(f"=== {h} ===")
        print(f"Supported actions: {actions}")
        print(chunk[:400] + ("..." if len(chunk) > 400 else ""))
        print("-" * 50)

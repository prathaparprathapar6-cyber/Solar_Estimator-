import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

queries = [
    "sendTicketReply", "updateTicketStatus", "pdLoad", "pdSave", "pdRenderAdminList",
    "renderFeedbackTable", "replyFeedback", "deleteFeedback", "updateHierarchyRole",
    "removeHierarchyUser", "addHierarchyUser", "sendEmailReport", "generateQuote", "downloadPdf"
]

for q in queries:
    pos = 0
    found = []
    while True:
        idx = text.find(q, pos)
        if idx == -1:
            break
        # Print surrounding 200 chars
        snippet = text[max(0, idx-50):min(len(text), idx+250)]
        found.append((idx, snippet))
        pos = idx + len(q)
    print(f"=== Query: {q} (Occurrences: {len(found)}) ===")
    for idx, snip in found[:3]:
        print(f"[{idx}]: {repr(snip)}")
    print("-" * 50)

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("VoltRoof_Combined.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "tdReplyText" in l or "tdSendReply" in l or "openTicketDetail" in l or "renderTicketMessages" in l or "tdStatusSelect" in l:
        print(f"Line {i+1}: {l.strip()[:100]}")

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('VoltRoof_Combined.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("File size:", len(text), "bytes")
print("Total lines:", len(text.splitlines()))

# Check sections
sections = [
    '<div class="name-gate',
    '<aside class="sidebar"',
    'id="adminNavSec"',
    'id="view-dashboard"',
    'id="view-adminDashboard"',
    'id="view-adminPricing"',
    'id="view-policyDesk"',
    'id="view-contentStudio"',
    'id="view-adminTeam"',
    'id="view-adminUsers"',
    'id="view-adminManual"',
    'id="view-adminVisitors"',
    'id="view-adminFeedback"',
    'id="view-adminAudit"',
    'id="view-adminSettings"',
    'id="view-adminTickets"',
    'id="unsavedBanner"'
]

for s in sections:
    pos = text.find(s)
    print(f"Section {s}: pos {pos}")

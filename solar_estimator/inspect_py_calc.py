with open("solar_pv_estimator.py", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find("def build_system_report(")
print("build_system_report signature:")
print(text[idx:idx+400])

idx_post = text.find("def do_POST(")
print("\ndo_POST snippet:")
print(text[idx_post:idx_post+600])

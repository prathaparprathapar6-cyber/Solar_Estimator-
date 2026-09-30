import sys
sys.stdout.reconfigure(encoding='utf-8')

media_html = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.user_uploaded\media_1790335657134.html"

with open(media_html, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx_modals = text.rfind('<div class="name-gate" id="modalFeedback"')
print(f"modalFeedback located at: {idx_modals}")
print("End of HTML snippet:")
print(text[-2000:])

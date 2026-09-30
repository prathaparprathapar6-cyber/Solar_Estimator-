with open('VoltRoof_Combined.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'function timeGreetingWord(h) {\n  h = typeof h === "number" ? h : new Date().getHours();\n  if (h < 12) return (h % 2 === 0 ? "Good morning" : "Good day");\n  if (h < 17) return "Good afternoon";\n  if (h < 21) return "Good evening";\n  return "Good night";\n}'

replacement = '''function timeGreetingWord(h) {
  h = typeof h === "number" ? h : new Date().getHours();
  if (h < 12) return (h % 2 === 0 ? "Good morning" : "Good day");
  if (h < 17) return "Good afternoon";
  if (h < 21) return "Good evening";
  return "Good night";
}

function loadCustomGreetings() {
  try {
    const a = JSON.parse(localStorage.getItem(VR_GREET_KEY) || "[]");
    return Array.isArray(a) ? a.filter(Boolean) : [];
  } catch (e) { return []; }
}'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open('VoltRoof_Combined.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added loadCustomGreetings back to VoltRoof_Combined.html")
else:
    print("Target not found")

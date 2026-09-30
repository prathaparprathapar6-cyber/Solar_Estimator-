import json

transcript_path = r"C:\Users\DELL\.gemini\antigravity\brain\de43946a-320e-4f83-b5e8-e03abab7f14d\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in transcript_full: {len(lines)}")
for i in range(max(0, len(lines)-10), len(lines)):
    obj = json.loads(lines[i])
    c = obj.get("content", "")
    media = obj.get("media", [])
    print(f"Line {i}: step_index={obj.get('step_index')}, type={obj.get('type')}, source={obj.get('source')}, len={len(c)}, media={len(media)}")
    if "<!DOCTYPE html>" in c:
        idx = c.find("<!DOCTYPE html>")
        print(f"  FOUND <!DOCTYPE html> in line {i} at offset {idx}")
        with open("attached_user_input.html", "w", encoding="utf-8") as out_f:
            out_f.write(c[idx:])
        with open("VoltRoof_A_to_Z_Handoff.md", "w", encoding="utf-8") as h_f:
            h_f.write(c[:idx])
        print("  Wrote attached_user_input.html and VoltRoof_A_to_Z_Handoff.md!")
    if media:
        print("  media entries:", media)

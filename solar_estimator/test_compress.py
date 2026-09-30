import zlib
import base64

with open('VoltRoof_Combined.html', 'rb') as f:
    raw_bytes = f.read()

comp = zlib.compress(raw_bytes, level=9)
b64_str = base64.b64encode(comp).decode('ascii')
print(f"Original size: {len(raw_bytes):,} bytes")
print(f"Compressed size: {len(comp):,} bytes")
print(f"Base64 length: {len(b64_str):,} chars")

# Verify round trip
round_trip = zlib.decompress(base64.b64decode(b64_str.encode('ascii')))
print("Round trip matches exactly:", round_trip == raw_bytes)

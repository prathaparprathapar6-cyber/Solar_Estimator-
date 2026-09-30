import sys
import backend_ext

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

catalog = backend_ext.get_pricing_catalog()
print("Total categories:", len(catalog))
for cat_key, cat_data in catalog.items():
    title = cat_data.get("title", cat_key)
    items = cat_data.get("items", [])
    print(f"\n[{cat_key}] {title} - {len(items)} items")
    for it in items[:2]:
        filtered = {k: v for k, v in it.items() if k not in ['specs', 'desc']}
        print("  ", repr(filtered))

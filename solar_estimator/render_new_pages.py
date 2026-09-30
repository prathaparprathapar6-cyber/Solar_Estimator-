import pypdfium2 as pdfium

doc = pdfium.PdfDocument("test_multi_site_new.pdf")
print(f"Rendering pages from test_multi_site_new.pdf (Total {len(doc)} pages)...")

# Render Page 6 (Site 1 BOM), Page 7 (Site 2 BOM), Page 8 (Grand Total Matrix)
for p_no in [6, 7, 8]:
    page = doc[p_no - 1]
    pix = page.render(scale=2.0)
    img = pix.to_pil()
    img_path = f"multi_site_new_p{p_no}.png"
    img.save(img_path)
    print(f"Saved {img_path} ({img.width}x{img.height})")

print("Finished rendering selected pages!")

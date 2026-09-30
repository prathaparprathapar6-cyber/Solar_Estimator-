import pypdfium2 as pdfium

doc = pdfium.PdfDocument("test_single_site_new.pdf")
print(f"Single-site pages: {len(doc)}")
for p_no in [1, 2, 3]:
    page = doc[p_no - 1]
    pix = page.render(scale=2.0)
    img = pix.to_pil()
    img_path = f"single_site_new_p{p_no}.png"
    img.save(img_path)
    print(f"Saved {img_path}")

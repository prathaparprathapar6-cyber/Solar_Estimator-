import pypdfium2 as pdfium
import os

scratch_dir = r"C:\Users\DELL\.gemini\antigravity\scratch\solar_estimator"
pdf_path = os.path.join(scratch_dir, "test_multi_site.pdf")

pdf = pdfium.PdfDocument(pdf_path)
print(f"Total pages in {os.path.basename(pdf_path)}: {len(pdf)}")

for i, page in enumerate(pdf):
    # Render at scale 2 (144 DPI) for crisp readable preview
    image = page.render(scale=2.0).to_pil()
    out_name = f"multi_site_p{i+1}.png"
    out_path = os.path.join(scratch_dir, out_name)
    image.save(out_path)
    print(f"Saved {out_name} ({image.width}x{image.height})")

print("Finished rendering all pages!")

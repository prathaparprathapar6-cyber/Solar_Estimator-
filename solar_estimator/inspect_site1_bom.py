import pypdfium2 as pdfium

doc = pdfium.PdfDocument("test_multi_site_new.pdf")
print("=== PAGE 6 TEXT ===")
page = doc[5] # 0-indexed, so page 6
text = page.get_textpage().get_text_range()
print(text)

print("=== PAGE 7 TEXT ===")
page7 = doc[6]
text7 = page7.get_textpage().get_text_range()
print(text7)

print("=== PAGE 8 TEXT ===")
page8 = doc[7]
text8 = page8.get_textpage().get_text_range()
print(text8)

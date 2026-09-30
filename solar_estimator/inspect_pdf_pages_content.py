import pypdfium2 as pdfium

doc = pdfium.PdfDocument("test_multi_site_new.pdf")
print(f"Total pages: {len(doc)}")
for i, page in enumerate(doc):
    text = page.get_textpage().get_text_range()
    headings = []
    for l in text.splitlines():
        l = l.strip()
        if any(k in l for k in ['[PORTFOLIO]', '[ALLOCATION]', '[ARRAY]', '[INVERTER]', '[MCB]', '[CABLES]', '[ACDB]', '[SITE BOM]', '[UTILITY]', '[PORTFOLIO TOTAL]', '[CAPEX MATRIX]', '[FINANCE]', '[ANALYTICS]']):
            headings.append(l)
        elif 'Bill of Materials' in l or 'Amortization' in l or 'Generation Analytics' in l or 'Architecture' in l or 'Portfolio' in l:
            headings.append(l)
    print(f"Page {i+1}: {headings}")

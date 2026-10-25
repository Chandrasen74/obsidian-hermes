import pymupdf

src = r"C:\Users\Kanchan Verma\Downloads\Grade_10_Computer_Applications_165_HTML_Practical_File.pdf"
doc = pymupdf.open(src)
for i in (0, 1):
    page = doc[i]
    print(f"=== PAGE {i+1} ===")
    d = page.get_text("dict")
    for block in d["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if "_" in span["text"]:
                    print(f"size={span['size']:.1f} font={span['font']} bbox={[round(v,1) for v in span['bbox']]} text={span['text']!r}")
    print("underline-like drawings:")
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.width > 60 and r.height < 3:
            print("  line", [round(v,1) for v in r])

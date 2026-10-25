import pymupdf

src = r"C:\Users\Kanchan Verma\Downloads\Grade_10_Computer_Applications_165_HTML_Practical_File.pdf"
doc = pymupdf.open(src)
page = doc[1]
raw = page.get_text("rawdict")
for block in raw["blocks"]:
    for line in block.get("lines", []):
        text = "".join(ch["c"] for span in line["spans"] for ch in span["chars"])
        if "certify that" in text:
            for span in line["spans"]:
                chars = span["chars"]
                s = "".join(c["c"] for c in chars)
                idx = s.find("_")
                if idx >= 0:
                    run = chars[idx:]
                    print("underscore run x:", round(run[0]["bbox"][0], 1), "to", round(run[-1]["bbox"][2], 1))
                    print("baseline y:", round(run[0]["bbox"][3], 1), "font size:", span["size"])
                # section blank
                sidx = s.find("Section")
                if sidx >= 0:
                    tail = s[sidx:]
                    bidx = tail.find("_")
                    if bidx >= 0:
                        rc = chars[sidx + bidx:]
                        print("section blank x:", round(rc[0]["bbox"][0], 1), "to", round(rc[-1]["bbox"][2], 1))

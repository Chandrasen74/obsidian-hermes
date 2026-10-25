import pymupdf

path = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\manas html practical grade 10\Grade_10_HTML_Practical_File_with_outputs.pdf"
doc = pymupdf.open(path)
font = pymupdf.Font("helv")
SIZE = 11

def centered(text, x0, x1, baseline, size=SIZE):
    w = font.text_length(text, fontsize=size)
    return (x0 + x1) / 2 - w / 2, baseline

# --- Cover page ---
cover = doc[0]
cover.insert_text((320, 281.5), "Manas", fontname="helv", fontsize=SIZE, color=(0, 0, 0))
cover.insert_text((320, 299.5), "X", fontname="helv", fontsize=SIZE, color=(0, 0, 0))

# --- Certificate ---
cert = doc[1]
x, y = centered("Manas", 167.0, 367.2, 110.7, 12)
cert.insert_text((x, y), "Manas", fontname="helv", fontsize=12, color=(0, 0, 0))

doc.saveIncr()
print("filled name and class")

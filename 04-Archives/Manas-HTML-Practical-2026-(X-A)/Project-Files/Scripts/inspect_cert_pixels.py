import io
import pymupdf
from PIL import Image

p = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\manas html practical grade 10\Grade_10_HTML_Practical_File_with_outputs.pdf"
doc = pymupdf.open(p)
page = doc[1]
dpi = 300
s = dpi / 72
im = Image.open(io.BytesIO(page.get_pixmap(dpi=dpi).tobytes("png"))).convert("L")
px = im.load()

def rowdark(y0, y1, x0, x1):
    out = []
    for y in range(int(y0 * s), int(y1 * s)):
        n = sum(1 for x in range(int(x0 * s), int(x1 * s), 2) if px[x, y] < 120)
        out.append((round(y / s, 1), n))
    return out

print("name blank area rows (x 167-367):")
for y, n in rowdark(95, 118, 167, 367):
    if n:
        print(f"  y={y}  dark={n}")
print("section blank area rows (x 470-515):")
for y, n in rowdark(95, 118, 470, 515):
    if n:
        print(f"  y={y}  dark={n}")

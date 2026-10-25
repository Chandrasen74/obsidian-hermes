import os
import pymupdf

folder = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\manas html practical grade 10"
path = os.path.join(folder, "Grade_10_HTML_Practical_File_with_outputs.pdf")
doc = pymupdf.open(path)
for i in range(3, 13):
    page = doc[i]
    img = page.get_images(full=True)[0]
    info = doc.extract_image(img[0])
    border = [d["rect"] for d in page.get_drawings()
              if d["rect"].width > 100 and d["rect"].y0 > 250 and d["rect"].y1 < 740]
    print(f"page {i+1}: {info['ext']} {info['width']}x{info['height']} "
          f"border={[round(v) for v in border[0]] if border else None}")
print("pdf size KB:", os.path.getsize(path) // 1024)

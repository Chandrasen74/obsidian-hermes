import glob
import os
from PIL import Image, ImageChops
import pymupdf

FOLDER = r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\manas html practical grade 10"
SHOTS = os.path.join(FOLDER, "screenshots")
CROPS = os.path.join(SHOTS, "cropped")
SRC = r"C:\Users\Kanchan Verma\Downloads\Grade_10_Computer_Applications_165_HTML_Practical_File.pdf"
OUT = os.path.join(FOLDER, "Grade_10_HTML_Practical_File_with_outputs.pdf")

os.makedirs(CROPS, exist_ok=True)


def crop_to_content(src_png, dst_png, pad=24):
    im = Image.open(src_png).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    mask = diff.convert("L").point(lambda v: 255 if v > 18 else 0)
    bbox = mask.getbbox() or (0, 0, im.width, im.height)
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(im.width, x1 + pad), min(im.height, y1 + pad)
    im.crop((x0, y0, x1, y1)).save(dst_png, "PNG")
    return x1 - x0, y1 - y0


for png in sorted(glob.glob(os.path.join(SHOTS, "*.png"))):
    base = os.path.splitext(os.path.basename(png))[0]
    crop_to_content(png, os.path.join(CROPS, base + ".png"))
    Image.open(os.path.join(CROPS, base + ".png")).convert("RGB").save(
        os.path.join(CROPS, base + ".jpg"), "JPEG", quality=92, dpi=(300, 300), optimize=True
    )

doc = pymupdf.open(SRC)

# --- screenshots under each Expected Output ---
for page_no in range(4, 14):
    page = doc[page_no - 1]
    exp = None
    for b in page.get_text("blocks"):
        if b[6] == 0 and "Expected Output" in b[4]:
            exp = b
    box = pymupdf.Rect(57, exp[3] + 12, 555, 730)
    n = page_no - 3
    base = "practical10_submitted" if n == 10 else f"practical{n}"
    path = os.path.join(CROPS, base + ".jpg")
    pix = pymupdf.Pixmap(path)
    scale = min(box.width / pix.width, box.height / pix.height)
    w, h = pix.width * scale, pix.height * scale
    x = box.x0 + (box.width - w) / 2
    r = pymupdf.Rect(x, box.y0, x + w, box.y0 + h)
    page.insert_image(r, filename=path)
    page.draw_rect(r + (-3, -3, 3, 3), color=(0, 0, 0), width=0.8)

# --- fill cover fields like the printed "Academic Session" value ---
cover = doc[0]
VALUES = [("Manas", 281.5), ("X-A", 299.5)]  # name row, class & section row
for text, baseline in VALUES:
    cover.draw_rect(pymupdf.Rect(309, baseline - 13.5, 460, baseline + 1.5),
                    color=None, fill=(1, 1, 1), width=0)
    cover.insert_text((311.2, baseline), text, fontname="helv", fontsize=10, color=(0, 0, 0))

# --- certificate: inline blanks ---
cert = doc[1]
font = pymupdf.Font("helv")


def write_centered(page, text, x0, x1, baseline, size=12):
    w = font.text_length(text, fontsize=size)
    page.insert_text(((x0 + x1) / 2 - w / 2, baseline), text,
                     fontname="helv", fontsize=size, color=(0, 0, 0))


write_centered(cert, "Manas", 167.0, 367.2, 107.0)
write_centered(cert, "A", 475.2, 508.6, 107.0)

doc.save(OUT, deflate=True, garbage=3)
print("saved", OUT)

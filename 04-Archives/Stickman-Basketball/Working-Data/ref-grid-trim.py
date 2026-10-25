# Compose the reference frames into a labeled grid PDF (3x2 per page), animation section only (f000-f140).
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\ref-frames")
OUT = Path(r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\animate\reference-frames.pdf")

KEEP_MAX = 140          # f145+ is the "10 hours" title card in the source clip
COLS, ROWS = 3, 2
CW, CH = 600, 338
GAP, MARGIN, TITLE = 16, 16, 44
fb = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
ft = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)

cells = []
for p in sorted(SRC.glob("f*.png")):
    n = (int(p.stem[1:]) - 1) * 5
    if n > KEEP_MAX:
        continue
    im = Image.open(p).convert("RGB").resize((CW, CH), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    label = f"f {n:03d}   t {n/30.0:5.2f}s"
    tw = d.textlength(label, font=fb)
    d.rectangle([CW - tw - 16, CH - 34, CW, CH], fill=(20, 16, 12))
    d.text((CW - tw - 8, CH - 30), label, font=fb, fill=(255, 244, 224))
    cells.append(im)

pw = MARGIN * 2 + COLS * CW + (COLS - 1) * GAP
ph = TITLE + MARGIN * 2 + ROWS * CH + (ROWS - 1) * GAP
per = COLS * ROWS
npages = (len(cells) + per - 1) // per
pages = []
for i in range(npages):
    page = Image.new("RGB", (pw, ph), (246, 238, 222))
    d = ImageDraw.Draw(page)
    head = ("REFERENCE FRAMES - stickman basketball, flat cartoon style "
            f"(1280x720, 30fps, frames f000-f140 = 0.0-4.7s, one frame every 5th = 0.167s apart) "
            f"- page {i + 1}/{npages}")
    d.text((MARGIN, 12), head, font=ft, fill=(40, 28, 16))
    for j in range(per):
        k = i * per + j
        if k >= len(cells):
            break
        cx = MARGIN + (j % COLS) * (CW + GAP)
        cy = TITLE + MARGIN + (j // COLS) * (CH + GAP)
        page.paste(cells[k], (cx, cy))
        d.rectangle([cx - 1, cy - 1, cx + CW, cy + CH], outline=(120, 96, 64), width=1)
    pages.append(page)

pages[0].save(OUT, "PDF", save_all=True, append_images=pages[1:], resolution=96, quality=88)
print(f"{len(cells)} frames - {npages} pages - {OUT}")

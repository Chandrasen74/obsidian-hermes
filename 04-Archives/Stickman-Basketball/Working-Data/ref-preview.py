# Quick preview: whole reference as one small labeled contact sheet (for a human/vision check, not the deliverable).
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\ref-frames")
OUT = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\ref-preview.png")

COLS, CW, CH, GAP, MARGIN = 6, 300, 169, 8, 10
fb = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 14)

frames = sorted(SRC.glob("f*.png"))
cells = []
for p in frames:
    im = Image.open(p).convert("RGB").resize((CW, CH), Image.LANCZOS)
    n = (int(p.stem[1:]) - 1) * 5
    d = ImageDraw.Draw(im)
    label = f"f{n:03d} t{n/30.0:4.1f}s"
    d.rectangle([0, CH - 20, 110, CH], fill=(20, 16, 12))
    d.text((4, CH - 19), label, font=fb, fill=(255, 244, 224))
    cells.append(im)

rows = (len(cells) + COLS - 1) // COLS
W = MARGIN * 2 + COLS * CW + (COLS - 1) * GAP
H = MARGIN * 2 + rows * CH + (rows - 1) * GAP
sheet = Image.new("RGB", (W, H), (240, 232, 216))
for i, c in enumerate(cells):
    x = MARGIN + (i % COLS) * (CW + GAP)
    y = MARGIN + (i // COLS) * (CH + GAP)
    sheet.paste(c, (x, y))
sheet.save(OUT, quality=90)
print(OUT, sheet.size)

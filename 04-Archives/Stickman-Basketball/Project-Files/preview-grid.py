from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\projects\animate\deliverables")
TMP = Path(r"C:\Users\Kanchan Verma\AppData\Local\Temp\opencode\preview")
TMP.mkdir(exist_ok=True)
cells = [("stickman-dunk-sfx", 2.8, "dunk 2.8s (slam)"), ("stickman-dunk-sfx", 4.4, "dunk 4.4s (10 / 10)"),
         ("stickman-layup-sfx", 1.0, "layup 1.0s (drive)"), ("stickman-layup-sfx", 4.4, "layup 4.4s (make)")]
CW, CH = 760, 428
fb = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
sheet = Image.new("RGB", (CW * 2 + 24, CH * 2 + 24), (230, 224, 212))
d = ImageDraw.Draw(sheet)
for i, (name, t, label) in enumerate(cells):
    p = TMP / f"{name}-{t}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(OUT / f"{name}.mp4"), "-ss", str(t),
                    "-frames:v", "1", str(p)], check=True)
    im = Image.open(p).convert("RGB").resize((CW, CH), Image.LANCZOS)
    x = 8 + (i % 2) * (CW + 8)
    y = 8 + (i // 2) * (CH + 8)
    sheet.paste(im, (x, y))
    d.rectangle([x, y + CH - 30, x + 250, y + CH], fill=(20, 16, 12))
    d.text((x + 8, y + CH - 27), label, font=fb, fill=(255, 244, 224))
sheet.save(TMP / "graded-preview.png", quality=90)
print(TMP / "graded-preview.png", sheet.size)

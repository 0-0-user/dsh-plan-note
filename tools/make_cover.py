"""Render the Xiaohongshu cover slide (1080x1440): loud headline, same visual system."""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = r"D:\Users\xu\Documents\dsh-plan-note"
DOCS = os.path.join(ROOT, "docs")

BG = (13, 17, 23)
LINE = (42, 54, 72)
TEXT = (235, 239, 247)
MUTED = (141, 157, 180)
BLUE = (77, 107, 254)
CYAN = (86, 204, 242)
ORANGE = (255, 159, 67)

FONT_ZH_B = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_ZH = r"C:\Windows\Fonts\msyh.ttc"
FONT_MONO = r"C:\Windows\Fonts\consolab.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), "Desktop", "dsh-plan-note-poster")
    os.makedirs(out_dir, exist_ok=True)

    w, h = 1080, 1440
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)

    for x in range(0, w, 40):
        d.line([(x, 0), (x, h)], fill=(17, 22, 31))
    for y in range(0, h, 40):
        d.line([(0, y), (w, y)], fill=(17, 22, 31))
    d.rectangle([24, 24, w - 25, h - 25], outline=LINE, width=2)

    # brand, centred and small
    mark = Image.open(os.path.join(DOCS, "mark.png")).convert("RGBA")
    mark.thumbnail((70, 70), Image.LANCZOS)
    word = Image.open(os.path.join(DOCS, "brand.png")).convert("RGBA")
    word.thumbnail((250, 100), Image.LANCZOS)
    total = mark.width + 14 + word.width
    bx = (w - total) // 2
    img.paste(mark, (bx, 68), mark)
    img.paste(word, (bx + mark.width + 14, 76), word)

    # tag chip
    chip = "免费 · 开源 · 一条命令装好"
    f_chip = font(FONT_ZH, 26)
    cw = d.textlength(chip, font=f_chip)
    cx = (w - cw) / 2
    d.rounded_rectangle([cx - 26, 200, cx + cw + 26, 254], radius=27, outline=ORANGE, width=2)
    d.text((cx, 212), chip, font=f_chip, fill=ORANGE)

    # headline
    f1 = font(FONT_ZH_B, 92)
    f2 = font(FONT_ZH_B, 118)
    f3 = font(FONT_ZH_B, 92)

    def centered(text, fnt, y, fill):
        tw = d.textlength(text, font=fnt)
        d.text(((w - tw) / 2, y), text, font=fnt, fill=fill)

    centered("分享一个", f1, 306, TEXT)
    centered("超级好用的", f2, 410, BLUE)
    centered("DSH 插件", f3, 566, TEXT)

    # underline under the highlighted line
    uw = 560
    ux = (w - uw) / 2
    for i in range(60):
        t = i / 59
        color = (
            int(BLUE[0] + (CYAN[0] - BLUE[0]) * t),
            int(BLUE[1] + (CYAN[1] - BLUE[1]) * t),
            int(BLUE[2] + (CYAN[2] - BLUE[2]) * t),
        )
        d.rectangle([ux + i * (uw / 60), 690, ux + (i + 1) * (uw / 60), 694], fill=color)

    centered("DeepSeek Harness · 计划评审逐条批注", font(FONT_ZH, 26), 722, MUTED)

    # whale, large
    whale = Image.open(os.path.join(DOCS, "mark.png")).convert("RGBA")
    whale.thumbnail((520, 520), Image.LANCZOS)
    img.paste(whale, (int((w - whale.width) / 2), 800), whale)

    # bottom strip
    d.rounded_rectangle([64, 1272, w - 64, 1352], radius=12, outline=LINE, width=1)
    f_b = font(FONT_ZH_B, 28)
    d.text((92, 1296), "划到最后一张", font=f_b, fill=TEXT)
    d.text((92 + d.textlength("划到最后一张", font=f_b) + 14, 1300), "看安装方式 →", font=font(FONT_ZH, 24), fill=MUTED)
    d.text((w - 92 - d.textlength("dsh-plan-note", font=font(FONT_MONO, 22)), 1301), "dsh-plan-note", font=font(FONT_MONO, 22), fill=BLUE)

    path = os.path.join(out_dir, "00-cover.png")
    img.save(path, quality=95)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()

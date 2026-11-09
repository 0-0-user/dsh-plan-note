"""Render the README hero card: terminal frame, whale on the left, content right."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1440, 560
SS = 2

BG = (13, 17, 23)
BLUE = (77, 107, 254)
FRAME = (58, 74, 99)
FRAME_DARK = (32, 41, 56)
BAR = (21, 27, 38)
PANEL = (16, 21, 30)
GRID = (23, 30, 43)
TEXT = (232, 238, 248)
MUTED = (139, 155, 178)
CYAN = (86, 204, 242)
ORANGE = (255, 159, 67)
GREEN = (39, 201, 63)
YELLOW = (255, 189, 46)
RED = (255, 95, 86)

FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_B = r"C:\Windows\Fonts\consolab.ttf"
FONT_ZH = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_CARTOON = r"C:\Windows\Fonts\comicbd.ttf"
LOGO = r"D:\opt\tmp\ds-logo\logo.png"


def font(path, size):
    return ImageFont.truetype(path, size)


def pixel_text(text, fnt, color, scale=2):
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=fnt)
    tmp = Image.new("RGBA", (box[2] + 4, box[3] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((2 - box[0], 2 - box[1]), text, font=fnt, fill=color)
    return tmp.resize((tmp.width * scale, tmp.height * scale), Image.NEAREST)


def load_glyph(height):
    """Official whale mark, recoloured to brand blue, cutouts preserved."""
    src = Image.open(LOGO).convert("RGBA").crop((0, 0, 220, 165))
    px = src.load()
    mask = Image.new("L", src.size, 0)
    mp = mask.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a > 120 and not (r > 225 and g > 225 and b > 225):
                mp[x, y] = 255
    box = mask.getbbox()
    mask = mask.crop(box)
    scale = height / mask.height
    mask = mask.resize((max(1, int(mask.width * scale)), height), Image.LANCZOS)
    out = Image.new("RGBA", mask.size, BLUE + (255,))
    out.putalpha(mask)
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "docs", "hero.png")
    w, h = W * SS, H * SS

    def u(v):
        return int(v * SS)

    img = Image.new("RGBA", (w, h), BG + (255,))
    d = ImageDraw.Draw(img)

    # window
    d.rounded_rectangle([u(40), u(40), u(1400), u(520)], radius=u(12), fill=FRAME_DARK, outline=FRAME, width=u(2))
    d.rounded_rectangle([u(40), u(40), u(1400), u(98)], radius=u(12), fill=BAR)
    d.rectangle([u(40), u(84), u(1400), u(98)], fill=BAR)
    d.line([(u(40), u(98)), (u(1400), u(98))], fill=FRAME, width=u(1))

    for i, color in enumerate((RED, YELLOW, GREEN)):
        x = u(62 + i * 30)
        d.rectangle([x, u(58), x + u(16), u(74)], fill=color)

    d.text((u(152), u(55)), "DSH  //  PLAN-NOTE", font=font(FONT_MONO_B, u(20)), fill=MUTED)

    for i in range(52):
        x = u(760 + i * 7)
        d.line([(x, u(55)), (x, u(77))], fill=FRAME, width=u(2))
    d.rectangle([u(1360), u(58), u(1376), u(74)], fill=GREEN)

    # panel + grid
    px0, py0, px1, py1 = 66, 124, 1374, 494
    d.rounded_rectangle([u(px0), u(py0), u(px1), u(py1)], radius=u(8), fill=PANEL, outline=FRAME, width=u(1))
    for gx in range(px0 + 40, px1 - 20, 40):
        d.line([(u(gx), u(py0 + 2)), (u(gx), u(py1 - 2))], fill=GRID, width=1)
    for gy in range(py0 + 40, py1 - 20, 40):
        d.line([(u(px0 + 2), u(gy)), (u(px1 - 2), u(gy))], fill=GRID, width=1)
    d.rounded_rectangle([u(px0), u(py0), u(px1), u(py1)], radius=u(8), outline=FRAME, width=u(1))

    div_x = 560
    d.line([(u(div_x), u(py0 + 18)), (u(div_x), u(py1 - 18))], fill=FRAME, width=u(1))

    # ---- left: whale + stacked wordmark ----
    glyph = load_glyph(u(150))
    gx = u(px0 + (div_x - px0 - glyph.width / SS) / 2)
    img.alpha_composite(glyph, (gx, u(py0 + 28)))

    f_brand = font(FONT_CARTOON, u(44))
    for i, word in enumerate(("deepseek", "harness")):
        tw = d.textlength(word, font=f_brand)
        word_x = u((px0 + div_x) / 2) - tw / 2
        d.text((word_x, u(py0 + 196 + i * 56)), word, font=f_brand, fill=BLUE)

    # ---- right: content ----
    cx0 = div_x + 40
    d.rectangle([u(cx0), u(py0 + 26), u(cx0 + 14), u(py0 + 40)], fill=ORANGE)
    d.text((u(cx0 + 26), u(py0 + 23)), "PLAN ANNOTATOR   ·   DEEPSEEK HARNESS PLUGIN", font=font(FONT_MONO_B, u(15)), fill=MUTED)

    f_title = font(FONT_MONO_B, u(30))
    line1 = pixel_text("PLAN", f_title, TEXT + (255,), scale=2)
    line2 = pixel_text("NOTE", f_title, TEXT + (255,), scale=2)
    img.alpha_composite(line1, (u(cx0 - 2), u(py0 + 58)))
    img.alpha_composite(line2, (u(cx0 - 2), u(py0 + 58) + line1.height + u(2)))

    gy = py0 + 220
    seg = u(360) / 48
    for i in range(48):
        t = i / 47
        if t < 0.5:
            k = t * 2
            color = tuple(int(GREEN[j] + (YELLOW[j] - GREEN[j]) * k) for j in range(3))
        else:
            k = (t - 0.5) * 2
            color = tuple(int(YELLOW[j] + (ORANGE[j] - YELLOW[j]) * k) for j in range(3))
        d.rectangle([u(cx0) + int(i * seg), u(gy), u(cx0) + int((i + 1) * seg), u(gy + 4)], fill=color)

    d.text((u(cx0), u(gy + 14)), "选中计划原文，逐条批注", font=font(FONT_ZH, u(24)), fill=TEXT)
    d.text((u(cx0), u(gy + 50)), "Annotate the plan. Ship with intent.", font=font(FONT_MONO, u(14)), fill=MUTED)

    def badge(x, label):
        f = font(FONT_MONO_B, u(12))
        tw = d.textlength(label, font=f)
        d.rectangle([u(x), u(gy + 82), u(x) + int(tw) + u(22), u(gy + 106)], outline=FRAME, width=u(1))
        d.text((u(x) + u(11), u(gy + 86)), label, font=f, fill=MUTED)

    badge(cx0, "NODE.JS 22.19+")
    badge(cx0 + 156, "MIT")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, quality=95)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

"""Render the README hero card: a terminal-styled frame with a mechanical whale."""

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
GRID = (22, 29, 41)
TEXT = (232, 238, 248)
MUTED = (139, 155, 178)
CYAN = (86, 204, 242)
ORANGE = (255, 159, 67)
GREEN = (39, 201, 63)
YELLOW = (255, 189, 46)
RED = (255, 95, 86)
STEEL = (47, 74, 109)
STEEL_LIGHT = (74, 106, 146)
STEEL_DARK = (28, 44, 66)

FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_B = r"C:\Windows\Fonts\consolab.ttf"
FONT_ZH = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_ROUND = r"C:\Windows\Fonts\ARLRDBD.TTF"
LOGO = r"D:\opt\tmp\ds-logo\logo.png"


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


def load_lockup(height):
    """Official whale + wordmark, kept as the original artwork."""
    src = Image.open(LOGO).convert("RGBA")
    box = src.split()[3].getbbox()
    src = src.crop(box)
    scale = height / src.height
    return src.resize((max(1, int(src.width * scale)), height), Image.LANCZOS)


def font(path, size):
    return ImageFont.truetype(path, size)


def pixel_text(text, fnt, color, scale=2):
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=fnt)
    tmp = Image.new("RGBA", (box[2] + 4, box[3] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((2 - box[0], 2 - box[1]), text, font=fnt, fill=color)
    return tmp.resize((tmp.width * scale, tmp.height * scale), Image.NEAREST)


def draw_whale(size):
    w, h = size
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    bx, by = w * 0.54, h * 0.58
    brx, bry = w * 0.31, h * 0.21

    # tail flukes
    for sign in (-1, 1):
        d.polygon(
            [
                (bx - brx * 0.80, by - sign * h * 0.03),
                (w * 0.03, by + sign * h * 0.20),
                (w * 0.12, by + sign * h * 0.05),
                (bx - brx * 0.80, by + sign * h * 0.02),
            ],
            fill=STEEL,
            outline=STEEL_DARK,
        )

    # body
    d.ellipse([bx - brx, by - bry, bx + brx, by + bry], fill=STEEL, outline=STEEL_DARK, width=4)
    for k in range(1, 4):
        x = bx - brx + brx * 2 * k / 4
        d.line([(x, by - bry * 0.80), (x, by + bry * 0.80)], fill=STEEL_DARK, width=3)
    for k in range(5):
        x = bx - brx * 0.78 + brx * 1.56 * k / 4
        for yy in (by - bry * 0.66, by + bry * 0.60):
            d.ellipse([x - 3, yy - 3, x + 3, yy + 3], fill=STEEL_LIGHT)

    # belly plate
    d.ellipse([bx - brx * 0.74, by + bry * 0.20, bx + brx * 0.80, by + bry * 0.92], fill=STEEL_DARK)
    for k in range(4):
        x = bx - brx * 0.46 + brx * k / 3
        d.line([(x, by + bry * 0.26), (x, by + bry * 0.84)], fill=STEEL_LIGHT, width=2)

    # porthole eye
    ex, ey = bx + brx * 0.44, by - bry * 0.24
    r = h * 0.095
    d.ellipse([ex - r - 10, ey - r - 10, ex + r + 10, ey + r + 10], fill=STEEL_DARK)
    d.ellipse([ex - r - 5, ey - r - 5, ex + r + 5, ey + r + 5], outline=CYAN, width=4)
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(12, 20, 32))
    d.ellipse([ex - r * 0.58, ey - r * 0.58, ex + r * 0.58, ey + r * 0.58], fill=CYAN)
    d.ellipse([ex - r * 0.22, ey - r * 0.22, ex + r * 0.22, ey + r * 0.22], fill=(255, 255, 255))

    # jaw seam
    d.arc(
        [bx + brx * 0.08, by + bry * 0.02, bx + brx * 1.00, by + bry * 0.78],
        start=8,
        end=112,
        fill=STEEL_LIGHT,
        width=5,
    )

    # antenna
    ax, ay = bx + brx * 0.02, by - bry * 0.94
    d.line([(ax, ay), (ax, ay - h * 0.11)], fill=STEEL_LIGHT, width=5)
    d.ellipse([ax - 8, ay - h * 0.11 - 8, ax + 8, ay - h * 0.11 + 8], fill=RED)

    # gear
    gx, gy = bx - brx * 0.32, by + bry * 0.06
    gr = h * 0.085
    for i in range(10):
        a = i * math.pi / 5
        d.line(
            [(gx + math.cos(a) * gr, gy + math.sin(a) * gr), (gx + math.cos(a) * (gr + 8), gy + math.sin(a) * (gr + 8))],
            fill=STEEL_LIGHT,
            width=6,
        )
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=STEEL_DARK, outline=STEEL_LIGHT, width=4)
    d.ellipse([gx - gr * 0.34, gy - gr * 0.34, gx + gr * 0.34, gy + gr * 0.34], fill=CYAN)

    # bubbles
    for bx2, by2, rr in [(w * 0.70, h * 0.20, 6), (w * 0.77, h * 0.12, 4), (w * 0.66, h * 0.08, 3)]:
        d.ellipse([bx2 - rr, by2 - rr, bx2 + rr, by2 + rr], outline=CYAN, width=2)

    return im


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "docs", "hero.png")
    w, h = W * SS, H * SS

    def u(v):
        return int(v * SS)

    img = Image.new("RGBA", (w, h), BG + (255,))
    d = ImageDraw.Draw(img)

    # window frame
    d.rounded_rectangle([u(40), u(40), u(1400), u(520)], radius=u(12), fill=FRAME_DARK, outline=FRAME, width=u(2))

    # title bar
    d.rounded_rectangle([u(40), u(40), u(1400), u(98)], radius=u(12), fill=BAR)
    d.rectangle([u(40), u(84), u(1400), u(98)], fill=BAR)
    d.line([(u(40), u(98)), (u(1400), u(98))], fill=FRAME, width=u(1))

    for i, color in enumerate((RED, YELLOW, GREEN)):
        x = u(62 + i * 30)
        d.rectangle([x, u(58), x + u(16), u(74)], fill=color)

    # brand lockup in the title bar: official artwork + product suffix
    lock = load_lockup(u(26))
    img.alpha_composite(lock, (u(158), u(50)))
    f_brand = font(FONT_ROUND, u(20))
    d.text((u(158) + lock.width + u(6), u(75)), "harness", font=f_brand, fill=BLUE, anchor="ls")

    for i in range(52):
        x = u(760 + i * 7)
        d.line([(x, u(55)), (x, u(77))], fill=FRAME, width=u(2))
    d.rectangle([u(1360), u(58), u(1376), u(74)], fill=GREEN)

    # inner panel
    px0, py0, px1, py1 = 66, 124, 1374, 494
    d.rounded_rectangle([u(px0), u(py0), u(px1), u(py1)], radius=u(8), fill=PANEL, outline=FRAME, width=u(1))

    # faint grid inside the panel
    for gx in range(px0 + 40, px1 - 20, 40):
        d.line([(u(gx), u(py0 + 2)), (u(gx), u(py1 - 2))], fill=GRID, width=1)
    for gy in range(py0 + 40, py1 - 20, 40):
        d.line([(u(px0 + 2), u(gy)), (u(px1 - 2), u(gy))], fill=GRID, width=1)
    d.rounded_rectangle([u(px0), u(py0), u(px1), u(py1)], radius=u(8), outline=FRAME, width=u(1))

    div_x = 850
    d.line([(u(div_x), u(py0 + 18)), (u(div_x), u(py1 - 18))], fill=FRAME, width=u(1))

    # tag
    d.rectangle([u(106), u(150), u(120), u(164)], fill=ORANGE)
    d.text((u(132), u(147)), "PLAN ANNOTATOR   ·   DEEPSEEK HARNESS PLUGIN", font=font(FONT_MONO_B, u(15)), fill=MUTED)

    # pixel title
    f_title = font(FONT_MONO_B, u(30))
    line1 = pixel_text("PLAN", f_title, TEXT + (255,), scale=2)
    line2 = pixel_text("NOTE", f_title, TEXT + (255,), scale=2)
    img.alpha_composite(line1, (u(104), u(182)))
    img.alpha_composite(line2, (u(104), u(182) + line1.height + u(2)))

    # gradient rule
    gy = 344
    seg = (u(470) - u(106)) / 48
    for i in range(48):
        t = i / 47
        if t < 0.5:
            k = t * 2
            color = tuple(int(GREEN[j] + (YELLOW[j] - GREEN[j]) * k) for j in range(3))
        else:
            k = (t - 0.5) * 2
            color = tuple(int(YELLOW[j] + (ORANGE[j] - YELLOW[j]) * k) for j in range(3))
        d.rectangle([u(106) + int(i * seg), u(gy), u(106) + int((i + 1) * seg), u(gy + 4)], fill=color)

    # subtitle
    d.text((u(106), u(358)), "选中计划原文，逐条批注", font=font(FONT_ZH, u(24)), fill=TEXT)
    d.text((u(106), u(392)), "Annotate the plan. Ship with intent.", font=font(FONT_MONO, u(14)), fill=MUTED)

    # badges
    def badge(x, label):
        f = font(FONT_MONO_B, u(12))
        tw = d.textlength(label, font=f)
        d.rectangle([u(x), u(424), u(x) + int(tw) + u(22), u(448)], outline=FRAME, width=u(1))
        d.text((u(x) + u(11), u(428)), label, font=f, fill=MUTED)

    badge(106, "NODE.JS 22.19+")
    badge(262, "MIT")

    # art: the same official mark, large
    big = load_glyph(u(250))
    img.alpha_composite(big, (u(div_x + (px1 - div_x - big.width / SS) / 2), u(py0 + (py1 - py0 - big.height / SS) / 2)))

    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, quality=95)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

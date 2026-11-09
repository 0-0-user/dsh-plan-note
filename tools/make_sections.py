"""Render section header banners for the README.

A different language from the hero: a blue index number, a bright title, a thin
circuit of dots trailing to the right edge. No tag block, no tick strip.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1440, 56
SS = 2

BG = (16, 21, 32)
EDGE = (27, 37, 54)
BLUE = (77, 107, 254)
CYAN = (86, 204, 242)
TITLE = (236, 240, 247)
DOT = (34, 56, 88)

FONT_MONO_B = r"C:\Windows\Fonts\consolab.ttf"
FONT_ZH = r"C:\Windows\Fonts\msyhbd.ttc"

SECTIONS = [
    ("01", "intro", "简介", "Intro"),
    ("02", "demo", "演示示例", "Demo"),
    ("03", "index", "目录", "Contents"),
    ("04", "features", "主要能力", "Main features"),
    ("05", "use-cases", "适用场景", "Where it helps"),
    ("06", "quick-start", "快速开始", "Quick start"),
    ("07", "usage", "使用", "Usage"),
    ("08", "limits", "兼容与限制", "Compatibility and limits"),
    ("09", "dev", "开发", "Development"),
    ("10", "thanks", "致谢", "Acknowledgements"),
    ("11", "feedback", "反馈", "Feedback"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def render(number, title, zh):
    w, h = W * SS, H * SS
    img = Image.new("RGBA", (w, h), BG + (255,))
    d = ImageDraw.Draw(img)

    # left accent: vertical blue -> cyan bar
    for y in range(h):
        k = y / max(1, h - 1)
        color = (
            int(BLUE[0] + (CYAN[0] - BLUE[0]) * k),
            int(BLUE[1] + (CYAN[1] - BLUE[1]) * k),
            int(BLUE[2] + (CYAN[2] - BLUE[2]) * k),
        )
        d.line([(0, y), (5 * SS, y)], fill=color)

    # index number
    f_num = font(FONT_MONO_B, 18 * SS)
    d.text((28 * SS, (h - 20 * SS) / 2 - 2), number, font=f_num, fill=BLUE)

    # title
    f_title = font(FONT_ZH, 24 * SS) if zh else font(FONT_MONO_B, 22 * SS)
    tx = 78 * SS
    d.text((tx, (h - (28 if zh else 26) * SS) / 2), title, font=f_title, fill=TITLE)

    # circuit dots
    title_w = d.textlength(title, font=f_title)
    x = int(tx + title_w + 34 * SS)
    end = w - 30 * SS
    while x < end:
        d.ellipse([x, h / 2 - 2 * SS, x + 4 * SS, h / 2 + 2 * SS], fill=DOT)
        x += 22 * SS

    # hairlines
    d.line([(0, h - 1), (w, h - 1)], fill=EDGE, width=1)
    d.line([(0, 0), (w, 0)], fill=EDGE, width=1)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(here, "..", "docs", "sections")
    for number, slug, title_zh, title_en in SECTIONS:
        for lang, title, zh in (("zh", title_zh, True), ("en", title_en, False)):
            out_dir = os.path.join(root, lang)
            os.makedirs(out_dir, exist_ok=True)
            img = render(number, title, zh)
            path = os.path.join(out_dir, f"{number}-{slug}.png")
            img.convert("RGB").save(path, optimize=True)
            print("wrote", path, os.path.getsize(path))

    render("03", "主要能力", True).convert("RGB").save(
        os.path.join(here, "..", "docs", "_section_preview.png")
    )


if __name__ == "__main__":
    main()

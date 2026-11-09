"""Render section header banners for the README.

Each banner is a dark bar with a khaki tag block, a title, a tick strip and a
green marker - the same box language as the hero card.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1440, 64
SS = 2

BG = (20, 24, 31)
BORDER = (74, 74, 58)
TAG = (143, 138, 111)
TAG_TEXT = (27, 27, 20)
TITLE = (236, 240, 247)
TICK = (90, 90, 70)
GREEN = (39, 201, 63)

FONT_MONO_B = r"C:\Windows\Fonts\consolab.ttf"
FONT_ZH = r"C:\Windows\Fonts\msyhbd.ttc"

SECTIONS = [
    ("01", "intro", "INTRO", "简介", "Intro"),
    ("02", "index", "INDEX", "目录", "Contents"),
    ("03", "features", "FEATURES", "主要能力", "Main features"),
    ("04", "use-cases", "USE CASES", "适用场景", "Where it helps"),
    ("05", "quick-start", "GET", "快速开始", "Quick start"),
    ("06", "usage", "USAGE", "使用", "Usage"),
    ("07", "limits", "LIMITS", "兼容与限制", "Compatibility and limits"),
    ("08", "dev", "DEV", "开发", "Development"),
    ("09", "thanks", "THANKS", "致谢", "Acknowledgements"),
    ("10", "feedback", "CONTACT", "反馈", "Feedback"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def render(tag, title, zh):
    w, h = W * SS, H * SS
    img = Image.new("RGBA", (w, h), BG + (255,))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, w - 1, h - 1], outline=BORDER, width=SS)

    tag_w = 150 * SS
    d.rectangle([SS, SS, tag_w, h - SS], fill=TAG + (255,))
    f_tag = font(FONT_MONO_B, 20 * SS)
    tw = d.textlength(tag, font=f_tag)
    d.text(((tag_w - tw) / 2, (h - 24 * SS) / 2), tag, font=f_tag, fill=TAG_TEXT)

    f_title = font(FONT_ZH, 26 * SS) if zh else font(FONT_MONO_B, 24 * SS)
    tx = tag_w + 22 * SS
    d.text((tx, (h - (30 if zh else 28) * SS) / 2), title, font=f_title, fill=TITLE)

    title_w = d.textlength(title, font=f_title)
    tick_x = int(tx + title_w + 26 * SS)
    tick_end = w - 60 * SS
    x = tick_x
    while x < tick_end:
        d.line([(x, 20 * SS), (x, 44 * SS)], fill=TICK, width=SS)
        x += 7 * SS

    d.rectangle([w - 44 * SS, 24 * SS, w - 28 * SS, 40 * SS], fill=GREEN)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(here, "..", "docs", "sections")
    for number, slug, tag, title_zh, title_en in SECTIONS:
        for lang, title, zh in (("zh", title_zh, True), ("en", title_en, False)):
            out_dir = os.path.join(root, lang)
            os.makedirs(out_dir, exist_ok=True)
            img = render(tag, title, zh)
            path = os.path.join(out_dir, f"{number}-{slug}.png")
            img.convert("RGB").save(path, optimize=True)
            print("wrote", path, os.path.getsize(path))

    preview = render("FEATURES", "主要能力", True)
    preview.convert("RGB").save(os.path.join(here, "..", "docs", "_section_preview.png"))


if __name__ == "__main__":
    main()

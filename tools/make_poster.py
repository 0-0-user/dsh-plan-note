"""Render a vertical Xiaohongshu poster for dsh-plan-note (1080x1440)."""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440

BG = (13, 17, 23)
PANEL = (18, 23, 33)
CARD = (23, 29, 41)
LINE = (42, 54, 72)
TEXT = (235, 239, 247)
MUTED = (141, 157, 180)
BLUE = (77, 107, 254)
CYAN = (86, 204, 242)
ORANGE = (255, 159, 67)
RED = (214, 69, 69)
BAR = (44, 56, 74)

FONT_ZH_B = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_ZH = r"C:\Windows\Fonts\msyh.ttc"
FONT_MONO = r"C:\Windows\Fonts\consolab.ttf"

ROOT = r"D:\Users\xu\Documents\dsh-plan-note"


def font(path, size):
    return ImageFont.truetype(path, size)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), "Desktop", "dsh-plan-note-poster")
    os.makedirs(out_dir, exist_ok=True)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(17, 22, 31))
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(17, 22, 31))
    d.rectangle([28, 28, W - 29, H - 29], outline=LINE, width=2)

    # brand
    mark = Image.open(os.path.join(ROOT, "docs", "mark.png")).convert("RGBA")
    mark.thumbnail((92, 92), Image.LANCZOS)
    img.paste(mark, (72, 66), mark)
    brand = Image.open(os.path.join(ROOT, "docs", "brand.png")).convert("RGBA")
    brand.thumbnail((320, 126), Image.LANCZOS)
    img.paste(brand, (72 + mark.width + 18, 74), brand)

    # headline
    f_h = font(FONT_ZH_B, 92)
    d.text((72, 206), "计划评审", font=f_h, fill=TEXT)
    d.text((72, 312), "逐条批注", font=f_h, fill=BLUE)

    d.text((74, 432), "Inline annotations for DeepSeek Harness", font=font(FONT_MONO, 25), fill=MUTED)

    for i in range(60):
        t = i / 59
        color = (
            int(BLUE[0] + (CYAN[0] - BLUE[0]) * t),
            int(BLUE[1] + (CYAN[1] - BLUE[1]) * t),
            int(BLUE[2] + (CYAN[2] - BLUE[2]) * t),
        )
        d.rectangle([72 + i * 6, 480, 72 + (i + 1) * 6, 484], fill=color)

    # points
    points = [
        ("01", "选中原文", "批注钉在句子上，不跑偏"),
        ("02", "多条共存", "想写几条写几条，一次发送"),
        ("03", "按批注改稿", "agent 留在计划模式，改完再看"),
    ]
    f_num = font(FONT_MONO, 25)
    f_t = font(FONT_ZH_B, 34)
    f_d = font(FONT_ZH, 24)

    y = 516
    for num, title, desc in points:
        d.rectangle([72, y + 8, 76, y + 44], fill=ORANGE)
        d.text((96, y), num, font=f_num, fill=BLUE)
        d.text((152, y - 6), title, font=f_t, fill=TEXT)
        d.text((152, y + 42), desc, font=f_d, fill=MUTED)
        y += 104

    # product mock
    px, py, pw, ph = 72, 836, 936, 366
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=10, fill=CARD, outline=LINE, width=2)

    # mock header
    d.text((px + 26, py + 20), "计划批注", font=font(FONT_ZH_B, 22), fill=TEXT)
    d.text((px + 132, py + 24), "2 条", font=font(FONT_ZH, 18), fill=MUTED)
    for i in range(3):
        bx = px + pw - 40 - i * 22
        d.rectangle([bx, py + 22, bx + 14, py + 36], outline=LINE, width=1)

    # mock plan lines
    line_y = py + 72
    widths = [0.88, 0.72, 0.54]
    for i, ratio in enumerate(widths):
        d.rounded_rectangle([px + 26, line_y, px + 26 + int((pw - 52) * ratio), line_y + 11], radius=5, fill=BAR)
        line_y += 34

    # highlighted line with red underline
    hx0, hy = px + 26, py + 72 + 34 * 1 + 18
    hx1 = hx0 + int((pw - 52) * 0.46)
    d.rounded_rectangle([hx0, hy, hx1, hy + 11], radius=5, fill=(88, 112, 158))
    d.line([(hx0, hy + 15), (hx1, hy + 15)], fill=RED, width=3)

    # comment cards
    cy = py + 190
    f_q = font(FONT_ZH, 19)
    f_n = font(FONT_ZH, 20)
    notes = [
        ("「空内容时禁用」", "改成始终可点，空内容导出空模板"),
        ("「plan-note-<时间戳>.md」", "文件名加项目前缀，好找"),
    ]
    for quote, note in notes:
        d.rounded_rectangle([px + 26, cy, px + pw - 26, cy + 70], radius=8, fill=PANEL, outline=LINE, width=1)
        d.line([(px + 34, cy + 14), (px + 34, cy + 56)], fill=LINE, width=2)
        d.text((px + 46, cy + 10), quote, font=f_q, fill=MUTED)
        d.text((px + 46, cy + 38), note, font=f_n, fill=TEXT)
        cy += 82

    # footer
    fy = 1248
    d.rounded_rectangle([72, fy, W - 72, fy + 58], radius=8, fill=PANEL, outline=LINE, width=1)
    d.text((96, fy + 15), "dsh plugin --profile web add dsh-plan-note", font=font(FONT_MONO, 22), fill=TEXT)

    f_small = font(FONT_MONO, 20)
    d.text((74, fy + 72), "github.com/0-0-user/dsh-plan-note", font=f_small, fill=MUTED)
    right = "npm: dsh-plan-note"
    d.text((W - 74 - d.textlength(right, font=f_small), fy + 72), right, font=f_small, fill=MUTED)

    path = os.path.join(out_dir, "01-poster.png")
    img.save(path, quality=95)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()

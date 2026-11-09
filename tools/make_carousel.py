"""Render the Xiaohongshu carousel for dsh-plan-note.

Produces:
  02-intro.png        vertical 1080x1440   bullet intro
  03..06-demo*.png    horizontal 1440x1080 screenshots with captions
  07-summary.png      vertical 1080x1440   install + links + thanks, whale backdrop
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = r"D:\Users\xu\Documents\dsh-plan-note"
DOCS = os.path.join(ROOT, "docs")

BG = (13, 17, 23)
PANEL = (18, 23, 33)
CARD = (23, 29, 41)
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


def base(w, h, with_frame=True):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, w, 40):
        d.line([(x, 0), (x, h)], fill=(17, 22, 31))
    for y in range(0, h, 40):
        d.line([(0, y), (w, y)], fill=(17, 22, 31))
    if with_frame:
        d.rectangle([24, 24, w - 25, h - 25], outline=LINE, width=2)
    return img, d


def brand(img, x, y, scale=1.0):
    mark = Image.open(os.path.join(DOCS, "mark.png")).convert("RGBA")
    mark.thumbnail((int(84 * scale), int(84 * scale)), Image.LANCZOS)
    img.paste(mark, (x, y), mark)
    word = Image.open(os.path.join(DOCS, "brand.png")).convert("RGBA")
    word.thumbnail((int(300 * scale), int(118 * scale)), Image.LANCZOS)
    img.paste(word, (x + mark.width + 16, y + int(8 * scale)), word)


def footer(img, d, w, y, right_text):
    f = font(FONT_MONO, 20)
    d.text((64, y), "github.com/0-0-user/dsh-plan-note", font=f, fill=MUTED)
    d.text((w - 64 - d.textlength(right_text, font=f), y), right_text, font=f, fill=MUTED)


def intro(out_dir):
    w, h = 1080, 1440
    img, d = base(w, h)
    brand(img, 64, 58)

    d.text((64, 200), "能做什么", font=font(FONT_ZH_B, 76), fill=TEXT)
    d.text((66, 306), "What it does", font=font(FONT_MONO, 24), fill=MUTED)

    for i in range(54):
        t = i / 53
        color = (
            int(BLUE[0] + (CYAN[0] - BLUE[0]) * t),
            int(BLUE[1] + (CYAN[1] - BLUE[1]) * t),
            int(BLUE[2] + (CYAN[2] - BLUE[2]) * t),
        )
        d.rectangle([64 + i * 6, 352, 64 + (i + 1) * 6, 356], fill=color)

    items = [
        ("01", "选中原文", "计划里的任意一段都能拖选"),
        ("02", "就地批注", "意见钉在那句话上，不跑偏"),
        ("03", "多条共存", "想写几条写几条，互不干扰"),
        ("04", "一次发送", "汇总成结构化反馈回传"),
        ("05", "仍可批准", "没问题就一键同意执行"),
    ]
    f_num = font(FONT_MONO, 24)
    f_t = font(FONT_ZH_B, 34)
    f_d = font(FONT_ZH, 24)

    y = 410
    for num, title, desc in items:
        d.rectangle([64, y + 8, 68, y + 44], fill=ORANGE)
        d.text((88, y), num, font=f_num, fill=BLUE)
        d.text((144, y - 6), title, font=f_t, fill=TEXT)
        d.text((144, y + 42), desc, font=f_d, fill=MUTED)
        y += 136

    d.rounded_rectangle([64, 1120, w - 64, 1216], radius=10, fill=PANEL, outline=LINE, width=1)
    d.text((92, 1146), "计划评审不再是「同意 / 拒绝」二选一", font=font(FONT_ZH_B, 26), fill=TEXT)
    d.text((92, 1184), "Plan review, one comment at a time.", font=font(FONT_MONO, 20), fill=MUTED)

    footer(img, d, w, 1280, "npm: dsh-plan-note")

    path = os.path.join(out_dir, "02-intro.png")
    img.save(path, quality=95)
    print("wrote", path)


def demo(out_dir, index, shot, number, title, caption):
    w, h = 1440, 1080
    img, d = base(w, h)

    d.rectangle([64, 62, 68, 74], fill=ORANGE)
    d.text((84, 52), number, font=font(FONT_MONO, 26), fill=BLUE)
    d.text((140, 40), title, font=font(FONT_ZH_B, 42), fill=TEXT)
    d.text((142, 96), caption, font=font(FONT_ZH, 24), fill=MUTED)

    src = Image.open(os.path.join(DOCS, shot)).convert("RGB")
    target_w = 1256
    target_h = int(src.height * target_w / src.width)
    src = src.resize((target_w, target_h), Image.LANCZOS)
    x = (w - target_w) // 2
    y = 156
    d.rectangle([x - 2, y - 2, x + target_w + 1, y + target_h + 1], outline=LINE, width=2)
    img.paste(src, (x, y))

    footer(img, d, w, y + target_h + 22, "dsh-plan-note")

    path = os.path.join(out_dir, f"{index}-{shot.replace('demo-', 'demo-').replace('.png', '')}.png")
    img.save(path, quality=95)
    print("wrote", path)


def summary(out_dir):
    w, h = 1080, 1440
    img, d = base(w, h)

    # whale backdrop, bottom-right and quiet
    whale = Image.open(os.path.join(DOCS, "mark.png")).convert("RGBA")
    whale.thumbnail((620, 460), Image.LANCZOS)
    tint = Image.new("RGBA", whale.size, (77, 107, 254, 0))
    alpha = whale.split()[3].point(lambda v: int(v * 0.09))
    tint.putalpha(alpha)
    img.paste(tint, (w - whale.width - 30, 1040), tint)

    brand(img, 64, 56, 0.9)

    d.text((64, 200), "开始使用", font=font(FONT_ZH_B, 80), fill=TEXT)
    d.text((66, 304), "Get started", font=font(FONT_MONO, 24), fill=MUTED)

    for i in range(54):
        t = i / 53
        color = (
            int(BLUE[0] + (CYAN[0] - BLUE[0]) * t),
            int(BLUE[1] + (CYAN[1] - BLUE[1]) * t),
            int(BLUE[2] + (CYAN[2] - BLUE[2]) * t),
        )
        d.rectangle([64 + i * 6, 348, 64 + (i + 1) * 6, 352], fill=color)

    # install box
    d.rounded_rectangle([64, 392, w - 64, 566], radius=12, fill=PANEL, outline=LINE, width=1)
    d.text((92, 412), "npm（推荐）", font=font(FONT_ZH_B, 24), fill=MUTED)
    d.text((92, 448), "dsh plugin --profile web add dsh-plan-note", font=font(FONT_MONO, 22), fill=TEXT)
    d.text((92, 490), "Release 附件", font=font(FONT_ZH_B, 24), fill=MUTED)
    d.text((92, 524), "releases/latest/download/dsh-plan-note.tgz", font=font(FONT_MONO, 20), fill=TEXT)

    # links
    d.text((64, 604), "github.com/0-0-user/dsh-plan-note", font=font(FONT_MONO, 22), fill=TEXT)
    d.text((64, 640), "npmjs.com/package/dsh-plan-note", font=font(FONT_MONO, 22), fill=TEXT)

    # thanks
    d.text((64, 760), "致谢", font=font(FONT_ZH_B, 34), fill=TEXT)
    thanks = [
        "Claude Code — Add comment 交互的灵感来源",
        "DeepSeek Harness — 插件平台与 slot API",
        "鲸鱼标属于 DeepSeek，本作为粉丝作品",
    ]
    yy = 816
    for line in thanks:
        d.rectangle([64, yy + 10, 68, yy + 30], fill=ORANGE)
        d.text((82, yy), line, font=font(FONT_ZH, 22), fill=MUTED)
        yy += 48

    # contact
    d.text((64, 990), "反馈与演示", font=font(FONT_ZH_B, 34), fill=TEXT)
    d.text((64, 1046), "小红书 1551112051   ·   Bilibili 1615793632", font=font(FONT_ZH, 24), fill=MUTED)
    d.text((64, 1090), "欢迎各路大神提供意见建议", font=font(FONT_ZH, 24), fill=MUTED)

    # closing line
    d.rounded_rectangle([64, 1180, w - 64, 1296], radius=12, fill=CARD, outline=LINE, width=1)
    d.text((92, 1204), "计划评审，逐条批注", font=font(FONT_ZH_B, 34), fill=TEXT)
    d.text((92, 1252), "Annotate the plan. Ship with intent.", font=font(FONT_MONO, 22), fill=MUTED)

    footer(img, d, w, 1338, "MIT")

    path = os.path.join(out_dir, "07-summary.png")
    img.save(path, quality=95)
    print("wrote", path)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"), "Desktop", "dsh-plan-note-poster")
    os.makedirs(out_dir, exist_ok=True)

    intro(out_dir)
    demo(out_dir, "03", "demo-1-overview.png", "01", "打开计划评审", "计划直接出现在右侧栏，不挡对话")
    demo(out_dir, "04", "demo-2-select.png", "02", "选中要讨论的文字", "拖选一段，批注框就地弹出")
    demo(out_dir, "05", "demo-3-comment.png", "03", "添加局部批注", "意见钉在原文上，同意/关闭临时变灰")
    demo(out_dir, "06", "demo-4-overall.png", "04", "多条批注与整体意见", "一次发送，agent 按批注改稿")
    summary(out_dir)


if __name__ == "__main__":
    main()

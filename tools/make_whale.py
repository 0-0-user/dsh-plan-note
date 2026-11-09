"""Render an animated DeepSeek-blue whale banner for the README."""

import math
import os

from PIL import Image, ImageDraw

W, H = 880, 240
SS = 3
FRAMES = 36
DURATION = 90

BLUE = (77, 107, 254)
DEEP = (43, 70, 210)
WHITE = (255, 255, 255)
INK = (11, 18, 32)
BUBBLE = (127, 160, 255)
PALETTE = [BLUE, DEEP, WHITE, INK, BUBBLE]


def draw_frame(t):
    w, h = W * SS, H * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    phase = t * 2 * math.pi
    bob = 7 * math.sin(phase * 2)
    cx = (W / 2 + 16 * math.sin(phase)) * SS
    cy = (H / 2 + 10 + bob) * SS

    rx, ry = 168 * SS, 64 * SS

    # tail: a solid wedge overlapping the body so there is no gap
    wag = 0.22 * math.sin(phase * 2 + 0.7)
    base_x = cx - rx * 0.72
    tip_x = base_x - 96 * SS
    up = (tip_x, cy - (58 + 26 * wag) * SS)
    down = (tip_x, cy + (58 - 26 * wag) * SS)
    d.polygon(
        [
            (base_x, cy - 24 * SS),
            up,
            (tip_x + 34 * SS, cy - 8 * SS),
            (tip_x + 34 * SS, cy + 8 * SS),
            down,
            (base_x, cy + 24 * SS),
        ],
        fill=BLUE,
    )

    # body
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=BLUE)

    # pectoral fin
    d.polygon(
        [
            (cx - 26 * SS, cy + ry * 0.42),
            (cx + 16 * SS, cy + ry * 0.92),
            (cx - 14 * SS, cy + ry * 1.18),
            (cx - 44 * SS, cy + ry * 0.78),
        ],
        fill=DEEP,
    )

    # eye: white sclera + dark pupil + glint
    ex, ey = cx + rx * 0.56, cy - ry * 0.16
    d.ellipse([ex - 13 * SS, ey - 13 * SS, ex + 13 * SS, ey + 13 * SS], fill=WHITE)
    d.ellipse([ex - 6 * SS, ey - 6 * SS, ex + 6 * SS, ey + 6 * SS], fill=INK)
    d.ellipse([ex + 1 * SS, ey - 5 * SS, ex + 5 * SS, ey - 1 * SS], fill=WHITE)

    # smile
    d.arc(
        [cx + rx * 0.60, cy + ry * 0.02, cx + rx * 0.94, cy + ry * 0.58],
        start=15,
        end=95,
        fill=INK,
        width=int(3 * SS),
    )

    # blowhole spray
    sx, sy = cx + rx * 0.18, cy - ry * 0.88
    d.arc(
        [sx - 20 * SS, sy - 34 * SS, sx + 20 * SS, sy + 6 * SS],
        start=205,
        end=335,
        fill=DEEP,
        width=int(4 * SS),
    )
    for i in range(7):
        bp = (phase + i * 0.42) % 1.0
        bx2 = sx + math.sin(bp * 3.0 + i * 1.1) * 30 * SS
        by2 = sy - 14 * SS - bp * 82 * SS
        r = (2.2 + bp * 5.4) * SS
        d.ellipse([bx2 - r, by2 - r, bx2 + r, by2 + r], fill=BUBBLE)

    return img.resize((W, H), Image.LANCZOS)


def to_palette(img):
    px = img.load()
    out = Image.new("P", img.size, 0)
    pal = []
    for c in PALETTE:
        pal.extend(c)
    pal.extend([0, 0, 0] * (256 - len(PALETTE)))
    out.putpalette(pal)
    op = out.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a < 90:
                op[x, y] = 0
                continue
            best, bestd = 1, None
            for i, c in enumerate(PALETTE, start=1):
                dd = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2
                if bestd is None or dd < bestd:
                    best, bestd = i, dd
            op[x, y] = best
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "..", "docs")
    os.makedirs(out_dir, exist_ok=True)

    frames = [to_palette(draw_frame(i / FRAMES)) for i in range(FRAMES)]
    gif_path = os.path.join(out_dir, "whale.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION,
        loop=0,
        disposal=2,
        transparency=0,
        optimize=False,
    )
    print("wrote", gif_path, os.path.getsize(gif_path), "bytes")

    draw_frame(0.25).convert("RGB").save(os.path.join(out_dir, "_whale_preview.png"))


if __name__ == "__main__":
    main()

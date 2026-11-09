"""Render a cartoon whale banner for the README.

The design follows the DeepSeek whale: the same blue, the same two-lobed tail
and a light belly patch. Motion, face and bubbles are added on top.
"""

import math
import os

from PIL import Image, ImageChops, ImageDraw, ImageFilter

W, H = 880, 260
SS = 3
FRAMES = 40
DURATION = 85

BLUE = (77, 107, 254)
DEEP = (36, 58, 176)
BELLY = (196, 208, 255)
WHITE = (255, 255, 255)
INK = (16, 22, 40)
BLUSH = (255, 150, 170)
BUBBLE = (150, 180, 255)
PALETTE = [BLUE, DEEP, BELLY, WHITE, INK, BLUSH, BUBBLE]


def build_whale(size, blink):
    w, h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    bx, by = w * 0.60, h * 0.56
    brx, bry = w * 0.33, h * 0.25

    # tail: two rounded flukes, swept up-left
    for sign, angle in ((-1, -0.38), (1, 0.26)):
        fw, fh = w * 0.17, h * 0.105
        cx, cy = bx - brx * 0.92, by + sign * h * 0.085
        fluke = Image.new("RGBA", (int(fw * 2), int(fh * 2)), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fluke)
        fd.ellipse([0, 0, fw * 2 - 1, fh * 2 - 1], fill=BLUE + (255,))
        fluke = fluke.rotate(math.degrees(angle), expand=True, resample=Image.BICUBIC)
        layer.alpha_composite(fluke, (int(cx - fluke.width / 2), int(cy - fluke.height / 2)))

    # body
    d.ellipse([bx - brx, by - bry, bx + brx, by + bry], fill=BLUE + (255,))
    # snout
    d.ellipse(
        [bx + brx * 0.45, by - bry * 0.72, bx + brx * 1.12, by + bry * 0.62],
        fill=BLUE + (255,),
    )

    # belly patch, clipped to the body
    body_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(body_mask).ellipse([bx - brx, by - bry, bx + brx, by + bry], fill=255)
    belly = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(belly).ellipse(
        [bx - brx * 0.86, by + bry * 0.18, bx + brx * 0.90, by + bry * 0.98],
        fill=BELLY + (255,),
    )
    belly.putalpha(ImageChops.multiply(belly.split()[3], body_mask))
    layer = Image.alpha_composite(layer, belly)
    d = ImageDraw.Draw(layer)

    # pectoral fin, protruding from the lower body edge
    d.polygon(
        [
            (bx - brx * 0.10, by + bry * 0.72),
            (bx + brx * 0.22, by + bry * 1.28),
            (bx - brx * 0.16, by + bry * 1.06),
        ],
        fill=DEEP + (255,),
    )

    # outline from the composed alpha
    alpha = layer.split()[3]
    grown = alpha.filter(ImageFilter.MaxFilter(11))
    ring = Image.composite(Image.new("L", (w, h), 255), Image.new("L", (w, h), 0), grown)
    ring = Image.composite(Image.new("L", (w, h), 0), ring, alpha)
    outline = Image.new("RGBA", (w, h), DEEP + (255,))
    outline.putalpha(ring)
    layer = Image.alpha_composite(outline, layer)
    d = ImageDraw.Draw(layer)

    # eye
    ex, ey = bx + brx * 0.30, by - bry * 0.18
    er = h * 0.095
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=WHITE + (255,))
    if blink:
        d.arc([ex - er, ey - er * 0.4, ex + er, ey + er * 0.7], start=20, end=160, fill=INK + (255,), width=max(2, SS * 3))
    else:
        pr = er * 0.52
        px, py = ex + er * 0.12, ey
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=INK + (255,))
        gr = er * 0.18
        d.ellipse([px - gr + pr * 0.25, py - gr - pr * 0.35, px + gr + pr * 0.25, py + gr - pr * 0.35], fill=WHITE + (255,))

    # smile
    d.arc(
        [ex - er * 0.55, ey + er * 0.72, ex + er * 1.5, ey + er * 2.05],
        start=18,
        end=128,
        fill=INK + (255,),
        width=max(2, SS * 2),
    )

    # blush
    d.ellipse(
        [ex - er * 1.75, ey + er * 0.45, ex - er * 1.05, ey + er * 1.05],
        fill=BLUSH + (255,),
    )

    return layer


def draw_frame(t, whale):
    w, h = W * SS, H * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    index = int(t * FRAMES) % FRAMES
    blink = index in (14, 15)
    layer = build_whale(whale.size, blink) if blink else whale

    phase = t * 2 * math.pi
    bob = 8 * math.sin(phase * 2)
    tilt = 2.2 * math.sin(phase * 2 + 0.5)
    rotated = layer.rotate(tilt, resample=Image.BICUBIC, expand=True)

    cx = int(w / 2 - rotated.width / 2 + 12 * math.sin(phase) * SS)
    cy = int(h / 2 - rotated.height / 2 + (4 + bob) * SS)
    img.alpha_composite(rotated, (cx, cy))

    d = ImageDraw.Draw(img)
    sx, sy = cx + rotated.width * 0.76, cy + rotated.height * 0.10
    for i in range(7):
        bp = (phase + i * 0.33) % 1.0
        bx = sx + math.sin(bp * 3.1 + i * 1.3) * 26 * SS
        by = sy - bp * 92 * SS
        r = (2.0 + bp * 4.6) * SS
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=BUBBLE + (255,))

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

    size = (int(880 * SS * 0.55), int(260 * SS * 0.62))
    whale = build_whale(size, False)
    frames = [to_palette(draw_frame(i / FRAMES, whale)) for i in range(FRAMES)]

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

    draw_frame(0.3, whale).convert("RGB").save(os.path.join(out_dir, "_whale_preview.png"))


if __name__ == "__main__":
    main()

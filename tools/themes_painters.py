"""Wallpapers drawn here for the themes that have no photograph: pixel art, manga screentone, festival
lamps and lanterns, a crescent night, powder colours and a golden lattice. Every picture is drawn from
shapes and colours, so there is nothing to licence and nothing to credit."""
import math

from PIL import Image, ImageDraw, ImageFilter


def register(g):
    W, H = g["WALL_W"], g["WALL_H"]
    hex_rgb = g["hex_rgb"]
    sky = g["sky"]

    def layer():
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def glow(img, draw_fn, blur):
        top = layer()
        draw_fn(ImageDraw.Draw(top))
        return Image.alpha_composite(img, top.filter(ImageFilter.GaussianBlur(blur)))

    def sharp(img, draw_fn):
        top = layer()
        draw_fn(ImageDraw.Draw(top))
        return Image.alpha_composite(img, top)

    # PIXEL ART: a moonlit mountain range in blocks, drawn small and scaled up without smoothing.
    def paint_pixels(entry, rnd):
        scale = 8
        w, h = W // scale, H // scale
        img = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(img)
        bands = ["#140A2E", "#1E0F45", "#2B1466", "#3E1A7A", "#5B2287", "#8A2E8F", "#C4448A", "#F2706A", "#FFB35C"]
        bottom = int(h * 0.64)
        for i, colour in enumerate(bands):
            d.rectangle([0, bottom * i // len(bands), w, bottom * (i + 1) // len(bands)], fill=colour)
        for _ in range(70):
            d.point((rnd.randrange(w), rnd.randrange(int(h * 0.42))), fill=rnd.choice(["#FFFFFF", "#C9B6FF", "#FFE9A8"]))
        cx, cy, r = int(w * 0.72), int(h * 0.22), 9
        for yy in range(-r, r + 1):
            for xx in range(-r, r + 1):
                if xx * xx + yy * yy <= r * r:
                    d.point((cx + xx, cy + yy), fill="#FFF3C4")
        for dx, dy in ((-3, -3), (2, 1), (-1, 4), (4, -4)):
            d.rectangle([cx + dx, cy + dy, cx + dx + 1, cy + dy + 1], fill="#E8D48A")

        def ridge(base, amp, colour):
            y = base
            for x in range(w):
                y = max(base - amp, min(base + amp, y + rnd.choice([-1, 0, 0, 1])))
                d.line([(x, y), (x, h)], fill=colour)

        ridge(int(h * 0.6), 6, "#4A1F7A")
        ridge(int(h * 0.68), 6, "#2E1458")
        ridge(int(h * 0.76), 5, "#1B0B3A")
        ground = int(h * 0.84)
        d.rectangle([0, ground, w, h], fill="#0F0724")
        for x in range(0, w, 4):
            d.rectangle([x, ground, x + 1, ground + 1], fill="#3FBF5A")
            d.rectangle([x + 2, ground + 2, x + 3, ground + 3], fill="#2A8A42")
        for _ in range(5):
            cx, cy = rnd.randrange(8, w - 12), rnd.randrange(int(h * 0.1), int(h * 0.4))
            for bx, by, bw in ((0, 0, 10), (2, -2, 6), (-2, 2, 14)):
                d.rectangle([cx + bx, cy + by, cx + bx + bw, cy + by + 1], fill="#D9C8FF")
        return img.resize((W, H), Image.NEAREST).convert("RGBA")

    # MANGA: panels with screentone, speed lines and a splash of sakura pink.
    def paint_manga(entry, rnd):
        pink = hex_rgb(entry["colors"]["accent"])
        img = Image.new("RGBA", (W, H), (252, 251, 248, 255))
        d = ImageDraw.Draw(img)
        panels = [(30, 40, W - 30, 520), (30, 560, W // 2 - 10, 1060), (W // 2 + 10, 560, W - 30, 1060),
                  (30, 1100, W - 30, H - 40)]
        for index, box in enumerate(panels):
            x0, y0, x1, y1 = box
            tile = Image.new("RGBA", (x1 - x0, y1 - y0), (252, 251, 248, 255))
            td = ImageDraw.Draw(tile)
            pw, ph = tile.size
            if index == 0:
                cx, cy = pw * 0.62, ph * 0.5
                for _ in range(150):
                    a = rnd.uniform(0, math.tau)
                    inner = rnd.uniform(70, 170)
                    outer = max(pw, ph)
                    td.line([(cx + math.cos(a) * inner, cy + math.sin(a) * inner),
                             (cx + math.cos(a) * outer, cy + math.sin(a) * outer)], fill=(30, 30, 34, 255), width=rnd.choice([1, 2, 2, 3]))
            elif index == 1:
                for yy in range(0, ph, 16):
                    for xx in range(0, pw, 16):
                        size = 1 + 6.5 * (yy / ph)
                        ox = 8 if (yy // 16) % 2 else 0
                        td.ellipse([xx + ox - size / 2, yy - size / 2, xx + ox + size / 2, yy + size / 2], fill=pink + (255,))
            elif index == 2:
                for k in range(-ph, pw, 14):
                    td.line([(k, 0), (k + ph, ph)], fill=(60, 60, 66, 255), width=2)
            else:
                for yy in range(0, ph, 14):
                    for xx in range(0, pw, 14):
                        size = 1 + 5.5 * (1 - yy / ph)
                        ox = 7 if (yy // 14) % 2 else 0
                        td.ellipse([xx + ox - size / 2, yy - size / 2, xx + ox + size / 2, yy + size / 2], fill=(40, 40, 46, 255))
            img.paste(tile, (x0, y0))
            d.rectangle(box, outline=(20, 20, 24, 255), width=8)
        return img

    def lamp(d, x, y, size):
        # A clay lamp: a shallow bowl with a lit wick.
        d.pieslice([x - size, y - size * 0.55, x + size, y + size * 0.75], 0, 180, fill=(176, 92, 40, 255))
        d.pieslice([x - size * 0.85, y - size * 0.45, x + size * 0.85, y + size * 0.45], 0, 180, fill=(120, 58, 26, 255))
        d.polygon([(x, y - size * 1.5), (x - size * 0.28, y - size * 0.45), (x + size * 0.28, y - size * 0.45)], fill=(255, 214, 120, 255))

    # DIWALI: a row of lit clay lamps in a warm dark, with golden lights out of focus behind them.
    def paint_lamps(entry, rnd):
        img = sky((38, 8, 14), (14, 4, 6))
        for _ in range(46):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(14, 52)
            colour = rnd.choice([(255, 178, 60), (255, 120, 40), (255, 214, 120), (220, 70, 90)])
            img = glow(img, lambda d, x=x, y=y, r=r, c=colour: d.ellipse([x - r, y - r, x + r, y + r], fill=c + (rnd.randint(40, 90),)), 6)
        positions = [(0.18, 0.78, 46), (0.5, 0.74, 56), (0.82, 0.79, 44), (0.34, 0.86, 38), (0.68, 0.88, 40)]
        for fx, fy, size in positions:
            x, y = fx * W, fy * H
            img = glow(img, lambda d, x=x, y=y, s=size: d.ellipse([x - s * 2.6, y - s * 3.2, x + s * 2.6, y + s * 1.2], fill=(255, 170, 60, 90)), 40)
            img = sharp(img, lambda d, x=x, y=y, s=size: lamp(d, x, y, s))
        return img

    # MARIGOLD: only the glow: orange, gold and magenta lights drifting in the dark.
    def paint_marigold(entry, rnd):
        img = sky((46, 10, 22), (18, 6, 10))
        palette = [(255, 150, 40), (255, 196, 70), (232, 70, 120), (255, 110, 60), (190, 50, 110)]
        for _ in range(60):
            x, y, r = rnd.uniform(-40, W + 40), rnd.uniform(0, H), rnd.uniform(24, 110)
            colour = rnd.choice(palette)
            img = glow(img, lambda d, x=x, y=y, r=r, c=colour: d.ellipse([x - r, y - r, x + r, y + r], fill=c + (rnd.randint(30, 80),)), 14)
        img = glow(img, lambda d: d.ellipse([W * 0.1, H * 0.3, W * 0.9, H * 0.75], fill=(255, 150, 60, 40)), 160)
        return img

    # A CRESCENT NIGHT: emerald dark, a golden crescent and star, lanterns hanging from the top and a
    # faint eight-point star lattice across the foot.
    def paint_crescent(entry, rnd):
        img = sky((6, 40, 44), (3, 14, 20))
        gold = (236, 190, 96)
        for _ in range(90):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.6)
            r = rnd.choice([1.2, 1.6, 2.2, 3.0])
            img = sharp(img, lambda d, x=x, y=y, r=r: d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 200, rnd.randint(110, 230))))

        cx, cy, r = W * 0.7, H * 0.2, 150
        crescent_layer = layer()
        ImageDraw.Draw(crescent_layer).ellipse([cx - r, cy - r, cx + r, cy + r], fill=gold + (255,))
        alpha = crescent_layer.getchannel("A")
        cut = Image.new("L", (W, H), 0)
        ImageDraw.Draw(cut).ellipse([cx - r * 0.62, cy - r * 1.04, cx + r * 1.2, cy + r * 0.66], fill=255)
        alpha.paste(0, mask=cut)
        crescent_layer.putalpha(alpha)
        img = Image.alpha_composite(img, crescent_layer.filter(ImageFilter.GaussianBlur(0.6)))
        img = glow(img, lambda d: d.ellipse([cx - 230, cy - 230, cx + 230, cy + 230], fill=gold + (50,)), 70)

        def star(d, x, y, r, points=8):
            pts = []
            for k in range(points * 2):
                rr = r if k % 2 == 0 else r * 0.55
                a = math.pi * k / points - math.pi / 2
                pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
            d.polygon(pts, fill=gold + (255,))

        img = glow(img, lambda d: star(d, W * 0.52, H * 0.3, 40), 12)
        img = sharp(img, lambda d: star(d, W * 0.52, H * 0.3, 26))

        def lantern(d, x, length, size):
            d.line([(x, 0), (x, length)], fill=gold + (160,), width=3)
            top = length
            d.polygon([(x - size * 0.5, top + size * 0.25), (x, top - size * 0.35), (x + size * 0.5, top + size * 0.25)], fill=gold + (255,))
            d.rounded_rectangle([x - size * 0.42, top + size * 0.25, x + size * 0.42, top + size * 1.5], radius=size * 0.18, fill=(255, 170, 60, 210), outline=gold + (255,), width=4)
            d.polygon([(x - size * 0.3, top + size * 1.5), (x, top + size * 1.95), (x + size * 0.3, top + size * 1.5)], fill=gold + (255,))

        for fx, length, size in ((0.16, 150, 70), (0.4, 260, 60), (0.9, 190, 64)):
            img = glow(img, lambda d, x=fx * W, l=length, s=size: lantern(d, x, l, s), 20)
            img = sharp(img, lambda d, x=fx * W, l=length, s=size: lantern(d, x, l, s))

        def lattice(d):
            step = 120
            for gy in range(int(H * 0.62), H + step, step):
                for gx in range(0, W + step, step):
                    cx2 = gx + (step // 2 if ((gy // step) % 2) else 0)
                    d.line([(cx2 - 40, gy), (cx2 + 40, gy)], fill=gold + (34,), width=2)
                    d.line([(cx2, gy - 40), (cx2, gy + 40)], fill=gold + (34,), width=2)
                    d.line([(cx2 - 28, gy - 28), (cx2 + 28, gy + 28)], fill=gold + (34,), width=2)
                    d.line([(cx2 - 28, gy + 28), (cx2 + 28, gy - 28)], fill=gold + (34,), width=2)

        return sharp(img, lattice)

    # HOLI: powder colour clouds drifting through a dark, with fine specks of powder.
    def paint_powder(entry, rnd):
        img = sky((16, 8, 36), (8, 4, 20))
        palette = [(255, 56, 140), (255, 200, 30), (0, 200, 230), (80, 220, 90), (255, 120, 30), (150, 70, 255)]
        for _ in range(26):
            x, y, r = rnd.uniform(-60, W + 60), rnd.uniform(-60, H + 60), rnd.uniform(110, 300)
            colour = rnd.choice(palette)
            img = glow(img, lambda d, x=x, y=y, r=r, c=colour: d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=c + (rnd.randint(120, 200),)), 60)
        for _ in range(900):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            r = rnd.choice([1, 1, 2, 2, 3])
            colour = rnd.choice(palette)
            img = sharp(img, lambda d, x=x, y=y, r=r, c=colour: d.ellipse([x - r, y - r, x + r, y + r], fill=c + (rnd.randint(90, 220),)))
        return img

    # LUNAR NEW YEAR: lucky red with a golden lattice of overlapping circles and a rising gold sun.
    def paint_fortune(entry, rnd):
        img = sky((150, 18, 28), (62, 6, 14))
        gold = (255, 205, 100)

        def lattice(d):
            r = 70
            for row in range(-1, int(H / r) + 2):
                for col in range(-1, int(W / (r * 1.4)) + 2):
                    cx = col * r * 1.4 + (r * 0.7 if row % 2 else 0)
                    cy = row * r * 0.7
                    for k, rr in enumerate((r, r * 0.74, r * 0.48)):
                        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=gold + (34 - k * 6,), width=2)

        img = sharp(img, lattice)
        img = glow(img, lambda d: d.ellipse([W * 0.15, H * 0.08, W * 0.85, H * 0.5], fill=gold + (70,)), 120)
        img = sharp(img, lambda d: d.ellipse([W * 0.34, H * 0.14, W * 0.66, H * 0.14 + W * 0.32], fill=gold + (235,)))
        for _ in range(120):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            r = rnd.choice([1.5, 2, 3])
            img = sharp(img, lambda d, x=x, y=y, r=r: d.ellipse([x - r, y - r, x + r, y + r], fill=gold + (rnd.randint(80, 200),)))
        return img

    g["PAINTERS"].update(pixels=paint_pixels, manga=paint_manga, lamps=paint_lamps, marigold=paint_marigold,
                         crescent=paint_crescent, powder=paint_powder, fortune=paint_fortune)

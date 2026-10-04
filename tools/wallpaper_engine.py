"""THE WALLPAPER ENGINE: phone-sized pictures for the catalog, made the way a designer would make them
by hand rather than as flat computer gradients.

A picture is built in layers, every one of them optional:

  base     a mesh gradient of four to six soft colour points, blended in Oklab so the colours between
           them stay clean rather than going muddy, and gently warped so no edge looks ruled; or a
           photograph ("photo wash"), cropped to the phone around a focus point, softened, mapped onto
           the theme's own palette and washed with a gradient in its colours;
  blobs    soft, blurred pools of light, screened over the base;
  wash     vertical bands of colour over everything, which is how the foot of the screen is kept dark
           (or light) enough for the dock;
  texture  a faint paper or linen surface;
  vignette a gentle darkening towards the corners;
  silhouette a flat dark shape along the foot, such as hills under a moon;
  grain    monochrome film grain, which also breaks up the banding a smooth gradient shows on an OLED.

Everything is seeded by the theme, so the same picture comes out on every run, and saved as WebP at
the phone's resolution, kept to a size the catalog can carry (MAX_BYTES).
"""
import hashlib
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

W, H = 1080, 2400
MAX_BYTES = 400_000

# Where the screen's furniture sits, as fractions of its height: the dock along the foot, and the
# clock at the top. A picture is checked for contrast behind both.
DOCK = (0.80, 0.97)
CLOCK = (0.04, 0.16)


# COLOUR

def hex_rgb(value):
    value = value.lstrip("#")
    if len(value) == 8:
        value = value[2:]
    return np.array([int(value[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def to_oklab(rgb):
    r, g, b = np.moveaxis(to_linear(rgb), -1, 0)
    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], axis=-1)


def from_oklab(lab):
    L, a, b = np.moveaxis(lab, -1, 0)
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return to_srgb(np.stack([4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                             -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                             -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s], axis=-1))


def luminance(rgb):
    """WCAG relative luminance of sRGB values in 0..1."""
    lin = to_linear(rgb)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def contrast(l1, l2):
    hi, lo = np.maximum(l1, l2), np.minimum(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# FIELDS

def resize_field(field, w, h):
    return np.asarray(Image.fromarray(field.astype(np.float32)).resize((w, h), Image.BICUBIC), dtype=np.float32)


def smooth_noise(rng, w, h, cells):
    """Soft noise with about [cells] bumps across the width, scaled to a standard deviation of one."""
    cw = max(3, int(cells))
    ch = max(3, int(cells * h / w))
    field = resize_field(rng.standard_normal((ch, cw)), w, h)
    return (field - field.mean()) / (field.std() + 1e-6)


def soften(field):
    """A blur of about two-thirds of a pixel: a 1-2-1 kernel down and across, so grain and fibres
    are soft-edged like film rather than hard digital speckle."""
    padded = np.pad(field, 1, mode="edge")
    across = 0.25 * padded[:, :-2] + 0.5 * padded[:, 1:-1] + 0.25 * padded[:, 2:]
    return 0.25 * across[:-2] + 0.5 * across[1:-1] + 0.25 * across[2:]


def grid(w, h):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    return xs / (w - 1), ys / (h - 1)


# THE BASE

def mesh(points, rng, warp=0.06, softness=1.0):
    """A mesh gradient through [points], each (x, y, colour) or (x, y, colour, reach), with x and y
    as fractions of the screen and reach in screen widths. Worked out at a quarter of the size, which
    a gradient this soft loses nothing by, and blended in Oklab."""
    lw, lh = W // 4, H // 4
    x, y = grid(lw, lh)
    x = x + warp * smooth_noise(rng, lw, lh, 3)
    y = y + warp * smooth_noise(rng, lw, lh, 3) * (W / H)
    total = np.zeros((lh, lw), np.float32)
    acc = np.zeros((lh, lw, 3), np.float32)
    for p in points:
        px, py, colour = p[0], p[1], p[2]
        reach = (p[3] if len(p) > 3 else 0.42) * softness
        d2 = (x - px) ** 2 + ((y - py) * H / W) ** 2
        weight = np.exp(-d2 / (2 * reach * reach)) + 1e-6
        acc += weight[..., None] * to_oklab(hex_rgb(colour))
        total += weight
    lab = acc / total[..., None]
    return np.stack([resize_field(lab[..., k], W, H) for k in range(3)], axis=-1)


def place(img, scale, center, threshold=0.12, feather=(1.3, 0.3)):
    """A zoom out for a single bright subject on a dark sky, such as the Moon: [img] set on a black
    canvas of the phone's shape, its width [scale] times the canvas's, with the subject's middle at
    [center] (fractions of the canvas). The subject is found as the pixels brighter than
    [threshold] of the brightest (its middle the median of them, its radius that of a disc of the
    same area), and the photo is faded out from feather[0] radii over feather[1] more, so its own sky
    meets the canvas without an edge."""
    a = np.asarray(img.convert("L"), np.float32)
    ys, xs = np.nonzero(a > threshold * a.max())
    mx, my = np.median(xs), np.median(ys)
    r = (len(xs) / np.pi) ** 0.5
    yy, xx = np.mgrid[0:img.height, 0:img.width]
    d = np.sqrt((xx - mx) ** 2 + (yy - my) ** 2)
    outer, fade = feather
    mask = Image.fromarray((np.clip((r * outer - d) / (r * fade), 0, 1) * 255).astype(np.uint8), "L")
    canvas_w = int(img.width / scale)
    canvas = Image.new("RGB", (canvas_w, int(canvas_w * H / W)), (0, 0, 0))
    canvas.paste(img, (int(center[0] * canvas.width - mx), int(center[1] * canvas.height - my)), mask)
    return canvas


def photo(spec, source_dir):
    """The photograph [spec] names, cropped to the phone around its focus point and softened, then
    mapped onto the palette (spec["map"]: dark-to-light stops) by spec["mapAmount"]."""
    path = os.path.join(source_dir, spec["file"])
    with Image.open(path) as raw:
        img = ImageOps.exif_transpose(raw).convert("RGB")
    if spec.get("place"):
        img = place(img, **spec["place"])
    w, h = img.size
    aspect = W / H
    zoom = spec.get("zoom", 1.0)
    cw = min(w, h * aspect) / zoom
    ch = cw / aspect
    fx, fy = spec.get("focus", (0.5, 0.5))
    left = min(max(fx * w - cw / 2, 0), w - cw)
    top = min(max(fy * h - ch / 2, 0), h - ch)
    img = img.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((W, H), Image.LANCZOS)
    if spec.get("blur"):
        img = img.filter(ImageFilter.GaussianBlur(spec["blur"]))
    rgb = np.asarray(img, dtype=np.float32) / 255.0
    lab = to_oklab(rgb)
    saturation = spec.get("saturation", 1.0)
    lab[..., 1:] *= saturation
    stops = spec.get("map")
    if stops:
        # A gradient map: the photo's lightness, stretched to its own range, read off the palette.
        L = lab[..., 0]
        lo, hi = np.percentile(L, 1), np.percentile(L, 99)
        t = np.clip((L - lo) / max(hi - lo, 1e-3), 0, 1)
        positions = np.array([s[0] for s in stops], np.float32)
        colours = np.stack([to_oklab(hex_rgb(s[1])) for s in stops])
        mapped = np.stack([np.interp(t, positions, colours[:, k]) for k in range(3)], axis=-1)
        amount = spec.get("mapAmount", 0.5)
        lab = lab * (1 - amount) + mapped * amount
    return lab


# THE LAYERS OVER IT

def blobs(img, items):
    """Soft pools of light, each (x, y, radius, colour, strength), screened over [img]."""
    lw, lh = W // 4, H // 4
    x, y = grid(lw, lh)
    for bx, by, radius, colour, strength in items:
        d2 = (x - bx) ** 2 + ((y - by) * H / W) ** 2
        g = resize_field(np.exp(-d2 / (2 * radius * radius)), W, H)[..., None] * strength
        img = 1 - (1 - img) * (1 - hex_rgb(colour) * g)
    return img


def wash(img, stops):
    """Vertical bands of colour, each stop (y, colour, opacity), laid over [img]."""
    ys = np.linspace(0, 1, H, dtype=np.float32)
    pos = np.array([s[0] for s in stops], np.float32)
    colours = np.stack([hex_rgb(s[1]) for s in stops])
    alpha = np.interp(ys, pos, np.array([s[2] for s in stops], np.float32))[:, None, None]
    colour = np.stack([np.interp(ys, pos, colours[:, k]) for k in range(3)], axis=-1)[:, None, :]
    return img * (1 - alpha) + colour * alpha


def vignette(img, amount):
    x, y = grid(W, H)
    d = np.sqrt(((x - 0.5) * 2) ** 2 + ((y - 0.5) * 2 * 0.75) ** 2)
    fall = np.clip((d - 0.55) / 0.9, 0, 1)
    return img * (1 - amount * fall * fall)[..., None]


def texture(img, kind, amount, rng):
    """A faint paper (soft fibres and cloudy density) or linen (crossed threads) surface."""
    if kind == "paper":
        fibres = resize_field(rng.standard_normal((H // 2, W // 12)), W, H)
        cloud = smooth_noise(rng, W, H, 24)
        fine = soften(rng.standard_normal((H, W)).astype(np.float32))
        field = 0.45 * fibres / (fibres.std() + 1e-6) + 0.35 * cloud + 0.2 * fine / (fine.std() + 1e-6)
    elif kind == "linen":
        rows = resize_field(rng.standard_normal((H // 2, 1)).repeat(4, axis=1), W, H)
        cols = resize_field(rng.standard_normal((1, W // 2)).repeat(4, axis=0), W, H)
        slub = smooth_noise(rng, W, H, 40)
        field = 0.45 * rows / (rows.std() + 1e-6) + 0.45 * cols / (cols.std() + 1e-6) + 0.1 * slub
    else:
        raise ValueError(kind)
    return img * (1 + amount * np.clip(field, -3, 3))[..., None]


def silhouette(img, shape, colour):
    """A flat dark shape across the foot of the screen, laid over a photo or a gradient before the
    grain, so it carries the same grain. "hills": the rolling hills the generator's painted moon has
    (its paint_moon), drawn at full size."""
    if shape != "hills":
        raise ValueError(shape)
    layer = Image.new("L", (W, H), 0)
    s = W / 720.0
    ImageDraw.Draw(layer).polygon(
        [(0, H * 0.84)] + [(x, H * 0.82 - 40 * s * np.sin(x / (90.0 * s)) - 25 * s * np.sin(x / (37.0 * s)))
                           for x in range(0, W + 1, 8)] + [(W, H), (0, H)], fill=255)
    a = (np.asarray(layer, np.float32) / 255.0)[..., None]
    return img * (1 - a) + hex_rgb(colour) * a


def grain(img, amount, rng):
    """Monochrome film grain; [amount] is the grain layer's strength (0.03 to 0.05 suits most)."""
    noise = rng.standard_normal((H, W)).astype(np.float32)
    noise = soften(noise)
    noise /= noise.std() + 1e-6
    return img + (noise * amount * 0.5)[..., None]


# THE WHOLE PICTURE

def seed(theme_id):
    return int.from_bytes(hashlib.sha256(theme_id.encode("utf-8")).digest()[:8], "big")


def render(spec, theme_id, source_dir=None, base_image=None):
    """[spec] as an RGB picture W by H. [base_image], when given, is a picture painted elsewhere
    (one of the generator's own painters), upscaled and finished here."""
    rng = np.random.default_rng(seed(theme_id))
    if base_image is not None:
        img = np.asarray(base_image.convert("RGB").resize((W, H), Image.LANCZOS), np.float32) / 255.0
    elif "photo" in spec:
        img = from_oklab(photo(spec["photo"], source_dir))
    else:
        img = from_oklab(mesh(spec["mesh"], rng, spec.get("warp", 0.06), spec.get("softness", 1.0)))
    if spec.get("blobs"):
        img = blobs(img, spec["blobs"])
    if spec.get("wash"):
        img = wash(img, spec["wash"])
    if spec.get("texture"):
        img = texture(img, spec["texture"], spec.get("textureAmount", 0.03), rng)
    if spec.get("vignette"):
        img = vignette(img, spec["vignette"])
    if spec.get("silhouette"):
        img = silhouette(img, **spec["silhouette"])
    img = grain(img, spec.get("grain", 0.04), rng)
    return Image.fromarray(np.clip(np.rint(img * 255), 0, 255).astype(np.uint8), "RGB")


def readability(img, ink):
    """How readable the dock and the clock are over [img] in the theme's [ink]: for each, the
    contrast against the area's average, and against its worst few percent (its lightest for light
    ink, its darkest for dark ink)."""
    rgb = np.asarray(img, np.float32) / 255.0
    ink_l = float(luminance(hex_rgb(ink)))
    out = {}
    for name, (top, bottom) in (("dock", DOCK), ("clock", CLOCK)):
        band = luminance(rgb[int(top * H):int(bottom * H)])
        worst = np.percentile(band, 95 if ink_l > 0.5 else 5)
        out[name] = (float(contrast(ink_l, band.mean())), float(contrast(ink_l, worst)))
    return out


def save_webp(img, path):
    """[img] as WebP at [path], at the best quality that keeps it to MAX_BYTES. Returns the size."""
    for quality in (90, 86, 82, 78, 74, 70, 66, 62, 58):
        img.save(path, "WEBP", quality=quality, method=6)
        size = os.path.getsize(path)
        if size <= MAX_BYTES:
            return size
    raise AssertionError((path, "over %d bytes even at quality 58" % MAX_BYTES))

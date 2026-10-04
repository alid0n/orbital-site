"""Helpers the themes_*.py modules share: a small kit that adds a theme to make_catalog's tables in one
call, the standard photo wash, and a contrast check for the accessibility themes.

Each module defines register(g), called by make_catalog with its own globals, so a module can use the
catalog's helpers (theme, pal, w, CLOCK ...) without importing it back."""
import math


def luminance(hex_colour):
    value = hex_colour.lstrip("#")[-6:]
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


class Kit:
    def __init__(self, g):
        self.g = g
        for name in ("pal", "w", "side", "CLOCK", "WEATHER", "MEDIA", "MEDIA_FULL", "rendered", "picture"):
            setattr(self, name, g[name])

    def photo(self, file, title, author, source, license, url):
        self.g["PHOTOS"][file] = dict(title=title, author=author, source=source, license=license, url=url,
                                      retrieved="2026-10-04")

    def washed(self, file, colour, focus=(0.5, 0.5), zoom=1.0, top=0.55, bottom=0.8, mid=0.12, blur=0.4,
               saturation=1.0, map=None, map_amount=0.5, vignette=0.15, grain=0.03, texture=None):
        photo = dict(file=file, focus=focus, zoom=zoom, blur=blur, saturation=saturation)
        if map:
            photo.update(map=map, mapAmount=map_amount)
        wash = [(0.0, colour, top), (0.18, colour, round(top * 0.8, 3)), (0.34, colour, mid),
                (0.62, colour, mid), (0.8, colour, round(bottom * 0.85, 3)), (1.0, colour, bottom)]
        spec = dict(photo=photo, wash=wash, vignette=vignette, grain=grain)
        if texture:
            spec.update(texture=texture, textureAmount=0.01)
        return self.rendered(**spec)

    def flat(self, colour):
        """A plain, single-colour wallpaper: nothing to distract, nothing to lose contrast against."""
        return self.rendered(mesh=[(0.5, 0.5, colour, 2.0), (0.2, 0.9, colour, 2.0)], warp=0.0, grain=0.0)

    def add(self, id, name, description, tags, colors, wallpaper, look, mood, swatch, layout=None,
            assistant="STANDARD", styles=("one-handed",), topics=(), **kw):
        g = self.g
        g["THEMES"].append(g["theme"](id, name, description, tags, colors, wallpaper, look, **kw))
        g["MOODS"][id] = (list(mood), swatch)
        g["TOPICS"][id] = list(topics)
        if kw.get("kind") != "accent":
            g["LAYOUTS"][id] = layout
            g["ASSISTANTS"][id] = assistant
            g["STYLES"][id] = list(styles)

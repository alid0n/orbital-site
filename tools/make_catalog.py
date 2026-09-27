"""Writes the starter theme catalog for orbitallauncher.com: one folder per theme with theme.json and
preview.png, and themes/index.json with each file's size and SHA-256. Run from anywhere."""
import hashlib
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SITE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\addis\Documents\tests\orbital-site"
ROOT = os.path.join(SITE, "themes")
APP_VERSION = 10  # the first version with the catalog


def theme(id, name, description, tags, colors, wallpaper, look, premium=False, layout=None,
          effect="", assistant=None, base="ORBITAL"):
    return dict(id=id, name=name, description=description, tags=tags, colors=colors,
                wallpaper=wallpaper, look=look, premium=premium, layout=layout, effect=effect,
                assistant=assistant, base=base)


def pal(accent, alt, ink, dim, drawer, surface, elevated, veil="#33000000", light=False):
    return dict(accent=accent, accentAlt=alt, ink=ink, dim=dim, drawer=drawer, surface=surface,
                elevated=elevated, veil=veil, light=light)


def drawn(style, colors, light=False):
    return {"drawn": {"style": style, "colors": colors, "light": light}}


THEMES = [
    theme("groove_70s", "70s Groove",
          "Burnt orange, mustard and chocolate brown, with soft rounded shapes and a warm glow.",
          ["audience:general", "era:70s", "vibe:retro", "vibe:cozy", "color:orange", "color:yellow"],
          pal("#FFB347", "#E8743B", "#FFF1DC", "#C9A27E", "#1E120A", "#28180D", "#3A2414", "#33140A04"),
          drawn("DUNES", ["#3B1F0E", "#E8743B", "#FFB347", "#D9A441", "#1A0F08"]),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="PILL", widgetEdge="NONE", widgetTint=0.3, widgetSolid=0.9,
               font="baloo_2", clockFace="STACK", panelLook="CARD", notch="DOT", glow=False)),
    theme("neon_80s", "80s Neon",
          "Hot pink and electric cyan over a glowing grid that runs to the horizon.",
          ["audience:general", "era:80s", "vibe:retro", "vibe:energetic", "color:pink", "color:neon", "color:blue"],
          pal("#FF3FA4", "#29E6FF", "#FFE9F6", "#B58DC0", "#0B0214", "#12041E", "#220A34", "#55000000"),
          drawn("HORIZON", ["#1A0433", "#000000", "#FF3FA4", "#29E6FF", "#6B3CFF"]),
          dict(corner="SLIGHT", iconShape="ROUNDED", iconStyle="DUOTONE", widgetLook="OUTLINE",
               widgetCorner="SLIGHT", widgetEdge="FINE", widgetTint=0.25, widgetSolid=0.5,
               font="audiowide", clockFace="LINE", uppercase=True, panelLook="LINES", notch="RUNG",
               glow=True, flow=True),
          premium=True, effect="twinkle-stars"),
    theme("bright_90s", "90s Bright",
          "Bold teal, purple and sunshine yellow, with playful shapes and a light, friendly page.",
          ["audience:general", "era:90s", "vibe:playful", "vibe:energetic", "color:purple", "color:yellow"],
          pal("#7B2FBF", "#0E9C9C", "#1D1230", "#6A5C80", "#FFF8E8", "#FFFBF0", "#F2ECFF", "#11FFFFFF", light=True),
          drawn("MOSAIC", ["#FFF6D8", "#E8F7F5", "#7B2FBF", "#18B7B0", "#FFC928"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="ROUNDED", widgetEdge="BOLD", widgetTint=0.2, widgetSolid=1.0,
               font="fredoka", clockFace="DIGITS", panelLook="CARD", notch="PIP")),
    theme("y2k_chrome", "Y2K Chrome",
          "Liquid silver, icy blue and frosted glass, straight out of the new millennium.",
          ["audience:general", "era:2000s", "vibe:futuristic", "vibe:dreamy", "color:blue", "color:white"],
          pal("#9FD8FF", "#D5C8FF", "#F2F7FF", "#9AA7BA", "#0A0F18", "#101826", "#1B2638", "#33060A14"),
          drawn("PRISM", ["#1A2233", "#070A12", "#CFE6FF", "#9FD8FF", "#E3D6FF"]),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.4,
               font="exo_2", clockFace="LINE", panelLook="FADE", notch="DOT", glow=True),
          premium=True),
    theme("candy", "Candy Shop",
          "Bubblegum pink, mint and lemon on a soft cream page. Sweet, bright and easy to read.",
          ["audience:kids", "vibe:playful", "color:pink", "color:pastel", "style:easy to see"],
          pal("#D6337A", "#2E9E86", "#3A1830", "#8A6A80", "#FFF6FA", "#FFF9FB", "#FFE8F2", "#11FFFFFF", light=True),
          drawn("BUBBLES", ["#FFE3F0", "#FFF7E6", "#FF8FC7", "#8FE3C8", "#FFE27A"], light=True),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="PILL", widgetEdge="NONE", widgetTint=0.35, widgetSolid=0.95,
               widgetShadow=True, font="fredoka", clockFace="STACK", panelLook="CARD", notch="DOT"),
          effect=""),
    theme("road_trip", "Road Trip",
          "Asphalt grey with sunset orange and dashed-line yellow, ready for the open road.",
          ["audience:general", "vibe:sporty", "vibe:energetic", "color:orange", "color:black"],
          pal("#FF8A3D", "#FFD23F", "#FFF3E6", "#B39C88", "#111214", "#17191C", "#24272B", "#44000000"),
          drawn("HORIZON", ["#2A1A12", "#0C0D0F", "#FF8A3D", "#FFD23F", "#C2452D"]),
          dict(corner="SLIGHT", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="SLIGHT", widgetEdge="FINE", widgetTint=0.15, widgetSolid=0.95,
               font="rajdhani", clockFace="LINE", uppercase=True, panelLook="LINES", notch="CHEVRON"),
          layout=dict(dockStyle="ROW", anchor="BOTTOM")),
    theme("beach", "Beach",
          "Sea-glass turquoise, warm sand and a bright summer sky.",
          ["audience:general", "vibe:chill", "vibe:calm", "color:blue", "color:yellow", "color:pastel"],
          pal("#0B7F8C", "#D9822B", "#10303A", "#5E7B80", "#F4FBFA", "#F8FCFB", "#E3F4F2", "#11FFFFFF", light=True),
          drawn("DUNES", ["#BFEFF2", "#F3DDB0", "#FFF4D6", "#5FC7C9", "#E8C58C"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.6,
               font="quicksand", clockFace="STACK", panelLook="FADE", notch="DOT"),
          effect=""),
    theme("sparkles", "Sparkles",
          "Midnight violet scattered with shimmering stars that sparkle across your home screen.",
          ["audience:general", "vibe:dreamy", "vibe:elegant", "color:purple", "color:gold"],
          pal("#F5C8FF", "#FFD98A", "#FCF3FF", "#B49BC4", "#0E0718", "#150A22", "#241236", "#33000000"),
          drawn("NEBULA", ["#1C0B30", "#07030F", "#F5C8FF", "#FFD98A", "#9B8CFF"]),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.3, widgetSolid=0.45,
               font="cormorant", clockFace="STACK", panelLook="FADE", notch="DOT", glow=True),
          premium=True, effect="sparkles"),
    theme("disco", "Disco",
          "Mirror-ball lights sweep the page in magenta, gold and blue. The party starts on your home screen.",
          ["audience:general", "era:70s", "vibe:energetic", "vibe:playful", "color:purple", "color:gold", "color:neon"],
          pal("#FFCC4D", "#FF4FD8", "#FFF6E6", "#C0A3C8", "#0C0412", "#14081C", "#241030", "#44000000"),
          drawn("ARCS", ["#1E0A2A", "#08030C", "#FFCC4D", "#FF4FD8", "#4FC3FF"]),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="ROUNDED", widgetEdge="FINE", widgetTint=0.3, widgetSolid=0.7,
               font="outfit", clockFace="LINE", uppercase=True, panelLook="CARD", notch="DOT", glow=True),
          premium=True, effect="disco-lights"),
    theme("gaming_90s", "90s Gaming System",
          "Classic grey plastic, a deep purple accent and chunky pixel lettering, like an evening of couch co-op.",
          ["audience:general", "era:90s", "vibe:retro", "vibe:playful", "color:purple", "style:power user"],
          pal("#8C7BFF", "#E0503C", "#EDEBF2", "#9C98A8", "#1A1A20", "#222229", "#302F3A", "#33000000"),
          drawn("GRID", ["#2B2A33", "#121216", "#8C7BFF", "#C9C6D6", "#3D3A52"]),
          dict(corner="SLIGHT", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="SLIGHT", widgetEdge="BOLD", widgetTint=0.1, widgetSolid=1.0,
               font="vt323", clockFace="DIGITS", uppercase=True, panelLook="LINES", notch="PIP"),
          layout=dict(dockStyle="ROW", drawerLayout="GRID")),
    theme("gaming_future", "Futuristic Gaming System",
          "Ice-white panels, neon cyan edges and a quiet hum of starlight. Next generation, today.",
          ["audience:general", "vibe:futuristic", "vibe:energetic", "color:blue", "color:neon", "color:white", "style:power user"],
          pal("#34F5FF", "#7B6CFF", "#EAFBFF", "#86A6B3", "#03070C", "#060D14", "#0D1A26", "#55000000"),
          drawn("LIGHT_GRID", ["#021320", "#000000", "#34F5FF", "#B6FBFF", "#1A4B8C"]),
          dict(corner="SLIGHT", iconShape="HEX", iconStyle="DUOTONE", widgetLook="BRACKET",
               widgetCorner="SLIGHT", widgetEdge="FINE", widgetTint=0.25, widgetSolid=0.5,
               font="oxanium", clockFace="LINE", uppercase=True, panelLook="LINES", notch="RUNG",
               glow=True, flow=True),
          premium=True, effect="twinkle-stars"),
    theme("gaming_green", "Green Gaming System",
          "Deep black with bright green highlights and a crisp monospace readout.",
          ["audience:general", "vibe:dark", "vibe:energetic", "color:green", "color:black", "style:power user"],
          pal("#4BE35A", "#A8FF60", "#E8FFE9", "#86A889", "#030603", "#070C07", "#102012", "#55000000"),
          drawn("HEX", ["#0A1A0B", "#000000", "#4BE35A", "#A8FF60", "#135C1A"]),
          dict(corner="SQUARE", iconShape="SQUARE", iconStyle="ORIGINAL", widgetLook="OUTLINE",
               widgetCorner="SQUARE", widgetEdge="FINE", widgetTint=0.2, widgetSolid=0.5,
               font="share_tech_mono", clockFace="LINE", uppercase=True, panelLook="LINES",
               notch="RUNG", glow=True),
          layout=dict(drawerLayout="LIST")),
    theme("cozy_cabin", "Cozy Cabin",
          "Firelight amber, pine green and warm wood. A blanket-and-cocoa kind of home screen.",
          ["audience:general", "vibe:cozy", "vibe:calm", "color:orange", "color:green"],
          pal("#F0A35E", "#8DB38B", "#FBEFE2", "#B59C85", "#140E0A", "#1C140E", "#2A1F16", "#33120A04"),
          drawn("GEARS", ["#2A1C12", "#0D0906", "#F0A35E", "#8DB38B", "#6B4426"]),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.9,
               font="lora", clockFace="STACK", panelLook="CARD", notch="DOT")),
    theme("midnight_jazz", "Midnight Jazz",
          "Smoky navy, brass and a single spotlight. Elegant, late and unhurried.",
          ["audience:general", "vibe:elegant", "vibe:chill", "vibe:dark", "color:blue", "color:gold"],
          pal("#E0B865", "#8FA9E0", "#F5EEDC", "#A39C8C", "#070A12", "#0C1120", "#161E33", "#44000000"),
          drawn("SILK", ["#141B33", "#05070E", "#E0B865", "#C9A6C3", "#2B3358"]),
          dict(corner="SLIGHT", iconShape="CIRCLE", iconStyle="MONOCHROME", widgetLook="BARE",
               widgetCorner="SLIGHT", widgetEdge="NONE", widgetTint=0.1, widgetSolid=0.3,
               font="playfair_display", clockFace="ANALOGUE", panelLook="FADE", notch="TAPER"),
          premium=True, effect="twinkle-stars"),
    theme("crayon_box", "Crayon Box",
          "Big, bright crayon colors, rounded shapes and friendly handwriting for young explorers.",
          ["audience:kids", "vibe:playful", "color:red", "color:blue", "color:yellow", "style:easy to see"],
          pal("#1F6FD1", "#E0402F", "#1E1A14", "#6F665A", "#FFFBF2", "#FFFDF7", "#FFF1D6", "#11FFFFFF", light=True),
          drawn("MOSAIC", ["#FFF4D6", "#FFFDF7", "#E0402F", "#1F6FD1", "#FFC928"], light=True),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="PILL", widgetEdge="BOLD", widgetTint=0.3, widgetSolid=1.0,
               font="patrick_hand", clockFace="DIGITS", panelLook="CARD", notch="DOT")),
    theme("arcade_assistant", "Arcade Assistant",
          "A glowing retro terminal for Orbital Assistant, with answers that type themselves out.",
          ["audience:assistant", "vibe:retro", "era:80s", "color:green", "color:black"],
          pal("#4BE35A", "#A8FF60", "#E8FFE9", "#86A889", "#030603", "#070C07", "#102012", "#55000000"),
          None,
          dict(font="vt323"),
          assistant=dict(look="RETRO"), base="TERMINAL"),
]


# EVERY THEME'S FULL LAYOUT, suited to who it is for: the home layout, the dock and where it stands,
# the widgets on the page or the drawer home, the drawer, and the assistant look it pairs with.

def w(id, kind, x, y, width=0.0, height=0.0, tint=0, scale=1.0):
    out = {"id": id, "kind": kind, "x": x, "y": y, "col": 0, "row": 0}
    if width:
        out["w"] = width
    if height:
        out["h"] = height
    if tint:
        out["tint"] = tint
    if scale != 1.0:
        out["scale"] = scale
    return out


def side(kind, tint=0, end="SIDE"):
    return {"kind": kind, "end": end, "tint": tint}


CLOCK = lambda y=0.03, scale=1.0: w("clock", "CLOCK", 0.0, y, 1.0, scale=scale)
WEATHER = lambda x=0.04, y=0.19, width=0.92: w("weather", "WEATHER", x, y, width)
MEDIA_FULL = lambda y=0.34: w("music", "MEDIA", 0.06, y, 0.88, tint=1)
MEDIA = lambda y=0.34: w("music", "MEDIA", 0.04, y, 0.92)

LAYOUTS = {
    # Warm and familiar: pages, the orbit low for the thumb, the time, the weather and music.
    "groove_70s": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    # Neon party: a bold row dock and a full Now playing card, with sparkles over the page.
    "neon_80s": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                     widgets=[CLOCK(), MEDIA_FULL(0.2)]),
    "bright_90s": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), w("week", "CALENDAR_WEEK", 0.04, 0.19, 0.92), MEDIA(0.42)]),
    # The canvas: room to arrange on a big screen.
    "y2k_chrome": dict(homeLayout="FREE_ROAM", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), WEATHER(0.06, 0.2, 0.42), MEDIA(0.36)]),
    # Kids and easy to see: big icons on pages, a plain row of apps, and very little else.
    "candy": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                  widgets=[CLOCK(scale=1.2)]),
    "crayon_box": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(scale=1.2), WEATHER(0.04, 0.2, 0.92)]),
    # Out and about: the weather and the music.
    "road_trip": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                      widgets=[CLOCK(), WEATHER(), MEDIA_FULL(0.33)]),
    "beach": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                  widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    "sparkles": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                     widgets=[CLOCK(scale=1.1), MEDIA_FULL(0.24)]),
    "disco": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                  widgets=[CLOCK(), MEDIA_FULL(0.2)]),
    # The gaming systems: a bold flat dock and a full Now playing card.
    "gaming_90s": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), MEDIA_FULL(0.2)]),
    "gaming_future": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                          widgets=[CLOCK(), MEDIA_FULL(0.2), w("battery", "BATTERY", 0.06, 0.62, 0.4)]),
    # Power user: the drawer home, with a widget column holding the calendar, and the music.
    "gaming_green": dict(homeLayout="DRAWER", dockStyle="ROW", anchor="BOTTOM", drawerLayout="LIST",
                         drawerWidgets=[side("CLOCK"), side("CALENDAR"), side("MEDIA", tint=1)]),
    "cozy_cabin": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), WEATHER(), w("next", "AGENDA", 0.04, 0.33, 0.92)]),
    # Minimal: one page with just a clock.
    "midnight_jazz": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="LIST",
                          widgets=[CLOCK(0.08, 1.2)]),
    # The assistant up front on a drawer home, with the calendar in the column.
    "arcade_assistant": dict(homeLayout="DRAWER", dockStyle="ROW", anchor="BOTTOM", drawerLayout="LIST",
                             drawerWidgets=[side("COMMAND", end="TOP"), side("CLOCK"), side("CALENDAR")]),
}

ASSISTANTS = {
    "groove_70s": "NOTEPAD", "neon_80s": "HUD", "bright_90s": "CHAT", "y2k_chrome": "SPOTLIGHT",
    "candy": "VOICE", "crayon_box": "VOICE", "road_trip": "VOICE", "beach": "CHAT",
    "sparkles": "SPOTLIGHT", "disco": "CHAT", "gaming_90s": "RETRO", "gaming_future": "HUD",
    "gaming_green": "COMMAND_PROMPT", "cozy_cabin": "NOTEPAD", "midnight_jazz": "MINIMAL_LINE",
    "arcade_assistant": "RETRO",
}

# The phone-use style each layout is for. Kept consistent with the layouts above by the app's tests.
STYLES = {
    "groove_70s": ["one-handed"], "neon_80s": ["one-handed"], "bright_90s": ["one-handed"],
    "y2k_chrome": ["big screen"], "candy": ["easy to see"], "crayon_box": ["easy to see"],
    "road_trip": ["one-handed"], "beach": ["one-handed"], "sparkles": ["one-handed"],
    "disco": ["one-handed"], "gaming_90s": ["one-handed"], "gaming_future": ["one-handed"],
    "gaming_green": ["power user"], "cozy_cabin": ["one-handed"], "midnight_jazz": ["minimal"],
    "arcade_assistant": ["power user"],
}

EFFECTS = {"neon_80s": "sparkles"}

LOOK_EXTRA = {
    "candy": dict(homeIconScale=1.3, homeLabels=True),
    "crayon_box": dict(homeIconScale=1.3, homeLabels=True),
}


def finish(entry):
    tid = entry["id"]
    entry["layout"] = dict(LAYOUTS[tid], **{k: v for k, v in (entry["layout"] or {}).items() if k not in LAYOUTS[tid]})
    entry["assistant"] = {"look": ASSISTANTS[tid]}
    entry["tags"] = [t for t in entry["tags"] if not t.startswith("style:")] + ["style:" + s for s in STYLES[tid]]
    if tid in EFFECTS:
        entry["effect"] = EFFECTS[tid]
    entry["look"] = dict(entry["look"], **LOOK_EXTRA.get(tid, {}))
    return entry


def hex_rgb(value):
    value = value.lstrip("#")
    if len(value) == 8:
        value = value[2:]
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def preview(entry, path):
    """A small portrait picture: the wallpaper's colours, a clock, a page of icons and a dock."""
    w, h = 240, 480
    paper = (entry["wallpaper"] or {}).get("drawn")
    colors = paper["colors"] if paper else [entry["colors"]["surface"], entry["colors"]["drawer"],
                                            entry["colors"]["accent"], entry["colors"]["accentAlt"],
                                            entry["colors"]["elevated"]]
    top, bottom = hex_rgb(colors[0]), hex_rgb(colors[1])
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        row = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = row
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    rnd = random.Random(entry["id"])
    for k in range(7):
        c = hex_rgb(colors[2 + k % 3])
        r = rnd.randint(40, 110)
        cx, cy = rnd.randint(0, w), rnd.randint(0, h)
        g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img)
    ink = hex_rgb(entry["colors"]["ink"])
    accent = hex_rgb(entry["colors"]["accent"])
    alt = hex_rgb(entry["colors"]["accentAlt"])
    try:
        big = ImageFont.truetype("arial.ttf", 44)
        small = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        big = small = ImageFont.load_default()
    d.text((w / 2, 70), "10:08", fill=ink, font=big, anchor="mm")
    d.text((w / 2, 104), entry["name"], fill=accent, font=small, anchor="mm")
    radius = {"PILL": 22, "ROUNDED": 12, "SLIGHT": 6, "SQUARE": 1}.get(entry["look"].get("corner", "ROUNDED"), 10)
    d.rounded_rectangle([24, 132, w - 24, 200], radius=min(radius, 30),
                        fill=hex_rgb(entry["colors"]["elevated"]) + (200,), outline=accent + (160,))
    for row in range(3):
        for col in range(4):
            cx = 42 + col * 52
            cy = 240 + row * 56
            fill = (accent if (row + col) % 3 == 0 else alt if (row + col) % 3 == 1 else ink) + (220,)
            d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=fill)
    d.arc([10, 380, w - 10, 560], 200, 340, fill=accent + (180,), width=3)
    for k in range(5):
        a = math.radians(205 + k * 32.5)
        cx = w / 2 + math.cos(a) * (w / 2 - 10)
        cy = 470 + math.sin(a) * 90
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(alt if k % 2 else accent) + (235,))
    img.convert("RGB").save(path, "PNG", optimize=True)


def theme_json(entry):
    out = {
        "kind": "orbital-theme", "format": 1,
        "id": entry["id"], "name": entry["name"], "description": entry["description"],
        "author": "Orbital", "version": 1, "minAppVersion": APP_VERSION,
        "premium": entry["premium"], "tags": entry["tags"], "previews": ["preview.png"],
        "base": entry["base"], "colors": entry["colors"], "look": entry["look"],
    }
    if entry["wallpaper"]:
        out["wallpaper"] = entry["wallpaper"]
    if entry["layout"]:
        out["layout"] = entry["layout"]
    if entry["assistant"]:
        out["assistant"] = entry["assistant"]
    if entry["effect"]:
        out["effect"] = entry["effect"]
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def main():
    os.makedirs(ROOT, exist_ok=True)
    index = []
    for entry in map(finish, THEMES):
        folder = os.path.join(ROOT, entry["id"])
        os.makedirs(folder, exist_ok=True)
        data = theme_json(entry).encode("utf-8")
        with open(os.path.join(folder, "theme.json"), "wb") as f:
            f.write(data)
        png = os.path.join(folder, "preview.png")
        preview(entry, png)
        size = os.path.getsize(png)
        assert size < 300_000, (entry["id"], size)
        index.append({
            "id": entry["id"], "name": entry["name"], "description": entry["description"],
            "version": 1, "tags": entry["tags"], "thumbnail": entry["id"] + "/preview.png",
            "file": entry["id"] + "/theme.json", "premium": entry["premium"], "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "base": entry["base"],
            "colors": entry["colors"],
        })
        print(entry["id"], len(data), "bytes json,", size, "bytes png")
    with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"kind": "orbital-theme-index", "format": 1, "themes": index}, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()

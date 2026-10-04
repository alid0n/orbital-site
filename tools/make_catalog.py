"""Writes the starter theme catalog for orbitallauncher.com: one folder per theme with theme.json and
preview.png, themes/index.json with each file's size and SHA-256, and t/<id>/index.html, the page a
shared theme link (orbitallauncher.com/t/<id>) shows where Orbital is not installed. Run from
anywhere."""
import calendar
import datetime
import hashlib
import html
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

import wallpaper_engine as engine

SITE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\addis\Documents\tests\orbital-site"
ROOT = os.path.join(SITE, "themes")
APP_VERSION = 10  # the first version with the catalog

# The original photographs the photo-wash wallpapers are made from. They stay out of git: only the
# finished WebP is published. Where a photo is not here, its theme's committed wallpaper.webp is kept
# as it is rather than made again.
SOURCES = os.environ.get("ORBITAL_WALL_SRC", r"C:\osite-wall-src")


def theme(id, name, description, tags, colors, wallpaper, look, premium=False, layout=None,
          effect="", assistant=None, base="ORBITAL", season=None, tap=False, kind="full"):
    """season: the id of a season in FEATURED["seasonal"]; the theme is then offered only while that
    season is on, every year (the app's SeasonalThemes). tap: the effect answers a tap on empty
    home-screen space with a small burst (the app's TapReaction), where the effect has one.
    kind: "full", or "accent" for a theme that changes only the colours and the font, and leaves
    the layout and the wallpaper as they are."""
    return dict(id=id, name=name, description=description, tags=tags, colors=colors,
                wallpaper=wallpaper, look=look, premium=premium, layout=layout, effect=effect,
                assistant=assistant, base=base, season=season, tap=tap, kind=kind)


def pal(accent, alt, ink, dim, drawer, surface, elevated, veil="#33000000", light=False):
    return dict(accent=accent, accentAlt=alt, ink=ink, dim=dim, drawer=drawer, surface=surface,
                elevated=elevated, veil=veil, light=light)


def drawn(style, colors, light=False):
    return {"drawn": {"style": style, "colors": colors, "light": light}}


def picture(kind, **finish):
    """A wallpaper painted here, by one of the painters in PAINTERS, then finished by the wallpaper
    engine ([finish]: its grain, vignette and the rest) and saved into the theme's folder as
    wallpaper.webp at the phone's resolution."""
    return {"image": "wallpaper.webp", "paint": kind, "render": finish}


def rendered(**spec):
    """A wallpaper made by the wallpaper engine (tools/wallpaper_engine.py): a mesh gradient, or a
    photo wash of one of PHOTOS, with its light, wash, texture and grain."""
    return {"image": "wallpaper.webp", "render": spec}


# THE PHOTOGRAPHS the photo-wash wallpapers are made from, each with the credit its theme carries.
# Only public-domain and CC0 pictures from the approved sources are used (see PHOTO_SOURCES); each
# licence was checked on the picture's own page, on the date given.
PHOTO_SOURCES = {"NASA Image and Video Library", "Wikimedia Commons", "Smithsonian Open Access",
                 "The Metropolitan Museum of Art", "Art Institute of Chicago", "Cleveland Museum of Art",
                 "Rijksmuseum", "StockSnap.io"}
FREE_LICENSES = {"CC0 1.0", "Public domain"}
PHOTOS = {
    "nasa-iss073e0427643.jpg": dict(
        title="Circular arcs of star trails viewed from International Space Station", author="NASA",
        source="NASA Image and Video Library", license="Public domain",
        url="https://images.nasa.gov/details/iss073e0427643", retrieved="2026-10-03"),
    "nasa-iss075e0144232.jpg": dict(
        title="Star trails above Earth, blue lights of fishing boats, and yellow lights of Indonesia",
        author="NASA", source="NASA Image and Video Library", license="Public domain",
        url="https://images.nasa.gov/details/iss075e0144232", retrieved="2026-10-03"),
    "commons-bilberry-bush-and-moss-in-gullmarsskogen-ravine.jpg": dict(
        title="Bilberry bush and moss in Gullmarsskogen ravine", author="W.carter",
        source="Wikimedia Commons", license="CC0 1.0",
        url="https://commons.wikimedia.org/wiki/File:Bilberry_bush_and_moss_in_Gullmarsskogen_ravine.jpg",
        retrieved="2026-10-03"),
    "commons-raindrops-on-a-window-in-brastad-1.jpg": dict(
        title="Raindrops on a window in Brastad 1", author="W.carter",
        source="Wikimedia Commons", license="CC0 1.0",
        url="https://commons.wikimedia.org/wiki/File:Raindrops_on_a_window_in_Brastad_1.jpg",
        retrieved="2026-10-03"),
    "commons-shinjuku-shinjuku258.jpg": dict(
        title="Shinjuku - Shinjuku258", author="lumoplank",
        source="Wikimedia Commons", license="CC0 1.0",
        url="https://commons.wikimedia.org/wiki/File:Shinjuku_-_Shinjuku258.jpg", retrieved="2026-10-03"),
    "nasa-NHQ202211080005.jpg": dict(
        title="Total Lunar Eclipse", author="NASA/Joel Kowsky",
        source="NASA Image and Video Library", license="Public domain",
        url="https://images.nasa.gov/details/NHQ202211080005", retrieved="2026-10-03"),
    "commons-alaska-aurora-borealis.jpg": dict(
        title="Alaska Aurora Borealis", author="Justin Connaher, U.S. Air Force",
        source="Wikimedia Commons", license="Public domain",
        url="https://commons.wikimedia.org/wiki/File:Alaska_Aurora_Borealis.jpg", retrieved="2026-10-03"),
    "commons-nasa-apollo8-earthrise.jpg": dict(
        title="Earthrise (Apollo 8, AS08-14-2383)", author="NASA / Bill Anders",
        source="Wikimedia Commons", license="Public domain",
        url="https://commons.wikimedia.org/wiki/File:NASA-Apollo8-Dec24-Earthrise.jpg", retrieved="2026-10-04"),
    "commons-hokusai-great-wave-off-kanagawa.jpg": dict(
        title="The Great Wave off Kanagawa", author="Katsushika Hokusai",
        source="Wikimedia Commons", license="Public domain",
        url="https://commons.wikimedia.org/wiki/File:The_Great_Wave_off_Kanagawa.jpg", retrieved="2026-10-04"),
    "commons-wpa-grand-canyon-national-park-lccn2007676131.jpg": dict(
        title="Grand Canyon National Park, a free government service", author="Work Projects Administration Poster Collection",
        source="Wikimedia Commons", license="Public domain",
        url="https://commons.wikimedia.org/wiki/File:Grand_Canyon_National_Park,_a_free_government_service_LCCN2007676131.jpg",
        retrieved="2026-10-04"),
    "commons-nasa-sdo-fulldisk-670.jpg": dict(
        title="Full-disk Sun in extreme ultraviolet", author="NASA / Solar Dynamics Observatory",
        source="Wikimedia Commons", license="Public domain",
        url="https://commons.wikimedia.org/wiki/File:446667main1_sdo-fulldisk-670.jpg", retrieved="2026-10-04"),
    "commons-mucha-gismonda-1894.jpg": dict(
        title="Poster for Victorien Sardou's Gismonda starring Sarah Bernhardt", author="Alphonse Mucha",
        source="Wikimedia Commons", license="Public domain",
        url="https://commons.wikimedia.org/wiki/File:Alphonse_Mucha_-_Poster_for_Victorien_Sardou%27s_Gismonda_starring_Sarah_Bernhardt_-_Original.jpg",
        retrieved="2026-10-04"),
}


def credits_of(entry):
    """The credits a theme carries: one for each photograph its wallpaper is made from."""
    spec = (entry["wallpaper"] or {}).get("render") or {}
    if "photo" not in spec:
        return []
    credit = PHOTOS[spec["photo"]["file"]]
    return [{k: credit[k] for k in ("title", "author", "source", "license", "url")}]


THEMES = [
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
    theme("cozy_cabin", "Cozy Cabin",
          "Firelight amber, pine green and warm wood. A blanket-and-cocoa kind of home screen.",
          ["audience:general", "vibe:cozy", "vibe:calm", "color:orange", "color:green"],
          pal("#F0A35E", "#8DB38B", "#FBEFE2", "#B59C85", "#140E0A", "#1C140E", "#2A1F16", "#33120A04"),
          # Firelight on warm wood, a little pine, and a linen weave, like a blanket over the chair.
          rendered(mesh=[(0.2, 0.08, "#2A1C12", 0.4), (0.85, 0.2, "#1F2A1D", 0.4), (0.35, 0.5, "#6E3E1C", 0.38),
                         (0.85, 0.62, "#2A1C12", 0.4), (0.3, 0.9, "#0D0906", 0.42)],
                   blobs=[(0.3, 0.5, 0.21, "#F0A35E", 0.45), (0.72, 0.28, 0.16, "#8DB38B", 0.16)],
                   wash=[(0.0, "#0D0906", 0.0), (0.74, "#0D0906", 0.0), (1.0, "#0D0906", 0.6)],
                   texture="linen", textureAmount=0.02, vignette=0.3, grain=0.045),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.9,
               font="lora", clockFace="STACK", panelLook="CARD", notch="DOT")),
    theme("midnight_jazz", "Midnight Jazz",
          "Smoky navy, brass and a single spotlight. Elegant, late and unhurried.",
          ["audience:general", "vibe:elegant", "vibe:chill", "vibe:dark", "color:blue", "color:gold"],
          pal("#E0B865", "#8FA9E0", "#F5EEDC", "#A39C8C", "#070A12", "#0C1120", "#161E33", "#44000000"),
          # Smoky navy, with one warm brass spotlight high on the stage.
          rendered(mesh=[(0.5, 0.0, "#2B3358", 0.35), (0.12, 0.3, "#141B33", 0.4), (0.88, 0.42, "#0C1120", 0.4),
                         (0.4, 0.7, "#070A12", 0.45), (0.8, 0.92, "#05070E", 0.4)],
                   blobs=[(0.62, 0.17, 0.17, "#E0B865", 0.26), (0.3, 0.5, 0.25, "#C9A6C3", 0.07)],
                   vignette=0.35, grain=0.045),
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

    # THE SEASONAL THEMES, each listed under its season in FEATURED below.
    theme("halloween_night", "Halloween Night",
          "Pumpkin orange and deep violet under a starry October sky.",
          ["audience:general", "vibe:spooky", "vibe:dark", "color:orange", "color:purple"],
          pal("#FF8C2B", "#B06CFF", "#FFF0E0", "#B89A8C", "#0C0710", "#140B1A", "#23122C", "#44000000"),
          drawn("NEBULA", ["#24103A", "#07040C", "#FF8C2B", "#B06CFF", "#3A1C52"]),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="ROUNDED", widgetEdge="FINE", widgetTint=0.3, widgetSolid=0.8,
               font="outfit", clockFace="STACK", panelLook="CARD", notch="DOT", glow=True),
          premium=True, effect="twinkle-stars", season="halloween"),
    theme("pumpkin_patch", "Pumpkin Patch",
          "Friendly pumpkins, falling leaves and big, easy-to-read letters for autumn.",
          ["audience:kids", "vibe:playful", "color:orange", "color:yellow", "style:easy to see"],
          pal("#C2410C", "#15803D", "#2A160A", "#7A5A44", "#FFF7EC", "#FFFAF3", "#FFEBD2", "#11FFFFFF", light=True),
          drawn("BUBBLES", ["#FFE7C7", "#FFF8EC", "#FF9A3C", "#7CC46A", "#FFD166"], light=True),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="PILL", widgetEdge="BOLD", widgetTint=0.3, widgetSolid=1.0,
               font="fredoka", clockFace="DIGITS", panelLook="CARD", notch="DOT"),
          season="halloween"),
    theme("winter_snow", "Winter Snow",
          "Crisp snow white, frosted blue and a quiet, sparkling winter light.",
          ["audience:general", "vibe:calm", "vibe:cozy", "color:white", "color:blue", "color:pastel"],
          pal("#2F6FB3", "#7FA8D6", "#12263A", "#5B7189", "#F5F9FD", "#F9FBFE", "#E6EFF8", "#11FFFFFF", light=True),
          drawn("MIST", ["#EAF3FB", "#FFFFFF", "#BFD8EE", "#8FB6DD", "#DDE9F5"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.6,
               font="quicksand", clockFace="STACK", panelLook="FADE", notch="DOT"),
          season="winter"),
    theme("valentines_day", "Valentine's",
          "Rose red, soft blush and warm gold, with rounded shapes and a gentle glow.",
          ["audience:general", "vibe:dreamy", "vibe:elegant", "color:red", "color:pink", "color:gold"],
          pal("#E0245E", "#F2B45A", "#FFF0F4", "#C79AA8", "#1A070D", "#230A12", "#36111D", "#33000000"),
          drawn("PETALS", ["#3A0D1C", "#12040A", "#E0245E", "#FF8FB1", "#F2B45A"]),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.3, widgetSolid=0.5,
               font="cormorant", clockFace="STACK", panelLook="FADE", notch="DOT", glow=True),
          premium=True, effect="sparkles", season="valentines", tap=True),
    theme("summer_splash", "Summer Splash",
          "Pool blue, lemon yellow and watermelon pink on a bright summer page.",
          ["audience:general", "vibe:energetic", "vibe:playful", "color:blue", "color:yellow", "color:pink"],
          pal("#0A74C9", "#E8436E", "#0F2A3D", "#557184", "#F2FAFF", "#F7FCFF", "#E0F1FC", "#11FFFFFF", light=True),
          drawn("DUNES", ["#BFE8FF", "#FFF6C7", "#FF8FAB", "#39B7F0", "#FFD84D"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="ROUNDED", widgetEdge="NONE", widgetTint=0.25, widgetSolid=0.9,
               font="baloo_2", clockFace="STACK", panelLook="CARD", notch="PIP"),
          season="summer"),
    theme("spring_bloom", "Spring Bloom",
          "Fresh leaf green, blossom pink and morning light, for the first warm days of the year.",
          ["audience:general", "vibe:calm", "vibe:dreamy", "color:green", "color:pink", "color:pastel"],
          pal("#2E8B57", "#D94F8A", "#1B2E22", "#62786A", "#F6FBF4", "#FAFDF8", "#E7F4E4", "#11FFFFFF", light=True),
          drawn("PETALS", ["#F4FBEF", "#FFF4F8", "#9BD68C", "#F6A6C8", "#FFE59A"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.85,
               font="lora", clockFace="STACK", panelLook="CARD", notch="DOT"),
          season="spring"),

    # MORE HALLOWEEN, offered only from October 1 to November 1.
    theme("ghost_glow", "Ghost Glow",
          "Glow-in-the-dark green on midnight black, with violet accents and friendly ghosts drifting by.",
          ["audience:general", "vibe:spooky", "vibe:dark", "vibe:playful", "color:green", "color:purple", "color:neon"],
          pal("#39FF14", "#9B30FF", "#EDFFE8", "#8FB394", "#040705", "#070B08", "#101A12", "#55000000"),
          picture("ghosts", vignette=0.25, grain=0.04),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="DUOTONE", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="FINE", widgetTint=0.3, widgetSolid=0.5,
               font="permanent_marker", clockFace="STACK", panelLook="FADE", notch="DOT", glow=True),
          premium=True, effect="floating-ghosts", season="halloween", tap=True),
    theme("haunted_mansion", "Haunted Mansion",
          "Deep velvet purple and candlelight gold, with elegant lettering and bats in the rafters.",
          ["audience:general", "vibe:spooky", "vibe:elegant", "vibe:dark", "color:purple", "color:gold"],
          pal("#F2C46D", "#9D6BE0", "#F8EFDC", "#A99BB6", "#0C0612", "#130A1C", "#221336", "#44000000"),
          drawn("SILK", ["#2A1245", "#08040E", "#F2C46D", "#9D6BE0", "#3D1F5C"]),
          dict(corner="SLIGHT", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="SLIGHT", widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.8,
               font="cinzel", clockFace="ANALOGUE", panelLook="FADE", notch="TAPER", glow=True),
          premium=True, effect="bats", season="halloween", tap=True),
    theme("witching_hour", "Witching Hour",
          "Midnight black and ember orange under a copper-red eclipsed moon.",
          ["audience:general", "vibe:spooky", "vibe:dark", "color:orange", "color:black"],
          pal("#FF7A1A", "#FFB45C", "#FFF1E3", "#B39A86", "#060403", "#0C0806", "#1B120C", "#55000000"),
          # A total lunar eclipse, set small and high on a midnight sky in the theme's ember colours,
          # over the rolling hills the painted moon had. (Its old painted wallpaper.png stays
          # published, unused, for links made before.)
          rendered(photo=dict(file="nasa-NHQ202211080005.jpg", place=dict(scale=1.6, center=(0.55, 0.33)),
                              blur=0.6, saturation=0.9,
                              map=[(0.0, "#050302"), (0.4, "#24120A"), (0.78, "#E0954E"), (1.0, "#FFE9C8")], mapAmount=0.4),
                   blobs=[(0.6, 0.33, 0.22, "#FF7A1A", 0.18), (0.5, 0.8, 0.3, "#FF7A1A", 0.14)],
                   wash=[(0.0, "#050302", 0.0), (0.7, "#050302", 0.0), (1.0, "#050302", 0.6)],
                   vignette=0.25, silhouette=dict(shape="hills", colour="#080503"), grain=0.04),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5,
               font="marcellus", clockFace="STACK", uppercase=True, panelLook="FADE", notch="DOT", glow=True),
          premium=True, effect="bats", season="halloween", tap=True),
    theme("candy_corn", "Candy Corn",
          "Sunny orange, lemon yellow and bright white, with big friendly shapes for trick-or-treaters.",
          ["audience:kids", "vibe:playful", "color:orange", "color:yellow", "color:white", "style:easy to see"],
          pal("#C2410C", "#A16207", "#2B1A0A", "#7A5A44", "#FFFBF2", "#FFFDF8", "#FFF0D6", "#11FFFFFF", light=True),
          drawn("BUBBLES", ["#FFF1D6", "#FFFFFF", "#FF9A2E", "#FFD23F", "#FFF6E0"], light=True),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="PILL", widgetEdge="BOLD", widgetTint=0.3, widgetSolid=1.0,
               font="fredoka", clockFace="DIGITS", panelLook="CARD", notch="DOT"),
          season="halloween"),
    theme("spider_web", "Spider Web",
          "Silver threads on charcoal: a quiet, monochrome page with just the time.",
          ["audience:general", "vibe:spooky", "vibe:dark", "vibe:calm", "color:black", "color:white"],
          pal("#D8DCE2", "#9AA1AB", "#F2F4F7", "#8A9099", "#060607", "#0B0B0D", "#18181C", "#44000000"),
          picture("webs", vignette=0.3, grain=0.035),
          dict(corner="SLIGHT", iconShape="CIRCLE", iconStyle="MONOCHROME", widgetLook="BARE",
               widgetCorner="SLIGHT", widgetEdge="NONE", widgetTint=0.1, widgetSolid=0.3,
               font="manrope", clockFace="LINE", panelLook="FADE", notch="TAPER"),
          season="halloween"),
    theme("jack_o_lantern", "Jack-o'-Lantern",
          "A warm orange glow flickering out of the dark, like a carved pumpkin on the porch.",
          ["audience:general", "vibe:spooky", "vibe:cozy", "color:orange", "color:yellow"],
          pal("#FF9A1F", "#FFD166", "#FFF3E0", "#BFA088", "#0B0603", "#140A04", "#24130A", "#44000000"),
          drawn("NEBULA", ["#3A1A05", "#0A0502", "#FF8C1A", "#FFC247", "#7A2E00"]),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="ROUNDED", widgetEdge="NONE", widgetTint=0.3, widgetSolid=0.85,
               font="baloo_2", clockFace="STACK", panelLook="CARD", notch="DOT", glow=True),
          season="halloween"),

    # AUTUMN, through November.
    theme("harvest", "Harvest",
          "Russet, wheat gold and deep brown, with leaves drifting down past the time.",
          ["audience:general", "vibe:cozy", "vibe:calm", "color:orange", "color:gold"],
          pal("#E8A33D", "#C8553D", "#FBF0E0", "#B89C82", "#140C07", "#1C110A", "#2C1B10", "#33120A04"),
          drawn("DUNES", ["#4A2410", "#140904", "#D9822B", "#E8B04A", "#8C3B1A"]),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.9,
               font="lora", clockFace="STACK", panelLook="CARD", notch="DOT"),
          premium=True, effect="falling-leaves", season="autumn", tap=True),
    theme("autumn_leaves", "Autumn Leaves",
          "Maple red and amber on a warm cream page, bright and easy on a crisp morning.",
          ["audience:general", "vibe:cozy", "vibe:calm", "color:red", "color:orange"],
          pal("#B8401A", "#8C5A2B", "#2A170C", "#7A5E48", "#FFF8F0", "#FFFBF6", "#FBEBD9", "#11FFFFFF", light=True),
          drawn("PETALS", ["#FFF1DE", "#FFF9F0", "#D9531E", "#F2A33A", "#B5763A"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="ROUNDED", widgetEdge="NONE", widgetTint=0.25, widgetSolid=0.9,
               font="nunito", clockFace="STACK", panelLook="CARD", notch="DOT"),
          season="autumn"),

    # WINTER, from December 1 to January 6.
    theme("northern_lights", "Northern Lights",
          "Green and violet ribbons of light over a starry polar night.",
          ["audience:general", "vibe:dreamy", "vibe:calm", "color:green", "color:purple", "color:blue"],
          pal("#5CF2B8", "#8C9CFF", "#EAFBF5", "#8FA8B0", "#030811", "#060D18", "#0E1A2B", "#44000000"),
          rendered(photo=dict(file="commons-alaska-aurora-borealis.jpg", focus=(0.62, 0.5), blur=1.2, saturation=1.15,
                              map=[(0.0, "#02050C"), (0.45, "#06142A"), (0.75, "#3DF5B0"), (1.0, "#E8FFF6")], mapAmount=0.3),
                   wash=[(0.0, "#030811", 0.25), (0.25, "#030811", 0.0), (0.66, "#030811", 0.15),
                         (0.82, "#030811", 0.72), (1.0, "#030811", 0.85)],
                   vignette=0.25, grain=0.035),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.45,
               font="exo_2", clockFace="LINE", panelLook="FADE", notch="DOT", glow=True),
          premium=True, effect="twinkle-stars", season="winter", tap=True),

    # NEW YEAR, from December 26 to January 7.
    theme("midnight_fireworks", "Midnight Fireworks",
          "Gold, magenta and electric blue bursting over a midnight sky.",
          ["audience:general", "vibe:energetic", "vibe:dark", "color:gold", "color:pink", "color:blue"],
          pal("#FFD24A", "#FF4FA3", "#FFF7E0", "#B8A6C0", "#05040E", "#0A0818", "#171230", "#55000000"),
          drawn("NEBULA", ["#0B0A2A", "#02020A", "#FFD24A", "#FF4FA3", "#4FC3FF"]),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="FINE", widgetTint=0.3, widgetSolid=0.5,
               font="outfit", clockFace="LINE", uppercase=True, panelLook="FADE", notch="DOT", glow=True),
          premium=True, effect="fireworks", season="new_year", tap=True),
    theme("golden_countdown", "Golden Countdown",
          "Black and champagne gold, with one elegant clock counting down to the new year.",
          ["audience:general", "vibe:elegant", "vibe:dark", "color:gold", "color:black"],
          pal("#E8C15A", "#F5E3A8", "#FBF4E0", "#A89C80", "#060503", "#0B0906", "#19150C", "#44000000"),
          drawn("SILK", ["#1A1408", "#050402", "#E8C15A", "#FFF1C4", "#6B5320"]),
          dict(corner="SLIGHT", iconShape="CIRCLE", iconStyle="MONOCHROME", widgetLook="BARE",
               widgetCorner="SLIGHT", widgetEdge="NONE", widgetTint=0.1, widgetSolid=0.3,
               font="playfair_display", clockFace="ANALOGUE", panelLook="FADE", notch="TAPER"),
          season="new_year"),

    # VALENTINE'S, from February 1 to February 15.
    theme("love_letters", "Love Letters",
          "Blush paper, rose ink and a handwritten note, soft and warm.",
          ["audience:general", "vibe:dreamy", "vibe:calm", "color:pink", "color:red", "color:pastel"],
          pal("#B8325A", "#C77D2E", "#2E1219", "#7E5A63", "#FFF6F8", "#FFFAFB", "#FCE8EE", "#11FFFFFF", light=True),
          drawn("PETALS", ["#FFEFF3", "#FFF9FA", "#E05A7A", "#F7A8B8", "#F2C57C"], light=True),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.9,
               font="caveat", clockFace="STACK", panelLook="CARD", notch="DOT"),
          season="valentines"),

    # SPRING, from March 20 to May 31.
    theme("cherry_blossom", "Cherry Blossom",
          "Pale pink blossom, fresh green leaves and soft morning light.",
          ["audience:general", "vibe:calm", "vibe:dreamy", "color:pink", "color:green", "color:pastel"],
          pal("#B8336A", "#3E8E5A", "#2A1620", "#7A6070", "#FFF7FA", "#FFFBFD", "#FBE9F0", "#11FFFFFF", light=True),
          drawn("PETALS", ["#FFEFF5", "#FDFBFF", "#F48FB1", "#FFC1D6", "#A5D6A7"], light=True),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.7,
               font="comfortaa", clockFace="STACK", panelLook="FADE", notch="DOT"),
          season="spring"),

    # SUMMER, from June 1 to August 31.
    theme("tropical", "Tropical",
          "Lagoon teal, palm green and hibiscus coral under a bright island sun.",
          ["audience:general", "vibe:energetic", "vibe:chill", "color:blue", "color:green", "color:orange"],
          pal("#0B7A6E", "#D2472F", "#0E2A26", "#557A73", "#F2FBF8", "#F7FDFB", "#DEF4EE", "#11FFFFFF", light=True),
          drawn("DUNES", ["#B2F0E6", "#FFF3C4", "#FF6F61", "#1FB5A3", "#FFD166"], light=True),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="ROUNDED", widgetEdge="NONE", widgetTint=0.25, widgetSolid=0.9,
               font="varela_round", clockFace="STACK", panelLook="CARD", notch="PIP"),
          season="summer"),

    # THE FIRST WALLPAPER-ENGINE BATCH: mesh gradients, photo washes and two accent themes.
    #
    # Everyday minimal.
    theme("paper", "Paper",
          "Warm, softly textured paper with ink-dark lettering. A calm, uncluttered page for every day.",
          ["audience:general", "vibe:calm", "color:white"],
          pal("#2F4A6B", "#B5562E", "#1F1C18", "#77706A", "#F7F3EC", "#FAF7F1", "#EFE9DE", "#11FFFFFF", light=True),
          rendered(mesh=[(0.15, 0.1, "#F8F4EC", 0.5), (0.9, 0.2, "#F2ECE0", 0.45), (0.3, 0.55, "#F6F1E7", 0.5),
                         (0.85, 0.75, "#EDE5D6", 0.45), (0.2, 0.95, "#E9E1D1", 0.4)],
                   blobs=[(0.78, 0.12, 0.35, "#FFF9EE", 0.35)],
                   texture="paper", textureAmount=0.012, vignette=0.1, grain=0.035),
          dict(corner="SLIGHT", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="SLIGHT", widgetEdge="HAIR", widgetTint=0.1, widgetSolid=0.9,
               font="dm_sans", clockFace="LINE", panelLook="LINES", notch="TAPER")),
    theme("graphite", "Graphite",
          "Cool graphite greys and crisp white lettering. Refreshes your colours and font, and keeps "
          "your layout and wallpaper just as they are.",
          ["audience:general", "vibe:calm", "vibe:dark", "color:black", "color:white"],
          pal("#C9CED6", "#8A93A0", "#EEF0F3", "#8B9099", "#121315", "#17181B", "#222428", "#44000000"),
          None,
          dict(font="inter"),
          kind="accent"),
    # Calm.
    theme("matcha", "Matcha",
          "Soft green tea and warm cream with rounded lettering. Refreshes your colours and font, and "
          "keeps your layout and wallpaper just as they are.",
          ["audience:general", "vibe:calm", "color:green", "color:pastel"],
          pal("#4F7A3A", "#A8834B", "#1F2A1A", "#6B7564", "#F3F5EC", "#F7F8F1", "#E6ECD9", "#11FFFFFF", light=True),
          None,
          dict(font="quicksand"),
          kind="accent"),
    # Nature.
    theme("forest_floor", "Forest Floor",
          "Moss, bilberry leaves and dappled woodland light, in deep greens that keep every icon clear.",
          ["audience:general", "vibe:calm", "vibe:cozy", "color:green"],
          pal("#B8D98A", "#E0B15C", "#EEF4E6", "#9AAB8F", "#0B120B", "#101910", "#1A271A", "#44000000"),
          rendered(photo=dict(file="commons-bilberry-bush-and-moss-in-gullmarsskogen-ravine.jpg", focus=(0.6, 0.5),
                              blur=1.0, saturation=0.85,
                              map=[(0.0, "#071007"), (0.5, "#2F4A22"), (0.85, "#A9C27A"), (1.0, "#F2E9C8")], mapAmount=0.4),
                   wash=[(0.0, "#0B120B", 0.45), (0.2, "#0B120B", 0.1), (0.6, "#0B120B", 0.15),
                         (0.8, "#0B120B", 0.7), (1.0, "#0B120B", 0.85)],
                   vignette=0.3, grain=0.04),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.5,
               font="lora", clockFace="STACK", panelLook="FADE", notch="DOT"),
          premium=True),
    theme("desert_dusk", "Desert Dusk",
          "Rose, apricot and violet melting into a desert evening, finished with a fine film grain.",
          ["audience:general", "vibe:calm", "vibe:dreamy", "color:pink", "color:purple", "color:orange"],
          pal("#FFB38A", "#C9A0FF", "#FFF2EA", "#C4A6A0", "#1A0F17", "#22131D", "#33202C", "#44000000"),
          rendered(mesh=[(0.2, 0.05, "#C9786A", 0.4), (0.85, 0.18, "#B8606E", 0.42), (0.3, 0.27, "#E89A7A", 0.3),
                         (0.35, 0.42, "#9C5C86", 0.45), (0.8, 0.6, "#4C2F5E", 0.42), (0.25, 0.8, "#2A1830", 0.45),
                         (0.7, 0.98, "#140A14", 0.4)],
                   blobs=[(0.66, 0.36, 0.16, "#FFD2A6", 0.35)],
                   wash=[(0.0, "#140A14", 0.3), (0.2, "#140A14", 0.0), (0.72, "#140A14", 0.0), (1.0, "#140A14", 0.55)],
                   vignette=0.25, grain=0.045),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.45,
               font="marcellus", clockFace="STACK", uppercase=True, panelLook="FADE", notch="DOT"),
          premium=True),
    # From the seasonal list, though rain is welcome all year, so it is offered all year.
    theme("cozy_rainy_day", "Cozy Rainy Day",
          "Raindrops on the window and warm lamplight beyond. A calm, cozy page for slow afternoons.",
          ["audience:general", "vibe:cozy", "vibe:calm", "vibe:dark", "color:orange", "color:black"],
          pal("#F2B66D", "#8FB3C9", "#F6EFE6", "#A99F94", "#0E0D0C", "#151311", "#221F1B", "#44000000"),
          rendered(photo=dict(file="commons-raindrops-on-a-window-in-brastad-1.jpg", focus=(0.5, 0.45), blur=0.8,
                              saturation=0.9,
                              map=[(0.0, "#0E0D0C"), (0.5, "#3A332B"), (0.85, "#E3A867"), (1.0, "#FFF0D8")], mapAmount=0.35),
                   wash=[(0.0, "#0E0D0C", 0.2), (0.3, "#0E0D0C", 0.0), (0.7, "#0E0D0C", 0.2),
                         (0.84, "#0E0D0C", 0.7), (1.0, "#0E0D0C", 0.85)],
                   vignette=0.25, grain=0.04),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="PAPER",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.85,
               font="nunito", clockFace="STACK", panelLook="CARD", notch="DOT"),
          premium=True),
    # City.
    theme("tokyo_night", "Tokyo Night",
          "Neon signs and late-night streets in Shinjuku, tinted magenta and electric blue.",
          ["audience:general", "vibe:energetic", "vibe:dark", "color:pink", "color:blue", "color:neon"],
          pal("#FF4FA0", "#3FE0FF", "#F3F0FF", "#A79EC4", "#08061A", "#0E0B24", "#1A1538", "#55000000"),
          rendered(photo=dict(file="commons-shinjuku-shinjuku258.jpg", focus=(0.5, 0.42), blur=1.0, saturation=1.05,
                              map=[(0.0, "#08061A"), (0.45, "#2A1F5C"), (0.75, "#FF4FA0"), (1.0, "#BFF6FF")], mapAmount=0.4),
                   wash=[(0.0, "#08061A", 0.5), (0.22, "#08061A", 0.05), (0.62, "#08061A", 0.15),
                         (0.8, "#08061A", 0.75), (1.0, "#08061A", 0.88)],
                   vignette=0.25, grain=0.04),
          dict(corner="SLIGHT", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="SLIGHT", widgetEdge="FINE", widgetTint=0.3, widgetSolid=0.5,
               font="space_grotesk", clockFace="LINE", uppercase=True, panelLook="LINES", notch="CHEVRON", glow=True),
          premium=True),
    # Premium showpieces, built around the Showcase and the Orbit Pad.
    theme("constellation", "Constellation",
          "Star trails circling above the Earth, photographed from the International Space Station, "
          "with gold lettering and the Showcase layout.",
          ["audience:general", "vibe:elegant", "vibe:dark", "vibe:dreamy", "color:blue", "color:gold"],
          pal("#F2D28A", "#8FB8FF", "#F4F1E8", "#A3A6B8", "#05060D", "#090B16", "#141A2C", "#55000000"),
          rendered(photo=dict(file="nasa-iss073e0427643.jpg", focus=(0.6, 0.5), blur=1.2, saturation=0.8,
                              map=[(0.0, "#04060E"), (0.45, "#1B2440"), (0.8, "#B8925A"), (1.0, "#FFF0D0")], mapAmount=0.45),
                   wash=[(0.0, "#05060D", 0.25), (0.3, "#05060D", 0.0), (0.7, "#05060D", 0.15),
                         (0.84, "#05060D", 0.7), (1.0, "#05060D", 0.85)],
                   vignette=0.3, grain=0.035),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.45,
               font="cormorant", clockFace="LINE", panelLook="FADE", notch="TAPER", glow=True),
          premium=True, effect="twinkle-stars", tap=True),
    theme("glass", "Glass",
          "Luminous cyan and violet light behind frosted glass, built around the Orbit Pad.",
          ["audience:general", "vibe:futuristic", "vibe:calm", "vibe:dark", "color:blue", "color:purple"],
          pal("#9FE8FF", "#C6A8FF", "#F2F7FF", "#9DA9C0", "#070A12", "#0C111C", "#18202F", "#44000000"),
          rendered(mesh=[(0.15, 0.12, "#1A2C5C", 0.4), (0.85, 0.08, "#3B2A6E", 0.4), (0.5, 0.45, "#0E1830", 0.45),
                         (0.2, 0.7, "#123A52", 0.4), (0.85, 0.85, "#070A12", 0.4)],
                   blobs=[(0.25, 0.28, 0.2, "#6FD8FF", 0.55), (0.8, 0.42, 0.22, "#B48CFF", 0.5),
                          (0.45, 0.62, 0.16, "#4FA8FF", 0.3)],
                   wash=[(0.0, "#070A12", 0.0), (0.74, "#070A12", 0.0), (1.0, "#070A12", 0.6)],
                   vignette=0.3, grain=0.04, warp=0.09),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.35,
               font="lexend", clockFace="LINE", panelLook="FADE", notch="DOT", glow=True),
          premium=True),
    # Kids.
    theme("space_cadet", "Space Cadet",
          "Stars and city lights seen from the International Space Station, with big, bright icons for "
          "young astronauts.",
          ["audience:kids", "vibe:playful", "color:blue", "color:yellow"],
          pal("#FFD23F", "#4FC3FF", "#FFFFFF", "#B4C2E0", "#070B1E", "#0C1230", "#182253", "#55000000"),
          rendered(photo=dict(file="nasa-iss075e0144232.jpg", focus=(0.5, 0.45), blur=1.5,
                              map=[(0.0, "#050A24"), (0.5, "#1E3A8A"), (0.85, "#4FC3FF"), (1.0, "#FFF6D0")], mapAmount=0.35),
                   wash=[(0.0, "#070B1E", 0.2), (0.25, "#070B1E", 0.0), (0.62, "#070B1E", 0.15),
                         (0.8, "#070B1E", 0.72), (1.0, "#070B1E", 0.85)],
                   vignette=0.2, grain=0.035),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="PILL", widgetEdge="BOLD", widgetTint=0.3, widgetSolid=1.0,
               font="fredoka", clockFace="DIGITS", panelLook="CARD", notch="DOT")),
    # Five themes from public-domain art and NASA pictures, each on a different layout and dock.
    theme("earthrise", "Earthrise",
          "The Earth rising over the Moon, as the Apollo 8 crew saw it in 1968, with quiet lettering "
          "and a free-roaming canvas.",
          ["audience:general", "vibe:calm", "vibe:dark", "vibe:futuristic", "color:blue", "color:black"],
          pal("#7FB3E6", "#D9C9A8", "#F2F4F7", "#8A94A3", "#07090D", "#0D1117", "#161C25", "#33000000"),
          rendered(photo=dict(file="commons-nasa-apollo8-earthrise.jpg", focus=(0.68, 0.5), blur=0.6, saturation=0.95),
                   wash=[(0.0, "#05070B", 0.45), (0.22, "#05070B", 0.0), (0.7, "#05070B", 0.2),
                         (0.82, "#05070B", 0.78), (1.0, "#05070B", 0.9)],
                   vignette=0.25, grain=0.03),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.4,
               font="inter", clockFace="BARE", panelLook="FADE", notch="DOT"),
          premium=True),
    theme("great_wave", "Great Wave",
          "Hokusai's wave over warm paper, with indigo lettering and a vermilion seal, and every app "
          "on one drawer home.",
          ["audience:general", "vibe:elegant", "vibe:calm", "color:blue", "color:white", "color:red"],
          pal("#1F4E8C", "#C2452D", "#14233F", "#5A6781", "#F1E8D4", "#F5EDDA", "#E7DBBE", "#22F1E8D4", light=True),
          rendered(photo=dict(file="commons-hokusai-great-wave-off-kanagawa.jpg", focus=(0.3, 0.5), blur=0.4, saturation=0.9),
                   wash=[(0.0, "#F1E8D4", 0.5), (0.2, "#F1E8D4", 0.2), (0.6, "#F1E8D4", 0.3),
                         (0.8, "#F1E8D4", 0.8), (1.0, "#F1E8D4", 0.9)],
                   texture="paper", textureAmount=0.012, vignette=0.08, grain=0.03),
          dict(corner="SLIGHT", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="OUTLINE",
               widgetCorner="SLIGHT", widgetEdge="FINE", widgetTint=0.1, widgetSolid=0.8,
               font="cormorant", clockFace="ANALOGUE", panelLook="LINES", notch="TAPER"),
          premium=True),
    theme("canyon_poster", "Canyon Poster",
          "A 1930s national park poster of the Grand Canyon, in sunset rust and gold with bold capitals "
          "and a flat dock along the right edge.",
          ["audience:general", "vibe:retro", "vibe:energetic", "color:orange", "color:gold", "era:30s"],
          pal("#F0A03C", "#D2552B", "#FBEBD0", "#D9B98F", "#1F100A", "#2A1710", "#3B2318", "#33000000"),
          rendered(photo=dict(file="commons-wpa-grand-canyon-national-park-lccn2007676131.jpg", focus=(0.5, 0.5), blur=0.5, saturation=0.95),
                   wash=[(0.0, "#1F100A", 0.55), (0.22, "#1F100A", 0.3), (0.6, "#1F100A", 0.4),
                         (0.8, "#1F100A", 0.8), (1.0, "#1F100A", 0.9)],
                   vignette=0.2, grain=0.04),
          dict(corner="SQUARE", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="SOLID",
               widgetCorner="SQUARE", widgetEdge="BOLD", widgetTint=0.3, widgetSolid=1.0,
               font="montserrat", clockFace="DIGITS", uppercase=True, panelLook="CARD", notch="CHEVRON")),
    theme("solar", "Solar",
          "The Sun in extreme ultraviolet from NASA's Solar Dynamics Observatory, in ember orange, with "
          "the Showcase layout.",
          ["audience:general", "vibe:energetic", "vibe:futuristic", "vibe:dark", "color:orange", "color:gold"],
          pal("#FF7A1A", "#FFC24A", "#FFF1E0", "#C99B73", "#050302", "#0A0605", "#1B0F09", "#33000000"),
          rendered(photo=dict(file="commons-nasa-sdo-fulldisk-670.jpg", focus=(0.5, 0.5), blur=0.8, saturation=1.0,
                              map=[(0.0, "#050302"), (0.4, "#4A1604"), (0.75, "#FF7A1A"), (1.0, "#FFE7B0")], mapAmount=0.85),
                   wash=[(0.0, "#050302", 0.7), (0.18, "#050302", 0.6), (0.3, "#050302", 0.0), (0.7, "#050302", 0.1),
                         (0.82, "#050302", 0.72), (1.0, "#050302", 0.88)],
                   vignette=0.3, grain=0.03),
          dict(corner="ROUNDED", iconShape="SQUIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS",
               widgetCorner="ROUNDED", widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5,
               font="oxanium", clockFace="LINE", panelLook="FADE", notch="CHEVRON", glow=True),
          premium=True),
    theme("gismonda", "Gismonda",
          "Mucha's 1894 Art Nouveau poster in gold and sage, with a serif clock and the Orbit Pad.",
          ["audience:general", "vibe:elegant", "vibe:dreamy", "color:gold", "color:green"],
          pal("#D8A93C", "#8FA47A", "#F5E9C8", "#BDAE86", "#17130A", "#231E12", "#322A19", "#44000000"),
          rendered(photo=dict(file="commons-mucha-gismonda-1894.jpg", focus=(0.5, 0.4), zoom=1.5, blur=0.4, saturation=1.0),
                   wash=[(0.0, "#17130A", 0.55), (0.2, "#17130A", 0.3), (0.6, "#17130A", 0.3),
                         (0.8, "#17130A", 0.82), (1.0, "#17130A", 0.9)],
                   vignette=0.25, grain=0.035),
          dict(corner="PILL", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD",
               widgetCorner="PILL", widgetEdge="HAIR", widgetTint=0.3, widgetSolid=0.8,
               font="playfair_display", clockFace="STACK", panelLook="CARD", notch="DOT"),
          premium=True),
]

# EACH THEME'S MOOD (the words the store's mood filter offers) and its swatch, the one colour it is
# filed under in the colour filter: the colour it reads as at a glance.
MOOD_WORDS = {"calm", "bold", "dark", "light", "pastel", "vivid", "minimal", "cozy", "playful"}
MOODS = {
    "candy": (["light", "pastel", "playful"], "#F27BB5"),
    "road_trip": (["bold", "dark", "vivid"], "#FF8A3D"),
    "beach": (["light", "calm", "pastel"], "#4FB8BD"),
    "sparkles": (["dark", "vivid"], "#7A4FB0"),
    "disco": (["bold", "dark", "vivid", "playful"], "#C03FB0"),
    "cozy_cabin": (["cozy", "dark", "calm"], "#B8743A"),
    "midnight_jazz": (["dark", "minimal", "calm"], "#1E2A4A"),
    "crayon_box": (["light", "playful", "vivid"], "#1F6FD1"),
    "arcade_assistant": (["dark", "bold", "minimal"], "#2E9E3A"),
    "halloween_night": (["dark", "vivid"], "#FF8C2B"),
    "pumpkin_patch": (["light", "playful", "vivid"], "#FF9A3C"),
    "winter_snow": (["light", "calm", "pastel"], "#BFD8EE"),
    "valentines_day": (["dark", "vivid"], "#E0245E"),
    "summer_splash": (["light", "vivid", "playful"], "#39B7F0"),
    "spring_bloom": (["light", "pastel", "calm"], "#9BD68C"),
    "ghost_glow": (["dark", "vivid", "playful"], "#3FCF2A"),
    "haunted_mansion": (["dark", "bold"], "#4A2470"),
    "witching_hour": (["dark", "bold"], "#E8691A"),
    "candy_corn": (["light", "playful", "vivid"], "#FFB02E"),
    "spider_web": (["dark", "minimal", "calm"], "#3A3B40"),
    "jack_o_lantern": (["dark", "cozy"], "#F07F1A"),
    "harvest": (["cozy", "dark", "calm"], "#C46A2A"),
    "autumn_leaves": (["light", "cozy"], "#D9531E"),
    "northern_lights": (["dark", "calm", "vivid"], "#2FC79A"),
    "midnight_fireworks": (["dark", "vivid", "bold"], "#2A2266"),
    "golden_countdown": (["dark", "minimal"], "#C9A24A"),
    "love_letters": (["light", "pastel", "cozy"], "#F2A7B8"),
    "cherry_blossom": (["light", "pastel", "calm"], "#F7B6CC"),
    "tropical": (["light", "vivid", "playful"], "#1FB5A3"),
    "paper": (["light", "minimal", "calm"], "#F3EDE2"),
    "graphite": (["dark", "minimal", "calm"], "#2A2C30"),
    "matcha": (["light", "pastel", "calm"], "#9DB67A"),
    "forest_floor": (["dark", "calm", "cozy"], "#3F5E2A"),
    "desert_dusk": (["dark", "vivid", "calm"], "#C76B7E"),
    "cozy_rainy_day": (["dark", "cozy", "calm"], "#3A332B"),
    "tokyo_night": (["dark", "vivid", "bold"], "#2A1F5C"),
    "constellation": (["dark", "calm", "minimal"], "#1B2440"),
    "glass": (["dark", "minimal", "vivid"], "#3D4F8F"),
    "space_cadet": (["dark", "playful", "vivid"], "#1E3A8A"),
    "earthrise": (["dark", "calm", "minimal"], "#1E3552"),
    "great_wave": (["light", "calm", "minimal"], "#1F4E8C"),
    "canyon_poster": (["bold", "vivid", "dark"], "#D2552B"),
    "solar": (["dark", "vivid", "bold"], "#FF7A1A"),
    "gismonda": (["dark", "calm", "bold"], "#8C6A24"),
}

# THE CURATED COLLECTIONS the store shows as shelves of their own, each from its first to its last
# day. Only themes offered all year: a collection never shows a theme that is out of season.
COLLECTIONS = [
    {"id": "minimal_setups", "name": "Minimal setups",
     "description": "Quiet pages with just what you need: a clean clock, soft colour and plenty of space.",
     "themes": ["paper", "graphite", "matcha", "midnight_jazz", "glass"],
     "start": "2026-10-05", "end": "2027-03-31"},
    {"id": "one_handed_favourites", "name": "One-handed favourites",
     "description": "Everything within easy reach of your thumb, from the Orbit Pad to a dock along the foot of the screen.",
     "themes": ["glass", "forest_floor", "cozy_rainy_day", "beach", "sparkles", "road_trip"],
     "start": "2026-10-05", "end": "2027-03-31"},
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
    "cozy_cabin": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), WEATHER(), w("next", "AGENDA", 0.04, 0.33, 0.92)]),
    # Minimal: one page with just a clock.
    "midnight_jazz": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="LIST",
                          widgets=[CLOCK(0.08, 1.2)]),
    # The assistant up front on a drawer home, with the calendar in the column.
    "arcade_assistant": dict(homeLayout="DRAWER", dockStyle="ROW", anchor="BOTTOM", drawerLayout="LIST",
                             drawerWidgets=[side("COMMAND", end="TOP"), side("CLOCK"), side("CALENDAR")]),
    # The seasonal themes: pages with the time and what the season is for.
    "halloween_night": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                            widgets=[CLOCK(), MEDIA_FULL(0.24)]),
    "pumpkin_patch": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                          widgets=[CLOCK(scale=1.2), WEATHER(0.04, 0.2, 0.92)]),
    "winter_snow": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                        widgets=[CLOCK(), WEATHER(), w("next", "AGENDA", 0.04, 0.33, 0.92)]),
    "valentines_day": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                           widgets=[CLOCK(scale=1.1), MEDIA_FULL(0.24)]),
    "summer_splash": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                          widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    "spring_bloom": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                         widgets=[CLOCK(), WEATHER(), w("week", "CALENDAR_WEEK", 0.04, 0.33, 0.92)]),
    # More Halloween: the music for the party, the calendar for the plans, the time alone.
    "ghost_glow": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(), MEDIA_FULL(0.24)]),
    "haunted_mansion": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="LIST",
                            widgets=[CLOCK(0.05, 1.1), w("next", "AGENDA", 0.04, 0.3, 0.92)]),
    "witching_hour": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                          widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    "candy_corn": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                       widgets=[CLOCK(scale=1.2), WEATHER(0.04, 0.2, 0.92)]),
    "spider_web": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="LIST",
                       widgets=[CLOCK(0.08, 1.2)]),
    "jack_o_lantern": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                           widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    # The other seasons.
    "harvest": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                    widgets=[CLOCK(), WEATHER(), w("next", "AGENDA", 0.04, 0.33, 0.92)]),
    "autumn_leaves": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                          widgets=[CLOCK(), WEATHER(), w("week", "CALENDAR_WEEK", 0.04, 0.33, 0.92)]),
    "northern_lights": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                            widgets=[CLOCK(scale=1.1), WEATHER(), MEDIA(0.36)]),
    "midnight_fireworks": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                               widgets=[CLOCK(), MEDIA_FULL(0.2)]),
    "golden_countdown": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="LIST",
                             widgets=[CLOCK(0.08, 1.2)]),
    "love_letters": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                         widgets=[CLOCK(), w("next", "AGENDA", 0.04, 0.2, 0.92)]),
    "cherry_blossom": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                           widgets=[CLOCK(), WEATHER(), w("week", "CALENDAR_WEEK", 0.04, 0.33, 0.92)]),
    "tropical": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                     widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    # The wallpaper-engine batch. Minimal: the time and what is next, in a plain list drawer.
    "paper": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="LIST",
                  widgets=[CLOCK(0.08, 1.2), w("next", "AGENDA", 0.04, 0.3, 0.92)]),
    "forest_floor": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                         widgets=[CLOCK(), WEATHER()]),
    "desert_dusk": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                        widgets=[CLOCK(scale=1.1), WEATHER(0.04, 0.2, 0.92)]),
    "cozy_rainy_day": dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                           widgets=[CLOCK(), WEATHER(), MEDIA(0.33)]),
    "tokyo_night": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                        widgets=[CLOCK(), MEDIA_FULL(0.2)]),
    # The showpieces: the Showcase's row of large tiles, and the Orbit Pad with pages behind it.
    "constellation": dict(homeLayout="CONSOLE", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID"),
    "glass": dict(homeLayout="ORBIT_PAD", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                  widgets=[CLOCK(0.06, 1.1)]),
    "space_cadet": dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID",
                        widgets=[CLOCK(scale=1.2), WEATHER(0.04, 0.2, 0.92)]),
    # Five more, each a different layout and dock: a free canvas with a container dock, a drawer home
    # with no dock, pages with a flat dock down the right edge, the Showcase, and the Orbit Pad.
    "earthrise": dict(homeLayout="FREE_ROAM", dockStyle="CARD", anchor="BOTTOM", drawerLayout="GRID",
                      widgets=[CLOCK(0.07, 1.2)]),
    "great_wave": dict(homeLayout="DRAWER", dockStyle="NONE", anchor="BOTTOM", drawerLayout="GRID",
                       drawerRail=True, drawerWidgets=[side("CLOCK", end="TOP"), side("COMMAND")]),
    "canyon_poster": dict(homeLayout="PAGES", dockStyle="ROW", anchor="RIGHT", drawerLayout="GRID",
                          widgets=[CLOCK(0.06, 1.1), WEATHER(0.04, 0.22, 0.78)]),
    "solar": dict(homeLayout="CONSOLE", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID"),
    "gismonda": dict(homeLayout="ORBIT_PAD", dockStyle="PAD", anchor="BOTTOM", drawerLayout="GRID",
                     widgets=[CLOCK(0.07, 1.1)]),
}

ASSISTANTS = {
    "candy": "VOICE", "crayon_box": "VOICE", "road_trip": "VOICE", "beach": "CHAT",
    "sparkles": "SPOTLIGHT", "disco": "CHAT", "cozy_cabin": "NOTEPAD", "midnight_jazz": "MINIMAL_LINE",
    "arcade_assistant": "RETRO",
    "halloween_night": "HUD", "pumpkin_patch": "VOICE", "winter_snow": "NOTEPAD",
    "valentines_day": "SPOTLIGHT", "summer_splash": "CHAT", "spring_bloom": "NOTEPAD",
    "ghost_glow": "HUD", "haunted_mansion": "SPOTLIGHT", "witching_hour": "CHAT", "candy_corn": "VOICE",
    "spider_web": "MINIMAL_LINE", "jack_o_lantern": "CHAT", "harvest": "NOTEPAD", "autumn_leaves": "CHAT",
    "northern_lights": "SPOTLIGHT", "midnight_fireworks": "HUD", "golden_countdown": "MINIMAL_LINE",
    "love_letters": "NOTEPAD", "cherry_blossom": "NOTEPAD", "tropical": "CHAT",
    "paper": "NOTEPAD", "forest_floor": "NOTEPAD", "desert_dusk": "SPOTLIGHT", "cozy_rainy_day": "NOTEPAD",
    "tokyo_night": "HUD", "constellation": "SPOTLIGHT", "glass": "MINIMAL_LINE", "space_cadet": "VOICE",
    "earthrise": "MINIMAL_LINE", "great_wave": "NOTEPAD", "canyon_poster": "CHAT", "solar": "HUD",
    "gismonda": "SPOTLIGHT",
}

# The phone-use style each layout is for. Kept consistent with the layouts above by the app's tests.
STYLES = {
    "candy": ["easy to see"], "crayon_box": ["easy to see"],
    "road_trip": ["one-handed"], "beach": ["one-handed"], "sparkles": ["one-handed"],
    "disco": ["one-handed"], "cozy_cabin": ["one-handed"], "midnight_jazz": ["minimal"],
    "arcade_assistant": ["power user"],
    "halloween_night": ["one-handed"], "pumpkin_patch": ["easy to see"], "winter_snow": ["one-handed"],
    "valentines_day": ["one-handed"], "summer_splash": ["one-handed"], "spring_bloom": ["one-handed"],
    "ghost_glow": ["one-handed"], "haunted_mansion": ["one-handed"], "witching_hour": ["one-handed"],
    "candy_corn": ["easy to see"], "spider_web": ["minimal"], "jack_o_lantern": ["one-handed"],
    "harvest": ["one-handed"], "autumn_leaves": ["one-handed"], "northern_lights": ["one-handed"],
    "midnight_fireworks": ["one-handed"], "golden_countdown": ["minimal"], "love_letters": ["one-handed"],
    "cherry_blossom": ["one-handed"], "tropical": ["one-handed"],
    "paper": ["minimal"], "forest_floor": ["one-handed"], "desert_dusk": ["one-handed"],
    "cozy_rainy_day": ["one-handed"], "tokyo_night": ["one-handed"], "constellation": ["big screen"],
    "glass": ["one-handed"], "space_cadet": ["easy to see"],
    "earthrise": ["minimal"], "great_wave": ["minimal"], "canyon_poster": ["one-handed"],
    "solar": ["big screen"], "gismonda": ["one-handed"],
}

EFFECTS = {}

LOOK_EXTRA = {
    "candy": dict(homeIconScale=1.3, homeLabels=True),
    "crayon_box": dict(homeIconScale=1.3, homeLabels=True),
    "pumpkin_patch": dict(homeIconScale=1.3, homeLabels=True),
    "candy_corn": dict(homeIconScale=1.3, homeLabels=True),
    "space_cadet": dict(homeIconScale=1.3, homeLabels=True),
}

# WHAT EACH THEME IS ABOUT, for the interests somebody picks in the app (see Interests.kt there).
# "topic:family" marks a theme for everyone that suits children too; kids themes are audience:kids.
TOPICS = {
    "candy": ["family"], "crayon_box": ["family"],
    "road_trip": ["cars", "travel"], "beach": ["beach", "travel"], "sparkles": ["space"],
    "disco": ["music"], "cozy_cabin": ["nature"], "midnight_jazz": ["music"],
    "arcade_assistant": ["gaming", "retro"],
    "halloween_night": ["halloween", "space"], "pumpkin_patch": ["halloween", "family"],
    "winter_snow": ["winter", "nature", "family"], "valentines_day": ["valentines"],
    "summer_splash": ["summer", "beach", "sports", "family"], "spring_bloom": ["spring", "nature", "family"],
    "ghost_glow": ["halloween"], "haunted_mansion": ["halloween"], "witching_hour": ["halloween", "space"],
    "candy_corn": ["halloween", "family"], "spider_web": ["halloween"], "jack_o_lantern": ["halloween", "family"],
    "harvest": ["autumn", "nature"], "autumn_leaves": ["autumn", "nature", "family"],
    "northern_lights": ["winter", "nature", "space"], "midnight_fireworks": ["new year", "music"],
    "golden_countdown": ["new year"], "love_letters": ["valentines"],
    "cherry_blossom": ["spring", "nature", "family"], "tropical": ["summer", "beach", "travel"],
    "forest_floor": ["nature"], "desert_dusk": ["nature", "travel"], "cozy_rainy_day": ["autumn"],
    "tokyo_night": ["travel", "city"], "constellation": ["space"], "glass": ["orbit pad"],
    "space_cadet": ["space", "family"],
    "earthrise": ["space"], "great_wave": ["art", "travel"], "canyon_poster": ["travel", "nature", "art"],
    "solar": ["space"], "gismonda": ["art"],
}

# THE FEATURED SECTION of the index: the theme of each week, the drops, and the seasons.
#
# Dates are calendar days, read in the phone's own time zone, so a drop goes live at local midnight
# everywhere; "until" is the last day, inclusive. Premium members get a drop from premiumFrom, and
# everybody from publicFrom. Seasons repeat every year and may run over New Year.
FEATURED = {
    "weeks": [
        {"id": "beach", "start": "2026-09-21", "end": "2026-09-27"},
        {"id": "disco", "start": "2026-09-28", "end": "2026-10-04"},
        {"id": "ghost_glow", "start": "2026-10-05", "end": "2026-10-11"},
        {"id": "midnight_jazz", "start": "2026-10-12", "end": "2026-10-18"},
        {"id": "halloween_night", "start": "2026-10-19", "end": "2026-10-25"},
        {"id": "pumpkin_patch", "start": "2026-10-26", "end": "2026-11-01"},
        {"id": "sparkles", "start": "2026-11-02", "end": "2026-11-08"},
        {"id": "road_trip", "start": "2026-11-09", "end": "2026-11-15"},
        {"id": "crayon_box", "start": "2026-11-16", "end": "2026-11-22"},
        {"id": "candy", "start": "2026-11-23", "end": "2026-11-29"},
        {"id": "cozy_cabin", "start": "2026-11-30", "end": "2026-12-06"},
        {"id": "winter_snow", "start": "2026-12-07", "end": "2026-12-13"},
    ],
    "drops": [
        {"id": "spooky_week", "name": "Spooky Week",
         "description": "A starry Halloween night, glowing ghosts, a witching-hour moon and a friendly pumpkin patch.",
         "themes": ["halloween_night", "ghost_glow", "witching_hour", "pumpkin_patch"],
         "premiumFrom": "2026-10-23", "publicFrom": "2026-10-26", "until": "2026-11-01"},
        {"id": "winter_pack", "name": "Winter Pack",
         "description": "Fresh snow, frosted blue and the northern lights for the cold months.",
         "themes": ["winter_snow", "northern_lights"],
         "premiumFrom": "2026-11-28", "publicFrom": "2026-12-01", "until": "2026-12-13"},
    ],
    # Each season's "from" and "until" are its first and last days, every year. A theme that names a
    # season (theme(..., season=)) is offered only then; Premium members with early access get it
    # earlyDays sooner, and the store says it is coming teaseDays before it opens.
    "seasonal": [
        {"id": "halloween", "name": "Halloween", "from": "10-01", "until": "11-01", "teaseDays": 5, "earlyDays": 3,
         "themes": ["halloween_night", "ghost_glow", "haunted_mansion", "witching_hour", "jack_o_lantern",
                    "spider_web", "pumpkin_patch", "candy_corn"]},
        {"id": "autumn", "name": "Autumn", "from": "11-01", "until": "11-30", "teaseDays": 5, "earlyDays": 3,
         "themes": ["harvest", "autumn_leaves", "cozy_cabin"]},
        {"id": "winter", "name": "Winter holidays", "from": "12-01", "until": "01-06", "teaseDays": 5, "earlyDays": 3,
         "themes": ["winter_snow", "northern_lights"]},
        {"id": "new_year", "name": "New Year", "from": "12-26", "until": "01-07", "teaseDays": 5, "earlyDays": 3,
         "themes": ["midnight_fireworks", "golden_countdown", "sparkles", "disco"]},
        {"id": "valentines", "name": "Valentine's", "from": "02-01", "until": "02-15", "teaseDays": 5, "earlyDays": 3,
         "themes": ["valentines_day", "love_letters"]},
        {"id": "spring", "name": "Spring", "from": "03-20", "until": "05-31", "teaseDays": 5, "earlyDays": 3,
         "themes": ["spring_bloom", "cherry_blossom"]},
        {"id": "summer", "name": "Summer", "from": "06-01", "until": "08-31", "teaseDays": 5, "earlyDays": 3,
         "themes": ["summer_splash", "tropical", "beach"]},
    ],
}

# THE RULES A CATALOG THEME IS HELD TO, as the app reads it: the only effects it can draw, and the
# faces in its font library. A name not on these lists would make the theme unreadable in the app.
EFFECTS_ALLOWED = {"", "sparkles", "disco-lights", "floating-bubbles", "twinkle-stars",
                   "floating-ghosts", "bats", "falling-leaves", "fireworks"}
# The effects that answer a tap (the app's ThemeEffect.tap); "tap" on any other does nothing.
TAP_EFFECTS = {"sparkles", "twinkle-stars", "floating-ghosts", "bats", "falling-leaves", "fireworks"}
LIBRARY_FONTS = {
    "inter", "manrope", "poppins", "montserrat", "dm_sans", "outfit", "space_grotesk",
    "orbitron", "rajdhani", "share_tech_mono", "jetbrains_mono", "vt323", "exo_2", "audiowide",
    "oxanium", "space_mono", "cormorant", "playfair_display", "cinzel", "lora", "marcellus",
    "quicksand", "comfortaa", "nunito", "fredoka", "baloo_2", "varela_round", "caveat",
    "permanent_marker", "patrick_hand", "kalam", "indie_flower", "atkinson_hyperlegible",
    "ibm_plex_sans", "lexend", "source_sans_3",
}


def month_day(text, where):
    """A season's "MM-DD" as (month, day), or a failure naming [where]. February 29 is allowed, as
    the app reads it as the 28th in a year without one."""
    try:
        parsed = datetime.date.fromisoformat("2024-" + text)
    except (TypeError, ValueError):
        raise AssertionError("%s: %r is not a month and day (MM-DD)" % (where, text))
    return parsed.month, parsed.day


def day(text, where):
    try:
        return datetime.date.fromisoformat(text)
    except (TypeError, ValueError):
        raise AssertionError("%s: %r is not a date (YYYY-MM-DD)" % (where, text))


def season_days(season, year):
    """The first and last day of [season]'s occurrence that starts in [year]."""
    fm, fd = month_day(season["from"], season["id"])
    um, ud = month_day(season["until"], season["id"])
    wraps = (um, ud) < (fm, fd)

    def on(y, m, d):
        return datetime.date(y, m, 28 if (m, d) == (2, 29) and not calendar.isleap(y) else d)
    return on(year, fm, fd), on(year + 1 if wraps else year, um, ud)


def in_season(season, first, last, early=0):
    """Whether the days [first] to [last] all fall in one occurrence of [season], opened [early]
    days sooner."""
    for year in (first.year - 1, first.year):
        start, end = season_days(season, year)
        if start - datetime.timedelta(days=early) <= first and last <= end:
            return True
    return False


def check_featured(entries):
    """The featured section reads as the app reads it: every theme it names is in the catalog, every
    date parses, every season a theme names exists, and nothing puts a seasonal theme on show
    outside its season."""
    ids = {e["id"] for e in entries}
    seasons = {s["id"]: s for s in FEATURED["seasonal"]}
    theme_season = {e["id"]: e.get("season") for e in entries}
    named = [w["id"] for w in FEATURED["weeks"]]
    for group in FEATURED["drops"] + FEATURED["seasonal"]:
        named += group["themes"]
    missing = sorted(set(named) - ids)
    assert not missing, missing
    assert len(seasons) == len(FEATURED["seasonal"]), "two seasons share an id"
    for season in FEATURED["seasonal"]:
        month_day(season["from"], season["id"])
        month_day(season["until"], season["id"])
        for key in ("teaseDays", "earlyDays"):
            assert isinstance(season.get(key, 0), int) and 0 <= season.get(key, 0) <= 30, (season["id"], key)
        for tid in season["themes"]:
            own = theme_season[tid]
            assert own in (None, season["id"]), "%s is listed under %s but is seasonal in %s" % (tid, season["id"], own)
        mine = [tid for tid, own in theme_season.items() if own == season["id"]]
        assert len(mine) >= 2, "%s has fewer than two seasonal themes" % season["id"]
    for tid, own in theme_season.items():
        assert own is None or own in seasons, "%s names the season %r, which is not in FEATURED" % (tid, own)
    for week in FEATURED["weeks"]:
        start, end = day(week["start"], week["id"]), day(week["end"], week["id"])
        assert start <= end, week
        own = theme_season[week["id"]]
        assert own is None or in_season(seasons[own], start, end), "%s is featured outside its season" % week["id"]
    for drop in FEATURED["drops"]:
        early = day(drop["premiumFrom"], drop["id"])
        public = day(drop["publicFrom"], drop["id"])
        until = day(drop["until"], drop["id"])
        assert early <= public <= until, drop["id"]
        for tid in drop["themes"]:
            own = theme_season[tid]
            if own is None:
                continue
            season = seasons[own]
            assert in_season(season, public, until), "%s drops %s outside its season" % (drop["id"], tid)
            assert in_season(season, early, until, season.get("earlyDays", 0)), \
                "%s drops %s early, before Premium's early access to its season" % (drop["id"], tid)


def check_collections(entries):
    """Every collection has an id the app accepts, a name and a description, dates that parse in
    order, and two or more themes, all in the catalog and all offered all year."""
    by_id = {e["id"]: e for e in entries}
    ids = [c["id"] for c in COLLECTIONS]
    assert len(ids) == len(set(ids)), "two collections share an id"
    for c in COLLECTIONS:
        assert set(c) == {"id", "name", "description", "themes", "start", "end"}, c["id"]
        assert c["id"].replace("_", "").isalnum() and c["id"] == c["id"].lower() and len(c["id"]) <= 40, c["id"]
        assert c["name"] and len(c["name"]) <= 40 and c["description"] and len(c["description"]) <= 280, c["id"]
        assert day(c["start"], c["id"]) <= day(c["end"], c["id"]), c["id"]
        assert len(c["themes"]) >= 2 and len(set(c["themes"])) == len(c["themes"]), c["id"]
        for tid in c["themes"]:
            assert tid in by_id, "%s names %s, which is not in the catalog" % (c["id"], tid)
            assert not by_id[tid]["season"], "%s names %s, which is seasonal" % (c["id"], tid)


def check_credits(entry):
    """A theme's credits are complete, and a wallpaper made from a photograph is credited to an
    approved source under a CC0 or public-domain licence. Refuses the theme otherwise."""
    tid = entry["id"]
    for credit in entry["credits"]:
        assert set(credit) == {"title", "author", "source", "license", "url"}, (tid, credit)
        assert all(isinstance(v, str) and v.strip() for v in credit.values()), (tid, credit)
        assert credit["url"].startswith("https://"), (tid, credit["url"])
    spec = (entry["wallpaper"] or {}).get("render") or {}
    if "photo" in spec:
        photo = PHOTOS.get(spec["photo"]["file"])
        assert photo, "%s uses a photo with no credit recorded in PHOTOS" % tid
        assert photo["license"] in FREE_LICENSES, \
            "%s uses a photo licensed %r; only CC0 or public domain may be used" % (tid, photo["license"])
        assert photo["source"] in PHOTO_SOURCES, "%s uses a photo from %r, not an approved source" % (tid, photo["source"])
        assert photo.get("retrieved"), "%s: the photo's licence check has no date" % tid
        assert entry["credits"], "%s is photo-based but carries no credit" % tid


def check_theme(entry):
    """One theme against the app's rules: a whitelisted effect, and only on a Premium theme, a font
    in the library, and a season written as an id."""
    tid = entry["id"]
    assert entry["kind"] in ("full", "accent"), (tid, entry["kind"])
    if entry["kind"] == "accent":
        # The colours and the font, and nothing that would move or repaint the home screen.
        assert not entry["wallpaper"] and not entry["layout"] and not entry["effect"], tid
        assert set(entry["look"]) <= {"font"}, (tid, "an accent theme's look is its font alone")
    moods, swatch = entry["mood"], entry["swatch"]
    assert moods and set(moods) <= MOOD_WORDS and len(set(moods)) == len(moods), (tid, moods)
    assert len(swatch) == 7 and swatch[0] == "#" and all(c in "0123456789ABCDEF" for c in swatch[1:]), (tid, swatch)
    check_credits(entry)
    assert entry["effect"] in EFFECTS_ALLOWED, (tid, entry["effect"])
    if entry["effect"]:
        assert entry["premium"], "%s has an effect, which is part of Premium" % tid
    if entry["tap"]:
        assert entry["effect"] in TAP_EFFECTS, "%s asks for a tap reaction its effect does not have" % tid
    font = entry["look"].get("font")
    assert font in LIBRARY_FONTS, (tid, font)
    assert len(entry["name"]) <= 40 and len(entry["description"]) <= 280, tid
    assert any(t.startswith("vibe:") for t in entry["tags"]), "%s has no vibe" % tid


def finish(entry):
    tid = entry["id"]
    entry["mood"], entry["swatch"] = MOODS[tid]
    entry["credits"] = credits_of(entry)
    if entry["kind"] == "accent":
        # Only colours and a font: no layout, assistant look or phone style of its own.
        entry["tags"] = [t for t in entry["tags"] if not t.startswith("style:")]
        entry["tags"] += ["topic:" + t for t in TOPICS.get(tid, [])]
        return entry
    entry["layout"] = dict(LAYOUTS[tid], **{k: v for k, v in (entry["layout"] or {}).items() if k not in LAYOUTS[tid]})
    entry["assistant"] = {"look": ASSISTANTS[tid]}
    entry["tags"] = [t for t in entry["tags"] if not t.startswith("style:")] + ["style:" + s for s in STYLES[tid]]
    entry["tags"] += ["topic:" + t for t in TOPICS.get(tid, [])]
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
    image = (entry["wallpaper"] or {}).get("image")
    painted = os.path.join(os.path.dirname(path), image) if image else None
    colors = paper["colors"] if paper else [entry["colors"]["surface"], entry["colors"]["drawer"],
                                            entry["colors"]["accent"], entry["colors"]["accentAlt"],
                                            entry["colors"]["elevated"]]
    if painted and os.path.exists(painted):
        # The wallpaper itself, cut to the preview's shape.
        with Image.open(painted) as wall:
            img = ImageOps.fit(wall.convert("RGBA"), (w, h), Image.LANCZOS)
    else:
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
        # The store's mood and colour filters, and the credit for a photograph in the wallpaper.
        # (Whether it is a full theme or an accent is said in the index only: "kind" here is the
        # file's own kind, "orbital-theme", which the app checks.)
        "mood": entry["mood"], "swatch": entry["swatch"], "credits": entry["credits"],
    }
    if entry["wallpaper"]:
        out["wallpaper"] = {k: v for k, v in entry["wallpaper"].items() if k not in ("paint", "render")}
    if entry["layout"]:
        out["layout"] = entry["layout"]
    if entry["assistant"]:
        out["assistant"] = entry["assistant"]
    if entry["effect"]:
        out["effect"] = entry["effect"]
        if entry["tap"]:
            out["tap"] = True
    if entry["season"]:
        out["season"] = entry["season"]
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


# THE PAINTED WALLPAPERS, for pictures no drawn style makes: soft shapes on a dark sky, blurred and
# saved small. Seeded by the theme, so the same picture comes out every run.

# Painted at two-thirds of the phone's size (the shapes are soft, so nothing is lost), then scaled up
# and finished by the wallpaper engine at its full size.
WALL_W, WALL_H = 720, 1600


def sky(top, bottom):
    img = Image.new("RGB", (WALL_W, WALL_H))
    d = ImageDraw.Draw(img)
    for y in range(WALL_H):
        t = y / (WALL_H - 1)
        d.line([(0, y), (WALL_W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img.convert("RGBA")


def glow_layer(draw_fn, blur):
    layer = Image.new("RGBA", (WALL_W, WALL_H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    return layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer


def paint_ghosts(entry, rnd):
    green, violet = hex_rgb(entry["colors"]["accent"]), hex_rgb(entry["colors"]["accentAlt"])
    img = sky((10, 16, 12), (2, 3, 2))

    def ghost(d, cx, cy, r, lean, colour, alpha, eyes):
        # A sheet: a round head, sides that flare and lean as it drifts, and a hem of soft points.
        pts = [(cx + math.cos(a) * r, cy - math.sin(a) * r) for a in [math.pi * k / 16 for k in range(17)]]
        hem_y = cy + r * 2.1
        pts.append((cx - r * 1.15 + lean, hem_y))
        for k in range(1, 8):
            x = cx - r * 1.15 + lean + k * (r * 2.3 / 8)
            pts.append((x, hem_y - (r * 0.28 if k % 2 else 0)))
        pts.append((cx + r * 1.15 + lean, hem_y))
        d.polygon(pts, fill=colour + (alpha,))
        if eyes:
            eye = r * 0.13
            for ex in (cx - r * 0.33, cx + r * 0.33):
                d.ellipse([ex - eye, cy - eye * 1.5, ex + eye, cy + eye * 1.5], fill=(6, 10, 7, 170))

    ghosts = []
    while len(ghosts) < 7:
        x, y, r = rnd.randint(90, WALL_W - 90), rnd.randint(160, WALL_H - 320), rnd.randint(45, 85)
        if all(abs(x - gx) > 170 or abs(y - gy) > 260 for gx, gy, _, _, _ in ghosts):
            ghosts.append((x, y, r, rnd.randint(-30, 30), len(ghosts) % 3 != 2))
    for blur, alpha, eyes in ((46, 70, False), (16, 80, False), (4, 70, True)):
        img = Image.alpha_composite(img, glow_layer(
            lambda d: [ghost(d, x, y, r, lean, green if g else violet, alpha, eyes) for x, y, r, lean, g in ghosts], blur))
    return img


def paint_moon(entry, rnd):
    ember = hex_rgb(entry["colors"]["accent"])
    img = sky((22, 12, 6), (3, 2, 1))
    cx, cy, r = WALL_W * 0.62, WALL_H * 0.24, 170
    img = Image.alpha_composite(img, glow_layer(lambda d: d.ellipse([cx - r * 1.8, cy - r * 1.8, cx + r * 1.8, cy + r * 1.8], fill=ember + (70,)), 80))
    img = Image.alpha_composite(img, glow_layer(lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 150, 255)), 2))

    def craters(d):
        for _ in range(7):
            a, dist, s = rnd.random() * 6.28, rnd.random() * r * 0.7, rnd.randint(12, 34)
            x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist
            d.ellipse([x - s, y - s, x + s, y + s], fill=(225, 170, 105, 90))
    img = Image.alpha_composite(img, glow_layer(craters, 4))

    def hills(d):
        d.polygon([(0, WALL_H * 0.82)] + [(x, WALL_H * 0.8 - 40 * math.sin(x / 90.0) - 25 * math.sin(x / 37.0))
                                          for x in range(0, WALL_W + 1, 12)] + [(WALL_W, WALL_H), (0, WALL_H)],
                  fill=(8, 5, 3, 255))
    img = Image.alpha_composite(img, glow_layer(hills, 1))

    def stars(d):
        for _ in range(60):
            x, y, s = rnd.randint(0, WALL_W), rnd.randint(0, int(WALL_H * 0.7)), rnd.choice((1, 1, 2))
            d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 230, 200, rnd.randint(90, 200)))
    return Image.alpha_composite(img, glow_layer(stars, 0))


def paint_webs(entry, rnd):
    silver = hex_rgb(entry["colors"]["accent"])
    img = sky((20, 20, 23), (5, 5, 6))

    def web(d, cx, cy, reach, spokes, rings, alpha):
        angles = [2 * math.pi * k / spokes + rnd.uniform(-0.08, 0.08) for k in range(spokes)]
        for a in angles:
            d.line([(cx, cy), (cx + math.cos(a) * reach, cy + math.sin(a) * reach)], fill=silver + (alpha,), width=2)
        for ring in range(1, rings + 1):
            rr = reach * ring / rings
            pts = [(cx + math.cos(a) * rr * (0.94 + 0.06 * math.sin(ring + a * 3)),
                    cy + math.sin(a) * rr * (0.94 + 0.06 * math.sin(ring + a * 3))) for a in angles]
            for k in range(spokes):
                x0, y0 = pts[k]
                x1, y1 = pts[(k + 1) % spokes]
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                sag = 0.9
                d.line([(x0, y0), (cx + (mx - cx) * sag, cy + (my - cy) * sag), (x1, y1)], fill=silver + (alpha,), width=2)

    img = Image.alpha_composite(img, glow_layer(lambda d: web(d, 0, 0, 620, 12, 9, 120), 1))
    img = Image.alpha_composite(img, glow_layer(lambda d: web(d, WALL_W, WALL_H * 0.72, 480, 12, 7, 80), 1))
    img = Image.alpha_composite(img, glow_layer(lambda d: d.ellipse([WALL_W * 0.2, WALL_H * 0.35, WALL_W * 0.9, WALL_H * 0.7], fill=silver + (18,)), 120))
    return img


PAINTERS = {"ghosts": paint_ghosts, "moon": paint_moon, "webs": paint_webs}


# How readable the screen's furniture must stay over a wallpaper made here, as contrast ratios
# against the theme's ink: the dock (on average, and against its lightest or darkest few percent),
# and the clock, which is large text, against its worst few percent.
DOCK_AVERAGE, DOCK_WORST, CLOCK_WORST = 4.5, 3.0, 3.0


def make_wallpaper(entry, folder):
    """Makes [entry]'s wallpaper.webp in [folder] with the wallpaper engine: painted here first, or a
    mesh gradient, or a photo wash. Checks the dock and the clock read clearly over it. A photo wash
    whose original is not in SOURCES keeps the committed picture. Returns its path and size."""
    paper = entry["wallpaper"]
    path = os.path.join(folder, paper["image"])
    spec = paper.get("render") or {}
    if "photo" in spec and not os.path.exists(os.path.join(SOURCES, spec["photo"]["file"])):
        assert os.path.exists(path), "%s: the photo %s is not in %s and there is no wallpaper to keep" % (
            entry["id"], spec["photo"]["file"], SOURCES)
        print(entry["id"], "keeps its wallpaper; the original photo is not in", SOURCES)
        img = Image.open(path).convert("RGB")
    else:
        base = None
        if paper.get("paint"):
            base = PAINTERS[paper["paint"]](entry, random.Random(entry["id"]))
        img = engine.render(spec, entry["id"], SOURCES, base_image=base)
        engine.save_webp(img, path)
    read = engine.readability(img, entry["colors"]["ink"])
    assert read["dock"][0] >= DOCK_AVERAGE and read["dock"][1] >= DOCK_WORST, (entry["id"], "dock", read["dock"])
    assert read["clock"][1] >= CLOCK_WORST, (entry["id"], "clock", read["clock"])
    return path, os.path.getsize(path)


SHARE_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{name} &mdash; a theme for Orbital Launcher</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#07090e">
<link rel="canonical" href="https://orbitallauncher.com/t/{id}">
<meta property="og:type" content="website">
<meta property="og:title" content="{name}, a theme for Orbital Launcher">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://orbitallauncher.com/t/{id}">
<meta property="og:image" content="https://orbitallauncher.com/themes/{id}/preview.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=7">
<script src="/assets/theme.js"></script>
<style>
  .share-theme {{ display: grid; gap: 2rem; align-items: center; grid-template-columns: minmax(0, 240px) minmax(0, 1fr); margin-top: 2rem; }}
  .share-theme img {{ width: 100%; height: auto; border-radius: 28px; border: 1px solid var(--card-edge); }}
  .share-tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 1rem 0 1.5rem; padding: 0; list-style: none; }}
  .share-tags li {{ font-size: 0.85rem; padding: 0.3rem 0.7rem; border-radius: 999px; border: 1px solid var(--card-edge); }}
  .share-actions {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .season-note {{ margin: -0.5rem 0 1.25rem; font-size: 0.95rem; color: var(--accent); }}
  .credit {{ margin: -0.5rem 0 1.25rem; font-size: 0.85rem; opacity: 0.75; }}
  .credit a {{ color: inherit; }}
  @media (max-width: 640px) {{ .share-theme {{ grid-template-columns: 1fr; }} .share-theme img {{ max-width: 220px; }} }}
</style>
</head>
<body data-share="theme">
<header class="top">
  <a class="mark" href="/"><span>Orbital</span></a>
  <nav aria-label="Site"><a href="/themes.html">Themes</a><a href="/features.html">Features</a></nav>
</header>
<main class="wrap">
  <div class="share-theme">
    <img src="/themes/{id}/preview.png" width="240" height="480" alt="A preview of the {name} theme">
    <div>
      <p class="eyebrow">A theme for Orbital Launcher{premium}</p>
      <h1>{name}</h1>
      <p class="lede">{description}</p>
      <ul class="share-tags">{tags}</ul>{season}{credit}
      <div class="share-actions">
        <a class="btn" data-open-app href="https://play.google.com/store/apps/details?id=com.alid0n.orbital">Get it in Orbital</a>
        <a class="btn ghost" data-play href="https://play.google.com/store/apps/details?id=com.alid0n.orbital">Get Orbital on Google Play</a>
      </div>
    </div>
  </div>
</main>
<footer class="foot">
  <p><a href="/">Home</a> &middot; <a href="/themes.html">All themes</a> &middot; <a href="/privacy.html">Privacy policy</a></p>
</footer>
<script src="/assets/share.js"></script>{season_script}
</body>
</html>
"""


def share_page(entry):
    """The page a theme link opens where Orbital is not installed: orbitallauncher.com/t/<id>."""
    esc = html.escape
    words = []
    for t in entry["tags"]:
        word = t.split(":", 1)[1]
        if not t.startswith("audience:") and word not in words:
            words.append(word)
    tags = "".join("<li>" + esc(word) + "</li>" for word in words)
    season = ""
    season_script = ""
    if entry["season"]:
        # Said in the page itself for readers without scripts; season.js says whether it is on now,
        # and puts the Get button away outside it.
        s = next(s for s in FEATURED["seasonal"] if s["id"] == entry["season"])
        span = "%s–%s" % (short_day(s["from"]), short_day(s["until"]))
        season = ('\n      <p class="season-note" data-season-from="%s" data-season-until="%s">'
                  'A seasonal theme. Available %s.</p>' % (esc(s["from"]), esc(s["until"]), esc(span)))
        season_script = '\n<script src="/assets/season.js"></script>'
    credit = ""
    if entry["credits"]:
        # The photograph in the wallpaper: its title, who made it, where it is from and its licence.
        credit = '\n      <p class="credit">Wallpaper photo: ' + "; ".join(
            '<a href="%s" rel="noopener">%s</a> by %s, %s (%s)' % (
                esc(c["url"]), esc(c["title"]), esc(c["author"]), esc(c["source"]), esc(c["license"]))
            for c in entry["credits"]) + ".</p>"
    return SHARE_PAGE.format(
        id=esc(entry["id"]),
        name=esc(entry["name"]),
        description=esc(entry["description"]),
        premium=" &middot; Orbital Premium" if entry["premium"] else "",
        tags=tags,
        season=season,
        credit=credit,
        season_script=season_script,
    )


def short_day(md):
    """"10-01" as "Oct 1"."""
    month, dd = month_day(md, md)
    return "%s %d" % (calendar.month_abbr[month], dd)


def write_share_pages(entries):
    """One folder per theme under t/, so /t/<id> serves its page."""
    root = os.path.join(SITE, "t")
    for entry in entries:
        folder = os.path.join(root, entry["id"])
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(share_page(entry))


def main():
    os.makedirs(ROOT, exist_ok=True)
    finished = []
    index = []
    for entry in map(finish, THEMES):
        check_theme(entry)
        finished.append(entry)
    ids = [e["id"] for e in finished]
    assert len(ids) == len(set(ids)), "two themes share an id"
    check_featured(finished)
    check_collections(finished)
    only = set(os.environ.get("ORBITAL_ONLY", "").split(",")) - {""}
    for entry in finished:
        folder = os.path.join(ROOT, entry["id"])
        os.makedirs(folder, exist_ok=True)
        data = theme_json(entry).encode("utf-8")
        with open(os.path.join(folder, "theme.json"), "wb") as f:
            f.write(data)
        if (entry["wallpaper"] or {}).get("image") and (not only or entry["id"] in only):
            print(entry["id"], make_wallpaper(entry, folder)[1], "bytes wallpaper")
        png = os.path.join(folder, "preview.png")
        preview(entry, png)
        size = os.path.getsize(png)
        assert size < 300_000, (entry["id"], size)
        item = {
            "id": entry["id"], "name": entry["name"], "description": entry["description"],
            "version": 1, "tags": entry["tags"], "thumbnail": entry["id"] + "/preview.png",
            "file": entry["id"] + "/theme.json", "premium": entry["premium"], "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "base": entry["base"],
            "colors": entry["colors"],
            "kind": entry["kind"], "mood": entry["mood"], "swatch": entry["swatch"], "credits": entry["credits"],
        }
        if entry["season"]:
            item["season"] = entry["season"]
        index.append(item)
        print(entry["id"], len(data), "bytes json,", size, "bytes png")
    with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"kind": "orbital-theme-index", "format": 1, "themes": index, "featured": FEATURED,
                   "collections": COLLECTIONS},
                  f, indent=2, ensure_ascii=False)
        f.write("\n")
    check_written()
    write_share_pages(finished)


def check_written():
    """Reads back what was written, as the app will: every index entry's file is there, its size and
    SHA-256 match, and every season a theme names is in the index's own featured section."""
    with open(os.path.join(ROOT, "index.json"), encoding="utf-8") as f:
        text = f.read()
    # The app reads no index longer than this (ThemeCatalogFormat.MAX_CHARS).
    assert len(text) <= 262_144, ("index.json", len(text))
    index = json.loads(text)
    seasons = {s["id"] for s in index["featured"]["seasonal"]}
    listed = {item["id"] for item in index["themes"]}
    for c in index["collections"]:
        assert set(c["themes"]) <= listed, c["id"]
    for item in index["themes"]:
        with open(os.path.join(ROOT, item["file"]), "rb") as f:
            data = f.read()
        assert len(data) == item["size"], (item["id"], "size")
        assert hashlib.sha256(data).hexdigest() == item["sha256"], (item["id"], "sha256")
        theme_file = json.loads(data.decode("utf-8"))
        assert theme_file.get("season") == item.get("season"), (item["id"], "season")
        assert item.get("season") is None or item["season"] in seasons, (item["id"], item["season"])
        assert theme_file["kind"] == "orbital-theme", (item["id"], "kind")
        for key in ("mood", "swatch", "credits"):
            assert theme_file[key] == item[key], (item["id"], key)
        if item["kind"] == "accent":
            assert "layout" not in theme_file and "wallpaper" not in theme_file, (item["id"], "accent")
        image = (theme_file.get("wallpaper") or {}).get("image")
        if image:
            picture_path = os.path.join(ROOT, item["id"], image)
            assert os.path.getsize(picture_path) <= engine.MAX_BYTES, (item["id"], image)
            with Image.open(picture_path) as picture:
                # Within what the app will decode (ThemeImages.MAX_SIDE).
                assert max(picture.size) <= 4096, (item["id"], picture.size)


if __name__ == "__main__":
    main()

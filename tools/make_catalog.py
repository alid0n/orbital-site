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

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SITE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\addis\Documents\tests\orbital-site"
ROOT = os.path.join(SITE, "themes")
APP_VERSION = 10  # the first version with the catalog


def theme(id, name, description, tags, colors, wallpaper, look, premium=False, layout=None,
          effect="", assistant=None, base="ORBITAL", season=None, tap=False):
    """season: the id of a season in FEATURED["seasonal"]; the theme is then offered only while that
    season is on, every year (the app's SeasonalThemes). tap: the effect answers a tap on empty
    home-screen space with a small burst (the app's TapReaction), where the effect has one."""
    return dict(id=id, name=name, description=description, tags=tags, colors=colors,
                wallpaper=wallpaper, look=look, premium=premium, layout=layout, effect=effect,
                assistant=assistant, base=base, season=season, tap=tap)


def pal(accent, alt, ink, dim, drawer, surface, elevated, veil="#33000000", light=False):
    return dict(accent=accent, accentAlt=alt, ink=ink, dim=dim, drawer=drawer, surface=surface,
                elevated=elevated, veil=veil, light=light)


def drawn(style, colors, light=False):
    return {"drawn": {"style": style, "colors": colors, "light": light}}


def picture(kind):
    """A wallpaper painted here, by one of the painters in PAINTERS, into the theme's folder as
    wallpaper.png, under 300 KB."""
    return {"image": "wallpaper.png", "paint": kind}


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
          picture("ghosts"),
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
          "Midnight black and ember orange under a great full moon.",
          ["audience:general", "vibe:spooky", "vibe:dark", "color:orange", "color:black"],
          pal("#FF7A1A", "#FFB45C", "#FFF1E3", "#B39A86", "#060403", "#0C0806", "#1B120C", "#55000000"),
          picture("moon"),
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
          picture("webs"),
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
          drawn("AURORA", ["#06142A", "#02050C", "#3DF5B0", "#6C8CFF", "#B46CFF"]),
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
}

ASSISTANTS = {
    "groove_70s": "NOTEPAD", "neon_80s": "HUD", "bright_90s": "CHAT", "y2k_chrome": "SPOTLIGHT",
    "candy": "VOICE", "crayon_box": "VOICE", "road_trip": "VOICE", "beach": "CHAT",
    "sparkles": "SPOTLIGHT", "disco": "CHAT", "gaming_90s": "RETRO", "gaming_future": "HUD",
    "gaming_green": "COMMAND_PROMPT", "cozy_cabin": "NOTEPAD", "midnight_jazz": "MINIMAL_LINE",
    "arcade_assistant": "RETRO",
    "halloween_night": "HUD", "pumpkin_patch": "VOICE", "winter_snow": "NOTEPAD",
    "valentines_day": "SPOTLIGHT", "summer_splash": "CHAT", "spring_bloom": "NOTEPAD",
    "ghost_glow": "HUD", "haunted_mansion": "SPOTLIGHT", "witching_hour": "CHAT", "candy_corn": "VOICE",
    "spider_web": "MINIMAL_LINE", "jack_o_lantern": "CHAT", "harvest": "NOTEPAD", "autumn_leaves": "CHAT",
    "northern_lights": "SPOTLIGHT", "midnight_fireworks": "HUD", "golden_countdown": "MINIMAL_LINE",
    "love_letters": "NOTEPAD", "cherry_blossom": "NOTEPAD", "tropical": "CHAT",
}

# The phone-use style each layout is for. Kept consistent with the layouts above by the app's tests.
STYLES = {
    "groove_70s": ["one-handed"], "neon_80s": ["one-handed"], "bright_90s": ["one-handed"],
    "y2k_chrome": ["big screen"], "candy": ["easy to see"], "crayon_box": ["easy to see"],
    "road_trip": ["one-handed"], "beach": ["one-handed"], "sparkles": ["one-handed"],
    "disco": ["one-handed"], "gaming_90s": ["one-handed"], "gaming_future": ["one-handed"],
    "gaming_green": ["power user"], "cozy_cabin": ["one-handed"], "midnight_jazz": ["minimal"],
    "arcade_assistant": ["power user"],
    "halloween_night": ["one-handed"], "pumpkin_patch": ["easy to see"], "winter_snow": ["one-handed"],
    "valentines_day": ["one-handed"], "summer_splash": ["one-handed"], "spring_bloom": ["one-handed"],
    "ghost_glow": ["one-handed"], "haunted_mansion": ["one-handed"], "witching_hour": ["one-handed"],
    "candy_corn": ["easy to see"], "spider_web": ["minimal"], "jack_o_lantern": ["one-handed"],
    "harvest": ["one-handed"], "autumn_leaves": ["one-handed"], "northern_lights": ["one-handed"],
    "midnight_fireworks": ["one-handed"], "golden_countdown": ["minimal"], "love_letters": ["one-handed"],
    "cherry_blossom": ["one-handed"], "tropical": ["one-handed"],
}

EFFECTS = {"neon_80s": "sparkles"}

LOOK_EXTRA = {
    "candy": dict(homeIconScale=1.3, homeLabels=True),
    "crayon_box": dict(homeIconScale=1.3, homeLabels=True),
    "pumpkin_patch": dict(homeIconScale=1.3, homeLabels=True),
    "candy_corn": dict(homeIconScale=1.3, homeLabels=True),
}

# WHAT EACH THEME IS ABOUT, for the interests somebody picks in the app (see Interests.kt there).
# "topic:family" marks a theme for everyone that suits children too; kids themes are audience:kids.
TOPICS = {
    "groove_70s": ["music", "retro"], "neon_80s": ["music", "retro"], "bright_90s": ["retro"],
    "y2k_chrome": ["retro"], "candy": ["family"], "crayon_box": ["family"],
    "road_trip": ["cars", "travel"], "beach": ["beach", "travel"], "sparkles": ["space"],
    "disco": ["music"], "gaming_90s": ["gaming", "retro"], "gaming_future": ["gaming", "space"],
    "gaming_green": ["gaming"], "cozy_cabin": ["nature"], "midnight_jazz": ["music"],
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
}

# THE FEATURED SECTION of the index: the theme of each week, the drops, and the seasons.
#
# Dates are calendar days, read in the phone's own time zone, so a drop goes live at local midnight
# everywhere; "until" is the last day, inclusive. Premium members get a drop from premiumFrom, and
# everybody from publicFrom. Seasons repeat every year and may run over New Year.
FEATURED = {
    "weeks": [
        {"id": "groove_70s", "start": "2026-09-21", "end": "2026-09-27"},
        {"id": "neon_80s", "start": "2026-09-28", "end": "2026-10-04"},
        {"id": "ghost_glow", "start": "2026-10-05", "end": "2026-10-11"},
        {"id": "midnight_jazz", "start": "2026-10-12", "end": "2026-10-18"},
        {"id": "halloween_night", "start": "2026-10-19", "end": "2026-10-25"},
        {"id": "pumpkin_patch", "start": "2026-10-26", "end": "2026-11-01"},
        {"id": "sparkles", "start": "2026-11-02", "end": "2026-11-08"},
        {"id": "road_trip", "start": "2026-11-09", "end": "2026-11-15"},
        {"id": "gaming_future", "start": "2026-11-16", "end": "2026-11-22"},
        {"id": "y2k_chrome", "start": "2026-11-23", "end": "2026-11-29"},
        {"id": "cozy_cabin", "start": "2026-11-30", "end": "2026-12-06"},
        {"id": "winter_snow", "start": "2026-12-07", "end": "2026-12-13"},
    ],
    "drops": [
        {"id": "retro_week", "name": "Retro Week",
         "description": "Four decades of style: 70s warmth, 80s neon, 90s colour and a classic games console.",
         "themes": ["groove_70s", "neon_80s", "bright_90s", "gaming_90s"],
         "premiumFrom": "2026-09-24", "publicFrom": "2026-09-27", "until": "2026-10-11"},
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


def check_theme(entry):
    """One theme against the app's rules: a whitelisted effect, and only on a Premium theme, a font
    in the library, and a season written as an id."""
    tid = entry["id"]
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
    painted = os.path.join(os.path.dirname(path), "wallpaper.png")
    colors = paper["colors"] if paper else [entry["colors"]["surface"], entry["colors"]["drawer"],
                                            entry["colors"]["accent"], entry["colors"]["accentAlt"],
                                            entry["colors"]["elevated"]]
    if (entry["wallpaper"] or {}).get("paint") and os.path.exists(painted):
        # The painted wallpaper itself, cut to the preview's shape.
        with Image.open(painted) as wall:
            img = wall.convert("RGBA").resize((w, int(wall.height * w / wall.width))).crop((0, 0, w, h))
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
    }
    if entry["wallpaper"]:
        out["wallpaper"] = {k: v for k, v in entry["wallpaper"].items() if k != "paint"}
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

WALL_W, WALL_H = 720, 1560


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


def paint_wallpaper(entry, folder):
    """Paints [entry]'s picture into [folder] as wallpaper.png, kept under 300 KB. Returns its path."""
    kind = entry["wallpaper"]["paint"]
    img = PAINTERS[kind](entry, random.Random(entry["id"])).convert("RGB")
    path = os.path.join(folder, "wallpaper.png")
    # Soft pictures banded into a palette of their own stay smooth and small.
    for colours in (256, 128, 64):
        img.quantize(colors=colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, "PNG", optimize=True)
        if os.path.getsize(path) < 300_000:
            return path
    raise AssertionError((entry["id"], "wallpaper.png is over 300 KB"))


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
      <ul class="share-tags">{tags}</ul>{season}
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
    return SHARE_PAGE.format(
        id=esc(entry["id"]),
        name=esc(entry["name"]),
        description=esc(entry["description"]),
        premium=" &middot; Orbital Premium" if entry["premium"] else "",
        tags=tags,
        season=season,
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
    for entry in finished:
        folder = os.path.join(ROOT, entry["id"])
        os.makedirs(folder, exist_ok=True)
        data = theme_json(entry).encode("utf-8")
        with open(os.path.join(folder, "theme.json"), "wb") as f:
            f.write(data)
        if (entry["wallpaper"] or {}).get("paint"):
            print(entry["id"], os.path.getsize(paint_wallpaper(entry, folder)), "bytes wallpaper")
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
        }
        if entry["season"]:
            item["season"] = entry["season"]
        index.append(item)
        print(entry["id"], len(data), "bytes json,", size, "bytes png")
    with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"kind": "orbital-theme-index", "format": 1, "themes": index, "featured": FEATURED},
                  f, indent=2, ensure_ascii=False)
        f.write("\n")
    check_written()
    write_share_pages(finished)


def check_written():
    """Reads back what was written, as the app will: every index entry's file is there, its size and
    SHA-256 match, and every season a theme names is in the index's own featured section."""
    with open(os.path.join(ROOT, "index.json"), encoding="utf-8") as f:
        index = json.load(f)
    seasons = {s["id"] for s in index["featured"]["seasonal"]}
    for item in index["themes"]:
        with open(os.path.join(ROOT, item["file"]), "rb") as f:
            data = f.read()
        assert len(data) == item["size"], (item["id"], "size")
        assert hashlib.sha256(data).hexdigest() == item["sha256"], (item["id"], "sha256")
        theme_file = json.loads(data.decode("utf-8"))
        assert theme_file.get("season") == item.get("season"), (item["id"], "season")
        assert item.get("season") is None or item["season"] in seasons, (item["id"], item["season"])
        image = (theme_file.get("wallpaper") or {}).get("image")
        if image:
            picture_path = os.path.join(ROOT, item["id"], image)
            assert os.path.getsize(picture_path) < 300_000, (item["id"], image)


if __name__ == "__main__":
    main()

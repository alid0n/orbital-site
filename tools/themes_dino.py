"""Five dinosaur fossil themes: museum skeletons, a working quarry and two classic paintings."""
from themes_common import Kit


def register(g):
    k = Kit(g)
    pal, w, CLOCK = k.pal, k.w, k.CLOCK
    commons = "Wikimedia Commons"

    k.photo("commons-gary-todd-trex-zhengzhou.jpg", "Tyrannosaurus Rex (Zhengzhou)", "Gary Todd", commons, "CC0 1.0",
            "https://commons.wikimedia.org/wiki/File:Tyrannosaurus_Rex_(Zhengzhou).jpg")
    k.photo("commons-knight-laelaps-1897.jpg", "Laelaps", "Charles R. Knight", commons, "Public domain",
            "https://commons.wikimedia.org/wiki/File:Laelaps-Charles_Knight-1897.jpg")
    k.photo("commons-blm-cleveland-lloyd-quarry-26784733111.jpg", "Cleveland-Lloyd Dinosaur Quarry",
            "Bureau of Land Management, Utah", commons, "Public domain",
            "https://commons.wikimedia.org/wiki/File:Cleveland_Lloyd_Dinosaur_Quarry_(26784733111).jpg")
    k.photo("commons-knight-brontosaurus.jpg", "Brontosaurus illustration", "Charles R. Knight", commons, "Public domain",
            "https://commons.wikimedia.org/wiki/File:Illustration_of_the_Brontosaurus_by_Charles_R._Knight.jpg")
    k.photo("commons-gary-todd-ankylosaurus-skeleton.jpg", "Ankylosaurus Skeleton", "Gary Todd", commons, "CC0 1.0",
            "https://commons.wikimedia.org/wiki/File:Ankylosaurus_Skeleton_(31556851166).jpg")

    k.add("trex_hall", "T. rex Hall",
          "A towering skeleton in a museum hall, in bone ivory and amber, with the Orbit Pad.",
          ["audience:general", "vibe:elegant", "vibe:dark", "color:gold", "color:black"],
          pal("#E8C27A", "#9FD0C0", "#F5EEDD", "#B3A88F", "#0A0806", "#12100C", "#241E16", "#33000000"),
          k.washed("commons-gary-todd-trex-zhengzhou.jpg", "#0A0806", focus=(0.5, 0.3), zoom=1.5, top=0.5, bottom=0.8, mid=0.2),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="GLASS", widgetCorner="ROUNDED",
               widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5, font="cinzel", clockFace="LINE", panelLook="FADE", notch="DOT"),
          ["dark", "bold", "minimal"], "#2A2218", premium=True,
          layout=dict(homeLayout="ORBIT_PAD", dockStyle="PAD", anchor="BOTTOM", drawerLayout="GRID",
                      widgets=[CLOCK(0.07, 1.0), w("next", "AGENDA", 0.04, 0.22, 0.92)]),
          assistant="SPOTLIGHT", topics=["dinosaurs", "nature"])

    k.add("laelaps", "Laelaps",
          "Charles R. Knight's classic 1897 painting of two dinosaurs, in teal and olive, on the Showcase.",
          ["audience:general", "vibe:dreamy", "vibe:dark", "color:green", "color:gold"],
          pal("#E3C25B", "#6FC1A8", "#F6F2E4", "#B9C4A9", "#0A1410", "#13231D", "#1F3A30", "#33000000"),
          k.washed("commons-knight-laelaps-1897.jpg", "#0A1410", focus=(0.42, 0.5), top=0.5, bottom=0.8, mid=0.15),
          dict(corner="ROUNDED", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="GLASS", widgetCorner="ROUNDED",
               widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5, font="lora", clockFace="LINE", panelLook="FADE", notch="TAPER"),
          ["dark", "vivid", "calm"], "#2E5A44", premium=True,
          layout=dict(homeLayout="CONSOLE", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID"),
          assistant="NOTEPAD", styles=("big screen",), topics=["dinosaurs", "nature", "art"])

    k.add("in_the_rock", "In the Rock",
          "Fossil bone still set in sandstone, with every app a stone tile in rust and sand.",
          ["audience:general", "vibe:energetic", "vibe:dark", "color:orange", "color:gold"],
          pal("#E08A3C", "#E8CB8A", "#F6EFE4", "#C7B9A5", "#1B1714", "#2A2420", "#3A322B", "#33000000"),
          k.washed("commons-blm-cleveland-lloyd-quarry-26784733111.jpg", "#1B1714", top=0.5, bottom=0.78, mid=0.25),
          dict(corner="SQUARE", iconShape="TILE", iconStyle="ORIGINAL", widgetLook="SOLID", widgetCorner="SQUARE",
               widgetEdge="NONE", widgetTint=0.2, widgetSolid=1.0, font="dm_sans", clockFace="LINE", uppercase=True,
               panelLook="CARD", notch="NONE"),
          ["dark", "bold", "cozy"], "#6B4A2A",
          layout=dict(homeLayout="PAGES", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID", tiledDrawer=True,
                      drawerColumns=4, widgets=[CLOCK(0.05, 1.0), w("next", "AGENDA", 0.04, 0.18, 0.92)]),
          assistant="CHAT", topics=["dinosaurs", "nature"])

    k.add("brontosaurus_study", "Brontosaurus Study",
          "A vintage field illustration on parchment green, in a light theme with the Orbit wheel.",
          ["audience:general", "vibe:calm", "vibe:elegant", "color:green", "color:white"],
          pal("#3F6B4A", "#B5552E", "#2B2A1E", "#6B6A55", "#EDE6CF", "#F4EEDA", "#E3DABD", "#33EDE6CF", light=True),
          k.washed("commons-knight-brontosaurus.jpg", "#EDE6CF", focus=(0.55, 0.5), top=0.6, bottom=0.85, mid=0.25,
                   saturation=0.9, texture="paper"),
          dict(corner="ROUNDED", iconShape="CIRCLE", iconStyle="ORIGINAL", widgetLook="CARD", widgetCorner="ROUNDED",
               widgetEdge="HAIR", widgetTint=0.2, widgetSolid=0.9, font="marcellus", clockFace="LINE", panelLook="LINES", notch="TAPER"),
          ["light", "calm", "cozy"], "#C9C29C",
          layout=dict(homeLayout="PAGES", dockStyle="ORBIT", anchor="BOTTOM", drawerLayout="GRID",
                      widgets=[CLOCK(0.06, 1.0), w("note", "NOTE", 0.04, 0.2, 0.92)]),
          assistant="NOTEPAD", styles=("one-handed",), topics=["dinosaurs", "nature", "art"])

    k.add("ankylosaurus", "Ankylosaurus",
          "An armoured skeleton in a museum hall, with every app a hexagon plate on an open canvas.",
          ["audience:general", "vibe:futuristic", "vibe:dark", "color:gold", "color:green"],
          pal("#D9A441", "#8FB8A8", "#F7F1E6", "#BCAF98", "#14100B", "#1B1610", "#2D251B", "#33000000"),
          k.washed("commons-gary-todd-ankylosaurus-skeleton.jpg", "#14100B", focus=(0.45, 0.5), top=0.55, bottom=0.8, mid=0.2),
          dict(corner="ROUNDED", iconShape="HEX", iconStyle="ORIGINAL", widgetLook="GLASS", widgetCorner="ROUNDED",
               widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5, font="exo_2", clockFace="LINE", panelLook="LINES", notch="CHEVRON"),
          ["dark", "bold", "cozy"], "#4A3A22", premium=True, base="HONEYCOMB",
          layout=dict(homeLayout="FREE_ROAM", dockStyle="ROW", anchor="BOTTOM", drawerLayout="GRID", tiledDrawer=True,
                      drawerColumns=5, drawerRail=False, widgets=[CLOCK(0.06, 1.1)]),
          assistant="HUD", topics=["dinosaurs", "nature"])

"""Ten themes for the interests people ask for: music, sports, cars, food, fitness, pets, books, fashion,
gaming and manga. Eight are CC0 photographs with no people in them; gaming and manga are drawn here."""
from themes_common import Kit


def register(g):
    k = Kit(g)
    pal, w, CLOCK, WEATHER, MEDIA_FULL = k.pal, k.w, k.CLOCK, k.WEATHER, k.MEDIA_FULL
    snap = "StockSnap.io"

    def stock(file, title, author, slug):
        k.photo(file, title, author, snap, "CC0 1.0", "https://stocksnap.io/photo/" + slug)

    stock("stocksnap-vinyl-record-dilopnohdi.jpg", "Vinyl Record", "Spencer Selover", "vinyl-record-DILOPNOHDI")
    stock("stocksnap-basketball-hoop-rjky5wws8v.jpg", "Basketball Hoop", "Steve Johnson", "basketball-hoop-RJKY5WWS8V")
    stock("stocksnap-car-auto-aqpi3ekz9e.jpg", "Car Auto", "Jp Valery", "car-auto-AQPI3EKZ9E")
    stock("stocksnap-cooking-food-rrazgyxtzi.jpg", "Cooking Food", "Healthy Living", "cooking-food-RRAZGYXTZI")
    stock("stocksnap-fitness-weights-fvuo0yimkh.jpg", "Fitness Weights", "Kristin Hardwick", "fitness-weights-FVUO0YIMKH")
    stock("stocksnap-pug-dog-jhpve3xlue.jpg", "Pug Dog", "Matthew Henry", "pug-dog-JHPVE3XLUE")
    stock("stocksnap-books-knowledge-2venf09zow.jpg", "Books Knowledge", "Dakota Corbin", "books-knowledge-2VENF09ZOW")
    stock("stocksnap-fashion-clothes-zn97zif3zu.jpg", "Fashion Clothes", "Hannah Morgan", "fashion-clothes-ZN97ZIF3ZU")

    def look(font, clock="LINE", shape="CIRCLE", widget="GLASS", corner="ROUNDED", **extra):
        out = dict(corner=corner, iconShape=shape, iconStyle="ORIGINAL", widgetLook=widget, widgetCorner=corner,
                   widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5, font=font, clockFace=clock, panelLook="FADE",
                   notch="DOT")
        out.update(extra)
        return out

    def pages(dock="ROW", widgets=None, **extra):
        return dict(homeLayout="PAGES", dockStyle=dock, anchor="BOTTOM", drawerLayout="GRID",
                    widgets=widgets or [CLOCK(0.06, 1.0)], **extra)

    k.add("vinyl_nights", "Vinyl Nights",
          "A record spinning on a wooden shelf, in amber and cream, with your music a swipe away.",
          ["audience:general", "vibe:chill", "vibe:dark", "color:orange", "color:gold"],
          pal("#FFB454", "#E9D8B4", "#F8EEDC", "#BBA98C", "#0D0805", "#140E09", "#241A12", "#33000000"),
          k.washed("stocksnap-vinyl-record-dilopnohdi.jpg", "#0D0805", focus=(0.5, 0.78), zoom=1.4, top=0.55, bottom=0.8, mid=0.2),
          look("dm_sans"), ["dark", "cozy", "calm"], "#3A2A1A",
          layout=pages("ORBIT", [CLOCK(0.06, 1.0), MEDIA_FULL(0.2)]), assistant="CHAT", topics=["music"])

    k.add("courtside", "Courtside",
          "A basketball hoop against a warm orange wall, with bold sporty lettering.",
          ["audience:general", "vibe:sporty", "vibe:energetic", "color:orange", "color:black"],
          pal("#FF8A3D", "#FFD9B0", "#FFF4EA", "#E0B898", "#150A05", "#1D0F08", "#301A0E", "#33000000"),
          k.washed("stocksnap-basketball-hoop-rjky5wws8v.jpg", "#150A05", focus=(0.45, 0.5), top=0.5, bottom=0.78, mid=0.15),
          look("rajdhani", uppercase=True), ["bold", "vivid", "dark"], "#C25E1E",
          layout=pages("ROW", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="VOICE", topics=["sports"])

    k.add("muscle_car", "Muscle Car",
          "A violet muscle car with chrome lettering, built for people who love the road.",
          ["audience:general", "vibe:sporty", "vibe:energetic", "color:purple", "color:black"],
          pal("#C77DFF", "#E0E0F0", "#F6F0FF", "#B5A8CF", "#0B0614", "#120A1E", "#201232", "#33000000"),
          k.washed("stocksnap-car-auto-aqpi3ekz9e.jpg", "#0B0614", top=0.55, bottom=0.8, mid=0.2),
          look("oxanium", shape="SQUIRCLE"), ["dark", "bold", "vivid"], "#5A2E8A",
          layout=pages("ORBIT"), assistant="HUD", topics=["cars"])

    k.add("fresh_table", "Fresh Table",
          "Warm tomatoes, herbs and pasta in a kitchen glow, for people who love to cook.",
          ["audience:general", "vibe:cozy", "vibe:energetic", "color:red", "color:orange"],
          pal("#E8553D", "#8FBF6A", "#FFF3E4", "#CDB6A0", "#140A07", "#1C100B", "#2E1C14", "#33000000"),
          k.washed("stocksnap-cooking-food-rrazgyxtzi.jpg", "#140A07", top=0.55, bottom=0.8, mid=0.25),
          look("nunito"), ["dark", "cozy", "vivid"], "#8A3A22",
          layout=pages("CARD", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="CHAT", topics=["food"])

    k.add("strength", "Strength",
          "Bright blue dumbbells on warm wood, with a weekly view to keep your training on track.",
          ["audience:general", "vibe:energetic", "vibe:sporty", "color:blue", "color:orange"],
          pal("#2F9BFF", "#FFB347", "#F2F6FA", "#A3B1C2", "#06090E", "#0B1018", "#161F2C", "#33000000"),
          k.washed("stocksnap-fitness-weights-fvuo0yimkh.jpg", "#06090E", top=0.55, bottom=0.8, mid=0.2),
          look("outfit", clock="DIGITS", shape="ROUNDED"), ["dark", "vivid", "bold"], "#1F6FBF",
          layout=pages("ROW", [CLOCK(0.05, 1.0), w("week", "CALENDAR_WEEK", 0.04, 0.3, 0.92)]), assistant="VOICE",
          topics=["fitness", "sports"])

    k.add("cozy_pug", "Cozy Pug",
          "A pug wrapped in a blanket, in warm sand and sage, with friendly rounded lettering.",
          ["audience:general", "vibe:cozy", "vibe:playful", "color:orange", "color:green"],
          pal("#E0A56B", "#8DB38F", "#FBF3E8", "#CDB89F", "#1A130D", "#231A12", "#352619", "#33000000"),
          k.washed("stocksnap-pug-dog-jhpve3xlue.jpg", "#1A130D", top=0.5, bottom=0.78, mid=0.15),
          look("baloo_2", clock="STACK"), ["cozy", "playful", "calm"], "#8A6A45",
          layout=pages("ROW", [CLOCK(0.06, 1.1), WEATHER(0.04, 0.22, 0.92)]), assistant="CHAT",
          topics=["animals", "family"])

    k.add("reading_room", "Reading Room",
          "Shelves of books in lamplight, with every app listed in a calm library-style index.",
          ["audience:general", "vibe:cozy", "vibe:elegant", "color:gold", "color:green"],
          pal("#E3B35A", "#7FB9B0", "#F7EEDC", "#BFAE90", "#0E0A06", "#16100A", "#2A1E12", "#33000000"),
          k.washed("stocksnap-books-knowledge-2venf09zow.jpg", "#0E0A06", top=0.55, bottom=0.8, mid=0.25),
          look("lora", shape="ROUNDED"), ["dark", "cozy", "calm"], "#4A3320", premium=True,
          layout=dict(homeLayout="DRAWER", dockStyle="ROW", anchor="BOTTOM", drawerLayout="LIST", drawerListAlign="LEFT",
                      drawerWidgets=[g["side"]("CLOCK", end="TOP"), g["side"]("CALENDAR")]),
          assistant="NOTEPAD", styles=("minimal",), topics=["books"])

    k.add("wardrobe", "Wardrobe",
          "A neutral rail of clothes in soft sand and espresso, a light theme with a classic serif.",
          ["audience:general", "vibe:elegant", "vibe:calm", "color:white", "color:orange"],
          pal("#8A5A3C", "#2F4F4F", "#2A211B", "#7A6A5C", "#F1E9DE", "#F7F1E8", "#E6DACB", "#33F1E9DE", light=True),
          k.washed("stocksnap-fashion-clothes-zn97zif3zu.jpg", "#F1E9DE", top=0.6, bottom=0.85, mid=0.3),
          look("cormorant", widget="CARD", panelLook="LINES"), ["light", "calm", "minimal"], "#D8C6AE",
          layout=pages("CARD", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="SPOTLIGHT", topics=["fashion"])

    k.add("pixel_quest", "Pixel Quest",
          "A moonlit pixel-art mountain range, with blocky square icons and bold retro lettering.",
          ["audience:general", "vibe:retro", "vibe:playful", "color:purple", "color:yellow", "era:80s"],
          pal("#FFD84D", "#5CE1E6", "#FBF6FF", "#B8A6E0", "#0E0620", "#140A2E", "#241250", "#33000000"),
          g["picture"]("pixels", wash=[(0.0, "#0E0620", 0.5), (0.2, "#0E0620", 0.3), (0.62, "#0E0620", 0.1),
                                       (0.8, "#0E0620", 0.55), (1.0, "#0E0620", 0.75)], vignette=0.1, grain=0.0),
          dict(corner="SQUARE", iconShape="SQUARE", iconStyle="FLAT", widgetLook="SOLID", widgetCorner="SQUARE",
               widgetEdge="BOLD", widgetTint=0.3, widgetSolid=1.0, font="vt323", clockFace="LINE", uppercase=True,
               panelLook="LINES", notch="PIP"),
          ["dark", "playful", "vivid"], "#5B2287",
          layout=pages("ROW", [CLOCK(0.06, 1.0), w("next", "AGENDA", 0.04, 0.2, 0.92)]), assistant="RETRO",
          topics=["gaming", "retro"])

    k.add("manga_panel", "Manga Panel",
          "Ink-black panel borders, screentone dots and a splash of sakura pink, in a light theme.",
          ["audience:general", "vibe:playful", "vibe:energetic", "color:white", "color:pink", "color:black"],
          pal("#E8678A", "#2B2B33", "#1A1A1F", "#5C5C66", "#FCFBF8", "#FFFFFF", "#F0EEEA", "#33FFFFFF", light=True),
          g["picture"]("manga", wash=[(0.0, "#FCFBF8", 0.62), (0.18, "#FCFBF8", 0.5), (0.34, "#FCFBF8", 0.5),
                                      (0.62, "#FCFBF8", 0.5), (0.8, "#FCFBF8", 0.82), (1.0, "#FCFBF8", 0.9)],
                      vignette=0.0, grain=0.0),
          dict(corner="SQUARE", iconShape="ROUNDED", iconStyle="ORIGINAL", widgetLook="CARD", widgetCorner="SQUARE",
               widgetEdge="BOLD", widgetTint=0.2, widgetSolid=1.0, font="kalam", clockFace="BARE", panelLook="CARD",
               notch="NONE"),
          ["light", "playful", "bold"], "#F3A9BE",
          layout=pages("ORBIT", [CLOCK(0.06, 1.1), WEATHER(0.04, 0.22, 0.92)]), assistant="CHAT",
          topics=["anime", "art"])

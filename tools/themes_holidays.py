"""Themes for the holidays, each offered only while its season is on (see FEATURED["seasonal"]):
Christmas, Hanukkah, Easter, Mother's Day, Independence Day, Father's Day, Thanksgiving, St Patrick's
Day, Holi, Eid, Lunar New Year (two) and Diwali (two). Nine are CC0 photographs with no people in them;
the rest are drawn here (see themes_painters)."""
from themes_common import Kit


def register(g):
    k = Kit(g)
    pal, w, CLOCK, WEATHER, MEDIA = k.pal, k.w, k.CLOCK, k.WEATHER, k.MEDIA
    snap = "StockSnap.io"

    def stock(file, title, author, slug):
        k.photo(file, title, author, snap, "CC0 1.0", "https://stocksnap.io/photo/" + slug)

    stock("stocksnap-christmas-tree-gvw1gu9xps.jpg", "Christmas Tree", "Dawid Zawiła", "christmas-tree-GVW1GU9XPS")
    stock("stocksnap-candles-light-w1md6oxurg.jpg", "Candles Light", "Nicola Fioravanti", "candles-light-W1MD6OXURG")
    stock("stocksnap-easter-eggs-app4wjvpuc.jpg", "Easter Eggs", "Altered Reality", "easter-eggs-APP4WJVPUC")
    stock("stocksnap-leaves-pumpkin-ak32pjis4t.jpg", "Leaves Pumpkin", "Cala", "leaves-pumpkin-AK32PJIS4T")
    stock("stocksnap-chinese-lanterns-1vzo8ddchz.jpg", "Chinese Lanterns", "Humphrey Muleba", "chinese-lanterns-1VZO8DDCHZ")
    stock("stocksnap-green-clover-ui30icngu6.jpg", "Green Clover", "Quentin REY", "green-clover-UI30ICNGU6")
    stock("stocksnap-fireworks-lights-fjkmzcb8fg.jpg", "Fireworks Lights", "Aaron Burden", "fireworks-lights-FJKMZCB8FG")
    stock("stocksnap-flowers-nature-7ldgqbuwdm.jpg", "Flowers Nature", "Alex Blăjan", "flowers-nature-7LDGQBUWDM")
    stock("stocksnap-wood-tools-00f7db5857.jpg", "Wood Tools", "Todd Quackenbush", "wood-tools-00F7DB5857")

    def look(font, clock="LINE", shape="CIRCLE", widget="GLASS", corner="ROUNDED", **extra):
        out = dict(corner=corner, iconShape=shape, iconStyle="ORIGINAL", widgetLook=widget, widgetCorner=corner,
                   widgetEdge="HAIR", widgetTint=0.25, widgetSolid=0.5, font=font, clockFace=clock, panelLook="FADE",
                   notch="DOT")
        out.update(extra)
        return out

    def pages(dock="ROW", widgets=None):
        return dict(homeLayout="PAGES", dockStyle=dock, anchor="BOTTOM", drawerLayout="GRID",
                    widgets=widgets or [CLOCK(0.06, 1.0)])

    # WINTER HOLIDAYS (12-01 to 01-06): Christmas and Hanukkah join the winter themes.
    k.add("christmas_lights", "Christmas Lights",
          "A tree glowing with colour against the dark, with soft lettering and sparkles when you tap.",
          ["audience:general", "vibe:cozy", "vibe:dreamy", "color:red", "color:green", "color:gold"],
          pal("#FF5A5A", "#7FE08A", "#FFF4E6", "#D6B9A0", "#0A0504", "#120806", "#24100C", "#33000000"),
          k.washed("stocksnap-christmas-tree-gvw1gu9xps.jpg", "#0A0504", top=0.5, bottom=0.78, mid=0.15),
          look("cormorant"), ["dark", "cozy", "vivid"], "#6A1E1A", premium=True, effect="sparkles", tap=True,
          season="winter", layout=pages("ORBIT", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]),
          assistant="SPOTLIGHT", topics=["christmas", "winter"])

    k.add("festival_of_lights", "Festival of Lights",
          "Candlelight in deep blue and gold, with twinkling stars, for the eight nights of Hanukkah.",
          ["audience:general", "vibe:elegant", "vibe:calm", "color:blue", "color:gold", "color:white"],
          pal("#E8C766", "#8FB4FF", "#F4F7FF", "#9FB0D0", "#030A1E", "#06122E", "#0E2250", "#33000000"),
          k.washed("stocksnap-candles-light-w1md6oxurg.jpg", "#030A1E", top=0.55, bottom=0.8, mid=0.2,
                   map=[(0.0, "#04102E"), (0.45, "#0B2A6B"), (0.8, "#C9A24A"), (1.0, "#FFF3C8")], map_amount=0.75),
          look("cinzel"), ["dark", "calm", "bold"], "#0B2A6B", premium=True, effect="twinkle-stars", tap=True,
          season="winter", layout=pages("ROW", [CLOCK(0.06, 1.0), w("next", "AGENDA", 0.04, 0.2, 0.92)]),
          assistant="SPOTLIGHT", topics=["hanukkah", "winter"])

    # SPRING (03-20 to 05-31): Easter and Mother's Day join the spring themes.
    k.add("spring_eggs", "Spring Eggs",
          "Pastel eggs in soft pink and blue, a light and cheerful theme for Easter.",
          ["audience:general", "vibe:playful", "vibe:dreamy", "color:pink", "color:blue", "color:pastel"],
          pal("#E0609A", "#4FA7D8", "#3A2A44", "#8A7596", "#FFF6FB", "#FFFBFD", "#F6E4EE", "#33FFF6FB", light=True),
          k.washed("stocksnap-easter-eggs-app4wjvpuc.jpg", "#FFF6FB", top=0.62, bottom=0.86, mid=0.3, saturation=1.05),
          look("quicksand", widget="CARD"), ["light", "pastel", "playful"], "#F2B6CF", season="spring",
          layout=pages("ROW", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="CHAT",
          topics=["easter", "spring", "family"])

    k.add("mothers_day", "Mother's Day",
          "Pink roses on a deep plum background, with graceful lettering, for the people who raised us.",
          ["audience:general", "vibe:elegant", "vibe:dreamy", "color:pink", "color:red"],
          pal("#F2789F", "#F5D0DC", "#FFF0F5", "#D9A7B8", "#160610", "#1F0A16", "#34142A", "#33000000"),
          k.washed("stocksnap-flowers-nature-7ldgqbuwdm.jpg", "#160610", top=0.55, bottom=0.8, mid=0.2),
          look("playfair_display"), ["dark", "vivid", "calm"], "#7A2C4A", season="spring",
          layout=pages("ORBIT", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="SPOTLIGHT",
          topics=["mothers day", "family"])

    # SUMMER (06-01 to 08-31): Independence Day and Father's Day join the summer themes.
    k.add("independence_day", "Independence Day",
          "Fireworks lighting a night sky in red, white and blue, with a burst when you tap.",
          ["audience:general", "vibe:energetic", "vibe:dark", "color:red", "color:blue", "color:white"],
          pal("#FF4D5E", "#6FA8FF", "#FFFFFF", "#B8C4E0", "#050A1C", "#0A1230", "#16224A", "#33000000"),
          k.washed("stocksnap-fireworks-lights-fjkmzcb8fg.jpg", "#050A1C", top=0.5, bottom=0.78, mid=0.15),
          look("montserrat"), ["dark", "vivid", "bold"], "#0A1230", premium=True, effect="fireworks", tap=True,
          season="summer", layout=pages("ROW", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="HUD",
          topics=["independence day", "summer"])

    k.add("fathers_day", "Father's Day",
          "A workbench of well-used tools in walnut and brass, with sturdy lettering.",
          ["audience:general", "vibe:cozy", "vibe:elegant", "color:gold", "color:black"],
          pal("#D9A441", "#7FA6BF", "#F3ECE0", "#BDAE96", "#0D0A07", "#15100B", "#271D14", "#33000000"),
          k.washed("stocksnap-wood-tools-00f7db5857.jpg", "#0D0A07", top=0.55, bottom=0.8, mid=0.2),
          look("rajdhani", uppercase=True), ["dark", "cozy", "bold"], "#4A3520", season="summer",
          layout=pages("ROW", [CLOCK(0.06, 1.0), w("next", "AGENDA", 0.04, 0.2, 0.92)]), assistant="NOTEPAD",
          topics=["fathers day", "family"])

    # AUTUMN (11-01 to 11-30): Thanksgiving joins the autumn themes.
    k.add("harvest_table", "Harvest Table",
          "A pumpkin and fallen leaves in warm amber, with leaves drifting down when you tap.",
          ["audience:general", "vibe:cozy", "vibe:calm", "color:orange", "color:gold"],
          pal("#E8872F", "#C9A25A", "#FBEFD9", "#CDB08A", "#120A05", "#1B100A", "#2E1C10", "#33000000"),
          k.washed("stocksnap-leaves-pumpkin-ak32pjis4t.jpg", "#120A05", top=0.55, bottom=0.8, mid=0.2),
          look("lora"), ["dark", "cozy", "calm"], "#7A4A1E", premium=True, effect="falling-leaves", tap=True,
          season="autumn", layout=pages("ORBIT", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="NOTEPAD",
          topics=["thanksgiving", "autumn", "family"])

    # MARCH FESTIVALS (02-28 to 03-31): St Patrick's Day, Holi and Eid.
    k.add("lucky_clover", "Lucky Clover",
          "Dewy clover leaves in rich green, with friendly rounded lettering for St Patrick's Day.",
          ["audience:general", "vibe:playful", "vibe:calm", "color:green", "color:gold"],
          pal("#3DDC84", "#F2D45C", "#F1FFF4", "#9FC9AC", "#04130A", "#07200E", "#103A1C", "#33000000"),
          k.washed("stocksnap-green-clover-ui30icngu6.jpg", "#04130A", top=0.55, bottom=0.8, mid=0.25),
          look("fredoka"), ["dark", "vivid", "playful"], "#1F7A3A", season="march_festivals",
          layout=pages("ROW"), assistant="CHAT", topics=["st patricks day", "nature"])

    k.add("holi_colors", "Festival of Colors",
          "Powder clouds of pink, gold and turquoise drifting through the dark, for the spring festival of Holi.",
          ["audience:general", "vibe:playful", "vibe:energetic", "color:pink", "color:yellow", "color:purple"],
          pal("#FF4D9A", "#FFD23A", "#FFFFFF", "#D9C8F0", "#100824", "#180C34", "#2A1658", "#33000000"),
          g["picture"]("powder", wash=[(0.0, "#100824", 0.45), (0.18, "#100824", 0.3), (0.34, "#100824", 0.0),
                                       (0.62, "#100824", 0.0), (0.8, "#100824", 0.5), (1.0, "#100824", 0.7)],
                      vignette=0.15, grain=0.02),
          look("baloo_2"), ["dark", "vivid", "playful"], "#B0307A", season="march_festivals",
          layout=pages("ORBIT"), assistant="VOICE", topics=["holi", "spring"])

    k.add("crescent_night", "Crescent Night",
          "A golden crescent and star over lanterns, in deep emerald, with twinkling stars, for Eid.",
          ["audience:general", "vibe:elegant", "vibe:dreamy", "color:green", "color:gold"],
          pal("#ECBE60", "#6FD3C0", "#F4FBF8", "#9FC8C0", "#03181A", "#062226", "#0D3A40", "#33000000"),
          g["picture"]("crescent", wash=[(0.0, "#03181A", 0.35), (0.18, "#03181A", 0.2), (0.34, "#03181A", 0.05),
                                         (0.62, "#03181A", 0.1), (0.8, "#03181A", 0.6), (1.0, "#03181A", 0.8)],
                      vignette=0.15, grain=0.02),
          look("cormorant"), ["dark", "calm", "vivid"], "#0B4A4A", premium=True, effect="twinkle-stars", tap=True,
          season="march_festivals", layout=pages("ORBIT"), assistant="SPOTLIGHT", topics=["eid", "ramadan"])

    # LUNAR NEW YEAR (01-15 to 02-21): two themes.
    k.add("lantern_festival", "Lantern Festival",
          "Red lanterns glowing against the sky, in gold and crimson, for Lunar New Year.",
          ["audience:general", "vibe:energetic", "vibe:elegant", "color:red", "color:gold"],
          pal("#FFC857", "#FF6B5E", "#FFF3E0", "#E0B896", "#1A0506", "#260A0B", "#431416", "#33000000"),
          k.washed("stocksnap-chinese-lanterns-1vzo8ddchz.jpg", "#1A0506", top=0.5, bottom=0.78, mid=0.15),
          look("cinzel"), ["dark", "vivid", "bold"], "#8A1A1E", premium=True, effect="sparkles", tap=True,
          season="lunar_new_year", layout=pages("ORBIT", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]),
          assistant="SPOTLIGHT", topics=["lunar new year"])

    k.add("golden_fortune", "Golden Fortune",
          "Lucky red with a golden lattice and a rising sun, for Lunar New Year.",
          ["audience:general", "vibe:elegant", "vibe:energetic", "color:red", "color:gold"],
          pal("#FFD27A", "#FF8A6B", "#FFF5E1", "#E8B79A", "#2A0508", "#38090E", "#5A1018", "#33000000"),
          g["picture"]("fortune", wash=[(0.0, "#2A0508", 0.5), (0.18, "#2A0508", 0.3), (0.34, "#2A0508", 0.05),
                                        (0.62, "#2A0508", 0.1), (0.8, "#2A0508", 0.55), (1.0, "#2A0508", 0.78)],
                      vignette=0.15, grain=0.02),
          look("marcellus"), ["dark", "bold", "vivid"], "#962028", season="lunar_new_year",
          layout=pages("ROW", [CLOCK(0.06, 1.0), w("next", "AGENDA", 0.04, 0.2, 0.92)]), assistant="SPOTLIGHT",
          topics=["lunar new year"])

    # DIWALI (10-15 to 11-15): two themes.
    k.add("festival_of_lamps", "Festival of Lamps",
          "A row of clay lamps glowing in the dark, in gold and rose, with sparkles when you tap, for Diwali.",
          ["audience:general", "vibe:dreamy", "vibe:elegant", "color:orange", "color:gold", "color:pink"],
          pal("#FFB347", "#FF6F91", "#FFF1DC", "#E3B98F", "#1C0508", "#26080C", "#42101A", "#33000000"),
          g["picture"]("lamps", wash=[(0.0, "#1C0508", 0.45), (0.18, "#1C0508", 0.3), (0.34, "#1C0508", 0.05),
                                      (0.62, "#1C0508", 0.1), (0.8, "#1C0508", 0.35), (1.0, "#1C0508", 0.55)],
                      vignette=0.2, grain=0.02),
          look("marcellus"), ["dark", "vivid", "cozy"], "#7A1A22", premium=True, effect="sparkles", tap=True,
          season="diwali", layout=pages("ORBIT"), assistant="SPOTLIGHT", topics=["diwali"])

    k.add("marigold_glow", "Marigold Glow",
          "Orange, gold and magenta lights drifting in the dark, a warm and festive theme for Diwali.",
          ["audience:general", "vibe:energetic", "vibe:dreamy", "color:orange", "color:pink", "color:gold"],
          pal("#FFC247", "#FF5E8A", "#FFF4E0", "#E6B994", "#1A0610", "#240A18", "#3C1228", "#33000000"),
          g["picture"]("marigold", wash=[(0.0, "#1A0610", 0.45), (0.18, "#1A0610", 0.3), (0.34, "#1A0610", 0.05),
                                         (0.62, "#1A0610", 0.1), (0.8, "#1A0610", 0.5), (1.0, "#1A0610", 0.7)],
                      vignette=0.15, grain=0.02),
          look("poppins"), ["dark", "vivid", "bold"], "#B03060", season="diwali",
          layout=pages("ROW", [CLOCK(0.06, 1.0), WEATHER(0.04, 0.2, 0.92)]), assistant="CHAT", topics=["diwali"])

    # THE SEASONS these themes are offered in. Each opens and closes on the same days every year, so a
    # holiday that moves (Easter, Eid, Diwali, Lunar New Year, Holi) gets a window wide enough for the
    # next several years. Eid moves earlier each year; its window needs a look every year.
    seasonal = g["FEATURED"]["seasonal"]
    by_id = {s["id"]: s for s in seasonal}
    for season_id, ids in (("winter", ["christmas_lights", "festival_of_lights"]),
                           ("spring", ["spring_eggs", "mothers_day"]),
                           ("summer", ["independence_day", "fathers_day"]),
                           ("autumn", ["harvest_table"])):
        by_id[season_id]["themes"] = by_id[season_id]["themes"] + ids
    seasonal.extend([
        {"id": "march_festivals", "name": "March festivals", "from": "02-28", "until": "03-31", "teaseDays": 5,
         "earlyDays": 3, "themes": ["lucky_clover", "holi_colors", "crescent_night"]},
        {"id": "lunar_new_year", "name": "Lunar New Year", "from": "01-15", "until": "02-21", "teaseDays": 5,
         "earlyDays": 3, "themes": ["lantern_festival", "golden_fortune"]},
        {"id": "diwali", "name": "Diwali", "from": "10-15", "until": "11-15", "teaseDays": 5, "earlyDays": 3,
         "themes": ["festival_of_lamps", "marigold_glow"]},
    ])

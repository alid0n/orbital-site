"""Fifteen accessibility themes. Accessibility is never gated, so every one is free: pages with a flat row
or the Orbit wheel, no effects, fonts from the free part of the library, and plain single-colour
wallpapers with nothing to compete with the text. Big icons with their names, solid widgets with bold
edges, and a palette whose contrast is checked here against WCAG ratios when the catalog is built."""
from themes_common import Kit, contrast


def register(g):
    k = Kit(g)
    pal, w, CLOCK, WEATHER = k.pal, k.w, k.CLOCK, k.WEATHER

    def make(id, name, description, bg, surface, elevated, ink, dim, accent, alt, font, vibes, colours, mood, swatch,
             light=False, dock="ROW", shape="ROUNDED", widgets=None, strong=True):
        # THE CONTRAST CHECK. The strong themes meet AAA (7:1) for the lettering on every surface; the
        # others meet AA (4.5:1). An accent or a second accent is held to 4.5:1 and 3:1.
        need = 7.0 if strong else 4.5
        for place in (bg, surface, elevated):
            assert contrast(ink, place) >= need, (id, "ink", place, contrast(ink, place))
            assert contrast(dim, place) >= 4.5, (id, "dim", place, contrast(dim, place))
            assert contrast(accent, place) >= 4.5, (id, "accent", place, contrast(accent, place))
            assert contrast(alt, place) >= 3.0, (id, "alt", place, contrast(alt, place))
        veil = "#00000000"
        k.add(id, name, description,
              ["audience:general", "vibe:calm"] + ["vibe:" + v for v in vibes] + ["color:" + c for c in colours],
              pal(accent, alt, ink, dim, bg, surface, elevated, veil, light=light),
              k.flat(bg),
              dict(corner="ROUNDED", iconShape=shape, iconStyle="ORIGINAL", widgetLook="SOLID", widgetCorner="ROUNDED",
                   widgetEdge="BOLD", widgetTint=0.0, widgetSolid=1.0, font=font, clockFace="BARE", panelLook="CARD",
                   notch="NONE", homeIconScale=1.5, homeLabels=True),
              mood, swatch,
              layout=dict(homeLayout="PAGES", dockStyle=dock, anchor="BOTTOM", drawerLayout="GRID", drawerColumns=3,
                          drawerIconScale=1.4, drawerLabels=True,
                          widgets=widgets or [CLOCK(0.06, 1.3), w("next", "AGENDA", 0.04, 0.24, 0.92)]),
              assistant="STANDARD", styles=("easy to see",), topics=["accessibility"])

    make("high_contrast_dark", "High Contrast Dark",
         "Pure white lettering on black with yellow highlights. The strongest contrast Orbital offers, with big icons and clear names.",
         "#000000", "#000000", "#1C1C1C", "#FFFFFF", "#D0D0D0", "#FFE600", "#00E5FF", "atkinson_hyperlegible",
         ["dark"], ["black", "white", "yellow"], ["dark", "bold", "minimal"], "#000000")
    make("high_contrast_light", "High Contrast Light",
         "Black lettering on white with deep blue highlights. Maximum contrast in bright light, with big icons and clear names.",
         "#FFFFFF", "#FFFFFF", "#E6E6E6", "#000000", "#2B2B2B", "#0033CC", "#B00020", "atkinson_hyperlegible",
         ["elegant"], ["white", "black", "blue"], ["light", "bold", "minimal"], "#FFFFFF", light=True)
    make("yellow_on_black", "Yellow on Black",
         "Bright yellow lettering on black, a classic high-visibility pairing that many people with low vision find easiest to read.",
         "#000000", "#000000", "#1A1A00", "#FFFF33", "#D9D900", "#FFFFFF", "#FFB000", "atkinson_hyperlegible",
         ["dark"], ["yellow", "black"], ["dark", "bold", "minimal"], "#1A1A00")
    make("black_on_yellow", "Black on Yellow",
         "Black lettering on a sunny yellow page, with deep blue highlights. Strong contrast that stays easy on the eyes.",
         "#FFE600", "#FFEE55", "#F2D600", "#000000", "#333300", "#0A1F8F", "#7A0019", "atkinson_hyperlegible",
         ["energetic"], ["yellow", "black", "blue"], ["light", "bold", "vivid"], "#FFE600", light=True)
    make("amber_night", "Amber Night",
         "Warm amber on black, gentle in a dark room and kind to your eyes in the evening.",
         "#000000", "#0A0600", "#1F1200", "#FFB454", "#C98A3A", "#FF9A1F", "#D96A00", "lexend",
         ["dark"], ["orange", "black"], ["dark", "calm", "minimal"], "#1F1200", dock="ORBIT")
    make("reading_cream", "Reading Cream",
         "Soft cream paper and dark ink in a typeface designed for easy reading, with no harsh white glare.",
         "#FAF3DC", "#FFF9E6", "#EFE5C6", "#1F2933", "#4A5560", "#1D4E89", "#8A3B12", "atkinson_hyperlegible",
         ["calm"], ["white", "blue"], ["light", "calm", "minimal"], "#FAF3DC", light=True)
    make("reading_dark", "Reading Dark",
         "Warm off-white lettering on soft charcoal in a clear, evenly spaced typeface. Easy reading without the glare.",
         "#17171C", "#1B1B21", "#2A2A33", "#EDE6D3", "#B9B2A0", "#8CC0FF", "#F2B880", "lexend",
         ["dark"], ["black", "blue"], ["dark", "calm", "minimal"], "#17171C")
    make("colour_blind_dark", "Colour-Blind Safe Dark",
         "A dark theme in blue and orange, a pairing that stays clear for every common kind of colour blindness.",
         "#0B0B0F", "#101015", "#1D1D26", "#F5F5F5", "#BDBDBD", "#56B4E9", "#E69F00", "atkinson_hyperlegible",
         ["dark"], ["blue", "orange", "black"], ["dark", "calm", "bold"], "#101015")
    make("colour_blind_light", "Colour-Blind Safe Light",
         "A light theme in deep blue and burnt orange, a pairing that stays clear for every common kind of colour blindness.",
         "#F8F8F4", "#FFFFFF", "#ECECE6", "#111111", "#444444", "#005A8C", "#A84300", "atkinson_hyperlegible",
         ["elegant"], ["blue", "orange", "white"], ["light", "calm", "bold"], "#F8F8F4", light=True)
    make("red_teal_safe", "Red and Teal Safe",
         "A dark theme in coral red and teal, chosen to stay distinct for people who find blue and yellow hard to tell apart.",
         "#101214", "#14171A", "#22272B", "#F2F2F2", "#BFC4C8", "#FF6B6B", "#2EC4B6", "atkinson_hyperlegible",
         ["dark"], ["red", "green", "black"], ["dark", "calm", "bold"], "#14171A")
    make("big_and_simple", "Big and Simple",
         "Large icons with their names, a big clock and warm white pages, for anyone who wants the phone to be easy to read at a glance.",
         "#FFFDF7", "#FFFFFF", "#F0EEE6", "#1A1A1A", "#4D4D4D", "#0B5CAD", "#B3261E", "atkinson_hyperlegible",
         ["elegant"], ["white", "blue"], ["light", "calm", "minimal"], "#FFFDF7", light=True,
         widgets=[CLOCK(0.05, 1.5), WEATHER(0.04, 0.26, 0.92)], strong=True)
    make("calm_low_stimulation", "Calm Low Stimulation",
         "Muted sage and soft grey with no bright colours or busy detail, for a quiet, restful phone.",
         "#262D2A", "#2B3330", "#38423E", "#E4EAE6", "#A9B8B0", "#8FBFA8", "#C8B88A", "nunito",
         ["dark", "chill"], ["green", "black"], ["dark", "calm", "minimal"], "#2B3330", dock="ORBIT", strong=False,
         widgets=[CLOCK(0.08, 1.2)])
    make("easy_reach", "Easy Reach",
         "Everything sits low on the screen within thumb reach, with big icons, bold edges and clear names.",
         "#0B1420", "#101B2A", "#1B2C44", "#F2F6FF", "#B4C2DA", "#FFC857", "#7FD1FF", "atkinson_hyperlegible",
         ["dark"], ["blue", "yellow", "black"], ["dark", "calm", "bold"], "#101B2A",
         widgets=[CLOCK(0.4, 1.3), w("next", "AGENDA", 0.04, 0.56, 0.92)])
    make("glare_free_grey", "Glare-Free Grey",
         "Mid-dark neutral grey with soft white lettering and no colour at all, easy on sensitive eyes.",
         "#2A2A2A", "#303030", "#444444", "#F2F2F2", "#C0C0C0", "#FFFFFF", "#D0D0D0", "inter",
         ["dark"], ["black", "white"], ["dark", "minimal", "calm"], "#303030", strong=True)
    make("clear_day", "Clear Day",
         "Pale sky blue with deep navy lettering and big icons, bright and crisp without being harsh.",
         "#EEF5FC", "#F7FBFE", "#DCE9F6", "#0B1F33", "#3D5873", "#0A58CA", "#B3541E", "inter",
         ["elegant"], ["blue", "white"], ["light", "calm", "minimal"], "#EEF5FC", light=True, dock="ORBIT")

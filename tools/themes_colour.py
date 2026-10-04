"""Sixteen colour-only themes. Each changes the colours and the font and nothing else, so a person keeps
their own layout and wallpaper. Eleven are dark and five are light."""
from themes_common import Kit, contrast

# id, name, accent, alt, ink, dim, drawer, surface, elevated, font, light, vibes, colours, mood, swatch
COLOURS = [
    ("crimson", "Crimson", "#E5484D", "#FF9A8B", "#FBEFEF", "#B58E90", "#130708", "#1A0A0C", "#2A1316", "manrope",
     False, ["energetic", "dark"], ["red", "black"], ["dark", "bold", "vivid"], "#B3262C"),
    ("tangerine", "Tangerine", "#FF8A3D", "#FFC27A", "#FFF3E8", "#C2A088", "#140B05", "#1B0F07", "#2B1A0E", "poppins",
     False, ["energetic", "dark"], ["orange", "black"], ["dark", "bold", "vivid"], "#E0701F"),
    ("sunflower", "Sunflower", "#F5C518", "#FFE580", "#FFF9E0", "#C9B76B", "#131005", "#1A1507", "#2A230C", "dm_sans",
     False, ["energetic", "dark"], ["yellow", "black"], ["dark", "bold", "vivid"], "#C79E0C"),
    ("emerald", "Emerald", "#2EC27E", "#8FE3B8", "#EAFBF2", "#7FAF97", "#04120B", "#07190F", "#0F2A1B", "outfit",
     False, ["calm", "dark"], ["green", "black"], ["dark", "calm", "vivid"], "#1B8A57"),
    ("teal", "Teal", "#14B8A6", "#7FE3D6", "#E8FBF8", "#78B3AC", "#041413", "#071B1A", "#0E2E2C", "quicksand",
     False, ["calm", "dark"], ["green", "blue", "black"], ["dark", "calm", "vivid"], "#0E8579"),
    ("ocean", "Ocean", "#3B82F6", "#93C5FD", "#EEF4FF", "#8497B8", "#060D1C", "#0A1428", "#14223F", "inter",
     False, ["calm", "dark"], ["blue", "black"], ["dark", "calm", "vivid"], "#2563C9"),
    ("indigo", "Indigo", "#6366F1", "#A5B4FC", "#F0F0FF", "#8E91C0", "#0A0A1E", "#0F0F2A", "#1B1B45", "space_grotesk",
     False, ["dreamy", "dark"], ["blue", "purple", "black"], ["dark", "calm", "bold"], "#4547C2"),
    ("violet", "Violet", "#A855F7", "#D8B4FE", "#F7EEFF", "#A58BC0", "#0F0618", "#160A24", "#26143D", "montserrat",
     False, ["dreamy", "dark"], ["purple", "black"], ["dark", "bold", "vivid"], "#7E34C9"),
    ("rose", "Rose", "#F43F7E", "#FDA4C0", "#FFEEF4", "#C48EA3", "#170610", "#1F0A16", "#341425", "nunito",
     False, ["dreamy", "dark"], ["pink", "black"], ["dark", "bold", "vivid"], "#C42A60"),
    ("cocoa", "Cocoa", "#C08552", "#E3B98F", "#F8EEE4", "#AD9582", "#120C08", "#1A110B", "#2C1D13", "lora",
     False, ["cozy", "dark"], ["orange", "black"], ["dark", "cozy", "calm"], "#8A5A33"),
    ("slate", "Slate", "#94A3B8", "#CBD5E1", "#F1F5F9", "#8391A6", "#0B0F14", "#10161D", "#1C2530", "ibm_plex_sans",
     False, ["calm", "dark"], ["blue", "white", "black"], ["dark", "calm", "minimal"], "#566274"),
    ("sand", "Sand", "#9A5A1A", "#5B8A72", "#2B2118", "#7A6A58", "#F4EBDD", "#FAF4E9", "#EADFCB", "source_sans_3",
     True, ["calm", "cozy"], ["orange", "white"], ["light", "calm", "minimal"], "#E6D3B3"),
    ("mint", "Mint", "#17855A", "#2B7DE9", "#12302A", "#5E7F76", "#E9F6F0", "#F2FBF7", "#D8EEE5", "dm_sans",
     True, ["calm", "chill"], ["green", "white", "pastel"], ["light", "pastel", "calm"], "#BFE5D3"),
    ("lavender", "Lavender", "#7C4DDB", "#E0589A", "#2A1F44", "#7568A0", "#F0EBFA", "#F7F3FD", "#E2DAF4", "outfit",
     True, ["dreamy", "calm"], ["purple", "white", "pastel"], ["light", "pastel", "calm"], "#D3C5F0"),
    ("sky", "Sky", "#1E7FD6", "#F28C28", "#10243A", "#5C7490", "#E8F2FB", "#F2F8FD", "#D6E7F6", "manrope",
     True, ["calm", "chill"], ["blue", "white", "pastel"], ["light", "pastel", "calm"], "#BBD8F2"),
    ("blush", "Blush", "#D6537A", "#3D8F85", "#3A1B27", "#8A5B6C", "#FBEDF1", "#FDF4F7", "#F4DCE4", "nunito",
     True, ["dreamy", "elegant"], ["pink", "white", "pastel"], ["light", "pastel", "calm"], "#F0C4D2"),
]


def register(g):
    k = Kit(g)
    for (id, name, accent, alt, ink, dim, drawer, surface, elevated, font, light, vibes, colours, mood, swatch) in COLOURS:
        # Lettering must read on every surface the theme draws: 4.5:1 or better.
        for place in (drawer, surface, elevated):
            assert contrast(ink, place) >= 7.0, (id, "ink", place)
            assert contrast(accent, place) >= 3.0, (id, "accent", place, contrast(accent, place))
            assert contrast(dim, place) >= 3.0, (id, "dim", place, contrast(dim, place))
        k.add(id, name,
              "%s accents on a %s base. Refreshes your colours and font, and keeps your layout and wallpaper "
              "just as they are." % (name, "deep dark" if not light else "soft light"),
              ["audience:general"] + ["vibe:" + v for v in vibes] + ["color:" + c for c in colours],
              k.pal(accent, alt, ink, dim, drawer, surface, elevated, "#44000000" if not light else "#11FFFFFF", light=light),
              None, dict(font=font), mood, swatch, kind="accent")

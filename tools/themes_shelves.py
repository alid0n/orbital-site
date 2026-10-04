"""Curated collections for the themes added in this batch: shelves the store shows from their start to their
end day. Only themes offered all year may be on a shelf, so none of the holiday themes are here."""
from themes_colour import COLOURS

ACCESS = ["high_contrast_dark", "high_contrast_light", "yellow_on_black", "black_on_yellow", "amber_night",
          "reading_cream", "reading_dark", "colour_blind_dark", "colour_blind_light", "red_teal_safe",
          "big_and_simple", "calm_low_stimulation", "easy_reach", "glare_free_grey", "clear_day"]


def register(g):
    start, end = "2026-10-05", "2027-12-31"
    g["COLLECTIONS"].extend([
        {"id": "easy_to_see", "name": "Easy to see",
         "description": "High-contrast, large-print and colour-blind-safe themes, with big icons and clear names. All free.",
         "themes": ACCESS, "start": start, "end": end},
        {"id": "made_for_programmers", "name": "Made for programmers",
         "description": "Terminal looks, editor palettes, monospaced type and command-line drawers.",
         "themes": ["matrix", "command_prompt", "dos_blue", "solarized_dark", "monokai", "nord", "gruvbox",
                    "paper_terminal", "dev_dark", "night_pass", "vintage_logic", "mesh_network", "pico", "overclock"],
         "start": start, "end": end},
        {"id": "colour_only", "name": "Just the colours",
         "description": "Change your colours and font and keep your layout and wallpaper exactly as they are.",
         "themes": ["graphite", "matcha"] + [c[0] for c in COLOURS], "start": start, "end": end},
        {"id": "hobbies_and_passions", "name": "Hobbies and passions",
         "description": "Music, sport, cars, cooking, fitness, pets, books, fashion, gaming and manga.",
         "themes": ["vinyl_nights", "courtside", "muscle_car", "fresh_table", "strength", "cozy_pug", "reading_room",
                    "wardrobe", "pixel_quest", "manga_panel"], "start": start, "end": end},
        {"id": "dinosaur_fossils", "name": "Dinosaur fossils",
         "description": "Museum skeletons, a working quarry and classic paintings of the age of dinosaurs.",
         "themes": ["trex_hall", "laelaps", "in_the_rock", "brontosaurus_study", "ankylosaurus"],
         "start": start, "end": end},
    ])

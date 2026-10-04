"""Writes the free Wallpaper Gallery for orbitallauncher.com: one folder per wallpaper under wallpapers/
with phone.webp (1440x3120, 9:19.5), wide.webp (2560x1600, 16:10, for tablets and unfolded foldables,
where the picture allows one) and thumb.webp (270x585), and wallpapers/index.json with each file's size,
SHA-256 and pixel size, the picture's credit, a swatch colour and whether it is dark. Run from anywhere:
    python tools/make_gallery.py [site folder]
ORBITAL_ONLY=id1,id2 remakes only those wallpapers' images (the index is always rewritten).

Every picture is free for any use, commercial use in an app included, with no attribution or licence
obligations: CC0 1.0, or public domain, as stated on the item's own record page or API on the date given
(see check_licence). The credits are still carried, because they are good manners and good provenance.
The originals stay out of git, in ORBITAL_GALLERY_SRC with their provenance in sources.json (written
when they were downloaded); only the finished WebP files are published. Where an original is not
there, the wallpaper's committed files are kept as they are rather than made again."""
import hashlib
import io
import json
import os
import sys
import urllib.parse

from PIL import Image, ImageFilter, ImageStat

Image.MAX_IMAGE_PIXELS = None  # a few museum masters are over 150 megapixels

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
ROOT = os.path.join(SITE, "wallpapers")
SOURCES = os.environ.get("ORBITAL_GALLERY_SRC", r"C:\osite-wall-src\gallery")

PHONE = (1440, 3120)  # 9:19.5
WIDE = (2560, 1600)  # 16:10
THUMB = (270, 585)
PHONE_MAX_BYTES = 2_000_000
WIDE_MAX_BYTES = 1_600_000
THUMB_MAX_BYTES = 150_000
TOTAL_MAX_BYTES = 150_000_000  # the whole gallery, every file in wallpapers/
# What the app accepts (it silently drops an entry over any of these): a picture at most 4 MiB and
# 4096 px a side, a thumbnail at most 512 KiB, index.json at most 256 KiB.
APP_MAX_PICTURE_BYTES = 4 * 1024 * 1024
APP_MAX_SIDE = 4096
APP_MAX_THUMB_BYTES = 512 * 1024
APP_MAX_INDEX_BYTES = 256 * 1024
MIN_LONG_SIDE = 2400  # the source pixels a crop uses, on its long side
MIN_SOURCE_PIXELS = 1.0  # source pixels per output pixel, along each side: nothing is ever enlarged

# THE LICENCE BAR. Only these licences, only from these sources, each checked on the item's own record.
# Written exactly so: the app shows the licence string as it is.
FREE_LICENSES = {"CC0", "Public domain"}
APPROVED_HOSTS = {
    "www.metmuseum.org": "The Metropolitan Museum of Art",
    "clevelandart.org": "Cleveland Museum of Art",
    "images.nasa.gov": "NASA",
    "science.nasa.gov": "NASA",  # the NASA Photojournal (photojournal.jpl.nasa.gov redirects here)
    "www.loc.gov": "Library of Congress",
    "commons.wikimedia.org": None,  # only US-government or author-dedicated public-domain/CC0 files
}
# NASA imagery. Never: other space agencies, STScI/Webb, astronauts of other agencies (whose photographs
# are credited to their own agencies), citizen-processed images, or anything marked © or non-commercial.
NASA_EXCLUDED = ("ESA", "CSA", "JAXA", "Roscosmos", "STScI", "Webb", "Gill", "Doran", "processing", "©",
                 "CC BY", "commercial", "Saint-Jacques", "Hadfield", "Kuipers", "Gerst", "Noguchi", "Yui",
                 "Pesquet", "Cristoforetti", "Parmitano")
# The partners NASA names in Photojournal credit lines for images it publishes under its media usage
# guidelines (any use, commercial included, without implying endorsement). A Photojournal credit must
# be made of these alone, and is carried verbatim. (USGS is a US federal agency: its work is public domain.)
NASA_CREDIT_PARTS = {"NASA", "JPL", "JPL-Caltech", "SSI", "Space Science Institute", "MSSS", "ASU",
                     "Arizona State University", "JHUAPL", "Johns Hopkins University Applied Physics Laboratory",
                     "SwRI", "Southwest Research Institute", "University of Arizona", "Univ. of Arizona",
                     "UArizona", "GSFC", "USGS"}
NASA_GUIDELINES = "https://www.nasa.gov/nasa-brand-center/images-and-media/"
RETRIEVED = "2026-10-03"

CATEGORIES = [
    {"id": "space", "name": "Space"},
    {"id": "earth", "name": "Earth from Orbit"},
    {"id": "planets", "name": "Planets"},
    {"id": "landscapes", "name": "Landscapes"},
    {"id": "botanical", "name": "Botanical"},
    {"id": "japanese", "name": "Japanese Prints"},
    {"id": "patterns", "name": "Patterns"},
    {"id": "oceans", "name": "Oceans"},
    {"id": "cities", "name": "Cities"},
]


# Credits, one helper per source. [src] is the original's name in SOURCES, without .jpg.
def met(n, title, creator):
    return "met-%d" % n, dict(title=title, creator=creator, institution="The Metropolitan Museum of Art",
                              url="https://www.metmuseum.org/art/collection/search/%d" % n, license="CC0")


def cma(n, accession, title, creator):
    return "cma-%d" % n, dict(title=title, creator=creator, institution="Cleveland Museum of Art",
                              url="https://clevelandart.org/art/%s" % accession, license="CC0")


def nasa(nasa_id, title, creator="NASA", centre="Johnson Space Center"):
    return "nasa-%s" % nasa_id, dict(title=title, creator=creator, institution="NASA, %s" % centre,
                                     url="https://images.nasa.gov/details/%s" % nasa_id, license="Public domain")


def pj(pia, slug, title, credit):
    """A NASA Photojournal image, credited exactly as NASA credits it."""
    return "pj-%s" % pia, dict(title=title, creator=credit, institution="NASA, Jet Propulsion Laboratory",
                               url="https://science.nasa.gov/photojournal/%s/" % slug, license="Public domain")


def loc(n, title):
    return "loc-%d" % n, dict(title=title, creator="Detroit Publishing Co.",
                              institution="Library of Congress, Prints and Photographs Division",
                              url="https://www.loc.gov/item/%d/" % n, license="Public domain")


def commons(src, file, title, creator, institution):
    return src, dict(title=title, creator=creator, institution=institution,
                     url="https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(file.replace(" ", "_"), safe="()'"),
                     license="Public domain")


# Crops. Coordinates are fractions of the original's width and height.
def crop(fx, fy, h=1.0, region=(0.0, 0.0, 1.0, 1.0)):
    """The largest crop of the target shape that is [h] of the image's height (or as tall as [region]
    allows), centred as near (fx, fy) as [region] lets it be."""
    return {"mode": "crop", "focus": (fx, fy), "h": h, "region": region}


def fit(left, top, right, bottom, pad=None):
    """The box (left, top, right, bottom), whole, on a canvas of the target shape filled with [pad] (an
    RGB tuple) or, by default, the colour of the box's own edge: for plates on plain paper or pictures on
    black sky, where the subject is wider than a phone."""
    return {"mode": "fit", "box": (left, top, right, bottom), "pad": pad}


def wall(id, category, title, source, phone, wide=None):
    src, credit = source
    return dict(id=id, category=category, title=title, src=src, credit=credit, phone=phone, wide=wide)


WALLPAPERS = [
    # SPACE: NASA's own photographs only (crew and NASA photographers), no partner imagery.
    wall("earthrise", "space", "Earthrise",
         nasa("as08-14-2383", "Apollo 8 Mission image, Earth over the horizon of the moon"),
         fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0)), crop(0.5, 0.6, 0.625)),
    wall("earthset", "space", "Earthset",
         nasa("art002e021278", "A Breathtaking Earthset from Orion"),
         crop(0.5, 0.5), crop(0.5, 0.5, 0.93)),
    wall("diamond_ring", "space", "Diamond Ring",
         nasa("AFRC2017-0233-009", "2017 Total Solar Eclipse", "NASA/Carla Thomas", "Armstrong Flight Research Center"),
         crop(0.48, 0.5), crop(0.5, 0.5, 0.93)),
    wall("eclipse_from_orion", "space", "Eclipse from Orion",
         nasa("art002e016324", "Solar Eclipse During Artemis II"),
         fit(0.45, 0.0, 1.0, 1.0, (0, 0, 0))),
    wall("moon_crescent_eclipse", "space", "Lunar Silhouette",
         nasa("art002e009298", "Artemis II Total Solar Eclipse, Partial Frame"),
         crop(0.66, 0.5), crop(0.5, 0.5, 0.93)),
    wall("eclipse_emergence", "space", "Sunlight's Return",
         nasa("art002e009299", "Solar Eclipse Emergence from Orion"),
         crop(0.48, 0.45), crop(0.5, 0.5, 0.93)),
    # Spitzer and WISE infrared views, credited NASA/JPL-Caltech alone.
    wall("north_america_nebula", "space", "North America Nebula",
         pj("PIA13845", "north-america-nebula-in-different-lights", "North America Nebula in Different Lights",
            "NASA/JPL-Caltech"),
         crop(0.35, 0.5), crop(0.5, 0.5, 0.6)),
    wall("helix_nebula", "space", "Helix Nebula",
         pj("PIA15817", "the-helix-nebula-unraveling-at-the-seams", "The Helix Nebula: Unraveling at the Seams",
            "NASA/JPL-Caltech"),
         crop(0.5, 0.5, 0.75), crop(0.5, 0.5, 0.6)),
    wall("eta_carinae", "space", "Clouds of Eta Carinae",
         pj("PIA17257", "the-tortured-clouds-of-eta-carinae", "The Tortured Clouds of Eta Carinae", "NASA/JPL-Caltech"),
         crop(0.5, 0.5), crop(0.5, 0.48, 0.6)),
    wall("witch_head_nebula", "space", "Witch Head Nebula",
         pj("PIA17553", "witch-head-brews-baby-stars", "'Witch Head' Brews Baby Stars", "NASA/JPL-Caltech"),
         crop(0.6, 0.5, 0.8), crop(0.55, 0.5, 0.6)),
    wall("tarantula_nebula", "space", "Tarantula Nebula",
         pj("PIA23647", "tarantula-nebula-spitzer-3-color-image", "Tarantula Nebula Spitzer 3-Color Image",
            "NASA/JPL-Caltech"),
         crop(0.3, 0.55), crop(0.5, 0.5, 0.93)),
    wall("godzilla_nebula", "space", "Godzilla Nebula",
         pj("PIA24579", "godzilla-nebula-imaged-by-spitzer", "Godzilla Nebula Imaged by Spitzer", "NASA/JPL-Caltech"),
         crop(0.3, 0.6), crop(0.5, 0.5, 0.6)),
    wall("andromeda_infrared", "space", "Andromeda in Infrared",
         pj("PIA26276", "the-infrared-face-of-the-andromeda-galaxy", "The Infrared Face of the Andromeda Galaxy",
            "NASA/JPL-Caltech"),
         crop(0.5, 0.5, 0.45), crop(0.5, 0.5, 0.6)),
    wall("orion_dreamy_stars", "space", "Orion's Dreamy Stars",
         pj("PIA13005", "orions-dreamy-stars", "Orion's Dreamy Stars", "NASA/JPL-Caltech"),
         crop(0.5, 0.5)),
    wall("galactic_center", "space", "Heart of the Milky Way",
         pj("PIA03654", "a-cauldron-of-stars-at-the-galaxys-center", "A Cauldron of Stars at the Galaxy's Center",
            "NASA/JPL-Caltech"),
         crop(0.5, 0.5), crop(0.5, 0.5, 0.85)),

    # EARTH FROM ORBIT
    wall("blue_marble", "earth", "The Blue Marble",
         nasa("as17-148-22727", "View of the Earth seen by the Apollo 17 crew traveling toward the moon"),
         fit(0.15, 0.14, 0.87, 0.88, (0, 0, 0)), fit(0.15, 0.14, 0.87, 0.88, (0, 0, 0))),
    wall("green_aurora", "earth", "Green Aurora",
         nasa("iss071e570863", "Green aurora dance above the Indian Ocean"),
         crop(0.55, 0.6, 0.8), crop(0.5, 0.6, 0.8)),
    wall("aurora_and_city_lights", "earth", "Aurora and City Lights",
         nasa("iss058e005282", "View of the Earth's limb with an aurora"),
         crop(0.72, 0.55), crop(0.6, 0.66, 0.68)),
    wall("airglow", "earth", "Airglow at Orbital Sunset",
         nasa("iss062e103874", "City lights sparkle underneath an atmospheric glow and a starry night sky"),
         crop(0.5, 0.5), crop(0.5, 0.5, 0.93)),
    wall("bahamas_from_orbit", "earth", "The Bahamas",
         nasa("iss071e449837", "The clear blue waters surrounding The Bahamas"),
         crop(0.5, 0.5), crop(0.5, 0.45, 0.85)),
    wall("tibetan_glaciers", "earth", "Himalayan Glaciers",
         nasa("iss074e0603585", "Glaciers flow downhill from the Himalayas' northern slopes onto China's Tibetan Plateau"),
         crop(0.6, 0.5), crop(0.5, 0.5, 0.93)),
    wall("hurricane_eye", "earth", "Eye of the Storm",
         nasa("iss069e090102", "A hurricane's ragged eye over the Atlantic Ocean"),
         crop(0.5, 0.5), crop(0.53, 0.5, 0.85)),
    wall("aurora_australis", "earth", "Aurora Australis",
         nasa("iss073e0247726", "The aurora australis arcs above a partly cloudy Indian Ocean"),
         crop(0.2, 0.45, 0.8), crop(0.45, 0.38, 0.7)),
    wall("eye_of_the_sahara", "earth", "Eye of the Sahara",
         nasa("iss069e005526", "The \"Eye of the Sahara\" in the African nation of Mauritania"),
         crop(0.55, 0.5), crop(0.52, 0.48, 0.9)),
    wall("mount_fuji_from_orbit", "earth", "Mount Fuji",
         nasa("iss074e0459342", "Near-overhead shot of Mount Fuji taken from the International Space Station",
              "NASA/Chris Williams"),
         crop(0.5, 0.45), crop(0.5, 0.45, 0.93)),
    wall("bassas_da_india", "earth", "Bassas da India",
         nasa("iss072e094988", "The French atoll of Bassas da India in the Mozambique Channel"),
         crop(0.5, 0.55), crop(0.5, 0.5, 0.93)),
    wall("aurora_on_the_limb", "earth", "Aurora on the Limb",
         nasa("iss062e148363", "The Earth's glow mingles with the aurora australis over the Indian Ocean"),
         crop(0.5, 0.5), crop(0.48, 0.5, 0.9)),
    wall("namib_dunes", "earth", "Namib Dunes",
         nasa("iss067e187073", "The Namib Desert on Namibia's Atlantic coast"),
         crop(0.4, 0.6), crop(0.5, 0.5, 0.93)),
    wall("eleuthera", "earth", "Eleuthera",
         nasa("iss072e715777", "Eleuthera, an island state that is part of the Bahamas archipelago"),
         crop(0.45, 0.5), crop(0.5, 0.5, 0.93)),
    wall("khuvsgul_lake_ice", "earth", "Khuvsgul Lake Ice",
         nasa("iss073e0119404", "The ice-covered Khuvsgul Lake in northern Mongolia"),
         crop(0.55, 0.5), crop(0.5, 0.5, 0.93)),
    wall("blood_moon_over_earth", "earth", "Blood Moon over Earth",
         nasa("iss073e0611610", "The lunar eclipse, also known as the Blood Moon, above Earth's horizon"),
         crop(0.5, 0.5), crop(0.5, 0.4, 0.42)),

    # PLANETS: NASA and JPL images, credited exactly as the Photojournal credits them.
    wall("saturn_portrait", "planets", "Saturn",
         pj("PIA06193", "the-greatest-saturn-portrait-yet", "The Greatest Saturn Portrait ...Yet",
            "NASA/JPL/Space Science Institute"),
         crop(0.52, 0.55), crop(0.5, 0.52, 0.95)),
    wall("day_the_earth_smiled", "planets", "The Day the Earth Smiled",
         pj("PIA17172", "the-day-the-earth-smiled", "The Day the Earth Smiled", "NASA/JPL-Caltech/SSI"),
         crop(0.5, 0.5), crop(0.5, 0.5, 1.0)),
    wall("jupiter", "planets", "Jupiter",
         pj("PIA04866", "cassini-jupiter-portrait", "Cassini Jupiter Portrait", "NASA/JPL/Space Science Institute"),
         fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0)), fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0))),
    wall("io", "planets", "Io",
         pj("PIA02308", "global-image-of-io-true-color", "Global image of Io (true color)",
            "NASA/JPL/University of Arizona"),
         fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0)), fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0))),
    wall("mars", "planets", "Mars",
         pj("PIA00407", "global-color-views-of-mars", "Global Color Views of Mars", "NASA/JPL/USGS"),
         fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0)), fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0))),
    wall("jezero_crater_rim", "planets", "Jezero Crater Rim",
         pj("PIA26373", "perseverance-rovers-view-up-crater", "Perseverance Rover's View Up Crater",
            "NASA/JPL-Caltech/ASU/MSSS"),
         crop(0.78, 0.55, 0.7, (0.0, 0.2, 1.0, 0.9)), crop(0.72, 0.55, 0.6, (0.0, 0.2, 1.0, 0.9))),
    wall("pluto", "planets", "Pluto",
         pj("PIA19952", "the-rich-color-variations-of-pluto", "The Rich Color Variations of Pluto",
            "NASA/Johns Hopkins University Applied Physics Laboratory/Southwest Research Institute"),
         fit(0.05, 0.02, 0.97, 0.98, (0, 0, 0)), fit(0.05, 0.02, 0.97, 0.98, (0, 0, 0))),
    wall("pluto_and_charon", "planets", "Pluto and Charon",
         pj("PIA19966", "charon-and-pluto-strikingly-different-worlds", "Charon and Pluto: Strikingly Different Worlds",
            "NASA/Johns Hopkins University Applied Physics Laboratory/Southwest Research Institute"),
         fit(0.08, 0.05, 0.97, 0.95, (0, 0, 0)), fit(0.08, 0.05, 0.97, 0.95, (0, 0, 0))),
    wall("plutos_blue_haze", "planets", "Pluto's Blue Haze",
         pj("PIA21590", "blue-rays-new-horizons-high-res-farewell-to-pluto",
            "Blue Rays: New Horizons' High-Res Farewell to Pluto",
            "NASA/Johns Hopkins University Applied Physics Laboratory/Southwest Research Institute"),
         fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0)), fit(0.0, 0.0, 1.0, 1.0, (0, 0, 0))),
    wall("moon_far_side", "planets", "The Moon's Far Side",
         nasa("art002e009212", "Orientale on Display"),
         fit(0.3, 0.0, 1.0, 1.0, (0, 0, 0)), fit(0.3, 0.0, 1.0, 1.0, (0, 0, 0))),
    wall("moon_edge_of_light", "planets", "The Moon at the Terminator",
         nasa("art002e020686", "Orientale Basin at the Edge of Light"),
         crop(0.4, 0.45), crop(0.5, 0.5, 0.93)),
    wall("orientale_basin", "planets", "Orientale Basin",
         nasa("art002e012090", "The Rings of the Orientale Basin"),
         crop(0.45, 0.5), crop(0.5, 0.5, 0.93)),

    # LANDSCAPES AND NATURE
    wall("twilight_in_the_wilderness", "landscapes", "Twilight in the Wilderness",
         cma(141639, "1965.233", "Twilight in the Wilderness", "Frederic Edwin Church"),
         crop(0.5, 0.5), crop(0.5, 0.5, 0.95)),
    wall("two_poplars", "landscapes", "Two Poplars",
         cma(135310, "1958.32", "Two Poplars in the Alpilles near Saint-Rémy", "Vincent van Gogh"),
         crop(0.52, 0.5, 0.96)),
    wall("denali_aurora", "landscapes", "Aurora over Denali",
         commons("commons-north-to-alaska-aurora-in-denali-7957749870", "North to Alaska Aurora in Denali (7957749870).jpg",
                 "North to Alaska Aurora in Denali", "NPS / Jacob W. Frank", "National Park Service"),
         crop(0.55, 0.5), crop(0.5, 0.5, 0.93)),
    wall("mount_starr_king", "landscapes", "Mount Starr King",
         cma(172815, "1922.684", "Mount Starr King, Yosemite", "Albert Bierstadt"),
         crop(0.55, 0.5, 1.0, (0.01, 0.0, 0.99, 1.0)), crop(0.5, 0.5, 0.85)),
    wall("schroon_mountain", "landscapes", "Schroon Mountain",
         cma(93014, "1917.1335", "View of Schroon Mountain, Essex County, New York, After a Storm", "Thomas Cole"),
         crop(0.45, 0.5), crop(0.5, 0.5, 0.95)),

    # BOTANICAL AND NATURAL HISTORY
    wall("flowers_in_a_glass", "botanical", "Flowers in a Glass",
         cma(136207, "1960.108", "Flowers in a Glass", "Ambrosius Bosschaert"),
         crop(0.52, 0.42, 0.92, (0.02, 0.0, 0.98, 0.98)), crop(0.5, 0.35, 0.5, (0.02, 0.0, 0.98, 0.98))),
    wall("morning_glory", "botanical", "Morning Glory",
         cma(118188, "1939.292", "Star-glory Morning-glory", "Henri Joseph Redouté"),
         fit(0.08, 0.04, 0.86, 0.9), fit(0.08, 0.04, 0.86, 0.9)),
    wall("crown_imperial", "botanical", "Crown Imperial",
         met(762064, "Crown Imperial (Fritillaria imperialis), from \"Les Liliacées\"", "Pierre Joseph Redouté"),
         fit(0.12, 0.04, 0.88, 0.86), fit(0.12, 0.04, 0.88, 0.86)),
    wall("spiraea_cyanotype", "botanical", "Spiraea Cyanotype",
         met(285421, "Spiraea aruncus (Tyrol)", "Anna Atkins"),
         crop(0.5, 0.5, 0.94, (0.06, 0.03, 0.94, 0.95))),
    wall("plums", "botanical", "Plums",
         cma(132850, "1955.310", "Pomona Britannica: No. 17 - Plums", "George Brookshaw"),
         fit(0.06, 0.05, 0.94, 0.88), fit(0.06, 0.05, 0.94, 0.88)),

    # JAPANESE PRINTS
    wall("great_wave", "japanese", "The Great Wave",
         met(45434, "Under the Wave off Kanagawa (Kanagawa oki nami ura), also known as The Great Wave",
             "Katsushika Hokusai"),
         fit(0.0, 0.0, 1.0, 1.0), crop(0.5, 0.5, 0.9)),
    wall("red_fuji", "japanese", "Red Fuji",
         cma(111654, "1930.189", "South Wind, Clear Sky, from Thirty-Six Views of Mount Fuji", "Katsushika Hokusai"),
         crop(0.72, 0.5, 0.92, (0.02, 0.03, 0.98, 0.95)), crop(0.55, 0.5, 0.85, (0.02, 0.03, 0.98, 0.95))),
    wall("eagle_over_fukagawa", "japanese", "Eagle over Fukagawa",
         met(55733, "Jūmantsubo Plain at Fukagawa Susaki, from One Hundred Famous Views of Edo",
             "Utagawa Hiroshige"),
         crop(0.4, 0.5, 0.86, (0.06, 0.06, 0.94, 0.93))),
    wall("sudden_shower", "japanese", "Sudden Shower",
         cma(103244, "1921.318", "Sudden Shower over Shin-Ōhashi Bridge and Atake, from One Hundred Famous Views of Edo",
             "Utagawa Hiroshige"),
         crop(0.55, 0.5, 0.94, (0.03, 0.02, 0.97, 0.97))),
    wall("fireworks_at_ryogoku", "japanese", "Fireworks at Ryōgoku",
         cma(120225, "1940.986", "Fireworks at Ryōgoku, from One Hundred Views of Famous Places in Edo",
             "Utagawa Hiroshige"),
         crop(0.45, 0.5, 0.94, (0.02, 0.02, 0.97, 0.97))),
    wall("meguro_in_snow", "japanese", "Meguro in Snow",
         cma(106968, "1924.971", "Meguro Drum Bridge and Sunset Hill, from One Hundred Views of Famous Places in Edo",
             "Utagawa Hiroshige"),
         crop(0.5, 0.5, 0.94, (0.02, 0.02, 0.98, 0.97))),
    wall("whirlpools_of_awa", "japanese", "Whirlpools of Awa",
         cma(111649, "1930.183.b", "The Whirlpools of Awa", "Utagawa Hiroshige"),
         crop(0.45, 0.5, 0.95, (0.0, 0.01, 1.0, 0.99))),
    wall("kiso_road_in_snow", "japanese", "Kiso Road in Snow",
         cma(111644, "1930.180.a", "Mountain and River on the Kiso Road", "Utagawa Hiroshige"),
         crop(0.5, 0.5, 0.95, (0.01, 0.01, 0.99, 0.99))),

    # ABSTRACT AND PATTERNS
    wall("strawberry_thief", "patterns", "Strawberry Thief",
         cma(117129, "1937.696", "Strawberry Thief", "William Morris"),
         crop(0.5, 0.5, 0.93, (0.05, 0.02, 0.95, 0.98)), crop(0.5, 0.5, 0.55, (0.05, 0.02, 0.95, 0.98))),
    wall("honeysuckle", "patterns", "Honeysuckle",
         cma(117130, "1937.697", "Honeysuckle", "William Morris"),
         crop(0.5, 0.5, 0.92, (0.03, 0.03, 0.97, 0.97)), crop(0.5, 0.5, 0.55, (0.03, 0.03, 0.97, 0.97))),
    wall("kennet", "patterns", "Kennet",
         cma(117131, "1937.698", "Kennet", "William Morris"),
         crop(0.48, 0.5, 0.92, (0.02, 0.03, 0.95, 0.97)), crop(0.48, 0.5, 0.55, (0.02, 0.03, 0.95, 0.97))),
    wall("snakeshead", "patterns", "Snakeshead",
         cma(117128, "1937.695", "Snakeshead", "William Morris"),
         crop(0.5, 0.5, 0.94, (0.04, 0.02, 0.96, 0.98)), crop(0.5, 0.5, 0.58, (0.04, 0.02, 0.96, 0.98))),
    wall("peacock_and_dragon", "patterns", "Peacock and Dragon",
         cma(130609, "1953.330", "Peacock and Dragon", "William Morris"),
         crop(0.5, 0.5, 0.95, (0.02, 0.01, 0.98, 0.99)), crop(0.5, 0.5, 0.48, (0.02, 0.01, 0.98, 0.99))),
    wall("ikat_hanging", "patterns", "Ikat",
         cma(164664, "2006.150", "Wall Hanging (pardah)", "Unknown maker, Central Asia"),
         crop(0.5, 0.5, 0.95, (0.04, 0.02, 0.96, 0.98))),
    wall("velvet_sunbursts", "patterns", "Sunburst Velvet",
         cma(166196, "2008.146", "Brocaded velvet cover with sunbursts", "Unknown maker, Ottoman Turkey"),
         crop(0.5, 0.5, 0.95, (0.03, 0.02, 0.97, 0.98))),

    # OCEANS
    wall("coral_and_fish", "oceans", "Coral and Fish",
         commons("commons-coral-and-fish-39506096061", "Coral And Fish (39506096061).jpg", "Coral and Fish",
                 "Greg McFall / NOAA", "NOAA, National Marine Sanctuary of American Samoa"),
         crop(0.5, 0.5), crop(0.5, 0.6, 0.5)),
    wall("reef_in_sunlight", "oceans", "Reef in Sunlight",
         commons("commons-nmsas-reef-in-sunlight-31782520361", "NMSAS - Reef In Sunlight (31782520361).jpg",
                 "Reef in Sunlight", "Greg McFall / NOAA", "NOAA, National Marine Sanctuary of American Samoa"),
         crop(0.55, 0.5), crop(0.5, 0.6, 0.4)),
    wall("florida_keys_reef", "oceans", "Florida Keys Reef",
         commons("commons-fknms-reef-34136062951", "FKNMS - Reef (34136062951).jpg", "Reef",
                 "Matt McIntosh / NOAA", "NOAA, Florida Keys National Marine Sanctuary"),
         crop(0.5, 0.5), crop(0.5, 0.5, 0.93)),
    wall("morning_after_a_storm", "oceans", "Morning after a Storm",
         cma(106088, "1924.195", "Early Morning After a Storm at Sea", "Winslow Homer"),
         crop(0.6, 0.5), crop(0.5, 0.5, 0.93)),
    wall("seascape_open_sky", "oceans", "Seascape with Open Sky",
         cma(92480, "2020.116", "Seascape with Open Sky", "Eugène Boudin"),
         crop(0.65, 0.5, 0.96, (0.01, 0.01, 0.99, 0.96)), crop(0.5, 0.5, 0.8, (0.01, 0.01, 0.99, 0.96))),

    # CITIES AND ARCHITECTURE (historic)
    wall("suleymaniye", "cities", "Süleymaniye Mosque",
         loc(2003653113, "Süleymaniye Camii (mosque), Constantinople, Turkey"),
         crop(0.62, 0.5, 0.97, (0.0, 0.012, 0.96, 0.98))),
    wall("three_bridges_venice", "cities", "Three Bridges, Venice",
         loc(2001701040, "Three Bridges, Venice, Italy"),
         crop(0.5, 0.5, 0.92, (0.03, 0.02, 0.97, 0.94))),
    wall("burning_parliament", "cities", "The Burning of Parliament",
         cma(122351, "1942.647", "The Burning of the Houses of Lords and Commons, 16 October 1834",
             "Joseph Mallord William Turner"),
         crop(0.48, 0.45, 0.95), crop(0.5, 0.5, 0.85)),
    wall("cathedral_interior", "cities", "Interior of a Cathedral",
         cma(119725, "1940.560", "Interior of a Cathedral", "Samuel Prout"),
         crop(0.5, 0.5, 0.93, (0.03, 0.02, 0.97, 0.97))),
    wall("venetian_capriccio", "cities", "Venetian Capriccio",
         cma(111702, "1930.23", "Capriccio: A Palace with a Courtyard by the Lagoon", "Antonio Canaletto"),
         crop(0.68, 0.5, 0.96, (0.01, 0.01, 0.99, 0.99)), crop(0.5, 0.5, 0.85, (0.01, 0.01, 0.99, 0.99))),
]


def check_licence(entry, provenance):
    """Refuses any entry that is not CC0 or public domain from an approved source, or whose recorded
    provenance (sources.json, written from the item's own record when it was downloaded) disagrees."""
    wid, credit = entry["id"], entry["credit"]
    assert set(credit) == {"title", "creator", "institution", "url", "license"}, (wid, credit)
    assert all(isinstance(v, str) and v.strip() for v in credit.values()), (wid, credit)
    assert credit["license"] in FREE_LICENSES, "%s: %r is not CC0 or public domain" % (wid, credit["license"])
    url = urllib.parse.urlparse(credit["url"])
    assert url.scheme == "https" and url.netloc in APPROVED_HOSTS, "%s: %s is not an approved source" % (wid, credit["url"])
    named = APPROVED_HOSTS[url.netloc]
    assert named is None or credit["institution"].startswith(named), (wid, credit["institution"])
    if url.netloc in ("images.nasa.gov", "science.nasa.gov") or "NASA" in credit["institution"]:
        seen = credit["creator"] + " " + credit["institution"] + " " + credit["title"]
        refused = [p for p in NASA_EXCLUDED if p in seen]
        assert not refused, "%s: credited to %s, whose images NASA does not release freely" % (wid, refused)
        assert credit["creator"].startswith("NASA"), "%s: %r is not a NASA credit" % (wid, credit["creator"])
    if url.netloc == "science.nasa.gov":
        parts = [p.strip() for p in credit["creator"].split("/")]
        outside = [p for p in parts if p not in NASA_CREDIT_PARTS]
        assert not outside, "%s: the credit names %s, outside the partners NASA publishes freely" % (wid, outside)
    if provenance is None:
        return
    rec = provenance.get(entry["src"])
    assert rec, "%s: %s has no provenance in sources.json" % (wid, entry["src"])
    assert rec["license"].startswith(("CC0", "Public domain")), (wid, rec["license"])
    assert rec.get("evidence") and rec.get("retrieved"), "%s: the licence check is not recorded" % wid
    assert urllib.parse.unquote(rec["url"]).replace(" ", "_") == urllib.parse.unquote(credit["url"]), \
        (wid, rec["url"], credit["url"])
    if url.netloc == "science.nasa.gov":
        assert rec["creator"] == credit["creator"], "%s: the credit is not NASA's own line %r" % (wid, rec["creator"])
        assert NASA_GUIDELINES in rec.get("note", ""), "%s: the NASA media guidelines are not noted" % wid


def check_entry(entry):
    wid = entry["id"]
    assert wid.replace("_", "").isalnum() and wid == wid.lower() and len(wid) <= 40, wid
    assert entry["category"] in {c["id"] for c in CATEGORIES}, (wid, entry["category"])
    assert entry["title"] and len(entry["title"]) <= 28, wid  # shown as written in every language
    for spec in (entry["phone"], entry["wide"]):
        if spec and spec["mode"] == "crop":
            fx, fy = spec["focus"]
            l, t, r, b = spec["region"]
            assert 0 <= l < r <= 1 and 0 <= t < b <= 1 and 0 < spec["h"] <= 1 and 0 <= fx <= 1 and 0 <= fy <= 1, wid
        elif spec:
            l, t, r, b = spec["box"]
            assert 0 <= l < r <= 1 and 0 <= t < b <= 1, wid


def edge_colour(img):
    """The median colour of a picture's outermost few pixels, for padding it out."""
    w, h = img.size
    band = max(4, min(w, h) // 100)
    strips = [img.crop((0, 0, w, band)), img.crop((0, h - band, w, h)),
              img.crop((0, 0, band, h)), img.crop((w - band, 0, w, h))]
    sample = Image.new("RGB", (w * 2 + h * 2, band))
    x = 0
    for s in strips:
        if s.width < s.height:
            s = s.rotate(90, expand=True)
        sample.paste(s, (x, 0))
        x += s.width
    return tuple(int(v) for v in ImageStat.Stat(sample).median)


def sharpen_for(src):
    """The light unsharp mask a picture gets after its Lanczos downscale: photographs (fine grain and
    stars) a little more than paintings and prints (canvas, paper and brushwork, which ring if pushed)."""
    if src.startswith(("met-", "cma-", "loc-")):
        return ImageFilter.UnsharpMask(radius=0.8, percent=40, threshold=3)
    return ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=2)


def check_scale(ratio, wid, kind):
    """Every output pixel must come from at least one source pixel: nothing is ever enlarged."""
    assert ratio >= MIN_SOURCE_PIXELS, "%s %s: %.2f source pixels per output pixel, under %.1f" % (
        wid, kind, ratio, MIN_SOURCE_PIXELS)


def render(img, spec, size, wid, kind, sharpen):
    """[img] cut to [spec], downscaled to exactly [size] with Lanczos and lightly sharpened."""
    W, H = img.size
    tw, th = size
    if spec["mode"] == "crop":
        l, t, r, b = spec["region"]
        rl, rt, rr, rb = l * W, t * H, r * W, b * H
        ch = min(spec["h"] * H, rb - rt)
        cw = ch * tw / th
        if cw > rr - rl:
            cw = rr - rl
            ch = cw * th / tw
        cx = min(max(spec["focus"][0] * W, rl + cw / 2), rr - cw / 2)
        cy = min(max(spec["focus"][1] * H, rt + ch / 2), rb - ch / 2)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        assert max(cw, ch) >= MIN_LONG_SIDE, "%s %s: the crop is %dx%d, under %d on its long side" % (
            wid, kind, cw, ch, MIN_LONG_SIDE)
        check_scale(cw / tw, wid, kind)
        return img.resize(size, Image.LANCZOS, box=box).filter(sharpen)
    l, t, r, b = spec["box"]
    part = img.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
    pad = spec["pad"] or edge_colour(part)
    scale = min(tw / part.width, th / part.height)
    check_scale(1 / scale, wid, kind)
    assert max(part.size) >= MIN_LONG_SIDE, "%s %s: the box is %dx%d, under %d on its long side" % (
        wid, kind, part.width, part.height, MIN_LONG_SIDE)
    pw, ph = round(part.width * scale), round(part.height * scale)
    part = part.resize((pw, ph), Image.LANCZOS).filter(sharpen)
    canvas = Image.new("RGB", size, pad)
    x, y = (tw - pw) // 2, (th - ph) // 2
    # Feather the picture's edge into the pad, so paper or sky meets it without a seam.
    feather = max(8, min(pw, ph) // 40)
    mask = Image.new("L", (pw, ph), 0)
    mask.paste(255, (feather, feather, pw - feather, ph - feather))
    mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
    if pw >= tw:
        mask.paste(255, (0, 0, feather, ph)), mask.paste(255, (pw - feather, 0, pw, ph))
    if ph >= th:
        mask.paste(255, (0, 0, pw, feather)), mask.paste(255, (0, ph - feather, pw, ph))
    canvas.paste(part, (x, y), mask)
    return canvas


def save_webp(img, path, max_bytes):
    """[img] as WebP at [path], at the best quality that keeps it to [max_bytes]. Nothing is softened to
    save bytes: detail is what a wallpaper is for, so the budget is generous and only the quality moves.
    The search encodes quickly; the file is then written with the slowest, smallest setting. Returns the
    size."""
    for quality in (92, 90, 88, 85, 82, 78, 74, 70):
        trial = io.BytesIO()
        img.save(trial, "WEBP", quality=quality, method=4)
        if trial.tell() <= max_bytes * 1.02:
            img.save(path, "WEBP", quality=quality, method=6)
            size = os.path.getsize(path)
            if size <= max_bytes:
                return size
    raise AssertionError((path, "over %d bytes even at quality 70" % max_bytes))


def describe(path):
    with open(path, "rb") as f:
        data = f.read()
    with Image.open(path) as img:
        w, h = img.size
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest(), "w": w, "h": h}


def make_images(entry, folder):
    """Makes [entry]'s phone, wide and thumbnail WebP files in [folder] from the original."""
    path = os.path.join(SOURCES, entry["src"] + ".jpg")
    with Image.open(path) as img:
        img = img.convert("RGB")  # always at full size: every source pixel counts
    sharpen = sharpen_for(entry["src"])
    phone = render(img, entry["phone"], PHONE, entry["id"], "phone", sharpen)
    save_webp(phone, os.path.join(folder, "phone.webp"), PHONE_MAX_BYTES)
    wide_path = os.path.join(folder, "wide.webp")
    if entry["wide"]:
        save_webp(render(img, entry["wide"], WIDE, entry["id"], "wide", sharpen), wide_path, WIDE_MAX_BYTES)
    elif os.path.exists(wide_path):
        os.remove(wide_path)
    save_webp(phone.resize(THUMB, Image.LANCZOS), os.path.join(folder, "thumb.webp"), THUMB_MAX_BYTES)


def swatch_and_dark(path):
    """The phone picture's average colour as #RRGGBB, and whether it is dark enough that the app should
    draw light text and icons over it (mean luminance under 45%)."""
    with Image.open(path) as img:
        small = img.convert("RGB").resize((36, 78), Image.BOX)
    r, g, b = (int(round(v)) for v in ImageStat.Stat(small).mean)
    lum = ImageStat.Stat(small.convert("L")).mean[0] / 255
    return "#%02X%02X%02X" % (r, g, b), lum < 0.45


def load_provenance():
    path = os.path.join(SOURCES, "sources.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return {rec["id"]: rec for rec in json.load(f)["images"]}


def main():
    provenance = load_provenance()
    ids = [e["id"] for e in WALLPAPERS]
    assert len(ids) == len(set(ids)), "two wallpapers share an id"
    for entry in WALLPAPERS:
        check_entry(entry)
        check_licence(entry, provenance)
    os.makedirs(ROOT, exist_ok=True)
    only = set(os.environ.get("ORBITAL_ONLY", "").split(",")) - {""}
    index = []
    for entry in WALLPAPERS:
        folder = os.path.join(ROOT, entry["id"])
        os.makedirs(folder, exist_ok=True)
        have_src = os.path.exists(os.path.join(SOURCES, entry["src"] + ".jpg"))
        if have_src and (not only or entry["id"] in only):
            make_images(entry, folder)
        assert os.path.exists(os.path.join(folder, "phone.webp")), \
            "%s: no files, and the original %s was not made here (it is not in %s, or ORBITAL_ONLY left it out)" % (
            entry["id"], entry["src"], SOURCES)
        files = {k: describe(os.path.join(folder, k + ".webp")) if os.path.exists(os.path.join(folder, k + ".webp"))
                 else None for k in ("phone", "wide", "thumb")}
        for k, f in files.items():
            if f:
                f["url"] = "%s/%s.webp" % (entry["id"], k)
                files[k] = {key: f[key] for key in ("url", "size", "sha256", "w", "h")}
        swatch, dark = swatch_and_dark(os.path.join(folder, "phone.webp"))
        index.append({"id": entry["id"], "title": entry["title"], "category": entry["category"],
                      "credit": entry["credit"], "phone": files["phone"], "wide": files["wide"],
                      "thumb": files["thumb"], "swatch": swatch, "dark": dark})
        print("%-28s %7d phone %7s wide %6d thumb %s%s" % (
            entry["id"], files["phone"]["size"], files["wide"]["size"] if files["wide"] else "-",
            files["thumb"]["size"], swatch, " dark" if dark else ""))
    with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"version": 1, "categories": CATEGORIES, "wallpapers": index}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    check_written()


def check_written():
    """Reads back what was written, as the app will: every file the index names is there at the size,
    SHA-256 and pixel size it gives, every credit passes the licence bar, nothing is left over, and the
    whole gallery fits its budget."""
    with open(os.path.join(ROOT, "index.json"), encoding="utf-8") as f:
        text = f.read()
    assert len(text.encode("utf-8")) <= APP_MAX_INDEX_BYTES, ("index.json", len(text.encode("utf-8")))
    index = json.loads(text)
    assert set(index) == {"version", "categories", "wallpapers"} and index["version"] == 1
    categories = {c["id"] for c in index["categories"]}
    assert all(set(c) == {"id", "name"} for c in index["categories"])
    total = len(text.encode("utf-8"))
    listed = set()
    for item in index["wallpapers"]:
        wid = item["id"]
        assert set(item) == {"id", "title", "category", "credit", "phone", "wide", "thumb", "swatch", "dark"}, wid
        assert item["category"] in categories, wid
        assert isinstance(item["dark"], bool), wid
        sw = item["swatch"]
        assert len(sw) == 7 and sw[0] == "#" and all(c in "0123456789ABCDEF" for c in sw[1:]), (wid, sw)
        check_licence({"id": wid, "credit": item["credit"]}, None)
        for kind, size, limit in (("phone", PHONE, PHONE_MAX_BYTES), ("wide", WIDE, WIDE_MAX_BYTES),
                                  ("thumb", THUMB, THUMB_MAX_BYTES)):
            f = item[kind]
            if f is None:
                assert kind == "wide", (wid, kind)
                assert not os.path.exists(os.path.join(ROOT, wid, "wide.webp")), (wid, "stray wide.webp")
                continue
            assert set(f) == {"url", "size", "sha256", "w", "h"} and f["url"] == "%s/%s.webp" % (wid, kind), (wid, kind)
            path = os.path.join(ROOT, f["url"])
            with open(path, "rb") as fh:
                data = fh.read()
            assert len(data) == f["size"] <= limit, (wid, kind, "size")
            assert f["size"] <= (APP_MAX_THUMB_BYTES if kind == "thumb" else APP_MAX_PICTURE_BYTES), (wid, kind)
            assert max(f["w"], f["h"]) <= APP_MAX_SIDE, (wid, kind)
            assert hashlib.sha256(data).hexdigest() == f["sha256"], (wid, kind, "sha256")
            with Image.open(path) as img:
                assert img.format == "WEBP" and img.size == size == (f["w"], f["h"]), (wid, kind, img.size)
            listed.add(os.path.normcase(os.path.abspath(path)))
            total += len(data)
    for folder, _, names in os.walk(ROOT):
        for name in names:
            path = os.path.normcase(os.path.abspath(os.path.join(folder, name)))
            assert name == "index.json" and folder == ROOT or path in listed, ("not in the index", path)
    assert total <= TOTAL_MAX_BYTES, ("the gallery is %d bytes" % total)
    print("%d wallpapers, %d bytes in all" % (len(index["wallpapers"]), total))


if __name__ == "__main__":
    main()

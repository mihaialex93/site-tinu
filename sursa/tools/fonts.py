"""Taie fonturile la caracterele necesare (română + Latin-1) și la intervalul de grosimi folosit."""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

SRC = os.path.join(os.path.dirname(__file__), "..", "vendor", "ttf")
OUT = os.path.join(os.path.dirname(__file__), "..", "src", "fonts")
os.makedirs(OUT, exist_ok=True)

UNICODES = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) +
    [0x102, 0x103, 0x218, 0x219, 0x21A, 0x21B, 0x15E, 0x15F, 0x162, 0x163,
     0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E,
     0x2022, 0x2026, 0x2030, 0x20AC, 0x2122, 0x2212, 0x2009, 0x202F, 0x2192]
)

# Simboluri de măsură folosite doar în titluri: Δ (delta), Ω (ohm), ₂ (indice).
SYMBOLS = [0x394, 0x3A9, 0x2082]

JOBS = [
    ("SofiaSans[wght].ttf", "sofia-sans.woff2", (400, 700), []),
    ("SofiaSansExtraCondensed[wght].ttf", "sofia-sans-extra-condensed.woff2", (500, 900), SYMBOLS),
]

for src, out, (lo, hi), extra in JOBS:
    font = TTFont(os.path.join(SRC, src))
    font = instancer.instantiateVariableFont(font, {"wght": (lo, hi)})
    opts = subset.Options()
    opts.layout_features = ["kern", "liga", "locl", "ccmp", "mark", "mkmk", "tnum", "lnum", "pnum", "case", "frac", "sups", "subs"]
    opts.flavor = "woff2"
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    opts.notdef_outline = True
    opts.drop_tables += ["DSIG"]
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=UNICODES + extra)
    sub.subset(font)
    font.flavor = "woff2"
    path = os.path.join(OUT, out)
    font.save(path)
    print(out, os.path.getsize(path), "octeți")

#!/usr/bin/env python3
"""Draw entry.png for news-image-20261118: a one-page newspaper front
summing up the world news of Wednesday 18 November 2026.

Layout (1024x1024): dark masthead with the date, one lead story in a
tinted block, five more story rows below, thin footer line.
Run: python3 tools/make_image.py  ->  writes entry.png at the repo root.
No network; Pillow + Noto Sans only.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (252, 250, 244)
NAVY = (16, 28, 54)
GOLD = (198, 158, 38)
INK = (22, 22, 22)
GREY = (96, 93, 86)
RULE = (208, 202, 188)
LEAD_BG = (232, 236, 242)
ALT_BG = (243, 240, 231)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns the lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


LEAD = (
    "DIPLOMACY  ·  SHENZHEN",
    (26, 110, 138),
    "Xi greets Trump on the tarmac",
    "Xi and Putin meet in Shenzhen a day before the first-ever "
    "three-way summit with Trump — on Ukraine, Iran and trade.",
)

STORIES = [
    ("MIDDLE EAST", (178, 122, 26),
     "US jets strike Iran's Qeshm Island",
     "Iran answers by firing at US sites in Kuwait and Bahrain."),
    ("EUROPE  ·  WAR", (176, 58, 46),
     "Kerch Bridge hit a second day",
     "Part of the road span collapses into the strait, Kyiv says."),
    ("UNITED STATES", (90, 90, 90),
     "Peltola wins Alaska Senate seat",
     "Democrats take a 56–44 majority in the incoming Senate."),
    ("SOUTH ASIA  ·  WEATHER", (26, 110, 138),
     "Cyclone Akvan bears down on India",
     "Landfall due Friday on the Andhra Pradesh coast, winds to 145 km/h."),
    ("TECHNOLOGY", (90, 90, 90),
     "Nvidia posts record $115.8bn quarter",
     "Beats forecasts in its first report since Jensen Huang's exit."),
]


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r],
              outline=GOLD, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
          start=0, end=360, fill=GOLD, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 154], fill=GOLD)
    draw_globe(d, 948, 62, 34)
    d.text((36, 24), "THE WORLD IN ONE DAY", font=fnt(BOLD, 24), fill=GOLD)
    d.text((34, 54), "WEDNESDAY 18 NOVEMBER 2026",
           font=fnt(BOLD, 52), fill=(255, 255, 255))
    d.text((36, 118), "Six stories that defined the day",
           font=fnt(REG, 26), fill=(203, 208, 220))

    # ---- Lead story ----
    y = 154
    d.rectangle([0, y, W, y + 190], fill=LEAD_BG)
    tag, color, head, deck = LEAD
    d.text((36, y + 22), tag, font=fnt(BOLD, 24), fill=color)
    for i, line in enumerate(wrap(d, head, fnt(BOLD, 44), W - 72)):
        d.text((36, y + 56 + i * 52), line, font=fnt(BOLD, 44), fill=INK)
    deck_lines = wrap(d, deck, fnt(REG, 26), W - 72)
    d.text((36, y + 56 + 52 + 14), deck_lines[0], font=fnt(REG, 26), fill=GREY)
    if len(deck_lines) > 1:
        d.text((36, y + 56 + 52 + 46), deck_lines[1], font=fnt(REG, 26), fill=GREY)
    y += 190
    d.rectangle([0, y, W, y + 4], fill=GOLD)

    # ---- Five story rows ----
    row_h = 118
    for idx, (tag, color, head, deck) in enumerate(STORIES):
        top = y + 4 + idx * row_h
        if idx % 2 == 1:
            d.rectangle([0, top, W, top + row_h], fill=ALT_BG)
        d.text((36, top + 16), tag, font=fnt(BOLD, 22), fill=color)
        d.text((36, top + 44), head, font=fnt(BOLD, 33), fill=INK)
        d.text((36, top + 84), deck, font=fnt(REG, 24), fill=GREY)
        if idx < len(STORIES) - 1:
            d.line([36, top + row_h, W - 36, top + row_h], fill=RULE, width=1)

    # ---- Footer ----
    fy = y + 4 + len(STORIES) * row_h + 14
    d.text((36, fy), "Drawn from the day's reporting  ·  Wednesday 18 November 2026",
           font=fnt(REG, 22), fill=GREY)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

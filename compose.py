#!/usr/bin/env python3
"""Compose the news-image-20261118 front page, round 3 (top-30 rebuild).

1024x1024 PNG, <=1 MiB. Strict modular grid: masthead, hero (Shenzhen +
three leaders), lead story with drop cap, two-column story grid, indices
box, footer ticker. All text PIL-rendered. Subtle paper-grain texture.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(BASE, "assets", "media-generation-hero-shenzhen-trilateral-v3-0-341dd25c-8b2d-46e7-b205-49574ca5f1db.webp")
OUT = os.path.join(BASE, "entry.png")

W, H = 1024, 1024
NAVY = (16, 32, 64)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (80, 80, 80)
FAINT = (200, 200, 200)
PAPER = (248, 246, 241)
GOLD = (212, 175, 105)

def font(name, size):
    paths = [
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/{name}.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_MAST = font("DejaVuSerif-Bold", 54)
F_DATE = font("DejaVuSans-Bold", 18)
F_KICK = font("DejaVuSans-Bold", 14)
F_HEAD_LEAD = font("DejaVuSans-Bold", 28)
F_HEAD_COL = font("DejaVuSans-Bold", 20)
F_SUM_LEAD = font("DejaVuSans", 17)
F_SUM_COL = font("DejaVuSans", 15)
F_FOOT = font("DejaVuSans", 14)
F_IDX_HEAD = font("DejaVuSans-Bold", 14)
F_IDX = font("DejaVuSans", 14)
F_DROP = font("DejaVuSerif-Bold", 46)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_story(d, x, y, col_w, kicker, head, summ):
    """One compact story block; returns y after the block."""
    d.text((x, y), kicker, font=F_KICK, fill=RED)
    y += 18
    for line in wrap(d, head, F_HEAD_COL, col_w):
        d.text((x, y), line, font=F_HEAD_COL, fill=INK)
        y += 24
    for line in wrap(d, summ, F_SUM_COL, col_w):
        d.text((x, y), line, font=F_SUM_COL, fill=GREY)
        y += 18
    return y

def main():
    hero = Image.open(HERO).convert("RGB")
    print("hero size:", hero.size)
    # center-crop hero to 1024x280
    tw, th = 1024, 280
    scale = max(tw / hero.width, th / hero.height)
    nw, nh = int(hero.width * scale), int(hero.height * scale)
    hero = hero.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - tw) // 2
    y0 = (nh - th) // 2
    hero = hero.crop((x0, y0, x0 + tw, y0 + th))

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    title = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=F_MAST)) / 2, 10), title, font=F_MAST, fill=(255, 255, 255))
    date = "WEDNESDAY  •  18 NOVEMBER 2026  •  VOL. 1, ISSUE 24"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 70), date, font=F_DATE, fill=GOLD)

    # ---- hero ----
    img.paste(hero, (0, 96))
    d.rectangle([0, 376, W, 380], fill=RED)

    # ---- lead story (full width, drop cap) ----
    margin = 48
    max_w = W - 2 * margin
    y = 392
    d.text((margin, y), "DIPLOMACY", font=F_KICK, fill=RED)
    y += 18
    lead_head = "TRUMP, XI AND PUTIN TO MEET IN FIRST-EVER SHENZHEN SUMMIT"
    for line in wrap(d, lead_head, F_HEAD_LEAD, max_w):
        d.text((margin, y), line, font=F_HEAD_LEAD, fill=INK)
        y += 32
    lead_sum = "China confirms a China-Russia-U.S. Summit for 19 November at Kylin Villa. Nuclear arms and Iran are on the table; Ukraine is not. No deals are expected."
    first = lead_sum[0]
    rest = lead_sum[1:]
    dw = int(d.textlength(first, font=F_DROP)) + 8
    d.text((margin, y - 6), first, font=F_DROP, fill=INK)
    words = rest.split()
    pos = 0
    lines_out = []
    for _ in range(2):
        cur = ""
        while pos < len(words):
            t = (cur + " " + words[pos]).strip()
            if d.textlength(t, font=F_SUM_LEAD) <= max_w - dw:
                cur = t
                pos += 1
            else:
                break
        if cur:
            lines_out.append((cur, margin + dw))
        else:
            break
    cur = ""
    while pos < len(words):
        t = (cur + " " + words[pos]).strip()
        if d.textlength(t, font=F_SUM_LEAD) <= max_w:
            cur = t
            pos += 1
        else:
            lines_out.append((cur, margin))
            cur = ""
    if cur:
        lines_out.append((cur, margin))
    ly = y
    for text, x in lines_out:
        d.text((x, ly), text, font=F_SUM_LEAD, fill=GREY)
        ly += 21
    y = ly + 6
    d.line([margin, y + 4, W - margin, y + 4], fill=FAINT, width=1)
    col_top = y + 14

    # ---- two-column grid ----
    col_w = 452
    lx, rx = margin, 524
    d.line([512, col_top, 512, 976], fill=FAINT, width=1)

    # left column: Iran, Markets, Indices box
    ly = col_top
    ly = draw_story(d, lx, ly, col_w, "GULF CRISIS",
        "IRAN DENIES DIRTY-BOMB PLOT; TRUMP WARNS OF 'UNPRECEDENTED' PRICE",
        "US officials allege a radiological plot on Washington. Tehran calls it fabricated; Rubio sees no imminent threat.")
    ly += 6
    d.line([lx, ly, lx + col_w, ly], fill=FAINT, width=1)
    ly += 8
    ly = draw_story(d, lx, ly, col_w, "MARKETS",
        "DOW PLUNGES 561 POINTS IN THIRD STRAIGHT DROP",
        "Dow closes at 50,198, down 2,149 points in three days. S&P slips 0.23% while Nasdaq rises 0.42%.")
    ly += 6
    box_top = ly
    box_h = 30 + 5 * 18 + 10  # header + 5 rows + padding (fits content)
    d.rectangle([lx, box_top, lx + col_w, box_top + box_h - 2], outline=FAINT, width=1)
    d.text((lx + 12, box_top + 8), "INDICES", font=F_IDX_HEAD, fill=RED)
    idx_rows = [
        ("DOW", "50,198", "-1.11%", True),
        ("S&P 500", "7,324", "-0.23%", True),
        ("NASDAQ", "24,430", "+0.42%", False),
        ("GOLD", "$3,772", "-2.38%", True),
        ("10-YR", "5.10%", "", False),
    ]
    iy = box_top + 30
    for name, val, chg, neg in idx_rows:
        d.text((lx + 12, iy), name, font=F_IDX, fill=INK)
        right = f"{val}  {chg}" if chg else val
        d.text((lx + col_w - 12 - d.textlength(right, font=F_IDX), iy), right, font=F_IDX, fill=RED if neg else INK)
        iy += 18

    # right column: Nvidia, Ukraine, Cyclone
    ry = col_top
    ry = draw_story(d, rx, ry, col_w, "BUSINESS",
        "NVIDIA REVENUE DOUBLES TO $115.8BN — BUT STOCK KEEPS FALLING",
        "Record quarter beats estimates; Q4 guide is $130B. The board rules out reinstating ousted CEO Jensen Huang.")
    ry += 6
    d.line([rx, ry, rx + col_w, ry], fill=FAINT, width=1)
    ry += 8
    ry = draw_story(d, rx, ry, col_w, "WAR IN UKRAINE",
        "UKRAINE CRIPPLES CRIMEAN BRIDGE AS KYIV BRIDGES ARE HIT",
        "The road arch collapses into the sea after two days of strikes. Russia pounds Kyiv's bridges; UN counts 372 killed in October.")
    ry += 6
    d.line([rx, ry, rx + col_w, ry], fill=FAINT, width=1)
    ry += 8
    ry = draw_story(d, rx, ry, col_w, "WEATHER",
        "CYCLONE AKVAN BEARS DOWN ON ANDHRA PRADESH",
        "The severe storm is forecast to make landfall at noon on 20 November with winds of 120-130 km/h. Seven districts on red alert.")
    print("left column end:", ly, "right column end:", ry, "limit: 976")

    # ---- footer ticker ----
    d.rectangle([0, H - 48, W, H], fill=NAVY)
    foot = "ALSO:  Quad unveils maritime, AI and cyber pact in Manila  •  Canada and China agree tariff cuts  •  Dhoni retires from IPL"
    flines = wrap(d, foot, F_FOOT, W - 2 * 24)
    fy = H - 44
    for line in flines[:2]:
        d.text((24, fy), line, font=F_FOOT, fill=(255, 255, 255))
        fy += 18

    # ---- paper grain (very subtle, keeps PNG small) ----
    noise = Image.effect_noise((W, H), 14).convert("RGB")
    img = Image.blend(img, noise, 0.01)

    img.save(OUT, optimize=True)
    print("saved:", OUT, os.path.getsize(OUT), "bytes", img.size)

if __name__ == "__main__":
    main()

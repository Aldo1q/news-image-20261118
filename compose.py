#!/usr/bin/env python3
"""Compose the news-image-20261118 front page, round 5 (broadsheet rebuild).

Design (DeepSeek analysis + creative lanes, after round 4 ranked 8105/11402):
square broadsheet, not a dashboard. Off-white newsprint, black rules, ONE red
accent reserved for the lead kicker and the Dow chart callout. Dominant
Trump-Xi-Putin/Shenzhen lead (text left, venue hero right), a "Why it matters"
box, data modules (Dow line chart, Nvidia revenue bars), three compact
briefs, and a World Briefs rail instead of a ticker. All text PIL-rendered;
only the hero is an AI photo (venue + flags, no faces).
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(BASE, "assets", "media-generation-hero-shenzhen-summit-v5-0-8440a4c4-35b2-401e-9dd9-82878876b53b.webp")
OUT = os.path.join(BASE, "entry.png")

W, H = 1024, 1024
M = 48                      # margin
CW = W - 2 * M              # content width = 928
PAPER = (247, 243, 234)
INK = (18, 18, 18)
GREY = (84, 84, 84)
FAINT = (188, 182, 170)
RED = (178, 34, 34)
BAR = (40, 40, 40)

def font(name, size):
    for p in (f"/usr/share/fonts/truetype/dejavu/{name}.ttf", f"/usr/share/fonts/{name}.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_MAST = font("DejaVuSerif-Bold", 54)
F_FURN = font("DejaVuSans-Bold", 14)
F_HOOK = font("DejaVuSans-Bold", 14)
F_KICK = font("DejaVuSans-Bold", 16)
F_LEAD = font("DejaVuSerif-Bold", 43)
F_DECK = font("DejaVuSerif", 20)
F_BODY = font("DejaVuSans", 15)
F_BYLINE = font("DejaVuSans-Bold", 12)
F_CAP = font("DejaVuSans", 12)
F_BOXHEAD = font("DejaVuSans-Bold", 14)
F_BULLET = font("DejaVuSans", 14)
F_MODHEAD = font("DejaVuSerif-Bold", 25)
F_MODHEAD_SM = font("DejaVuSerif-Bold", 18)
F_MODTEXT = font("DejaVuSans", 14)
F_MODTEXT_SM = font("DejaVuSans", 13)
F_CHART = font("DejaVuSans-Bold", 17)
F_CHART_SM = font("DejaVuSans", 11)
F_BRIEF = font("DejaVuSans", 13)

def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(d, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def crop_to_fill(img, tw, th, fx=0.5, fy=0.5):
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale + 0.5), int(img.height * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x0 = min(max(int(fx * nw - tw / 2), 0), nw - tw)
    y0 = min(max(int(fy * nh - th / 2), 0), nh - th)
    return img.crop((x0, y0, x0 + tw, y0 + th))

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- furniture + masthead ----------
    d.line([M, 22, W - M, 22], fill=INK, width=2)
    d.text((M, 30), "WORLD EDITION", font=F_FURN, fill=INK)
    date = "Wednesday, 18 November 2026"
    d.text(((W - d.textlength(date, font=F_FURN)) / 2, 30), date, font=F_FURN, fill=INK)
    vol = "VOL. 1 · NO. 24 · PAGE 1"
    d.text((W - M - d.textlength(vol, font=F_FURN), 30), vol, font=F_FURN, fill=INK)
    d.line([M, 54, W - M, 54], fill=INK, width=1)
    title = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(title, font=F_MAST)) / 2, 64), title, font=F_MAST, fill=INK)
    hook = "THE DAY THE GEOPOLITICAL ORDER FRACTURED"
    d.text(((W - d.textlength(hook, font=F_HOOK)) / 2, 132), hook, font=F_HOOK, fill=GREY)
    d.line([M, 156, W - M, 156], fill=INK, width=4)
    d.line([M, 164, W - M, 164], fill=INK, width=1)

    # ---------- lead story ----------
    LX, LW = M, 520
    RX, RW = 592, W - M - 592   # 384
    y = 182
    d.text((LX, y), "SHENZHEN · APEC SUMMIT", font=F_KICK, fill=RED)
    y += 26
    y = text_block(d, LX, y, "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN", F_LEAD, INK, LW, 54)
    y += 6
    y = text_block(d, LX, y, "The first trilateral summit of the three leaders convenes tomorrow on the APEC sidelines — and could redraw the global order.", F_DECK, INK, LW, 27)
    y += 8
    y = text_block(d, LX, y, "APEC opened in Shenzhen on Tuesday. Trump said he may meet Putin if schedules allow, and voiced confidence that Xi and Putin would also sit down together.", F_BODY, GREY, LW, 21)
    y += 8
    d.text((LX, y), "By the World Desk · Shenzhen", font=F_BYLINE, fill=INK)
    lead_left_end = y + 16

    ry = 182
    hero = crop_to_fill(Image.open(HERO).convert("RGB"), RW, 196, fx=0.42, fy=0.58)
    img.paste(hero, (RX, ry))
    ry += 204
    ry = text_block(d, RX, ry, "Shenzhen's convention district, where APEC opened Tuesday. The three flags fly ahead of tomorrow's summit.", F_CAP, GREY, RW, 16)
    d.text((RX, ry), "PHOTO: WIRE IMAGE", font=F_CAP, fill=INK)
    ry += 24
    box_top = ry
    bullets = [
        "First-ever meeting of the three leaders",
        "Nuclear arms and Iran top the agenda",
        "Allies and markets watch for a new order",
    ]
    by = box_top + 12
    d.text((RX + 14, by), "WHY IT MATTERS", font=F_BOXHEAD, fill=INK)
    by += 24
    for b in bullets:
        d.rectangle([RX + 14, by + 5, RX + 20, by + 11], fill=INK)
        by = text_block(d, RX + 28, by, b, F_BULLET, GREY, RW - 42, 19)
        by += 3
    box_bot = by + 6
    d.rectangle([RX, box_top, RX + RW, box_bot], outline=INK, width=1)
    lead_end = max(lead_left_end, box_bot)
    print("lead ends:", lead_left_end, box_bot)

    # ---------- markets + nvidia band ----------
    y = lead_end + 14
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 16
    band_top = y
    # markets (left, wide)
    MX, MW = M, 568
    my = text_block(d, MX, y, "MARKETS", F_KICK, INK, MW, 20)
    my += 2
    my = text_block(d, MX, my, "DOW PLUNGES 848 POINTS AS INVESTORS FLEE TECH", F_MODHEAD, INK, MW, 31)
    my += 6
    # intraday line chart
    cx, cy, cw, ch = MX, my, 520, 64
    d.line([cx, cy + 8, cx + cw, cy + 8], fill=FAINT, width=1)          # open level
    pts = [(0, 8), (90, 22), (180, 44), (250, 58), (320, 46), (400, 52), (520, 48)]
    line = [(cx + px, cy + py) for px, py in pts]
    d.line(line, fill=INK, width=3)
    ex, ey = line[-1]
    d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=RED)
    d.text((ex - 118, ey - 26), "-848.75", font=F_CHART, fill=RED)
    d.text((cx, cy + ch + 2), "INTRADAY · CLOSE 50,575.52 · -2.0%", font=F_CHART_SM, fill=GREY)
    my = cy + ch + 20
    my = text_block(d, MX, my, "Institutions are cutting tech holdings and shifting into gold. A Fed official warns more rate hikes may be needed before spring 2027.", F_MODTEXT, GREY, MW, 19)
    markets_end = my
    # nvidia (right, narrow)
    NX, NW = 664, W - M - 664   # 312
    d.line([640, band_top, 640, band_top + 196], fill=FAINT, width=1)
    ny = text_block(d, NX, y, "TECHNOLOGY", F_KICK, INK, NW, 20)
    ny += 2
    ny = text_block(d, NX, ny, "NVIDIA REVENUE DOUBLES", F_MODHEAD, INK, NW, 31)
    ny += 8
    for label, val, frac in (("A YEAR AGO", "$57.9B", 0.5), ("THIS YEAR", "$115.8B", 1.0)):
        d.text((NX, ny), label, font=F_CHART_SM, fill=GREY)
        ny += 15
        d.rectangle([NX, ny, NX + int(272 * frac), ny + 13], fill=BAR)
        d.text((NX + int(272 * frac) + 8, ny - 1), val, font=F_CHART_SM, fill=INK)
        ny += 22
    ny += 2
    ny = text_block(d, NX, ny, "The board bars CEO Jensen Huang's return; Trump backs him.", F_MODTEXT, GREY, NW, 19)
    band_end = max(markets_end, ny)
    print("band ends:", markets_end, ny)

    # ---------- three briefs ----------
    y = band_end + 14
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 14
    briefs = [
        ("SECURITY", "IRAN DIRTY-BOMB FEARS ALARM WASHINGTON",
         "U.S. officials cite a possible radiological plot against senior officials. Bahrain is all-clear; Kuwait intercepted drones."),
        ("WAR IN UKRAINE", "372 CIVILIANS KILLED IN UKRAINE IN OCTOBER",
         "The UN toll for October alone underlines the war's cost as Kyiv strikes the Crimean Bridge again."),
        ("CLIMATE", "CYCLONE AKVAN BEARS DOWN ON INDIA",
         "The severe storm is forecast to make landfall on 20 November. Coastal districts are on high alert."),
    ]
    bw = 296
    for i, (kick, head, body) in enumerate(briefs):
        bx = M + i * (bw + 20)
        if i:
            d.line([bx - 10, y, bx - 10, y + 118], fill=FAINT, width=1)
        byy = text_block(d, bx, y, kick, F_BOXHEAD, INK, bw, 18)
        byy += 2
        byy = text_block(d, bx, byy, head, F_MODHEAD_SM, INK, bw, 23)
        byy += 3
        byy = text_block(d, bx, byy, body, F_MODTEXT_SM, GREY, bw, 18)
        print("brief", i, "ends", byy)
    y = y + 126

    # ---------- world briefs rail + folio ----------
    rail_top = y + 6
    d.rectangle([M, rail_top, W - M, rail_top + 46], outline=INK, width=1)
    brief_text = "WORLD BRIEFS — Quad leaders unveil a new plan in Manila · Amazon invests $7B in India's renewable energy · Voyager 1 nears one light-day from Earth · Thailand and the U.S. advance a trade pact"
    text_block(d, M + 12, rail_top + 7, brief_text, F_BRIEF, INK, CW - 24, 18)
    folio = "The World in One Image · Shenzhen — Washington — Kyiv · 18 November 2026"
    d.text(((W - d.textlength(folio, font=F_CAP)) / 2, rail_top + 56), folio, font=F_CAP, fill=GREY)
    print("rail ends:", rail_top + 46, "folio at:", rail_top + 56)

    # ---------- paper grain ----------
    noise = Image.effect_noise((W, H), 14).convert("RGB")
    img = Image.blend(img, noise, 0.01)

    img.save(OUT, optimize=True)
    print("saved:", OUT, os.path.getsize(OUT), "bytes", img.size)

if __name__ == "__main__":
    main()

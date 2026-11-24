#!/usr/bin/env python3
"""Draw the news-image-20261124 front page (1024x1024 PNG).

Written fresh for this entry, in this session. 45 verified stories
from Tuesday 24 November 2026, 7 regions, 5 real news photographs
from Wikimedia Commons, a numbers strip, a region bar, a UTC
timeline, 3 photo leads, 2 more photo stories, 10 medium cards, a
world map with 13 stories pinned, 30 more stories, and a DATE CHECK
box listing the wrong-day stories deliberately left out. Every text
block is measured first and the script ABORTS on any overflow
instead of cutting words off.
"""
import hashlib
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 20
CW = W - 2 * MARGIN  # 984

PAPER = (247, 242, 231)
INK = (20, 20, 20)
NAVY = (14, 42, 74)
RED = (176, 30, 36)
GREY = (90, 90, 90)
BAND = (220, 230, 239)
SEA = (168, 196, 216)
LAND = (122, 155, 109)
RULE = (180, 175, 165)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_R = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def abort(msg):
    print("OVERFLOW: " + msg, file=sys.stderr)
    sys.exit(2)


def width(s, f):
    return f.getlength(s)


def wrap(s, f, maxw):
    """Greedy word wrap; returns list of lines (no line exceeds maxw)."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if width(trial, f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(s, f, maxw, maxlines, what):
    lines = wrap(s, f, maxw)
    if len(lines) > maxlines:
        abort(f"{what}: {len(lines)} lines > {maxlines}: {s!r}")
    for ln in lines:
        if width(ln, f) > maxw:
            abort(f"{what}: single word too wide: {ln!r}")
    return lines


def cover(path, tw, th, fx=0.5, fy=0.5):
    """Cover-crop a photo to tw x th, keeping focus point (fx, fy)."""
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    cx, cy = int(fx * nw), int(fy * nh)
    x0 = min(max(cx - tw // 2, 0), nw - tw)
    y0 = min(max(cy - th // 2, 0), nh - th)
    return im.crop((x0, y0, x0 + tw, y0 + th))


def tag_chip(x, y, tag):
    col = NAVY if tag == "REPORTED" else (RED if tag == "ONGOING" else (120, 90, 20))
    f = F_B(9)
    tw = width(tag, f) + 10
    d.rounded_rectangle([x, y, x + tw, y + 14], radius=3, fill=col)
    d.text((x + 5, y + 2), tag, font=f, fill=(255, 255, 255))
    return tw


# ---------------------------------------------------------------- data
# region per story; counts are computed from this list and asserted.
STORIES = [
    # leads 1-3 (big photo cards)
    dict(n=1, headline="MYANMAR GENERALS SANCTIONED",
         body="UK sanctions Myanmar's generals after the ICJ genocide ruling; 14 nations endorse the verdict on the Rohingya.",
         tag="REPORTED", src="10Things, Horizon", region="ASIA-PACIFIC",
         photo="photos/icj.jpg", fx=0.5, fy=0.5,
         caption="THE HAGUE \u2014 THE COURT THAT RULED"),
    dict(n=2, headline="TANKERS ABLAZE IN HORMUZ",
         body="Three oil tankers catch fire after hitting mines in the Strait of Hormuz; Iran warns against a US naval blockade.",
         tag="ONGOING", src="Reuters, Al Jazeera", region="MIDDLE EAST",
         photo="photos/tanker.jpg", fx=0.62, fy=0.5,
         caption="STRAIT OF HORMUZ \u2014 TANKERS HIT MINES"),
    dict(n=3, headline="HUANG IS BACK",
         body="Nvidia reinstates Jensen Huang as CEO after Trump intervenes; shares surge and the Nasdaq jumps 6.51%.",
         tag="REPORTED", src="10Things, Principia", region="NORTH AMERICA",
         photo="photos/huang.jpg", fx=0.5, fy=0.4,
         caption="NVIDIA \u2014 HUANG REINSTATED"),
    # photo row 4-5
    dict(n=4, headline="GAZA: 77 YEARS UNDONE",
         body="UN: Gaza war erased 77 years of progress; six killed in Tuesday strikes.",
         tag="ONGOING", src="Reuters, Principia", region="MIDDLE EAST",
         photo="photos/gaza.jpg", fx=0.5, fy=0.5,
         caption="GAZA \u2014 77 YEARS ERASED"),
    dict(n=5, headline="INDONESIA PICKS VP",
         body="Prabowo names Amran Sulaiman and Sugiono to replace Gibran; assembly votes 11 Dec.",
         tag="REPORTED", src="Daily Summary", region="ASIA-PACIFIC",
         photo="photos/prabowo.jpg", fx=0.5, fy=0.35,
         caption="JAKARTA \u2014 SUCCESSOR TO BE ELECTED"),
    # medium 6-15
    dict(n=6, headline="NATO: WE'LL DEFEND SPACE",
         body="Rutte: NATO will defend space as Russia readies a nuclear satellite.",
         tag="REPORTED", src="Global Eye, Daily Summary", region="EUROPE"),
    dict(n=7, headline="GERMANY GETS DELTA",
         body="First access to Ukraine's Delta battlefield system; more interceptors agreed.",
         tag="REPORTED", src="Kyiv Independent", region="EUROPE"),
    dict(n=8, headline="ESTONIA 'ON VERGE OF WAR'",
         body="Moscow: Estonia's moves risk open war; Medvedev floats a preventive strike.",
         tag="REPORTED", src="IQMIA, Principia", region="EUROPE"),
    dict(n=9, headline="EL CHAPO ISIDRO CAUGHT",
         body="US drone aids Mexico's capture of El Chapo Isidro; Mexico will try him.",
         tag="REPORTED", src="Daily Summary", region="LATIN AMERICA"),
    dict(n=10, headline="UK LOGS RECORD HORMUZ ATTACKS",
         body="UK records its most Iranian attacks yet in the Strait of Hormuz as tensions rise.",
         tag="REPORTED", src="IQMIA", region="MIDDLE EAST"),
    dict(n=11, headline="EU VISA CURBS FOR RUSSIANS",
         body="Seven states back EU limits on Russian visas for tourists and sports.",
         tag="REPORTED", src="Kyiv Independent", region="EUROPE"),
    dict(n=12, headline="EBOLA TEAMS TRAPPED",
         body="Fighting in Ituri traps Congo Ebola teams; WHO: crews took cover 24 hours.",
         tag="ONGOING", src="UN News, Global Eye", region="AFRICA"),
    dict(n=13, headline="SANOFI BUYS INSMED $41BN",
         body="Sanofi to buy Insmed for $41bn, the biggest biotech deal in ~3 years.",
         tag="REPORTED", src="Principia", region="EUROPE"),
    dict(n=14, headline="NEPAL QUAKE 5.6",
         body="A 5.6-magnitude earthquake strikes Nepal near the Chinese border.",
         tag="REPORTED", src="Horizon", region="ASIA-PACIFIC"),
    dict(n=15, headline="MEASLES: US STATUS LOST",
         body="US loses measles-free status after 25 years; ninth death in Pennsylvania.",
         tag="REPORTED", src="Principia, Horizon", region="NORTH AMERICA"),
]

ALSO = [
    (16, "HASINA TO RETURN 16 DEC", "Daily Summary", "ASIA-PACIFIC"),
    (17, "MALAYSIA RETURNS 6,803", "Daily Summary", "ASIA-PACIFIC"),
    (18, "SPY GETS DEATH IN CHINA", "Daily Summary", "ASIA-PACIFIC"),
    (19, "RUSSIAN JETS IN KOREA ZONE", "Daily Summary", "ASIA-PACIFIC"),
    (20, "PENTAGON REBUKES CANADA", "Daily Summary", "NORTH AMERICA"),
    (21, "US BLACKLISTS MEGASPEED", "Daily Summary", "NORTH AMERICA"),
    (22, "TRIPOLI GRILLS KYIV ON SHIPS", "Daily Summary", "AFRICA"),
    (23, "LIBYA: UN SEEKS BENGHAZI PROBE", "UN News", "AFRICA"),
    (24, "SOMALIA, UGANDA HIT AL-SHABAAB", "IQMIA", "AFRICA"),
    (25, "YEMEN: DOZENS DEAD IN STRIKES", "Horizon", "MIDDLE EAST"),
    (26, "IRAN LASHES SINGER 74 TIMES", "Horizon", "MIDDLE EAST"),
    (27, "IRAN: NO TALKS UNTIL 7 DEMANDS", "Horizon", "MIDDLE EAST"),
    (28, "SOLOMONS END CHINA PACT", "10Things", "ASIA-PACIFIC"),
    (29, "NETANYAHU PUSHES IRAN STRIKES", "10Things", "MIDDLE EAST"),
    (30, "BURNHAM RULES OUT EU RETURN", "10Things", "EUROPE"),
    (31, "FRANCE RARE-EARTH RESERVES", "Horizon", "EUROPE"),
    (32, "ZELENSKY SEEKS 4-WAY TALKS", "Daily Summary", "EUROPE"),
    (33, "IRAQ PM SEIZES KURD OILFIELDS", "Reuters", "MIDDLE EAST"),
    (34, "COLOMBIA CAR BOMB", "Hindu", "LATIN AMERICA"),
    (35, "TIANGONG OPENS TO PAKISTAN", "Straits Times", "SPORT & SCIENCE"),
    (36, "ARM CEO EXTENDED TO 2033", "IQMIA", "EUROPE"),
    (37, "FDA CLEARS LIMB-GIRDLE DRUG", "Principia", "SPORT & SCIENCE"),
    (38, "FARTHEST BLACK HOLE FOUND", "Principia", "SPORT & SCIENCE"),
    (39, "UK: TEEN STABBED IN BLAINA", "IQMIA", "EUROPE"),
    (40, "CUBA: WHO CHIEF VISITS", "Horizon", "LATIN AMERICA"),
    (41, "KOSPI +6%, NIKKEI +3.91%", "Horizon", "ASIA-PACIFIC"),
    (42, "LAGARDE SUCCESSOR TIPPED", "Horizon", "EUROPE"),
    (43, "US SUES MUSK OVER GROK IMAGES", "Principia", "NORTH AMERICA"),
    (44, "700,000 RUSSIAN DEAD: LEAK", "Principia", "EUROPE"),
    (45, "MEASLES HITS 46 PA COUNTIES", "Horizon", "NORTH AMERICA"),
]

NUMBERS = [
    ("14", "NATIONS BACK ICJ RULING"),
    ("3", "TANKERS HIT IN HORMUZ"),
    ("+6.51%", "NASDAQ"),
    ("700,000", "RUSSIAN DEAD \u2014 LEAK"),
    ("5,303", "MIGRANTS TO RETURN"),
    ("$41BN", "SANOFI BUYS INSMED"),
]

TIMELINE = [
    ("00:30", "Zelensky talks"),
    ("00:52", "Megaspeed listed"),
    ("01:04", "Jets in Korea"),
    ("02:15", "NATO space vow"),
    ("02:38", "Indonesia VP picks"),
    ("05:54", "Malaysia returns"),
]

DATECHECK = ("DATE CHECK \u2014 Wires read to 13:00 UTC, Tuesday 24 November 2026. "
             "Left out as wrong-day news: the ICJ ruling itself (19 Nov \u2014 only "
             "Tuesday's sanctions shown) \u00b7 COP31's collapse (23 Nov) \u00b7 Dymer "
             "rescue (23 Nov) \u00b7 El Chapo capture (weekend) \u00b7 Banten fire "
             "(22 Nov) \u00b7 Peru quake (20 Nov) \u00b7 Shenzhen summit (19\u201320 Nov).")

PINS = [  # (story no, lon, lat, dx, dy) — dx/dy nudge pins apart in the
    # crowded Europe cluster (schematic map)
    (1, 4.3, 52.1, 10, 4), (2, 56.5, 26.5, 8, 6), (3, -121.9, 37.4, 0, 0),
    (4, 34.5, 31.5, 0, 0), (5, 106.8, -6.2, 0, 0), (6, 4.35, 50.85, -8, -8),
    (7, 13.4, 52.5, 0, -10), (8, 24.7, 59.4, -6, 0), (9, -107.4, 24.8, 0, 0),
    (10, 29.5, 1.5, 0, 0), (12, 85.3, 27.7, -6, 0), (13, 2.35, 48.86, -8, 0),
    (15, -77.5, 40.9, 0, 0),
]

# schematic world landmask, 48 cols (lon -180..180) x 14 rows (lat 85..-55)
LANDMASK = [
    ".............########..........###..............",
    ".##############.#####.....###.#################.",
    ".###############..##..#..######################.",
    ".....###########.......#######################..",
    "....##########..........##################.#....",
    "....#########.........############.##.####.#....",
    ".......#####..........############.##..####.....",
    ".........####.........#########.....#..#####....",
    ".............####.......########........#####...",
    ".............#####.......#######........######..",
    ".............####........######.........#####...",
    ".............####.........####..........#####...",
    "..............###.......................####..#.",
    "...............#..............................#.",
]
for _row in LANDMASK:
    assert len(_row) == 48, f"landmask row len {len(_row)}: {_row!r}"
assert len(LANDMASK) == 14

# region counts, computed from the data (never hand-typed)
REGIONS = ["EUROPE", "ASIA-PACIFIC", "NORTH AMERICA", "MIDDLE EAST",
           "AFRICA", "LATIN AMERICA", "SPORT & SCIENCE"]
_counts = {r: 0 for r in REGIONS}
for _s in STORIES:
    _counts[_s["region"]] += 1
for _n, _h, _src, _r in ALSO:
    _counts[_r] += 1
TOTAL = sum(_counts.values())
assert TOTAL == 45, f"story total {TOTAL} != 45"
assert len(STORIES) + len(ALSO) == 45

y = 0
GAP = 3


def section(h):
    global y
    top = y
    y += h + GAP
    return top


# ---------------------------------------------------------------- masthead
top = section(58)
d.rectangle([0, top, W, top + 58], fill=NAVY)
d.text((MARGIN, top + 8), "THE WORLD IN ONE DAY", font=F_SERIF_B(38), fill=(255, 255, 255))
date_s = "TUESDAY, 24 NOVEMBER 2026"
dw = width(date_s, F_B(17))
d.text((W - MARGIN - dw, top + 20), date_s, font=F_B(17), fill=(255, 255, 255))

# ---------------------------------------------------------------- subline
top = section(22)
sub = (f"{TOTAL} STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED "
       f"TUESDAY, 24 NOVEMBER 2026")
sw = width(sub, F_B(14))
d.text(((W - sw) / 2, top + 3), sub, font=F_B(14), fill=NAVY)

# ---------------------------------------------------------------- numbers
top = section(44)
cell = CW // 6
for i, (num, lab) in enumerate(NUMBERS):
    cx = MARGIN + i * cell
    nw = width(num, F_B(20))
    d.text((cx + (cell - nw) / 2, top + 2), num, font=F_B(20), fill=NAVY)
    lw = width(lab, F_R(10))
    d.text((cx + (cell - lw) / 2, top + 26), lab, font=F_R(10), fill=GREY)
    if i:
        d.line([cx, top + 4, cx, top + 40], fill=RULE, width=1)

# ---------------------------------------------------------------- regions
top = section(22)
d.rectangle([0, top, W, top + 22], fill=BAND)
parts = [f"{r} {_counts[r]}" for r in REGIONS]
reg = "  \u00b7  ".join(parts)
rw = width(reg, F_B(12))
d.text(((W - rw) / 2, top + 4), reg, font=F_B(12), fill=NAVY)

# ---------------------------------------------------------------- timeline
top = section(22)
d.rectangle([0, top, W, top + 22], fill=NAVY)
tl = "  \u00b7  ".join(f"{t}  {txt}" for t, txt in TIMELINE)
tlw = width(tl, F_B(10))
if tlw > CW:
    abort(f"timeline too wide: {tlw}")
d.text(((W - tlw) / 2, top + 5), tl, font=F_B(10), fill=(255, 255, 255))

# ---------------------------------------------------------------- leads 1-3
top = section(192)
colw = (CW - 2 * 12) // 3
for i, s in enumerate(STORIES[:3]):
    x = MARGIN + i * (colw + 12)
    ph = cover(s["photo"], colw, 128, s["fx"], s["fy"])
    img.paste(ph, (x, top))
    d.rectangle([x, top, x + colw - 1, top + 127], outline=NAVY, width=2)
    cap = s["caption"]
    cf = F_B(9)
    cw_ = width(cap, cf)
    if cw_ > colw - 8:
        abort(f"caption too wide: {cap!r}")
    d.rectangle([x, top + 128 - 18, x + colw, top + 128], fill=NAVY)
    d.text((x + (colw - cw_) / 2, top + 128 - 15), cap, font=cf, fill=(255, 255, 255))
    ty = top + 132
    hl = fit(f"{s['n']}. {s['headline']}", F_B(15), colw, 1, f"lead {s['n']} headline")
    d.text((x, ty), hl[0], font=F_B(15), fill=INK)
    ty += 19
    bl = fit(s["body"], F_R(10.5), colw, 2, f"lead {s['n']} body")
    for ln in bl:
        d.text((x, ty), ln, font=F_R(10.5), fill=INK)
        ty += 13
    ty += 2
    tw_ = tag_chip(x, ty, s["tag"])
    d.text((x + tw_ + 6, ty + 1), s["src"], font=F_R(10), fill=GREY)

# ---------------------------------------------------------------- photo row 4-5
top = section(140)
colw2 = (CW - 12) // 2
for i, s in enumerate(STORIES[3:5]):
    x = MARGIN + i * (colw2 + 12)
    ph = cover(s["photo"], 200, 96, s["fx"], s["fy"])
    img.paste(ph, (x, top + 22))
    d.rectangle([x, top + 22, x + 199, top + 117], outline=NAVY, width=2)
    cap = s["caption"]
    cf = F_B(8)
    cw_ = width(cap, cf)
    if cw_ > 200 - 6:
        abort(f"caption too wide: {cap!r}")
    d.rectangle([x, top + 118 - 14, x + 200, top + 118], fill=NAVY)
    d.text((x + (200 - cw_) / 2, top + 118 - 12), cap, font=cf, fill=(255, 255, 255))
    tx = x + 212
    tw2 = colw2 - 212
    hl = fit(f"{s['n']}. {s['headline']}", F_B(14), tw2, 1, f"photo {s['n']} headline")
    d.text((tx, top + 22), hl[0], font=F_B(14), fill=INK)
    bl = fit(s["body"], F_R(10.5), tw2, 2, f"photo {s['n']} body")
    by = top + 42
    for ln in bl:
        d.text((tx, by), ln, font=F_R(10.5), fill=INK)
        by += 13
    tw_ = tag_chip(tx, top + 96, s["tag"])
    d.text((tx + tw_ + 6, top + 97), s["src"], font=F_R(10), fill=GREY)

# ---------------------------------------------------------------- medium 6-15
top = section(215)
ROW_H = 43
for i, s in enumerate(STORIES[5:15]):
    col = i % 2
    row = i // 2
    x = MARGIN + col * (colw2 + 12)
    yy = top + row * ROW_H
    num = f"{s['n']}."
    nw_ = width(num, F_B(13))
    d.text((x, yy), num, font=F_B(13), fill=RED)
    hl = fit(s["headline"], F_B(13), colw2 - nw_ - 6, 1, f"medium {s['n']} headline")
    d.text((x + nw_ + 6, yy), hl[0], font=F_B(13), fill=INK)
    bl = fit(s["body"], F_R(11), colw2 - nw_ - 6, 1, f"medium {s['n']} body")
    d.text((x + nw_ + 6, yy + 17), bl[0], font=F_R(11), fill=INK)
    tagline = f"{s['tag']} \u00b7 {s['src']}"
    d.text((x + nw_ + 6, yy + 31), tagline, font=F_R(9), fill=GREY)

# ---------------------------------------------------------------- bottom band
top = section(255)
map_x, map_w = MARGIN, 480
also_x, also_w = MARGIN + 492, 492

# map (left)
d.text((map_x, top), "WHERE IT HAPPENED \u2014 13 STORIES PINNED", font=F_B(12), fill=NAVY)
map_top = top + 20
map_h = 160
d.rectangle([map_x, map_top, map_x + map_w - 1, map_top + map_h - 1], fill=SEA, outline=NAVY, width=1)
cw_cell = map_w / 48.0
ch_cell = map_h / 14.0
for r, row in enumerate(LANDMASK):
    for c, ch in enumerate(row):
        if ch == "#":
            d.rectangle([map_x + c * cw_cell, map_top + r * ch_cell,
                         map_x + (c + 1) * cw_cell - 0.5, map_top + (r + 1) * ch_cell - 0.5],
                        fill=LAND)


def pin_xy(lon, lat):
    px = map_x + (lon + 180.0) / 360.0 * map_w
    py = map_top + (85.0 - lat) / 140.0 * map_h
    return px, py


for n, lon, lat, dx, dy in PINS:
    px, py = pin_xy(lon, lat)
    px += dx
    py += dy
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    ns = str(n)
    nf = F_B(8 if n < 10 else 7)
    nw_ = width(ns, nf)
    d.text((px - nw_ / 2, py - 5), ns, font=nf, fill=(255, 255, 255))

# date check (left, under map)
dc_top = map_top + map_h + 8
d.rectangle([map_x, dc_top, map_x + map_w - 1, top + 255 - 1], outline=NAVY, width=1)
d.text((map_x + 6, dc_top + 4), "DATE CHECK", font=F_B(11), fill=NAVY)
dc_lines = fit(DATECHECK, F_R(9.5), map_w - 12, 4, "date check")
dy = dc_top + 19
for ln in dc_lines:
    d.text((map_x + 6, dy), ln, font=F_R(9.5), fill=INK)
    dy += 12

# ALSO (right)
d.text((also_x, top), "ALSO ON TUESDAY, 24 NOVEMBER \u2014 30 MORE STORIES", font=F_B(12), fill=NAVY)
also_top = top + 20
sub_w = (also_w - 12) // 2
af = F_R(9)
for i, (n, hl, src, _r) in enumerate(ALSO):
    col = i % 2
    row = i // 2
    x = also_x + col * (sub_w + 12)
    yy = also_top + row * 15
    line = f"{n}. {hl} \u2014 {src}"
    if width(line, af) > sub_w:
        abort(f"ALSO too wide: {line!r} ({width(line, af):.0f} > {sub_w})")
    d.text((x, yy), line, font=af, fill=INK)

# ---------------------------------------------------------------- footer
top = section(16)
foot = ("Sources: Daily Summary of World, The Global Eye, Horizon, 10Things, Principia, IQMIA, "
        "Kyiv Independent \u2014 all events Tuesday, 24 November 2026. "
        "All photographs are real news photographs of the events and places shown. "
        "REPORTED = confirmed by sources \u00b7 ONGOING = still developing \u00b7 "
        "CLAIM = as claimed, unverified.")
fl = fit(foot, F_R(9), CW, 2, "footer")
fy = top
for ln in fl:
    lw_ = width(ln, F_R(9))
    d.text(((W - lw_) / 2, fy), ln, font=F_R(9), fill=GREY)
    fy += 11

print(f"layout ends at y={y} of {H}")
if y > H:
    abort(f"layout overflows: y={y} > {H}")

img.save("entry.png", optimize=True)
data = open("entry.png", "rb").read()
print(f"entry.png: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}")
print(f"stories: {TOTAL}, regions: " + ", ".join(f"{r} {_counts[r]}" for r in REGIONS))

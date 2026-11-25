#!/usr/bin/env python3
"""Painter for the Tuesday 24 November 2026 world-news broadsheet, entry 2.

Draws one 1024x1024 digest page with Pillow in the mandated 3-tier
broadsheet recipe: masthead + KPI bar, hero tier, map + UTC timeline +
regional tally, wire grid over 7 region groups, date-audit footer.
Fully deterministic: one fixed seed, no clock, no network.
Run: MAKEFUN_OUTPUT_DIR=out python3 main.py  ->  out/entry.png
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

SEED = 20261124
W = 1024
H = 1024
PAPER = (250, 247, 240)
INK = (17, 19, 24)
RED = (196, 30, 36)
BLUE = (27, 59, 111)
GREY = (96, 92, 84)
RULE = (196, 186, 168)
GREEN = (34, 120, 60)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

REGION_COLOURS = {
    "WORLD": (90, 86, 78),
    "EUROPE": (20, 90, 120),
    "MIDDLE EAST": (196, 30, 36),
    "ASIA-PACIFIC": (200, 130, 30),
    "AFRICA": (90, 130, 60),
    "AMERICAS": (27, 59, 111),
    "SPORT & CULTURE": (110, 60, 140),
}

TALLY = [
    ("EUROPE", 7),
    ("MIDDLE EAST", 6),
    ("ASIA-PACIFIC", 6),
    ("AFRICA", 7),
    ("AMERICAS", 7),
    ("SPORT & CULTURE", 3),
]

TIMELINE = [
    ("04Z", "Hormuz", "3 tankers hit"),
    ("09Z", "Banten", "toll hits 26"),
    ("13Z", "Mali leak", "349 dead"),
    ("17Z", "Huang", "apology"),
    ("19Z", "Kyiv", "drones hit"),
    ("21Z", "Dow", "tops 50,000"),
]

DAY_NUMBERS = [
    ("3", "tankers hit in Hormuz"),
    ("349", "Russians dead in Mali"),
    ("26", "dead in Banten fire"),
    ("50,018", "Dow tops 50,000"),
]

MARKETS = [
    ("S&P 500", "7,201.09", "-0.50%"),
    ("Nasdaq", "23,733.54", "-1.48%"),
    ("Dow", "50,018.70", "+0.85%"),
    ("Nvidia", "$155.38", "-5.86%"),
]

# wire items: (number, headline, body, source)
WIRE = {
    "EUROPE": [
        (4, "Warsaw: Russian drone strays into Poland",
         "Brief incursion; jets scrambled.", "Reuters"),
        (5, "Girona: Junts rallies as Puigdemont counts down",
         "Exile nears end; presser due Wednesday.", "El Pais"),
        (6, "Madrid: Birth leave stretched to 20 weeks",
         "1,600 migrants reach El Hierro in a day.", "RTVE"),
        (7, "Moscow: Duma passes record military budget",
         "2027-29 plan sails through.", "Moscow Times"),
        (8, "Kyiv: Zelenskyy confirms Sparta II strike",
         "Seeks 48 Patriot missiles from Hegseth.", "Kyiv Post"),
        (9, "Eskisehir: Army helicopter crashes; 5 dead",
         "Crew killed in central Turkiye.", "Daily Sabah"),
    ],
    "MIDDLE EAST": [
        (10, "Gaza: Meningitis alert as 15 die",
         "1,790 cases; strikes kill 7 more.", "Al Jazeera"),
        (11, "Riyadh: Tallest tower hit again; 11 hurt",
         "Second strike in under a week.", "Radio Farda"),
        (12, "Jerusalem: Coalition talks fracture",
         "Democrats halt Yashar talks; first deal signed.", "Times of Israel"),
        (13, "Tehran: Israel says Iran builds chemical arms",
         "Tehran vows to break the blockade.", "I24 News"),
        (14, "Aden: Yemen forces brace for Houthi push",
         "Troops mobilise to hold the port city.", "Arabi21"),
    ],
    "ASIA-PACIFIC": [
        (15, "Serang: Banten fire toll rises to 26",
         "28 missing; negligence probe opens.", "Xinhua"),
        (16, "Shanghai: Party chief Chen probed",
         "Top official falls in graft inquiry.", "SCMP"),
        (17, "Beijing: Shenzhou-24 crew unveiled",
         "First foreign astronaut joins mission.", "CGTN"),
        (18, "Ras Al Khaimah: Crash kills 13, 11 Indians",
         "13 die in road crash; consulate steps in.", "Mathrubhumi"),
        (19, "Suryavanshi smashes six records in one match",
         "Teen hits fastest 100, 150, 200.", "Dainik Bhaskar"),
        (20, "Tokyo: Takaichi backs ICC funding",
         "Lower house tightens land-buy rules.", "Japan Times"),
    ],
    "AFRICA": [
        (21, "Mali: Leak lists 349 Russians killed",
         "Rosstat files expose junta war toll.", "Guardian"),
        (22, "Benghazi: AU condemns port attacks",
         "Ships hit; UN mission protests.", "PANA"),
        (23, "Khartoum: Drones killed 1,600 in Sudan",
         "UN rights body counts the toll.", "UN News"),
        (24, "Addis Ababa: Amnesty seeks UN action",
         "14 civilians dead in Ethiopia.", "Amnesty"),
        (25, "Nairobi: Doctors give 72-hour strike notice",
         "Pay delays push KNH medics out.", "Daily Nation"),
        (26, "Nairobi: eCitizen users told to reset passwords",
         "Hack reports trigger security alert.", "Citizen TV"),
        (27, "Pretoria: Zimbabwean convicted over Ukraine plan",
         "Court finds he plotted to join war.", "Radio Generation"),
    ],
    "AMERICAS": [
        (28, "Washington: Huawei convicted in US court",
         "Trade-secrets conspiracy proven.", "NBC"),
        (29, "Washington: Abrego Garcia leaves US for Europe",
         "Deportation saga ends in exile.", "CBS"),
        (30, "Washington: Biggest anti-scam sweep in history",
         "Trump team targets fraud rings.", "Breitbart"),
        (31, "New York: FAA ground stop snarls holiday travel",
         "Busy hub halted before Thanksgiving.", "Newsweek"),
        (32, "Washington: Fresh tariffs eyed on China, EU +14",
         "Trade war returns; markets flinch.", "Firstpost"),
        (33, "Washington: Democrats ready probes of Trump firms",
         "Accountability drive takes shape.", "MSNBC"),
    ],
    "SPORT & CULTURE": [
        (34, "Manchester: City held 2-2 by Napoli",
         "Hojlund double undone in Europe.", "ANSA"),
        (35, "Eindhoven: PSV and Feyenoord fall in Europe",
         "Dutch duo lose Champions League ties.", "NOS"),
        (36, "Istanbul: Galatasaray edge Aston Villa 1-0",
         "Aslan strike seals famous win.", "Aydinlik"),
    ],
}

PINS = {
    1: (178, 46, "MIDDLE EAST"),
    2: (28, 40, "AMERICAS"),
    3: (178, 24, "EUROPE"),
    4: (168, 20, "EUROPE"),
    5: (150, 28, "EUROPE"),
    9: (168, 34, "EUROPE"),
    15: (258, 78, "ASIA-PACIFIC"),
    16: (252, 44, "ASIA-PACIFIC"),
    21: (150, 58, "AFRICA"),
    22: (168, 48, "AFRICA"),
    23: (178, 62, "AFRICA"),
    28: (62, 38, "AMERICAS"),
}


def load(path, size):
    font = ImageFont.truetype(path, size)
    return font


def wrap_lines(text, fnt, width):
    out = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if fnt.getlength(trial) <= width:
            current = trial
        if fnt.getlength(trial) > width:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def sky(d, box, top, bottom):
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for yy in range(y0, y1):
        t = (yy - y0) / span
        col = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(x0, yy), (x1, yy)], fill=col)


def scatter_stars(d, box, count, rng):
    x0, y0, x1, y1 = box
    for _ in range(count):
        sx = rng.randint(x0, x1)
        sy = rng.randint(y0, y1)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 220))


def scene_tanker(d, box, rng):
    x0, y0, x1, y1 = box
    sky(d, box, (232, 122, 62), (74, 52, 96))
    d.ellipse([x1 - 56, y0 + 10, x1 - 14, y0 + 52], fill=(255, 214, 130))
    d.rectangle([x0, y1 - 46, x1, y1], fill=(28, 42, 66))
    for i in range(9):
        wx = x0 + 12 + i * 38
        d.line([(wx, y1 - 8), (wx + 22, y1 - 8)], fill=(90, 120, 150), width=1)
    d.rectangle([x0 + 60, y1 - 88, x0 + 300, y1 - 46], fill=(24, 24, 28))
    d.rectangle([x0 + 60, y1 - 88, x0 + 300, y1 - 78], fill=(60, 20, 18))
    d.rectangle([x0 + 210, y1 - 116, x0 + 236, y1 - 88], fill=(40, 40, 44))
    d.rectangle([x0 + 96, y1 - 104, x0 + 116, y1 - 88], fill=(40, 40, 44))
    for i, col in enumerate([(255, 120, 30), (255, 170, 40), (230, 60, 30)]):
        fx = x0 + 96 + i * 52
        d.polygon([(fx, y1 - 104), (fx + 14, y1 - 138), (fx + 28, y1 - 104)],
                  fill=col)
    for i in range(6):
        sx = x0 + 110 + i * 34
        sy = y1 - 130 - (i % 3) * 8
        d.ellipse([sx, sy, sx + 16, sy + 12], fill=(120, 116, 110))
    d.line([(x0 + 300, y1 - 88), (x1 - 20, y1 - 60)], fill=(200, 200, 190),
           width=2)


def scene_chip(d, box, rng):
    x0, y0, x1, y1 = box
    sky(d, box, (10, 26, 18), (16, 60, 34))
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    d.rectangle([cx - 26, cy - 22, cx + 26, cy + 22], fill=(24, 140, 80))
    d.rectangle([cx - 15, cy - 12, cx + 15, cy + 12], fill=(16, 90, 52))
    for i in range(5):
        d.line([(cx - 26, cy - 16 + i * 8), (cx - 38, cy - 16 + i * 8)],
               fill=(120, 200, 150), width=2)
        d.line([(cx + 26, cy - 16 + i * 8), (cx + 38, cy - 16 + i * 8)],
               fill=(120, 200, 150), width=2)
    d.line([(x0 + 12, y1 - 14), (x1 - 34, y0 + 12)], fill=(220, 60, 60), width=4)
    d.polygon([(x1 - 34, y0 + 12), (x1 - 48, y0 + 12), (x1 - 34, y0 + 26)],
              fill=(220, 60, 60))
    d.ellipse([x0 + 8, y0 + 8, x0 + 20, y0 + 20], fill=(255, 220, 120))


def scene_city(d, box, rng):
    x0, y0, x1, y1 = box
    sky(d, box, (16, 28, 58), (58, 84, 130))
    scatter_stars(d, box, 30, rng)
    d.ellipse([x1 - 44, y0 + 8, x1 - 12, y0 + 40], fill=(235, 230, 215))
    for i in range(6):
        bx = x0 + 8 + i * 23
        bh = 26 + ((i * 17) % 34)
        d.rectangle([bx, y1 - bh, bx + 17, y1], fill=(26, 30, 44))
        d.rectangle([bx + 4, y1 - bh + 5, bx + 13, y1 - bh + 12],
                    fill=(255, 214, 130))
    d.polygon([(x0 + 96, y1 - 40), (x0 + 110, y1 - 66), (x0 + 124, y1 - 40)],
              fill=(255, 120, 30))
    d.ellipse([x0 + 100, y1 - 30, x0 + 120, y1 - 12], fill=(255, 170, 40))
    d.ellipse([x0 + 30, y0 + 14, x0 + 44, y0 + 24], fill=(200, 200, 200))
    d.line([(x0 + 30, y0 + 19), (x0 + 44, y0 + 19)], fill=(120, 120, 120),
           width=1)


def draw_world_map(d, box, rng):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 238))
    d.rectangle(box, outline=(120, 120, 110), width=1)
    blobs = [
        [(10, 28), (55, 16), (95, 24), (88, 48), (60, 58), (30, 52), (12, 42)],
        [(72, 66), (92, 62), (102, 80), (88, 100), (74, 88)],
        [(148, 22), (178, 14), (196, 24), (190, 40), (168, 42), (150, 34)],
        [(152, 48), (178, 44), (192, 58), (182, 82), (164, 78), (152, 62)],
        [(200, 20), (250, 12), (282, 26), (276, 48), (240, 52), (212, 42)],
        [(238, 96), (262, 92), (272, 104), (252, 112), (238, 104)],
    ]
    sx = (x1 - x0) / 300
    sy = (y1 - y0) / 150
    for blob in blobs:
        pts = [(x0 + px * sx, y0 + py * sy) for px, py in blob]
        d.polygon(pts, fill=(232, 220, 188), outline=(150, 140, 110))
    for _ in range(40):
        gx = rng.randint(x0 + 4, x1 - 4)
        gy = rng.randint(y0 + 4, y1 - 4)
        d.point((gx, gy), fill=(170, 190, 205))
    for num, (px, py, region) in PINS.items():
        cx = x0 + px * sx
        cy = y0 + py * sy
        col = REGION_COLOURS[region]
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=col,
                  outline=(255, 255, 255), width=1)
        f = load(SANSB, 8)
        tw = f.getlength(str(num))
        d.text((cx - tw / 2, cy - 5), str(num), font=f, fill=(255, 255, 255))


def draw_wire_group(d, x, y, width, region, items, label):
    col = REGION_COLOURS[region]
    if label is None:
        label = region
    d.rectangle([x, y, x + width, y + 16], fill=col)
    d.text((x + 6, y + 2), label, font=load(SANSB, 11),
           fill=(255, 255, 255))
    yy = y + 21
    for num, head, body, src in items:
        d.text((x, yy), str(num), font=load(SANSB, 10), fill=RED)
        tx = x + 22
        avail = (x + width) - tx
        head_f = load(SERIFB, 10)
        body_f = load(SERIF, 9)
        head_lines = wrap_lines(head, head_f, avail)
        for li, ln in enumerate(head_lines[:2]):
            d.text((tx, yy + li * 12), ln, font=head_f, fill=INK)
        by = yy + len(head_lines[:2]) * 12 + 1
        body_lines = wrap_lines(body + " \u2014 " + src, body_f, avail)
        for li, ln in enumerate(body_lines[:1]):
            d.text((tx, by + li * 11), ln, font=body_f, fill=(40, 38, 34))
        yy = by + 12
        d.line([(x, yy), (x + width, yy)], fill=(228, 222, 210), width=1)
        yy += 4
    return yy


def paint():
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    for _ in range(9000):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        v = rng.randint(-7, 5)
        px = img.getpixel((x, y))
        img.putpixel((x, y), tuple(max(0, min(255, c + v)) for c in px))
    d = ImageDraw.Draw(img)

    # ---- Zone 1: masthead + KPI bar (0-88) ----
    d.rectangle([0, 0, W, 5], fill=RED)
    title_f = load(SERIFB, 30)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - title_f.getlength(title)) / 2, 12), title, font=title_f, fill=INK)
    date_f = load(SANSB, 22)
    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - date_f.getlength(date)) / 2, 46), date, font=date_f, fill=RED)
    pill = "36 VERIFIED STORIES  \u00b7  7 REGIONS  \u00b7  00:00\u201323:59 UTC  \u00b7  DATE-AUDITED"
    pf = load(SANS, 11)
    pw = pf.getlength(pill)
    d.line([(16, 76), ((W - pw) / 2 - 14, 76)], fill=INK, width=1)
    d.line([((W + pw) / 2 + 14, 76), (W - 16, 76)], fill=INK, width=1)
    d.text(((W - pw) / 2, 69), pill, font=pf, fill=INK)
    d.line([(0, 88), (W, 88)], fill=INK, width=2)

    # ---- Zone 2: hero (88-404) ----
    d.text((16, 96), "LEAD STORY", font=load(SANSB, 11), fill=RED)
    scene_tanker(d, (16, 112, 376, 282), rng)
    d.rectangle([16, 112, 376, 282], outline=INK, width=1)
    chip = "3 TANKERS HIT"
    cf = load(SANSB, 11)
    cw = cf.getlength(chip) + 14
    d.rectangle([376 - cw - 6, 118, 376 - 6, 138], fill=RED)
    d.text((376 - cw, 120), chip, font=cf, fill=(255, 255, 255))
    fx = 392
    d.text((fx, 112), "STRAIT OF HORMUZ", font=load(SANSB, 11), fill=INK)
    d.text((fx, 126), "MIDDLE EAST \u00b7 SHIPPING", font=load(SANS, 10), fill=GREY)
    facts = [
        ("3", "tankers hit mines, on fire"),
        ("0", "crew lost \u2014 all accounted for"),
        ("+1.8%", "WTI crude to $81.63"),
    ]
    fy = 148
    for num, lab in facts:
        nf = load(SERIFB, 20)
        d.text((fx, fy), num, font=nf, fill=RED)
        d.text((fx + nf.getlength(num) + 10, fy + 5), lab, font=load(SANS, 11),
               fill=INK)
        fy += 30
    d.line([(fx, 244), (600, 244)], fill=RULE, width=1)
    d.text((fx, 252), "Under US escort \u2014", font=load(SERIFI, 12), fill=INK)
    d.text((fx, 268), "the escort could not stop it.", font=load(SERIFI, 12),
           fill=INK)
    head_f = load(SERIFB, 36)
    head_lines = wrap_lines("Three tankers burn in Hormuz", head_f, 584)
    hy = 290
    for li, ln in enumerate(head_lines[:2]):
        d.text((16, hy + li * 40), ln, font=head_f, fill=INK)
    sum_f = load(SERIF, 14)
    sum_lines = wrap_lines(
        "The IRGC says three oil tankers hit naval mines and caught fire; "
        "UK monitors confirm three vessels struck. Oil climbs as shipping "
        "risk jumps.", sum_f, 584)
    sy = hy + len(head_lines[:2]) * 40 + 4
    for li, ln in enumerate(sum_lines[:2]):
        d.text((16, sy + li * 18), ln, font=sum_f, fill=(40, 38, 34))
    d.text((16, sy + 40), "Sources: IRNA \u00b7 UKMTO \u00b7 Reuters",
           font=load(SANS, 9), fill=GREY)
    d.line([(600, 96), (600, 396)], fill=RULE, width=1)

    # sub-leads, right column
    subleads = [
        (96, "2", "SANTA CLARA, USA", "AMERICAS \u00b7 MARKETS", scene_chip,
         "Huang says sorry as Nvidia slides 5.9%",
         "Monday's +31.5% record rally fades; Dow tops 50,000.",
         "Investors.com \u00b7 Reuters"),
        (254, "3", "KYIV, UKRAINE", "EUROPE \u00b7 WAR", scene_city,
         "Drones set Kyiv block ablaze",
         "112 drones overnight; 88 downed; Odesa hit kills two.",
         "Reuters \u00b7 Kyiv Independent"),
    ]
    for sy0, num, place, tag, scene, head, summ, src in subleads:
        scene(d, (612, sy0, 762, sy0 + 84), rng)
        d.rectangle([612, sy0, 762, sy0 + 84], outline=INK, width=1)
        d.text((772, sy0), num + "  " + place, font=load(SANSB, 10), fill=INK)
        d.text((772, sy0 + 13), tag, font=load(SANS, 9), fill=GREY)
        hf = load(SERIFB, 21)
        hlines = wrap_lines(head, hf, 236)
        hyy = sy0 + 28
        for li, ln in enumerate(hlines[:2]):
            d.text((772, hyy + li * 23), ln, font=hf, fill=INK)
        byy = sy0 + 86
        bf = load(SERIF, 11)
        blines = wrap_lines(summ, bf, 396)
        for li, ln in enumerate(blines[:2]):
            d.text((612, byy + li * 14), ln, font=bf, fill=(40, 38, 34))
        d.text((612, byy + len(blines[:2]) * 14 + 3), src,
               font=load(SANS, 9), fill=GREY)
    d.line([(612, 246), (1008, 246)], fill=RULE, width=1)
    d.line([(0, 404), (W, 404)], fill=INK, width=2)

    # ---- Zone 3: map + day numbers + timeline + tally (404-600) ----
    d.text((16, 412), "WHERE IT HAPPENED", font=load(SANSB, 11), fill=INK)
    d.text((16, 426), "pins match story numbers", font=load(SANS, 9), fill=GREY)
    draw_world_map(d, (16, 442, 316, 592), rng)
    d.text((332, 412), "DAY IN NUMBERS", font=load(SANSB, 11), fill=INK)
    d.text((332, 426), "the figures that moved Tuesday",
           font=load(SANS, 9), fill=GREY)
    ny = 440
    for num, lab in DAY_NUMBERS:
        d.text((332, ny), num, font=load(SERIFB, 24), fill=RED)
        d.text((332, ny + 27), lab, font=load(SANS, 10), fill=INK)
        ny += 36
    d.line([(316, 442), (316, 592)], fill=RULE, width=1)
    d.line([(576, 412), (576, 592)], fill=RULE, width=1)
    d.text((588, 412), "THE DAY IN UTC", font=load(SANSB, 11), fill=INK)
    d.text((588, 426), "00Z \u2014 23Z, as reported", font=load(SANS, 9), fill=GREY)
    tx0, tx1 = 600, 996
    d.line([(tx0, 462), (tx1, 462)], fill=INK, width=2)
    for i, (hh, t1, t2) in enumerate(TIMELINE):
        cx = tx0 + (tx1 - tx0) * i / 5
        d.ellipse([cx - 5, 457, cx + 5, 467], fill=RED, outline=(255, 255, 255),
                  width=1)
        tf = load(SANSB, 10)
        tw = tf.getlength(hh)
        lx = min(max(cx - tw / 2, 588), 1008 - tw)
        d.text((lx, 440), hh, font=tf, fill=RED)
        lf = load(SANS, 9)
        for li, lab in enumerate((t1, t2)):
            lw = lf.getlength(lab)
            lx = min(max(cx - lw / 2, 588), 1008 - lw)
            lab_col = GREY
            if li == 0:
                lab_col = INK
            d.text((lx, 474 + li * 12), lab, font=lf, fill=lab_col)
    d.text((588, 508), "REGIONAL TALLY \u2014 36 STORIES", font=load(SANSB, 11),
           fill=INK)
    ty = 528
    bar_w = 420 - 130
    for name, count in TALLY:
        d.text((588, ty), name, font=load(SANSB, 10), fill=INK)
        d.rectangle([718, ty + 1, 718 + bar_w * count / 7, ty + 11],
                    fill=REGION_COLOURS[name])
        d.text((718 + bar_w + 6, ty), str(count), font=load(SANSB, 10), fill=INK)
        ty += 10
    d.line([(0, 600), (W, 600)], fill=INK, width=2)

    # ---- Zone 4: wire grid (600-976), 4 columns ----
    d.text((16, 608), "THE WIRES \u2014 33 MORE STORIES", font=load(SANSB, 11),
           fill=INK)
    d.text((700, 608), "numbers match the map", font=load(SANS, 9), fill=GREY)
    col_w = 236
    col_x = [16, 268, 520, 772]
    end_a = draw_wire_group(d, col_x[0], 628, col_w, "EUROPE",
                            WIRE["EUROPE"], None)
    end_a = draw_wire_group(d, col_x[0], end_a + 8, col_w, "SPORT & CULTURE",
                            WIRE["SPORT & CULTURE"], None)
    end_b = draw_wire_group(d, col_x[1], 628, col_w, "MIDDLE EAST",
                            WIRE["MIDDLE EAST"], None)
    end_b = draw_wire_group(d, col_x[1], end_b + 8, col_w, "AMERICAS",
                            WIRE["AMERICAS"][:3], None)
    end_c = draw_wire_group(d, col_x[2], 628, col_w, "ASIA-PACIFIC",
                            WIRE["ASIA-PACIFIC"], None)
    end_c = draw_wire_group(d, col_x[2], end_c + 8, col_w, "AMERICAS",
                            WIRE["AMERICAS"][3:], "AMERICAS (cont.)")
    end_d = draw_wire_group(d, col_x[3], 628, col_w, "AFRICA", WIRE["AFRICA"],
                            None)
    mx = col_x[3]
    my = end_d + 10
    d.rectangle([mx, my, mx + col_w, my + 16], fill=BLUE)
    d.text((mx + 6, my + 2), "MARKETS AT THE CLOSE", font=load(SANSB, 11),
           fill=(255, 255, 255))
    my += 22
    for name, val, chg in MARKETS:
        d.text((mx, my), name, font=load(SANSB, 11), fill=INK)
        d.text((mx + 118, my - 1), val, font=load(SERIFB, 12), fill=INK)
        chg_col = GREEN
        if chg.startswith("-"):
            chg_col = RED
        d.text((mx + 196, my), chg, font=load(SANSB, 11), fill=chg_col)
        my += 19
    d.text((mx, my + 2), "Tue 24 Nov \u00b7 Wall Street close",
           font=load(SANS, 9), fill=GREY)
    d.text((mx, my + 14), "Nvidia -5.9% as the comeback rally fades.",
           font=load(SERIF, 10), fill=(40, 38, 34))
    d.line([(0, 976), (W, 976)], fill=INK, width=2)

    # ---- Zone 5: date audit footer (976-1024) ----
    d.rectangle([0, 976, W, H], fill=INK)
    ff = load(SANS, 10)
    line1 = ("DATE AUDIT: ALL 36 STORIES VERIFIED ON 24 NOV 2026 UTC  \u00b7  "
             "EXCLUDED: NOV 22 & NOV 23 CARRYOVERS")
    line2 = ("SOURCES: REUTERS, AP, AFP, UN, BBC, AL JAZEERA  \u00b7  "
             "SCENES ARE DRAWN ILLUSTRATIONS, NOT PHOTOGRAPHS")
    d.text((16, 984), line1, font=ff, fill=(255, 255, 255))
    d.text((16, 1002), line2, font=ff, fill=(200, 205, 220))

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, "entry.png")
    img.save(outpath, optimize=True)
    return img


if __name__ == "__main__":
    paint()
    print("painted entry.png")

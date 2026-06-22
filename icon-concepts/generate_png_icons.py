from pathlib import Path
from math import cos, sin, radians

from PIL import Image, ImageDraw, ImageFilter


OUT = Path(__file__).resolve().parent / "png"
OUT.mkdir(exist_ok=True)

S = 4
SIZE = 1024
CANVAS = SIZE * S

COLORS = {
    "red": "#ae222a",
    "red_dark": "#8c1b22",
    "green_dark": "#142a08",
    "green": "#1f7419",
    "green_mid": "#2d8020",
    "green_shadow": "#15500f",
    "orange": "#ff7a00",
    "yellow": "#ffd700",
    "cream": "#f7efe7",
    "cream2": "#ead7ca",
    "brown": "#5a3c31",
    "brown_dark": "#3d2922",
    "white": "#f4f8f0",
    "ink": "#17120f",
    "blue": "#1f7f92",
    "pink": "#e97bb9",
}


def sc(v):
    return int(round(v * S))


def xy(points):
    return [(sc(x), sc(y)) for x, y in points]


def make_canvas():
    return Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))


def down(img):
    return img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def draw_shadowed_badge(img, box, fill, radius=54, shadow=True):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    b = tuple(sc(v) for v in box)
    if shadow:
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow_layer)
        sd.rounded_rectangle((b[0], b[1] + sc(18), b[2], b[3] + sc(18)), radius=sc(radius), fill=(20, 42, 8, 58))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(sc(18)))
        img.alpha_composite(shadow_layer)
    d.rounded_rectangle(b, radius=sc(radius), fill=fill)
    img.alpha_composite(layer)


def draw_sun(d, cx, cy, r):
    d.ellipse((sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)), fill=COLORS["orange"])
    d.ellipse((sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r * 0.45)), fill=COLORS["yellow"])


def draw_wall(d, variant=0):
    if variant == 0:
        d.polygon(xy([(112, 220), (438, 78), (864, 158), (910, 850), (150, 850)]), fill=COLORS["cream"])
        d.polygon(xy([(438, 78), (864, 158), (910, 850), (590, 850), (542, 275)]), fill=COLORS["brown"])
        d.polygon(xy([(112, 220), (542, 275), (590, 850), (150, 850)]), fill=COLORS["cream2"])
    elif variant == 1:
        d.polygon(xy([(94, 210), (350, 104), (598, 142), (516, 850), (100, 850)]), fill=COLORS["cream"])
        d.polygon(xy([(350, 104), (598, 142), (930, 278), (930, 850), (516, 850)]), fill=COLORS["brown"])
        d.polygon(xy([(100, 598), (500, 356), (930, 850), (100, 850)]), fill=COLORS["cream2"])
    else:
        d.polygon(xy([(95, 188), (388, 86), (872, 168), (920, 842), (116, 842)]), fill=COLORS["cream"])
        d.polygon(xy([(388, 86), (872, 168), (920, 842), (686, 842), (594, 268)]), fill=COLORS["brown_dark"])
        d.polygon(xy([(116, 842), (256, 500), (594, 268), (686, 842)]), fill=COLORS["cream2"])


def hold(d, x, y, color, scale=1, rot=0):
    # Irregular climbing hold blob.
    pts = []
    for i, (rr, aa) in enumerate([(1.0, 0), (0.72, 55), (0.92, 122), (0.65, 198), (0.9, 272)]):
        a = radians(aa + rot)
        pts.append((x + cos(a) * 30 * scale * rr, y + sin(a) * 21 * scale * rr))
    d.polygon(xy(pts), fill=color)
    d.ellipse((sc(x - 7 * scale), sc(y - 5 * scale), sc(x + 7 * scale), sc(y + 5 * scale)), fill=(20, 42, 8, 80))


def climber(d, x, y, scale=1, flip=1, shirt=None):
    ink = COLORS["ink"]
    skin = "#f2a06f"
    shirt = shirt or COLORS["green_dark"]
    # head
    d.ellipse((sc(x - 13 * scale), sc(y - 45 * scale), sc(x + 13 * scale), sc(y - 19 * scale)), fill=skin)
    # hair
    d.pieslice((sc(x - 15 * scale), sc(y - 49 * scale), sc(x + 13 * scale), sc(y - 20 * scale)), 180, 350, fill=ink)
    # torso
    d.polygon(xy([
        (x - 18 * scale, y - 14 * scale),
        (x + 17 * scale, y - 16 * scale),
        (x + 11 * scale, y + 38 * scale),
        (x - 20 * scale, y + 34 * scale),
    ]), fill=shirt)
    # harness/shorts
    d.polygon(xy([(x - 20 * scale, y + 34 * scale), (x + 11 * scale, y + 38 * scale), (x + 2 * scale, y + 60 * scale), (x - 23 * scale, y + 54 * scale)]), fill=COLORS["red"])
    sw = sc(10 * scale)
    # arms
    d.line(xy([(x - 10 * scale, y - 8 * scale), (x - 58 * scale * flip, y - 38 * scale)]), fill=skin, width=sw)
    d.line(xy([(x + 12 * scale, y - 10 * scale), (x + 48 * scale * flip, y - 64 * scale)]), fill=skin, width=sw)
    d.ellipse((sc(x - 63 * scale * flip - 5 * scale), sc(y - 43 * scale), sc(x - 63 * scale * flip + 5 * scale), sc(y - 33 * scale)), fill=skin)
    d.ellipse((sc(x + 48 * scale * flip - 5 * scale), sc(y - 69 * scale), sc(x + 48 * scale * flip + 5 * scale), sc(y - 59 * scale)), fill=skin)
    # legs
    d.line(xy([(x - 9 * scale, y + 54 * scale), (x - 46 * scale * flip, y + 105 * scale)]), fill=ink, width=sw)
    d.line(xy([(x + 3 * scale, y + 56 * scale), (x + 53 * scale * flip, y + 88 * scale)]), fill=ink, width=sw)
    d.ellipse((sc(x - 51 * scale * flip - 8 * scale), sc(y + 101 * scale), sc(x - 51 * scale * flip + 8 * scale), sc(y + 113 * scale)), fill=COLORS["white"])
    d.ellipse((sc(x + 53 * scale * flip - 8 * scale), sc(y + 84 * scale), sc(x + 53 * scale * flip + 8 * scale), sc(y + 96 * scale)), fill=COLORS["white"])


def save_icon(name, draw_fn):
    img = make_canvas()
    draw_fn(img)
    path = OUT / f"{name}.png"
    down(img).save(path)
    return path


def all_skill_levels(img):
    d = ImageDraw.Draw(img)
    draw_shadowed_badge(img, (78, 76, 946, 948), COLORS["green_dark"], radius=96)
    draw_sun(d, 314, 274, 174)
    draw_wall(d, 0)
    for args in [
        (228, 320, COLORS["red"], 1.1, 20), (420, 250, COLORS["blue"], .85, -12),
        (650, 310, COLORS["orange"], 1.0, 60), (790, 450, COLORS["pink"], .9, 12),
        (305, 620, COLORS["green"], 1.0, -40), (575, 570, COLORS["red_dark"], .8, 20),
        (705, 710, COLORS["orange"], .95, 80)
    ]:
        hold(d, *args)
    # Progression route.
    d.line(xy([(226, 732), (350, 610), (472, 490), (626, 382), (764, 258)]), fill=COLORS["white"], width=sc(8))
    for x, y in [(226, 732), (350, 610), (472, 490), (626, 382), (764, 258)]:
        d.ellipse((sc(x - 14), sc(y - 14), sc(x + 14), sc(y + 14)), fill=COLORS["red"])
    climber(d, 274, 642, 1.24, 1, COLORS["red"])
    climber(d, 520, 444, .9, -1, COLORS["green_dark"])
    climber(d, 740, 258, .68, 1, COLORS["blue"])


def thriving_community(img):
    d = ImageDraw.Draw(img)
    draw_shadowed_badge(img, (78, 76, 946, 948), COLORS["cream"], radius=96)
    draw_wall(d, 1)
    for args in [
        (210, 258, COLORS["orange"], 1, 15), (380, 215, COLORS["pink"], .8, 50),
        (620, 240, COLORS["blue"], .85, -20), (780, 346, COLORS["red"], 1.15, 35),
        (260, 566, COLORS["green"], 1.1, -50), (485, 610, COLORS["orange"], .9, 20),
        (702, 640, COLORS["pink"], .85, 90), (835, 535, COLORS["green"], .8, -10)
    ]:
        hold(d, *args)
    d.line(xy([(230, 520), (380, 372), (560, 514), (730, 390), (842, 560)]), fill=COLORS["green_dark"], width=sc(7))
    climber(d, 230, 504, 1.05, -1, COLORS["orange"])
    climber(d, 482, 510, .95, 1, COLORS["blue"])
    climber(d, 735, 365, .92, -1, COLORS["red"])
    climber(d, 820, 565, .74, 1, COLORS["green_dark"])
    # Small celebration spark marks.
    for x, y, c in [(160, 190, COLORS["red"]), (710, 190, COLORS["yellow"]), (850, 260, COLORS["orange"])]:
        d.line(xy([(x - 16, y), (x + 16, y)]), fill=c, width=sc(6))
        d.line(xy([(x, y - 16), (x, y + 16)]), fill=c, width=sc(6))


def all_disciplines(img):
    d = ImageDraw.Draw(img)
    draw_shadowed_badge(img, (78, 76, 946, 948), COLORS["green_dark"], radius=96)
    draw_wall(d, 2)
    # Boulder holds
    for args in [
        (230, 310, COLORS["red"], 1.05, 20), (404, 310, COLORS["blue"], .9, -10),
        (560, 428, COLORS["orange"], 1, 62), (732, 350, COLORS["pink"], .85, 15),
        (285, 665, COLORS["green"], 1.1, -50), (678, 718, COLORS["red_dark"], .95, 25)
    ]:
        hold(d, *args)
    # Top rope line
    d.line(xy([(766, 150), (766, 790)]), fill=COLORS["white"], width=sc(7))
    d.ellipse((sc(742), sc(132), sc(790), sc(180)), outline=COLORS["white"], width=sc(7))
    # Speed arrow
    d.line(xy([(240, 760), (470, 318)]), fill=COLORS["orange"], width=sc(12))
    d.polygon(xy([(468, 306), (468, 374), (526, 340)]), fill=COLORS["orange"])
    # Quickdraw
    d.rounded_rectangle((sc(665), sc(480), sc(722), sc(578)), radius=sc(22), outline=COLORS["red"], width=sc(10))
    d.rounded_rectangle((sc(704), sc(560), sc(762), sc(658)), radius=sc(22), outline=COLORS["red"], width=sc(10))
    d.line(xy([(710, 558), (720, 582)]), fill=COLORS["red"], width=sc(10))
    # Climber
    climber(d, 514, 504, 1.08, -1, COLORS["green_dark"])
    # discipline labels as symbols, no text
    d.ellipse((sc(186), sc(708), sc(226), sc(748)), fill=COLORS["white"])
    d.rectangle((sc(835), sc(520), sc(890), sc(575)), fill=COLORS["white"])


paths = [
    save_icon("all-skill-levels", all_skill_levels),
    save_icon("thriving-community", thriving_community),
    save_icon("all-disciplines", all_disciplines),
]

# Preview sheet.
sheet = Image.new("RGBA", (1800, 700), "#f5f5f5")
sd = ImageDraw.Draw(sheet)
labels = ["All Skill Levels", "Thriving Community", "All Disciplines"]
for i, path in enumerate(paths):
    x = 80 + i * 570
    y = 90
    card = Image.new("RGBA", (470, 520), (255, 255, 255, 255))
    mask = Image.new("L", card.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, 470, 520), radius=36, fill=255)
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((0, 18, 470, 520), radius=36, fill=(0, 0, 0, 36))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    sheet.alpha_composite(shadow, (x, y))
    sheet.alpha_composite(card, (x, y))
    icon = Image.open(path).convert("RGBA").resize((360, 360), Image.Resampling.LANCZOS)
    sheet.alpha_composite(icon, (x + 55, y + 42))
    sd.text((x + 235, y + 444), labels[i], anchor="mm", fill=COLORS["ink"])
sheet.convert("RGB").save(OUT / "preview.png", quality=95)

for path in paths:
    print(path)
print(OUT / "preview.png")

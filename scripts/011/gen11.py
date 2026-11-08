# Dessins de la video 011 (Ludger Sylbaris, montagne Pelee). Apres gen_images.py et gen13.py.
SKIN = (150, 100, 70)

def stone_cell(seed=60, dark=0.55, slit_glow=0.0, slit_col=(255, 200, 120)):
    """Cachot : pierres, porte epaisse avec une fente, sol de terre."""
    im = paper(seed, dark, (52, 46, 40)); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for row in range(0, 1500, 110):
        off = 0 if (row//110) % 2 == 0 else 90
        for x in range(-off, W, 180):
            c = 34 + rnd.randint(-6, 6)
            d.rounded_rectangle((x + 6, row + 6, x + 172, row + 102), radius=14, fill=(c, c - 4, c - 8, 255), outline=(16, 12, 10, 255), width=4)
    d.rectangle((0, 1500, W, H), fill=(30, 22, 16, 255))
    # porte
    d.rectangle((560, 520, 960, 1500), fill=(44, 30, 20, 255), outline=INK+(255,), width=8)
    for y in (640, 1000, 1360): d.rectangle((560, y, 960, y + 34), fill=(30, 30, 34, 255), outline=INK+(255,), width=3)
    poly_hatch(im, [(560, 520), (960, 520), (960, 1500), (560, 1500)], 16, 0.0, (10, 6, 3, 110), 4); d = ImageDraw.Draw(im)
    d.rectangle((690, 760, 830, 784), fill=(6, 4, 3, 255))  # la fente
    if slit_glow > 0:
        d.rectangle((690, 760, 830, 784), fill=slit_col + (255,))
        glow(im, (760, 772), 160, slit_col, 0.5*slit_glow)
    return im

def prisoner(im, cx, cy, s=1.0, mood=1, burnt=False):
    """Homme assis, genoux replies, chemise claire de marin, visage simple."""
    d = ImageDraw.Draw(im)
    shirt = (190, 180, 160) if not burnt else (120, 90, 70)
    # jambes repliees
    d.polygon([(cx - 150*s, cy + 330*s), (cx - 40*s, cy + 120*s), (cx + 120*s, cy + 160*s), (cx + 200*s, cy + 330*s)], fill=(40, 40, 52, 255), outline=INK+(255,))
    # torse
    d.polygon([(cx - 110*s, cy + 260*s), (cx - 90*s, cy - 10*s), (cx + 90*s, cy - 10*s), (cx + 110*s, cy + 260*s)], fill=shirt + (255,), outline=INK+(255,))
    for k in range(4): d.line((cx - 90*s, cy + 40*s + k*50*s, cx + 90*s, cy + 40*s + k*50*s), fill=(60, 70, 120, 255), width=int(8*s))  # rayures de marin
    # bras autour des genoux
    d.line((cx - 90*s, cy + 20*s, cx + 60*s, cy + 200*s), fill=SKIN + (255,), width=int(40*s))
    d.line((cx + 90*s, cy + 20*s, cx + 120*s, cy + 190*s), fill=SKIN + (255,), width=int(40*s))
    if burnt:
        for k in range(6):
            x = cx - 60*s + k*30*s; d.ellipse((x - 14*s, cy + 60*s + (k % 3)*40*s, x + 14*s, cy + 84*s + (k % 3)*40*s), fill=(150, 40, 30, 255))
    # tete
    d.ellipse((cx - 70*s, cy - 170*s, cx + 70*s, cy - 10*s), fill=SKIN + (255,), outline=INK+(255,), width=4)
    d.chord((cx - 72*s, cy - 178*s, cx + 72*s, cy - 70*s), 180, 360, fill=(20, 14, 10, 255))  # cheveux
    ey = cy - 90*s
    for sx in (-1, 1):
        d.line((cx + sx*30*s - 14*s*sx, ey - 22*s - mood*4, cx + sx*30*s + 14*s*sx, ey - 16*s), fill=INK+(255,), width=int(5*s))
        d.ellipse((cx + sx*30*s - 10*s, ey - 6*s, cx + sx*30*s + 10*s, ey + 8*s), fill=(240, 236, 220, 255), outline=INK+(255,), width=2)
        d.ellipse((cx + sx*30*s - 4*s, ey - 3*s, cx + sx*30*s + 4*s, ey + 5*s), fill=INK+(255,))
    d.arc((cx - 22*s, cy - 46*s, cx + 22*s, cy - 26*s), 200, 340, fill=INK+(255,), width=int(4*s))

def small_town(im, y_base=1390, seed=31, lit=True):
    rnd = random.Random(seed); d = ImageDraw.Draw(im); x = -20
    while x < W + 20:
        w = rnd.randint(60, 110); h = rnd.randint(70, 170)
        d.polygon([(x, y_base), (x, y_base - h), (x + w/2, y_base - h - 40), (x + w, y_base - h), (x + w, y_base)], fill=(16, 11, 9, 255), outline=(40, 26, 18, 255))
        for wx in range(x + 12, x + w - 18, 26):
            for wy in range(y_base - h + 16, y_base - 20, 40):
                d.rectangle((wx, wy, wx + 10, wy + 16), fill=(240, 170, 60, 255) if (lit and rnd.random() < 0.3) else (34, 22, 16, 255))
        x += w - 2

def volcano_town(im, smoke=True, lit=True, sea=True):
    d = ImageDraw.Draw(im)
    pts = [(-200, 1400), (300, 640), (430, 560), (560, 580), (700, 700), (1280, 1400)]
    d.polygon(pts, fill=(62, 52, 46, 255), outline=(20, 16, 14, 255))
    poly_hatch(im, pts, 18, 0.6, (14, 10, 8, 110), 3); d = ImageDraw.Draw(im)
    if smoke:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g); rnd = random.Random(3)
        for i in range(10):
            r = 50 + i*20; x = 480 + rnd.randint(-30, 30) + i*12; y = 520 - i*42
            gd.ellipse((x - r, y - r, x + r, y + r), fill=(80, 74, 70, 190))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    if sea:
        d.rectangle((0, 1390, W, H), fill=(22, 34, 52, 255))
        for k in range(18): d.line(((k*67) % W, 1430 + (k*37) % 400, (k*67) % W + 80, 1430 + (k*37) % 400), fill=(60, 80, 110, 255), width=3)
    small_town(im, 1395, 31, lit)

def cloud_layer(im, cx, cy, r, col=(80, 70, 66), hot=True, seed=0):
    """Nuee ardente : boules de fumee + coeur incandescent."""
    rnd = random.Random(seed); g = Image.new("RGBA", im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for i in range(26):
        a = rnd.uniform(0, 2*math.pi); dd = rnd.uniform(0, r*0.8); rr = rnd.uniform(r*0.25, r*0.55)
        x, y = cx + dd*math.cos(a)*1.3, cy + dd*math.sin(a)*0.7
        f = rnd.uniform(0.75, 1.2); c = tuple(min(255, int(v*f)) for v in col)
        gd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=c + (235,))
    g = g.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(g)
    if hot: glow(im, (int(cx), int(cy + r*0.4)), int(r*0.9), (255, 110, 30), 0.55)

def ruins(im, seed=70):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for k in range(9):
        x = 20 + k*120 + rnd.randint(-20, 20); h = rnd.randint(140, 420)
        pts = [(x, 1400), (x, 1400 - h), (x + 30, 1400 - h + rnd.randint(10, 60)), (x + 60, 1400 - h - rnd.randint(0, 40)), (x + 100, 1400 - h + rnd.randint(20, 90)), (x + 110, 1400)]
        d.polygon(pts, fill=(48, 42, 38, 255), outline=(16, 12, 10, 255))
        for wy in range(1400 - h + 60, 1380, 90):
            d.rectangle((x + 30, wy, x + 60, wy + 40), fill=(10, 8, 6, 255))
    d.rectangle((0, 1400, W, H), fill=(54, 50, 46, 255))
    for k in range(80):
        x, y = rnd.randint(0, W), rnd.randint(1400, 1900); r = rnd.randint(6, 24)
        d.ellipse((x - r, y - r*0.6, x + r, y + r*0.6), fill=(70 + rnd.randint(0, 30), 64, 58, 255))
    smoke(im, 300, 1150, 4); smoke(im, 800, 1100, 5)

def rescuer(L, x, y, s=1.0, lamp=True):
    figure(L, x, y, s, col=(14, 12, 10), hat=True)
    if lamp:
        d = ImageDraw.Draw(L); d.line((x + 26*s, y - 170*s, x + 80*s, y - 120*s), fill=(14, 12, 10, 255), width=int(12*s))
        d.rectangle((x + 66*s, y - 130*s, x + 96*s, y - 90*s), fill=(255, 210, 120, 255), outline=INK+(255,), width=2)
        glow(L, (int(x + 81*s), int(y - 110*s)), int(90*s), (255, 200, 110), 0.6)

def circus(im, seed=80):
    d = ImageDraw.Draw(im)
    # chapiteau a rayures
    cx, top, base = 540, 800, 1340
    for k in range(10):
        x0 = cx - 520 + k*104; x1 = x0 + 104
        col = (180, 30, 34, 255) if k % 2 == 0 else (230, 214, 180, 255)
        d.polygon([(cx, top), (x0, base), (x1, base)], fill=col, outline=INK+(255,))
    d.line((cx, top, cx, top - 120), fill=INK+(255,), width=8); d.polygon([(cx, top - 120), (cx + 90, top - 95), (cx, top - 70)], fill=(200, 160, 50, 255))
    d.rectangle((cx - 90, base - 260, cx + 90, base), fill=(10, 8, 6, 255))
    # guirlande d'ampoules
    for k in range(16):
        x = 40 + k*65; y = 780 + 40*math.sin(k*0.7)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 220, 120, 255)); glow(im, (x, int(y)), 24, (255, 210, 110), 0.4)
    d.rectangle((0, base, W, H), fill=(54, 40, 26, 255))

def cage_wagon(im, cx, cy, s=1.0, with_man=True):
    d = ImageDraw.Draw(im)
    d.rectangle((cx - 300*s, cy - 320*s, cx + 300*s, cy), fill=(120, 24, 28, 255), outline=INK+(255,), width=6)
    d.rectangle((cx - 260*s, cy - 290*s, cx + 260*s, cy - 30*s), fill=(30, 24, 20, 255), outline=(200, 160, 50, 255), width=6)
    # pierres peintes = copie de la cellule
    for row in range(3):
        for k in range(5):
            d.rectangle((cx - 250*s + k*100*s + (row % 2)*40*s, cy - 280*s + row*84*s, cx - 165*s + k*100*s + (row % 2)*40*s, cy - 210*s + row*84*s), outline=(60, 54, 48, 255), width=3)
    if with_man:
        figure(im, cx, cy - 40*s, 0.95*s, col=(190, 180, 160))
        d.ellipse((cx - 24*s, cy - 290*s, cx + 24*s, cy - 242*s), fill=SKIN + (255,))
    for k in range(9):
        x = cx - 260*s + k*65*s; d.rectangle((x - 5*s, cy - 290*s, x + 5*s, cy - 30*s), fill=(200, 160, 50, 255))
    for wx in (cx - 200*s, cx + 200*s):
        r = 70*s; d.ellipse((wx - r, cy - r + 30*s, wx + r, cy + r + 30*s), outline=(30, 20, 12, 255), width=int(14*s))
        d.ellipse((wx - 18*s, cy + 12*s, wx + 18*s, cy + 48*s), fill=(200, 160, 50, 255))
    f = ImageFont.truetype(FS, int(40*s)); t = "L'HOMME DU JUGEMENT DERNIER"
    while f.getlength(t) > 560*s: f = ImageFont.truetype(FS, f.size - 2)
    d.rectangle((cx - 300*s, cy - 380*s, cx + 300*s, cy - 322*s), fill=(230, 214, 180, 255), outline=INK+(255,), width=4)
    d.text((cx - f.getlength(t)/2, cy - 374*s), t, font=f, fill=(150, 20, 24, 255))

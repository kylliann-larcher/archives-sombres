# Dessins propres a la video 017 (pierres de la faim). Reutilise gen016 (-> gen015 -> gen008 -> gen010).
exec(open(f"{HERE}/gen016.py", encoding="utf-8").read())

FSERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def fserif(sz): return ImageFont.truetype(FSERIF, sz)

def sky_river(im, level=0.0, cracked=False, seed=1, dusk=False):
    """Vallee de l'Elbe : ciel, collines, fleuve. level 0 = plein, 1 = presque a sec."""
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    top = (190, 120, 70) if dusk else (150, 120, 90)
    for y in range(0, 1150, 6):
        k = y/1150; c = tuple(int(top[i]*(1-k) + (220, 180, 120)[i]*k) for i in range(3))
        d.rectangle((0, y, W, y + 6), fill=c + (255,))
    glow(im, (760, 760), 160, (255, 220, 150), 0.7 if not dusk else 0.5)
    d = ImageDraw.Draw(im); d.ellipse((700, 700, 820, 820), fill=(255, 236, 190, 255))
    for k, (yb, col) in enumerate(((1060, (92, 74, 54)), (1120, (64, 50, 36)))):
        pts = [(0, H)]
        for x in range(0, W + 60, 60): pts.append((x, yb - 90*math.sin(x/170 + k*2) - 40*math.sin(x/53 + k)))
        pts.append((W, H)); d.polygon(pts, fill=col + (255,))
    bank = 1180
    d.rectangle((0, bank, W, H), fill=(110, 86, 58, 255))
    water_top = int(bank + 40 + level*420)
    mud = (128, 100, 66)
    d.rectangle((0, bank + 40, W, H), fill=mud + (255,))
    if cracked:
        for _ in range(140):
            x = rnd.randint(0, W); y = rnd.randint(bank + 60, H)
            for _ in range(3):
                x2 = x + rnd.randint(-70, 70); y2 = y + rnd.randint(-30, 30)
                d.line((x, y, x2, y2), fill=(60, 44, 28, 255), width=3); x, y = x2, y2
    wc = (54, 76, 92)
    d.rectangle((0, water_top, W, H), fill=wc + (255,))
    for _ in range(60):
        x = rnd.randint(0, W); y = rnd.randint(water_top + 10, H)
        d.line((x, y, x + rnd.randint(30, 90), y), fill=(120, 150, 160, 160), width=3)
    return water_top

def hunger_stone(im, cx, cy, s=1.0, inscription=True, dates=(), sub=0.0):
    """Gros rocher grave. sub = part immergee (0 a 1) dessinee par l'appelant via l'eau."""
    d = ImageDraw.Draw(im)
    pts = [(cx-330*s, cy+170*s), (cx-360*s, cy+20*s), (cx-300*s, cy-150*s), (cx-120*s, cy-230*s), (cx+110*s, cy-240*s),
           (cx+300*s, cy-170*s), (cx+370*s, cy-10*s), (cx+340*s, cy+170*s)]
    d.polygon(pts, fill=(112, 104, 94, 255), outline=INK + (255,))
    d.line(pts + [pts[0]], fill=INK + (255,), width=int(8*s))
    # ombre et relief
    poly_hatch(im, [(cx+120*s, cy-230*s), (cx+300*s, cy-170*s), (cx+370*s, cy-10*s), (cx+340*s, cy+170*s), (cx+120*s, cy+170*s)], step=14, col=(0, 0, 0, 70), w=3)
    d = ImageDraw.Draw(im)
    rnd = random.Random(int(cx))
    for _ in range(26):
        x = cx + rnd.randint(-300, 300)*s; y = cy + rnd.randint(-180, 150)*s
        d.ellipse((x-4*s, y-3*s, x+4*s, y+3*s), fill=(80, 74, 66, 255))
    # algues seches a la base
    d.rectangle((cx-340*s, cy+120*s, cx+350*s, cy+175*s), fill=(70, 78, 50, 200))
    if inscription:
        f = fserif(int(40*s))
        for k, line in enumerate(("WENN DU MICH", "SIEHST,", "DANN WEINE")):
            tw = f.getlength(line); y = cy - 175*s + k*58*s
            d.text((cx - tw/2 + 2, y + 3), line, font=f, fill=(46, 40, 34, 255))
            d.text((cx - tw/2, y), line, font=f, fill=(196, 188, 170, 255))
    fd = fserif(int(46*s))
    for (txt, x, y, col) in dates:
        d.text((cx + x*s + 2, cy + y*s + 3), txt, font=fd, fill=(40, 34, 30, 255))
        d.text((cx + x*s, cy + y*s), txt, font=fd, fill=col + (255,))

def water_over(im, top, seed=3):
    """Repeint l'eau devant le rocher a partir de y=top."""
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    d.rectangle((0, top, W, H), fill=(54, 76, 92, 235))
    for _ in range(40):
        x = rnd.randint(0, W); y = rnd.randint(top + 6, H)
        d.line((x, y, x + rnd.randint(30, 90), y), fill=(120, 150, 160, 160), width=3)
    d.line((0, top, W, top), fill=(170, 200, 210, 220), width=5)

def chisel(im, x, y, s=1.0, ang=-35):
    L = Image.new("RGBA", (int(420*s), int(420*s)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = 210*s
    d.rectangle((c-14*s, c-170*s, c+14*s, c+40*s), fill=(150, 150, 156, 255), outline=INK + (255,), width=3)
    d.polygon([(c-14*s, c+40*s), (c+14*s, c+40*s), (c, c+80*s)], fill=(190, 190, 196, 255), outline=INK + (255,))
    d.rounded_rectangle((c-24*s, c-200*s, c+24*s, c-150*s), radius=int(8*s), fill=(110, 70, 40, 255), outline=INK + (255,), width=3)
    L = L.rotate(ang, resample=Image.BICUBIC)
    im.paste(L, (int(x - L.width/2), int(y - L.height/2)), L)

def hammer(im, x, y, s=1.0, ang=30):
    L = Image.new("RGBA", (int(420*s), int(420*s)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = 210*s
    d.rectangle((c-10*s, c-40*s, c+10*s, c+170*s), fill=(120, 80, 46, 255), outline=INK + (255,), width=3)
    d.rectangle((c-70*s, c-90*s, c+70*s, c-30*s), fill=(90, 90, 96, 255), outline=INK + (255,), width=4)
    L = L.rotate(ang, resample=Image.BICUBIC)
    im.paste(L, (int(x - L.width/2), int(y - L.height/2)), L)

def dead_field(im, base=1500, seed=5):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    d.rectangle((0, base, W, H), fill=(150, 112, 62, 255))
    for _ in range(90):
        x = rnd.randint(0, W); y = rnd.randint(base, H); hgt = rnd.randint(60, 150)
        bend = rnd.randint(-50, 50)
        d.line((x, y, x + bend, y - hgt), fill=(96, 70, 34, 255), width=4)
        d.line((x + bend, y - hgt, x + bend + 26, y - hgt + 30), fill=(96, 70, 34, 255), width=4)
    for _ in range(120):
        x = rnd.randint(0, W); y = rnd.randint(base + 10, H)
        d.line((x, y, x + rnd.randint(-50, 50), y + rnd.randint(-15, 15)), fill=(90, 62, 30, 255), width=3)

def scorch_sun(im, cx, cy, r=150):
    glow(im, (cx, cy), r*2.4, (255, 150, 60), 0.8)
    d = ImageDraw.Draw(im); d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(255, 210, 120, 255))

def coin(im, cx, cy, r=70):
    d = ImageDraw.Draw(im)
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=GOLD + (255,), outline=INK + (255,), width=5)
    d.ellipse((cx-r*0.72, cy-r*0.72, cx+r*0.72, cy+r*0.72), outline=(150, 110, 30, 255), width=4)

def bread_scale(im, cx, cy, s=1.0):
    """Balance : une miche minuscule face a une pile de pieces."""
    d = ImageDraw.Draw(im)
    d.rectangle((cx-8*s, cy-260*s, cx+8*s, cy+200*s), fill=(60, 40, 24, 255), outline=INK + (255,), width=3)
    d.rectangle((cx-130*s, cy+200*s, cx+130*s, cy+230*s), fill=(60, 40, 24, 255), outline=INK + (255,), width=3)
    d.line((cx-280*s, cy-170*s, cx+280*s, cy-250*s), fill=INK + (255,), width=int(12*s))
    for (px, py) in ((cx-280*s, cy-170*s), (cx+280*s, cy-250*s)):
        d.line((px, py, px-90*s, py+150*s), fill=INK + (255,), width=4); d.line((px, py, px+90*s, py+150*s), fill=INK + (255,), width=4)
        d.chord((px-120*s, py+110*s, px+120*s, py+200*s), 0, 180, fill=(140, 110, 70, 255), outline=INK + (255,))
    d.ellipse((cx+250*s, cy-130*s, cx+310*s, cy-100*s), fill=(190, 140, 70, 255), outline=INK + (255,), width=3)

def hungry(im, x, y, s=1.0, col=(30, 24, 22)):
    """Silhouette maigre assise, genoux serres, tete basse."""
    d = ImageDraw.Draw(im)
    d.ellipse((x-34*s, y-300*s, x+34*s, y-232*s), fill=col + (255,))
    d.polygon([(x-40*s, y-230*s), (x+40*s, y-230*s), (x+70*s, y-60*s), (x-70*s, y-60*s)], fill=col + (255,))
    d.polygon([(x-70*s, y-60*s), (x+130*s, y-70*s), (x+150*s, y), (x-80*s, y)], fill=col + (255,))
    d.line((x+30*s, y-200*s, x+110*s, y-90*s), fill=col + (255,), width=int(16*s))
    d.ellipse((x-120*s, y-30*s, x+90*s, y+20*s), fill=(0, 0, 0, 90))

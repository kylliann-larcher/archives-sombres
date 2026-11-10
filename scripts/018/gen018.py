# Dessins propres a la video 018 (le Masque de fer). Reutilise gen017 (-> gen016 -> gen015 -> gen008 -> gen010).
exec(open(f"{HERE}/gen017.py", encoding="utf-8").read())

def cell_walls(im, seed=1, light=True):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    d.rectangle((0, 0, W, H), fill=(58, 52, 48, 255))
    for row, y in enumerate(range(0, H, 70)):
        off = 0 if row % 2 == 0 else 70
        for x in range(-off, W, 140):
            c = rnd.randint(-10, 10)
            d.rectangle((x + 3, y + 3, x + 137, y + 67), fill=(70 + c, 64 + c, 58 + c, 255), outline=(36, 32, 30, 255), width=3)
    if light:
        glow(im, (760, 1000), 260, (240, 230, 200), 0.45)
        d = ImageDraw.Draw(im); d.rectangle((680, 880, 840, 1100), fill=(200, 200, 190, 255), outline=INK + (255,), width=6)
        for x in range(700, 840, 34): d.line((x, 880, x, 1100), fill=INK + (255,), width=10)
    d = ImageDraw.Draw(im); d.rectangle((0, 1640, W, H), fill=(40, 34, 30, 255))
    for _ in range(40):
        x = rnd.randint(0, W); y = rnd.randint(1650, H); d.line((x, y, x + rnd.randint(20, 80), y), fill=(70, 60, 50, 255), width=3)

def masked_man(im, cx, cy, s=1.0, mask=True, shackle=False):
    """Buste d'homme en manteau sombre, visage couvert d'un masque de velours noir (tete en cx, cy)."""
    d = ImageDraw.Draw(im)
    # corps
    d.polygon([(cx-260*s, cy+620*s), (cx-210*s, cy+180*s), (cx-90*s, cy+120*s), (cx+90*s, cy+120*s), (cx+210*s, cy+180*s), (cx+260*s, cy+620*s)],
              fill=(46, 40, 48, 255), outline=INK + (255,))
    d.polygon([(cx-60*s, cy+120*s), (cx+60*s, cy+120*s), (cx+20*s, cy+260*s), (cx-20*s, cy+260*s)], fill=(214, 206, 188, 255), outline=INK + (255,))
    poly_hatch(im, [(cx+40*s, cy+140*s), (cx+210*s, cy+180*s), (cx+260*s, cy+620*s), (cx+60*s, cy+620*s)], step=14, col=(0, 0, 0, 80), w=3)
    d = ImageDraw.Draw(im)
    # cou et tete
    d.rectangle((cx-40*s, cy+60*s, cx+40*s, cy+130*s), fill=(214, 178, 140, 255), outline=INK + (255,), width=3)
    d.ellipse((cx-115*s, cy-150*s, cx+115*s, cy+110*s), fill=(214, 178, 140, 255), outline=INK + (255,), width=4)
    # cheveux longs
    for k in range(-6, 7):
        x = cx + k*20*s
        d.line((x, cy-140*s, x + k*6*s, cy+90*s if abs(k) > 4 else cy-110*s), fill=(60, 44, 30, 255), width=int(16*s))
    d.chord((cx-120*s, cy-170*s, cx+120*s, cy-40*s), 180, 360, fill=(60, 44, 30, 255))
    if mask:
        d.rounded_rectangle((cx-112*s, cy-80*s, cx+112*s, cy+105*s), radius=int(40*s), fill=(14, 12, 16, 255), outline=(40, 36, 44, 255), width=4)
        for ex in (-48, 48):
            d.ellipse((cx+(ex-22)*s, cy-40*s, cx+(ex+22)*s, cy-14*s), fill=(4, 2, 2, 255))
            d.ellipse((cx+(ex-6)*s, cy-32*s, cx+(ex+6)*s, cy-22*s), fill=(200, 190, 170, 255))
        d.line((cx-112*s, cy-40*s, cx-150*s, cy-10*s), fill=(14, 12, 16, 255), width=int(8*s))
        d.line((cx+112*s, cy-40*s, cx+150*s, cy-10*s), fill=(14, 12, 16, 255), width=int(8*s))
        # reflet du velours
    else:
        d.ellipse((cx-50*s, cy-36*s, cx-26*s, cy-20*s), fill=INK + (255,)); d.ellipse((cx+26*s, cy-36*s, cx+50*s, cy-20*s), fill=INK + (255,))
        d.line((cx-30*s, cy+50*s, cx+30*s, cy+50*s), fill=INK + (255,), width=4)
    if shackle:
        for hx in (-150, 150):
            d.ellipse((cx+(hx-40)*s, cy+460*s, cx+(hx+40)*s, cy+520*s), outline=(120, 120, 126, 255), width=int(12*s))
        d.line((cx-110*s, cy+490*s, cx+110*s, cy+490*s), fill=(120, 120, 126, 255), width=int(8*s))

def jailer(im, cx, base, s=1.0):
    """Officier en tricorne et manteau rouge sombre, de profil."""
    d = ImageDraw.Draw(im)
    d.polygon([(cx-90*s, base), (cx-70*s, base-420*s), (cx+70*s, base-420*s), (cx+100*s, base)], fill=(110, 30, 34, 255), outline=INK + (255,))
    d.rectangle((cx-75*s, base-260*s, cx+75*s, base-235*s), fill=(30, 20, 14, 255))
    d.ellipse((cx-55*s, base-540*s, cx+55*s, base-420*s), fill=(214, 178, 140, 255), outline=INK + (255,), width=3)
    d.polygon([(cx-100*s, base-520*s), (cx+100*s, base-520*s), (cx, base-600*s)], fill=(20, 14, 12, 255))
    d.ellipse((cx+10*s, base-500*s, cx+28*s, base-486*s), fill=INK + (255,))
    for k in range(4): d.ellipse((cx-8*s, base-400*s + k*40*s, cx+8*s, base-384*s + k*40*s), fill=GOLD + (255,))

def fortress_rock(im, cx, base, s=1.0, sea=True):
    d = ImageDraw.Draw(im)
    if sea:
        d.rectangle((0, base - 20*s, W, H), fill=(40, 62, 84, 255))
        for k in range(30): x = (k*97) % W; y = base + (k*53) % 500; d.line((x, y, x + 60, y), fill=(110, 140, 160, 180), width=3)
    d.polygon([(cx-420*s, base), (cx-300*s, base-160*s), (cx+300*s, base-180*s), (cx+440*s, base)], fill=(96, 86, 72, 255), outline=INK + (255,))
    d.rectangle((cx-300*s, base-420*s, cx+300*s, base-160*s), fill=(150, 136, 112, 255), outline=INK + (255,), width=5)
    for x in range(int(cx-300*s), int(cx+300*s), int(50*s)): d.rectangle((x, base-450*s, x + 26*s, base-420*s), fill=(150, 136, 112, 255), outline=INK + (255,), width=3)
    for wx in (-180, 0, 180): d.rectangle((cx+(wx-14)*s, base-340*s, cx+(wx+14)*s, base-290*s), fill=(20, 16, 14, 255))

def bastille(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-380*s, base-420*s, cx+380*s, base), fill=(110, 100, 88, 255), outline=INK + (255,), width=5)
    for tx in (-380, -130, 130, 380):
        d.rectangle((cx+(tx-80)*s, base-560*s, cx+(tx+80)*s, base), fill=(124, 112, 98, 255), outline=INK + (255,), width=5)
        for k in range(4): d.rectangle((cx+(tx-80+k*44)*s, base-590*s, cx+(tx-56+k*44)*s, base-560*s), fill=(124, 112, 98, 255), outline=INK + (255,), width=3)
        d.rectangle((cx+(tx-10)*s, base-460*s, cx+(tx+10)*s, base-420*s), fill=(20, 16, 14, 255))
    poly_hatch(im, [(cx-380*s, base-420*s), (cx+460*s, base-420*s), (cx+460*s, base), (cx-380*s, base)], step=16, col=(0, 0, 0, 50), w=3)

def route_map(im, cx, cy, active=3, s=1.0):
    """Carte schematique : Pignerol -> Exilles -> Sainte-Marguerite -> Bastille."""
    d = ImageDraw.Draw(im)
    d.rectangle((cx-380*s, cy-460*s, cx+380*s, cy+460*s), fill=(214, 196, 156, 255), outline=INK + (255,), width=6)
    pts = [(cx+220*s, cy+40*s), (cx+40*s, cy+340*s), (cx-120*s, cy-320*s)]
    names = ["PIGNEROL", "STE-MARGUERITE", "BASTILLE"]
    for k in range(max(0, min(active, 2))):
        d.line((pts[k], pts[k+1]), fill=(170, 30, 30, 255), width=int(8*s))
    f = font(int(40*s))
    for k, (p, n) in enumerate(zip(pts, names)):
        if k > active: continue
        d.ellipse((p[0]-16*s, p[1]-16*s, p[0]+16*s, p[1]+16*s), fill=(170, 30, 30, 255), outline=INK + (255,), width=3)
        tw = f.getlength(n); x = min(max(p[0] - tw/2, cx-360*s), cx+360*s - tw)
        d.text((x, p[1] - 58*s), n, font=f, fill=INK + (255,))

def grave_name(im, cx, cy, s=1.0, name="MARCHIOLY"):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx-230*s, cy-300*s, cx+230*s, cy+340*s), radius=int(200*s), fill=(116, 110, 100, 255), outline=INK+(255,), width=5)
    hatch(d, (cx-230*s, cy-300*s, cx+230*s, cy+340*s), 14, 0.5, (30, 28, 24, 90), 3)
    d.line((cx, cy-240*s, cx, cy-130*s), fill=(40, 34, 30, 255), width=int(10*s)); d.line((cx-45*s, cy-200*s, cx+45*s, cy-200*s), fill=(40, 34, 30, 255), width=int(10*s))
    d.rectangle((cx-280*s, cy+330*s, cx+280*s, cy+370*s), fill=(80, 74, 66, 255), outline=INK+(255,), width=4); f = fserif(int(54*s)); tw = f.getlength(name)
    d.text((cx - tw/2, cy - 40*s), name, font=f, fill=(40, 34, 30, 255))
    f2 = fserif(int(46*s)); t2 = "1703"; d.text((cx - f2.getlength(t2)/2, cy + 40*s), t2, font=f2, fill=(40, 34, 30, 255))

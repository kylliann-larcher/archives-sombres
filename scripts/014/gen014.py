# Dessins propres a la video 014 (Jacques de Molay). Reutilise gen010 + gen008.
exec(open(f"{HERE}/gen008.py", encoding="utf-8").read())

def templar(im, cx, cy, s=1.0, mood=1, chains=False, cross=True):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-230*s, cy+520*s), (cx-130*s, cy+160*s), (cx+130*s, cy+160*s), (cx+230*s, cy+520*s)], fill=(228, 224, 212, 255), outline=INK+(255,))
    hatch(d, (cx-230*s, cy+160*s, cx+230*s, cy+520*s), 16, 0.3, (60, 56, 50, 70), 3)
    if cross:
        d.rectangle((cx-18*s, cy+210*s, cx+18*s, cy+400*s), fill=(176, 30, 30, 255)); d.rectangle((cx-70*s, cy+260*s, cx+70*s, cy+296*s), fill=(176, 30, 30, 255))
    if chains:
        for k in range(8):
            d.ellipse((cx-150*s+k*40*s, cy+170*s+k*4*s, cx-120*s+k*40*s, cy+200*s+k*4*s), outline=(120, 120, 126, 255), width=int(6*s))
    d.ellipse((cx-95*s, cy-100*s, cx+95*s, cy+130*s), fill=(214, 172, 138, 255), outline=INK+(255,), width=4)
    d.pieslice((cx-102*s, cy-120*s, cx+102*s, cy+40*s), 180, 360, fill=(235, 232, 222, 255), outline=INK+(255,), width=3)
    d.polygon([(cx-90*s, cy+30*s), (cx-60*s, cy+210*s), (cx, cy+260*s), (cx+60*s, cy+210*s), (cx+90*s, cy+30*s), (cx+60*s, cy+60*s), (cx-60*s, cy+60*s)], fill=(150, 146, 140, 255), outline=INK+(255,), width=3)
    ey = cy
    for sx in (-1, 1):
        d.line((cx+sx*38*s-20*s*sx, ey-30*s-mood*5, cx+sx*38*s+20*s*sx, ey-22*s+mood*4), fill=INK+(255,), width=int(6*s))
        d.ellipse((cx+sx*38*s-15*s, ey-10*s, cx+sx*38*s+15*s, ey+12*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=3)
        d.ellipse((cx+sx*38*s-6*s, ey-5*s, cx+sx*38*s+6*s, ey+9*s), fill=INK+(255,))
    d.line((cx, ey+8*s, cx-8*s, cy+50*s), fill=INK+(255,), width=int(5*s))

def cardinal(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-170*s, cy+480*s), (cx-90*s, cy+120*s), (cx+90*s, cy+120*s), (cx+170*s, cy+480*s)], fill=(160, 24, 32, 255), outline=INK+(255,))
    hatch(d, (cx-170*s, cy+120*s, cx+170*s, cy+480*s), 14, 0.4, (40, 6, 8, 90), 3)
    d.polygon([(cx-40*s, cy+120*s), (cx+40*s, cy+120*s), (cx, cy+200*s)], fill=(236, 230, 214, 255))
    d.ellipse((cx-70*s, cy-80*s, cx+70*s, cy+130*s), fill=(214, 172, 138, 255), outline=INK+(255,), width=3)
    d.polygon([(cx-80*s, cy-50*s), (cx-60*s, cy-110*s), (cx+60*s, cy-110*s), (cx+80*s, cy-50*s)], fill=(170, 26, 34, 255), outline=INK+(255,), width=3)
    for sx in (-1, 1): d.ellipse((cx+sx*26*s-8*s, cy-6*s, cx+sx*26*s+8*s, cy+10*s), fill=INK+(255,))
    d.line((cx-24*s, cy+60*s, cx+24*s, cy+60*s), fill=INK+(255,), width=int(4*s))

def notre_dame(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im); g = (112, 106, 98, 255)
    d.rectangle((cx-420*s, base-760*s, cx+420*s, base), fill=g, outline=INK+(255,), width=5)
    for sx in (-1, 1): d.rectangle((cx+sx*300*s-120*s, base-1000*s, cx+sx*300*s+120*s, base-760*s), fill=g, outline=INK+(255,), width=5)
    d.rectangle((cx-420*s, base-800*s, cx+420*s, base-770*s), fill=(88, 82, 76, 255))
    d.ellipse((cx-130*s, base-640*s, cx+130*s, base-380*s), fill=(60, 80, 130, 255), outline=INK+(255,), width=6)
    d.ellipse((cx-60*s, base-570*s, cx+60*s, base-450*s), fill=(190, 150, 70, 255), outline=INK+(255,), width=4)
    for sx in (-1, 0, 1):
        d.rounded_rectangle((cx+sx*270*s-90*s, base-360*s, cx+sx*270*s+90*s, base), radius=int(90*s), fill=(20, 16, 16, 255), outline=INK+(255,), width=4)
    hatch(d, (cx-420*s, base-760*s, cx+420*s, base), 22, 0.1, (30, 26, 22, 70), 3)

def seine(im, y0, seed=1):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    d.rectangle((0, y0, W, H), fill=(14, 20, 34, 255))
    for k in range(60):
        y = y0 + rnd.randint(10, H - y0); x = rnd.randint(-100, W); L = rnd.randint(80, 300)
        d.line((x, y, x+L, y), fill=(60, 80, 110, 160), width=3)

def pyre(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im)
    for sx in (-1, 1):
        x = cx + sx*150*s
        d.rectangle((x-20*s, base-520*s, x+20*s, base), fill=(40, 28, 20, 255), outline=INK+(255,), width=3)
    d.polygon([(cx-300*s, base+60*s), (cx-220*s, base-60*s), (cx+220*s, base-60*s), (cx+300*s, base+60*s)], fill=(60, 40, 26, 255), outline=INK+(255,), width=4)
    hatch(d, (cx-300*s, base-60*s, cx+300*s, base+60*s), 14, 0.3, (20, 10, 4, 120), 3)

def mitre(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-170*s, cy+480*s), (cx-90*s, cy+120*s), (cx+90*s, cy+120*s), (cx+170*s, cy+480*s)], fill=(236, 230, 214, 255), outline=INK+(255,))
    d.polygon([(cx-40*s, cy+120*s), (cx+40*s, cy+120*s), (cx, cy+230*s)], fill=(190, 150, 60, 255))
    d.ellipse((cx-70*s, cy-80*s, cx+70*s, cy+130*s), fill=(214, 172, 138, 255), outline=INK+(255,), width=3)
    d.polygon([(cx-80*s, cy-60*s), (cx, cy-260*s), (cx+80*s, cy-60*s)], fill=(236, 226, 190, 255), outline=INK+(255,), width=3)
    d.line((cx, cy-250*s, cx, cy-130*s), fill=(190, 150, 60, 255), width=int(8*s))
    for sx in (-1, 1): d.ellipse((cx+sx*26*s-8*s, cy-6*s, cx+sx*26*s+8*s, cy+10*s), fill=INK+(255,))
    d.line((cx-24*s, cy+60*s, cx+24*s, cy+60*s), fill=INK+(255,), width=int(4*s))

def throne_king(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-260*s, cy-300*s, cx+260*s, cy+520*s), fill=(90, 24, 34, 255), outline=INK+(255,), width=5)
    hatch(d, (cx-260*s, cy-300*s, cx+260*s, cy+520*s), 16, 0.4, (30, 4, 8, 90), 3)
    d.polygon([(cx-200*s, cy+520*s), (cx-110*s, cy+170*s), (cx+110*s, cy+170*s), (cx+200*s, cy+520*s)], fill=(40, 50, 120, 255), outline=INK+(255,))
    d.polygon([(cx-40*s, cy+170*s), (cx+40*s, cy+170*s), (cx, cy+300*s)], fill=(236, 230, 214, 255))
    d.ellipse((cx-85*s, cy-90*s, cx+85*s, cy+150*s), fill=(214, 172, 138, 255), outline=INK+(255,), width=4)
    crown_obj(im, cx, cy-120*s, 0.7*s)
    d = ImageDraw.Draw(im)
    for sx in (-1, 1):
        d.line((cx+sx*50*s-18*s*sx, cy-14*s, cx+sx*50*s+18*s*sx, cy-6*s), fill=INK+(255,), width=int(6*s))
        d.ellipse((cx+sx*34*s-13*s, cy-2*s, cx+sx*34*s+13*s, cy+16*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=3)
        d.ellipse((cx+sx*34*s-5*s, cy+2*s, cx+sx*34*s+5*s, cy+14*s), fill=INK+(255,))
    d.line((cx-30*s, cy+80*s, cx+30*s, cy+76*s), fill=INK+(255,), width=int(5*s))

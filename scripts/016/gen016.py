# Dessins propres a la video 016 (sommeil en deux temps). Reutilise gen015 (-> gen008 -> gen010).
exec(open(f"{HERE}/gen015.py", encoding="utf-8").read())

def moon_window(im, cx, cy, s=1.0, dawn=False):
    d = ImageDraw.Draw(im)
    sky = (60, 70, 120) if not dawn else (170, 110, 80)
    d.rectangle((cx-150*s, cy-210*s, cx+150*s, cy+210*s), fill=sky+(255,), outline=INK+(255,), width=int(10*s))
    if dawn: glow(im, (cx, cy+160*s), 200*s, (255, 190, 120), 0.6)
    else:
        d.ellipse((cx+20*s, cy-150*s, cx+100*s, cy-70*s), fill=(236, 230, 200, 255))
        for k in range(9):
            x = cx-130*s + (k*53 % 260)*s; y = cy-190*s + (k*71 % 360)*s
            d.ellipse((x-3, y-3, x+3, y+3), fill=(230, 230, 210, 255))
    d = ImageDraw.Draw(im)
    d.line((cx, cy-210*s, cx, cy+210*s), fill=INK+(255,), width=int(10*s)); d.line((cx-150*s, cy, cx+150*s, cy), fill=INK+(255,), width=int(10*s))

def sleeper(im, cx, cy, s=1.0, awake=False):
    """Lit a baldaquin simple, dormeur (yeux fermes) ou assis eveille."""
    d = ImageDraw.Draw(im)
    d.rectangle((cx-340*s, cy-330*s, cx-305*s, cy+170*s), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.rectangle((cx+305*s, cy-330*s, cx+340*s, cy+170*s), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.rectangle((cx-345*s, cy-360*s, cx+345*s, cy-320*s), fill=(90, 30, 34, 255), outline=INK+(255,), width=4)
    d.polygon([(cx-310*s, cy+10*s), (cx+310*s, cy+10*s), (cx+310*s, cy+130*s), (cx-310*s, cy+130*s)], fill=(70, 50, 34, 255), outline=INK+(255,))
    d.ellipse((cx-290*s, cy-70*s, cx-130*s, cy+30*s), fill=(214, 208, 192, 255), outline=INK+(255,), width=3)
    if awake:
        # assis : buste droit, couverture sur les jambes
        d.polygon([(cx-60*s, cy+20*s), (cx+300*s, cy+20*s), (cx+300*s, cy-40*s), (cx-60*s, cy-60*s)], fill=(150, 140, 120, 255), outline=INK+(255,))
        d.polygon([(cx-170*s, cy+20*s), (cx-50*s, cy+20*s), (cx-60*s, cy-170*s), (cx-160*s, cy-170*s)], fill=(222, 214, 196, 255), outline=INK+(255,))
        d.ellipse((cx-170*s, cy-300*s, cx-50*s, cy-170*s), fill=(226, 190, 150, 255), outline=INK+(255,), width=3)
        d.chord((cx-176*s, cy-312*s, cx-44*s, cy-200*s), 180, 360, fill=(236, 232, 220, 255), outline=INK+(255,))
        d.ellipse((cx-135*s, cy-245*s, cx-121*s, cy-231*s), fill=INK+(255,)); d.ellipse((cx-98*s, cy-245*s, cx-84*s, cy-231*s), fill=INK+(255,))
        d.arc((cx-125*s, cy-215*s, cx-95*s, cy-195*s), 200, 340, fill=INK+(255,), width=3)
    else:
        d.polygon([(cx-140*s, cy+20*s), (cx+300*s, cy+20*s), (cx+300*s, cy-50*s), (cx-140*s, cy-80*s)], fill=(150, 140, 120, 255), outline=INK+(255,))
        hatch(d, (cx-140*s, cy-80*s, cx+300*s, cy+20*s), 16, 0.3, (30, 26, 20, 100), 3)
        d.ellipse((cx-255*s, cy-130*s, cx-145*s, cy-20*s), fill=(226, 190, 150, 255), outline=INK+(255,), width=3)
        d.chord((cx-262*s, cy-142*s, cx-138*s, cy-60*s), 180, 360, fill=(236, 232, 220, 255), outline=INK+(255,))
        d.arc((cx-225*s, cy-80*s, cx-200*s, cy-66*s), 0, 180, fill=INK+(255,), width=3); d.arc((cx-190*s, cy-80*s, cx-165*s, cy-66*s), 0, 180, fill=INK+(255,), width=3)

def zzz(im, x, y, s=1.0):
    d = ImageDraw.Draw(im)
    for k, sz in enumerate((40, 56, 74)):
        d.text((x + k*44*s, y - k*60*s), "z", font=font(int(sz*s)), fill=CREAM+(255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))

def veilleuse(im, cx, cy, s=1.0):
    """Femme assise de profil a une table, eclairee par une bougie (inspiree des veilleuses du XVIIe)."""
    d = ImageDraw.Draw(im)
    d.rectangle((cx+40*s, cy+210*s, cx+420*s, cy+240*s), fill=(70, 46, 28, 255), outline=INK+(255,), width=4)
    d.rectangle((cx+70*s, cy+240*s, cx+95*s, cy+520*s), fill=(56, 36, 22, 255)); d.rectangle((cx+370*s, cy+240*s, cx+395*s, cy+520*s), fill=(56, 36, 22, 255))
    d.polygon([(cx-230*s, cy+520*s), (cx-170*s, cy+120*s), (cx+40*s, cy+120*s), (cx+90*s, cy+520*s)], fill=(150, 36, 40, 255), outline=INK+(255,))
    hatch(d, (cx-230*s, cy+120*s, cx+90*s, cy+520*s), 14, 0.25, (20, 4, 6, 100), 3)
    d.polygon([(cx-150*s, cy+130*s), (cx+30*s, cy+130*s), (cx+40*s, cy-20*s), (cx-120*s, cy-30*s)], fill=(228, 220, 200, 255), outline=INK+(255,))
    d.line((cx+20*s, cy+40*s, cx+160*s, cy+190*s), fill=(228, 200, 165, 255), width=int(34*s))
    d.ellipse((cx-110*s, cy-200*s, cx+30*s, cy-50*s), fill=(228, 200, 165, 255), outline=INK+(255,), width=3)
    d.chord((cx-130*s, cy-215*s, cx+10*s, cy-60*s), 100, 290, fill=(40, 24, 16, 255), outline=INK+(255,))
    d.line((cx-125*s, cy-90*s, cx-150*s, cy+120*s), fill=(40, 24, 16, 255), width=int(40*s))
    d.ellipse((cx+2*s, cy-140*s, cx+14*s, cy-128*s), fill=INK+(255,))
    candle(im, int(cx+300*s), int(cy+40*s), 0.9*s, False)

def lamppost(im, x, base, s=1.0, lit=True):
    d = ImageDraw.Draw(im)
    d.rectangle((x-10*s, base-520*s, x+10*s, base), fill=(18, 14, 12, 255))
    d.polygon([(x-40*s, base-600*s), (x+40*s, base-600*s), (x+30*s, base-520*s), (x-30*s, base-520*s)], fill=(250, 220, 140, 255) if lit else (40, 36, 30, 255), outline=INK+(255,))
    if lit: glow(im, (x, base-560*s), 170*s, (255, 210, 120), 0.55)

def timeline(im, cx, cy, active=0, s=1.0):
    d = ImageDraw.Draw(im)
    lab = [("1er SOMME", (40, 52, 96)), ("VEILLE", (150, 100, 40)), ("2nd SOMMEIL", (40, 52, 96))]
    wd = [300, 180, 300]; x = cx - sum(wd)*s/2
    for k, (t, c) in enumerate(lab):
        col = c if (active == -1 or k == active) else tuple(int(v*0.45) for v in c)
        d.rectangle((x, cy-55*s, x + wd[k]*s - 8, cy+55*s), fill=col+(255,), outline=INK+(255,), width=4)
        f = font(int(34*s)); tw = f.getlength(t)
        d.text((x + wd[k]*s/2 - tw/2, cy-22*s), t, font=f, fill=CREAM+(255,), stroke_width=3, stroke_fill=(0, 0, 0, 255))
        x += wd[k]*s

def hearth(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-260*s, base-420*s, cx+260*s, base), fill=(70, 60, 56, 255), outline=INK+(255,), width=5)
    d.rectangle((cx-180*s, base-300*s, cx+180*s, base), fill=(14, 8, 6, 255))
    d.rectangle((cx-300*s, base-460*s, cx+300*s, base-420*s), fill=(90, 66, 44, 255), outline=INK+(255,), width=4)
    for k in range(3): d.line((cx-120*s+k*40*s, base-20*s, cx+80*s+k*20*s, base-50*s), fill=(60, 36, 20, 255), width=int(22*s))
    glow(im, (cx, base-120*s), 260*s, (255, 140, 40), 0.5)

def praying(im, x, y, s=1.0):
    d = ImageDraw.Draw(im); col = (12, 8, 6, 255)
    d.ellipse((x-26*s, y-210*s, x+26*s, y-158*s), fill=col)
    d.polygon([(x-60*s, y), (x-34*s, y-156*s), (x+34*s, y-156*s), (x+70*s, y)], fill=col)
    d.polygon([(x+30*s, y-140*s), (x+70*s, y-190*s), (x+80*s, y-180*s), (x+40*s, y-120*s)], fill=col)

# Dessins propres a la video 015 (danse de 1518, Strasbourg). Reutilise gen008 (qui reutilise gen010).
exec(open(f"{HERE}/gen008.py", encoding="utf-8").read())

SKIN = (226, 190, 150)
def _dk(c, k=24): return tuple(max(0, v - k) for v in c)

def dancer(im, cx, base, s=1.0, dress=(120, 36, 48), hair=(48, 30, 22), male=False, up=(1.0, 0.7), cap=False):
    d = ImageDraw.Draw(im)
    if male:
        d.polygon([(cx-52*s, base-250*s), (cx+52*s, base-250*s), (cx+62*s, base-150*s), (cx-62*s, base-150*s)], fill=dress+(255,), outline=INK+(255,))
        for sx in (-1, 1):
            d.line((cx+sx*26*s, base-150*s, cx+sx*42*s, base-16*s), fill=(44, 32, 26, 255), width=int(28*s))
            d.ellipse((cx+sx*42*s-24*s, base-26*s, cx+sx*42*s+34*s, base+6*s), fill=(20, 14, 10, 255))
    else:
        d.polygon([(cx-34*s, base-250*s), (cx+34*s, base-250*s), (cx+135*s, base), (cx-135*s, base)], fill=dress+(255,), outline=INK+(255,))
        hatch(d, (cx-125*s, base-240*s, cx+125*s, base), 12, 0.25, (20, 6, 8, 90), 3)
    d.polygon([(cx-46*s, base-352*s), (cx+46*s, base-352*s), (cx+40*s, base-238*s), (cx-40*s, base-238*s)], fill=_dk(dress)+(255,), outline=INK+(255,))
    for sx, a in ((-1, up[0]), (1, up[1])):
        x0, y0 = cx+sx*44*s, base-336*s
        x1, y1 = cx+sx*(100+30*a)*s, y0-(40+120*a)*s
        d.line((x0, y0, x1, y1), fill=SKIN+(255,), width=int(17*s)); d.ellipse((x1-15*s, y1-15*s, x1+15*s, y1+15*s), fill=SKIN+(255,), outline=INK+(255,), width=2)
    hy = base-392*s
    d.ellipse((cx-37*s, hy-40*s, cx+37*s, hy+42*s), fill=SKIN+(255,), outline=INK+(255,), width=3)
    if cap: d.pieslice((cx-42*s, hy-52*s, cx+42*s, hy+30*s), 180, 360, fill=hair+(255,), outline=INK+(255,), width=3)
    else: d.pieslice((cx-40*s, hy-48*s, cx+40*s, hy+24*s), 180, 360, fill=hair+(255,), outline=INK+(255,), width=3)
    for sx in (-1, 1):
        d.ellipse((cx+sx*15*s-8*s, hy-8*s, cx+sx*15*s+8*s, hy+8*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=2)
        d.ellipse((cx+sx*15*s-3*s, hy-3*s, cx+sx*15*s+3*s, hy+4*s), fill=INK+(255,))
    d.ellipse((cx-9*s, hy+16*s, cx+9*s, hy+30*s), fill=(60, 16, 18, 255), outline=INK+(255,), width=2)

def musician(im, cx, base, s=1.0, kind="fiddle", col=(70, 52, 38)):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-52*s, base-340*s), (cx+52*s, base-340*s), (cx+66*s, base-130*s), (cx-66*s, base-130*s)], fill=col+(255,), outline=INK+(255,))
    hatch(d, (cx-60*s, base-330*s, cx+60*s, base-130*s), 12, 0.3, (20, 10, 6, 90), 3)
    for sx in (-1, 1):
        d.line((cx+sx*28*s, base-130*s, cx+sx*34*s, base-12*s), fill=(36, 28, 24, 255), width=int(28*s))
        d.ellipse((cx+sx*34*s-22*s, base-24*s, cx+sx*34*s+34*s, base+6*s), fill=(18, 12, 8, 255))
    hy = base-396*s
    d.ellipse((cx-36*s, hy-40*s, cx+36*s, hy+42*s), fill=SKIN+(255,), outline=INK+(255,), width=3)
    d.polygon([(cx-44*s, hy-14*s), (cx-30*s, hy-62*s), (cx+30*s, hy-62*s), (cx+44*s, hy-14*s)], fill=(36, 60, 90, 255), outline=INK+(255,), width=3)
    for sx in (-1, 1):
        d.line((cx+sx*15*s-9*s, hy-2*s, cx+sx*15*s+9*s, hy-2*s), fill=INK+(255,), width=int(4*s))
    d.line((cx-10*s, hy+22*s, cx+10*s, hy+22*s), fill=INK+(255,), width=int(4*s))
    if kind == "fiddle":
        d.ellipse((cx-84*s, base-346*s, cx-12*s, base-292*s), fill=(160, 88, 34, 255), outline=INK+(255,), width=3)
        d.ellipse((cx-74*s, base-306*s, cx+2*s, base-244*s), fill=(160, 88, 34, 255), outline=INK+(255,), width=3)
        d.line((cx-84*s, base-326*s, cx-210*s, base-380*s), fill=INK+(255,), width=int(8*s))
        d.line((cx+104*s, base-232*s, cx-160*s, base-300*s), fill=(220, 200, 150, 255), width=int(5*s))
        d.line((cx+44*s, base-326*s, cx+100*s, base-236*s), fill=col+(255,), width=int(18*s))
    elif kind == "drum":
        d.rounded_rectangle((cx-84*s, base-250*s, cx+84*s, base-140*s), radius=int(16*s), fill=(150, 100, 60, 255), outline=INK+(255,), width=4)
        d.ellipse((cx-84*s, base-268*s, cx+84*s, base-232*s), fill=(226, 206, 160, 255), outline=INK+(255,), width=3)
        d.line((cx+46*s, base-326*s, cx+80*s, base-280*s), fill=col+(255,), width=int(16*s)); d.line((cx+80*s, base-280*s, cx+104*s, base-300*s), fill=INK+(255,), width=int(6*s))
        d.line((cx-46*s, base-326*s, cx-80*s, base-280*s), fill=col+(255,), width=int(16*s)); d.line((cx-80*s, base-280*s, cx-106*s, base-300*s), fill=INK+(255,), width=int(6*s))
    else:  # cor
        d.polygon([(cx+16*s, base-352*s), (cx+210*s, base-300*s), (cx+300*s, base-250*s), (cx+300*s, base-370*s), (cx+210*s, base-340*s), (cx+16*s, base-336*s)], fill=(196, 156, 56, 255), outline=INK+(255,))
        d.line((cx+40*s, base-330*s, cx+90*s, base-300*s), fill=col+(255,), width=int(16*s))

def cathedral(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im); g = (150, 92, 84, 255); g2 = (118, 70, 66, 255)
    d.rectangle((cx-380*s, base-720*s, cx+120*s, base), fill=g, outline=INK+(255,), width=5)
    d.rectangle((cx+120*s, base-1000*s, cx+320*s, base), fill=g2, outline=INK+(255,), width=5)
    d.polygon([(cx+120*s, base-1000*s), (cx+320*s, base-1000*s), (cx+270*s, base-1150*s), (cx+170*s, base-1150*s)], fill=g, outline=INK+(255,), width=4)
    d.polygon([(cx+170*s, base-1150*s), (cx+270*s, base-1150*s), (cx+220*s, base-1500*s)], fill=g2, outline=INK+(255,), width=4)
    d.ellipse((cx-250*s, base-640*s, cx-30*s, base-420*s), fill=(60, 80, 130, 255), outline=INK+(255,), width=6)
    d.ellipse((cx-190*s, base-580*s, cx-90*s, base-480*s), fill=(190, 150, 70, 255), outline=INK+(255,), width=4)
    for sx in (-1, 0, 1):
        d.rounded_rectangle((cx-140*s+sx*140*s-50*s, base-330*s, cx-140*s+sx*140*s+50*s, base), radius=int(50*s), fill=(20, 16, 16, 255), outline=INK+(255,), width=4)
    for k in range(5): d.polygon([(cx-380*s+k*100*s, base-720*s), (cx-330*s+k*100*s, base-800*s), (cx-280*s+k*100*s, base-720*s)], fill=g, outline=INK+(255,), width=3)
    hatch(d, (cx-380*s, base-720*s, cx+320*s, base), 22, 0.1, (40, 14, 10, 70), 3)

def councilman(im, cx, base, s=1.0, robe=(42, 32, 38), beard=(120, 110, 100), book=False, point=False):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-60*s, base-360*s), (cx+60*s, base-360*s), (cx+150*s, base), (cx-150*s, base)], fill=robe+(255,), outline=INK+(255,))
    hatch(d, (cx-140*s, base-350*s, cx+140*s, base), 14, 0.3, (10, 6, 8, 100), 3)
    d.polygon([(cx-50*s, base-360*s), (cx+50*s, base-360*s), (cx, base-250*s)], fill=(236, 230, 214, 255), outline=INK+(255,))
    hy = base-430*s
    d.ellipse((cx-44*s, hy-48*s, cx+44*s, hy+50*s), fill=SKIN+(255,), outline=INK+(255,), width=3)
    d.polygon([(cx-44*s, hy+6*s), (cx-30*s, hy+84*s), (cx, hy+104*s), (cx+30*s, hy+84*s), (cx+44*s, hy+6*s), (cx+20*s, hy+30*s), (cx-20*s, hy+30*s)], fill=beard+(255,), outline=INK+(255,), width=3)
    d.rectangle((cx-52*s, hy-66*s, cx+52*s, hy-40*s), fill=robe+(255,), outline=INK+(255,), width=3)
    d.rectangle((cx-34*s, hy-92*s, cx+34*s, hy-64*s), fill=robe+(255,), outline=INK+(255,), width=3)
    for sx in (-1, 1):
        d.line((cx+sx*18*s-12*s, hy-18*s, cx+sx*18*s+12*s, hy-12*s), fill=INK+(255,), width=int(5*s))
        d.ellipse((cx+sx*18*s-8*s, hy-8*s, cx+sx*18*s+8*s, hy+8*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=2)
        d.ellipse((cx+sx*18*s-3*s, hy-4*s, cx+sx*18*s+3*s, hy+4*s), fill=INK+(255,))
    if book:
        d.rectangle((cx-90*s, base-300*s, cx+10*s, base-210*s), fill=(110, 40, 36, 255), outline=INK+(255,), width=3)
        d.rectangle((cx-80*s, base-292*s, cx, base-218*s), fill=(226, 210, 168, 255))
    if point:
        d.line((cx+50*s, base-330*s, cx+170*s, base-380*s), fill=robe+(255,), width=int(24*s)); d.line((cx+170*s, base-380*s, cx+220*s, base-392*s), fill=SKIN+(255,), width=int(10*s))

def saint(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im)
    glow(im, (cx, base-470*s), 230*s, (250, 210, 110), 0.55)
    d = ImageDraw.Draw(im)
    d.polygon([(cx-62*s, base-360*s), (cx+62*s, base-360*s), (cx+170*s, base), (cx-170*s, base)], fill=(226, 220, 200, 255), outline=INK+(255,))
    hatch(d, (cx-160*s, base-350*s, cx+160*s, base), 14, 0.3, (60, 50, 40, 90), 3)
    d.polygon([(cx-62*s, base-360*s), (cx+62*s, base-360*s), (cx+40*s, base-190*s), (cx-40*s, base-190*s)], fill=(150, 40, 40, 255), outline=INK+(255,))
    hy = base-440*s
    d.ellipse((cx-46*s, hy-52*s, cx+46*s, hy+52*s), fill=SKIN+(255,), outline=INK+(255,), width=3)
    d.polygon([(cx-46*s, hy+4*s), (cx-30*s, hy+90*s), (cx, hy+112*s), (cx+30*s, hy+90*s), (cx+46*s, hy+4*s), (cx+20*s, hy+30*s), (cx-20*s, hy+30*s)], fill=(210, 206, 196, 255), outline=INK+(255,), width=3)
    d.ellipse((cx-86*s, hy-112*s, cx+86*s, hy-12*s), outline=(230, 180, 50, 255), width=int(9*s))
    for sx in (-1, 1):
        d.line((cx+sx*19*s-12*s*sx, hy-26*s, cx+sx*19*s+12*s*sx, hy-16*s), fill=INK+(255,), width=int(6*s))
        d.ellipse((cx+sx*19*s-8*s, hy-10*s, cx+sx*19*s+8*s, hy+6*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=2)
        d.ellipse((cx+sx*19*s-3*s, hy-5*s, cx+sx*19*s+3*s, hy+3*s), fill=INK+(255,))
    d.line((cx+60*s, base-330*s, cx+150*s, base-470*s), fill=(226, 220, 200, 255), width=int(24*s))
    d.ellipse((cx+130*s, base-500*s, cx+176*s, base-450*s), fill=SKIN+(255,), outline=INK+(255,), width=2)

def chapel(im, cx, base, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-150*s, base-200*s, cx+150*s, base), fill=(126, 116, 104, 255), outline=INK+(255,), width=4)
    d.polygon([(cx-170*s, base-200*s), (cx, base-340*s), (cx+170*s, base-200*s)], fill=(96, 60, 46, 255), outline=INK+(255,), width=4)
    d.rounded_rectangle((cx-36*s, base-130*s, cx+36*s, base), radius=int(36*s), fill=(40, 28, 20, 255), outline=INK+(255,), width=3)
    d.rectangle((cx-5*s, base-420*s, cx+5*s, base-336*s), fill=(210, 190, 120, 255)); d.rectangle((cx-26*s, base-396*s, cx+26*s, base-386*s), fill=(210, 190, 120, 255))
    d.ellipse((cx-100*s, base-170*s, cx-70*s, base-120*s), fill=(250, 190, 80, 255))

def bowl(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.ellipse((cx-190*s, cy-40*s, cx+190*s, cy+60*s), fill=(90, 62, 40, 255), outline=INK+(255,), width=4)
    d.pieslice((cx-190*s, cy-100*s, cx+190*s, cy+120*s), 0, 180, fill=(120, 84, 52, 255), outline=INK+(255,), width=4)
    d.ellipse((cx-150*s, cy-30*s, cx+150*s, cy+30*s), fill=(30, 20, 14, 255))
    d.line((cx+210*s, cy-120*s, cx+90*s, cy-10*s), fill=(160, 120, 70, 255), width=int(14*s))

def street(seed, dark=0.45, lit=True, ybase=1430, warm=(52, 34, 26)):
    im = paper(seed, dark, warm); glow(im, (470, 1200), 520, (240, 190, 120), 0.14)
    houses(im, ybase, seed + 1, lit)
    d = ImageDraw.Draw(im); d.rectangle((0, ybase, W, H), fill=(40, 28, 20, 255))
    for k in range(40):
        x = (k*97 + seed*13) % W; y = ybase + 30 + (k*53) % (H - ybase - 40)
        d.line((x, y, x+90, y), fill=(60, 44, 30, 255), width=3)
    return im

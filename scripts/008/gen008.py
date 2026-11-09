# Dessins propres a la video 008 (Philibert Aspairt). Reutilise ceux de la 010 (gen010.py).
exec(open(f"{HERE}/gen010.py", encoding="utf-8").read())
STONE = (96, 90, 84)

def stairs(im, cx, cy, s=1.0, n=9):
    """Escalier qui descend vers le noir (vue de face)."""
    d = ImageDraw.Draw(im)
    d.rectangle((cx-380*s, cy-520*s, cx+380*s, cy+520*s), fill=(18, 14, 14, 255), outline=INK+(255,), width=5)
    for k in range(n):
        w = (330 - k*34)*s; top = cy - 260*s + k*58*s; hh = 56*s
        shade = max(8, 120 - k*13)
        d.rectangle((cx-w, top, cx+w, top+hh), fill=(shade, shade-6, shade-12, 255), outline=INK+(255,), width=3)
        d.rectangle((cx-w, top+hh*0.55, cx+w, top+hh), fill=(max(4, shade-40), max(4, shade-44), max(4, shade-48), 255))
    d.rectangle((cx-380*s, cy-520*s, cx-330*s, cy+520*s), fill=STONE+(255,)); d.rectangle((cx+330*s, cy-520*s, cx+380*s, cy+520*s), fill=STONE+(255,))
    hatch(d, (cx-380*s, cy-520*s, cx-330*s, cy+520*s), 12, 0.0, (20, 18, 16, 120), 3); hatch(d, (cx+330*s, cy-520*s, cx+380*s, cy+520*s), 12, 0.0, (20, 18, 16, 120), 3)

def portier(im, cx, cy, s=1.0, mood=1, with_candle=True, keys=True):
    d = ImageDraw.Draw(im)
    # corps : veste brune, jabot clair
    d.polygon([(cx-210*s, cy+520*s), (cx-120*s, cy+160*s), (cx+120*s, cy+160*s), (cx+210*s, cy+520*s)], fill=(76, 56, 40, 255), outline=INK+(255,))
    hatch(d, (cx-210*s, cy+160*s, cx+210*s, cy+520*s), 14, 0.2, (20, 10, 4, 110), 3)
    d.polygon([(cx-70*s, cy+140*s), (cx+70*s, cy+140*s), (cx, cy+260*s)], fill=(226, 218, 196, 255), outline=INK+(255,))
    for k in range(4): d.ellipse((cx-8*s, cy+270*s+k*55*s, cx+8*s, cy+286*s+k*55*s), fill=GOLD+(255,))
    if keys: keyring(im, cx+150*s, cy+420*s, 0.55*s)
    d = ImageDraw.Draw(im)
    # cheveux et bonnet
    d.ellipse((cx-100*s, cy-130*s, cx+100*s, cy-10*s), fill=(52, 38, 30, 255), outline=INK+(255,), width=3)
    d.ellipse((cx-90*s, cy-100*s, cx+90*s, cy+130*s), fill=(214, 172, 138, 255), outline=INK+(255,), width=4)
    d.polygon([(cx-98*s, cy-60*s), (cx-70*s, cy-170*s), (cx+70*s, cy-170*s), (cx+98*s, cy-60*s), (cx+80*s, cy-50*s), (cx-80*s, cy-50*s)], fill=(46, 36, 30, 255), outline=INK+(255,), width=3)
    hatch(d, (cx-80*s, cy-40*s, cx-30*s, cy+110*s), 12, 0.5, (60, 30, 15, 40), 2)
    ey = cy+0*s
    for sx in (-1, 1):
        d.line((cx+sx*38*s-20*s*sx, ey-30*s-mood*6, cx+sx*38*s+20*s*sx, ey-22*s+mood*4), fill=INK+(255,), width=int(6*s))
        d.ellipse((cx+sx*38*s-15*s, ey-10*s, cx+sx*38*s+15*s, ey+12*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=3)
        d.ellipse((cx+sx*38*s-6*s, ey-5*s, cx+sx*38*s+6*s, ey+9*s), fill=INK+(255,))
    d.line((cx, ey+8*s, cx-8*s, cy+50*s), fill=INK+(255,), width=int(5*s)); d.line((cx-8*s, cy+50*s, cx+10*s, cy+52*s), fill=INK+(255,), width=int(5*s))
    d.polygon([(cx-44*s, cy+66*s), (cx, cy+58*s), (cx+44*s, cy+66*s), (cx+30*s, cy+80*s), (cx-30*s, cy+80*s)], fill=(60, 44, 34, 255))
    d.arc((cx-26*s, cy+88*s, cx+26*s, cy+112*s), 200, 340, fill=(110, 50, 50, 255), width=int(4*s))
    if with_candle:
        d.line((cx+160*s, cy+260*s, cx+250*s, cy+170*s), fill=(76, 56, 40, 255), width=int(34*s))
        d.rectangle((cx+232*s, cy+110*s, cx+268*s, cy+240*s), fill=(226, 212, 172, 255), outline=INK+(255,), width=3)

def keyring(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.ellipse((cx-60*s, cy-60*s, cx+60*s, cy+60*s), outline=(150, 150, 156, 255), width=int(10*s))
    for k, ang in enumerate((200, 235, 270, 305, 340, 20)):
        a = math.radians(ang); L = (190 + 30*(k % 3))*s
        x1, y1 = cx + 60*s*math.cos(a), cy + 60*s*math.sin(a) + 40*s; x2, y2 = cx + L*math.cos(a), cy + L*math.sin(a)*0.9 + 140*s
        d.line((x1, y1, x2, y2), fill=(120, 120, 126, 255), width=int(14*s))
        d.ellipse((x1-22*s, y1-22*s, x1+22*s, y1+22*s), outline=(150, 150, 156, 255), width=int(8*s))
        d.rectangle((x2-18*s, y2-8*s, x2+18*s, y2+24*s), fill=(110, 110, 116, 255))

def skull(d, x, y, r, tone=0):
    c = (214 - tone, 204 - tone, 178 - tone, 255)
    d.ellipse((x-r, y-r, x+r, y+r*0.9), fill=c, outline=INK+(255,), width=2)
    d.rectangle((x-r*0.55, y+r*0.5, x+r*0.55, y+r*1.05), fill=c, outline=INK+(255,), width=2)
    for sx in (-1, 1): d.ellipse((x+sx*r*0.42-r*0.26, y-r*0.2, x+sx*r*0.42+r*0.26, y+r*0.32), fill=(14, 10, 8, 255))
    d.polygon([(x-r*0.1, y+r*0.36), (x+r*0.1, y+r*0.36), (x, y+r*0.2)], fill=(14, 10, 8, 255))

def ossuary(im, y0, y1, seed=1, r=36):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    d.rectangle((0, y0, W, y1), fill=(40, 34, 30, 255))
    row = 0; y = y0 + r
    while y < y1:
        x = (r if row % 2 == 0 else 2*r)
        while x < W:
            if row % 3 == 2:
                d.line((x-r, y, x+r, y+rnd.randint(-6, 6)), fill=(206, 196, 170, 255), width=int(r*0.5))
            else: skull(d, x, y, r*0.95, rnd.randint(0, 36))
            x += 2*r + 4
        y += int(r*1.55); row += 1

def corridor(im, cx, cy, s=1.0, depth=8, lit=0.0):
    d = ImageDraw.Draw(im)
    for k in range(depth):
        w = max(24, 330 - k*30)*s; top = cy - max(40, 430 - k*38)*s; bot = cy + max(30, 330 - k*28)*s
        shade = max(6, 78 - k*9 + int(40*lit))
        d.rounded_rectangle((cx-w, top, cx+w, bot), radius=int(w*0.55), fill=(shade, shade-4, shade-8, 255), outline=(10, 8, 8, 255), width=3)
    d.rectangle((cx-40*s, cy-60*s, cx+40*s, cy+40*s), fill=(0, 0, 0, 255))

def fork(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((0, cy-420*s, W, cy+420*s), fill=(44, 38, 34, 255))
    hatch(d, (0, cy-420*s, W, cy+420*s), 22, 0.1, (20, 16, 14, 100), 3)
    for sx in (-1, 1):
        x = cx + sx*250*s
        d.rounded_rectangle((x-170*s, cy-300*s, x+170*s, cy+360*s), radius=int(170*s), fill=(8, 6, 6, 255), outline=(10, 8, 8, 255), width=4)
        d.rounded_rectangle((x-110*s, cy-200*s, x+110*s, cy+360*s), radius=int(110*s), fill=(0, 0, 0, 255))

def tombstone(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx-230*s, cy-340*s, cx+230*s, cy+340*s), radius=int(230*s), fill=(116, 110, 100, 255), outline=INK+(255,), width=5)
    hatch(d, (cx-230*s, cy-340*s, cx+230*s, cy+340*s), 14, 0.5, (30, 28, 24, 90), 3)
    d.rectangle((cx-290*s, cy+340*s, cx+290*s, cy+390*s), fill=(90, 84, 78, 255), outline=INK+(255,), width=4)
    f1, f2 = font(int(44*s)), font(int(36*s))
    for txt, yy, f in (("PERDU DANS", cy-160*s, f2), ("CETTE CARRIÈRE", cy-110*s, f2), ("PHILIBERT", cy+10*s, f1), ("ASPAIRT", cy+66*s, f1), ("1793 – 1804", cy+190*s, f2)):
        d.text((cx - f.getlength(txt)/2, yy), txt, font=f, fill=(30, 26, 22, 255))
    d.line((cx, cy-300*s, cx, cy-230*s), fill=(30, 26, 22, 255), width=int(10*s)); d.line((cx-34*s, cy-272*s, cx+34*s, cy-272*s), fill=(30, 26, 22, 255), width=int(10*s))

def worker(im, x, y, s=1.0, lamp=True):
    figure(im, x, y, s, col=(10, 8, 7), hat=True)
    if lamp:
        d = ImageDraw.Draw(im)
        d.line((x+26*s, y-170*s, x+90*s, y-120*s), fill=(10, 8, 7, 255), width=int(14*s))
        d.rectangle((x+76*s, y-130*s, x+112*s, y-80*s), fill=(60, 50, 40, 255), outline=INK+(255,), width=2)

def calendar_sheet2(im, cx, cy, w, h, ang, head, day):
    t = Image.new("RGBA", (w+40, h+40), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((20, 20, w+20, h+20), fill=(226, 210, 168, 255), outline=INK+(255,), width=4)
    d.rectangle((20, 20, w+20, 150), fill=(160, 30, 30, 255), outline=INK+(255,), width=4)
    d.text((w//2+20 - font(62).getlength(head)/2, 48), head, font=font(62), fill=(238, 224, 196, 255))
    fb = font(420); d.text((w//2+20 - fb.getlength(day)/2, 190), day, font=fb, fill=(40, 24, 14, 255))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(t, (int(cx-t.width/2), int(cy-t.height/2)))

def quarry_map(im, cx, cy, s=1.0, seed=3):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    d.rectangle((cx-420*s, cy-520*s, cx+420*s, cy+520*s), fill=(214, 196, 150, 255), outline=INK+(255,), width=5)
    pts = [(cx, cy-420*s)]
    def branch(x, y, ang, n):
        if n == 0: return
        L = rnd.randint(70, 130)*s
        x2, y2 = x + L*math.cos(ang), y + L*math.sin(ang)
        d.line((x, y, x2, y2), fill=(50, 34, 22, 255), width=int(10*s))
        if x2 < cx-400*s or x2 > cx+400*s or y2 > cy+500*s or y2 < cy-500*s: return
        branch(x2, y2, ang + rnd.uniform(-0.5, 0.5), n-1)
        if rnd.random() < 0.55: branch(x2, y2, ang + rnd.choice((-1, 1))*rnd.uniform(0.7, 1.4), n-1)
    branch(cx, cy-430*s, math.pi/2, 7)
    for k in range(4): branch(cx, cy-430*s + k*100*s, math.pi/2 + rnd.choice((-1.2, 1.2)), 5)
    d.ellipse((cx-18*s, cy-448*s, cx+18*s, cy-412*s), fill=RED+(255,), outline=INK+(255,), width=2)

# Dessins propres a la video 013 (Marie-Antoinette). A executer apres les fonctions de gen_images.py.
def poly_hatch(im, pts, step=12, ang=0.2, col=(0, 0, 0, 100), w=3):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); hatch(ImageDraw.Draw(L), (min(xs), min(ys), max(xs), max(ys)), step, ang, col, w)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(pts, fill=255)
    L.putalpha(ImageChops.multiply(L.getchannel("A"), m)); im.alpha_composite(L)
FI = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
WHITEHAIR = (226, 222, 212)

def queen(im, cx, cy, s=1.0, hair=WHITEHAIR, dress=(24, 20, 26), bonnet=True, mood=1, eyes_closed=False):
    """Marie-Antoinette en veuve : robe sombre, fichu blanc, cheveux blanchis, bonnet."""
    d = ImageDraw.Draw(im)
    d.polygon([(cx-250*s, cy+560*s), (cx-105*s, cy+170*s), (cx+105*s, cy+170*s), (cx+250*s, cy+560*s)], fill=dress+(255,), outline=INK+(255,))
    poly_hatch(im, [(cx-250*s, cy+560*s), (cx-105*s, cy+170*s), (cx+105*s, cy+170*s), (cx+250*s, cy+560*s)], 13, 0.2, (0, 0, 0, 110), 3); d = ImageDraw.Draw(im)
    # fichu blanc croise
    d.polygon([(cx-150*s, cy+150*s), (cx+150*s, cy+150*s), (cx+40*s, cy+330*s), (cx-40*s, cy+330*s)], fill=(236, 230, 214, 255), outline=INK+(255,))
    d.line((cx-150*s, cy+150*s, cx+40*s, cy+330*s), fill=(150, 140, 120, 255), width=3)
    # cheveux (pouf) blanchis
    for k in range(3):
        d.ellipse((cx-128*s+k*12*s, cy-200*s+k*22*s, cx+128*s-k*12*s, cy+60*s), fill=tuple(max(0, c - k*14) for c in hair)+(255,), outline=INK+(255,), width=3)
    for sx in (-1, 1):
        d.ellipse((cx+sx*96*s-32*s, cy+5*s, cx+sx*96*s+32*s, cy+150*s), fill=hair+(255,), outline=INK+(255,), width=3)
    if bonnet:
        for k in range(9):
            a = math.radians(200 + k*17.5)
            bx, by = cx + 150*s*math.cos(a), cy - 90*s + 110*s*math.sin(a)
            d.ellipse((bx-34*s, by-26*s, bx+34*s, by+26*s), fill=(244, 240, 230, 255), outline=(120, 110, 100, 255), width=2)
        d.ellipse((cx-120*s, cy-215*s, cx+120*s, cy-60*s), fill=(246, 242, 234, 255), outline=(120, 110, 100, 255), width=3)
    # visage pale
    d.ellipse((cx-92*s, cy-100*s, cx+92*s, cy+118*s), fill=(236, 214, 190, 255), outline=INK+(255,), width=4)
    hatch(d, (cx-80*s, cy-60*s, cx-30*s, cy+90*s), 12, 0.5, (60, 30, 15, 35), 2)
    ey = cy-5*s
    for sx in (-1, 1):
        # sourcils tristes (interieur releve)
        d.line((cx+sx*40*s-20*s*sx, ey-30*s - mood*6, cx+sx*40*s+20*s*sx, ey-22*s + mood*4), fill=INK+(255,), width=int(5*s))
        if eyes_closed:
            d.arc((cx+sx*40*s-14*s, ey-8*s, cx+sx*40*s+14*s, ey+10*s), 0, 180, fill=INK+(255,), width=int(4*s))
        else:
            d.ellipse((cx+sx*40*s-13*s, ey-8*s, cx+sx*40*s+13*s, ey+8*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=3)
            d.ellipse((cx+sx*40*s-5*s, ey-4*s, cx+sx*40*s+5*s, ey+6*s), fill=INK+(255,))
        d.arc((cx+sx*40*s-16*s, ey+8*s, cx+sx*40*s+16*s, ey+22*s), 20, 160, fill=(120, 80, 70, 255), width=2)  # cernes
    d.line((cx, ey, cx-8*s, cy+42*s), fill=INK+(255,), width=int(4*s)); d.line((cx-8*s, cy+42*s, cx+10*s, cy+44*s), fill=INK+(255,), width=int(4*s))
    d.arc((cx-24*s, cy+72*s, cx+24*s, cy+96*s), 200, 340, fill=(130, 50, 50, 255), width=int(4*s))

def guillotine(im, cx, base_y, s=1.0, blade=True, blade_off=0.0, col=(30, 20, 14)):
    d = ImageDraw.Draw(im)
    # estrade + marches
    d.rectangle((cx-300*s, base_y-60*s, cx+300*s, base_y), fill=(46, 30, 20, 255), outline=INK+(255,), width=4)
    hatch(d, (cx-300*s, base_y-60*s, cx+300*s, base_y), 12, 0.0, (10, 5, 2, 120), 3)
    for k in range(4):
        d.rectangle((cx-420*s+k*30*s, base_y-15*s*(k+1), cx-300*s, base_y-15*s*k), fill=(40, 26, 18, 255), outline=INK+(255,), width=2)
    # montants
    for sx in (-1, 1):
        d.rectangle((cx+sx*70*s-16*s, base_y-620*s, cx+sx*70*s+16*s, base_y-60*s), fill=col+(255,), outline=INK+(255,), width=3)
    d.rectangle((cx-110*s, base_y-650*s, cx+110*s, base_y-610*s), fill=col+(255,), outline=INK+(255,), width=3)
    # lunette
    d.rectangle((cx-54*s, base_y-200*s, cx+54*s, base_y-150*s), fill=(52, 36, 24, 255), outline=INK+(255,), width=3)
    d.ellipse((cx-20*s, base_y-196*s, cx+20*s, base_y-156*s), fill=(10, 6, 4, 255))
    # banc
    d.rectangle((cx+40*s, base_y-160*s, cx+280*s, base_y-130*s), fill=(52, 36, 24, 255), outline=INK+(255,), width=3)
    if blade:
        by = base_y - 600*s + blade_off*390*s
        d.polygon([(cx-54*s, by), (cx+54*s, by), (cx+54*s, by+90*s), (cx-54*s, by+40*s)], fill=(150, 150, 156, 255), outline=INK+(255,))
        d.rectangle((cx-54*s, by-34*s, cx+54*s, by), fill=(60, 44, 30, 255), outline=INK+(255,), width=2)

def blade_only(im, cx, by, s=1.0):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-54*s, by), (cx+54*s, by), (cx+54*s, by+90*s), (cx-54*s, by+40*s)], fill=(150, 150, 156, 255), outline=INK+(255,))
    d.rectangle((cx-54*s, by-34*s, cx+54*s, by), fill=(60, 44, 30, 255), outline=INK+(255,), width=2)

def cell_bg(seed=30, dark=0.35):
    im = paper(seed, dark, (58, 50, 44)); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for row in range(0, H, 90):
        off = 0 if (row//90) % 2 == 0 else 80
        for x in range(-off, W, 160):
            d.rectangle((x+4, row+4, x+156, row+86), outline=(26, 20, 16, 160), width=3)
    # fenetre a barreaux + clair de lune
    glow(im, (760, 560), 230, (170, 190, 230), 0.45)
    d.rectangle((660, 440, 860, 680), fill=(30, 36, 52, 255), outline=INK+(255,), width=6)
    for x in range(690, 860, 40): d.rectangle((x-5, 440, x+5, 680), fill=(16, 12, 10, 255))
    return im

def cart(im, cx, y, s=1.0, with_queen=True):
    d = ImageDraw.Draw(im)
    if with_queen:
        figure(im, cx-10*s, y-90*s, 1.0*s, col=(236, 230, 214))  # robe blanche du dernier jour
        d.ellipse((cx-40*s, y-370*s, cx+20*s, y-310*s), fill=WHITEHAIR+(255,), outline=INK+(255,), width=2)
    d.polygon([(cx-190*s, y-140*s), (cx+190*s, y-140*s), (cx+170*s, y), (cx-170*s, y)], fill=(70, 46, 26, 255), outline=INK+(255,))
    hatch(d, (cx-190*s, y-140*s, cx+190*s, y), 18, 0.0, (20, 10, 5, 140), 4)
    r = 95*s; wx, wy = cx-40*s, y+40*s
    d.ellipse((wx-r, wy-r, wx+r, wy+r), outline=(30, 20, 12, 255), width=int(12*s))
    for k in range(8):
        a = k*math.pi/4; d.line((wx, wy, wx+r*math.cos(a), wy+r*math.sin(a)), fill=(30, 20, 12, 255), width=int(7*s))
    # cheval
    hx = cx+330*s
    d.ellipse((hx-120*s, y-170*s, hx+120*s, y-60*s), fill=(18, 12, 9, 255))
    d.polygon([(hx+80*s, y-150*s), (hx+150*s, y-280*s), (hx+200*s, y-260*s), (hx+130*s, y-120*s)], fill=(18, 12, 9, 255))
    d.ellipse((hx+150*s, y-300*s, hx+230*s, y-250*s), fill=(18, 12, 9, 255))
    for lx in (-90, -50, 60, 100): d.rectangle((hx+lx*s, y-80*s, hx+lx*s+16*s, y+40*s), fill=(18, 12, 9, 255))
    d.line((cx+190*s, y-110*s, hx-110*s, y-120*s), fill=(18, 12, 9, 255), width=int(8*s))

def scissors(im, cx, cy, s=1.0, open_=0.0):
    t = Image.new("RGBA", (int(760*s), int(760*s)), (0, 0, 0, 0)); d = ImageDraw.Draw(t); c = 380*s
    for sgn in (-1, 1):
        a = math.radians(sgn*(5 + 15*open_))
        ux, uy = math.sin(a), -math.cos(a)          # vers la pointe
        px, py = math.cos(a), math.sin(a)            # perpendiculaire
        tip = (c + 320*s*ux, c + 320*s*uy)
        ring = (c - 170*s*ux - sgn*30*s*px, c - 170*s*uy - sgn*30*s*py)
        d.polygon([tip, (c + 26*s*px, c + 26*s*py), (c - 26*s*px, c - 26*s*py)], fill=(178, 178, 186, 255), outline=INK+(255,))
        d.line((c, c, ring[0], ring[1]), fill=(40, 40, 46, 255), width=int(18*s))
        d.ellipse((ring[0]-52*s, ring[1]-52*s, ring[0]+52*s, ring[1]+52*s), outline=(40, 40, 46, 255), width=int(16*s))
    d.ellipse((c-13*s, c-13*s, c+13*s, c+13*s), fill=INK+(255,))
    im.alpha_composite(t, (int(cx - t.width/2), int(cy - t.height/2)))

def lock(im, x, y, s=1.0, ang=0):
    d = ImageDraw.Draw(im)
    pts = [(x + 14*s*math.sin(k*0.7 + ang), y + k*14*s) for k in range(14)]
    d.line(pts, fill=WHITEHAIR+(255,), width=int(12*s)); d.line(pts, fill=(150, 146, 136, 255), width=int(3*s))

def hands_tied(im, cx, cy, s=1.0):
    """Vue de dos : epaules en robe blanche, avant-bras qui descendent et se croisent, poignets lies."""
    d = ImageDraw.Draw(im)
    d.polygon([(cx-300*s, cy-420*s), (cx+300*s, cy-420*s), (cx+220*s, cy+40*s), (cx-220*s, cy+40*s)], fill=(236, 230, 214, 255), outline=INK+(255,))
    d.line((cx, cy-420*s, cx, cy+40*s), fill=(180, 170, 150, 255), width=3)
    for sx in (-1, 1):
        sh = (cx + sx*300*s, cy-380*s); el = (cx + sx*250*s, cy-60*s); wr = (cx - sx*40*s, cy+170*s)
        d.line((sh, el), fill=INK+(255,), width=int(108*s)); d.line((sh, el), fill=(236, 230, 214, 255), width=int(100*s))  # manche
        d.line((el, wr), fill=INK+(255,), width=int(70*s)); d.line((el, wr), fill=(236, 214, 190, 255), width=int(62*s))  # avant-bras
        hx, hy = wr[0] - sx*10*s, wr[1] + 70*s
        d.ellipse((hx-42*s, hy-56*s, hx+42*s, hy+50*s), fill=(236, 214, 190, 255), outline=INK+(255,), width=3)  # main pendante
        for k in range(4): d.line((hx-24*s+k*16*s, hy+30*s, hx-26*s+k*16*s, hy+86*s), fill=(236, 214, 190, 255), width=int(13*s))
        for k in range(4): d.line((hx-24*s+k*16*s, hy+30*s, hx-26*s+k*16*s, hy+86*s), fill=INK+(160,), width=2)
    for k in range(4):
        d.rounded_rectangle((cx-110*s, cy+120*s+k*22*s, cx+110*s, cy+138*s+k*22*s), radius=int(8*s), fill=(170, 140, 90, 255), outline=(70, 50, 30, 255), width=3)
    d.line((cx+90*s, cy+150*s, cx+170*s, cy+340*s), fill=(170, 140, 90, 255), width=int(14*s))

def shoe_boot(im, cx, cy, s=1.0, step=1.0):
    d = ImageDraw.Draw(im)
    # botte du bourreau
    d.rounded_rectangle((cx-40*s, cy-360*s, cx+80*s, cy-40*s), radius=int(16*s), fill=(18, 12, 9, 255), outline=(60, 44, 30, 255), width=3)
    d.rounded_rectangle((cx-150*s, cy-90*s, cx+90*s, cy), radius=int(30*s), fill=(18, 12, 9, 255), outline=(60, 44, 30, 255), width=3)
    # soulier prune de la reine (descend sur la botte)
    sy = cy - 90*s - (1 - step)*260*s
    d.polygon([(cx-300*s, sy+10*s), (cx-60*s, sy-40*s), (cx+30*s, sy-10*s), (cx+40*s, sy+30*s), (cx-300*s, sy+40*s)], fill=(80, 30, 60, 255), outline=INK+(255,))
    d.rectangle((cx-300*s, sy+30*s, cx-270*s, sy+80*s), fill=(60, 20, 44, 255))
    d.line((cx-60*s, sy-40*s, cx-90*s, sy-160*s), fill=(236, 230, 214, 255), width=int(46*s))

def brioche(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-210*s, cy+60*s), (cx-170*s, cy+180*s), (cx+170*s, cy+180*s), (cx+210*s, cy+60*s)], fill=(150, 90, 30, 255), outline=INK+(255,))
    for k in range(7):
        x = cx - 180*s + k*60*s
        d.ellipse((x-46*s, cy-30*s, x+46*s, cy+110*s), fill=(196, 128, 44, 255), outline=INK+(255,), width=3)
    d.ellipse((cx-90*s, cy-140*s, cx+90*s, cy+10*s), fill=(206, 140, 52, 255), outline=INK+(255,), width=3)
    d.ellipse((cx-56*s, cy-210*s, cx+56*s, cy-110*s), fill=(214, 150, 60, 255), outline=INK+(255,), width=3)
    glow(im, (cx-40*s, cy-120*s), 60*s, (255, 230, 160), 0.4)

def book(im, cx, cy, s=1.0, text="CONFESSIONS"):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-230*s, cy-300*s), (cx+230*s, cy-300*s), (cx+250*s, cy+300*s), (cx-210*s, cy+300*s)], fill=(90, 26, 26, 255), outline=INK+(255,))
    d.rectangle((cx-200*s, cy-260*s, cx+200*s, cy+250*s), outline=(190, 150, 60, 255), width=5)
    f = ImageFont.truetype(FS, int(46*s)); w = f.getlength(text)
    d.text((cx - w/2, cy - 120*s), text, font=f, fill=(210, 170, 70, 255))
    f2 = ImageFont.truetype(FS, int(30*s)); t2 = "J.-J. ROUSSEAU"; d.text((cx - f2.getlength(t2)/2, cy - 30*s), t2, font=f2, fill=(210, 170, 70, 255))

def quill(im, x, y, s=1.0, ang=-35):
    t = Image.new("RGBA", (int(500*s), int(500*s)), (0, 0, 0, 0)); d = ImageDraw.Draw(t); c = 250*s
    d.line((c, c+200*s, c, c-200*s), fill=(40, 30, 20, 255), width=int(6*s))
    d.polygon([(c, c+120*s), (c-60*s, c-60*s), (c-10*s, c-220*s), (c+40*s, c-80*s)], fill=(236, 230, 214, 255), outline=INK+(255,))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    # pointe en bas : on colle pour que la pointe soit en (x, y)
    im.alpha_composite(t, (int(x - t.width/2 + 120*s*math.sin(math.radians(ang))), int(y - t.height/2 - 190*s*math.cos(math.radians(ang)))))

def letter(im, cx, cy, w=560, h=700, ang=-4, n_lines=1.0, text=True):
    t = Image.new("RGBA", (w+40, h+40), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((20, 20, w+20, h+20), fill=(226, 210, 170, 255), outline=INK+(255,), width=3)
    f = ImageFont.truetype(FI, 40)
    lines = ["ce 16 8bre à 4 h ½", "du matin", "", "C'est à vous, ma Sœur,", "que j'écris pour la", "dernière fois."]
    if text:
        y = 60
        for i, L in enumerate(lines):
            if i/len(lines) > n_lines: break
            d.text((60, y), L, font=f, fill=(40, 26, 18, 255)); y += 58
    rnd = random.Random(5)
    for i in range(6):
        yy = 440 + i*42
        if yy > h - 20: break
        d.line((60, yy, 20 + w - 60 - rnd.randint(0, 120), yy), fill=(90, 66, 44, 200), width=3)
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(t, (int(cx - t.width/2), int(cy - t.height/2)))

def clock(im, cx, cy, r, minutes=0):
    d = ImageDraw.Draw(im)
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(222, 206, 166, 255), outline=INK+(255,), width=8)
    for k in range(12):
        a = k*math.pi/6; d.line((cx + 0.82*r*math.sin(a), cy - 0.82*r*math.cos(a), cx + 0.94*r*math.sin(a), cy - 0.94*r*math.cos(a)), fill=INK+(255,), width=8)

def hands(im, cx, cy, r, minutes):
    d = ImageDraw.Draw(im)
    ah = (minutes/60.0)*math.pi/6; am = (minutes % 60)/60.0*2*math.pi
    d.line((cx, cy, cx + 0.5*r*math.sin(ah), cy - 0.5*r*math.cos(ah)), fill=INK+(255,), width=16)
    d.line((cx, cy, cx + 0.78*r*math.sin(am), cy - 0.78*r*math.cos(am)), fill=RED+(255,), width=10)
    d.ellipse((cx-16, cy-16, cx+16, cy+16), fill=INK+(255,))

def plane(im, cx, cy, s=1.0, col=(238, 224, 196)):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-140*s, cy+20*s), (cx+160*s, cy-90*s), (cx-20*s, cy+60*s)], fill=col+(255,), outline=INK+(255,))
    d.polygon([(cx-20*s, cy+60*s), (cx+160*s, cy-90*s), (cx+10*s, cy+130*s)], fill=tuple(int(c*0.8) for c in col)+(255,), outline=INK+(255,))

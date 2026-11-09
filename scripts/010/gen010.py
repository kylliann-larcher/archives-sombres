# Dessins propres a la video 010 (Louis XVII). Executes apres gen_images.py et gen13.py (paper, glow, hatch, flame, candle, wig_face, figure, queen, guillotine, cell_bg...).
SKIN = (236, 208, 178)
BLOND = (214, 178, 96)
GOLD = (206, 164, 54)

def door(im, cx, cy, s=1.0, grille=True):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = cx-260*s, cy-420*s, cx+260*s, cy+420*s
    d.rectangle((x0, y0, x1, y1), fill=(58, 38, 24, 255), outline=INK+(255,), width=6)
    for k in range(1, 8):
        d.line((x0+k*65*s, y0, x0+k*65*s, y1), fill=(30, 18, 10, 255), width=4)
    hatch(d, (x0, y0, x1, y1), 14, 0.0, (12, 6, 3, 110), 3)
    for yy in (cy-250*s, cy+250*s):
        d.rectangle((x0, yy-24*s, x1, yy+24*s), fill=(34, 34, 40, 255), outline=INK+(255,), width=3)
        for xx in range(int(x0+30*s), int(x1), int(70*s)):
            d.ellipse((xx-8*s, yy-8*s, xx+8*s, yy+8*s), fill=(90, 90, 98, 255), outline=INK+(255,), width=2)
    if grille:
        d.rectangle((cx-100*s, cy-340*s, cx+100*s, cy-170*s), fill=(8, 6, 6, 255), outline=INK+(255,), width=6)
    d.rectangle((cx+150*s, cy-10*s, cx+230*s, cy+90*s), fill=(40, 40, 46, 255), outline=INK+(255,), width=4)
    d.ellipse((cx+178*s, cy+14*s, cx+202*s, cy+38*s), fill=INK+(255,)); d.rectangle((cx+186*s, cy+30*s, cx+194*s, cy+66*s), fill=INK+(255,))

def grille_bars(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    for k in range(-2, 3):
        d.rectangle((cx+k*40*s-6*s, cy-340*s, cx+k*40*s+6*s, cy-170*s), fill=(30, 30, 36, 255), outline=INK+(255,), width=2)

def prince(im, cx, cy, s=1.0, mood=1, crown=False, eyes_closed=False, body=True):
    d = ImageDraw.Draw(im)
    if body:
        d.polygon([(cx-200*s, cy+520*s), (cx-110*s, cy+150*s), (cx+110*s, cy+150*s), (cx+200*s, cy+520*s)], fill=(40, 56, 110, 255), outline=INK+(255,))
        hatch(d, (cx-200*s, cy+150*s, cx+200*s, cy+520*s), 14, 0.2, (10, 10, 30, 110), 3)
        d.polygon([(cx-120*s, cy+130*s), (cx+120*s, cy+130*s), (cx+60*s, cy+210*s), (cx, cy+170*s), (cx-60*s, cy+210*s)], fill=(238, 232, 214, 255), outline=INK+(255,))
        for k in range(4): d.ellipse((cx-8*s, cy+240*s+k*60*s, cx+8*s, cy+256*s+k*60*s), fill=GOLD+(255,))
    # boucles blondes
    for k in range(-4, 5):
        d.ellipse((cx+k*28*s-42*s, cy-150*s+abs(k)*10*s, cx+k*28*s+42*s, cy-30*s+abs(k)*10*s), fill=BLOND+(255,), outline=INK+(255,), width=3)
    for sx in (-1, 1):
        for r in range(3):
            d.ellipse((cx+sx*(90+r*8)*s-34*s, cy-10*s+r*50*s, cx+sx*(90+r*8)*s+34*s, cy+60*s+r*50*s), fill=BLOND+(255,), outline=INK+(255,), width=3)
    d.ellipse((cx-88*s, cy-100*s, cx+88*s, cy+120*s), fill=SKIN+(255,), outline=INK+(255,), width=4)
    hatch(d, (cx-80*s, cy-60*s, cx-30*s, cy+100*s), 12, 0.5, (60, 30, 15, 35), 2)
    ey = cy-5*s
    for sx in (-1, 1):
        d.line((cx+sx*40*s-20*s*sx, ey-32*s-mood*6, cx+sx*40*s+20*s*sx, ey-22*s+mood*4), fill=INK+(255,), width=int(5*s))
        if eyes_closed:
            d.arc((cx+sx*40*s-15*s, ey-8*s, cx+sx*40*s+15*s, ey+10*s), 0, 180, fill=INK+(255,), width=int(4*s))
        else:
            d.ellipse((cx+sx*40*s-16*s, ey-12*s, cx+sx*40*s+16*s, ey+12*s), fill=(245, 240, 225, 255), outline=INK+(255,), width=3)
            d.ellipse((cx+sx*40*s-7*s, ey-7*s, cx+sx*40*s+7*s, ey+9*s), fill=(40, 60, 100, 255)); d.ellipse((cx+sx*40*s-3*s, ey-3*s, cx+sx*40*s+3*s, ey+3*s), fill=INK+(255,))
    d.line((cx, ey+6*s, cx-7*s, cy+42*s), fill=INK+(255,), width=int(4*s)); d.line((cx-7*s, cy+42*s, cx+9*s, cy+44*s), fill=INK+(255,), width=int(4*s))
    d.arc((cx-24*s, cy+66*s, cx+24*s, cy+92*s), 200, 340, fill=(120, 40, 40, 255), width=int(5*s))
    d.ellipse((cx-60*s, cy+30*s, cx-30*s, cy+54*s), fill=(236, 170, 150, 120)); d.ellipse((cx+30*s, cy+30*s, cx+60*s, cy+54*s), fill=(236, 170, 150, 120))
    if crown: crown_obj(im, cx, cy-190*s, s*0.9)

def crown_obj(im, cx, cy, s=1.0, ang=0):
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    pts = [(cx-110*s, cy+50*s), (cx-120*s, cy-60*s), (cx-60*s, cy-10*s), (cx, cy-100*s), (cx+60*s, cy-10*s), (cx+120*s, cy-60*s), (cx+110*s, cy+50*s)]
    d.polygon(pts, fill=GOLD+(255,), outline=INK+(255,))
    d.rectangle((cx-110*s, cy+20*s, cx+110*s, cy+62*s), fill=(176, 132, 36, 255), outline=INK+(255,), width=3)
    for dx, c in ((-60, (170, 30, 40)), (0, (40, 80, 170)), (60, (170, 30, 40))): d.ellipse((cx+dx*s-12*s, cy+30*s, cx+dx*s+12*s, cy+54*s), fill=c+(255,), outline=INK+(255,), width=2)
    for px, py in ((-120, -60), (0, -100), (120, -60)): d.ellipse((cx+px*s-12*s, cy+py*s-12*s, cx+px*s+12*s, cy+py*s+12*s), fill=(240, 232, 200, 255), outline=INK+(255,), width=2)
    if ang: t = t.rotate(ang, center=(cx, cy+40*s), resample=Image.BILINEAR)
    im.alpha_composite(t)

def kid_back(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-120*s, cy+300*s), (cx-70*s, cy+40*s), (cx+70*s, cy+40*s), (cx+120*s, cy+300*s)], fill=(26, 32, 62, 255), outline=INK+(255,))
    for k in range(-3, 4): d.ellipse((cx+k*20*s-34*s, cy-90*s, cx+k*20*s+34*s, cy+10*s), fill=BLOND+(255,), outline=INK+(255,), width=2)
    d.ellipse((cx-56*s, cy-70*s, cx+56*s, cy+50*s), fill=BLOND+(255,), outline=INK+(255,), width=3)
    d.rectangle((cx-70*s, cy+300*s, cx+70*s, cy+330*s), fill=(20, 14, 10, 255))

def jar(im, cx, cy, s=1.0, lit=True):
    d = ImageDraw.Draw(im)
    # table
    d.rectangle((cx-330*s, cy+250*s, cx+330*s, cy+290*s), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.rectangle((cx-300*s, cy+290*s, cx+300*s, cy+420*s), fill=(40, 26, 16, 255))
    if lit: glow(im, (cx, cy), 360*s, (255, 190, 100), 0.45)
    # bocal en verre
    d.rounded_rectangle((cx-130*s, cy-170*s, cx+130*s, cy+250*s), radius=int(60*s), fill=(150, 190, 200, 70), outline=(200, 225, 230, 230), width=int(6*s))
    d.rectangle((cx-90*s, cy-230*s, cx+90*s, cy-170*s), fill=(96, 62, 36, 255), outline=INK+(255,), width=4)
    # coeur desseche
    hx, hy = cx, cy+40*s
    d.ellipse((hx-82*s, hy-70*s, hx+4*s, hy+20*s), fill=(100, 36, 30, 255), outline=INK+(255,), width=3)
    d.ellipse((hx-6*s, hy-70*s, hx+82*s, hy+20*s), fill=(92, 32, 28, 255), outline=INK+(255,), width=3)
    d.polygon([(hx-80*s, hy-10*s), (hx+80*s, hy-10*s), (hx+6*s, hy+110*s), (hx-6*s, hy+110*s)], fill=(96, 34, 28, 255), outline=INK+(255,))
    hatch(d, (hx-80*s, hy-60*s, hx+80*s, hy+100*s), 10, 0.5, (30, 10, 8, 110), 2)
    d.rectangle((hx-18*s, hy-110*s, hx+18*s, hy-62*s), fill=(80, 28, 24, 255), outline=INK+(255,), width=3)
    d.line((cx-100*s, cy-120*s, cx-100*s, cy+170*s), fill=(235, 245, 248, 150), width=int(8*s))

def tower(im, cx, base_y, s=1.0, lit=()):
    d = ImageDraw.Draw(im)
    glow(im, (cx+250*s, base_y-900*s), 200*s, (170, 190, 230), 0.45)
    d.ellipse((cx+190*s, base_y-950*s, cx+310*s, base_y-830*s), fill=(236, 232, 214, 255))
    body = (22, 18, 22, 255)
    d.rectangle((cx-170*s, base_y-720*s, cx+170*s, base_y), fill=body, outline=(46, 36, 32, 255), width=4)
    for sx in (-1, 1):
        d.rectangle((cx+sx*170*s-60*s, base_y-640*s, cx+sx*170*s+60*s, base_y), fill=body, outline=(46, 36, 32, 255), width=4)
        d.polygon([(cx+sx*170*s-76*s, base_y-640*s), (cx+sx*170*s, base_y-820*s), (cx+sx*170*s+76*s, base_y-640*s)], fill=(16, 14, 18, 255), outline=(46, 36, 32, 255))
    for k in range(7): d.rectangle((cx-170*s+k*50*s, base_y-770*s, cx-170*s+k*50*s+30*s, base_y-720*s), fill=body, outline=(46, 36, 32, 255), width=3)
    ws = []
    for row in range(4):
        for col in range(3):
            wx, wy = cx-100*s+col*100*s, base_y-640*s+row*130*s
            ws.append((wx, wy))
            on = (row*3+col) in lit
            d.rectangle((wx-18*s, wy, wx+18*s, wy+64*s), fill=(250, 190, 80, 255) if on else (34, 24, 20, 255), outline=INK+(255,), width=2)
    d.rectangle((cx-40*s, base_y-110*s, cx+40*s, base_y), fill=(10, 8, 8, 255), outline=INK+(255,), width=3)
    return ws

def simon(im, x, y, s=1.0):
    d = ImageDraw.Draw(im)
    figure(im, x, y, s, col=(32, 26, 22)); d = ImageDraw.Draw(im)
    d.polygon([(x-44*s, y-10*s), (x-30*s, y-170*s), (x+30*s, y-170*s), (x+44*s, y-10*s)], fill=(124, 92, 58, 255), outline=INK+(255,), width=3)
    d.ellipse((x-34*s, y-262*s, x+34*s, y-196*s), fill=(214, 168, 134, 255), outline=INK+(255,), width=3)
    d.polygon([(x-36*s, y-250*s), (x+4*s, y-330*s), (x+40*s, y-250*s)], fill=(190, 24, 28, 255), outline=INK+(255,))
    d.line((x-22*s, y-216*s, x+22*s, y-216*s), fill=INK+(255,), width=int(6*s)); d.line((x-18*s, y-240*s, x-8*s, y-236*s), fill=INK+(255,), width=int(4*s)); d.line((x+8*s, y-236*s, x+18*s, y-240*s), fill=INK+(255,), width=int(4*s))
    # soulier dans la main
    d.line((x+30*s, y-160*s, x+110*s, y-120*s), fill=(32, 26, 22, 255), width=int(16*s))
    d.polygon([(x+90*s, y-130*s), (x+170*s, y-150*s), (x+190*s, y-110*s), (x+100*s, y-90*s)], fill=(84, 54, 32, 255), outline=INK+(255,), width=3)

def bonnet_rouge(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-90*s, cy+40*s), (cx-60*s, cy-60*s), (cx+10*s, cy-110*s), (cx+70*s, cy-40*s), (cx+90*s, cy+40*s)], fill=(190, 24, 28, 255), outline=INK+(255,), width=3)
    d.rectangle((cx-96*s, cy+30*s, cx+96*s, cy+60*s), fill=(160, 18, 22, 255), outline=INK+(255,), width=3)
    d.ellipse((cx+54*s, cy-72*s, cx+94*s, cy-34*s), fill=(236, 232, 214, 255), outline=INK+(255,), width=2)

def calendar_sheet(im, cx, cy, w=620, h=760, ang=-3):
    t = Image.new("RGBA", (w+40, h+40), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((20, 20, w+20, h+20), fill=(226, 210, 168, 255), outline=INK+(255,), width=4)
    d.rectangle((20, 20, w+20, 150), fill=(160, 30, 30, 255), outline=INK+(255,), width=4)
    d.text((w//2+20 - font(70).getlength("JUIN 1795")/2, 44), "JUIN 1795", font=font(70), fill=(238, 224, 196, 255))
    fb = font(420); d.text((w//2+20 - fb.getlength("8")/2, 190), "8", font=fb, fill=(40, 24, 14, 255))
    for k in range(6): d.line((60+k*8, h+10, 60+k*8+40, h+30), fill=INK+(255,), width=3)
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(t, (int(cx-t.width/2), int(cy-t.height/2)))

def bed(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-330*s, cy-260*s, cx-290*s, cy+160*s), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.rectangle((cx+290*s, cy-100*s, cx+330*s, cy+160*s), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.polygon([(cx-300*s, cy+10*s), (cx+300*s, cy+10*s), (cx+300*s, cy+120*s), (cx-300*s, cy+120*s)], fill=(88, 84, 78, 255), outline=INK+(255,))
    hatch(d, (cx-300*s, cy+10*s, cx+300*s, cy+120*s), 14, 0.3, (20, 18, 16, 110), 3)
    d.ellipse((cx-280*s, cy-70*s, cx-130*s, cy+30*s), fill=(214, 208, 192, 255), outline=INK+(255,), width=3)
    d.polygon([(cx-120*s, cy-10*s), (cx+280*s, cy-30*s), (cx+280*s, cy+20*s), (cx-120*s, cy+30*s)], fill=(120, 116, 108, 255), outline=INK+(255,))
    d.rectangle((cx-320*s, cy+160*s, cx+320*s, cy+190*s), fill=(40, 26, 16, 255))

def crosses(im, y_base, seed=1):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    d.rectangle((0, y_base, W, H), fill=(22, 20, 20, 255))
    d.polygon([(0, y_base), (W, y_base-40), (W, y_base+60), (0, y_base+60)], fill=(30, 26, 24, 255))
    for row in range(4):
        for k in range(7):
            x = 60 + k*150 + rnd.randint(-30, 30) + row*30; y = y_base + 80 + row*130; sc = 0.6 + row*0.18
            d.rectangle((x-8*sc, y-130*sc, x+8*sc, y), fill=(60, 52, 48, 255), outline=INK+(255,))
            d.rectangle((x-40*sc, y-100*sc, x+40*sc, y-84*sc), fill=(60, 52, 48, 255), outline=INK+(255,))
            d.ellipse((x-60*sc, y-6*sc, x+60*sc, y+24*sc), fill=(34, 28, 26, 255))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for i in range(10):
        x0 = rnd.randint(-200, 700); gd.ellipse((x0, y_base-200+rnd.randint(0, 100), x0+rnd.randint(400, 700), y_base+100+rnd.randint(0, 200)), fill=(150, 160, 175, 40))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))

def handkerchief(im, cx, cy, s=1.0, red=0.0):
    d = ImageDraw.Draw(im)
    pts = [(cx-110*s, cy-80*s), (cx+90*s, cy-100*s), (cx+120*s, cy+70*s), (cx-90*s, cy+100*s)]
    d.polygon(pts, fill=(240, 236, 224, 255), outline=INK+(255,))
    d.line((cx-110*s, cy-80*s, cx+120*s, cy+70*s), fill=(190, 184, 170, 255), width=3); d.line((cx+90*s, cy-100*s, cx-90*s, cy+100*s), fill=(190, 184, 170, 255), width=3)
    if red > 0.02: d.ellipse((cx-40*s, cy-30*s, cx+40*s, cy+30*s), fill=(170, 24, 24, int(220*red)))

def doctor(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    wig_face(im, cx, cy, s, mood=1, hair=(190, 186, 176)); d = ImageDraw.Draw(im)
    # poche du manteau
    d.polygon([(cx+70*s, cy+330*s), (cx+200*s, cy+330*s), (cx+190*s, cy+400*s), (cx+80*s, cy+400*s)], fill=(20, 26, 66, 255), outline=INK+(255,), width=3)

def helix(im, cx, cy, h=700, w=160, phase=0.0, col1=(200, 40, 40), col2=(60, 120, 210), rungs=14):
    d = ImageDraw.Draw(im); n = 70
    p1, p2 = [], []
    for i in range(n+1):
        y = cy - h/2 + h*i/n; a = phase + i/n*6*math.pi
        p1.append((cx + w*math.sin(a), y)); p2.append((cx - w*math.sin(a), y))
    for i in range(rungs):
        k = int((i+0.5)*n/rungs); d.line((p1[k][0], p1[k][1], p2[k][0], p2[k][1]), fill=(230, 220, 190, 220), width=6)
    d.line(p1, fill=col1+(255,), width=14, joint="curve"); d.line(p2, fill=col2+(255,), width=14, joint="curve")

def hair_frame(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-130*s, cy-160*s, cx+130*s, cy+160*s), fill=(150, 112, 44, 255), outline=INK+(255,), width=5)
    d.rectangle((cx-100*s, cy-130*s, cx+100*s, cy+130*s), fill=(226, 210, 168, 255), outline=INK+(255,), width=3)
    for r in range(4): d.arc((cx-60*s+r*8*s, cy-80*s+r*12*s, cx+60*s-r*8*s, cy+60*s-r*6*s), 20+r*30, 330, fill=(214, 206, 190, 255), width=int(7*s))
    d.rectangle((cx-50*s, cy+88*s, cx+50*s, cy+108*s), fill=(160, 30, 30, 255), outline=INK+(255,), width=2)

def flask(im, cx, cy, s=1.0, liquid=(80, 170, 120)):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-30*s, cy-170*s), (cx+30*s, cy-170*s), (cx+30*s, cy-60*s), (cx+130*s, cy+120*s), (cx-130*s, cy+120*s), (cx-30*s, cy-60*s)], fill=(180, 210, 220, 80), outline=(210, 230, 235, 230))
    d.polygon([(cx-84*s, cy+30*s), (cx+84*s, cy+30*s), (cx+130*s, cy+120*s), (cx-130*s, cy+120*s)], fill=liquid+(200,), outline=INK+(255,))
    d.rectangle((cx-34*s, cy-190*s, cx+34*s, cy-170*s), fill=(96, 62, 36, 255), outline=INK+(255,), width=3)

def urn(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-260*s, cy+120*s, cx+260*s, cy+200*s), fill=(150, 150, 154, 255), outline=INK+(255,), width=4)
    d.ellipse((cx-210*s, cy+60*s, cx+210*s, cy+150*s), fill=(140, 24, 40, 255), outline=INK+(255,), width=4)
    glow(im, (cx, cy-20*s), 300*s, (255, 220, 160), 0.4); d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx-130*s, cy-210*s, cx+130*s, cy+90*s), radius=int(100*s), fill=(190, 220, 230, 70), outline=(214, 234, 240, 240), width=int(6*s))
    hx, hy = cx, cy-10*s
    d.ellipse((hx-60*s, hy-50*s, hx+4*s, hy+14*s), fill=(100, 36, 30, 255), outline=INK+(255,), width=2); d.ellipse((hx-4*s, hy-50*s, hx+60*s, hy+14*s), fill=(92, 32, 28, 255), outline=INK+(255,), width=2)
    d.polygon([(hx-58*s, hy-6*s), (hx+58*s, hy-6*s), (hx+4*s, hy+80*s), (hx-4*s, hy+80*s)], fill=(96, 34, 28, 255), outline=INK+(255,))

def basilica(im, cx, base_y, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((0, base_y-1100*s, W, base_y), fill=(34, 32, 36, 255))
    # piliers et arcs gothiques
    for x in (-360, -120, 120, 360):
        d.rectangle((cx+x*s-34*s, base_y-1000*s, cx+x*s+34*s, base_y), fill=(86, 80, 82, 255), outline=INK+(255,), width=3)
        hatch(d, (cx+x*s-34*s, base_y-1000*s, cx+x*s+34*s, base_y), 12, 0.0, (20, 18, 20, 120), 3)
    for x in (-240, 0, 240):
        d.polygon([(cx+x*s-120*s, base_y-1000*s), (cx+x*s-100*s, base_y-1150*s), (cx+x*s, base_y-1280*s), (cx+x*s+100*s, base_y-1150*s), (cx+x*s+120*s, base_y-1000*s)], outline=INK+(255,), fill=(26, 24, 30, 255))
    glow(im, (cx, base_y-1000*s), 340*s, (250, 210, 150), 0.35); d = ImageDraw.Draw(im)
    d.rectangle((0, base_y-30*s, W, H), fill=(52, 48, 50, 255))
    for k in range(6): d.line((0, base_y+k*60*s, W, base_y+k*60*s), fill=(34, 30, 32, 255), width=3)
    # gisants (rois couches) de part et d'autre
    for sx in (-1, 1):
        x0 = cx + sx*360*s
        d.rounded_rectangle((x0-120*s, base_y-80*s, x0+120*s, base_y-10*s), radius=int(14*s), fill=(160, 156, 150, 255), outline=INK+(255,), width=3)
        d.ellipse((x0-96*s, base_y-130*s, x0-40*s, base_y-80*s), fill=(190, 186, 178, 255), outline=INK+(255,), width=2)
        d.rectangle((x0-30*s, base_y-116*s, x0+90*s, base_y-84*s), fill=(176, 172, 164, 255), outline=INK+(255,), width=2)
        d.polygon([(x0-98*s, base_y-130*s), (x0-90*s, base_y-160*s), (x0-70*s, base_y-140*s), (x0-50*s, base_y-160*s), (x0-42*s, base_y-130*s)], fill=GOLD+(255,), outline=INK+(255,))

def question_mark(im, cx, cy, size=700, alpha=60):
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); f = font(size)
    ImageDraw.Draw(L).text((cx - f.getlength("?")/2, cy - size*0.6), "?", font=f, fill=(238, 224, 196, alpha))
    im.alpha_composite(L)

def pointing(im, x, y, s=1.0, col=(8, 6, 5), dirx=1):
    figure(im, x, y, s, col=col)
    d = ImageDraw.Draw(im)
    d.line((x+dirx*26*s, y-170*s, x+dirx*140*s, y-200*s), fill=col+(255,), width=int(14*s))
    d.line((x+dirx*140*s, y-200*s, x+dirx*190*s, y-206*s), fill=col+(255,), width=int(6*s))

def furniture(im, seed=3):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    for k in range(5):
        t = Image.new("RGBA", (300, 200), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
        td.rectangle((10, 10, 290, 190), fill=(66, 42, 24, 255), outline=INK+(255,), width=4); hatch(td, (10, 10, 290, 190), 12, 0.3, (20, 10, 4, 120), 3)
        t = t.rotate(rnd.randint(-70, 70), expand=True, resample=Image.BILINEAR)
        im.alpha_composite(t, (rnd.randint(40, 700), rnd.randint(1050, 1450)))

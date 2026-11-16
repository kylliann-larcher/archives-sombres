"""Figures communes 025-027 (dessins originaux, rien de graphique)."""
SKIN=(208,169,128); CLOTH=(34,39,43); GOLD=(203,164,91)

def room(seed,wall=(96,70,48),floor=(64,46,32),dark=.06,warm=(100,70,40)):
    im=paper(seed,dark,warm);d=ImageDraw.Draw(im)
    d.rectangle((40,640,1040,1240),fill=wall+(255,),outline=INK+(255,),width=5)
    for x in range(120,1040,160):d.line((x,650,x,1236),fill=tuple(int(v*.88) for v in wall)+(255,),width=3)
    d.rectangle((0,1240,W,H),fill=floor+(255,))
    for k in range(-9,10):d.line((540+k*34,1240,540+k*260,H),fill=tuple(int(v*.78) for v in floor)+(255,),width=3)
    d.rectangle((0,1226,W,1246),fill=tuple(int(v*1.3) for v in floor)+(255,),outline=INK+(255,),width=4)
    return im

def person(im,x=470,y=1230,s=1,coat=CLOTH,hair=(48,34,25),back=False,mouth='flat',eyes='open',dress=False,skin=SKIN,hat=False,bald=False):
    d=ImageDraw.Draw(im);w=max(2,int(4*s))
    if dress:
        d.polygon([(x-150*s,y),(x-60*s,y-230*s),(x+60*s,y-230*s),(x+150*s,y)],fill=coat+(255,),outline=INK+(255,))
    else:
        d.polygon([(x-105*s,y),(x-85*s,y-190*s),(x-37*s,y-238*s),(x+37*s,y-238*s),(x+85*s,y-190*s),(x+105*s,y)],fill=coat+(255,),outline=INK+(255,))
    if back:
        d.ellipse((x-59*s,y-360*s,x+59*s,y-230*s),fill=hair+(255,),outline=INK+(255,),width=w);return
    if not dress:
        d.polygon([(x-37*s,y-238*s),(x,y-151*s),(x+37*s,y-238*s)],fill=(209,194,160,255),outline=INK+(255,))
    d.ellipse((x-59*s,y-360*s,x+59*s,y-230*s),fill=skin+(255,),outline=INK+(255,),width=w)
    if not bald:d.arc((x-61*s,y-363*s,x+62*s,y-245*s),170,355,fill=hair+(255,),width=max(3,int(15*s)))
    if dress and not bald:
        for sx in (-1,1):d.ellipse((x+sx*58*s-20*s,y-330*s,x+sx*58*s+20*s,y-250*s),fill=hair+(255,),outline=INK+(255,),width=2)
    if hat:
        d.rectangle((x-70*s,y-372*s,x+70*s,y-352*s),fill=(20,18,18,255));d.rectangle((x-46*s,y-450*s,x+46*s,y-366*s),fill=(20,18,18,255),outline=INK+(255,))
    if eyes=='closed':
        for sx in (-1,1):d.arc((x+sx*25*s-10*s,y-305*s,x+sx*25*s+10*s,y-288*s),20,160,fill=INK+(255,),width=max(2,int(3*s)))
    elif mouth=='wide':
        for sx in (-1,1):d.ellipse((x+sx*25*s-10*s,y-306*s,x+sx*25*s+10*s,y-286*s),fill=(250,250,240,255),outline=INK+(255,),width=2)
    else:
        for sx in (-1,1):d.ellipse((x+sx*25*s-7*s,y-303*s,x+sx*25*s+7*s,y-289*s),fill=INK+(255,))
    if mouth=='wide':d.ellipse((x-12*s,y-268*s,x+12*s,y-246*s),fill=(70,30,30,255))
    elif mouth=='smile':d.arc((x-18*s,y-268*s,x+18*s,y-246*s),20,160,fill=(96,48,41,255),width=max(2,int(3*s)))
    else:d.line((x-16*s,y-253*s,x+16*s,y-253*s),fill=(96,48,41,255),width=max(2,int(3*s)))

def hand(im,x,y,s=1,flip=1,sleeve=(80,62,46)):
    d=ImageDraw.Draw(im)
    d.polygon([(x-40*s,y+40*s),(x+40*s,y+40*s),(x+60*s*flip+40*s,y+360*s),(x+60*s*flip-60*s,y+360*s)],fill=sleeve+(255,),outline=INK+(255,))
    d.rounded_rectangle((x-46*s,y-40*s,x+46*s,y+50*s),radius=int(26*s),fill=SKIN+(255,),outline=INK+(255,),width=3)
    for k in range(4):d.line((x-34*s+k*22*s,y-40*s,x-34*s+k*22*s,y-8*s),fill=(170,130,96,255),width=3)

def table(im,y=1150,x0=100,x1=980,col=(92,66,42)):
    d=ImageDraw.Draw(im);d.rectangle((x0,y,x1,y+50),fill=col+(255,),outline=INK+(255,),width=5)
    for x in (x0+30,x1-30):d.rectangle((x-12,y+50,x+12,y+250),fill=tuple(int(v*.75) for v in col)+(255,),outline=INK+(255,),width=3)

def steam(im,t,x,y,n=5,amp=1.0,spread=520,col=(210,206,196)):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    for k in range(n):
        x0=x-spread/2+k*spread/max(1,n-1);rise=((t*55+k*50)%240)
        pts=[(x0+26*math.sin((j+t*3+k)*.9)*amp,y-rise-j*26) for j in range(9)]
        a=int(170*amp*(1-rise/260))
        if a>8:d.line(pts,fill=col+(a,),width=12,joint='curve')
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(3)))

def question_mark(im,x,y,s=1):
    d=ImageDraw.Draw(im);d.text((x,y),'?',font=font(int(260*s)),fill=(230,210,170,255),stroke_width=8,stroke_fill=INK+(255,),anchor='mm')

def door(im,x,y,u,frame=(40,30,22),leaf=(120,84,50)):
    d=ImageDraw.Draw(im)
    d.rectangle((x-110,y-420,x+110,y),fill=frame+(255,),outline=INK+(255,),width=5)
    w=int(220*(1-u));d.rectangle((x-110,y-420,x-110+w,y),fill=leaf+(255,),outline=INK+(255,),width=4)

def coins(im,x,y,n,s=1):
    d=ImageDraw.Draw(im)
    for k in range(n):
        yy=y-k*16*s;d.ellipse((x-50*s,yy-14*s,x+50*s,yy+14*s),fill=(214,176,80,255),outline=INK+(255,),width=3)

def red_cross(im,x,y,r,u):
    if u<=0:return
    d=ImageDraw.Draw(im);L=int(r*u)
    d.line((x-L,y-L,x+L,y+L),fill=RED+(255,),width=18);d.line((x+L,y-L,x-L,y+L),fill=RED+(255,),width=18)

def slam_stamp(im,text,x,y,t,t0,size=110,ang=-10):
    a=t-t0
    if a<0:return
    sc=1+1.2*max(0,1-a/.15)**2
    f=font(int(size*sc));w=int(f.getlength(text))+60;h=int(size*sc*1.5)
    L=Image.new('RGBA',(w,h));d=ImageDraw.Draw(L)
    d.rectangle((3,3,w-4,h-4),outline=RED+(255,),width=max(6,int(10*sc)));d.text((30,h//2),text,font=f,fill=RED+(255,),anchor='lm')
    L=L.rotate(ang,expand=True,resample=Image.BICUBIC);im.alpha_composite(L,(int(x-L.width/2),int(y-L.height/2)))

# ---------- Effets enrichis (v2, demande du 2026-11-16) ----------
def blinking(t, ph=0.0):
    return 'closed' if t > 0.5 and ((t + ph) % 3.1) < 0.12 else 'open'  # jamais fermés sur la première image

def brows(im, x, y, s=1, kind='flat'):
    d = ImageDraw.Draw(im); w = max(3, int(6*s))
    for sx in (-1, 1):
        cx = x + sx*25*s; o, i = cx + sx*14*s, cx - sx*8*s  # bout extérieur (côté tempe), bout intérieur (côté nez)
        if kind == 'worried': yo, yi = y - 318*s, y - 330*s
        elif kind == 'angry': yo, yi = y - 330*s, y - 316*s
        elif kind == 'up': yo, yi = y - 334*s, y - 334*s
        else: yo, yi = y - 322*s, y - 322*s
        d.line((o, yo, i, yi), fill=INK+(255,), width=w)

def actor(im, x, y, s, t, ph=0.0, kind='flat', mouth='flat', eyes=None, **kw):
    """Personnage vivant : respiration, clignement des yeux, sourcils expressifs."""
    bob = int(4*s*math.sin(t*2.4 + ph))
    person(im, x, y + bob, s, eyes=eyes or blinking(t, ph), mouth=mouth, **kw)
    if not kw.get('back'): brows(im, x, y + bob, s, kind)

def dust(frame, t, n=36, col=(255, 226, 170), seed=7):
    layer = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(layer); rnd = random.Random(seed)
    for k in range(n):
        x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(8, 26), rnd.uniform(2, 5)
        x = (x0 + 18*math.sin(t*.7 + k)) % W; y = (y0 - sp*t) % H
        a = int(70 + 60*math.sin(t*1.7 + k*1.3))
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (max(0, a),))
    return layer.filter(ImageFilter.GaussianBlur(1.2))

def snow(im, t, n=70, seed=11):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for k in range(n):
        x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(60, 140), rnd.uniform(3, 7)
        x = (x0 + 30*math.sin(t*1.1 + k)) % W; y = (y0 + sp*t) % H
        d.ellipse((x - r, y - r, x + r, y + r), fill=(245, 248, 255, 210))

def rays(im, x, y, t, col=(255, 230, 170), n=4, spread=26, length=900, strength=.18):
    layer = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(layer)
    for k in range(n):
        a = math.radians(100 + (k - n/2)*spread/n*4 + 2*math.sin(t*.6 + k))
        w = 70 + 20*k
        x1, y1 = x + length*math.cos(a), y + length*math.sin(a)
        d.polygon([(x - w/4, y), (x + w/4, y), (x1 + w, y1), (x1 - w, y1)], fill=col + (int(255*strength*(.7 + .3*math.sin(t*1.3 + k))),))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))

def candle_lit(im, x, y, t, s=1.0):
    candle(im, x, y, s, lit=False)
    fl = int(4*math.sin(t*13 + x)); glow(im, (x, int(y - 60*s)), int((90 + fl*3)*s), (255, 170, 70), .55)
    d = ImageDraw.Draw(im); h = (46 + fl)*s
    d.polygon([(x - 11*s, y - 12*s), (x, y - 12*s - h), (x + 11*s, y - 12*s)], fill=(255, 200, 80, 255))
    d.polygon([(x - 5*s, y - 14*s), (x, y - 14*s - h*.55), (x + 5*s, y - 14*s)], fill=(255, 250, 220, 255))

def hanging_lamp(im, x, y, t, col=(255, 210, 140)):
    a = math.radians(6*math.sin(t*1.6)); L = 260
    lx, ly = x + L*math.sin(a), y + L*math.cos(a)
    d = ImageDraw.Draw(im); d.line((x, y, lx, ly), fill=INK+(255,), width=4)
    glow(im, (int(lx), int(ly + 30)), 170, col, .6)
    d.polygon([(lx - 60, ly + 40), (lx + 60, ly + 40), (lx + 30, ly), (lx - 30, ly)], fill=(60, 50, 40, 255), outline=INK+(255,))
    d.ellipse((lx - 22, ly + 30, lx + 22, ly + 66), fill=col + (255,))

def wall_clock(im, x, y, t, r=70):
    d = ImageDraw.Draw(im)
    d.ellipse((x - r - 10, y - r - 10, x + r + 10, y + r + 10), fill=(110, 76, 40, 255), outline=INK+(255,), width=4)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(236, 226, 200, 255), outline=INK+(255,), width=3)
    for k in range(12):
        a = k*math.pi/6; d.line((x + (r - 12)*math.sin(a), y - (r - 12)*math.cos(a), x + (r - 4)*math.sin(a), y - (r - 4)*math.cos(a)), fill=INK+(255,), width=3)
    a1 = t*1.2; a2 = t*.1
    d.line((x, y, x + (r - 16)*math.sin(a1), y - (r - 16)*math.cos(a1)), fill=INK+(255,), width=4)
    d.line((x, y, x + (r - 34)*math.sin(a2), y - (r - 34)*math.cos(a2)), fill=INK+(255,), width=6)

def sparkle(im, x, y, t, s=1.0, col=(255, 240, 180)):
    k = .5 + .5*math.sin(t*9 + x)
    if k < .15: return
    d = ImageDraw.Draw(im); L = 26*s*k
    d.polygon([(x, y - L), (x + L*.22, y), (x, y + L), (x - L*.22, y)], fill=col + (230,))
    d.polygon([(x - L, y), (x, y - L*.22), (x + L, y), (x, y + L*.22)], fill=col + (230,))

def puff(im, x, y, t, t0, col=(150, 120, 90), n=10, spread=160):
    a = t - t0
    if a < 0 or a > 1.2: return
    layer = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(layer); rnd = random.Random(int(x))
    for k in range(n):
        ang = rnd.uniform(0, 2*math.pi); dist = spread*min(1, a*2.2)*rnd.uniform(.5, 1)
        r = 24 + 40*a; al = int(170*(1 - a/1.2))
        cx, cy = x + dist*math.cos(ang), y - abs(dist*math.sin(ang))*.6
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (al,))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10)))

def wallpaper(im, col=(110, 86, 74), y0=650, y1=1230, step=90, seed=0):
    d = ImageDraw.Draw(im)
    for yy in range(y0 + 30, y1, step):
        for xx in range(80 + ((yy//step) % 2)*step//2, 1020, step):
            d.ellipse((xx - 10, yy - 16, xx + 10, yy + 16), outline=col + (255,), width=3)
            d.line((xx, yy - 26, xx, yy + 26), fill=col + (160,), width=2)

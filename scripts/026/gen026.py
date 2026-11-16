"""Illustrations originales 026 (enfants envoyés par la poste) ; personnes historiques dessinées sans portrait ressemblant."""
exec(open(f"{HERE}/figs.py",encoding="utf-8").read())
COAT=(150,44,52); MAILBLUE=(46,70,110)

def post_office(seed=260):
    im=room(seed,wall=(70,82,96),floor=(54,46,40),warm=(70,80,100));d=ImageDraw.Draw(im)
    for r in range(4):
        for c in range(7):
            x=120+c*120;y=700+r*90;d.rectangle((x,y,x+100,y+76),fill=(48,40,34,255),outline=INK+(255,),width=3)
            if (r*7+c)%3==0:d.rectangle((x+14,y+30,x+86,y+70),fill=(220,206,170,255),outline=INK+(255,),width=2)
    glow(im,(470,900),420,(255,210,150),.18)
    return im

def girl(im,x,y,s=.62,stamps=6,mouth='smile'):
    person(im,x,y,s,coat=COAT,hair=(120,74,40),dress=True,mouth=mouth)
    d=ImageDraw.Draw(im)
    for k in range(stamps):
        sx=x-50*s+(k%3)*40*s;sy=y-190*s+(k//3)*48*s
        d.rectangle((sx,sy,sx+32*s,sy+38*s),fill=(214,200,150,255),outline=(120,30,30,255),width=2)
        d.rectangle((sx+6*s,sy+6*s,sx+26*s,sy+26*s),fill=(70,110,160,255) if k%2 else (180,60,60,255))
    d.rectangle((x+30*s,y-150*s,x+120*s,y-90*s),fill=(236,226,196,255),outline=INK+(255,),width=2)
    d.line((x+30*s,y-120*s,x+10*s,y-170*s),fill=INK+(255,),width=2)

def sack(im,x,y,s=1,label=True):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x-120*s,y-260*s,x+120*s,y),radius=int(60*s),fill=(176,150,104,255),outline=INK+(255,),width=5)
    d.polygon([(x-50*s,y-260*s),(x+50*s,y-260*s),(x+30*s,y-310*s),(x-30*s,y-310*s)],fill=(150,126,86,255),outline=INK+(255,))
    if label:d.text((x,y-120*s),'U.S. MAIL',font=font(int(38*s)),fill=(40,40,70,255),anchor='mm')

def parcel(im,x,y,s=1):
    d=ImageDraw.Draw(im)
    d.rectangle((x-90*s,y-120*s,x+90*s,y),fill=(176,134,84,255),outline=INK+(255,),width=4)
    d.line((x,y-120*s,x,y),fill=(120,80,50,255),width=6);d.line((x-90*s,y-60*s,x+90*s,y-60*s),fill=(120,80,50,255),width=6)

def counter(im,y=1170):
    d=ImageDraw.Draw(im);d.rectangle((60,y,1020,y+90),fill=(110,80,56,255),outline=INK+(255,),width=5)
    d.rectangle((60,y,1020,y+18),fill=(140,104,70,255),outline=INK+(255,),width=3)

def scale(im,x,y,u):
    d=ImageDraw.Draw(im)
    d.rectangle((x-170,y-30,x+170,y),fill=(120,120,126,255),outline=INK+(255,),width=5)
    d.rectangle((x-30,y,x+30,y+120),fill=(90,90,96,255),outline=INK+(255,),width=4)
    cx,cy=x+260,y-60;d.ellipse((cx-80,cy-80,cx+80,cy+80),fill=(236,230,210,255),outline=INK+(255,),width=5)
    a=math.radians(-120+200*u);d.line((cx,cy,cx+64*math.sin(a),cy-64*math.cos(a)),fill=RED+(255,),width=6)

def mountains(seed=270,snow=True):
    im=paper(seed,.02,(110,130,160));d=ImageDraw.Draw(im)
    rnd=random.Random(seed)
    for layer,(col,y0) in enumerate((((150,160,180),1020),((110,120,140),1140))):
        pts=[(0,1100)];x=0
        while x<W+100:
            x+=rnd.randint(140,240);pts.append((x,y0-rnd.randint(80,260)));x+=rnd.randint(60,140);pts.append((x,y0))
        pts+= [(W+200,1240),(0,1240)];d.polygon(pts,fill=col+(255,))
        if snow and layer==0:
            for i in range(1,len(pts)-2,2):
                px,py=pts[i];d.polygon([(px,py),(px-40,py+50),(px+40,py+50)],fill=(240,244,250,255))
    d.rectangle((0,1240,W,H),fill=(90,96,90,255))
    return im

def train(im,x,y,s=1,kids=1):
    d=ImageDraw.Draw(im)
    d.rectangle((x-260*s,y-210*s,x+260*s,y-30*s),fill=MAILBLUE+(255,),outline=INK+(255,),width=5)
    d.rectangle((x-280*s,y-230*s,x+280*s,y-206*s),fill=(30,40,60,255),outline=INK+(255,),width=4)
    d.text((x-60*s,y-90*s),'U.S. MAIL',font=font(int(40*s)),fill=(230,214,170,255),anchor='mm')
    for k in range(kids):
        wx=x+120*s+k*-300*s;d.rectangle((wx-50*s,y-180*s,wx+50*s,y-120*s),fill=(250,220,140,255),outline=INK+(255,),width=3)
        d.ellipse((wx-16*s,y-170*s,wx+16*s,y-138*s),fill=(208,169,128,255));d.rectangle((wx-22*s,y-138*s,wx+22*s,y-120*s),fill=COAT+(255,))
    for wx in (x-180*s,x-80*s,x+80*s,x+180*s):d.ellipse((wx-40*s,y-60*s,wx+40*s,y+20*s),fill=(40,40,44,255),outline=INK+(255,),width=4)
    d.rectangle((0,y+10*s,W,y+24*s),fill=(70,60,50,255))

def house(im,x,y,u):
    d=ImageDraw.Draw(im)
    d.rectangle((x-300,y-420,x+300,y),fill=(170,130,96,255),outline=INK+(255,),width=5)
    d.polygon([(x-340,y-420),(x,y-620),(x+340,y-420)],fill=(110,60,50,255),outline=INK+(255,))
    d.rectangle((x+140,y-300,x+250,y-200),fill=(250,220,140,255),outline=INK+(255,),width=4)
    door(im,x-80,y,u)

def paper_form(im,x,y):
    d=ImageDraw.Draw(im);d.rectangle((x-220,y-160,x+220,y+160),fill=(232,220,188,255),outline=INK+(255,),width=4)
    for k in range(6):d.line((x-180,y-110+k*40,x+150-(k%3)*60,y-110+k*40),fill=(90,70,50,255),width=4)

def calendar(im,x,y,label):
    d=ImageDraw.Draw(im);d.rectangle((x-110,y-150,x+110,y),fill=(236,230,214,255),outline=INK+(255,),width=5)
    d.rectangle((x-110,y-150,x+110,y-110),fill=RED+(255,));d.text((x,y-55),label,font=font(64),fill=INK+(255,),anchor='mm')

# ---------- v2 : décor enrichi ----------
def post_office2(seed, t=None):
    im = post_office(seed); d = ImageDraw.Draw(im)
    for x in (170, 790):
        d.rectangle((x - 60, 1000, x + 60, 1150), fill=(196, 180, 140, 255), outline=INK+(255,), width=3)
        d.rectangle((x - 44, 1016, x + 44, 1070), fill=(150, 60, 50, 255)); d.line((x - 40, 1100, x + 40, 1100), fill=(90, 70, 50, 255), width=4)
    return im

def office_life(im, t):
    hanging_lamp(im, 470, 600, t); wall_clock(im, 880, 760, t, 56)

def wheels(im, x, y, s, t):
    d = ImageDraw.Draw(im)
    for wx in (x - 180*s, x - 80*s, x + 80*s, x + 180*s):
        a = t*8
        for k in range(4):
            aa = a + k*math.pi/4; d.line((wx - 34*s*math.cos(aa), y - 20*s - 34*s*math.sin(aa), wx + 34*s*math.cos(aa), y - 20*s + 34*s*math.sin(aa)), fill=(150, 150, 156, 255), width=4)

def poles(im, t, y=1240, speed=420):
    d = ImageDraw.Draw(im)
    for k in range(5):
        x = (k*300 - t*speed) % 1500 - 200
        d.rectangle((x - 8, y - 380, x + 8, y), fill=(70, 50, 36, 255)); d.rectangle((x - 50, y - 370, x + 50, y - 356), fill=(70, 50, 36, 255))
    d.line([(-200, y - 360)] + [((k*300 - t*speed) % 1500 - 200, y - 362) for k in range(5)], fill=(40, 30, 24, 255), width=2)

def smoke_puffs(im, x, y, t):
    layer = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(layer)
    for k in range(6):
        a = (t*1.4 + k/6) % 1; r = 30 + 70*a
        cx, cy = x - 260*a, y - 120*a - 40*math.sin(a*3)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(230, 230, 236, int(200*(1 - a))))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(6)))

def grandma(im, x, y, t, u):
    actor(im, x, y, .8, t, kind='up', mouth='smile', coat=(90, 90, 110), dress=True, hair=(200, 200, 200))
    d = ImageDraw.Draw(im); a = u*50
    for sx in (-1, 1):
        d.line((x + sx*60, y - 160, x + sx*(90 + a), y - 230 - a*.6), fill=(90, 90, 110, 255), width=26)
        d.ellipse((x + sx*(90 + a) - 16, y - 246 - a*.6, x + sx*(90 + a) + 16, y - 214 - a*.6), fill=SKIN+(255,), outline=INK+(255,), width=2)

def heart(im, x, y, s=1):
    d = ImageDraw.Draw(im)
    d.ellipse((x - 30*s, y - 24*s, x, y + 6*s), fill=(220, 70, 80, 230)); d.ellipse((x, y - 24*s, x + 30*s, y + 6*s), fill=(220, 70, 80, 230))
    d.polygon([(x - 30*s, y - 6*s), (x + 30*s, y - 6*s), (x, y + 34*s)], fill=(220, 70, 80, 230))

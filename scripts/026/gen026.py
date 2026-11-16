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

"""Illustrations originales 025 (momies mangées) ; rien de graphique, corps toujours bandés ou couverts."""
exec(open(f"{HERE}/figs.py",encoding="utf-8").read())
LINEN=(196,176,130); POWDER=(120,82,48)

def shop(seed=250):
    im=room(seed,wall=(88,62,40),floor=(58,40,28),warm=(110,72,36));d=ImageDraw.Draw(im)
    for row in range(3):
        y=760+row*130;d.rectangle((90,y,990,y+16),fill=(60,38,22,255),outline=INK+(255,),width=3)
        rnd=random.Random(seed+row);x=110
        while x<960:
            w=rnd.randint(46,70);h=rnd.randint(70,110);col=rnd.choice([(90,120,90),(150,110,60),(110,80,60),(80,90,120)])
            d.rounded_rectangle((x,y-h,x+w,y),radius=10,fill=col+(240,),outline=INK+(255,),width=3)
            d.rectangle((x+w*.25,y-h-18,x+w*.75,y-h),fill=(200,180,140,255),outline=INK+(255,),width=2)
            x+=w+rnd.randint(14,30)
    glow(im,(470,900),420,(255,170,90),.22)
    return im

def mummy(im,x,y,s=1,ang=0):
    L=Image.new('RGBA',(W,H));d=ImageDraw.Draw(L)
    d.rounded_rectangle((x-70*s,y-420*s,x+70*s,y),radius=int(60*s),fill=LINEN+(255,),outline=INK+(255,),width=5)
    d.ellipse((x-62*s,y-520*s,x+62*s,y-390*s),fill=LINEN+(255,),outline=INK+(255,),width=5)
    for k in range(14):
        yy=y-500*s+k*36*s;d.line((x-66*s,yy,x+66*s,yy+18*s),fill=(150,128,90,255),width=max(2,int(4*s)))
    for sx in (-1,1):d.line((x+sx*24*s-12*s,y-460*s,x+sx*24*s+12*s,y-460*s),fill=(70,50,30,255),width=max(3,int(6*s)))
    if ang:L=L.rotate(ang,resample=Image.Resampling.BICUBIC,center=(x,y))
    im.alpha_composite(L)

def sarcophagus(im,x,y,s=1):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x-130*s,y-620*s,x+130*s,y),radius=int(110*s),fill=(150,104,40,255),outline=INK+(255,),width=6)
    d.rounded_rectangle((x-100*s,y-590*s,x+100*s,y-20*s),radius=int(90*s),fill=(40,30,24,255),outline=(200,160,70,255),width=5)

def spoon(im,x,y,u=1,s=1):
    d=ImageDraw.Draw(im)
    d.line((x,y,x+260*s,y+150*s),fill=(190,190,196,255),width=int(22*s))
    d.ellipse((x-90*s,y-55*s,x+40*s,y+45*s),fill=(200,200,206,255),outline=INK+(255,),width=4)
    if u>0:d.ellipse((x-75*s,y-40*s,x+25*s,y+30*s),fill=POWDER+(255,))

def cup(im,x,y,s=1,liquid=True,swirl=0):
    d=ImageDraw.Draw(im)
    d.polygon([(x-110*s,y-200*s),(x+110*s,y-200*s),(x+70*s,y-20*s),(x-70*s,y-20*s)],fill=(170,150,120,255),outline=INK+(255,))
    d.rectangle((x-14*s,y-20*s,x+14*s,y+80*s),fill=(170,150,120,255),outline=INK+(255,),width=3)
    d.ellipse((x-80*s,y+60*s,x+80*s,y+100*s),fill=(170,150,120,255),outline=INK+(255,),width=4)
    if liquid:
        d.ellipse((x-104*s,y-214*s,x+104*s,y-186*s),fill=(96,60,34,255),outline=INK+(255,),width=3)
        if swirl:d.arc((x-70*s,y-210*s,x+70*s,y-190*s),int(swirl)%360,int(swirl+200)%360,fill=(150,100,60,255),width=4)

def mortar(im,x,y,t,s=1):
    d=ImageDraw.Draw(im)
    a=math.sin(t*7)*18;px=x+40*s+a;d.line((px,y-20*s,px+90*s,y-300*s),fill=(110,100,92,255),width=int(38*s))
    d.pieslice((x-180*s,y-180*s,x+180*s,y+150*s),0,180,fill=(130,120,110,255),outline=INK+(255,),width=5)
    d.rectangle((x-190*s,y-30*s,x+190*s,y),fill=(150,140,128,255),outline=INK+(255,),width=5)
    for k in range(6):
        rr=random.Random(k+int(t*8))
        d.ellipse((x-120*s+k*40*s,y-50*s-rr.randint(0,30),x-100*s+k*40*s,y-30*s-rr.randint(0,30)),fill=POWDER+(255,))

def strips(im,x,y,t):
    d=ImageDraw.Draw(im)
    for k in range(5):
        yy=y+((t*80+k*60)%240);d.line((x-120+k*50,yy,x-60+k*50,yy+20),fill=LINEN+(255,),width=10)

def pour(im,x,y,t,t0):
    a=t-t0
    if a<0:return
    d=ImageDraw.Draw(im)
    for k in range(int(min(40,a*60))):
        ox=random.Random(k).randint(-10,10);yy=y+((a*400+k*25)%260)
        d.ellipse((x-6+ox,yy-4,x+6+ox,yy+4),fill=POWDER+(255,))

def pouch(im,x,y,s=1,g=0):
    d=ImageDraw.Draw(im)
    if g>0:glow(im,(x,y),120*s,(255,200,120),g)
    d.ellipse((x-60*s,y-50*s,x+60*s,y+60*s),fill=(120,80,50,255),outline=INK+(255,),width=4)
    d.polygon([(x-30*s,y-50*s),(x+30*s,y-50*s),(x+15*s,y-80*s),(x-15*s,y-80*s)],fill=(100,66,40,255),outline=INK+(255,))

def desert(seed=260):
    im=paper(seed,.02,(150,110,60));d=ImageDraw.Draw(im)
    d.rectangle((0,1040,W,H),fill=(176,140,86,255))
    for k in range(5):d.arc((-200+k*300,1000,200+k*300,1120),180,360,fill=(150,116,70,255),width=6)
    glow(im,(820,700),160,(255,230,150),.8);d.ellipse((760,640,880,760),fill=(250,230,170,255))
    return im

def covered(im,x,y,s=1):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x-170*s,y-60*s,x+170*s,y),radius=int(40*s),fill=(205,190,160,255),outline=INK+(255,),width=4)
    d.ellipse((x-200*s,y-70*s,x-110*s,y-5*s),fill=(205,190,160,255),outline=INK+(255,),width=4)

def crate(im,x,y,label=True):
    d=ImageDraw.Draw(im);d.rectangle((x-110,y-140,x+110,y),fill=(140,100,60,255),outline=INK+(255,),width=5)
    d.line((x-110,y-70,x+110,y-70),fill=INK+(255,),width=3)
    if label:d.text((x,y-40),'MUMIA',font=font(40),fill=(40,24,14,255),anchor='mm')

def mumia_jar(im,x=470,y=1200):
    d=ImageDraw.Draw(im);d.rounded_rectangle((x-90,y-240,x+90,y),radius=30,fill=(150,110,60,255),outline=INK+(255,),width=5)
    d.rectangle((x-70,y-140,x+70,y-80),fill=(230,214,170,255),outline=INK+(255,),width=3);d.text((x,y-110),'MUMIA',font=font(36),fill=(40,24,14,255),anchor='mm')

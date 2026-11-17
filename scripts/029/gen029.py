"""Illustrations originales 029 (cercueil de sécurité à cloche) ; dessins de brevet stylisés, rien de graphique, aucun corps."""
exec(open(f"{HERE}/figs.py",encoding="utf-8").read())
BRONZE=(190,140,60); EARTH=(84,62,44); Y0=1010

def graveyard(seed=400):
    im=paper(seed,.12,(52,56,78));d=ImageDraw.Draw(im);rnd=random.Random(seed)
    glow(im,(820,640),150,(235,235,210),.35);d.ellipse((780,600,860,680),fill=(238,234,212,255))
    for x,h in ((110,170),(300,210),(660,180),(950,200)):
        d.rounded_rectangle((x-55,1120-h,x+55,1135),radius=50,fill=(96,98,110,255),outline=INK+(255,),width=5)
        d.line((x,1120-h+40,x,1120-h+110),fill=INK+(255,),width=5);d.line((x-26,1120-h+70,x+26,1120-h+70),fill=INK+(255,),width=5)
    d.rectangle((0,1135,W,H),fill=(46,40,38,255))
    for k in range(70):
        x=rnd.randint(0,W);y=rnd.randint(1135,1300);d.line((x,y,x+rnd.randint(-8,8),y-rnd.randint(14,30)),fill=(60,84,52,255),width=3)
    return im

def street(seed=401):
    im=paper(seed,.12,(56,56,76));d=ImageDraw.Draw(im);rnd=random.Random(seed)
    for x in range(-20,1080,190):
        h=rnd.randint(300,430);d.rectangle((x,1240-h,x+180,1240),fill=(80,74,84,255),outline=INK+(255,),width=5)
        d.polygon([(x-8,1240-h),(x+90,1240-h-90),(x+188,1240-h)],fill=(60,52,60,255),outline=INK+(255,))
        for wy in range(1240-h+40,1180,90):
            lit=rnd.random()<.45
            d.rectangle((x+30,wy,x+70,wy+50),fill=(255,208,140,255) if lit else (30,34,56,255),outline=INK+(255,),width=3)
            d.rectangle((x+110,wy,x+150,wy+50),fill=(255,208,140,255) if rnd.random()<.4 else (30,34,56,255),outline=INK+(255,),width=3)
    d.rectangle((0,1240,W,H),fill=(66,62,70,255))
    for k in range(-9,10):d.line((540+k*34,1240,540+k*280,H),fill=(52,48,56,255),width=3)
    for x in (90,990):
        d.line((x,820,x,1240),fill=INK+(255,),width=9);glow(im,(x,810),130,(255,214,150),.5)
    fog=Image.new('RGBA',(W,H),(0,0,0,0));fd=ImageDraw.Draw(fog);fd.rectangle((0,1080,W,1300),fill=(200,200,220,60));im.alpha_composite(fog.filter(ImageFilter.GaussianBlur(40)))
    return im

def bell(im,x,y,s=1,ang=0):
    L=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(L)
    d.line((x,y-40*s,x,y+10*s),fill=INK+(255,),width=max(3,int(8*s)))
    d.polygon([(x-30*s,y+12*s),(x+30*s,y+12*s),(x+78*s,y+170*s),(x-78*s,y+170*s)],fill=BRONZE+(255,),outline=INK+(255,))
    d.ellipse((x-34*s,y-4*s,x+34*s,y+30*s),fill=BRONZE+(255,),outline=INK+(255,),width=3)
    d.rectangle((x-88*s,y+166*s,x+88*s,y+190*s),fill=(214,168,84,255),outline=INK+(255,),width=3)
    d.ellipse((x-16*s,y+186*s,x+16*s,y+222*s),fill=(60,44,30,255),outline=INK+(255,),width=3)
    if ang:L=L.rotate(ang,resample=Image.BICUBIC,center=(x,y-40*s))
    im.alpha_composite(L)

def sound_arcs(im,x,y,t,t0,n=3):
    a=t-t0
    if a<0:return
    d=ImageDraw.Draw(im)
    for k in range(n):
        r=70+((a*260+k*70)%300);al=int(255*max(0,1-r/380))
        L=Image.new('RGBA',(W,H),(0,0,0,0));ImageDraw.Draw(L).arc((x-r,y-r,x+r,y+r),200,340,fill=(255,236,180,al),width=7);im.alpha_composite(L)

def underground(im,t=0,ring=0,rope_wave=0,hand=True,bell_on=True):
    d=ImageDraw.Draw(im)
    d.rectangle((40,Y0,1040,1240),fill=EARTH+(255,),outline=INK+(255,),width=5)
    d.rectangle((40,Y0-30,1040,Y0+8),fill=(70,100,60,255),outline=INK+(255,),width=4)
    rnd=random.Random(5)
    for k in range(60):
        x=rnd.randint(60,1020);y=rnd.randint(Y0+20,1230);r=rnd.randint(4,9);d.ellipse((x-r,y-r,x+r,y+r),fill=(110,86,62,255))
    d.rounded_rectangle((250,1150,690,1225),radius=14,fill=(120,80,46,255),outline=INK+(255,),width=5)
    d.rectangle((250,1170,690,1180),fill=(90,58,32,255))
    d.rectangle((443,Y0,497,1150),fill=(36,30,28,255),outline=INK+(255,),width=4)
    for y in range(Y0+16,1146,26):d.line((443,y,497,y),fill=(150,126,90,255),width=4)
    d.line((452,Y0,452,1150),fill=(150,126,90,255),width=3);d.line((488,Y0,488,1150),fill=(150,126,90,255),width=3)
    # post + bell au-dessus du sol
    d.line((700,Y0-30,700,780),fill=(64,46,32,255),width=16);d.line((700,780,560,780),fill=(64,46,32,255),width=14)
    a=ring*14*math.sin(t*20) if ring else 0
    if bell_on:bell(im,560,780,.85,a)
    # corde : cloche -> bouche du tube -> coffre
    pts=[(560,780+190*.85),(470,Y0-30)]+[(470+rope_wave*math.sin(y*.05+t*30)*6*((y-Y0)/140),y) for y in range(Y0,1150,10)]
    d.line(pts,fill=(214,196,150,255),width=5)
    if hand:d.ellipse((452,1140,490,1170),fill=SKIN+(255,),outline=INK+(255,),width=3)

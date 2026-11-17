"""Illustrations originales 028 (gardes de l'Élysée, malaises) ; silhouettes gravées, rien de graphique."""
exec(open(f"{HERE}/figs.py",encoding="utf-8").read())
NAVY=(34,44,92); SILVER=(196,200,210); PLUME=(190,30,30); SUIT=(26,28,38)

def courtyard(seed=280):
    im=paper(seed,.10,(62,60,78));d=ImageDraw.Draw(im)
    d.rectangle((40,640,1040,1240),fill=(100,94,104,255),outline=INK+(255,),width=5)
    for x in range(100,1000,170):
        d.rectangle((x,730,x+90,980),fill=(32,38,62,255),outline=INK+(255,),width=5)
        d.pieslice((x,690,x+90,770),180,360,fill=(32,38,62,255),outline=INK+(255,),width=5)
        d.line((x+45,730,x+45,980),fill=INK+(255,),width=4)
        glow(im,(x+45,860),80,(255,214,150),.22)
    d.rectangle((0,1240,W,H),fill=(70,66,72,255))
    for k in range(-9,10):d.line((540+k*34,1240,540+k*280,H),fill=(54,50,56,255),width=3)
    for y in (1290,1360,1450,1570,1720):d.line((0,y,W,y),fill=(54,50,56,255),width=3)
    d.rectangle((0,1226,W,1246),fill=(130,124,130,255),outline=INK+(255,),width=4)
    for x in (150,930):glow(im,(x,980),150,(255,214,150),.28)
    return im

def steps(im,x=420,y=1240,n=4):
    d=ImageDraw.Draw(im)
    for k in range(n):d.rectangle((x-190-k*20,y-k*34-34,x+190+k*20,y-k*34),fill=(150,144,150,255),outline=INK+(255,),width=4)

def column(im,x):
    d=ImageDraw.Draw(im);d.rectangle((x-34,660,x+34,1240),fill=(138,130,136,255),outline=INK+(255,),width=5)
    for y in range(700,1240,60):d.line((x-34,y,x+34,y),fill=(112,106,112,255),width=3)

def guard(im,x,y,s=.85,ang=0,sabre=True,mouth='flat',eyes='open',lean=0):
    L=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(L)
    person(L,x,y,s,coat=NAVY,hair=(40,30,24),mouth=mouth,eyes=eyes)
    d.chord((x-68*s,y-398*s,x+68*s,y-300*s),180,360,fill=SILVER+(255,),outline=INK+(255,),width=3)
    d.rectangle((x-70*s,y-356*s,x+70*s,y-340*s),fill=GOLD+(255,),outline=INK+(255,),width=2)
    d.ellipse((x-14*s,y-440*s,x+14*s,y-390*s),fill=PLUME+(255,),outline=INK+(255,),width=2)
    d.line((x-82*s,y-215*s,x+70*s,y-60*s),fill=(232,232,232,255),width=max(4,int(14*s)))
    for sx in (-1,1):d.ellipse((x+sx*92*s-26*s,y-236*s,x+sx*92*s+26*s,y-200*s),fill=GOLD+(255,),outline=INK+(255,),width=2)
    if sabre:
        d.line((x+84*s,y-30*s,x+84*s,y-440*s),fill=SILVER+(255,),width=max(3,int(9*s)))
        d.ellipse((x+70*s,y-160*s,x+98*s,y-120*s),fill=(240,240,240,255),outline=INK+(255,),width=2)
    if ang:L=L.rotate(ang,resample=Image.BICUBIC,center=(x,y))
    im.alpha_composite(L)

def sabre_obj(im,x,y,length=330,ang=0):
    L=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(L)
    d.line((x-length//2,y,x+length//2,y),fill=SILVER+(255,),width=11);d.line((x-length//2-4,y-16,x-length//2-4,y+16),fill=GOLD+(255,),width=10)
    L=L.rotate(ang,resample=Image.BICUBIC,center=(x,y));im.alpha_composite(L)

def fall_angle(t,t0,t1,sign=1):
    """Oscille de plus en plus fort entre t0 et t1, puis bascule (sans rebond brutal)."""
    if t<t0:return 0
    if t<t1:
        u=(t-t0)/(t1-t0);return sign*(10*u*u)*math.sin((t-t0)*9)
    a=ease((t-t1)/.7);return sign*(10*math.sin((t1-t0)*9)*0+8+77*a)

def suit(im,x,y,s=.85,mouth='flat',kind='flat',t=0,back=False):
    actor(im,x,y,s,t,kind=kind,mouth=mouth,coat=SUIT,hair=(70,60,52),back=back)
    d=ImageDraw.Draw(im);d.polygon([(x-14*s,y-238*s),(x+14*s,y-238*s),(x+10*s,y-120*s),(x,y-100*s),(x-10*s,y-120*s)],fill=(160,30,30,255))

def bubble(im,x,y,text,sz=60,tail=(0,90)):
    d=ImageDraw.Draw(im);f=font(sz);w=int(f.getlength(text))+70;h=int(sz*2)
    d.ellipse((x-w//2,y-h//2,x+w//2,y+h//2),fill=(238,228,206,255),outline=INK+(255,),width=5)
    d.polygon([(x-20,y+h//2-8),(x+20,y+h//2-8),(x+tail[0],y+h//2+tail[1])],fill=(238,228,206,255),outline=INK+(255,))
    d.text((x,y),text,font=f,fill=INK+(255,),anchor='mm')

def gauge(im,x,y,r,needle):
    d=ImageDraw.Draw(im);d.ellipse((x-r,y-r,x+r,y+r),fill=(226,214,184,255),outline=INK+(255,),width=7)
    for k in range(-60,241,30):
        a=math.radians(k);d.line((x+r*.78*math.cos(a),y-r*.78*math.sin(a),x+r*.92*math.cos(a),y-r*.92*math.sin(a)),fill=INK+(255,),width=5)
    d.pieslice((x-r*.92,y-r*.92,x+r*.92,y+r*.92),-60,-10,fill=(200,28,28,255))
    a=math.radians(needle);d.line((x,y,x+r*.8*math.cos(a),y-r*.8*math.sin(a)),fill=INK+(255,),width=10)
    d.ellipse((x-14,y-14,x+14,y+14),fill=INK+(255,))

def brain(im,x,y,s,dim):
    d=ImageDraw.Draw(im)
    col=tuple(int(c*(1-.65*dim)) for c in (224,150,160))
    for dx,dy,rr in ((-60,0,70),(0,-26,76),(60,0,70),(-30,38,60),(34,38,60)):
        d.ellipse((x+(dx-rr)*s,y+(dy-rr)*s,x+(dx+rr)*s,y+(dy+rr)*s),fill=col+(255,),outline=INK+(255,),width=4)
    d.line((x,y-90*s,x,y+60*s),fill=INK+(255,),width=4)

def check(im,x,y,s=1,u=1):
    if u<=0:return
    d=ImageDraw.Draw(im);p=[(x-90*s,y),(x-30*s,y+70*s),(x+100*s,y-80*s)]
    d.line(p[:2],fill=(120,200,120,255),width=26);
    if u>.5:d.line(p[1:],fill=(120,200,120,255),width=26)

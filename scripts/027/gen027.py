"""Illustrations originales 027 (photos des morts, mythe démonté) ; aucun corps montré : défunt endormi sous une couverture."""
exec(open(f"{HERE}/figs.py",encoding="utf-8").read())
SEPIA_L=(196,170,128); SEPIA_D=(92,70,48); METAL=(70,70,76)

def parlor(seed=270):
    im=room(seed,wall=(84,66,58),floor=(56,40,32),warm=(96,70,52));d=ImageDraw.Draw(im)
    d.rectangle((40,640,1040,700),fill=(70,50,40,255),outline=INK+(255,),width=4)
    glow(im,(470,900),420,(255,200,140),.18)
    return im

def stand(im,x,y,s=1,tilt=0,glowing=0):
    L=Image.new('RGBA',(W,H));d=ImageDraw.Draw(L)
    if glowing>0:glow(L,(x,y-200*s),160*s,(255,220,120),glowing)
    d.line((x,y-20*s,x,y-430*s),fill=METAL+(255,),width=int(14*s))
    for dx in (-90,0,90):d.line((x,y-20*s,x+dx*s,y),fill=METAL+(255,),width=int(12*s))
    d.arc((x-50*s,y-470*s,x+50*s,y-400*s),180,360,fill=METAL+(255,),width=int(12*s))
    d.ellipse((x-14*s,y-250*s,x+14*s,y-222*s),fill=(110,110,116,255),outline=INK+(255,),width=2)
    if tilt:L=L.rotate(tilt,resample=Image.Resampling.BICUBIC,center=(x,y))
    im.alpha_composite(L)

def frame_photo(im,x,y,w=520,h=640,kind='standing',t=0,glow_stand=0):
    d=ImageDraw.Draw(im)
    d.rectangle((x-w//2-26,y-h//2-26,x+w//2+26,y+h//2+26),fill=(110,76,40,255),outline=INK+(255,),width=6)
    d.rectangle((x-w//2,y-h//2,x+w//2,y+h//2),fill=SEPIA_L+(255,),outline=INK+(255,),width=3)
    s=w/520;base=y+h//2-30*s
    if kind=='standing':
        stand(im,int(x-60*s),int(base),.62*s,0,glow_stand)
        person(im,int(x-60*s),int(base),.62*s,coat=SEPIA_D,hair=(60,44,30),skin=(206,180,140))
        person(im,int(x+90*s),int(base),.56*s,coat=(120,96,70),hair=(60,44,30),dress=True,skin=(206,180,140))
    elif kind=='empty':
        d.rectangle((x-w//2+20,y-h//2+20,x+w//2-20,y+h//2-20),fill=(150,130,100,255))
        question_mark(im,x,y,.6*s)

def camera_box(im,x,y,s=1,flash=0):
    d=ImageDraw.Draw(im)
    for dx in (-80,0,80):d.line((x,y-260*s,x+dx*s,y),fill=(80,60,40,255),width=int(10*s))
    d.rectangle((x-110*s,y-400*s,x+90*s,y-260*s),fill=(70,46,30,255),outline=INK+(255,),width=5)
    d.rectangle((x+90*s,y-370*s,x+150*s,y-290*s),fill=(40,40,44,255),outline=INK+(255,),width=4)
    d.ellipse((x+130*s,y-360*s,x+170*s,y-300*s),fill=(120,140,160,255),outline=INK+(255,),width=3)
    d.polygon([(x-110*s,y-400*s),(x-200*s,y-260*s),(x-110*s,y-260*s)],fill=(20,18,18,255))
    if flash>0:glow(im,(int(x+150*s),int(y-330*s)),260*s,(255,255,230),flash)

def sofa_sleeper(im,x,y,s=1):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x-330*s,y-170*s,x+330*s,y),radius=int(40*s),fill=(110,50,50,255),outline=INK+(255,),width=5)
    d.rounded_rectangle((x-360*s,y-250*s,x-260*s,y),radius=int(30*s),fill=(96,42,42,255),outline=INK+(255,),width=5)
    d.ellipse((x-270*s,y-250*s,x-150*s,y-150*s),fill=(230,214,190,255),outline=INK+(255,),width=3)
    d.ellipse((x-250*s,y-260*s,x-150*s,y-170*s),fill=SKIN+(255,),outline=INK+(255,),width=4)
    d.arc((x-252*s,y-262*s,x-148*s,y-190*s),190,350,fill=(60,44,30,255),width=int(12*s))
    for sx in (-1,1):d.arc((x-200*s+sx*20*s-9*s,y-222*s,x-200*s+sx*20*s+9*s,y-208*s),20,160,fill=INK+(255,),width=3)
    d.rounded_rectangle((x-160*s,y-200*s,x+300*s,y-130*s),radius=int(30*s),fill=(214,200,170,255),outline=INK+(255,),width=4)
    for k in range(4):d.ellipse((x+60*s+k*50*s,y-240*s,x+100*s+k*50*s,y-200*s),fill=(230,230,240,255),outline=INK+(255,),width=2)

def book(im,x,y,t):
    d=ImageDraw.Draw(im)
    d.polygon([(x-300,y),(x,y+30),(x,y-170),(x-300,y-200)],fill=(236,226,200,255),outline=INK+(255,))
    d.polygon([(x+300,y),(x,y+30),(x,y-170),(x+300,y-200)],fill=(230,218,190,255),outline=INK+(255,))
    for k in range(3):
        d.rectangle((x-250,y-170+k*55,x-160,y-125+k*55),fill=(160,136,100,255),outline=INK+(255,),width=2)
        d.rectangle((x+60,y-170+k*55,x+150,y-125+k*55),fill=(160,136,100,255),outline=INK+(255,),width=2)
    mx=x+int(140*math.sin(t*1.5));my=y-100
    d.ellipse((mx-80,my-80,mx+80,my+80),outline=(60,50,40,255),width=12);d.line((mx+56,my+56,mx+150,my+150),fill=(60,40,26,255),width=22)

# ---------- v2 : décor enrichi ----------
def parlor2(seed, window=True):
    im = parlor(seed); wallpaper(im, (104, 82, 70))
    d = ImageDraw.Draw(im)
    if window:
        d.rectangle((760, 720, 960, 980), fill=(40, 52, 80, 255), outline=INK+(255,), width=6)
        d.line((860, 720, 860, 980), fill=INK+(255,), width=5); d.line((760, 850, 960, 850), fill=INK+(255,), width=5)
        d.ellipse((880, 740, 940, 800), fill=(230, 230, 210, 255))
    return im

def parlor_life(im, t, window=True):
    if window: rays(im, 860, 760, t, (200, 210, 255), 3, 18, 700, .1)
    candle_lit(im, 120, 1120, t, .8)

def camera_flash(frame_im, t, t0):
    a = t - t0
    if 0 <= a < .35:
        layer = Image.new('RGBA', (W, H), (255, 255, 240, int(200*(1 - a/.35)))); frame_im.alpha_composite(layer)

def portraits_wall(im, t):
    for k, (x, y) in enumerate(((200, 760), (380, 740), (560, 770))):
        d = ImageDraw.Draw(im); d.ellipse((x - 60, y - 76, x + 60, y + 76), fill=(110, 76, 40, 255), outline=INK+(255,), width=4)
        d.ellipse((x - 46, y - 62, x + 46, y + 62), fill=SEPIA_L+(255,)); d.ellipse((x - 20, y - 40, x + 20, y), fill=(150, 120, 90, 255)); d.rectangle((x - 30, y, x + 30, y + 50), fill=SEPIA_D+(255,))

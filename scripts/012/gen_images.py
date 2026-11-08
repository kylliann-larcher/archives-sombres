import math, random, json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

W, H = 1080, 1920
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
CREAM = (238, 224, 196); RED = (200, 28, 28); INK = (22, 14, 10); SEPIA = (66, 44, 28)
def font(sz, f=FB): return ImageFont.truetype(f, sz)

def paper(seed, dark=0.0, warm=(70, 46, 30)):
    rnd = np.random.RandomState(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W/2) / (W*0.62))**2 + ((yy - H/2) / (H*0.55))**2)
    base = np.clip(1.0 - 0.75*d**1.7, 0, 1)
    img = np.zeros((H, W, 3), np.float32)
    for c in range(3):
        img[..., c] = warm[c] * (0.35 + 0.9*base) * (1-dark)
    img += rnd.normal(0, 4.5, (H, W, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

def glow(im, xy, r, color, strength=1.0):
    g = Image.new("RGBA", im.size, (0,0,0,0)); d = ImageDraw.Draw(g)
    d.ellipse((xy[0]-r, xy[1]-r, xy[0]+r, xy[1]+r), fill=color+(int(170*strength),))
    g = g.filter(ImageFilter.GaussianBlur(r/2.2))
    im.alpha_composite(g)

def hatch(d, box, step=9, ang=0.6, col=(14,8,5,90), w=2):
    x0,y0,x1,y1 = box
    L = int(math.hypot(x1-x0, y1-y0))
    for k in range(-L, L, step):
        d.line((x0+k, y0, x0+k+int((y1-y0)*math.tan(ang)), y1), fill=col, width=w)

def flame(im, cx, base_y, h, wdt, seed=0, color=(255,150,30)):
    rnd = random.Random(seed)
    glow(im, (cx, base_y - h*0.5), h*1.1, (255,120,20), 0.9)
    d = ImageDraw.Draw(im)
    for scale, col in ((1.0, (230,70,20,255)), (0.78, (255,150,30,255)), (0.5, (255,225,120,255)), (0.25, (255,250,215,255))):
        pts = []
        n = 16
        for i in range(n+1):
            t = i / n
            hh = base_y - h*scale*math.sin(t*math.pi)**0.8 * (0.85 + 0.25*rnd.random())
            xx = cx - wdt*scale/2 + wdt*scale*t
            pts.append((xx, base_y if i in (0, n) else hh))
        # teardrop: pinch the top
        pts = [(cx + (x-cx)*(1 - 0.55*((base_y-y)/(h*scale+1))), y) for x, y in pts]
        d.polygon(pts, fill=col)

def vignette(im, power=1.0):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W/2) / (W*0.7))**2 + ((yy - H/2) / (H*0.6))**2)
    m = np.clip(1 - 0.55*d**2.2*power, 0.15, 1)
    a = np.array(im.convert("RGB")).astype(np.float32) * m[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def title(im, lines, y=440, size=92, maxw=800, cx=470):
    d = ImageDraw.Draw(im)
    for text, col in lines:
        sz = size
        while font(sz).getlength(text) > maxw and sz > 40: sz -= 3
        f = font(sz)
        w = f.getlength(text)
        d.text((cx - w/2, y), text, font=f, fill=col, stroke_width=8, stroke_fill=(0,0,0))
        y += int(sz*1.18)
    return y

def small(im, text, y=385, size=40, col=(235,215,170)):
    d = ImageDraw.Draw(im); f = font(size)
    d.text((120, y), text, font=f, fill=col, stroke_width=4, stroke_fill=(0,0,0))

def stamp_red(im, text, cx, cy, size=96, ang=-8):
    f = font(size); w = int(f.getlength(text)) + 60; h = int(size*1.5)
    t = Image.new("RGBA", (w, h), (0,0,0,0)); d = ImageDraw.Draw(t)
    d.rectangle((2,2,w-3,h-3), outline=RED+(255,), width=9)
    d.text((30, h//2 - size*0.62), text, font=f, fill=RED+(255,))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(t, (int(cx - t.width/2), int(cy - t.height/2)))

# ---------- objets ----------
def cassette(im, cx, cy, s=1.0, lit=False, seal=True):
    d = ImageDraw.Draw(im)
    w, h = int(520*s), int(300*s)
    x0, y0 = cx-w//2, cy-h//2
    top = [(x0+40*s, y0-70*s), (x0+w+40*s, y0-70*s), (x0+w, y0), (x0, y0)]
    d.polygon(top, fill=(92,58,32,255), outline=INK+(255,))
    d.rectangle((x0, y0, x0+w, y0+h), fill=(76,46,26,255), outline=INK+(255,), width=5)
    hatch(d, (x0, y0, x0+w, y0+h), 12, 0.0, (20,10,5,110), 3)
    d.polygon([(x0+w, y0), (x0+w+40*s, y0-70*s), (x0+w+40*s, y0+h-70*s), (x0+w, y0+h)], fill=(52,31,17,255), outline=INK+(255,))
    for bx in (x0+int(70*s), x0+w-int(100*s)):
        d.rectangle((bx, y0, bx+int(30*s), y0+h), fill=(40,40,44,255), outline=INK+(255,), width=3)
    d.rectangle((cx-int(40*s), cy-int(40*s), cx+int(40*s), cy+int(40*s)), fill=(150,120,55,255), outline=INK+(255,), width=4)
    d.ellipse((cx-8, cy-10, cx+8, cy+6), fill=INK+(255,)); d.rectangle((cx-3, cy, cx+3, cy+22), fill=INK+(255,))
    if seal:
        sx, sy = cx+int(110*s), y0+int(h*0.55)
        d.ellipse((sx-34, sy-34, sx+34, sy+34), fill=(170,20,20,255), outline=(70,5,5,255), width=4)
        d.ellipse((sx-16, sy-16, sx+16, sy+16), outline=(90,8,8,255), width=4)
    if lit: glow(im, (cx, cy), 420*s, (255,140,40), 0.45)

def candle(im, x, y, s=1.0, lit=True):
    d = ImageDraw.Draw(im)
    d.rectangle((x-22*s, y, x+22*s, y+170*s), fill=(225,210,170,255), outline=INK+(255,), width=3)
    d.line((x, y, x, y-18*s), fill=INK+(255,), width=4)
    if lit: flame(im, x, y-8, 110*s, 56*s, seed=int(x))

def paper_sheet(im, cx, cy, w, h, ang, burn=0.0, seed=0):
    t = Image.new("RGBA", (w+40, h+40), (0,0,0,0)); d = ImageDraw.Draw(t)
    d.rectangle((20, 20, w+20, h+20), fill=(222,204,160,255), outline=INK+(255,), width=3)
    rnd = random.Random(seed)
    for i in range(9):
        yy = 50 + i*(h-50)//9
        d.line((45, yy, 20+w-45-rnd.randint(0, 80), yy), fill=(60,40,25,255), width=3)
    if burn > 0:
        for k in range(int(8*burn)+1):
            bx, by = rnd.randint(w//2, w+20), rnd.randint(20, h)
            d.ellipse((bx-60*burn, by-60*burn, bx+60*burn, by+60*burn), fill=(20,10,5,255))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(t, (int(cx-t.width/2), int(cy-t.height/2)))

def wig_face(im, cx, cy, s=1.0, crown=False, mood=0, hair=(150,150,150)):
    d = ImageDraw.Draw(im)
    # perruque
    for k in range(-5, 6):
        for r in range(4):
            rr = (230 - r*28)*s
            ox = k*34*s
            d.ellipse((cx+ox-rr*0.34, cy-60*s+r*70*s, cx+ox+rr*0.34, cy+190*s+r*70*s), fill=(120-r*10,112-r*10,100-r*10,255), outline=INK+(255,), width=3)
    # visage
    d.ellipse((cx-105*s, cy-110*s, cx+105*s, cy+135*s), fill=(214,180,140,255), outline=INK+(255,), width=4)
    hatch(d, (cx-100*s, cy-100*s, cx+10*s, cy+130*s), 9, 0.5, (60,30,15,70), 2)
    ey = cy-15*s
    for sx in (-1, 1):
        d.line((cx+sx*52*s-24*s, ey-28*s - mood*6, cx+sx*52*s+24*s, ey-24*s + mood*6*sx), fill=INK+(255,), width=int(6*s))
        d.ellipse((cx+sx*52*s-16*s, ey-10*s, cx+sx*52*s+16*s, ey+10*s), fill=(245,240,225,255), outline=INK+(255,), width=3)
        d.ellipse((cx+sx*52*s-6*s, ey-6*s, cx+sx*52*s+6*s, ey+6*s), fill=INK+(255,))
    d.line((cx, ey, cx-10*s, cy+48*s), fill=INK+(255,), width=int(5*s)); d.line((cx-10*s, cy+48*s, cx+14*s, cy+50*s), fill=INK+(255,), width=int(5*s))
    d.line((cx-46*s, cy+80*s, cx+46*s, cy+80*s - mood*5), fill=INK+(255,), width=int(6*s))
    d.arc((cx-60*s, cy+66*s, cx-8*s, cy+86*s), 180, 360, fill=INK+(255,), width=int(4*s)); d.arc((cx+8*s, cy+66*s, cx+60*s, cy+86*s), 180, 360, fill=INK+(255,), width=int(4*s))
    # corps
    d.polygon([(cx-210*s, cy+520*s), (cx-130*s, cy+170*s), (cx+130*s, cy+170*s), (cx+210*s, cy+520*s)], fill=(30,38,90,255), outline=INK+(255,))
    d.polygon([(cx-60*s, cy+150*s), (cx+60*s, cy+150*s), (cx, cy+300*s)], fill=(235,225,205,255), outline=INK+(255,))
    for k in range(5): d.ellipse((cx-8*s, cy+300*s+k*38*s, cx+8*s, cy+316*s+k*38*s), fill=(190,150,60,255))
    if crown:
        d.polygon([(cx-90*s, cy-40*s), (cx-70*s, cy-150*s), (cx-30*s, cy-85*s), (cx, cy-170*s), (cx+30*s, cy-85*s), (cx+70*s, cy-150*s), (cx+90*s, cy-40*s)], fill=(200,160,50,255), outline=INK+(255,))

def woman(im, cx, cy, s=1.0, fan=True, point=False, dress=(110,20,40)):
    d = ImageDraw.Draw(im)
    d.polygon([(cx-260*s, cy+560*s), (cx-110*s, cy+170*s), (cx+110*s, cy+170*s), (cx+260*s, cy+560*s)], fill=dress+(255,), outline=INK+(255,))
    hatch(d, (cx-250*s, cy+170*s, cx+250*s, cy+560*s), 14, 0.2, (15,5,5,100), 3)
    d.ellipse((cx-170*s, cy+130*s, cx+170*s, cy+215*s), fill=(228,200,165,255), outline=INK+(255,), width=3)
    for k in range(3):
        d.ellipse((cx-120*s+k*10*s, cy-190*s+k*20*s, cx+120*s-k*10*s, cy+60*s), fill=(60-k*10,36-k*6,22,255), outline=INK+(255,), width=3)
    for sx in (-1, 1):
        d.ellipse((cx+sx*95*s-34*s, cy+10*s, cx+sx*95*s+34*s, cy+140*s), fill=(60,36,22,255), outline=INK+(255,), width=3)
    d.ellipse((cx-95*s, cy-100*s, cx+95*s, cy+120*s), fill=(232,206,172,255), outline=INK+(255,), width=4)
    ey = cy-5*s
    for sx in (-1, 1):
        d.line((cx+sx*40*s-20*s, ey-26*s, cx+sx*40*s+20*s, ey-22*s), fill=INK+(255,), width=int(5*s))
        d.ellipse((cx+sx*40*s-13*s, ey-8*s, cx+sx*40*s+13*s, ey+8*s), fill=(245,240,225,255), outline=INK+(255,), width=3)
        d.ellipse((cx+sx*40*s-5*s, ey-5*s, cx+sx*40*s+5*s, ey+5*s), fill=INK+(255,))
    d.line((cx, ey, cx-8*s, cy+42*s), fill=INK+(255,), width=int(4*s)); d.line((cx-8*s, cy+42*s, cx+10*s, cy+44*s), fill=INK+(255,), width=int(4*s))
    d.ellipse((cx-22*s, cy+68*s, cx+22*s, cy+88*s), fill=(160,40,45,255), outline=INK+(255,), width=3)
    if fan:
        fx, fy = cx+170*s, cy+330*s
        for k in range(7):
            a = math.radians(-70 + k*23)
            d.polygon([(fx, fy), (fx+260*s*math.sin(a-0.2), fy-260*s*math.cos(a-0.2)), (fx+260*s*math.sin(a+0.2), fy-260*s*math.cos(a+0.2))], fill=(210+k%2*20, 190, 140, 255), outline=INK+(255,))
    if point:
        d.polygon([(cx-420*s, cy+300*s), (cx-120*s, cy+250*s), (cx-120*s, cy+290*s), (cx-420*s, cy+340*s)], fill=(30,20,15,255))

def figure(im, x, y, s=1.0, col=(12,8,6), hat=False, arms_up=False, kid=False):
    d = ImageDraw.Draw(im)
    if kid: s *= 0.62
    d.ellipse((x-24*s, y-250*s, x+24*s, y-200*s), fill=col+(255,))
    if hat: d.rectangle((x-34*s, y-262*s, x+34*s, y-248*s), fill=col+(255,)); d.rectangle((x-22*s, y-290*s, x+22*s, y-260*s), fill=col+(255,))
    d.polygon([(x-48*s, y), (x-26*s, y-196*s), (x+26*s, y-196*s), (x+48*s, y)], fill=col+(255,))
    if arms_up:
        d.line((x-26*s, y-180*s, x-70*s, y-290*s), fill=col+(255,), width=int(14*s)); d.line((x+26*s, y-180*s, x+70*s, y-290*s), fill=col+(255,), width=int(14*s))

def vials(im, cx, cy, s=1.0, seed=1):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for row in range(3):
        yy = cy - 230*s + row*190*s
        d.rectangle((cx-420*s, yy+100*s, cx+420*s, yy+118*s), fill=(60,38,22,255), outline=INK+(255,), width=3)
        x = cx-390*s
        while x < cx+380*s:
            hh = rnd.randint(70, 130)*s; ww = rnd.randint(30, 52)*s
            col = rnd.choice([(80,130,80,230), (150,50,50,230), (190,160,70,230), (70,90,150,230)])
            d.rounded_rectangle((x, yy+100*s-hh, x+ww, yy+100*s), radius=int(10*s), fill=col, outline=INK+(255,), width=3)
            d.rectangle((x+ww*0.3, yy+100*s-hh-22*s, x+ww*0.7, yy+100*s-hh), fill=(210,190,150,255), outline=INK+(255,), width=2)
            x += ww + rnd.randint(12, 30)*s

def houses(im, y_base, seed=2, lit=True):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    x = -40
    while x < W+40:
        w = rnd.randint(140, 230); h = rnd.randint(260, 560)
        d.polygon([(x, y_base), (x, y_base-h), (x+w/2, y_base-h-90-rnd.randint(0,50)), (x+w, y_base-h), (x+w, y_base)], fill=(14,9,7,255), outline=(40,26,18,255))
        for wx in range(x+24, x+w-30, 52):
            for wy in range(y_base-h+30, y_base-40, 80):
                if lit and rnd.random() < 0.28: d.rectangle((wx, wy, wx+22, wy+36), fill=(240,170,60,255))
                else: d.rectangle((wx, wy, wx+22, wy+36), fill=(34,22,16,255))
        x += w - 6

def stake(im, cx, base_y, seed=0, big=True):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    d.polygon([(cx-230, base_y), (cx-60, base_y-190), (cx+60, base_y-190), (cx+230, base_y)], fill=(70,44,24,255), outline=INK+(255,))
    hatch(d, (cx-230, base_y-190, cx+230, base_y), 10, 0.5, (15,8,4,120), 3)
    d.rectangle((cx-14, base_y-560, cx+14, base_y-180), fill=(48,30,18,255), outline=INK+(255,))
    figure(im, cx, base_y-175, 1.0, col=(8,6,5))
    flame(im, cx, base_y-60, 360, 520, seed=seed+3)
    flame(im, cx-140, base_y-30, 220, 240, seed=seed+5)
    flame(im, cx+150, base_y-30, 240, 260, seed=seed+7)

def smoke(im, cx, y, seed=0):
    rnd = random.Random(seed); g = Image.new("RGBA", im.size, (0,0,0,0)); d = ImageDraw.Draw(g)
    for i in range(14):
        r = 70 + i*16; d.ellipse((cx-r+rnd.randint(-70,70), y-i*80-r, cx+r+rnd.randint(-70,70), y-i*80+r), fill=(30,26,24,70))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(28)))

def make(name, fn, seed, dark=0.0, warm=(70,46,30), ttl=None, fil=True, extra=None):
    im = paper(seed, dark, warm)
    fn(im)
    im = vignette(im)
    if ttl: ttl(im)
    if extra: extra(im)
    im.convert("RGB").save(f"/home/claude/work012/img/{name}.png")

S = {}
# 1 cassette + bougie, hook
def s01(im):
    cassette(im, 470, 1040, 1.15, lit=False); candle(im, 800, 1000, 1.4)
def t01(im):
    title(im, [("ELLE VOULAIT", CREAM), ("TE TUER ?", RED)], y=470, size=132)
make("s01", s01, 1, ttl=t01, fil=False)
# 2 papiers en feu, hook
def s02(im):
    paper_sheet(im, 360, 1080, 380, 520, -14, 0.8, 1); paper_sheet(im, 560, 1010, 380, 520, 9, 0.5, 2); paper_sheet(im, 460, 1090, 380, 520, -3, 0.2, 3)
    flame(im, 330, 1260, 420, 360, 11); flame(im, 600, 1230, 460, 420, 12); flame(im, 470, 1290, 560, 520, 13)
def t02(im):
    title(im, [("TU BRÛLES", CREAM), ("TOUT", RED)], y=470, size=140)
make("s02", s02, 2, dark=0.15, ttl=t02, fil=False)
# 3 Louis XIV
def s03(im): wig_face(im, 470, 880, 1.15, crown=True)
make("s03", s03, 3)
# 4 Paris de nuit
def s04(im):
    glow(im, (800, 700), 260, (230,200,130), 0.6)
    d = ImageDraw.Draw(im); d.ellipse((740, 640, 860, 760), fill=(240,225,180,255))
    houses(im, 1260, 5)
make("s04", s04, 4, dark=0.25)
# 5 fioles
def s05(im): vials(im, 470, 960, 1.0, 7)
make("s05", s05, 5)
# 6 chambre ardente
def s06(im):
    d = ImageDraw.Draw(im); d.rectangle((0, 560, W, 1300), fill=(8,6,6,255))
    for x in (170, 470, 770): 
        d.rectangle((x-8, 760, x+8, 900), fill=(50,34,22,255)); flame(im, x, 760, 130, 70, seed=x)
    d.rectangle((120, 1080, 820, 1120), fill=(60,38,22,255), outline=INK+(255,)); d.rectangle((140, 1120, 800, 1260), fill=(40,26,16,255))
    for x in (230, 380, 530, 680): figure(im, x, 1090, 0.95, col=(0,0,0), hat=True)
def t06(im): 
    title(im, [("À L'ARSENAL", CREAM), ("SALLE TENDUE DE NOIR", RED)], y=440, size=84)
make("s06", s06, 6, dark=0.5, ttl=t06)
# 7 accusés (compteur)
def s07(im):
    d = ImageDraw.Draw(im)
    for r in range(4):
        for k in range(9): figure(im, 100+k*100+(r%2)*40, 1030+r*70, 0.55+0.08*r, col=(14,10,8))
def t07(im):
    title(im, [("442", RED), ("ACCUSÉS", CREAM)], y=440, size=104)
make("s07", s07, 7, ttl=t07)
# 8 Place de Grève
def s08(im):
    houses(im, 1180, 9, lit=False)
    stake(im, 470, 1210, 4); smoke(im, 470, 880, 2)
    for k in range(12): figure(im, 40+k*90, 1330, 0.7, col=(5,3,2), arms_up=(k%3==0))
def t08(im): title(im, [("FACE À L'HÔTEL DE VILLE", CREAM)], y=440, size=76)
make("s08", s08, 8, dark=0.35, warm=(78,40,24), ttl=t08)
# 9 la fille
def s09(im):
    woman(im, 330, 830, 0.8, fan=False, dress=(60,60,70))
    d = ImageDraw.Draw(im); d.rectangle((120, 1230, 830, 1260), fill=(60,38,22,255))
    figure(im, 740, 1230, 1.05, col=(10,8,6), hat=True)
    paper_sheet(im, 600, 1200, 170, 120, 8, 0, 4); 
    d.line((730, 1090, 650, 1190), fill=(10,8,6,255), width=9)
def t09(im): title(im, [("SA FILLE", CREAM), ("MARIE-MARGUERITE", RED)], y=440, size=92)
make("s09", s09, 9, ttl=t09)
# 10 Montespan
def s10(im): woman(im, 420, 800, 1.05, fan=True)
def t10(im): title(im, [("FAVORITE DU ROI", CREAM), ("DEPUIS 1667", RED)], y=440, size=92)
make("s10", s10, 10, ttl=t10)
# 11 enfants
def s11(im):
    for k in range(7): figure(im, 100+k*120, 1230 - (k%2)*30, 1.15, col=(18,12,10), kid=True)
    for k in range(7): glow(im, (100+k*120, 1060), 36, (230,190,90), 0.35)
def t11(im): title(im, [("7 ENFANTS", CREAM), ("LÉGITIMÉS", RED)], y=440, size=96)
make("s11", s11, 11, ttl=t11)
# 12 doigt pointé / accusés
def s12(im):
    woman(im, 470, 830, 1.0, fan=True, point=True)
    d = ImageDraw.Draw(im)
    for k in range(4): figure(im, 120+k*60, 1330, 0.9, col=(4,3,2), arms_up=True)
def t12(im): title(im, [("AUCUNE PREUVE", RED), ("SEULEMENT DES AVEUX", CREAM)], y=440, size=84)
make("s12", s12, 12, dark=0.1, ttl=t12)
# 13 question
def s13(im):
    wig_face(im, 470, 900, 1.1, crown=True, mood=-1)
    d = ImageDraw.Draw(im); f = font(420); d.text((570, 520), "?", font=f, fill=RED+(210,), stroke_width=10, stroke_fill=(0,0,0))
make("s13", s13, 13, dark=0.1)
# 14 chambre fermée
def s14(im):
    d = ImageDraw.Draw(im)
    d.rectangle((250, 640, 700, 1260), fill=(52,32,18,255), outline=INK+(255,), width=6)
    d.rectangle((280, 670, 670, 1230), outline=(30,18,10,255), width=5); hatch(d, (250,640,700,1260), 14, 0.0, (10,5,2,110), 4)
    d.ellipse((620, 960, 664, 1004), fill=(190,160,60,255), outline=INK+(255,), width=3)
    paper_sheet(im, 470, 940, 300, 210, -4, 0, 5); stamp_red(im, "FERMÉE", 470, 940, 62, -10)
def t14(im): title(im, [("21 JUILLET 1682", CREAM), ("LETTRE DE CACHET", RED)], y=440, size=92)
make("s14", s14, 14, ttl=t14)
# 15 cassette scellée
def s15(im): cassette(im, 470, 960, 1.2, seal=True); glow(im, (470,960), 380, (255,120,30), 0.15)
make("s15", s15, 15, dark=0.2)
# 16 papiers qui brûlent — montée
def s16(im):
    d = ImageDraw.Draw(im)
    for k, (cx, cy, a) in enumerate([(300, 1120, -18), (470, 1080, 4), (640, 1130, 20), (470, 1210, -8)]): paper_sheet(im, cx, cy, 340, 470, a, 0.6+0.1*k, k)
    for k in range(6): flame(im, 220+k*130, 1290 - (k%2)*60, 330+40*(k%3), 300, seed=k)
def t16(im): title(im, [("1709 : LA REYNIE", CREAM), ("EST MORT", RED)], y=440, size=92)
make("s16", s16, 16, dark=0.3, warm=(80,40,22), ttl=t16)
# 17 trentaine d'exécutés (silhouettes de poteaux)
def s17(im):
    d = ImageDraw.Draw(im)
    for k in range(10):
        x = 70 + k*100; d.rectangle((x-6, 870, x+6, 1230), fill=(24,16,10,255)); figure(im, x, 1230, 0.55, col=(6,4,3))
    houses(im, 900, 21, lit=False)
make("s17", s17, 17, dark=0.45)
# 18 Montespan NI CONDAMNÉE NI BLANCHIE
def s18(im): woman(im, 470, 820, 1.0, fan=True, dress=(70,60,70))
def t18(im): title(im, [("NI CONDAMNÉE", RED), ("NI BLANCHIE", CREAM)], y=440, size=96)
make("s18", s18, 18, dark=0.25, ttl=t18)
# 19 aveux vrais ou arrachés
def s19(im):
    d = ImageDraw.Draw(im); d.rectangle((260, 700, 680, 1280), fill=(46,30,18,255), outline=INK+(255,), width=5)
    paper_sheet(im, 470, 960, 260, 340, 3, 0, 8); stamp_red(im, "?", 470, 950, 200, -6)
def t19(im): title(im, [("AVEUX : VRAIS", CREAM), ("OU ARRACHÉS ?", RED)], y=440, size=92)
make("s19", s19, 19, ttl=t19)
# 20 cendres
def s20(im):
    d = ImageDraw.Draw(im); rnd = random.Random(3)
    for k in range(140):
        x, y = rnd.randint(60, 900), rnd.randint(700, 1240); r = rnd.randint(4, 18)
        d.ellipse((x, y, x+r*2, y+r), fill=(14+rnd.randint(0,30),10,8,255))
    paper_sheet(im, 470, 1100, 340, 220, -6, 1.0, 11); flame(im, 470, 1180, 170, 150, seed=5)
make("s20", s20, 20, dark=0.4)
# 21 question finale (titre seul)
def s21(im):
    candle(im, 170, 1250, 1.2)
def t21(im): title(im, [("TA FAVORITE…", CREAM), ("OU LA VÉRITÉ ?", RED)], y=520, size=104)
make("s21", s21, 21, dark=0.55, ttl=t21, fil=False)
# 22 boucle cassette
make("s22", lambda im: (cassette(im, 470, 1040, 1.15, lit=False), candle(im, 800, 1000, 1.4)), 22, dark=0.1)
print("ok")

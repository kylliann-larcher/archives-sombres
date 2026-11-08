#!/usr/bin/env python3
"""Video 012 v2 : rendu image par image (calques animes, flammes vivantes, secousses, flashs, titres pop)."""
import json, math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = "/home/claude/work012"
src = open(f"{HERE}/gen_images.py", encoding="utf-8").read().split("S = {}")[0]
exec(src)  # fonctions de dessin (paper, flame, cassette, wig_face, woman, figure, ...)

FPS = 30
WD = json.load(open(f"{HERE}/words2.json"))
WORDS = WD["words"]; DUR = WD["dur"]
def T(i): return WORDS[i]["start"] if i < len(WORDS) else DUR

BI = Image.BILINEAR
VIG = None
def vignette_mask():
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W/2) / (W*0.72))**2 + ((yy - H/2) / (H*0.62))**2)
    m = np.clip(1 - 0.5*d**2.2, 0.2, 1)
    return Image.fromarray((m*255).astype(np.uint8)).convert("RGB")

# ---------- flammes vivantes ----------
FC = {}
def flame_set(h, wd, n=8):
    key = (h, wd)
    if key not in FC:
        pad = int(h*1.1); L = []
        for s in range(n):
            tmp = Image.new("RGBA", (int(wd + 2*pad), int(h + 2*pad)), (0,0,0,0))
            flame(tmp, tmp.width//2, pad + h, h, wd, seed=s*7 + 1)
            L.append(tmp)
        FC[key] = (L, pad)
    return FC[key]

class Flame:
    def __init__(self, x, base_y, h, wd, on=None, off=None, k0=0.0, ramp=0.4, kmax=1.0):
        self.x, self.y, self.h, self.w = x, base_y, int(h), int(wd)
        self.on, self.off, self.ramp, self.kmax = on, off, ramp, kmax
    def draw(self, world, t, fr):
        if self.on is not None and t < self.on: return
        k = self.kmax
        if self.on is not None: k *= min(1.0, (t - self.on)/self.ramp)
        if self.off is not None:
            if t > self.off: return
            k *= max(0.0, min(1.0, (self.off - t)/0.5))
        if k < 0.05: return
        L, pad = flame_set(self.h, self.w)
        im = L[(fr//2 + int(self.x)) % len(L)]
        wob = 1.0 + 0.06*math.sin(fr*0.9 + self.x)
        sc = k*wob
        if abs(sc - 1) > 0.02:
            im = im.resize((max(1, int(im.width*sc)), max(1, int(im.height*sc))), BI)
        bx = (pad + self.h)*sc
        world.paste(im, (int(self.x - im.width/2), int(self.y - bx)), im)

class Spr:
    def __init__(self, draw_fn, pivot, anim=None, appear=None, vanish=None):
        L = Image.new("RGBA", (W, H), (0,0,0,0)); draw_fn(L)
        x0, y0, x1, y1 = L.getbbox()
        px, py = pivot
        hx = max(px - x0, x1 - px) + 4; hy = max(py - y0, y1 - py) + 4
        c = Image.new("RGBA", (int(2*hx), int(2*hy)), (0,0,0,0))
        c.paste(L.crop((x0, y0, x1, y1)), (int(hx - (px - x0)), int(hy - (py - y0))))
        self.img, self.pivot, self.anim, self.appear, self.vanish = c, pivot, anim, appear, vanish
    def draw(self, world, t):
        if self.appear is not None and t < self.appear: return
        if self.vanish is not None and t > self.vanish: return
        dx, dy, rot, sc, al = self.anim(t) if self.anim else (0, 0, 0, 1, 1)
        if al <= 0.01: return
        im = self.img
        if abs(sc - 1) > 0.005: im = im.resize((max(1, int(im.width*sc)), max(1, int(im.height*sc))), BI)
        if abs(rot) > 0.05: im = im.rotate(rot, resample=BI)
        if al < 0.99:
            im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v*al)))
        world.paste(im, (int(self.pivot[0] + dx - im.width/2), int(self.pivot[1] + dy - im.height/2)), im)

def breathe(t, amp=0.012, rot=1.2, bob=6, ph=0.0):
    return (0, bob*math.sin(t*2.2 + ph), rot*math.sin(t*1.3 + ph), 1 + amp*math.sin(t*2.2 + ph), 1)

def pop(t0, dur=0.22, over=1.5, fade=0.0):
    def f(t):
        a = t - t0
        s = 1.0 if a >= dur else over - (over - 1.0)*max(0, a)/dur
        return (0, 0, 0, s, min(1.0, max(0, a)/0.06) if fade == 0 else 1)
    return f

# ---------- decors (fond sans element anime) ----------
def bg_paper(seed, dark=0.0, warm=(70, 46, 30)): return paper(seed, dark, warm)

def mk_cassette_bg(lit=False):
    im = bg_paper(1)
    cassette(im, 470, 1040, 1.15, lit=False); candle(im, 800, 1000, 1.4, lit=False)
    return im

def shot_defs():
    S = []
    # --- 0 : hook 1 cassette + bougie
    S.append(dict(name="hook1", a=0, b=7, bg=mk_cassette_bg(),
        flames=[Flame(800, 992, 154, 78)],
        sprites=[], focus=[(470, 1040), (800, 1000)],
        titles=[("ELLE VOULAIT", CREAM, 132, 0.15, 470), ("TE TUER ?", RED, 132, T(5), 625)]))
    # --- 1 : hook 2 papiers en feu
    def bgB():
        im = bg_paper(2, 0.15)
        paper_sheet(im, 360, 1080, 380, 520, -14, 0.8, 1); paper_sheet(im, 560, 1010, 380, 520, 9, 0.5, 2); paper_sheet(im, 460, 1090, 380, 520, -3, 0.2, 3)
        return im
    S.append(dict(name="hook2", a=7, b=12, bg=bgB(),
        flames=[Flame(330, 1260, 420, 360, on=T(7), ramp=0.5, kmax=0.9), Flame(600, 1230, 460, 420, on=T(7)+0.1, ramp=0.5), Flame(470, 1290, 560, 520, on=T(9), ramp=0.25)],
        sprites=[], focus=[(470, 1100), (470, 1200)],
        titles=[("TU BRÛLES", CREAM, 140, T(8), 470), ("TOUT", RED, 140, T(11), 635)]))
    # --- 2 : Louis XIV
    louis = Spr(lambda L: wig_face(L, 470, 880, 1.15, crown=True), (470, 1250), lambda t: breathe(t, 0.01, 1.4, 7))
    S.append(dict(name="louis", a=12, b=16, bg=bg_paper(3), flames=[], sprites=[louis], focus=[(470, 900), (470, 820)], titles=[]))
    # --- 3 : Paris de nuit + brume verte
    def bgC():
        im = bg_paper(4, 0.25); glow(im, (800, 700), 260, (230, 200, 130), 0.6)
        ImageDraw.Draw(im).ellipse((740, 640, 860, 760), fill=(240, 225, 180, 255)); houses(im, 1260, 5)
        return im
    mist = Spr(lambda L: glow(L, (300, 1180), 300, (90, 200, 90), 0.5), (300, 1180), lambda t: (60*math.sin(t*0.8), -20*math.sin(t*0.6), 0, 1 + 0.08*math.sin(t*1.1), 0.6), appear=T(19))
    S.append(dict(name="paris", a=16, b=22, bg=bgC(), flames=[], sprites=[mist], focus=[(700, 800), (300, 1100)], titles=[]))
    # --- 4 : fioles (voyantes, apothicaires)
    def bgD():
        im = bg_paper(5); vials(im, 470, 960, 1.0, 7); return im
    S.append(dict(name="vials1", a=22, b=26, bg=bgD(), flames=[], sprites=[], focus=[(250, 800), (700, 1100)], titles=[]))
    # --- 5 : nobles soupconnes de vendre la mort (rouge)
    redglow = Spr(lambda L: glow(L, (470, 960), 420, (200, 20, 20), 0.55), (470, 960), lambda t: (0, 0, 0, 1 + 0.05*math.sin(t*6), 0.2 + 0.8*min(1, max(0, (t - T(31))/0.6))), appear=T(26))
    S.append(dict(name="vials2", a=26, b=34, bg=bgD(), flames=[], sprites=[redglow], focus=[(470, 960), (300, 900), (650, 1050)], titles=[]))
    # --- 6 : tribunal (Chambre ardente)
    def bgE():
        im = bg_paper(6, 0.5); d = ImageDraw.Draw(im); d.rectangle((0, 560, W, 1300), fill=(8, 6, 6, 255))
        for x in (170, 470, 770): d.rectangle((x-8, 760, x+8, 900), fill=(50, 34, 22, 255))
        d.rectangle((120, 1080, 820, 1120), fill=(60, 38, 22, 255), outline=INK+(255,)); d.rectangle((140, 1120, 800, 1260), fill=(40, 26, 16, 255))
        for x in (230, 380, 530, 680): figure(im, x, 1090, 0.95, col=(0, 0, 0), hat=True)
        return im
    S.append(dict(name="tribunal", a=34, b=43, bg=bgE(),
        flames=[Flame(170, 760, 130, 70), Flame(470, 760, 130, 70), Flame(770, 760, 130, 70)],
        sprites=[], focus=[(470, 900), (170, 780), (470, 1050), (770, 780)],
        titles=[("À L'ARSENAL", CREAM, 84, T(38), 440), ("SALLE TENDUE DE NOIR", RED, 84, T(41), 540)]))
    # --- 7 : 442 accuses
    def bgF():
        im = bg_paper(7)
        for r in range(4):
            for k in range(9): figure(im, 100 + k*100 + (r % 2)*40, 1030 + r*70, 0.55 + 0.08*r, col=(14, 10, 8))
        return im
    S.append(dict(name="accuses", a=43, b=49, bg=bgF(), flames=[], sprites=[], focus=[(470, 1100), (200, 1100), (700, 1150)],
        titles=[("#COUNT#", RED, 104, T(44), 440), ("ACCUSÉS", CREAM, 104, T(48), 560)], count=(T(45), T(48), 442)))
    # --- 8 : Place de Greve - le bucher
    def bgG():
        im = bg_paper(8, 0.35, (78, 40, 24)); houses(im, 1180, 9, lit=False)
        d = ImageDraw.Draw(im); cx, base_y = 470, 1210
        d.polygon([(cx-230, base_y), (cx-60, base_y-190), (cx+60, base_y-190), (cx+230, base_y)], fill=(70, 44, 24, 255), outline=INK+(255,))
        hatch(d, (cx-230, base_y-190, cx+230, base_y), 10, 0.5, (15, 8, 4, 120), 3)
        d.rectangle((cx-14, base_y-560, cx+14, base_y-180), fill=(48, 30, 18, 255), outline=INK+(255,)); figure(im, cx, base_y-175, 1.0, col=(8, 6, 5))
        smoke(im, 470, 880, 2)
        for k in range(12): figure(im, 40 + k*90, 1330, 0.7, col=(5, 3, 2), arms_up=(k % 3 == 0))
        return im
    on = T(55)
    S.append(dict(name="greve", a=49, b=66, bg=bgG(),
        flames=[Flame(470, 1150, 360, 520, on=on, ramp=0.5), Flame(330, 1180, 220, 240, on=on+0.15, ramp=0.5), Flame(620, 1180, 240, 260, on=on+0.25, ramp=0.5)],
        sprites=[], focus=[(470, 1000), (470, 1300), (300, 1250), (470, 900), (700, 1300)],
        titles=[("FACE À L'HÔTEL DE VILLE", CREAM, 76, T(61), 440)]))
    # --- 9 : la fille
    def d_daughter(L): woman(L, 330, 830, 0.8, fan=False, dress=(60, 60, 70))
    daughter = Spr(d_daughter, (330, 1100), lambda t: (0, 4*math.sin(t*2.4), 1.2*math.sin(t*1.7), 1, 1))
    def d_clerk(L): figure(L, 740, 1230, 1.05, col=(10, 8, 6), hat=True)
    clerk = Spr(d_clerk, (740, 1230), lambda t: (0, 3*math.sin(t*3), 0, 1, 1))
    def d_quill(L): ImageDraw.Draw(L).line((730, 1090, 650, 1190), fill=(10, 8, 6, 255), width=9)
    quill = Spr(d_quill, (730, 1090), lambda t: (0, 0, 10*math.sin(t*14), 1, 1))
    def bgH():
        im = bg_paper(9); ImageDraw.Draw(im).rectangle((120, 1230, 830, 1260), fill=(60, 38, 22, 255)); paper_sheet(im, 600, 1200, 170, 120, 8, 0, 4); return im
    S.append(dict(name="fille", a=66, b=75, bg=bgH(), flames=[], sprites=[daughter, clerk, quill], focus=[(330, 950), (740, 1150), (500, 1100)],
        titles=[("SA FILLE", CREAM, 92, T(67), 440), ("MARIE-MARGUERITE", RED, 92, T(70), 548)]))
    # --- 10 : Montespan
    mont = Spr(lambda L: woman(L, 420, 800, 1.05, fan=False), (420, 1100), lambda t: breathe(t, 0.012, 1.0, 5, 1.0))
    def d_fan(L):
        s, cx, cy = 1.05, 420, 800; fx, fy = cx + 170*s, cy + 330*s; d = ImageDraw.Draw(L)
        for k in range(7):
            a = math.radians(-70 + k*23)
            d.polygon([(fx, fy), (fx + 260*s*math.sin(a-0.2), fy - 260*s*math.cos(a-0.2)), (fx + 260*s*math.sin(a+0.2), fy - 260*s*math.cos(a+0.2))], fill=(210 + k % 2*20, 190, 140, 255), outline=INK+(255,))
    fan = Spr(d_fan, (420 + 170*1.05, 800 + 330*1.05), lambda t: (0, 0, 9*math.sin(t*5.5), 1, 1))
    S.append(dict(name="montespan", a=75, b=80, bg=bg_paper(10), flames=[], sprites=[mont, fan], focus=[(420, 850), (420, 800)],
        titles=[("FAVORITE DU ROI", CREAM, 92, T(78), 440), ("DEPUIS 1667", RED, 92, T(79), 548)]))
    # --- 11 : 7 enfants
    kids = []
    for k in range(7):
        ap = T(80) + 0.12 + k*(T(84) - T(80) - 0.15)/7
        kids.append(Spr(lambda L, k=k: figure(L, 100 + k*120, 1230 - (k % 2)*30, 1.15, col=(18, 12, 10), kid=True), (100 + k*120, 1180), pop(ap, 0.2, 1.4), appear=ap))
        kids.append(Spr(lambda L, k=k: glow(L, (100 + k*120, 1060), 36, (230, 190, 90), 0.5), (100 + k*120, 1060), lambda t: (0, 0, 0, 1, 0.5 + 0.5*math.sin(t*5)), appear=ap))
    S.append(dict(name="kids", a=80, b=85, bg=bg_paper(11), flames=[], sprites=kids, focus=[(470, 1150), (150, 1150), (700, 1150)],
        titles=[("7 ENFANTS", CREAM, 96, T(81), 440), ("LÉGITIMÉS", RED, 96, T(84), 555)]))
    # --- 12 : le doigt pointe, accuses qui hurlent
    mont2 = Spr(lambda L: woman(L, 470, 830, 1.0, fan=True, point=True), (470, 1100), lambda t: breathe(t, 0.01, 1.0, 4))
    acc = []
    for k in range(4):
        acc.append(Spr(lambda L, k=k: figure(L, 120 + k*60, 1330, 0.9, col=(4, 3, 2), arms_up=True), (120 + k*60, 1330), lambda t, k=k: (3*math.sin(t*9 + k), 5*abs(math.sin(t*7 + k*1.3)), 3*math.sin(t*8 + k), 1, 1)))
    S.append(dict(name="point", a=85, b=99, bg=bg_paper(12, 0.1), flames=[], sprites=[mont2] + acc, focus=[(470, 950), (150, 1250), (470, 1100), (350, 1000)],
        titles=[("AUCUNE PREUVE", RED, 84, T(92), 440), ("SEULEMENT DES AVEUX", CREAM, 84, T(96), 540)]))
    # --- 13 : Alors, tu fais quoi ? (Louis + ?)
    louis2 = Spr(lambda L: wig_face(L, 470, 900, 1.1, crown=True, mood=-1), (470, 1250), lambda t: breathe(t, 0.02, 2.0, 5))
    q = Spr(lambda L: ImageDraw.Draw(L).text((570, 520), "?", font=font(420), fill=RED+(230,), stroke_width=10, stroke_fill=(0, 0, 0)), (680, 700), pop(T(102), 0.25, 2.0), appear=T(102))
    S.append(dict(name="quoi", a=99, b=103, bg=bg_paper(13, 0.1), flames=[], sprites=[louis2, q], focus=[(470, 900), (500, 800)], titles=[]))
    # --- 14 : porte fermee 1682 + tampon
    def bgI():
        im = bg_paper(14); d = ImageDraw.Draw(im)
        d.rectangle((250, 640, 700, 1260), fill=(52, 32, 18, 255), outline=INK+(255,), width=6); d.rectangle((280, 670, 670, 1230), outline=(30, 18, 10, 255), width=5)
        hatch(d, (250, 640, 700, 1260), 14, 0.0, (10, 5, 2, 110), 4); d.ellipse((620, 960, 664, 1004), fill=(190, 160, 60, 255), outline=INK+(255,), width=3)
        paper_sheet(im, 470, 940, 300, 210, -4, 0, 5); return im
    st = Spr(lambda L: stamp_red(L, "FERMÉE", 470, 940, 62, -10), (470, 940), pop(T(109), 0.12, 2.6), appear=T(109))
    S.append(dict(name="porte", a=103, b=111, bg=bgI(), flames=[], sprites=[st], focus=[(470, 940), (470, 800), (600, 1000)],
        titles=[("21 JUILLET 1682", CREAM, 92, T(106), 440), ("LETTRE DE CACHET", RED, 92, T(108), 548)]))
    # --- 15 : dossiers -> cassette
    def bgJ():
        im = bg_paper(15, 0.2); cassette(im, 470, 960, 1.2, seal=False); return im
    sheets = []
    for k in range(5):
        t0 = T(112) + k*(T(117) - T(112) - 0.4)/5
        sheets.append(Spr(lambda L, k=k: paper_sheet(L, 470, 960, 260, 180, -10 + k*5, 0, k), (470, 960), lambda t, t0=t0: (0, -900*(1 - min(1, max(0, (t - t0)/0.45)))**2 if t >= t0 else -900, 6*math.sin(t*3), 1 - 0.3*min(1, max(0, (t - t0 - 0.4)/0.1)), 1 if t < t0 + 0.5 else 0), appear=t0 - 0.01, vanish=t0 + 0.55))
    seal = Spr(lambda L: ImageDraw.Draw(L).ellipse((602 - 34, 978 - 34, 602 + 34, 978 + 34), fill=(170, 20, 20, 255), outline=(70, 5, 5, 255), width=4), (602, 978), pop(T(117), 0.12, 2.5), appear=T(117))
    S.append(dict(name="cassette", a=111, b=118, bg=bgJ(), flames=[], sprites=sheets + [seal], focus=[(470, 960), (600, 960), (470, 900)], titles=[]))
    # --- 16 : 1709 : la bougie met le feu
    def bgK():
        im = bg_paper(16, 0.3, (80, 40, 22))
        for k, (cx, cy, a) in enumerate([(300, 1120, -18), (470, 1080, 4), (640, 1130, 20), (470, 1210, -8)]): paper_sheet(im, cx, cy, 340, 470, a, 0.15 + 0.05*k, k)
        return im
    cand = Spr(lambda L: candle(L, 800, 800, 1.3, lit=False), (800, 900), lambda t: (-330*min(1, max(0, (t - T(118))/(T(123) - T(118)))), 280*min(1, max(0, (t - T(118))/(T(123) - T(118)))), 0, 1, 1), vanish=T(124))
    ig = T(123)
    fl16 = [Flame(220 + k*130, 1290 - (k % 2)*60, 330 + 40*(k % 3), 300, on=ig + 0.04*k, ramp=0.3) for k in range(6)]
    S.append(dict(name="feu1709", a=118, b=128, bg=bgK(), flames=fl16, sprites=[cand], focus=[(470, 1150), (800, 900), (470, 1250)],
        titles=[("1709 : LA REYNIE", CREAM, 92, T(120), 440), ("EST MORT", RED, 92, T(123), 548)], candle_flame=(T(118), ig)))
    # --- 17 : trentaine d'executes
    def bgL():
        im = bg_paper(17, 0.45); houses(im, 900, 21, lit=False); return im
    stk = []
    for k in range(10):
        ap = T(128) + 0.1 + k*(T(135) - T(128) - 0.8)/10
        def dd(L, k=k):
            x = 70 + k*100; ImageDraw.Draw(L).rectangle((x-6, 870, x+6, 1230), fill=(24, 16, 10, 255)); figure(L, x, 1230, 0.55, col=(6, 4, 3))
        stk.append(Spr(dd, (70 + k*100, 1100), pop(ap, 0.18, 1.3), appear=ap))
    S.append(dict(name="executes", a=128, b=135, bg=bgL(), flames=[], sprites=stk, focus=[(470, 1100), (200, 1100), (800, 1100)], titles=[]))
    # --- 18 : jamais jugee
    m3 = Spr(lambda L: woman(L, 470, 820, 1.0, fan=True, dress=(70, 60, 70)), (470, 1100), lambda t: breathe(t, 0.01, 0.8, 4, 2.0))
    S.append(dict(name="jamais", a=135, b=140, bg=bg_paper(18, 0.25), flames=[], sprites=[m3], focus=[(470, 900), (470, 800)],
        titles=[("NI CONDAMNÉE", RED, 96, T(137), 440), ("NI BLANCHIE", CREAM, 96, T(139), 555)]))
    # --- 19 : aveux ?
    def bgM():
        im = bg_paper(19); ImageDraw.Draw(im).rectangle((260, 700, 680, 1280), fill=(46, 30, 18, 255), outline=INK+(255,), width=5)
        paper_sheet(im, 470, 960, 260, 340, 3, 0, 8); return im
    qs = Spr(lambda L: stamp_red(L, "?", 470, 950, 200, -6), (470, 950), lambda t: (0, 0, 5*math.sin(t*4), 1 + 0.07*math.sin(t*6), 1))
    S.append(dict(name="aveux", a=140, b=150, bg=bgM(), flames=[], sprites=[qs], focus=[(470, 950), (470, 850), (470, 1100)],
        titles=[("AVEUX : VRAIS", CREAM, 92, T(144), 440), ("OU ARRACHÉS ?", RED, 92, T(146), 548)]))
    # --- 20 : la verite a brule (cendres)
    def bgN():
        im = bg_paper(20, 0.4); d = ImageDraw.Draw(im); rnd = random.Random(3)
        for k in range(140):
            x, y = rnd.randint(60, 900), rnd.randint(700, 1240); r = rnd.randint(4, 18); d.ellipse((x, y, x+r*2, y+r), fill=(14 + rnd.randint(0, 30), 10, 8, 255))
        paper_sheet(im, 470, 1100, 340, 220, -6, 1.0, 11); return im
    S.append(dict(name="cendres", a=150, b=157, bg=bgN(), flames=[Flame(470, 1180, 190, 170, on=T(152), ramp=0.4, off=T(157) - 0.2)], sprites=[], focus=[(470, 1100), (470, 1000)], titles=[]))
    # --- 21 : question finale
    def bgO():
        im = bg_paper(21, 0.55); candle(im, 170, 1250, 1.2, lit=False); return im
    S.append(dict(name="question", a=157, b=170, bg=bgO(), flames=[Flame(170, 1242, 132, 67)], sprites=[], focus=[(170, 1200), (470, 1000)],
        titles=[("TA FAVORITE…", CREAM, 104, T(162), 520), ("OU LA VÉRITÉ ?", RED, 104, T(167), 645)]))
    # --- 22 : boucle
    S.append(dict(name="boucle", a=170, b=len(WORDS), bg=mk_cassette_bg(), flames=[Flame(800, 992, 154, 78)], sprites=[], focus=[(470, 1040), (800, 1000)], titles=[]))
    return S

IMPACTS = [(3, 14, (255, 255, 255)), (9, 24, (255, 170, 60)), (11, 16, None), (15, 10, None), (21, 6, (120, 255, 120)), (33, 14, (200, 30, 30)), (41, 10, None),
           (47, 14, None), (56, 24, (255, 170, 60)), (77, 18, (200, 30, 30)), (84, 8, None), (102, 14, (255, 255, 255)), (109, 22, (255, 255, 255)), (117, 14, None),
           (124, 28, (255, 170, 60)), (134, 18, None), (139, 22, (200, 30, 30)), (153, 14, (255, 170, 60)), (169, 10, None)]

TITLE_CACHE = {}
def title_layer(text, col, size):
    key = (text, col, size)
    if key not in TITLE_CACHE:
        sz = size
        while font(sz).getlength(text) > 800 and sz > 40: sz -= 3
        f = font(sz); w = int(f.getlength(text)) + 40; h = int(sz*1.4)
        L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(L).text((20, 8), text, font=f, fill=col + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
        TITLE_CACHE[key] = L
    return TITLE_CACHE[key]

def camera(world, t, rel, dur, focus, shot_idx, shake):
    # coupe toutes les <= 1,9 s : alterne plan large / plan serre
    nchunk = max(1, int(math.ceil(dur/1.9)))
    ch = min(nchunk - 1, int(rel/(dur/nchunk)))
    t0 = ch*dur/nchunk; t1 = (ch + 1)*dur/nchunk
    p = (rel - t0)/max(1e-6, t1 - t0)
    fx, fy = focus[ch % len(focus)]
    if ch % 2 == 0: z0, z1 = 1.0, 1.1; fx, fy = (W/2, H/2)
    else: z0, z1 = 1.28, 1.38
    if shot_idx in (0, 1) and ch == 0: z0, z1 = 1.05, 1.18; fx, fy = focus[0]
    z = z0 + (z1 - z0)*p
    cx = fx + shake[0]; cy = fy + shake[1]
    vw, vh = W/z, H/z
    cx = min(max(cx, vw/2), W - vw/2); cy = min(max(cy, vh/2), H - vh/2)
    box = (cx - vw/2, cy - vh/2, cx + vw/2, cy + vh/2)
    return world.transform((W, H), Image.EXTENT, box, resample=BI)

def render_shot(args):
    idx, outpath = args
    S = shot_defs()[idx]
    ta, tb = T(S["a"]), (T(S["b"]) if S["b"] < len(WORDS) else DUR)
    if S["a"] == 0: ta = 0.0
    fa, fb = int(round(ta*FPS)), int(round(tb*FPS))
    if idx == len(shot_defs()) - 1: fb = int(round(DUR*FPS))
    vig = vignette_mask()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", outpath]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    dur = max((fb - fa)/FPS, 0.1)
    for fr in range(fa, fb):
        t = fr/FPS; rel = t - fa/FPS
        world = S["bg"].copy()
        for sp in S["sprites"]: sp.draw(world, t)
        for fl in S["flames"]: fl.draw(world, t, fr)
        if S.get("candle_flame"):
            a0, a1 = S["candle_flame"]
            if t < a1:
                pr_ = min(1, max(0, (t - a0)/(T(123) - a0)))
                Flame(800 - 330*pr_, 792 + 280*pr_, 130, 70).draw(world, t, fr)
        # secousse / flash
        sx = sy = 0.0; flash = None
        for (i, amp, col) in IMPACTS:
            age = t - T(i)
            if 0 <= age < 0.45:
                a = amp*math.exp(-age*11)
                sx += a*math.sin(age*95); sy += a*math.cos(age*83)
                if col is not None and age < 0.22:
                    fa_ = 0.38*(1 - age/0.22)
                    if flash is None or fa_ > flash[1]: flash = (col, fa_)
        frame = camera(world, t, rel, dur, S["focus"], idx, (sx, sy)).convert("RGB")
        frame = ImageChops.multiply(frame, vig)
        if flash:
            ov = Image.new("RGB", (W, H), flash[0]); frame = Image.blend(frame, ov, flash[1])
        d = None
        for (text, col, size, tstart, y) in S["titles"]:
            if t < tstart: continue
            age = t - tstart
            if text == "#COUNT#":
                c0, c1, tot = S["count"]; p = min(1, max(0, (t - c0)/(c1 - c0))); text = str(int(round(tot*p)))
            lay = title_layer(text, col, size)
            sc = 1.0 + 0.35*max(0, 1 - age/0.16)**2
            if sc > 1.005: lay = lay.resize((int(lay.width*sc), int(lay.height*sc)), BI)
            if age < 0.05: lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v*age/0.05)))
            frame.paste(lay, (int(470 - lay.width/2), int(y - (lay.height - title_layer(text, col, size).height)/2)), lay)
        pr.stdin.write(frame.tobytes())
    pr.stdin.close(); pr.wait()
    return idx

if __name__ == "__main__":
    n = len(shot_defs())
    os.makedirs(f"{HERE}/shots", exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(n))
    from multiprocessing import Pool
    with Pool(2) as p:
        for i in p.imap_unordered(render_shot, [(i, f"{HERE}/shots/shot_{i:02d}.mp4") for i in only]): print("done", i, flush=True)

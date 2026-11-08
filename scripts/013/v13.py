#!/usr/bin/env python3
"""Video 013 (Marie-Antoinette), moteur v2 : rendu image par image (calques animes, flammes vivantes, secousses, flashs, titres pop)."""
import json, math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = "/home/claude/work013"
src = open(f"{HERE}/gen_images.py", encoding="utf-8").read().split("S = {}")[0]
exec(src)  # fonctions de dessin (paper, flame, cassette, wig_face, woman, figure, ...)
exec(open(f"{HERE}/gen13.py", encoding="utf-8").read())

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


def clamp01(x): return min(1.0, max(0.0, x))
def ease(x): x = clamp01(x); return x*x*(3 - 2*x)

def bg_cell_desk(lit_letter=True, seed=30):
    im = cell_bg(seed, 0.35); d = ImageDraw.Draw(im)
    d.rectangle((60, 1290, 1020, 1330), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.rectangle((90, 1330, 990, 1600), fill=(40, 26, 16, 255))
    candle(im, 820, 1110, 1.3, lit=False)
    letter(im, 430, 1150, 520, 560, -6, 1.0)
    return im

def guard(L, x, y, s=1.0): figure(L, x, y, s, col=(8, 6, 5), hat=True)

def shot_defs():
    S = []
    # 0 : hook - cellule, bougie, lettre
    S.append(dict(name="hook1", a=0, b=7, bg=bg_cell_desk(), flames=[Flame(820, 1102, 143, 73)], sprites=[],
        focus=[(560, 880), (800, 900)],
        titles=[("IL TE RESTE", CREAM, 132, 0.15, 470), ("QUELQUES HEURES", RED, 120, T(3), 625)]))
    # 1 : la plume ecrit
    def bg1():
        im = paper(31, 0.3, (64, 50, 40)); letter(im, 470, 1000, 640, 720, -3, 1.0); return im
    qu = Spr(lambda L: quill(L, 640, 1150, 1.3, -30), (640, 1150), lambda t: (60*math.sin(t*3.1), 18*math.sin(t*7.3), 3*math.sin(t*5), 1, 1))
    S.append(dict(name="hook2", a=7, b=12, bg=bg1(), flames=[], sprites=[qu], focus=[(470, 900), (600, 1100)],
        titles=[("16 OCTOBRE 1793", CREAM, 96, T(8), 440), ("4 H 30 DU MATIN", RED, 96, T(10), 548)]))
    # 2 : jamais remise
    def bg2():
        im = paper(32, 0.45, (60, 46, 38)); letter(im, 470, 1020, 600, 680, 5, 1.0); return im
    st = Spr(lambda L: stamp_red(L, "JAMAIS REMISE", 470, 1040, 70, -9), (470, 1040), pop(T(14), 0.12, 2.4), appear=T(14))
    S.append(dict(name="hook3", a=12, b=15, bg=bg2(), flames=[], sprites=[st], focus=[(470, 1000), (470, 1040)], titles=[]))
    # 3 : Tu es Marie-Antoinette
    q = Spr(lambda L: queen(L, 470, 930, 1.15), (470, 1300), lambda t: breathe(t, 0.01, 1.0, 5))
    def bg3():
        im = paper(33, 0.2, (70, 40, 44)); glow(im, (470, 900), 420, (190, 160, 120), 0.25); return im
    S.append(dict(name="reine", a=15, b=18, bg=bg3(), flames=[], sprites=[q], focus=[(470, 950), (470, 880)], titles=[]))
    # 4 : Louis XVI guillotine - le couperet tombe
    def bg4():
        im = paper(34, 0.4, (60, 44, 36)); houses(im, 1150, 7, lit=False); guillotine(im, 470, 1290, 1.25, blade=False); return im
    tb = T(22)
    bl = Spr(lambda L: blade_only(L, 470, 1290 - 600*1.25, 1.25), (470, 1290 - 600*1.25), lambda t: (0, 390*1.25*ease((t - tb)/0.18) if t > tb else 0, 0, 1, 1))
    S.append(dict(name="louis16", a=18, b=25, bg=bg4(), flames=[], sprites=[bl], focus=[(470, 900), (470, 1100), (470, 800)],
        titles=[("LOUIS XVI", CREAM, 104, T(19), 440), ("21 JANVIER 1793", RED, 96, T(23), 555)]))
    # 5 : on t'arrache ton fils
    def bg5(): return paper(35, 0.3, (64, 46, 40))
    mom = Spr(lambda L: queen(L, 300, 960, 0.85, mood=2), (300, 1300), lambda t: breathe(t, 0.01, 1.0, 4))
    t0 = T(28)
    away = lambda t, k=0: (420*ease((t - t0)/1.6) if t > t0 else 0, 4*math.sin(t*6 + k), 0, 1, 1)
    kid = Spr(lambda L: figure(L, 700, 1320, 1.4, col=(30, 26, 40), kid=True), (700, 1250), lambda t: away(t, 1))
    kglow = Spr(lambda L: glow(L, (700, 1060), 60, (230, 200, 120), 0.5), (700, 1060), lambda t: away(t, 1))
    gd = Spr(lambda L: guard(L, 820, 1330, 1.15), (820, 1200), lambda t: away(t, 2))
    S.append(dict(name="fils", a=25, b=35, bg=bg5(), flames=[], sprites=[mom, kglow, kid, gd], focus=[(300, 1000), (720, 1150), (470, 1100)],
        titles=[("LOUIS-CHARLES", CREAM, 100, T(29), 440), ("3 JUILLET 1793", RED, 96, T(31), 552)]))
    # 6 : le proces
    def bg6():
        im = paper(36, 0.5); d = ImageDraw.Draw(im); d.rectangle((0, 560, W, 1300), fill=(8, 6, 6, 255))
        for x in (170, 470, 770): d.rectangle((x-8, 760, x+8, 900), fill=(50, 34, 22, 255))
        d.rectangle((120, 1080, 820, 1120), fill=(60, 38, 22, 255), outline=INK+(255,)); d.rectangle((140, 1120, 800, 1260), fill=(40, 26, 16, 255))
        for x in (230, 380, 530, 680): figure(im, x, 1090, 0.95, col=(0, 0, 0), hat=True)
        return im
    S.append(dict(name="proces", a=35, b=40, bg=bg6(), flames=[Flame(170, 760, 130, 70), Flame(470, 760, 130, 70), Flame(770, 760, 130, 70)], sprites=[],
        focus=[(470, 950), (470, 1100)],
        titles=[("14 – 16 OCTOBRE 1793", CREAM, 92, T(36), 440), ("2 JOURS D'AUDIENCE", RED, 92, T(38), 548)]))
    # 7 : l'accusation (Hebert)
    def bg7():
        im = paper(37, 0.35, (80, 30, 26)); return im
    def d_heb(L):
        figure(L, 260, 1330, 1.3, col=(6, 4, 3), hat=True); ImageDraw.Draw(L).line((295, 1090, 560, 1010), fill=(6, 4, 3, 255), width=26)
    heb = Spr(d_heb, (260, 1300), lambda t: (0, 3*math.sin(t*5), 0.8*math.sin(t*3), 1, 1))
    q7 = Spr(lambda L: queen(L, 760, 1010, 0.72, mood=2), (760, 1300), lambda t: breathe(t, 0.01, 0.6, 3))
    redp = Spr(lambda L: glow(L, (470, 1050), 440, (210, 20, 20), 0.5), (470, 1050), lambda t: (0, 0, 0, 1 + 0.05*math.sin(t*7), 0.15 + 0.85*clamp01((t - T(46))/0.5)), appear=T(44))
    S.append(dict(name="accuse", a=40, b=52, bg=bg7(), flames=[], sprites=[redp, heb, q7], focus=[(470, 1100), (300, 1050), (760, 1050), (470, 1000)],
        titles=[("TÉMOIN : HÉBERT", CREAM, 96, T(41), 440), ("LE « PÈRE DUCHESNE »", RED, 88, T(45), 550)]))
    # 8 : j'en appelle a toutes les meres
    def bg8():
        im = paper(38, 0.3, (70, 50, 40)); return im
    q8 = Spr(lambda L: queen(L, 470, 900, 1.0, mood=2), (470, 1300), lambda t: breathe(t, 0.012, 1.2, 4))
    crowd = []
    for k in range(9):
        x = 60 + k*120
        crowd.append(Spr(lambda L, x=x, k=k: figure(L, x, 1520 + (k % 2)*30, 1.1, col=(10, 7, 6)), (x, 1400), lambda t, k=k: (0, 6*math.sin(t*3 + k), 0, 1, 1)))
    warm = Spr(lambda L: glow(L, (470, 1300), 460, (255, 190, 110), 0.55), (470, 1300), lambda t: (0, 0, 0, 1, clamp01((t - T(58))/1.2)), appear=T(58))
    S.append(dict(name="meres", a=52, b=64, bg=bg8(), flames=[], sprites=[warm, q8] + crowd, focus=[(470, 1000), (470, 1300), (470, 900), (300, 1350)], titles=[]))
    # 9 : la salle emue, les jures non
    def bg9():
        im = paper(39, 0.55, (40, 44, 56)); d = ImageDraw.Draw(im)
        d.rectangle((80, 1080, 1000, 1130), fill=(50, 34, 22, 255), outline=INK+(255,)); d.rectangle((100, 1130, 980, 1280), fill=(34, 22, 14, 255))
        for x in (190, 340, 490, 640, 790, 940): figure(im, x, 1090, 0.9, col=(0, 0, 0), hat=True)
        return im
    cold = Spr(lambda L: glow(L, (470, 950), 480, (120, 150, 210), 0.45), (470, 950), lambda t: (0, 0, 0, 1, clamp01((t - T(68))/0.4)), appear=T(68))
    S.append(dict(name="jures", a=64, b=71, bg=bg9(), flames=[], sprites=[cold], focus=[(470, 1050), (300, 1000), (700, 1000)],
        titles=[("MÊME LES TRICOTEUSES", CREAM, 84, T(64), 440), ("SONT ÉMUES", RED, 92, T(66), 548)]))
    # 10 : verdict, la mort
    def bg10():
        im = paper(40, 0.65, (40, 40, 54)); glow(im, (760, 620), 200, (220, 220, 240), 0.5)
        ImageDraw.Draw(im).ellipse((700, 560, 820, 680), fill=(236, 232, 214, 255)); houses(im, 1300, 11, lit=False); return im
    st10 = Spr(lambda L: stamp_red(L, "MORT", 470, 1040, 150, -8), (470, 1040), pop(T(78), 0.12, 2.6), appear=T(78))
    S.append(dict(name="verdict", a=71, b=79, bg=bg10(), flames=[], sprites=[st10], focus=[(700, 700), (470, 1100), (470, 1040)], titles=[]))
    # 11 : 4 h 30, elle ecrit a sa belle-soeur
    qu11 = Spr(lambda L: quill(L, 560, 1250, 1.1, -30), (560, 1250), lambda t: (45*math.sin(t*3.3), 14*math.sin(t*8.1), 3*math.sin(t*5), 1, 1))
    S.append(dict(name="cellule", a=79, b=91, bg=bg_cell_desk(seed=41), flames=[Flame(820, 1102, 143, 73)], sprites=[qu11], focus=[(760, 700), (470, 880), (800, 900), (470, 900)],
        titles=[("CONCIERGERIE", CREAM, 104, T(80), 440), ("CACHOT DE LA REINE", RED, 92, T(84), 556)]))
    # 12 : "C'est a vous, ma soeur..."
    def bg12():
        im = paper(42, 0.35, (60, 48, 40)); letter(im, 470, 1020, 700, 760, -2, 1.0); glow(im, (900, 700), 260, (255, 150, 60), 0.35); return im
    S.append(dict(name="lettre", a=91, b=102, bg=bg12(), flames=[], sprites=[], focus=[(420, 860), (470, 1000), (500, 1150)], titles=[]))
    # 13 : Elisabeth ne la recevra jamais / saisie
    eli = Spr(lambda L: woman(L, 470, 900, 0.95, fan=False, dress=(50, 60, 90)), (470, 1300), lambda t: breathe(t, 0.01, 0.8, 4, 1.0))
    lt = Spr(lambda L: letter(L, 780, 1250, 300, 340, 12, 1.0), (780, 1250), lambda t: (0, 10*math.sin(t*2), 2*math.sin(t*1.5), 1, 1))
    st13 = Spr(lambda L: stamp_red(L, "SAISIE", 780, 1250, 70, -12), (780, 1250), pop(T(110), 0.12, 2.6), appear=T(110))
    S.append(dict(name="elisabeth", a=102, b=111, bg=paper(43, 0.3, (52, 54, 66)), flames=[], sprites=[eli, lt, st13], focus=[(470, 950), (780, 1250), (470, 1050)],
        titles=[("MADAME ÉLISABETH", CREAM, 96, T(103), 440), ("SŒUR DE LOUIS XVI", RED, 92, T(106), 550)]))
    # 14 : elle meurt a son tour, sans savoir
    def bg14():
        im = paper(44, 0.6, (40, 40, 50)); houses(im, 1180, 13, lit=False); guillotine(im, 700, 1250, 0.7, blade=True); return im
    eli2 = Spr(lambda L: woman(L, 300, 1000, 0.75, fan=False, dress=(50, 60, 90)), (300, 1300), lambda t: (0, 3*math.sin(t*2), 0, 1, 1 - 0.75*clamp01((t - T(121))/1.5)))
    S.append(dict(name="elisabeth2", a=111, b=128, bg=bg14(), flames=[], sprites=[eli2], focus=[(470, 1050), (700, 1000), (300, 1050), (470, 1100)],
        titles=[("GUILLOTINÉE", CREAM, 104, T(116), 440), ("LE 10 MAI 1794", RED, 100, T(119), 556)]))
    # 15 : cheveux coupes
    def bg15():
        im = paper(45, 0.3, (60, 50, 46)); return im
    q15 = Spr(lambda L: queen(L, 470, 1000, 0.95, bonnet=False), (470, 1350), lambda t: breathe(t, 0.008, 0.6, 3))
    def dyn_sc(world, t, fr):
        o = 0.5 + 0.5*math.cos(t*9) if T(130) < t < T(134) else 0.8
        scissors(world, 700, 760, 0.9, o)
    locks = []
    for k in range(6):
        ap = T(131) + k*0.18
        locks.append(Spr(lambda L, k=k: lock(L, 560 + k*30, 820, 1.0, k), (580 + k*30, 900), lambda t, ap=ap, k=k: (20*math.sin(t*3 + k), 520*clamp01((t - ap)/1.6)**1.4, 40*(t - ap), 1, 1), appear=ap))
    S.append(dict(name="cheveux", a=128, b=134, bg=bg15(), flames=[], sprites=[q15] + locks, dyn=[dyn_sc], focus=[(560, 900), (470, 1050), (650, 800)], titles=[]))
    # 16 : mains liees dans le dos
    def bg16():
        im = paper(46, 0.35, (62, 50, 44)); hands_tied(im, 470, 1000, 1.2); return im
    S.append(dict(name="mains", a=134, b=140, bg=bg16(), flames=[], sprites=[], focus=[(470, 1050), (470, 1000)], titles=[]))
    # 17 : la charrette a travers Paris
    def bg17():
        im = paper(47, 0.35, (70, 48, 34)); houses(im, 1150, 17, lit=False); return im
    tc = T(140)
    car = Spr(lambda L: cart(L, 420, 1300, 0.9), (420, 1200), lambda t: (-330 + 520*clamp01((t - tc)/3.0), 4*abs(math.sin(t*6)), 0.6*math.sin(t*6), 1, 1))
    mob = []
    for k in range(10):
        x = 40 + k*110
        mob.append(Spr(lambda L, x=x, k=k: figure(L, x, 1560 + (k % 2)*25, 1.0, col=(6, 4, 3), arms_up=(k % 2 == 0)), (x, 1450), lambda t, k=k: (3*math.sin(t*8 + k), 8*abs(math.sin(t*6 + k*1.3)), 3*math.sin(t*7 + k), 1, 1)))
    S.append(dict(name="charrette", a=140, b=146, bg=bg17(), flames=[], sprites=[car] + mob, focus=[(470, 1250), (300, 1200), (650, 1300)],
        titles=[("SOUS LES INSULTES", CREAM, 92, T(141), 440)]))
    # 18 : midi et quart
    def bg18():
        im = paper(48, 0.3, (66, 52, 40)); clock(im, 470, 1000, 300); return im
    def dyn_clock(world, t, fr):
        m = 720 + 15*ease((t - T(146))/(T(148) - T(146) + 0.3)); hands(world, 470, 1000, 300, m)
    S.append(dict(name="midi", a=146, b=149, bg=bg18(), flames=[], sprites=[], dyn=[dyn_clock], focus=[(470, 1000), (470, 950)],
        titles=[("PLACE DE LA RÉVOLUTION", CREAM, 84, T(146), 440), ("AUJOURD'HUI LA CONCORDE", RED, 80, T(148), 540)]))
    # 19 : le pied du bourreau
    def bg19():
        im = paper(49, 0.5, (60, 44, 36)); guillotine(im, 470, 1700, 1.6, blade=True); return im
    def dyn_step(world, t, fr):
        shoe_boot(world, 560, 1250, 1.15, ease((t - T(152))/(T(155) - T(152) + 0.1)))
    S.append(dict(name="pied", a=149, b=158, bg=bg19(), flames=[], sprites=[], dyn=[dyn_step], focus=[(470, 1000), (480, 1150), (470, 900)],
        titles=[("SON SOULIER DE SATIN", CREAM, 84, T(150), 440)]))
    # 20 : Pardon, monsieur
    def bg20():
        im = paper(50, 0.45, (80, 30, 30)); glow(im, (470, 950), 400, (230, 200, 170), 0.2); return im
    q20 = Spr(lambda L: queen(L, 470, 930, 1.2, bonnet=False, mood=1), (470, 1300), lambda t: breathe(t, 0.01, 0.8, 3))
    S.append(dict(name="pardon", a=158, b=173, bg=bg20(), flames=[], sprites=[q20], focus=[(470, 950), (470, 880), (470, 1000)], titles=[]))
    # 21 : brioche - aucune preuve
    def bg21():
        im = paper(51, 0.2, (78, 56, 36)); brioche(im, 470, 1260, 1.5); return im
    st21 = Spr(lambda L: stamp_red(L, "AUCUNE PREUVE", 470, 1150, 76, -8), (470, 1150), pop(T(180), 0.12, 2.4), appear=T(180))
    S.append(dict(name="brioche", a=173, b=186, bg=bg21(), flames=[], sprites=[st21], focus=[(470, 1000), (470, 1050)],
        titles=[("« QU'ILS MANGENT", CREAM, 96, T(174), 440), ("DE LA BRIOCHE »", RED, 96, T(177), 552)]))
    # 22 : Rousseau
    def bg22():
        im = paper(52, 0.3, (66, 48, 36)); book(im, 470, 1180, 0.95); return im
    S.append(dict(name="rousseau", a=186, b=196, bg=bg22(), flames=[], sprites=[], focus=[(470, 1000), (470, 1020)],
        titles=[("ROUSSEAU, CONFESSIONS", CREAM, 84, T(187), 440), ("ÉCRITES VERS 1765", RED, 92, T(189), 548)]))
    # 23 : Envoie ca
    def bg23():
        im = paper(53, 0.25, (70, 50, 40)); brioche(im, 470, 1250, 0.9); return im
    tp = T(196)
    pl = Spr(lambda L: plane(L, 470, 1000, 1.3), (470, 1000), lambda t: (-500 + 1100*ease((t - tp)/2.2), 220 - 380*ease((t - tp)/2.2), -12 + 10*math.sin(t*3), 1, 1))
    S.append(dict(name="envoie", a=196, b=205, bg=bg23(), flames=[], sprites=[pl], focus=[(470, 1100), (470, 1000)],
        titles=[("ENVOIE ÇA", CREAM, 120, T(196), 440), ("À QUELQU'UN", RED, 110, T(199), 580)]))
    # 24 : boucle vers le debut
    S.append(dict(name="boucle", a=205, b=len(WORDS), bg=bg_cell_desk(), flames=[Flame(820, 1102, 143, 73)], sprites=[], focus=[(560, 880), (800, 900)], titles=[]))
    return S

IMPACTS = [(3, 12, (255, 255, 255)), (11, 8, None), (14, 22, (200, 30, 30)), (17, 10, None), (22, 26, (255, 255, 255)), (28, 14, None), (30, 10, None),
           (36, 10, None), (43, 12, (200, 30, 30)), (47, 16, (200, 30, 30)), (58, 8, None), (68, 10, (120, 150, 220)), (70, 12, None), (78, 28, (200, 30, 30)),
           (80, 8, None), (91, 6, None), (106, 10, None), (110, 22, (200, 30, 30)), (116, 14, None), (121, 18, (255, 255, 255)), (133, 14, None), (136, 14, None),
           (141, 10, None), (146, 14, (255, 255, 255)), (155, 22, None), (165, 8, None), (174, 10, None), (180, 22, (200, 30, 30)), (186, 10, None), (196, 14, (255, 255, 255))]

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

def frame_at(S, idx, fr, fa, dur, vig):
    t = fr/FPS; rel = t - fa/FPS
    world = S["bg"].copy()
    for sp in S["sprites"]: sp.draw(world, t)
    for fn in S.get("dyn", []): fn(world, t, fr)
    for fl in S["flames"]: fl.draw(world, t, fr)
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

    return frame

_SH = None
def all_shots():
    global _SH
    if _SH is None: _SH = shot_defs()
    return _SH

def render_shot(args):
    idx, outpath = args
    S = all_shots()[idx]
    ta, tb = T(S["a"]), (T(S["b"]) if S["b"] < len(WORDS) else DUR)
    if S["a"] == 0: ta = 0.0
    fa, fb = int(round(ta*FPS)), int(round(tb*FPS))
    if idx == len(all_shots()) - 1: fb = int(round(DUR*FPS))
    vig = vignette_mask()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", outpath]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    dur = max((fb - fa)/FPS, 0.1)
    for fr in range(fa, fb):
        frame = frame_at(S, idx, fr, fa, dur, vig)
        pr.stdin.write(frame.tobytes())
    pr.stdin.close(); pr.wait()
    return idx

if __name__ == "__main__":
    n = 25
    os.makedirs(f"{HERE}/shots", exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(n))
    from multiprocessing import Pool
    with Pool(2) as p:
        for i in p.imap_unordered(render_shot, [(i, f"{HERE}/shots/shot_{i:02d}.mp4") for i in only]): print("done", i, flush=True)

#!/usr/bin/env python3
"""Video 013 (Marie-Antoinette), moteur v2 : rendu image par image (calques animes, flammes vivantes, secousses, flashs, titres pop)."""
import json, math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = "/home/claude/work013b"
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

def bg_cell_desk(seed=30):
    im = cell_bg(seed, 0.35); d = ImageDraw.Draw(im)
    d.rectangle((60, 1290, 1020, 1330), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
    d.rectangle((90, 1330, 990, 1600), fill=(40, 26, 16, 255))
    candle(im, 820, 1110, 1.3, lit=False)
    letter(im, 430, 1150, 520, 560, -6, 1.0)
    return im

def bg_hook(seed=30):
    """Premiere image : la reine a sa table, la lettre devant elle, la bougie."""
    im = cell_bg(seed, 0.35)
    queen_desk(im, 430, 1090, 0.88)
    letter(im, 330, 1470, 420, 330, -6, 1.0)
    candle(im, 850, 1270, 1.2, lit=False)
    return im

def guard(L, x, y, s=1.0): figure(L, x, y, s, col=(8, 6, 5), hat=True)

def shot_defs():
    S = []
    # 0 : hook - la reine ecrit a la bougie (visible des la 1re image)
    S.append(dict(name="hook1", a=0, b=7, bg=bg_hook(), flames=[Flame(850, 1262, 132, 67)], sprites=[],
        focus=[(470, 1150), (430, 1100)],
        titles=[("IL TE RESTE", CREAM, 132, 0.0, 470), ("QUELQUES HEURES", RED, 120, T(3), 625)]))
    # 1 : la plume ecrit (pas de titre : un seul texte a la fois)
    def bg1():
        im = paper(31, 0.3, (64, 50, 40)); letter(im, 470, 1060, 640, 720, -3, 1.0); return im
    qu = Spr(lambda L: quill(L, 640, 1210, 1.3, -30), (640, 1210), lambda t: (60*math.sin(t*3.1), 18*math.sin(t*7.3), 3*math.sin(t*5), 1, 1))
    S.append(dict(name="hook2", a=7, b=12, bg=bg1(), flames=[], sprites=[qu], focus=[(470, 1060), (600, 1150)], titles=[]))
    # 2 : jamais remise
    def bg2():
        im = paper(32, 0.45, (60, 46, 38)); letter(im, 470, 1080, 600, 680, 5, 1.0); return im
    st = Spr(lambda L: stamp_red(L, "JAMAIS REMISE", 470, 1100, 70, -9), (470, 1100), pop(T(14), 0.12, 2.4), appear=T(14))
    S.append(dict(name="hook3", a=12, b=15, bg=bg2(), flames=[], sprites=[st], focus=[(470, 1060), (470, 1100)], titles=[]))
    # 3 : Tu es Marie-Antoinette
    q = Spr(lambda L: queen(L, 470, 1120, 1.15), (470, 1450), lambda t: breathe(t, 0.01, 1.0, 5))
    def bg3():
        im = paper(33, 0.2, (70, 40, 44)); glow(im, (470, 1100), 420, (190, 160, 120), 0.25); return im
    S.append(dict(name="reine", a=15, b=18, bg=bg3(), flames=[], sprites=[q], focus=[(470, 960), (470, 950)], titles=[]))
    # 4 : teaser brioche - la phrase qu'on te prete... jamais dite
    def bg4():
        im = paper(34, 0.25, (78, 56, 36)); brioche(im, 470, 1300, 1.35); return im
    st4 = Spr(lambda L: stamp_red(L, "JAMAIS DITE", 470, 1240, 84, -8), (470, 1240), pop(T(31), 0.12, 2.6), appear=T(31))
    S.append(dict(name="teaser", a=18, b=32, bg=bg4(), flames=[], sprites=[st4], focus=[(470, 1100), (470, 1180), (470, 1050)],
        titles=[("« QU'ILS MANGENT", CREAM, 96, T(20), 440), ("DE LA BRIOCHE » ?", RED, 96, T(25), 552)]))
    # 5 : Louis XVI - le couperet tombe
    def bg5():
        im = paper(35, 0.4, (60, 44, 36)); houses(im, 1150, 7, lit=False); guillotine(im, 470, 1290, 1.25, blade=False); return im
    tb = T(36)
    bl = Spr(lambda L: blade_only(L, 470, 1290 - 600*1.25, 1.25), (470, 1290 - 600*1.25), lambda t: (0, 390*1.25*ease((t - tb)/0.18) if t > tb else 0, 0, 1, 1))
    S.append(dict(name="louis16", a=32, b=39, bg=bg5(), flames=[], sprites=[bl], focus=[(470, 900), (470, 1100), (470, 900)],
        titles=[("LOUIS XVI", CREAM, 104, T(33), 440), ("21 JANVIER 1793", RED, 96, T(37), 555)]))
    # 6 : on t'arrache ton fils
    mom = Spr(lambda L: queen(L, 300, 1070, 0.85, mood=2), (300, 1400), lambda t: breathe(t, 0.01, 1.0, 4))
    t0 = T(42)
    away = lambda t, k=0: (420*ease((t - t0)/1.6) if t > t0 else 0, 4*math.sin(t*6 + k), 0, 1, 1)
    kid = Spr(lambda L: figure(L, 700, 1340, 1.4, col=(30, 26, 40), kid=True), (700, 1270), lambda t: away(t, 1))
    kglow = Spr(lambda L: glow(L, (700, 1080), 60, (230, 200, 120), 0.5), (700, 1080), lambda t: away(t, 1))
    gd = Spr(lambda L: guard(L, 820, 1350, 1.15), (820, 1220), lambda t: away(t, 2))
    S.append(dict(name="fils", a=39, b=49, bg=paper(36, 0.3, (64, 46, 40)), flames=[], sprites=[mom, kglow, kid, gd], focus=[(300, 1000), (720, 1150), (470, 1100)],
        titles=[("LOUIS-CHARLES", CREAM, 100, T(40), 440), ("3 JUILLET 1793", RED, 96, T(43), 552)]))
    # 7 : le proces
    def bg7():
        im = paper(37, 0.5); d = ImageDraw.Draw(im); d.rectangle((0, 760, W, 1500), fill=(8, 6, 6, 255))
        for x in (170, 470, 770): d.rectangle((x-8, 960, x+8, 1100), fill=(50, 34, 22, 255))
        d.rectangle((120, 1280, 820, 1320), fill=(60, 38, 22, 255), outline=INK+(255,)); d.rectangle((140, 1320, 800, 1460), fill=(40, 26, 16, 255))
        for x in (230, 380, 530, 680): figure(im, x, 1290, 0.95, col=(0, 0, 0), hat=True)
        return im
    S.append(dict(name="proces", a=49, b=54, bg=bg7(), flames=[Flame(170, 960, 130, 70), Flame(470, 960, 130, 70), Flame(770, 960, 130, 70)], sprites=[],
        focus=[(470, 1100), (470, 1200)],
        titles=[("14 – 16 OCTOBRE 1793", CREAM, 92, T(50), 440), ("2 JOURS D'AUDIENCE", RED, 92, T(52), 548)]))
    # 8 : l'accusation (Hebert)
    def d_heb(L):
        figure(L, 260, 1380, 1.3, col=(6, 4, 3), hat=True); ImageDraw.Draw(L).line((295, 1140, 560, 1060), fill=(6, 4, 3, 255), width=26)
    heb = Spr(d_heb, (260, 1350), lambda t: (0, 3*math.sin(t*5), 0.8*math.sin(t*3), 1, 1))
    q8 = Spr(lambda L: queen(L, 760, 1070, 0.72, mood=2), (760, 1350), lambda t: breathe(t, 0.01, 0.6, 3))
    redp = Spr(lambda L: glow(L, (470, 1100), 440, (210, 20, 20), 0.5), (470, 1100), lambda t: (0, 0, 0, 1 + 0.05*math.sin(t*7), 0.15 + 0.85*clamp01((t - T(60))/0.5)), appear=T(58))
    S.append(dict(name="accuse", a=54, b=66, bg=paper(38, 0.35, (80, 30, 26)), flames=[], sprites=[redp, heb, q8], focus=[(470, 1150), (300, 1100), (760, 1050), (470, 1100)],
        titles=[("TÉMOIN : HÉBERT", CREAM, 96, T(55), 440), ("LE « PÈRE DUCHESNE »", RED, 88, T(59), 550)]))
    # 9 : j'en appelle a toutes les meres
    q9 = Spr(lambda L: queen(L, 470, 1060, 1.0, mood=2), (470, 1400), lambda t: breathe(t, 0.012, 1.2, 4))
    crowd = []
    for k in range(9):
        x = 60 + k*120
        crowd.append(Spr(lambda L, x=x, k=k: figure(L, x, 1600 + (k % 2)*30, 1.1, col=(10, 7, 6)), (x, 1480), lambda t, k=k: (0, 6*math.sin(t*3 + k), 0, 1, 1)))
    warm = Spr(lambda L: glow(L, (470, 1350), 460, (255, 190, 110), 0.55), (470, 1350), lambda t: (0, 0, 0, 1, clamp01((t - T(72))/1.2)), appear=T(72))
    S.append(dict(name="meres", a=66, b=78, bg=paper(39, 0.3, (70, 50, 40)), flames=[], sprites=[warm, q9] + crowd, focus=[(470, 920), (470, 1300), (470, 900), (300, 1350)], titles=[]))
    # 10 : la salle emue, les jures... non
    def bg10():
        im = paper(40, 0.55, (40, 44, 56)); d = ImageDraw.Draw(im)
        d.rectangle((80, 1180, 1000, 1230), fill=(50, 34, 22, 255), outline=INK+(255,)); d.rectangle((100, 1230, 980, 1380), fill=(34, 22, 14, 255))
        for x in (190, 340, 490, 640, 790, 940): figure(im, x, 1190, 0.9, col=(0, 0, 0), hat=True)
        return im
    cold = Spr(lambda L: glow(L, (470, 1050), 480, (120, 150, 210), 0.45), (470, 1050), lambda t: (0, 0, 0, 1, clamp01((t - T(84))/0.3)), appear=T(83))
    S.append(dict(name="jures", a=78, b=85, bg=bg10(), flames=[], sprites=[cold], focus=[(470, 1150), (300, 1100), (700, 1100)],
        titles=[("MÊME LES TRICOTEUSES", CREAM, 84, T(78), 440), ("SONT ÉMUES", RED, 92, T(80), 548)]))
    # 11 : 4 h du matin : la mort
    def bg11():
        im = paper(41, 0.65, (40, 40, 54)); glow(im, (760, 620), 200, (220, 220, 240), 0.5)
        ImageDraw.Draw(im).ellipse((700, 560, 820, 680), fill=(236, 232, 214, 255)); houses(im, 1350, 11, lit=False); return im
    st11 = Spr(lambda L: stamp_red(L, "MORT", 470, 1120, 150, -8), (470, 1120), pop(T(90), 0.12, 2.6), appear=T(90))
    S.append(dict(name="verdict", a=85, b=91, bg=bg11(), flames=[], sprites=[st11], focus=[(700, 800), (470, 1150), (470, 1120)], titles=[]))
    # 12 : 4 h 30, elle ecrit a sa belle-soeur
    qu12 = Spr(lambda L: quill(L, 560, 1250, 1.1, -30), (560, 1250), lambda t: (45*math.sin(t*3.3), 14*math.sin(t*8.1), 3*math.sin(t*5), 1, 1))
    S.append(dict(name="cellule", a=91, b=100, bg=bg_cell_desk(seed=41), flames=[Flame(820, 1102, 143, 73)], sprites=[qu12], focus=[(760, 800), (470, 1000), (800, 1000), (470, 1000)],
        titles=[("CONCIERGERIE", CREAM, 104, T(92), 440), ("CACHOT DE LA REINE", RED, 92, T(95), 556)]))
    # 13 : "C'est a vous, ma soeur..."
    def bg13():
        im = paper(42, 0.35, (60, 48, 40)); letter(im, 470, 1100, 700, 760, -2, 1.0); glow(im, (900, 800), 260, (255, 150, 60), 0.35); return im
    S.append(dict(name="lettre", a=100, b=111, bg=bg13(), flames=[], sprites=[], focus=[(420, 1000), (470, 1100), (500, 1200)], titles=[]))
    # 14 : Elisabeth ne la recevra jamais / saisie
    eli = Spr(lambda L: woman(L, 470, 1050, 0.95, fan=False, dress=(50, 60, 90)), (470, 1450), lambda t: breathe(t, 0.01, 0.8, 4, 1.0))
    lt = Spr(lambda L: letter(L, 780, 1330, 300, 340, 12, 1.0), (780, 1330), lambda t: (0, 10*math.sin(t*2), 2*math.sin(t*1.5), 1, 1))
    st14 = Spr(lambda L: stamp_red(L, "SAISIE", 780, 1330, 70, -12), (780, 1330), pop(T(119), 0.12, 2.6), appear=T(119))
    S.append(dict(name="elisabeth", a=111, b=120, bg=paper(43, 0.3, (52, 54, 66)), flames=[], sprites=[eli, lt, st14], focus=[(470, 920), (780, 1250), (470, 950)],
        titles=[("MADAME ÉLISABETH", CREAM, 96, T(111), 440), ("SŒUR DE LOUIS XVI", RED, 92, T(114), 550)]))
    # 15 : elle meurt a son tour, sans savoir
    def bg15():
        im = paper(44, 0.6, (40, 40, 50)); houses(im, 1230, 13, lit=False); guillotine(im, 700, 1300, 0.7, blade=True); return im
    eli2 = Spr(lambda L: woman(L, 300, 1060, 0.75, fan=False, dress=(50, 60, 90)), (300, 1360), lambda t: (0, 3*math.sin(t*2), 0, 1, 1 - 0.75*clamp01((t - T(127))/1.5)))
    S.append(dict(name="elisabeth2", a=120, b=133, bg=bg15(), flames=[], sprites=[eli2], focus=[(470, 1100), (700, 1050), (300, 950), (470, 1150)],
        titles=[("GUILLOTINÉE", CREAM, 104, T(121), 440), ("LE 10 MAI 1794", RED, 100, T(124), 556)]))
    # 16 : on te coupe les cheveux
    q16 = Spr(lambda L: queen(L, 470, 1100, 0.95, bonnet=False), (470, 1450), lambda t: breathe(t, 0.008, 0.6, 3))
    def dyn_sc(world, t, fr):
        o = 0.5 + 0.5*math.cos(t*9) if T(137) < t < T(140) else 0.8
        scissors(world, 740, 940, 0.9, o)
    locks = []
    for k in range(6):
        ap = T(138) + k*0.15
        locks.append(Spr(lambda L, k=k: lock(L, 560 + k*30, 960, 1.0, k), (580 + k*30, 1040), lambda t, ap=ap, k=k: (20*math.sin(t*3 + k), 480*clamp01((t - ap)/1.6)**1.4, 40*(t - ap), 1, 1), appear=ap))
    S.append(dict(name="cheveux", a=133, b=140, bg=paper(45, 0.3, (60, 50, 46)), flames=[], sprites=[q16] + locks, dyn=[dyn_sc], focus=[(560, 900), (470, 950), (650, 900)], titles=[]))
    # 17 : on te lie les mains
    def bg17():
        im = paper(46, 0.35, (62, 50, 44)); hands_tied(im, 470, 1100, 1.2); return im
    S.append(dict(name="mains", a=140, b=145, bg=bg17(), flames=[], sprites=[], focus=[(470, 1050), (470, 1000)], titles=[]))
    # 18 : la charrette a travers Paris, sous les insultes (date non dite a l'ecran)
    def bg18():
        im = paper(47, 0.35, (70, 48, 34)); houses(im, 1150, 17, lit=False); return im
    tc = T(145)
    car = Spr(lambda L: cart(L, 420, 1300, 0.9), (420, 1200), lambda t: (-330 + 520*clamp01((t - tc)/3.0), 4*abs(math.sin(t*6)), 0.6*math.sin(t*6), 1, 1))
    mob = []
    for k in range(10):
        x = 40 + k*110
        mob.append(Spr(lambda L, x=x, k=k: figure(L, x, 1560 + (k % 2)*25, 1.0, col=(6, 4, 3), arms_up=(k % 2 == 0)), (x, 1450), lambda t, k=k: (3*math.sin(t*8 + k), 8*abs(math.sin(t*6 + k*1.3)), 3*math.sin(t*7 + k), 1, 1)))
    S.append(dict(name="charrette", a=145, b=154, bg=bg18(), flames=[], sprites=[car] + mob, focus=[(470, 1250), (300, 1150), (650, 1300)],
        titles=[("16 OCTOBRE 1793", CREAM, 100, T(146), 440)]))
    # 19 : midi et quart (horloge seule)
    def bg19():
        im = paper(48, 0.3, (66, 52, 40)); clock(im, 470, 1080, 300); return im
    def dyn_clock(world, t, fr):
        m = 720 + 15*ease((t - T(154))/(T(156) - T(154) + 0.3)); hands(world, 470, 1080, 300, m)
    S.append(dict(name="midi", a=154, b=157, bg=bg19(), flames=[], sprites=[], dyn=[dyn_clock], focus=[(470, 1080), (470, 1050)], titles=[]))
    # 20 : le pied du bourreau (gros plan lisible)
    def bg20():
        im = paper(49, 0.4, (60, 44, 36)); planks(im, 760, 1800); return im
    def dyn_step(world, t, fr):
        shoe_boot(world, 600, 1330, 1.3, ease((t - T(160))/(T(163) - T(160) + 0.1)))
    S.append(dict(name="pied", a=157, b=166, bg=bg20(), flames=[], sprites=[], dyn=[dyn_step], focus=[(480, 1150), (520, 1250), (470, 1150)],
        titles=[("PLACE DE LA RÉVOLUTION", CREAM, 84, T(157), 440), ("AUJOURD'HUI LA CONCORDE", RED, 80, T(159), 540)]))
    # 21 : Pardon, monsieur (yeux ouverts puis fermes)
    def bg21():
        im = paper(50, 0.45, (80, 30, 30)); glow(im, (470, 1150), 400, (230, 200, 170), 0.2); return im
    tclose = T(177) + 0.3
    q21a = Spr(lambda L: queen(L, 470, 1150, 1.2, bonnet=False, mood=1), (470, 1500), lambda t: breathe(t, 0.01, 0.8, 3), vanish=tclose)
    q21b = Spr(lambda L: queen(L, 470, 1150, 1.2, bonnet=False, mood=2, eyes_closed=True), (470, 1500), lambda t: breathe(t, 0.006, 0.4, 2), appear=tclose)
    S.append(dict(name="pardon", a=166, b=178, bg=bg21(), flames=[], sprites=[q21a, q21b], focus=[(470, 950), (470, 900), (470, 1000)], titles=[]))
    # 22 : brioche - jamais dite
    def bg22():
        im = paper(51, 0.2, (78, 56, 36)); brioche(im, 470, 1260, 1.5); return im
    st22 = Spr(lambda L: stamp_red(L, "AUCUNE PREUVE", 470, 1150, 76, -8), (470, 1150), pop(T(189), 0.12, 2.4), appear=T(189))
    S.append(dict(name="brioche", a=178, b=191, bg=bg22(), flames=[], sprites=[st22], focus=[(470, 1000), (470, 1050)],
        titles=[("« QU'ILS MANGENT", CREAM, 96, T(181), 440), ("DE LA BRIOCHE »", RED, 96, T(183), 552)]))
    # 23 : Rousseau
    def bg23():
        im = paper(52, 0.3, (66, 48, 36)); book(im, 470, 1180, 0.95); return im
    S.append(dict(name="rousseau", a=191, b=201, bg=bg23(), flames=[], sprites=[], focus=[(470, 1000), (470, 1020)],
        titles=[("ROUSSEAU, CONFESSIONS", CREAM, 84, T(192), 440), ("ÉCRITES VERS 1765", RED, 92, T(194), 548)]))
    # 24 : Envoie ca
    def bg24():
        im = paper(53, 0.25, (70, 50, 40)); brioche(im, 470, 1250, 0.9); return im
    tp = T(201)
    pl = Spr(lambda L: plane(L, 470, 1050, 1.3), (470, 1050), lambda t: (-500 + 1100*ease((t - tp)/2.2), 220 - 380*ease((t - tp)/2.2), -12 + 10*math.sin(t*3), 1, 1))
    S.append(dict(name="envoie", a=201, b=210, bg=bg24(), flames=[], sprites=[pl], focus=[(470, 1100), (470, 1050)],
        titles=[("ENVOIE ÇA", CREAM, 120, T(201), 440), ("À QUELQU'UN", RED, 110, T(204), 580)]))
    # 25 : boucle vers la premiere image
    S.append(dict(name="boucle", a=210, b=len(WORDS), bg=bg_hook(), flames=[Flame(850, 1262, 132, 67)], sprites=[], focus=[(470, 1150), (430, 1100)], titles=[]))
    return S

IMPACTS = [(3, 12, (255, 255, 255)), (11, 8, None), (14, 22, (200, 30, 30)), (17, 10, None), (26, 10, None), (31, 22, (200, 30, 30)), (36, 26, (255, 255, 255)),
           (42, 14, None), (44, 10, None), (50, 10, None), (57, 12, (200, 30, 30)), (61, 16, (200, 30, 30)), (72, 8, None), (84, 14, (120, 150, 220)),
           (90, 28, (200, 30, 30)), (91, 8, None), (100, 6, None), (114, 10, None), (119, 22, (200, 30, 30)), (126, 18, (255, 255, 255)), (137, 14, None),
           (142, 14, None), (146, 10, None), (154, 14, (255, 255, 255)), (163, 22, None), (170, 8, None), (181, 10, None), (189, 22, (200, 30, 30)),
           (191, 10, None), (201, 14, (255, 255, 255))]

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
    n = 26
    os.makedirs(f"{HERE}/shots", exist_ok=True)
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(n))
    from multiprocessing import Pool
    with Pool(2) as p:
        for i in p.imap_unordered(render_shot, [(i, f"{HERE}/shots/shot_{i:02d}.mp4") for i in only]): print("done", i, flush=True)

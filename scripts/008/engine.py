#!/usr/bin/env python3
"""Video 013 (Marie-Antoinette), moteur v2 : rendu image par image (calques animes, flammes vivantes, secousses, flashs, titres pop)."""
import json, math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = "/home/claude/work008"
src = open(f"{HERE}/gen_images.py", encoding="utf-8").read().split("S = {}")[0]
exec(src)  # fonctions de dessin (paper, flame, cassette, wig_face, woman, figure, ...)
exec(open(f"{HERE}/gen13.py", encoding="utf-8").read())
exec(open(f"{HERE}/gen008.py", encoding="utf-8").read())

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


def clamp01(x): return min(1.0, max(0.0, x))
def ease(x): x = clamp01(x); return x*x*(3 - 2*x)
def bg_paper(seed, dark=0.0, warm=(70, 46, 30)): return paper(seed, dark, warm)

exec(open(f"{HERE}/shots008.py", encoding="utf-8").read())
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
    os.makedirs(f"{HERE}/shots", exist_ok=True)
    n = len(all_shots())
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(n))
    from multiprocessing import Pool
    with Pool(4) as p:
        for i in p.imap_unordered(render_shot, [(i, f"{HERE}/shots/shot_{i:02d}.mp4") for i in only]): print("done", i, flush=True)

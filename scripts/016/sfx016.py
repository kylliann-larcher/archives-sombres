import json, math, re, numpy as np, wave, unicodedata
SR = 44100
WD = json.load(open("words2.json")); WORDS = WD["words"]; DUR = WD["dur"]
def _n(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn"); return re.sub(r"[^a-z0-9'-]", "", s)
def I(w, after=0):
    w = _n(w)
    for k in range(after, len(WORDS)):
        if _n(WORDS[k]["text"]).startswith(w): return k
def T(i): return WORDS[i]["start"]
N = int(DUR*SR); t = np.arange(N)/SR; rng = np.random.RandomState(16)
def lp(x, k): return np.convolve(x, np.ones(int(k))/int(k), "same")
def put(buf, at, snd, amp=1.0):
    i = int(at*SR)
    if 0 <= i < len(buf): j = min(len(buf), i+len(snd)); buf[i:j] += amp*snd[:j-i]
def boom(L=0.8, f0=65):
    tt = np.arange(int(L*SR))/SR; return np.sin(2*np.pi*(f0*np.exp(-tt*5)+28)*tt)*np.exp(-tt*5) + lp(rng.normal(0,1,len(tt)),30)*np.exp(-tt*14)*0.8
def tick(f=2100, L=0.04):
    tt = np.arange(int(L*SR))/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt*110)*0.5
def whoosh(L=0.3):
    tt = np.arange(int(L*SR))/SR; n = rng.normal(0,1,len(tt)); n = n - lp(n, 25); return n*np.sin(np.pi*tt/L)**1.5*0.25
# musique : nappe grave en mineur + cloche lointaine
mus = np.zeros(N)
for f, a in ((55, 0.5), (65.4, 0.35), (82.4, 0.3), (110, 0.2)):
    mus += a*np.sin(2*np.pi*f*t + 0.3*np.sin(2*np.pi*0.07*t))
mus *= 0.55 + 0.25*np.sin(2*np.pi*0.05*t)
bell = np.zeros(N)
for k in np.arange(0.5, DUR, 6.0):
    L = int(4*SR); tt = np.arange(L)/SR; put(bell, k, (np.sin(2*np.pi*440*tt)+0.5*np.sin(2*np.pi*660*tt))*np.exp(-tt*1.2)*0.12)
mus = mus*0.6 + bell
mus /= np.max(np.abs(mus))
# coupure de musique sur "morte" et "disparu" (0,8 s de silence)
for w in ("morte", "disparu"):
    a = T(I(w)) + 0.4; i0 = int(a*SR); i1 = int((a+0.9)*SR); mus[i0:i1] *= np.linspace(1, 0, i1-i0)**3
sfx = np.zeros(N)
for w, amp in (("l'insomnie", 0.7), ("mille", 1.0), ("meurtre", 1.0), ("traite", 0.5), ("proces", 0.6), ("morte", 1.0), ("donc", 0.7), ("cambrioler", 0.9), ("disparu", 0.8), ("reveillaient", 0.6), ("souvenir", 0.7)):
    k = I(w); put(sfx, T(k), boom(), amp)
# tic-tac sous minuit et sous le reveil de 3 h
for a, b in ((T(I("vers")), T(I("puis", I("vers")))), (T(I("alors")), T(I("toi", I("alors"))))):
    for k, x in enumerate(np.arange(a, b, 0.5)): put(sfx, x, tick(2100 if k % 2 == 0 else 1700), 0.5)
for x in np.arange(0, DUR, 2.8): put(sfx, x, whoosh(), 0.3)
def wr(name, x):
    with wave.open(name, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes())
wr("tension16.wav", mus*0.6); wr("sfx16.wav", sfx/np.max(np.abs(sfx))*0.8); print("sfx ok")

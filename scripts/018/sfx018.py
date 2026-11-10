import json, numpy as np, wave
SR = 44100
WD = json.load(open("words2.json")); WORDS = WD["words"]; DUR = WD["dur"]
def T(i): return WORDS[i]["start"]
N = int(DUR*SR); t = np.arange(N)/SR; rng = np.random.RandomState(18)
def lp(x, k): return np.convolve(x, np.ones(int(k))/int(k), "same")
def put(buf, at, snd, amp=1.0):
    i = int(at*SR)
    if 0 <= i < len(buf): j = min(len(buf), i+len(snd)); buf[i:j] += amp*snd[:j-i]
def boom(L=0.8, f0=65):
    tt = np.arange(int(L*SR))/SR; return np.sin(2*np.pi*(f0*np.exp(-tt*5)+28)*tt)*np.exp(-tt*5) + lp(rng.normal(0,1,len(tt)),30)*np.exp(-tt*14)*0.8
def clink(L=0.25, f=2600):
    tt = np.arange(int(L*SR))/SR; return (np.sin(2*np.pi*f*tt) + 0.6*np.sin(2*np.pi*f*1.5*tt))*np.exp(-tt*25)*0.4
def knock(L=0.12):
    tt = np.arange(int(L*SR))/SR; return (lp(rng.normal(0,1,len(tt)), 6)*np.exp(-tt*60) + np.sin(2*np.pi*900*tt)*np.exp(-tt*50))*0.7
def whoosh(L=0.3):
    tt = np.arange(int(L*SR))/SR; n = rng.normal(0,1,len(tt)); n = n - lp(n, 25); return n*np.sin(np.pi*tt/L)**1.5*0.25
mus = np.zeros(N)
for f, a in ((55, 0.5), (65.4, 0.35), (82.4, 0.3), (98, 0.18)):
    mus += a*np.sin(2*np.pi*f*t + 0.3*np.sin(2*np.pi*0.07*t))
mus *= 0.55 + 0.25*np.sin(2*np.pi*0.05*t)
mus /= np.max(np.abs(mus))
for k in (8, 50, 90):
    a = T(k) + 0.35; i0 = int(a*SR); i1 = int((a+0.8)*SR); mus[i0:i1] *= np.linspace(1, 0, i1-i0)**3
water = np.zeros(N)
sfx = np.zeros(N)
for k, amp in ((3, 0.6), (8, 1.0), (12, 0.6), (23, 0.6), (33, 0.7), (50, 1.0), (52, 0.6), (61, 0.5), (62, 0.5), (64, 0.7), (77, 0.6), (83, 0.6), (90, 1.0), (99, 0.7)):
    put(sfx, T(k), boom(), amp)
for x in np.arange(T(52), T(60), 0.6): put(sfx, x, knock(), 0.35)  # pas
for k in range(3): put(sfx, T(48) + 0.05 + k*0.11, clink(f=1800 + 200*k), 0.5)  # chaines
for x in np.arange(0, DUR, 2.4): put(sfx, x, whoosh(), 0.3)
def wr(name, x):
    with wave.open(name, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes())
wr("tension18.wav", mus*0.6); wr("sfx18.wav", (sfx/np.max(np.abs(sfx))*0.8 + water*0.25)); print("sfx ok")

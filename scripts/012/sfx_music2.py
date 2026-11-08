import json, numpy as np, wave, subprocess
SR = 44100
WD = json.load(open("words2.json")); WORDS = WD["words"]; DUR = WD["dur"]
def T(i): return WORDS[i]["start"] if i < len(WORDS) else DUR
w = wave.open("voix2.wav"); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768; w.close()
N = len(v); t = np.arange(N)/SR
rng = np.random.RandomState(7)

def lp(x, k):  # lissage simple (passe-bas)
    k = max(1, int(k)); return np.convolve(x, np.ones(k)/k, "same")
def put(buf, at, snd, amp=1.0):
    i = int(at*SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(snd)); buf[i:j] += amp*snd[:j-i]

def boom(L=0.7, f0=70):
    tt = np.arange(int(L*SR))/SR
    s = np.sin(2*np.pi*(f0*np.exp(-tt*5) + 28)*tt)*np.exp(-tt*5.5)
    n = lp(rng.normal(0, 1, len(tt)), 30)*np.exp(-tt*14)*0.9
    return s + n
def tick(f=1800, L=0.05):
    tt = np.arange(int(L*SR))/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt*90)*0.6
def whoosh(L=0.16):
    tt = np.arange(int(L*SR))/SR; n = rng.normal(0, 1, len(tt)); n = n - lp(n, 25)
    return n*np.sin(np.pi*tt/L)**1.5*0.35
def swish(L=0.28):
    tt = np.arange(int(L*SR))/SR; n = rng.normal(0, 1, len(tt)); n = lp(n, 6)
    return n*np.sin(np.pi*tt/L)**2*0.5
def crackle(a, b, amp=1.0, dens=60):
    out = np.zeros(N)
    nclk = int((b - a)*dens)
    for _ in range(nclk):
        at = a + rng.rand()*(b - a)
        env = min(1.0, (at - a)/0.6)*min(1.0, (b - at)/0.5)
        L = int(rng.uniform(0.004, 0.02)*SR); s = rng.normal(0, 1, L)*np.exp(-np.arange(L)/(L*0.3))
        put(out, at, s, amp*env*rng.uniform(0.2, 1.0))
    # bruit de fond de feu (souffle)
    i0, i1 = int(a*SR), min(N, int(b*SR))
    if i1 > i0:
        base = lp(rng.normal(0, 1, i1 - i0), 60)*0.5
        ramp = np.minimum(np.linspace(0, 1, i1 - i0)*8, 1)*np.minimum(np.linspace(1, 0, i1 - i0)*5, 1)
        out[i0:i1] += base*ramp*amp*0.8
    return out

# ----- musique de tension (nappe + battement 72 bpm + montees) -----
drone = 0.5*np.sin(2*np.pi*55*t) + 0.3*np.sin(2*np.pi*82.4*t + 0.5*np.sin(2*np.pi*0.1*t)) + 0.15*np.sin(2*np.pi*110*t)
drone *= 0.6 + 0.4*np.sin(2*np.pi*0.07*t)
beat = np.zeros(N); per = 60/72; k = 0
def thud(at, amp=1.0, f=52):
    i = int(at*SR); L = int(0.28*SR)
    if i + L > N: return
    tt = np.arange(L)/SR; beat[i:i+L] += amp*np.sin(2*np.pi*(f*np.exp(-tt*9) + 30)*tt)*np.exp(-tt*14)
while k*per < DUR:
    thud(k*per, 1.0); thud(k*per + 0.22, 0.6); k += 1
rise = np.zeros(N)
def swell(a, b, amp=1.0):
    ia, ib = int(a*SR), min(N, int(b*SR)); n = ib - ia; ramp = np.linspace(0, 1, n)**2
    ns = lp(rng.normal(0, 1, n), 40)
    rise[ia:ib] += amp*ramp*(0.25*ns + 0.5*np.sin(2*np.pi*(110 + 220*ramp)*np.arange(n)/SR))
swell(T(49), T(55), 0.45); swell(T(118), T(123), 0.95); swell(T(135), T(139), 0.5); swell(T(150), T(153), 0.4)
mus = 0.45*drone + 0.55*beat + 0.3*rise
env = lp(np.abs(v), 0.12*SR); env = np.clip(env/(np.percentile(env, 95) + 1e-6), 0, 1)
mus = mus*(1 - 0.62*env); mus = mus/(np.max(np.abs(mus)) + 1e-6)*0.9

# ----- bruitages -----
sfx = np.zeros(N)
IMP = [(3, 0.8), (9, 1.0), (11, 0.7), (15, 0.5), (21, 0.4), (33, 0.7), (41, 0.5), (47, 0.7), (56, 1.0), (77, 0.9), (84, 0.4), (102, 0.7), (109, 1.0), (117, 0.7), (124, 1.2), (134, 0.8), (139, 1.0), (153, 0.7), (169, 0.5)]
for i, a in IMP: put(sfx, T(i), boom(), a*0.9)
TIT = [0.15] + [T(i) for i in (5, 8, 11, 38, 41, 44, 48, 61, 67, 70, 78, 79, 81, 84, 92, 96, 106, 108, 120, 123, 137, 139, 144, 146, 162, 167)]
for a in TIT: put(sfx, a, whoosh(), 0.8)
c0, c1 = T(45), T(48); n = 14
for j in range(n): put(sfx, c0 + j*(c1 - c0)/n, tick(1200 + j*80), 0.5)
for k in range(7): put(sfx, T(80) + 0.12 + k*(T(84) - T(80) - 0.15)/7, tick(900 + k*40), 0.7)
for k in range(5): put(sfx, T(112) + k*(T(117) - T(112) - 0.4)/5, swish(), 0.9)
for k in range(10): put(sfx, T(128) + 0.1 + k*(T(135) - T(128) - 0.8)/10, tick(500, 0.09), 0.7)
sfx += crackle(T(7), T(12), 0.8) + crackle(T(55), T(66), 1.0) + crackle(T(123), T(135), 1.1) + crackle(T(152), T(157), 0.7)
sfx = sfx/(np.max(np.abs(sfx)) + 1e-6)*0.9
for name, arr in (("tension2", mus), ("sfx2", sfx)):
    w = wave.open(f"{name}.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((arr*32767).astype(np.int16).tobytes()); w.close()
print("ok", DUR)

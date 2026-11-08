import json, math, numpy as np, wave, subprocess
SR = 44100
WD = json.load(open("words2.json")); WORDS = WD["words"]; DUR = WD["dur"]
def T(i): return WORDS[i]["start"] if i < len(WORDS) else DUR
w = wave.open("voix2.wav"); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768; w.close()
N = int(DUR*SR); v = np.pad(v, (0, max(0, N - len(v))))[:N]; t = np.arange(N)/SR
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
swell(T(65), T(81), 0.9); swell(T(92), T(107), 0.7); swell(T(171), T(183), 0.4)
mus = 0.45*drone + 0.55*beat + 0.3*rise
env = lp(np.abs(v), 0.12*SR); env = np.clip(env/(np.percentile(env, 95) + 1e-6), 0, 1)
mus = mus*(1 - 0.62*env); mus = mus/(np.max(np.abs(mus)) + 1e-6)*0.9

# ----- bruitages -----
sfx = np.zeros(N)
IMPACTS = eval(open("v11_shots.py", encoding="utf-8").read().split("IMPACTS = ")[1])
for i, amp, col in IMPACTS: put(sfx, T(i), boom(0.7, 60 if amp > 18 else 75), min(1.2, amp/22))
TIT = [0.02] + [T(i) for i in (6, 12, 16, 33, 35, 38, 66, 71, 79, 113, 116, 124, 140, 145, 155, 159, 178, 181)]
for a in TIT: put(sfx, a, whoosh(), 0.8)
# porte du cachot qui claque
put(sfx, T(45), boom(0.5, 90), 1.1)
# grondement du volcan (rumble grave)
i0, i1 = int(T(65)*SR), int(T(92)*SR)
if i1 > i0:
    n = i1 - i0; r = lp(rng.normal(0, 1, n), 400)*6.0
    sfx[i0:i1] += r*np.minimum(np.linspace(0, 1, n)*3, 1)*np.minimum(np.linspace(1, 0, n)*6, 1)*np.linspace(0.4, 1.0, n)
# explosion + souffle de la nuee
put(sfx, T(81), boom(1.4, 45), 1.6)
for k in range(5): put(sfx, T(81) + 0.25*k, boom(0.9, 55 + 10*k), 0.6)
i0, i1 = int(T(82)*SR), int(T(92)*SR)
if i1 > i0:
    n = i1 - i0; r = lp(rng.normal(0, 1, n), 60)*2.2
    sfx[i0:i1] += r*np.minimum(np.linspace(0, 1, n)*4, 1)*np.minimum(np.linspace(1, 0, n)*4, 1)
# chaleur : crepitements et souffle dans le cachot
sfx += crackle(T(92), T(112), 1.0, 70) + crackle(T(112), T(119), 0.6, 40)
# respiration (souffle doux) quand il respire encore
for k in range(3):
    put(sfx, T(119) + 0.2 + k*1.3, whoosh(0.9), 0.5)
# jours qui passent : ticks
for k in range(4): put(sfx, T(124) + k*(T(130) - T(124))/4, tick(700, 0.12), 0.9)
# sauveteurs (pas sur les gravats)
for k in range(10): put(sfx, T(131) + k*0.3, tick(300, 0.06), 0.8)
# foule du cirque
def murmur(a, b, amp=0.6):
    i0, i1 = int(a*SR), min(N, int(b*SR)); n = i1 - i0
    if n <= 0: return
    x = lp(rng.normal(0, 1, n), 18) - lp(rng.normal(0, 1, n), 120)
    m = 0.6 + 0.4*np.sin(2*np.pi*np.cumsum(rng.uniform(1.5, 4, n))/SR)
    r = np.minimum(np.linspace(0, 1, n)*4, 1)*np.minimum(np.linspace(1, 0, n)*3, 1)
    sfx[i0:i1] += x*m*r*amp
murmur(T(139), T(164), 0.9)
# roues du chariot
i0, i1 = int(T(139)*SR), int((T(139) + 2.2)*SR)
sfx[i0:i1] += lp(rng.normal(0, 1, i1 - i0), 220)*3.0*np.minimum(np.linspace(1, 0, i1 - i0)*3, 1)
sfx = sfx/(np.max(np.abs(sfx)) + 1e-6)*0.9
for name, arr in (("tension11", mus), ("sfx11", sfx)):
    w = wave.open(f"{name}.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((arr*32767).astype(np.int16).tobytes()); w.close()
print("ok", DUR)

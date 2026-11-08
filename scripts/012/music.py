import numpy as np, subprocess, wave, json
SR = 44100
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","voix.mp3","-ac","1","-ar",str(SR),"voix.wav"],check=True)
w = wave.open("voix.wav"); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768; w.close()
N = len(v); T = N/SR
t = np.arange(N)/SR
# nappe grave
drone = 0.5*np.sin(2*np.pi*55*t) + 0.3*np.sin(2*np.pi*82.4*t+0.5*np.sin(2*np.pi*0.1*t)) + 0.15*np.sin(2*np.pi*110*t)
drone *= 0.6 + 0.4*np.sin(2*np.pi*0.07*t)
# battement 72 bpm (double thud)
beat = np.zeros(N); period = 60/72
def thud(at, amp=1.0, f=52):
    i = int(at*SR); L = int(0.28*SR)
    if i+L > N: return
    tt = np.arange(L)/SR
    beat[i:i+L] += amp*np.sin(2*np.pi*(f*np.exp(-tt*9)+30)*tt)*np.exp(-tt*14)
k = 0
while k*period < T:
    thud(k*period, 1.0); thud(k*period+0.22, 0.6); k += 1
# montees avant twists : 43.0->46.0 (1709), 54.0->? et coups sur impacts
rise = np.zeros(N)
def swell(a, b, amp=1.0):
    ia, ib = int(a*SR), int(b*SR)
    n = ib-ia; ramp = np.linspace(0,1,n)**2
    ns = np.random.RandomState(1).normal(0,1,n)
    # bruit filtre grossierement
    ns = np.convolve(ns, np.ones(40)/40, "same")
    rise[ia:ib] += amp*ramp*(0.25*ns + 0.5*np.sin(2*np.pi*(110+220*ramp)*np.arange(n)/SR))
swell(43.2, 46.1, 0.9); swell(26.0, 27.2, 0.4); swell(54.0, 56.6, 0.5)
for at, amp in ((0.5, 1.6), (2.7, 1.4), (46.1, 1.8), (27.2, 1.2), (31.4, 1.0), (53.3, 1.3), (14.0,1.0)):
    thud(at, amp, 46)
mus = 0.45*drone + 0.55*beat + 0.3*rise
# ducking sous la voix
env = np.convolve(np.abs(v), np.ones(int(0.12*SR))/int(0.12*SR), "same")
env = np.clip(env/ (np.percentile(env, 95)+1e-6), 0, 1)
duck = 1 - 0.62*env
mus = mus*duck
mus /= np.max(np.abs(mus))+1e-6
mus *= 0.9
out = (mus*32767).astype(np.int16)
w = wave.open("tension.wav","wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
print("ok", T)

import json, re, numpy as np, subprocess, wave
raw = json.load(open("words_raw.json"))
if isinstance(raw, dict): raw = raw.get("words", raw)
words = [w for w in raw if w.get("type", "word") == "word" and re.search(r"\w", w["text"])]
sr = 44100
a = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "voix.wav", "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True).stdout, np.int16).astype(np.float32)/32768
hop = int(0.01*sr); n = len(a)//hop
rms = np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2) + 1e-12) for i in range(n)])
db = 20*np.log10(rms); thr = db.max() - 42
sil = db < thr
LONG = [14, 31, 83, 90, 153, 156, 177, 185]
# segments silencieux
cuts = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        L = (j - i)*0.01
        if L > 0.32 and i > 0 and j < n:
            keep = 0.22
            mid = (i + j)*0.005
            for k in LONG:  # pauses dramatiques conservees
                if words[k]["start"] - 0.05 <= mid <= words[k+1]["start"] + 0.05 and words[k]["start"] < mid: keep = min(L, 0.5)
            cuts.append((i*0.01 + keep/2, j*0.01 - keep/2))
        i = j
    else: i += 1
def remap(t):
    sh = 0.0
    for (c0, c1) in cuts:
        if t >= c1: sh += c1 - c0
        elif t > c0: sh += t - c0
    return t - sh
# assemble audio
segs = []; prev = 0.0
for c0, c1 in cuts:
    segs.append(a[int(prev*sr):int(c0*sr)]); prev = c1
segs.append(a[int(prev*sr):])
# petits fondus aux raccords
out = []
for s in segs:
    s = s.copy(); f = min(len(s)//2, int(0.008*sr))
    if f > 0: s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
    out.append(s)
b = np.concatenate(out)
with wave.open("voix2.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(b, -1, 1)*32767).astype(np.int16).tobytes())
W2 = [dict(text=w["text"], start=round(remap(w["start"]), 3), end=round(remap(w["end"]), 3)) for w in words]
dur = len(b)/sr + 0.6
json.dump(dict(words=W2, dur=dur, cuts=cuts), open("words2.json", "w"), ensure_ascii=False, indent=0)
print("cuts", len(cuts), "removed %.2f s" % sum(c1-c0 for c0, c1 in cuts), "dur", round(dur, 2), "words", len(W2))
for i, w in enumerate(W2): print(i, w["text"], w["start"], end=" | ")

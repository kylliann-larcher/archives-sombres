"""Video 017 : decoupe la voix en phrases (pauses detectees), raccourcit les pauses, repartit les mots au prorata des lettres."""
import json, re, wave, subprocess, numpy as np
sr = 44100
a = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "voix.wav", "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True).stdout, np.int16).astype(np.float32)/32768
hop = int(0.01*sr); n = len(a)//hop
db = 20*np.log10(np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2) + 1e-12) for i in range(n)]))
sil = db < db.max() - 38
gaps = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        if j - i >= 15: gaps.append((i/100, j/100))
        i = j
    else: i += 1
on = 0
while sil[on]: on += 1
start0 = max(0, on/100 - 0.02)
PH = ["Si tu me vois,", "pleure.", "C'est gravé sur une pierre.", "Et le pire,", "c'est qu'elle continue de sortir de l'eau.",
      "Elle dort au fond de l'Elbe,", "en Tchéquie.", "Autrefois,", "on ne la voyait que quand le fleuve était presque à sec.",
      "Alors, à chaque fois,", "quelqu'un y gravait l'année.", "Et ses initiales.", "Parce qu'un fleuve à sec, ça voulait dire :",
      "récoltes perdues,", "prix qui flambent...", "et la faim.", "On les appelle les pierres de la faim.", "Sur celle-ci :",
      "1616.", "1707.", "1893.", "Et en 2018,", "puis en 2022...", "elle est encore ressortie.", "Et toi,", "tu graverais quoi dessus ?",
      "N'hésite pas à t'abonner si tu aimes ce genre de contenu."]
assert len(PH) == len(gaps) + 1, (len(PH), len(gaps))
# segments parles
spans = []; prev = start0
for g0, g1 in gaps: spans.append((prev, g0)); prev = g1
end = n/100
while sil[int(end*100) - 1]: end -= 0.01
spans.append((prev, end + 0.05))
# pauses gardees : 0,22 s, sauf pauses dramatiques
KEEP = {1: 0.35, 14: 0.45, 22: 0.5, 23: 0.3}  # avant "pleure", avant "et la faim", avant "elle est encore ressortie", avant "Et toi"
segs = []; words = []; t = 0.0
for k, (s0, s1) in enumerate(spans):
    if k > 0:
        p = KEEP.get(k - 1 + 1 - 1, None)
    gap = 0.0 if k == 0 else KEEP.get(k - 1, 0.22)
    if k > 0:
        g = np.zeros(int(gap*sr), np.float32); segs.append(g); t += gap
    seg = a[int(s0*sr):int(s1*sr)].copy(); f = int(0.008*sr); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    segs.append(seg)
    toks = PH[k].replace(" :", ":").replace(" ?", "?").split()
    toks = [w for w in toks if re.search(r"\w", w)]
    L = [len(re.sub(r"\W", "", w)) + (5 if re.match(r"^\d{4}", w) else 1) for w in toks]
    dur = s1 - s0; tot = sum(L); acc = 0
    for w, l in zip(toks, L):
        ws = t + dur*acc/tot; acc += l; we = t + dur*acc/tot
        words.append(dict(text=w.replace(":", " :").replace("?", " ?").strip(), start=round(ws, 3), end=round(we, 3), ph=k))
    t += dur
b = np.concatenate(segs)
with wave.open("voix2.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(b, -1, 1)*32767).astype(np.int16).tobytes())
DUR = len(b)/sr + 0.6
json.dump(dict(words=words, dur=DUR), open("words2.json", "w"), ensure_ascii=False, indent=0)
print("dur", round(DUR, 2), "mots", len(words))
for i, w in enumerate(words): print(i, w["text"], w["start"], end=" | ")

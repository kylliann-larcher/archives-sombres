"""Sous-titres 017 : groupes de 3 mots max, coupes aux fins de phrase, mot actif en jaune. Hook et question masques (titres a l'ecran)."""
import json, re
def ass_time(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
d = json.load(open("words2.json")); W = d["words"]; dur = d["dur"]
mask = set(range(0, 5)) | set(range(91, 97))
sent = []; cur = []
for k, w in enumerate(W):
    cur.append(k)
    if k == len(W) - 1 or W[k+1]["ph"] != w["ph"] or re.search(r"[.?!…:,]$", w["text"]): sent.append(cur); cur = []
groups = []
for sn in sent:
    L = len(sn); m = -(-L//3); base, extra = divmod(L, m); p = 0
    for c in range(m):
        size = base + (1 if c < extra else 0); groups.append(sn[p:p+size]); p += size
hdr = open("cap_header.txt", encoding="utf-8").read()
lines = [f"Dialogue: 1,{ass_time(0)},{ass_time(dur)},Stamp,,0,0,0,,ARCHIVE N° 017",
         f"Dialogue: 1,{ass_time(0)},{ass_time(dur)},Track,,0,0,0,,TCHÉQUIE · DEPUIS 1616"]
for grp in groups:
    vis = [g for g in grp if g not in mask]
    if not vis: continue
    g_end = W[grp[-1]]["end"]
    for a, k in enumerate(vis):
        s = W[k]["start"]; e = min(W[vis[a+1]]["start"] if a + 1 < len(vis) else g_end + 0.15, W[k]["end"] + 0.4)
        parts = [("{\\c&H0000D7FF&}" + W[g]["text"].upper() + "{\\c&HFFFFFF&}") if g == k else W[g]["text"].upper() for g in vis]
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(max(e, s + 0.05))},Cap,,0,0,0,,{{\\an5\\pos(470,760)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{' '.join(parts)}")
open("cap17.ass", "w", encoding="utf-8").write(hdr + "\n".join(lines) + "\n")
print(len(groups), "groupes")

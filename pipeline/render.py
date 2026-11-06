#!/usr/bin/env python3
"""Montage Archives Sombres : images fixes (Ken Burns) + voix + sous-titres animes -> MP4 1080x1920.

Usage: python3 render.py spec.json out.mp4
spec.json:
{
  "audio": "voix.mp3",                      # voix ElevenLabs (ou fichier test)
  "music": "tension.mp3",                    # optionnel, mixe a -18 dB
  "stamp": "ARCHIVE N° 010",                # optionnel, tampon en haut (hors zone 0-270 px: place a y=300)
  "part": "PARTIE 1",                        # optionnel
  "scenes": [ {"image": "a.png", "start": 0.0, "end": 4.2}, ... ],
  "words": [ {"w": "Il", "start": 0.0, "end": 0.2}, ... ]   # timings mot a mot (transcription)
}
Zones de securite: texte entre y=270 et y=1248, colonne droite libre (x < 940).
"""
import json, subprocess, sys, os, tempfile

W, H, FPS = 1080, 1920, 30
FONT = "Poppins"

def ass_time(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def build_ass(words, stamp, part, duration, path):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{FONT},84,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,2,5,70,140,0,1
Style: Stamp,{FONT},46,&H0000D7FF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,3,0,1,4,0,8,70,140,300,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = []
    if stamp or part:
        txt = " - ".join(x for x in (stamp, part) if x)
        ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(duration)},Stamp,,0,0,0,,{txt}")
    # groupes de 3 mots max, un seul calque de texte, mot actif en jaune
    i = 0
    while i < len(words):
        grp = words[i:i + 3]
        i += 3
        g_start, g_end = grp[0]["start"], grp[-1]["end"]
        for k, w in enumerate(grp):
            s = w["start"]
            e = grp[k + 1]["start"] if k + 1 < len(grp) else g_end
            parts = []
            for j, ww in enumerate(grp):
                word = ww["w"].upper().replace("{", "").replace("}", "")
                parts.append(("{\\c&H0000D7FF&}" + word + "{\\c&HFFFFFF&}") if j == k else word)
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(max(e, s + 0.05))},Cap,,0,0,0,,{{\\an5\\pos(470,760)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{' '.join(parts)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(hdr + "\n".join(ev) + "\n")

def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", P(spec["audio"])]).strip())
    scenes = spec["scenes"]
    scenes[-1]["end"] = max(scenes[-1]["end"], dur)
    tmp = tempfile.mkdtemp()
    ass = os.path.join(tmp, "cap.ass")
    build_ass(spec["words"], spec.get("stamp"), spec.get("part"), dur, ass)

    inputs, filters, labels = [], [], []
    for n, sc in enumerate(scenes):
        d = max(sc["end"] - sc["start"], 0.5)
        frames = int(d * FPS) + 1
        inputs += ["-loop", "1", "-t", f"{d:.2f}", "-i", P(sc["image"])]
        zoom = f"min(zoom+0.0007,1.25)" if n % 2 == 0 else f"if(eq(on,1),1.25,max(zoom-0.0007,1.0))"
        filters.append(f"[{n}:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
                       f"zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
                       f"eq=brightness=-0.08:saturation=0.85,setsar=1[v{n}]")
        labels.append(f"[v{n}]")
    filters.append("".join(labels) + f"concat=n={len(scenes)}:v=1:a=0[bg]")
    filters.append(f"[bg]ass={ass}:fontsdir=/usr/share/fonts/truetype/google-fonts[vid]")
    inputs += ["-i", P(spec["audio"])]
    a_idx = len(scenes)
    if spec.get("music"):
        inputs += ["-stream_loop", "-1", "-i", P(spec["music"])]
        filters.append(f"[{a_idx}:a]volume=1.0[va];[{a_idx+1}:a]volume=0.12[ma];[va][ma]amix=inputs=2:duration=first:normalize=0[aud]")
        amap = "[aud]"
    else:
        amap = f"{a_idx}:a"
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[vid]", "-map", amap,
           "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("OK", out, f"{dur:.1f}s")

if __name__ == "__main__":
    main()

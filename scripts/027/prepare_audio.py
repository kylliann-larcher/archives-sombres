from pathlib import Path
import json, math, re, subprocess, wave
import numpy as np

HERE=Path(__file__).resolve().parent
SR=44100
# Prise 027 à la vitesse 1,15 : sans accélération au montage (sinon moins de 35 s).
TEMPO=1.0
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(HERE/'voice/voice.mp3'),'-af',f'atempo={TEMPO}','-f','s16le','-ac','1','-ar',str(SR),'-'])
a=np.frombuffer(raw,np.int16).astype(np.float64)/32768
j=json.loads((HERE/'voice/alignment.json').read_text(encoding='utf-8'))
al=j['alignment']
txt=''.join(al['characters'])
start=[t/TEMPO for t in al['character_start_times_seconds']]; end=[t/TEMPO for t in al['character_end_times_seconds']]
# Locate the actual silence before CTA, not the punctuation's synthetic timing.
ci=txt.index("N'h");qi=txt.rindex('?',0,ci)
lo,hi=end[qi]-.2,start[ci]+.15
hop=441
rms=np.array([np.sqrt(np.mean(a[i:i+hop]**2)+1e-12) for i in range(0,len(a),hop)])
quiet=rms<rms.max()*10**(-36/20)
gaps=[]; i=int(lo*100)
while i<min(int(hi*100),len(quiet)):
    if quiet[i]:
        k=i
        while i<len(quiet) and quiet[i]:i+=1
        gaps.append((k/100,i/100))
    else:i+=1
g0,g1=max(gaps,key=lambda g:g[1]-g[0])
if g1-g0<.15:raise RuntimeError('No safe CTA gap')
first=int(np.flatnonzero(~quiet)[0])/100
trim=max(0,first-.015)
cut0,cut1=int(g0*SR),int(g1*SR)
gap=np.zeros(round(.5*SR))
v=np.concatenate([a[int(trim*SR):cut0],gap,a[cut1:]])
offset=.5-(g1-g0)
def shift(t):
    if t<=g0:return max(0,t-trim)
    if t>=g1:return t+offset-trim
    return g0-trim+(t-g0)*.5/(g1-g0)
words=[]; ph=0
for m in re.finditer(r'\S+',txt):
    text=m[0]
    if not re.search(r'\w',text):
        if words:
            words[-1]['text']+=text
            if text.endswith(('.','!')) and not words[-1]['text'][:-len(text)].endswith(('.','?','!')):ph+=1
        continue
    ws=shift(start[m.start()]); we=shift(end[m.end()-1])
    words.append(dict(text=text,start=round(ws,4),end=round(min(len(v)/SR,we),4),ph=ph))
    if text.endswith(('.', '?', '!')):ph+=1
# The service splits accented letters into separate fragments: regroup them on the script's own words.
key=lambda s:re.sub(r'[\W_]','',s)
script=[]
for tok in (HERE/'script-intended.txt').read_text(encoding='utf-8-sig').split():
    if re.search(r'\w',tok):script.append(tok)
    elif script:script[-1]+=tok
merged=[];i=0;ph=0
for tok in script:
    acc='';first=i
    while key(acc)!=key(tok):
        acc+=words[i]['text'];i+=1
        if len(key(acc))>len(key(tok)):raise RuntimeError('Alignment mismatch at '+tok)
    clean=tok.replace('«','').replace('»','')
    merged.append(dict(text=clean,start=words[first]['start'],end=words[i-1]['end'],ph=ph))
    if clean.endswith(('.','?','!')):ph+=1
if i!=len(words):raise RuntimeError('Unconsumed alignment fragments')
words=merged
qph=next(w['ph'] for w in reversed(words) if w['text'].endswith('?'))
question_start=next(w['start'] for w in words if w['ph']==qph)
# Standalone question mark was folded in; split the final CTA by its actual word.
abo=next(k for k,w in enumerate(words) if w['text'].startswith("N'h"))
for w in words[abo:]:w['ph']=qph+1
dur=math.ceil((len(v)/SR+.55)*30)/30
v=np.pad(v,(0,round(dur*SR)-len(v)))
with wave.open(str(HERE/'voice-edit.wav'),'wb') as out:
    out.setnchannels(1);out.setsampwidth(2);out.setframerate(SR)
    out.writeframes((np.clip(v,-1,1)*32767).astype(np.int16).tobytes())
data=dict(question_ph=qph,words=words,dur=dur,question_start=question_start,cta_start=words[abo]['start'],pause_start=g0-trim,pause_end=g0-trim+.5,trim=trim,original_gap=[g0,g1],method='ElevenLabs native character alignment, split on whitespace, verified silence gap replaced by exactly 0.5s')
(HERE/'words2.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('DURATION',dur,'CTA_PAUSE',.5,'TRIM',trim,'ORIGINAL_GAP',g0,g1)
for k,w in enumerate(words):print(k,w['text'],w['start'],w['end'],w['ph'])

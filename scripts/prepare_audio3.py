"""Alignement Scribe -> words2.json + voice-edit.wav (voix v3 calme). Usage: python3 prepare_audio3.py 025"""
from pathlib import Path
import json, math, re, subprocess, sys, wave, shutil
import numpy as np
N=sys.argv[1]; HERE=Path(__file__).resolve().parent/N; SR=44100
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(HERE/'voice-v3/voice.mp3'),'-f','s16le','-ac','1','-ar',str(SR),'-'])
a=np.frombuffer(raw,np.int16).astype(np.float64)/32768
sc=json.loads((HERE/'voice-v3/scribe.json').read_text(encoding='utf-8'))
sw=[w for w in (sc['words'] if isinstance(sc,dict) else sc) if w.get('type','word')=='word' and re.search(r'\w',w['text'])]
script=[]
for tok in (HERE/f'script-voix-{N}.txt').read_text(encoding='utf-8-sig').split():
    if re.search(r'\w',tok):script.append(tok)
    elif script:script[-1]+=tok
if len(script)!=len(sw):raise RuntimeError(f'token mismatch script={len(script)} scribe={len(sw)}')
abo=next(k for k,t in enumerate(script) if t.startswith("N'h"))
lo=sw[abo-1]['end']-.05; hi=sw[abo]['start']+.15
hop=441
rms=np.array([np.sqrt(np.mean(a[i:i+hop]**2)+1e-12) for i in range(0,len(a),hop)])
quiet=rms<rms.max()*10**(-36/20)
gaps=[];i=int(lo*100)
while i<min(int(hi*100),len(quiet)):
    if quiet[i]:
        k=i
        while i<len(quiet) and quiet[i]:i+=1
        gaps.append((k/100,i/100))
    else:i+=1
if not gaps:raise RuntimeError('No safe CTA gap')
g0,g1=max(gaps,key=lambda g:g[1]-g[0])
if g1-g0<.15:raise RuntimeError('CTA gap too short %.2f'%(g1-g0))
first=int(np.flatnonzero(~quiet)[0])/100; trim=max(0,first-.015)
cut0,cut1=int(g0*SR),int(g1*SR)
v=np.concatenate([a[int(trim*SR):cut0],np.zeros(round(.5*SR)),a[cut1:]])
offset=.5-(g1-g0)
def shift(t):
    if t<=g0:return max(0,t-trim)
    if t>=g1:return t+offset-trim
    return g0-trim+(t-g0)*.5/(g1-g0)
words=[];ph=0
for tok,w in zip(script,sw):
    clean=tok.replace('«','').replace('»','')
    words.append(dict(text=clean,start=round(shift(w['start']),4),end=round(min(len(v)/SR,shift(w['end'])),4),ph=ph))
    if clean.endswith(('.','?','!')):ph+=1
qph=next(w['ph'] for w in reversed(words[:abo]) if w['text'].endswith('?'))
question_start=next(w['start'] for w in words if w['ph']==qph)
for w in words[abo:]:w['ph']=qph+1
dur=max(math.ceil((len(v)/SR+.55)*30)/30,math.ceil(35.6*30)/30)
v=np.pad(v,(0,round(dur*SR)-len(v)))
if (HERE/'words2.json').exists() and not (HERE/'words2-v2.json').exists():shutil.copy(HERE/'words2.json',HERE/'words2-v2.json')
with wave.open(str(HERE/'voice-edit.wav'),'wb') as out:
    out.setnchannels(1);out.setsampwidth(2);out.setframerate(SR);out.writeframes((np.clip(v,-1,1)*32767).astype(np.int16).tobytes())
data=dict(question_ph=qph,words=words,dur=dur,question_start=question_start,cta_start=words[abo]['start'],pause_start=g0-trim,pause_end=g0-trim+.5,trim=trim,original_gap=[g0,g1],method='ElevenLabs Scribe word timings, voice v3 (calm), CTA gap set to 0.5s')
(HERE/'words2.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(N,'DURATION',dur,'GAP',g0,g1,'words',len(words),'qph',qph)

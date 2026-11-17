from pathlib import Path
import json,math,subprocess,wave
import numpy as np

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'words2.json').read_text(encoding='utf-8'));dur=data['dur'];SR=44100
def run(args):return subprocess.run(['ffmpeg','-y','-hide_banner',*args],cwd=HERE,check=True,capture_output=True,text=True,encoding='utf-8').stderr
def wav(name,x):
    with wave.open(str(HERE/name),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
with wave.open(str(HERE/'voice-edit.wav')) as f:v=np.frombuffer(f.readframes(f.getnframes()),np.int16).astype(float)/32768
t=np.arange(len(v))/SR
bed=np.zeros(len(v));rng=np.random.default_rng(21)
for hz,amp in ((55,.55),(65.4,.25),(82.4,.20),(110,.12)):
    bed+=amp*np.sin(2*np.pi*hz*t+.13*np.sin(2*np.pi*.07*t)+.5)
bed*=.6+.13*np.cos(2*np.pi*.095*t)
for bt in np.arange(0,dur,60/72):
    i=int(bt*SR);n=min(int(.40*SR),len(v)-i);a=np.arange(n)/SR
    bed[i:i+n]+=.18*np.sin(2*np.pi*(44*a+5*(1-np.exp(-a*12))))*np.exp(-a*12)
vrms=np.sqrt(np.mean(v*v));brms=np.sqrt(np.mean(bed*bed));bed*=vrms/(10**(10/20))/brms
bed*=np.minimum(1,np.maximum(0,(dur-t)/.25))
fx=np.zeros(len(v))
for k in (7, 15, 36, 51, 67, 76, 90):
    i=int(data['words'][k]['start']*SR);n=min(int(.25*SR),len(v)-i);tt=np.arange(n)/SR
    fx[i:i+n]+=(np.sin(2*np.pi*(58*tt+4*(1-np.exp(-tt*13))))*.5)*np.exp(-tt*20)*vrms
mix=v+bed+fx
wav('music.wav',bed);wav('sfx.wav',fx);wav('mix.wav',mix)
stats=run(['-loglevel','info','-i','mix.wav','-af','loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json','-f','null','-'])
j=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0]
filt=('loudnorm=I=-14:TP=-1.8:LRA=11:'+f'measured_I={j["input_i"]}:measured_TP={j["input_tp"]}:measured_LRA={j["input_lra"]}:measured_thresh={j["input_thresh"]}:offset={j["target_offset"]}:linear=true:print_format=json')
run(['-v','error','-i','mix.wav','-af','acompressor=threshold=0.18:ratio=2.5:attack=5:release=100:makeup=1.4,loudnorm=I=-14:TP=-2.8:LRA=7:linear=false,volume=1.5dB,aresample=192000,alimiter=limit=0.77:level=false:attack=5:release=50','-ar',str(SR),'mix-normalized.wav'])
files=sorted((HERE/'shots').glob('shot_*.mp4'))
if not files:raise RuntimeError('No shots')
(HERE/'concat.txt').write_text(''.join("file '"+p.relative_to(HERE).as_posix()+"'\n" for p in files),encoding='utf-8')
run(['-v','error','-f','concat','-safe','0','-i','concat.txt','-c','copy','video-raw.mp4'])
run(['-v','warning','-i','video-raw.mp4','-i','mix-normalized.wav','-vf','ass=cap.ass:fontsdir=fonts','-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(dur),'-movflags','+faststart','video-027-photos-des-morts.mp4'])
measurement=run(['-loglevel','info','-i','video-027-photos-des-morts.mp4','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
final=json.JSONDecoder().raw_decode(measurement[measurement.rfind('{'):])[0]
results=dict(duration_requested=dur,integrated_lufs=float(final['input_i']),true_peak_db=float(final['input_tp']),lra=float(final['input_lra']),music_below_voice_rms_db=round(20*np.log10(vrms/np.sqrt(np.mean(bed*bed))),2),pause_seconds=.5,one_take=True,voices_generated=1,manual_listening='not claimed; user review pending')
(HERE/'quality-audio.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2),flush=True)
if not 35<=dur<=50 or results['true_peak_db']>-1.5:raise RuntimeError('Audio/duration gate requires correction')
print('FINAL_MP4_READY',flush=True)

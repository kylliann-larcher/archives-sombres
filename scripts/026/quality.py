from pathlib import Path
import json,subprocess,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
review=HERE/'review';frames=review/'frames';frames.mkdir(exist_ok=True)
v=HERE/'video-026-enfants-par-la-poste.mp4'
for old in frames.glob('q-*.png'):old.unlink()
for old in review.glob('contact-*.jpg'):old.unlink()
DUR=json.loads((HERE/'words2.json').read_text(encoding='utf-8'))['dur']
subprocess.run(['ffmpeg','-y','-v','error','-i',str(v),'-vf',r'select=not(mod(n\,15)),crop=1080:700:0:340,scale=648:420','-fps_mode','vfr',str(frames/'q-%03d.png')],check=True)
images=sorted(frames.glob('q-*.png'));font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
for page in range(math.ceil(len(images)/18)):
    sheet=Image.new('RGB',(1944,2676),(16,16,16));d=ImageDraw.Draw(sheet)
    for k,p in enumerate(images[page*18:(page+1)*18]):
        x=(k%3)*648;y=(k//3)*446
        sheet.paste(Image.open(p),(x,y));d.text((x+12,y+421),f'{(page*18+k)*.5:04.1f} s',font=font,fill='white')
    sheet.save(review/f'contact-{page+1}.jpg',quality=94)
for name,pos in [('first',0),('last',DUR-1/30)]:
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(pos),'-i',str(v),'-frames:v','1',str(review/f'{name}-final.png')],check=True)
first=Image.open(review/'first-final.png').convert('RGB');last=Image.open(review/'last-final.png').convert('RGB')
cover=first.copy();cover.save(HERE/'cover-tiktok.png')
d=ImageDraw.Draw(cover);d.line((810,980,610,1070),fill=(220,37,32),width=7);d.polygon([(610,1070),(637,1032),(648,1066)],fill=(220,37,32));cover.save(HERE/'cover-instagram.png')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate','-of','json',str(v)]))
result=dict(samples_every_seconds=.5,samples=len(images),band_y=[340,1040],pages=math.ceil(len(images)/18),first_last_mean_absolute_rgb_error=float(np.abs(np.array(first).astype(float)-np.array(last).astype(float)).mean()),probe=probe)
(review/'quality-visual.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))

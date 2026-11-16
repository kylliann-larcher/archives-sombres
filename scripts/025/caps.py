from pathlib import Path
import json,re
from PIL import ImageFont

HERE=Path(__file__).resolve().parent
wd=json.loads((HERE/'words2.json').read_text(encoding='utf-8'));words=wd['words'];dur=wd['dur']
font=ImageFont.truetype(str(HERE/'fonts/Poppins-Bold.ttf'),74)
def tm(t):
    cs=round(t*100);return f'{cs//360000}:{(cs//6000)%60:02d}:{(cs//100)%60:02d}.{cs%100:02d}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Poppins,74,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,1,5,120,180,0,1
Style: Track,Poppins,34,&H00C4D8E8,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,3,0,7,120,180,370,1
Style: Stamp,Poppins,42,&H0000D7FF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,3,0,1,3,0,7,120,180,300,1
Style: Count,Poppins,76,&H00DCEBF5,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,4,0,1,5,0,7,120,180,262,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''
# Compteur de dates : change quand la voix nomme le siècle ou l'année.
idx=lambda s:next(k for k,w in enumerate(words) if w['text'].startswith(s))
keys=[(words[12]['start'],'XVIe SIÈCLE'),(words[82]['start'],'XVIIIe SIÈCLE')]
def year_at(t):
    lab=keys[0][1]
    for ta,l in keys:
        if t>=ta:lab=l
    return lab
t_end=dur-.3
lines=[f'Dialogue: 1,{tm(0)},{tm(keys[0][0])},Stamp,,0,0,0,,ARCHIVE N° 025',f'Dialogue: 1,{tm(0)},{tm(dur)},Track,,0,0,0,,EUROPE']
t=keys[0][0];step=1/30
while t<t_end:
    y=year_at(t);t2=t
    while t2<t_end and year_at(t2)==y:t2+=step
    lines.append(f'Dialogue: 1,{tm(t)},{tm(min(t2,t_end))},Count,,0,0,0,,{y}');t=t2
# Mots clés en rouge en permanence, dans le style de la référence ; le mot prononcé reste surligné en jaune.
KEY={'MOMIE', 'CADAVRES', 'RÉCENTS', 'BROYÉES', 'MOMIES', 'MUMIA'}
norm=lambda s:re.sub(r'[^\w\']','',s.upper())
groups=[];group=[]
for k,w in enumerate(words):
    if w['ph'] in (0,wd['question_ph']):
        if group:groups.append(group);group=[]
        continue
    candidate=group+[k]
    text=' '.join(words[i]['text'].upper() for i in candidate)
    if group and (len(candidate)>3 or words[group[0]]['ph']!=w['ph'] or font.getlength(text)>620):
        groups.append(group);group=[k]
    else:group=candidate
    if re.search(r'[.?!,]$',w['text']):groups.append(group);group=[]
if group:groups.append(group)
maxw=0
for g in groups:
    text=' '.join(words[i]['text'].upper() for i in g)
    size=min(74,int(74*620/max(620,font.getlength(text))));actual_font=ImageFont.truetype(str(HERE/'fonts/Poppins-Bold.ttf'),size)
    maxw=max(maxw,actual_font.getlength(text))
    next_start=words[g[-1]+1]['start'] if g[-1]+1<len(words) else dur
    group_end=min(words[g[-1]]['end']+.08,next_start-.015,dur-.3)
    for ix,k in enumerate(g):
        start=words[k]['start'];end=words[g[ix+1]]['start'] if ix+1<len(g) else group_end
        chunks=[]
        for pos in g:
            s=words[pos]['text'].upper()
            if norm(s) in KEY:s=r'{\c&H2525DC&}'+s+r'{\c&HFFFFFF&}'
            elif pos==k:s=r'{\c&H0000D7FF&}'+s+r'{\c&HFFFFFF&}'
            chunks.append(s)
        lines.append(f'Dialogue: 0,{tm(start)},{tm(max(start+.025,end))},Cap,,0,0,0,,'+r'{\an5\pos(470,760)'+f'\\fs{size}'+'}'+' '.join(chunks))
(HERE/'cap.ass').write_text(header+'\n'.join(lines)+'\n',encoding='utf-8-sig')
(HERE/'caption-check.json').write_text(json.dumps(dict(groups=len(groups),maximum_width=round(maxw,2),left=round(470-maxw/2-6,2),right=round(470+maxw/2+6,2),hook_and_question_masked=True),indent=2),encoding='utf-8')
print('CAPTIONS',len(groups),'max width',round(maxw,1))

"""Aperçu d'une image au milieu de chaque plan (contrôle avant rendu complet). Usage : python preview_shots.py <dossier>"""
import os, sys
HERE = os.path.abspath(sys.argv[1]); os.chdir(HERE)
src = open('engine.py', encoding='utf-8').read().split('if __name__')[0].replace('HERE = os.path.dirname(os.path.abspath(__file__))', '')
g = {'HERE': HERE, '__name__': 'preview', '__file__': os.path.join(HERE, 'gen_base.py')}; exec(src, g)
from PIL import Image
S = g['all_shots'](); vig = g['vignette_mask'](); thumbs = []
for i, s in enumerate(S):
    ta = g['T'](s['a']) if s['a'] else 0.0
    tb = g['T'](s['b']) if s['b'] < len(g['WORDS']) else g['DUR']
    fr = int(((ta + tb)/2)*30)
    f = g['frame_at'](s, i, fr, int(round(ta*30)), max(.1, tb - ta), vig); thumbs.append(f.resize((360, 640)))
    print(i, s['name'], round(ta, 2), round(tb, 2), round(tb - ta, 2))
sheet = Image.new('RGB', (360*5, 640*((len(thumbs) + 4)//5)))
for k, t in enumerate(thumbs): sheet.paste(t, ((k % 5)*360, (k//5)*640))
os.makedirs('review', exist_ok=True); sheet.save('review/preview-shots.jpg', quality=85)

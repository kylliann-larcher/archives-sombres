import sys,os
sys.argv=['x']
import engine
from PIL import Image
n=len(engine.all_shots());vig=engine.vignette_mask()
sheet=Image.new('RGB',(5*300,3*540),(16,16,16))
for i in range(n):
    S=engine.all_shots()[i];ta=engine.T(S['a']);tb=engine.T(S['b']) if S['b']<len(engine.WORDS) else engine.DUR
    fa=int(ta*30);fr=fa+int((tb-ta)*30*.75)
    f=engine.frame_at(S,i,fr,fa,max(.5,tb-ta),vig).resize((300,533));sheet.paste(f,((i%5)*300,(i//5)*540))
sheet.save('review/preview-sheet.jpg',quality=88)
print(n)

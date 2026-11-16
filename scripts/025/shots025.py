"""Limites de plans = indices de words2.json ; chaque plan a sa propre action lisible."""
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def opening():
        im=shop(250);sarcophagus(im,720,1240,.9);mummy(im,720,1215,.82);return im
    def offer(im,t,fr):
        spoon(im,int(300+8*math.sin(t*2)),int(1090+6*math.cos(t*2.3)),1,1.05)
    add('hook',0,7,opening(),[offer],titles=[('TON REMÈDE :',CREAM,84,0,412),('DE LA MOMIE',RED,100,0,530)])
    im=shop(251);table(im,1180)
    def drink(im,t,fr):
        u=ease((t-T(7))/1.2);cup(im,470,1170,1.1,True,t*90);hand(im,int(700-120*u),int(1080-30*u),1.0,1)
    add('avaler',7,11,im,[drink])
    im=shop(252);table(im,1200)
    def apothecary(im,t,fr):
        person(im,470,1200,.95,coat=(60,40,70),mouth='smile')
        for k,x in enumerate((240,700)):
            if t>=T(11)+.35*k:coins(im,x,1190,3+k,.9)
    add('apothicaires',11,17,im,[apothecary])
    im=shop(259)
    def jar(im,t,fr):
        on=clamp01((t-T(21))/.4)
        if on>0:glow(im,(470,1080),200,(255,200,120),.5*on)
        mumia_jar(im,470,1200);pour(im,700,960,t,T(19))
    add('mumia',17,24,im,[jar])
    im=shop(253);table(im,1200)
    def grind(im,t,fr):
        strips(im,470,830,t);mortar(im,470,1180,t,1.1)
    add('broyees',24,31,im,[grind])
    im=shop(254);table(im,1200)
    def dilute(im,t,fr):
        cup(im,470,1190,1.1,True,t*120);pour(im,470,880,t,T(31))
        person(im,820,1330,.75,coat=(70,60,90),mouth='wide' if t>T(40) else 'flat')
    add('boisson',31,47,im,[dilute])
    im=paper(255,.05,(90,60,90));d=ImageDraw.Draw(im);d.rectangle((0,1240,W,H),fill=(50,30,50,255))
    for x in range(80,1040,120):d.line((x,640,x,1240),fill=(110,80,110,255),width=6)
    def king(im,t,fr):
        wig_face(im,470,1110,.85,crown=True,mood=0);pouch(im,640,1240,1.0,.4+.2*math.sin(t*4))
    add('francois',47,59,im,[king],focus=[(470,1120),(560,1180)])
    im=shop(256);table(im,1200)
    def price(im,t,fr):
        n=int(clamp01((t-T(59))/1.2)*14);coins(im,380,1190,n,1.0);coins(im,560,1190,max(0,n-3),1.0)
        mummy(im,800,1190,.5)
    add('cher',59,65,im,[price])
    im=desert(260)
    def fake(im,t,fr):
        for k,x in enumerate((260,540,820)):covered(im,x,1190+k*8,.75)
        person(im,int(150+40*math.sin(t)),1330,.85,coat=(110,70,40))
        u=clamp01((t-T(73))/.6);crate(im,int(1000-180*u),1230)
    add('faux',65,78,im,[fake],focus=[(470,1100),(540,1150)])
    im=shop(257)
    def empty(im,t,fr):
        mumia_jar(im,470,1200);red_cross(im,470,1080,150,ease((t-T(86))/.5))
    add('xviiie',78,89,im,[empty])
    im=shop(258);table(im,1180)
    def back(im,t,fr):cup(im,470,1170,1.1,True,t*90);hand(im,580,1080,1.0,1)
    add('question',89,94,im,[back],titles=[("TU L'AURAIS",CREAM,84,T(89),412),('BU ?',RED,100,T(89),530)])
    def clean_end(im,t,fr):offer(im,0 if t>DUR-.3 else t,fr)
    add('loop',94,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(6,6,None),(10,4,None),(30,6,None),(46,5,None),(70,5,None),(88,5,None)]
    return shots

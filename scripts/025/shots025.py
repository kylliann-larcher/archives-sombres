"""Limites de plans = indices de words2.json ; chaque plan a sa propre action lisible (v2 enrichie)."""
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def opening():
        im=shop2(250);sarcophagus(im,720,1240,.9);mummy(im,720,1215,.82);return im
    def offer(im,t,fr):
        candle_lit(im,180,1080,t,.9);candle_lit(im,900,1100,t,.8)
        spoon(im,int(300+8*math.sin(t*2)),int(1090+6*math.cos(t*2.3)),1,1.05)
        sparkle(im,330,1080,t,1.2)
    HOOK=[('TON REMÈDE :',CREAM,84,0,412),('DE LA MOMIE',RED,100,0,530)]
    add('hook',0,4,opening(),[offer],titles=HOOK)
    im=shop2(249,croc=False);sarcophagus(im,470,1260,1.15);mummy(im,470,1235,1.05)
    def reveal(im,t,fr):
        glow(im,(470,1000),300,(255,200,120),.25+.1*math.sin(t*6));candle_lit(im,180,1150,t,.9);candle_lit(im,770,1150,t,.9)
    add('hook2',4,7,im,[reveal],titles=HOOK,focus=[(470,1060),(470,1020)])
    im=shop2(251);table(im,1200)
    def drink(im,t,fr):
        u=ease((t-T(7))/.9)
        actor(im,360,1330,.95,t,kind='worried',mouth='wide' if u>.6 else 'flat',coat=(70,60,90))
        cup(im,int(640-150*u),int(1250-70*u),.7,True,t*90);candle_lit(im,860,1150,t,.8)
    add('avaler',7,11,im,[drink],focus=[(470,1060),(420,1040)])
    im=shop2(252);table(im,1200)
    def apothecary(im,t,fr):
        actor(im,330,1210,.9,t,kind='up',mouth='smile',coat=(60,40,70))
        balance(im,700,1200,t)
        for k,x in enumerate((140,880)):candle_lit(im,x,1120,t,.7)
    add('apothicaires',11,17,im,[apothecary])
    im=shop2(248);table(im,1200)
    def powder(im,t,fr):
        cup(im,470,1190,.9,False);pour(im,470,880,t,T(17));actor(im,780,1330,.8,t,kind='up',mouth='smile',coat=(60,40,70))
        candle_lit(im,180,1150,t,.8)
    add('poudre',17,21,im,[powder])
    im=shop2(259,croc=False)
    def jar(im,t,fr):
        on=clamp01((t-T(21))/.4)
        rays(im,470,640,t,(255,214,140),3,20,700,.12+.1*on)
        if on>0:glow(im,(470,1080),220,(255,200,120),.55*on)
        mumia_jar(im,470,1200);pour(im,700,960,t,T(19))
        for k in range(3):sparkle(im,400+k*70,1000-k*30,t+k,1.0)
        candle_lit(im,220,1150,t,.8)
    add('mumia',21,24,im,[jar])
    im=shop2(253);table(im,1200)
    def grind(im,t,fr):
        mummy(im,820,1190,.45);strips(im,470,830,t);mortar(im,470,1180,t,1.1)
        puff(im,470,1110,t,T(27),POWDER,12,180);puff(im,470,1110,t,T(29),POWDER,10,150)
    add('broyees',24,31,im,[grind])
    im=shop2(254);table(im,1200)
    def dilute(im,t,fr):
        cup(im,420,1190,1.1,True,t*120);pour(im,420,880,t,T(31))
        k='worried' if t<T(44) else 'up'
        actor(im,790,1330,.8,t,kind=k,mouth='wide' if T(37)<t<T(41) else 'flat',coat=(70,60,90))
        hand(im,860,1010,.55,1,(70,60,90)) if T(37)<t<T(41) else None
        candle_lit(im,170,1150,t,.75)
    add('boisson',31,47,im,[dilute])
    im=throne_room(255)
    def king(im,t,fr):
        for x in (190,750):candle_lit(im,x,1180,t,1.0)
        wig_face(im,470,1110,.85,crown=True,mood=0);pouch(im,640,1240,1.0,.4+.2*math.sin(t*4))
        sparkle(im,700,1200,t,1.3);sparkle(im,600,1180,t+1,1.0)
    add('francois',47,59,im,[king],focus=[(470,1120),(560,1180)])
    im=shop2(256);table(im,1200)
    def price(im,t,fr):
        n=int(clamp01((t-T(59))/1.2)*14);coins(im,330,1190,n,1.0);coins(im,500,1190,max(0,n-3),1.0)
        for k in range(3):sparkle(im,330+k*90,1190-n*16,t+k,1.1)
        actor(im,780,1330,.85,t,kind='angry',mouth='smile',coat=(110,70,40))
    add('cher',59,65,im,[price])
    im=desert(260);pyramids(im,1040)
    def fake(im,t,fr):
        heat(im,t);vulture(im,int(300+120*math.sin(t*.4)),760,t);vulture(im,int(640+90*math.cos(t*.5)),720,t+1)
        for k,x in enumerate((300,560,800)):covered(im,x,1200+k*8,.7)
        actor(im,150,1330,.85,t,kind='angry',mouth='smile',coat=(110,70,40))
        u=clamp01((t-T(73))/.6);crate(im,int(1000-180*u),1240)
    add('faux',65,78,im,[fake],focus=[(470,1100),(540,1150)])
    im=shop2(257,croc=False)
    def empty(im,t,fr):
        mumia_jar(im,470,1200);red_cross(im,470,1080,150,ease((t-T(86))/.5))
        puff(im,470,1100,t,T(86),(120,100,80),10,170);candle_lit(im,200,1150,t,.8);candle_lit(im,760,1150,t,.8)
    add('xviiie',78,89,im,[empty])
    im=shop2(258);table(im,1200)
    def back(im,t,fr):
        actor(im,360,1330,.95,t,kind='up',mouth='flat',coat=(70,60,90))
        cup(im,640,1180,.85,True,t*90);sparkle(im,640,990,t,1.2);candle_lit(im,860,1150,t,.8)
    add('question',89,94,im,[back],titles=[("TU L'AURAIS",CREAM,84,T(89),412),('BU ?',RED,100,T(89),530)])
    def clean_end(im,t,fr):offer(im,0 if t>DUR-.3 else t,fr)
    add('loop',94,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(6,6,None),(10,4,None),(30,6,None),(46,5,None),(70,5,None),(88,5,None)]
    return shots

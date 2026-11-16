"""Limites de plans = indices de words2.json ; chaque plan a sa propre action lisible (v2 enrichie)."""
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def opening():return parlor2(270,False)
    def photo_hook(im,t,fr):
        candle_lit(im,150,1120,t,.85);candle_lit(im,800,1120,t,.85)
        frame_photo(im,470,1000,520,600,'standing',t)
        glow(im,(410,1000),160,(255,240,200),.12+.08*math.sin(t*5))
    HOOK=[('ILS SERAIENT',CREAM,84,0,412),('DÉJÀ MORTS',RED,100,0,530)]
    add('hook',0,4,opening(),[photo_hook],titles=HOOK)
    im=parlor2(283,False)
    def closeup(im,t,fr):
        frame_photo(im,470,1060,700,820,'standing',t,.4+.3*math.sin(t*6));candle_lit(im,110,1150,t,.8)
    add('hook2',4,8,im,[closeup],titles=HOOK,focus=[(470,1060),(420,1040)])
    im=parlor2(271)
    def everywhere(im,t,fr):
        parlor_life(im,t)
        for k,(x,y) in enumerate(((260,960),(640,990),(450,1130))):
            if t>=T(8)+k*.3:frame_photo(im,x,y,300,360,'standing');sparkle(im,x+110,y-150,t+k,1.0)
    add('partout',8,13,im,[everywhere])
    im=parlor2(272,False)
    def fake(im,t,fr):
        candle_lit(im,130,1120,t,.8);frame_photo(im,470,1000,520,600,'standing')
        slam_stamp(im,'FAUX',470,1130,t,T(15),130);puff(im,470,1150,t,T(15),(200,180,150),12,220)
    add('faux',13,16,im,[fake])
    im=parlor2(273)
    def no_photo(im,t,fr):
        parlor_life(im,t)
        for k,x in enumerate((250,600)):frame_photo(im,x,1000,300,360,'empty')
    add('xixe',16,21,im,[no_photo])
    im=parlor2(274,False)
    def family(im,t,fr):
        candle_lit(im,110,1120,t,.8);candle_lit(im,860,1120,t,.8)
        for k,x in enumerate((250,420,600,760)):actor(im,x,1300,.7 if k%2 else .8,t,ph=k,kind='worried',coat=(60,50,46),dress=bool(k%2))
    add('familles',21,28,im,[family])
    im=parlor2(275)
    def photographer(im,t,fr):
        parlor_life(im,t);u=ease((t-T(28))/1.0);door(im,800,1240,u)
        if u>.6:camera_box(im,500,1290,.9);actor(im,250,1320,.85,t,kind='flat',mouth='flat',coat=(30,30,34),hat=True)
    add('photographe',28,37,im,[photographer])
    im=parlor2(276)
    def existed(im,t,fr):
        parlor_life(im,t)
        f=clamp01(1-(t-T(38))/.3) if t>=T(38) else 0
        camera_box(im,280,1290,.75,f)
        if t<T(38):frame_photo(im,660,1000,320,380,'empty')
        else:
            d=ImageDraw.Draw(im);d.rectangle((500,810,820,1190),fill=(110,76,40,255),outline=INK+(255,),width=6);d.rectangle((520,830,800,1170),fill=SEPIA_L+(255,))
            sofa_sleeper(im,660,1150,.4)
        camera_flash(im,t,T(38))
    add('existe',37,44,im,[existed])
    im=parlor2(277,False)
    def asleep(im,t,fr):
        candle_lit(im,830,1080,t,.9);sofa_sleeper(im,470,1240,1.0)
        glow(im,(300,1020),220,(255,220,160),.12)
    add('allonges',44,52,im,[asleep],focus=[(420,1080),(330,1040)])
    im=parlor2(278)
    def stands(im,t,fr):
        parlor_life(im,t)
        stand(im,470,1260,1.2,0,.5+.3*math.sin(t*5) if t>=T(56) else 0)
        actor(im,470,1270,1.0,t,coat=(60,50,46),back=True)
        if t>=T(56):
            for k in range(3):sparkle(im,470+(k-1)*60,1000+k*40,t+k,1.2)
    add('pieds',52,60,im,[stands])
    im=parlor2(279)
    def posing(im,t,fr):
        parlor_life(im,t);stand(im,400,1260,1.05)
        actor(im,400,1270,.95,t,kind='worried',mouth='flat',coat=(60,50,46),eyes='open')
        flash_t=T(65);camera_box(im,820,1290,.65,.6 if 0<=t-flash_t<.2 else 0);camera_flash(im,t,flash_t)
        wall_clock(im,640,985,t*4,44)
    add('vivants',60,68,im,[posing])
    im=parlor2(280)
    def light(im,t,fr):
        parlor_life(im,t)
        a=t-T(73);tilt=0 if a<0 else min(55,a*90)+3*math.sin(t*12)*(a<.6)
        stand(im,470,1260,1.15,tilt);puff(im,560,1250,t,T(74),(160,140,120),10,200)
        d=ImageDraw.Draw(im);d.text((760,1180),'≈ 10 KG',font=font(54),fill=(236,224,196,255),stroke_width=5,stroke_fill=INK+(255,),anchor='mm')
    add('legers',68,77,im,[light])
    im=parlor2(281);table(im,1200)
    def historians(im,t,fr):
        parlor_life(im,t);book(im,470,1190,t)
        mx=470+int(140*math.sin(t*1.5));sparkle(im,mx-40,1060,t,1.4)
        actor(im,820,1330,.75,t,kind='up',mouth='flat',coat=(40,40,60))
    add('historiens',77,91,im,[historians])
    im=parlor2(282,False)
    add('question',91,96,im,[photo_hook],titles=[('TU Y',CREAM,84,T(91),412),('CROYAIS ?',RED,100,T(91),530)])
    def clean_end(im,t,fr):photo_hook(im,0 if t>DUR-.3 else t,fr)
    add('loop',96,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(7,6,None),(15,7,None),(36,5,None),(51,4,None),(67,5,None),(76,6,None),(90,5,None)]
    return shots

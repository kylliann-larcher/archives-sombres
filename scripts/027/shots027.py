"""Limites de plans = indices de words2.json ; chaque plan a sa propre action lisible."""
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def opening():
        im=parlor(270);return im
    def photo_hook(im,t,fr):frame_photo(im,470,1000,520,600,'standing',t)
    add('hook',0,8,opening(),[photo_hook],titles=[('ILS SERAIENT',CREAM,84,0,412),('DÉJÀ MORTS',RED,100,0,530)])
    im=parlor(271)
    def everywhere(im,t,fr):
        for k,(x,y) in enumerate(((260,960),(680,980),(470,1120))):
            if t>=T(8)+k*.3:frame_photo(im,x,y,300,360,'standing')
    add('partout',8,13,im,[everywhere])
    im=parlor(272)
    def fake(im,t,fr):frame_photo(im,470,1000,520,600,'standing');slam_stamp(im,'FAUX',470,1130,t,T(15),130)
    add('faux',13,16,im,[fake])
    im=parlor(273)
    def no_photo(im,t,fr):
        for k,x in enumerate((250,690)):frame_photo(im,x,1000,300,360,'empty')
    add('xixe',16,21,im,[no_photo])
    im=parlor(274)
    def family(im,t,fr):
        for k,x in enumerate((250,420,600,760)):person(im,x,1300,.7 if k%2 else .8,coat=(60,50,46),dress=bool(k%2),mouth='flat')
    add('familles',21,28,im,[family])
    im=parlor(275)
    def photographer(im,t,fr):
        u=ease((t-T(28))/1.0);door(im,800,1240,u)
        if u>.6:camera_box(im,500,1290,.9);person(im,250,1320,.85,coat=(30,30,34),hat=True)
    add('photographe',28,37,im,[photographer])
    im=parlor(276)
    def existed(im,t,fr):
        f=clamp01(1-(t-T(38))/.3) if t>=T(38) else 0
        camera_box(im,280,1290,.75,f);frame_photo(im,660,1000,320,380,'empty') if t<T(38) else None
        if t>=T(38):
            d=ImageDraw.Draw(im);d.rectangle((500,810,820,1190),fill=(110,76,40,255),outline=INK+(255,),width=6);d.rectangle((520,830,800,1170),fill=SEPIA_L+(255,))
            sofa_sleeper(im,660,1150,.4)
    add('existe',37,44,im,[existed])
    im=parlor(277)
    def asleep(im,t,fr):sofa_sleeper(im,470,1240,1.0)
    add('allonges',44,52,im,[asleep],focus=[(420,1080),(330,1040)])
    im=parlor(278)
    def stands(im,t,fr):
        stand(im,470,1260,1.2,0,.5+.3*math.sin(t*5) if t>=T(56) else 0)
        person(im,470,1270,1.0,coat=(60,50,46),back=True)
    add('pieds',52,60,im,[stands])
    im=parlor(279)
    def posing(im,t,fr):
        stand(im,400,1260,1.05);person(im,400,1270,.95,coat=(60,50,46),mouth='flat')
        camera_box(im,820,1290,.65,.6 if (t-T(65))%1.2<.15 and t>=T(65) else 0)
    add('vivants',60,68,im,[posing])
    im=parlor(280)
    def light(im,t,fr):
        a=t-T(73);tilt=0 if a<0 else min(55,a*90)+3*math.sin(t*12)*(a<.6)
        stand(im,470,1260,1.15,tilt)
        d=ImageDraw.Draw(im);d.text((760,1180),'≈ 10 KG',font=font(54),fill=(236,224,196,255),stroke_width=5,stroke_fill=INK+(255,),anchor='mm')
    add('legers',68,77,im,[light])
    im=parlor(281);table(im,1200)
    def historians(im,t,fr):book(im,470,1190,t)
    add('historiens',77,91,im,[historians])
    im=parlor(282)
    add('question',91,96,im,[photo_hook],titles=[('TU Y',CREAM,84,T(91),412),('CROYAIS ?',RED,100,T(91),530)])
    def clean_end(im,t,fr):photo_hook(im,0 if t>DUR-.3 else t,fr)
    add('loop',96,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(7,6,None),(15,7,None),(36,5,None),(51,4,None),(67,5,None),(90,5,None)]
    return shots

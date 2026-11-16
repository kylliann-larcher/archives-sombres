"""Limites de plans = indices de words2.json ; chaque plan a sa propre action lisible (v2 enrichie)."""
def shot_defs():
    globals()['DUST_COL']=(220,230,255)
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def opening():
        im=post_office2(260);counter(im,1210);return im
    def waiting(im,t,fr):
        office_life(im,t);sack(im,720,1210,.9)
        actor(im,400,int(1230+4*math.sin(t*3)),.75,t,kind='up',mouth='smile',coat=COAT,hair=(120,74,40),dress=True)
        girl_stamps(im,400,1230,.75,6,t)
    def girl_stamps(im,x,y,s,n,t):
        d=ImageDraw.Draw(im)
        for k in range(n):
            sx=x-50*s+(k%3)*40*s;sy=y-190*s+(k//3)*48*s
            d.rectangle((sx,sy,sx+32*s,sy+38*s),fill=(214,200,150,255),outline=(120,30,30,255),width=2)
            d.rectangle((sx+6*s,sy+6*s,sx+26*s,sy+26*s),fill=(70,110,160,255) if k%2 else (180,60,60,255))
        d.rectangle((x+30*s,y-150*s,x+120*s,y-90*s),fill=(236,226,196,255),outline=INK+(255,),width=2)
        d.line((x+30*s,y-120*s,x+10*s,y-170*s),fill=INK+(255,),width=2)
    HOOK=[('CHEZ MAMIE',CREAM,84,0,412),('PAR LA POSTE',RED,100,0,530)]
    add('hook',0,4,opening(),[waiting],titles=HOOK)
    im=post_office2(266);counter(im,1210)
    def postman(im,t,fr):
        office_life(im,t);actor(im,700,1230,.85,t,kind='flat',mouth='smile',coat=MAILBLUE,hat=True)
        u=ease((t-T(4))/.6);sack(im,int(330+60*u),1210,.8)
    add('hook2',4,7,im,[postman],titles=HOOK)
    im=post_office2(261)
    def stamping(im,t,fr):
        n=int(clamp01((t-T(7))/1.4)*6)
        actor(im,470,1300,.95,t,kind='up',mouth='wide' if n<6 else 'smile',coat=COAT,hair=(120,74,40),dress=True)
        girl_stamps(im,470,1300,.95,n,t)
        if n:sparkle(im,int(470-50*.95+((n-1)%3)*40*.95+15),int(1300-190*.95+((n-1)//3)*48*.95),t,1.4)
    add('timbres',7,14,im,[stamping],focus=[(470,1100),(450,1120)])
    im=post_office2(265);counter(im,1210)
    def year(im,t,fr):
        office_life(im,t);u=ease((t-T(15))/.3);calendar(im,470,int(1200-40*u),'1913');sack(im,780,1210,.7,False)
        actor(im,180,1230,.75,t,kind='up',coat=MAILBLUE,hat=True)
    add('1913',14,16,im,[year])
    im=post_office2(267);counter(im,1210)
    def clerk(im,t,fr):
        office_life(im,t);actor(im,470,1230,.9,t,kind='up',mouth='smile',coat=MAILBLUE,hat=True)
        a=(t*3)%1;hand(im,700,int(1100+60*abs(math.sin(a*math.pi))),.6,1,MAILBLUE);parcel(im,700,1210,.6)
    add('poste',16,18,im,[clerk])
    im=post_office2(262);counter(im,1210)
    def parcels(im,t,fr):
        office_life(im,t)
        for k in range(4):
            u=ease((t-T(18)-k*.3)/.45);parcel(im,int(1100-u*(700-k*170)),1210,.8)
    add('colis',18,22,im,[parcels])
    im=post_office2(263);counter(im,1210)
    def weigh(im,t,fr):
        office_life(im,t);u=ease((t-T(27))/.6);scale(im,380,1210,.15+.6*u)
        actor(im,780,1230,.8,t,kind='worried' if u>.5 else 'flat',mouth='wide' if u>.5 else 'flat',coat=MAILBLUE,hat=True)
        if u>0:
            girl_y=int(1180+(1-u)*-200);actor(im,380,girl_y,.55,t,kind='up',mouth='smile',coat=COAT,hair=(120,74,40),dress=True);girl_stamps(im,380,girl_y,.55,4,t)
    add('regle',22,30,im,[weigh])
    im=mountains(270)
    def parents(im,t,fr):
        snow(im,t)
        actor(im,300,1300,.85,t,kind='worried',coat=(60,60,70));actor(im,560,1300,.85,t,ph=1,kind='worried',coat=(90,60,80),dress=True,hair=(70,46,30))
        actor(im,430,1300,.6,t,ph=2,kind='up',mouth='smile',coat=COAT,hair=(120,74,40),dress=True)
    add('idaho',30,42,im,[parents])
    im=post_office2(264);counter(im,1210)
    def pay(im,t,fr):
        office_life(im,t);n=int(clamp01((t-T(42))/1.0)*9);coins(im,330,1200,n,1.0)
        for k in range(2):sparkle(im,330+k*40,1200-n*16,t+k,1.0)
        actor(im,640,1200,.6,t,kind='up',mouth='smile',coat=COAT,hair=(120,74,40),dress=True);girl_stamps(im,640,1200,.6,int(clamp01((t-T(44))/.8)*6),t)
    add('cents',42,47,im,[pay])
    im=mountains(271)
    def ride(im,t,fr):
        snow(im,t,50);poles(im,t)
        x=int(470+20*math.sin(t*.8));train(im,x,1210,1.0,1);wheels(im,x,1210,1.0,t);smoke_puffs(im,x-240,1000,t)
    add('wagon',47,58,im,[ride],focus=[(470,1100),(560,1080)])
    im=paper(272,.03,(120,140,110));d=ImageDraw.Draw(im);d.rectangle((0,1240,W,H),fill=(90,110,70,255))
    def arrive(im,t,fr):
        snow(im,t,30);u=ease((t-T(60))/.8);house(im,470,1240,u)
        if u>.5:grandma(im,380,1300,t,u)
        actor(im,int(700-150*u),1300,.6,t,ph=2,kind='up',mouth='smile',coat=COAT,hair=(120,74,40),dress=True)
        if u>.9:heart(im,540,int(980-30*((t*1.5)%1)),1.2)
    add('grandmere',58,67,im,[arrive])
    im=post_office2(273);counter(im,1240)
    def ban(im,t,fr):
        office_life(im,t);paper_form(im,470,1080);slam_stamp(im,'INTERDIT',470,1100,t,T(70),100);puff(im,470,1140,t,T(70),(200,190,170),12,220)
    add('interdit',67,76,im,[ban])
    im=mountains(274)
    def again(im,t,fr):
        snow(im,t,60);poles(im,t,1240,300)
        x=int(600-120*clamp01((t-T(76))/2));train(im,x,1210,.9,2);wheels(im,x,1210,.9,t);smoke_puffs(im,x-220,1010,t)
    add('1915',76,84,im,[again],focus=[(470,1100),(470,1080)])
    im=post_office2(275);counter(im,1210)
    def back(im,t,fr):
        office_life(im,t);sack(im,720,1210,.9)
        actor(im,400,1230,.75,t,kind='worried',coat=COAT,hair=(120,74,40),dress=True);girl_stamps(im,400,1230,.75,6,t)
    add('question',84,90,im,[back],titles=[("ILS T'AURAIENT",CREAM,84,T(84),412),('POSTÉ ?',RED,100,T(84),530)])
    def clean_end(im,t,fr):waiting(im,0 if t>DUR-.3 else t,fr)
    add('loop',90,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(6,6,None),(13,4,None),(29,6,None),(46,5,None),(66,4,None),(83,5,None)]
    return shots

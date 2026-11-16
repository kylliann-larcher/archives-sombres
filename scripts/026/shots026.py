"""Limites de plans = indices de words2.json ; chaque plan a sa propre action lisible."""
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def opening():
        im=post_office(260);counter(im,1210);return im
    def waiting(im,t,fr):
        sack(im,720,1210,.9);girl(im,400,int(1230+4*math.sin(t*3)),.75,6)
    add('hook',0,7,opening(),[waiting],titles=[('CHEZ MAMIE',CREAM,84,0,412),('PAR LA POSTE',RED,100,0,530)])
    im=post_office(261)
    def stamping(im,t,fr):
        n=int(clamp01((t-T(7))/1.4)*6);girl(im,470,1300,.95,n)
    add('timbres',7,14,im,[stamping],focus=[(470,1100),(450,1120)])
    im=post_office(265);counter(im,1210)
    def year(im,t,fr):
        u=ease((t-T(15))/.3);calendar(im,470,int(1200-40*u),'1913');sack(im,780,1210,.7,False)
    add('1913',14,18,im,[year])
    im=post_office(262);counter(im,1210)
    def parcels(im,t,fr):
        for k in range(4):
            u=ease((t-T(18)-k*.3)/.45);parcel(im,int(1100-u*(700-k*170)),1210,.8)
    add('colis',18,22,im,[parcels])
    im=post_office(263);counter(im,1210)
    def weigh(im,t,fr):
        u=ease((t-T(27))/.6);scale(im,380,1210,.15+.6*u)
        if u>0:girl(im,380,int(1180+(1-u)*-200),.55,4)
    add('regle',22,30,im,[weigh])
    im=mountains(270)
    def parents(im,t,fr):
        person(im,300,1300,.85,coat=(60,60,70));person(im,560,1300,.85,coat=(90,60,80),dress=True,hair=(70,46,30))
        girl(im,430,1300,.6,0)
    add('idaho',30,42,im,[parents])
    im=post_office(264);counter(im,1210)
    def pay(im,t,fr):
        n=int(clamp01((t-T(42))/1.0)*9);coins(im,330,1200,n,1.0);girl(im,640,1200,.6,int(clamp01((t-T(44))/.8)*6))
    add('cents',42,47,im,[pay])
    im=mountains(271)
    def ride(im,t,fr):
        train(im,int(470+40*math.sin(t*.8)),1210,1.0,1);steam(im,t,200,980,3,.8,120,(220,220,220))
    add('wagon',47,58,im,[ride],focus=[(470,1100),(560,1080)])
    im=paper(272,.03,(120,140,110));d=ImageDraw.Draw(im);d.rectangle((0,1240,W,H),fill=(90,110,70,255))
    def arrive(im,t,fr):
        u=ease((t-T(60))/.8);house(im,470,1240,u)
        if u>.5:person(im,380,1300,.8,coat=(90,90,110),dress=True,hair=(200,200,200),mouth='smile')
        girl(im,int(700-150*u),1300,.6,6)
    add('grandmere',58,67,im,[arrive])
    im=post_office(273);counter(im,1240)
    def ban(im,t,fr):paper_form(im,470,1080);slam_stamp(im,'INTERDIT',470,1100,t,T(70),100)
    add('interdit',67,76,im,[ban])
    im=mountains(274)
    def again(im,t,fr):
        train(im,int(600-120*clamp01((t-T(76))/2)),1210,.9,2)
    add('1915',76,84,im,[again],focus=[(470,1100),(470,1080)])
    im=post_office(275);counter(im,1210)
    def back(im,t,fr):sack(im,720,1210,.9);girl(im,400,1230,.75,6,'flat')
    add('question',84,90,im,[back],titles=[("ILS T'AURAIENT",CREAM,84,T(84),412),('POSTÉ ?',RED,100,T(84),530)])
    def clean_end(im,t,fr):waiting(im,0 if t>DUR-.3 else t,fr)
    add('loop',90,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(6,6,None),(13,4,None),(29,6,None),(46,5,None),(66,4,None),(83,5,None)]
    return shots

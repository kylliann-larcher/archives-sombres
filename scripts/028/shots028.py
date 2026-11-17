"""Limites de plans = indices de words2.json."""
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    def lineup(im,t,fr,xs=(250,470,690),s=.8,sway_idx=1,amp=0,y=1270):
        for k,x in enumerate(xs):
            a=amp*math.sin(t*5.5)*(1 if k==sway_idx else 0)
            guard(im,x+int(2*math.sin(t*2+k)),y,s,ang=a)
    def opening():return courtyard(300)
    HOOK=[('UN GARDE',CREAM,84,0,412),("S'EFFONDRE",RED,100,0,530)]
    def hook_a(im,t,fr):
        steps(im,470,1240,3);lineup(im,t,fr,amp=min(22,6+t*14))
    add('hook',0,3,opening(),[hook_a],titles=HOOK)
    def hook_b(im,t,fr):
        guard(im,330,1290,.95,ang=-82,sabre=False,mouth='wide',eyes='closed')
        u=ease((t-T(3))/.5);sabre_obj(im,720,1290-int(60*(1-u)),340,-6+30*(1-u))
        sparkle(im,720,1270,t,1.2)
    add('hook2',3,6,courtyard(301),[hook_b],titles=HOOK,focus=[(470,1100),(500,1060)])
    def sabre_fall(im,t,fr):
        column(im,150);column(im,930)
        t0=T(8)-.4;u=clamp01((t-t0)/.4)
        y=900+380*u*u;ang=-400*u if u<1 else -8-6*math.exp(-(t-T(8))*8)*math.sin((t-T(8))*30)
        sabre_obj(im,470,int(y),380,ang)
        if t>=T(8):puff(im,470,1280,t,T(8),(190,180,170),12,260);sparkle(im,430,1280,t,1.3)
    add('sabre',6,12,courtyard(302),[sabre_fall])
    def journalist(im,t,fr):
        steps(im,700,1240,3)
        actor(im,300,1290,.95,t,kind='worried',mouth='flat',coat=(74,62,52),hair=(52,40,32))
        d=ImageDraw.Draw(im);d.rectangle((390,1130,418,1180),fill=(30,30,34,255),outline=INK+(255,),width=2);d.ellipse((382,1100,426,1140),fill=(60,60,64,255),outline=INK+(255,),width=3)
        actor(im,880,1300,.8,t,ph=1,kind='worried',coat=(60,60,70),back=True)
        if t>=T(15):
            a=t-T(15);sc=1+.4*max(0,1-a/.2)**2
            if a<4:bubble(im,600,980,'OH LÀ LÀ !',int(58*sc),(-120,90))
    add('journaliste',12,21,courtyard(303),[journalist],focus=[(400,1100),(600,1040)])
    def evening(im,t,fr):
        d=ImageDraw.Draw(im);glow(im,(850,700),130,(240,240,220),.5);d.ellipse((810,660,890,740),fill=(240,236,214,255))
        steps(im,540,1240,4);lineup(im,t,fr,(150,330,750,930),.7,sway_idx=9)
        for x in (150,930):glow(im,(x,1050),160,(255,214,150),.3+.05*math.sin(t*6))
    add('mercredi',21,29,courtyard(304),[evening])
    def gardes(im,t,fr):
        steps(im,540,1240,3);lineup(im,t,fr,(110,260,410,660,810,960),.62,sway_idx=9,y=1280)
        u=ease((t-T(33))/1.6)
        suit(im,1250-int(430*u),1300,.8,t=t);
    add('gardes',29,36,courtyard(305),[gardes],focus=[(540,1100),(700,1060)])
    def main_guard(im,t,carry=0):
        ang=fall_angle(t,T(38),T(41)-.05,-1)
        fallen=t>=T(41)-.05
        guard(im,470-carry,1280,1.0,ang=ang,sabre=not fallen,mouth='wide' if fallen or t>T(39) else 'flat',eyes='closed' if fallen else 'open')
        if fallen:sabre_obj(im,780,1285,360,-6)
    def salute(im,t,fr):
        steps(im,470,1240,3);main_guard(im,t)
    add('salue',36,41,courtyard(306),[salute],focus=[(470,1060),(470,1020)])
    def carried(im,t,fr):
        u=ease((t-T(42))/1.8);carry=int(280*u)
        main_guard(im,t,carry)
        for k,dx in enumerate((-150,-40,70,180,260)):
            if t>=T(41)-.1+k*.12:actor(im,470-carry+dx-150+int(60*(1-ease((t-T(41))/.6))),1300,.78,t,ph=k,kind='worried',coat=(48,52,60),hair=(48,36,28),back=True)
    add('emportent',41,44,courtyard(307),[carried])
    def second(im,t,fr):
        for k,x in enumerate((200,)):
            for dx in (-1,0,1):pass
        guard(im,170,1300,.6,ang=-84,sabre=False,mouth='wide',eyes='closed')
        for k,dx in enumerate((250,340)):actor(im,dx+120,1310,.6,t,ph=k,kind='worried',coat=(48,52,60),back=True)
        ang=fall_angle(t,T(46),T(51),1)
        guard(im,830,1290,.85,ang=ang,sabre=ang<12,mouth='wide' if ang>12 else 'flat',eyes='closed' if ang>40 else 'open')
        if t>=T(51):
            u=clamp01((t-T(51))/.35);sabre_obj(im,1000,int(1000+280*u*u),360,60-50*u)
        if t>=T(52):
            d=ImageDraw.Draw(im);d.text((560,1010),'HORS CAMÉRA',font=font(56),fill=(236,224,196,255),stroke_width=6,stroke_fill=INK+(255,),anchor='mm')
    add('pendant',44,54,courtyard(308),[second],focus=[(300,1100),(830,1090)])
    def two(im,t,fr):
        guard(im,300,1280,.75,ang=-84,sabre=False,mouth='wide',eyes='closed');guard(im,760,1280,.75,ang=84,sabre=False,mouth='wide',eyes='closed')
        sabre_obj(im,540,1295,300,-4)
        sc=1+.8*max(0,1-(t-T(54))/.2)**2
        if t>=T(54):
            d=ImageDraw.Draw(im);d.text((540,1040),'2',font=font(int(260*sc)),fill=RED+(255,),stroke_width=9,stroke_fill=INK+(255,),anchor='mm')
    add('deux',54,59,courtyard(309),[two])
    def frozen(im,t,fr):
        steps(im,420,1240,4)
        suit(im,560,1290,1.0,mouth='flat',kind='up',t=t)
        suit(im,800,1300,.9,mouth='flat',kind='worried',t=t+1)
        guard(im,150,1300,.6,ang=-84,sabre=False,eyes='closed')
    add('fige',59,67,courtyard(310),[frozen],focus=[(560,1060),(700,1040)])
    def unknown(im,t,fr):
        u=clamp01((t-T(67))/.5);pulse=1+.05*math.sin(t*4)
        question_mark(im,470,1180,1.6*pulse*(.5+.5*u))
        guard(im,150,1300,.55,ang=-84,sabre=False,eyes='closed');guard(im,860,1300,.55,ang=84,sabre=False,eyes='closed')
    add('inconnu',67,72,courtyard(311),[unknown])
    def source(im,t,fr):
        paper_sheet(im,470,1080,560,400,-3,0,5);d=ImageDraw.Draw(im)
        if t>=T(74):d.text((470,930),'SOURCE : ÉLYSÉE',font=font(46),fill=INK+(255,),anchor='mm')
        slam_stamp(im,'MALAISE VAGAL',470,1130,t,T(79),64,-8)
    add('source',72,81,courtyard(312),[source])
    def pressure(im,t,fr):
        needle=60-110*ease((t-T(82))/(T(84)-T(82)+.3))
        gauge(im,350,1080,160,needle)
        dim=ease((t-T(85))/(T(88)-T(85)));brain(im,730,1080,1.0,dim)
        d=ImageDraw.Draw(im);d.text((350,1290),'PRESSION',font=font(48),fill=CREAM+(255,),stroke_width=5,stroke_fill=INK+(255,),anchor='mm');d.text((730,1290),'CERVEAU',font=font(48),fill=CREAM+(255,),stroke_width=5,stroke_fill=INK+(255,),anchor='mm')
    add('pression',81,89,courtyard(313),[pressure],focus=[(470,1080),(540,1080)])
    def nobody(im,t,fr):
        guard(im,250,1290,.8);guard(im,690,1290,.8)
        check(im,470,1000,1.4,clamp01((t-T(89))/.3)*2)
    add('blesse',89,95,courtyard(314),[nobody])
    def resume(im,t,fr):
        steps(im,540,1240,3);lineup(im,t,fr,(120,260,820,960),.62,sway_idx=9,y=1280)
        suit(im,430,1300,.85,mouth='smile',t=t);suit(im,650,1300,.85,mouth='smile',t=t+1)
        d=ImageDraw.Draw(im);d.line((505,1130,575,1130),fill=SKIN+(255,),width=16)
    add('reprend',95,100,courtyard(315),[resume])
    def lone(im,t,fr):
        guard(im,470,1290,.95,eyes='open',mouth='flat')
    add('question',100,108,courtyard(316),[lone],titles=[('SELON TOI,',CREAM,84,T(100),412),('POURQUOI ?',RED,100,T(104),530)])
    def clean_end(im,t,fr):hook_a(im,0 if t>DUR-.3 else t,fr)
    add('loop',108,len(WORDS),opening(),[clean_end])
    globals()['IMPACTS']=[(7,6,None),(41,6,None),(51,7,None),(62,4,None),(80,5,None),(90,4,None)]
    return shots

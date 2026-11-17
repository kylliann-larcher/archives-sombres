"""Limites de plans = indices de words2.json (par phrase)."""
def wi(t,n=0):return [i for i,w in enumerate(WORDS) if w['text'].lower().startswith(t)][n]
def first(g):return next(i for i,w in enumerate(WORDS) if w['ph']==g)
def shot_defs():
    shots=[]
    def add(name,a,b,bg,dyn=None,titles=None,focus=None):
        shots.append(dict(name=name,a=a,b=b,bg=bg,flames=[],dyn=dyn or [],sprites=[],titles=titles or [],focus=focus or [(470,1080),(470,1040)]))
    HOOK=[('ENTERRÉ AVEC',CREAM,84,0,412),('UNE CLOCHE',RED,100,0,530)]
    def mound(im,t,fr,ang=None):
        d=ImageDraw.Draw(im);d.ellipse((260,1100,680,1200),fill=(70,54,40,255),outline=INK+(255,),width=5)
        d.rectangle((440,1090,500,1130),fill=(36,30,28,255),outline=INK+(255,),width=4)
        d.line((700,1150,700,830),fill=(64,46,32,255),width=16);d.line((700,830,560,830),fill=(64,46,32,255),width=14)
        a=(6+8*min(1,t/1.5))*math.sin(t*5) if ang is None else ang
        bell(im,560,830,.9,a)
        d.line((560,830+190*.9,470,1095),fill=(214,196,150,255),width=5)
    add('hook',0,wi('cloche')+1,graveyard(410),[mound],titles=HOOK)
    def handrope(im,t,fr):
        d=ImageDraw.Draw(im);d.rectangle((0,1060,W,H),fill=(34,28,26,255))
        d.line((470,820,470,1120),fill=(214,196,150,255),width=7)
        hand(im,470,1180,1.6,1,(80,62,46))
        bell(im,470,760,.8,5*math.sin(t*4))
    add('hook2',wi('cloche')+1,first(1),graveyard(411),[handrope],titles=HOOK,focus=[(470,1100),(470,1060)])
    def xixe(im,t,fr):
        for k,x in enumerate((250,520,800)):actor(im,x,1300+8*(k%2),.8,t,ph=k,kind='worried',coat=(46,44,56),hair=(40,34,30),back=bool(k%2),hat=True)
        glow(im,(250,1100),180,(255,214,150),.15)
    add('xixe',first(1),first(2),street(412),[xixe])
    def inventors(im,t,fr):
        table(im,1200)
        for k,x in enumerate((220,470,720)):
            L=Image.new('RGBA',(W,H),(0,0,0,0));paper_sheet(L,x,930,190,230,(-5+5*k),0,k+1);im.alpha_composite(L)
            d=ImageDraw.Draw(im);d.rounded_rectangle((x-60,960,x+60,1000),radius=8,fill=(120,80,46,255),outline=INK+(255,),width=3)
        actor(im,880,1300,.9,t,kind='up',coat=(70,56,40),hat=True)
    add('inventeurs',first(2),first(3),room(413,(70,62,56),(54,42,34)),[inventors])
    def brevet(im,t,fr):
        paper_sheet(im,470,1060,640,440,-2,0,6);d=ImageDraw.Draw(im)
        d.text((470,900),'BREVET US 81 437',font=font(52),fill=INK+(255,),anchor='mm')
        d.text((470,1050),'FRANZ VESTER · NEWARK',font=font(40),fill=(60,40,25,255),anchor='mm')
        d.text((470,1110),'25 AOÛT 1868',font=font(40),fill=(60,40,25,255),anchor='mm')
        slam_stamp(im,'BREVET',470,1190,t,T(wi('brevet.')),70,-8)
    add('brevet',first(3),first(4),graveyard(414),[brevet])
    def tube(im,t,fr):
        underground(im,t,0,0,hand=False,bell_on=False)
        u=ease((t-T(first(4)))/1.2);d=ImageDraw.Draw(im)
        d.rectangle((443,Y0,497,Y0+int((1150-Y0)*u)),fill=(36,30,28,255))
    add('tube',first(4),first(5),graveyard(415),[tube],focus=[(470,1080),(470,1130)])
    def corde(im,t,fr):
        underground(im,t,ring=1 if t>=T(wi('cloche',1)) and t<T(wi('cloche',1))+1.2 else 0,hand=True)
    add('corde',first(5),first(6),graveyard(416),[corde],focus=[(470,1110),(560,1000)])
    def sonner(im,t,fr):
        ts=T(wi('sonner'));r=1 if t>=ts-.1 else 0
        underground(im,t,ring=r);sound_arcs(im,560,900,t,ts)
    add('sonner',first(6),first(7),graveyard(417),[sonner],focus=[(560,950),(470,1060)])
    def allemagne(im,t,fr):
        d=ImageDraw.Draw(im);t0=T(first(7))+.5
        d.text((470,985),'ALLEMAGNE',font=font(56),fill=CREAM+(255,),stroke_width=6,stroke_fill=INK+(255,),anchor='mm')
        for k in range(30):
            if t<t0+k*.045:continue
            x=130+(k%6)*160;y=1060+(k//6)*50
            d.rounded_rectangle((x-50,y-18,x+50,y+18),radius=8,fill=(120,80,46,255),outline=INK+(255,),width=3)
        d.text((470,1250),'+ DE 30 BREVETS',font=font(50),fill=CREAM+(255,),stroke_width=6,stroke_fill=INK+(255,),anchor='mm') if False else None
    add('allemagne',first(7),first(8),street(418),[allemagne])
    def aucun(im,t,fr):
        bell(im,470,880,1.1,0)
        red_cross(im,470,1020,200,ease((t-T(wi('aucun')))/.25))
        slam_stamp(im,'AUCUN SAUVETAGE',470,1230,t,T(wi('aucun')),52,-6)
    add('aucun',first(8),first(9),graveyard(419),[aucun])
    def rien(im,t,fr):
        underground(im,t,0,0,hand=True);question_mark(im,830,1110,.9)
    add('rien',first(9),first(10),graveyard(420),[rien],focus=[(470,1100),(700,1080)])
    def fausse(im,t,fr):
        ts=T(wi('toute'))
        underground(im,t,ring=1 if t>=ts else 0,rope_wave=1 if t>=ts-.3 else 0)
        if t>=ts:sound_arcs(im,560,900,t,ts)
        slam_stamp(im,'FAUSSE ALERTE',770,1120,t,ts,52,-6)
    add('fausse',first(10),first(11),graveyard(421),[fausse],focus=[(470,1100),(600,1040)])
    def coins_bell(im,t,fr):
        coins(im,260,1230,6,1.2);bell(im,720,900,1.0,6*math.sin(t*4))
    add('question',first(11),first(12),graveyard(422),[coins_bell],titles=[('TU AURAIS',CREAM,84,T(first(11)),412),('PAYÉ LA CLOCHE ?',RED,100,T(wi('payé')),530)])
    def clean_end(im,t,fr):mound(im,0 if t>DUR-.3 else t,fr,ang=0 if t>DUR-.3 else None)
    add('loop',first(12),len(WORDS),graveyard(410),[clean_end])
    globals()['IMPACTS']=[(4,6,None),(27,5,None),(36,6,None),(64,5,None),(74,6,None),(92,5,None)]
    return shots

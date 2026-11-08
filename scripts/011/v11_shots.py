def clamp01(x): return min(1.0, max(0.0, x))
def ease(x): x = clamp01(x); return x*x*(3 - 2*x)
exec(open(f"{HERE}/gen11.py", encoding="utf-8").read())

def bg_hook():
    im = stone_cell(60, 0.55, slit_glow=0.35, slit_col=(200, 210, 230))
    prisoner(im, 330, 1180, 1.1, mood=2)
    return im

def shot_defs():
    S = []
    # 0 : hook - le prisonnier dans son cachot (visible des la 1re image)
    S.append(dict(name="hook1", a=0, b=9, bg=bg_hook(), flames=[], sprites=[], focus=[(400, 1150), (330, 1100)],
        titles=[("ENFERMÉ AU CACHOT", CREAM, 110, 0.0, 470), ("IL SURVIT", RED, 132, T(6), 610)]))
    # 1 : la catastrophe - la nuee sur la ville
    def bg1():
        im = paper(61, 0.45, (80, 60, 50)); volcano_town(im, lit=False); return im
    t1 = T(9)
    cl1 = Spr(lambda L: cloud_layer(L, 470, 640, 200, (70, 62, 58), True, 1), (470, 640),
              lambda t: (60*ease((t - t1)/2.5), 520*ease((t - t1)/2.5), 0, 1 + 1.4*ease((t - t1)/2.5), 1), appear=t1)
    S.append(dict(name="hook2", a=9, b=18, bg=bg1(), flames=[], sprites=[cl1], focus=[(470, 1000), (470, 1150)],
        titles=[("30 000 MORTS", RED, 132, T(12), 470), ("EN QUELQUES MINUTES", CREAM, 92, T(16), 610)]))
    # 2 : ce qui l'a sauve... sa punition
    def bg2(): return stone_cell(62, 0.6)
    st2 = Spr(lambda L: stamp_red(L, "SA PUNITION", 760, 1080, 74, -9), (760, 1080), pop(T(25), 0.12, 2.5), appear=T(25))
    q2 = Spr(lambda L: ImageDraw.Draw(L).text((300, 820), "?", font=font(380), fill=RED+(230,), stroke_width=10, stroke_fill=(0, 0, 0)), (400, 1040), pop(T(19), 0.25, 1.8), appear=T(19), vanish=T(25))
    S.append(dict(name="punition", a=18, b=26, bg=bg2(), flames=[], sprites=[q2, st2], focus=[(760, 1000), (700, 1080)], titles=[]))
    # 3 : Tu t'appelles Ludger Sylbaris (portrait)
    lud = Spr(lambda L: prisoner(L, 470, 1130, 1.6, mood=1), (470, 1500), lambda t: breathe(t, 0.01, 0.8, 4))
    S.append(dict(name="ludger", a=26, b=30, bg=paper(63, 0.35, (60, 50, 44)), flames=[], sprites=[lud], focus=[(470, 1000), (470, 950)], titles=[]))
    # 4 : Saint-Pierre, Martinique
    def bg4():
        im = paper(64, 0.15, (90, 70, 50)); glow(im, (800, 520), 200, (255, 220, 160), 0.5); volcano_town(im, smoke=True, lit=True); return im
    S.append(dict(name="ville", a=30, b=37, bg=bg4(), flames=[], sprites=[], focus=[(470, 1300), (300, 1350), (700, 1300)],
        titles=[("SAINT-PIERRE, 1902", CREAM, 100, T(33), 440), ("« LE PETIT PARIS DES ANTILLES »", RED, 76, T(35), 552)]))
    # 5 : on te jette au cachot
    t5 = T(41)
    push = Spr(lambda L: prisoner(L, 330, 1180, 1.1, mood=3), (330, 1450), lambda t: (-500*(1 - ease((t - t5)/0.6)), 0, -8*(1 - ease((t - t5)/0.6)), 1, 1))
    S.append(dict(name="jete", a=37, b=46, bg=stone_cell(65, 0.6), flames=[], sprites=[push], focus=[(470, 1150), (330, 1150), (760, 1000)],
        titles=[("7 MAI 1902, AU SOIR", CREAM, 96, T(38), 440)]))
    # 6 : la cellule (murs, pas de fenetre)
    lud6 = Spr(lambda L: prisoner(L, 330, 1180, 1.1, mood=2), (330, 1450), lambda t: breathe(t, 0.006, 0.4, 2))
    S.append(dict(name="cellule", a=46, b=59, bg=stone_cell(66, 0.6), flames=[], sprites=[lud6], focus=[(470, 1300), (200, 700), (330, 1150), (800, 900)], titles=[]))
    # 7 : la fente dans la porte
    def bg7(): return stone_cell(67, 0.55, slit_glow=0.6, slit_col=(210, 220, 240))
    S.append(dict(name="fente", a=59, b=65, bg=bg7(), flames=[], sprites=[], focus=[(760, 900), (760, 850)], titles=[]))
    # 8 : le volcan gronde
    def bg8():
        im = paper(68, 0.3, (90, 64, 48)); volcano_town(im, smoke=True, lit=True); return im
    ash = Spr(lambda L: cloud_layer(L, 520, 380, 150, (90, 84, 80), False, 4), (520, 380), lambda t: (30*math.sin(t*0.7), -20*math.sin(t*0.5), 0, 1 + 0.25*ease((t - T(70))/3), 0.9))
    S.append(dict(name="volcan", a=65, b=78, bg=bg8(), flames=[], sprites=[ash], focus=[(470, 900), (470, 650), (470, 1300)],
        titles=[("MONTAGNE PELÉE", CREAM, 100, T(66), 440), ("1 397 MÈTRES", RED, 96, T(71), 552)]))
    # 9 : l'eruption - la nuee devale et engloutit la ville
    def bg9():
        im = paper(69, 0.35, (96, 60, 40)); volcano_town(im, smoke=True, lit=True); return im
    te = T(81)
    blast = Spr(lambda L: glow(L, (470, 560), 330, (255, 150, 50), 0.9), (470, 560), lambda t: (0, 0, 0, 1 + 0.4*ease((t - te)/0.4), clamp01((t - te)/0.15)), appear=te)
    cl9 = Spr(lambda L: cloud_layer(L, 470, 600, 200, (66, 58, 54), True, 9), (470, 600),
              lambda t: (40*ease((t - te)/(T(91) - te + 0.3)), 640*ease((t - te)/(T(91) - te + 0.3)), 0, 1 + 1.9*ease((t - te)/(T(91) - te + 0.3)), 1), appear=te)
    S.append(dict(name="eruption", a=78, b=92, bg=bg9(), flames=[], sprites=[blast, cl9], focus=[(470, 700), (470, 1000), (470, 1200)],
        titles=[("8 MAI 1902, VERS 8 H", CREAM, 96, T(79), 440)]))
    # 10 : l'air brulant par la fente, il brule, les murs tiennent
    th = T(92)
    slit = Spr(lambda L: (ImageDraw.Draw(L).rectangle((690, 760, 830, 784), fill=(255, 190, 90, 255)), glow(L, (760, 772), 220, (255, 130, 40), 0.9)), (760, 772),
               lambda t: (0, 0, 0, 1 + 0.08*math.sin(t*14), clamp01((t - th)/0.6)), appear=th)
    heat = Spr(lambda L: glow(L, (600, 1000), 700, (255, 90, 20), 0.6), (600, 1000), lambda t: (0, 0, 0, 1, 0.65*clamp01((t - th)/2.0)*(0.85 + 0.15*math.sin(t*9))), appear=th)
    tb = T(101)
    p1 = Spr(lambda L: prisoner(L, 330, 1180, 1.1, mood=3), (330, 1450), lambda t: (3*math.sin(t*20), 0, 1.5*math.sin(t*17), 1, 1), vanish=tb)
    p2 = Spr(lambda L: prisoner(L, 330, 1180, 1.1, mood=3, burnt=True), (330, 1450), lambda t: (3*math.sin(t*20), 0, 1.5*math.sin(t*17), 1, 1), appear=tb)
    S.append(dict(name="brule", a=92, b=112, bg=stone_cell(70, 0.6), flames=[], sprites=[heat, slit, p1, p2], focus=[(760, 900), (330, 1150), (470, 1100), (330, 1100), (760, 950)], titles=[]))
    # 11 : dehors, la ville est morte
    def bg11():
        im = paper(71, 0.5, (70, 62, 58)); ruins(im); return im
    S.append(dict(name="ruines", a=112, b=119, bg=bg11(), flames=[Flame(250, 1400, 120, 90), Flame(820, 1390, 150, 110)], sprites=[], focus=[(470, 1250), (300, 1250)],
        titles=[("UNE POIGNÉE", CREAM, 104, T(113), 440), ("DE SURVIVANTS", RED, 104, T(116), 560)]))
    # 12 : toi... tu respires encore
    def bg12(): return stone_cell(72, 0.7)
    p12 = Spr(lambda L: prisoner(L, 470, 1130, 1.5, mood=3, burnt=True), (470, 1500), lambda t: (0, 8*math.sin(t*1.6), 0, 1 + 0.015*math.sin(t*1.6), 1))
    S.append(dict(name="respire", a=119, b=123, bg=bg12(), flames=[], sprites=[p12], focus=[(470, 1000), (470, 950)], titles=[]))
    # 13 : quatre jours dans les ruines
    def bg13():
        im = stone_cell(73, 0.75, slit_glow=0.2, slit_col=(200, 200, 210)); prisoner(im, 330, 1180, 1.1, mood=3, burnt=True); return im
    S.append(dict(name="jours", a=123, b=131, bg=bg13(), flames=[], sprites=[], focus=[(400, 1150), (330, 1100)],
        titles=[("#DAY#", RED, 132, T(124), 470)], day=(T(124), T(130), 4)))
    # 14 : les sauveteurs
    def bg14():
        im = paper(74, 0.6, (60, 56, 54)); ruins(im, 75); return im
    resc = []
    for k, x in enumerate((180, 420, 680)):
        resc.append(Spr(lambda L, x=x: rescuer(L, x, 1560, 1.25), (x, 1400), lambda t, k=k: (60*ease((t - T(131))/3) + 4*math.sin(t*5 + k), 6*abs(math.sin(t*4 + k)), 0, 1, 1)))
    S.append(dict(name="sauveteurs", a=131, b=135, bg=bg14(), flames=[], sprites=resc, focus=[(470, 1300), (420, 1250)],
        titles=[]))
    # 15 : ta vie bascule -> le cirque
    def bg15():
        im = paper(75, 0.35, (40, 30, 46)); circus(im); return im
    tw = T(139)
    wag = Spr(lambda L: cage_wagon(L, 540, 1450, 0.9), (540, 1350), lambda t: (-900*(1 - ease((t - tw)/2.2)), 4*abs(math.sin(t*6)), 0, 1, 1))
    S.append(dict(name="cirque", a=135, b=153, bg=bg15(), flames=[], sprites=[wag], focus=[(540, 1150), (540, 1000), (540, 1300), (300, 1200)],
        titles=[("BARNUM & BAILEY", CREAM, 100, T(140), 440), ("TOURNÉE AUX ÉTATS-UNIS", RED, 84, T(145), 552)]))
    # 16 : "l'homme qui a survecu au jour du Jugement dernier"
    def bg16():
        im = paper(76, 0.35, (40, 30, 46)); circus(im); cage_wagon(im, 540, 1450, 0.9); return im
    crowd = []
    for k in range(9):
        x = 60 + k*120
        crowd.append(Spr(lambda L, x=x, k=k: figure(L, x, 1900 + (k % 2)*20, 1.1, col=(8, 6, 6), hat=(k % 3 == 0)), (x, 1780), lambda t, k=k: (0, 6*math.sin(t*3 + k), 0, 1, 1)))
    S.append(dict(name="surnom", a=153, b=164, bg=bg16(), flames=[], sprites=crowd, focus=[(540, 1250), (540, 1200)],
        titles=[("« L'HOMME QUI A SURVÉCU", CREAM, 84, T(155), 440), ("AU JUGEMENT DERNIER »", RED, 88, T(159), 548)]))
    # 17 : le prisonnier puni est devenu une star
    def bg17():
        im = paper(77, 0.6, (40, 30, 46)); return im
    spot = Spr(lambda L: ImageDraw.Draw(L).polygon([(440, 0), (500, 0), (800, 1700), (140, 1700)], fill=(255, 240, 200, 70)), (470, 850), lambda t: (0, 0, 0, 1, clamp01((t - T(164))/0.3)))
    star = Spr(lambda L: prisoner(L, 470, 1130, 1.5, mood=0), (470, 1500), lambda t: breathe(t, 0.01, 0.8, 4))
    sparks = []
    for k in range(7):
        ap = T(169) + k*0.08
        sparks.append(Spr(lambda L, k=k: glow(L, (180 + k*120, 900 + (k % 3)*120), 40, (255, 230, 150), 0.9), (180 + k*120, 900 + (k % 3)*120), pop(ap, 0.2, 2.0), appear=ap))
    S.append(dict(name="star", a=164, b=171, bg=bg17(), flames=[], sprites=[spot, star] + sparks, focus=[(470, 1000), (470, 950)], titles=[]))
    # 18 : question finale
    def bg18(): return stone_cell(78, 0.75, slit_glow=0.3, slit_col=(255, 150, 60))
    p18 = Spr(lambda L: prisoner(L, 330, 1180, 1.1, mood=3, burnt=True), (330, 1450), lambda t: breathe(t, 0.006, 0.4, 2))
    S.append(dict(name="question", a=171, b=184, bg=bg18(), flames=[], sprites=[p18], focus=[(400, 1150), (330, 1100)],
        titles=[("TU AURAIS TENU", CREAM, 110, T(178), 470), ("COMBIEN DE TEMPS ?", RED, 110, T(181), 610)]))
    # 19 : abonnement + boucle
    S.append(dict(name="boucle", a=184, b=len(WORDS), bg=bg_hook(), flames=[], sprites=[], focus=[(400, 1150), (330, 1100)], titles=[]))
    return S

IMPACTS = [(6, 14, (255, 255, 255)), (13, 18, (255, 140, 40)), (25, 22, (200, 30, 30)), (29, 10, None), (36, 8, None), (45, 16, None), (51, 10, None), (55, 10, None),
           (58, 10, None), (61, 12, None), (77, 12, None), (81, 30, (255, 170, 60)), (89, 16, None), (96, 14, (255, 140, 40)), (107, 18, (255, 140, 40)), (111, 14, None),
           (118, 18, None), (122, 10, (255, 255, 255)), (125, 10, None), (134, 12, None), (138, 24, (255, 255, 255)), (141, 12, None), (152, 10, None), (163, 16, None),
           (170, 22, (255, 220, 120)), (183, 10, None)]

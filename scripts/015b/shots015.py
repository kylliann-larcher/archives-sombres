GOLD = globals().get("GOLD", (212, 175, 80))
COLS = [(120, 36, 48), (58, 70, 112), (92, 102, 52), (140, 100, 40), (84, 52, 94), (40, 84, 82), (130, 60, 40)]

def DS(cx, base, s, ph, appear=None, vanish=None, speed=5.5, **kw):
    return Spr(lambda L: dancer(L, cx, base, s, **kw), (cx, base - 210*s),
               lambda t: (10*s*math.sin(t*speed + ph), -18*s*abs(math.sin(t*speed + ph)), 9*math.sin(t*speed/2 + ph), 1, 1), appear=appear, vanish=vanish)

def MS(cx, base, s, kind, ph=0.0, appear=None):
    return Spr(lambda L: musician(L, cx, base, s, kind), (cx, base - 200*s), lambda t: (0, -8*s*abs(math.sin(t*4.5 + ph)), 3*math.sin(t*4.5 + ph), 1, 1), appear=appear)

def shot_defs():
    S = []
    def bg0():
        im = street(140, 0.45, True, 1430); return im
    dan0 = [DS(330, 1560, 1.05, 0.0, dress=COLS[0], up=(1.0, 0.6)), DS(520, 1600, 1.2, 1.7, dress=COLS[1], male=True, up=(0.8, 1.0), cap=True),
            DS(700, 1560, 1.05, 3.1, dress=COLS[2], up=(0.6, 1.0)), DS(150, 1520, 0.85, 4.4, dress=COLS[3], male=True, cap=True)]
    mus0 = [MS(840, 1480, 0.85, "fiddle", 0.5), MS(110, 1450, 0.7, "drum", 1.2)]
    S.append(dict(name="hook", a=0, b=19, bg=bg0(), flames=[], sprites=mus0 + dan0, focus=[(470, 1200), (500, 1250), (420, 1250), (560, 1200)],
        titles=[("LA VILLE PAYE DES MUSICIENS", CREAM, 70, 0.0, 440), ("ÇA A TOUT EMPIRÉ", RED, 100, T(15), 552)]))
    # 1 : annonce, les morts
    def bg1():
        im = paper(141, 0.7, (30, 30, 38)); crosses(im, 1280, 3); question_mark(im, 470, 1350, 560, 45); return im
    S.append(dict(name="morts_annonce", a=19, b=30, bg=bg1(), flames=[], sprites=[], focus=[(470, 1250), (470, 1100), (470, 1350)],
        titles=[("LE PLUS ÉTRANGE", CREAM, 84, T(19), 440), ("LES MORTS ?", RED, 100, T(27), 552)]))
    # 2 : Strasbourg juillet 1518
    def bg2():
        im = paper(142, 0.35, (60, 46, 50)); glow(im, (470, 1050), 520, (240, 190, 130), 0.25); cathedral(im, 420, 1800, 0.6); return im
    S.append(dict(name="strasbourg", a=30, b=41, bg=bg2(), flames=[], sprites=[], focus=[(560, 1150), (470, 1300), (620, 1000), (470, 1350)],
        titles=[("STRASBOURG", CREAM, 84, T(34), 440), ("JUILLET 1518", RED, 100, T(36), 552)]))
    # 3 : la femme sort et danse
    def bg3():
        im = street(143, 0.5, False, 1430); d = ImageDraw.Draw(im)
        d.rectangle((560, 1000, 900, 1430), fill=(60, 40, 28, 255), outline=INK+(255,), width=5); d.rectangle((650, 1180, 760, 1430), fill=(20, 12, 8, 255)); return im
    f3 = DS(430, 1580, 1.35, 0.0, appear=T(46), dress=COLS[0], up=(1.0, 0.8), speed=5.0)
    f3b = Spr(lambda L: dancer(L, 700, 1430, 0.9, dress=COLS[0], up=(0.0, 0.0)), (700, 1300), lambda t: (0, 0, 0, 1, 1), vanish=T(46))
    S.append(dict(name="femme", a=41, b=52, bg=bg3(), flames=[], sprites=[f3b, f3], focus=[(560, 1300), (430, 1250), (500, 1350)],
        titles=[("UNE FEMME", CREAM, 100, T(41), 440), ("ELLE DANSE", RED, 110, T(50), 552)]))
    # 4 : sans musique, sans fete
    def bg4():
        im = street(144, 0.7, False, 1430); glow(im, (470, 1150), 380, (250, 220, 170), 0.22); return im
    f4 = DS(470, 1600, 1.5, 0.3, dress=COLS[0], up=(1.0, 0.9), speed=4.2)
    note = Spr(lambda L: (ImageDraw.Draw(L).ellipse((130, 1000, 210, 1060), fill=CREAM+(255,)), ImageDraw.Draw(L).rectangle((198, 860, 214, 1030), fill=CREAM+(255,)), ImageDraw.Draw(L).line((120, 1180, 240, 960), fill=RED+(255,), width=18), ImageDraw.Draw(L).line((120, 960, 240, 1180), fill=RED+(255,), width=18)), (180, 1070), pop(T(53), 0.15, 2.0), appear=T(53))
    S.append(dict(name="sans_musique", a=52, b=60, bg=bg4(), flames=[], sprites=[f4, note], focus=[(470, 1300), (470, 1200), (400, 1350)],
        titles=[("SANS MUSIQUE", CREAM, 84, T(52), 440), ("SANS FÊTE", RED, 100, T(54), 552), ("ELLE NE S'ARRÊTE", CREAM, 84, T(57), 440), ("PLUS", RED, 100, T(57), 552)]))
    # 5 : la foule grandit
    def bg5(): return street(145, 0.5, True, 1380)
    cr5 = []
    pos = [(150, 1450, 0.8), (780, 1450, 0.8), (310, 1470, 0.9), (640, 1470, 0.9), (470, 1600, 1.15), (190, 1620, 1.1), (760, 1620, 1.1), (350, 1680, 1.2), (590, 1690, 1.2)]
    for k, (x, y, sc) in enumerate(pos):
        cr5.append(DS(x, y, sc, k*1.3, appear=T(60) + k*0.22, dress=COLS[k % len(COLS)], male=(k % 3 == 1), cap=(k % 2 == 0), up=(1.0, 0.5 + 0.5*(k % 2))))
    S.append(dict(name="foule", a=60, b=78, bg=bg5(), flames=[], sprites=cr5, focus=[(470, 1350), (470, 1500), (330, 1450), (620, 1450)],
        titles=[("QUELQUES JOURS PLUS TARD", CREAM, 64, T(60), 440), ("50 À 400 DANSEURS", RED, 90, T(70), 552), ("SELON LES ESTIMATIONS", CREAM, 64, T(75), 440)]))
    # 6 : le conseil, sang chaud
    def bg6():
        im = paper(146, 0.5, (46, 30, 30)); d = ImageDraw.Draw(im); d.rectangle((60, 1380, 1020, 1470), fill=(70, 44, 26, 255), outline=INK+(255,), width=5); return im
    cm = [Spr(lambda L, x=x, c=c: councilman(L, x, 1420, 0.78, robe=c, point=(x == 560)), (x, 1200), lambda t, x=x: breathe(t, 0.008, 0.6, 3, x/100), appear=T(78) + k*0.15) for k, (x, c) in enumerate([(200, (42, 32, 38)), (440, (30, 44, 40)), (680, (58, 30, 36)), (860, (36, 36, 60))])]
    fl = Spr(lambda L: (flask(L, 470, 1460, 0.5, (200, 30, 30))), (470, 1420), lambda t: (0, 0, 0, 1 + 0.03*math.sin(t*6), 1), appear=T(86))
    S.append(dict(name="conseil", a=78, b=90, bg=bg6(), flames=[], sprites=cm + [fl], focus=[(470, 1200), (330, 1250), (620, 1250), (470, 1300)],
        titles=[("LE CONSEIL DE LA VILLE", CREAM, 72, T(78), 440), ("SANG CHAUD", RED, 96, T(88), 552)]))
    # 7 : le remede : danser encore plus
    def bg7():
        im = street(147, 0.55, True, 1380); glow(im, (470, 1200), 480, (200, 40, 40), 0.22); return im
    cr7 = [DS(x, y, sc, k*0.9, dress=COLS[(k+2) % len(COLS)], male=(k % 2 == 0), cap=True, up=(1.0, 1.0), speed=6.5 + k*0.3) for k, (x, y, sc) in enumerate([(210, 1560, 1.05), (440, 1620, 1.25), (680, 1560, 1.05), (840, 1500, 0.85), (90, 1480, 0.8)])]
    S.append(dict(name="remede", a=90, b=97, bg=bg7(), flames=[], sprites=cr7, focus=[(470, 1300), (470, 1250), (560, 1350)],
        titles=[("LE REMÈDE", CREAM, 100, T(90), 440), ("DANSER ENCORE PLUS", RED, 80, T(94), 552)]))
    # 8 : musiciens et danseurs professionnels
    def bg8(): return street(148, 0.4, True, 1400)
    ms8 = [MS(190, 1560, 1.0, "fiddle", 0.0, appear=T(97)), MS(470, 1600, 1.15, "drum", 0.7, appear=T(99)), MS(760, 1560, 1.0, "horn", 1.4, appear=T(100))]
    pr8 = DS(560, 1480, 0.85, 2.0, appear=T(103), dress=(170, 130, 40), up=(1.0, 1.0), speed=6.5)
    S.append(dict(name="musiciens", a=97, b=106, bg=bg8(), flames=[], sprites=ms8 + [pr8], focus=[(470, 1350), (230, 1380), (760, 1380), (470, 1300)],
        titles=[("ON ENGAGE", CREAM, 96, T(97), 440), ("DES MUSICIENS", RED, 100, T(101), 552)]))
    # 9 : Waller : ca aggrave tout
    def bg9():
        im = paper(149, 0.55, (40, 34, 40)); glow(im, (330, 1100), 400, (230, 200, 150), 0.18); return im
    wal = Spr(lambda L: councilman(L, 300, 1480, 0.9, robe=(34, 52, 44), book=True), (300, 1200), lambda t: breathe(t, 0.008, 0.6, 3), appear=T(106))
    sil = []
    for k in range(14):
        x = 560 + (k % 5)*85; y = 1330 + (k // 5)*110
        sil.append(Spr(lambda L, x=x, y=y: figure(L, x, y, 0.55, col=(12, 8, 6), arms_up=True), (x, y - 100), lambda t, k=k: (0, -6*abs(math.sin(t*6 + k)), 6*math.sin(t*3 + k), 1, 1), appear=T(110) + k*0.12))
    S.append(dict(name="waller", a=106, b=115, bg=bg9(), flames=[], sprites=[wal] + sil, focus=[(420, 1250), (330, 1250), (650, 1300), (470, 1300)],
        titles=[("JOHN WALLER", CREAM, 96, T(108), 440), ("ÇA AGGRAVE TOUT", RED, 90, T(112), 552)]))
    # 10 : 2 aout, interdit
    def bg10():
        im = paper(150, 0.5, (48, 34, 30)); calendar_sheet2(im, 470, 1370, 560, 640, -3, "AOÛT 1518", "2"); return im
    st10 = Spr(lambda L: stamp_red(L, "INTERDIT", 470, 1500, 110, -9), (470, 1500), pop(T(122), 0.12, 2.6), appear=T(122))
    S.append(dict(name="interdit", a=115, b=123, bg=bg10(), flames=[], sprites=[st10], focus=[(470, 1250), (470, 1150), (470, 1300)],
        titles=[("VOLTE-FACE", CREAM, 84, T(118), 440), ("DANSE INTERDITE", RED, 96, T(119), 552)]))
    # 11 : pelerinage vers saint Guy, puis tout s'arrete
    def bg11():
        im = paper(151, 0.7, (26, 30, 52)); glow(im, (700, 1050), 420, (240, 220, 170), 0.2)
        d = ImageDraw.Draw(im); d.polygon([(0, 1550), (0, 1500), (300, 1380), (620, 1170), (900, 1100), (1080, 1120), (1080, 1920), (0, 1920)], fill=(22, 18, 20, 255), outline=INK+(255,))
        chapel(im, 780, 1130, 0.9); return im
    pil = [Spr(lambda L, k=k: figure(L, 120 + k*95, 1600 - k*52, 0.82 - k*0.06, col=(10, 8, 7), arms_up=(k % 3 == 0)), (120 + k*95, 1500 - k*52), lambda t, k=k: (0, 4*math.sin(t*3 + k), 2*math.sin(t*2 + k), 1, 1), appear=T(123) + k*0.25) for k in range(6)]
    halo = Spr(lambda L: glow(L, (780, 800), 260, (250, 210, 110), 0.75), (780, 800), lambda t: (0, 0, 0, 1 + 0.05*math.sin(t*3), 0.7 + 0.3*math.sin(t*2)), appear=T(129))
    S.append(dict(name="pelerinage", a=123, b=135, bg=bg11(), flames=[], sprites=pil + [halo], focus=[(470, 1350), (700, 1150), (300, 1450), (780, 1100)],
        titles=[("PÈLERINAGE", CREAM, 84, T(126), 440), ("SAINT GUY", RED, 100, T(129), 552), ("EN SEPTEMBRE,", CREAM, 84, T(131), 440), ("TOUT S'ARRÊTE", RED, 100, T(133), 552)]))
    # 12 : personne ne sait pourquoi
    def bg12():
        im = street(152, 0.8, False, 1430, (40, 40, 56)); question_mark(im, 470, 1350, 560, 50); return im
    S.append(dict(name="vide", a=135, b=140, bg=bg12(), flames=[], sprites=[], focus=[(470, 1250), (470, 1150)],
        titles=[("PERSONNE NE SAIT", CREAM, 76, T(135), 440), ("POURQUOI", RED, 120, T(138), 552)]))
    # 13 : et les morts : quinze par jour (recit tardif)
    def bg13():
        im = paper(153, 0.7, (30, 30, 38)); crosses(im, 1220, 5); question_mark(im, 470, 1350, 560, 40); return im
    S.append(dict(name="morts", a=140, b=153, bg=bg13(), flames=[], sprites=[], focus=[(470, 1250), (470, 1400), (470, 1150)], count=(T(149), T(152), 15),
        titles=[("ET LES MORTS ?", CREAM, 84, T(140), 440), ("ON RACONTE…", CREAM, 84, T(143), 552), ("#COUNT# PAR JOUR", RED, 100, T(149), 552)]))
    # 14 : recits ecrits plus tard
    def bg14():
        im = paper(154, 0.5, (50, 40, 30)); paper_sheet(im, 470, 1380, 580, 620, -2, 0.0, 3); return im
    qu = Spr(lambda L: quill(L, 760, 1330, 1.2, -35), (760, 1330), lambda t: (-14*math.sin(t*4), 8*math.sin(t*8), 0, 1, 1))
    S.append(dict(name="recits", a=153, b=160, bg=bg14(), flames=[], sprites=[qu], focus=[(470, 1200), (600, 1150), (470, 1300)],
        titles=[("RÉCITS ÉCRITS", CREAM, 96, T(155), 440), ("PLUS TARD", RED, 120, T(158), 552)]))
    # 15 : archives de la ville : aucun mort
    def bg15():
        im = paper(155, 0.5, (44, 34, 28)); paper_sheet(im, 290, 1380, 420, 600, -3, 0.0, 5); paper_sheet(im, 660, 1380, 420, 600, 2, 0.0, 6); candle(im, 930, 1640, 1.1, True); return im
    st15 = Spr(lambda L: stamp_red(L, "AUCUN MORT", 470, 1420, 100, -8), (470, 1420), pop(T(168), 0.12, 2.6), appear=T(168))
    S.append(dict(name="archives", a=160, b=172, bg=bg15(), flames=[], sprites=[st15], focus=[(470, 1200), (330, 1200), (640, 1250), (470, 1300)],
        titles=[("ARCHIVES DE LA VILLE", CREAM, 76, T(162), 440), ("À L'ÉPOQUE : 0 MORT", RED, 90, T(167), 552)]))
    # 16 : la cause : famine, maladies, saint Guy
    def bg16():
        im = paper(156, 0.7, (34, 24, 28)); glow(im, (470, 1250), 500, (150, 40, 30), 0.25); return im
    bw = Spr(lambda L: bowl(L, 250, 1450, 1.0), (250, 1450), lambda t: breathe(t, 0.01, 0.6, 3), appear=T(174))
    sg = Spr(lambda L: saint(L, 720, 1560, 0.95), (720, 1250), lambda t: breathe(t, 0.01, 0.8, 4), appear=T(176))
    S.append(dict(name="cause", a=172, b=182, bg=bg16(), flames=[], sprites=[bw, sg], focus=[(470, 1350), (250, 1400), (720, 1250), (470, 1300)],
        titles=[("LA CAUSE ?", CREAM, 84, T(172), 440), ("FAMINE · MALADIES", RED, 84, T(174), 552), ("PEUR DE SAINT GUY", RED, 84, T(176), 552)]))
    # 17 : panique collective
    def bg17():
        im = paper(157, 0.7, (40, 22, 28)); glow(im, (470, 1250), 560, (190, 30, 40), 0.35); return im
    pn = []
    for r in range(3):
        for c in range(7):
            x = 90 + c*135 + (r % 2)*60; y = 1360 + r*150
            pn.append(Spr(lambda L, x=x, y=y, r=r: figure(L, x, y, 0.7 + r*0.12, col=(10, 6, 6), arms_up=True), (x, y - 120), lambda t, c=c, r=r: (0, -10*abs(math.sin(t*5 - c*0.6)), 7*math.sin(t*2.5 - c*0.6), 1, 1)))
    S.append(dict(name="panique", a=182, b=192, bg=bg17(), flames=[], sprites=pn, focus=[(470, 1450), (300, 1450), (650, 1450), (470, 1380)],
        titles=[("LA PISTE LA PLUS SÉRIEUSE", CREAM, 62, T(182), 440), ("PANIQUE COLLECTIVE", RED, 88, T(186), 552)]))
    # 18 : la question finale
    def bg18():
        im = paper(158, 0.88, (26, 22, 24)); glow(im, (470, 1250), 420, (200, 170, 130), 0.22); return im
    f18 = DS(470, 1620, 1.45, 0.0, dress=COLS[0], up=(1.0, 0.9), speed=3.6)
    S.append(dict(name="question", a=192, b=205, bg=bg18(), flames=[], sprites=[f18], focus=[(470, 1300), (470, 1250), (470, 1350)],
        titles=[("ET TOI,", CREAM, 84, T(192), 440), ("LA PEUR SE PROPAGE", CREAM, 76, T(197), 440), ("COMME UNE MALADIE ?", RED, 84, T(202), 552)]))
    # 19 : appel au partage
    S.append(dict(name="partage", a=205, b=213, bg=bg0(), flames=[], sprites=mus0 + dan0, focus=[(470, 1250), (420, 1250), (560, 1200)],
        titles=[("ENVOIE ÇA", RED, 84, T(205), 440), ("À QUELQU'UN", CREAM, 90, T(207), 552), ("QUI NE PEUT PAS", CREAM, 84, T(210), 440), ("S'ARRÊTER DE DANSER", RED, 84, T(213), 552)]))
    # 20 : boucle
    S.append(dict(name="boucle", a=213, b=len(WORDS), bg=bg0(), flames=[], sprites=mus0 + dan0, focus=[(470, 1200), (500, 1250)],
        titles=[("QUI NE PEUT PAS", CREAM, 84, 0.0, 440), ("S'ARRÊTER DE DANSER", RED, 84, 0.0, 552)]))
    return S

IMPACTS = [(15, 14, (200, 30, 30)), (18, 20, (200, 30, 30)), (29, 12, None), (50, 10, None), (59, 16, None), (70, 10, None), (88, 10, None), (94, 14, None), (113, 18, (200, 30, 30)), (122, 22, (200, 30, 30)), (129, 10, None), (134, 16, None), (149, 12, None), (168, 22, (255, 255, 255)), (186, 14, (200, 30, 30)), (205, 12, None)]

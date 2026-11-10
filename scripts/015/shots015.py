def shot_defs():
    S = []
    def bg0():
        im = paper(140, 0.65, (30, 24, 36)); glow(im, (470, 1050), 460, (240, 180, 110), 0.22); houses(im, 1700, 7, lit=True); return im
    dn0 = Spr(lambda L: dancer(L, 470, 1000, 1.0, mood=1), (470, 1400), lambda t: (30*math.sin(t*3), 18*abs(math.sin(t*3)), 8*math.sin(t*3), 1, 1))
    S.append(dict(name="danseuse", a=0, b=16, bg=bg0(), flames=[], sprites=[dn0], focus=[(470, 1050), (470, 1000), (470, 1100), (470, 1000)],
        titles=[("ON DIT QU'ILS SONT", CREAM, 84, 0.0, 440), ("MORTS DE DANSER", RED, 110, T(4), 552), ("LES ARCHIVES SE TAISENT", CREAM, 64, T(10), 660)]))
    # 1 : Strasbourg, juillet 1518
    def bg1():
        im = paper(141, 0.4, (60, 48, 40)); houses(im, 1650, 9, lit=False); return im
    pp = []
    for k, x in enumerate((130, 330, 770, 930)):
        pp.append(Spr(lambda L, x=x: figure(L, x, 1500, 1.5, col=(30, 22, 18), hat=(k % 2 == 0)), (x, 1250), lambda t, k=k: (0, 4*math.sin(t*2 + k), 0, 1, 1)))
    S.append(dict(name="strasbourg", a=16, b=26, bg=bg1(), flames=[], sprites=pp, focus=[(470, 1300), (470, 1450), (470, 1350)],
        titles=[("STRASBOURG", CREAM, 110, T(19), 440), ("JUILLET 1518", RED, 100, T(21), 552)]))
    # 2 : une femme se met a danser
    def bg2():
        im = paper(142, 0.5, (50, 40, 36)); glow(im, (470, 1100), 500, (230, 190, 120), 0.2); return im
    dn2 = Spr(lambda L: dancer(L, 470, 1020, 1.05, mood=1), (470, 1450), lambda t: (35*math.sin((t - T(29))*3.2), 22*abs(math.sin((t - T(29))*3.2)), 9*math.sin((t - T(29))*3.2), 1, 1))
    S.append(dict(name="troffea", a=26, b=35, bg=bg2(), flames=[], sprites=[dn2], focus=[(470, 1100), (470, 1000), (470, 1200)],
        titles=[("UNE FEMME", CREAM, 100, T(29), 440), ("FRAU TROFFEA", RED, 100, T(37), 552)]))
    # 3 : des jours (soleil et lune)
    def bg3():
        im = paper(143, 0.45, (46, 40, 52)); return im
    sun = Spr(lambda L: glow(L, (470, 700), 220, (250, 210, 120), 0.9), (470, 700), lambda t: (-380 + 760*clamp01((t - T(39))/(T(45) - T(39))), 80*math.sin(clamp01((t - T(39))/(T(45) - T(39)))*math.pi)*-1, 0, 1, 1))
    dn3 = Spr(lambda L: dancer(L, 470, 1100, 1.0, dress=(40, 60, 130), mood=-1), (470, 1500), lambda t: (30*math.sin(t*3.4), 20*abs(math.sin(t*3.4)), 8*math.sin(t*3.4), 1, 1))
    S.append(dict(name="jours", a=35, b=46, bg=bg3(), flames=[], sprites=[sun, dn3], focus=[(470, 1100), (470, 1050), (470, 1200)],
        titles=[("ELLE NE S'ARRÊTE PAS", CREAM, 76, T(39), 440), ("DES JOURS", RED, 130, T(43), 552)]))
    # 4 : d'autres la rejoignent
    def bg4():
        im = paper(144, 0.5, (46, 38, 34)); houses(im, 1750, 11, lit=False); return im
    cr = []
    for k in range(9):
        x = 110 + 110*k; ap = T(47) + 0.15*k
        cr.append(Spr(lambda L, x=x, k=k: dancer(L, x, 1100 + 30*(k % 3), 0.42, dress=[(150, 40, 40), (40, 90, 60), (60, 60, 130)][k % 3], mood=1), (x, 1250),
                      lambda t, k=k: (14*math.sin(t*3 + k), 10*abs(math.sin(t*3 + k)), 8*math.sin(t*3 + k), 1, 1), appear=ap))
    S.append(dict(name="foule", a=46, b=58, bg=bg4(), flames=[], sprites=cr, focus=[(470, 1200), (300, 1200), (700, 1200), (470, 1150)],
        titles=[("50 À 400", RED, 150, T(50), 440), ("SELON LES ESTIMATIONS", CREAM, 58, T(55), 590)]))
    # 5 : les autorites
    def bg5():
        im = paper(145, 0.45, (44, 34, 38)); glow(im, (470, 1100), 440, (220, 190, 140), 0.2); return im
    au = []
    for k, x in enumerate((200, 470, 740)):
        au.append(Spr(lambda L, x=x: cardinal(L, x, 1050, 0.6), (x, 1300), lambda t, k=k: breathe(t, 0.01, 0.8, 3, k)))
    S.append(dict(name="autorites", a=58, b=71, bg=bg5(), flames=[], sprites=au, focus=[(470, 1150), (200, 1100), (740, 1100), (470, 1150)],
        titles=[("L'IDÉE DES AUTORITÉS", CREAM, 72, T(58), 440), ("LES LAISSER DANSER", RED, 88, T(66), 552)]))
    # 6 : musiciens payes
    def bg6():
        im = paper(146, 0.4, (56, 40, 30)); drum(im, 220, 1260, 1.0); lute(im, 760, 1180, 1.0); return im
    coins = []
    for k in range(6):
        ap = T(73) + 0.12*k
        coins.append(Spr(lambda L, k=k: ImageDraw.Draw(L).ellipse((450 + k*18, 900, 490 + k*18, 940), fill=GOLD+(255,), outline=INK+(255,), width=3), (470 + k*18, 920),
                         lambda t, ap=ap, k=k: (0, 400*clamp01((t - ap)/0.8), 0, 1, 1 - clamp01((t - ap - 0.6)/0.3)), appear=ap))
    dn6 = Spr(lambda L: dancer(L, 470, 1200, 0.55, dress=(60, 60, 130)), (470, 1450), lambda t: (20*math.sin(t*4), 14*abs(math.sin(t*4)), 8*math.sin(t*4), 1, 1))
    S.append(dict(name="musiciens", a=71, b=82, bg=bg6(), flames=[], sprites=coins + [dn6], focus=[(470, 1200), (220, 1250), (760, 1200), (470, 1250)],
        titles=[("MUSICIENS PAYÉS", CREAM, 90, T(72), 440), ("DANSEURS PROFESSIONNELS", RED, 64, T(77), 552)]))
    # 7 : ca empire
    def bg7():
        im = paper(147, 0.5, (54, 24, 28)); houses(im, 1800, 13, lit=False); return im
    cr7 = []
    for k in range(10):
        x = 80 + 100*k
        cr7.append(Spr(lambda L, x=x, k=k: dancer(L, x, 1100 + 40*(k % 3), 0.4, dress=[(150, 40, 40), (40, 90, 60), (60, 60, 130)][k % 3], mood=-1), (x, 1250),
                       lambda t, k=k: (16*math.sin(t*5 + k), 14*abs(math.sin(t*5 + k)), 10*math.sin(t*5 + k), 1, 1)))
    S.append(dict(name="empire", a=82, b=85, bg=bg7(), flames=[], sprites=cr7, focus=[(470, 1200)],
        titles=[("ÇA EMPIRE", RED, 130, T(82), 440)]))
    # 8 : 2 aout, danse interdite
    def bg8():
        im = paper(148, 0.4, (60, 50, 44)); d = ImageDraw.Draw(im)
        d.rectangle((300, 1000, 340, 1750), fill=(90, 62, 40, 255), outline=INK+(255,), width=4)
        d.rectangle((140, 1000, 820, 1480), fill=(226, 210, 170, 255), outline=INK+(255,), width=6)
        hatch(d, (140, 1000, 820, 1480), 18, 0.3, (80, 60, 40, 60), 3); return im
    st8 = Spr(lambda L: stamp_red(L, "INTERDIT", 480, 1240, 140, -8), (480, 1240), pop(T(88), 0.12, 2.6), appear=T(88))
    S.append(dict(name="interdit", a=85, b=92, bg=bg8(), flames=[], sprites=[st8], focus=[(470, 1150), (470, 1100), (470, 1200)],
        titles=[("2 AOÛT", CREAM, 130, T(85), 440), ("DANSE INTERDITE", RED, 92, T(88), 552)]))
    # 9 : pelerinage
    def bg9():
        im = paper(149, 0.5, (40, 38, 50)); glow(im, (470, 900), 400, (240, 220, 180), 0.2); cross_pole(im, 470, 800, 1.2); return im
    pl = []
    for k, x in enumerate((100, 270, 640, 810)):
        pl.append(Spr(lambda L, x=x: figure(L, x, 1620, 1.1, col=(12, 9, 8), hat=True), (x, 1450), lambda t, k=k: (10*math.sin(t*2 + k) , 8*abs(math.sin(t*2.5 + k)), 0, 1, 1)))
    S.append(dict(name="pelerinage", a=92, b=98, bg=bg9(), flames=[], sprites=pl, focus=[(470, 1250), (470, 1100)],
        titles=[("DIRECTION", CREAM, 90, T(92), 440), ("LE PÈLERINAGE", RED, 100, T(95), 552)]))
    # 10 : chroniques tardives
    def bg10():
        im = paper(150, 0.45, (46, 38, 32)); chronicle(im, 470, 1250, 520, 720, "CHRONIQUES"); return im
    st10 = Spr(lambda L: stamp_red(L, "TARDIVES", 470, 1450, 110, -8), (470, 1450), pop(T(101), 0.12, 2.6), appear=T(101))
    S.append(dict(name="chroniques", a=98, b=106, bg=bg10(), flames=[], sprites=[st10], focus=[(470, 1250), (470, 1200), (470, 1300)],
        titles=[("SELON DES CHRONIQUES", CREAM, 70, T(98), 440), ("MORTS D'ÉPUISEMENT ?", RED, 78, T(102), 552)]))
    # 11 : aucun document de l'epoque
    def bg11():
        im = paper(151, 0.4, (50, 44, 40)); paper_sheet(im, 470, 1380, 560, 760, -2, 0.0, 6); return im
    qm = Spr(lambda L: ImageDraw.Draw(L).text((350, 1190), "?", font=font(520), fill=(110, 28, 30, 255)), (470, 1380), pop(T(108), 0.2, 1.8, 0.1), appear=T(108))
    S.append(dict(name="aucun", a=106, b=114, bg=bg11(), flames=[], sprites=[qm], focus=[(470, 1250), (470, 1200)],
        titles=[("AUCUN DOCUMENT", RED, 96, T(107), 440), ("DE L'ÉPOQUE", CREAM, 90, T(110), 552)]))
    # 12 : panique collective
    def bg12():
        im = paper(152, 0.6, (34, 28, 44)); glow(im, (470, 1150), 520, (150, 60, 160), 0.3); return im
    cr12 = []
    for k in range(7):
        x = 110 + 125*k
        cr12.append(Spr(lambda L, x=x, k=k: figure(L, x, 1500 + 20*(k % 2), 0.9, col=(12, 9, 14), arms_up=True), (x, 1350), lambda t, k=k: (8*math.sin(t*4 + k), 12*abs(math.sin(t*4 + k)), 6*math.sin(t*4 + k), 1, 1)))
    sw = Spr(lambda L: glow(L, (470, 1050), 300, (190, 80, 190), 0.8), (470, 1050), lambda t: (0, 0, 0, 1 + 0.08*math.sin(t*3), 0.6 + 0.3*math.sin(t*2)))
    S.append(dict(name="panique", a=114, b=130, bg=bg12(), flames=[], sprites=[sw] + cr12, focus=[(470, 1250), (300, 1300), (700, 1300), (470, 1150)],
        titles=[("LES HISTORIENS", CREAM, 90, T(114), 440), ("PANIQUE COLLECTIVE", RED, 82, T(119), 552), ("DU GROUPE, PAS DU CORPS", CREAM, 54, T(124), 640)]))
    # 13 : la question, la porte fermee
    def bg13():
        im = paper(153, 0.8, (22, 20, 30)); houses(im, 1750, 15, lit=True); door(im, 470, 1500, 1.3, grille=False); return im
    sh = []
    for k, x in enumerate((100, 240, 700, 860)):
        sh.append(Spr(lambda L, x=x: figure(L, x, 1650, 0.8, col=(8, 6, 10), arms_up=True), (x, 1500), lambda t, k=k: (6*math.sin(t*4 + k), 10*abs(math.sin(t*4 + k)), 5*math.sin(t*4 + k), 1, 0.7)))
    S.append(dict(name="question", a=130, b=148, bg=bg13(), flames=[], sprites=sh, focus=[(470, 1350), (470, 1250), (470, 1450), (470, 1300)],
        titles=[("ET TOI,", CREAM, 110, T(130), 440), ("TOUTE TA VILLE DANSE", CREAM, 72, T(133), 552), ("TU DANSES OU TU FERMES ?", RED, 66, T(140), 650)]))
    S.append(dict(name="boucle", a=148, b=len(WORDS), bg=bg0(), flames=[], sprites=[dn0], focus=[(470, 1050), (470, 1000)], titles=[]))
    return S

IMPACTS = [(4, 14, (200, 30, 30)), (19, 8, None), (34, 12, None), (45, 12, None), (50, 18, (200, 30, 30)), (70, 8, None), (84, 24, (200, 30, 30)), (91, 14, (255, 255, 255)),
           (105, 10, None), (113, 14, None), (121, 12, None), (147, 10, None)]

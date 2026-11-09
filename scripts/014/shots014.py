def shot_defs():
    S = []
    # decor du hook et de la boucle : Molay en prison, derriere la grille
    def bg0():
        im = paper(120, 0.5, (36, 30, 30)); glow(im, (470, 1150), 440, (240, 190, 120), 0.18)
        door(im, 470, 1330, 1.5)
        d = ImageDraw.Draw(im); d.rectangle((470-150, 1330-510, 470+150, 1330-255), fill=(10, 8, 8, 255), outline=INK+(255,), width=8)
        return im
    mol0 = Spr(lambda L: templar(L, 470, 880, 0.82, mood=2, cross=False), (470, 1000), lambda t: breathe(t, 0.008, 0.8, 3))
    bars0 = Spr(lambda L: grille_bars(L, 470, 1330, 1.5), (470, 1200), lambda t: (0, 0, 0, 1, 1))
    S.append(dict(name="prison", a=0, b=20, bg=bg0(), flames=[], sprites=[mol0, bars0], focus=[(470, 1000), (470, 1040), (470, 980), (470, 1000)],
        titles=[("CONDAMNÉ À VIE", CREAM, 104, 0.0, 440), ("IL REFUSE DE SE TAIRE", CREAM, 76, T(9), 552), ("BRÛLÉ LE SOIR MÊME", RED, 96, T(14), 660)]))
    # 1 : Jacques de Molay
    def bg1():
        im = paper(121, 0.4, (44, 36, 36)); glow(im, (470, 1050), 460, (230, 200, 150), 0.25); return im
    mol1 = Spr(lambda L: templar(L, 470, 1030, 1.1, mood=1), (470, 1500), lambda t: breathe(t, 0.01, 0.8, 4))
    S.append(dict(name="molay", a=20, b=32, bg=bg1(), flames=[], sprites=[mol1], focus=[(470, 1100), (470, 1000), (470, 1200)],
        titles=[("JACQUES DE MOLAY", CREAM, 92, T(23), 440), ("DERNIER GRAND MAÎTRE", RED, 70, T(26), 552)]))
    # 2 : six ans en prison
    def bg2():
        im = cell_bg(122, 0.55); d = ImageDraw.Draw(im); d.rectangle((60, 1500, 1020, 1540), fill=(46, 30, 20, 255)); return im
    mol2 = Spr(lambda L: templar(L, 470, 1130, 1.0, mood=-1, chains=True), (470, 1500), lambda t: breathe(t, 0.006, 0.6, 3))
    S.append(dict(name="six_ans", a=32, b=41, bg=bg2(), flames=[], sprites=[mol2], focus=[(470, 1150), (470, 1100), (470, 1250)],
        titles=[("PLUS DE", CREAM, 90, T(32), 440), ("6 ANS", RED, 140, T(35), 540)]))
    # 3 : les aveux
    def bg3():
        im = paper(123, 0.5, (40, 34, 30)); paper_sheet(im, 470, 1150, 560, 760, -3, 0.0, 4); return im
    st3 = Spr(lambda L: stamp_red(L, "AVEUX", 470, 1250, 130, -10), (470, 1250), pop(T(47), 0.12, 2.6), appear=T(47))
    S.append(dict(name="aveux", a=41, b=49, bg=bg3(), flames=[], sprites=[st3], focus=[(470, 1150), (470, 1100), (470, 1250)],
        titles=[("SOUS LA TORTURE", CREAM, 92, T(43), 440)]))
    # 4 : Notre-Dame, mars 1314
    def bg4():
        im = paper(124, 0.45, (50, 46, 52)); notre_dame(im, 470, 1700, 0.85)
        cardinal(im, 270, 1230, 0.55); cardinal(im, 470, 1230, 0.55); cardinal(im, 670, 1230, 0.55); return im
    mol4 = Spr(lambda L: templar(L, 470, 1470, 0.55, mood=-1, chains=False), (470, 1500), lambda t: breathe(t, 0.008, 0.6, 3))
    S.append(dict(name="notredame", a=49, b=62, bg=bg4(), flames=[], sprites=[mol4], focus=[(470, 1150), (470, 1300), (470, 1000), (470, 1250)],
        titles=[("MARS 1314", CREAM, 110, T(50), 440), ("NOTRE-DAME", RED, 100, T(55), 552)]))
    # 5 : prison perpetuelle, la foule attend qu'il baisse la tete
    def bg5():
        im = paper(125, 0.5, (40, 36, 40)); return im
    cr = []
    for k, x in enumerate((110, 280, 660, 830)):
        cr.append(Spr(lambda L, x=x: figure(L, x, 1560, 1.2, col=(10, 8, 7)), (x, 1400), lambda t, k=k: (0, 5*math.sin(t*2 + k), 0, 1, 1)))
    mol5 = Spr(lambda L: templar(L, 470, 1130, 0.9, mood=-1), (470, 1500), lambda t: (0, 40*ease((t - T(70))/0.8) - 0, 0, 1, 1))
    S.append(dict(name="perpetuelle", a=62, b=74, bg=bg5(), flames=[], sprites=cr + [mol5], focus=[(470, 1150), (470, 1000), (470, 1200)],
        titles=[("PRISON PERPÉTUELLE", CREAM, 84, T(62), 440), ("TOUS ATTENDENT", RED, 80, T(65), 552)]))
    # 6 : il releve la tete, renie ses aveux
    def bg6():
        im = paper(126, 0.35, (50, 42, 40)); glow(im, (470, 1000), 500, (240, 210, 160), 0.4); return im
    mol6 = Spr(lambda L: templar(L, 470, 1020, 1.15, mood=1), (470, 1500), lambda t: (0, -30*ease((t - T(74))/0.4), 0, 1.0 + 0.04*ease((t - T(74))/0.4), 1))
    rc = Spr(lambda L: stamp_red(L, "INNOCENT", 470, 1500, 120, -8), (470, 1500), pop(T(84), 0.12, 2.6), appear=T(84))
    S.append(dict(name="renie", a=74, b=88, bg=bg6(), flames=[], sprites=[mol6, rc], focus=[(470, 1050), (470, 950), (470, 1100)],
        titles=[("TU FAIS L'INVERSE", CREAM, 86, T(74), 440), ("ORDRE INNOCENT", RED, 96, T(85), 552)]))
    # 7 : Philippe le Bel
    def bg7():
        im = paper(127, 0.4, (44, 30, 34)); glow(im, (470, 1000), 460, (230, 180, 110), 0.3); return im
    k7 = Spr(lambda L: throne_king(L, 470, 1050, 0.95), (470, 1500), lambda t: breathe(t, 0.008, 0.6, 3))
    S.append(dict(name="roi", a=88, b=97, bg=bg7(), flames=[], sprites=[k7], focus=[(470, 1050), (470, 1000), (470, 1150)],
        titles=[("PHILIPPE LE BEL", CREAM, 90, T(90), 440), ("LE JOUR MÊME", RED, 100, T(94), 552)]))
    # 8 : pas de nouveau proces
    def bg8():
        im = paper(128, 0.5, (40, 36, 34)); door(im, 470, 1330, 1.4, grille=False); return im
    lk = Spr(lambda L: lock(L, 470, 1180, 1.2), (470, 1180), pop(T(99), 0.15, 2.0, 0.1), appear=T(99))
    S.append(dict(name="ferme", a=97, b=103, bg=bg8(), flames=[], sprites=[lk], focus=[(470, 1200), (470, 1150)],
        titles=[("PAS DE", CREAM, 100, T(97), 440), ("NOUVEAU PROCÈS", RED, 100, T(101), 552)]))
    # 9 : le soir, ile de la Seine
    def bg9():
        im = paper(129, 0.8, (18, 22, 40)); glow(im, (770, 900), 260, (220, 220, 240), 0.35)
        seine(im, 1250, 3); d = ImageDraw.Draw(im)
        d.ellipse((120, 1230, 980, 1330), fill=(26, 24, 22, 255), outline=INK+(255,), width=3)
        notre_dame(im, 560, 1260, 0.3); return im
    lant = Spr(lambda L: (ImageDraw.Draw(L).rectangle((150, 1420, 330, 1450), fill=(40, 28, 20, 255)), ImageDraw.Draw(L).ellipse((228, 1380, 252, 1420), fill=(250, 190, 80, 255))), (240, 1430),
               lambda t: (60*math.sin(t*0.8), 6*math.sin(t*1.7), 0, 1, 1))
    S.append(dict(name="ile", a=103, b=121, bg=bg9(), flames=[], sprites=[lant], focus=[(470, 1250), (400, 1300), (600, 1250), (470, 1300)],
        titles=[("LE SOIR MÊME", CREAM, 100, T(103), 440), ("ÎLE DE LA SEINE", RED, 92, T(110), 552)]))
    # 10 : le bucher (flammes seulement)
    def bg10():
        im = paper(130, 0.8, (22, 18, 28)); seine(im, 1500, 4); pyre(im, 470, 1380, 1.3); return im
    S.append(dict(name="bucher", a=121, b=131, bg=bg10(), flames=[Flame(400, 1380, 260, 120, on=T(124) - 0.2, ramp=0.4), Flame(540, 1380, 300, 130, on=T(124) - 0.1, ramp=0.4)],
        sprites=[], focus=[(470, 1250), (470, 1150), (470, 1300)],
        titles=[("LE BÛCHER", RED, 130, T(124), 440), ("AVEC GEOFFROY DE CHARNAY", CREAM, 58, T(128), 560)]))
    # 11 : la legende de la malediction
    def bg11():
        im = paper(131, 0.7, (34, 20, 40)); glow(im, (470, 1100), 520, (180, 30, 40), 0.3); return im
    ki = Spr(lambda L: throne_king(L, 250, 1150, 0.62), (250, 1500), lambda t: breathe(t, 0.008, 0.6, 3))
    po = Spr(lambda L: mitre(L, 760, 1150, 0.78), (760, 1500), lambda t: breathe(t, 0.008, 0.6, 3, 1.0))
    mal = Spr(lambda L: glow(L, (470, 1200), 360, (190, 20, 30), 0.7), (470, 1200), lambda t: (0, 0, 0, 1 + 0.06*math.sin(t*5), 0.5 + 0.4*math.sin(t*3)), appear=T(136))
    S.append(dict(name="legende", a=131, b=142, bg=bg11(), flames=[], sprites=[mal, ki, po], focus=[(470, 1150), (250, 1100), (760, 1100)],
        titles=[("SELON LA LÉGENDE", CREAM, 86, T(131), 440), ("LA MALÉDICTION", RED, 100, T(136), 552)]))
    # 12 : le pape meurt un mois plus tard
    def bg12():
        im = paper(132, 0.5, (40, 36, 44)); return im
    po2 = Spr(lambda L: mitre(L, 470, 1100, 1.0), (470, 1500), lambda t: (0, 0, 0, 1, 1 - ease((t - T(145))/(T(149) - T(145)))))
    S.append(dict(name="pape", a=142, b=149, bg=bg12(), flames=[], sprites=[po2], focus=[(470, 1100), (470, 1050)],
        titles=[("LE PAPE MEURT", CREAM, 100, T(143), 440), ("UN MOIS APRÈS", RED, 100, T(145), 552)]))
    # 13 : le roi avant la fin de l'annee
    def bg13():
        im = paper(133, 0.5, (40, 30, 34)); return im
    k13 = Spr(lambda L: throne_king(L, 470, 1100, 0.95), (470, 1500), lambda t: (0, 0, 0, 1, 1 - ease((t - T(153))/(T(156) - T(153)))))
    S.append(dict(name="roi_fin", a=149, b=156, bg=bg13(), flames=[], sprites=[k13], focus=[(470, 1100), (470, 1050)],
        titles=[("LE ROI AUSSI", CREAM, 100, T(149), 440), ("AVANT LA FIN DE L'ANNÉE", RED, 72, T(151), 552)]))
    # 14 : les historiens se mefient
    def bg14():
        im = paper(134, 0.4, (44, 38, 34)); d = ImageDraw.Draw(im); d.rounded_rectangle((250, 880, 690, 1560), radius=18, fill=(110, 28, 30, 255), outline=INK+(255,), width=6); d.rectangle((280, 910, 660, 1530), outline=GOLD+(255,), width=4)
        f = font(64); d.text((470 - f.getlength("LÉGENDE ?")/2, 1160), "LÉGENDE ?", font=f, fill=GOLD+(255,)); return im
    st14 = Spr(lambda L: stamp_red(L, "APRÈS COUP", 470, 1300, 100, -8), (470, 1300), pop(T(165), 0.12, 2.6), appear=T(165))
    S.append(dict(name="historiens", a=156, b=168, bg=bg14(), flames=[], sprites=[st14], focus=[(470, 1250), (470, 1200), (470, 1300)],
        titles=[("LES HISTORIENS", CREAM, 90, T(157), 440), ("SE MÉFIENT", RED, 100, T(159), 552)]))
    # 15 : la question (Molay dans l'ombre)
    def bg15():
        im = paper(135, 0.85, (22, 20, 22)); glow(im, (470, 1100), 420, (200, 170, 130), 0.18); return im
    mol15 = Spr(lambda L: templar(L, 470, 1150, 1.0, mood=2), (470, 1500), lambda t: (0, 0, 0, 1, 0.85))
    S.append(dict(name="question", a=168, b=180, bg=bg15(), flames=[], sprites=[mol15], focus=[(470, 1150), (470, 1100), (470, 1200)],
        titles=[("ET TOI,", CREAM, 110, T(168), 440), ("À SA PLACE,", CREAM, 96, T(170), 552), ("AVOUER OU TENIR ?", RED, 92, T(175), 660)]))
    # 16 : boucle
    S.append(dict(name="boucle", a=180, b=len(WORDS), bg=bg0(), flames=[], sprites=[mol0, bars0], focus=[(470, 1000), (470, 1040)], titles=[]))
    return S

IMPACTS = [(8, 18, (200, 30, 30)), (19, 22, (200, 30, 30)), (25, 8, None), (35, 12, None), (47, 14, None), (61, 8, None), (64, 12, None), (80, 20, (255, 255, 255)),
           (96, 10, None), (102, 14, None), (124, 26, (200, 30, 30)), (141, 14, None), (148, 14, None), (155, 14, None), (167, 18, (200, 30, 30))]

def shot_defs():
    S = []
    # ---- decor reutilisable : escalier + portier (1re image et boucle finale)
    def bg0():
        im = paper(90, 0.55, (30, 26, 28)); glow(im, (470, 1150), 460, (240, 190, 120), 0.2)
        stairs(im, 470, 1300, 0.95); return im
    por0 = Spr(lambda L: portier(L, 470, 980, 0.9, mood=2), (470, 1400), lambda t: breathe(t, 0.008, 0.8, 3))
    fl0 = Flame(470 + 250*0.9, 980 + 110*0.9, 110, 56)
    S.append(dict(name="escalier", a=0, b=15, bg=bg0(), flames=[fl0], sprites=[por0], focus=[(470, 1000), (600, 1100), (470, 1000)],
        titles=[("UN SOIR, IL DESCEND", CREAM, 96, 0.0, 440), ("UN ESCALIER", CREAM, 110, T(5), 552), ("ONZE ANS APRÈS", RED, 104, T(11), 660)]))
    # 1 : Val-de-Grace, la cour
    def bg1():
        im = paper(91, 0.5, (34, 30, 40)); glow(im, (200, 1000), 300, (240, 190, 110), 0.3); glow(im, (880, 1000), 300, (240, 190, 110), 0.3)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 1560, W, 1920), fill=(46, 42, 40, 255)); hatch(d, (0, 1560, W, 1920), 26, 0.1, (16, 14, 14, 110), 3)
        stairs(im, 470, 1300, 0.95); return im
    t1 = T(25); t2 = T(31)
    por1 = Spr(lambda L: portier(L, 470, 980, 0.62, mood=1, keys=False), (470, 1300),
               lambda t: (0, 330*ease((t - t1)/(t2 - t1)), 0, 1 - 0.35*ease((t - t1)/(t2 - t1)), 1 - 0.6*ease((t - t2 + 0.3)/0.8)))
    S.append(dict(name="cour", a=15, b=32, bg=bg1(), flames=[], sprites=[por1], focus=[(470, 1050), (470, 1200), (470, 1100), (470, 1250)],
        titles=[("PORTIER", CREAM, 110, T(18), 440), ("VAL-DE-GRÂCE", RED, 100, T(21), 552)]))
    # 2 : tu ne remonteras jamais (noir qui monte)
    def bg2():
        im = paper(92, 0.6, (30, 26, 28)); stairs(im, 470, 1300, 0.95); return im
    blk = Spr(lambda L: ImageDraw.Draw(L).rectangle((0, 0, W, H), fill=(0, 0, 0, 255)), (W/2, H/2),
              lambda t: (0, 0, 0, 1, 0.9*clamp01((t - T(33))/(T(36) - T(33)))), appear=T(32))
    S.append(dict(name="jamais", a=32, b=36, bg=bg2(), flames=[], sprites=[blk], focus=[(470, 1100), (470, 1250)],
        titles=[("TU NE REMONTERAS", CREAM, 84, T(32), 440), ("JAMAIS", RED, 140, T(35), 552)]))
    # 3 : reseau de carrieres
    def bg3():
        im = paper(93, 0.5, (40, 34, 28)); quarry_map(im, 470, 1250, 1.0, seed=5); return im
    pulse = Spr(lambda L: ImageDraw.Draw(L).ellipse((440, 760, 500, 820), outline=RED + (255,), width=8), (470, 790),
                lambda t: (0, 0, 0, 1 + 0.5*abs(math.sin(t*3)), 1 - 0.5*abs(math.sin(t*3))))
    S.append(dict(name="reseau", a=36, b=45, bg=bg3(), flames=[], sprites=[pulse], focus=[(470, 1250), (470, 900), (470, 1500)],
        titles=[("SOUS PARIS", CREAM, 120, T(36), 440), ("DES KILOMÈTRES DE GALERIES", RED, 64, T(41), 560)]))
    # 4 : couloirs noirs identiques
    def bg4():
        im = paper(94, 0.3, (30, 26, 24)); corridor(im, 470, 1180, 1.0, 9, lit=0.3); return im
    S.append(dict(name="couloirs", a=45, b=50, bg=bg4(), flames=[], sprites=[], focus=[(470, 1180), (470, 1150)],
        titles=[("DES COULOIRS NOIRS", CREAM, 90, T(45), 440), ("TOUS IDENTIQUES", RED, 100, T(48), 552)]))
    # 5 : ossements (rien de graphique : cranes stylises)
    def bg5():
        im = paper(95, 0.5, (30, 26, 24)); ossuary(im, 880, 1920, seed=3, r=40); glow(im, (470, 1300), 480, (240, 190, 120), 0.18); return im
    S.append(dict(name="ossements", a=50, b=64, bg=bg5(), flames=[], sprites=[], focus=[(470, 1300), (300, 1250), (700, 1400), (470, 1250)],
        titles=[("DEPUIS 7 ANS", CREAM, 100, T(50), 440), ("≈ 6 MILLIONS", RED, 124, T(61), 552), ("D'OSSEMENTS", CREAM, 66, T(61) + 0.3, 650)]))
    # 6 : bougie + trousseau
    def bg6():
        im = paper(96, 0.5, (30, 26, 24)); corridor(im, 470, 1200, 1.0, 9, lit=0.05); return im
    por6 = Spr(lambda L: portier(L, 470, 1040, 1.0, mood=1), (470, 1500), lambda t: breathe(t, 0.01, 0.8, 4))
    fl6 = Flame(470 + 250, 1040 + 110, 120, 60)
    S.append(dict(name="bougie", a=64, b=80, bg=bg6(), flames=[fl6], sprites=[por6], focus=[(470, 1100), (700, 1150), (470, 1250), (470, 1050)],
        titles=[("UNE BOUGIE", CREAM, 110, T(65), 440), ("UN TROUSSEAU DE CLÉS", RED, 76, T(69), 552)]))
    # 7 : la legende de la bouteille
    def bg7():
        im = paper(97, 0.4, (44, 36, 30)); glow(im, (470, 1200), 420, (200, 150, 90), 0.2); return im
    def bottle(L):
        d = ImageDraw.Draw(L)
        d.rounded_rectangle((690, 1230, 870, 1620), radius=40, fill=(60, 110, 70, 255), outline=INK + (255,), width=5)
        d.rectangle((755, 1100, 805, 1240), fill=(60, 110, 70, 255), outline=INK + (255,), width=5)
        d.rectangle((748, 1080, 812, 1110), fill=(120, 80, 40, 255), outline=INK + (255,), width=4)
        d.rectangle((700, 1330, 860, 1520), fill=(210, 190, 120, 255), outline=INK + (255,), width=3)
    por7 = Spr(lambda L: portier(L, 310, 1080, 0.9, mood=-1, keys=False, with_candle=False), (310, 1500), lambda t: breathe(t, 0.01, 0.8, 4))
    bo = Spr(bottle, (780, 1350), pop(T(86), 0.2, 1.5, 0.1), appear=T(86))
    S.append(dict(name="legende", a=80, b=89, bg=bg7(), flames=[], sprites=[por7, bo], focus=[(310, 1100), (780, 1350)],
        titles=[("SELON LA LÉGENDE", CREAM, 88, T(80), 440), ("UNE BOUTEILLE ?", RED, 110, T(86), 552)]))
    # 8 : la lumiere s'eteint
    def bg8():
        im = paper(98, 0.3, (30, 26, 24)); corridor(im, 470, 1150, 1.0, 9, lit=0.1); return im
    por8 = Spr(lambda L: portier(L, 470, 1130, 0.7, mood=1, keys=False), (470, 1450), lambda t: breathe(t, 0.01, 0.8, 4))
    fl8 = Flame(470 + 250*0.7, 1130 + 110*0.7, 90, 46, off=T(95) + 0.1, ramp=0.1)
    dk = Spr(lambda L: ImageDraw.Draw(L).rectangle((0, 0, W, H), fill=(0, 0, 0, 255)), (W/2, H/2),
             lambda t: (0, 0, 0, 1, 0.85*clamp01((t - T(95))/0.35)), appear=T(94))
    S.append(dict(name="eteint", a=89, b=96, bg=bg8(), flames=[fl8], sprites=[por8, dk], focus=[(470, 1150), (470, 1130)],
        titles=[("PEUT-ÊTRE", CREAM, 100, T(91), 440), ("LA LUMIÈRE S'ÉTEINT", RED, 76, T(94), 552)]))
    # 9 : gauche / droite
    def bg9():
        im = paper(99, 0.3, (30, 26, 24)); fork(im, 470, 1200, 1.0); return im
    por9 = Spr(lambda L: portier(L, 470, 1300, 0.5, mood=1, keys=False, with_candle=False), (470, 1500),
               lambda t: (-120*ease((t - T(98))/0.5) + 240*ease((t - T(100))/0.5), 0, 0, 1, 1))
    S.append(dict(name="fourche", a=96, b=103, bg=bg9(), flames=[], sprites=[por9], focus=[(470, 1200), (300, 1200), (640, 1200)],
        titles=[("À GAUCHE", CREAM, 110, T(98), 440), ("PUIS À DROITE", RED, 100, T(100), 552)]))
    # 10 : chaque couloir ressemble au precedent
    def bg10():
        im = paper(100, 0.3, (30, 26, 24)); corridor(im, 470, 1180, 1.0, 11, lit=0.2); return im
    S.append(dict(name="memes", a=103, b=108, bg=bg10(), flames=[], sprites=[], focus=[(470, 1180), (470, 1150)],
        titles=[("CHAQUE COULOIR", CREAM, 96, T(103), 440), ("LE MÊME", RED, 120, T(105), 552)]))
    # 11 : 3 novembre 1793
    def bg11():
        im = paper(101, 0.3, (66, 52, 40)); calendar_sheet2(im, 470, 1290, 600, 700, -3, "NOVEMBRE 1793", "3"); return im
    st11 = Spr(lambda L: stamp_red(L, "DISPARU", 480, 1380, 120, -10), (480, 1380), pop(T(115), 0.12, 2.6), appear=T(115))
    S.append(dict(name="calendrier", a=108, b=116, bg=bg11(), flames=[], sprites=[st11], focus=[(470, 1250), (470, 1200), (470, 1300)],
        titles=[("3 NOVEMBRE 1793", CREAM, 100, T(108), 440)]))
    # 12 : personne ne te retrouve
    def bg12():
        im = paper(102, 0.6, (24, 24, 34)); corridor(im, 470, 1250, 0.9, 9, lit=0.0); return im
    gh = Spr(lambda L: portier(L, 470, 1130, 0.7, mood=2, keys=False, with_candle=False), (470, 1450), lambda t: (0, 0, 0, 1, 1 - ease((t - T(117))/(T(121) - T(117)))))
    S.append(dict(name="personne", a=116, b=121, bg=bg12(), flames=[], sprites=[gh], focus=[(470, 1150), (470, 1130)],
        titles=[("PERSONNE", CREAM, 120, T(117), 440), ("NE TE RETROUVE", RED, 90, T(119), 552)]))
    # 13 : onze ans passent (pages)
    def bg13():
        im = paper(103, 0.4, (50, 42, 38)); return im
    pgs = []
    for k in range(6):
        ap = T(121) + k*0.16
        pgs.append(Spr(lambda L, k=k: paper_sheet(L, 200 + k*130, 1100, 170, 220, 12*k - 30, 0, k), (200 + k*130, 1100),
                       lambda t, ap=ap, k=k: (30*math.sin((t - ap)*3 + k), 500*clamp01((t - ap)/1.1), 140*(t - ap), 1, 1 - clamp01((t - ap - 0.8)/0.4)), appear=ap))
    S.append(dict(name="pages", a=121, b=124, bg=bg13(), flames=[], sprites=pgs, focus=[(470, 1200)],
        titles=[("11 ANS", RED, 150, T(121), 440)]))
    # 14 : la decouverte
    def bg14():
        im = paper(104, 0.5, (30, 26, 24)); corridor(im, 470, 1200, 1.0, 9, lit=0.1); glow(im, (470, 1400), 500, (240, 190, 120), 0.18); return im
    wl = Spr(lambda L: worker(L, 250, 1560, 1.1), (250, 1300), lambda t: breathe(t, 0.01, 1.0, 4))
    wr = Spr(lambda L: worker(L, 760, 1560, 1.1), (760, 1300), lambda t: breathe(t, 0.01, 1.0, 4, 1.0))
    S.append(dict(name="decouverte", a=124, b=139, bg=bg14(), flames=[], sprites=[wl, wr], focus=[(470, 1300), (330, 1300), (700, 1300)],
        titles=[("1804", CREAM, 130, T(125), 440), ("RUE D'ENFER", RED, 110, T(137), 552)]))
    # 15 : le trousseau
    def bg15():
        im = paper(105, 0.4, (30, 26, 24)); glow(im, (470, 1150), 480, (240, 200, 130), 0.3); return im
    kr = Spr(lambda L: keyring(L, 470, 1020, 1.5), (470, 1020), lambda t: (0, 0, 4*math.sin(t*2), 1, 1), appear=T(139))
    S.append(dict(name="trousseau", a=139, b=148, bg=bg15(), flames=[], sprites=[kr], focus=[(470, 1150), (470, 1000)],
        titles=[("UN TROUSSEAU DE CLÉS", CREAM, 76, T(141), 440), ("VAL-DE-GRÂCE", RED, 100, T(146), 552)]))
    # 16 : c'est toi
    def bg16():
        im = paper(106, 0.4, (40, 34, 30)); glow(im, (470, 1050), 440, (240, 190, 120), 0.25); return im
    por16 = Spr(lambda L: portier(L, 470, 1000, 1.2, mood=2, keys=False, with_candle=False), (470, 1500), lambda t: breathe(t, 0.008, 0.6, 3))
    S.append(dict(name="toi", a=148, b=150, bg=bg16(), flames=[], sprites=[por16], focus=[(470, 1050)],
        titles=[("C'EST TOI", RED, 140, T(148), 440)]))
    # 17 : la tombe
    def bg17():
        im = paper(107, 0.5, (34, 34, 40)); glow(im, (470, 1200), 480, (170, 180, 200), 0.18); tombstone(im, 470, 1330, 1.0); return im
    S.append(dict(name="tombe", a=150, b=159, bg=bg17(), flames=[], sprites=[], focus=[(470, 1330), (470, 1200), (470, 1450)],
        titles=[("ENTERRÉ SUR PLACE", CREAM, 84, T(150), 440), ("TOUJOURS LÀ", RED, 110, T(157), 552)]))
    # 18 : la question (noir, bougie eteinte)
    def bg18():
        im = paper(108, 0.9, (22, 20, 20)); candle(im, 470, 1500, 1.4, lit=False); return im
    S.append(dict(name="question", a=159, b=171, bg=bg18(), flames=[], sprites=[], focus=[(470, 1300), (470, 1150), (470, 1400)],
        titles=[("ET TOI,", CREAM, 110, T(159), 440), ("DANS LE NOIR", CREAM, 96, T(164), 552), ("TU FAIS QUOI ?", RED, 116, T(167), 660)]))
    # 19 : boucle vers la 1re image
    S.append(dict(name="boucle", a=171, b=len(WORDS), bg=bg0(), flames=[Flame(470 + 250*0.9, 980 + 110*0.9, 110, 56)], sprites=[por0], focus=[(470, 1000), (470, 1050)], titles=[]))
    return S

IMPACTS = [(5, 8, None), (14, 18, (200, 30, 30)), (22, 8, None), (35, 24, (200, 30, 30)), (45, 8, None), (61, 14, None), (67, 10, None), (86, 10, None),
           (95, 22, (255, 255, 255)), (115, 28, (200, 30, 30)), (121, 14, None), (131, 10, None), (142, 12, None), (149, 30, (200, 30, 30)), (158, 14, None), (170, 12, None)]

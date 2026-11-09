def shot_defs():
    S = []
    def bg_door(seed=60):
        im = paper(seed, 0.35, (52, 44, 40))
        glow(im, (470, 1080), 420, (240, 190, 120), 0.18)
        door(im, 470, 1090, 1.5)
        return im
    # 0 : hook - porte de cellule, le petit prince derriere la grille (visible des la 1re image)
    def bg0():
        im = paper(60, 0.35, (52, 44, 40)); glow(im, (470, 1250), 420, (240, 190, 120), 0.18)
        door(im, 470, 1330, 1.5)
        d = ImageDraw.Draw(im)
        d.rectangle((470-150, 1330-510, 470+150, 1330-255), fill=(10, 8, 8, 255), outline=INK+(255,), width=8)
        return im
    face = Spr(lambda L: prince(L, 470, 940, 0.9, mood=2, body=False), (470, 1000), lambda t: breathe(t, 0.008, 0.8, 3))
    bars = Spr(lambda L: grille_bars(L, 470, 1330, 1.5), (470, 1200), lambda t: (0, 0, 0, 1, 1))
    S.append(dict(name="porte", a=0, b=14, bg=bg0(), flames=[], sprites=[face, bars], focus=[(470, 1000), (470, 1040), (470, 980)],
        titles=[("ON DISAIT QU'IL", CREAM, 104, 0.0, 440), ("S'ÉTAIT ÉVADÉ", CREAM, 104, T(9), 552)]))
    # 1 : le coeur desseche dans son bocal
    def bg1():
        im = paper(61, 0.3, (60, 42, 30)); jar(im, 470, 1230, 1.3); return im
    S.append(dict(name="bocal", a=14, b=21, bg=bg1(), flames=[Flame(790, 940, 120, 62)], sprites=[], focus=[(470, 1200), (470, 1160), (470, 1140)],
        titles=[("UN CŒUR A PROUVÉ", CREAM, 96, T(14), 440), ("LE CONTRAIRE", RED, 124, T(18), 552)]))
    # 2 : tu as sept ans (portrait du petit prince)
    def bg2():
        im = paper(62, 0.3, (60, 54, 66)); glow(im, (470, 1000), 440, (200, 190, 210), 0.22); return im
    p2 = Spr(lambda L: prince(L, 470, 1040, 1.15, mood=2), (470, 1500), lambda t: breathe(t, 0.01, 1.0, 5))
    S.append(dict(name="sept_ans", a=21, b=26, bg=bg2(), flames=[], sprites=[p2], focus=[(470, 1000), (470, 950), (470, 1000)],
        titles=[("TU AS 7 ANS", CREAM, 124, T(22), 440)]))
    # 3 : le pere est guillotine (couperet, rien de montre)
    def bg3():
        im = paper(63, 0.15, (92, 66, 48)); houses(im, 1250, 21, lit=False); guillotine(im, 470, 1400, 1.2, blade=False, col=(78, 54, 38)); return im
    tb = T(29)
    bl = Spr(lambda L: blade_only(L, 470, 1400 - 600*1.2, 1.2), (470, 1400 - 600*1.2), lambda t: (0, 390*1.2*ease((t - tb)/0.18) if t > tb else 0, 0, 1, 1))
    blk = Spr(lambda L: ImageDraw.Draw(L).rectangle((0, 0, W, H), fill=(0, 0, 0, 255)), (W/2, H/2), lambda t: (0, 0, 0, 1, clamp01((t - tb - 0.2)/0.25)), appear=tb)
    S.append(dict(name="pere", a=26, b=30, bg=bg3(), flames=[], sprites=[bl, blk], focus=[(470, 1000), (470, 1150)],
        titles=[("TON PÈRE", CREAM, 110, T(26), 440)]))
    # 4 : roi de France pour les royalistes (couronne)
    def bg4():
        im = paper(64, 0.25, (66, 50, 60)); glow(im, (470, 900), 460, (230, 190, 120), 0.3); return im
    p4 = Spr(lambda L: prince(L, 470, 1040, 1.15, mood=1), (470, 1500), lambda t: breathe(t, 0.01, 1.0, 5))
    tc = T(35)
    cr = Spr(lambda L: crown_obj(L, 470, 820, 1.0), (470, 820), lambda t: (0, -140*max(0, 1 - ease((t - tc)/0.3)), 0, 1, clamp01((t - tc)/0.1)), appear=tc)
    S.append(dict(name="couronne", a=30, b=40, bg=bg4(), flames=[], sprites=[p4, cr], focus=[(470, 980), (470, 800), (470, 950)],
        titles=[("POUR LES ROYALISTES", CREAM, 84, T(30), 440), ("LOUIS XVII", RED, 130, T(35), 552)]))
    # 5 : la tour du Temple, Paris
    def bg5():
        im = paper(65, 0.6, (34, 36, 52)); houses(im, 1500, 5, lit=False); tower(im, 470, 1560, 1.15, lit=(4,)); return im
    lights = []
    for k, (row, col) in enumerate(((0, 0), (1, 2), (2, 1), (3, 0))):
        wx = 470 - 100*1.15 + col*100*1.15; wy = 1560 - 640*1.15 + row*130*1.15
        lights.append(Spr(lambda L, wx=wx, wy=wy: ImageDraw.Draw(L).rectangle((wx-18*1.15, wy, wx+18*1.15, wy+64*1.15), fill=(250, 190, 80, 255), outline=INK+(255,), width=2), (wx, wy+36),
                          lambda t, k=k: (0, 0, 0, 1, 0.6 + 0.4*math.sin(t*5 + k*2)), appear=T(41) + k*0.7))
    S.append(dict(name="temple", a=40, b=51, bg=bg5(), flames=[], sprites=lights, focus=[(470, 900), (470, 1000), (470, 850), (470, 1100)],
        titles=[("PRISON DU TEMPLE", CREAM, 88, T(46), 440), ("PARIS", RED, 120, T(50), 552)]))
    # 6 : on t'arrache a sa mere
    mom = Spr(lambda L: queen(L, 300, 1070, 0.85, mood=2), (300, 1400), lambda t: breathe(t, 0.01, 1.0, 4))
    t0 = T(52)
    away = lambda t, k=0: (430*ease((t - t0)/1.6) if t > t0 else 0, 4*math.sin(t*6 + k), 0, 1, 1)
    kid = Spr(lambda L: prince(L, 700, 1180, 0.5, mood=2), (700, 1330), lambda t: away(t, 1))
    gd = Spr(lambda L: figure(L, 840, 1370, 1.15, col=(8, 6, 5), hat=True), (840, 1230), lambda t: away(t, 2))
    S.append(dict(name="mere", a=51, b=61, bg=paper(66, 0.3, (64, 46, 40)), flames=[], sprites=[mom, kid, gd], focus=[(300, 1000), (720, 1150), (470, 1100)],
        titles=[("ARRACHÉ À SA MÈRE", CREAM, 88, T(52), 440), ("JAMAIS REVUE", RED, 100, T(59), 552)]))
    # 7 : le cordonnier Simon
    def bg7():
        im = paper(67, 0.35, (66, 48, 34)); d = ImageDraw.Draw(im)
        d.rectangle((560, 1300, 1000, 1340), fill=(60, 38, 22, 255), outline=INK+(255,), width=4); d.rectangle((590, 1340, 970, 1560), fill=(40, 26, 16, 255))
        return im
    sim = Spr(lambda L: simon(L, 360, 1560, 1.75), (360, 1330), lambda t: breathe(t, 0.008, 1.4, 4))
    bon = Spr(lambda L: bonnet_rouge(L, 770, 1230, 1.0), (770, 1290), pop(T(67), 0.2, 1.6, 0.1), appear=T(67))
    S.append(dict(name="simon", a=61, b=70, bg=bg7(), flames=[], sprites=[sim, bon], focus=[(300, 1050), (700, 1230), (400, 1100)],
        titles=[("UN CORDONNIER", CREAM, 96, T(61), 440), ("UN PETIT RÉPUBLICAIN", RED, 80, T(67), 552)]))
    # 8 : seul, des mois, dans le noir (la bougie fond)
    def bg8():
        im = cell_bg(68, 0.55); d = ImageDraw.Draw(im)
        d.rectangle((60, 1290, 1020, 1330), fill=(60, 38, 22, 255), outline=INK+(255,), width=4); d.rectangle((90, 1330, 990, 1600), fill=(40, 26, 16, 255))
        return im
    fl8 = Flame(560, 1100, 130, 66, off=T(78) + 0.2, ramp=0.1)
    def dyn_candle(world, t, fr):
        p = clamp01((t - T(70))/(T(78) - T(70)))
        h = 170*1.3*(1 - 0.75*p)
        d = ImageDraw.Draw(world)
        d.rectangle((560 - 22*1.3, 1290 - h, 560 + 22*1.3, 1290), fill=(225, 210, 170, 255), outline=INK+(255,), width=3)
        fl8.y = 1290 - h - 8; fl8.h = int(130*(1 - 0.3*p))
    kb = Spr(lambda L: kid_back(L, 300, 1020, 1.2), (300, 1300), lambda t: breathe(t, 0.006, 0.6, 3))
    S.append(dict(name="seul", a=70, b=79, bg=bg8(), flames=[fl8], sprites=[kb], dyn=[dyn_candle], focus=[(430, 1000), (560, 1100), (300, 1000)],
        titles=[("SEUL.", CREAM, 130, T(74), 440), ("DES MOIS.", RED, 110, T(76), 570)]))
    # 9 : 8 juin 1795
    def bg9():
        im = paper(69, 0.3, (66, 52, 40)); calendar_sheet(im, 470, 1290, 600, 700, -3); return im
    st9 = Spr(lambda L: stamp_red(L, "MORT", 480, 1380, 140, -10), (480, 1380), pop(T(86), 0.12, 2.6), appear=T(86))
    S.append(dict(name="calendrier", a=79, b=87, bg=bg9(), flames=[], sprites=[st9], focus=[(470, 1150), (470, 1250), (470, 1200)],
        titles=[("8 JUIN 1795", CREAM, 120, T(81), 440)]))
    # 10 : lit vide, dix ans
    def bg10():
        im = cell_bg(70, 0.45); bed(im, 470, 1180, 1.3); return im
    ray = Spr(lambda L: glow(L, (500, 1150), 420, (200, 215, 240), 0.5), (500, 1150), lambda t: (0, 0, 0, 1 + 0.03*math.sin(t*2), 0.5 + 0.5*clamp01((t - T(87))/1.2)))
    S.append(dict(name="lit", a=87, b=95, bg=bg10(), flames=[], sprites=[ray], focus=[(470, 1100), (470, 1180), (470, 1100)],
        titles=[("10 ANS", RED, 150, T(89), 440)]))
    # 11 : fosse commune, brume
    def bg11():
        im = paper(71, 0.6, (40, 40, 52)); crosses(im, 1000, 3); return im
    fog = Spr(lambda L: glow(L, (300, 1150), 380, (170, 180, 195), 0.5), (300, 1150), lambda t: (80*math.sin(t*0.9), 0, 0, 1, 0.6))
    S.append(dict(name="fosse", a=95, b=101, bg=bg11(), flames=[], sprites=[fog], focus=[(470, 1200), (470, 1150), (470, 1250)],
        titles=[("FOSSE COMMUNE", CREAM, 100, T(98), 440)]))
    # 12 : le medecin et le mouchoir
    def bg12():
        im = paper(72, 0.3, (60, 44, 40)); return im
    doc = Spr(lambda L: doctor(L, 400, 1030, 1.0), (400, 1450), lambda t: breathe(t, 0.01, 0.8, 4))
    tm = T(113)
    hk = Spr(lambda L: handkerchief(L, 640, 1160, 1.0, 0.0), (640, 1160), lambda t: ((-230 + 0)*ease((t - tm)/0.7) * 0 + 300*ease((t - tm)/0.7) * 0 + 0 + (130*ease((t - tm)/0.7)), 20*ease((t - tm)/0.7) + 8*math.sin(t*3), -6*ease((t - tm)/0.7), 1 - 0.45*ease((t - tm)/0.7), 1))
    hk_red = Spr(lambda L: handkerchief(L, 640, 1160, 1.0, 1.0), (640, 1160), lambda t: ((130*ease((t - tm)/0.7)), 20*ease((t - tm)/0.7), -6*ease((t - tm)/0.7), 1 - 0.45*ease((t - tm)/0.7), clamp01((t - tm - 0.2)/0.6)), appear=tm)
    S.append(dict(name="medecin", a=101, b=116, bg=bg12(), flames=[], sprites=[doc, hk, hk_red], focus=[(400, 1000), (640, 1180), (470, 1050), (400, 1000)],
        titles=[("SELON LA TRADITION", CREAM, 84, T(102), 440), ("UN MOUCHOIR", RED, 110, T(113), 552)]))
    # 13 : la rumeur
    def bg13():
        im = paper(73, 0.45, (46, 42, 52)); question_mark(im, 700, 1000, 900, 55); return im
    fig = []
    for k, x in enumerate((130, 330, 530, 880)):
        fig.append(Spr(lambda L, x=x, k=k: pointing(L, x, 1500, 1.15, dirx=1 if x < 700 else -1), (x, 1330), lambda t, k=k: (0, 5*abs(math.sin(t*4 + k)), 2*math.sin(t*3 + k), 1, 1)))
    tgt = Spr(lambda L: prince(L, 760, 1040, 0.55, mood=1), (760, 1300), lambda t: breathe(t, 0.01, 1.2, 4))
    S.append(dict(name="rumeur", a=116, b=131, bg=bg13(), flames=[], sprites=[tgt] + fig, focus=[(470, 1150), (700, 1100), (300, 1300), (470, 1050)],
        titles=[("LA RUMEUR", CREAM, 120, T(116), 440), ("PAS LE VRAI ROI", RED, 104, T(124), 552), ("LE VRAI S'EST ENFUI", CREAM, 68, T(127), 640)]))
    # 14 : le coeur passe de main en main
    def bg14():
        im = paper(74, 0.35, (62, 44, 34)); return im
    hand_x = lambda t: 120 + 740*clamp01((t - T(131))/(T(141) - T(131)))
    jr = Spr(lambda L: jar(L, 470, 1050, 0.55, lit=False), (470, 1050), lambda t: (hand_x(t) - 470, 12*math.sin(t*4), 4*math.sin(t*3), 1, 1))
    hs = []
    for k, x in enumerate((120, 470, 820)):
        hs.append(Spr(lambda L, x=x: figure(L, x, 1500, 1.3, col=(10, 7, 6)), (x, 1330), lambda t, k=k: (0, 6*math.sin(t*2 + k), 0, 1, 1)))
    S.append(dict(name="main", a=131, b=141, bg=bg14(), flames=[], sprites=hs + [jr], focus=[(300, 1100), (470, 1060), (700, 1100)], titles=[]))
    # 15 : un pillage
    def bg15():
        im = paper(75, 0.45, (60, 40, 32)); furniture(im, 4); return im
    papers = []
    for k in range(7):
        ap = T(142) + k*0.12
        papers.append(Spr(lambda L, k=k: paper_sheet(L, 300 + k*70, 1250, 140, 180, 12*k - 40, 0, k), (300 + k*70, 1250), lambda t, ap=ap, k=k: (60*math.sin((t - ap)*3 + k), -260*clamp01((t - ap)/1.2) + 330*clamp01((t - ap - 1.2)/1.5), 90*(t - ap), 1, 1 - clamp01((t - ap - 1.8)/0.5)), appear=ap))
    jr2 = Spr(lambda L: jar(L, 470, 1050, 0.6, lit=False), (470, 1050), lambda t: (0, -90 + 90*ease((t - T(145))/0.4), 8*math.sin(t*9)*(1 if t < T(145) else 0.2), 1, 1))
    S.append(dict(name="pillage", a=141, b=147, bg=bg15(), flames=[], sprites=papers + [jr2], focus=[(470, 1150), (470, 1050), (470, 1100)],
        titles=[("1830", CREAM, 130, T(142), 440), ("UN PILLAGE", RED, 110, T(145), 572)]))
    # 16 : le laboratoire, l'ADN
    def bg16():
        im = paper(76, 0.3, (40, 54, 56)); d = ImageDraw.Draw(im)
        d.rectangle((60, 1470, 1020, 1510), fill=(60, 38, 22, 255), outline=INK+(255,), width=4)
        flask(im, 200, 1350, 1.0); flask(im, 860, 1350, 0.9, (170, 90, 150)); hair_frame(im, 470, 1380, 0.95)
        return im
    hx = Spr(lambda L: helix(L, 470, 1030, 340, 120, 0.0), (470, 1030), lambda t: (0, 0, 0, 1, clamp01((t - T(153))/0.5)), appear=T(153))
    S.append(dict(name="labo", a=147, b=164, bg=bg16(), flames=[], sprites=[hx], focus=[(470, 1100), (470, 1000), (200, 1300), (470, 1250), (470, 1000)],
        titles=[("EN L'AN 2000", CREAM, 96, T(147), 440), ("L'ADN", RED, 124, T(155), 560)]))
    # 17 : c'est bien toi
    def bg17():
        im = paper(77, 0.35, (40, 40, 52)); glow(im, (470, 950), 460, (110, 140, 220), 0.35); return im
    hA = Spr(lambda L: helix(L, 330, 950, 640, 110, 0.0, (200, 40, 40), (60, 120, 210)), (330, 950), lambda t: (150*ease((t - T(164))/0.9), 0, 0, 1, 1))
    hB = Spr(lambda L: helix(L, 610, 950, 640, 110, 0.0, (200, 40, 40), (60, 120, 210)), (610, 950), lambda t: (-150*ease((t - T(164))/0.9), 0, 0, 1, 1))
    st17 = Spr(lambda L: stamp_red(L, "C'EST BIEN LUI", 470, 1230, 84, -8), (470, 1230), pop(T(165), 0.12, 2.6), appear=T(165))
    S.append(dict(name="verdict", a=164, b=168, bg=bg17(), flames=[], sprites=[hA, hB, st17], focus=[(470, 950), (470, 1150), (470, 1180)], titles=[("VERDICT", CREAM, 110, T(164), 440)]))
    # 18 : mort dans sa cellule
    def bg18():
        im = cell_bg(78, 0.6); d = ImageDraw.Draw(im)
        d.rectangle((60, 1500, 1020, 1540), fill=(46, 30, 20, 255)); kid_back(im, 400, 1130, 1.2); return im
    S.append(dict(name="cellule", a=168, b=174, bg=bg18(), flames=[], sprites=[], focus=[(400, 1150), (470, 1100)],
        titles=[("MORT DANS", CREAM, 96, T(168), 440), ("SA CELLULE", RED, 112, T(172), 552)]))
    # 19 : Saint-Denis, le coeur parmi les rois
    def bg19():
        im = paper(79, 0.5, (40, 38, 46)); basilica(im, 470, 1450, 1.0); urn(im, 470, 1110, 1.3); return im
    S.append(dict(name="saint_denis", a=174, b=188, bg=bg19(), flames=[], sprites=[], focus=[(470, 1100), (470, 1050), (470, 900), (470, 1150)],
        titles=[("DEPUIS 2004", CREAM, 100, T(174), 440), ("SAINT-DENIS", RED, 108, T(181), 552)]))
    # 20 : la couronne sur l'urne, de travers
    def bg20():
        im = paper(80, 0.5, (40, 38, 46)); basilica(im, 470, 1450, 1.0); urn(im, 470, 1110, 1.3); return im
    tcr = T(189)
    cr2 = Spr(lambda L: crown_obj(L, 470, 880, 1.0), (470, 880), lambda t: (0, -260*(1 - ease((t - tcr)/0.5)), 12*ease((t - tcr)/0.5), 1, clamp01((t - tcr)/0.1)), appear=tcr)
    S.append(dict(name="couronne2", a=188, b=197, bg=bg20(), flames=[], sprites=[cr2], focus=[(470, 1000), (470, 950), (470, 1100)],
        titles=[("JAMAIS ROI", CREAM, 110, T(189), 440), ("ENFIN RENTRÉ", RED, 110, T(195), 552)]))
    # 21 : la question finale, fond noir, une bougie
    def bg21():
        im = paper(81, 0.9, (30, 26, 24)); candle(im, 200, 1280, 1.1, lit=False); return im
    S.append(dict(name="question", a=197, b=210, bg=bg21(), flames=[Flame(200, 1272, 120, 60)], sprites=[], focus=[(470, 1000), (300, 1150), (470, 1000)],
        titles=[("POURQUOI TANT", CREAM, 104, T(199), 440), ("DE GENS ONT REFUSÉ", CREAM, 84, T(202), 560), ("D'Y CROIRE ?", RED, 116, T(206), 660)]))
    # 22 : boucle vers la 1re image
    S.append(dict(name="boucle", a=210, b=len(WORDS), bg=bg0(), flames=[], sprites=[face, bars], focus=[(470, 1000), (470, 1040)], titles=[]))
    return S

IMPACTS = [(4, 8, None), (18, 24, (200, 30, 30)), (22, 8, None), (29, 28, (255, 255, 255)), (35, 20, (200, 30, 30)), (46, 8, None), (52, 14, None),
           (67, 12, None), (74, 10, None), (86, 28, (200, 30, 30)), (89, 12, None), (113, 10, None), (116, 10, None), (130, 12, None), (142, 8, None),
           (145, 20, (255, 255, 255)), (155, 10, None), (165, 30, (200, 30, 30)), (173, 12, None), (181, 10, None), (189, 18, None), (199, 8, None)]

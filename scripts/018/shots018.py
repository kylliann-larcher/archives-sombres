# Plans de la video 018 (le Masque de fer). Indices = numeros de mots de words2.json.
def shot_defs():
    S = []; G = globals()
    def cell_man(seed, mask=True, shackle=False):
        im = paper(seed, 0.2, (50, 40, 34)); cell_walls(im, seed, True); masked_man(im, 470, 1150, 1.1, mask, shackle); return im
    hook_bg = cell_man(181)
    S.append(dict(name="hook", a=0, b=9, bg=hook_bg, flames=[], sprites=[], focus=[(470, 1150), (470, 1100), (470, 1200)],
        titles=[("34 ANS DE PRISON", CREAM, 84, -0.3, 440), ("S'IL PARLAIT...", RED, 100, T(4), 552), ("ON LE TUAIT.", RED, 100, T(6), 552)]))
    # 1 promesse : un ordre scelle
    def bg1():
        im = paper(182, 0.45, (50, 36, 26)); paper_sheet(im, 470, 1330, 560, 660, -3, 0.0, 3); candle(im, 870, 1640, 1.0, False); return im
    st1 = Spr(lambda L: stamp_red(L, "SECRET", 470, 1360, 110, -8), (470, 1360), pop(T(12), 0.12, 2.4), appear=T(12))
    S.append(dict(name="promesse", a=9, b=18, bg=bg1(), flames=[Flame(870, 1632, 90, 46)], sprites=[st1], focus=[(470, 1250), (470, 1150)],
        titles=[("AUJOURD'HUI ENCORE", CREAM, 80, T(9), 440), ("PERSONNE NE SAIT QUI", RED, 88, T(12), 552)]))
    # 2 arrestation de nuit
    def bg2():
        im = paper(183, 0.7, (26, 26, 40)); glow(im, (800, 950), 160, (230, 230, 200), 0.4)
        d = ImageDraw.Draw(im); d.ellipse((760, 910, 840, 990), fill=(236, 230, 200, 255)); houses(im, 1600, 4, False)
        d = ImageDraw.Draw(im); d.rectangle((0, 1600, W, H), fill=(20, 16, 14, 255)); return im
    man = Spr(lambda L: figure(L, 470, 1640, 2.0, col=(70, 60, 80)), (470, 1450), lambda t: breathe(t, 0.01, 0.6, 2))
    guards = [Spr(lambda L, x=x: figure(L, x, 1660, 2.1, col=(8, 6, 5), hat=True), (x, 1450), lambda t: (0, 0, 0, 1, 1), appear=T(23) + k*0.15) for k, x in enumerate((230, 710))]
    S.append(dict(name="arrestation", a=18, b=27, bg=bg2(), flames=[], sprites=[man] + guards, focus=[(470, 1300), (470, 1200)],
        titles=[("JUILLET 1669", CREAM, 84, T(18), 440), ("ARRÊTÉ PRÈS DE CALAIS", RED, 84, T(23), 552)]))
    # 3 l'ordre : un seul nom
    def bg3():
        im = paper(184, 0.4, (54, 40, 28)); paper_sheet(im, 470, 1330, 600, 660, 2, 0.0, 5)
        d = ImageDraw.Draw(im); d.rectangle((210, 1250, 730, 1400), fill=(222, 204, 160, 255)); return im
    nm = Spr(lambda L: ImageDraw.Draw(L).text((470 - fserif(44).getlength("EUSTACHE DAUGER")/2, 1300), "EUSTACHE DAUGER", font=fserif(44), fill=(40, 26, 18, 255)), (470, 1325), pop(T(32), 0.15, 1.6), appear=T(32))
    qu = Spr(lambda L: quill(L, 720, 1240, 1.2, -35), (720, 1240), lambda t: (-12*math.sin(t*4), 6*math.sin(t*8), 0, 1, 1))
    S.append(dict(name="ordre", a=27, b=34, bg=bg3(), flames=[], sprites=[nm, qu], focus=[(470, 1300), (470, 1200)],
        titles=[("UN SEUL NOM", CREAM, 84, T(29), 440), ("EUSTACHE DAUGER", RED, 92, T(32), 552)]))
    # 4 le geolier et la consigne
    def bg4():
        im = paper(185, 0.2, (50, 40, 34)); cell_walls(im, 185, True); masked_man(im, 360, 1180, 0.95, True, True); return im
    jl = Spr(lambda L: jailer(L, 790, 1700, 1.35), (790, 1300), lambda t: breathe(t, 0.006, 0.5, 2))
    S.append(dict(name="geolier", a=34, b=48, bg=bg4(), flames=[], sprites=[jl], focus=[(470, 1250), (360, 1150), (700, 1150)],
        titles=[("SON GEÔLIER : SAINT-MARS", CREAM, 76, T(34), 440), ("UNE CONSIGNE", RED, 96, T(37), 552), ("S'IL PARLE...", CREAM, 84, T(40), 440)]))
    # 5 on le tue
    def bg5():
        im = paper(186, 0.75, (30, 10, 10)); glow(im, (470, 1150), 420, (160, 20, 20), 0.35); masked_man(im, 470, 1150, 1.25, True); return im
    S.append(dict(name="tue", a=48, b=51, bg=bg5(), flames=[], sprites=[], focus=[(470, 1150)],
        titles=[("ON LE TUE.", RED, 100, T(48), 552)]))
    # 6 34 ans, de prison en prison
    maps = [Spr(lambda L, k=k: route_map(L, 470, 1340, k, 0.95), (470, 1340), lambda t: (0, 0, 0, 1, 1), appear=a_) for k, a_ in ((0, T(61)), (1, T(62)), (2, T(64)))]
    S.append(dict(name="prisons", a=51, b=65, bg=(lambda: (lambda im: (route_map(im, 470, 1340, -1, 0.95), im)[1])(paper(187, 0.5, (50, 38, 28))))(), flames=[], sprites=maps,
        focus=[(470, 1300), (470, 1200), (470, 1400)],
        titles=[("34 ANS", RED, 100, T(52), 552), ("DE PRISON EN PRISON", CREAM, 76, T(54), 440), ("PIGNEROL", RED, 100, T(61), 552),
                ("SAINTE-MARGUERITE", RED, 88, T(62), 552), ("LA BASTILLE", RED, 100, T(63), 552)]))
    # 7 visage couvert : devant la Bastille
    def bg7():
        im = paper(188, 0.5, (40, 34, 40)); bastille(im, 470, 1500, 0.9)
        d = ImageDraw.Draw(im); d.rectangle((0, 1500, W, H), fill=(30, 26, 22, 255)); return im
    mm = Spr(lambda L: masked_man(L, 470, 1300, 0.7, True), (470, 1500), lambda t: (0, 4*math.sin(t*5), 0, 1, 1))
    S.append(dict(name="visage", a=65, b=80, bg=bg7(), flames=[], sprites=[mm], focus=[(470, 1300), (470, 1200)],
        titles=[("EN VOYAGE · À LA MESSE", CREAM, 76, T(65), 440), ("UN MASQUE DE VELOURS", RED, 88, T(77), 552)]))
    # 8 la mort, le faux nom
    def bg8():
        im = paper(189, 0.7, (24, 24, 34)); glow(im, (470, 1250), 380, (180, 180, 200), 0.2); crosses(im, 1620, 3)
        d = ImageDraw.Draw(im); d.rectangle((0, 1620, W, H), fill=(22, 18, 16, 255)); grave_name(im, 470, 1330, 0.85); return im
    S.append(dict(name="mort", a=80, b=91, bg=bg8(), flames=[], sprites=[], focus=[(470, 1300), (470, 1200)],
        titles=[("IL MEURT EN 1703", CREAM, 84, T(80), 440), ("SOUS UN FAUX NOM", RED, 92, T(84), 552), ("MARCHIOLY", RED, 100, T(90), 552)]))
    # 9 Voltaire : un demi-frere de Louis XIV ?
    def bg9():
        im = paper(190, 0.4, (60, 40, 24)); glow(im, (470, 1250), 380, (230, 180, 90), 0.25); throne_king(im, 470, 1150, 0.95); return im
    q9 = Spr(lambda L: question_mark(L, 820, 1100, 380, 200), (820, 1100), pop(T(99), 0.15, 1.8), appear=T(99))
    S.append(dict(name="voltaire", a=91, b=104, bg=bg9(), flames=[], sprites=[q9], focus=[(470, 1200), (470, 1100)],
        titles=[("VOLTAIRE", CREAM, 96, T(91), 440), ("UN FRÈRE DE LOUIS XIV ?", RED, 84, T(94), 552), ("JAMAIS PROUVÉ", RED, 100, T(99), 552)]))
    # 10 question
    S.append(dict(name="question", a=104, b=111, bg=cell_man(191), flames=[], sprites=[], focus=[(470, 1150), (470, 1100)],
        titles=[("ET TOI ?", CREAM, 96, T(104), 440), ("IL ÉTAIT QUI ?", RED, 100, T(107), 552)]))
    # 11 boucle
    S.append(dict(name="boucle", a=111, b=len(WORDS), bg=hook_bg, flames=[], sprites=[], focus=[(470, 1150), (470, 1100)],
        titles=[("34 ANS DE PRISON", CREAM, 84, T(111), 440), ("S'IL PARLAIT...", RED, 100, T(111), 552)]))
    G["IMPACTS"] = [(4, 10, None), (8, 18, (200, 30, 30)), (12, 14, None), (23, 12, None), (32, 14, None), (39, 10, None), (48, 24, (200, 30, 30)),
        (52, 14, None), (61, 10, None), (62, 10, None), (64, 12, None), (77, 12, None), (83, 12, None), (90, 18, (200, 30, 30)), (99, 14, None)]
    return S
IMPACTS = []

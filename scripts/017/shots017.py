# Plans de la video 017 (pierres de la faim). Indices = numeros de mots de words2.json.
def shot_defs():
    S = []
    G = globals()
    def stone_scene(seed, water, dates=(), cracked=False, dusk=False, insc=True):
        im = paper(seed, 0.25, (60, 44, 30)); sky_river(im, 0.0, cracked, seed, dusk)
        if water is None: water_top = H
        else: water_top = water
        if cracked:
            d = ImageDraw.Draw(im); d.rectangle((0, 1220, W, H), fill=(128, 100, 66, 255)); sky_river_cracks(im, seed)
        hunger_stone(im, 470, 1310, 1.0, insc, dates)
        if water is not None: water_over(im, water_top, seed)
        return im
    def sky_river_cracks(im, seed):
        d = ImageDraw.Draw(im); rnd = random.Random(seed)
        for _ in range(160):
            x = rnd.randint(0, W); y = rnd.randint(1240, H)
            for _ in range(3):
                x2 = x + rnd.randint(-70, 70); y2 = y + rnd.randint(-30, 30)
                d.line((x, y, x2, y2), fill=(70, 50, 30, 255), width=3); x, y = x2, y2
    DATES = [("1616", -250, 5, (232, 222, 200)), ("1707", 10, 5, (232, 222, 200)), ("1893", -120, 75, (232, 222, 200))]
    # 0 hook : la pierre hors de l'eau, inscription lisible, texte du hook des la 1re image
    hook_bg = stone_scene(171, 1440)
    S.append(dict(name="hook", a=0, b=10, bg=hook_bg, flames=[], sprites=[], focus=[(470, 1200), (470, 1150), (470, 1250)],
        titles=[("« SI TU ME VOIS, »", CREAM, 84, -0.3, 440), ("PLEURE.", RED, 100, T(4), 552), ("GRAVÉ DANS LA PIERRE", CREAM, 76, T(5), 440)]))
    # 1 promesse : l'eau baisse, la pierre sort
    bg1 = stone_scene(172, None)
    a1, b1 = T(10), T(20)
    def water_drop(world, t, fr):
        p = min(1, max(0, (t - a1)/(b1 - a1))); water_over(world, int(1230 + 230*ease(p)), 172)
    S.append(dict(name="promesse", a=10, b=20, bg=bg1, flames=[], sprites=[], dyn=[water_drop], focus=[(470, 1250), (470, 1200)],
        titles=[("LE PIRE ?", CREAM, 84, T(10), 440), ("ELLE RESSORT ENCORE", RED, 92, T(15), 552)]))
    # 2 Elbe : ville et fleuve plein, pierre invisible sous l'eau
    def bg2():
        im = paper(173, 0.2, (60, 44, 30)); sky_river(im, 0.0, False, 173, dusk=True); small_town(im, 1185, 7)
        d = ImageDraw.Draw(im); d.rectangle((0, 1180, W, H), fill=(54, 76, 92, 255))
        hunger_stone(im, 470, 1420, 0.85, False); water_over(im, 1190, 173)
        glow(im, (470, 1420), 260, (20, 30, 40), 0.3); return im
    S.append(dict(name="elbe", a=20, b=28, bg=bg2(), flames=[], sprites=[], focus=[(470, 1250), (300, 1150), (650, 1200)],
        titles=[("AU FOND DE L'ELBE", CREAM, 84, T(20), 440), ("TCHÉQUIE", RED, 100, T(26), 552)]))
    # 3 a sec : lit craquele, pierre entiere
    S.append(dict(name="sec", a=28, b=41, bg=stone_scene(174, None, cracked=True), flames=[], sprites=[], focus=[(470, 1250), (470, 1150), (300, 1400)],
        titles=[("AUTREFOIS", CREAM, 84, T(28), 440), ("SEULEMENT À SEC", RED, 96, T(36), 552)]))
    # 4 gravure : burin + marteau, l'annee apparait
    bg4 = stone_scene(175, 1460)
    hm = Spr(lambda L: hammer(L, 820, 1060, 1.0, 30), (820, 1060), lambda t: (0, 0, 22*abs(math.sin(t*9)), 1, 1))
    ch = Spr(lambda L: chisel(L, 700, 1150, 1.0, -35), (700, 1150), lambda t: (3*math.sin(t*18), 2*math.sin(t*18), 0, 1, 1))
    yr = Spr(lambda L: hunger_stone_dates(L, [("1616", -250, 5, (232, 222, 200))]), (470, 1310), pop(T(47), 0.15, 1.6), appear=T(47))
    ini = Spr(lambda L: hunger_stone_dates(L, [("H.W.", 20, 5, (232, 222, 200))]), (470, 1310), pop(T(51), 0.15, 1.6), appear=T(51))
    S.append(dict(name="gravure", a=41, b=52, bg=bg4, flames=[], sprites=[yr, ini, ch, hm], focus=[(470, 1250), (560, 1200)],
        titles=[("À CHAQUE FOIS", CREAM, 84, T(41), 440), ("ON GRAVAIT L'ANNÉE", RED, 92, T(45), 552), ("ET SES INITIALES", CREAM, 84, T(49), 440)]))
    # 5 recoltes perdues : champ mort sous le soleil
    def bg5():
        im = paper(176, 0.1, (90, 60, 30)); d = ImageDraw.Draw(im)
        for y in range(0, 1500, 6):
            k = y/1500; d.rectangle((0, y, W, y + 6), fill=(int(200 - 40*k), int(120 - 30*k), int(60 - 20*k), 255))
        scorch_sun(im, 680, 1080, 130); dead_field(im, 1420, 176); return im
    S.append(dict(name="champ", a=52, b=62, bg=bg5(), flames=[], sprites=[], focus=[(470, 1300), (680, 1150), (300, 1450)],
        titles=[("UN FLEUVE À SEC", CREAM, 84, T(52), 440), ("RÉCOLTES PERDUES", RED, 96, T(60), 552)]))
    # 6 prix et faim : balance, pieces qui tombent, silhouette
    def bg6():
        im = paper(177, 0.15, (90, 62, 38)); glow(im, (470, 1250), 420, (230, 170, 90), 0.35); bread_scale(im, 470, 1250, 1.0); return im
    coins = [Spr(lambda L, k=k: coin(L, 190 + 12*k, 1140 - 26*k, 54), (190, 1140 - 26*k), lambda t, k=k: (0, -260*max(0, 1 - (t - T(62) - k*0.08)/0.3), 0, 1, 1), appear=T(62) + k*0.08) for k in range(5)]
    hu = Spr(lambda L: hungry(L, 470, 1660, 1.3, (20, 14, 12)), (470, 1500), lambda t: breathe(t, 0.006, 0.4, 2), appear=T(65))
    S.append(dict(name="prix", a=62, b=68, bg=bg6(), flames=[], sprites=coins + [hu], focus=[(470, 1250), (300, 1200)],
        titles=[("LES PRIX FLAMBENT", RED, 92, T(62), 552), ("ET LA FAIM", RED, 100, T(65), 552)]))
    # 7 nom
    S.append(dict(name="nom", a=68, b=76, bg=stone_scene(178, 1460, dusk=True), flames=[], sprites=[], focus=[(470, 1200), (470, 1300)],
        titles=[("ON LES APPELLE", CREAM, 84, T(68), 440), ("LES PIERRES DE LA FAIM", RED, 88, T(71), 552)]))
    # 8 dates
    ds = [Spr(lambda L, dd=dd: hunger_stone_dates(L, [dd]), (470, 1310), pop(T(78 + k), 0.15, 1.7), appear=T(78 + k)) for k, dd in enumerate(DATES)]
    S.append(dict(name="dates", a=76, b=81, bg=stone_scene(179, 1460, insc=False), flames=[], sprites=ds, focus=[(470, 1250), (470, 1200)],
        titles=[("SUR CELLE-CI", CREAM, 84, T(76), 440), ("1616", RED, 100, T(78), 552), ("1707", RED, 100, T(79), 552), ("1893", RED, 100, T(80), 552)]))
    # 9 retour : 2018, 2022
    bg9 = stone_scene(180, 1460, dates=DATES, insc=False)
    st18 = Spr(lambda L: stamp_red(L, "2018", 300, 1530, 90, -8), (300, 1530), pop(T(83), 0.12, 2.2), appear=T(83))
    st22 = Spr(lambda L: stamp_red(L, "2022", 640, 1540, 90, 6), (640, 1540), pop(T(86), 0.12, 2.2), appear=T(86))
    S.append(dict(name="retour", a=81, b=91, bg=bg9, flames=[], sprites=[st18, st22], focus=[(470, 1250), (470, 1350)],
        titles=[("2018", RED, 100, T(83), 552), ("2022", RED, 100, T(86), 552), ("ELLE EST RESSORTIE", CREAM, 80, T(87), 440)]))
    # 10 question
    q10 = Spr(lambda L: chisel(L, 760, 1120, 1.1, -30), (760, 1120), lambda t: breathe(t, 0.01, 2, 4))
    S.append(dict(name="question", a=91, b=97, bg=stone_scene(181, 1460, dates=DATES, insc=False), flames=[], sprites=[q10], focus=[(470, 1250), (470, 1200)],
        titles=[("ET TOI ?", CREAM, 96, T(91), 440), ("TU GRAVERAIS QUOI ?", RED, 92, T(94), 552)]))
    # 11 boucle sur la premiere image
    S.append(dict(name="boucle", a=97, b=len(WORDS), bg=hook_bg, flames=[], sprites=[], focus=[(470, 1200), (470, 1250)],
        titles=[("« SI TU ME VOIS, »", CREAM, 84, T(97), 440), ("PLEURE.", RED, 100, T(97), 552)]))
    G["IMPACTS"] = [(4, 18, (200, 30, 30)), (9, 10, None), (15, 12, None), (47, 12, None), (60, 12, None), (62, 10, None), (67, 22, (200, 30, 30)),
        (72, 14, None), (78, 12, None), (79, 12, None), (80, 12, None), (83, 16, (200, 30, 30)), (86, 18, (200, 30, 30)), (90, 14, None)]
    return S

def hunger_stone_dates(L, dates):
    """Ne dessine que les dates gravees, a la position de la pierre (470, 1310)."""
    d = ImageDraw.Draw(L); fd = fserif(46); cx, cy = 470, 1310
    for (txt, x, y, col) in dates:
        d.text((cx + x + 2, cy + y + 3), txt, font=fd, fill=(40, 34, 30, 255)); d.text((cx + x, cy + y), txt, font=fd, fill=col + (255,))
IMPACTS = []
def small_town(im, base, seed=7):
    d = ImageDraw.Draw(im); rnd = random.Random(seed); x = 20
    while x < W - 20:
        w = rnd.randint(50, 90); h = rnd.randint(70, 150)
        d.rectangle((x, base - h, x + w, base), fill=(28, 22, 20, 255))
        d.polygon([(x - 6, base - h), (x + w/2, base - h - rnd.randint(30, 60)), (x + w + 6, base - h)], fill=(40, 26, 22, 255))
        for _ in range(2):
            wx = x + rnd.randint(10, w - 20); wy = base - rnd.randint(25, h - 20); d.rectangle((wx, wy, wx + 10, wy + 14), fill=(250, 200, 110, 255))
        x += w + rnd.randint(4, 20)
    tx = 760; d.rectangle((tx, base - 260, tx + 50, base), fill=(28, 22, 20, 255)); d.polygon([(tx - 10, base - 260), (tx + 25, base - 340), (tx + 60, base - 260)], fill=(40, 26, 22, 255))

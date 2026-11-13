# Plans de la video 019 (Boycott). Indices = numeros de mots de words2.json.
def shot_defs():
    S = []; G = globals()
    def field_bg(seed, dark=0.3, base=1300):
        im = paper(seed, dark*0.5, (74, 54, 34)); glow(im, (600, 1250), 560, (250, 200, 110), 0.5); wheat_field(im, base, seed); return im
    # 0 hook : soldats autour d'un champ
    def bg0():
        im = field_bg(191, 0.25, 1250)
        for k, x in enumerate((120, 300, 640, 820, 980)): rifle_soldier(im, x, 1500 + (k % 2)*40, 1.5)
        return im
    S.append(dict(name="hook", a=0, b=8, bg=bg0(), flames=[], sprites=[], focus=[(470, 1250), (470, 1200), (470, 1300)],
        titles=[("DES CENTAINES DE SOLDATS", CREAM, 76, T(0), 440), ("POUR UNE SEULE RÉCOLTE", RED, 84, T(4), 552)]))
    # 1 un seul homme, personne ne lui parle
    def bg1():
        im = field_bg(192, 0.35, 1350); crowd(im, 1560, (110, 250, 700, 850, 990), s=1.7); return im
    man = Spr(lambda L: boycott_man(L, 470, 1640, 2.0), (470, 1450), lambda t: breathe(t, 0.01, 0.6, 2))
    S.append(dict(name="seul", a=8, b=17, bg=bg1(), flames=[], sprites=[man], focus=[(470, 1300), (470, 1200)],
        titles=[("UN SEUL HOMME", CREAM, 84, T(8), 440), ("PERSONNE NE LUI PARLE", RED, 84, T(11), 552)]))
    # 2 le nom devenu un mot
    def bg2():
        im = paper(193, 0.45, (54, 38, 26)); word_page(im, 470, 1320, "BOYCOTT", 640, 440, -3, 110); return im
    s2 = Spr(lambda L: stamp_red(L, "UN MOT", 470, 1580, 100, -6), (470, 1580), pop(T(22), 0.12, 2.4), appear=T(22))
    S.append(dict(name="mot", a=17, b=24, bg=bg2(), flames=[], sprites=[s2], focus=[(470, 1320), (470, 1250)],
        titles=[("SON NOM", CREAM, 84, T(17), 440), ("EST DEVENU UN MOT", RED, 88, T(20), 552)]))
    # 3 qui est-il
    def bg3():
        im = paper(194, 0.12, (74, 58, 60)); glow(im, (470, 1250), 560, (244, 196, 124), 0.6); houses(im, 1600, 4, True)
        d = ImageDraw.Draw(im); d.rectangle((0, 1600, W, H), fill=(26, 22, 18, 255)); return im
    m3 = Spr(lambda L: boycott_man(L, 470, 1680, 2.1), (470, 1450), lambda t: breathe(t, 0.01, 0.6, 2))
    S.append(dict(name="homme", a=24, b=38, bg=bg3(), flames=[], sprites=[m3], focus=[(470, 1300), (470, 1200)],
        titles=[("CHARLES BOYCOTT", RED, 92, T(26), 552), ("RÉGISSEUR EN IRLANDE", CREAM, 76, T(28), 440)]))
    # 4 loyers
    def bg4():
        im = paper(195, 0.12, (74, 58, 44)); glow(im, (470, 1300), 560, (244, 196, 124), 0.6); paper_sheet(im, 760, 1300, 420, 560, 4, 0.0, 6); crowd(im, 1620, (130, 280, 430), col=(30, 22, 18), s=1.8); return im
    S.append(dict(name="loyers", a=38, b=52, bg=bg4(), flames=[], sprites=[], focus=[(470, 1300), (300, 1250), (700, 1250)],
        titles=[("SEPTEMBRE 1880", CREAM, 84, T(38), 440), ("LES LOYERS ÉTRANGLENT", RED, 80, T(42), 552), ("BAISSER LE PRIX", CREAM, 80, T(47), 440)]))
    # 5 il refuse, menace
    def bg5():
        im = paper(196, 0.12, (74, 52, 44)); glow(im, (470, 1350), 560, (244, 196, 124), 0.6); crowd(im, 1650, (120, 260, 400), col=(24, 18, 16), s=1.8); d = ImageDraw.Draw(im); return im
    pt = Spr(lambda L: pointing(L, 700, 1660, 2.2, col=(30, 24, 36), dirx=-1), (700, 1450), lambda t: breathe(t, 0.008, 0.5, 2))
    S.append(dict(name="refuse", a=52, b=59, bg=bg5(), flames=[], sprites=[pt], focus=[(470, 1300), (600, 1250)],
        titles=[("IL REFUSE", RED, 100, T(52), 552), ("IL MENACE D'EXPULSER", CREAM, 76, T(54), 440)]))
    # 6 l'ignorer
    def bg6():
        im = field_bg(197, 0.45, 1400); crowd(im, 1600, (90, 210, 330, 610, 740, 880, 1000), col=(12, 8, 10), s=1.8); return im
    m6 = Spr(lambda L: boycott_man(L, 470, 1650, 1.7), (470, 1450), lambda t: breathe(t, 0.008, 0.5, 2))
    S.append(dict(name="ignorer", a=59, b=71, bg=bg6(), flames=[], sprites=[m6], focus=[(470, 1300), (470, 1200)],
        titles=[("UNE AUTRE ARME", CREAM, 84, T(59), 440), ("NE PAS LE FRAPPER", RED, 88, T(65), 552), ("JUSTE L'IGNORER", RED, 92, T(69), 552)]))
    # 7 totalement : plus d'ouvriers, de courses, de courrier
    def bg7():
        im = field_bg(198, 0.5, 1450); return im
    w7 = Spr(lambda L: figure(L, 220, 1620, 1.9, col=(12, 8, 10), hat=True), (220, 1450), lambda t: (-40*t, 0, 0, 1, 1), appear=T(72))
    d7 = Spr(lambda L: door(L, 560, 1330, 0.6, False), (560, 1330), pop(T(74), 0.15, 1.4), appear=T(74))
    e7 = Spr(lambda L: envelope(L, 830, 1500, 0.9), (830, 1500), lambda t: (0, 6*math.sin(t*4), -8, 1, 1), appear=T(77))
    S.append(dict(name="plus", a=71, b=80, bg=bg7(), flames=[], sprites=[w7, d7, e7], focus=[(470, 1350), (470, 1250), (560, 1350)],
        titles=[("TOTALEMENT", CREAM, 88, T(71), 440), ("PLUS D'OUVRIERS", RED, 88, T(72), 552), ("PLUS DE COURSES", RED, 88, T(74), 552), ("PLUS DE COURRIER", RED, 88, T(77), 552)]))
    # 8 le gouvernement envoie des soldats
    def bg8():
        im = field_bg(199, 0.3, 1300)
        for k, x in enumerate((90, 230, 370, 710, 850, 990)): rifle_soldier(im, x, 1560 + (k % 2)*40, 1.6)
        for x in (500, 590): worker(im, x, 1640, 1.6, lamp=False)
        return im
    S.append(dict(name="soldats", a=80, b=89, bg=bg8(), flames=[], sprites=[], focus=[(470, 1350), (300, 1300), (700, 1300)],
        titles=[("LE GOUVERNEMENT ENVOIE", CREAM, 72, T(80), 440), ("DES SOLDATS", RED, 100, T(86), 552)]))
    # 9 il part
    def bg9():
        im = paper(200, 0.5, (30, 38, 52)); glow(im, (800, 1050), 240, (230, 220, 200), 0.3); return im
    sh = Spr(lambda L: ship(L, 470, 1560, 1.4), (470, 1560), lambda t: (0, 10*math.sin(t*2), 2*math.sin(t*1.4), 1, 1))
    S.append(dict(name="depart", a=89, b=95, bg=bg9(), flames=[], sprites=[sh], focus=[(470, 1300), (470, 1250)],
        titles=[("1ER DÉCEMBRE", CREAM, 84, T(89), 440), ("IL QUITTE L'IRLANDE", RED, 88, T(92), 552)]))
    # 10 la presse : le mot est deja un verbe
    def bg10():
        im = paper(201, 0.45, (54, 40, 26)); word_page(im, 470, 1330, "BOYCOTT", 700, 520, 2, 120); return im
    S.append(dict(name="presse", a=95, b=108, bg=bg10(), flames=[], sprites=[], focus=[(470, 1330), (470, 1250)],
        titles=[("DÈS NOVEMBRE", CREAM, 84, T(95), 440), ("DÉJÀ UN VERBE", RED, 100, T(103), 552)]))
    # 11 aujourd'hui
    def bg11():
        im = paper(202, 0.4, (60, 42, 24)); glow(im, (470, 1250), 380, (230, 180, 90), 0.25); d = ImageDraw.Draw(im); d.rectangle((250, 1050, 690, 1620), fill=(96, 22, 28, 255), outline=INK + (255,), width=6); d.rectangle((280, 1080, 660, 1590), outline=(206, 164, 54, 255), width=4)
        f = fserif(64); d.text((470 - f.getlength("BOYCOTT")/2, 1290), "BOYCOTT", font=f, fill=(206, 164, 54, 255)); d.line((330, 1400, 610, 1400), fill=(206, 164, 54, 255), width=4); return im
    S.append(dict(name="aujourdhui", a=108, b=115, bg=bg11(), flames=[], sprites=[], focus=[(470, 1330), (470, 1250)],
        titles=[("AUJOURD'HUI", CREAM, 88, T(108), 440), ("TU LE DIS SANS LE SAVOIR", RED, 76, T(111), 552)]))
    # 12 question
    S.append(dict(name="question", a=115, b=128, bg=field_bg(203, 0.4, 1400), flames=[], sprites=[Spr(lambda L: boycott_man(L, 470, 1660, 1.8), (470, 1450), lambda t: breathe(t, 0.008, 0.5, 2))], focus=[(470, 1300), (470, 1200)],
        titles=[("ET TOI ?", CREAM, 96, T(115), 440), ("IGNORER OU PARLER ?", RED, 90, T(120), 552)]))
    # 13 boucle
    S.append(dict(name="boucle", a=128, b=len(WORDS), bg=bg0(), flames=[], sprites=[], focus=[(470, 1250), (470, 1200)],
        titles=[("DES CENTAINES DE SOLDATS", CREAM, 76, T(128), 440), ("POUR UNE SEULE RÉCOLTE", RED, 84, T(128), 552)]))
    DY = -250
    for sh in S:
        b = sh["bg"]; n = Image.new("RGBA", b.size); n.paste(b, (0, DY)); n.paste(b.crop((0, H - 40, W, H)).resize((W, -DY)), (0, H + DY)); sh["bg"] = n
        for sp in sh["sprites"]: sp.pivot = (sp.pivot[0], sp.pivot[1] + DY)
    G["IMPACTS"] = [(3, 10, None), (7, 18, (200, 30, 30)), (23, 18, (200, 30, 30)), (27, 12, None), (53, 14, None), (71, 14, None), (73, 10, None),
        (76, 10, None), (79, 12, None), (88, 18, (200, 30, 30)), (94, 12, None), (107, 18, (200, 30, 30)), (127, 12, None)]
    return S
IMPACTS = []

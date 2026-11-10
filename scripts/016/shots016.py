# Plans de la video 016 (sommeil en deux temps). Indices de mots trouves par recherche dans la transcription.
import unicodedata, re
def _n(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9'-]", "", s)
def I(word, after=0):
    w = _n(word)
    for k in range(after, len(WORDS)):
        if _n(WORDS[k]["text"]).startswith(w): return k
    raise KeyError(word)

def shot_defs():
    S = []
    i_et = I("et", 5); i_jus = I("jusqu", i_et); i_on = I("couchait", i_jus) - 1; i_vers = I("vers", i_on); i_puis = I("puis", i_vers)
    i_ind = I("l'indice", i_puis); i_fil = I("fillette", i_ind) - 1; i_prem = I("premier", I("morte", i_fil)); i_il = I("trouvera", i_prem) - 1
    i_cette = I("cette", i_il); i_med = I("medecin", i_cette) - 1; i_dau = I("d'autres", i_med) - 1; i_lum = I("lumiere", i_dau) - 2
    i_ann = I("annees", i_lum) - 2; i_alors = I("alors", i_ann); i_q = I("toi", i_alors) - 1; i_abo = I("n'hesite", i_q)
    G = globals(); G["IDX"] = dict(q=i_q, abo=i_abo, hook_end=i_et)
    def bg_room(seed=160, dawn=False):
        im = paper(seed, 0.7, (26, 24, 40)); moon_window(im, 800, 1000, 0.8, dawn); return im
    def bg_hook():
        im = bg_room(160); glow(im, (470, 1250), 360, (255, 190, 110), 0.35); veilleuse(im, 380, 1180, 1.0); return im
    cflame = [Flame(380 + 300, 1180 + 40 - 10, 90, 46)]
    S.append(dict(name="hook", a=0, b=i_et, bg=bg_hook(), flames=cflame, sprites=[], focus=[(560, 1250), (470, 1250), (620, 1200)],
        titles=[("3 H DU MATIN ?", CREAM, 84, 0.0, 440), ("PAS DE L'INSOMNIE", RED, 96, T(I("l'insomnie")), 552), ("UN RÉFLEXE DE 1 000 ANS", RED, 84, T(I("reflexe")), 552)]))
    def bg1():
        im = paper(161, 0.6, (40, 30, 28)); paper_sheet(im, 470, 1400, 520, 600, -3, 0.0, 2); question_mark(im, 470, 1350, 600, 50); return im
    q1 = Spr(lambda L: stamp_red(L, "MEURTRE", 470, 1480, 110, -8), (470, 1480), pop(T(I("meurtre", i_et)), 0.12, 2.6), appear=T(I("meurtre", i_et)))
    S.append(dict(name="annonce", a=i_et, b=i_jus, bg=bg1(), flames=[], sprites=[q1], focus=[(470, 1250), (470, 1150)],
        titles=[("CE QU'ILS FAISAIENT", CREAM, 76, T(i_et), 440), ("UNE AFFAIRE DE MEURTRE", RED, 84, T(I("affaire", i_et)), 552)]))
    def bg2():
        im = paper(162, 0.65, (24, 26, 48)); glow(im, (800, 950), 200, (230, 230, 200), 0.4)
        d = ImageDraw.Draw(im); d.ellipse((760, 910, 840, 990), fill=(236, 230, 200, 255)); houses(im, 1600, 9, True)
        d = ImageDraw.Draw(im); d.rectangle((0, 1600, W, H), fill=(20, 16, 14, 255)); return im
    S.append(dict(name="village", a=i_jus, b=i_on, bg=bg2(), flames=[], sprites=[], focus=[(470, 1350), (300, 1400), (650, 1400)],
        titles=[("JUSQU'AU XIXe SIÈCLE", CREAM, 76, T(i_jus), 440), ("PAS D'UNE TRAITE", RED, 96, T(I("traite", i_jus)), 552)]))
    def bg3():
        im = bg_room(163); sleeper(im, 470, 1350, 1.05); timeline(im, 470, 1700, 0, 0.95); return im
    z3 = Spr(lambda L: zzz(L, 300, 1150, 1.0), (360, 1100), lambda t: (0, -10*math.sin(t*2), 0, 1, 0.6 + 0.4*abs(math.sin(t*1.5))))
    S.append(dict(name="premier", a=i_on, b=i_vers, bg=bg3(), flames=[], sprites=[z3], focus=[(470, 1300), (330, 1250), (470, 1400)],
        titles=[("À LA TOMBÉE DE LA NUIT", CREAM, 70, T(i_on), 440), ("LE PREMIER SOMME", RED, 96, T(I("somme", i_on)), 552)]))
    def bg4():
        im = bg_room(164); sleeper(im, 470, 1350, 1.05, awake=True); timeline(im, 470, 1700, 1, 0.95); return im
    ck = Spr(lambda L: (clock(L, 830, 1070, 110, 0), hands(L, 830, 1070, 110, 0)), (830, 1070), pop(T(i_vers), 0.15, 1.8), appear=T(i_vers))
    S.append(dict(name="minuit", a=i_vers, b=i_puis, bg=bg4(), flames=[], sprites=[ck], focus=[(400, 1250), (470, 1300), (330, 1200)],
        titles=[("MINUIT", CREAM, 96, T(i_vers), 440), ("ON SE RÉVEILLE", RED, 96, T(I("reveillait", i_vers)), 552), ("UNE HEURE, PARFOIS PLUS", CREAM, 70, T(I("pendant", i_vers)), 440)]))
    def bg5():
        im = bg_room(165, dawn=True); sleeper(im, 470, 1350, 1.05); timeline(im, 470, 1700, 2, 0.95); return im
    S.append(dict(name="second", a=i_puis, b=i_ind, bg=bg5(), flames=[], sprites=[z3], focus=[(470, 1300), (330, 1250), (470, 1400)],
        titles=[("JUSQU'À L'AUBE", CREAM, 84, T(i_puis), 440), ("LE SECOND SOMMEIL", RED, 90, T(I("second", i_puis)), 552)]))
    def bg6():
        im = paper(166, 0.5, (50, 40, 30)); paper_sheet(im, 470, 1400, 600, 640, -2, 0.0, 4); candle(im, 900, 1620, 1.0, False); return im
    qu6 = Spr(lambda L: quill(L, 760, 1320, 1.2, -35), (760, 1320), lambda t: (-14*math.sin(t*4), 8*math.sin(t*8), 0, 1, 1))
    st6 = Spr(lambda L: stamp_red(L, "1697", 360, 1560, 96, -8), (360, 1560), pop(T(I("proces", i_ind)), 0.12, 2.4), appear=T(I("proces", i_ind)))
    S.append(dict(name="indice", a=i_ind, b=i_fil, bg=bg6(), flames=[Flame(900, 1612, 90, 46)], sprites=[qu6, st6], focus=[(470, 1250), (600, 1200), (470, 1350)],
        titles=[("ROGER EKIRCH, HISTORIEN", CREAM, 70, T(I("roger", i_ind)), 440), ("UN PROCÈS-VERBAL", RED, 96, T(I("proces", i_ind)), 552)]))
    def bg7():
        im = paper(167, 0.45, (40, 34, 50)); d = ImageDraw.Draw(im)
        d.rectangle((560, 1000, 900, 1560), fill=(16, 12, 10, 255), outline=INK+(255,), width=6); glow(im, (730, 1300), 200, (240, 200, 140), 0.25)
        d = ImageDraw.Draw(im); d.rectangle((0, 1560, W, H), fill=(30, 22, 18, 255)); return im
    kid = Spr(lambda L: figure(L, 330, 1640, 2.1, col=(92, 80, 120), kid=True), (330, 1500), lambda t: breathe(t, 0.01, 0.5, 2))
    men = [Spr(lambda L, x=x: figure(L, x, 1560, 1.05, col=(8, 6, 5), hat=True), (x, 1400), lambda t, x=x: (0, 0, 0, 1, 1), appear=T(I("hommes", i_fil)) + k*0.2) for k, x in enumerate((680, 790))]
    S.append(dict(name="fillette", a=i_fil, b=i_prem, bg=bg7(), flames=[], sprites=[kid] + men, focus=[(470, 1350), (300, 1400), (730, 1350)],
        titles=[("UNE FILLETTE DE 9 ANS", CREAM, 76, T(i_fil), 440), ("DES HOMMES À LA PORTE", CREAM, 76, T(I("hommes", i_fil)), 440), ("RETROUVÉE MORTE", RED, 96, T(I("morte", i_fil)), 552)]))
    def bg8():
        im = paper(168, 0.8, (30, 26, 30)); question_mark(im, 470, 1350, 620, 55); timeline(im, 470, 1650, -1, 0.95); return im
    S.append(dict(name="donc", a=i_prem, b=i_il, bg=bg8(), flames=[], sprites=[], focus=[(470, 1300), (470, 1450)],
        titles=[("« PREMIER » SOMMEIL ?", CREAM, 80, T(i_prem), 440), ("DONC UN SECOND", RED, 100, T(I("donc", i_prem)), 552)]))
    def bg9():
        im = paper(169, 0.5, (46, 36, 28))
        for k in range(7): paper_sheet(im, 180 + (k % 4)*240, 1250 + (k // 4)*330, 300, 380, -6 + k*2.5, 0.0, 10 + k)
        return im
    S.append(dict(name="mentions", a=i_il, b=i_cette, bg=bg9(), flames=[], sprites=[], focus=[(470, 1300), (330, 1250), (620, 1400)],
        count=(T(I("deux", i_il)), T(I("deux", i_il)) + 1.0, 2000),
        titles=[("PLUS DE #COUNT# MENTIONS", RED, 84, T(I("deux", i_il)), 552), ("12 LANGUES", CREAM, 96, T(I("douzaine", i_il)), 440)]))
    def bg10():
        im = paper(170, 0.6, (40, 26, 20)); hearth(im, 620, 1600, 1.0); glow(im, (230, 1450), 220, (240, 200, 140), 0.3); praying(im, 230, 1660, 1.8); return im
    S.append(dict(name="veille", a=i_cette, b=i_med, bg=bg10(), flames=[Flame(620, 1580, 170, 120)], sprites=[], focus=[(470, 1350), (620, 1400), (260, 1400)],
        titles=[("ON PRIAIT", CREAM, 96, T(I("priait", i_cette)), 440), ("LE FEU · LES REMÈDES", RED, 84, T(I("ranimait", i_cette)), 552), ("LES VOISINS", RED, 96, T(I("voisins", i_cette)), 552)]))
    def bg11():
        im = paper(171, 0.55, (44, 34, 30)); glow(im, (470, 1250), 380, (230, 200, 150), 0.2); return im
    doc = Spr(lambda L: doctor(L, 470, 1150, 0.9), (470, 1350), lambda t: breathe(t, 0.008, 0.6, 3))
    S.append(dict(name="medecin", a=i_med, b=i_dau, bg=bg11(), flames=[], sprites=[doc], focus=[(470, 1250), (470, 1150), (470, 1350)],
        titles=[("UN MÉDECIN DU XVIe", CREAM, 84, T(i_med), 440), ("POUR FAIRE DES ENFANTS", RED, 80, T(I("enfants", i_med)) - 0.6, 552)]))
    def bg12():
        im = street(172, 0.75, False, 1500, (30, 26, 36)); glow(im, (470, 1250), 380, (160, 30, 30), 0.25); return im
    th = Spr(lambda L: worker(L, 470, 1650, 1.4, True), (470, 1450), lambda t: (-120 + 70*t % 240 if False else 30*math.sin(t*1.5), 4*math.sin(t*6), 0, 1, 1))
    S.append(dict(name="cambrioler", a=i_dau, b=i_lum, bg=bg12(), flames=[], sprites=[th], focus=[(470, 1300), (470, 1400)],
        titles=[("D'AUTRES", CREAM, 96, T(i_dau), 440), ("CAMBRIOLAIENT", RED, 100, T(I("cambrioler", i_dau)), 552)]))
    def bg13():
        im = street(173, 0.6, True, 1550, (40, 34, 30))
        for x in (140, 470, 800): lamppost(im, x, 1700, 1.0, True)
        return im
    S.append(dict(name="lumiere", a=i_lum, b=i_ann, bg=bg13(), flames=[], sprites=[], focus=[(470, 1250), (140, 1200), (800, 1200)],
        titles=[("LA LUMIÈRE ARTIFICIELLE", CREAM, 70, T(i_lum), 440), ("LE SECOND DISPARAÎT", RED, 88, T(I("disparu", i_lum)) - 0.4, 552)]))
    def bg14():
        im = paper(174, 0.85, (20, 20, 30)); sleeper(im, 470, 1400, 1.0, awake=True); return im
    fl14 = Spr(lambda L: flask(L, 850, 1050, 0.6, (80, 140, 200)), (850, 1050), lambda t: breathe(t, 0.02, 1, 3))
    S.append(dict(name="experience", a=i_ann, b=i_alors, bg=bg14(), flames=[], sprites=[fl14], focus=[(470, 1300), (400, 1250), (470, 1400)],
        titles=[("ANNÉES 1990", CREAM, 96, T(i_ann), 440), ("PAS DE LUMIÈRE LE SOIR", RED, 80, T(I("prive", i_ann)), 552), ("RÉVEIL EN PLEINE NUIT", RED, 80, T(I("reveillaient", i_ann)), 552)]))
    def bg15():
        im = bg_room(175); glow(im, (470, 1250), 300, (255, 190, 110), 0.25); return im
    ck15 = Spr(lambda L: (clock(L, 470, 1300, 220, 180), hands(L, 470, 1300, 220, 180)), (470, 1300), lambda t: breathe(t, 0.01, 0.3, 2))
    S.append(dict(name="souvenir", a=i_alors, b=i_q, bg=bg15(), flames=[], sprites=[ck15], focus=[(470, 1250), (470, 1350)],
        titles=[("TON RÉVEIL DE 3 H ?", CREAM, 84, T(i_alors), 440), ("UN VIEUX SOUVENIR", RED, 96, T(I("souvenir", i_alors)) - 0.5, 552)]))
    S.append(dict(name="question", a=i_q, b=i_abo, bg=bg_hook(), flames=cflame, sprites=[], focus=[(560, 1250), (470, 1250)],
        titles=[("ET TOI ?", CREAM, 96, T(i_q), 440), ("TU EN FERAIS QUOI ?", RED, 96, T(I("ferais", i_q)) - 0.3, 552)]))
    S.append(dict(name="boucle", a=i_abo, b=len(WORDS), bg=bg_hook(), flames=cflame, sprites=[], focus=[(560, 1250), (470, 1250)],
        titles=[("3 H DU MATIN ?", CREAM, 84, T(i_abo), 440), ("PAS DE L'INSOMNIE", RED, 96, T(i_abo), 552)]))
    G["IMPACTS"] = [(I("l'insomnie"), 12, None), (I("mille"), 16, (200, 30, 30)), (I("meurtre", i_et), 20, (200, 30, 30)), (I("traite", i_jus), 10, None), (i_vers, 12, None),
        (I("proces", i_ind), 14, None), (I("morte", i_fil), 22, (200, 30, 30)), (I("donc", i_prem), 14, None), (I("cambrioler", i_dau), 18, (200, 30, 30)),
        (I("disparu", i_lum), 16, None), (I("reveillaient", i_ann), 12, None), (I("souvenir", i_alors), 12, None)]
    return S
IMPACTS = []

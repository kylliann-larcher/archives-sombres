# Dessins propres a la video 019 (Boycott). Reutilise gen018 -> gen017 -> ... -> gen010.
exec(open(f"{HERE}/gen018.py", encoding="utf-8").read())

def wheat_field(im, base=1300, seed=7, gold=(214, 172, 72), density=330):
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    d.rectangle((0, base, W, H), fill=(112, 86, 46, 255))
    for _ in range(density):
        x = rnd.randint(-20, W + 20); y = rnd.randint(base + 5, H - 60); hg = rnd.randint(120, 230)
        sway = rnd.randint(-22, 22); c = tuple(max(0, v + rnd.randint(-22, 22)) for v in gold)
        d.line((x, y, x + sway, y - hg), fill=c + (255,), width=4)
        for k in range(5):
            yy = y - hg + k*14; d.ellipse((x + sway - 7, yy - 12, x + sway + 7, yy + 6), fill=c + (255,))
    hatch(d, (0, base, W, H), 16, 0.2, (20, 12, 6, 70), 3)

def boycott_man(im, x, y, s=1.0):
    figure(im, x, y, s, col=(34, 28, 40))
    d = ImageDraw.Draw(im)
    d.rectangle((x-30*s, y-262*s, x+30*s, y-248*s), fill=(20, 16, 24, 255)); d.rectangle((x-22*s, y-318*s, x+22*s, y-258*s), fill=(20, 16, 24, 255))

def rifle_soldier(im, x, y, s=1.0):
    figure(im, x, y, s, col=(10, 6, 6), hat=True)
    d = ImageDraw.Draw(im); d.line((x+46*s, y-30*s, x+54*s, y-330*s), fill=(60, 46, 36, 255), width=int(8*s))
    d.polygon([(x+50*s, y-330*s), (x+58*s, y-330*s), (x+54*s, y-360*s)], fill=(200, 200, 205, 255))
    d.rectangle((x-48*s, y-130*s, x+48*s, y-112*s), fill=(150, 20, 24, 255))

def ship(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    for mx in (-110, 40, 170):
        d.line((cx+mx*s, cy-20*s, cx+mx*s, cy-420*s), fill=(40, 28, 20, 255), width=int(9*s))
    for mx, hh in ((-110, 300), (40, 360), (170, 240)):
        d.polygon([(cx+(mx-80)*s, cy-60*s), (cx+(mx+80)*s, cy-60*s), (cx+(mx+60)*s, cy-(hh+40)*s), (cx+(mx-60)*s, cy-(hh+40)*s)], fill=(214, 200, 168, 255), outline=INK+(255,), width=3)
    d.polygon([(cx-290*s, cy-30*s), (cx+300*s, cy-30*s), (cx+220*s, cy+80*s), (cx-210*s, cy+80*s)], fill=(24, 16, 12, 255), outline=INK+(255,), width=4)
    for k in range(7):
        yy = cy + 90*s + k*34
        d.arc((cx-420 + k*20, yy - 24, cx+420 - k*20, yy + 30), 0, 180, fill=(120, 140, 160, 255), width=4)

def envelope(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-170*s, cy-110*s, cx+170*s, cy+110*s), fill=(224, 208, 168, 255), outline=INK+(255,), width=4)
    d.line((cx-170*s, cy-110*s, cx, cy+10*s), fill=INK+(255,), width=4); d.line((cx+170*s, cy-110*s, cx, cy+10*s), fill=INK+(255,), width=4)

def word_page(im, cx, cy, word, w=620, h=420, ang=-3, size=96):
    paper_sheet(im, cx, cy, w, h, ang, 0.0, 4)
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t); f = fserif(size)
    sz = size
    while f.getlength(word) > w - 80 and sz > 30: sz -= 4; f = fserif(sz)
    d.rectangle((30, h//2 - sz//2 - 10, w - 30, h//2 + sz//2 + 24), fill=(222, 204, 160, 255))
    d.text((w/2 - f.getlength(word)/2, h/2 - sz/2), word, font=f, fill=(40, 20, 14, 255))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(t, (int(cx - t.width/2), int(cy - t.height/2)))

def crowd(im, y, xs, col=(14, 10, 12), s=1.7):
    for k, x in enumerate(xs): figure(im, x, y, s*(0.95 + 0.1*((k*7) % 3)/2), col=col)

# Dessins propres a la video 015 (danse de 1518). Reutilise gen014 (dont gen008/gen010).
exec(open(f"{HERE}/gen014.py", encoding="utf-8").read())

def dancer(im, cx, cy, s=1.0, dress=(150, 40, 40), arms=1.0, mood=1):
    d = ImageDraw.Draw(im)
    # robe
    d.polygon([(cx-260*s, cy+520*s), (cx-70*s, cy+140*s), (cx+70*s, cy+140*s), (cx+260*s, cy+520*s)], fill=dress+(255,), outline=INK+(255,))
    hatch(d, (cx-260*s, cy+140*s, cx+260*s, cy+520*s), 14, 0.5, (20, 6, 6, 90), 3)
    d.rectangle((cx-70*s, cy+150*s, cx+70*s, cy+210*s), fill=(226, 214, 180, 255), outline=INK+(255,), width=3)
    # bras leves
    for sx in (-1, 1):
        d.line((cx+sx*60*s, cy+170*s, cx+sx*190*s, cy-(60*arms)*s+ (40*s if sx > 0 else 0)), fill=(214, 172, 138, 255), width=int(34*s))
        d.ellipse((cx+sx*190*s-22*s, cy-(60*arms)*s-22*s+(40*s if sx > 0 else 0), cx+sx*190*s+22*s, cy-(60*arms)*s+22*s+(40*s if sx > 0 else 0)), fill=(214, 172, 138, 255), outline=INK+(255,), width=3)
    # tete + coiffe
    d.ellipse((cx-80*s, cy-90*s, cx+80*s, cy+140*s), fill=(214, 172, 138, 255), outline=INK+(255,), width=4)
    d.pieslice((cx-92*s, cy-120*s, cx+92*s, cy+60*s), 180, 360, fill=(236, 230, 214, 255), outline=INK+(255,), width=3)
    d.rectangle((cx-92*s, cy-30*s, cx-70*s, cy+110*s), fill=(236, 230, 214, 255)); d.rectangle((cx+70*s, cy-30*s, cx+92*s, cy+110*s), fill=(236, 230, 214, 255))
    for sx in (-1, 1): d.ellipse((cx+sx*30*s-9*s, cy+4*s, cx+sx*30*s+9*s, cy+24*s), fill=INK+(255,))
    d.arc((cx-26*s, cy+64*s, cx+26*s, cy+96*s), 200 if mood > 0 else 20, 340 if mood > 0 else 160, fill=(120, 40, 40, 255), width=int(5*s))

def drum(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-140*s, cy, cx+140*s, cy+170*s), fill=(150, 60, 40, 255), outline=INK+(255,), width=4)
    d.ellipse((cx-140*s, cy-40*s, cx+140*s, cy+40*s), fill=(226, 214, 180, 255), outline=INK+(255,), width=4)
    for k in range(6): d.line((cx-140*s+k*56*s, cy+10*s, cx-112*s+k*56*s, cy+170*s), fill=(40, 20, 10, 255), width=int(5*s))
    d.line((cx+30*s, cy-150*s, cx+110*s, cy-20*s), fill=(100, 70, 40, 255), width=int(12*s))

def lute(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.ellipse((cx-120*s, cy, cx+120*s, cy+260*s), fill=(176, 120, 60, 255), outline=INK+(255,), width=4)
    d.ellipse((cx-40*s, cy+90*s, cx+40*s, cy+170*s), fill=(30, 20, 14, 255))
    d.rectangle((cx-18*s, cy-300*s, cx+18*s, cy+20*s), fill=(100, 70, 40, 255), outline=INK+(255,), width=3)
    for k in (-1, 0, 1): d.line((cx+k*8*s, cy-290*s, cx+k*8*s, cy+170*s), fill=(236, 226, 190, 255), width=2)

def cross_pole(im, cx, cy, s=1.0):
    d = ImageDraw.Draw(im)
    d.rectangle((cx-10*s, cy, cx+10*s, cy+520*s), fill=(100, 70, 40, 255), outline=INK+(255,), width=3)
    d.rectangle((cx-70*s, cy+60*s, cx+70*s, cy+90*s), fill=(100, 70, 40, 255), outline=INK+(255,), width=3)

def chronicle(im, cx, cy, w=480, h=680, title="CHRONIQUE"):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx-w//2, cy-h//2, cx+w//2, cy+h//2), radius=18, fill=(86, 54, 34, 255), outline=INK+(255,), width=6)
    d.rectangle((cx-w//2+30, cy-h//2+30, cx+w//2-30, cy+h//2-30), outline=GOLD+(255,), width=4)
    f = font(54); d.text((cx - f.getlength(title)/2, cy-30), title, font=f, fill=GOLD+(255,))

# -*- coding: utf-8 -*-
"""İLK 11 · Hikâye Reels motoru (Hoca anlatımlı, şablon sahneli).

Kullanım:
  python3 motor/hikaye.py senaryo.json cikti --onizleme   # sahne kareleri + zamanlama (hızlı kontrol)
  python3 motor/hikaye.py senaryo.json cikti              # cikti/<slug>.mp4 (+ kapak.jpg)

senaryo.json:
{
 "slug": "2026-10-24-leicester",
 "ses": "ses.mp3",                       # ana anlatım (tüm cümleler sırayla, tek dosya)
 "cumleler": [ "Cümle 1.", {"soz": "Bin dokuz yüz elli dört.", "altyazi": "1954."}, ... ],
 "sahneler": [ {"tip": "kanca", "cumleler": [0], ...parametreler}, ... ],
 "soru": "Sence ... ?",                  # kapanış sahnesindeki soru
 "kapak_sn": 2.5                         # isteğe bağlı: kapak karesi
}
Kapanış (takip çağrısı) sahnesi ve Hoca'nın "Daha fazlası için İlk On Bir'i takip etmeyi unutma!" sesi otomatik eklenir.
Sahne tipleri ve parametreleri: motor/SABLONLAR.md
"at" alanları: o anın söylendiği kelimenin başı (küçük harf, ör. "madrid"); yoksa sahne başından saniye (sayı).
"""
import json, math, os, re, subprocess, sys, wave, random, html as HT
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ilk_parts import (hoca, kid, bowl, paper, ball, colosseum, stopwatch, confetti, tr_flag, es_flag,
                       OL, LIME, TR_RED, SKIN)

SR, FPS = 44100, 30
VOW = set("aeıioöuüâîûAEIİOÖUÜ")


def tr_upper(s):
    return str(s).replace("i", "İ").replace("ı", "I").upper()


def esc(s):
    return HT.escape(str(s), quote=True)


def norm(w):
    return w.replace("İ", "i").replace("I", "ı").lower().strip(".,:;!?…\"'’")


def accent(text, color=LIME):
    """'KURAYLA *DÜNYA KUPASI*?' -> vurgulu tspan"""
    parts = re.split(r"(\*[^*]+\*)", text)
    out = ""
    for p in parts:
        if p.startswith("*") and p.endswith("*"):
            out += f"<tspan fill='{color}'>{esc(p[1:-1])}</tspan>"
        else:
            out += esc(p)
    return out


# ============================================================ BAYRAKLAR
def bayrak(code, w):
    h = w * 2 / 3
    code = (code or "").lower()
    V = lambda cs: "".join(f"<rect x='{w * i / len(cs):.1f}' width='{w / len(cs) + .5:.1f}' height='{h:.1f}' fill='{c}'/>" for i, c in enumerate(cs))
    H = lambda cs: "".join(f"<rect y='{h * i / len(cs):.1f}' width='{w:.1f}' height='{h / len(cs) + .5:.1f}' fill='{c}'/>" for i, c in enumerate(cs))
    if code == "tr":
        return tr_flag(w)
    if code == "es":
        return es_flag(w)
    simple = {"it": V(["#009246", "#FFFFFF", "#CE2B37"]), "fr": V(["#0055A4", "#FFFFFF", "#EF4135"]),
              "be": V(["#000000", "#FDDA24", "#EF3340"]), "ie": V(["#169B62", "#FFFFFF", "#FF883E"]),
              "mx": V(["#006847", "#FFFFFF", "#CE1126"]), "ng": V(["#008751", "#FFFFFF", "#008751"]),
              "de": H(["#000000", "#DD0000", "#FFCE00"]), "nl": H(["#AE1C28", "#FFFFFF", "#21468B"]),
              "ru": H(["#FFFFFF", "#0039A6", "#D52B1E"]), "at": H(["#ED2939", "#FFFFFF", "#ED2939"]),
              "hu": H(["#CE2939", "#FFFFFF", "#477050"]), "co": H(["#FCD116", "#FCD116", "#003893", "#CE1126"]),
              "hr": H(["#FF0000", "#FFFFFF", "#171796"]), "rs": H(["#C6363C", "#0C4076", "#FFFFFF"]),
              "ua": H(["#0057B7", "#FFD700"]), "pl": H(["#FFFFFF", "#DC143C"])}
    if code in simple:
        return simple[code]
    if code == "pt":
        return (f"<rect width='{w * .4:.1f}' height='{h:.1f}' fill='#006600'/><rect x='{w * .4:.1f}' width='{w * .6:.1f}' height='{h:.1f}' fill='#FF0000'/>"
                f"<circle cx='{w * .4:.1f}' cy='{h / 2:.1f}' r='{h * .2:.1f}' fill='#FFCC00'/>")
    if code == "br":
        return (f"<rect width='{w}' height='{h:.1f}' fill='#009C3B'/><polygon points='{w * .08:.1f},{h / 2:.1f} {w / 2:.1f},{h * .1:.1f} {w * .92:.1f},{h / 2:.1f} {w / 2:.1f},{h * .9:.1f}' fill='#FFDF00'/>"
                f"<circle cx='{w / 2:.1f}' cy='{h / 2:.1f}' r='{h * .22:.1f}' fill='#002776'/>")
    if code == "ar":
        return H(["#74ACDF", "#FFFFFF", "#74ACDF"]) + f"<circle cx='{w / 2:.1f}' cy='{h / 2:.1f}' r='{h * .1:.1f}' fill='#F6B40E'/>"
    if code == "uy":
        return (H(["#FFFFFF", "#0038A8"] * 4 + ["#FFFFFF"]) + f"<rect width='{w * .38:.1f}' height='{h * 5 / 9:.1f}' fill='#FFFFFF'/>"
                f"<circle cx='{w * .19:.1f}' cy='{h * .27:.1f}' r='{h * .15:.1f}' fill='#FCD116'/>")
    if code in ("eng", "en", "gb-eng"):
        return (f"<rect width='{w}' height='{h:.1f}' fill='#FFFFFF'/><rect x='{w * .44:.1f}' width='{w * .12:.1f}' height='{h:.1f}' fill='#CE1124'/>"
                f"<rect y='{h * .41:.1f}' width='{w}' height='{h * .18:.1f}' fill='#CE1124'/>")
    if code in ("sct", "gb-sct"):
        return (f"<rect width='{w}' height='{h:.1f}' fill='#005EB8'/><path d='M0 0 L{w} {h:.1f} M{w} 0 L0 {h:.1f}' stroke='#FFFFFF' stroke-width='{h * .2:.1f}'/>")
    if code == "jp":
        return f"<rect width='{w}' height='{h:.1f}' fill='#FFFFFF'/><circle cx='{w / 2:.1f}' cy='{h / 2:.1f}' r='{h * .3:.1f}' fill='#BC002D'/>"
    if code == "gr":
        return H(["#0D5EAF", "#FFFFFF"] * 4 + ["#0D5EAF"]) + f"<rect width='{w * .37:.1f}' height='{h * 5 / 9:.1f}' fill='#0D5EAF'/>" + \
            f"<path d='M{w * .185:.1f} 0 V{h * 5 / 9:.1f} M0 {h * 5 / 18:.1f} H{w * .37:.1f}' stroke='#FFFFFF' stroke-width='{h / 9:.1f}'/>"
    if code == "us":
        return H(["#B22234", "#FFFFFF"] * 6 + ["#B22234"]) + f"<rect width='{w * .4:.1f}' height='{h * 7 / 13:.1f}' fill='#3C3B6E'/>"
    if code == "ge":  # Gürcistan: beyaz zemin, kırmızı büyük haç + dört küçük haç
        s = h * .2
        out = f"<rect width='{w}' height='{h:.1f}' fill='#FFFFFF'/>"
        out += f"<rect x='{(w - s) / 2:.1f}' width='{s:.1f}' height='{h:.1f}' fill='#FF0000'/><rect y='{(h - s) / 2:.1f}' width='{w}' height='{s:.1f}' fill='#FF0000'/>"
        for cx, cy in ((w * .25, h * .25), (w * .75, h * .25), (w * .25, h * .75), (w * .75, h * .75)):
            a, b = h * .13, h * .045
            out += (f"<rect x='{cx - b:.1f}' y='{cy - a:.1f}' width='{2 * b:.1f}' height='{2 * a:.1f}' fill='#FF0000'/>"
                    f"<rect x='{cx - a:.1f}' y='{cy - b:.1f}' width='{2 * a:.1f}' height='{2 * b:.1f}' fill='#FF0000'/>")
        return out
    if code.startswith("#"):  # "#renk1,#renk2" kulüp renk şeridi (logo yok)
        cs = code.split(",")
        return H(cs)
    return f"<rect width='{w}' height='{h:.1f}' fill='#3A4A40'/>"


def bayrak_kutu(code, x, y, w, cls="", style=""):
    h = w * 2 / 3
    return (f"<g transform='translate({x:.0f} {y:.0f})'><g class='{cls}' style='{style}'>"
            f"<rect x='-5' y='-5' width='{w + 10}' height='{h + 10:.0f}' rx='6' fill='{OL}'/>"
            f"<svg width='{w}' height='{h:.1f}' viewBox='0 0 {w} {h:.1f}' overflow='hidden'>{bayrak(code, w)}</svg></g></g>")


# ============================================================ İKONLAR (merkez 0,0; yaklaşık 300px)
def ikon(name, pid="i"):
    n = (name or "top").lower()
    if n.startswith("bayrak:"):
        c = n.split(":", 1)[1]
        return f"<g transform='translate(-170 -113)'>{bayrak_kutu(c, 0, 0, 340)}</g>"
    if n.startswith("forma"):
        parts = (n.split(":", 1)[1] if ":" in n else "#C6FF00,#0A0A0A,11").split(",")
        c1, c2, num = (parts + ["#0A0A0A", "11"])[:3]
        return (f"<path d='M-90 -150 Q0 -118 90 -150 L170 -112 L230 -20 L170 20 L150 -6 L150 160 Q0 180 -150 160 L-150 -6 L-170 20 L-230 -20 L-170 -112Z' "
                f"fill='{c1}' stroke='{OL}' stroke-width='10' stroke-linejoin='round'/>"
                f"<path d='M-90 -150 Q0 -118 90 -150' fill='none' stroke='{c2}' stroke-width='14'/>"
                f"<text y='110' text-anchor='middle' font-family='Anton' font-size='200' fill='{c2}' stroke='{OL}' stroke-width='6' paint-order='stroke'>{esc(num)}</text>")
    if n == "top":
        return ball(0, 0, 150, pid)
    if n == "kupa":
        return ("<path d='M-120 -150 H120 V-70 C120 20 60 70 0 80 C-60 70 -120 20 -120 -70Z' fill='#F2C14E' stroke='#0A0A0A' stroke-width='12' stroke-linejoin='round'/>"
                "<path d='M-120 -120 C-200 -120 -200 0 -110 10 M120 -120 C200 -120 200 0 110 10' fill='none' stroke='#0A0A0A' stroke-width='26'/>"
                "<path d='M-120 -120 C-200 -120 -200 0 -110 10 M120 -120 C200 -120 200 0 110 10' fill='none' stroke='#F2C14E' stroke-width='12'/>"
                "<rect x='-24' y='78' width='48' height='60' fill='#E0A93A' stroke='#0A0A0A' stroke-width='10'/>"
                "<rect x='-90' y='134' width='180' height='40' rx='8' fill='#6B4A2A' stroke='#0A0A0A' stroke-width='10'/>"
                "<path d='M-70 -120 V-60' stroke='#FFF3C4' stroke-width='16' stroke-linecap='round' opacity='.8'/>")
    if n == "duduk":
        return ("<g transform='rotate(-15)'><rect x='-120' y='-50' width='240' height='110' rx='45' fill='#D9DEE2' stroke='#0A0A0A' stroke-width='12'/>"
                "<circle cx='-90' cy='10' r='80' fill='#D9DEE2' stroke='#0A0A0A' stroke-width='12'/><rect x='70' y='-36' width='34' height='26' fill='#0A0A0A'/>"
                "<circle cx='-90' cy='10' r='26' fill='#9AA3AA'/></g>")
    if n == "saat":
        return stopwatch(140)
    if n in ("kart_kirmizi", "kart_sari"):
        c = "#E31B23" if n == "kart_kirmizi" else "#FFD400"
        return (f"<g transform='rotate(10)'><rect x='-100' y='-150' width='200' height='290' rx='18' fill='{c}' stroke='#0A0A0A' stroke-width='12'/>"
                "<path d='M-70 -120 L-70 60' stroke='#FFFFFF' stroke-width='14' opacity='.35' stroke-linecap='round'/></g>")
    if n == "para":
        s = ""
        for i in range(4):
            s += (f"<g transform='translate({-30 + i * 22} {60 - i * 34}) rotate({-8 + i * 5})'><rect x='-150' y='-60' width='300' height='120' rx='12' fill='#5DBB63' stroke='#0A0A0A' stroke-width='10'/>"
                  f"<circle r='38' fill='#3E8E44' stroke='#0A0A0A' stroke-width='6'/><text y='22' text-anchor='middle' font-family='Anton' font-size='60' fill='#E8F5E9'>€</text></g>")
        return s
    if n == "sozlesme":
        return ("<rect x='-130' y='-170' width='260' height='340' rx='14' fill='#F4EBD8' stroke='#0A0A0A' stroke-width='12'/>"
                + "".join(f"<path d='M-90 {-110 + i * 50} H90' stroke='#B9AD94' stroke-width='12' stroke-linecap='round'/>" for i in range(4))
                + "<path d='M-90 110 C-50 70 -20 140 20 100 S70 90 90 110' stroke='#1E4FD8' stroke-width='10' fill='none' stroke-linecap='round'/>"
                "<g transform='translate(110 60) rotate(35)'><rect x='-16' y='-120' width='32' height='200' rx='8' fill='#1E1E1E' stroke='#0A0A0A' stroke-width='8'/><path d='M-16 80 L0 120 L16 80Z' fill='#D9DEE2' stroke='#0A0A0A' stroke-width='6'/></g>")
    if n == "kale":
        return ("<rect x='-210' y='-120' width='420' height='230' fill='none' stroke='#FFFFFF' stroke-width='16'/>"
                + "".join(f"<path d='M{-210 + i * 42} -120 V110' stroke='#FFFFFF' stroke-width='3' opacity='.5'/>" for i in range(1, 10))
                + "".join(f"<path d='M-210 {-120 + i * 46} H210' stroke='#FFFFFF' stroke-width='3' opacity='.5'/>" for i in range(1, 5))
                + ball(80, 40, 60, pid + "k"))
    if n in ("soru", "unlem"):
        ch = "?" if n == "soru" else "!"
        return f"<text y='110' text-anchor='middle' font-family='Anton' font-size='340' fill='{LIME}' stroke='#0A0A0A' stroke-width='12' paint-order='stroke'>{ch}</text>"
    if n == "fanus":
        return bowl(170, 4, "shuffle")
    if n == "mikrofon":
        return ("<rect x='-70' y='-170' width='140' height='200' rx='70' fill='#C7CDD2' stroke='#0A0A0A' stroke-width='12'/>"
                + "".join(f"<path d='M-60 {-130 + i * 34} H60' stroke='#8C959D' stroke-width='8'/>" for i in range(5))
                + "<path d='M-110 -20 C-110 90 110 90 110 -20' fill='none' stroke='#0A0A0A' stroke-width='14'/><rect x='-12' y='70' width='24' height='90' fill='#0A0A0A'/>"
                "<rect x='-70' y='150' width='140' height='24' rx='10' fill='#0A0A0A'/>")
    return ball(0, 0, 150, pid)


# ============================================================ ARKA PLANLAR
def arka(kind, seed=1):
    rnd = random.Random(seed)
    if kind == "gece":
        crowd = "".join(f"<circle cx='{rnd.uniform(0, 1080):.0f}' cy='{rnd.uniform(1060, 1180):.0f}' r='{rnd.uniform(1.5, 3.5):.1f}' "
                        f"fill='{rnd.choice(['#FFFFFF', '#FFE9A8', LIME])}' opacity='{rnd.uniform(.3, .9):.2f}'/>" for _ in range(240))
        return ("<rect width='1080' height='1920' fill='url(#nightSky)'/>"
                "<circle cx='120' cy='260' r='150' fill='#FFF6D8' opacity='.25' filter='url(#blur)'/><circle cx='960' cy='260' r='150' fill='#FFF6D8' opacity='.25' filter='url(#blur)'/>"
                "<path d='M-20 1060 Q540 980 1100 1060 L1100 1200 L-20 1200Z' fill='#0B1022'/>" + crowd + "<rect y='1190' width='1080' height='730' fill='#1F6B35'/>")
    if kind == "gunbatimi":
        return ("<rect width='1080' height='1920' fill='url(#duskSky)'/><circle cx='540' cy='880' r='200' fill='#FFB46B' opacity='.5'/>"
                "<path d='M-20 1000 Q540 900 1100 1000 L1100 1130 L-20 1130Z' fill='#2A1A2E'/>"
                + "".join(f"<rect x='{30 + i * 70}' y='{960 - 30 * math.sin(i / 15 * math.pi):.0f}' width='34' height='40' fill='#F7A04A' opacity='.35'/>" for i in range(15))
                + "<rect y='1120' width='1080' height='800' fill='#1E1420'/>")
    if kind == "roma":
        return "<rect width='1080' height='1920' fill='url(#duskSky)'/><circle cx='540' cy='820' r='200' fill='#FFB46B' opacity='.55'/>" + colosseum(780) + "<rect y='1110' width='1080' height='810' fill='#1E1420'/>"
    if kind == "soyunma":
        tiles = "".join(f"<rect x='{x}' y='{y}' width='118' height='118' fill='none' stroke='#0E2620' stroke-width='4'/>" for x in range(0, 1080, 120) for y in range(0, 1920, 120))
        return "<rect width='1080' height='1920' fill='#123A31'/>" + tiles + "<rect y='1180' width='1080' height='740' fill='#0C241E'/>"
    if kind == "marka":
        stripes = "".join(f"<rect x='{-600 + i * 110}' y='-400' width='55' height='2800' fill='#FFFFFF'/>" for i in range(24))
        return f"<rect width='1080' height='1920' fill='url(#brandBg)'/><g transform='rotate(-24 540 900)' opacity='.05'>{stripes}</g>"
    # karanlik (spot ışığı)
    return ("<rect width='1080' height='1920' fill='url(#bgDark)'/>"
            "<polygon class='flick' points='450,-60 630,-60 1080,1150 0,1150' fill='#FFF6D8' opacity='.10'/>"
            "<ellipse cx='540' cy='1150' rx='520' ry='70' fill='#FFF6D8' opacity='.12'/>"
            "<rect y='1150' width='1080' height='780' fill='#14301F'/><rect y='1150' width='1080' height='16' fill='#2C5A3C'/>")


def pill(x, y, text, size=40, bg="#0B0F0C", fg=LIME, cls="pop", d=0.0):
    w = len(text) * size * .6 + 70
    h = size * 1.7
    return (f"<g transform='translate({x} {y})'><g class='{cls}' style='--d:{d:.2f}s'>"
            f"<rect x='{-w / 2:.0f}' y='{-h / 2:.0f}' width='{w:.0f}' height='{h:.0f}' rx='{h / 2:.0f}' fill='{bg}' fill-opacity='.92' stroke='{fg}' stroke-width='4'/>"
            f"<text y='{size * .36:.0f}' text-anchor='middle' font-family='Anton' font-size='{size}' letter-spacing='2' fill='{fg}'>{esc(text)}</text></g></g>")


def stamp_text(x, y, text, d, size=80, color=TR_RED, rot=-8):
    w = len(text) * size * .52 + 70
    return (f"<g transform='translate({x} {y}) rotate({rot})'><g class='stamp' style='--d:{d:.2f}s'>"
            f"<rect x='{-w / 2:.0f}' y='{-size * .75:.0f}' width='{w:.0f}' height='{size * 1.5:.0f}' rx='12' fill='#000' fill-opacity='.25' stroke='{color}' stroke-width='10'/>"
            f"<text y='{size * .36:.0f}' text-anchor='middle' font-family='Anton' font-size='{size}' letter-spacing='4' fill='{color}'>{esc(text)}</text></g></g>")


def baslik_svg(text, y=440, maxw=960, size=96, color="#FFFFFF"):
    """1-2 satırlık başlık; '|' satır böler; *vurgu*."""
    lines = text.split("|")
    out = ""
    for i, ln in enumerate(lines):
        L = len(re.sub(r"\*", "", ln))
        fs = min(size, int(maxw / max(1, L * .46)))
        out += (f"<text x='540' y='{y + i * fs * 1.02:.0f}' text-anchor='middle' font-family='Anton' font-size='{fs}' letter-spacing='2' "
                f"fill='{color}' stroke='#0A0A0A' stroke-width='6' paint-order='stroke'>{accent(ln)}</text>")
    return out


def shake(inner, ds):
    for d in ds:
        inner = f"<g class='shake' style='--d:{d:.2f}s'>{inner}</g>"
    return inner


def motes(n=22, seed=3):
    rnd = random.Random(seed)
    return "".join(f"<circle class='float' style='--d:-{rnd.uniform(0, 3):.1f}s' cx='{rnd.uniform(60, 1020):.0f}' cy='{rnd.uniform(200, 1500):.0f}' "
                   f"r='{rnd.uniform(2, 5):.1f}' fill='#FFFFFF' opacity='{rnd.uniform(.15, .45):.2f}'/>" for _ in range(n))


HOCA_IFADE = {"sok": "smile", "smile": "smile", "wink": "wink", "cheer": "cheer"}


def hoca_g(x, y, sc, poz="stand", ifade="smile", cls="", style=""):
    h = hoca(poz, ((HOCA_IFADE.get(ifade, "smile"), None, None),))
    return (f"<g transform='translate({x} {y}) scale({sc})'><g class='{cls}' style='{style}'><g class='bob' style='--d:.6s'>{h}</g></g></g>")


# ============================================================ ŞABLONLAR
# her şablon: f(p, at, sfx, idx) -> svg ; at("kelime"|sayı) -> sahne içi saniye ; sfx(t_rel, tür)
def t_kanca(p, at, sfx, i):
    ik = p.get("ikon", "soru")
    s = arka(p.get("arka", "karanlik"), i) + baslik_svg(p.get("baslik", ""), 465)
    s += (f"<g transform='translate(540 820)'><g class='pop' style='--d:.15s'><g class='bob'>"
          f"<circle r='230' fill='{LIME}' opacity='.10'/>{ikon(ik, 'k' + str(i))}</g></g></g>")
    sfx(.15, "pop")
    if p.get("hoca", "sok") != "yok":
        s += hoca_g(190, 1080, .55, "stand", p.get("hoca", "smile"), "slidein", "--d:.5s;--t:.5s;--fx:-420px;--fy:0px")
        sfx(.5, "whoosh")
    if p.get("damga"):
        d = at(p["damga"].get("at", 1.2))
        s += stamp_text(560, 1080, p["damga"]["metin"], d, 70, p["damga"].get("renk", LIME), -6)
        sfx(d, "stamp")
    return s + motes()


def t_tahta(p, at, sfx, i):
    s = arka("soyunma", i)
    s += ("<rect x='300' y='420' width='720' height='560' rx='18' fill='#6B4A2A' stroke='#0A0A0A' stroke-width='10'/>"
          "<rect x='326' y='446' width='668' height='508' rx='8' fill='#1F3A2E'/>"
          "<ellipse cx='520' cy='560' rx='160' ry='40' fill='#FFFFFF' opacity='.04'/><ellipse cx='820' cy='860' rx='190' ry='50' fill='#FFFFFF' opacity='.05'/>")
    rows = p.get("satirlar", [])[:3]
    ys = {1: [700], 2: [620, 820], 3: [580, 730, 880]}[max(1, len(rows))]
    for (r, y) in zip(rows, ys):
        d = at(r.get("at", .4))
        txt = r.get("metin", "")
        fs = min(int(r.get("boyut", 150 if len(rows) == 1 else 110 if len(rows) == 2 else 84)), int(620 / max(1, len(txt) * .5)))
        bx = ""
        if r.get("bayrak"):
            bx = bayrak_kutu(r["bayrak"], 360, y - fs * .62, 110)
        s += (f"<g class='chalk' style='--d:{d:.2f}s'>{bx}<text x='{700 if r.get('bayrak') else 660}' y='{y}' text-anchor='middle' font-family='Anton' "
              f"font-size='{fs}' fill='{r.get('renk', '#F2F2E8')}'>{esc(txt)}</text></g>")
        sfx(d, "chalk")
    s += hoca_g(185, 840, .78, "point", p.get("hoca", "smile"), "slidein", "--d:.05s;--t:.55s;--fx:-520px;--fy:0px")
    return s


def t_skor(p, at, sfx, i):
    s = arka("gece", i)
    bulbs = "".join(f"<circle class='glow' style='--d:-{(k % 4) * .2:.1f}s' cx='{90 + k * 39}' cy='436' r='7' fill='#FFB000'/>"
                    f"<circle class='glow' style='--d:-{(k % 4) * .2 + .1:.1f}s' cx='{90 + k * 39}' cy='1004' r='7' fill='#FFB000'/>" for k in range(24))
    b = ("<rect x='66' y='412' width='948' height='616' rx='20' fill='#0E0E0E' stroke='#2C2C2C' stroke-width='10'/>" + bulbs
         + f"<text x='540' y='512' text-anchor='middle' font-family='Anton' font-size='54' letter-spacing='8' fill='#FFB000'>{esc(p.get('baslik', ''))}</text>")
    rows = p.get("satirlar", [])[:3]
    ys = {1: [760], 2: [680, 880], 3: [640, 780, 920]}[max(1, len(rows))]
    for r, y in zip(rows, ys):
        d = at(r.get("at", .3))
        sfx(d, "clack")
        lf, rf = r.get("sol_bayrak"), r.get("sag_bayrak")
        nfs = 58 if max(len(r.get("sol", "")), len(r.get("sag", ""))) <= 9 else 44
        b += (f"<g class='flipin' style='--d:{d:.2f}s'>"
              + (f"<text x='540' y='{y - 74}' text-anchor='middle' font-family='Inter' font-weight='800' font-size='30' letter-spacing='6' fill='#9AA59C'>{esc(r.get('etiket', ''))}</text>" if r.get("etiket") else "")
              + (bayrak_kutu(lf, 100, y - 42, 96) if lf else "")
              + f"<text x='{216 if lf else 110}' y='{y + 22}' font-family='Anton' font-size='{nfs}' fill='#FFFFFF'>{esc(r.get('sol', ''))}</text>"
              f"<rect x='432' y='{y - 52}' width='216' height='104' rx='10' fill='#1C1C1C' stroke='#333' stroke-width='4'/>"
              f"<text x='540' y='{y + 36}' text-anchor='middle' font-family='Anton' font-size='96' fill='#FFB000'>{esc(r.get('skor', ''))}</text>"
              f"<text x='{864 if rf else 970}' y='{y + 22}' text-anchor='end' font-family='Anton' font-size='{nfs}' fill='#FFFFFF'>{esc(r.get('sag', ''))}</text>"
              + (bayrak_kutu(rf, 884, y - 42, 96) if rf else "") + "</g>")
    if p.get("damga"):
        d = at(p["damga"].get("at", 2.0))
        b += stamp_text(540, 975, p["damga"]["metin"], d, 70, p["damga"].get("renk", LIME), -6)
        sfx(d, "stamp")
        b = shake(b, [d])
    return s + b


def t_sayi(p, at, sfx, i):
    d = at(p.get("at", .4))
    s = arka(p.get("arka", "karanlik"), i)
    if p.get("ust"):
        s += pill(540, 420, p["ust"], 42, d=.1)
    s += (f"<g transform='translate(540 700)'><g class='pop' style='--d:{max(0, d - .5):.2f}s'><g class='bob'><circle r='180' fill='{LIME}' opacity='.08'/>"
          f"<g transform='scale(.8)'>{ikon(p.get('ikon', 'unlem'), 's' + str(i))}</g></g></g></g>")
    txt = p.get("sayi", "")
    fs = min(220, int(980 / max(1, len(txt) * .5)))
    s += (f"<g transform='translate(540 1020)'><g class='stamp' style='--d:{d:.2f}s'><text text-anchor='middle' font-family='Anton' font-size='{fs}' "
          f"fill='{p.get('renk', LIME)}' stroke='#0A0A0A' stroke-width='10' paint-order='stroke'>{esc(txt)}</text></g></g>")
    if p.get("etiket"):
        s += f"<g class='fadein' style='--d:{d + .3:.2f}s'><text x='540' y='1100' text-anchor='middle' font-family='Anton' font-size='48' letter-spacing='4' fill='#FFFFFF'>{esc(p['etiket'])}</text></g>"
    sfx(d, "stamp")
    return shake(s, [d]) + motes(14, i)


def t_an(p, at, sfx, i):
    d = at(p.get("at", .4))
    s = arka(p.get("arka", "gece"), i)
    if p.get("ust"):
        s += pill(540, 420, p["ust"], 40, d=.15)
    if p.get("sol_bayrak") or p.get("sag_bayrak"):
        if p.get("sol_bayrak"):
            s += bayrak_kutu(p["sol_bayrak"], 140, 500, 170) + f"<text x='225' y='668' text-anchor='middle' font-family='Anton' font-size='44' fill='#FFFFFF'>{esc(p.get('sol', ''))}</text>"
        if p.get("sag_bayrak"):
            s += bayrak_kutu(p["sag_bayrak"], 770, 500, 170) + f"<text x='855' y='668' text-anchor='middle' font-family='Anton' font-size='44' fill='#FFFFFF'>{esc(p.get('sag', ''))}</text>"
    if p.get("buyuk"):
        db = at(p.get("buyuk_at", p.get("at", .6)))
        s += (f"<g transform='translate(540 650)'><g class='stamp' style='--d:{db:.2f}s'><text text-anchor='middle' font-family='Anton' font-size='200' fill='{LIME}' "
              f"stroke='#0A0A0A' stroke-width='10' paint-order='stroke'>{esc(p['buyuk'])}</text></g></g>")
        sfx(db, "stamp")
    s += (f"<g transform='translate(540 900)'><g class='pop' style='--d:{d:.2f}s'><g transform='scale(.62)'>{ikon(p.get('ikon', 'top'), 'a' + str(i))}</g>"
          + (f"<g class='spinhand' style='--d:{d + .1:.2f}s'><line x1='0' y1='0' x2='0' y2='-70' stroke='{OL}' stroke-width='9' stroke-linecap='round'/></g>" if p.get("ikon") == "saat" else "")
          + (f"<text y='160' text-anchor='middle' font-family='Anton' font-size='52' fill='#FFFFFF' stroke='#0A0A0A' stroke-width='6' paint-order='stroke'>{esc(p['metin'])}</text>" if p.get("metin") else "")
          + "</g></g>")
    sfx(d, "tick" if p.get("ikon") == "saat" else "pop")
    return shake(s, [db]) if p.get("buyuk") else s


def t_hoca(p, at, sfx, i):
    s = arka(p.get("arka", "marka"), i)
    s += hoca_g(540, 860, .95, p.get("poz", "stand"), p.get("ifade", "smile"), "rise", "--d:.05s")
    if p.get("balon"):
        d = at(p.get("at", .5))
        txt = p["balon"]
        lines = [txt] if len(txt) <= 22 else [txt[:len(txt) // 2].rsplit(" ", 1)[0], txt[len(txt[:len(txt) // 2].rsplit(" ", 1)[0]) + 1:]]
        fs = 62 if max(len(l) for l in lines) <= 20 else 52
        s += (f"<g transform='translate(540 470)'><g class='pop' style='--d:{d:.2f}s'>"
              "<rect x='-430' y='-120' width='860' height='230' rx='40' fill='#FFF6E0' stroke='#0A0A0A' stroke-width='7'/>"
              "<path d='M-40 106 L0 180 L40 106Z' fill='#FFF6E0' stroke='#0A0A0A' stroke-width='7' stroke-linejoin='round'/><rect x='-34' y='96' width='68' height='16' fill='#FFF6E0'/>"
              + "".join(f"<text y='{(-20 if len(lines) > 1 else 22) + k * 80}' text-anchor='middle' font-family='Anton' font-size='{fs}' fill='#2A1A10'>{esc(l)}</text>" for k, l in enumerate(lines))
              + "</g></g>")
        sfx(d, "pop")
    return s


def t_zafer(p, at, sfx, i):
    d = at(p.get("at", .6))
    s = arka("karanlik", i)
    rays = "".join(f"<polygon points='540,640 {540 + 1400 * math.cos(math.radians(a)):.0f},{640 + 1400 * math.sin(math.radians(a)):.0f} "
                   f"{540 + 1400 * math.cos(math.radians(a + 7)):.0f},{640 + 1400 * math.sin(math.radians(a + 7)):.0f}' fill='#FFFFFF' opacity='.07'/>" for a in range(0, 360, 15))
    renk = p.get("renk", TR_RED)
    s += (f"<g class='fadein' style='--d:{d:.2f}s'><rect width='1080' height='1920' fill='{renk}' opacity='.35'/>"
          f"<g class='spin' style='--t:30s;transform-box:view-box;transform-origin:540px 640px'>{rays}</g></g>")
    if p.get("bayrak"):
        s += (f"<g transform='translate(195 300)'><g class='unfurl' style='--d:{d + .05:.2f}s'><g class='flagwave'>"
              f"<rect x='-8' y='-8' width='706' height='476' rx='10' fill='#0A0A0A'/><svg width='690' height='460' viewBox='0 0 690 460'>{bayrak(p['bayrak'], 690)}</svg></g></g></g>")
    word = p.get("kelime", "")
    fs = min(170, int(660 / max(1, len(word) * .5)))
    du = at(p.get("kart_at", max(0, d - 1.2)))
    s += (f"<g transform='translate(540 900)'><g class='unfold' style='--d:{du:.2f}s'>"
          "<rect x='-360' y='-130' width='720' height='260' rx='14' fill='#F4EBD8' stroke='#0A0A0A' stroke-width='9'/><path d='M-360 0 L360 0' stroke='#D8CBAE' stroke-width='5'/>"
          f"<g transform='translate(0 {fs * .36:.0f})'><g class='stamp' style='--d:{d:.2f}s'><text text-anchor='middle' font-family='Anton' font-size='{fs}' letter-spacing='4' fill='{renk}'>{esc(word)}</text></g></g></g></g>")
    s += confetti(540, 760, d + .02, 70)
    if p.get("alt"):
        s += pill(540, 1110, p["alt"], 40, d=at(p.get("alt_at", d + 1.2)))
    sfx(du, "whoosh"); sfx(d, "zafer"); sfx(d, "stamp")
    return shake(s, [d])


def t_takip(p, at, sfx, i, soru, rtak):
    s = arka("marka", i)
    if soru:
        s += pill(540, 400, tr_upper(soru), 38 if len(soru) <= 40 else 32, d=.2, fg="#FFFFFF")
    s += hoca_g(540, 760, .88, "stand", "wink", "rise", "--d:.05s")
    s += (f"<g transform='translate(540 1105)'><g class='pop' style='--d:.35s'>"
          "<rect x='-430' y='-78' width='860' height='156' rx='78' fill='#0B0F0C' stroke='#C6FF00' stroke-width='5'/>"
          f"<circle cx='-350' cy='0' r='54' fill='#0B0F0C' stroke='{LIME}' stroke-width='7'/>"
          f"<text x='-350' y='26' text-anchor='middle' font-family='Anton' font-size='64' fill='{LIME}'>11</text>"
          "<text x='-275' y='-8' font-family='Anton' font-size='44' fill='#FFFFFF'>İLK 11</text>"
          "<text x='-275' y='38' font-family='Inter' font-weight='700' font-size='30' fill='#B9C2BB'>@ilk.onbir11</text>"
          f"<g class='hide' style='--d:{rtak + .25:.2f}s'><g transform='translate(250 0)'><g class='pulse'><rect x='-140' y='-48' width='280' height='96' rx='48' fill='{LIME}'/>"
          "<text y='17' text-anchor='middle' font-family='Anton' font-size='46' letter-spacing='2' fill='#0A0A0A'>TAKİP ET</text></g></g></g>"
          f"<g class='show' style='--d:{rtak + .25:.2f}s'><g transform='translate(250 0)'><rect x='-140' y='-48' width='280' height='96' rx='48' fill='#2A2F2B' stroke='#5B655D' stroke-width='3'/>"
          "<text y='17' text-anchor='middle' font-family='Anton' font-size='42' letter-spacing='1' fill='#FFFFFF'>TAKİPTESİN ✓</text></g></g></g></g>")
    s += (f"<g transform='translate(820 1230)'><g class='tapin' style='--d:{rtak - .25:.2f}s'>"
          "<g transform='rotate(-25)'><path d='M0 0 C-8 -60 -6 -120 6 -128 C18 -136 28 -126 28 -112 L30 -70 C40 -82 60 -78 62 -62 C74 -72 92 -66 92 -50 "
          "C104 -58 120 -50 118 -32 L114 20 C110 60 80 80 40 80 L20 80 C0 74 -10 50 -14 30Z' fill='#FFFFFF' stroke='#0A0A0A' stroke-width='8' stroke-linejoin='round'/></g></g></g>"
          f"<g transform='translate(790 1110)'><circle class='boom' style='--d:{rtak + .2:.2f}s' r='70' fill='none' stroke='{LIME}' stroke-width='8'/></g>")
    sfx(.35, "pop"); sfx(rtak + .2, "tap")
    return s


FOTO_DIR = None  # senaryo.json'un klasörü (main içinde atanır)


def _foto_uri(path):
    import base64, mimetypes
    p = path if os.path.isabs(path) else os.path.join(FOTO_DIR or ".", path)
    mt = mimetypes.guess_type(p)[0] or "image/jpeg"
    return f"data:{mt};base64," + base64.b64encode(open(p, "rb").read()).decode()


def t_foto(p, at, sfx, i):
    """Gerçek fotoğraf sahnesi — YALNIZ kullanım hakkı olan (ör. Wikimedia Commons CC lisanslı) fotoğraflar.
    p: foto (dosya, senaryo.json'a göre), kredi ("Foto: Ad · Wikimedia · CC BY-SA 4.0" — zorunlu), baslik (ops., '|' ve *vurgu*),
       ust (ops. çip), alt (ops. etiket), alt_at, odak ("ust"|"orta"; varsayılan ust), damga (ops.).
    Güvenli alan: üst etiket ~300-335px, altyazı bandı 1170px'ten aşağı; kart 360-1160 arasında kalır."""
    uri = _foto_uri(p["foto"])
    s = arka(p.get("arka", "karanlik"), i)
    if p.get("baslik"):
        cw, ch, cy = 520, 560, 585
    else:
        cw, ch, cy = 640, 680, 465
    cx = (1080 - cw) // 2
    s += (f"<defs><filter id='fb{i}'><feGaussianBlur stdDeviation='28'/></filter>"
          f"<clipPath id='fc{i}'><rect x='0' y='0' width='{cw}' height='{ch}' rx='14'/></clipPath></defs>")
    s += (f"<image href='{uri}' x='-140' y='-60' width='1360' height='2040' preserveAspectRatio='xMidYMid slice' "
          f"filter='url(#fb{i})' opacity='.38'/><rect width='1080' height='1920' fill='#050806' opacity='.35'/>")
    if p.get("baslik"):
        s += f"<g class='fadein' style='--d:.2s'>{baslik_svg(p['baslik'], 450, size=88)}</g>"
    elif p.get("ust"):
        w = len(p["ust"]) * 24 + 60
        s += (f"<g class='fadein' style='--d:.1s'><rect x='{540 - w / 2:.0f}' y='375' width='{w}' height='58' rx='29' fill='{LIME}'/>"
              f"<text x='540' y='417' text-anchor='middle' font-family='Anton' font-size='36' letter-spacing='3' fill='#0A0F0A'>{esc(p['ust'])}</text></g>")
    ar = "xMidYMin slice" if p.get("odak", "ust") == "ust" else "xMidYMid slice"
    card = (f"<rect x='-14' y='-14' width='{cw + 28}' height='{ch + 28}' rx='20' fill='#F4F1E8'/>"
            f"<g clip-path='url(#fc{i})'><image href='{uri}' width='{cw}' height='{ch}' preserveAspectRatio='{ar}'/>"
            f"<rect x='0' y='{ch - 52}' width='{cw}' height='52' fill='#000000' opacity='.6'/></g>"
            f"<text x='{cw - 16}' y='{ch - 18}' text-anchor='end' font-family='Inter' font-weight='700' font-size='21' fill='#E8EDE9'>{esc(p.get('kredi', ''))}</text>")
    s += (f"<g transform='translate({cx} {cy}) rotate(-2 {cw / 2} {ch / 2})'><g class='pop' style='--d:.25s'>"
          f"<g filter='drop-shadow(0 18px 30px rgba(0,0,0,.55))'>{card}</g></g></g>")
    sfx(.25, "pop")
    if p.get("alt"):
        s += pill(540, cy + ch - 110, p["alt"], 40, d=at(p.get("alt_at", 1.0)))
    if p.get("damga"):
        d = at(p["damga"].get("at", 1.2))
        s += stamp_text(560, cy + ch - 120, p["damga"]["metin"], d, 66, p["damga"].get("renk", LIME), -6)
        sfx(d, "stamp")
    return s + motes()


TEMPLATES = {"kanca": t_kanca, "tahta": t_tahta, "skor": t_skor, "sayi": t_sayi, "an": t_an, "hoca": t_hoca, "zafer": t_zafer,
             "foto": t_foto}

DEFS = ("<defs>"
        "<radialGradient id='bgDark' cx='.5' cy='.4' r='.8'><stop offset='0' stop-color='#1A2A20'/><stop offset='1' stop-color='#060908'/></radialGradient>"
        "<radialGradient id='brandBg' cx='.5' cy='.45' r='.8'><stop offset='0' stop-color='#1E5636'/><stop offset='.55' stop-color='#0B2416'/><stop offset='1' stop-color='#030805'/></radialGradient>"
        "<linearGradient id='nightSky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#03050C'/><stop offset='.55' stop-color='#0B1433'/><stop offset='1' stop-color='#1A2C5E'/></linearGradient>"
        "<linearGradient id='duskSky' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#1E1730'/><stop offset='.5' stop-color='#6B2E3A'/><stop offset='1' stop-color='#E07A3F'/></linearGradient>"
        "<radialGradient id='vig' cx='.5' cy='.45' r='.75'><stop offset='.55' stop-color='#000' stop-opacity='0'/><stop offset='1' stop-color='#000' stop-opacity='.65'/></radialGradient>"
        "<filter id='blur' x='-50%' y='-50%' width='200%' height='200%'><feGaussianBlur stdDeviation='40'/></filter>"
        "</defs>")


# ============================================================ SES ZAMANLAMASI
def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def sentence_spans(sig, n):
    hop = int(.01 * SR)
    env = np.array([np.sqrt(np.mean(sig[i:i + hop] ** 2)) for i in range(0, len(sig) - hop, hop)])
    q = env < max(1e-4, .05 * np.percentile(env, 95))
    gaps, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]:
                j += 1
            if (j - i) * .01 >= .22:
                gaps.append((i * .01, j * .01))
            i = j
        else:
            i += 1
    voiced = np.where(~q)[0]
    a0, b0 = voiced[0] * .01, voiced[-1] * .01 + .01
    inner = [g for g in gaps if g[0] > a0 and g[1] < b0]
    inner.sort(key=lambda g: g[1] - g[0], reverse=True)
    cuts = sorted(inner[:n - 1])
    if len(cuts) < n - 1:  # yeterli boşluk yoksa eşit böl
        L = (b0 - a0) / n
        cuts = sorted(cuts + [(a0 + L * k, a0 + L * k) for k in range(1, n) if all(abs(a0 + L * k - c[0]) > .5 for c in cuts)])[:n - 1]
    spans, st = [], a0
    for g in cuts:
        spans.append((st, g[0])); st = g[1]
    spans.append((st, b0))
    return spans


def syl(w):
    if re.match(r"^[\d\-'’.,:]+$", w):
        return max(2, len(re.sub(r"\D", "", w)))
    return max(1, sum(c in VOW for c in w))


def word_times(spoken, shown, a, b):
    toks = shown.split()
    weights = [syl(t) for t in toks]
    if len(spoken.split()) and shown != spoken:  # gösterilen metni konuşulan süreye yay
        tot_sp = sum(syl(w) for w in spoken.split())
        k0 = tot_sp / max(1, sum(weights))
        weights = [w * k0 for w in weights]
    ws = [(w, x + .4, .8 if w.endswith(",") else 0) for w, x in zip(toks, weights)]
    total = sum(x + p for _, x, p in ws) - ws[-1][2]
    k, t, out = (b - a) / total, a, []
    for w, x, p in ws:
        out.append([w, round(t, 3), round(t + x * k, 3)])
        t += (x + p) * k
    return out


def chunks(WT, T):
    res = []
    for wt in WT:
        cur = []
        for w in wt:
            cur.append(w)
            if len(cur) >= 3 or len(" ".join(x[0] for x in cur)) >= 12 or re.search(r"[.,:!?…]$", w[0]):
                res.append(cur); cur = []
        if cur:
            res.append(cur)
    out = []
    for i, c in enumerate(res):
        nxt = res[i + 1][0][1] if i + 1 < len(res) else T
        out.append(dict(t0=c[0][1] - .04, end=min(nxt, c[-1][2] + .55), w=c))
    return out


# ============================================================ SES MİKSİ
_rng = np.random.default_rng(11)


def _sn(n, c, w):
    sp = np.fft.rfft(_rng.standard_normal(n)); fr = np.fft.rfftfreq(n, 1 / SR)
    sp *= np.exp(-((np.log(fr + 1) - np.log(c)) ** 2) / w)
    x = np.fft.irfft(sp, n)
    return x / (np.abs(x).max() + 1e-9)


def _t(n):
    return np.arange(n) / SR


def sfx_signal(kind):
    if kind == "pop":
        n = int(.12 * SR); x = _t(n)
        return .35 * np.sin(2 * np.pi * np.cumsum(900 * (1 + 1.2 * np.exp(-x / .015))) / SR) * np.exp(-x / .04)
    if kind == "whoosh":
        n = int(.5 * SR); x = _t(n)
        return .3 * _sn(n, 800, .7) * np.sin(np.pi * x / .5) ** 2
    if kind in ("stamp", "thud"):
        n = int(.9 * SR); x = _t(n)
        s = np.sin(2 * np.pi * np.cumsum(34 + 40 * np.exp(-x / .05)) / SR) * np.exp(-x / .22) + .5 * _sn(n, 300, .8) * np.exp(-x / .04)
        s[:int(.15 * SR)] += .35 * _sn(int(.15 * SR), 1500, .6) * np.exp(-x[:int(.15 * SR)] / .03)
        return .6 * s
    if kind == "chalk":
        n = int(.5 * SR); x = _t(n)
        return .18 * _sn(n, 3500, .5) * (.6 + .4 * np.sin(2 * np.pi * 9 * x)) * np.minimum(1, x / .03) * np.minimum(1, (.5 - x) / .05)
    if kind == "clack":
        n = int(.08 * SR); x = _t(n)
        return .4 * (_sn(n, 2500, .5) * np.exp(-x / .01) + .5 * np.sin(2 * np.pi * 900 * x) * np.exp(-x / .02))
    if kind == "tick":
        out = np.zeros(int(2 * SR))
        for k in range(8):
            n = int(.05 * SR); x = _t(n); i = int(k * .25 * SR)
            out[i:i + n] += .25 * np.sin(2 * np.pi * 2200 * x) * np.exp(-x / .008)
        return out
    if kind == "tap":
        n = int(.12 * SR); x = _t(n)
        return .45 * np.sin(2 * np.pi * np.cumsum(1100 * (1 + 1.2 * np.exp(-x / .015))) / SR) * np.exp(-x / .04)
    if kind == "zafer":
        n = int(4 * SR); x = _t(n)
        e = np.minimum(1, x / .25) * np.exp(-np.maximum(0, x - 1.0) / 1.3)
        crowd = (_sn(n, 700, 1.4) + .5 * _sn(n, 1600, 1.0)) * e * (1 + .25 * np.sin(2 * np.pi * 3.3 * x))
        return .5 * crowd
    return np.zeros(10)


def build_audio(voice, cta, cta_at, T, scenes, events, out_wav):
    N = int(T * SR)
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    moods = {"kanca": [38, 45, 50, 53], "tahta": [34, 41, 50, 53], "skor": [36, 43, 48, 52], "sayi": [37, 44, 49, 52],
             "an": [36, 43, 46, 51], "hoca": [41, 48, 53, 57], "zafer": [38, 45, 50, 54, 57, 62], "takip": [43, 47, 50, 55, 59]}
    music = np.zeros(N, np.float32)
    for sc in scenes:
        a, b = sc["start"], sc["end"]
        i0, i1 = int(a * SR), min(N, int((b + .6) * SR))
        x = _t(i1 - i0); dur = b - a
        e = np.minimum(1, x / .35) * np.clip((dur + .6 - x) / .6, 0, 1)
        seg = np.zeros(i1 - i0)
        notes = moods.get(sc["tip"], moods["kanca"])
        for m in notes:
            for det in (-6, 6):
                f = mtof(m) * 2 ** (det / 1200)
                for h in range(1, 6):
                    seg += (1 / h) * np.sin(2 * np.pi * f * h * x + h) * (.85 ** h)
        music[i0:i1] += (seg * e / len(notes)).astype(np.float32)
        if sc["tip"] in ("skor", "an", "sayi"):
            t = a
            while t < b:
                n = int(.6 * SR); xx = _t(n)
                dr = np.sin(2 * np.pi * np.cumsum(48 + 60 * np.exp(-xx / .03)) / SR) * np.exp(-xx / .18)
                k = int(t * SR); seg2 = music[k:k + n]; seg2 += (2.2 * dr[:len(seg2)]).astype(np.float32)
                t += 60 / 96
    music /= np.abs(music).max() + 1e-9
    music *= .17
    fx = np.zeros(N + 5 * SR, np.float32)
    for sc in scenes[1:]:
        s = sfx_signal("whoosh"); i = int(max(0, sc["start"] - .27) * SR); fx[i:i + len(s)] += s.astype(np.float32)
    for t, kind in events:
        s = np.asarray(sfx_signal(kind), dtype=np.float32); i = int(max(0, t) * SR); fx[i:i + len(s)] += s
    v = np.zeros(N, np.float32)
    v[:min(N, len(voice))] = voice[:N]
    i0 = int(cta_at * SR); v[i0:i0 + len(cta)] += cta[:max(0, N - i0)]
    v = v / (np.sqrt(np.mean(v[np.abs(v) > .01] ** 2)) + 1e-9) * .16
    hop = int(.05 * SR)
    envv = np.array([np.sqrt(np.mean(v[i:i + hop] ** 2)) for i in range(0, N, hop)])
    duck = np.repeat(np.where(envv > .02, .6, 1.0), hop)[:N]
    duck = np.convolve(duck, np.ones(hop * 4) / (hop * 4), mode="same")
    mix = v + music * duck + fx[:N] * .55
    fo = int(1.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    mix *= .95 / (np.abs(mix).max() + 1e-9)
    st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())


# ============================================================ ANA AKIŞ
def main():
    spec_path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "cikti"
    preview = "--onizleme" in sys.argv
    os.makedirs(out, exist_ok=True)
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    global FOTO_DIR
    FOTO_DIR = os.path.dirname(os.path.abspath(spec_path))
    voice = load_audio(os.path.join(base, spec.get("ses", "ses.mp3")))
    cta = load_audio(spec.get("cta") and os.path.join(base, spec["cta"]) or os.path.join(HERE, "ses", "cta_hoca.mp3"))
    cum = [c if isinstance(c, dict) else {"soz": c} for c in spec["cumleler"]]
    spans = sentence_spans(voice, len(cum))
    WT = [word_times(c["soz"], c.get("altyazi", c["soz"]), a, b) for c, (a, b) in zip(cum, spans)]
    main_end = len(voice) / SR
    cta_spans = sentence_spans(cta, 2)
    cta_at = spans[-1][1] + .5
    cta_scene_start = cta_at - .15
    cta_words = [word_times("Daha fazlası için", "Daha fazlası için", cta_at + cta_spans[0][0], cta_at + cta_spans[0][1]),
                 word_times("İlk On Bir'i takip etmeyi unutma!", "İLK 11'i takip etmeyi unutma!", cta_at + cta_spans[1][0], cta_at + cta_spans[1][1])]
    T = round(cta_at + len(cta) / SR + 1.2, 2)
    allWT = WT + cta_words

    def find(name, s0, scene_words):
        if isinstance(name, (int, float)):
            return float(name)
        key = norm(str(name))
        for w in scene_words:
            if norm(w[0]).startswith(key):
                return max(0, w[1] - s0)
        for wt in WT:
            for w in wt:
                if norm(w[0]).startswith(key):
                    return max(0, w[1] - s0)
        print("UYARI: 'at' kelimesi bulunamadı:", name)
        return .5

    scenes = []
    sc_list = spec["sahneler"]
    for k, sc in enumerate(sc_list):
        first = min(sc["cumleler"])
        start = 0.0 if k == 0 else max(0.0, spans[first][0] - .3)
        scenes.append({"tip": sc["tip"], "start": round(start, 2), "spec": sc})
    for k in range(len(scenes)):
        scenes[k]["end"] = scenes[k + 1]["start"] if k + 1 < len(scenes) else cta_scene_start
    scenes.append({"tip": "takip", "start": round(cta_scene_start, 2), "end": T, "spec": {}})

    events = []
    secs = ""
    rtak = None
    for k, sc in enumerate(scenes):
        s0 = sc["start"]
        words = [w for i in sc["spec"].get("cumleler", []) for w in WT[i]]
        at = lambda name, s0=s0, words=words: find(name, s0, words)
        sfx = lambda t, kind, s0=s0: events.append((s0 + t, kind))
        if sc["tip"] == "takip":
            rtak = cta_words[1][2][1] - s0
            body = t_takip({}, at, sfx, k, spec.get("soru", ""), rtak)
        else:
            body = TEMPLATES[sc["tip"]](sc["spec"], at, sfx, k)
            if sc["spec"].get("ozel_svg"):
                body += sc["spec"]["ozel_svg"]
        dur = sc["end"] - s0
        secs += (f"<section class='scene' data-start='{s0}' style='z-index:{k + 1}'><svg viewBox='0 0 1080 1920' xmlns='http://www.w3.org/2000/svg'>{DEFS}"
                 f"<g class='kb' style='--t:{dur + .4:.2f}s'>{body}</g><rect width='1080' height='1920' fill='url(#vig)' opacity='.7'/></svg></section>")

    css = open(os.path.join(HERE, "stil.css"), encoding="utf-8").read().replace("FONTDIR", "file://" + os.path.join(HERE, "fonts"))
    js = open(os.path.join(HERE, "oynat.js"), encoding="utf-8").read()
    data = {"scenes": [{"start": s["start"], "end": s["end"]} for s in scenes], "chunks": chunks(allWT, T), "T": T,
            "labelEnd": cta_scene_start}
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{secs}"
            "<div id='label'>İLK 11 · FUTBOL HİKÂYELERİ</div><div id='band'></div><div id='subs'></div>"
            f"<script>window.__DATA={json.dumps(data, ensure_ascii=False)};{js}</script></body></html>")
    hp = os.path.join(out, "_sayfa.html")
    open(hp, "w", encoding="utf-8").write(page)
    print("Süre:", T, "sn | sahneler:", [(s["tip"], s["start"]) for s in scenes])

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--font-render-hinting=none"])
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.abspath(hp))
        pg.wait_for_function("window.__ready===true")
        if preview:
            from PIL import Image
            shots = []
            for k, sc in enumerate(scenes):
                for frac in (.35, .9):
                    t = sc["start"] + (sc["end"] - sc["start"]) * frac
                    pg.evaluate(f"seek({t})")
                    f = os.path.join(out, f"onizleme_{k + 1}_{int(frac * 100)}.png")
                    pg.screenshot(path=f); shots.append(f)
            ims = [Image.open(f).resize((270, 480)) for f in shots]
            cols = 6; rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * 276, rows * 486), "white")
            for i, im in enumerate(ims):
                sheet.paste(im, ((i % cols) * 276, (i // cols) * 486))
            sheet.save(os.path.join(out, "onizleme.png"))
            print("Önizleme:", os.path.join(out, "onizleme.png"))
            br.close()
            return
        vid = os.path.join(out, "_video.mp4")
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
        for fi in range(int(round(T * FPS))):
            pg.evaluate(f"seek({fi / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=94))
        ff.stdin.close(); ff.wait()
        kt = float(spec.get("kapak_sn", 2.5))
        pg.evaluate(f"seek({kt})")
        pg.screenshot(path=os.path.join(out, "kapak.jpg"), type="jpeg", quality=92)
        br.close()
    wav = os.path.join(out, "_mix.wav")
    build_audio(voice, cta, cta_at, T, scenes, events, wav)
    mp4 = os.path.join(out, f"{spec.get('slug', 'hikaye')}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", mp4], check=True)
    print("VIDEO:", mp4, f"({T} sn)")


if __name__ == "__main__":
    main()

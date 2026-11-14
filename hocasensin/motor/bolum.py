#!/usr/bin/env python3
"""Anadoluspor (@hocasensin1) bölüm motoru.

Kullanım:
  python3 bolum.py senaryo.json cikti/                 # tam video (mp4 + kapak.jpg)
  python3 bolum.py senaryo.json cikti/ --onizleme 3.5,12,40   # seçili anların kareleri + onizleme.jpg
  python3 bolum.py senaryo.json --kelimeler            # zaman damgalı kelime listesi (w:N çapaları için)

Senaryo biçimi: hocasensin/MOTOR.md
"""
import json, math, os, re, subprocess, sys, wave
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAR = os.path.join(KOK, "varliklar")
W, H, FPS, SR = 1080, 1920, 30, 48000

RENK = {
    "mor": (98, 44, 150), "koyumor": (46, 18, 78), "sari": (255, 208, 50), "beyaz": (255, 255, 255),
    "siyah": (22, 14, 34), "kirmizi": (226, 48, 60), "yesil": (36, 186, 104), "mavi": (40, 120, 220),
    "turuncu": (255, 140, 30), "gri": (60, 60, 70),
}
PURPLE, PURPLE_D, YELLOW, WHITE, INK, RED, GREEN = (RENK[k] for k in ["mor", "koyumor", "sari", "beyaz", "siyah", "kirmizi", "yesil"])

def rk(v, vars_=None):
    if isinstance(v, (list, tuple)): return tuple(v)
    return RENK.get(v, v) if v is not None else vars_

# ---------------------------------------------------------------- yardımcılar
@lru_cache(None)
def font(name, size):
    path = {"anton": "Anton.ttf", "black": "Rubik-Black.ttf", "xbold": "Rubik-ExtraBold.ttf"}[name]
    return ImageFont.truetype(os.path.join(VAR, "fonts", path), size)

def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()

def ease_out_back(x, s=1.9):
    x = min(max(x, 0.0), 1.0) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def shadowed(img, off=(0, 8), blur=6, alpha=110):
    pad = blur * 3 + max(abs(off[0]), abs(off[1]))
    out = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(img.split()[3].point(lambda v: v * alpha // 255))
    if blur: sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh, (pad + off[0], pad + off[1]))
    out.alpha_composite(img, (pad, pad))
    return out

def text_img(text, fname, size, fill, stroke=0, stroke_fill=INK, shadow=True):
    f = font(fname, size)
    l, t, r, b = f.getbbox(text, stroke_width=stroke)
    img = Image.new("RGBA", (r - l + 4, b - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((2 - l, 2 - t), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return shadowed(img) if shadow else img

def rrect(size, radius, fill, border=0, border_col=INK):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if border:
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=border_col)
        d.rounded_rectangle((border, border, w - 1 - border, h - 1 - border), max(radius - border, 2), fill=fill)
    else:
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=fill)
    return img

def fit_text(text, fname, size, maxw):
    while size > 20 and font(fname, size).getlength(text) > maxw:
        size -= 2
    return size

def pill(text, size=54, fg=YELLOW, bg=PURPLE, fname="black", pad=(36, 20), border=6, tilt=0):
    size = fit_text(text, fname, size, 960 - pad[0] * 2)
    f = font(fname, size)
    l, t, r, b = f.getbbox(text)
    tw, th = r - l, b - t
    w, h = tw + pad[0] * 2 + border * 2, th + pad[1] * 2 + border * 2
    img = rrect((w, h), min(h // 2, 26), bg, border)
    ImageDraw.Draw(img).text(((w - tw) // 2 - l, (h - th) // 2 - t), text, font=f, fill=fg)
    img = shadowed(img)
    return img.rotate(tilt, resample=Image.BICUBIC, expand=True) if tilt else img

def stack(imgs, gap=10):
    w = max(i.width for i in imgs); h = sum(i.height for i in imgs) + gap * (len(imgs) - 1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); y = 0
    for i in imgs:
        out.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height + gap
    return out

def heart(size, col=RED):
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img); r = s * 0.27
    d.ellipse((s * 0.5 - 2 * r, s * 0.18, s * 0.5, s * 0.18 + 2 * r), fill=col)
    d.ellipse((s * 0.5, s * 0.18, s * 0.5 + 2 * r, s * 0.18 + 2 * r), fill=col)
    d.polygon([(s * 0.5 - 2 * r + s * 0.02, s * 0.18 + r * 1.25), (s * 0.5 + 2 * r - s * 0.02, s * 0.18 + r * 1.25), (s * 0.5, s * 0.92)], fill=col)
    return img.resize((size, size), Image.LANCZOS)

# ---------------------------------------------------------------- öğe çizimleri
def crest(size=260):
    s = size * 2
    img = Image.new("RGBA", (s, int(s * 1.18)), (0, 0, 0, 0)); d = ImageDraw.Draw(img); w, h = img.size
    shield = lambda m: [(m, m), (w - m, m), (w - m, h * 0.52), (w / 2, h - m), (m, h * 0.52)]
    d.polygon(shield(0), fill=INK); d.polygon(shield(16), fill=YELLOW); d.polygon(shield(34), fill=PURPLE)
    band = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(band).polygon([(w * 0.62, 34), (w * 0.86, 34), (w * 0.38, h - 34), (w * 0.14, h - 34)], fill=YELLOW)
    mask = Image.new("L", img.size, 0); ImageDraw.Draw(mask).polygon(shield(34), fill=255)
    img.paste(band, (0, 0), Image.composite(band.split()[3], Image.new("L", img.size, 0), mask))
    f = font("anton", int(s * 0.5)); l, t, r, b = f.getbbox("A", stroke_width=14)
    d.text(((w - (r - l)) / 2 - l, h * 0.40 - (b - t) / 2 - t), "A", font=f, fill=WHITE, stroke_width=14, stroke_fill=INK)
    return shadowed(img.resize((size, int(size * 1.18)), Image.LANCZOS))

def name_tag(num, name, sub):
    n = text_img(num, "anton", 74 if len(num) <= 2 else 56, INK, shadow=False)
    nb = rrect((n.width + 40, 150), 18, YELLOW, 6)
    nb.alpha_composite(n, ((nb.width - n.width) // 2, (nb.height - n.height) // 2))
    t1 = text_img(name, "black", fit_text(name, "black", 50, 680), WHITE, shadow=False)
    t2 = text_img(sub, "xbold", fit_text(sub, "xbold", 30, 680), YELLOW, shadow=False)
    bw = max(t1.width, t2.width) + 60
    box = rrect((bw, 150), 18, PURPLE, 6)
    box.alpha_composite(t1, (30, 22)); box.alpha_composite(t2, (30, 22 + t1.height + 8))
    out = Image.new("RGBA", (nb.width + box.width - 6, 150), (0, 0, 0, 0))
    out.alpha_composite(box, (nb.width - 6, 0)); out.alpha_composite(nb, (0, 0))
    return shadowed(out).rotate(2, resample=Image.BICUBIC, expand=True)

def counter_card(title, value, sub, value_col=PURPLE, sub_col=RED):
    w, h = 700, 330
    card = rrect((w, h), 30, WHITE, 7); d = ImageDraw.Draw(card)
    d.rounded_rectangle((7, 7, w - 8, 92), 24, fill=PURPLE); d.rectangle((7, 60, w - 8, 92), fill=PURPLE)
    t = text_img(title, "black", fit_text(title, "black", 44, w - 60), YELLOW, shadow=False)
    card.alpha_composite(t, ((w - t.width) // 2, 50 - t.height // 2))
    amt = text_img(value, "anton", fit_text(value, "anton", 150, w - 60), value_col, shadow=False)
    card.alpha_composite(amt, ((w - amt.width) // 2, 104 + max(0, (150 - amt.height) // 4)))
    if sub:
        f = text_img(sub, "xbold", fit_text(sub, "xbold", 32, w - 50), sub_col, shadow=False)
        card.alpha_composite(f, ((w - f.width) // 2, h - f.height - 24))
    return shadowed(card)

def ledger_card(title, rows, total_label, total_value, note=""):
    """Kasa defteri: başlık, (etiket, tutar, renk) satırları, KALAN satırı, isteğe bağlı not."""
    w = 860; row_h = 76; head_h = 96
    h = head_h + 24 + row_h * len(rows) + 22 + 110 + (60 if note else 0) + 20
    card = rrect((w, h), 30, WHITE, 7); d = ImageDraw.Draw(card)
    d.rounded_rectangle((7, 7, w - 8, head_h), 24, fill=PURPLE); d.rectangle((7, head_h - 30, w - 8, head_h), fill=PURPLE)
    t = text_img(title, "black", fit_text(title, "black", 46, w - 60), YELLOW, shadow=False)
    card.alpha_composite(t, ((w - t.width) // 2, (head_h + 7) // 2 - t.height // 2))
    y = head_h + 24
    for i, (lab, val, col) in enumerate(rows):
        if i % 2 == 0: d.rectangle((14, y, w - 15, y + row_h), fill=(246, 240, 252))
        L = text_img(lab, "xbold", fit_text(lab, "xbold", 40, w - 330), INK, shadow=False)
        V = text_img(val, "anton", fit_text(val, "anton", 54, 290), col, shadow=False)
        card.alpha_composite(L, (36, y + (row_h - L.height) // 2))
        card.alpha_composite(V, (w - 36 - V.width, y + (row_h - V.height) // 2))
        y += row_h
    y += 10; d.line((30, y, w - 30, y), fill=INK, width=5); y += 12
    d.rounded_rectangle((20, y, w - 21, y + 100), 22, fill=YELLOW, outline=INK, width=4)
    L = text_img(total_label, "black", fit_text(total_label, "black", 48, w - 420), INK, shadow=False)
    V = text_img(total_value, "anton", fit_text(total_value, "anton", 78, 380), PURPLE, shadow=False)
    card.alpha_composite(L, (46, y + (100 - L.height) // 2)); card.alpha_composite(V, (w - 46 - V.width, y + (100 - V.height) // 2))
    y += 110
    if note:
        N = text_img(note, "xbold", fit_text(note, "xbold", 32, w - 60), RED, shadow=False)
        card.alpha_composite(N, ((w - N.width) // 2, y + 8))
    return shadowed(card)

@lru_cache(maxsize=256)
def standings_card(title, rows, old_order, hl, pq, badge, sub=""):
    """Puan tablosu. rows: ((takım, O, G, B, M, AV, P), ...) yeni sırada; old_order: eski sıradaki takım adları;
    hl: vurgulanan takım; pq: 0..100 geçiş ilerlemesi (eski sıradan yeni sıraya kayma)."""
    p = ease_out(pq / 100.0)
    w = 960; head = 96; colh = 50; rh = 74; n = len(rows)
    h = head + colh + rh * n + (64 if sub else 24)
    card = rrect((w, h), 30, WHITE, 7); d = ImageDraw.Draw(card)
    d.rounded_rectangle((7, 7, w - 8, head), 24, fill=PURPLE); d.rectangle((7, head - 30, w - 8, head), fill=PURPLE)
    t = text_img(title, "black", fit_text(title, "black", 44, w - 60), YELLOW, shadow=False)
    card.alpha_composite(t, ((w - t.width) // 2, (head + 7) // 2 - t.height // 2))
    xs = [44, 96, 560, 625, 690, 755, 830, 905]   # #, takım, O, G, B, M, AV, P (sütun merkezleri / sol)
    fh = font("xbold", 26)
    for j, lab in enumerate(["#", "TAKIM", "O", "G", "B", "M", "AV", "P"]):
        d.text((xs[j], head + colh // 2 + 4), lab, font=fh, fill=(120, 110, 140), anchor="lm" if j == 1 else "mm")
    top = head + colh
    def ypos(name):
        a = old_order.index(name) if name in old_order else rows.index(next(r for r in rows if r[0] == name))
        b = [r[0] for r in rows].index(name)
        return top + (a + (b - a) * p) * rh
    order = [r for r in rows if r[0] != hl] + [r for r in rows if r[0] == hl]
    for i in range(n):
        if i % 2 == 0: d.rectangle((14, top + i * rh, w - 15, top + (i + 1) * rh), fill=(246, 240, 252))
    for i in range(n):
        d.text((xs[0], top + i * rh + rh // 2), str(i + 1), font=font("anton", 40), fill=INK, anchor="mm")
    for r in order:
        y = ypos(r[0]); is_hl = r[0] == hl
        if is_hl:
            d.rounded_rectangle((70, y + 6, w - 18, y + rh - 6), 18, fill=YELLOW, outline=INK, width=4)
        name_f = font("black" if is_hl else "xbold", fit_text(r[0], "black" if is_hl else "xbold", 38, 420))
        d.text((xs[1], y + rh // 2), r[0], font=name_f, fill=PURPLE if is_hl else INK, anchor="lm")
        for j, v in enumerate(r[1:]):
            col = INK
            if j == 4: col = GREEN if str(v).startswith("+") else (RED if str(v).startswith("-") else INK)
            d.text((xs[j + 2], y + rh // 2), str(v), font=font("anton", 46 if j == 5 else 38), fill=PURPLE if (j == 5 and is_hl) else col, anchor="mm")
    if badge and pq >= 100:
        hy = top + [r[0] for r in rows].index(hl) * rh
        num = text_img(badge.lstrip("▲▼ "), "anton", 36, WHITE, shadow=False)
        bw, bh = num.width + 60, 50
        b = rrect((bw, bh), bh // 2, GREEN, 4); bd = ImageDraw.Draw(b)
        up = not badge.startswith("▼")
        tri = [(14, 35), (36, 35), (25, 14)] if up else [(14, 15), (36, 15), (25, 36)]
        bd.polygon(tri, fill=WHITE)
        b.alpha_composite(num, (44, (bh - num.height) // 2))
        card.alpha_composite(b, (434, int(hy + (rh - bh) / 2)))
    if sub:
        sb = text_img(sub, "xbold", fit_text(sub, "xbold", 30, w - 60), RED, shadow=False)
        card.alpha_composite(sb, ((w - sb.width) // 2, h - 44 - sb.height // 2 + 8))
    return shadowed(card)

@lru_cache(maxsize=128)
def jersey_back(name, number, w=300):
    """Mor-sarı forma sırtı: üstte isim, ortada numara (taraftar adları için)."""
    h = int(w * 1.15); S = 3
    big = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    W_, H_ = w * S, h * S
    body = [(0.22, 0.06), (0.38, 0.0), (0.62, 0.0), (0.78, 0.06), (1.0, 0.24), (0.88, 0.40), (0.80, 0.34),
            (0.80, 1.0), (0.20, 1.0), (0.20, 0.34), (0.12, 0.40), (0.0, 0.24)]
    m = 0.04
    pts = [((m + x * (1 - 2 * m)) * W_, (m + y * (1 - 2 * m)) * H_) for x, y in body]
    d.polygon(pts, fill=PURPLE, outline=INK); d.line(pts + [pts[0]], fill=INK, width=6 * S)
    P = lambda x, y: ((m + x * (1 - 2 * m)) * W_, (m + y * (1 - 2 * m)) * H_)
    d.line([P(0.38, 0.0), P(0.5, 0.05), P(0.62, 0.0)], fill=YELLOW, width=7 * S)
    d.line([P(0.03, 0.27), P(0.13, 0.37)], fill=YELLOW, width=6 * S); d.line([P(0.97, 0.27), P(0.87, 0.37)], fill=YELLOW, width=6 * S)
    big = big.resize((w, h), Image.LANCZOS)
    nm = tr_upper(name.lstrip("@"))
    fs = int(w * 0.11)
    while fs > 11 and font("black", fs).getlength(nm) > w * 0.5: fs -= 1
    t = text_img(nm, "black", fs, YELLOW, shadow=False)
    big.alpha_composite(t, ((w - t.width) // 2, int(h * 0.17)))
    n = text_img(str(number), "anton", int(w * 0.42), YELLOW, shadow=False)
    big.alpha_composite(n, ((w - n.width) // 2, int(h * 0.33)))
    return shadowed(big)

def like_sticker(text, bg=GREEN):
    hrt = heart(64, WHITE)
    t = text_img(text, "black", fit_text(text, "black", 50, 760), WHITE, shadow=False)
    w = hrt.width + t.width + 90
    img = rrect((w, 110), 55, bg, 6)
    img.alpha_composite(hrt, (30, (110 - hrt.height) // 2)); img.alpha_composite(t, (30 + hrt.width + 22, (110 - t.height) // 2))
    return shadowed(img).rotate(-4, resample=Image.BICUBIC, expand=True)

def option_card(letter, name, head, accent):
    w, h = 310, 430
    card = rrect((w, h), 28, WHITE, 7); d = ImageDraw.Draw(card)
    d.rounded_rectangle((7, 7, w - 8, 300), 22, fill=accent)
    hd = head.copy(); hd.thumbnail((w - 40, 280), Image.LANCZOS)
    card.alpha_composite(hd, ((w - hd.width) // 2, 300 - hd.height))
    nm = text_img(name, "black", fit_text(name, "black", 42, w - 30), PURPLE, shadow=False)
    card.alpha_composite(nm, ((w - nm.width) // 2, 300 + (h - 300 - nm.height) // 2))
    b = Image.new("RGBA", (130, 130), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
    bd.ellipse((0, 0, 129, 129), fill=INK); bd.ellipse((7, 7, 122, 122), fill=YELLOW)
    lt = text_img(letter, "anton", fit_text(letter, "anton", 76, 100), INK, shadow=False)
    b.alpha_composite(lt, ((130 - lt.width) // 2, (130 - lt.height) // 2 - 2))
    out = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    out.alpha_composite(card, (40, 40)); out.alpha_composite(b, (0, 0))
    return shadowed(out)

def sign_plate(top, big):
    w, h = 400, 230
    img = Image.new("RGBA", (w, h + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.line((90, 0, 120, 75), fill=INK, width=7); d.line((w - 90, 0, w - 120, 75), fill=INK, width=7)
    plate = rrect((w, h), 18, WHITE, 8, RED)
    t1 = text_img(top, "black", fit_text(top, "black", 46, w - 40), INK, shadow=False)
    t2 = text_img(big, "anton", fit_text(big, "anton", 108, w - 40), RED, shadow=False)
    plate.alpha_composite(t1, ((w - t1.width) // 2, 22)); plate.alpha_composite(t2, ((w - t2.width) // 2, 22 + t1.height + 6))
    img.alpha_composite(plate, (0, 70))
    return shadowed(img).rotate(-5, resample=Image.BICUBIC, expand=True)

def progress_bar(left, right, ratio, here):
    w, h = 940, 190
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.alpha_composite(rrect((w - 80, 44), 22, (255, 255, 255, 230), 6), (40, 70))
    d = ImageDraw.Draw(img)
    fillw = int((w - 92) * max(0, min(1, ratio)))
    if fillw > 20: d.rounded_rectangle((46, 76, 46 + fillw, 108), 16, fill=YELLOW)
    cx = 58 + int((w - 116) * max(0, min(1, ratio)))
    d.ellipse((cx - 36, 56, cx + 36, 128), fill=YELLOW, outline=INK, width=6)
    d.ellipse((w - 94, 56, w - 22, 128), fill=WHITE, outline=INK, width=6)
    l = text_img(left, "black", 34, WHITE, 5); r = text_img(right, "black", 34, YELLOW, 5)
    img.alpha_composite(l, (0, 128)); img.alpha_composite(r, (w - r.width, 128))
    if here:
        hz = text_img(here, "black", 28, INK, shadow=False)
        hp = rrect((hz.width + 30, hz.height + 18), 14, YELLOW, 4); hp.alpha_composite(hz, (15, 9))
        img.alpha_composite(hp, (max(0, min(w - hp.width, cx - hp.width // 2)), 0))
    return img

def stamp(text, col=RED, size=120, tilt=-12):
    size = fit_text(text, "anton", size, 900)
    t = text_img(text, "anton", size, col, shadow=False)
    w, h = t.width + 70, t.height + 50
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), 20, outline=col, width=12)
    img.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2))
    return shadowed(img, alpha=80).rotate(tilt, resample=Image.BICUBIC, expand=True)

def title(text, size=190, fill=YELLOW, stroke=12, stroke_fill=PURPLE_D):
    size = fit_text(text, "anton", size, 980)
    return text_img(text, "anton", size, fill, stroke, stroke_fill)

def bubble(text):
    t = text_img(text, "black", fit_text(text, "black", 44, 820), INK, shadow=False)
    w, h = t.width + 60, t.height + 44
    img = Image.new("RGBA", (w, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=INK); d.rounded_rectangle((6, 6, w - 7, h - 7), 22, fill=WHITE)
    d.polygon([(w * 0.25, h - 8), (w * 0.25 + 50, h - 8), (w * 0.2, h + 36)], fill=INK)
    d.polygon([(w * 0.25 + 9, h - 12), (w * 0.25 + 40, h - 12), (w * 0.2 + 4, h + 22)], fill=WHITE)
    img.alpha_composite(t, (30, 22))
    return shadowed(img)

def banner(text, bg=(255, 250, 235), fg=PURPLE, tilt=-3):
    f = font("black", fit_text(text, "black", 56, 820))
    l, t, r, b = f.getbbox(text)
    w, h = r - l + 90, b - t + 60
    img = Image.new("RGBA", (w, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # hafif sarkık kumaş
    pts = [(0, 10)] + [(x, 10 + 10 * math.sin(math.pi * x / w)) for x in range(0, w + 1, 20)] + [(w, 10), (w, h + 10)] + \
          [(x, h + 10 + 10 * math.sin(math.pi * x / w)) for x in range(w, -1, -20)]
    d.polygon(pts, fill=bg, outline=INK)
    d.line([(0, 10), (0, h + 10)], fill=INK, width=6); d.line([(w - 1, 10), (w - 1, h + 10)], fill=INK, width=6)
    d.text(((w - (r - l)) // 2 - l, 10 + (h - (b - t)) // 2 - t + 4), text, font=f, fill=fg)
    for x in (12, w - 12):
        d.ellipse((x - 9, 1, x + 9, 19), fill=YELLOW, outline=INK, width=3)
    return shadowed(img).rotate(tilt, resample=Image.BICUBIC, expand=True)

@lru_cache(None)
def name_label(name, size, title=""):
    """Küçük isim etiketi (beyaz hap, mor yazı) + isteğe bağlı sarı unvan şeridi."""
    txt = name if name.startswith("@") else "@" + name
    f = font("xbold", size); l, t, r, b = f.getbbox(txt)
    pad = max(4, size // 3); w, h = r - l + pad * 2, b - t + pad * 2 - 2
    bw = max(2, size // 8)
    img = rrect((w, h), h // 2, WHITE, bw, PURPLE)
    ImageDraw.Draw(img).text(((w - (r - l)) // 2 - l, (h - (b - t)) // 2 - t), txt, font=f, fill=PURPLE)
    if title:
        ft = font("black", max(9, int(size * 0.72))); l2, t2, r2, b2 = ft.getbbox(title)
        tw, th = r2 - l2 + pad * 2, b2 - t2 + pad
        tb = rrect((tw, th), th // 2, YELLOW, max(1, bw - 1), INK)
        ImageDraw.Draw(tb).text(((tw - (r2 - l2)) // 2 - l2, (th - (b2 - t2)) // 2 - t2), title, font=ft, fill=INK)
        out = Image.new("RGBA", (max(w, tw), h + th - 2), (0, 0, 0, 0))
        out.alpha_composite(img, ((out.width - w) // 2, 0)); out.alpha_composite(tb, ((out.width - tw) // 2, h - 2))
        img = out
    return shadowed(img, off=(0, 3), blur=2, alpha=120)

@lru_cache(None)
def turk_bayragi(w):
    """Türk bayrağı (Bayrak Kanunu oranları: G yükseklik, 1,5G en; hilal ve yıldız ölçüleri)."""
    G = int(w / 1.5); S = 3
    img = Image.new("RGBA", (w * S, G * S), (227, 10, 23, 255)); d = ImageDraw.Draw(img)
    g = G * S; cy = g / 2
    def circ(cx, r, col): d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    circ(0.5 * g, 0.25 * g, WHITE)            # hilal dış çemberi
    circ(0.5625 * g, 0.2 * g, (227, 10, 23))  # iç çember (1/16 G kaydırılmış)
    sx, R = 0.8208 * g, 0.125 * g             # yıldız çemberi (çap 1/4 G), bir ucu göndere bakar
    r_in = R * 0.381966
    pts = []
    for k in range(10):
        ang = math.pi + k * math.pi / 5
        rr = R if k % 2 == 0 else r_in
        pts.append((sx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=WHITE)
    return img.resize((w, G), Image.LANCZOS)

def wave_flag(base, t, amp=None):
    a = np.asarray(base).astype(np.float32); h, w = a.shape[:2]
    amp = amp if amp is not None else h * 0.045
    xs = np.arange(w); ramp = (xs / w) ** 0.8
    dy = amp * ramp * np.sin(2 * np.pi * (xs / (w * 0.55) - t * 0.9))
    shade = 1 + 0.16 * ramp * np.cos(2 * np.pi * (xs / (w * 0.55) - t * 0.9))
    pad = int(amp) + 4
    out = np.zeros((h + pad * 2, w, 4), np.float32)
    ys = np.arange(h + pad * 2)[:, None] - pad - dy[None, :]
    yi = np.clip(np.round(ys).astype(int), 0, h - 1); valid = (ys >= 0) & (ys <= h - 1)
    out = a[yi, xs[None, :]]
    out[..., :3] *= shade[None, :, None]
    out[..., 3] *= valid
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")

def flag_with_pole(t, w, half_mast=True):
    fl = wave_flag(turk_bayragi(w), t)
    pole_h = int(fl.height * 1.75); pw = max(8, w // 45)
    img = Image.new("RGBA", (w + pw * 3, pole_h + pw * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle((pw, pw * 2, pw * 2, pole_h + pw * 2), fill=(225, 225, 230), outline=INK, width=2)
    d.ellipse((pw * 0.4, 0, pw * 2.6, pw * 2.2), fill=(240, 200, 60), outline=INK, width=2)
    y = int(pole_h * (0.30 if half_mast else 0.06))
    img.alpha_composite(fl, (pw * 2, y))
    return img

LIST_W, LIST_ROW, LIST_VIS = 920, 60, 9

def list_body(names, cols=2):
    names = [n if n.startswith("@") else "@" + n for n in names]
    rows = (len(names) + cols - 1) // cols
    colw = (LIST_W - 60) // cols
    img = Image.new("RGBA", (LIST_W - 28, max(rows, 1) * LIST_ROW + 20), (255, 255, 255, 255)); d = ImageDraw.Draw(img)
    for i, n in enumerate(names):
        r, c = i // cols, i % cols
        size = fit_text(n, "xbold", 38, colw - 30)
        if r % 2 == 0 and c == 0: d.rectangle((0, 10 + r * LIST_ROW, img.width, 10 + (r + 1) * LIST_ROW), fill=(246, 240, 252))
        d.text((24 + c * colw, 10 + r * LIST_ROW + LIST_ROW // 2), n, font=font("xbold", size), fill=PURPLE, anchor="lm")
    return img

def list_frame(title, body, offset, vis_rows=LIST_VIS):
    vis_h = min(body.height, vis_rows * LIST_ROW + 20)
    head_h = 96
    w, h = LIST_W, head_h + vis_h + 14
    card = rrect((w, h), 28, WHITE, 7); d = ImageDraw.Draw(card)
    d.rounded_rectangle((7, 7, w - 8, head_h), 24, fill=PURPLE); d.rectangle((7, head_h - 30, w - 8, head_h), fill=PURPLE)
    t = text_img(title, "black", fit_text(title, "black", 46, w - 60), YELLOW, shadow=False)
    card.alpha_composite(t, ((w - t.width) // 2, (head_h + 7 - t.height) // 2))
    y0 = int(max(0, min(offset, body.height - vis_h)))
    card.alpha_composite(body.crop((0, y0, body.width, y0 + vis_h)), (14, head_h + 2))
    if body.height > vis_h:  # alt kenarda solma
        fade = Image.new("RGBA", (w - 28, 50), (255, 255, 255, 0)); fd = ImageDraw.Draw(fade)
        for i in range(50): fd.line((0, i, w, i), fill=(255, 255, 255, int(255 * i / 50)))
        card.alpha_composite(fade, (14, head_h + vis_h - 48))
    return shadowed(card)

def scoreboard(home, away, hs, as_, minute):
    w, h = 980, 150
    img = rrect((w, h), 26, INK, 0); d = ImageDraw.Draw(img)
    d.rounded_rectangle((6, 6, w - 7, h - 7), 22, fill=(30, 22, 46))
    sw = 220
    d.rounded_rectangle(((w - sw) // 2, 14, (w + sw) // 2, h - 14), 18, fill=YELLOW)
    sc = text_img(f"{hs} - {as_}", "anton", 92, INK, shadow=False)
    img.alpha_composite(sc, ((w - sc.width) // 2, (h - sc.height) // 2))
    for txt, side in ((home, 0), (away, 1)):
        maxw = (w - sw) // 2 - 50
        tt = text_img(txt, "black", fit_text(txt, "black", 44, maxw), WHITE, shadow=False)
        x = (w - sw) // 2 - 25 - tt.width if side == 0 else (w + sw) // 2 + 25
        img.alpha_composite(tt, (x, (h - tt.height) // 2))
    out = Image.new("RGBA", (w, h + 70), (0, 0, 0, 0)); out.alpha_composite(img, (0, 0))
    if minute:
        m = pill(minute, 34, WHITE, RED, pad=(20, 8), border=4)
        out.alpha_composite(m, ((w - m.width) // 2, h - 22))
    return shadowed(out)

# ---------------------------------------------------------------- varlıklar
@lru_cache(None)
def load_bg(name):
    p = name if os.path.isabs(name) else os.path.join(VAR, "arka", name if "." in name else name + ".jpg")
    return Image.open(p).convert("RGB")

@lru_cache(None)
def load_char(name):
    p = name if os.path.isabs(name) else os.path.join(VAR, "karakter", name if "." in name else name + ".png")
    return Image.open(p).convert("RGBA")

@lru_cache(None)
def make_bg(name, blur=0, dark=1.0, tint=None):
    im = load_bg(name)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    if dark != 1.0: im = ImageEnhance.Brightness(im).enhance(dark)
    if tint: im = Image.blend(im, Image.new("RGB", im.size, tuple(tint)), 0.25)
    return im

def head_of(name, frac=0.38):
    im = load_char(name)
    return im.crop((0, 0, im.width, int(im.height * frac)))

def silhouette(im):
    s = Image.new("RGBA", im.size, (18, 10, 30, 255)); s.putalpha(im.split()[3]); return s

@lru_cache(None)
def char_scaled(name, height, flip=False, sil=False):
    im = load_char(name)
    if sil: im = silhouette(im)
    r = height / im.height
    im = im.resize((max(1, int(im.width * r)), height), Image.LANCZOS)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im

# ---------------------------------------------------------------- senaryo
class Bolum:
    def __init__(self, path):
        self.dir = os.path.dirname(os.path.abspath(path))
        self.s = json.load(open(path, encoding="utf-8"))
        wpath = os.path.join(self.dir, self.s.get("kelimeler", "kelimeler.json"))
        raw = json.load(open(wpath, encoding="utf-8"))
        raw = raw["words"] if isinstance(raw, dict) else raw
        self.words = [w for w in raw if w.get("type", "word") == "word" and not w["text"].startswith("[")]
        self.end = float(self.s.get("son", self.words[-1]["end"] + 1.4))
        self._build_subs()
        self._build_scenes()

    def T(self, v):
        """Zaman: sayı (sn) ya da 'w:N', 'w:N+0.2', 'we:N' (N. kelimenin bitişi)."""
        if isinstance(v, (int, float)): return float(v)
        if re.fullmatch(r"-?[\d.]+", str(v).strip()): return float(v)
        m = re.fullmatch(r"(w|we):(\d+)([+-][\d.]+)?", str(v).strip())
        if not m: raise ValueError(f"zaman anlaşılamadı: {v}")
        w = self.words[int(m.group(2))]
        t = w["start"] if m.group(1) == "w" else w["end"]
        return t + float(m.group(3) or 0)

    def _build_subs(self):
        merges = [([x.lower() for x in seq], disp) for seq, disp in self.s.get("birlestir", [])]
        norm = lambda x: x.lower().strip(",.:!?…\"'").replace("...", "")
        words, i = [], 0
        while i < len(self.words):
            hit = None
            for seq, disp in merges:
                if [norm(w["text"]) for w in self.words[i:i + len(seq)]] == seq: hit = (seq, disp); break
            if hit:
                last = self.words[i + len(hit[0]) - 1]
                tail = last["text"][len(last["text"].rstrip(",.:!?…")):]
                words.append({"text": hit[1] + tail, "start": self.words[i]["start"], "end": last["end"]}); i += len(hit[0])
            else:
                words.append(self.words[i]); i += 1
        chunks, cur = [], []
        for w in words:
            txt = w["text"]; clean = txt.rstrip(",.:…").replace("...", "")
            nch = sum(len(x["d"]) for x in cur)
            if cur and (len(cur) >= 3 or nch + len(clean) > 15): chunks.append(cur); cur = []
            cur.append({"d": tr_upper(clean), "s": w["start"], "e": w["end"]})
            if txt.endswith((".", "!", "?", ":", ",")): chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        for k, c in enumerate(chunks):
            nxt = chunks[k + 1][0]["s"] if k + 1 < len(chunks) else None
            ce = c[-1]["e"] + 0.25
            if nxt is not None and nxt - c[-1]["e"] < 0.7: ce = nxt
            c[0]["ce"] = ce
        self.chunks = chunks
        self.sub_y = int(self.s.get("altyazi_y", 1395))

    def _ov_img(self, o):
        tip = o["tip"]
        if tip == "etiket":
            return pill(o["metin"], o.get("boyut", 56), rk(o.get("renk", "sari")), rk(o.get("zemin", "mor")), tilt=o.get("egim", 0))
        if tip == "baslik":
            im = title(o["metin"], o.get("boyut", 190), rk(o.get("renk", "sari")))
            return im.rotate(o["egim"], resample=Image.BICUBIC, expand=True) if o.get("egim") else im
        if tip == "damga":
            return stamp(o["metin"], rk(o.get("renk", "kirmizi")), o.get("boyut", 130), o.get("egim", -12))
        if tip == "isim":
            return name_tag(str(o.get("no", "")), o["ad"], o.get("alt", ""))
        if tip == "seri":
            return stack([pill("ANADOLUSPOR", 60, YELLOW, PURPLE), pill(f"BÖLÜM {o['bolum']}", 40, INK, YELLOW, pad=(26, 12))], gap=-6)
        if tip == "arma":
            return crest(o.get("boyut", 230))
        if tip == "sayac":
            return counter_card(o["baslik"], o["deger"], o.get("alt", ""), rk(o.get("deger_renk", "mor")), rk(o.get("alt_renk", "kirmizi")))
        if tip == "forma":
            return jersey_back(o["isim"], o.get("no", "12"), int(o.get("genislik", 300)))
        if tip == "kasa":
            rows = [(r[0], r[1], rk(r[2]) if len(r) > 2 else (GREEN if str(r[1]).startswith("+") else RED)) for r in o["satirlar"]]
            return ledger_card(o.get("baslik", "KULÜP KASASI"), rows, o.get("kalan_etiket", "KASADA KALAN"), o["kalan"], o.get("not", ""))
        if tip == "begeni":
            return like_sticker(o["metin"], rk(o.get("zemin", "yesil")))
        if tip == "secenek":
            return option_card(o["harf"], o["ad"], head_of(o["karakter"], o.get("oran", 0.38)), rk(o.get("renk", [120, 200, 255])))
        if tip == "tabela":
            return sign_plate(o.get("ust", ""), o["metin"])
        if tip == "ilerleme":
            return progress_bar(o.get("sol", "HALI SAHA"), o.get("sag", "SÜPER LİG"), o.get("oran", 0.0), o.get("isaret", "BURADAYIZ"))
        if tip == "balon":
            return bubble(o["metin"])
        if tip == "yazi":
            fn = o.get("font", "black"); lines = o["metin"].split("\n"); size = o.get("boyut", 54)
            ims = [text_img(L, fn, fit_text(L, fn, size, 980), rk(o.get("renk", "beyaz")), o.get("kontur", 0), shadow=o.get("golge", True)) for L in lines]
            return stack(ims, gap=o.get("aralik", 6))
        if tip == "pankart":
            return banner(o["metin"], rk(o.get("zemin", [255, 250, 235])), rk(o.get("renk", "mor")), o.get("egim", -3))
        if tip == "skor":
            return scoreboard(o["ev"], o["dep"], o.get("ev_skor", 0), o.get("dep_skor", 0), o.get("dakika", ""))
        if tip == "resim":
            p = o["dosya"] if os.path.isabs(o["dosya"]) else os.path.join(self.dir, o["dosya"])
            if not os.path.exists(p): p = os.path.join(VAR, o["dosya"])
            im = Image.open(p).convert("RGBA")
            if o.get("genislik"): im = im.resize((o["genislik"], int(im.height * o["genislik"] / im.width)), Image.LANCZOS)
            return shadowed(im) if o.get("golge", True) else im
        raise ValueError(f"bilinmeyen öğe tipi: {tip}")

    def _build_scenes(self):
        sc = self.s["sahneler"]
        self.scenes = []
        for i, s in enumerate(sc):
            t0 = self.T(s["bas"])
            t1 = self.T(sc[i + 1]["bas"]) if i + 1 < len(sc) else self.end
            bg = make_bg(s["arka"], s.get("bulanik", 0), s.get("karanlik", 1.0), tuple(s["renk"]) if s.get("renk") else None)
            chars = []
            for c in s.get("karakterler", []):
                chars.append(dict(ad=c["ad"], h=int(c.get("h", 980)), x=c.get("x", 540), ayak=c.get("ayak", 1640),
                                  t0=self.T(c.get("bas", t0)), t1=self.T(c["bitis"]) if "bitis" in c else None,
                                  giris=c.get("giris", "up"), sure=c.get("sure", 0.35), ayna=c.get("ayna", False),
                                  golge=c.get("golge", False), kos=c.get("kos", False), faz=c.get("faz", 0),
                                  etiket=c.get("etiket"), etiket_alt=c.get("etiket_alt", ""), etiket_y=c.get("etiket_y", 0.37), etiket_boyut=c.get("etiket_boyut")))
            ovs = []
            for o in s.get("ogeler", []):
                if o["tip"] == "bayrak":
                    w_ = o.get("genislik", 560)
                    ovs.append(dict(img=flag_with_pole(0, w_, o.get("yarim", True)), bayrak=(w_, o.get("yarim", True)),
                                    t0=self.T(o.get("bas", t0)), t1=self.T(o["bitis"]) if "bitis" in o else None,
                                    x=o.get("x", 540), y=o.get("y", 700), anim=o.get("anim", "fade"), sure=o.get("sure", 0.8), rot=0, nabiz=False, titre=False))
                    continue
                if o["tip"] == "puan":
                    pdat = (o.get("baslik", "PUAN TABLOSU"), tuple(tuple(r) for r in o["satirlar"]), tuple(o.get("eski", [r[0] for r in o["satirlar"]])),
                            o.get("vurgu", "ANADOLUSPOR"), o.get("rozet", ""), o.get("alt", ""))
                    t0p = self.T(o.get("bas", t0))
                    ovs.append(dict(img=standings_card(pdat[0], pdat[1], pdat[2], pdat[3], 0, pdat[4], pdat[5]), puan=pdat,
                                    kay=(t0p + float(o.get("gecikme", 0.7)), float(o.get("kayma", 1.1))),
                                    t0=t0p, t1=self.T(o["bitis"]) if "bitis" in o else None,
                                    x=o.get("x", 540), y=o.get("y", 760), anim=o.get("anim", "pop"), sure=o.get("sure", 0.3), rot=0, nabiz=False, titre=False))
                    continue
                if o["tip"] == "liste":
                    body = list_body(o["isimler"], o.get("sutun", 2))
                    ovs.append(dict(img=list_frame(o.get("baslik", "TRİBÜN"), body, 0, o.get("satir", LIST_VIS)), liste=(o.get("baslik", "TRİBÜN"), body, o.get("satir", LIST_VIS)),
                                    t0=self.T(o.get("bas", t0)), t1=self.T(o["bitis"]) if "bitis" in o else None, t_end=t1,
                                    x=o.get("x", 540), y=o.get("y", 640), anim=o.get("anim", "pop"), sure=0.3, rot=0, nabiz=False, titre=False))
                    continue
                ovs.append(dict(img=self._ov_img(o), t0=self.T(o.get("bas", t0)), t1=self.T(o["bitis"]) if "bitis" in o else None,
                                x=o.get("x", 540), y=o.get("y", 320), anim=o.get("anim", "pop"), sure=o.get("sure", 0.3 if o.get("anim", "pop") != "stamp" else 0.2),
                                rot=o.get("dondur", 0), nabiz=o.get("nabiz", False), titre=o.get("titre", False)))
            crowd = build_crowd(s["arka"], s["tribun"]) if s.get("tribun") else []
            dark = [(self.T(a), self.T(b)) for a, b in s.get("isik_kapali", [])]
            z = s.get("zoom", [1.0, 1.08]); m = s.get("merkez", [[0.5, 0.55], [0.5, 0.55]])
            self.scenes.append(dict(t0=t0, t1=t1, bg=bg, z=z, m=m, chars=chars, ovs=ovs, dark=dark, crowd=crowd, sub_y=s.get("altyazi_y")))

    # ------------------------------------------------------------ çizim
    @lru_cache(None)
    def sub_img(self, ci, active):
        c = self.chunks[ci]; size = 116
        f = font("anton", size); sp = f.getlength(" ")
        widths = [f.getlength(w["d"]) for w in c]; total = sum(widths) + sp * (len(c) - 1)
        if total > 990:
            size = int(size * 990 / total); f = font("anton", size); sp = f.getlength(" ")
            widths = [f.getlength(w["d"]) for w in c]; total = sum(widths) + sp * (len(c) - 1)
        hpx = int(size * 1.6)
        img = Image.new("RGBA", (int(total) + 40, hpx), (0, 0, 0, 0)); d = ImageDraw.Draw(img); x = 20
        for j, w in enumerate(c):
            d.text((x, hpx // 2), w["d"], font=f, fill=YELLOW if j == active else WHITE, stroke_width=10, stroke_fill=INK, anchor="lm")
            x += widths[j] + sp
        return shadowed(img, off=(0, 7), blur=5, alpha=150)

    def draw_subs(self, frame, t, y=None):
        if y is False: return
        for ci, c in enumerate(self.chunks):
            if c[0]["s"] <= t < c[0]["ce"]:
                active = max([j for j, w in enumerate(c) if w["s"] <= t] or [0])
                k = min((t - c[0]["s"]) / 0.12, 1.0)
                paste(frame, self.sub_img(ci, active), W // 2, self.sub_y if y is None else int(y), 1.12 - 0.12 * ease_out(k))
                return

    def frame(self, t):
        sc = next((s for s in self.scenes if s["t0"] <= t < s["t1"]), self.scenes[-1])
        lt = t - sc["t0"]; k = min(max(lt / max(sc["t1"] - sc["t0"], 0.01), 0), 1)
        z = sc["z"][0] + (sc["z"][1] - sc["z"][0]) * k
        punch = 1 + 0.07 * (1 - ease_out(lt / 0.25)) if lt < 0.25 else 1.0
        cx = sc["m"][0][0] + (sc["m"][1][0] - sc["m"][0][0]) * k
        cy = sc["m"][0][1] + (sc["m"][1][1] - sc["m"][0][1]) * k
        if sc["crowd"]:
            bgc = sc["bg"].copy().convert("RGBA")
            draw_crowd(bgc, sc["crowd"], t)
            fr = bg_frame(bgc, z * punch, cx, cy)
        else:
            fr = bg_frame(sc["bg"], z * punch, cx, cy)
        labs = [draw_char(fr, c, t) for c in sc["chars"]]
        for lab in labs:  # etiketler tüm figürlerin üstünde (öndeki figür arkadakinin adını örtmesin)
            if lab: safe_comp(fr, *lab)
        for a, b in sc["dark"]:
            if a <= t < b: fr = darken(fr, 0.16)
        for o in sc["ovs"]: draw_ov(fr, o, t)
        self.draw_subs(fr, t, sc.get("sub_y"))
        return fr.convert("RGB")

    # ------------------------------------------------------------ ses
    def sfx_track(self):
        tr = np.zeros(int(SR * self.end) + SR, np.float32); rng = np.random.default_rng(7)
        def add(t, sig, g=1.0):
            i = int(max(t, 0) * SR); j = min(i + len(sig), len(tr)); tr[i:j] += sig[: j - i] * g
        for s in self.scenes[1:]: add(s["t0"] - 0.08, swoosh(rng), 0.35)
        for s in self.scenes:
            for o in s["ovs"]:
                if o["anim"] == "pop": add(o["t0"], pop(), 0.6)
                elif o["anim"] == "stamp": add(o["t0"], thud(rng), 0.7)
            for a, b in s["dark"]: add(a, click(rng), 0.9)
        lib = {"duduk": lambda: whistle(rng, 0.4), "kisa_duduk": lambda: whistle(rng, 0.22), "klik": lambda: click(rng),
               "zil": ring, "uzgun": sad, "pop": pop, "gum": lambda: thud(rng), "kasa": kaching, "tezahurat": lambda: crowd(rng)}
        for e in self.s.get("sesler", []):
            add(self.T(e["t"]), lib[e["tip"]](), e.get("ses", 0.8))
        pk = np.abs(tr).max()
        return tr / max(pk, 1e-6) * 0.6

    def mix(self, outdir):
        sfx = os.path.join(outdir, "sfx.wav"); tr = self.sfx_track()
        with wave.open(sfx, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.stack([tr, tr], 1) * 32767).astype(np.int16).tobytes())
        ses = os.path.join(self.dir, self.s.get("ses", "ses.mp3"))
        muz = self.s.get("muzik", "neseli_1")
        muz = muz if os.path.isabs(muz) else os.path.join(VAR, "muzik", muz if "." in muz else muz + ".mp3")
        vol = self.s.get("muzik_ses", 0.30); D = self.end
        mb = float(self.T(self.s.get("muzik_bas", 0))); ms = int(mb * 1000)
        out = os.path.join(outdir, "mix.m4a")
        fc = (f"[0:a]aresample={SR},aformat=channel_layouts=stereo,apad=whole_dur={D},asplit=2[v1][v2];"
              f"[1:a]aresample={SR},aformat=channel_layouts=stereo,atrim=0:{max(D-mb,1)},volume={vol},afade=t=in:st=0:d={1.2 if mb else 0.01},adelay={ms}|{ms},afade=t=out:st={max(D-1.8,0)}:d=1.8[m];"
              f"[m][v2]sidechaincompress=threshold=0.04:ratio=4:attack=15:release=350[md];"
              f"[v1][md][2:a]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[o]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ses, "-stream_loop", "-1", "-i", muz, "-i", sfx, "-filter_complex", fc,
                        "-map", "[o]", "-ar", str(SR), "-c:a", "aac", "-b:a", "192k", "-t", f"{D}", out], check=True)
        return out

    def render(self, outdir):
        os.makedirs(os.path.join(outdir, "sahneler"), exist_ok=True)
        parts = []
        for i, sc in enumerate(self.scenes):
            n0, n1 = round(sc["t0"] * FPS), round(sc["t1"] * FPS)
            tmp = os.path.join(outdir, "sahneler", f"s{i:02d}.tmp.mp4"); fin = tmp.replace(".tmp", "")
            p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                                  "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
                                 stdin=subprocess.PIPE)
            for n in range(n0, n1): p.stdin.write(self.frame(n / FPS).tobytes())
            p.stdin.close()
            if p.wait() != 0: raise SystemExit(f"sahne {i} kodlanamadı")
            os.replace(tmp, fin); parts.append(fin); print(f"sahne {i}: {n1 - n0} kare", flush=True)
        lst = os.path.join(outdir, "liste.txt")
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        video = os.path.join(outdir, "video.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)
        audio = self.mix(outdir)
        slug = self.s.get("slug", "bolum")
        final = os.path.join(outdir, f"{slug}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c", "copy",
                        "-shortest", "-movflags", "+faststart", final], check=True)
        kt = self.T(self.s.get("kapak", 3.6))
        self.frame(kt).save(os.path.join(outdir, "kapak.jpg"), quality=92)
        print("BİTTİ", final, f"{self.end:.2f} sn")
        return final

    def preview(self, outdir, times):
        os.makedirs(outdir, exist_ok=True); ims = []
        for t in times:
            im = self.frame(t); im.save(os.path.join(outdir, f"kare_{t:05.2f}.jpg"), quality=88); ims.append(im.resize((360, 640)))
        cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 360, rows * 640))
        for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 360, (i // cols) * 640))
        sheet.save(os.path.join(outdir, "onizleme.jpg"), quality=85)
        print("önizleme:", os.path.join(outdir, "onizleme.jpg"))

# ---------------------------------------------------------------- tribün
@lru_cache(None)
def fan_imgs():
    d = os.path.join(VAR, "taraftar")
    return [Image.open(os.path.join(d, f)).convert("RGBA") for f in sorted(os.listdir(d)) if f.endswith(".png")]

@lru_cache(None)
def fan_scaled(i, h, flip):
    im = fan_imgs()[i]; r = h / im.height
    im = im.resize((max(1, int(im.width * r)), h), Image.LANCZOS)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im

def build_crowd(bgname, spec):
    """spec: {"sayi": N, "tohum": 7}. Sıralar varliklar/arka/<arka>.json içindeki "siralar"dan (arka plan piksel koordinatı)."""
    meta = os.path.join(VAR, "arka", bgname + ".json")
    if not os.path.exists(meta): raise SystemExit(f"tribün düzeni yok: {meta}")
    rows = json.load(open(meta))["siralar"]          # arkadan öne: [{"ayak":y,"x0":..,"x1":..,"h":..}]
    names = list(spec.get("isimler", [])); ozel = spec.get("ozel", {})
    n = len(names) + max(0, int(spec.get("sayi", 0))); rng = np.random.default_rng(spec.get("tohum", 7))
    fac = spec.get("aralik", 0.5 if names else 0.38)
    caps = [max(1, int((r["x1"] - r["x0"]) / (r["h"] * fac))) for r in rows]
    order = list(range(len(rows)))[::-1]             # önce ön sıralar dolsun
    fill = {i: 0 for i in order}; left = min(n, sum(caps))
    while left > 0:
        for i in order:
            if left and fill[i] < caps[i]: fill[i] += 1; left -= 1
    nf = len(fan_imgs()); out = []; k = 0
    for i, r in enumerate(rows):                      # arkadan öne çiz
        m = fill[i]
        if not m: continue
        slots = rng.permutation(caps[i])[:m]; slots.sort()
        step = (r["x1"] - r["x0"]) / caps[i]
        for sl in slots:
            x = r["x0"] + step * (sl + 0.5) + rng.uniform(-0.2, 0.2) * step
            h = int(r["h"] * rng.uniform(0.9, 1.08))
            out.append(dict(img=(k + int(rng.integers(0, nf))) % nf, h=h, x=x, y=r["ayak"], flip=bool(rng.integers(0, 2)), ph=float(rng.uniform(0, 1)), sp=float(rng.uniform(1.2, 2.0)), row=i, name=None, zig=0))
            k += 1
    # isimleri önce ön sıralara, soldan sağa ver; komşu etiketler çakışmasın diye zikzak
    order = sorted(range(len(out)), key=lambda j: (-out[j]["row"], out[j]["x"]))
    lsize = spec.get("etiket_boyut", 16)
    for idx, j in enumerate(order[:len(names)]):
        nm = names[idx]; out[j]["name"] = nm; out[j]["title"] = ozel.get(nm.lstrip("@"), "")
    for i in set(f["row"] for f in out):
        rowf = sorted([f for f in out if f["row"] == i], key=lambda f: f["x"])
        for m, f in enumerate(rowf): f["zig"] = m % 2
    for f in out: f["lsize"] = lsize
    return out

def draw_crowd(bg, crowd, t):
    labels = []
    for f in crowd:
        im = fan_scaled(f["img"], f["h"], f["flip"])
        jump = abs(math.sin(math.pi * (t * f["sp"] + f["ph"]))) * f["h"] * 0.06
        x, y = int(f["x"] - im.width / 2), int(f["y"] - im.height - jump)
        x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + im.width, bg.width), min(y + im.height, bg.height)
        if x1 > x0 and y1 > y0:
            bg.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))
        if f.get("name"):
            lab = name_label(f["name"], f["lsize"], f.get("title", ""))
            labels.append((lab, int(f["x"] - lab.width / 2), int(y + im.height * (0.30 + 0.13 * f["zig"]))))
    for lab, lx, ly in labels:
        x0, y0 = max(lx, 0), max(ly, 0); x1, y1 = min(lx + lab.width, bg.width), min(ly + lab.height, bg.height)
        if x1 > x0 and y1 > y0:
            bg.alpha_composite(lab.crop((x0 - lx, y0 - ly, x1 - lx, y1 - ly)), (x0, y0))

# ---------------------------------------------------------------- kompozisyon
def paste(frame, img, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if scale <= 0.01 or alpha <= 0.01: return
    im = img
    if abs(scale - 1) > 0.005: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    safe_comp(frame, im, int(cx - im.width / 2), int(cy - im.height / 2))

def safe_comp(frame, im, x, y):
    x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + im.width, W), min(y + im.height, H)
    if x1 <= x0 or y1 <= y0: return
    frame.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

def bg_frame(bgimg, z, cxf, cyf):
    sw, sh = bgimg.size
    # kapla: arka plan 9:16 değilse ortadan kırp
    tw, th = (sw, sw * 16 / 9) if sw * 16 / 9 <= sh else (sh * 9 / 16, sh)
    cw, ch = tw / z, th / z
    cx = min(max(cxf * sw, cw / 2), sw - cw / 2); cy = min(max(cyf * sh, ch / 2), sh - ch / 2)
    return bgimg.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).convert("RGBA")

def draw_char(frame, c, t):
    if t < c["t0"] or (c["t1"] is not None and t > c["t1"]): return
    im = char_scaled(c["ad"], c["h"], c["ayna"], c["golge"])
    k = (t - c["t0"]) / c["sure"]; x, feet = c["x"], c["ayak"]; sx = 1.0
    g = c["giris"]
    if g == "up": feet += (1 - ease_out_back(k, 1.4)) * 900
    elif g == "right": x += (1 - ease_out(k)) * 900
    elif g == "left": x -= (1 - ease_out(k)) * 900
    elif g == "pop": sx = max(ease_out_back(k, 2.2), 0.01)
    bob = 18 * abs(math.sin(2 * math.pi * t * 2.4)) if c["kos"] else 7 * math.sin(2 * math.pi * (t * 0.8 + c["faz"]))
    br = 1 + 0.012 * math.sin(2 * math.pi * (t * 0.8 + c["faz"]))
    w2, h2 = int(im.width * sx), int(im.height * sx * br)
    if (w2, h2) != im.size: im = im.resize((max(w2, 1), max(h2, 1)), Image.BILINEAR)
    top = int(feet - im.height - bob)
    safe_comp(frame, im, int(x - im.width / 2), top)
    if c.get("etiket") and (c["giris"] != "pop" or k >= 1):
        lab = name_label(c["etiket"], c.get("etiket_boyut") or max(24, int(c["h"] * 0.034)), c.get("etiket_alt", ""))
        lx = min(max(int(x - lab.width / 2), 8), W - 8 - lab.width)  # etiket kadrajdan taşmasın
        return (lab, lx, int(top + im.height * c.get("etiket_y", 0.37)))

def draw_ov(frame, o, t):
    if t < o["t0"] or (o["t1"] is not None and t > o["t1"]): return
    if o.get("bayrak"):
        o = dict(o, img=flag_with_pole(t, *o["bayrak"]))
    if o.get("puan"):
        a, dur = o["kay"]; pq = int(round(min(max((t - a) / dur, 0), 1) * 50)) * 2
        P = o["puan"]; o = dict(o, img=standings_card(P[0], P[1], P[2], P[3], pq, P[4], P[5]))
    if o.get("liste"):
        title, body, vr = o["liste"]
        end = o["t1"] if o["t1"] is not None else o["t_end"]
        vis_h = min(body.height, vr * LIST_ROW + 20)
        p = min(max((t - o["t0"] - 0.8) / max(end - o["t0"] - 1.6, 0.1), 0), 1)
        o = dict(o, img=list_frame(title, body, p * (body.height - vis_h), vr))
    k = (t - o["t0"]) / o["sure"]; sc, al, dy = 1.0, 1.0, 0
    a = o["anim"]
    if a == "pop": sc = max(ease_out_back(k, 2.0), 0.01)
    elif a == "stamp": sc = 1.8 - 0.8 * ease_out(k); al = min(k * 3, 1)
    elif a == "down": dy = -(1 - ease_out(k)) * 260; al = min(k * 2, 1)
    elif a == "fade": al = min(k, 1)
    if o["t1"] is not None:
        fo = (o["t1"] - t) / 0.12
        if fo < 1: al *= max(fo, 0); sc *= 0.9 + 0.1 * max(fo, 0)
    if o["nabiz"]: sc *= 1 + 0.04 * math.sin(2 * math.pi * t * 2)
    if o["titre"] and t - o["t0"] < 0.6: dy += 10 * math.sin((t - o["t0"]) * 70)
    paste(frame, o["img"], o["x"], o["y"] + dy, sc, al, o["rot"])

def darken(frame, amount):
    arr = np.asarray(frame).astype(np.float32); arr[..., :3] *= amount; arr[..., 2] += 18 * (1 - amount)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")

# ---------------------------------------------------------------- efekt sesleri
def _env(n, a=0.005, r=0.08):
    e = np.ones(n, np.float32); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def _tone(f0, f1, dur, sq=False):
    n = int(dur * SR); ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR
    return np.sign(np.sin(ph)) * 0.5 if sq else np.sin(ph)

def whistle(rng, dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(2900 * (1 + 0.035 * np.sign(np.sin(2 * np.pi * 28 * t)))) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * rng.standard_normal(n)
    return (s * _env(n, 0.01, 0.06) * 0.35).astype(np.float32)

def pop():
    return (_tone(380, 1100, 0.07) * _env(int(0.07 * SR), 0.002, 0.04) * 0.45).astype(np.float32)

def thud(rng):
    n = int(0.28 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (95 - 40 * t) * t) * np.exp(-t * 14) + 0.35 * rng.standard_normal(n) * np.exp(-t * 60)
    return (s * 0.8).astype(np.float32)

def click(rng):
    n = int(0.05 * SR); t = np.arange(n) / SR
    return (rng.standard_normal(n) * np.exp(-t * 180) * 0.7 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 120) * 0.5).astype(np.float32)

def swoosh(rng, dur=0.22):
    n = int(dur * SR); x = rng.standard_normal(n); c = np.concatenate([[0], np.cumsum(x)])
    k = np.linspace(40, 4, n).astype(int); idx = np.arange(n); a = np.maximum(0, idx - k)
    out = (c[idx + 1] - c[a]) / (idx + 1 - a)
    return (out * np.sin(np.linspace(0, np.pi, n)) ** 2 * 0.9).astype(np.float32)

def ring():
    n = int(0.32 * SR); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 1300 * t) + np.sin(2 * np.pi * 1650 * t)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * t)))
    one = (s * _env(n, 0.005, 0.03) * 0.16).astype(np.float32)
    return np.concatenate([one, np.zeros(int(0.08 * SR), np.float32), one])

def sad():
    parts = [_tone(f, f, 0.18, True) * _env(int(0.18 * SR), 0.01, 0.05) for f in (392, 370, 349)]
    n = int(0.6 * SR); t = np.arange(n) / SR
    parts.append(np.sign(np.sin(2 * np.pi * np.cumsum(330 + 8 * np.sin(2 * np.pi * 6 * t)) / SR)) * 0.5 * _env(n, 0.01, 0.25))
    return (np.concatenate(parts) * 0.22).astype(np.float32)

def kaching():
    a = _tone(1500, 1500, 0.35) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9)
    b = _tone(2250, 2250, 0.5) * np.exp(-np.arange(int(0.5 * SR)) / SR * 6)
    out = np.zeros(int(0.6 * SR)); out[:len(a)] += a * 0.5; out[int(0.08 * SR):int(0.08 * SR) + len(b)] += b * 0.5
    return out.astype(np.float32)

def crowd(rng, dur=1.6):
    n = int(dur * SR); x = rng.standard_normal(n)
    c = np.concatenate([[0], np.cumsum(x)]); k = 12; y = (c[k:] - c[:-k])[:n] / k
    y = np.pad(y, (0, n - len(y)))
    return (y * np.sin(np.linspace(0, np.pi, n)) * 2.2).astype(np.float32)

# ---------------------------------------------------------------- giriş
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    b = Bolum(sys.argv[1])
    if sys.argv[2] == "--kelimeler":
        for i, w in enumerate(b.words): print(f"{i:3d}  {w['start']:6.2f}-{w['end']:6.2f}  {w['text']}")
        print(f"son: {b.end:.2f}"); sys.exit(0)
    out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 3 and sys.argv[3] == "--onizleme":
        ts = [b.T(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [ (s["t0"] + s["t1"]) / 2 for s in b.scenes ]
        b.preview(out, ts)
    else:
        b.render(out)

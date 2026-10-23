# -*- coding: utf-8 -*-
"""İLK 11 · Maç günü ve son dakika kartları.

Kullanım:  python3 motor/ozel.py girdi.json cikti_klasoru
Çıktı: 01_kart.jpg (derbide 02_kart.jpg da), NN_takip.jpg, hikaye.jpg (1080x1920)
Gönderi = kart(lar) + takip kartı · Hikâye = hikaye.jpg

1) KADRO  (ilk 11 açıklandığında)
{"tip":"kadro","turnuva":"SÜPER LİG · 10. HAFTA","saat":"20:00",
 "ev":"GALATASARAY","dep":"KASIMPAŞA",
 "takimlar":[{"ad":"GALATASARAY","dizilis":"4-2-3-1",
              "oyuncular":["Uğurcan", "Sallai", ...11 ad],
              "teknik_direktor":"Okan Buruk"}]}
 - oyuncular: önce kaleci, sonra her hat SAĞDAN SOLA (sağ bek önce), hatlar geriden ileriye.
 - dizilis kaynaklarda açıkça yoksa YAZMA → kart, diziliş iddia etmeyen liste düzenine geçer.
 - Derbide (iki takım da bizim takımlarımızdansa) takimlar'a iki takım da girer → iki kart.
2) SONUÇ  (maç bitince)
{"tip":"sonuc","turnuva":"UEFA KONFERANS LİGİ · 2. HAFTA","ev":"TRABZONSPOR","dep":"HEARTS","skor":"2-0",
 "goller":[{"dk":"32","ad":"Salah","taraf":"ev","not":"P"}],   # isteğe bağlı; yalnız doğrulanmışsa
 "not":"Trabzonspor iki maçta 6 puana ulaştı.",                 # isteğe bağlı, ≤ 90 karakter
 "sonraki":"5 Kasım · Freiburg (iç saha)", "kaynaklar":["UEFA","AA"]}
3) SON DAKİKA
{"tip":"sondakika","takim":"FENERBAHÇE","baslik":"…","ozet":"…","kaynaklar":["KAP","AA"]}

4) DEMEÇ  (maç öncesi / sonrası röportaj; aynı maça ait demeçler TAM METİN olarak tek gönderide)
{"tip":"demec","baslik":"MAÇ SONU","mac":"BEŞİKTAŞ – CRYSTAL PALACE · AVRUPA LİGİ",
 "sozler":[{"kim":"Ad Soyad","rol":"Teknik direktör","takim":"BEŞİKTAŞ","soz":"Kaynaktaki demecin TAMAMI, birebir. Paragraflar \\n ile ayrılabilir."}],
 "kaynaklar":["AA","beIN Sports"]}
 - baslik: "MAÇ ÖNCESİ" ya da "MAÇ SONU". Söz kaynaktakiyle birebir aynı olur; çıkarılan yer olursa "…" kullanılır, kelime değiştirilmez.
 - Uzunluk sınırı yok: uzun demeç cümle sınırlarından otomatik bölünür ve birkaç karta yayılır (gönderide en fazla 19 kart + takip).
 - Gazeteci sorusu vermek istersen söz metnine "Soru: …" satırı olarak ekleyebilirsin (isteğe bağlı).
 - hikaye.jpg: bütün demeçler tek ekranda, yazı boyu sığacak şekilde otomatik küçülür.

5) PUAN DURUMU  (Avrupa kupaları; her turnuva ayrı kart, bizim takımlar vurgulu)
{"tip":"puan","tablolar":[{"turnuva":"ŞAMPİYONLAR LİGİ","alt":"LİG AŞAMASI · 3. HAFTA SONU",
   "satirlar":[[1,"PSG",9],[2,"Aston Villa",9], ...36 satır: [sıra, takım, puan]]}],
 "bizim":{"Galatasaray":"GALATASARAY","Fenerbahçe":"FENERBAHÇE"},   # tablodaki ad → renk anahtarı
 "kaynaklar":["UEFA","AA"]}
 - Sıra ve puanlar yalnız doğrulanmış tablodan (resmî ya da iki bağımsız kaynakta aynı) yazılır.
 - Hikâye: bütün turnuvalarda bizim takımların sırası ve puanı tek ekranda.

6) FİKSTÜR / KALAN MAÇLAR  (bizim her takım için ayrı kart, rakip logolarıyla)
{"tip":"fikstur","baslik":"KALAN MAÇLAR","alt":"LİG AŞAMASI",
 "takimlar":[{"ad":"GALATASARAY","turnuva":"ŞAMPİYONLAR LİGİ",
   "maclar":[{"hafta":4,"tarih":"2026-11-03","ev":"GALATASARAY","dep":"STUTTGART","saat":"20:45"}, ...]}],   # saat isteğe bağlı
 "renkler":{"STUTTGART":["#E32219","#FFFFFF"]}, "kaynaklar":["beIN Sports","Habertürk"]}
 - Tarih, gün ve iç saha/deplasman yalnız doğrulanmış fikstürden (resmî ya da iki bağımsız kaynakta aynı) yazılır.
 - Gün adı tarihten otomatik hesaplanır. Rakip logosu motor/logolar/<sade-ad>.png (ör. astonvilla.png) varsa kullanılır.
 - Hikâye: bütün takımların kalan maçları tek ekranda (yazı boyu otomatik sığar).

Renkler: ana takımlar için hazır; diğerleri için "renkler":{"KASIMPAŞA":["#1B3A8C","#FFFFFF"]} eklenebilir.
Kulüp logosu kodla ÇİZİLMEZ. motor/logolar/ klasöründe resmî logo dosyası varsa (ör. besiktas.png, galatasaray.png,
fenerbahce.png, trabzonspor.png, turkiye.png; rakipler için ör. crystalpalace.png) renk şeridi yerine o dosya
değiştirilmeden kullanılır; dosya yoksa renk şeridine düşülür.
"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from haber import CSS, esc, top, foot, takip

HERE = os.path.dirname(os.path.abspath(__file__))
RENKLER = {"TÜRKİYE": ("#E30A17", "#FFFFFF"), "BEŞİKTAŞ": ("#111111", "#FFFFFF"),
           "FENERBAHÇE": ("#FFED00", "#0A2D6E"), "GALATASARAY": ("#FDB912", "#A90432"),
           "TRABZONSPOR": ("#7A1E3B", "#6CC4EE")}
VARSAYILAN = ("#2F3B34", "#C9D6CE")

EK_CSS = """
.panel{position:absolute;border-radius:30px;background:rgba(0,0,0,.38);border:2px solid rgba(255,255,255,.08)}
.nm{position:absolute;transform:translateX(-50%);white-space:nowrap;max-width:210px;overflow:hidden;text-overflow:ellipsis;
 padding:5px 14px;border-radius:14px;background:rgba(5,12,8,.82);font:800 27px Inter;color:#fff;text-align:center}
.tok{position:absolute;width:74px;height:74px;border-radius:50%;transform:translate(-50%,-50%);
 display:flex;align-items:center;justify-content:center;font:400 34px Anton;box-shadow:0 8px 18px rgba(0,0,0,.45)}
.chip-red{background:#E30A17;color:#fff}
"""


def renk(ad, d):
    r = (d.get("renkler") or {}).get(ad)
    return tuple(r) if r else RENKLER.get(ad, VARSAYILAN)


LOGO_DIR = os.path.join(HERE, "logolar")


def _sade(ad):
    tr = str.maketrans("ÇĞİIÖŞÜçğıiöşü", "cgiiosucgiiosu")
    return "".join(ch for ch in ad.translate(tr).lower() if ch.isalnum())


_ZEMIN = set()   # açık rengi olmayan (koyu zeminde kaybolan) logolar: arkasına açık daire konur, dosya değişmez


def _koyu_logo(f):
    """Logoda açık renk yoksa (ör. koyu yeşil/kırmızı tek renk arma) True."""
    try:
        from PIL import Image
        im = Image.open(f).convert("RGBA")
        im.thumbnail((120, 120))
        px = [p for p in getattr(im, "get_flattened_data", im.getdata)() if p[3] > 128]
        acik = sum(1 for r, g, b, a in px if .2126 * r + .7152 * g + .0722 * b > 110)
        return bool(px) and acik / len(px) < .05
    except Exception:
        return False


def logo(ad):
    """motor/logolar/<sade-ad>.png|.svg|.webp varsa data URI döndürür (ör. besiktas.png, turkiye.png)."""
    import base64
    for uz, mt in ((".png", "image/png"), (".svg", "image/svg+xml"), (".webp", "image/webp")):
        f = os.path.join(LOGO_DIR, _sade(ad) + uz)
        if os.path.exists(f):
            src = f"data:{mt};base64," + base64.b64encode(open(f, "rb").read()).decode()
            if uz != ".svg" and _koyu_logo(f):
                _ZEMIN.add(src)
            return src
    return None


def _logo_img(src, s):
    if src in _ZEMIN:
        return (f"<span style='display:inline-flex;flex:none;width:{s}px;height:{s}px;align-items:center;justify-content:center;"
                f"border-radius:50%;background:rgba(255,255,255,.93);box-shadow:0 4px 12px rgba(0,0,0,.4)'>"
                f"<img src='{src}' style='width:72%;height:72%;object-fit:contain'></span>")
    return (f"<span style='display:inline-flex;flex:none;width:{s}px;height:{s}px;align-items:center;justify-content:center'>"
            f"<img src='{src}' style='max-width:100%;max-height:100%;object-fit:contain;filter:drop-shadow(0 4px 10px rgba(0,0,0,.45))'></span>")


def serit(ad, d, w=18, h=84):
    src = logo(ad)
    if src:
        return _logo_img(src, h)
    a, b = renk(ad, d)
    return (f"<span style='display:inline-flex;flex:none;width:{w}px;height:{h}px;border-radius:6px;overflow:hidden;"
            f"box-shadow:0 0 0 2px rgba(255,255,255,.25)'><i style='flex:1;background:{a}'></i><i style='flex:1;background:{b}'></i></span>")


def rozet(ad, d, s=150):
    src = logo(ad)
    if src:
        return f"<div style='width:{s}px;height:{s}px;margin:0 auto;display:flex;align-items:center;justify-content:center'>{_logo_img(src, s)}</div>"
    a, b = renk(ad, d)
    return (f"<div style='width:{s}px;height:{s}px;border-radius:50%;margin:0 auto;border:6px solid rgba(255,255,255,.85);"
            f"background:linear-gradient(90deg,{a} 0 50%,{b} 50% 100%);box-shadow:0 14px 30px rgba(0,0,0,.45)'></div>")


def saha_svg(x, y, w, h):
    s = "".join(f"<rect x='0' y='{i * h / 10:.1f}' width='{w}' height='{h / 10:.1f}' fill='{'#2E7D47' if i % 2 else '#2A7341'}'/>" for i in range(10))
    L = "stroke='rgba(255,255,255,.55)' stroke-width='4' fill='none'"
    bw, bh, gw, gh = w * .56, h * .15, w * .26, h * .055
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px;border-radius:26px' width='{w}' height='{h}'>{s}"
            f"<rect x='14' y='14' width='{w - 28}' height='{h - 28}' rx='6' {L}/><line x1='14' y1='{h / 2}' x2='{w - 14}' y2='{h / 2}' {L}/>"
            f"<circle cx='{w / 2}' cy='{h / 2}' r='{h * .1:.0f}' {L}/>"
            f"<rect x='{(w - bw) / 2}' y='{h - 14 - bh}' width='{bw}' height='{bh}' {L}/><rect x='{(w - gw) / 2}' y='{h - 14 - gh}' width='{gw}' height='{gh}' {L}/>"
            f"<rect x='{(w - bw) / 2}' y='14' width='{bw}' height='{bh}' {L}/><rect x='{(w - gw) / 2}' y='14' width='{gw}' height='{gh}' {L}/></svg>")


def kadro_kart(d, t, n, total):
    ad = t["ad"]
    a, b = renk(ad, d)
    oy = t["oyuncular"]
    hat = None
    if t.get("dizilis"):
        try:
            hat = [1] + [int(x) for x in t["dizilis"].split("-")]
            if sum(hat) != len(oy) or len(oy) != 11:
                hat = None
        except ValueError:
            hat = None
    X, Y, W, H = 70, 400, 940, 770
    ust = (f"<div style='position:absolute;left:70px;top:150px'><span class='chip' style='background:#C6FF00;color:#0A0F0A'>İLK 11 BELLİ OLDU</span></div>"
           f"<div style='position:absolute;left:70px;right:70px;top:232px;display:flex;align-items:center;gap:22px'>{serit(ad, d)}"
           f"<h1 style='font-size:88px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(ad)}</h1></div>"
           f"<div style='position:absolute;left:70px;right:70px;top:338px;font:700 31px Inter;color:#B9C7BE;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>"
           f"{esc(d['ev'])} – {esc(d['dep'])} · {esc(d.get('turnuva', ''))}{' · ' + esc(d['saat']) if d.get('saat') else ''}</div>")
    if hat:
        govde = saha_svg(X, Y, W, H)
        nrow = len(hat)
        ybot, ytop = Y + H - 80, Y + 95
        i = 0
        for r, k in enumerate(hat):
            yy = ybot - (ybot - ytop) * r / (nrow - 1)
            for j in range(k):
                xx = X + W - (j + .5) * W / k          # sağdan sola
                nm = oy[i]; i += 1
                govde += (f"<div class='tok' style='left:{xx:.0f}px;top:{yy - 16:.0f}px;background:{a};border:5px solid {b}'></div>"
                          f"<div class='nm' style='left:{xx:.0f}px;top:{yy + 24:.0f}px;max-width:{min(230, W / k - 8):.0f}px'>{esc(nm)}</div>")
        govde += (f"<div style='position:absolute;right:92px;top:{Y + 26}px;padding:6px 16px;border-radius:12px;background:rgba(5,12,8,.8);"
                  f"font:400 34px Anton;color:#C6FF00'>{esc(t['dizilis'])}</div>")
    else:
        rows = "".join(f"<div style='display:flex;align-items:center;gap:16px;padding:14px 20px;border-radius:18px;background:rgba(255,255,255,.05)'>"
                       f"<span style='flex:none;width:52px;height:52px;border-radius:50%;background:{a};border:4px solid {b};display:flex;align-items:center;"
                       f"justify-content:center;font:400 26px Anton;color:{b if a != b else '#000'}'>{k + 1}</span>"
                       f"<span style='font:800 34px Inter;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(nm)}</span></div>"
                       for k, nm in enumerate(oy))
        govde = (f"<div class='panel' style='left:{X}px;top:{Y}px;width:{W}px;height:{H}px;padding:30px;display:grid;"
                 f"grid-template-columns:1fr 1fr;grid-auto-rows:min-content;gap:14px 18px;align-content:center'>{rows}</div>")
    td = (f"<div style='position:absolute;left:70px;top:1196px;font:700 30px Inter;color:#C9D6CE'>Teknik direktör: <b style='color:#fff'>{esc(t['teknik_direktor'])}</b></div>"
          if t.get("teknik_direktor") else "")
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}{ust}{govde}{td}{foot()}</div>")


def sonuc_kart(d, n, total):
    ev, dep = d["ev"], d["dep"]
    gol = {"ev": "", "dep": ""}
    for g in d.get("goller", []):
        gol[g.get("taraf", "ev")] += (f"<div>{esc(str(g['dk']))}' {esc(g['ad'])}{' (' + esc(g['not']) + ')' if g.get('not') else ''}</div>")

    def kol(ad, side):
        return (f"<div style='flex:1;text-align:center'>{rozet(ad, d)}"
                f"<div style='margin-top:26px;font:400 54px/1.05 Anton;letter-spacing:1px'>{esc(ad)}</div>"
                f"<div style='margin-top:18px;font:600 29px/1.5 Inter;color:#C9D6CE'>{gol[side]}</div></div>")
    sk = d["skor"].replace("-", "–")
    alt = ""
    if d.get("not"):
        alt += f"<p style='font:700 38px/1.35 Inter;color:#E6EEE8'>{esc(d['not'])}</p>"
    if d.get("sonraki"):
        alt += f"<p style='margin-top:18px;font:700 32px Inter;color:#9FB3A6'>Sıradaki maç: <span class='hl'>{esc(d['sonraki'])}</span></p>"
    if d.get("kaynaklar"):
        alt += f"<p style='margin-top:18px;font:700 28px Inter;color:#8FA597'>Kaynak: {esc(' · '.join(d['kaynaklar']))}</p>"
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}"
            f"<div style='position:absolute;left:70px;right:70px;top:150px;display:flex;align-items:center;gap:20px;flex-wrap:wrap'>"
            f"<span class='chip' style='background:#C6FF00;color:#0A0F0A'>MAÇ SONUCU</span>"
            f"<span style='font:800 30px Inter;color:#B9C7BE;letter-spacing:1px'>{esc(d.get('turnuva', ''))}</span></div>"
            f"<div style='position:absolute;left:50px;right:50px;top:250px;bottom:180px;display:flex;flex-direction:column;justify-content:center;gap:70px'>"
            f"<div style='display:flex;align-items:flex-start'>"
            f"{kol(ev, 'ev')}<div style='flex:none;width:330px;text-align:center;font:400 190px/1 Anton;margin-top:-6px'>{esc(sk)}</div>{kol(dep, 'dep')}</div>"
            f"<div style='padding:0 20px'>{alt}</div></div>"
            f"{foot()}</div>")


def sondakika_kart(d, n, total):
    ad = d["takim"]
    L = len(d["baslik"])
    fs = 104 if L <= 38 else 92 if L <= 55 else 80 if L <= 75 else 70
    kay = " · ".join(d.get("kaynaklar", []))
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}"
            "<div style='position:absolute;right:60px;top:120px;font:400 520px/1 Anton;color:rgba(227,10,23,.13);transform:rotate(8deg)'>!</div>"
            "<div style='position:absolute;left:70px;right:70px;top:230px;bottom:190px;display:flex;flex-direction:column;justify-content:center;gap:38px'>"
            "<div style='display:flex;align-items:center;gap:22px;flex-wrap:wrap'><span class='chip chip-red'>● SON DAKİKA</span>"
            f"<span style='display:inline-flex;align-items:center;gap:14px;font:400 40px Anton;letter-spacing:1px'>{serit(ad, d, 14, 46)}{esc(ad)}</span></div>"
            f"<h1 style='font-size:{fs}px'>{esc(d['baslik'])}</h1>"
            "<div style='width:120px;height:10px;border-radius:5px;background:#E30A17'></div>"
            f"<p style='font:600 40px/1.38 Inter;color:#DCE6DF'>{esc(d['ozet'])}</p>"
            + (f"<p style='font:700 28px Inter;color:#8FA597;letter-spacing:1px'>Kaynak: {esc(kay)}</p>" if kay else "")
            + f"</div>{foot()}</div>")


MIC = ("<svg width='54' height='54' viewBox='0 0 24 24' fill='none' stroke='#C6FF00' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'>"
       "<rect x='9' y='2' width='6' height='12' rx='3'/><path d='M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8'/></svg>")


PARCA = 360  # bir karttaki en fazla karakter (demeç)


def parcala(metin, sinir=PARCA):
    """Metni cümle/paragraf sınırlarından kelime değiştirmeden parçalara böler."""
    import re
    cumleler = []
    for par in [x.strip() for x in metin.split("\n") if x.strip()]:
        cumleler += [c for c in re.split(r"(?<=[.!?…])\s+", par) if c]
        cumleler.append("\n")
    parcalar, cur = [], ""
    for c in cumleler:
        if c == "\n":
            if cur:
                cur += "\n"
            continue
        while len(c) > sinir:  # tek cümle çok uzunsa kelime sınırından böl
            k = c.rfind(" ", 0, sinir)
            k = k if k > 0 else sinir
            if cur.strip():
                parcalar.append(cur.strip()); cur = ""
            parcalar.append(c[:k].strip()); c = c[k:].strip()
        aday = (cur + ("" if not cur or cur.endswith("\n") else " ") + c)
        if len(aday.strip()) > sinir and cur.strip():
            parcalar.append(cur.strip()); cur = c
        else:
            cur = aday
    if cur.strip():
        parcalar.append(cur.strip())
    return parcalar


def demec_kart(d, s, soz, n, total, devam=False, surer=False):
    L = len(soz)
    fs = 64 if L <= 70 else 56 if L <= 110 else 48 if L <= 160 else 42 if L <= 220 else 38 if L <= 290 else 34
    ad = s.get("takim", "")
    govde = "<br>".join(esc(x) for x in soz.split("\n"))
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}"
            "<div style='position:absolute;right:40px;top:640px;font:400 640px/1 Anton;color:rgba(198,255,0,.09)'>”</div>"
            "<div style='position:absolute;left:70px;right:70px;top:150px;display:flex;align-items:center;gap:20px;flex-wrap:wrap'>"
            f"{MIC}<span class='chip' style='background:#C6FF00;color:#0A0F0A'>{esc(d.get('baslik', 'MAÇ SONU'))}</span>"
            f"<span style='font:800 30px Inter;color:#B9C7BE;letter-spacing:1px'>{esc(d.get('mac', ''))}</span></div>"
            "<div style='position:absolute;left:70px;right:70px;top:260px;bottom:190px;display:flex;flex-direction:column;justify-content:center;gap:44px'>"
            f"<p style='font:800 {fs}px/1.3 Inter;color:#fff;letter-spacing:-.3px'>{'… ' if devam else '“'}{govde}{' …' if surer else '”'}</p>"
            "<div style='display:flex;align-items:center;gap:22px'>"
            + (serit(ad, d, 16, 96) if ad else "") +
            f"<div><div style='font:400 58px/1.05 Anton;letter-spacing:.5px'>{esc(s['kim'])}</div>"
            f"<div style='margin-top:8px;font:700 31px Inter;color:#B9C7BE'>{esc(s.get('rol', ''))}{' · ' + esc(ad) if ad else ''}</div></div></div>"
            + (f"<p style='font:700 28px Inter;color:#8FA597;letter-spacing:1px'>Kaynak: {esc(' · '.join(d['kaynaklar']))}</p>" if d.get("kaynaklar") else "")
            + f"</div>{foot('KAYDIR →')}</div>")


def demec_hikaye(d, out):
    """Bütün demeçleri tek 1080x1920 ekranda veren hikâye (yazı boyu otomatik sığdırılır)."""
    from haber import CSS as _CSS
    bloklar = ""
    for s in d["sozler"]:
        soz = s["soz"].strip().strip('"“”')
        ad = s.get("takim", "")
        govde = "<br>".join(esc(x) for x in soz.split("\n"))
        bloklar += ("<div class='blk'><div style='display:flex;align-items:center;gap:16px;margin-bottom:.5em'>"
                    + (serit(ad, d, 12, 64) if ad else "") +
                    f"<div><div style='font:400 1.45em/1.05 Anton;letter-spacing:.5px'>{esc(s['kim'])}</div>"
                    f"<div style='font:700 .72em Inter;color:#B9C7BE'>{esc(s.get('rol', ''))}{' · ' + esc(ad) if ad else ''}</div></div></div>"
                    f"<p style='font-weight:700;line-height:1.36;color:#fff'>“{govde}”</p></div>")
    kay = (f"<p style='margin-top:.9em;font:700 .66em Inter;color:#8FA597;letter-spacing:1px'>Kaynak: {esc(' · '.join(d['kaynaklar']))}</p>"
           if d.get("kaynaklar") else "")
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{_CSS}"
            ".s{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:Inter,sans-serif;"
            "background:radial-gradient(110% 70% at 50% 40%,#1E5636 0%,#0B2416 55%,#030805 100%)}"
            ".blk+.blk{margin-top:1.1em;padding-top:1.1em;border-top:2px solid rgba(255,255,255,.12)}"
            "</style></head><body><div class='s'><div class='stripes'></div>"
            "<div style='position:absolute;left:70px;right:70px;top:90px;display:flex;align-items:center;gap:18px;flex-wrap:wrap'>"
            f"<div class='brand' style='font:400 46px Anton;display:flex;align-items:center;gap:14px'><div class='logo'>11</div>İLK 11</div>"
            f"{MIC}<span class='chip' style='background:#C6FF00;color:#0A0F0A'>{esc((d.get('baslik') or 'MAÇ SONU') + ' KONUŞTU')}</span></div>"
            f"<div style='position:absolute;left:70px;right:70px;top:250px;font:800 30px Inter;color:#B9C7BE;letter-spacing:1px'>{esc(d.get('mac', ''))}</div>"
            f"<div id='box' style='position:absolute;left:70px;right:70px;top:320px;bottom:250px;overflow:hidden'><div id='txt' style='font-size:46px'>{bloklar}{kay}</div></div>"
            "<div style='position:absolute;left:150px;right:150px;bottom:70px;display:flex;align-items:center;gap:22px;padding:20px 26px;"
            "border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'><div class='logo'>11</div>"
            "<div style='flex:1'><div style='font:400 40px Anton'>İLK 11</div><div style='font:700 26px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
            "<div style='padding:16px 28px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 38px Anton;letter-spacing:2px'>TAKİP ET</div></div>"
            "</div></body></html>")
    p = os.path.abspath(out + ".html")
    open(p, "w", encoding="utf-8").write(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + p)
        pg.evaluate("document.fonts.ready")
        fs = pg.evaluate("""() => {const b=document.getElementById('box'), t=document.getElementById('txt'); let f=46;
            while (t.scrollHeight > b.clientHeight && f > 14) { f -= 1; t.style.fontSize = f + 'px'; } return f; }""")
        sigdi = pg.evaluate("() => document.getElementById('txt').scrollHeight <= document.getElementById('box').clientHeight")
        pg.wait_for_timeout(200)
        pg.query_selector(".s").screenshot(path=out, type="jpeg", quality=92)
        br.close()
    os.remove(p)
    if not sigdi:
        sys.exit("HATA: demeç hikâyeye 14px ile bile sığmadı; hikâyeyi bölmeden paylaşma, durumu bildir.")
    if fs < 22:
        print(f"UYARI: hikâye yazı boyu {fs}px; okunurluğu Read ile kontrol et.", file=sys.stderr)



def puan_kart(d, t, n, total):
    bizim = d.get("bizim", {})
    rows = t["satirlar"]
    yarim = (len(rows) + 1) // 2

    def kol(parca):
        h = ""
        for sira, ad, pu in parca:
            vurgu = ad in bizim
            bg = "background:#C6FF00;color:#0A0F0A" if vurgu else "background:rgba(0,0,0,.30);color:#EAF1EC"
            sr = serit(bizim[ad], d, 8, 30) if vurgu else ""
            h += (f"<div style='display:flex;align-items:center;gap:10px;height:40px;padding:0 14px;border-radius:10px;{bg};"
                  f"font:{'800' if vurgu else '600'} 23px Inter'><span style='width:34px;text-align:right;opacity:.8'>{sira}</span>"
                  f"{sr}<span style='flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(ad)}</span>"
                  f"<span style='font:400 26px Anton;width:34px;text-align:right'>{pu}</span></div>")
        return f"<div style='flex:1;display:flex;flex-direction:column;gap:4px'>{h}</div>"
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}"
            "<div style='position:absolute;left:60px;right:60px;top:150px'>"
            f"<span class='chip' style='background:#C6FF00;color:#0A0F0A'>PUAN DURUMU</span>"
            f"<div style='margin-top:18px;font:400 60px/1 Anton;letter-spacing:1px'>{esc(t['turnuva'])}</div>"
            f"<div style='margin-top:8px;font:800 26px Inter;color:#B9C7BE;letter-spacing:2px'>{esc(t.get('alt', ''))}</div>"
            f"<div style='margin-top:22px;display:flex;gap:16px'>{kol(rows[:yarim])}{kol(rows[yarim:])}</div>"
            + (f"<p style='margin-top:16px;font:700 22px Inter;color:#8FA597;letter-spacing:1px'>Kaynak: {esc(' · '.join(t.get('kaynaklar') or d.get('kaynaklar', [])))}</p>")
            + f"</div>{foot('KAYDIR →')}</div>")


def puan_hikaye(d, out):
    from haber import CSS as _CSS
    bizim = d.get("bizim", {})
    bl = ""
    for t in d["tablolar"]:
        n = len(t["satirlar"])
        for sira, ad, pu in t["satirlar"]:
            if ad in bizim:
                bl += ("<div style='display:flex;align-items:center;gap:24px;padding:26px 30px;border-radius:28px;background:rgba(0,0,0,.38);"
                       "border:2px solid rgba(255,255,255,.1)'>" + serit(bizim[ad], d, 16, 110) +
                       f"<div style='flex:1'><div style='font:400 58px/1 Anton'>{esc(bizim[ad])}</div>"
                       f"<div style='margin-top:8px;font:800 28px Inter;color:#B9C7BE'>{esc(t['turnuva'])}</div></div>"
                       f"<div style='text-align:right'><div style='font:400 74px/1 Anton;color:#C6FF00'>{sira}.</div>"
                       f"<div style='font:800 30px Inter'>{pu} puan</div></div></div>")
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{_CSS}"
            ".s{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:Inter,sans-serif;"
            "background:radial-gradient(110% 70% at 50% 40%,#1E5636 0%,#0B2416 55%,#030805 100%)}</style></head><body><div class='s'><div class='stripes'></div>"
            "<div style='position:absolute;left:0;right:0;top:110px;display:flex;flex-direction:column;align-items:center;gap:24px'>"
            "<div class='brand' style='font:400 50px Anton;display:flex;align-items:center;gap:16px'><div class='logo'>11</div>İLK 11</div>"
            "<span class='chip' style='background:#C6FF00;color:#0A0F0A;font-size:46px'>AVRUPA'DA PUAN DURUMU</span></div>"
            f"<div style='position:absolute;left:80px;right:80px;top:400px;display:flex;flex-direction:column;gap:26px'>{bl}</div>"
            "<div style='position:absolute;left:0;right:0;bottom:250px;text-align:center;font:700 38px Inter;color:#DCE6DF'>Tüm tablolar profilde</div>"
            "<div style='position:absolute;left:150px;right:150px;bottom:70px;display:flex;align-items:center;gap:22px;padding:20px 26px;"
            "border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'><div class='logo'>11</div>"
            "<div style='flex:1'><div style='font:400 40px Anton'>İLK 11</div><div style='font:700 26px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
            "<div style='padding:16px 28px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 38px Anton;letter-spacing:2px'>TAKİP ET</div></div>"
            "</div></body></html>")
    p = os.path.abspath(out + ".html")
    open(p, "w", encoding="utf-8").write(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + p)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(200)
        pg.query_selector(".s").screenshot(path=out, type="jpeg", quality=92)
        br.close()
    os.remove(p)


AY_KISA = ["OCA", "ŞUB", "MAR", "NİS", "MAY", "HAZ", "TEM", "AĞU", "EYL", "EKİ", "KAS", "ARA"]
GUN_ADI = ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]


def _tarih(t):
    import datetime
    g = datetime.date.fromisoformat(t)
    return g.day, AY_KISA[g.month - 1], GUN_ADI[g.weekday()]


def _rakip(t, m):
    biz = t["ad"]
    if m["ev"] == biz:
        return m["dep"], True
    if m["dep"] == biz:
        return m["ev"], False
    sys.exit(f"HATA: {biz} maçında takım adı ev/dep ile eşleşmiyor: {m['ev']} – {m['dep']}")


def fikstur_kart(d, t, n, total):
    ad = t["ad"]
    ms = t["maclar"]
    k = len(ms)
    alan = 760
    gap = 14 if k <= 6 else 8
    rh = min(140, (alan - gap * (k - 1)) / max(k, 1))
    sc = rh / 140
    rows = ""
    for m in ms:
        rak, ic = _rakip(t, m)
        gun, ay, gad = _tarih(m["tarih"])
        alt = gad + (f" · {m['saat']}" if m.get("saat") else "") + (f" · {m['hafta']}. HAFTA" if m.get("hafta") else "")
        etiket = ("<span style='flex:none;padding:10px 18px;border-radius:30px;background:#C6FF00;color:#0A0F0A;font:400 {f}px Anton;letter-spacing:2px'>İÇ SAHA</span>"
                  if ic else
                  "<span style='flex:none;padding:8px 16px;border-radius:30px;border:3px solid rgba(255,255,255,.75);color:#fff;font:400 {f}px Anton;letter-spacing:2px'>DEPLASMAN</span>"
                  ).format(f=int(28 * sc + 2))
        rows += (f"<div style='height:{rh:.0f}px;display:flex;align-items:center;gap:{int(24 * sc)}px;padding:0 28px;border-radius:24px;"
                 f"background:rgba(0,0,0,.34);border:2px solid rgba(255,255,255,.07)'>"
                 f"<div style='flex:none;width:{int(112 * sc + 8)}px;text-align:center'>"
                 f"<div style='font:400 {int(66 * sc)}px/1 Anton;color:#C6FF00'>{gun}</div>"
                 f"<div style='margin-top:4px;font:800 {int(24 * sc + 2)}px Inter;letter-spacing:3px;color:#DCE6DF'>{ay}</div></div>"
                 f"<div style='flex:none;width:2px;align-self:stretch;margin:{int(24 * sc)}px 0;background:rgba(255,255,255,.14)'></div>"
                 f"{serit(rak, d, int(16 * sc + 2), int(84 * sc))}"
                 f"<div style='flex:1;min-width:0'>"
                 f"<div style='font:400 {int(50 * sc)}px/1.05 Anton;letter-spacing:.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(rak)}</div>"
                 f"<div style='margin-top:6px;font:700 {int(24 * sc + 2)}px Inter;color:#9FB3A6;letter-spacing:1px'>{esc(alt)}</div></div>"
                 f"{etiket}</div>")
    kay = t.get("kaynaklar") or d.get("kaynaklar")
    alt_satir = " · ".join(x for x in [t.get("turnuva", ""), d.get("alt", ""), f"{k} MAÇ KALDI"] if x)
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}"
            f"<div style='position:absolute;left:70px;top:150px'><span class='chip' style='background:#C6FF00;color:#0A0F0A'>{esc(d.get('baslik', 'KALAN MAÇLAR'))}</span></div>"
            f"<div style='position:absolute;left:70px;right:70px;top:236px;display:flex;align-items:center;gap:24px'>{serit(ad, d, 18, 92)}"
            f"<h1 style='font-size:88px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(ad)}</h1></div>"
            f"<div style='position:absolute;left:70px;right:70px;top:344px;font:800 28px Inter;color:#B9C7BE;letter-spacing:2px;white-space:nowrap'>{esc(alt_satir)}</div>"
            f"<div style='position:absolute;left:60px;right:60px;top:404px;display:flex;flex-direction:column;gap:{gap}px'>{rows}</div>"
            + (f"<div style='position:absolute;left:70px;right:70px;top:1180px;font:700 24px Inter;color:#8FA597;letter-spacing:1px'>Kaynak: {esc(' · '.join(kay))}</div>" if kay else "")
            + f"{foot('KAYDIR →')}</div>")


def fikstur_hikaye(d, out):
    """Bütün takımların kalan maçları tek 1080x1920 ekranda; sığan en büyük yazı boyu seçilir."""
    from haber import CSS as _CSS

    def sayfa(fs):
        lg, hl = round(fs * 1.15), round(fs * 1.75)       # satır logosu / takım logosu (px)
        bl = ""
        for t in d["takimlar"]:
            satir = ""
            for m in t["maclar"]:
                rak, ic = _rakip(t, m)
                gun, ay, gad = _tarih(m["tarih"])
                satir += ("<div style='display:flex;align-items:center;gap:.5em;padding:.2em 0;border-top:1px solid rgba(255,255,255,.09)'>"
                          f"<span style='flex:none;width:4.2em;font:400 1em/1.1 Anton;color:#C6FF00;letter-spacing:.5px'>{gun} {ay}</span>"
                          f"<span style='flex:none;width:7.4em;font:700 .6em Inter;color:#9FB3A6;letter-spacing:1px'>{gad}</span>"
                          f"{serit(rak, d, max(6, round(fs * .26)), lg)}"
                          f"<span style='flex:1;min-width:0;font:400 1em/1.1 Anton;letter-spacing:.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(rak)}</span>"
                          f"<span style='flex:none;font:400 .68em Anton;letter-spacing:1px;color:{'#C6FF00' if ic else '#DCE6DF'}'>{'İÇ SAHA' if ic else 'DEPLASMAN'}</span></div>")
            bl += ("<div class='blk'><div style='display:flex;align-items:center;gap:.5em;margin-bottom:.25em'>"
                   f"{serit(t['ad'], d, max(8, round(fs * .34)), hl)}<div style='flex:1'><div style='font:400 1.35em/1 Anton;letter-spacing:.5px'>{esc(t['ad'])}</div>"
                   f"<div style='margin-top:.15em;font:800 .58em Inter;color:#B9C7BE;letter-spacing:2px'>{esc(t.get('turnuva', ''))}</div></div></div>{satir}</div>")
        return (f"<!doctype html><html><head><meta charset='utf-8'><style>{_CSS}"
                ".s{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:Inter,sans-serif;"
                "background:radial-gradient(110% 70% at 50% 40%,#1E5636 0%,#0B2416 55%,#030805 100%)}"
                ".blk{padding:.45em .8em;border-radius:24px;background:rgba(0,0,0,.34);border:2px solid rgba(255,255,255,.08)}.blk+.blk{margin-top:.45em}"
                "</style></head><body><div class='s'><div class='stripes'></div>"
                "<div style='position:absolute;left:0;right:0;top:80px;display:flex;flex-direction:column;align-items:center;gap:20px'>"
                "<div class='brand' style='font:400 50px Anton;display:flex;align-items:center;gap:16px'><div class='logo'>11</div>İLK 11</div>"
                f"<span class='chip' style='background:#C6FF00;color:#0A0F0A;font-size:44px'>{esc(d.get('hikaye_baslik', 'KALAN MAÇLAR'))}</span></div>"
                "<div id='box' style='position:absolute;left:60px;right:60px;top:285px;bottom:245px;overflow:hidden;display:flex;flex-direction:column;justify-content:center'>"
                f"<div id='txt' style='font-size:{fs}px'>{bl}</div></div>"
                "<div style='position:absolute;left:150px;right:150px;bottom:60px;display:flex;align-items:center;gap:22px;padding:20px 26px;"
                "border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'><div class='logo'>11</div>"
                "<div style='flex:1'><div style='font:400 40px Anton'>İLK 11</div><div style='font:700 26px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
                "<div style='padding:16px 28px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 38px Anton;letter-spacing:2px'>TAKİP ET</div></div>"
                "</div></body></html>")

    from playwright.sync_api import sync_playwright
    p = os.path.abspath(out + ".html")
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for fs in range(40, 15, -1):
            open(p, "w", encoding="utf-8").write(sayfa(fs))
            pg.goto("file://" + p)
            pg.evaluate("document.fonts.ready")
            if pg.evaluate("() => document.getElementById('txt').scrollHeight <= document.getElementById('box').clientHeight"):
                break
        else:
            br.close(); os.remove(p)
            sys.exit("HATA: fikstür hikâyeye sığmadı; takımları ayrı hikâyelere böl.")
        pg.wait_for_timeout(200)
        pg.query_selector(".s").screenshot(path=out, type="jpeg", quality=92)
        br.close()
    os.remove(p)
    if fs < 24:
        print(f"UYARI: hikâye yazı boyu {fs}px; okunurluğu Read ile kontrol et.", file=sys.stderr)


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2] if len(sys.argv) > 2 else "ozel_cikti"
    os.makedirs(out, exist_ok=True)
    tip = d["tip"]
    if tip == "kadro":
        total = len(d["takimlar"]) + 1
        slides = [kadro_kart(d, t, i + 1, total) for i, t in enumerate(d["takimlar"])]
        ust = "İLK 11 BELLİ OLDU"
    elif tip == "sonuc":
        total = 2
        slides = [sonuc_kart(d, 1, total)]
        ust = "MAÇ SONUCU"
    elif tip == "sondakika":
        total = 2
        slides = [sondakika_kart(d, 1, total)]
        ust = "SON DAKİKA"
    elif tip == "demec":
        isler = []
        for s in d["sozler"]:
            pp = parcala(s["soz"].strip().strip('"“”'))
            for j, parca in enumerate(pp):
                isler.append((s, parca, j > 0, j < len(pp) - 1))
        if len(isler) > 19:
            sys.exit(f"HATA: {len(isler)} kart çıktı; Instagram en fazla 20 görsel alır. Demeçleri iki gönderiye ayır.")
        total = len(isler) + 1
        slides = [demec_kart(d, s, parca, i + 1, total, dv, sr) for i, (s, parca, dv, sr) in enumerate(isler)]
        ust = (d.get("baslik") or "MAÇ SONU") + " KONUŞTU"
    elif tip == "puan":
        total = len(d["tablolar"]) + 1
        slides = [puan_kart(d, t, i + 1, total) for i, t in enumerate(d["tablolar"])]
        ust = "PUAN DURUMU"
    elif tip == "fikstur":
        total = len(d["takimlar"]) + 1
        slides = [fikstur_kart(d, t, i + 1, total) for i, t in enumerate(d["takimlar"])]
        ust = d.get("baslik", "KALAN MAÇLAR")
    else:
        sys.exit("bilinmeyen tip: " + tip)
    slides.append(takip(total))
    names = [f"{i + 1:02d}_kart" for i in range(total - 1)] + [f"{total:02d}_takip"]
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EK_CSS}</style></head><body>{''.join(slides)}</body></html>"
    p = os.path.abspath(os.path.join(out, "_ozel.html"))
    open(p, "w", encoding="utf-8").write(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto("file://" + p)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        for el, nm in zip(pg.query_selector_all(".slide"), names):
            el.screenshot(path=os.path.join(out, nm + ".jpg"), type="jpeg", quality=92)
        br.close()
    os.remove(p)
    if tip == "demec":
        demec_hikaye(d, os.path.join(out, "hikaye.jpg"))
    elif tip == "puan":
        puan_hikaye(d, os.path.join(out, "hikaye.jpg"))
    elif tip == "fikstur":
        fikstur_hikaye(d, os.path.join(out, "hikaye.jpg"))
    else:
        subprocess.run([sys.executable, os.path.join(HERE, "story.py"), os.path.join(out, "01_kart.jpg"),
                        os.path.join(out, "hikaye.jpg"), ust, "Detaylar profilde"], check=True, stdout=subprocess.DEVNULL)
    print("\n".join(os.path.join(out, nm + ".jpg") for nm in names + ["hikaye"]))


if __name__ == "__main__":
    main()

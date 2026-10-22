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

Renkler: ana takımlar için hazır; diğerleri için "renkler":{"KASIMPAŞA":["#1B3A8C","#FFFFFF"]} eklenebilir.
Kulüp logosu ASLA çizilmez; takımlar renk şeritleriyle temsil edilir.
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


def serit(ad, d, w=18, h=84):
    a, b = renk(ad, d)
    return (f"<span style='display:inline-flex;flex:none;width:{w}px;height:{h}px;border-radius:6px;overflow:hidden;"
            f"box-shadow:0 0 0 2px rgba(255,255,255,.25)'><i style='flex:1;background:{a}'></i><i style='flex:1;background:{b}'></i></span>")


def rozet(ad, d, s=150):
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
    subprocess.run([sys.executable, os.path.join(HERE, "story.py"), os.path.join(out, "01_kart.jpg"),
                    os.path.join(out, "hikaye.jpg"), ust, "Detaylar profilde"], check=True, stdout=subprocess.DEVNULL)
    print("\n".join(os.path.join(out, nm + ".jpg") for nm in names + ["hikaye"]))


if __name__ == "__main__":
    main()

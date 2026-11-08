# -*- coding: utf-8 -*-
"""İLK 11 · İki takımın ilk 11'i TEK kartta yan yana (sayfa sahibinin isteği, 2026-11-08).

Kullanım:  python3 motor/yanyana.py kadro.json cikti_klasoru
Girdi: ozel.py'deki KADRO biçimi; takimlar'da iki takım olur (sol = ev sahibi, sağ = deplasman sırasıyla verilir).
Çıktı: 01_kart.jpg (1080x1350, gönderi) ve hikaye.jpg (1080x1920, hikâye).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from haber import CSS, esc, top, foot
from ozel import renk, logo, _logo_img, EK_CSS


def _yazi_rengi(a):
    a = a.lstrip("#")
    r, g, b = (int(a[i:i + 2], 16) for i in (0, 2, 4))
    return "#0A0F0A" if .2126 * r + .7152 * g + .0722 * b > 150 else "#FFFFFF"


def _kolon(d, t, x, y, w, h, s):
    """s: ölçek (gönderi 1.0, hikâye daha büyük)."""
    ad = t["ad"]
    a, b = renk(ad, d)
    yc = _yazi_rengi(a)
    src = logo(ad)
    lg = _logo_img(src, int(92 * s)) if src else (
        f"<span style='display:inline-block;width:{int(22 * s)}px;height:{int(92 * s)}px;border-radius:6px;"
        f"background:linear-gradient(90deg,{a} 0 50%,{b} 50%)'></span>")
    rh, gap = int(56 * s), int(8 * s)
    rows = "".join(
        f"<div style='display:flex;align-items:center;gap:{int(14 * s)}px;height:{rh}px;padding:0 {int(14 * s)}px;"
        f"border-radius:{int(14 * s)}px;background:rgba(255,255,255,.06)'>"
        f"<span style='flex:none;width:{int(42 * s)}px;height:{int(42 * s)}px;border-radius:50%;background:{a};"
        f"border:{max(3, int(3 * s))}px solid {b if b.upper() != a.upper() else '#fff'};display:flex;align-items:center;justify-content:center;"
        f"font:400 {int(22 * s)}px Anton;color:{yc}'>{k + 1}</span>"
        f"<span style='font:800 {int(30 * s)}px Inter;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(nm)}</span></div>"
        for k, nm in enumerate(t["oyuncular"]))
    td = (f"<div style='margin-top:{int(16 * s)}px;font:700 {int(23 * s)}px/1.25 Inter;color:#C9D6CE'>Teknik direktör<br>"
          f"<b style='color:#fff;font-size:{int(26 * s)}px'>{esc(t.get('teknik_direktor', ''))}</b></div>") if t.get("teknik_direktor") else ""
    return (f"<div class='panel' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;padding:{int(22 * s)}px;"
            f"border-top:{int(8 * s)}px solid {a}'>"
            f"<div style='display:flex;align-items:center;gap:{int(14 * s)}px;height:{int(100 * s)}px'>{lg}"
            f"<h1 style='font-size:{int(52 * s)}px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{esc(ad)}</h1></div>"
            f"<div style='display:flex;flex-direction:column;gap:{gap}px;margin-top:{int(12 * s)}px'>{rows}</div>{td}</div>")


def kart(d, W, H, hikaye=False):
    t1, t2 = d["takimlar"][:2]
    alt = f"{esc(d.get('turnuva', ''))}{' · ' + esc(d['saat']) if d.get('saat') else ''}"
    if not hikaye:
        s, py, ph = 1.0, 290, 960
        bas = (f"<div style='position:absolute;left:0;right:0;top:150px;text-align:center'>"
               f"<span class='chip' style='background:#C6FF00;color:#0A0F0A'>İLK 11 BELLİ OLDU</span></div>"
               f"<div style='position:absolute;left:0;right:0;top:232px;text-align:center;font:700 31px Inter;color:#B9C7BE'>{alt}</div>")
        son = foot("@ilk.onbir11'i takip et")
        ust = top(1, 2)
    else:
        s, py, ph = 1.18, 400, 1170
        ust = ("<div style='position:absolute;left:0;right:0;top:110px;display:flex;justify-content:center'>"
               "<div class='brand'><div class='logo'>11</div>İLK 11</div></div>")
        bas = (f"<div style='position:absolute;left:0;right:0;top:205px;text-align:center'>"
               f"<span class='chip' style='background:#C6FF00;color:#0A0F0A;font-size:48px;padding:14px 34px'>İLK 11 BELLİ OLDU</span></div>"
               f"<div style='position:absolute;left:0;right:0;top:318px;text-align:center;font:700 36px Inter;color:#B9C7BE'>{alt}</div>")
        son = ("<div style='position:absolute;left:110px;right:110px;top:1660px;display:flex;align-items:center;gap:24px;padding:22px 28px;"
               "border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'>"
               "<div class='logo' style='width:90px;height:90px;font-size:48px'>11</div>"
               "<div style='flex:1'><div style='font:400 44px Anton'>İLK 11</div><div style='font:700 28px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
               "<div style='padding:18px 30px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 42px Anton;letter-spacing:2px'>TAKİP ET</div></div>")
    gx, cw = 50, (W - 2 * 50 - 24) // 2
    kol = _kolon(d, t1, gx, py, cw, ph, s) + _kolon(d, t2, gx + cw + 24, py, cw, ph, s)
    vs = (f"<div style='position:absolute;left:{W // 2 - 34}px;top:{py + int(36 * s)}px;width:68px;height:68px;border-radius:50%;"
          f"background:#0B0F0C;border:4px solid #C6FF00;display:flex;align-items:center;justify-content:center;"
          f"font:400 30px Anton;color:#C6FF00;z-index:2'>VS</div>")
    return (f"<div class='s slide' style='width:{W}px;height:{H}px'><div class='stripes'></div>{ust}{bas}{kol}{vs}{son}</div>")


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for nm, (W, H, hk) in {"01_kart.jpg": (1080, 1350, False), "hikaye.jpg": (1080, 1920, True)}.items():
            page = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EK_CSS}</style></head><body>{kart(d, W, H, hk)}</body></html>"
            p = os.path.abspath(os.path.join(out, "_yy.html"))
            open(p, "w", encoding="utf-8").write(page)
            pg = br.new_page(viewport={"width": W, "height": H})
            pg.goto("file://" + p)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.query_selector(".s").screenshot(path=os.path.join(out, nm), type="jpeg", quality=92)
            pg.close()
            os.remove(p)
            print(os.path.join(out, nm))
        br.close()


if __name__ == "__main__":
    main()

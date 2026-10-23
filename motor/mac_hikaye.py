# -*- coding: utf-8 -*-
"""İLK 11 · Maç hikâyeleri (Instagram hikâyesi, 1080x1920): skor, puan durumu ve maçtaki olaylar.

Kullanım:  python3 motor/mac_hikaye.py mac.json cikti_klasoru
Görev talimatı: motor/gorevler/mac_hikaye.md

mac.json:
{"bicim": "ayri",                      # "ayri" (varsayılan): skor, puan ve her olay ayrı hikâye · "tek": hepsi tek hikâyede
 "turnuva": "TRENDYOL SÜPER LİG · 9. HAFTA", "ev": "ALANYASPOR", "dep": "KOCAELİSPOR", "skor": "1-2",
 "ilk_yari": "0-2",                    # isteğe bağlı
 "renkler": {"ALANYASPOR": ["#F47C20", "#00843D"]},   # logo yoksa renk şeridi/rozeti için
 "goller": [{"dk": "27", "ad": "Berkan Kutlu", "taraf": "dep", "not": "P"}],   # not: P (penaltı) / KK (kendi kalesine)
 "kartlar": [{"dk": "61", "ad": "Ad Soyad", "taraf": "ev"}],                   # isteğe bağlı: kırmızı kartlar
 "puan_alt": "9. HAFTA AÇILIŞI SONRASI",
 "puanlar": [{"sira": 6, "takim": "KOCAELİSPOR", "puan": 15, "ok": "▲", "vurgu": true}, {"sira": 9, "takim": "ALANYASPOR", "puan": 12}],
 "puan_not": "Hafta sürüyor; sıralama diğer maçlarla değişebilir.",
 "olaylar": [{"etiket": "TARAFTAR", "baslik": "Deplasman tribünü bir süre boş kaldı",
              "metin": "… (2–3 cümle, <b>vurgu</b> serbest)", "takim": "KOCAELİSPOR", "dk": "10'"}],
 "kaynaklar": ["Ajansspor", "Fanatik"]}
Çıktı (ayri): 01_skor.jpg, 02_puan.jpg, 03_olay.jpg, 04_olay.jpg … · (tek): hikaye.jpg
Logolar motor/logolar/<sade-ad>.png'den (ör. "GAZİANTEP FK" → gaziantepfk.png); yoksa renk rozeti.
"""
import json, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ozel  # noqa: E402  (logo bulma kuralı ortak)

FONT = "file://" + os.path.join(HERE, "fonts")
LIME = "#C6FF00"
e = lambda s: html.escape(str(s))


def _renk(ad, d):
    r = (d.get("renkler") or {}).get(ad)
    return tuple(r) if r else ozel.RENKLER.get(ad, ozel.VARSAYILAN)


def rozet(ad, d, s=170):
    src = ozel.logo(ad)
    if src:
        zemin = "background:rgba(255,255,255,.92);border-radius:50%;padding:12%;" if src in ozel._ZEMIN else ""
        return (f"<div style='width:{s}px;height:{s}px;margin:0 auto;display:flex;align-items:center;justify-content:center;{zemin}"
                f"filter:drop-shadow(0 14px 24px rgba(0,0,0,.5))'><img src='{src}' style='max-width:100%;max-height:100%'></div>")
    a, b = _renk(ad, d)
    return (f"<div style='width:{s}px;height:{s}px;border-radius:50%;margin:0 auto;border:6px solid rgba(255,255,255,.9);"
            f"background:linear-gradient(90deg,{a} 0 50%,{b} 50% 100%);box-shadow:0 14px 30px rgba(0,0,0,.5)'></div>")


def kucuk(ad, d, h=52):
    src = ozel.logo(ad)
    if src:
        return f"<img src='{src}' style='width:{h}px;height:{h}px;object-fit:contain;flex:none'>"
    a, b = _renk(ad, d)
    return (f"<span style='display:inline-flex;flex:none;width:16px;height:{h}px;border-radius:5px;overflow:hidden;box-shadow:0 0 0 2px rgba(255,255,255,.25)'>"
            f"<i style='flex:1;background:{a}'></i><i style='flex:1;background:{b}'></i></span>")


CSS = f"""
@font-face{{font-family:'Anton';src:url('{FONT}/anton-latin-ext-400-normal.woff2') format('woff2');unicode-range:U+0100-02AF,U+0130,U+0131,U+015E,U+015F,U+011E,U+011F}}
@font-face{{font-family:'Anton';src:url('{FONT}/anton-latin-400-normal.woff2') format('woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}} body{{background:#000}}
.s{{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:Inter,sans-serif;
 background:radial-gradient(110% 70% at 50% 38%,#1E5636 0%,#0B2416 55%,#030805 100%)}}
.st{{position:absolute;inset:-500px;background:repeating-linear-gradient(-24deg,rgba(255,255,255,.045) 0 55px,transparent 55px 110px)}}
.logo{{width:78px;height:78px;border-radius:50%;border:6px solid {LIME};display:flex;align-items:center;justify-content:center;
 font:400 40px Anton;color:{LIME};background:#0B0F0C;flex:none}}
.bas{{font:800 26px Inter;letter-spacing:4px;color:#A9BCB0;margin-bottom:14px}}
"""


def ust(etiket, alt, renk=LIME, yazi="#0A0F0A"):
    return (f"<div style='position:absolute;left:0;right:0;top:200px;display:flex;flex-direction:column;align-items:center;gap:20px'>"
            f"<div style='display:flex;align-items:center;gap:22px'>"
            f"<div style='display:flex;align-items:center;gap:14px;font:400 46px Anton;letter-spacing:2px'><div class='logo'>11</div>İLK 11</div>"
            f"<div style='padding:12px 30px;border-radius:50px;background:{renk};color:{yazi};font:400 42px Anton;letter-spacing:4px'>{e(etiket)}</div></div>"
            f"<div style='font:800 28px Inter;letter-spacing:4px;color:#B9C7BE'>{e(alt)}</div></div>")


def alt_bar(d):
    return (f"<div style='position:absolute;left:70px;right:70px;top:1570px;font:600 22px Inter;color:#7F9587'>Kaynak: {e(' · '.join(d.get('kaynaklar', [])))}</div>"
            f"<div style='position:absolute;left:150px;right:150px;top:1622px;display:flex;align-items:center;gap:22px;padding:18px 24px;"
            f"border-radius:90px;background:#0B0F0C;border:5px solid {LIME}'><div class='logo'>11</div>"
            f"<div style='flex:1'><div style='font:400 40px Anton'>İLK 11</div><div style='font:700 26px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
            f"<div style='padding:16px 28px;border-radius:50px;background:{LIME};color:#0A0A0A;font:400 38px Anton;letter-spacing:2px'>TAKİP ET</div></div>")


def mini_skor(d, top=380):
    sk = d["skor"].replace("-", "–")
    return (f"<div style='position:absolute;left:70px;right:70px;top:{top}px;display:flex;align-items:center;justify-content:center;gap:22px;"
            f"padding:18px 26px;border-radius:24px;background:rgba(0,0,0,.30);border:2px solid rgba(255,255,255,.08)'>"
            f"{kucuk(d['ev'], d, 58)}<span style='font:400 40px Anton;letter-spacing:1px'>{e(d['ev'])}</span>"
            f"<span style='font:400 56px Anton;color:{LIME};margin:0 10px'>{e(sk)}</span>"
            f"<span style='font:400 40px Anton;letter-spacing:1px'>{e(d['dep'])}</span>{kucuk(d['dep'], d, 58)}</div>")


def _gol_html(d, side, fs=30):
    out = ""
    for g in d.get("goller", []):
        if g.get("taraf") == side:
            out += f"<div>{e(g['dk'])}' {e(g['ad'])}{(' (' + e(g['not']) + ')') if g.get('not') else ''}</div>"
    for k in d.get("kartlar", []):
        if k.get("taraf") == side:
            out += (f"<div style='color:#FF8A8A'><span style='display:inline-block;width:18px;height:26px;border-radius:3px;background:#E30A17;"
                    f"vertical-align:-4px;margin-right:8px'></span>{e(k['dk'])}' {e(k['ad'])}</div>")
    return out or "&nbsp;"


def skor_blok(d, top, s=170, fs_sk=196):
    sk = d["skor"].replace("-", "–")

    def kol(ad, side):
        return (f"<div style='flex:1;text-align:center'>{rozet(ad, d, s)}"
                f"<div style='margin-top:22px;font:400 50px/1.05 Anton;letter-spacing:1px'>{e(ad)}</div>"
                f"<div style='margin-top:14px;font:700 30px/1.5 Inter;color:#D5E2D9'>{_gol_html(d, side)}</div></div>")
    iy = (f"<div style='margin-top:6px;font:800 26px Inter;letter-spacing:3px;color:#A9BCB0'>İLK YARI {e(d['ilk_yari'])}</div>"
          if d.get("ilk_yari") else "")
    return (f"<div style='position:absolute;left:40px;right:40px;top:{top}px;display:flex;align-items:flex-start'>{kol(d['ev'], 'ev')}"
            f"<div style='flex:none;width:330px;text-align:center'><div style='font:400 {fs_sk}px/1 Anton;text-shadow:0 10px 40px rgba(0,0,0,.5)'>{e(sk)}</div>{iy}</div>"
            f"{kol(d['dep'], 'dep')}</div>")


def puan_satirlar(d, fs=46):
    out = ""
    for p in d.get("puanlar", []):
        v = p.get("vurgu")
        out += (f"<div style='display:flex;align-items:center;gap:22px;padding:16px 26px;border-radius:22px;"
                f"background:{'rgba(198,255,0,.10)' if v else 'rgba(0,0,0,.30)'};border:2px solid {'rgba(198,255,0,.55)' if v else 'rgba(255,255,255,.08)'}'>"
                f"<span style='width:80px;font:400 {fs + 8}px Anton;color:{LIME};text-align:center'>{e(p['sira'])}.</span>{kucuk(p['takim'], d)}"
                f"<span style='flex:1;font:400 {fs}px Anton;letter-spacing:1px'>{e(p['takim'])}</span>"
                f"<span style='font:400 {fs + 8}px Anton'>{e(p['puan'])}<span style='font:800 24px Inter;color:#A9BCB0;margin-left:10px;letter-spacing:2px'>PUAN</span></span>"
                + (f"<span style='font:800 26px Inter;color:{LIME};margin-left:6px'>{e(p['ok'])}</span>" if p.get("ok") else "") + "</div>")
    return out


def sayfa_skor(d):
    return (f"<div class='s'><div class='st'></div>{ust('MAÇ SONUCU', d['turnuva'])}{skor_blok(d, 600, 230, 230)}{alt_bar(d)}</div>")


def sayfa_puan(d):
    return (f"<div class='s'><div class='st'></div>{ust('PUAN DURUMU', d.get('puan_alt', d['turnuva']))}{mini_skor(d)}"
            f"<div style='position:absolute;left:70px;right:70px;top:620px;display:flex;flex-direction:column;gap:22px'>{puan_satirlar(d, 56)}</div>"
            f"<div style='position:absolute;left:70px;right:70px;top:1080px;font:600 30px Inter;color:#9FB3A6'>{e(d.get('puan_not', ''))}</div>"
            f"{alt_bar(d)}</div>")


def sayfa_olay(d, o, n, tot):
    renk = "#E30A17" if o.get("kirmizi") else LIME
    yazi = "#FFFFFF" if o.get("kirmizi") else "#0A0F0A"
    tk = ""
    if o.get("takim"):
        tk = (f"<div style='display:flex;align-items:center;gap:16px;font:400 40px Anton;letter-spacing:1px'>{kucuk(o['takim'], d, 64)}{e(o['takim'])}"
              + (f"<span style='margin-left:10px;padding:6px 18px;border-radius:20px;background:rgba(255,255,255,.12);font:800 28px Inter'>{e(o['dk'])}</span>" if o.get("dk") else "")
              + "</div>")
    say = f"<div style='font:800 24px Inter;letter-spacing:3px;color:#7F9587'>{n}/{tot}</div>" if tot > 1 else ""
    return (f"<div class='s'><div class='st'></div>{ust(o.get('etiket', 'MAÇTAN NOT'), d['turnuva'], renk, yazi)}{mini_skor(d)}"
            f"<div style='position:absolute;left:70px;right:70px;top:600px;bottom:400px;display:flex;flex-direction:column;justify-content:center;gap:34px'>"
            f"{say}{tk}<div style='font:400 78px/1.06 Anton;letter-spacing:.5px'>{e(o['baslik'])}</div>"
            f"<div style='width:120px;height:10px;border-radius:5px;background:{renk}'></div>"
            f"<div style='font:600 40px/1.4 Inter;color:#E6EEE8'>{o['metin']}</div></div>{alt_bar(d)}</div>")


def sayfa_tek(d):
    notlar = "".join(
        f"<div style='display:flex;gap:18px;align-items:flex-start'><span style='flex:none;margin-top:6px;width:44px;height:44px;border-radius:50%;"
        f"background:{LIME};color:#0A0F0A;font:400 28px/44px Anton;text-align:center'>!</span>"
        f"<span style='font:600 32px/1.38 Inter;color:#E6EEE8'>{o['metin']}</span></div>" for o in d.get("olaylar", []))
    return (f"<div class='s'><div class='st'></div>{ust('MAÇ SONUCU', d['turnuva'])}{skor_blok(d, 400)}"
            f"<div style='position:absolute;left:70px;right:70px;top:820px'><div class='bas'>PUAN DURUMU · {e(d.get('puan_alt', ''))}</div>"
            f"<div style='display:flex;flex-direction:column;gap:14px'>{puan_satirlar(d)}</div>"
            f"<div style='margin-top:12px;font:600 24px Inter;color:#8FA597'>{e(d.get('puan_not', ''))}</div></div>"
            f"<div style='position:absolute;left:70px;right:70px;top:1222px'><div class='bas'>MAÇTAN NOTLAR</div>"
            f"<div style='display:flex;flex-direction:column;gap:22px'>{notlar}</div></div>{alt_bar(d)}</div>")


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "mac_hikaye")
    os.makedirs(out, exist_ok=True)
    if d.get("bicim", "ayri") == "tek":
        isler = [("hikaye", sayfa_tek(d))]
    else:
        isler = [("01_skor", sayfa_skor(d))]
        if d.get("puanlar"):
            isler.append(("02_puan", sayfa_puan(d)))
        ol = d.get("olaylar", [])
        for i, o in enumerate(ol):
            isler.append((f"{len(isler) + 1:02d}_olay", sayfa_olay(d, o, i + 1, len(ol))))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for ad, govde in isler:
            tmp = os.path.join(out, f"_{ad}.html")
            open(tmp, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{govde}</body></html>")
            pg.goto("file://" + tmp)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            pg.query_selector(".s").screenshot(path=os.path.join(out, ad + ".jpg"), type="jpeg", quality=93)
            os.remove(tmp)
        br.close()
    print("\n".join(os.path.join(out, ad + ".jpg") for ad, _ in isler))


if __name__ == "__main__":
    main()

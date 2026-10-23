# -*- coding: utf-8 -*-
"""İLK 11 · Fotoğraflı hikâye (1080x1920) — demeç ya da son dakika, kişi fotoğrafı + kulüp logoları.

Kullanım:  python3 motor/foto_hikaye.py girdi.json cikti.jpg

Fotoğraf YALNIZ kullanım lisansı uygun dosyadan (Wikimedia Commons CC / kamu malı) gelir; "kredi" zorunludur
ve ekranda yazılır (bkz. motor/fotolar/KAYNAK.txt). Logolar motor/logolar/ klasöründen, değiştirilmeden.

1) DEMEÇ — demecin TAMAMI tek ekranda (yazı boyu otomatik sığdırılır; metin kısaysa büyük fotoğraf düzeni)
{"tip":"demec","baslik":"MAÇ SONU","kim":"Okan Buruk","rol":"Teknik direktör","takim":"GALATASARAY",
 "mac":{"ev":"LILLE","dep":"GALATASARAY","skor":"2-4","alt":"ŞAMPİYONLAR LİGİ · 3. HAFTA · 21 EKİM"},
 "soz":"Kaynaktaki demecin tamamı, birebir. Paragraflar \\n ile ayrılır.",
 "foto":"buruk.jpg","odak":"50% 25%","kredi":"Foto: Zafer · Wikimedia Commons · CC BY 4.0",
 "kaynaklar":["galatasaray.org"]}

2) SON DAKİKA — bir ya da iki kişinin fotoğrafı
{"tip":"sondakika","takim":"FENERBAHÇE","baslik":"…","ozet":"…",
 "kisiler":[{"ad":"MARCO ASENSIO","buyuk":"~3 AY","alt":"Sol diz · ameliyat","foto":"asensio.jpg","odak":"50% 20%"}],
 "kredi":"Fotoğraflar: …","kaynaklar":["Fenerbahçe (resmî açıklama)"]}

foto yolları girdi.json'a göre çözülür. odak = CSS object-position (yüzün kadrajda kalması için).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from haber import CSS, esc
from ozel import logo, _logo_img, renk

ZEMIN = ("background:radial-gradient(110% 70% at 50% 40%,#1E5636 0%,#0B2416 55%,#030805 100%)")
MIC = ("<svg width='46' height='46' viewBox='0 0 24 24' fill='none' stroke='#C6FF00' stroke-width='2.2' stroke-linecap='round' "
       "stroke-linejoin='round'><rect x='9' y='2' width='6' height='12' rx='3'/><path d='M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8'/></svg>")


def _yol(d, f):
    return "file://" + os.path.abspath(os.path.join(d["_dir"], f))


def _logo(ad, d, s):
    src = logo(ad)
    if src:
        return _logo_img(src, s)
    a, b = renk(ad, d)
    return (f"<span style='display:inline-flex;flex:none;width:{s // 4}px;height:{s}px;border-radius:6px;overflow:hidden'>"
            f"<i style='flex:1;background:{a}'></i><i style='flex:1;background:{b}'></i></span>")


def _takip():
    return ("<div style='position:absolute;left:150px;right:150px;bottom:54px;display:flex;align-items:center;gap:22px;padding:18px 26px;"
            "border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'><div class='logo'>11</div>"
            "<div style='flex:1'><div style='font:400 40px Anton'>İLK 11</div><div style='font:700 26px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
            "<div style='padding:16px 28px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 38px Anton;letter-spacing:2px'>TAKİP ET</div></div>")


def _alt_bilgi(d):
    satir = []
    if d.get("kaynaklar"):
        satir.append("Kaynak: " + " · ".join(d["kaynaklar"]))
    if d.get("kredi"):
        satir.append("📷 " + d["kredi"])
    return ("<div style='position:absolute;left:70px;right:70px;bottom:196px;font:700 22px/1.45 Inter;color:#8FA597;letter-spacing:.5px'>"
            + "<br>".join(esc(s) for s in satir) + "</div>")


def _sayfa(govde):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}"
            f".s{{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:Inter,sans-serif;{ZEMIN}}}"
            ".foto{position:absolute;overflow:hidden;border-radius:30px;border:5px solid #C6FF00;box-shadow:0 26px 60px rgba(0,0,0,.55)}"
            ".foto img{width:100%;height:100%;object-fit:cover;display:block}"
            ".soz p{font-weight:600;line-height:1.34;color:#F2F6F3}.soz p+p{margin-top:.5em}"
            f"</style></head><body><div class='s'><div class='stripes'></div>{govde}{_takip()}</div></body></html>")


def bol(paras, n):
    """Paragrafları (kelime değiştirmeden) karakter sayısı dengeli n parçaya ayırır; paragraf bölünmez."""
    toplam = sum(len(p) for p in paras)
    parcalar, cur, birikim = [], [], 0
    for i, p in enumerate(paras):
        kalan_parca = n - len(parcalar)
        kalan_par = len(paras) - i
        if cur and kalan_parca > 1 and (birikim + len(p) / 2 > toplam * (len(parcalar) + 1) / n or kalan_par < kalan_parca):
            parcalar.append(cur); cur = []
        cur.append(p); birikim += len(p)
    parcalar.append(cur)
    return parcalar


def demec_html(d, buyuk, paras=None, sira=None):
    ad = d.get("takim", "")
    m = d.get("mac") or {}
    tum = [p.strip() for p in d["soz"].strip().strip('"“”').split("\n") if p.strip()]
    paras = list(paras or tum)
    if paras[0] == tum[0]:
        paras[0] = "“" + paras[0]
    else:
        paras[0] = "… " + paras[0]
    if paras[-1] == tum[-1]:
        paras[-1] = paras[-1] + "”"
    else:
        paras[-1] = paras[-1] + " …"
    soz = "".join(f"<p>{esc(p)}</p>" for p in paras)
    if buyuk:   # kısa demeç: büyük fotoğraf
        fx, fy, fw, fh, sag_y, ad_fs = 70, 190, 400, 500, 210, 84
        skor_y, kutu_ust = 730, 900
    else:       # uzun demeç: küçük fotoğraf, yazıya daha çok yer
        fx, fy, fw, fh, sag_y, ad_fs = 70, 175, 230, 288, 180, 64
        skor_y, kutu_ust = 488, 630
    sx = fx + fw + 40
    ek = f" · {sira}" if sira else ""
    ust = ("<div style='position:absolute;left:70px;right:70px;top:66px;display:flex;align-items:center;gap:18px'>"
           "<div class='brand' style='font:400 44px Anton;display:flex;align-items:center;gap:14px'><div class='logo'>11</div>İLK 11</div>"
           f"<span style='flex:1'></span>{MIC}<span class='chip' style='background:#C6FF00;color:#0A0F0A'>"
           f"{esc((d.get('baslik') or 'MAÇ SONU') + ' KONUŞTU' + ek)}</span></div>")
    foto = (f"<div class='foto' style='left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px'>"
            f"<img src='{_yol(d, d['foto'])}' style='object-position:{d.get('odak', '50% 25%')}'></div>")
    kim = esc(d["kim"].upper())
    sag = (f"<div style='position:absolute;left:{sx}px;right:70px;top:{sag_y}px;height:{fh - (sag_y - fy) - 10}px;display:flex;flex-direction:column;justify-content:center;gap:{22 if buyuk else 14}px'>"
           f"<div style='font:400 {ad_fs}px/1.02 Anton;letter-spacing:1px'>{kim}</div>"
           f"<div style='display:flex;align-items:center;gap:16px'>{_logo(ad, d, 74 if buyuk else 56) if ad else ''}"
           f"<div style='font:700 {32 if buyuk else 27}px/1.25 Inter;color:#C9D6CE'>{esc(d.get('rol', ''))}"
           f"{'<br><b style=color:#fff>' + esc(ad) + '</b>' if ad else ''}</div></div></div>")
    skor = ""
    if m:
        sk = m["skor"].replace("-", "–")
        lg = 64 if buyuk else 52
        fs = 46 if buyuk else 38
        skor = (f"<div style='position:absolute;left:70px;right:70px;top:{skor_y}px;padding:{18 if buyuk else 12}px 24px;border-radius:26px;"
                "background:rgba(0,0,0,.38);border:2px solid rgba(255,255,255,.09)'>"
                "<div style='display:flex;align-items:center;justify-content:center;gap:18px'>"
                f"{_logo(m['ev'], d, lg)}<span style='font:400 {fs}px Anton;letter-spacing:1px'>{esc(m['ev'])}</span>"
                f"<span style='padding:2px 18px;border-radius:14px;background:#C6FF00;color:#0A0F0A;font:400 {fs + 4}px Anton'>{esc(sk)}</span>"
                f"<span style='font:400 {fs}px Anton;letter-spacing:1px'>{esc(m['dep'])}</span>{_logo(m['dep'], d, lg)}</div>"
                + (f"<div style='margin-top:6px;text-align:center;font:800 {22 if buyuk else 20}px Inter;color:#9FB3A6;letter-spacing:2px'>{esc(m.get('alt', ''))}</div>"
                   if m.get("alt") else "") + "</div>")
    kutu = (f"<div id='box' style='position:absolute;left:70px;right:70px;top:{kutu_ust}px;bottom:278px;overflow:hidden;"
            f"display:flex;flex-direction:column;justify-content:center'><div id='txt' class='soz' style='font-size:46px'>{soz}</div></div>")
    return _sayfa(ust + foto + sag + skor + kutu + _alt_bilgi(d))


def sondakika_html(d):
    ad = d["takim"]
    ks = d["kisiler"]
    n = len(ks)
    w = (940 - 30 * (n - 1)) // n
    h = 640 if n > 1 else 700
    kartlar = ""
    for i, k in enumerate(ks):
        x = 70 + i * (w + 30)
        kartlar += (f"<div class='foto' style='left:{x}px;top:200px;width:{w}px;height:{h}px'>"
                    f"<img src='{_yol(d, k['foto'])}' style='object-position:{k.get('odak', '50% 20%')}'>"
                    "<div style='position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(0deg,rgba(3,8,5,.96) 8%,rgba(3,8,5,.6) 55%,transparent)'></div>"
                    "<div style='position:absolute;left:28px;right:24px;bottom:26px'>"
                    f"<div style='display:inline-block;padding:4px 18px;border-radius:14px;background:#E30A17;font:400 58px/1.1 Anton;letter-spacing:1px'>{esc(k['buyuk'])}</div>"
                    f"<div style='margin-top:12px;font:400 50px/1.02 Anton;letter-spacing:1px'>{esc(k['ad'])}</div>"
                    f"<div style='margin-top:6px;font:700 27px Inter;color:#DCE6DF'>{esc(k.get('alt', ''))}</div></div></div>")
    ust = ("<div style='position:absolute;left:70px;right:70px;top:66px;display:flex;align-items:center;gap:18px'>"
           "<div class='brand' style='font:400 44px Anton;display:flex;align-items:center;gap:14px'><div class='logo'>11</div>İLK 11</div>"
           "<span style='flex:1'></span><span class='chip' style='background:#E30A17;color:#fff'>● SON DAKİKA</span></div>")
    L = len(d["baslik"])
    fs = 92 if L <= 34 else 80 if L <= 48 else 70
    metin = (f"<div style='position:absolute;left:70px;right:70px;top:{200 + h + 46}px;bottom:278px;display:flex;flex-direction:column;gap:26px'>"
             f"<div style='display:flex;align-items:center;gap:16px'>{_logo(ad, d, 66)}<span style='font:400 44px Anton;letter-spacing:1px'>{esc(ad)}</span></div>"
             f"<h1 style='font-size:{fs}px'>{esc(d['baslik'])}</h1>"
             "<div style='width:120px;height:10px;border-radius:5px;background:#E30A17'></div>"
             f"<p style='font:600 36px/1.38 Inter;color:#DCE6DF'>{esc(d['ozet'])}</p></div>")
    return _sayfa(ust + kartlar + metin + _alt_bilgi(d))


def _cek(pg, html_path, html, sigdir):
    open(html_path, "w", encoding="utf-8").write(html)
    pg.goto("file://" + html_path)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(250)
    if not sigdir:
        return None, True
    fs = pg.evaluate("""() => {const b=document.getElementById('box'), t=document.getElementById('txt'); let f=46;
        while (t.scrollHeight > b.clientHeight && f > 14) { f -= 0.5; t.style.fontSize = f + 'px'; } return f; }""")
    ok = pg.evaluate("() => document.getElementById('txt').scrollHeight <= document.getElementById('box').clientHeight")
    return fs, ok


def main():
    src = os.path.abspath(sys.argv[1])
    out = os.path.abspath(sys.argv[2])
    d = json.load(open(src, encoding="utf-8"))
    d["_dir"] = os.path.dirname(src)
    tmp = out + ".html"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        if d["tip"] == "demec":
            tum = [p.strip() for p in d["soz"].strip().strip('"“”').split("\n") if p.strip()]
            n = int(d.get("ekran", 1))   # 1 = tek ekran (varsayılan); >1 yalnız sayfa sahibi isterse
            gruplar = bol(tum, n) if n > 1 else [tum]
            kok, uz = os.path.splitext(out)
            for i, g in enumerate(gruplar):
                sira = f"{i + 1}/{len(gruplar)}" if len(gruplar) > 1 else None
                hedef = f"{kok}_{i + 1}{uz}" if len(gruplar) > 1 else out
                fs, ok = _cek(pg, tmp, demec_html(d, True, g, sira), True)
                if fs < 30:
                    fs, ok = _cek(pg, tmp, demec_html(d, False, g, sira), True)
                if not ok:
                    br.close(); os.remove(tmp)
                    sys.exit("HATA: demeç ekrana 14px ile bile sığmadı.")
                print(f"{os.path.basename(hedef)} yazı boyu: {fs}px", file=sys.stderr)
                pg.query_selector(".s").screenshot(path=hedef, type="jpeg", quality=92)
                print(hedef)
            br.close()
            os.remove(tmp)
            return
        elif d["tip"] == "sondakika":
            _cek(pg, tmp, sondakika_html(d), False)
        else:
            sys.exit("bilinmeyen tip: " + d["tip"])
        pg.query_selector(".s").screenshot(path=out, type="jpeg", quality=92)
        br.close()
    os.remove(tmp)
    print(out)


if __name__ == "__main__":
    main()

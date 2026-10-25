# -*- coding: utf-8 -*-
"""İLK 11 · Günün Haberleri kart üreticisi.

Kullanım:  python3 motor/haber.py haber.json cikti_klasoru
haber.json:
{
  "tarih": "2026-10-23",
  "haberler": [
    {"etiket": "SÜPER LİG", "baslik": "…", "kisa": "kapakta görünecek kısa başlık (≤38 karakter)",
     "ozet": "2-3 cümle, en fazla ~240 karakter", "kaynaklar": ["TFF", "AA"],
     "skor": {"sol": "LİLLE", "sonuc": "2-4", "sag": "GALATASARAY"}   # isteğe bağlı, sadece maç sonucu haberlerinde}
  ]
}
Etiketler: SÜPER LİG, MİLLİ TAKIM, AVRUPA, TRANSFER, DÜNYA, 1. LİG, KADIN FUTBOLU (diğerleri varsayılan renkle çizilir).
Çıktı: 01_kapak.jpg, 02_haber.jpg …, NN_takip.jpg (1080x1350)
"""
import json, os, sys, html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilk_parts import hoca, ball, tr_flag

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "file://" + os.path.join(HERE, "fonts")
AYLAR = ["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN", "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"]
GUNLER = ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]
RENK = {"SÜPER LİG": ("#C6FF00", "#0A0F0A"), "MİLLİ TAKIM": ("#E30A17", "#FFFFFF"), "AVRUPA": ("#3D7BFF", "#FFFFFF"),
        "TRANSFER": ("#FFB000", "#0A0F0A"), "DÜNYA": ("#00C2A8", "#0A0F0A"), "1. LİG": ("#B57BFF", "#0A0F0A"),
        "KADIN FUTBOLU": ("#FF6FB1", "#0A0F0A")}

CSS = f"""
@font-face{{font-family:'Anton';src:url('{FONT}/anton-latin-ext-400-normal.woff2') format('woff2');unicode-range:U+0100-02AF,U+0130,U+0131,U+015E,U+015F,U+011E,U+011F}}
@font-face{{font-family:'Anton';src:url('{FONT}/anton-latin-400-normal.woff2') format('woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#000;font-family:'Inter',sans-serif}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;color:#fff;
 background:radial-gradient(120% 90% at 50% 30%,#1E5636 0%,#0B2416 55%,#030805 100%)}}
.stripes{{position:absolute;inset:-400px;background:repeating-linear-gradient(-24deg,rgba(255,255,255,.045) 0 55px,transparent 55px 110px)}}
.top{{position:absolute;left:70px;right:70px;top:64px;display:flex;align-items:center;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:16px;font:400 40px Anton;letter-spacing:2px}}
.logo{{width:64px;height:64px;border-radius:50%;border:5px solid #C6FF00;display:flex;align-items:center;justify-content:center;
 font:400 34px Anton;color:#C6FF00;background:#0B0F0C}}
.count{{font:800 30px Inter;color:#9FB3A6;letter-spacing:3px}}
.chip{{display:inline-block;padding:12px 26px;border-radius:40px;font:400 36px Anton;letter-spacing:3px}}
h1{{font-family:Anton;font-weight:400;line-height:1.02;letter-spacing:.5px}}
.foot{{position:absolute;left:70px;right:70px;bottom:60px;display:flex;justify-content:space-between;align-items:center;
 font:700 30px Inter;color:#9FB3A6}}
.hl{{color:#C6FF00}}
"""


def esc(s):
    return html.escape(s, quote=True)


def tarih_str(t):
    d = datetime.date.fromisoformat(t)
    return f"{d.day} {AYLAR[d.month - 1]} {d.year} · {GUNLER[d.weekday()]}"


def ikon(etiket):
    if etiket == "MİLLİ TAKIM":
        return f"<svg width='300' height='200' viewBox='0 0 300 200'>{tr_flag(300)}</svg>"
    if etiket == "TRANSFER":
        return ("<svg width='300' height='220' viewBox='0 0 300 220' fill='none' stroke='#FFB000' stroke-width='22' stroke-linecap='round' stroke-linejoin='round'>"
                "<path d='M30 70 H230 M190 30 L240 70 L190 110'/><path d='M270 160 H70 M110 120 L60 160 L110 200'/></svg>")
    return f"<svg width='240' height='240' viewBox='0 0 240 240'>{ball(120, 120, 112, 'b' + str(abs(hash(etiket)) % 999))}</svg>"


def top(n, total):
    return (f"<div class='top'><div class='brand'><div class='logo'>11</div>İLK 11</div>"
            f"<div class='count'>{n}/{total}</div></div>")


def foot(text="KAYDIR →"):
    return f"<div class='foot'><span>@ilk.onbir11</span><span style='color:#C6FF00'>{text}</span></div>"


def kapak(d, total):
    rows = ""
    sik = len(d["haberler"]) > 4
    cok = len(d["haberler"]) > 5
    pad, gap, mt = ("15px 24px", 12, 36) if sik else ("22px 26px", 18, 54)
    if cok:
        pad, gap, mt = ("11px 22px", 10, 28)
    fs = 140 if cok else 170
    for h in d["haberler"]:
        bg, fg = RENK.get(h["etiket"], ("#C6FF00", "#0A0F0A"))
        rows += (f"<div style='display:flex;align-items:center;gap:22px;padding:{pad};border-radius:24px;background:rgba(0,0,0,.35);"
                 f"border:2px solid rgba(255,255,255,.08)'><span class='chip' style='background:{bg};color:{fg};font-size:26px;padding:8px 18px;flex:none'>{esc(h['etiket'])}</span>"
                 f"<span style='font:700 34px/1.2 Inter;color:#F1F5F2'>{esc(h.get('kisa') or h['baslik'][:40])}</span></div>")
    return (f"<div class='slide'><div class='stripes'></div>{top(1, total)}"
            "<div style='position:absolute;left:70px;right:70px;top:200px'>"
            f"<h1 style='font-size:{fs}px'>GÜNÜN</h1><h1 class='hl' style='font-size:{fs}px;margin-top:-6px'>HABERLERİ</h1>"
            f"<div style='margin-top:26px;font:800 36px Inter;letter-spacing:5px;color:#C9D6CE'>{tarih_str(d['tarih'])}</div>"
            f"<div style='margin-top:{mt}px;display:flex;flex-direction:column;gap:{gap}px'>{rows}</div></div>"
            f"{foot()}</div>")


def haber(h, n, total):
    bg, fg = RENK.get(h["etiket"], ("#C6FF00", "#0A0F0A"))
    L = len(h["baslik"])
    fs = 104 if L <= 38 else 92 if L <= 55 else 80 if L <= 75 else 70
    kay = " · ".join(h.get("kaynaklar", []))
    return (f"<div class='slide'><div class='stripes'></div>{top(n, total)}"
            f"<div style='position:absolute;right:40px;top:150px;opacity:.16;transform:rotate(-8deg)'>{ikon(h['etiket'])}</div>"
            "<div style='position:absolute;left:70px;right:70px;top:250px;bottom:190px;display:flex;flex-direction:column;justify-content:center;gap:38px'>"
            f"<div><span class='chip' style='background:{bg};color:{fg}'>{esc(h['etiket'])}</span></div>"
            + skor_blok(h.get("skor"), bg, fg) +
            f"<h1 style='font-size:{fs}px'>{esc(h['baslik'])}</h1>"
            f"<div style='width:120px;height:10px;border-radius:5px;background:{bg}'></div>"
            f"<p style='font:600 40px/1.38 Inter;color:#DCE6DF'>{esc(h['ozet'])}</p>"
            + (f"<p style='font:700 28px Inter;color:#8FA597;letter-spacing:1px'>Kaynak: {esc(kay)}</p>" if kay else "")
            + f"</div>{foot('KAYDIR →' if n < total else '')}</div>")


def skor_blok(sk, bg, fg):
    if not sk:
        return ""
    team = "flex:1;font:400 46px Anton;letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
    return ("<div style='display:flex;align-items:center;gap:22px;padding:22px 28px;border-radius:28px;background:#0B0F0C;border:3px solid rgba(255,255,255,.12)'>"
            f"<div style='{team};text-align:right'>{esc(sk['sol'])}</div>"
            f"<div style='flex:none;padding:6px 26px;border-radius:18px;background:{bg};color:{fg};font:400 76px Anton'>{esc(sk['sonuc'])}</div>"
            f"<div style='{team}'>{esc(sk['sag'])}</div></div>")


def takip(total):
    h = hoca("stand", (("wink", None, None),))
    return (f"<div class='slide'><div class='stripes'></div>{top(total, total)}"
            "<div style='position:absolute;left:0;right:0;top:170px;text-align:center'>"
            "<h1 style='font-size:110px'>DAHA FAZLASI İÇİN</h1><h1 class='hl' style='font-size:150px'>TAKİP ET</h1></div>"
            f"<svg style='position:absolute;left:290px;top:520px' width='500' height='560' viewBox='-250 -230 500 560'>{h}</svg>"
            "<div style='position:absolute;left:110px;right:110px;top:930px;display:flex;align-items:center;gap:24px;padding:26px 30px;"
            "border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'>"
            "<div class='logo' style='width:96px;height:96px;font-size:52px'>11</div>"
            "<div style='flex:1'><div style='font:400 46px Anton'>İLK 11</div><div style='font:700 30px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>"
            "<div style='padding:20px 34px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 44px Anton;letter-spacing:2px'>TAKİP ET</div></div>"
            "<div style='position:absolute;left:70px;right:70px;top:1130px;text-align:center;font:700 34px/1.4 Inter;color:#C9D6CE'>"
            "Her sabah <span class='hl'>09:30</span> günün haberleri · Her akşam <span class='hl'>19:00</span> yeni bir hikâye</div></div>")


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2] if len(sys.argv) > 2 else "haber_cikti"
    os.makedirs(out, exist_ok=True)
    total = len(d["haberler"]) + 2
    slides = [kapak(d, total)] + [haber(h, i + 2, total) for i, h in enumerate(d["haberler"])] + [takip(total)]
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(slides)}</body></html>"
    p = os.path.join(out, "_kartlar.html")
    open(p, "w", encoding="utf-8").write(page)
    from playwright.sync_api import sync_playwright
    names = ["01_kapak"] + [f"{i + 2:02d}_haber" for i in range(len(d["haberler"]))] + [f"{total:02d}_takip"]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto("file://" + os.path.abspath(p))
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        for el, nm in zip(pg.query_selector_all(".slide"), names):
            el.screenshot(path=os.path.join(out, nm + ".jpg"), type="jpeg", quality=92)
        br.close()
    print("\n".join(os.path.join(out, nm + ".jpg") for nm in names))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""İLK 11 · Gönderiyi Instagram hikâyesine (1080x1920) çeviren kart.

Kullanım:  python3 motor/story.py kart.jpg cikti.jpg ["ÜST YAZI"] ["ALT YAZI"]
Varsayılan üst yazı: YENİ GÖNDERİ · alt yazı: Haberlerin tamamı profilde
Kartı (1080x1350) eğik bir çerçeveyle ortalar; altta @ilk.onbir11 TAKİP ET butonu.
"""
import os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "file://" + os.path.join(HERE, "fonts")


def main():
    kart = os.path.abspath(sys.argv[1])
    out = os.path.abspath(sys.argv[2])
    ust = html.escape(sys.argv[3] if len(sys.argv) > 3 else "YENİ GÖNDERİ")
    alt = html.escape(sys.argv[4] if len(sys.argv) > 4 else "Haberlerin tamamı profilde")
    page = f"""<!doctype html><html><head><meta charset='utf-8'><style>
@font-face{{font-family:'Anton';src:url('{FONT}/anton-latin-ext-400-normal.woff2') format('woff2');unicode-range:U+0100-02AF,U+0130,U+0131,U+015E,U+015F,U+011E,U+011F}}
@font-face{{font-family:'Anton';src:url('{FONT}/anton-latin-400-normal.woff2') format('woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#000}}
.s{{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:Inter,sans-serif;
 background:radial-gradient(110% 70% at 50% 40%,#1E5636 0%,#0B2416 55%,#030805 100%)}}
.st{{position:absolute;inset:-500px;background:repeating-linear-gradient(-24deg,rgba(255,255,255,.045) 0 55px,transparent 55px 110px)}}
.logo{{width:84px;height:84px;border-radius:50%;border:6px solid #C6FF00;display:flex;align-items:center;justify-content:center;
 font:400 44px Anton;color:#C6FF00;background:#0B0F0C}}
</style></head><body><div class='s'><div class='st'></div>
<div style='position:absolute;left:0;right:0;top:120px;display:flex;flex-direction:column;align-items:center;gap:26px'>
 <div style='display:flex;align-items:center;gap:18px;font:400 52px Anton;letter-spacing:2px'><div class='logo'>11</div>İLK 11</div>
 <div style='padding:14px 34px;border-radius:50px;background:#C6FF00;color:#0A0F0A;font:400 46px Anton;letter-spacing:4px'>{ust}</div>
</div>
<img src='file://{kart}' style='position:absolute;left:120px;top:400px;width:840px;height:1050px;border-radius:34px;
 transform:rotate(-2.5deg);box-shadow:0 40px 90px rgba(0,0,0,.6),0 0 0 6px rgba(198,255,0,.85)'>
<div style='position:absolute;left:0;right:0;top:1515px;text-align:center;font:700 40px Inter;color:#DCE6DF'>{alt}</div>
<div style='position:absolute;left:150px;right:150px;top:1600px;display:flex;align-items:center;gap:22px;padding:22px 26px;
 border-radius:90px;background:#0B0F0C;border:5px solid #C6FF00'>
 <div class='logo' style='width:84px;height:84px;font-size:44px'>11</div>
 <div style='flex:1'><div style='font:400 42px Anton'>İLK 11</div><div style='font:700 28px Inter;color:#B9C2BB'>@ilk.onbir11</div></div>
 <div style='padding:18px 30px;border-radius:50px;background:#C6FF00;color:#0A0A0A;font:400 40px Anton;letter-spacing:2px'>TAKİP ET</div>
</div>
</div></body></html>"""
    tmp = out + ".html"
    open(tmp, "w", encoding="utf-8").write(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.query_selector(".s").screenshot(path=out, type="jpeg", quality=92)
        br.close()
    os.remove(tmp)
    print(out)


if __name__ == "__main__":
    main()

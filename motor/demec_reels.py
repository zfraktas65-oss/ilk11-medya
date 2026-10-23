# -*- coding: utf-8 -*-
"""İLK 11 · Demeç / basın toplantısı klibinden Reels motoru.

Görev talimatı: motor/gorevler/demec_reels.md
Kullanım:
  python3 motor/demec_reels.py senaryo.json cikti --onizleme   # birkaç kare (hızlı kontrol)
  python3 motor/demec_reels.py senaryo.json cikti              # cikti/<slug>.mp4 + kapak.jpg + kapak_temiz.jpg

senaryo.json:
{
 "slug": "...", "video": "kaynak/orijinal.mp4", "bas": 0, "son": 59.8,
 "kirp": [x, y, w, h],                 # kaynakta pencereye girecek bölge (pencere oranına yakın)
 "ust": "MAÇ SONU KONUŞTU", "kim": "ITALIANO · BEŞİKTAŞ 2-2 CRYSTAL PALACE",
 "soz": "“ÇOK KOLAY GOLLER YİYORUZ”", "kredi": "Görüntü: TikTok @futbolarena",
 "soru": "Sence ... ?", "kapak_sn": 3.0,
 "ifadeler": [{"a": 0.0, "b": 3.0, "metin": "..."}]   # kaynak videonun zamanına göre
}
Sona Hoca'nın takip çağrısı sahnesi (hikaye.py ile aynı) eklenir.
"""
import json, os, re, subprocess, sys, wave
import numpy as np

MOTOR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MOTOR)
import hikaye as H  # noqa: E402

SR, FPS = 44100, 30
W, HH = 1080, 1920
WIN = (30, 452, 1020, 1060)          # pencere: x, y, w, h
SUB_Y0, SUB_H = 1150, 380            # altyazı katmanının kırpılan bölgesi
LIME = H.LIME
FONTS = "file://" + os.path.join(MOTOR, "fonts")
FONT_CSS = (f"@font-face{{font-family:'Anton';src:url('{FONTS}/anton-latin-ext-400-normal.woff2') format('woff2');"
            "unicode-range:U+0100-02AF,U+0130,U+0131,U+015E,U+015F,U+011E,U+011F}"
            f"@font-face{{font-family:'Anton';src:url('{FONTS}/anton-latin-400-normal.woff2') format('woff2')}}")


def run(cmd):
    subprocess.run(cmd, check=True)


# ------------------------------------------------------------ çerçeve (arka plan + başlık + delikli pencere)
def frame_svg(spec):
    x, y, w, h = WIN
    r = 34
    hole = f"M{x + r} {y} H{x + w - r} A{r} {r} 0 0 1 {x + w} {y + r} V{y + h - r} A{r} {r} 0 0 1 {x + w - r} {y + h} H{x + r} A{r} {r} 0 0 1 {x} {y + h - r} V{y + r} A{r} {r} 0 0 1 {x + r} {y}Z"
    bg = H.arka("marka", 3)
    ust = H.tr_upper(spec.get("ust", "MAÇ SONU KONUŞTU"))
    uw = len(ust) * 21 + 120
    kim = H.tr_upper(spec.get("kim", ""))
    soz = H.tr_upper(spec.get("soz", ""))
    fs_soz = min(92, int(1000 / max(1, len(soz) * .47)))
    fs_kim = min(46, int(980 / max(1, len(kim) * .5)))
    mic = ("<g transform='translate(-{0} 0)'><rect x='-9' y='-22' width='18' height='30' rx='9' fill='#0A0F0A'/>"
           "<path d='M-15 -2 Q-15 16 0 16 Q15 16 15 -2' fill='none' stroke='#0A0F0A' stroke-width='4'/>"
           "<rect x='-2' y='16' width='4' height='9' fill='#0A0F0A'/></g>").format(uw / 2 - 42)
    svg = (f"<svg viewBox='0 0 {W} {HH}' xmlns='http://www.w3.org/2000/svg'>{H.DEFS}"
           f"<mask id='m'><rect width='{W}' height='{HH}' fill='#fff'/><path d='{hole}' fill='#000'/></mask>"
           f"<g mask='url(#m)'>{bg}"
           # başlık
           f"<g transform='translate(540 214)'><rect x='{-uw / 2}' y='-31' width='{uw}' height='62' rx='31' fill='{LIME}'/>{mic}"
           f"<text x='18' y='15' text-anchor='middle' font-family='Anton' font-size='38' letter-spacing='3' fill='#0A0F0A'>{H.esc(ust)}</text></g>"
           f"<text x='540' y='{318}' text-anchor='middle' font-family='Anton' font-size='{fs_kim}' letter-spacing='2' fill='#FFFFFF'>{H.esc(kim)}</text>"
           f"<text x='540' y='{318 + 14 + fs_soz}' text-anchor='middle' font-family='Anton' font-size='{fs_soz}' letter-spacing='1' fill='{LIME}' "
           f"stroke='#06120A' stroke-width='8' paint-order='stroke'>{H.esc(soz)}</text>"
           # pencere altı: kaynak + sayfa
           f"<text x='{x + 8}' y='{y + h + 52}' font-family='Inter' font-weight='600' font-size='26' fill='#B9C2BB'>{H.esc(spec.get('kredi', ''))}</text>"
           f"<text x='{x + w - 8}' y='{y + h + 52}' text-anchor='end' font-family='Anton' font-size='34' letter-spacing='1' fill='{LIME}'>@ilk.onbir11</text>"
           "</g>"
           f"<path d='{hole}' fill='none' stroke='{LIME}' stroke-width='6'/>"
           # pencerenin sol üstünde küçük İLK 11 rozeti
           f"<g transform='translate({x + 26} {y + 26})'><rect width='150' height='54' rx='27' fill='#0B0F0C' fill-opacity='.82' stroke='{LIME}' stroke-width='3'/>"
           f"<text x='75' y='39' text-anchor='middle' font-family='Anton' font-size='32' letter-spacing='2' fill='#FFFFFF'>İLK <tspan fill='{LIME}'>11</tspan></text></g>"
           "</svg>")
    return svg


# ------------------------------------------------------------ altyazı zamanlaması
def word_chunks(ifadeler, bas):
    WT = []
    for f in ifadeler:
        a, b = f["a"] - bas, f["b"] - bas
        WT.append(H.word_times(f["metin"], f["metin"], a, b))
    res = []
    for wt in WT:
        cur = []
        for w in wt:
            cur.append(w)
            if len(cur) >= 3 or len(" ".join(x[0] for x in cur)) >= 14 or re.search(r"[.,:!?…]$", w[0]):
                res.append(cur); cur = []
        if cur:
            res.append(cur)
    return res


def sub_states(chunks, T):
    """[(t0, t1, html)] — her kelimenin vurgulandığı an ayrı durum."""
    st = []
    for i, c in enumerate(chunks):
        nxt = chunks[i + 1][0][1] if i + 1 < len(chunks) else T
        end = min(nxt, c[-1][2] + .5)
        for j, w in enumerate(c):
            t0 = max(0.0, (c[0][1] - .04) if j == 0 else w[1] - .03)
            t1 = (c[j + 1][1] - .03) if j + 1 < len(c) else end
            if t1 <= t0:
                continue
            spans = " ".join(f"<span class='{'on' if k == j else ('next' if k > j else '')}'>{H.esc(x[0])}</span>" for k, x in enumerate(c))
            st.append((t0, t1, spans))
    # boşlukları doldur
    out, t = [], 0.0
    for t0, t1, h in sorted(st):
        if t0 > t + 1e-3:
            out.append((t, t0, ""))
        t0 = max(t0, t)
        if t1 > t0:
            out.append((t0, t1, h)); t = t1
    if t < T:
        out.append((t, T, ""))
    return out


SUB_CSS = (FONT_CSS + "*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}"
           f"#band{{position:absolute;left:{WIN[0]}px;width:{WIN[2]}px;top:1190px;height:{WIN[1] + WIN[3] - 1190}px;border-radius:0 0 34px 34px;"
           "background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.5) 35%,rgba(0,0,0,.62))}"
           "#subs{position:absolute;left:70px;right:120px;top:1262px;text-align:center;font:900 78px/1.12 'Inter Display','Inter';"
           "letter-spacing:-.5px;color:#fff;text-shadow:0 0 2px #000,4px 4px 0 #000,-4px 4px 0 #000,4px -4px 0 #000,-4px -4px 0 #000,"
           "0 6px 0 #000,0 -6px 0 #000,6px 0 0 #000,-6px 0 0 #000,0 10px 26px rgba(0,0,0,.6)}"
           "#subs span{display:inline-block;margin:0 .06em}#subs span.on{color:" + LIME + "}#subs span.next{opacity:.6}")


# ------------------------------------------------------------ kapanış (Hoca takip çağrısı)
def outro(spec, out, br):
    cta = H.load_audio(os.path.join(MOTOR, "ses", "cta_hoca.mp3"))
    cs = H.sentence_spans(cta, 2)
    at0 = .35
    cw = [H.word_times("Daha fazlası için", "Daha fazlası için", at0 + cs[0][0], at0 + cs[0][1]),
          H.word_times("İlk On Bir'i takip etmeyi unutma!", "İLK 11'i takip etmeyi unutma!", at0 + cs[1][0], at0 + cs[1][1])]
    T = round(at0 + len(cta) / SR + 1.1, 2)
    rtak = cw[1][2][1]
    events = []
    body = H.t_takip({}, lambda n: .5, lambda t, k: events.append((t, k)), 0, spec.get("soru", ""), rtak)
    css = open(os.path.join(MOTOR, "stil.css"), encoding="utf-8").read().replace("FONTDIR", FONTS)
    js = open(os.path.join(MOTOR, "oynat.js"), encoding="utf-8").read()
    data = {"scenes": [{"start": 0, "end": T}], "chunks": H.chunks(cw, T), "T": T, "labelEnd": 0}
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>"
            f"<section class='scene' data-start='0'><svg viewBox='0 0 1080 1920' xmlns='http://www.w3.org/2000/svg'>{H.DEFS}"
            f"<g>{body}</g><rect width='1080' height='1920' fill='url(#vig)' opacity='.7'/></svg></section>"
            "<div id='label'></div><div id='band'></div><div id='subs'></div>"
            f"<script>window.__DATA={json.dumps(data, ensure_ascii=False)};{js}</script></body></html>")
    hp = os.path.join(out, "_outro.html")
    open(hp, "w", encoding="utf-8").write(page)
    pg = br.new_page(viewport={"width": W, "height": HH})
    pg.goto("file://" + os.path.abspath(hp))
    pg.wait_for_function("window.__ready===true")
    vid = os.path.join(out, "_outro_v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    for fi in range(int(round(T * FPS))):
        pg.evaluate(f"seek({fi / FPS})")
        ff.stdin.write(pg.screenshot(type="jpeg", quality=94))
    ff.stdin.close(); ff.wait()
    pg.close()
    # ses: Hoca + efektler
    N = int(T * SR)
    mix = np.zeros(N, np.float32)
    i0 = int(at0 * SR); mix[i0:i0 + len(cta)] += cta[:N - i0]
    for t, k in events:
        s = H.sfx_signal(k).astype(np.float32); i = int(t * SR)
        if i < N:
            mix[i:i + len(s)] += .5 * s[:N - i]
    mix *= .9 / (np.abs(mix).max() + 1e-9)
    wav = os.path.join(out, "_outro.wav")
    with wave.open(wav, "wb") as w:
        st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    mp4 = os.path.join(out, "_outro.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", mp4])
    return mp4, T


# ------------------------------------------------------------ ana akış
def main():
    spec_path, out = sys.argv[1], sys.argv[2]
    preview = "--onizleme" in sys.argv
    os.makedirs(out, exist_ok=True)
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    src = os.path.join(base, spec["video"])
    bas, son = float(spec.get("bas", 0)), float(spec["son"])
    T = son - bas
    states = sub_states(word_chunks(spec["ifadeler"], bas), T)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--font-render-hinting=none"])
        # çerçeve
        pg = br.new_page(viewport={"width": W, "height": HH})
        fh = os.path.join(out, "_cerceve.html")
        open(fh, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}*{{margin:0}}html,body{{background:transparent}}"
                                              f"svg{{display:block;width:{W}px;height:{HH}px}}</style></head><body>{frame_svg(spec)}</body></html>")
        pg.goto("file://" + os.path.abspath(fh))
        pg.evaluate("document.fonts.ready.then(()=>document.fonts.check('40px Anton'))")
        pg.wait_for_timeout(300)
        frame_png = os.path.join(out, "_cerceve.png")
        pg.screenshot(path=frame_png, omit_background=True)
        pg.close()
        # altyazı durumları
        pg = br.new_page(viewport={"width": W, "height": HH})
        sh = os.path.join(out, "_altyazi.html")
        open(sh, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{SUB_CSS}</style></head><body>"
                                              "<div id='band'></div><div id='subs'></div></body></html>")
        pg.goto("file://" + os.path.abspath(sh))
        pg.evaluate("document.fonts.ready")
        sdir = os.path.join(out, "_alt"); os.makedirs(sdir, exist_ok=True)
        lst = []
        cache = {}
        for k, (t0, t1, h) in enumerate(states):
            if h not in cache:
                fn = os.path.join(sdir, f"s{len(cache):04d}.png")
                pg.evaluate("h=>{document.getElementById('subs').innerHTML=h;document.getElementById('band').style.opacity=h?1:0}", h)
                pg.screenshot(path=fn, omit_background=True, clip={"x": 0, "y": SUB_Y0, "width": W, "height": SUB_H})
                cache[h] = fn
            lst.append((cache[h], t1 - t0))
        pg.close()
        with open(os.path.join(out, "_alt.txt"), "w") as f:
            for fn, d in lst:
                f.write(f"file '{os.path.abspath(fn)}'\nduration {d:.3f}\n")
            f.write(f"file '{os.path.abspath(lst[-1][0])}'\n")
        x, y, w, h = WIN
        cx, cy, cw, ch = spec["kirp"]
        fc = (f"[0:v]trim={bas}:{son},setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},scale={w}:{h}:flags=lanczos,setsar=1,"
              f"pad={W}:{HH}:{x}:{y}:color=black,fps={FPS}[v0];"
              f"[v0][1:v]overlay=0:0[v1];[2:v]format=rgba,fps={FPS}[s];[v1][s]overlay=0:{SUB_Y0}:eof_action=pass,format=yuv420p[v]")
        if preview:
            from PIL import Image
            ts = spec.get("onizleme_sn", [3, 15, 30, 45, 57])
            fr = Image.open(frame_png).convert("RGBA")
            shots = []
            for t in ts:
                raw = os.path.join(out, "_kare.png")
                run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{bas + t:.2f}", "-i", src, "-frames:v", "1", raw])
                im = Image.open(raw).convert("RGBA").crop((cx, cy, cx + cw, cy + ch)).resize((w, h), Image.LANCZOS)
                can = Image.new("RGBA", (W, HH), "black"); can.paste(im, (x, y))
                can.alpha_composite(fr)
                tt = 0.0
                for fn, d in lst:
                    if tt <= t < tt + d:
                        can.alpha_composite(Image.open(fn).convert("RGBA"), (0, SUB_Y0)); break
                    tt += d
                shots.append(can.convert("RGB"))
            sheet = Image.new("RGB", (len(shots) * 366, 640), "white")
            for i, im in enumerate(shots):
                sheet.paste(im.resize((360, 640)), (i * 366, 0))
            sheet.save(os.path.join(out, "onizleme.jpg"), quality=88)
            shots[0].save(os.path.join(out, "onizleme_tam.jpg"), quality=90)
            print("Önizleme:", os.path.join(out, "onizleme.jpg"), "| altyazı durumu:", len(states))
            br.close()
            return
        main_mp4 = os.path.join(out, "_ana.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-loop", "1", "-i", frame_png, "-f", "concat", "-safe", "0",
             "-i", os.path.join(out, "_alt.txt"), "-filter_complex",
             fc + f";[0:a]atrim={bas}:{son},asetpts=PTS-STARTPTS,afade=t=out:st={T - .35:.2f}:d=0.35,aresample=44100[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{T:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", main_mp4])
        out_mp4, To = outro(spec, out, br)
        br.close()
    final = os.path.join(out, f"{spec.get('slug', 'demec')}.mp4")
    xd = .3
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", main_mp4, "-i", out_mp4, "-filter_complex",
         f"[0:v]settb=AVTB,fps={FPS}[a0];[1:v]settb=AVTB,fps={FPS}[b0];[a0][b0]xfade=transition=fade:duration={xd}:offset={T - xd:.3f},format=yuv420p[v];"
         f"[0:a][1:a]acrossfade=d={xd}[a1];[a1]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", final])
    kt = float(spec.get("kapak_sn", 3.0))
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{kt}", "-i", final, "-frames:v", "1", "-q:v", "2", os.path.join(out, "kapak.jpg")])
    # altyazısız kapak: kaynak kare + çerçeve
    from PIL import Image
    raw = os.path.join(out, "_kapak_ham.png")
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{bas + kt:.2f}", "-i", src, "-frames:v", "1", raw])
    x, y, w, h = WIN
    cx, cy, cw, ch = spec["kirp"]
    im = Image.open(raw).convert("RGBA").crop((cx, cy, cx + cw, cy + ch)).resize((w, h), Image.LANCZOS)
    can = Image.new("RGBA", (W, HH), "black"); can.paste(im, (x, y))
    can.alpha_composite(Image.open(frame_png).convert("RGBA"))
    can.convert("RGB").save(os.path.join(out, "kapak_temiz.jpg"), quality=92)
    print("VIDEO:", final)


if __name__ == "__main__":
    main()

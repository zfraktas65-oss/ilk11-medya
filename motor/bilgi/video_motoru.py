#!/usr/bin/env python3
"""Sesli + animasyonlu bilgi videosu motoru (maskot "Kâşif" ile).

Kullanım:
  python3 video_motoru.py senaryo.json cikti              # 9x16 + 16x9 video ve kapak
  python3 video_motoru.py senaryo.json cikti --onizleme   # her sahneden kare (hızlı kontrol)

senaryo.json:
{"series": "Günün Bilgisi", "topic": "Ahtapot", "voice": "fahrettin", "speed": 1.0, "palette": 0-4 (ops.),
 "voice_file": "ses.mp3" (ops.; tüm anlatımı içeren hazır ses, sahnelere otomatik bölünür),
 "scenes": [{"kicker": "...", "headline": "Üç *kalp*", "narration": "...", "ifade": "saskin",
             "art": "<svg viewBox='0 0 600 600'>...</svg>"}]}
art içinde --d:{{kelime}} veya --d:{{kelime+0.3}} yazılırsa, anlatımda o kelimenin söylendiği an (ör. 2.40s) ile değiştirilir.
ifade (maskot Kâşif'in yüzü): merakli | saskin | mutlu | dusunceli | heyecanli | gulen | korkmus.
"maskot": false sahnede maskotu gizler. Maskot sol altta durur, anlatım sırasında ağzı konuşur.
"""
import json, sys, os, re, math, subprocess, wave, hashlib, html as HT
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.environ.get("TTS_MODELS", os.path.join(HERE, "models"))
FPS, SR = 30, 44100
PALETTES = [  # bg1, bg2, blob1, blob2, acc, txt, sub
    ("#101834", "#04060F", "#2E52BE", "#822E96", "#FFC43D", "#F6F7FB", "#C4CCE2"),
    ("#0A2628", "#020C0E", "#168276", "#224C96", "#FF8C60", "#F0F9F7", "#B6D6D0"),
    ("#26102E", "#0A0410", "#962C76", "#422CA0", "#68ECCC", "#FBF5FB", "#D6C4DA"),
    ("#12201A", "#040907", "#3C823E", "#1E6076", "#F4DE5C", "#F4F9F0", "#C4D4BE"),
    ("#2C180E", "#0E0703", "#B45622", "#802A36", "#7ACCFF", "#FCF7F1", "#DECCBC"),
]
LAYOUT = {"9x16": (1080, 1920, "v"), "16x9": (1920, 1080, "h")}


# ---------------- Maskot: Kâşif ----------------
IFADELER = {
    # kaşlar (sol, sağ: y kayması, açı), gözbebeği kayması, göz ölçeği, ağız
    "merakli":   dict(kas=((-6, -12), (-16, 8)), bak=(4, -3), goz=1.0, agiz="o_kucuk", yanak=False, efekt="soru"),
    "saskin":    dict(kas=((-20, 0), (-20, 0)), bak=(0, 0), goz=1.25, agiz="o_buyuk", yanak=False, efekt="unlem"),
    "mutlu":     dict(kas=((-8, 6), (-8, -6)), bak=(0, 2), goz=1.0, agiz="gulumse", yanak=True, efekt=""),
    "dusunceli": dict(kas=((-4, 10), (-12, -4)), bak=(-6, -8), goz=0.95, agiz="duz", yanak=False, efekt="dusunce"),
    "heyecanli": dict(kas=((-16, 8), (-16, -8)), bak=(0, 0), goz=1.15, agiz="kocaman", yanak=True, efekt="yildiz"),
    "gulen":     dict(kas=((-10, 6), (-10, -6)), bak=(0, 0), goz=0.0, agiz="kocaman", yanak=True, efekt=""),
    "korkmus":   dict(kas=((-14, -14), (-14, 14)), bak=(0, 4), goz=1.1, agiz="dalga", yanak=False, efekt="ter"),
}


def mascot_svg(ifade="merakli"):
    f = IFADELER.get(ifade, IFADELER["merakli"])
    INK, SKIN, HAIR, COAT, SCARF, HAT = "#1B1530", "#FFD3A8", "#5A3418", "#FFFFFF", "#FF6B4A", "#3FA66B"
    (k1y, k1a), (k2y, k2a) = f["kas"]
    bx, by = f["bak"]
    g = f["goz"]

    def eye(cx):
        if g == 0:  # mutluluktan kapalı göz ^ ^
            return (f"<path d='M{cx-17} 172 Q{cx} 152 {cx+17} 172' fill='none' stroke='{INK}' stroke-width='7' "
                    f"stroke-linecap='round'/>")
        return (f"<g class='kblink'><ellipse cx='{cx}' cy='168' rx='{17*g:.1f}' ry='{20*g:.1f}' fill='#fff'/>"
                f"<circle cx='{cx+bx}' cy='{168+by}' r='{9*min(g,1.1):.1f}' fill='{INK}'/>"
                f"<circle cx='{cx+bx+3}' cy='{164+by}' r='3.2' fill='#fff'/></g>")

    mouths = {
        "o_kucuk": f"<ellipse cx='150' cy='232' rx='9' ry='11' fill='{INK}'/>",
        "o_buyuk": f"<ellipse cx='150' cy='234' rx='16' ry='20' fill='{INK}'/><ellipse cx='150' cy='244' rx='9' ry='6' fill='#FF7A8A'/>",
        "gulumse": f"<path d='M126 224 Q150 250 174 224' fill='none' stroke='{INK}' stroke-width='7' stroke-linecap='round'/>",
        "duz": f"<path d='M134 232 Q150 228 166 230' fill='none' stroke='{INK}' stroke-width='7' stroke-linecap='round'/>",
        "kocaman": f"<path d='M120 220 Q150 270 180 220 Z' fill='{INK}'/><path d='M136 244 Q150 254 164 244 Q150 236 136 244Z' fill='#FF7A8A'/>",
        "dalga": f"<path d='M128 234 q6 -8 11 0 t11 0 t11 0 t11 0' fill='none' stroke='{INK}' stroke-width='6' stroke-linecap='round'/>",
    }
    efekt = {
        "soru": f"<g class='kfx'><text x='238' y='86' font-size='64' font-weight='900' fill='var(--acc)' stroke='{INK}' stroke-width='3'>?</text></g>",
        "unlem": f"<g class='kfx'><text x='236' y='88' font-size='70' font-weight='900' fill='var(--acc)' stroke='{INK}' stroke-width='3'>!</text><text x='262' y='70' font-size='46' font-weight='900' fill='var(--acc)' stroke='{INK}' stroke-width='3'>!</text></g>",
        "dusunce": f"<g class='kfx'><circle cx='236' cy='92' r='8' fill='#fff'/><circle cx='254' cy='66' r='12' fill='#fff'/><ellipse cx='282' cy='34' rx='30' ry='22' fill='#fff'/></g>",
        "yildiz": "<g class='kfx'>" + "".join(
            f"<path transform='translate({x} {y}) scale({s})' d='M0 -16 L4 -5 L16 -5 L6 2 L10 14 L0 6 L-10 14 L-6 2 L-16 -5 L-4 -5Z' fill='var(--acc)'/>"
            for x, y, s in ((40, 70, 1.2), (262, 80, 1.4), (240, 30, .8))) + "</g>",
        "ter": "<g class='kfx'><path d='M232 120 q8 14 0 22 q-8 -8 0 -22Z' fill='#7ACCFF'/></g>",
        "": "",
    }[f["efekt"]]
    yanak = (f"<ellipse cx='98' cy='208' rx='14' ry='8' fill='#FF8A8A' opacity='.55'/>"
             f"<ellipse cx='202' cy='208' rx='14' ry='8' fill='#FF8A8A' opacity='.55'/>") if f["yanak"] else ""
    el = "kwave" if ifade in ("heyecanli", "gulen", "mutlu") else "kpoint"
    return (
        f"<svg class='kasif' viewBox='0 0 300 400' xmlns='http://www.w3.org/2000/svg'>"
        f"<ellipse cx='150' cy='392' rx='92' ry='10' fill='#000' opacity='.3'/>"
        f"<g class='kbob'>"
        # gövde: önlük + atkı
        f"<path d='M78 400 L86 300 Q150 270 214 300 L222 400Z' fill='{COAT}' stroke='{INK}' stroke-width='6'/>"
        f"<path d='M150 300 L150 400' stroke='#D8DCE8' stroke-width='5'/>"
        f"<circle cx='132' cy='340' r='5' fill='{INK}'/><circle cx='132' cy='370' r='5' fill='{INK}'/>"
        f"<path d='M104 292 Q150 318 196 292 L198 308 Q150 334 102 308Z' fill='{SCARF}' stroke='{INK}' stroke-width='5'/>"
        f"<path d='M176 310 L192 352 L172 350Z' fill='{SCARF}' stroke='{INK}' stroke-width='5' stroke-linejoin='round'/>"
        # sol kol (sabit) + sağ kol (işaret / el sallama)
        f"<path d='M90 312 Q60 340 70 380' fill='none' stroke='{INK}' stroke-width='26' stroke-linecap='round'/>"
        f"<path d='M90 312 Q60 340 70 380' fill='none' stroke='{COAT}' stroke-width='16' stroke-linecap='round'/>"
        f"<circle cx='70' cy='382' r='13' fill='{SKIN}' stroke='{INK}' stroke-width='5'/>"
        f"<g class='{el}'><path d='M210 312 Q252 296 264 252' fill='none' stroke='{INK}' stroke-width='26' stroke-linecap='round'/>"
        f"<path d='M210 312 Q252 296 264 252' fill='none' stroke='{COAT}' stroke-width='16' stroke-linecap='round'/>"
        f"<circle cx='265' cy='244' r='15' fill='{SKIN}' stroke='{INK}' stroke-width='5'/>"
        f"<path d='M268 232 L270 210' stroke='{INK}' stroke-width='12' stroke-linecap='round'/>"
        f"<path d='M268 232 L270 210' stroke='{SKIN}' stroke-width='5' stroke-linecap='round'/></g>"
        # baş
        f"<circle cx='150' cy='180' r='92' fill='{SKIN}' stroke='{INK}' stroke-width='7'/>"
        f"<ellipse cx='58' cy='186' rx='14' ry='20' fill='{SKIN}' stroke='{INK}' stroke-width='6'/>"
        f"<ellipse cx='242' cy='186' rx='14' ry='20' fill='{SKIN}' stroke='{INK}' stroke-width='6'/>"
        # saç perçemi
        f"<path d='M84 128 Q100 96 150 100 Q206 100 220 136 Q190 118 168 126 Q160 108 140 122 Q118 112 84 128Z' fill='{HAIR}' stroke='{INK}' stroke-width='5'/>"
        # kâşif şapkası
        f"<path d='M62 112 Q150 86 238 112 L232 126 Q150 104 68 126Z' fill='{HAT}' stroke='{INK}' stroke-width='6' stroke-linejoin='round'/>"
        f"<path d='M92 110 Q96 40 150 36 Q204 40 208 110 Q150 94 92 110Z' fill='{HAT}' stroke='{INK}' stroke-width='6'/>"
        f"<path d='M96 96 Q150 82 204 96' fill='none' stroke='#2B7A4C' stroke-width='10'/>"
        # gözler + kocaman gözlük
        f"{eye(112)}{eye(188)}"
        f"<circle cx='112' cy='168' r='32' fill='none' stroke='{INK}' stroke-width='7'/>"
        f"<circle cx='188' cy='168' r='32' fill='none' stroke='{INK}' stroke-width='7'/>"
        f"<path d='M144 166 Q150 160 156 166' fill='none' stroke='{INK}' stroke-width='6'/>"
        # kaşlar
        f"<path transform='translate(0 {k1y}) rotate({k1a} 112 128)' d='M94 128 Q112 120 130 128' fill='none' stroke='{INK}' stroke-width='8' stroke-linecap='round'/>"
        f"<path transform='translate(0 {k2y}) rotate({k2a} 188 128)' d='M170 128 Q188 120 206 128' fill='none' stroke='{INK}' stroke-width='8' stroke-linecap='round'/>"
        f"{yanak}<path d='M146 200 Q150 208 156 202' fill='none' stroke='#C98A64' stroke-width='5' stroke-linecap='round'/>"
        f"<g class='kmouth'>{mouths[f['agiz']]}</g>"
        f"{efekt}</g></svg>")


# ---------------- Seslendirme ----------------
def ensure_model(voice):
    d = os.path.join(MODELS, f"vits-piper-tr_TR-{voice}-medium")
    if not os.path.exists(d):
        os.makedirs(MODELS, exist_ok=True)
        url = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-{voice}-medium.tar.bz2"
        subprocess.run(f"curl -sSL -m 600 '{url}' | tar xj -C '{MODELS}'", shell=True, check=True)
    return d


def synth(texts, voice, speed):
    import sherpa_onnx
    d = ensure_model(voice)
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{d}/tr_TR-{voice}-medium.onnx",
                                                    tokens=f"{d}/tokens.txt", data_dir=f"{d}/espeak-ng-data"),
        num_threads=4))
    tts = sherpa_onnx.OfflineTts(cfg)
    out = []
    for t in texts:
        a = tts.generate(t, sid=0, speed=speed)
        s = np.asarray(a.samples, dtype=np.float32)
        idx = np.where(np.abs(s) > 0.02 * np.abs(s).max())[0]
        s = s[max(0, idx[0] - 300): idx[-1] + 600]
        n = int(len(s) * SR / a.sample_rate)
        s = np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype(np.float32)
        out.append(s / max(1e-6, np.sqrt(np.mean(s ** 2))) * 0.13)
    return out


def load_voice_file(path, texts):
    """Hazır ses dosyasını (ör. ElevenLabs mp3, tüm anlatım tek parça) sahnelere böler."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    s = np.frombuffer(raw, dtype=np.float32).copy()
    hop = int(0.02 * SR)
    env = np.array([np.sqrt(np.mean(s[i:i + hop] ** 2)) for i in range(0, len(s) - hop, hop)])
    quiet = env < max(1e-4, 0.06 * np.percentile(env, 95))
    gaps, i = [], 0
    while i < len(quiet):  # en az 0.3 sn sessizlikler
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - i) * 0.02 >= 0.3:
                gaps.append(((i + j) / 2 * 0.02, (j - i) * 0.02))
            i = j
        else:
            i += 1
    voiced = np.where(~quiet)[0]
    t_a, t_b = voiced[0] * 0.02, voiced[-1] * 0.02 + 0.02
    wc = [len(t.split()) for t in texts]
    cuts, used = [], set()
    for k in range(1, len(texts)):
        exp = t_a + (t_b - t_a) * sum(wc[:k]) / sum(wc)
        cand = [(abs(g[0] - exp) - 0.5 * g[1], gi) for gi, g in enumerate(gaps) if gi not in used and
                (not cuts or g[0] > cuts[-1])]
        if not cand:
            cuts.append(exp)
            continue
        _, gi = min(cand)
        used.add(gi)
        cuts.append(gaps[gi][0])
    bounds = [0.0] + cuts + [len(s) / SR]
    out = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        seg = s[int(a * SR):int(b * SR)]
        idx = np.where(np.abs(seg) > 0.02 * np.abs(seg).max())[0]
        seg = seg[max(0, idx[0] - 600): idx[-1] + 1200]
        out.append((seg / max(1e-6, np.sqrt(np.mean(seg ** 2))) * 0.13).astype(np.float32))
    return out


def word_times(text, t0, dur):
    ws = []
    for w in text.split():
        core = re.sub(r"[^\w]", "", w)
        pause = 4.5 if re.search(r"[.!?;:]$", w) else (2.5 if w.endswith(",") else 0)
        ws.append((w, max(1, len(core)) + 1.5, pause))
    total = sum(a + b for _, a, b in ws) - ws[-1][2]
    k, t, out = dur / total, t0, []
    for w, wt, p in ws:
        out.append([w, round(t, 3), round(t + wt * k, 3)])
        t += (wt + p) * k
    return out


def chunk(wt):
    res, cur = [], []
    for w in wt:
        cur.append(w)
        if len(cur) >= 3 or len(" ".join(x[0] for x in cur)) >= 17 or re.search(r"[.!?;:,]$", w[0]):
            res.append(cur)
            cur = []
    if cur:
        res.append(cur)
    return [dict(t0=c[0][1], w=c) for c in res]


# ---------------- Müzik ve efekt ----------------
def music(total, seed, cues):
    n = int(total * SR) + SR
    rng = np.random.default_rng(seed)
    progs = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],
             [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]],
             [[52, 55, 59], [48, 52, 55], [55, 59, 62], [50, 54, 57]]]
    prog = progs[rng.integers(len(progs))]
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    out, bar = np.zeros(n), 4.0
    for ci in range(int(total / bar) + 2):
        ch, s = prog[ci % 4], int(ci * bar * SR)
        if s >= n:
            break
        e = min(n, s + int((bar + 2) * SR))
        tt = np.arange(e - s) / SR
        env = np.minimum(1, tt / 1.4) * np.exp(-np.maximum(0, tt - bar) / 0.7)
        for m in ch:
            for c in (-7, 7):
                out[s:e] += 0.045 * env * np.sin(2 * np.pi * mtof(m) * 2 ** (c / 1200) * tt)
        out[s:e] += 0.07 * env * np.sin(2 * np.pi * mtof(ch[0] - 12) * tt)
        for k in range(8):
            ps = s + int(k * 0.5 * SR)
            if ps >= n:
                break
            pe = min(n, ps + int(0.9 * SR))
            pt = np.arange(pe - ps) / SR
            f = mtof(ch[k % 3] + 12 + (12 if k % 4 == 3 else 0))
            out[ps:pe] += 0.022 * np.exp(-pt / 0.28) * np.sin(2 * np.pi * f * pt) * np.minimum(1, pt / 0.005)
    out = out[: int(total * SR)]
    out /= max(1e-6, np.abs(out).max())
    for ct in cues:  # geçiş "vuuş" efekti
        i = int(max(0, ct - 0.25) * SR)
        L = int(0.7 * SR)
        nz = rng.standard_normal(L)
        spec = np.fft.rfft(nz)
        fr = np.fft.rfftfreq(L, 1 / SR)
        spec *= np.exp(-((np.log(fr + 1) - np.log(900)) ** 2) / 0.9)
        w = np.fft.irfft(spec, L)
        tt = np.arange(L) / SR
        w *= np.minimum(1, tt / 0.22) * np.exp(-np.maximum(0, tt - 0.22) / 0.12)
        w /= np.abs(w).max() + 1e-9
        seg = out[i:i + L]
        seg += 0.9 * w[: len(seg)]
    fo = int(1.5 * SR)
    out[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))
    out[-fo:] *= np.linspace(1, 0, fo)
    return out.astype(np.float32)


# ---------------- Sayfa şablonu ----------------
CSS = r"""
@property --c{syntax:'<color>';inherits:true;initial-value:#FF7A8A}
*{margin:0;padding:0;box-sizing:border-box}
html,body{overflow:hidden;background:var(--bg2)}
body{position:relative;font-family:'Inter',sans-serif;color:var(--txt);
 background:radial-gradient(120% 80% at 50% 0%,var(--bg1),var(--bg2))}
.blob{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55}
.b1{background:var(--b1);animation:drift1 17s ease-in-out infinite}
.b2{background:var(--b2);animation:drift2 21s ease-in-out infinite}
@keyframes drift1{0%,100%{transform:translate(0,0)}50%{transform:translate(160px,120px)}}
@keyframes drift2{0%,100%{transform:translate(0,0)}50%{transform:translate(-140px,-160px)}}
.pt{position:absolute;border-radius:50%;background:#fff;animation:ptrise linear infinite}
@keyframes ptrise{from{transform:translateY(0);opacity:0}20%{opacity:.5}to{transform:translateY(-700px);opacity:0}}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.45))}
#top{position:absolute;z-index:5}
#bar{display:flex;gap:10px}
.seg{flex:1;height:7px;border-radius:4px;background:rgba(255,255,255,.22);overflow:hidden}
.seg i{display:block;height:100%;width:0;background:var(--acc)}
#label{margin-top:16px;font:600 26px 'Inter';letter-spacing:4px;opacity:.8}
.scene{position:absolute;inset:0;visibility:hidden}
.kicker{font:700 30px 'Inter';letter-spacing:5px;color:var(--acc);text-transform:uppercase}
h1{font-family:'Inter Display','Inter';font-weight:900;line-height:1.04;letter-spacing:-1px;margin-top:14px;
 text-shadow:0 6px 30px rgba(0,0,0,.35)}
h1 em{font-style:normal;color:var(--acc)}
.art{position:absolute}
.art>div{width:100%;height:100%;animation:artin .7s cubic-bezier(.2,.9,.3,1.2) both}
.art svg{width:100%;height:100%;overflow:visible}
@keyframes artin{from{transform:scale(.82) translateY(40px);opacity:0}to{transform:none;opacity:1}}
.mas{position:absolute;z-index:4}
.mas>div{width:100%;height:100%;animation:masin .6s cubic-bezier(.2,1.4,.4,1) both;animation-delay:.08s}
.mas svg{width:100%;height:100%;overflow:visible;filter:drop-shadow(0 10px 24px rgba(0,0,0,.45))}
@keyframes masin{from{transform:translateX(-120%) rotate(-12deg)}to{transform:none}}
.kbob{animation:kbob 1.8s ease-in-out infinite;transform-box:view-box;transform-origin:150px 390px}
@keyframes kbob{0%,100%{transform:translateY(0) rotate(-1.5deg)}50%{transform:translateY(-8px) rotate(1.5deg)}}
.kblink{animation:blink 3.1s infinite}
.kwave{animation:kwave .7s ease-in-out infinite;transform-box:view-box;transform-origin:212px 312px}
@keyframes kwave{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(12deg)}}
.kpoint{animation:kpoint 2.2s ease-in-out infinite;transform-box:view-box;transform-origin:212px 312px}
@keyframes kpoint{0%,100%{transform:rotate(0)}50%{transform:rotate(-8deg)}}
.kfx{animation:kfx 1.4s ease-in-out infinite}
@keyframes kfx{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-8px) scale(1.12)}}
.kmouth{transform-box:fill-box;transform-origin:center}
#subs{position:absolute;z-index:6;font:800 66px/1.18 'Inter';letter-spacing:-.5px;text-shadow:0 4px 22px rgba(0,0,0,.6)}
#subs span{display:inline-block;margin:0 .04em}
#subs span.on{color:var(--acc)}
#subs span.next{opacity:.55}
/* Dikey 9:16 */
body.v{width:1080px;height:1920px}
.v .b1{width:900px;height:900px;left:-250px;top:150px}.v .b2{width:850px;height:850px;right:-300px;top:950px}
.v #top{left:90px;right:90px;top:226px}
.v .hl{position:absolute;left:90px;right:120px;top:330px}
.v h1{font-size:96px}
.v .art{left:250px;top:585px;width:720px;height:720px}
.v .mas{left:10px;top:960px;width:345px;height:460px}
.v #subs{left:70px;right:110px;top:1430px;text-align:center}
/* Yatay 16:9 */
body.h{width:1920px;height:1080px}
.h .b1{width:900px;height:900px;left:-200px;top:-200px}.h .b2{width:900px;height:900px;right:-200px;top:300px}
.h #top{left:140px;right:140px;top:58px}
.h .hl{position:absolute;left:960px;right:120px;top:250px}
.h h1{font-size:88px}
.h .art{left:330px;top:210px;width:600px;height:600px}
.h .mas{left:40px;top:600px;width:270px;height:360px}
.h #subs{left:960px;right:120px;top:640px;text-align:left;font-size:58px}
.h #subs span:first-child{margin-left:0}
/* Animasyon kütüphanesi (SVG içinde class olarak kullan) */
svg *{transform-box:fill-box;transform-origin:center}
.fadeup{animation:fadeup .6s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,0s)}
@keyframes fadeup{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}
.fadein{animation:fadein .5s ease both;animation-delay:var(--d,0s)}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.out{animation:out .35s ease both;animation-delay:var(--d,0s)}
@keyframes out{from{opacity:1}to{opacity:0}}
.pop{animation:pop .65s cubic-bezier(.2,1.5,.4,1) both;animation-delay:var(--d,0s)}
@keyframes pop{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
.float{animation:float 3.2s ease-in-out infinite;animation-delay:var(--d,0s)}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-16px)}}
.sway{animation:sway 2.6s ease-in-out infinite;animation-delay:var(--d,0s);transform-origin:top center}
@keyframes sway{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(7deg)}}
.wave{animation:wave 1s ease-in-out infinite;animation-delay:var(--d,0s);transform-origin:top center}
@keyframes wave{0%,100%{transform:rotate(-22deg)}50%{transform:rotate(18deg)}}
.wiggle{animation:wiggle 1.2s ease-in-out infinite;animation-delay:var(--d,0s)}
@keyframes wiggle{0%,100%{transform:rotate(-10deg)}50%{transform:rotate(10deg)}}
.beat{animation:beat .9s ease-in-out infinite;animation-delay:var(--d,0s)}
@keyframes beat{0%,100%{transform:scale(1)}15%{transform:scale(1.18)}30%{transform:scale(.98)}45%{transform:scale(1.1)}}
.pulse{animation:pulse 1.6s ease-in-out infinite;animation-delay:var(--d,0s)}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
.spin{animation:spin var(--t,10s) linear infinite}
.spinrev{animation:spinrev var(--t,10s) linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes spinrev{to{transform:rotate(-360deg)}}
.orbit{animation:spin var(--t,6s) linear infinite;transform-box:view-box;transform-origin:var(--ox,300px) var(--oy,300px)}
.blink{animation:blink 3.4s infinite;animation-delay:var(--d,0s)}
@keyframes blink{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.1)}}
.rise{animation:rise var(--t,4s) linear infinite;animation-delay:var(--d,0s)}
@keyframes rise{from{transform:translateY(0);opacity:0}15%{opacity:.9}80%{opacity:.6}to{transform:translateY(-380px);opacity:0}}
.draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw var(--t,1.2s) ease-out forwards;animation-delay:var(--d,0s)}
@keyframes draw{to{stroke-dashoffset:0}}
.arc{stroke-dasharray:var(--p) 1;stroke-dashoffset:var(--p);animation:draw var(--t,1.4s) ease-out forwards;animation-delay:var(--d,0s)}
.flow{stroke-dasharray:.05 .05;animation:flow 1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-.2}}
.glow{animation:glow 1.4s ease-in-out infinite;animation-delay:var(--d,0s)}
@keyframes glow{0%,100%{opacity:.3}50%{opacity:1}}
.shift{animation:shift 6s linear infinite}
@keyframes shift{0%,100%{--c:#FF7A8A}25%{--c:#D9B26A}50%{--c:#5FB86A}75%{--c:#8A6CE0}}
.grow{animation:grow .9s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,0s);transform-origin:left center}
@keyframes grow{from{transform:scaleX(0)}}
"""

JS = r"""
const D = window.__DATA; let anims = null, curChunk = -2;
const scenes = [...document.querySelectorAll('.scene')];
const fills = [...document.querySelectorAll('.seg i')];
const subs = document.getElementById('subs');
const allChunks = []; D.scenes.forEach((s,i)=>s.chunks.forEach((c,j)=>allChunks.push({...c, si:i,
  end: j+1<s.chunks.length ? s.chunks[j+1].t0 : s.start+s.dur-0.25})));
function ease(x){x=Math.max(0,Math.min(1,x));return 1-Math.pow(1-x,3)}
function fit(){document.querySelectorAll('h1').forEach(h=>{let fs=parseFloat(getComputedStyle(h).fontSize);
  const max = fs*1.04*2+4; while(h.offsetHeight>max && fs>40){fs-=3;h.style.fontSize=fs+'px'}});}
function init(){scenes.forEach(s=>s.style.visibility='visible'); fit();
  anims=document.getAnimations(); anims.forEach(a=>{a.pause();
  const el=a.effect&&a.effect.target; const sc=el&&el.closest?el.closest('.scene'):null; a._si=sc?+sc.dataset.i:-1;});}
function fmt(n){return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,'.')}
function talking(si,t){const s=D.scenes[si]; return s.words.some(w=>t>=w[1]&&t<w[2]+0.04);}
function seek(t){ if(!anims) init();
  anims.forEach(a=>{const st=a._si<0?0:D.scenes[a._si].start; a.currentTime=Math.max(0,t-st)*1000;});
  D.scenes.forEach((s,i)=>{const el=scenes[i], lt=t-s.start; let o=0;
    if(lt>=0 && lt<s.dur){const last=i==D.scenes.length-1; o=Math.min(ease(lt/0.35), last?1:ease((s.dur-lt)/0.3));}
    el.style.visibility=o>0.002?'visible':'hidden'; el.style.opacity=o;
    const m=el.querySelector('.kmouth'); if(m){const k=talking(i,t)?0.45+0.55*Math.abs(Math.sin(t*17)):1;
      m.style.transform=`scaleY(${k.toFixed(3)})`;}
    el.querySelectorAll('.count').forEach(c=>{const d0=parseFloat(c.dataset.delay||0), du=parseFloat(c.dataset.dur||1.5);
      c.textContent=(c.dataset.pre||'')+fmt(parseFloat(c.dataset.to)*ease((lt-d0)/du))+(c.dataset.suf||'');});
    const f=fills[i]; f.style.width=(lt<=0?0:Math.min(1,lt/s.dur)*100)+'%';});
  let k=-1; allChunks.forEach((c,j)=>{if(t>=c.t0 && t<c.end) k=j;});
  if(k!==curChunk){curChunk=k; subs.innerHTML = k<0?'':allChunks[k].w.map(w=>`<span>${w[0]}</span>`).join(' ');}
  if(k>=0){const c=allChunks[k]; const sp=subs.children; const a=ease((t-c.t0)/0.18);
    subs.style.opacity=a; subs.style.transform=`scale(${0.94+0.06*a})`;
    c.w.forEach((w,j)=>{sp[j].className = (t>=w[1]&&t<w[2]+0.05)?'on':(t<w[1]?'next':'');});}
  return true;}
document.fonts.ready.then(()=>{init(); seek(0); window.__ready=true;});
"""

VARSAYILAN_IFADE = ["saskin", "merakli", "heyecanli", "dusunceli", "mutlu", "gulen"]


def esc_headline(s):
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", HT.escape(s))


def resolve_sync(art, words, start):
    def rep(m):
        key = m.group(1).strip().lower()
        off = 0.0
        if "+" in key:
            key, o = key.split("+", 1)
            off = float(o)
        for w, t0, _ in words:
            if re.sub(r"[^\w]", "", w.lower()).startswith(key):
                return f"{max(0, t0 - start + off):.2f}s"
        return "1.00s"
    return re.sub(r"\{\{([^}]+)\}\}", rep, art)


def build_html(spec, data, cls, pal, seed):
    rng = np.random.default_rng(seed)
    W, H = (1080, 1920) if cls == "v" else (1920, 1080)
    parts = "".join(
        f"<div class='pt' style='left:{rng.uniform(0, W):.0f}px;top:{rng.uniform(H * .3, H):.0f}px;"
        f"width:{s:.0f}px;height:{s:.0f}px;animation-duration:{rng.uniform(9, 16):.1f}s;"
        f"animation-delay:-{rng.uniform(0, 16):.1f}s'></div>" for s in rng.uniform(3, 7, 22))
    segs = "".join("<div class='seg'><i></i></div>" for _ in spec["scenes"])
    sc_html = ""
    for i, (s, d) in enumerate(zip(spec["scenes"], data["scenes"])):
        art = resolve_sync(s.get("art", ""), d["words"], d["start"])
        mas = ""
        if s.get("maskot", True) is not False:
            ifade = s.get("ifade") or VARSAYILAN_IFADE[i % len(VARSAYILAN_IFADE)]
            mas = f"<div class='mas'><div>{mascot_svg(ifade)}</div></div>"
        sc_html += (f"<section class='scene' data-i='{i}'><div class='hl'>"
                    f"<div class='kicker fadeup' style='--d:.1s'>{HT.escape(s.get('kicker', ''))}</div>"
                    f"<h1 class='fadeup' style='--d:.22s'>{esc_headline(s['headline'])}</h1></div>"
                    f"<div class='art'><div>{art}</div></div>{mas}</section>")
    label = f"{spec.get('series', 'Günün Bilgisi')}  ·  {spec['topic']}".replace("i", "İ").replace("ı", "I").upper()
    vars_ = ";".join(f"--{k}:{v}" for k, v in zip(["bg1", "bg2", "b1", "b2", "acc", "txt", "sub"], pal))
    pub = {"scenes": [{k: d[k] for k in ("start", "dur", "chunks", "words")} for d in data["scenes"]]}
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>:root{{{vars_}}}{CSS}</style></head>"
            f"<body class='{cls}'><div class='blob b1'></div><div class='blob b2'></div>{parts}<div id='vig'></div>"
            f"<div id='top'><div id='bar'>{segs}</div><div id='label'>{HT.escape(label)}</div></div>"
            f"{sc_html}<div id='subs'></div>"
            f"<script>window.__DATA={json.dumps(pub, ensure_ascii=False)};{JS}</script></body></html>")


def slugify(s):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return re.sub(r"[^a-z0-9]+", "-", s.translate(tr).lower()).strip("-")[:40] or "video"


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2] if len(sys.argv) > 2 else "cikti"
    preview = "--onizleme" in sys.argv
    os.makedirs(out, exist_ok=True)
    slug = slugify(spec["topic"])
    seed = int(hashlib.md5(spec["topic"].encode()).hexdigest()[:8], 16)
    pal = PALETTES[spec.get("palette", seed % len(PALETTES))]

    texts = [s["narration"] for s in spec["scenes"]]
    if spec.get("voice_file"):
        voices = load_voice_file(spec["voice_file"], texts)
    else:
        voices = synth(texts, spec.get("voice", "fahrettin"), spec.get("speed", 1.0))
    PRE, POST = 0.35, 0.55
    t, data = 0.0, {"scenes": []}
    for i, v in enumerate(voices):
        vd = len(v) / SR
        dur = PRE + vd + POST + (1.4 if i == len(voices) - 1 else 0)
        words = word_times(spec["scenes"][i]["narration"], t + PRE, vd)
        data["scenes"].append(dict(start=round(t, 3), dur=round(dur, 3), vstart=t + PRE, words=words, chunks=chunk(words)))
        t += dur
    total = t

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--font-render-hinting=none", "--disable-lcd-text"])
        if preview:
            from PIL import Image
            shots = []
            for fmt in ("9x16", "16x9"):
                W, H, cls = LAYOUT[fmt]
                pth = os.path.join(out, f".{slug}_{fmt}.html")
                open(pth, "w", encoding="utf-8").write(build_html(spec, data, cls, pal, seed))
                pg = br.new_page(viewport={"width": W, "height": H})
                pg.goto("file://" + os.path.abspath(pth))
                pg.wait_for_function("window.__ready===true")
                for i, s in enumerate(data["scenes"]):
                    if fmt == "16x9" and i not in (1, 3):
                        continue
                    pg.evaluate(f"seek({s['start'] + min(s['dur'] - 0.4, 3.2)})")
                    f = os.path.join(out, f"onizleme_{fmt}_{i + 1}.png")
                    pg.screenshot(path=f)
                    shots.append(f)
                pg.close()
            v = [Image.open(f).resize((360, 640)) for f in shots if "9x16" in f]
            sheet = Image.new("RGB", (len(v) * 370, 640), "white")
            for i, im in enumerate(v):
                sheet.paste(im, (i * 370, 0))
            sheet.save(os.path.join(out, "onizleme_dikey.png"))
            print("Önizleme:", os.path.join(out, "onizleme_dikey.png"), "| süre", round(total, 1), "sn",
                  "| sahneler:", [round(d["dur"], 1) for d in data["scenes"]])
            br.close()
            return

        # Ses: anlatım + müzik + geçiş efektleri
        n = int(total * SR)
        mix = np.zeros(n, np.float32)
        for v, d in zip(voices, data["scenes"]):
            i = int(d["vstart"] * SR)
            mix[i:i + len(v)] += v[: n - i]
        mix += 0.085 * music(total, seed, [d["start"] for d in data["scenes"][1:]])
        mix *= 0.97 / max(1e-6, np.abs(mix).max())
        wav = os.path.join(out, f".{slug}.wav")
        st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
        with wave.open(wav, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

        for fmt in spec.get("formats", ["9x16", "16x9"]):
            W, H, cls = LAYOUT[fmt]
            pth = os.path.join(out, f".{slug}_{fmt}.html")
            open(pth, "w", encoding="utf-8").write(build_html(spec, data, cls, pal, seed))
            pg = br.new_page(viewport={"width": W, "height": H})
            pg.goto("file://" + os.path.abspath(pth))
            pg.wait_for_function("window.__ready===true")
            mp4 = os.path.join(out, f"{slug}_{fmt}.mp4")
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                                   "-c:v", "mjpeg", "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium",
                                   "-crf", "19", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                                   "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest",
                                   "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
            for fi in range(int(total * FPS)):
                pg.evaluate(f"seek({fi / FPS})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
            ff.stdin.close()
            ff.wait()
            if fmt == "9x16":
                s0 = data["scenes"][0]
                pg.evaluate(f"seek({s0['start'] + min(s0['dur'] - 0.5, 2.8)})")
                pg.evaluate("document.getElementById('subs').style.opacity=0")
                pg.screenshot(path=os.path.join(out, f"{slug}_kapak.png"))
            pg.close()
            print(f"{mp4}  ({total:.1f} sn)")
        br.close()
        os.remove(wav)


if __name__ == "__main__":
    main()

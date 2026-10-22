# -*- coding: utf-8 -*-
"""İLK 11 çizim parçaları: kalın hatlı Hoca, gözü bağlı çocuk, kura fanusu, bayraklar, tabela, Kolezyum..."""
import math, random

OL = "#0A0A0A"
LIME = "#C6FF00"
SKIN = "#F3B78F"
SKIN_D = "#E3A07B"
TR_RED = "#E30A17"


def ball(cx, cy, r, pid, line=OL):
    k = r / 46.0
    pts = [(0, -16), (15.2, -4.9), (9.4, 12.9), (-9.4, 12.9), (-15.2, -4.9)]
    outs = [(0, -33), (31.4, -10.2), (19.4, 26.7), (-19.4, 26.7), (-31.4, -10.2)]
    caps = [(0, -46), (43.7, -14.2), (27, 37.2), (-27, 37.2), (-43.7, -14.2)]
    return (f"<g transform='translate({cx} {cy}) scale({k:.3f})'><defs><clipPath id='{pid}'><circle r='46'/></clipPath></defs>"
            f"<circle r='46' fill='#FFFFFF'/><g clip-path='url(#{pid})' fill='{line}'>"
            f"<polygon points='{' '.join(f'{x},{y}' for x, y in pts)}'/>"
            + "".join(f"<circle cx='{x}' cy='{y}' r='14'/>" for x, y in caps) + "</g>"
            + f"<g stroke='{line}' stroke-width='3.5' stroke-linecap='round'>"
            + "".join(f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}'/>" for a, b in zip(pts, outs)) + "</g>"
            f"<circle r='46' fill='none' stroke='{line}' stroke-width='4'/></g>")


def tr_flag(w, wave=False):
    """Türk bayrağı (resmî oran 3:2). Sol üst köşe (0,0)."""
    h = w * 2 / 3
    k = w / 1200
    return (f"<g transform='scale({k:.4f})'><rect width='1200' height='800' fill='{TR_RED}'/>"
            "<circle cx='425' cy='400' r='200' fill='#FFFFFF'/><circle cx='475' cy='400' r='160' fill='" + TR_RED + "'/>"
            "<polygon points='583.334,400 764.235,458.779 652.431,304.894 652.431,495.106 764.235,341.221' fill='#FFFFFF'/></g>")


def es_flag(w):
    h = w * 2 / 3
    return (f"<rect width='{w}' height='{h}' fill='#AA151B'/><rect y='{h / 4:.1f}' width='{w}' height='{h / 2:.1f}' fill='#F1BF00'/>")


def flag_box(kind, x, y, w, extra_cls="", style=""):
    h = w * 2 / 3
    f = tr_flag(w) if kind == "tr" else es_flag(w)
    return (f"<g transform='translate({x} {y})'><g class='{extra_cls}' style='{style}'>"
            f"<rect x='-5' y='-5' width='{w + 10}' height='{h + 10}' rx='6' fill='{OL}'/>{f}</g></g>")


# ---------------- HOCA (kalın hatlı) ----------------
def _arm(d, hand, color="#2F5D50", fist=False, point=False):
    hx, hy = hand
    s = (f"<path d='{d}' stroke='{OL}' stroke-width='84' fill='none' stroke-linecap='round'/>"
         f"<path d='{d}' stroke='{color}' stroke-width='62' fill='none' stroke-linecap='round'/>")
    if point:
        s += (f"<g transform='translate({hx} {hy})'><circle r='34' fill='{SKIN}' stroke='{OL}' stroke-width='9'/>"
              f"<path d='M10 -22 L64 -50' stroke='{OL}' stroke-width='30' stroke-linecap='round'/>"
              f"<path d='M10 -22 L64 -50' stroke='{SKIN}' stroke-width='14' stroke-linecap='round'/></g>")
    else:
        s += f"<circle cx='{hx}' cy='{hy}' r='{38 if fist else 34}' fill='{SKIN}' stroke='{OL}' stroke-width='9'/>"
        if fist:
            s += f"<path d='M{hx - 18} {hy - 6} h36 M{hx - 18} {hy + 8} h36' stroke='{OL}' stroke-width='5' stroke-linecap='round'/>"
    return s


def _hoca_face(expr):
    brows = ("<path d='M-86 -52 Q-56 -72 -20 -58' stroke='#0A0A0A' stroke-width='22' fill='none' stroke-linecap='round'/>"
             "<path d='M-86 -52 Q-56 -72 -20 -58' stroke='#BDBDBD' stroke-width='11' fill='none' stroke-linecap='round'/>"
             "<path d='M20 -58 Q56 -72 86 -52' stroke='#0A0A0A' stroke-width='22' fill='none' stroke-linecap='round'/>"
             "<path d='M20 -58 Q56 -72 86 -52' stroke='#BDBDBD' stroke-width='11' fill='none' stroke-linecap='round'/>")
    eye = lambda x: (f"<g class='blink'><ellipse cx='{x}' cy='6' rx='31' ry='34' fill='#FFFFFF' stroke='{OL}' stroke-width='7'/>"
                     f"<circle cx='{x + 4}' cy='8' r='20' fill='#C77A1E'/><circle cx='{x + 4}' cy='8' r='9.5' fill='#120A05'/>"
                     f"<circle cx='{x + 11}' cy='0' r='6' fill='#FFFFFF'/></g>")
    stache = (f"<path d='M0 70 C-26 60 -60 62 -80 78 C-66 98 -28 94 0 86 C28 94 66 98 80 78 C60 62 26 60 0 70Z' "
              f"fill='#D7D7D7' stroke='{OL}' stroke-width='8' stroke-linejoin='round'/>")
    if expr == "wink":
        eyes = eye(-48) + f"<path d='M20 12 Q50 -16 80 12' stroke='{OL}' stroke-width='11' fill='none' stroke-linecap='round'/>"
    elif expr == "cheer":
        eyes = (f"<path d='M-78 14 Q-48 -18 -18 14' stroke='{OL}' stroke-width='11' fill='none' stroke-linecap='round'/>"
                f"<path d='M18 14 Q48 -18 78 14' stroke='{OL}' stroke-width='11' fill='none' stroke-linecap='round'/>")
    else:
        eyes = eye(-48) + eye(48)
    if expr == "cheer":
        mouth = (f"<ellipse cx='0' cy='112' rx='40' ry='34' fill='#7A2E22' stroke='{OL}' stroke-width='7'/>"
                 "<ellipse cx='-80' cy='66' rx='26' ry='16' fill='#E8745E' opacity='.7'/><ellipse cx='80' cy='66' rx='26' ry='16' fill='#E8745E' opacity='.7'/>")
    else:
        mouth = (f"<path d='M-50 92 Q4 150 56 88 Q4 112 -50 92Z' fill='#7A2E22' stroke='{OL}' stroke-width='7' stroke-linejoin='round'/>"
                 "<path d='M-40 95 Q4 108 46 92 L44 100 Q4 116 -38 103Z' fill='#FFFFFF'/>"
                 "<ellipse cx='-76' cy='60' rx='22' ry='12' fill='#E8745E' opacity='.5'/><ellipse cx='76' cy='60' rx='22' ry='12' fill='#E8745E' opacity='.5'/>")
    nose = "<path d='M-4 26 Q-18 52 -2 60 Q12 63 17 52' stroke='#B8694A' stroke-width='6' fill='none' stroke-linecap='round'/>"
    return brows + eyes + nose + mouth + stache


def hoca(pose="stand", faces=(("smile", None, None),)):
    """Orijin: baş merkezi. Gövde y≈640'a kadar."""
    torso = (f"<path d='M-230 640 C-236 440 -220 320 -186 262 C-160 220 -112 202 -62 196 L62 196 C112 202 160 220 186 262 C220 320 236 440 230 640Z' fill='#2F5D50' stroke='{OL}' stroke-width='12' stroke-linejoin='round'/>"
             "<path d='M-214 340 L-160 244 M-200 362 L-146 262 M214 340 L160 244 M200 362 L146 262' stroke='#FFFFFF' stroke-width='11' stroke-linecap='round'/>"
             f"<path d='M-64 196 L-22 310 L22 310 L64 196 L40 186 L0 220 L-40 186Z' fill='#1F3F36' stroke='{OL}' stroke-width='10' stroke-linejoin='round'/>"
             "<path d='M0 220 L0 640' stroke='#C9D3CF' stroke-width='7'/>"
             f"<rect x='-40' y='110' width='80' height='96' fill='{SKIN_D}' stroke='{OL}' stroke-width='10'/>"
             "<path d='M-34 200 Q-26 300 -66 334 M34 200 Q24 300 -46 334' stroke='#D7262B' stroke-width='6' fill='none'/>"
             f"<g transform='translate(-60 350) rotate(-18)'><rect x='-30' y='-16' width='64' height='34' rx='13' fill='#D9DEE2' stroke='{OL}' stroke-width='7'/>"
             f"<circle cx='-22' cy='2' r='19' fill='#D9DEE2' stroke='{OL}' stroke-width='7'/></g>")
    if pose == "point":
        arms = _arm("M-190 280 Q-226 440 -206 560", (-206, 570)) + _arm("M190 280 Q300 250 330 150", (330, 150), point=True)
    elif pose == "cheer":
        arms = _arm("M-190 280 Q-290 200 -270 40", (-270, 30), fist=True) + _arm("M190 280 Q290 200 270 40", (270, 30), fist=True)
    else:
        arms = _arm("M-190 280 Q-226 440 -206 560", (-206, 570)) + _arm("M190 280 Q226 440 206 560", (206, 570))
    fl = ""
    for expr, on, off in faces:
        inner = _hoca_face(expr)
        if off is not None:
            inner = f"<g class='hide' style='--d:{off:.2f}s'>{inner}</g>"
        fl += f"<g class='{'show' if on is not None else ''}' style='--d:{(on or 0):.2f}s'>{inner}</g>"
    head = ("<circle cx='-114' cy='-22' r='30' fill='#D7D7D7' stroke='#0A0A0A' stroke-width='10'/><circle cx='114' cy='-22' r='30' fill='#D7D7D7' stroke='#0A0A0A' stroke-width='10'/>"
            f"<ellipse cx='-120' cy='16' rx='24' ry='34' fill='{SKIN_D}' stroke='{OL}' stroke-width='10'/><ellipse cx='120' cy='16' rx='24' ry='34' fill='{SKIN_D}' stroke='{OL}' stroke-width='10'/>"
            f"<path d='M0 -124 C74 -124 122 -72 122 0 C122 84 74 142 0 142 C-74 142 -122 84 -122 0 C-122 -72 -74 -124 0 -124Z' fill='{SKIN}' stroke='{OL}' stroke-width='12'/>"
            + fl +
            f"<path d='M-136 -56 C-142 -152 -64 -190 0 -190 C82 -190 144 -152 136 -56 C80 -76 -80 -76 -136 -56Z' fill='#6B5B4B' stroke='{OL}' stroke-width='12' stroke-linejoin='round'/>"
            "<path d='M-90 -152 L-66 -82 M-28 -178 L-20 -80 M42 -178 L32 -80 M100 -150 L82 -80' stroke='#857360' stroke-width='6'/>"
            f"<path d='M-130 -60 C-60 -86 80 -92 214 -62 C186 -28 66 -40 -130 -60Z' fill='#55483B' stroke='{OL}' stroke-width='11' stroke-linejoin='round'/>"
            f"<circle cx='0' cy='-188' r='13' fill='#55483B' stroke='{OL}' stroke-width='8'/>")
    if pose == "cheer":
        return torso + arms + head
    return torso + head + arms


# ---------------- Gözü bağlı çocuk ----------------
def kid(hand=(150, 330), expr="smile", arm_cls="", arm_style=""):
    """Orijin baş merkezi. Sağ kol (izleyiciye göre sağ) hand noktasına uzanır."""
    hx, hy = hand
    shirt = "#F4F1E8"
    s = (f"<path d='M-150 420 C-154 300 -140 230 -110 200 C-80 176 -40 170 0 170 C40 170 80 176 110 200 C140 230 154 300 150 420Z' fill='{shirt}' stroke='{OL}' stroke-width='10' stroke-linejoin='round'/>"
         "<path d='M-70 186 L-80 420 M70 186 L80 420' stroke='#7A4A26' stroke-width='18'/>"
         f"<path d='M-40 168 L0 206 L40 168' fill='none' stroke='{OL}' stroke-width='8' stroke-linejoin='round'/>"
         f"<rect x='-28' y='96' width='56' height='80' fill='{SKIN_D}' stroke='{OL}' stroke-width='8'/>"
         f"<path d='M-140 250 Q-170 340 -150 410' stroke='{OL}' stroke-width='62' fill='none' stroke-linecap='round'/>"
         f"<path d='M-140 250 Q-170 340 -150 410' stroke='{shirt}' stroke-width='44' fill='none' stroke-linecap='round'/>")
    arm = (f"<g class='{arm_cls}' style='{arm_style}'>"
           f"<path d='M120 240 Q{(120 + hx) / 2 + 40:.0f} {(240 + hy) / 2 - 40:.0f} {hx} {hy}' stroke='{OL}' stroke-width='62' fill='none' stroke-linecap='round'/>"
           f"<path d='M120 240 Q{(120 + hx) / 2 + 40:.0f} {(240 + hy) / 2 - 40:.0f} {hx} {hy}' stroke='{shirt}' stroke-width='44' fill='none' stroke-linecap='round'/>"
           f"<circle cx='{hx}' cy='{hy}' r='28' fill='{SKIN}' stroke='{OL}' stroke-width='8'/></g>")
    mouth = ("<path d='M-30 52 Q0 82 30 52' stroke='#7A2E22' stroke-width='9' fill='none' stroke-linecap='round'/>" if expr == "smile"
             else "<ellipse cx='0' cy='62' rx='14' ry='18' fill='#7A2E22' stroke='#0A0A0A' stroke-width='5'/>")
    head = (f"<ellipse cx='-98' cy='8' rx='20' ry='26' fill='{SKIN_D}' stroke='{OL}' stroke-width='8'/><ellipse cx='98' cy='8' rx='20' ry='26' fill='{SKIN_D}' stroke='{OL}' stroke-width='8'/>"
            f"<circle r='100' fill='{SKIN}' stroke='{OL}' stroke-width='10'/>"
            f"<path d='M-100 -6 C-108 -96 -40 -126 6 -124 C70 -122 110 -84 100 -10 C80 -50 50 -64 20 -66 L32 -92 L2 -70 L-14 -98 L-30 -68 C-60 -64 -86 -44 -100 -6Z' fill='#5A3A22' stroke='{OL}' stroke-width='9' stroke-linejoin='round'/>"
            "<ellipse cx='-58' cy='36' rx='18' ry='10' fill='#E8745E' opacity='.55'/><ellipse cx='58' cy='36' rx='18' ry='10' fill='#E8745E' opacity='.55'/>"
            f"<path d='M-104 -18 Q0 -34 104 -18 L104 26 Q0 12 -104 26Z' fill='#FFFFFF' stroke='{OL}' stroke-width='8' stroke-linejoin='round'/>"
            "<path d='M-90 0 Q0 -12 90 0' stroke='#D8D2C2' stroke-width='5' fill='none'/>"
            f"<path d='M104 -4 L146 -30 L140 8Z M104 6 L150 22 L128 44Z' fill='#FFFFFF' stroke='{OL}' stroke-width='7' stroke-linejoin='round'/>"
            "<path d='M-4 26 Q-12 40 0 44' stroke='#B8694A' stroke-width='5' fill='none' stroke-linecap='round'/>" + mouth)
    return s + head + arm


# ---------------- Kura fanusu ----------------
def bowl(r=170, seed=4, papers_cls=""):
    rnd = random.Random(seed)
    papers = ""
    for i in range(12):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0, r * .62)
        x, y = rr * math.cos(a), r * .25 + rr * .55 * math.sin(a)
        papers += (f"<g transform='translate({x:.0f} {y:.0f}) rotate({rnd.uniform(-60, 60):.0f})'>"
                   f"<rect x='-26' y='-14' width='52' height='28' rx='4' fill='#F4EBD8' stroke='#8A7D63' stroke-width='3'/>"
                   "<path d='M-26 0 L26 0' stroke='#CBBFA5' stroke-width='3'/></g>")
    return (f"<ellipse cx='0' cy='{r * .98:.0f}' rx='{r * .8:.0f}' ry='{r * .16:.0f}' fill='#000' opacity='.35'/>"
            f"<circle r='{r}' fill='#BFE6FF' fill-opacity='.16'/>"
            f"<g class='{papers_cls}'>{papers}</g>"
            f"<circle r='{r}' fill='none' stroke='#FFFFFF' stroke-opacity='.75' stroke-width='9'/>"
            f"<path d='M{-r * .7:.0f} {-r * .35:.0f} A{r * .8:.0f} {r * .8:.0f} 0 0 1 {-r * .1:.0f} {-r * .78:.0f}' stroke='#FFFFFF' stroke-opacity='.8' stroke-width='14' fill='none' stroke-linecap='round'/>"
            f"<ellipse cx='0' cy='{-r * .86:.0f}' rx='{r * .48:.0f}' ry='{r * .13:.0f}' fill='#0E1A22' fill-opacity='.5' stroke='#FFFFFF' stroke-opacity='.85' stroke-width='9'/>")


def paper(w=90, label=None, flag=None):
    s = (f"<rect x='{-w / 2}' y='{-w * .32:.0f}' width='{w}' height='{w * .64:.0f}' rx='6' fill='#F4EBD8' stroke='{OL}' stroke-width='5'/>"
         f"<path d='M{-w / 2} 0 L{w / 2} 0' stroke='#CBBFA5' stroke-width='4'/>")
    if flag:
        fw = w * .42
        s += f"<g transform='translate({-fw / 2:.0f} {-fw / 3:.0f})'>{tr_flag(fw) if flag == 'tr' else es_flag(fw)}</g>"
    return s


# ---------------- Mekânlar ----------------
def colosseum(y0=760, color="#2A1A2E"):
    s = f"<path d='M60 {y0 + 330} L60 {y0 + 60} Q540 {y0 - 60} 1020 {y0 + 60} L1020 {y0 + 330}Z' fill='{color}'/>"
    for row, (yy, hh, n) in enumerate(((y0 + 70, 70, 13), (y0 + 165, 72, 13), (y0 + 262, 60, 13))):
        for i in range(n):
            x = 100 + i * 70
            s += f"<path d='M{x} {yy + hh} L{x} {yy + 18} A22 22 0 0 1 {x + 44} {yy + 18} L{x + 44} {yy + hh}Z' fill='#F7A04A' opacity='{.55 - row * .12:.2f}'/>"
    return s


def stopwatch(r=110):
    return (f"<rect x='-22' y='{-r - 40}' width='44' height='34' rx='8' fill='#D9DEE2' stroke='{OL}' stroke-width='8'/>"
            f"<circle r='{r}' fill='#FFFFFF' stroke='{OL}' stroke-width='14'/>"
            + "".join(f"<line x1='0' y1='{-r + 14}' x2='0' y2='{-r + 30}' stroke='{OL}' stroke-width='7' transform='rotate({i * 30})'/>" for i in range(12))
            + f"<path d='M0 0 L0 {-r + 22} A{r - 22} {r - 22} 0 0 1 {(r - 22):.0f} 0Z' fill='{LIME}' opacity='.8'/>"
            f"<circle r='12' fill='{OL}'/>")


def confetti(cx, cy, d, n=60, seed=7):
    rnd = random.Random(seed)
    s = f"<g transform='translate({cx} {cy})'>"
    cols = [TR_RED, "#FFFFFF", LIME, "#FFD54A"]
    for i in range(n):
        a = rnd.uniform(-math.pi, 0) if i % 3 else rnd.uniform(0, 2 * math.pi)
        L = rnd.uniform(250, 620)
        dx, dy = L * math.cos(a), L * math.sin(a) + rnd.uniform(150, 450)
        w, h = rnd.uniform(14, 26), rnd.uniform(8, 14)
        s += (f"<g class='confetti' style='--d:{d + rnd.uniform(0, .25):.2f}s;--dx:{dx:.0f}px;--dy:{dy:.0f}px;--r:{rnd.uniform(-540, 540):.0f}deg'>"
              f"<rect x='{-w / 2:.0f}' y='{-h / 2:.0f}' width='{w:.0f}' height='{h:.0f}' rx='3' fill='{rnd.choice(cols)}'/></g>")
    return s + "</g>"

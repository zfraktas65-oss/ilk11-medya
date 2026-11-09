#!/usr/bin/env python3
"""Düz (açık gri/beyaz) zeminli çizimden karakter(ler)i kesip şeffaf PNG yapar.

  python3 kes.py girdi.png cikti.png              # tek karakter (en büyük parça)
  python3 kes.py girdi.png klasor/ ad1,ad2,ad3     # soldan sağa birden fazla karakter
"""
import sys, os
import cv2, numpy as np
from PIL import Image

def mask_of(img):
    h, w = img.shape[:2]
    border = np.concatenate([img[:20].reshape(-1, 3), img[-20:].reshape(-1, 3), img[:, :20].reshape(-1, 3), img[:, -20:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    diff = np.abs(img.astype(np.int16) - bg.astype(np.int16)).max(axis=2)
    near = (diff < 22).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(near, connectivity=4)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    bgm = np.zeros((h, w), np.uint8)
    for i in range(1, n):
        if i in edge or (stats[i, cv2.CC_STAT_AREA] > 1500 and diff[lab == i].mean() < 8):
            bgm[lab == i] = 1
    fg = cv2.morphologyEx(1 - bgm, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return cv2.erode(fg, np.ones((3, 3), np.uint8), iterations=1)

def clean(rgba):
    a = (rgba[:, :, 3] > 10).astype(np.uint8)
    k, lab, st, _ = cv2.connectedComponentsWithStats(a, connectivity=8)
    if k > 2:
        areas = st[1:, cv2.CC_STAT_AREA]; mx = areas.max()
        keep = np.isin(lab, [i + 1 for i, ar in enumerate(areas) if ar > 0.02 * mx])
        rgba[:, :, 3] = (rgba[:, :, 3] * keep).astype(np.uint8)
    ys, xs = np.where(rgba[:, :, 3] > 0)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def main():
    src, out = sys.argv[1], sys.argv[2]
    names = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    img = cv2.imread(src)
    fg = mask_of(img)
    alpha = cv2.GaussianBlur(fg.astype(np.float32), (3, 3), 0)
    rgba = np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (alpha * 255).astype(np.uint8)])
    if not names:
        Image.fromarray(clean(rgba)).save(out); print("kaydedildi:", out); return
    os.makedirs(out, exist_ok=True)
    occ = fg.sum(axis=0) > 3
    segs, inside = [], False
    for x in range(len(occ)):
        if occ[x] and not inside: s = x; inside = True
        elif not occ[x] and inside: segs.append((s, x)); inside = False
    if inside: segs.append((s, len(occ)))
    segs = [g for g in segs if g[1] - g[0] > 80]
    if len(segs) != len(names):
        print(f"UYARI: {len(segs)} parça bulundu, {len(names)} ad verildi; karakterler birbirine değiyor olabilir.")
    for name, (x0, x1) in zip(names, segs):
        sub = rgba[:, max(0, x0 - 6):x1 + 6].copy()
        p = os.path.join(out, f"{name}.png"); Image.fromarray(clean(sub)).save(p); print("kaydedildi:", p)

if __name__ == "__main__":
    main()

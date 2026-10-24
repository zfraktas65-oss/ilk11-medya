# -*- coding: utf-8 -*-
"""İLK 11 · Kişi fotoğrafının arka planını kaldırır (şeffaf PNG, kişiye göre kırpılmış).

Kullanım:  python3 motor/kesik.py motor/fotolar/okan-buruk-2025.jpg [daha fazla dosya ...]
Çıktı:     motor/fotolar/kesik/<ad>.png  (zaten varsa yeniden üretmez; --yeniden ile zorla)

Kurulum (bir kez): pip install --break-system-packages -q "rembg[cpu]"
Model (isnet-general-use, ~170 MB) ilk çalıştırmada GitHub'dan indirilir.
Kaynak fotoğrafın lisans kuralları aynen geçerlidir (bkz. fotolar/KAYNAK.txt); kredi yine zorunludur.
"""
import os, sys

KOK = os.path.dirname(os.path.abspath(__file__))
HEDEF = os.path.join(KOK, "fotolar", "kesik")
_oturum = None


def kes(girdi, yeniden=False):
    """Girdi fotoğrafın kesik PNG yolunu döndürür (gerekirse üretir)."""
    global _oturum
    from PIL import Image
    ad = os.path.splitext(os.path.basename(girdi))[0]
    os.makedirs(HEDEF, exist_ok=True)
    cikti = os.path.join(HEDEF, ad + ".png")
    if os.path.exists(cikti) and not yeniden:
        return cikti
    from rembg import remove, new_session
    if _oturum is None:
        _oturum = new_session("isnet-general-use")
    im = Image.open(girdi).convert("RGB")
    o = remove(im, session=_oturum, post_process_mask=True)
    a = o.getchannel("A").point(lambda v: 255 if v > 24 else 0)
    kutu = a.getbbox()
    if not kutu:
        raise SystemExit(f"{girdi}: kişi bulunamadı")
    o = o.crop(kutu)
    if max(o.size) > 1400:
        o.thumbnail((1400, 1400))
    o.save(cikti, optimize=True)
    return cikti


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); sys.exit(1)
    for f in args:
        print(kes(f, "--yeniden" in sys.argv))

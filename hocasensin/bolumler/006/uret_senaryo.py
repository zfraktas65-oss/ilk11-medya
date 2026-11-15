#!/usr/bin/env python3
"""Bölüm 6 senaryosu (elle üretim, 2026-11-15). Çalıştır: python3 uret_senaryo.py → senaryo.json"""
import json, copy, os
B = os.path.dirname(os.path.abspath(__file__))
K = os.path.dirname(os.path.dirname(B))
t = json.load(open(os.path.join(K, "taraftarlar.json")))
isim = json.load(open("/home/claude/work/b6_isimler.json"))

# ---------------------------------------------------------------- lig tablosu (5. hafta)
d = json.load(open(os.path.join(K, "durum.json")))
tab = {r["takim"]: dict(r) for r in d["lig_tablosu"]["takimlar"]}
eski = [r["takim"] for r in sorted(tab.values(), key=lambda r: (-r["P"], -(r["AG"] - r["YG"]), -r["AG"]))]
SONUC = [("ANADOLUSPOR", 2, 2, "BERBER FK"), ("MUHTARLIK GENÇLİK", 2, 0, "FIRIN SPOR"),
         ("BAKKAL GÜCÜ", 1, 1, "PAZAR YILDIZ"), ("SANAYİ DEMİR", 0, 1, "KAHVECİ SPOR")]
for a, ga, gb, b in SONUC:
    for x, gx, gy in ((a, ga, gb), (b, gb, ga)):
        r = tab[x]; r["O"] += 1; r["AG"] += gx; r["YG"] += gy
        if gx > gy: r["G"] += 1; r["P"] += 3
        elif gx == gy: r["B"] += 1; r["P"] += 1
        else: r["M"] += 1
yeni = sorted(tab.values(), key=lambda r: (-r["P"], -(r["AG"] - r["YG"]), -r["AG"]))
def av(r):
    v = r["AG"] - r["YG"]; return f"+{v}" if v > 0 else str(v)
satirlar = [[r["takim"], r["O"], r["G"], r["B"], r["M"], av(r), r["P"]] for r in yeni]
eski_sira = eski.index("ANADOLUSPOR") + 1; yeni_sira = [r["takim"] for r in yeni].index("ANADOLUSPOR") + 1
rozet = "" if eski_sira == yeni_sira else (f"▲{eski_sira - yeni_sira}" if yeni_sira < eski_sira else f"▼{yeni_sira - eski_sira}")
json.dump({"takimlar": yeni, "eski": eski, "anadoluspor_sira": yeni_sira, "onceki_sira": eski_sira,
           "sonuclar": [f"{a.title()} {ga}-{gb} {b.title()}" for a, ga, gb, b in SONUC]},
          open(os.path.join(B, "_lig.json"), "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- yardımcılar
def et(metin, bas, y, boyut=56, renk="siyah", zemin="sari", egim=-2, **kw):
    o = {"tip": "etiket", "metin": metin, "boyut": boyut, "renk": renk, "zemin": zemin, "egim": egim, "bas": bas, "y": y}; o.update(kw); return o
def baslik2(m1, m2, bas):
    return [et(m1, bas, 270, anim="down"), et(m2, bas, 380, boyut=40, renk="beyaz", zemin="mor", egim=2)]
def oy(ad, u, alt, bas, x, on, faz, boy=28):
    h, ayak = (640, 1560) if on else (560, 1385)
    return {"ad": ad, "x": x, "ayak": ayak, "h": h, "giris": "pop", "sure": 0.25, "bas": bas, "faz": faz,
            "etiket": u, "etiket_alt": alt, "etiket_boyut": boy}
def oy3(ad, u, alt, bas, x, on, faz):
    h, ayak = (700, 1580) if on else (620, 1450)
    return {"ad": ad, "x": x, "ayak": ayak, "h": h, "giris": "pop", "sure": 0.25, "bas": bas, "faz": faz,
            "etiket": u, "etiket_alt": alt, "etiket_boyut": 30}
def skor(e, dp, dk, bas, **kw):
    o = {"tip": "skor", "ev": "ANADOLUSPOR", "dep": "BERBER FK", "ev_skor": e, "dep_skor": dp, "dakika": dk, "bas": bas, "y": 280}; o.update(kw); return o
Z = lambda a, b: [a, b]
S = []

# 0 kanca
S.append({"bas": 0, "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.12], "merkez": [[0.5, 0.5], [0.5, 0.56]], "tribun": {"sayi": 60, "tohum": 4},
          "karakterler": [{"ad": "karaduman_baskan", "x": 560, "ayak": 1720, "h": 960, "giris": "up", "sure": 0.5, "bas": "w:3"}],
          "ogeler": [{"tip": "seri", "bolum": 6, "bas": 0.05, "y": 260, "anim": "down"},
                     {"tip": "damga", "metin": "ZİRVEDE DEPREM!", "boyut": 96, "egim": -8, "bas": "w:1", "y": 560, "anim": "stamp"},
                     et("KİBİRLİ BİR KOMŞU GELDİ...", "w:4", 730, boyut=46, renk="beyaz", zemin="mor", egim=2)]})
# 1 takip
S.append({"bas": "w:7-0.05", "arka": "eski_stadyum", "zoom": [1.04, 1.1], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [{"ad": "cem", "x": 540, "ayak": 1700, "h": 900}],
          "ogeler": [et("TAKİP ET", "w:7", 320, boyut=84, nabiz=True), et("YORUMUNA MEVKİNİ YAZ", "w:9", 460, boyut=48, renk="beyaz", zemin="mor", egim=2)]})
# 2 gün 6
S.append({"bas": "w:12-0.05", "arka": "eski_stadyum", "bulanik": 4, "zoom": [1.04, 1.1], "merkez": Z([0.5, 0.5], [0.5, 0.5]),
          "karakterler": [{"ad": "necmi", "x": 820, "ayak": 1700, "h": 880}],
          "ogeler": [{"tip": "baslik", "metin": "GÜN 6", "boyut": 230, "bas": "w:12", "bitis": "w:14-0.05", "y": 420, "anim": "stamp"},
                     {"tip": "begeni", "metin": "45 BEĞENİ", "bas": "w:16", "x": 360, "y": 470},
                     {"tip": "begeni", "metin": "125 YORUM", "zemin": "mavi", "bas": "w:19", "x": 380, "y": 640},
                     {"tip": "begeni", "metin": "+4.500 TL", "zemin": "mor", "bas": "w:25", "x": 380, "y": 810}]})
# 3 karar 5
S.append({"bas": "w:30-0.05", "arka": "eski_stadyum", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.6], [0.5, 0.6]),
          "karakterler": [{"ad": "otobus_morsari", "x": 540, "ayak": 1620, "h": 640}],
          "ogeler": [et("KARAR #5 TUTMADI", "w:30", 300, boyut=64, renk="beyaz", zemin="kirmizi", egim=-3, anim="stamp"),
                     et("HEDEF 260 · GELEN 45", "w:32", 430, boyut=46, renk="beyaz", zemin="mor", egim=2),
                     et("MOR-SARI OTOBÜSLE DEVAM", "w:36", 560, boyut=44),
                     {"tip": "damga", "metin": "PARA SAHAYA!", "boyut": 100, "egim": -8, "bas": "w:40", "y": 1500, "anim": "stamp"}]})
# 4 ısrar edenler
S.append({"bas": "w:42-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.5]),
          "karakterler": [{"ad": "cem", "x": 540, "ayak": 1700, "h": 900, "giris": "right", "kos": True}],
          "ogeler": [et("EN ÇOK ISRAR EDENLER", "w:42", 300, boyut=60), {"tip": "damga", "metin": "BUGÜN SAHADA!", "boyut": 100, "egim": -6, "bas": "w:44", "y": 470, "anim": "stamp"}]})
# 5 ilk 11 grup 1: kaleci, sol bek, stoper, stoper
S.append({"bas": "w:46-0.05", "arka": "eski_stadyum", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_solbek", "esedli_erdogan", "SOL BEK", "w:50", 410, False, 0.2),
                          oy("oyuncu_stoper2", "mertefegulsadik", "STOPER", "w:52", 920, False, 0.6),
                          oy("taraftar_kaleci", "enesardakaya20", "KALECİ", "w:48", 160, True, 0.0),
                          oy("oyuncu_stoper", "halbayevmurat", "STOPER", "w:51", 670, True, 0.4)],
          "ogeler": baslik2("İLK 11 · KALE VE DEFANS", "ŞEMA 4-4-2", "w:46-0.05") + [et("SONUNDA KALEDE!", "w:49", 500, boyut=44, renk="beyaz", zemin="yesil", egim=-4, anim="stamp")]})
# 6 grup 2: sağ bek, sol kanat, 2 orta saha
S.append({"bas": "w:55-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_solkanat", "samet_sw10", "SOL KANAT", "w:57", 410, False, 0.2),
                          oy("oyuncu_forvet_kadin", "hilalcaglaktas", "ORTA SAHA", "w:63", 920, False, 0.6),
                          oy("oyuncu_sagbek", "batuhan.2014", "SAĞ BEK", "w:55", 160, True, 0.0),
                          oy("oyuncu_ortasaha", "turkogluulviye", "ORTA SAHA · ÇINAR TÜRKOĞLU", "w:58", 670, True, 0.4)],
          "ogeler": baslik2("İLK 11 · DEFANS VE ORTA SAHA", "4-4-2", "w:55-0.05") + [{"tip": "damga", "metin": "3. KADIN FUTBOLCUMUZ!", "boyut": 64, "egim": -6, "bas": "w:62", "y": 520, "anim": "stamp"}]})
# 7 grup 3: sağ kanat, 2 forvet
S.append({"bas": "w:66-0.05", "arka": "eski_stadyum_kale", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy3("forvet", "zaesburakaktas.2", "FORVET", "w:69", 540, False, 0.3),
                          oy3("oyuncu_sagkanat", "michel._olise_17", "SAĞ KANAT", "w:66", 215, True, 0.0),
                          oy3("oyuncu_10", "sadettin0687", "FORVET", "w:71", 865, True, 0.6)],
          "ogeler": [et("İLK 11 · HÜCUM HATTI", "w:66-0.05", 270, anim="down")]})
# 8 yedekler 1/2
S.append({"bas": "w:72-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_solkanat", "urfanonur", "SOL KANAT", "w:75", 410, False, 0.2),
                          oy("oyuncu_libero", "mirac_x797", "ORTA SAHA", "w:77", 920, False, 0.6),
                          oy("oyuncu_kaleci2", "mehmetfurkanengin", "YEDEK KALECİ", "w:73", 160, True, 0.0),
                          oy("oyuncu_sagkanat", "firathtm_1907", "KANAT", "w:76", 670, True, 0.4)],
          "ogeler": [et("YEDEKLER · 1 / 2", "w:72-0.05", 270, anim="down")]})
# 9 yedekler 2/2 + tribün lideri
S.append({"bas": "w:78-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.03], "merkez": Z([0.45, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_10", "g.ecee1905", "SAĞ KANAT", "w:79", 410, False, 0.2),
                          oy("tribun_lideri", "melky.ak", "TRİBÜN LİDERİ", "w:86", 920, False, 0.6),
                          oy("oyuncu_forvet_kadin", "hacer.kahraman.735", "ORTA SAHA", "w:78", 160, True, 0.0),
                          oy("forvet", "atlasssay", "FORVET · NO 99", "w:83", 670, True, 0.4)],
          "ogeler": baslik2("YEDEKLER · 2 / 2", "+ TRİBÜN LİDERİ", "w:78-0.05") + [{"tip": "damga", "metin": "99 NUMARA!", "boyut": 80, "egim": -6, "bas": "w:80", "y": 520, "anim": "stamp", "bitis": "w:84-0.05"}]})
# 10 teknik ekip (4)
S.append({"bas": "w:87-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.04], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [{"ad": "cem", "x": 410, "ayak": 1385, "h": 560, "faz": 0.3},
                          {"ad": "yardimci_antrenor2", "x": 920, "ayak": 1385, "h": 560, "faz": 0.6, "etiket": "s_ahinpars", "etiket_alt": "YARDIMCI ANTRENÖR", "etiket_boyut": 26},
                          {"ad": "yardimci_antrenor1", "x": 160, "ayak": 1560, "h": 640, "faz": 0.0, "etiket": "hasan_zengi83", "etiket_alt": "YARDIMCI ANTRENÖR", "etiket_boyut": 26},
                          {"ad": "yedek_antrenor", "x": 670, "ayak": 1560, "h": 640, "giris": "pop", "sure": 0.3, "bas": "w:93", "faz": 0.4, "etiket": "balayevffs", "etiket_alt": "YEDEK ANTRENÖR", "etiket_boyut": 28}],
          "ogeler": baslik2("TEKNİK EKİP", "YENİ İSİM!", "w:87-0.05") + [{"tip": "damga", "metin": "HOŞ GELDİN BALAYEV!", "boyut": 64, "egim": -6, "bas": "w:93", "y": 520, "anim": "stamp"}]})
# 11 kulüp ailesi
S.append({"bas": "w:94-0.05", "arka": "eski_stadyum", "zoom": [1.0, 1.05], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [{"ad": "maskot", "x": 300, "ayak": 1580, "h": 700, "giris": "pop", "sure": 0.3, "bas": "w:98", "faz": 0.0, "etiket": "murat52_70", "etiket_alt": "MASKOT", "etiket_boyut": 30},
                          {"ad": "cayci", "x": 790, "ayak": 1580, "h": 720, "giris": "pop", "sure": 0.3, "bas": "w:101", "faz": 0.5, "etiket": "mustafaefesanal", "etiket_alt": "ÇAYCI", "etiket_boyut": 30}],
          "ogeler": baslik2("KULÜP AİLESİ", "BÜYÜYORUZ!", "w:94-0.05")})
# 12 kasa
S.append({"bas": "w:103-0.05", "arka": "eski_stadyum_soyunma", "bulanik": 10, "karanlik": 0.7, "zoom": [1.06, 1.1], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "ogeler": [{"tip": "kasa", "baslik": "KULÜP KASASI", "satirlar": [["DEVREDEN", "53.200 TL", "mor"], ["45 BEĞENİ × 100 TL", "+4.500 TL"], ["MASKOT KOSTÜMÜ", "−1.200 TL"], ["ÇAY OCAĞI", "−600 TL"]],
                      "kalan": "55.900 TL", "not": "KARAR #5 TUTMADI · PARA SAHAYA", "bas": "w:103", "y": 740},
                     {"tip": "damga", "metin": "55.900 TL", "boyut": 100, "egim": -8, "bas": "w:113", "y": 1225, "anim": "stamp"}]})
# 13 çağrı
S.append({"bas": "w:120-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.03, 1.07], "merkez": Z([0.5, 0.58], [0.5, 0.58]),
          "karakterler": [{"ad": "oyuncu_solkanat", "x": 900, "ayak": 1440, "h": 560, "faz": 0.5}, {"ad": "forvet", "x": 400, "ayak": 1440, "h": 560, "faz": 0.2},
                          {"ad": "taraftar_kaleci", "x": 180, "ayak": 1640, "h": 640, "faz": 0.1}, {"ad": "oyuncu_forvet_kadin", "x": 650, "ayak": 1640, "h": 640, "faz": 0.4}],
          "ogeler": [et("GEÇEN HAFTANIN KADROSU: BURADAYIM!", "w:120", 300, boyut=42, renk="beyaz", zemin="mor", egim=2, bitis="w:125-0.05"),
                     et("YORUM YAP", "w:128", 300, boyut=60, renk="sari", zemin="mor", egim=-3),
                     et("BEĞEN", "w:130", 420, boyut=60, renk="sari", zemin="mor", egim=2),
                     et("PAYLAŞ", "w:131", 540, boyut=60, renk="sari", zemin="mor", egim=-2),
                     et("ARKADAŞINA GÖNDER", "w:132", 660, boyut=60, renk="sari", zemin="mor", egim=2)]})
# 14 forma duvarı
NOS = {"erentepe5858": "1", "tostcuk_3731": "23", "dorukateskosar": "9", "rax6_976": "8", "nurgul_mahir": "10", "muhammed_20__13": "13",
       "dadi_metin_taha": "25", "jsp_2677": "31", "salih_pyrz06": "6"}
fw = isim["forma"][:9]
og = [et("FORMA DUVARI", "w:134-0.05", 270, boyut=60, anim="down")]
for i, u in enumerate(fw):
    og.append({"tip": "forma", "isim": "@" + u, "no": NOS.get(u, str(20 + i)), "genislik": 280, "x": [190, 540, 890][i % 3], "y": [560, 880, 1200][i // 3],
               "bas": round(54.8 + 0.25 * i, 2)})
S.append({"bas": "w:134-0.05", "arka": "eski_stadyum_soyunma", "bulanik": 6, "karanlik": 0.8, "zoom": [1.0, 1.04], "merkez": Z([0.5, 0.5], [0.5, 0.5]), "ogeler": og})
# 15 tribün + toplam taraftar
S.append({"bas": "w:140-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.75, 1.75], "merkez": Z([0.28, 0.5], [0.72, 0.5]),
          "tribun": {"isimler": isim["tribun"][:30], "etiket_boyut": 15, "sayi": 14},
          "ogeler": [{"tip": "sayac", "baslik": "TOPLAM TARAFTAR", "deger": "1.372", "alt": "TRİBÜN 1.026 · LOCA 346", "bas": "w:140", "y": 360}]})
# 16-18 loca
LT = [61.25, 62.95, 64.65]; LM = ["LOCA · 346 KİŞİLİK TEKNİK HEYET", "İSİMLER EKRANDA!", "LOCAYA HOŞ GELDİNİZ"]
for k in range(3):
    S.append({"bas": LT[k], "arka": "eski_stadyum_loca", "zoom": [1.6, 1.6], "merkez": Z([0.42, 0.5], [0.58, 0.5]) if k % 2 == 0 else Z([0.58, 0.5], [0.42, 0.5]),
              "tribun": {"isimler": isim["loca"][20 * k:20 * k + 20], "etiket_boyut": 15, "aralik": 1.3, "tohum": 11 + k},
              "ogeler": [et(LM[k], LT[k], 250, boyut=42, renk="beyaz" if k == 0 else "siyah", zemin="mor" if k == 0 else "sari")]})
# 19 maç başlıyor
S.append({"bas": "w:150-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.52]),
          "karakterler": [{"ad": "forvet", "x": 330, "ayak": 1700, "h": 760, "giris": "left", "sure": 0.4, "kos": True, "bas": "w:151"},
                          {"ad": "oyuncu_10", "x": 760, "ayak": 1700, "h": 740, "giris": "right", "sure": 0.4, "kos": True, "bas": "w:152"}],
          "ogeler": [skor(0, 0, "1'", "w:150"), et("LİG 5. HAFTA · ANADOLU ARENA PARK", "w:150", 450, boyut=42, renk="beyaz", zemin="mor"),
                     {"tip": "isim", "no": "VS", "ad": "BERBER FK", "alt": "ZİRVE YARIŞI", "bas": "w:152", "x": 520, "y": 620}]})
# 20 berber attı
S.append({"bas": "w:154-0.05", "arka": "eski_stadyum_kale", "zoom": [1.04, 1.12], "merkez": Z([0.5, 0.46], [0.5, 0.44]),
          "karakterler": [{"ad": "taraftar_kaleci", "x": 540, "ayak": 1740, "h": 920, "etiket": "enesardakaya20", "etiket_alt": "KALECİ"}],
          "ogeler": [skor(0, 0, "8'", "w:154", bitis="w:157-0.03"), skor(0, 1, "9'", "w:157"),
                     {"tip": "damga", "metin": "BERBER ATTI...", "boyut": 90, "egim": -6, "bas": "w:156", "y": 560, "anim": "stamp"}]})
# 21 orta
S.append({"bas": "w:159-0.05", "arka": "eski_stadyum", "zoom": [1.0, 1.1], "merkez": Z([0.4, 0.55], [0.6, 0.55]),
          "karakterler": [{"ad": "oyuncu_sagkanat", "x": 560, "ayak": 1720, "h": 900, "giris": "left", "sure": 0.35, "kos": True, "etiket": "michel._olise_17", "etiket_alt": "SAĞ KANAT"}],
          "ogeler": [skor(0, 1, "34'", "w:159"), et("ORTA!", "w:161", 560, boyut=90, anim="stamp")]})
# 22 burak gol
S.append({"bas": "w:162-0.05", "arka": "eski_stadyum_kale", "zoom": [1.05, 1.14], "merkez": Z([0.5, 0.5], [0.5, 0.46]),
          "karakterler": [{"ad": "forvet", "x": 540, "ayak": 1740, "h": 960, "giris": "right", "sure": 0.35, "kos": True, "etiket": "zaesburakaktas.2", "etiket_alt": "FORVET"}],
          "ogeler": [skor(0, 1, "35'", "w:162", bitis="w:164-0.03"), skor(1, 1, "35'", "w:164"),
                     {"tip": "baslik", "metin": "GOL!", "boyut": 220, "bas": "w:164", "y": 560, "anim": "stamp", "titre": True}]})
# 23 tekrar
S.append({"bas": "we:165+0.03", "arka": "eski_stadyum_kale", "zoom": [1.3, 1.4], "merkez": Z([0.5, 0.45], [0.5, 0.42]),
          "karakterler": [{"ad": "forvet", "x": 540, "ayak": 1800, "h": 1100, "faz": 0.2}],
          "ogeler": [et("TEKRAR", "we:165+0.05", 300, boyut=60, renk="beyaz", zemin="kirmizi"), skor(1, 1, "35'", "we:165+0.05", y=180)]})
# 24 berber yine önde
S.append({"bas": "w:166-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.06], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [{"ad": "yardimci_antrenor1", "x": 200, "ayak": 1620, "h": 720, "faz": 0.0}, {"ad": "cem", "x": 540, "ayak": 1660, "h": 800, "faz": 0.3},
                          {"ad": "yedek_antrenor", "x": 880, "ayak": 1620, "h": 720, "faz": 0.6}],
          "ogeler": [skor(1, 1, "71'", "w:166", bitis="w:170-0.03"), skor(1, 2, "72'", "w:170"), et("BERBER YİNE ÖNDE", "w:169", 450, boyut=56, renk="beyaz", zemin="kirmizi")]})
# 25 90. dakika sadettin
S.append({"bas": "w:172-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.12], "merkez": Z([0.5, 0.5], [0.5, 0.46]),
          "karakterler": [{"ad": "oyuncu_10", "x": 540, "ayak": 1740, "h": 940, "giris": "left", "sure": 0.35, "kos": True, "bas": "w:173", "etiket": "sadettin0687", "etiket_alt": "FORVET"}],
          "ogeler": [skor(1, 2, "90'", "w:172", bitis="w:175-0.03"), skor(2, 2, "90'", "w:175"), et("90. DAKİKA!", "w:172", 450, boyut=64, renk="beyaz", zemin="mor", bitis="w:175-0.03"),
                     {"tip": "baslik", "metin": "GOL!", "boyut": 220, "bas": "w:175", "y": 560, "anim": "stamp", "titre": True}]})
# 26 tribün 2-2
S.append({"bas": "we:176+0.02", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.5]), "tribun": {"sayi": 80, "tohum": 7},
          "ogeler": [skor(2, 2, "90'", "we:176+0.05"), {"tip": "damga", "metin": "2-2!", "boyut": 160, "egim": -8, "bas": "we:176+0.05", "y": 700, "anim": "stamp"}]})
# 27 enes kurtarış
S.append({"bas": "w:177-0.05", "arka": "eski_stadyum_kale", "zoom": [1.02, 1.12], "merkez": Z([0.5, 0.44], [0.5, 0.44]),
          "karakterler": [{"ad": "taraftar_kaleci", "x": 540, "ayak": 1740, "h": 920, "etiket": "enesardakaya20", "etiket_alt": "KALECİ"}],
          "ogeler": [skor(2, 2, "90+3'", "w:177"), {"tip": "damga", "metin": "DEV KURTARIŞ!", "boyut": 100, "egim": -8, "bas": "w:181", "y": 580, "anim": "stamp"}]})
# 28 puan tablosu
S.append({"bas": "we:182+0.15", "altyazi_y": False, "arka": "eski_stadyum_gece", "bulanik": 10, "karanlik": 0.7, "zoom": [1.04, 1.08], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "ogeler": [{"tip": "puan", "baslik": "HALI SAHA LİGİ · 5. HAFTA", "satirlar": satirlar, "eski": eski, "vurgu": "ANADOLUSPOR", "rozet": rozet,
                      "alt": "ŞAMPİYON 5 GALİBİYETLE ÜST LİGE ÇIKAR", "bas": "we:182+0.2", "gecikme": 1.6, "kayma": 1.1, "y": 830},
                     et("ANADOLUSPOR 2-2 BERBER FK", "we:182+0.2", 300, boyut=50, renk="beyaz", zemin="mor"),
                     et("MUHTARLIK ZİRVEDE · BİZ 2.YİZ", "w:184", 1320, boyut=52, renk="beyaz", zemin="kirmizi", egim=-3, anim="stamp", bitis="w:189-0.05"),
                     et("9 PUANLA İKİNCİYİZ", "w:190", 1320, boyut=60, egim=-3, anim="stamp")]})
# 29 karaduman başkanı
S.append({"bas": "w:193-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.1], "merkez": Z([0.5, 0.55], [0.5, 0.5]), "tribun": {"sayi": 50, "tohum": 3},
          "karakterler": [{"ad": "karaduman_baskan", "x": 560, "ayak": 1740, "h": 980, "giris": "up", "sure": 0.5, "bas": "w:196"}],
          "ogeler": [et("TRİBÜNDE BİRİ VAR...", "w:193", 300, boyut=56, renk="beyaz", zemin="mor"),
                     {"tip": "pankart", "metin": "KARADUMAN GÜCÜ", "zemin": [30, 30, 30], "renk": [255, 140, 0], "egim": -3, "bas": "w:197", "y": 450},
                     et("BAŞKAN", "w:199", 600, boyut=48, renk="siyah", zemin="beyaz", egim=3)]})
# 30 meydan okuma
S.append({"bas": "w:200-0.05", "arka": "eski_stadyum_uzak", "zoom": [1.0, 1.12], "merkez": Z([0.5, 0.55], [0.5, 0.6]),
          "karakterler": [{"ad": "karaduman_baskan", "x": 540, "ayak": 1800, "h": 1150, "faz": 0.2}],
          "ogeler": [{"tip": "damga", "metin": "MEYDAN OKUDU!", "boyut": 100, "egim": -8, "bas": "w:203", "y": 320, "anim": "stamp"},
                     {"tip": "pankart", "metin": "KOMŞU DERBİSİ GELİYOR!", "zemin": [30, 30, 30], "renk": [255, 140, 0], "egim": 3, "bas": "w:205", "y": 500},
                     et("2 BÖLÜM SONRA · KUPA MAÇI", "w:206", 640, boyut=42, renk="beyaz", zemin="mor", egim=-2)]})
# 31 saha oylaması (6 seçenek)
SEC = d["saha"]["acik_oylama"]["secenekler"]
KISA = {1: "KALE DİREKLERİ + FİLE", 2: "TRİBÜN BOYASI", 3: "PROJEKTÖRLER", 4: "TRİBÜNE +50 KOLTUK", 5: "SAHA ÇİMLERİ", 6: "YENİ TRİBÜN KOLTUKLARI"}
og = [et("PARA SAHAYA AYRILDI", "w:208", 280, boyut=52, renk="beyaz", zemin="mor"), et("SAHADA NEYİ DEĞİŞTİRELİM?", "w:211", 390, boyut=56)]
SB = ["w:214", "w:215", "w:216", "w:218", "w:219", "w:221"]
for i, s in enumerate(SEC):
    og.append(et(f"{s['no']}) {KISA[s['no']]} · {s['tl']:,} TL".replace(",", "."), SB[i], 530 + 105 * i, boyut=40, renk="siyah", zemin="beyaz", egim=0 if i % 2 else -1))
og.append(et("YORUMUNA NUMARANI YAZ: 1–6", "w:222", 1200, boyut=46, renk="sari", zemin="mor", egim=-2, anim="stamp"))
S.append({"bas": "w:208-0.05", "arka": "eski_stadyum_gece", "bulanik": 6, "karanlik": 0.75, "zoom": [1.0, 1.06], "merkez": Z([0.5, 0.45], [0.5, 0.42]), "altyazi_y": 1450, "ogeler": og})
# 32 karar 6
S.append({"bas": "w:224-0.05", "arka": "eski_stadyum_kale", "bulanik": 6, "karanlik": 0.75, "zoom": [1.05, 1.12], "merkez": Z([0.5, 0.45], [0.5, 0.45]),
          "ogeler": [et("KARAR #6", "w:224", 300, boyut=80, egim=-3, anim="stamp"),
                     et("HEDEF: 60 BEĞENİ", "w:228", 440, boyut=54, renk="beyaz", zemin="mor", egim=2),
                     et("GEÇERSE", "w:230", 600, boyut=44, renk="beyaz", zemin="yesil", egim=0, x=300),
                     {"tip": "secenek", "harf": "A", "ad": "DEV DERBİ PANKARTI", "karakter": "tribun_lideri", "oran": 0.38, "renk": [130, 220, 150], "bas": "w:231", "x": 300, "y": 900, "dondur": 3},
                     et("GEÇMEZSE", "w:235", 600, boyut=44, renk="beyaz", zemin="kirmizi", egim=0, x=790),
                     {"tip": "secenek", "harf": "B", "ad": "ELLE BOYANIR", "karakter": "maskot", "oran": 0.38, "renk": [255, 200, 120], "bas": "w:236", "x": 790, "y": 900, "dondur": -3}]})
# 33 taraftar grubu finali
S.append({"bas": "w:240-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.06], "merkez": Z([0.5, 0.5], [0.5, 0.5]), "tribun": {"sayi": 70, "tohum": 9}, "altyazi_y": 1450,
          "karakterler": [{"ad": "tribun_lideri", "x": 540, "ayak": 1760, "h": 640, "giris": "up", "etiket": "melky.ak", "etiket_alt": "TRİBÜN LİDERİ", "etiket_boyut": 26}],
          "ogeler": [{"tip": "pankart", "metin": "TARAFTAR GRUBU FİNALİ", "zemin": "mor", "renk": "sari", "egim": -3, "bas": "w:240", "y": 290},
                     et("GRUP 1 · ANADOLU KARDEŞLER", "w:245", 440, boyut=50, renk="sari", zemin="mor", egim=-2),
                     et("GRUP 2 · ANADOLU PARS", "w:247", 560, boyut=50, renk="sari", zemin="mor", egim=2),
                     et("GRUP 3 · ANADOLU KARTALLARI", "w:249", 680, boyut=50, renk="sari", zemin="mor", egim=-2),
                     et("YORUMUNA GRUP 1 · 2 · 3 YAZ!", "w:251", 820, boyut=48, egim=2, anim="stamp"),
                     et("ÖNERENLER: @hasankaya.4444 · @zaesburakaktas.2 · @salih_pyrz06", "w:252", 930, boyut=24, renk="beyaz", zemin="mor", egim=0)]})
# 34 kapanış
S.append({"bas": "w:259-0.05", "arka": "eski_stadyum", "zoom": [1.06, 1.0], "merkez": Z([0.5, 0.6], [0.5, 0.6]),
          "karakterler": [{"ad": "oyuncu_10", "x": 170, "ayak": 1630, "h": 770, "faz": 0.6}, {"ad": "maskot", "x": 905, "ayak": 1650, "h": 680, "faz": 0.2},
                          {"ad": "taraftar_kaleci", "x": 400, "ayak": 1650, "h": 800, "faz": 0.4}, {"ad": "cem", "x": 650, "ayak": 1680, "h": 900}],
          "ogeler": [et("TAKİP ET", "w:259", 320, boyut=84, nabiz=True), et("+ BEĞEN · YORUM YAZ", "w:261", 470, boyut=48, renk="beyaz", zemin="mor", egim=2),
                     et("ZİRVEYİ GERİ ALACAĞIZ!", "w:264", 610, boyut=50, egim=-2), et("DERBİYE HAZIRLAN!", "w:267", 730, boyut=50, renk="beyaz", zemin="kirmizi", egim=2)]})

# kadro figürlerinin pop sesleri: B5 gibi 'sesler'e pop
pops = []
for sc in S:
    for c in sc.get("karakterler", []):
        if c.get("giris") == "pop" and isinstance(c.get("bas"), str): pops.append({"tip": "pop", "t": c["bas"]})
SES = [{"tip": "gum", "t": "w:1"}, {"tip": "kasa", "t": "w:25", "ses": 1.0}, {"tip": "uzgun", "t": "w:32", "ses": 0.7}, {"tip": "tezahurat", "t": "w:44", "ses": 0.6},
       {"tip": "zil", "t": "w:93", "ses": 0.7}, {"tip": "tezahurat", "t": "w:99", "ses": 0.5}, {"tip": "kasa", "t": "w:113", "ses": 1.0},
       {"tip": "tezahurat", "t": "w:140", "ses": 0.7}, {"tip": "duduk", "t": "w:150"}, {"tip": "uzgun", "t": "w:157", "ses": 0.7},
       {"tip": "tezahurat", "t": "w:164", "ses": 0.9}, {"tip": "uzgun", "t": "w:170", "ses": 0.6}, {"tip": "tezahurat", "t": "w:175", "ses": 1.0},
       {"tip": "tezahurat", "t": "w:181", "ses": 0.8}, {"tip": "duduk", "t": "we:182+0.4"}, {"tip": "zil", "t": "we:182+1.6", "ses": 0.9},
       {"tip": "uzgun", "t": "w:185", "ses": 0.6}, {"tip": "gum", "t": "w:197"}, {"tip": "kasa", "t": "w:208", "ses": 0.9},
       {"tip": "tezahurat", "t": "w:245", "ses": 0.5}, {"tip": "tezahurat", "t": "w:259", "ses": 0.6}] + pops
BIR = [(["gün", "altı"], "Gün 6"), (["kırk", "beş", "beğeni"], "45 beğeni"), (["yüz", "yirmi", "beş", "yorum"], "125 yorum"),
       (["dört", "bin", "beş", "yüz", "lira"], "4.500 lira"), (["karar", "beş"], "Karar #5"), (["doksan", "dokuz"], "99"),
       (["bin", "iki", "yüz"], "1.200"), (["altı", "yüz", "lira"], "600 lira"), (["elli", "beş", "bin", "dokuz", "yüz", "lira"], "55.900 lira"),
       (["bin", "üç", "yüz", "yetmiş", "iki"], "1.372"), (["beşinci", "hafta"], "5. hafta"), (["sıfır", "bir"], "0-1"), (["bir", "bir"], "1-1"),
       (["bir", "iki"], "1-2"), (["iki", "iki"], "2-2"), (["doksanıncı", "dakika"], "90. dakika"), (["dokuz", "puanla"], "9 puanla"),
       (["karar", "altı"], "Karar #6"), (["altmış", "beğeniyi"], "60 beğeniyi"), (["grup", "bir"], "grup 1"), (["iki", "ya", "da", "üç"], "2 ya da 3")]
sen = {"slug": "anadoluspor_bolum006", "ses": "ses.mp3", "kelimeler": "kelimeler.json", "muzik": "neseli_2", "kapak": "w:4+0.3",
       "birlestir": [[a, b] for a, b in BIR], "sesler": SES, "sahneler": S}
json.dump(sen, open(os.path.join(B, "senaryo.json"), "w"), ensure_ascii=False, indent=1)
print("sahne", len(S), "| tablo:", [r[0] + ":" + str(r[6]) for r in satirlar], "| rozet", rozet)

#!/usr/bin/env python3
"""Bölüm 7 senaryosu (otomatik görev, 2026-11-16). Çalıştır: python3 uret_senaryo.py → senaryo.json"""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
K = os.path.dirname(os.path.dirname(B))
t = json.load(open(os.path.join(K, "taraftarlar.json")))
isim = json.load(open(os.path.join(B, "gosterilen_isimler.json")))

# ---------------------------------------------------------------- lig tablosu (6. hafta)
d = json.load(open(os.path.join(K, "durum.json")))
tab = {r["takim"]: dict(r) for r in d["lig_tablosu"]["takimlar"]}
key = lambda r: (-r["P"], -(r["AG"] - r["YG"]), -r["AG"])
eski = [r["takim"] for r in sorted(tab.values(), key=key)]
SONUC = [("ANADOLUSPOR", 3, 1, "PAZAR YILDIZ"), ("MUHTARLIK GENÇLİK", 1, 1, "SANAYİ DEMİR"),
         ("BAKKAL GÜCÜ", 2, 1, "BERBER FK"), ("KAHVECİ SPOR", 2, 0, "FIRIN SPOR")]
for a, ga, gb, b in SONUC:
    for x, gx, gy in ((a, ga, gb), (b, gb, ga)):
        r = tab[x]; r["O"] += 1; r["AG"] += gx; r["YG"] += gy
        if gx > gy: r["G"] += 1; r["P"] += 3
        elif gx == gy: r["B"] += 1; r["P"] += 1
        else: r["M"] += 1
yeni = sorted(tab.values(), key=key)
def av(r):
    v = r["AG"] - r["YG"]; return f"+{v}" if v > 0 else str(v)
satirlar = [[r["takim"], r["O"], r["G"], r["B"], r["M"], av(r), r["P"]] for r in yeni]
eski_sira = eski.index("ANADOLUSPOR") + 1; yeni_sira = [r["takim"] for r in yeni].index("ANADOLUSPOR") + 1
rozet = "" if eski_sira == yeni_sira else (f"▲{eski_sira - yeni_sira}" if yeni_sira < eski_sira else f"▼{yeni_sira - eski_sira}")
json.dump({"takimlar": yeni, "eski": eski, "anadoluspor_sira": yeni_sira, "onceki_sira": eski_sira,
           "sonuclar": ["Anadoluspor 3-1 Pazar Yıldız", "Muhtarlık Gençlik 1-1 Sanayi Demir", "Bakkal Gücü 2-1 Berber FK", "Kahveci Spor 2-0 Fırın Spor"]},
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
    o = {"tip": "skor", "ev": "ANADOLUSPOR", "dep": "PAZAR YILDIZ", "ev_skor": e, "dep_skor": dp, "dakika": dk, "bas": bas, "y": 280}; o.update(kw); return o
Z = lambda a, b: [a, b]
PANKART = "ANADOLUSPOR · DERBİYE HAZIRIZ!"
S = []

# 0 kanca: dev pankart asılıyor
S.append({"bas": 0, "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.1], "merkez": [[0.5, 0.5], [0.5, 0.55]], "tribun": {"sayi": 60, "tohum": 5},
          "ogeler": [{"tip": "seri", "bolum": 7, "bas": 0.05, "y": 260, "anim": "down"},
                     {"tip": "damga", "metin": "ZİRVE MAÇI!", "boyut": 110, "egim": -8, "bas": "w:0", "y": 560, "anim": "stamp"},
                     {"tip": "pankart", "metin": PANKART, "zemin": "mor", "renk": "sari", "egim": -3, "bas": "w:3", "y": 780, "anim": "down"}]})
# 1 takip
S.append({"bas": "w:8-0.05", "arka": "eski_stadyum", "zoom": [1.04, 1.1], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [{"ad": "cem", "x": 540, "ayak": 1700, "h": 900}],
          "ogeler": [et("TAKİP ET", "w:8", 320, boyut=84, nabiz=True), et("TEKNİK HEYETE KATIL", "w:10", 460, boyut=48, renk="beyaz", zemin="mor", egim=2)]})
# 2 gün 7
S.append({"bas": "w:13-0.05", "arka": "eski_stadyum", "bulanik": 4, "zoom": [1.04, 1.1], "merkez": Z([0.5, 0.5], [0.5, 0.5]),
          "karakterler": [{"ad": "necmi", "x": 820, "ayak": 1700, "h": 880}],
          "ogeler": [{"tip": "baslik", "metin": "GÜN 7", "boyut": 230, "bas": "w:13", "bitis": "w:15-0.05", "y": 420, "anim": "stamp"},
                     {"tip": "begeni", "metin": "68 BEĞENİ", "bas": "w:17", "x": 360, "y": 470},
                     {"tip": "begeni", "metin": "118 YORUM", "zemin": "mavi", "bas": "w:20", "x": 380, "y": 640},
                     {"tip": "begeni", "metin": "+6.800 TL", "zemin": "mor", "bas": "w:24", "x": 380, "y": 810}]})
# 3 karar 6 tuttu → dev pankart
S.append({"bas": "w:30-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.52]), "tribun": {"sayi": 70, "tohum": 8},
          "ogeler": [et("KARAR #6 TUTTU!", "w:30", 300, boyut=70, renk="beyaz", zemin="yesil", egim=-3, anim="stamp"),
                     et("HEDEF 60 · GELEN 68", "w:32", 430, boyut=46, renk="beyaz", zemin="mor", egim=2),
                     {"tip": "pankart", "metin": PANKART, "zemin": "mor", "renk": "sari", "egim": 2, "bas": "w:34", "y": 640, "anim": "stamp"}]})
# 4 yepyeni yüzler
S.append({"bas": "w:37-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.5]),
          "karakterler": [{"ad": "cem", "x": 540, "ayak": 1700, "h": 900, "giris": "right", "kos": True}],
          "ogeler": [et("BUGÜN SAHADA", "w:37", 300, boyut=60), {"tip": "damga", "metin": "YEPYENİ YÜZLER!", "boyut": 100, "egim": -6, "bas": "w:38", "y": 470, "anim": "stamp"}]})
# 5 İLK 11 grup 1: kaleci, sol bek, stoper, stoper
S.append({"bas": "w:41-0.05", "arka": "eski_stadyum", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_forvet_kadin", "aysel.dogan81", "SOL BEK", "w:44", 410, False, 0.2),
                          oy("oyuncu_stoper2", "kerim4toprak", "STOPER", "w:46", 920, False, 0.6),
                          oy("taraftar_kaleci", "ruzgarcatal9", "KALECİ", "w:42", 160, True, 0.0),
                          oy("oyuncu_stoper", "barisyahyadmrci", "STOPER", "w:45", 670, True, 0.4)],
          "ogeler": baslik2("İLK 11 · KALE VE DEFANS", "ŞEMA 4-3-3", "w:41-0.05")})
# 6 grup 2: sağ bek, ön libero, 2 orta saha
S.append({"bas": "w:48-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_libero", "omercan_.k28", "ÖN LİBERO", "w:51", 410, False, 0.2),
                          oy("oyuncu_forvet_kadin", "esma.cicekli", "ORTA SAHA", "w:55", 920, False, 0.6),
                          oy("oyuncu_sagbek", "2922kadir", "SAĞ BEK", "w:48", 160, True, 0.0),
                          oy("oyuncu_ortasaha", "_arda_saricicek", "ORTA SAHA", "w:53", 670, True, 0.4)],
          "ogeler": baslik2("İLK 11 · DEFANS VE ORTA SAHA", "4-3-3", "w:48-0.05")})
# 7 grup 3: sol kanat, forvet, sağ kanat
S.append({"bas": "w:56-0.05", "arka": "eski_stadyum_kale", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy3("forvet", "yildiraysavas8912", "FORVET", "w:58", 540, False, 0.3),
                          oy3("oyuncu_solkanat", "bilal134665", "SOL KANAT", "w:57", 215, True, 0.0),
                          oy3("oyuncu_sagkanat", "muhsinyildiz685432", "SAĞ KANAT", "w:60", 865, True, 0.6)],
          "ogeler": [et("İLK 11 · HÜCUM HATTI", "w:56-0.05", 270, anim="down")]})
# 8 yedekler 1/2 (bxeatwxx sesli okunmaz: Hayri ile Cemal Can arasında belirir)
S.append({"bas": "w:61-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.03], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [oy("oyuncu_solkanat", "hayri.pasa07", "SOL KANAT", "w:63", 410, False, 0.2),
                          oy("oyuncu_stoper", "cemal_can5506", "STOPER", "w:64", 920, False, 0.6),
                          oy("oyuncu_kaleci2", "mirhat_tuna", "YEDEK KALECİ", "w:62", 160, True, 0.0),
                          oy("oyuncu_ortasaha", "bxeatwxx", "HER YER", "we:63+0.02", 670, True, 0.4)],
          "ogeler": [et("YEDEKLER · 1 / 2", "w:61-0.05", 270, anim="down")]})
# 9 yedekler 2/2 + tribün lideri
S.append({"bas": "w:66-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.03], "merkez": Z([0.45, 0.55], [0.5, 0.55]),
          "karakterler": [oy("forvet", "orhan_sisek", "FORVET", "w:66", 410, False, 0.2),
                          oy("tribun_lideri", "halitozgenur", "TRİBÜN LİDERİ", "w:73", 920, False, 0.6),
                          oy("oyuncu_sagkanat", "pusatemiralpoglu", "SAĞ KANAT", "w:67", 160, True, 0.0),
                          oy("oyuncu_forvet_kadin", "eda1993temiz_", "DEFANS", "w:70", 670, True, 0.4)],
          "ogeler": baslik2("YEDEKLER · 2 / 2", "+ TRİBÜN LİDERİ", "w:66-0.05")})
# 10 kadrodakilere çağrı
S.append({"bas": "w:74-0.05", "arka": "eski_stadyum_kulube", "zoom": [1.03, 1.07], "merkez": Z([0.5, 0.58], [0.5, 0.58]),
          "karakterler": [{"ad": "oyuncu_sagkanat", "x": 900, "ayak": 1440, "h": 560, "faz": 0.5}, {"ad": "oyuncu_libero", "x": 400, "ayak": 1440, "h": 560, "faz": 0.2},
                          {"ad": "taraftar_kaleci", "x": 180, "ayak": 1640, "h": 640, "faz": 0.1}, {"ad": "oyuncu_forvet_kadin", "x": 650, "ayak": 1640, "h": 640, "faz": 0.4}],
          "ogeler": [et("ADINI GÖRDÜN MÜ? \"BURADAYIM\" YAZ!", "w:74", 300, boyut=42, renk="beyaz", zemin="mor", egim=2, bitis="w:77-0.05"),
                     et("YORUM YAP", "w:77", 300, boyut=60, renk="sari", zemin="mor", egim=-3),
                     et("BEĞEN", "w:78", 420, boyut=60, renk="sari", zemin="mor", egim=2),
                     et("PAYLAŞ", "w:79", 540, boyut=60, renk="sari", zemin="mor", egim=-2),
                     et("ARKADAŞINA GÖNDER", "w:80", 660, boyut=60, renk="sari", zemin="mor", egim=2)]})
# 11 forma duvarı
fw = isim["forma"][:9]
og = [et("FORMA DUVARI", "w:82-0.05", 270, boyut=60, anim="down")]
for i, (u, no) in enumerate(fw):
    og.append({"tip": "forma", "isim": "@" + u, "no": no, "genislik": 280, "x": [190, 540, 890][i % 3], "y": [560, 880, 1200][i // 3],
               "bas": round(35.6 + 0.22 * i, 2)})
S.append({"bas": "w:82-0.05", "arka": "eski_stadyum_soyunma", "bulanik": 6, "karanlik": 0.8, "zoom": [1.0, 1.04], "merkez": Z([0.5, 0.5], [0.5, 0.5]), "ogeler": og})
# 12 kasa defteri
S.append({"bas": "w:87-0.05", "arka": "eski_stadyum_soyunma", "bulanik": 10, "karanlik": 0.7, "zoom": [1.06, 1.1], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "ogeler": [{"tip": "kasa", "baslik": "KULÜP KASASI", "satirlar": [["DEVREDEN", "55.900 TL", "mor"], ["68 BEĞENİ × 100 TL", "+6.800 TL"], ["DEV DERBİ PANKARTI", "−2.500 TL"]],
                      "kalan": "60.200 TL", "not": "KARAR #6 TUTTU · PANKART HAZIR", "bas": "w:87", "y": 740},
                     {"tip": "damga", "metin": "60.200 TL", "boyut": 100, "egim": -8, "bas": "w:93", "y": 1225, "anim": "stamp"}]})
# 13 tribün + toplam taraftar
S.append({"bas": "w:98-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.75, 1.75], "merkez": Z([0.28, 0.5], [0.72, 0.5]),
          "tribun": {"isimler": isim["tribun"][:30], "etiket_boyut": 15, "sayi": 14},
          "ogeler": [{"tip": "sayac", "baslik": "TOPLAM TARAFTAR", "deger": "1.490", "alt": "TRİBÜN 1.144 · LOCA 346", "bas": "w:98", "y": 360}]})
# 14-16 loca (sessizlik içinde)
LT = [47.0, 48.8, 50.6]; LM = ["LOCA · 346 KİŞİLİK TEKNİK HEYET", "İSİMLER EKRANDA!", "LOCAYA HOŞ GELDİNİZ"]
for k in range(3):
    S.append({"bas": LT[k], "arka": "eski_stadyum_loca", "zoom": [1.6, 1.6], "merkez": Z([0.42, 0.5], [0.58, 0.5]) if k % 2 == 0 else Z([0.58, 0.5], [0.42, 0.5]),
              "tribun": {"isimler": isim["loca"][20 * k:20 * k + 20], "etiket_boyut": 15, "aralik": 1.3, "tohum": 21 + k},
              "ogeler": [et(LM[k], LT[k], 250, boyut=42, renk="beyaz" if k == 0 else "siyah", zemin="mor" if k == 0 else "sari")]})
# 17 maç başlıyor
S.append({"bas": "w:106-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.52]),
          "karakterler": [{"ad": "forvet", "x": 330, "ayak": 1700, "h": 760, "giris": "left", "sure": 0.4, "kos": True, "bas": "w:107"},
                          {"ad": "oyuncu_solkanat", "x": 760, "ayak": 1700, "h": 740, "giris": "right", "sure": 0.4, "kos": True, "bas": "w:108"}],
          "ogeler": [skor(0, 0, "1'", "w:106"), et("LİG 6. HAFTA · ANADOLU ARENA PARK", "w:106", 450, boyut=42, renk="beyaz", zemin="mor"),
                     {"tip": "isim", "no": "VS", "ad": "PAZAR YILDIZ", "alt": "ZİRVE İÇİN 3 PUAN", "bas": "w:109", "x": 520, "y": 620}]})
# 18 bilal orta
S.append({"bas": "w:111-0.05", "arka": "eski_stadyum", "zoom": [1.0, 1.1], "merkez": Z([0.35, 0.55], [0.6, 0.55]),
          "karakterler": [{"ad": "oyuncu_solkanat", "x": 560, "ayak": 1720, "h": 900, "giris": "left", "sure": 0.3, "kos": True, "etiket": "bilal134665", "etiket_alt": "SOL KANAT"}],
          "ogeler": [skor(0, 0, "23'", "w:111"), et("ORTA!", "w:112", 560, boyut=90, anim="stamp")]})
# 19 yıldıray kafa gol
S.append({"bas": "w:113-0.05", "arka": "eski_stadyum_kale", "zoom": [1.05, 1.14], "merkez": Z([0.5, 0.5], [0.5, 0.46]),
          "karakterler": [{"ad": "forvet", "x": 540, "ayak": 1740, "h": 960, "giris": "right", "sure": 0.3, "kos": True, "etiket": "yildiraysavas8912", "etiket_alt": "FORVET"}],
          "ogeler": [skor(0, 0, "24'", "w:113", bitis="w:115-0.03"), skor(1, 0, "24'", "w:115"), et("KAFA!", "w:114", 460, boyut=80, renk="beyaz", zemin="mor", bitis="w:115-0.03"),
                     {"tip": "baslik", "metin": "GOL!", "boyut": 220, "bas": "w:115", "y": 560, "anim": "stamp", "titre": True}]})
# 20 pazar eşitledi
S.append({"bas": "w:117-0.05", "arka": "eski_stadyum_kale", "zoom": [1.04, 1.12], "merkez": Z([0.5, 0.46], [0.5, 0.44]),
          "karakterler": [{"ad": "taraftar_kaleci", "x": 540, "ayak": 1740, "h": 920, "etiket": "ruzgarcatal9", "etiket_alt": "KALECİ"}],
          "ogeler": [skor(1, 0, "51'", "w:117", bitis="w:119-0.03"), skor(1, 1, "52'", "w:119"),
                     {"tip": "damga", "metin": "PAZAR EŞİTLEDİ...", "boyut": 86, "egim": -6, "bas": "w:118", "y": 560, "anim": "stamp"}]})
# 21 arda ara pas
S.append({"bas": "w:121-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.1], "merkez": Z([0.4, 0.55], [0.6, 0.55]),
          "karakterler": [{"ad": "oyuncu_ortasaha", "x": 560, "ayak": 1720, "h": 900, "giris": "left", "sure": 0.3, "kos": True, "etiket": "_arda_saricicek", "etiket_alt": "ORTA SAHA"}],
          "ogeler": [skor(1, 1, "77'", "w:121"), et("ARA PAS!", "w:122", 560, boyut=90, anim="stamp")]})
# 22 muhsin gol
S.append({"bas": "w:124-0.05", "arka": "eski_stadyum_kale", "zoom": [1.05, 1.14], "merkez": Z([0.5, 0.5], [0.5, 0.46]),
          "karakterler": [{"ad": "oyuncu_sagkanat", "x": 540, "ayak": 1740, "h": 940, "giris": "right", "sure": 0.3, "kos": True, "etiket": "muhsinyildiz685432", "etiket_alt": "SAĞ KANAT"}],
          "ogeler": [skor(1, 1, "78'", "w:124", bitis="w:125-0.03"), skor(2, 1, "78'", "w:125"),
                     {"tip": "baslik", "metin": "GOL!", "boyut": 220, "bas": "w:125", "y": 560, "anim": "stamp", "titre": True}]})
# 23 kulübe tepkisi
S.append({"bas": "w:126-0.02", "arka": "eski_stadyum_kulube", "zoom": [1.0, 1.06], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "karakterler": [{"ad": "yardimci_antrenor1", "x": 200, "ayak": 1620, "h": 720, "faz": 0.0}, {"ad": "cem", "x": 540, "ayak": 1660, "h": 800, "faz": 0.3},
                          {"ad": "yedek_antrenor", "x": 880, "ayak": 1620, "h": 720, "faz": 0.6}],
          "ogeler": [skor(2, 1, "78'", "w:126")]})
# 24 penaltı → rüzgar kurtardı
S.append({"bas": "w:127-0.05", "arka": "eski_stadyum_kale", "zoom": [1.02, 1.14], "merkez": Z([0.5, 0.44], [0.5, 0.42]),
          "karakterler": [{"ad": "taraftar_kaleci", "x": 540, "ayak": 1740, "h": 920, "etiket": "ruzgarcatal9", "etiket_alt": "KALECİ"}],
          "ogeler": [skor(2, 1, "88'", "w:127"), {"tip": "damga", "metin": "PENALTI!", "boyut": 110, "egim": -6, "bas": "w:129", "bitis": "w:130", "y": 560, "anim": "stamp"},
                     {"tip": "damga", "metin": "RÜZGAR KURTARDI!", "boyut": 96, "egim": -8, "bas": "w:131", "y": 560, "anim": "stamp", "titre": True}]})
# 25 orhan (yedekten) gol
S.append({"bas": "w:132-0.05", "arka": "eski_stadyum_gece", "zoom": [1.0, 1.12], "merkez": Z([0.5, 0.5], [0.5, 0.46]),
          "karakterler": [{"ad": "forvet", "x": 540, "ayak": 1740, "h": 940, "giris": "left", "sure": 0.3, "kos": True, "bas": "w:132", "etiket": "orhan_sisek", "etiket_alt": "FORVET · YEDEKTEN"}],
          "ogeler": [skor(2, 1, "90'", "w:132", bitis="w:135-0.03"), skor(3, 1, "90'", "w:135"), et("YEDEKTEN GİRDİ!", "w:132", 450, boyut=60, renk="beyaz", zemin="mor", bitis="w:135-0.03"),
                     {"tip": "baslik", "metin": "GOL!", "boyut": 220, "bas": "w:135", "y": 560, "anim": "stamp", "titre": True}]})
# 26 tekrar
S.append({"bas": "we:136+0.03", "arka": "eski_stadyum_gece", "zoom": [1.3, 1.4], "merkez": Z([0.5, 0.45], [0.5, 0.42]),
          "karakterler": [{"ad": "forvet", "x": 540, "ayak": 1800, "h": 1100, "faz": 0.2}],
          "ogeler": [et("TEKRAR", "we:136+0.05", 300, boyut=60, renk="beyaz", zemin="kirmizi"), skor(3, 1, "90'", "we:136+0.05", y=180)]})
# 27 tribün tepkisi 3-1
S.append({"bas": "we:136+1.05", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.08], "merkez": Z([0.5, 0.5], [0.5, 0.5]), "tribun": {"sayi": 80, "tohum": 7},
          "ogeler": [skor(3, 1, "90+2'", "we:136+1.08"), {"tip": "damga", "metin": "3-1!", "boyut": 170, "egim": -8, "bas": "we:136+1.1", "y": 700, "anim": "stamp"}]})
# 28 puan tablosu
S.append({"bas": "we:136+1.95", "altyazi_y": False, "arka": "eski_stadyum_gece", "bulanik": 10, "karanlik": 0.7, "zoom": [1.04, 1.08], "merkez": Z([0.5, 0.55], [0.5, 0.55]),
          "ogeler": [{"tip": "puan", "baslik": "HALI SAHA LİGİ · 6. HAFTA", "satirlar": satirlar, "eski": eski, "vurgu": "ANADOLUSPOR", "rozet": rozet,
                      "alt": "ŞAMPİYON 5 GALİBİYETLE ÜST LİGE ÇIKAR", "bas": "we:136+2.0", "gecikme": 1.0, "kayma": 1.1, "y": 830},
                     et("ANADOLUSPOR 3-1 PAZAR YILDIZ", "we:136+2.0", 300, boyut=50, renk="beyaz", zemin="mor"),
                     et("MUHTARLIK 1-1 · ZİRVE BİZİM!", "w:139", 1320, boyut=56, egim=-3, anim="stamp")]})
# 29 karaduman başkanı pankartı gördü
S.append({"bas": "w:142-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.1], "merkez": Z([0.5, 0.55], [0.5, 0.5]), "tribun": {"sayi": 50, "tohum": 3},
          "karakterler": [{"ad": "karaduman_baskan", "x": 560, "ayak": 1740, "h": 960, "giris": "up", "sure": 0.4, "bas": "w:143"}],
          "ogeler": [{"tip": "pankart", "metin": PANKART, "zemin": "mor", "renk": "sari", "egim": -3, "bas": "w:144", "y": 330},
                     {"tip": "damga", "metin": "BIYIĞI TİTREDİ!", "boyut": 90, "egim": -6, "bas": "w:146", "y": 520, "anim": "stamp", "titre": True}]})
# 30 taraftar grubu finali sürüyor
S.append({"bas": "w:148-0.05", "arka": "eski_stadyum_tribun", "zoom": [1.0, 1.06], "merkez": Z([0.5, 0.5], [0.5, 0.5]), "tribun": {"sayi": 70, "tohum": 9}, "altyazi_y": 1450,
          "karakterler": [{"ad": "tribun_lideri", "x": 540, "ayak": 1760, "h": 640, "giris": "up", "etiket": "halitozgenur", "etiket_alt": "TRİBÜN LİDERİ", "etiket_boyut": 26}],
          "ogeler": [{"tip": "pankart", "metin": "ANADOLUSPOR · . . . . . . ?", "zemin": "mor", "renk": "sari", "egim": -3, "bas": "w:148", "y": 290},
                     et("KÖŞE GRUBUN ADINA BOŞ!", "w:150", 400, boyut=40, renk="siyah", zemin="beyaz", egim=2),
                     et("GRUP 1 · ANADOLU KARDEŞLER", "w:153", 510, boyut=48, renk="sari", zemin="mor", egim=-2),
                     et("GRUP 2 · ANADOLU PARS", "w:155", 620, boyut=48, renk="sari", zemin="mor", egim=2),
                     et("GRUP 3 · ANADOLU KARTALLARI", "w:158", 730, boyut=48, renk="sari", zemin="mor", egim=-2),
                     et("FİNAL SÜRÜYOR: GRUP 1 · 2 · 3 YAZ!", "w:159", 850, boyut=44, egim=2, anim="stamp")]})
# 31 saha oylaması sürüyor (6 seçenek)
SEC = d["saha"]["acik_oylama"]["secenekler"]
KISA = {1: "KALE DİREKLERİ + FİLE", 2: "TRİBÜN BOYASI", 3: "PROJEKTÖRLER", 4: "TRİBÜNE +50 KOLTUK", 5: "SAHA ÇİMLERİ", 6: "YENİ TRİBÜN KOLTUKLARI"}
og = [et("SAHA OYLAMASI SÜRÜYOR", "w:160", 300, boyut=56)]
SB = ["w:161", "w:161+0.3", "w:162", "w:162+0.3", "w:163", "w:163+0.3"]
for i, s in enumerate(SEC):
    og.append(et(f"{s['no']}) {KISA[s['no']]} · {s['tl']:,} TL".replace(",", "."), SB[i], 440 + 105 * i, boyut=40, renk="siyah", zemin="beyaz", egim=0 if i % 2 else -1))
og.append(et("YORUMUNA NUMARANI YAZ: 1–6", "w:164", 1110, boyut=46, renk="sari", zemin="mor", egim=-2, anim="stamp"))
S.append({"bas": "w:160-0.05", "arka": "eski_stadyum", "bulanik": 6, "karanlik": 0.75, "zoom": [1.0, 1.06], "merkez": Z([0.5, 0.45], [0.5, 0.42]), "altyazi_y": 1450, "ogeler": og})
# 32 karar 7
S.append({"bas": "w:165-0.05", "arka": "eski_stadyum_kale", "bulanik": 6, "karanlik": 0.75, "zoom": [1.05, 1.12], "merkez": Z([0.5, 0.45], [0.5, 0.45]),
          "ogeler": [et("KARAR #7", "w:165", 300, boyut=80, egim=-3, anim="stamp"),
                     et("HEDEF: 90 BEĞENİ", "w:169", 440, boyut=54, renk="beyaz", zemin="mor", egim=2),
                     et("GEÇERSE", "w:171", 600, boyut=44, renk="beyaz", zemin="yesil", egim=0, x=300),
                     {"tip": "secenek", "harf": "A", "ad": "DERBİ BİZİM SAHADA", "karakter": "cem", "oran": 0.38, "renk": [130, 220, 150], "bas": "w:172", "x": 300, "y": 900, "dondur": 3},
                     et("GEÇMEZSE", "w:175", 600, boyut=44, renk="beyaz", zemin="kirmizi", egim=0, x=790),
                     {"tip": "secenek", "harf": "B", "ad": "DEPLASMANA OTOBÜSLE", "karakter": "otobus_morsari_kart", "oran": 0.4, "renk": [255, 200, 120], "bas": "w:178", "x": 790, "y": 900, "dondur": -3}]})
# 33 kapanış
S.append({"bas": "w:181-0.05", "arka": "eski_stadyum", "zoom": [1.06, 1.0], "merkez": Z([0.5, 0.6], [0.5, 0.6]),
          "karakterler": [{"ad": "oyuncu_sagkanat", "x": 170, "ayak": 1630, "h": 770, "faz": 0.6}, {"ad": "maskot", "x": 905, "ayak": 1650, "h": 680, "faz": 0.2},
                          {"ad": "taraftar_kaleci", "x": 400, "ayak": 1650, "h": 800, "faz": 0.4}, {"ad": "cem", "x": 650, "ayak": 1680, "h": 900}],
          "ogeler": [et("TAKİP ET", "w:181", 320, boyut=84, nabiz=True), et("+ BEĞEN · YORUM YAZ", "w:183", 470, boyut=48, renk="beyaz", zemin="mor", egim=2),
                     {"tip": "damga", "metin": "YARIN: DERBİ!", "boyut": 100, "egim": -6, "bas": "w:186", "y": 640, "anim": "stamp"}]})

pops = []
for sc in S:
    for c in sc.get("karakterler", []):
        if c.get("giris") == "pop" and isinstance(c.get("bas"), str): pops.append({"tip": "pop", "t": c["bas"]})
SES = [{"tip": "gum", "t": "w:0"}, {"tip": "kasa", "t": "w:24", "ses": 1.0}, {"tip": "zil", "t": "w:30", "ses": 0.8}, {"tip": "tezahurat", "t": "w:34", "ses": 0.7},
       {"tip": "tezahurat", "t": "w:38", "ses": 0.5}, {"tip": "kasa", "t": "w:93", "ses": 1.0}, {"tip": "tezahurat", "t": "w:98", "ses": 0.7},
       {"tip": "duduk", "t": "w:106"}, {"tip": "tezahurat", "t": "w:115", "ses": 1.0}, {"tip": "uzgun", "t": "w:119", "ses": 0.7},
       {"tip": "tezahurat", "t": "w:125", "ses": 1.0}, {"tip": "kisa_duduk", "t": "w:129"}, {"tip": "tezahurat", "t": "w:131", "ses": 0.9},
       {"tip": "tezahurat", "t": "w:135", "ses": 1.0}, {"tip": "duduk", "t": "we:136+1.2"}, {"tip": "zil", "t": "we:136+3.1", "ses": 0.9},
       {"tip": "gum", "t": "w:146"}, {"tip": "tezahurat", "t": "w:153", "ses": 0.5}, {"tip": "gum", "t": "w:165"}, {"tip": "tezahurat", "t": "w:181", "ses": 0.6}] + pops
BIR = [(["gün", "yedi"], "Gün 7"), (["altmış", "sekiz", "beğeni"], "68 beğeni"), (["yüz", "on", "sekiz", "yorum"], "118 yorum"),
       (["altı", "bin", "sekiz", "yüz", "lira"], "6.800 lira"), (["karar", "altı"], "Karar #6"),
       (["iki", "bin", "beş", "yüz"], "2.500"), (["altmış", "bin", "iki", "yüz", "lira"], "60.200 lira"),
       (["bin", "dört", "yüz", "doksan"], "1.490"), (["altıncı", "hafta"], "6. hafta"), (["bir", "sıfır"], "1-0"), (["bir", "bir"], "1-1"),
       (["iki", "bir"], "2-1"), (["üç", "bir"], "3-1"), (["grup", "bir"], "grup 1"), (["iki", "ya", "da", "üç"], "2 ya da 3"),
       (["karar", "yedi"], "Karar #7"), (["doksan", "beğeniyi"], "90 beğeniyi")]
sen = {"slug": "anadoluspor_bolum007", "ses": "ses.mp3", "kelimeler": "kelimeler.json", "muzik": "neseli_1", "kapak": "w:5+0.3",
       "birlestir": [[a, b] for a, b in BIR], "sesler": SES, "sahneler": S}
json.dump(sen, open(os.path.join(B, "senaryo.json"), "w"), ensure_ascii=False, indent=1)
print("sahne", len(S), "| tablo:", [r[0] + ":" + str(r[6]) for r in satirlar], "| rozet", rozet)

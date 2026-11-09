# Anadoluspor — Dizi Kitabı (@hocasensin1)

Instagram sayfası **@hocasensin1** (Metricool markası "anadoluspor", blogId **7980733**, saat dilimi Europe/Istanbul; Metricool hesabı eski kullanıcı adıyla "bjk3465.ist" gösterebilir — sayfa sahibi aynı hesap olduğunu onayladı). Her gün **19:00**'da bir Reels bölümü yayınlanır; hikâyeyi izleyicinin beğeni ve yorum SAYILARI yönlendirir.

## Konsept
Saatlik kiralık bir halı sahada kurulan mahalle takımı **Anadoluspor**. Takımın teknik direktörü yok: **teknik direktör izleyici** ("Hoca sensin"). Hedef: **Halı sahadan Süper Lig'e.** Anlatıcı kaptan **Cem** (birinci ağızdan, samimi, esprili).

## Kurallar (izleyici = hikâye)
- **Her beğeni = 10 TL** kulüp kasasına. Bir bölümün beğenileri ertesi günkü çalışmada sayılır.
- **Her yorum = tribünde 1 taraftar.** Tribün toplamı birikir (tüm bölümlerin yorum sayısı).
- **Takipçiler = teknik heyet** (takipçi sayısı).
- **Haftalık saha kirası 1.500 TL**, kira günü her 7. bölümde (7, 14, 21…). Kasa yetmezse eksik kısım Necmi abiye **borç** (veresiye) yazılır; sonraki kasadan önce borç ödenir. Borç 3.000 TL'yi geçerse Necmi abi sahayı başka takıma vermekle tehdit eder (kriz bölümü).
- **Her bölüm bir KARAR ile biter:** "Bu video **X beğeniyi** geçerse A, geçmezse B." Ertesi gün beğeni sayısına göre uygulanır ve yeni bölümün başında açıklanır. İsteğe bağlı ikinci hedef yorumla verilebilir ("Y yorumu geçerse tribün tezahürat yapar…").
- **Yorum METİNLERİ okunamaz** (Metricool yalnız sayı verir). Bu yüzden "en çok beğenilen yorum", "yorumlarda en çok istenen", "siz seçtiniz: X" gibi ifadeler KULLANMA, izleyici yorumu ya da kullanıcı adı UYDURMA. Kararlar yalnız sayılarla (beğeni / yorum / takipçi) verilir.
- **Hedef eşiği:** son bölümün beğenisinin ≈ 1,3 katı, 10'a yuvarla, en az 20 (Bölüm 1'de 100'dü). 3–4 bölümde bir bilerek daha kolay bir hedef koy (izleyici kazanmanın tadını alsın). Veri yoksa önceki eşiği koru.

## İlerleme
Lig sırası: Halı Saha Ligi → Mahalle Ligi → Amatör Lig → BAL → 3. Lig → 2. Lig → 1. Lig → Süper Lig. Bir üst lige çıkmak için o ligde **5 galibiyet**. İlerleme çubuğu oranı = (lig sırası + lig galibiyeti / 5) / 7.

**Maçlar:** her 3 bölümde bir maç bölümü (2, 5, 8, 11…). Maç sonucunu rastgele verme, verilere bağla: önceki bölümün KARARI maçla ilgiliyse onun sonucu belirler; değilse hedef tuttuysa galibiyet, tutmadıysa beraberlik ya da komik bir mağlubiyet. Tribün toplamı ≥ 20 ise "taraftar desteği" bir avantaj olarak sahneye girer. Skorlar gerçekçi halı saha skorları olabilir (7–5, 3–3…). Maç bölümünde "skor" öğesi kullan.

## Karakterler (varliklar/karakter/*.png)
| Dosya | Kim | Özellik / tekrar eden şaka |
|---|---|---|
| cem.png | **Kaptan Cem** (C) | Kurucu, anlatıcı, maçı ayarlayan ve parayı toplayan adam; mor eşofman, sarı kaptan bandı, el sallar |
| necmi.png | **Necmi Abi** | Saha sahibi; dev kronometre; saat dolunca ışıkları kapatır (penaltıda bile); parayla ilgili her şeyde ciddi |
| yasin.png | **Yoldayım Yasin** (7) | Hep geç kalır, telefonda "yoldayım abi, 5 dk"; tek terlik tek krampon |
| selim.png | **Pas Vermeyen Selim** (10) | Topu bırakmaz, kibirli; "son pas: 2019" |
| burak.png | **Ful Ekipman Burak** (4) | Her ekipman var (GPS yelek, 2 akıllı saat, gözlük) ama yeteneği yok; "her şey pro, kendisi hariç" |
| muhtar.png | **Muhtar** | Rakip Muhtarlık Gençlik'in sahibi ve aynı zamanda hakem; kırmızı kart + mühür |
| _karakter_sayfasi.jpg | Tüm karakterlerin referans sayfası (yeni çizimlerde stil referansı) | |

Yeni karakter eklenebilir (rakip takım oyuncusu, transfer, taraftar…): gerçek kişi, gerçek kulüp, marka ya da logo YOK. Yeni karakter tutarlılığı için referans sayfasını bağla.

**Çizim stili (karakter):** "polished 2D cartoon, thick clean black outlines, flat cel shading with soft highlights, big expressive heads (about one third of body height), vibrant saturated colors, sticker-like; same style as the reference sheet; team colors purple and yellow (rivals use other colors)". Tam boy, düz açık gri zemin (#E6E6E6), gölge yok, yazı yok, logo yok, marka (Nike vb.) yok. Kesip çıkarmak için `motor/kes.py`.

**Çizim stili (arka plan):** "Vertical 2D cartoon background illustration in a polished mobile-game art style: clean outlines, rich cel-shaded colors, slightly exaggerated perspective. No people, no characters, no text, no logos." + mekân + "The lower 40–45% of the image is open, empty ground, leaving room for characters." (9:16, 2K).

## Mekânlar (varliklar/arka/*.jpg)
halisaha (gün batımı, kafesli halı saha, sol arkada kulübe) · kulube (Necmi abinin kulübesi, saat, ışık şalterleri) · hoca_koltugu (gece, boş beyaz sandalye + soru işaretli taktik tahtası) · stadyum (hayal: dolu mor-sarı Süper Lig stadı) · bos_kale (gece, boş kale, yerde eldivenler). Yeni mekân eklenebilir (soyunma odası, mahalle kahvesi, otobüs, rakip saha…).

## Ton ve sınırlar
Aile dostu mahalle mizahı; kimseyi aşağılama, küfür yok, siyaset yok, bahis/kumar yok, gerçek kişi/kulüp/marka yok, şiddet yok (kırmızı kart, itiraz, komik düşme olur). Futbol jargonu ve halı saha klişeleri serbest (son dakika golü, "abi ofsayt yok burada", su molası, IBAN atan adam…).

## Bölüm yapısı (55–65 sn, anlatım 125–150 kelime)
1. **Kanca** (ilk cümle, merak açar, sonucu söylemez) — 2. cümle **sesli takip çağrısı** ("Takip et, Anadoluspor'un teknik heyetine katıl." ya da kısa bir varyasyonu).
2. **"Gün N."** + dünün sayıları: "Dünkü bölüm X beğeni aldı: kasaya Y lira girdi." (+ yorum/tribün) + **KARAR sonucu** ("Hedef tuttu: kaleye Necmi abi geçiyor!").
3. **Ana olay:** kararın komik sonucu, maç, transfer, kira krizi vb. Görüntü 3–4 sn'de bir değişsin.
4. **Durum kartı:** kasa / tribün / lig (sayac, ilerleme öğeleri).
5. **Yeni KARAR** (X beğeni eşiği, A/B) + yarın ne olacağı (cliffhanger).
6. **Kapanış:** "Takip et, beğen, yorum yaz…" + kısa esprili son söz.

Sayıları seslendirme metninde yazıyla yaz ("yüz elli beğeni"), altyazıda rakamla göstermek için senaryodaki `birlestir` listesini kullan.

## Açıklama (caption) şablonu
```
Anadoluspor · Bölüm N ⚽
<1–2 cümlelik özet, ölçülü emoji>

📊 Kasa: <kasa> TL · Tribün: <tribün> taraftar
🧤 KARAR #N: Bu video <X> beğeniyi geçerse <A>. Geçmezse <B>!

Yarın 19:00: <kısa merak cümlesi> 👀 Teknik heyete katılmak için @hocasensin1'i takip et

#anadoluspor #halısaha #futbol #futbolmizah #hocasensin
```
İlk satır her zaman **"Anadoluspor · Bölüm N"** ile başlar (ertesi gün Metricool'da bu satırla bulunur).

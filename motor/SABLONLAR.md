# İLK 11 · Hikâye motoru şablonları

`python3 motor/hikaye.py senaryo.json cikti --onizleme` → `cikti/onizleme.png` (her sahneden 2 kare) + sahne başlangıç saniyeleri
`python3 motor/hikaye.py senaryo.json cikti` → `cikti/<slug>.mp4` ve `cikti/kapak.jpg`

## senaryo.json
```json
{
 "slug": "2026-10-24-leicester-5000de1",
 "ses": "ses.mp3",
 "cumleler": ["Cümle 1.", {"soz": "Bin dokuz yüz elli dört.", "altyazi": "1954."}],
 "sahneler": [ {"tip": "kanca", "cumleler": [0], "...": "..."} ],
 "soru": "Sence ... mi?",
 "kapak_sn": 2.5
}
```
- `cumleler`: ElevenLabs'e gönderilen metindeki cümleler, AYNI sırada ve AYNI sayıda. Motor ses dosyasındaki duraklamalardan cümleleri bulur; bu yüzden ElevenLabs metninde her cümle ayrı paragraf olmalı (aralarında boş satır).
- Sayılar seslendirmede yazıyla (`"soz"`), altyazıda rakamla (`"altyazi"`) yazılır.
- `sahneler`: her sahne hangi cümleleri kapsadığını `cumleler` ile söyler; cümleler sırayla ve eksiksiz paylaştırılmalı. 5–7 sahne ideal, her sahne 3–7 sn.
- Kapanış (Hoca: "Daha fazlası için İlk On Bir'i takip etmeyi unutma!" + takip butonu + `soru`) OTOMATİK eklenir; metne yazma.
- **Takip rozeti** (OTOMATİK): 3. cümlenin başında (en erken 5. sn) üst etiketin yerine "<rozet> · TAKİP ET" rozeti çıkar, el ikonu butona dokunur ve kapanışa kadar kalır. `"rozet"`: rozet metni (varsayılan "HER AKŞAM 19:00 · YENİ HİKÂYE"; portre: "HER GÜN 13:00 · BİR EFSANE"; `""` kapatır), `"rozet_sn"`: başlama saniyesi (isteğe bağlı). Rozet y≈204–300 bandındadır; sahnelerde bu bandın içine yazı koyma.
- `at`: o anın söylendiği kelimenin başı (küçük harf, ör. `"madrid"`, rakamlı altyazıda `"2-2"`) ya da sahne başından saniye (sayı).
- Metinlerde Türkçe büyük harf kullan (İ, Ş, Ğ…). Yabancı adlar özgün yazımıyla: LILLE, LIVERPOOL.
- `*kelime*` vurgulu (neon yeşil) yazar. Başlıkta `|` ikinci satıra geçer.

## Sahne tipleri

### kanca — açılış (ilk sahne)
`{"tip":"kanca","cumleler":[0],"baslik":"*5000'DE 1* İHTİMAL","ikon":"para","hoca":"smile","arka":"karanlik","damga":{"metin":"İMKÂNSIZ?","at":"bahisçiler"}}`
- `hoca`: smile | wink | yok ; `damga` isteğe bağlı

### tahta — Hoca taktik tahtasında anlatır (1–3 satır, tebeşirle belirir)
`{"tip":"tahta","cumleler":[1,2],"satirlar":[{"metin":"2015-16","at":"sezon"},{"metin":"LEICESTER CITY","at":"leicester","boyut":80,"bayrak":"eng"}]}`

### skor — skor tabelası (1–3 satır) + isteğe bağlı damga
`{"tip":"skor","cumleler":[3,4],"baslik":"ELEME · 1954","satirlar":[{"etiket":"MADRİD","sol":"İSPANYA","sol_bayrak":"es","skor":"4-1","sag":"TÜRKİYE","sag_bayrak":"tr","at":"madrid"}],"damga":{"metin":"PUANLAR EŞİT","at":"puanlar"}}`
- Kulüpler için bayrak yerine renk şeridi: `"sol_bayrak":"#FDB913,#0053A0"` (logo ASLA çizilmez)

### sayi — dev sayı/istatistik damgası
`{"tip":"sayi","cumleler":[5],"ust":"BAHİS ORANI","ikon":"para","sayi":"5000'DE 1","etiket":"ŞAMPİYONLUK İHTİMALİ","at":"bahis","arka":"karanlik"}`

### an — dramatik an (ikon + yazı, isteğe bağlı iki taraf bayrağı ve dev skor)
`{"tip":"an","cumleler":[6],"arka":"gece","ust":"ROMA · TARAFSIZ SAHA","ikon":"saat","metin":"UZATMA · 120'","at":"uzatmalarla","sol_bayrak":"tr","sol":"TÜRKİYE","sag_bayrak":"es","sag":"İSPANYA","buyuk":"2-2","buyuk_at":"2-2"}`

### hoca — Hoca konuşma balonuyla (alıntı/yorum; balon ≤ 44 karakter)
`{"tip":"hoca","cumleler":[7],"ifade":"wink","poz":"stand","balon":"Futbolda imkânsız yoktur!","at":0.4,"arka":"marka"}`
- `poz`: stand | point | cheer ; `ifade`: smile | wink | cheer

### zafer — büyük açılış/sonuç anı (konfeti, ışık, bayrak/renk)
`{"tip":"zafer","cumleler":[9,10,11],"kelime":"ŞAMPİYON","renk":"#0053A0","bayrak":"eng","at":"şampiyon","kart_at":"ve","alt":"PREMIER LIG · 2016","alt_at":"tarih"}`
- `bayrak` yoksa sadece renk zemini; kelime ≤ 10 harf ideal

### foto — gerçek fotoğraf kartı (yalnız lisansı uygun fotoğraf)
`{"tip":"foto","cumleler":[0],"foto":"arda.jpg","kredi":"Foto: Ad · Wikimedia · CC BY-SA 4.0","baslik":"*ARDA GÜLER*|19 YAŞINDA REKOR","damga":{"metin":"REKOR","at":"rekorunu"}}`
`{"tip":"foto","cumleler":[2],"foto":"fb.jpg","kredi":"Foto: beIN SPORTS Türkiye · CC BY 3.0","ust":"2019 · FENERBAHÇE","alt":"16 YAŞINDA A TAKIM","alt_at":"forma"}`
- `foto` yolu senaryo.json'a göre; `kredi` ZORUNLU (yazar + lisans). Kaynak yalnız Wikimedia Commons'taki CC/kamu malı dosyalar (bkz. motor/fotolar/KAYNAK.txt).
- `baslik` ya da `ust`'ten biri; `odak`: "ust" (varsayılan, yüz üstte) | "orta". Gönderi açıklamasına da "📷 Fotoğraflar: …" kredi satırı eklenir.

## Seçenekler
- **ikon**: top, kupa, duduk, saat, kart_kirmizi, kart_sari, para, sozlesme, kale, soru, unlem, fanus, mikrofon, `bayrak:<kod>`, `forma:<renk1>,<renk2>,<numara>` (ör. `forma:#E30A17,#FFFFFF,10`)
- **arka**: karanlik (spot ışığı), gece (stadyum gecesi), gunbatimi, roma (Kolezyum), soyunma, marka
- **bayrak kodları**: tr es it fr de nl pt br ar uy eng sct be ie mx ng ru at hu co hr rs ua pl jp gr us — ya da renk şeridi `"#renk1,#renk2"`
- `ozel_svg` (isteğe bağlı): sahneye eklenecek ham SVG (1080x1920 koordinat).

## Kurallar
- Kulüp logosu ve maç görüntüsü yok. Gerçek kişi fotoğrafı yalnız `foto` sahnesiyle, lisansı uygun dosyayla ve kredisiyle. Gerçek kişiler adlarıyla anılır; Hoca anlatıcıdır.
- İlk cümle en çarpıcı an ama sonucu söylemez (merak açar); sonuç son 1–2 cümlede. İlk iki cümlede arka plan yok. Toplam anlatım 45–65 kelime (≈20–30 sn); görüntü en geç 3–4 sn'de bir değişir. Kapanış soru + takip + orta rozet otomatik.

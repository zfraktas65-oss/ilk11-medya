# İLK 11 · Hikâye motoru şablonları

> **VARSAYILAN STİL: KARAKTERLİ ÇİZGİ FİLM** (sayfa sahibinin seçimi, 2026-10-28). Hikâye (19:00) ve portre (13:00) Reels'leri bundan sonra aşağıdaki **c\*** sahneleriyle yapılır: iri kafalı, yüz ifadeli çizgi film oyuncular, canlı tribünlü gece stadyumu, TV skor bandı, harf harf zıplayan yazılar. Eski sahneler (kanca, tahta, skor, sayi, an, zafer) yalnız hiçbir c\* sahnesi hikâyeye uymuyorsa kullanılır. Gerçek kişi fotoğrafı kuralı (motor/FOTO_VIDEO.md) sürer: kesik `foto` sahnesi `"arka": "stadyum"` ile aynı çizgi film stadyumunun önünde gösterilir. Hoca anlatıcı ve kapanış değişmedi.

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
- Kapanış OTOMATİK eklenir; metne yazma. Ayrı son ekran YOK (2026-10-24, 1954 kura Reels'i: son ekran gelince kalan izleyici %35'ten %5'e düştü): `soru` son cümlenin başında rozetin altında (y≈322–400) belirir, Hoca'nın "Daha fazlası için İlk On Bir'i takip etmeyi unutma!" sesi son cümleden hemen sonra son sahnenin üstünde çalar ve el rozetteki TAKİP ET'e yeniden dokunur. Son sahnede y≈322–400 bandına önemli yazı koyma. `"kapanis": "kart"` eski ayrı kapanış kartını kullanır (gerekmedikçe kullanma).
- **Yarın etiketi:** `"yarin": "YARIN 13:00 · HAGİ"` (≤ 28 karakter) sorunun hemen altında lime şerit olarak belirir (2026-10-29: takip için "yarın ne var" sözü). Görevler bunu her gün doldurur ve ertesi gün o konuyu seçer.
- **Takip rozeti** (OTOMATİK): 3. cümlenin başında (en erken 5. sn) üst etiketin yerine "<rozet> · TAKİP ET" rozeti çıkar, el ikonu butona dokunur ve videonun sonuna kadar kalır. `"rozet"`: rozet metni (varsayılan "HER AKŞAM 19:00 · YENİ HİKÂYE"; portre: "HER GÜN 13:00 · BİR EFSANE"; `""` kapatır), `"rozet_sn"`: başlama saniyesi (isteğe bağlı). Rozet y≈204–300 bandındadır; sahnelerde bu bandın içine yazı koyma.
- `at`: o anın söylendiği kelimenin başı (küçük harf, ör. `"madrid"`, rakamlı altyazıda `"2-2"`) ya da sahne başından saniye (sayı).
- Metinlerde Türkçe büyük harf kullan (İ, Ş, Ğ…). Yabancı adlar özgün yazımıyla: LILLE, LIVERPOOL.
- `*kelime*` vurgulu (neon yeşil) yazar. Başlıkta `|` ikinci satıra geçer.

## Karakterli çizgi film sahneleri (VARSAYILAN)
Çizimi `motor/cizgi.js` yapar; her karede yeniden çizilir (tribün coşar, kamera yakınlaşır, yazılar harf harf zıplar). Tüm sahnelerde zemin aynı gece stadyumudur. Yerleşim altyazı bandına (y 1170–1500) ve rozet/soru bandına (y 204–410) göre ayarlıdır; ek koordinat verme. `at` / `*_at`: altyazıdaki kelimenin başı (rakamlı altyazıda rakam: `"3"`, `"2-2"`) ya da sahne başından saniye.

**Karakter tanımı** (`oyuncu`, `atan`, `kaleci`, `sol`, `sag`, `oyuncular[]`, `sol_forma`, `sag_forma`):
`{"takim":"gs","no":"10","ad":"HAGI","sac":"kahve","ten":"acik","sakal":false}`
- `takim` hazır renkler: `tr` (milli), `gs`, `fb`, `bjk`, `ts`, `kaleci` (lime), `kirmizi`, `beyaz`, `siyah`, `mavi`, `sari`, `lacivert`. Diğer kulüpler için renkleri ver: `"forma":"#E30A17"` (ya da `"#renk1,#renk2"` → çubuklu), `"forma2"`, `"desen":"cubuk"|"parcali"`, `"sort"`, `"corap"`, `"eldiven"`. Renkleri kulübün bilinen renklerinden al; logo çizilmez.
- `no` forma numarası (bilinmiyorsa yazma), `ad` isim etiketi (BÜYÜK HARF). `sac`: siyah|kahve|sari|kizil|gri|beyaz|yok ya da #renk. `ten`: acik|bugday|esmer|koyu ya da #renk. Gerçek kişiyi saygılı ve genel çiz (forma, numara, saç rengi yeter); karikatürleştirme yok.
- `ifade`: `uzgun` | `kararli` | `bagir` | `mutlu` | `saskin`. `poz`: `dur` | `yumruk` | `kos`.
- **Konuşma balonu kuralı:** gerçek bir kişinin karakterine balonla söz söyletmek yalnız **doğrulanmış gerçek bir söz** için (kısaltılmış, ≤ 30 karakter). Uydurma söz YOK; duygu için `ifade`, `efekt`, `damga` kullan.

### ckanca — açılış (ilk sahne; ckarakter ile aynı, `baslik` zorunlu)
`{"tip":"ckanca","cumleler":[0],"baslik":"DEVREDE *0-3* GERİDE!","oyuncu":{"forma":"#E30A17","no":"8"},"ifade":"uzgun","efekt":"bulut","ifade2":"kararli","ifade2_at":"ama","skor":{"sol":"LİV","sag":"MİL","deger":"0-3"}}`
- Tek karakter yakın plan. `ifade2` + `ifade2_at`: dönüm kelimesinde yüz değişir, karakter zıplar, kamera vurur (kanca için güçlü: üzgün → kararlı, şaşkın → mutlu). `poz2` de verilebilir.
- `efekt`: `bulut` (yağmur bulutu, ifade2'de dağılır) | `soru` | `unlem` | `ter` | `yildiz`; `efekt2`: ifade2'den sonra. `skor`: TV skor bandı `{"sol","sag","deger"}` (+ `"etiket":"PEN"`). `ust`: küçük lime etiket. `ad`: isim etiketi. `balon`: `{"metin","at"}` (kural yukarıda). `damga`: `{"metin","at","renk"}`.
- `baslik` ≤ 5 kelime, `*vurgu*` lime yazar; tek satır, sığmazsa küçülür (`|` kullanma).

### ckarakter — tek karakter anı (dönüm noktası, duygu, tanıtım)
ckanca ile aynı alanlar; `baslik` isteğe bağlı.
`{"tip":"ckarakter","cumleler":[3],"oyuncu":{"takim":"tr","no":"10","ad":"ARDA GÜLER"},"ifade":"saskin","ifade2":"mutlu","ifade2_at":"rekor","poz2":"yumruk","efekt2":"yildiz","damga":{"metin":"REKOR","at":"rekor"}}`

### cgol — gol anı (yandan şut, file sallanır, kaleci ters köşe, tribün coşar)
`{"tip":"cgol","cumleler":[4],"atan":{"forma":"#E30A17","no":"8","ad":"GERRARD"},"kaleci":{"takim":"beyaz"},"dakika":"54'","skor":{"sol":"LİV","sag":"MİL","once":"0-3","sonra":"1-3"},"at":"ağları"}`
- `at`: topun ağlara girdiği kelime (en erken 0,95 sn; şut 0,6 sn önce başlar). Skor bandı golde `once` → `sonra` döner. `metin` (varsayılan "GOL!"), `yukseklik`: "alcak", `kaleci_yon`: "sag", `baslik` isteğe bağlı.

### ckurtaris — kaleci kurtarışı (önden kale, uçan kaleci, yıldızlar)
`{"tip":"ckurtaris","cumleler":[5,6],"baslik":"SON PENALTI: *ŞEVÇENKO*","kaleci":{"takim":"kaleci","sac":"sari"},"at":"uzandı","yon":"sol","metin":"KURTARDI!","alt":"DUDEK KAHRAMAN"}`
- `at`: kurtarış kelimesi (top 0,5 sn önce yola çıkar). `yon`: sol | sag. `skor` isteğe bağlı.

### ckupa — kupa/şampiyonluk (kupa kaldırılır, konfeti, havai fişek, tribün coşar)
`{"tip":"ckupa","cumleler":[8],"kelime":"ŞAMPİYON","alt":"LİVERPOOL · 2005","oyuncu":{"forma":"#E30A17"},"at":"kaldırdı","kupa":"kulakli"}`
- `oyuncular`: 3 karakter ayrı ayrı (orta kupayı kaldırır); yoksa `oyuncu` üçüne uygulanır. `kupa`: kulakli (Şampiyonlar Ligi) | klasik (altın kupa). `kelime` ≤ 10 harf ideal.

### cikili — iki karakter karşı karşıya (rakipler, hoca–oyuncu, transfer, derbi)
`{"tip":"cikili","cumleler":[1],"baslik":"*DERBİ* GÜNÜ","sol":{"takim":"gs","ad":"GALATASARAY","ifade":"kararli"},"sag":{"takim":"fb","ad":"FENERBAHÇE","ifade":"kararli","ifade2":"saskin","ifade2_at":"gol"},"vs":"VS","vs_at":0.6}`
- Karakterler iki yandan kayarak girer, ortada VS rozeti patlar (`"vs":""` kapatır; "→" transfer için). Her tarafa `balon` (kural yukarıda), `ifade2`/`ifade2_at`.

### csayi — dev sayı/istatistik
`{"tip":"csayi","cumleler":[4],"ust":"6 DAKİKADA","sayi":"3 GOL","etiket":"SKOR 3-3","at":"3","oyuncu":{"forma":"#E30A17","no":"14"},"ifade":"mutlu","damga":{"metin":"REKOR","at":"rekor"}}`
- `sayi` ≤ 9 karakter ideal (sığmazsa küçülür). `oyuncu` isteğe bağlı (sol altta tepki verir; `ifade` varsayılan saskin).

### ctabela — stadyumun dev skor tabelası
`{"tip":"ctabela","cumleler":[2],"ust":"ŞAMPİYONLAR LİGİ FİNALİ · 2005","sol":"LİVERPOOL","sag":"MİLAN","skor":"0-3","sol_forma":{"forma":"#E30A17"},"sag_forma":{"takim":"beyaz"},"at":"finali","damga":{"metin":"İSTANBUL","at":"istanbul"}}`
- Skor `at` anında yanar (önce "– –"). Takım adları ve forma ikonları tabelada; bayrak gerekiyorsa adın yanına yazma, `ust`'e ülke/turnuva yaz.

### Önerilen akış (5–7 sahne)
- Hikâye: `ckanca` (gerilim, ifade değişimi) → `cikili` / `ctabela` (tehlikede ne var) → `cgol` / `ckurtaris` / `ckarakter` (dönüm anı) → `csayi` (çarpıcı rakam) → `foto` (`"arka":"stadyum"`, kişi kesik fotoğrafıyla) → `ckupa` ya da `ckarakter` (sonuç).
- Portre: `ckanca` (kişi karakteri, `ad` etiketi, `baslik` kişinin adı) → `foto` (`"arka":"stadyum"`) → `ckarakter` (dönüm noktası) → `ctabela`/`csayi` (rekor, kupa sayısı) → `cgol`/`ckupa` (zirve).
- Görüntü en geç 3–4 sn'de bir değişsin; aynı c* tipi art arda iki kez gelmesin.

## Eski sahne tipleri (yalnız çizgi film sahnesi uymazsa)

### kanca — açılış (ilk sahne)
`{"tip":"kanca","cumleler":[0],"baslik":"*5000'DE 1* İHTİMAL","ikon":"para","hoca":"smile","arka":"karanlik","damga":{"metin":"İMKÂNSIZ?","at":"bahisçiler"}}`
- `hoca`: smile | wink | yok ; `damga` isteğe bağlı

### tahta — Hoca taktik tahtasında anlatır (1–3 satır, tebeşirle belirir)
`{"tip":"tahta","cumleler":[1,2],"satirlar":[{"metin":"2015-16","at":"sezon"},{"metin":"LEICESTER CITY","at":"leicester","boyut":80,"bayrak":"eng"}]}`

### skor — skor tabelası (1–3 satır) + isteğe bağlı damga
`{"tip":"skor","cumleler":[3,4],"baslik":"ELEME · 1954","satirlar":[{"etiket":"MADRİD","sol":"İSPANYA","sol_bayrak":"es","skor":"4-1","sag":"TÜRKİYE","sag_bayrak":"tr","at":"madrid"}],"damga":{"metin":"PUANLAR EŞİT","at":"puanlar"}}`
- Kulüpler için bayrak yerine renk şeridi: `"sol_bayrak":"#FDB913,#0053A0"`. Sayfa sahibinin gönderdiği logo `motor/logolar/`'da varsa `"logo:<ad>"` (ör. `"logo:liverpool"`) kullanılabilir (2026-10-25, sayfa sahibinin isteği).

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
- **Varsayılan: arka planı kaldırılmış kişi.** `foto` bir `.png` ise (motor/kesik.py çıktısı, `motor/fotolar/kesik/`) kişi çerçevesiz, yeşil ışıltının önünde, altyazı bandının üstüne oturacak şekilde büyük çizilir. Kişi fotoğraflarını her zaman bu hâliyle kullan (bkz. motor/FOTO_VIDEO.md). Çizgi film Reels'lerinde **`"arka": "stadyum"`** ver (kişi, diğer sahnelerdeki canlı çizgi film stadyumunun önünde durur); `arka` varsayılanı "marka".
- **Birden çok kişi:** `"fotolar": [{"foto":"a.png","at":"gerrard","ad":"GERRARD"}, ...]` (2–3 kesik PNG) yan yana, her biri kendi `at` anında belirir; `ad` altta isim etiketi. `damga` üstte (`boyut` ops.).

## Seçenekler
- **ikon**: top, kupa, duduk, saat, kart_kirmizi, kart_sari, para, sozlesme, kale, soru, unlem, fanus, mikrofon, `bayrak:<kod>`, `forma:<renk1>,<renk2>,<numara>` (ör. `forma:#E30A17,#FFFFFF,10`)
- **arka**: stadyum (çizgi film stadyumu — çizgi film Reels'lerinde foto sahnesi için), karanlik (spot ışığı), gece (stadyum gecesi), gunbatimi, roma (Kolezyum), soyunma, marka
- **bayrak kodları**: tr es it fr de nl pt br ar uy eng sct be ie mx ng ru at hu co hr rs ua pl jp gr us — ya da renk şeridi `"#renk1,#renk2"`
- `ozel_svg` (isteğe bağlı): sahneye eklenecek ham SVG (1080x1920 koordinat).

## Kurallar
- Kulüp logosu ve maç görüntüsü yok. Gerçek kişi fotoğrafı yalnız `foto` sahnesiyle, lisansı uygun dosyayla, kredisiyle ve arka planı kaldırılmış (.png) hâliyle. Gerçek kişiler adlarıyla anılır; Hoca anlatıcıdır.
- İlk cümle en çarpıcı an ama sonucu söylemez (merak açar); sonuç son 1–2 cümlede. Kanca formülleri ve seçim kuralı: motor/kancalar.md (kanca sahnesinin `baslik`'ı aynı formülün ≤ 5 kelimelik ekran hâli). İlk iki cümlede arka plan yok. Toplam anlatım 45–65 kelime (≈20–30 sn); görüntü en geç 3–4 sn'de bir değişir. Kapanış (soru + Hoca'nın takip çağrısı, ayrı son ekran olmadan) ve orta rozet otomatik. Toplam video ≈24–34 sn.

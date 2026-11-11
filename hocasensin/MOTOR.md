# Bölüm motoru — senaryo biçimi (motor/bolum.py)

```
python3 motor/bolum.py <bolum_klasoru>/senaryo.json --kelimeler          # kelime listesi (w:N çapaları için)
python3 motor/bolum.py <bolum_klasoru>/senaryo.json <cikti> --onizleme   # her sahnenin ortası (ya da: --onizleme 3.5,w:20,40)
python3 motor/bolum.py <bolum_klasoru>/senaryo.json <cikti>              # tam video: <cikti>/<slug>.mp4 + kapak.jpg (≈1 dk sürer)
```
Çıktı 1080×1920, 30 fps; ses = seslendirme + müzik (otomatik kısılır) + efektler, −14 LUFS. Örnek: `bolumler/001/senaryo.json`.

## Üst alanlar
| alan | açıklama |
|---|---|
| slug | çıktı dosya adı, ör. `anadoluspor_bolum002` |
| ses | seslendirme dosyası (senaryo klasörüne göre), ör. `ses.mp3` |
| kelimeler | ElevenLabs transcribe `words.json` (kelime zamanları) |
| muzik | `neseli_1` / `neseli_2` (varliklar/muzik) — kısa gelirse döngüye girer |
| muzik_ses | varsayılan 0.30 |
| kapak | kapak karesinin zamanı (sn ya da çapa) — Reels kapağı; kanca sahnesinin en dolu anı |
| son | video sonu (varsayılan: son kelime + 1,4 sn) |
| birlestir | altyazıda rakama çevrilecek kelime dizileri: `[["yüz","elli","beğeni"],"150 beğeni"]` (küçük harf, noktalamasız) |
| sesler | ek efektler: `{"tip": "duduk|kisa_duduk|klik|zil|uzgun|pop|gum|kasa|tezahurat", "t": <zaman>, "ses": 0.8}` |
| altyazi_y | altyazı satırının y'si (varsayılan 1395) |
| sahneler | sahne listesi (sırayla; her sahne bir sonrakinin `bas`ına kadar sürer) |

**Zaman:** saniye (`12.4`) ya da kelime çapası: `"w:N"` = N. kelimenin başı, `"we:N"` = sonu, `"w:N+0.2"` / `"w:N-0.1"` kaydırma. N, `--kelimeler` listesindeki sıra (ses etiketleri `[excited]` sayılmaz). Sahne geçişlerini cümle başlarına koy (`"w:N-0.05"`).

Otomatik: altyazı (2–3 kelimelik parçalar, okunan kelime sarı), sahne başında "punch" zoom ve swoosh sesi, `pop` animasyonunda pop sesi, `stamp`'te gümleme, ışık kapanmasında klik.

## Sahne
```json
{"bas": "w:22-0.05", "arka": "halisaha", "bulanik": 0, "karanlik": 1.0, "renk": [40,10,60],
 "zoom": [1.0, 1.08], "merkez": [[0.5,0.55],[0.5,0.55]],
 "karakterler": [...], "ogeler": [...], "isik_kapali": [["w:37", "w:38"]]}
```
- `arka`: varliklar/arka içindeki ad (uzantısız) ya da yol. `bulanik` (px, karakter tanıtımında 10–12), `karanlik` (0–1), `renk` (hafif renk tonu).
- `zoom`: başlangıç→bitiş yakınlaştırma (1.0 = tam kare); `merkez`: başlangıç→bitiş odak noktası (0–1, kaydırma için).
- `isik_kapali`: o aralıkta görüntü kararır (Necmi abi ışıkları kapattı!).
- `tribun`: `{"sayi": N, "tohum": 7}` — yalnız sıra düzeni olan arka planlarla: `tribun` (varliklar/arka/tribun.json, ≈75 kişi) ve `loca` (loca.json, ≈16 kişi; loca sahnesinde zoom [1.0, 1.04], merkez [0.5, 0.45]). N çizgi taraftar (varliklar/taraftar/*.png) önden arkaya sıralara dağılır ve zıplar; kapasite ≈ 75. Tribün sahnesinde zoom [1.0, 1.05], merkez [0.5, 0.5] iyi durur; yazıları y 260–560'a (çatı hizası), öndeki karakteri ayak 1660, h 700–780 ile koy.

## Karakter
`{"ad": "cem", "h": 980, "x": 540, "ayak": 1640, "bas": <zaman>, "bitis": <zaman>, "giris": "up|left|right|pop|none", "sure": 0.35, "ayna": false, "golge": false, "kos": false, "faz": 0}`
- Tek karakter: h 950–1000, x 540, ayak 1640. Grup (4 kişi): h 600–800, x 170/380/690/905.
- `golge`: siyah siluet (gizem/tanıtım). `kos`: koşar gibi zıplar. `ayna`: yatay çevir. `faz`: kişiler aynı anda sallanmasın diye 0–1.

## Öğeler (ogeler)
Ortak: `tip`, `bas`, `bitis`, `x` (540), `y` (320), `anim` (`pop` | `stamp` | `down` | `fade`), `sure`, `dondur` (derece), `nabiz` (hafif büyüyüp küçülme), `titre` (girişte sallanma).
| tip | alanlar | ne için |
|---|---|---|
| seri | bolum | "ANADOLUSPOR / BÖLÜM N" rozeti (ilk sahnede, y 300, anim down) |
| etiket | metin, boyut (56), renk, zemin, egim | üst başlık şeridi; renk/zemin: sari, mor, beyaz, siyah, kirmizi, yesil, mavi, turuncu |
| baslik | metin, boyut (190), renk, egim | dev sarı yazı (GÜN 3, GOL!, SENSİN!) |
| damga | metin, boyut, renk, egim | kırmızı mühür (YOK!, MAÇ YOK!, HAKEM: MUHTAR) — anim stamp |
| isim | no, ad, alt | karakter künyesi (sol üst kutu); no 1–3 karakter |
| arma | boyut | kulüp arması |
| sayac | baslik, deger, alt, deger_renk, alt_renk | büyük sayı kartı (KULÜP KASASI / 1.250 TL, TRİBÜN / 37 TARAFTAR) |
| begeni | metin, zemin | yeşil kalpli çıkartma ("1 BEĞENİ = 10 TL") |
| secenek | harf, ad, karakter, oran, renk | seçenek kartı (karakterin başı); oran = kafanın boy oranı (0.36–0.42) |
| tabela | ust, metin | asılı tabela ("SAATİ" / "1.500 TL") |
| ilerleme | sol, sag, oran (0–1), isaret | lig ilerleme çubuğu |
| balon | metin | konuşma balonu (yalnız kurgu karakterler için) |
| pankart | metin, zemin, renk, egim | tribün pankartı (kumaş bez; ör. "ANADOLUSPOR TRİBÜNÜ", "@ad TRİBÜNDE!") |
| liste | baslik, isimler (liste), sutun (2), satir (görünen satır, 9) | isim panosu; @ kendiliğinden eklenir; sığmazsa sahne boyunca yavaşça kayar. Tribün sahnesinde y≈420 (5–10 isim), loca sahnesinde y≈1085 ve satir 6 |
| skor | ev, dep, ev_skor, dep_skor, dakika | maç skor tabelası (ör. y 330) |
| resim | dosya, genislik, golge | herhangi bir PNG (yeni nesne/karakter) |

## Yerleşim kuralları
- Instagram arayüzü üstte ~0–220 px ve altta ~1650–1920 px'i kapatır, sağ altta butonlar var: yazıları y 260–1250 arasına koy; altyazı y≈1395.
- Bir sahnede en fazla 3 yazı öğesi; her öğe konuşmada geçtiği kelimede (`w:N`) belirsin.
- Karakter başı (ayak 1640, h 980 için ≈ y 660–900) ile yazılar çakışmasın: başlıkları y 300–560'a koy.
- Önizlemede taşma, çakışma, boş sahne olmadığını kontrol et.

## Yeni öğeler ve alanlar (2026-11-11)
- **`kasa`** — kasa defteri: `{"tip":"kasa","baslik":"KULÜP KASASI","satirlar":[["132 BEĞENİ × 100 TL","+13.200 TL"],["SAHA KİRASI (1 HAFTA)","−1.500 TL"]],"kalan":"11.700 TL","not":"SONRAKİ KİRA: 7 BÖLÜM SONRA","y":760}`. Satır rengi `+` ile başlıyorsa yeşil, değilse kırmızı (3. eleman renk adı verilebilir). Kademeli göstermek için iki `kasa` öğesi kullan (ilki `bitis`, ikincisi `anim:"fade"`).
- **`puan`** — hareketli puan tablosu: `{"tip":"puan","baslik":"HALI SAHA LİGİ · 2. HAFTA","satirlar":[["TAKIM",O,G,B,M,"AV",P], ...yeni sırada],"eski":[eski sıradaki takım adları],"vurgu":"ANADOLUSPOR","rozet":"▲5","alt":"ŞAMPİYON 5 GALİBİYETLE ÜST LİGE ÇIKAR","bas":"we:N+0.15","gecikme":0.7,"kayma":1.1,"y":860}`. Satırlar `gecikme` sn sonra `kayma` sn içinde eski yerden yeni yere kayar; rozet kayma bitince çıkar ("▼N" düşüş).
- **`yazi`** — çok satırlı düz yazı (`metin` içinde `\n`, `font`, `boyut`, `renk`, `kontur`). **`bayrak`** — dalgalanan Türk bayrağı direkte (`genislik`, `yarim`: yarıya indirilmiş).
- **Karakter etiketi:** karakterde `"etiket":"kullanici","etiket_alt":"MEVKİ"` → başın hemen altında küçük @isim + sarı unvan şeridi (`etiket_y` oranı, varsayılan 0.37). `giris:"pop"` ise etiket giriş bitince çıkar.
- **Kalabalık isimleri:** sahnede `"tribun":{"isimler":[...],"ozel":{"kullanici":"UNVAN"},"sayi":ek_isimsiz,"aralik":0.42,"etiket_boyut":15,"tohum":11}` → isimler ön sıralardan başlayarak figürlerin başının altına yazılır. Okunurluk için tribünde zoom 1.75 + merkez x 0.28→0.72, locada zoom 1.6 + merkez y 0.38 ve sahne başına ≤30 isim.
- **Sahne `altyazi_y`:** o sahnede altyazının y konumu (`false` = altyazı yok). Kadro sahnesinde 1232 (iki sıra oyuncunun arası).
- **Üst düzey `muzik_bas`:** müziğin başlama zamanı (çapa da olur), yumuşak girişle.
- **Sese sessizlik ekleme** (isim/tablo sahneleri için): ham sesi `atrim` + `anullsrc` ile böl, kelimeler.json'daki `start/end` değerlerini ekleme noktasından sonra kaydır (Bölüm 2 örneği: 56.06 s +0.8, 60.82 s +1.5, 72.68 s +3.0).

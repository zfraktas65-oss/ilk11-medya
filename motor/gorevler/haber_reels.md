# İLK 11 – Haber Reels (büyük son dakika haberleri) görev talimatı

**Neden (sayfa sahibinin onayı, 2026-11-02):** Metricool'a göre kaydırmalı gönderiler gönderi başına ortalama 6 kişiye ulaşıyor, Reels'ler ise ortalama ~2.000 kez izleniyor. Bu yüzden **büyük** son dakika haberleri kart gönderisi yerine kısa bir Reels olarak paylaşılır; haberin hikâye kartı yine STORY olarak paylaşılır (takipçiler hemen görsün).

**KİŞİ FOTOĞRAFI VE VİDEO:** motor/FOTO_VIDEO.md'yi oku ve uygula.

Bu dosyayı SON DAKİKA görevi (motor/GOREVLER.md, A bölümü) çağırır: haber KURALLAR'a göre doğrulanmış ve `~/sondakika.json` yazılmış olarak gelir. Otomatik çalışmadır; kullanıcıya soru sorma. Tüm metinler Türkçe.

## Ne zaman uygulanır
Hepsi doğruysa: (1) haber aşağıdaki **BÜYÜK** listede, (2) bugün henüz haber Reels'i paylaşılmadı (motor/paylasilan.txt'de bugünün tarihiyle başlayıp ` (reels)` ile biten bir `sondakika` satırı yok — günde en fazla 1), (3) `motor/MANUEL_MOD` dosyası yok. Biri tutmuyorsa bu dosyayı uygulama; GOREVLER.md'deki normal kart akışı geçerlidir.

**BÜYÜK sayılanlar** (takip edilen 5 takım için):
- resmî transfer imzası (KAP bildirimi ya da kulübün resmî duyurusu) ya da yıldız bir oyuncunun resmî ayrılığı,
- teknik direktör ataması ya da ayrılığı (A Milli Takım dahil),
- kulüp başkanı değişikliği,
- kulübün açıkladığı, yıldız bir oyuncuyu uzun süre oyundan uzak tutacak sakatlık,
- kırılan büyük bir rekor.
PFDK/UEFA cezaları, aday kadrolar, maç saati/stat değişiklikleri ve diğer açıklamalar kart olarak paylaşılmaya devam eder.

## H1 · Hikâye kartı
`cd ~/ilk11-medya && rm -rf ~/cikti && python3 motor/ozel.py ~/sondakika.json ~/cikti`. Bu akışta yalnız `~/cikti/hikaye.jpg` kullanılır; Read ile aç ve kontrol et (gönderi kartları paylaşılmaz).

## H2 · Metin
5–6 kısa cümle (2. cümle kanca sonrası sesli takip çağrısı), toplam 32–44 kelime (takip cümlesi dahil; video ≈ 20–27 sn). Her cümle doğrulanmış bilgiye dayanır.
- **İlk cümle haberin kendisi:** kim, ne oldu; en çarpıcı kısım önde (✓ "Fenerbahçe'de geçici görev resmen Dirk Kuyt'a verildi."). Haberde sonuç saklanmaz.
- Sonra 1–2 doğrulanmış ayrıntı (sözleşme süresi, bonservis yalnız resmî açıklamada geçiyorsa; sakatlıkta yalnız kulübün açıkladığı tanı/süre), neden önemli olduğu (kendi cümlenle, taraf tutmadan, yorum katmadan) ve doğrulanmışsa sıradaki adım (ilk maç, dönüş tarihi).
- Söylenti, tahmin, uydurma söz yok. Bir kişinin sözü aktarılacaksa yalnız kaynakta birebir geçen kısa söz.
- Sayıları ve tarihleri yazıyla yaz (seslendirme); altyazı için rakamlı hâlini senaryoda ayrıca ver. Kapanıştaki takip çağrısını metne YAZMA (motor ekler); ama 2. cümle her zaman SABLONLAR.md'deki kanca sonrası sesli takip çağrısıdır (birebir `{"soz": "İlk On Bir'i takip et, devamı geliyor!", "altyazi": "İLK 11'i takip et, devamı geliyor!"}`; ElevenLabs metnine de 2. paragraf olarak girer).
- Ekranda sorulacak **iki seçenekli** soru (≤ 44 karakter, "X mi Y mi?"; ör. "Doğru karar mı, erken mi?").

## H3 · Seslendirme
ToolSearch: "select:mcp__Seslendirme__creative_generate_speech,mcp__Seslendirme__creative_get_flow_run_status". creative_generate_speech: voice_id "mF7tIc9VLrznhGooGjaT" (Hoca'nın sesi), model_id "eleven_v4", prompt = cümleler, her cümle ayrı paragraf (aralarında "\n\n"). Bu çağrıyı **YALNIZCA BİR KEZ** yap (kredi harcar; hata olsa bile tekrar deneme). flow_id ve session_ids ile poll_after_seconds aralıklarla creative_get_flow_run_status çağır; tamamlanınca content_url'yi `mkdir -p ~/haber && curl -sS -m 120 -o ~/haber/ses.mp3 '<content_url>'` ile indir, ffprobe ile süresini kontrol et. İndirilemezse **H-YEDEK**'e geç.

## H4 · ~/haber/senaryo.json
motor/SABLONLAR.md'ye birebir uy. slug "TARIH-haber-<anahtarın kısa hâli>", ses "ses.mp3", cumleler (ElevenLabs metniyle aynı sayı ve sırada), **3–5 sahne**, KARAKTERLİ ÇİZGİ FİLM stili (c* sahneleri):
- `ckanca`: haberin kişisi (kulübünün/milli takımın forma renkleri, bilinen forma numarası, `ad` etiketi); `baslik` haberin ≤ 5 kelimelik özeti, vurgulu kelimeyle (ör. "KUYT *RESMEN* BAŞLADI"); haber cümlesi + 2. cümledeki takip çağrısı, `"cumleler": [0, 1]`.
- Kişinin depoda lisanslı kesik fotoğrafı varsa `foto` sahnesi (`"arka": "stadyum"`, FOTO_VIDEO.md).
- `ctabela` / `csayi`: doğrulanmış bir rakam (sözleşme yılı, rekor sayısı, dönüş süresi).
- `ckarakter`: sonuç ya da sıradaki adım.
Ayrıca: `"etiket": "İLK 11 · SON DAKİKA"`, `"rozet": "SON DAKİKALAR İLK 11'DE"`, `soru`, `kapak_sn` (kanca sahnesinin ~1.5. saniyesi). `yarin` alanı YAZMA. Kulüp logosu ve maç görüntüsü kullanma (kulüpler için renk şeridi); gerçek kişiye uydurma söz balonu YOK.

## H5 · Önizleme ve video
`cd ~/haber && python3 ~/ilk11-medya/motor/hikaye.py senaryo.json cikti --onizleme` → cikti/onizleme.png'yi Read ile aç; yazı taşması, çakışma, boş sahne, yanlış forma rengi/isim varsa senaryo.json'u düzelt (en fazla 2 tur; metni değiştirme). Sonra `python3 ~/ilk11-medya/motor/hikaye.py senaryo.json cikti` (timeout 900000 ya da run_in_background). ffprobe ile süreyi kontrol et (16–26 sn beklenir) ve videodan 2 kare çıkarıp Read ile bak. Video üretilemezse **H-YEDEK**.

## H6 · Yükle
ANAHTAR = KAYIT'taki sondakika anahtarı. Video ve hikâye kartını aynı yetim commit'te kendi dalına normal push ile yükle (force-push KULLANMA):
```
cd ~/ilk11-medya && rm -rf ~/medya && git worktree prune
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout -q --orphan medya-haberreels-<ANAHTAR> && git rm -rqf .
mkdir -p <ANAHTAR> && cp ~/haber/cikti/<slug>.mp4 ~/cikti/hikaye.jpg <ANAHTAR>/ && git add <ANAHTAR> && git commit -qm "haberreels <ANAHTAR>" && git push -q origin HEAD:refs/heads/medya-haberreels-<ANAHTAR>
SHA=$(git rev-parse HEAD)
```
Dal zaten varsa adın sonuna -2 ekle. Bağlantılar `https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/$SHA/<ANAHTAR>/<dosya>` — dal adı yerine MUTLAKA SHA; her dosya için curl ile 200 döndüğünü doğrula.

## H7 · Paylaş (Metricool, blogId "7504196")
0. **Son kontrol:** GOREVLER.md P.0 ile aynı (paylasilan.txt + son 6 saatin gönderileri); aynı haber varsa dur.
1. **REEL:** createScheduledPost, date = şu an + 3 dk (+03:00). **Aralık kuralı:** getScheduledPosts'ta bu saate 45 dakikadan yakın başka bir Instagram REEL (ör. 13:00 Portre, 19:00 Hikâye) planlı ya da yayınlanmışsa date = o REEL'in saati + 45 dk. info: providers [{"network":"instagram"}], instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}, media [mp4 bağlantısı], videoCoverMilliseconds = kapak_sn × 1000, publicationDate {"dateTime": …, "timezone": "Europe/Istanbul"}, autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids": []}. text: GOREVLER.md A.4'teki SON DAKİKA açıklaması, soru olarak H2'deki iki seçenekli soru — **ilk satır mutlaka "🚨 SON DAKİKA | <TAKIM>"** (portre ve hikâye görevleri haber Reels'ini bu önekten tanır).
2. **STORY:** createScheduledPost, date = şu an + 5 dk; instagramData {"type":"STORY","isAiGenerated":false}, media [hikaye.jpg bağlantısı], text alanı yok; diğer alanlar aynı.
3. Yanıtlarda media bağlantılarının static.metricool.com'a taşındığını kontrol et.

## H8 · Kayıt ve bildirim
KAYIT satırı: `YYYY-AA-GG SS:DD sondakika <ANAHTAR> | <kısa başlık> (reels)` (GOREVLER.md KAYIT'taki gibi pull/commit/push). SendUserMessage ile kısa özet: haber, Reels'in planlandığı saat, kaynaklar ([Başlık](URL)), plannerUrl; videoyu SendUserFile ile gönder (status "proactive").

## H-YEDEK · Reels yapılamazsa
Seslendirme indirilemez, video üretilemez ya da yükleme başarısız olursa haberi kaybetme: GOREVLER.md A'daki normal kart akışına dön (kartları üret → Y → P → KAYIT, satır sonuna "(reels)" ekleme) ve bildirime Reels'in neden yapılamadığını tek satırla ekle. Seslendirmeyi yeniden deneme.

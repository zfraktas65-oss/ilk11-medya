# Anadoluspor (@hocasensin1) – Günlük Bölüm görevi (19:00)

Görev: Instagram **@hocasensin1** için dizinin bir sonraki bölümünü (≈1 dk dikey Reels) üret ve Metricool ile **bugün 19:00**'a (Europe/Istanbul) planla. Hikâyeyi **dünkü bölümün beğeni / yorum sayıları ve takipçi sayısı** yönlendirir. Bu otomatik bir çalışmadır: kullanıcıya soru sorma, en makul seçimi yapıp devam et. Kullanıcı Türkçe konuşuyor; tüm metinler Türkçe. Sayfa sahibi (2026-11-09) her gün 19:00'da bölümün kendisine sorulmadan paylaşılmasını ve hikâyenin Metricool'daki beğeni/yorum verisine göre devam etmesini istedi.

Kök klasör: `~/ilk11-medya/hocasensin` (aşağıda K). Önce **K/HIKAYE.md** (kurallar, karakterler, ton, bölüm yapısı, açıklama şablonu) ve **K/MOTOR.md** (senaryo biçimi) dosyalarını baştan sona oku; onlara birebir uy. Durum K/durum.json'dadır.

## ADIM 0 — Saat ve tekrar kontrolü
`TZ=Europe/Istanbul date '+%F %H:%M'` ile bugünü ve saati al (BUGUN). ToolSearch ile yükle: `select:mcp__Metricool_Social_Media_Management__getScheduledPosts,mcp__Metricool_Social_Media_Management__createScheduledPost,mcp__Metricool_Social_Media_Management__getAnalyticsDataByMetrics,SendUserMessage,SendUserFile`. getScheduledPosts (brandId "7980733", BUGUN 00:00–23:59, timezone "Europe/Istanbul"): metni "Anadoluspor · Bölüm" ile başlayan bir gönderi bugün zaten planlıysa hiçbir şey üretme, SendUserMessage/SendUserFile GÖNDERME; "Bugünün bölümü zaten planlı" diye tek satırla bitir. Ayrıca K/durum.json'daki `son_bolum_tarihi` BUGUN ise (bugün zaten üretilmiş) aynı şekilde sessizce bitir. Görev her gün 17:28'de çalışır (sayfa sahibinin isteği: 17:30'da verileri alıp hazırla, 19:00'da paylaş).

## ADIM 1 — Ortam
Depo klonlu değilse: mcp__claude-code-remote__add_repo (owner "zfraktas65-oss", repo "ilk11-medya", access "push") ve `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya` (timeout 600000). `python3 -c "import cv2, numpy, PIL"` çalışmazsa `pip install --break-system-packages -q numpy pillow opencv-python-headless`. ffmpeg hazır olmalı. K/durum.json'u, **K/taraftarlar.json**'u (yorumculardan seçilen tribün lideri / forvet / kaleci; HIKAYE.md "Taraftar oyuncular" ve "Tribün" bölümleri), son bölümün K/bolumler/<NNN>/metin.txt ve senaryo.json dosyalarını oku (NNN = son_bolum, 3 haneli). N = son_bolum, M = N + 1, MMM = M'nin 3 haneli hâli. `mkdir -p K/bolumler/MMM`.

## ADIM 2 — Dünkü verileri çek (Metricool)
a) getAnalyticsDataByMetrics: brandId "7980733", from = `<son_bolum_tarihi>T00:00:00+03:00`, to = şimdi (+03:00), metrics `["IGRE02","IGRE03","IGRE06","IGRE10","IGRE07","IGRE23","IGRE12","IGRE21"]` (tarih-saat, metin, bağlantı, beğeni, yorum, izlenme, kaydetme, paylaşım). Metni `son_bolum_aciklama_basi` ile başlayan satırı bul. Sonucu K/bolumler/NNN/veri.json'a kaydet.
b) getAnalyticsDataByMetrics: aynı brandId, from = dün 00:00, to = şimdi, metrics `["IGEV01"]` → son null olmayan değer = takipçi.
c) Bölüm N bulunamazsa (yayınlanmamış ya da veri gecikmiş): sayı UYDURMA. Kararı bir gün ertele (acik_karar aynen kalsın), bu bölümü karara bağlı olmayan bir olayla yaz (ör. antrenman, yeni oyuncu denemesi, Necmi abinin sayacı bozuldu) ve sonunda aynı kararı tekrar hatırlat; bildirimde durumu belirt. Bir alan null ise onu 0 değil "veri yok" say.

## ADIM 3 — Durumu güncelle (python ile hesapla, kafadan değil)
- Bölüm N'in beğeni, yorum, izlenme değerlerini `gecmis`'teki N kaydına yaz.
- Kasa: `kasa_tl += beğeni × begeni_tl`. Borç varsa önce kasadan borç ödenir.
- Tribün: `tribun_toplam += yorum`. Takipçi: `takipci = IGEV01`.
- Karar: `beğeni >= acik_karar.esik` ise `gecerse`, değilse `gecmezse` gerçekleşti (ör. `kaleci` alanını güncelle). Sonucu not al.
- M == sonraki_kira_bolumu ise KİRA GÜNÜ: kasa ≥ kira ise öde; değilse eksik kısmı `borc_tl`'ye ekle ve kasayı 0 yap. `sonraki_kira_bolumu += 7`.
- M bir maç bölümüyse (2, 5, 8, 11… yani (M − 2) % 3 == 0) maç sonucunu HIKAYE.md "İlerleme" kurallarına göre belirle ve `mac` alanlarını güncelle (5 lig galibiyetinde bir üst lige çık: `lig` değişir, `lig_galibiyet` 0'lanır).
- Yeni hedef eşiği: HIKAYE.md'deki formül (beğeni × 1,3, 10'a yuvarla, en az 20; 3–4 bölümde bir daha kolay).
Güncel durumu bellekte tut; dosyaya ADIM 10'dan sonra yaz.

## ADIM 4 — Bölüm M metni → K/bolumler/MMM/metin.txt
HIKAYE.md "Bölüm yapısı"na uy: her cümle ayrı satır, toplam **125–150 kelime** (python ile `[...]` etiketleri hariç say). İlk satır `[excited]` ile başlayan kanca, 2. satır sesli takip çağrısı, sonra "Gün <M yazıyla>.", dünün sayıları ve karar sonucu, ana olay, durum, yeni KARAR ("Bu video <X yazıyla> beğeniyi geçerse …, geçmezse …"), yarının merakı, son satır `[excited]` kapanış (takip et, beğen, yorum yaz). Sayılar yazıyla. Önceki bölümlerle tutarlı ol (`gecmis` özetleri, `yarin_soz`: dün izleyiciye ne söz verildiyse bugün o olsun). Yorum metni okuyamadığını unutma: yorum alıntısı ya da "en çok beğenilen yorum" yok. Esprili, hareketli, her 2–3 cümlede bir yeni görüntü.
**Taraftar rolleri:** taraftarlar.json'da `kullanici` dolu ve `tanitildi_bolum` null olan her rolü bu bölümde tanıt (HIKAYE.md kuralları; olumlu ve saygılı; seslendirmede yalnız `okunus` ya da ad söylemeden). Boş roller için (Bölüm 2'de mutlaka, sonra 2–3 bölümde bir) "taraftardan forvet / kaleci / tribün lideri arıyoruz, yorum yazanlar arasından seçeceğiz" duyurusu yap. Kullanıcı adı UYDURMA, yorumcu SEÇME.
**Tribün:** maç bölümlerinde ve çoğu bölümde bir tribün sahnesi olsun; taraftar sayısı = `tribun_toplam` (ADIM 3'te güncellenmiş hâli).
**Beğenenler tribüne, takip edenler locaya:** taraftarlar.json'da `gosterildi_bolum` null olan `tribun_isimleri` (beğenenler) ve `loca_isimleri` (takip edenler) varsa bu bölümde göster: tribün sahnesinde "TRİBÜNDE BUGÜN", loca sahnesinde (arka `loca`, `tribun.sayi` = min(takipçi, 16)) "LOCAYA HOŞ GELDİNİZ" başlıklı `liste` öğesi; anlatımda tek cümle ("Locaya yeni gelenler var, isimler ekranda!"). Yalnız dosyadaki isimler; isim uydurma, okuma.

## ADIM 5 — Seslendirme ve kelime zamanları
ToolSearch: `select:mcp__Seslendirme__creative_create_flow,mcp__Seslendirme__creative_generate_speech,mcp__Seslendirme__creative_get_flow_run_status,mcp__Seslendirme__creative_add_flow_asset_node,mcp__Seslendirme__creative_transcribe_audio`.
1. creative_create_flow (name "Anadoluspor - Bölüm M") → FLOW.
2. creative_generate_speech: flow_id FLOW, voice_id **"514g2BbzaXZcAjtgXoOr"** (Özenç — dizinin sesi, değiştirme), model_id "eleven_v4", generations_count 1, prompt = metin.txt'nin içeriği. **YALNIZCA BİR KEZ** çağır (kredi harcar; hata olsa bile tekrar deneme).
3. creative_get_flow_run_status ile (Bash `sleep` ile poll_after_seconds bekleyerek) tamamlanınca content_url'yi `curl -sS -m 120 -o K/bolumler/MMM/ses.mp3 '<url>'` ile indir; ffprobe ile süreyi ölç (beklenen 52–68 sn).
4. creative_add_flow_asset_node (flow_id FLOW, modality "audio", generation_id = sesin generation id'si) → creative_transcribe_audio (flow_id FLOW, model_id "eleven_scribe_v1", connect_from [o düğüm]) → creative_get_flow_run_status ile bekle → `words_download_url`'yi `K/bolumler/MMM/kelimeler.json` olarak indir.
Ses indirilemezse videoyu yapma; ADIM 11'deki gibi bildir.

## ADIM 6 — Yeni görsel (yalnız gerekiyorsa; en fazla 1 arka plan + 1 karakter)
Önce varliklar/arka ve varliklar/karakter'deki hazır görselleri kullan. Hikâye gerçekten yeni bir mekân ya da karakter istiyorsa: ToolSearch `select:mcp__Seslendirme__creative_add_flow_node,mcp__Seslendirme__creative_run_flow_nodes,mcp__Seslendirme__creative_get_generations,mcp__Seslendirme__creative_attach_reference_file`.
- **Arka plan:** creative_add_flow_node (flow_id FLOW, node_type "image-generation", model_id "gpt-image-2.5-sunburst", model_parameters {"aspect_ratio":"9:16","resolution":"2K","quality":"high"}, prompt = HIKAYE.md arka plan stili + mekân). creative_run_flow_nodes (generations_count 1, bir kez). Bitince creative_get_generations ile full_res_url'yi indir, Read ile bak, `varliklar/arka/<ad>.jpg` olarak JPG (kalite 93) kaydet.
- **Karakter:** stil referansı için creative_add_flow_asset_node (modality "image", generation_id "ZKPPwo6ezgvvOIzYGn1M"); hata verirse creative_attach_reference_file ile `https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/main/hocasensin/varliklar/karakter/_karakter_sayfasi.jpg`. creative_add_flow_node (aynı model, model_parameters {"aspect_ratio":"2:3","resolution":"2K","quality":"high"}, connect_from [referans düğümü], prompt = HIKAYE.md karakter stili + tarif + "single character, full body, plain flat light grey background (#E6E6E6), no text, no logos, no brand marks"). Bir kez çalıştır, indir, `python3 K/motor/kes.py girdi.png K/varliklar/karakter/<ad>.png`, sonucu Read ile kontrol et. HIKAYE.md'deki karakter tablosuna bir satır ekle.

## ADIM 7 — Senaryo ve önizleme
`python3 K/motor/bolum.py K/bolumler/MMM/senaryo.json --kelimeler` ile kelime listesini al (önce slug/ses/kelimeler ve tek sahneli geçici bir senaryo yaz). MOTOR.md'ye göre **K/bolumler/MMM/senaryo.json**'u yaz: slug "anadoluspor_bolumMMM", 11–16 sahne, sahneler cümle başlarında (`w:N-0.05`), ilk sahnede `seri` rozeti (bolum M) ve kanca görseli, dünün sayıları için `sayac` (KULÜP KASASI / TRİBÜN / TEKNİK HEYET), maç bölümünde `skor`, lig değişiminde `ilerleme`, KARAR sahnesinde "KARAR #M" + "HEDEF: X BEĞENİ" etiketleri ve "GEÇERSE"/"GEÇMEZSE" altında `secenek` kartları, son sahnede ekip + TAKİP ET. Tribün sahnesi: `"arka": "tribun"` + `"tribun": {"sayi": tribun_toplam}` + "TRİBÜN: N TARAFTAR" sayacı/etiketi. Taraftar oyuncu tanıtımında `isim` künyesi (no TL/9/1, ad "@kullanici", alt unvan); boş rol duyurusunda karakteri `golge: true` (siluet) ve "ARANIYOR" damgasıyla göster. Sayıları altyazıda rakamla göstermek için `birlestir` yaz. `kapak` = kanca sahnesinin en dolu anı. Bölüm 1 örneği: K/bolumler/001/senaryo.json.
`python3 K/motor/bolum.py K/bolumler/MMM/senaryo.json ~/onizleme --onizleme` → ~/onizleme/onizleme.jpg'yi Read ile aç: yazı taşması, çakışma, boş sahne, yanlış sayı, karakterin yanlış sahnede olması var mı? Düzelt ve tekrarla (en fazla 3 tur). Bu adımdan sonra metni değiştirme.

## ADIM 8 — Video
`python3 K/motor/bolum.py K/bolumler/MMM/senaryo.json ~/cikti` (Bash timeout 600000; ≈1–2 dk). ffprobe ile süreyi kontrol et; ffmpeg ile 3 kare çıkarıp Read ile bak.

## ADIM 9 — Medyayı yükle
```
cd ~/ilk11-medya && git config user.name "Claude" && git config user.email "noreply@anthropic.com"
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout --orphan medya-hocasensin && git rm -rqf .
mkdir -p BUGUN && cp ~/cikti/anadoluspor_bolumMMM.mp4 ~/cikti/kapak.jpg BUGUN/ && git add BUGUN && git commit -qm "hocasensin bolum M" && git push -f origin HEAD:medya-hocasensin
```
SHA=$(git rev-parse HEAD). Bağlantı: `https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/<SHA>/BUGUN/anadoluspor_bolumMMM.mp4` — dal adı yerine MUTLAKA SHA. `curl -sS -o /dev/null -w "%{http_code}" -r 0-1000 <bağlantı>` 200 ya da 206 dönmeli (gerekirse 10 sn bekleyip yeniden dene).

## ADIM 10 — Metricool'a planla ve durumu kaydet
createScheduledPost: blogId "7980733"; date BUGUN 19:00 (+03:00) — saat 18:50'yi geçtiyse şimdi + 10 dk. info: providers [{"network":"instagram"}], instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}, media [SHA'lı bağlantı], videoCoverMilliseconds = kapak × 1000 (sn'yi çapadan hesapla), publicationDate {"dateTime": "...", "timezone": "Europe/Istanbul"}, autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids": []}, text = HIKAYE.md açıklama şablonu (ilk satır "Anadoluspor · Bölüm M ⚽"; bu bölümde tanıtılan taraftar oyuncuları `@kullanici` ile etiketle). Yanıtta medyanın static.metricool.com'a taşındığını kontrol et.
Başarılıysa K/durum.json'u güncelle: son_bolum = M, son_bolum_tarihi = BUGUN, son_bolum_aciklama_basi = "Anadoluspor · Bölüm M", kasa/borç/tribün/takipçi/lig/mac/kaleci, yeni acik_karar (bolum M, esik X, gecerse, gecmezse), yarin_soz (yarın ne olacağını söz verdiysen), gecmis'e M kaydı (ozet 1–2 cümle; begeni/yorum null). Bu bölümde tanıtılan taraftar rollerinin `tanitildi_bolum` alanını ve ekranda gösterilen tribün/loca isimlerinin `gosterildi_bolum` alanını K/taraftarlar.json'da M yap. Sonra main dalına gönder:
```
cd ~/ilk11-medya && git add hocasensin && git commit -qm "hocasensin: bölüm M" && (git pull --rebase -q && git push -q || (sleep 5 && git pull --rebase -q && git push -q))
```
(ses.mp3 .gitignore'dadır; yeni görseller, metin, senaryo, kelimeler, veri ve durum gönderilir. Çakışma olursa en fazla 3 kez pull --rebase.)

## ADIM 11 — Bildir
SendUserFile (status "proactive") ile mp4'ü gönder. SendUserMessage ile kısa özet:
**🎬 Anadoluspor · Bölüm M — bugün 19:00'a planlandı**
- Dünkü bölüm: <beğeni> beğeni · <yorum> yorum · <izlenme> izlenme · takipçi <n>
- Karar #N: hedef <esik> → <tuttu/tutmadı>: <ne oldu>
- Kasa <n> TL · borç <n> TL · tribün <n> · <lig> (<galibiyet>G <beraberlik>B <mağlubiyet>M)
- Yeni karar #M: <X> beğeni → <A> / <B>
- Açıklama metni (tek kod bloğu) ve plannerUrl.
Bir adım başarısız olursa yarım içerik paylaşma; neyin olmadığını SendUserMessage ile kısaca bildir.

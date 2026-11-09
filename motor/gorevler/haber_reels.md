# İLK 11 – Haber Reels görev talimatı (son dakika · maç sonucu · maç öncesi demeç · günün haberleri)

**Neden (sayfa sahibinin kararı, 2026-11-09):** Haftalık rapora göre 2–8 Kasım'da 25 kaydırmalı gönderi toplam 195 kez görüntülendi, 12 Reels ise 22.640 kez izlendi. Bu yüzden aşağıdaki dört içerik **kaydırmalı gönderi olarak paylaşılmaz**; kısa bir Reels + bir hikâye kartı (STORY) olarak paylaşılır. (İlk 11 yalnız hikâye olarak paylaşılır: GOREVLER.md KADRO.) Bu dosya 2026-11-02'den beri yalnız büyük son dakika haberleri için kullanılıyordu; artık hepsini kapsar.

| TÜR | Çağıran görev | Gelen JSON | Günlük Reels sınırı |
|---|---|---|---|
| `sondakika` | GOREVLER.md SON DAKİKA A | `~/sondakika.json` | 3 |
| `demec` (maç öncesi) | GOREVLER.md SON DAKİKA B | `~/demec.json` | 3 |
| `sonuc` | GOREVLER.md SONUÇ | `~/sonuc.json` | her maç için 1 |
| `gunluk` | motor/gorevler/gunun_haberleri.md | `~/haber.json` | 1 (09:30) |

Çağıran görev bilgiyi KURALLAR'a göre doğrulamış ve JSON'u yazmış olarak gelir; bu dosya yalnız doğrulanmış bilgiyi kullanır. Otomatik çalışmadır; kullanıcıya soru sorma. Tüm metinler Türkçe.

**KİŞİ FOTOĞRAFI VE VİDEO:** motor/FOTO_VIDEO.md'yi oku ve uygula.

## H0 · Sınır kontrolü
- `sondakika` / `demec`: motor/paylasilan.txt'de bugünün tarihiyle başlayan, aynı turdan ve ` (reels)` ile biten satırları say. **3'e ulaştıysa** Reels yapma: yalnız hikâye kartını üret (H1), GOREVLER.md Y adımıyla yükle ve P.2 ile STORY olarak paylaş (gönderi YOK); KAYIT satırı ` (hikâye)` ile biter. Aynı çalışmada birden çok haber varsa en önemliyi (resmî transfer, teknik direktör, sakatlık, rekor; sonra cezalar, aday kadro, saat/stat değişikliği) Reels'e ayır.
- `sonuc`: aynı anahtarla ` (reels)` ile biten bir `sonuc` satırı varsa dur.
- `gunluk`: gunun_haberleri.md ADIM 0'daki kontrol yeterli.

## H1 · Hikâye kartı
- `sondakika`, `demec`, `sonuc`: `cd ~/ilk11-medya && rm -rf ~/cikti && python3 motor/ozel.py <JSON> ~/cikti` → yalnız `~/cikti/hikaye.jpg` kullanılır (gönderi kartları paylaşılmaz). Kişinin depoda kesik fotoğrafı varsa son dakika/demeç hikâyesi foto_hikaye.py ile de yapılabilir (FOTO_VIDEO.md). `demec` hikâyesinde demeçlerin TAM METNİ tek ekrandadır (sığmazsa kişi başına ayrı hikâye; GOREVLER.md B). **`sonuc` hikâyesini çağıran görev Reels'ten ÖNCE paylaşmıştır** (skor maç biter bitmez hikâyede); burada yeniden paylaşma.
- `gunluk`: `rm -rf ~/cikti && python3 motor/haber.py ~/haber.json ~/cikti && python3 motor/story.py ~/cikti/01_kapak.jpg ~/cikti/hikaye.jpg "GÜNÜN HABERLERİ" "Videosu profilde · Reels"`.
Hikâye kartını Read ile aç; taşma, yanlış harf, eksik bilgi varsa düzelt.

## H2 · Metin
Ortak kurallar (her TÜR):
- Kısa cümleler; her cümle doğrulanmış bilgiye dayanır. Söylenti, tahmin, yorum, uydurma söz yok; taraf tutulmaz.
- **İlk cümle haberin kendisidir** (kim, ne oldu; en çarpıcı kısım önde). Haber Reels'inde sonuç saklanmaz.
- **2. cümle** her zaman SABLONLAR.md'deki kanca sonrası sesli takip çağrısıdır: birebir `{"soz": "İlk On Bir'i takip et, devamı geliyor!", "altyazi": "İLK 11'i takip et, devamı geliyor!"}` (ElevenLabs metnine de 2. paragraf olarak girer). Kapanıştaki takip çağrısını metne YAZMA (motor ekler).
- Sayılar ve tarihler seslendirmede yazıyla (`soz`), altyazıda rakamla (`altyazi`).
- Ekranda sorulacak **iki seçenekli** soru (≤ 44 karakter, "X mi Y mi?").

TÜRE göre (kelime sayısına takip cümlesi dahildir):
- **sondakika** — 5–6 cümle, 32–44 kelime (video ≈ 20–27 sn). Haberden sonra 1–2 doğrulanmış ayrıntı (sözleşme süresi, bonservis yalnız resmî açıklamada geçiyorsa; sakatlıkta yalnız kulübün açıkladığı tanı/süre), neden önemli olduğu (kendi cümlenle) ve doğrulanmışsa sıradaki adım (ilk maç, dönüş tarihi). ✓ "Fenerbahçe'de geçici görev resmen Dirk Kuyt'a verildi."
- **sonuc** — 5–7 cümle, 34–46 kelime (≈ 22–28 sn). İlk cümle skor + maçın en çarpıcı gerçeği (✓ "Fenerbahçe, Çorum deplasmanından beş golle döndü."). Sonra yalnız `~/sonuc.json`'da doğrulanmış olanlar: goller (dakika + oyuncu; en fazla 3 gol cümlesi, çok gollü maçta "iki gol attı" gibi topla), kırmızı kart, `not` (puan, seri, tur), son cümlede `sonraki` maç.
- **demec** (maç öncesi) — 6–8 cümle, 42–58 kelime (≈ 26–34 sn). İlk cümle kim, hangi maç öncesi ve konuşmanın ana mesajı, kendi cümlenle ve söz gibi değil (✓ "Italiano, Celtic maçı öncesi rakibi için uyardı."). 3. cümleden itibaren kişinin **kaynakta birebir geçen** 2–4 cümlesi, kaynaktaki sırayla, kelimesi değiştirilmeden; `altyazi`'da tırnak içinde (“…”), `soz`'da tırnaksız. Uzun cümleden yalnız birebir bir parça alınabilir; arası atlanırsa altyazıda "…" konur. Konuşan değişince kısa bir geçiş cümlesi ("Hyeon-gyu Oh da heyecanlı.") eklenir. Hakaret/suç itham eden söz alınmaz. Son cümle maçın günü ve saati (doğrulanmış). Demecin TAM METNİ hikâyede ve açıklamada yer alır (GOREVLER.md B).
- **gunluk** — 7–9 cümle, 54–66 kelime (≈ 32–38 sn). İlk cümle günün en büyük haberi; 3. cümleden itibaren `~/haber.json`'daki diğer haberler, sırayla, her biri TEK cümle (toplam 3–5 haber). Son cümle: "Hepsi hikâyede; yarın sabah yine buradayız." Haberlerin özetleri haber.json'daki doğrulanmış bilgilerden; yeni bilgi ekleme.

## H3 · Seslendirme
ToolSearch: "select:mcp__Seslendirme__creative_generate_speech,mcp__Seslendirme__creative_get_flow_run_status". creative_generate_speech: voice_id "mF7tIc9VLrznhGooGjaT" (Hoca'nın sesi), model_id "eleven_v4", prompt = cümleler, her cümle ayrı paragraf (aralarında "\n\n"). Bu çağrıyı **YALNIZCA BİR KEZ** yap (kredi harcar; hata olsa bile tekrar deneme). flow_id ve session_ids ile poll_after_seconds aralıklarla creative_get_flow_run_status çağır; tamamlanınca content_url'yi `mkdir -p ~/haber && curl -sS -m 120 -o ~/haber/ses.mp3 '<content_url>'` ile indir, ffprobe ile süresini kontrol et. İndirilemezse **H-YEDEK**'e geç.

## H4 · ~/haber/senaryo.json
motor/SABLONLAR.md'ye birebir uy. slug "TARIH-<TÜR>-<anahtarın kısa hâli>", ses "ses.mp3", cumleler (ElevenLabs metniyle aynı sayı ve sırada), KARAKTERLİ ÇİZGİ FİLM stili (c* sahneleri). İlk sahne her zaman `ckanca` ve `"cumleler": [0, 1]` (haber cümlesi + takip çağrısı); `baslik` haberin ≤ 5 kelimelik ekran hâli, vurgulu kelimeyle. Görüntü en geç 3–4 sn'de bir değişsin; aynı c* tipi art arda gelmesin. Kişinin depoda lisanslı kesik fotoğrafı varsa bir `foto` sahnesi (`"arka": "stadyum"`). Kulüp logosu ve maç görüntüsü yok (kulüpler renk şeridi/forma renkleriyle); gerçek kişiye uydurma söz balonu YOK — balon yalnız kaynakta birebir geçen ≤ 30 karakterlik söz için. `yarin` alanını yalnız `gunluk` yazar. `kapak_sn`: kanca sahnesinin ~1,5. saniyesi.

| TÜR | `etiket` | `rozet` | Sahne sayısı ve akış |
|---|---|---|---|
| sondakika | İLK 11 · SON DAKİKA | SON DAKİKALAR İLK 11'DE | 3–5: `ckanca` (haberin kişisi: forma renkleri, numara, `ad`) → `foto` → `ctabela`/`csayi` (sözleşme yılı, rekor, dönüş süresi) → `ckarakter` (sonuç / sıradaki adım) |
| sonuc | İLK 11 · MAÇ SONUCU | MAÇ SONUÇLARI İLK 11'DE | 3–5: `ckanca` (kazanan ya da öne çıkan takımın oyuncusu, `skor` bandı `{"sol","sag","deger"}` — kısa adlar, ör. "ÇOR"/"FB") → `ctabela` (`ust` turnuva, iki takım, skor) → `cgol` (doğrulanmış bir gol: `atan` adı/numarası, `dakika`, skor `once`→`sonra`) → `csayi` (puan/sıra, `not`) ya da `ckarakter` (sonraki maç) |
| demec | İLK 11 · MAÇ ÖNCESİ | DEMEÇLER İLK 11'DE | 4–6: `ckanca` (konuşan kişi: takım renkleri, `ad`; `baslik` ör. "ITALIANO: *UYARDI*") → `foto` → `ckarakter` (aynı kişi, `balon` = birebir kısa söz, `ifade` söze uygun) → `cikili` (iki takım, `"vs":"VS"`, maç günü `ust`) → başka konuşan varsa onun `ckarakter`'i |
| gunluk | İLK 11 · GÜNÜN HABERLERİ | HER SABAH · GÜNÜN HABERLERİ | 5–7: `ckanca` (1. haber) → her haber için bir sahne: maç sonucu `ctabela`, kişi haberi `ckarakter` ya da `foto`, transfer `cikili` (`"vs":"→"`), rakam `csayi`. `"yarin": "YARIN 09:30 · YENİ HABERLER"` |

## H5 · Önizleme ve video
`cd ~/haber && python3 ~/ilk11-medya/motor/hikaye.py senaryo.json cikti --onizleme` → cikti/onizleme.png'yi Read ile aç; yazı taşması, çakışma, boş sahne, yanlış skor/forma rengi/isim varsa senaryo.json'u düzelt (en fazla 2 tur; metni değiştirme). Sonra `python3 ~/ilk11-medya/motor/hikaye.py senaryo.json cikti` (timeout 900000 ya da run_in_background). ffprobe ile süreyi kontrol et (H2'deki süre + ≈ 4 sn kapanış) ve videodan 2 kare çıkarıp Read ile bak. Video üretilemezse **H-YEDEK**.

## H6 · Yükle
ANAHTAR: `sondakika`/`demec`/`sonuc` için KAYIT'taki anahtar; `gunluk` için `TARIH-gunun-haberleri`. Video ve hikâye kartını aynı yetim commit'te kendi dalına normal push ile yükle (force-push KULLANMA):
```
cd ~/ilk11-medya && rm -rf ~/medya && git worktree prune
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout -q --orphan medya-<TÜR>reels-<ANAHTAR> && git rm -rqf .
mkdir -p <ANAHTAR> && cp ~/haber/cikti/<slug>.mp4 ~/cikti/hikaye.jpg <ANAHTAR>/ && git add <ANAHTAR> && git commit -qm "<TÜR>reels <ANAHTAR>" && git push -q origin HEAD:refs/heads/medya-<TÜR>reels-<ANAHTAR>
SHA=$(git rev-parse HEAD)
```
Dal zaten varsa adın sonuna -2 ekle. Bağlantılar `https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/$SHA/<ANAHTAR>/<dosya>` — dal adı yerine MUTLAKA SHA; her dosya için curl ile 200 döndüğünü doğrula.

## H7 · Paylaş (Metricool, blogId "7504196")
0. **Son kontrol:** GOREVLER.md P.0 ile aynı (paylasilan.txt + son 6 saatin gönderileri); aynı haber/maç için Reels ya da (sondakika/demec'te) gönderi varsa dur. `sonuc`'ta aynı maçın az önce paylaşılan skor hikâyesi bu kontrole GİRMEZ; yalnız aynı maçın REEL'i varsa dur.
1. **REEL:** createScheduledPost. date: `gunluk` için bugün 09:30 (+03:00; saat 09:20'yi geçtiyse şu an + 10 dk), diğerleri için şu an + 3 dk. **Aralık kuralı:** getScheduledPosts'ta bu saate 45 dakikadan yakın başka bir Instagram REEL (13:00 Portre, 19:00 Hikâye ya da başka bir haber Reels'i) planlı ya da yayınlanmışsa date = o REEL'in saati + 45 dk. info: providers [{"network":"instagram"}], instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}, media [mp4 bağlantısı], videoCoverMilliseconds = kapak_sn × 1000, publicationDate {"dateTime": …, "timezone": "Europe/Istanbul"}, autoPublish true, draft false, descendants [], firstCommentText "" (demec'te tam metin açıklamaya sığmazsa tam metin), hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids": []}.
   text — **ilk satırın öneki ZORUNLU** (portre, hikâye ve haftalık rapor görevleri Reels türünü bu önekten tanır):
   - sondakika: GOREVLER.md A'daki SON DAKİKA açıklaması, ilk satır `🚨 SON DAKİKA | <TAKIM>`.
   - sonuc: GOREVLER.md SONUÇ'taki açıklama, ilk satır `⚽ MAÇ SONUCU | <EV> <skor> <DEP>`.
   - demec: GOREVLER.md B'deki açıklama (tam metin; sığmazsa oradaki kural: tam metin `firstCommentText`'e), ilk satır `🎙️ MAÇ ÖNCESİ KONUŞTU | <EV> – <DEP>` (birden çok kişi: KONUŞTULAR).
   - gunluk: gunun_haberleri.md ADIM 6'daki açıklama, ilk satır `📰 Günün Haberleri | <gün ay>`.
   Soru olarak H2'deki iki seçenekli soru kullanılır (açıklamadaki soru satırının yerine).
2. **STORY** (`sonuc` hariç; onun hikâyesi zaten paylaşıldı): createScheduledPost, date = REEL saatinden 2 dk sonra (`gunluk`: 1 dk sonra, ör. 09:31); instagramData {"type":"STORY","isAiGenerated":false}, media [hikaye.jpg bağlantısı], text alanı yok; diğer alanlar aynı.
3. Yanıtlarda media bağlantılarının static.metricool.com'a taşındığını kontrol et.

## H8 · Kayıt ve bildirim
- KAYIT satırı (GOREVLER.md KAYIT'taki gibi pull/commit/push): `YYYY-AA-GG SS:DD <TÜR> <ANAHTAR> | <kısa başlık> (reels)`. `gunluk` kayıt yazmaz (tekrar kontrolü Metricool'dan yapılır).
- SendUserMessage ile kısa özet: ne paylaşıldı, Reels'in ve hikâyenin planlandığı saat, kaynaklar ([Başlık](URL)), plannerUrl; videoyu SendUserFile ile gönder (status "proactive").

## MANUEL MOD
`motor/MANUEL_MOD` varsa H6 (yükleme) ve H7'yi (Metricool) UYGULAMA, createScheduledPost ÇAĞIRMA. Bunun yerine SendUserFile ile (status "proactive") mp4'ü, hikaye.jpg'yi ve kapak karesini (ffmpeg ile videodan kapak_sn anındaki kare) gönder; SendUserMessage ile ilk satırı `📲 ELLE PAYLAŞ · Instagram Reels + hikâye · önerilen saat <H7'deki saat>` olan mesaj: açıklama metni tek kod bloğunda, "Kapak: videonun <kapak_sn>. saniyesi", "Hikâye: hikaye.jpg (açıklama yok)" ve kaynak bağlantıları. KAYIT satırının sonuna ` (manuel)` ekle.

## H-YEDEK · Reels yapılamazsa
Seslendirme indirilemez, video üretilemez ya da yükleme başarısız olursa içeriği kaybetme ve seslendirmeyi yeniden deneme. Eski kart akışına dön ve bildirime Reels'in neden yapılamadığını tek satırla ekle:
- `sondakika` / `demec`: ozel.py kartları → GOREVLER.md Y → P (gönderi + hikâye) → KAYIT (satır sonuna "(reels)" EKLEME, " — Reels yapılamadı, kart" ekle).
- `sonuc`: hikâye zaten paylaşıldı; kart gönderisini (01_kart.jpg + takip kartı) P.1 ile paylaş, KAYIT'a " — Reels yapılamadı, kart" ekle.
- `gunluk`: gunun_haberleri.md'deki YEDEK adımı (kaydırmalı gönderi, 09:30).

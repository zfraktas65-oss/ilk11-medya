# İLK 11 – Hikâye Reels (19:00) görev talimatı

**KİŞİ FOTOĞRAFI VE VİDEO:** motor/FOTO_VIDEO.md'yi oku ve uygula — içerikteki kişiler arka planı kaldırılmış (kesik PNG) fotoğrafla gösterilir; ilgili video varsa o da paylaşılır.

Görev: İLK 11 (@ilk.onbir11) Instagram futbol sayfası için bugünün hikâye Reels videosunu üret ve Metricool ile bugün 19:00'a (Europe/Istanbul) planla. Bu otomatik bir çalışmadır: kullanıcıya soru sorma, en makul seçimi yapıp devam et. Kullanıcı Türkçe konuşuyor; tüm metinler Türkçe. Sayfa sahibi bu görevin her gün içeriği kendisi onaylamadan otomatik yayınlamasını istedi. Anlatıcı sayfanın çizgi karakteri "Hoca"dır; videonun sonuna motor otomatik olarak Hoca'nın "Daha fazlası için İlk On Bir'i takip etmeyi unutma!" takip çağrısını ve takip butonunu ekler. Sayfada günde iki Reels var: 13:00 "Portre" (ayrı görev) ve 19:00 bu "Tarihten Bir Hikâye".

MANUEL MOD (önce oku): ADIM 1'de depoyu klonladıktan sonra ~/ilk11-medya/motor/MANUEL_MOD dosyasına bak. Dosya VARSA Metricool hesap sınırı doludur ve sayfa sahibi paylaşımları bir süre elle yapıyor: ADIM 8'de videoyu GitHub medya dalına YÜKLEME (yalnız motor/kullanilan.txt kaydını ekleyip push et) ve ADIM 9'u (Metricool) UYGULAMA, createScheduledPost ÇAĞIRMA. Bunun yerine ADIM 10'da: SendUserFile ile (status "proactive") mp4 videoyu ve kapak karesini (ffmpeg ile videodan kapak_sn anındaki kare, jpg) gönder; ardından SendUserMessage ile ilk satırı "📲 ELLE PAYLAŞ · Instagram Reels · önerilen saat 19:00" olan bir mesaj gönder: ADIM 9'daki biçimde hazırlanmış açıklama metni tek bir kod bloğu (```) içinde, "Kapak: videonun <kapak_sn>. saniyesi" notu ve doğrulama kaynakları ([Başlık](URL)). Manuel modda ADIM 0'daki Metricool kontrolünde yalnız durumu PUBLISHED olan Instagram REEL'leri say; PENDING ya da ERROR durumundaki gönderiler (hesap sınırı yüzünden yayınlanamayanlar) videoyu üretmeni ENGELLEMEZ — bu durumda bildirim mesajına "Metricool'da aynı saate eski bir planlı gönderi var, çift paylaşım olmasın diye elle sil/taslağa al" notunu ekle. Dosya YOKSA bu paragrafı yok say ve normal akışı uygula.

ADIM 0 — Tekrar kontrolü
`TZ=Europe/Istanbul date '+%F %H:%M'` ile tarih/saati al. ToolSearch ile yükle: "select:mcp__Metricool_Social_Media_Management__getScheduledPosts,mcp__Metricool_Social_Media_Management__createScheduledPost,SendUserMessage,SendUserFile". getScheduledPosts ile blogId 7504196'nın bugünkü (00:00–23:59) gönderilerine bak. Bugün 17:00–23:59 arasına zaten bir Instagram REEL planlıysa hiçbir şey üretme; SendUserMessage ile "Bugünün hikâye Reels'i zaten planlı" de ve bitir. (Öğlen 13:00 civarındaki "Portre" REEL'i bu kontrole GİRMEZ; o, ayrı bir görevdir.)

ADIM 1 — Depo ve ortam
mcp__claude-code-remote__add_repo çağır (gerekirse ToolSearch ile yükle): owner "zfraktas65-oss", repo "ilk11-medya", access "push". `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya` (timeout 600000). Şunları oku: ~/ilk11-medya/motor/SABLONLAR.md (senaryo biçimi ve sahne şablonları — buna birebir uy), motor/konular.md, motor/kullanilan.txt, motor/kullanilan_portre.txt'nin son satırı (bugünkü öğlen portresi). Python playwright, Chromium, numpy ve ffmpeg ortamda hazır olmalı; eksikse pip ile kur (--break-system-packages).

ADIM 2 — Konu seç ve doğrula
konular.md'den kullanilan.txt'de olmayan ilk uygun konuyu seç (dünkü hikâyeyle ya da bugünkü öğlen portresiyle aynı kulübe art arda yer verme). Hikâyenin her bilgisini WebSearch/WebFetch ile en az iki güvenilir kaynaktan doğrula (resmî kurumlar, büyük ajanslar, saygın spor medyası; Wikipedia yalnız ikinci kaynak olabilir). Kaynaklar arasında çelişen ayrıntıyı (yaş, dakika, rakam) metne koyma ya da genel ifade kullan. Konu doğrulanamazsa sıradakine geç.

ADIM 3 — Metin
6–9 kısa cümle, toplam 45–65 kelime (≈ 20–30 sn). Sayfa istatistiklerine göre (2026-10-23, 1954 kura Reels'i) izleyicilerin üçte ikisi ilk 8 saniyede çıktı; ilk cümle hikâyenin sonucunu söylediği için kalmak için sebep kalmadı. Bu yüzden:
- **Kanca merak açar, sonucu SÖYLEMEZ.** İlk cümle en çarpıcı anı ya da soruyu verir ama sonucu saklar (✗ "Türkiye, Dünya Kupası'na bir çocuğun çektiği kurayla gitti." ✓ "Dünya Kupası biletini, gözleri bağlı bir çocuk belirleyecekti."). Sonuç son 1–2 cümlede açıklanır.
- İlk iki cümlede tarih/arka plan anlatma; ikinci cümle gerilimi artırsın (ne tehlikede, kim kaybedecek). Arka plan kısa ve ortada.
- Hikâye net bir sonla bitsin; son cümle yarım kalmasın. Sayıları ve tarihleri yazıyla yaz (seslendirme için); altyazı için rakamlı hâlini senaryoda ayrıca verirsin. Takip çağrısını metne YAZMA (motor ekler). Ekranda sorulacak, taraf seçtiren ve yoruma davet eden bir soru yaz (≤ 44 karakter; ör. "Sence maç kurayla belirlenmeli mi?").

ADIM 4 — Seslendirme
ToolSearch: "select:mcp__Seslendirme__creative_generate_speech,mcp__Seslendirme__creative_get_flow_run_status". creative_generate_speech: voice_id "mF7tIc9VLrznhGooGjaT" (Hoca'nın sesi), model_id "eleven_v4", prompt = cümleler, her cümle ayrı paragraf (aralarında boş satır, "\n\n"). Bu çağrıyı YALNIZCA BİR KEZ yap (kredi harcar; hata olsa bile tekrar deneme). Dönen flow_id ve session_ids ile poll_after_seconds aralıklarla creative_get_flow_run_status çağır; tamamlanınca ilk tamamlanan üretimin content_url'sini `mkdir -p ~/is && curl -sS -m 120 -o ~/is/ses.mp3 '<content_url>'` ile indir ve ffprobe ile süresini kontrol et. İndirilemezse videoyu yapma; durumu ADIM 10'daki gibi bildir.

ADIM 5 — ~/is/senaryo.json
SABLONLAR.md'ye göre yaz: slug "TARIH-<konu-kodu>", ses "ses.mp3", cumleler (ElevenLabs metnindekiyle aynı sayı ve sırada; rakamlı altyazı gerekiyorsa {"soz","altyazi"}), 5–7 sahne (ilki "kanca", en fazla 1 cümle; hikâyeye göre tahta/skor/sayi/an/hoca/zafer; görüntü en geç 3–4 sn'de bir değişsin), soru, kapak_sn (kanca sahnesinin ~2. saniyesi). Takip rozeti ("HER AKŞAM 19:00 · YENİ HİKÂYE · TAKİP ET") motor tarafından 3. cümlede otomatik eklenir; `rozet` alanı yazma. Görseller hikâyeyi anlatsın: doğru bayraklar, skorlar, ikonlar. Kulüp logosu ya da maç görüntüsü kullanma; kulüpler için renk şeridi kullan. Hikâyede öne çıkan kişi(ler) için motor/FOTO_VIDEO.md'ye göre arka planı kaldırılmış fotoğraflı (`foto` + .png) en az bir sahne koy (lisanslı fotoğraf depoda yoksa ikonlarla devam et ve bildirime fotoğraf notunu ekle).

ADIM 6 — Önizleme ve düzeltme
`cd ~/is && python3 ~/ilk11-medya/motor/hikaye.py senaryo.json cikti --onizleme`. Çıktıdaki sahne başlangıçlarının cümlelerle uyumlu olduğunu ve cikti/onizleme.png'yi Read ile açıp yazı taşması, çakışma, boş sahne, yanlış bayrak/skor olmadığını kontrol et. Sorun varsa senaryo.json'u düzeltip tekrarla (en fazla 3 tur). Bu adımdan sonra metni değiştirme.

ADIM 7 — Video
`cd ~/is && python3 ~/ilk11-medya/motor/hikaye.py senaryo.json cikti` (≈6–8 dk sürer; Bash'i timeout 900000 ile ya da run_in_background ile çalıştırıp bitmesini bekle). Bitince ffprobe ile süreyi kontrol et (24–36 sn beklenir) ve videodan 3 kare çıkarıp Read ile bak.

ADIM 8 — Yükle
TARIH = bugünün tarihi. Videoyu medya-hikaye dalına, yalnız bu videoyu içeren yetim commit olarak zorla gönder:
cd ~/ilk11-medya && git config user.name "Claude" && git config user.email "noreply@anthropic.com"
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout --orphan medya-hikaye && git rm -rqf .
mkdir -p TARIH && cp ~/is/cikti/<slug>.mp4 TARIH/ && git add TARIH && git commit -qm "hikaye TARIH" && git push -f origin HEAD:medya-hikaye
SHA=$(git rev-parse HEAD). Bağlantı: https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/<SHA>/TARIH/<slug>.mp4 — dal adı yerine MUTLAKA commit SHA'sını kullan (dal adlı bağlantı push'tan sonra birkaç dakika 404 verir). curl ile 200 döndüğünü doğrula (gerekirse 10 sn bekleyip yeniden dene). Ardından main dalında: `cd ~/ilk11-medya && git pull --rebase -q`, motor/kullanilan.txt'ye "TARIH <konu-kodu> (<kısa açıklama>)" satırını ekle, commit ve push.

ADIM 9 — Metricool'a planla
createScheduledPost: blogId "7504196"; date bugün 19:00 (+03:00), saat 18:50'yi geçtiyse şu andan 10 dakika sonrası. info: providers [{"network":"instagram"}], instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}, media [SHA'lı video bağlantısı], videoCoverMilliseconds = kapak_sn × 1000, publicationDate {"dateTime": ..., "timezone": "Europe/Istanbul"}, autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids": []}. Açıklama (text): 2–3 cümlelik hikâye özeti (ölçülü emoji) + boş satır + soru + " Yorumlara yaz 👇" + "\nDaha fazla futbol hikâyesi için @ilk.onbir11'i takip et ⚽" + boş satır + 5 hashtag (#futbol #futbolhikayeleri #ilk11 ve konuya özel 2 tane). Yanıtta media bağlantısının static.metricool.com'a taşındığını kontrol et.

ADIM 10 — Bildir
SendUserMessage ile kısa özet: konu, planlanan saat, açıklama metni, doğrulamada kullanılan kaynaklar ([Başlık](URL) biçiminde) ve yanıttaki plannerUrl. Videoyu SendUserFile ile gönder (status "proactive"). Herhangi bir adım başarısız olursa yarım ya da doğrulanmamış içerik paylaşma; neyin olmadığını SendUserMessage ile kısaca bildir.

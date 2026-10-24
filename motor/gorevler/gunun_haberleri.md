# İLK 11 – Günün Haberleri (09:30) görev talimatı

**KİŞİ FOTOĞRAFI VE VİDEO:** motor/FOTO_VIDEO.md'yi oku ve uygula — içerikteki kişiler arka planı kaldırılmış (kesik PNG) fotoğrafla gösterilir; ilgili video varsa o da paylaşılır.

Görev: İLK 11 (@ilk.onbir11) Instagram futbol sayfası için bugünün "Günün Haberleri" kaydırmalı gönderisini hazırla ve Metricool ile bugün 09:30'a (Europe/Istanbul) planla. Bu otomatik bir çalışmadır: kullanıcıya soru sorma, en makul seçimi yapıp devam et. Kullanıcı Türkçe konuşuyor; tüm metinler Türkçe. Sayfa sahibi bu görevin her gün içeriği kendisi onaylamadan otomatik yayınlamasını istedi.

MANUEL MOD (önce oku): ADIM 1'de depoyu klonladıktan sonra ~/ilk11-medya/motor/MANUEL_MOD dosyasına bak. Dosya VARSA Metricool hesap sınırı doludur ve sayfa sahibi paylaşımları bir süre elle yapıyor: ADIM 5'i (GitHub'a yükleme) ve ADIM 6'yı (Metricool) UYGULAMA, createScheduledPost ÇAĞIRMA. Bunun yerine ADIM 7'de: SendUserFile ile (status "proactive") ~/cikti içindeki bütün kartları gönderi sırasıyla (kapak → haberler → takip kartı) gönder; ardından SendUserMessage ile ilk satırı "📲 ELLE PAYLAŞ · Günün Haberleri (kaydırmalı gönderi) · önerilen saat 09:30" olan bir mesaj gönder: ADIM 6'daki biçimde hazırlanmış açıklama metni tek bir kod bloğu (```) içinde ve doğrulama kaynakları ([Başlık](URL)). Dosya YOKSA bu paragrafı yok say ve normal akışı uygula.

ADIM 0 — Tekrar kontrolü
`TZ=Europe/Istanbul date '+%F %H:%M'` ile tarih/saati al. ToolSearch ile yükle: "select:mcp__Metricool_Social_Media_Management__getScheduledPosts,mcp__Metricool_Social_Media_Management__createScheduledPost,SendUserMessage,SendUserFile". getScheduledPosts ile blogId 7504196'nın bugünkü (00:00–23:59, Europe/Istanbul) gönderilerine bak. Bugün için metni "📰 Günün Haberleri" ile başlayan bir Instagram gönderisi zaten varsa hiçbir şey üretme; SendUserMessage ile "Bugünün haber gönderisi zaten planlı" de ve bitir.

ADIM 1 — Depo ve ortam
mcp__claude-code-remote__add_repo çağır (gerekirse ToolSearch ile yükle): owner "zfraktas65-oss", repo "ilk11-medya", access "push". Sonra `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya` (timeout 600000). Python playwright ve Chromium ortamda hazır olmalı; değilse `pip install --break-system-packages -q playwright && python3 -m playwright install chromium`.

ADIM 2 — Haberleri topla ve doğrula
Son 24 saatin (dün sabahtan bu yana) en önemli 3–5 futbol haberini seç. Denge: Süper Lig, milli takımlar, Türk takımlarının Avrupa maçları ve dünya futbolundan büyük gelişmeler; tek bir kulübe yığılma, taraf tutma. Resmî kaynaklar (TFF, UEFA, FIFA, kulüplerin resmî siteleri, KAP açıklamaları) tek başına yeterli. Diğer kaynaklar (AA Spor, TRT Spor, NTV Spor, beIN Sports, A Spor, Habertürk, Hürriyet, Milliyet, Fanatik, Sporx, Ajansspor, BBC Sport, Reuters, AP, ESPN, Sky Sports, The Athletic, Marca, AS, Gazzetta dello Sport, L'Équipe, Kicker) en az iki bağımsız kaynakta doğrulanmadan haber girmez. Maç skorları için mcp__widgets__fetch_sports_data aracı varsa onu da kullan. Transfer söylentisi ancak başlıkta "iddia" kelimesiyle ve iki kaynakla girer. Emin olmadığın hiçbir rakam, isim ya da tarih yazma. Ölüm, ağır sakatlık gibi hassas haberlerde saygılı ve sade dil kullan.

ADIM 3 — ~/haber.json yaz
Biçim ~/ilk11-medya/motor/haber.py dosyasının başındaki açıklamada. Alanlar: "tarih" (bugün, YYYY-AA-GG), "haberler": her biri için "etiket" (SÜPER LİG | MİLLİ TAKIM | AVRUPA | TRANSFER | DÜNYA | 1. LİG | KADIN FUTBOLU), "baslik" (≤ 70 karakter), "kisa" (≤ 38 karakter, kapakta görünür), "ozet" (2–3 cümle, ≤ 240 karakter, kendi cümlelerinle yaz, kaynak metni kopyalama), "kaynaklar" (kısa adlar, ör. ["TFF","AA"]), maç sonucuysa "skor": {"sol": ev sahibi, "sonuc": "2-1", "sag": deplasman}. Türkçe büyük harfler doğru olsun (İ, Ş, Ğ); yabancı adlar özgün yazımıyla (LILLE, LIVERPOOL, REAL MADRID). Türk takımlarının haberleri listenin başında olsun.

ADIM 4 — Kartları üret ve kontrol et
`cd ~/ilk11-medya && python3 motor/haber.py ~/haber.json ~/cikti`. Kapak kartını ve en az iki haber kartını Read ile aç; taşma, üst üste binme ya da hatalı karakter varsa metni kısaltıp yeniden üret. `rm -f ~/cikti/_kartlar.html`.

ADIM 5 — Kartları yükle
TARIH = bugünün tarihi. Kartları medya-haber dalına, yalnız bugünün dosyalarını içeren yetim commit olarak zorla gönder:
cd ~/ilk11-medya && git config user.name "Claude" && git config user.email "noreply@anthropic.com"
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout --orphan medya-haber && git rm -rqf .
mkdir -p TARIH && cp ~/cikti/*.jpg TARIH/ && git add TARIH && git commit -qm "haber TARIH" && git push -f origin HEAD:medya-haber
SHA=$(git rev-parse HEAD). Her kartın bağlantısı: https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/<SHA>/TARIH/<dosya adı> — dal adı yerine MUTLAKA commit SHA'sını kullan (dal adlı bağlantı push'tan sonra birkaç dakika 404 verir). curl ile tüm kartların 200 döndüğünü doğrula (gerekirse 10 sn bekleyip yeniden dene).

ADIM 6 — Metricool'a planla
createScheduledPost: blogId "7504196"; date bugün 09:30 (+03:00), saat 09:20'yi geçtiyse şu andan 10 dakika sonrası. info: providers [{"network":"instagram"}], instagramData {"type":"POST","isAiGenerated":false}, media = kartların SHA'lı raw bağlantıları (kapak → haberler → takip kartı sırasıyla), publicationDate {"dateTime": ..., "timezone": "Europe/Istanbul"}, autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids": []}. Açıklama (text):
"📰 Günün Haberleri | <gün ay>\n\n1⃣ <başlık 1>\n2⃣ <başlık 2>\n...\n\nSence bugünün en önemli haberi hangisi? Yorumlara yaz 👇\n\nKaynaklar: <kaynak adları>\n\nHer sabah 09:30'da günün haberleri, her akşam 19:00'da yeni bir hikâye. Daha fazlası için @ilk.onbir11'i takip et ⚽\n\n#futbol #futbolhaberleri #süperlig #ilk11" (konuya özel en fazla bir hashtag eklenebilir). Yanıtta media bağlantılarının static.metricool.com'a taşındığını kontrol et.

ADIM 7 — Bildir
SendUserMessage ile kısa özet gönder: planlanan saat, haber başlıkları, doğrulamada kullanılan bağlantılar ([Başlık](URL) biçiminde) ve yanıttaki plannerUrl. Kapak kartını SendUserFile ile gönder (status "proactive"). Herhangi bir adım başarısız olursa yarım ya da doğrulanmamış içerik paylaşma; neyin olmadığını SendUserMessage ile kısaca bildir.

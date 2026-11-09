# İLK 11 – Günün Haberleri (09:30 Reels + hikâye) görev talimatı

**KİŞİ FOTOĞRAFI VE VİDEO:** motor/FOTO_VIDEO.md'yi oku ve uygula — içerikteki kişiler arka planı kaldırılmış (kesik PNG) fotoğrafla gösterilir; ilgili video varsa o da paylaşılır.

Görev: İLK 11 (@ilk.onbir11) Instagram futbol sayfası için bugünün "Günün Haberleri" içeriğini hazırla ve Metricool ile bugün 09:30'a (Europe/Istanbul) planla. **Biçim (sayfa sahibinin kararı, 2026-11-09): kaydırmalı gönderi DEĞİL; günün 3–5 haberini Hoca'nın anlattığı ~35 sn'lik bir Reels (09:30) + haber kartlarının kapağından bir hikâye (09:31).** Neden: 2–8 Kasım'da kaydırmalı gönderiler gönderi başına ~8 kez görüntülendi, Reels'ler ~1.900 kez izlendi. Bu otomatik bir çalışmadır: kullanıcıya soru sorma, en makul seçimi yapıp devam et. Kullanıcı Türkçe konuşuyor; tüm metinler Türkçe. Sayfa sahibi bu görevin her gün içeriği kendisi onaylamadan otomatik yayınlamasını istedi.

MANUEL MOD (önce oku): ADIM 1'de depoyu klonladıktan sonra ~/ilk11-medya/motor/MANUEL_MOD dosyasına bak. Dosya VARSA Metricool hesap sınırı doludur ve sayfa sahibi paylaşımları bir süre elle yapıyor: ADIM 5'te haber_reels.md'nin MANUEL MOD bölümünü uygula (video, hikâye ve açıklama sohbete gönderilir; ilk satır "📲 ELLE PAYLAŞ · Günün Haberleri (Reels + hikâye) · önerilen saat 09:30"), createScheduledPost ÇAĞIRMA. Dosya YOKSA bu paragrafı yok say ve normal akışı uygula.

ADIM 0 — Tekrar kontrolü
`TZ=Europe/Istanbul date '+%F %H:%M'` ile tarih/saati al. ToolSearch ile yükle: "select:mcp__Metricool_Social_Media_Management__getScheduledPosts,mcp__Metricool_Social_Media_Management__createScheduledPost,SendUserMessage,SendUserFile". getScheduledPosts ile blogId 7504196'nın bugünkü (00:00–23:59, Europe/Istanbul) gönderilerine bak. Bugün için metni "📰 Günün Haberleri" ile başlayan bir Instagram REEL'i ya da gönderisi zaten varsa hiçbir şey üretme; SendUserMessage ile "Bugünün haber Reels'i zaten planlı" de ve bitir.

ADIM 1 — Depo ve ortam
mcp__claude-code-remote__add_repo çağır (gerekirse ToolSearch ile yükle): owner "zfraktas65-oss", repo "ilk11-medya", access "push". Sonra `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya` (timeout 600000). Depo içinde `git config user.name "Claude" && git config user.email "noreply@anthropic.com"`. Şunları oku: motor/gorevler/haber_reels.md (Reels akışı; TÜR `gunluk`) ve motor/SABLONLAR.md. Python playwright, Chromium, numpy ve ffmpeg ortamda hazır olmalı; değilse pip ile kur (--break-system-packages).

ADIM 2 — Haberleri topla ve doğrula
Son 24 saatin (dün sabahtan bu yana) en önemli 3–5 futbol haberini seç. Denge: Süper Lig, milli takımlar, Türk takımlarının Avrupa maçları ve dünya futbolundan büyük gelişmeler; tek bir kulübe yığılma, taraf tutma. Resmî kaynaklar (TFF, UEFA, FIFA, kulüplerin resmî siteleri, KAP açıklamaları) tek başına yeterli. Diğer kaynaklar (AA Spor, TRT Spor, NTV Spor, beIN Sports, A Spor, Habertürk, Hürriyet, Milliyet, Fanatik, Sporx, Ajansspor, BBC Sport, Reuters, AP, ESPN, Sky Sports, The Athletic, Marca, AS, Gazzetta dello Sport, L'Équipe, Kicker) en az iki bağımsız kaynakta doğrulanmadan haber girmez. Maç skorları için mcp__widgets__fetch_sports_data aracı varsa onu da kullan. Transfer söylentisi ancak başlıkta "iddia" kelimesiyle ve iki kaynakla girer. Emin olmadığın hiçbir rakam, isim ya da tarih yazma. Ölüm, ağır sakatlık gibi hassas haberlerde saygılı ve sade dil kullan.

ADIM 3 — ~/haber.json yaz
Biçim ~/ilk11-medya/motor/haber.py dosyasının başındaki açıklamada. Alanlar: "tarih" (bugün, YYYY-AA-GG), "haberler": her biri için "etiket" (SÜPER LİG | MİLLİ TAKIM | AVRUPA | TRANSFER | DÜNYA | 1. LİG | KADIN FUTBOLU), "baslik" (≤ 70 karakter), "kisa" (≤ 38 karakter, kapakta görünür), "ozet" (2–3 cümle, ≤ 240 karakter, kendi cümlelerinle yaz, kaynak metni kopyalama), "kaynaklar" (kısa adlar, ör. ["TFF","AA"]), maç sonucuysa "skor": {"sol": ev sahibi, "sonuc": "2-1", "sag": deplasman}. Türkçe büyük harfler doğru olsun (İ, Ş, Ğ); yabancı adlar özgün yazımıyla (LILLE, LIVERPOOL, REAL MADRID). Türk takımlarının haberleri listenin başında olsun.

ADIM 4 — Hikâye kartı
haber_reels.md H1 (`gunluk`): `cd ~/ilk11-medya && rm -rf ~/cikti && python3 motor/haber.py ~/haber.json ~/cikti && python3 motor/story.py ~/cikti/01_kapak.jpg ~/cikti/hikaye.jpg "GÜNÜN HABERLERİ" "Videosu profilde · Reels"`. hikaye.jpg'yi ve kapak kartını Read ile aç; taşma, üst üste binme ya da hatalı karakter varsa metni kısaltıp yeniden üret. `rm -f ~/cikti/_kartlar.html`.

ADIM 5 — Reels
haber_reels.md'yi TÜR `gunluk` ile H2'den H7'ye uygula: metin (7–9 cümle, 54–66 kelime; ilk cümle günün en büyük haberi, 2. cümle sesli takip çağrısı, sonra diğer haberler birer cümle), seslendirme (YALNIZCA BİR KEZ), senaryo (`"etiket": "İLK 11 · GÜNÜN HABERLERİ"`, `"rozet": "HER SABAH · GÜNÜN HABERLERİ"`, `"yarin": "YARIN 09:30 · YENİ HABERLER"`), önizleme, video, yükleme (ANAHTAR `TARIH-gunun-haberleri`), REEL bugün 09:30 (saat 09:20'yi geçtiyse şu an + 10 dk) ve STORY REEL'den 1 dk sonra.

ADIM 6 — Açıklama (REEL'in text alanı)
"📰 Günün Haberleri | <gün ay>\n\n1⃣ <başlık 1>\n2⃣ <başlık 2>\n...\n\n<iki seçenekli soru> Yorumlara yaz 👇\n\nKaynaklar: <kaynak adları>\n\nHer sabah 09:30'da günün haberleri, her akşam 19:00'da yeni bir hikâye. Daha fazlası için @ilk.onbir11'i takip et ⚽\n\n#futbol #futbolhaberleri #süperlig #ilk11" (konuya özel en fazla bir hashtag eklenebilir). İlk satırın "📰 Günün Haberleri" öneki ZORUNLU (diğer görevler bu Reels'i bu önekten tanır). Yanıtlarda media bağlantılarının static.metricool.com'a taşındığını kontrol et.

ADIM 7 — Bildir
SendUserMessage ile kısa özet gönder: Reels ve hikâyenin planlandığı saat, haber başlıkları, doğrulamada kullanılan bağlantılar ([Başlık](URL) biçiminde) ve yanıttaki plannerUrl. Videoyu SendUserFile ile gönder (status "proactive"). Herhangi bir adım başarısız olursa yarım ya da doğrulanmamış içerik paylaşma; neyin olmadığını SendUserMessage ile kısaca bildir.

YEDEK — Reels yapılamazsa (seslendirme indirilemez, video üretilemez)
Haberleri kaybetme; eski kaydırmalı gönderi akışına dön ve bildirime Reels'in neden yapılamadığını tek satırla ekle. Seslendirmeyi yeniden deneme.
1. Kartları (ADIM 4'te üretildi) medya-haber dalına, yalnız bugünün dosyalarını içeren yetim commit olarak zorla gönder:
   cd ~/ilk11-medya && rm -rf ~/medya && git worktree prune && git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout --orphan medya-haber && git rm -rqf .
   mkdir -p TARIH && cp ~/cikti/*.jpg TARIH/ && git add TARIH && git commit -qm "haber TARIH" && git push -f origin HEAD:medya-haber
   SHA=$(git rev-parse HEAD). Bağlantı: https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/<SHA>/TARIH/<dosya adı> (dal adı değil SHA); curl ile hepsinin 200 döndüğünü doğrula.
2. createScheduledPost: blogId "7504196"; date bugün 09:30 (+03:00; 09:20'yi geçtiyse şu an + 10 dk); instagramData {"type":"POST","isAiGenerated":false}; media = kartlar (kapak → haberler → takip kartı; hikaye.jpg HARİÇ); text = ADIM 6'daki açıklama (soru satırı "Sence bugünün en önemli haberi hangisi? Yorumlara yaz 👇"); publicationDate {"dateTime": ..., "timezone": "Europe/Istanbul"}, autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids": []}.
3. ADIM 7 gibi bildir; kapak kartını SendUserFile ile gönder.

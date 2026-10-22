# İLK 11 · Maç günü ve son dakika görevleri

Bu dosya otomatik görevlerin talimatıdır. Görev metni hangi bölümü uygulayacağını ve maç bilgilerini verir. Bu işler otomatik çalışır; kullanıcıya soru sorulmaz, en makul seçim yapılır. Sayfa sahibi bu paylaşımların kendisine sorulmadan yapılmasını istedi. Tüm metinler Türkçe olur.

**Takip edilen takımlar:** TÜRKİYE (A Milli Takım), BEŞİKTAŞ, FENERBAHÇE, GALATASARAY, TRABZONSPOR. Hazırlık maçları dahil bütün turnuvalar kapsanır.

---

## ORTAK ADIMLAR

### K0 · Kurulum
1. Tarih ve saati al: `TZ=Europe/Istanbul date '+%F %H:%M'`.
2. ToolSearch ile şu araçları yükle: `select:mcp__Metricool_Social_Media_Management__createScheduledPost,mcp__Metricool_Social_Media_Management__getScheduledPosts,SendUserMessage,SendUserFile,mcp__claude-code-remote__add_repo,mcp__claude-code-remote__create_trigger`.
3. `add_repo` çağır: owner `zfraktas65-oss`, repo `ilk11-medya`, access `push`.
4. `~/ilk11-medya` yoksa klonla: `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya`. Sonra şunu çalıştır: `git config user.name "Claude" && git config user.email "noreply@anthropic.com"` (depo içinde).
5. Python playwright ve Chromium hazır olmalı. Eksikse kur: `pip install --break-system-packages -q playwright && python3 -m playwright install chromium`.

### KAYIT · motor/paylasilan.txt
Her paylaşım tek satırla kaydedilir: `YYYY-AA-GG SS:DD <tur> <anahtar> | <kısa başlık>`. `tur` değeri kadro, sonuc veya sondakika olur.
- Anahtar örnekleri: kadro/sonuç için `2026-10-24-galatasaray-kasimpasa`, son dakika için `2026-10-24-fenerbahce-teknik-direktor`.
- **Paylaşmadan önce** aynı tur ve anahtarla bir satır varsa paylaşma.
- Son dakikada aynı olay farklı kelimelerle de olsa son 3 günde paylaşıldıysa paylaşma.
- Paylaşımdan sonra satırı ekle ve gönder: `cd ~/ilk11-medya && git pull --rebase -q && echo "<satır>" >> motor/paylasilan.txt && git add motor/paylasilan.txt && git commit -qm "kayıt" && git push -q`. Çakışma olursa en fazla 3 kez tekrar dene.

### Y · Kartları yükle
`<tur>` kadro, sonuc veya sondakika olur; `<ANAHTAR>` kayıttaki anahtardır.
```
cd ~/ilk11-medya && rm -rf ~/medya && git worktree prune
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout -q --orphan medya-<tur> && git rm -rqf .
mkdir -p <ANAHTAR> && cp ~/cikti/*.jpg <ANAHTAR>/ && git add <ANAHTAR> && git commit -qm "<tur> <ANAHTAR>" && git push -qf origin HEAD:medya-<tur>
SHA=$(git rev-parse HEAD)
```
- Bağlantı: `https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/$SHA/<ANAHTAR>/<dosya>`.
- Dal adı yerine **mutlaka SHA** kullan; dal adlı bağlantı ilk dakikalarda 404 verir.
- Her dosya için curl ile 200 döndüğünü doğrula.

### P · Paylaş (Metricool, blogId "7504196", Instagram)
1. **Gönderi:**
   - createScheduledPost, date = şu an + 3 dk (+03:00).
   - info: providers [{"network":"instagram"}], instagramData {"type":"POST","isAiGenerated":false}.
   - media: kartlar sırayla, en sonda takip kartı; hepsi SHA'lı bağlantı.
   - publicationDate {"dateTime":…,"timezone":"Europe/Istanbul"}.
   - autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, mediaAltText [], shortener false, smartLinkData {"ids":[]}.
   - text: açıklama metni.
2. **Hikâye:**
   - createScheduledPost, date = şu an + 5 dk.
   - Aynı alanlar; şu farklarla: instagramData {"type":"STORY","isAiGenerated":false}, media [hikaye.jpg bağlantısı], **text alanı yok**.
3. Yanıtlarda media bağlantılarının static.metricool.com'a taşındığını kontrol et.

Her açıklamanın sonunda şu satır bulunur: `Daha fazlası için @ilk.onbir11'i takip et ⚽`. Ardından en fazla 5 hashtag gelir.

### B · Bildir
SendUserMessage ile kısa bir özet gönder:
- ne paylaşıldı ve saati,
- kaynak bağlantıları ([Başlık](URL)),
- plannerUrl.

Kartı SendUserFile ile gönder (status "proactive").

Bir şey doğrulanamazsa ya da bir adım başarısız olursa **paylaşma**. Bunun yerine neyin olmadığını kısaca bildir.

### KURALLAR
- Kulüp logosu, gerçek kişi fotoğrafı ya da maç görüntüsü kullanılmaz; kartlar `motor/ozel.py` ile üretilir.
- Doğrulama şartı: resmî kaynak (kulübün resmî sitesi/hesabı, KAP, TFF, UEFA, FIFA) tek başına yeterlidir. Diğer bilgiler en az **iki bağımsız** güvenilir kaynakta aynı olmalıdır.
- Güvenilir kaynaklar: AA, TRT Spor, NTV Spor, beIN Sports, A Spor, Fanatik, Ajansspor, Sporx, Hürriyet, Milliyet, Habertürk, BBC Sport, Reuters, ESPN ve benzerleri.
- Söylenti haber gibi verilmez. Taraf tutulmaz; dil saygılı ve sade olur.
- Türkçe büyük harfler doğru yazılır (İ, Ş, Ğ). Yabancı adlar özgün yazımıyla kalır: LILLE, REAL MADRID.
- `motor/ozel.py` dosyasının başındaki açıklama JSON biçimini anlatır; ona birebir uy.

---

## KADRO GÖREVİ
Görev metni şunları verir: EV, DEP, TURNUVA, TARIH, SAAT (başlama, Europe/Istanbul) ve bizim takım(lar).

1. K0'ı uygula. Anahtar `TARIH-ev-dep` olur: küçük harf, Türkçe harfler sadeleşir (ç→c, ğ→g, ı→i, ö→o, ş→s, ü→u). Kayıtta `kadro <anahtar>` varsa dur.
2. **Resmî ilk 11'i bul.** Kulüpler ve TFF/UEFA kadroyu genellikle başlamadan 60–75 dk önce açıklar.
   - Aranacaklar: "<takım> <rakip> ilk 11", "<takım> 11'i belli oldu", "<takım> muhtemel değil resmi 11".
   - Kaynaklar: UEFA maç merkezi, TFF, kulüp sitesi; haber sitelerinde "ilk 11'ler belli oldu" haberleri.
   - **Muhtemel 11'leri ASLA kullanma.**
   - Kabul şartı: resmî kaynak tek başına yeter ya da iki bağımsız kaynakta aynı 11 isim geçer.
   - Henüz yoksa 3–4 dakika arayla yeniden ara: `Monitor` ile bekle ya da aramaları aralıklı yap. Bunu başlama saatine 10 dakika kalana kadar sürdür.
   - Yine doğrulanamazsa paylaşma ve B'yi uygula.
3. **Bizim her takımımız için** (derbide iki takım da) şunları belirle:
   - 11 oyuncu: kaleci önce, sonra hatlar geriden ileriye, her hat sağdan sola. Kısa ve yaygın kullanılan adlar.
   - Teknik direktör.
   - Yedekler (yalnız açıklamada kullanılır, isteğe bağlı).
   - `dizilis` alanını yalnız şu durumda yaz: kaynak dizilişi açıkça veriyor (ör. 4-2-3-1) ve oyuncuların mevkileri kaynaktan anlaşılıyor. Değilse yazma; kart liste düzeninde çıkar.
4. `~/kadro.json` yaz. Rakibin forma renkleri biliniyorsa `renkler` alanına ekle.
   - Çalıştır: `cd ~/ilk11-medya && rm -rf ~/cikti && python3 motor/ozel.py ~/kadro.json ~/cikti`.
   - Kartları Read ile aç. Taşma, yanlış harf veya eksik oyuncu varsa düzeltip yeniden üret.
5. Y'yi uygula (tur kadro), sonra P'yi. Açıklama:
   ```
   📋 İLK 11 BELLİ OLDU | <EV> – <DEP>

   <Takım> 11'i: <11 isim, virgülle>
   Yedekler: <varsa>
   Teknik direktör: <ad>

   ⏰ <SAAT> · <TURNUVA>

   Sence bu 11 kazanır mı? Yorumlara yaz 👇

   Kaynak: <kaynak adları>

   Daha fazlası için @ilk.onbir11'i takip et ⚽

   #<takım> #<rakip ya da turnuva> #ilk11 #futbol
   ```
   Derbide iki takımın 11'i ayrı paragraflarda yer alır.
6. KAYIT ve B adımlarını uygula.

## SONUÇ GÖREVİ
Görev metni şunları verir: EV, DEP, TURNUVA, TARIH ve başlama saati.

1. K0'ı uygula. Anahtar KADRO'daki gibidir. Kayıtta `sonuc <anahtar>` varsa dur.
2. **Maç bitti mi?** "<ev> <dep> maç sonucu" diye ara.
   - **Bitmediyse** (uzatma, penaltılar ya da gecikme varsa): `mcp__claude-code-remote__create_trigger` ile bu görev metninin aynısıyla tek seferlik yeni bir görev kur. run_once_at şu an + 25 dk olur. Ad aynı kalır; initiation "human_schedule", notifications {"push": true}. Ardından dur. Başlamadan 4 saat sonrasını geçtiyse yeniden kurma; durumu bildir.
   - **Ertelendi ya da tatil edildiyse:** resmî açıklama varsa SON DAKİKA biçiminde paylaş, yoksa yalnız bildir.
3. **Doğrula:**
   - Kesin skor: resmî kaynak (UEFA/TFF/kulüp) ya da iki bağımsız kaynak.
   - Goller (dakika + oyuncu, penaltı için not "P", kendi kalesine için "KK"): yalnız iki kaynak aynı veriyorsa yaz; değilse `goller` alanını boş bırak.
   - `not` (isteğe bağlı): doğrulanmış tek kısa bilgi, ör. puan durumu, tur atlama ya da seri.
   - `sonraki`: resmî fikstürden doğrulanmış sıradaki maç.
4. `~/sonuc.json` yaz, motor/ozel.py ile üret ve kontrol et (KADRO 4. adımdaki gibi).
5. Y'yi uygula (tur sonuc), sonra P'yi. Açıklama:
   ```
   ⚽ MAÇ SONUCU | <EV> <skor> <DEP>

   <2–3 cümlelik özet; yalnız doğrulanmış bilgiler>

   Sence maçın yıldızı kimdi? Yorumlara yaz 👇

   Kaynak: <…>

   Daha fazlası için @ilk.onbir11'i takip et ⚽

   #<takım> #<turnuva> #ilk11 #futbol
   ```
6. KAYIT ve B adımlarını uygula.

## SON DAKİKA GÖREVİ
1. K0'ı uygula. motor/paylasilan.txt dosyasını ve getScheduledPosts ile bugünkü gönderileri oku.
2. Takip edilen 5 takımla ilgili **son 4 saatin** haberlerini tara: her takım için ayrı arama yap, kulüplerin resmî açıklamalarına ve KAP'a bak.
3. **Önemli sayılanlar:**
   - resmî transfer (imza, KAP bildirimi) ya da resmî ayrılık,
   - teknik direktör ataması ya da ayrılığı,
   - resmî açıklanan ciddi sakatlık ya da uzun süre forma giyememe,
   - PFDK, UEFA veya FIFA cezaları,
   - milli takım aday kadrosu,
   - maç ertelemesi ya da saat/stat değişikliği,
   - kulüp başkanı ya da yönetim değişikliği,
   - kırılan önemli bir rekor,
   - çok konuşulan resmî bir açıklama.
4. **Paylaşılmayanlar:**
   - söylentiler ("iddia", "masada" gibi),
   - muhtemel 11'ler,
   - maç sonuçları ve ilk 11'ler (bunları diğer görevler paylaşır),
   - sıradan antrenman haberleri,
   - magazin,
   - doğrulanmamış her şey.
5. Her aday haberi doğrula (KURALLAR). KAYIT'la ve bugünkü Metricool gönderileriyle karşılaştır; daha önce paylaşıldıysa atla.
6. Bir çalışmada **en fazla 2** haber paylaş; bugün toplam 6 son dakika paylaşıldıysa dur. Önemli haber yoksa hiçbir şey paylaşma ve tek satırla bitir; bildirim gönderme.
7. Her haber için şunları yap:
   - `~/sondakika.json` yaz: takim, baslik (≤ 70 karakter), ozet (2–3 cümle, ≤ 240 karakter, kendi cümlelerinle), kaynaklar.
   - Kartı üret ve kontrol et.
   - Y'yi uygula (tur sondakika).
   - P'yi uygula. Açıklama:
     ```
     🚨 SON DAKİKA | <TAKIM>

     <özet>

     Sen ne düşünüyorsun? Yorumlara yaz 👇

     Kaynak: <…>

     Daha fazlası için @ilk.onbir11'i takip et ⚽

     #<takım> #sondakika #ilk11 #futbol
     ```
   - KAYIT ve B adımlarını uygula.

# İLK 11 · Maç günü ve son dakika görevleri

Bu dosya otomatik görevlerin talimatıdır. Görev metni hangi bölümü uygulayacağını ve maç bilgilerini verir. Bu işler otomatik çalışır; kullanıcıya soru sorulmaz, en makul seçim yapılır. Sayfa sahibi bu paylaşımların kendisine sorulmadan yapılmasını istedi. Tüm metinler Türkçe olur.

**Takip edilen takımlar:** TÜRKİYE (A Milli Takım), BEŞİKTAŞ, FENERBAHÇE, GALATASARAY, TRABZONSPOR. Hazırlık maçları dahil bütün turnuvalar kapsanır.

**KİŞİ FOTOĞRAFI VE VİDEO:** motor/FOTO_VIDEO.md'yi oku ve uygula — içerikteki kişiler arka planı kaldırılmış (kesik PNG) fotoğrafla gösterilir; ilgili video varsa o da paylaşılır.

---

## ORTAK ADIMLAR

> **MANUEL MOD:** `motor/MANUEL_MOD` dosyası varsa (Metricool hesap sınırı dolu; sayfa sahibi paylaşımları bir süre elle yapıyor) Y ve P adımlarını ATLA, yerine **M** adımını uygula. Dosya yoksa normal akış (Y → P → B) geçerlidir. Sayfa sahibi Metricool planını yükseltince dosya silinir.

### K0 · Kurulum
1. Tarih ve saati al: `TZ=Europe/Istanbul date '+%F %H:%M'`.
2. ToolSearch ile şu araçları yükle: `select:mcp__Metricool_Social_Media_Management__createScheduledPost,mcp__Metricool_Social_Media_Management__getScheduledPosts,SendUserMessage,SendUserFile,mcp__claude-code-remote__add_repo,mcp__claude-code-remote__create_trigger`.
3. `add_repo` çağır: owner `zfraktas65-oss`, repo `ilk11-medya`, access `push`.
4. `~/ilk11-medya` yoksa klonla: `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya`. Sonra şunu çalıştır: `git config user.name "Claude" && git config user.email "noreply@anthropic.com"` (depo içinde).
5. **Logolar (bir kez):** `motor/logolar/` içinde turkiye/besiktas/galatasaray/fenerbahce/trabzonspor dosyalarından eksik olan varsa indirmeyi dene; erişim yoksa (403/bağlantı reddi) sessizce geç, paylaşımı aksatma.
   - Türkiye: `curl -sfo motor/logolar/turkiye.png https://www.tff.org/Resources/TFF/Images/0000000015/TFF/TFF-Logolar/Orjinal/tff01.png`
   - Kulüpler: yalnız resmî siteden (bjk.com.tr, galatasaray.org, fenerbahce.org, trabzonspor.org.tr) ya da UEFA'nın takım logosu dosyasından (bkz. motor/logolar/KAYNAK.txt); logo sitelerinden indirme.
   - İndirileni Read ile aç, doğru ve bozulmamış armaysa commit edip gönder (`git add motor/logolar && git commit -qm "logo" && git push -q`).
6. Python playwright ve Chromium hazır olmalı. Eksikse kur: `pip install --break-system-packages -q playwright && python3 -m playwright install chromium`.

### KAYIT · motor/paylasilan.txt
Her paylaşım tek satırla kaydedilir: `YYYY-AA-GG SS:DD <tur> <anahtar> | <kısa başlık>`. `tur` değeri kadro, sonuc, sondakika, demec, demecvideo (maç sonu demeci için sayfa sahibine video haberi verildi), puan veya fikstur olur.
- Anahtar örnekleri: kadro/sonuç için `2026-10-24-galatasaray-kasimpasa`, son dakika için `2026-10-24-fenerbahce-teknik-direktor`.
- **Paylaşmadan önce** aynı tur ve anahtarla bir satır varsa paylaşma.
- Son dakikada aynı olay farklı kelimelerle de olsa son 3 günde paylaşıldıysa paylaşma.
- Paylaşımdan sonra satırı ekle ve gönder: `cd ~/ilk11-medya && git pull --rebase -q && echo "<satır>" >> motor/paylasilan.txt && git add motor/paylasilan.txt && git commit -qm "kayıt" && git push -q`. Çakışma olursa en fazla 3 kez tekrar dene.

### Y · Kartları yükle
`<tur>` kadro, sonuc, sondakika veya demec olur; `<ANAHTAR>` kayıttaki anahtardır.
```
cd ~/ilk11-medya && rm -rf ~/medya && git worktree prune
git worktree add --detach ~/medya HEAD && cd ~/medya && git checkout -q --orphan medya-<tur>-<ANAHTAR> && git rm -rqf .
mkdir -p <ANAHTAR> && cp ~/cikti/*.jpg <ANAHTAR>/ && git add <ANAHTAR> && git commit -qm "<tur> <ANAHTAR>" && git push -q origin HEAD:refs/heads/medya-<tur>-<ANAHTAR>
SHA=$(git rev-parse HEAD)
```
- Bağlantı: `https://raw.githubusercontent.com/zfraktas65-oss/ilk11-medya/$SHA/<ANAHTAR>/<dosya>`.
- Dal adı yerine **mutlaka SHA** kullan; dal adlı bağlantı ilk dakikalarda 404 verir.
- Force-push (`-f`) kullanma; her paylaşım kendi yeni dalına normal push ile yüklenir. Dal zaten varsa adın sonuna `-2` ekle.
- Her dosya için curl ile 200 döndüğünü doğrula.

### P · Paylaş (Metricool, blogId "7504196", Instagram)
0. **Son kontrol:** Paylaşmadan hemen önce `git pull` ile motor/paylasilan.txt dosyasına ve getScheduledPosts ile son 6 saatin gönderilerine yeniden bak. Aynı içerik (aynı maçın sonucu/kadrosu ya da aynı haber) paylaşılmış ya da planlanmışsa paylaşma ve dur.
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

### M · Manuel paylaşım paketi (yalnız MANUEL MOD'da)
Metricool'a hiçbir şey gönderme (createScheduledPost çağırma). Bunun yerine:
1. **Son kontrol:** `git pull` ile motor/paylasilan.txt'ye yeniden bak; aynı içerik kayıtlıysa gönderme ve dur.
2. SendUserFile ile (status "proactive") paylaşılacak görselleri sırayla gönder: önce gönderi kartları (01_…, 02_…, en sonda takip kartı), en sonda hikaye.jpg. caption: "Gönderi: 01–NN sırayla kaydırmalı · Hikâye: hikaye.jpg".
3. SendUserMessage ile kısa bir paylaşım notu gönder:
   - İlk satır: `📲 ELLE PAYLAŞ · <ne> · <önerilen saat: şimdi>`
   - Gönderi açıklama metni, kolay kopyalansın diye tek bir kod bloğu (```) içinde.
   - Altında "Hikâye: hikaye.jpg (açıklama yok)" satırı ve kaynak bağlantıları ([Başlık](URL)).
4. KAYIT satırının sonuna `(manuel)` ekle; paylaşılmış sayılır (aynı içerik tekrar gönderilmez).
5. Ayrıca B adımına gerek yok; bu mesaj bildirim yerine geçer.

### B · Bildir
SendUserMessage ile kısa bir özet gönder:
- ne paylaşıldı ve saati,
- kaynak bağlantıları ([Başlık](URL)),
- plannerUrl.

Kartı SendUserFile ile gönder (status "proactive").

Bir şey doğrulanamazsa ya da bir adım başarısız olursa **paylaşma**. Bunun yerine neyin olmadığını kısaca bildir.

### KURALLAR
- Kulüp logoları kullanılabilir (sayfa sahibinin izni): yalnız `motor/logolar/` klasöründeki resmî logo dosyaları, değiştirilmeden; `motor/ozel.py` bunları otomatik koyar. Logo kodla çizilmez, internetten rastgele logo sitelerinden indirilmez; dosyası olmayan takım renk şeridiyle gösterilir.
- Gerçek kişi fotoğrafı ya da maç görüntüsü kullanılmaz; kartlar `motor/ozel.py` ile üretilir.
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
Her saat çalışır. İki işi vardır: **A) son dakika haberleri** ve **B) maç öncesi / sonrası demeçler** (maç sonu demeçleri artık Reels için yalnız haber verilir; bkz. B).

1. K0'ı uygula. motor/paylasilan.txt dosyasını ve getScheduledPosts ile bugünkü gönderileri oku.
2. Takip edilen 5 takımla ilgili **son 2 saatin** haberlerini ve röportajlarını tara. Her takım için ayrı arama yap; kulüplerin resmî açıklamalarına ve KAP'a da bak.
3. Bulunanları KAYIT'la ve bugünkü Metricool gönderileriyle karşılaştır. Daha önce paylaşılanı atla.
4. Sınırlar:
   - Bir çalışmada en fazla 2 son dakika ve 2 demeç gönderisi paylaşılır.
   - Bir günde en fazla 8 son dakika ve 8 demeç paylaşılır.
   - Paylaşılacak bir şey yoksa hiçbir şey paylaşma ve tek satırla bitir; bildirim gönderme.

### A) Son dakika
**Önemli sayılanlar:**
- resmî transfer (imza, KAP bildirimi) ya da resmî ayrılık,
- teknik direktör ataması ya da ayrılığı,
- resmî açıklanan ciddi sakatlık ya da uzun süre forma giyememe,
- PFDK, UEFA veya FIFA cezaları,
- milli takım aday kadrosu,
- maç ertelemesi ya da saat/stat değişikliği,
- kulüp başkanı ya da yönetim değişikliği,
- kırılan önemli bir rekor,
- çok konuşulan resmî bir açıklama.

**Paylaşılmayanlar:**
- söylentiler ("iddia", "masada" gibi),
- muhtemel 11'ler,
- maç sonuçları ve ilk 11'ler (bunları diğer görevler paylaşır),
- sıradan antrenman haberleri,
- magazin,
- doğrulanmamış her şey.

Her haber için:
1. KURALLAR'a göre doğrula.
2. `~/sondakika.json` yaz: takim, baslik (≤ 70 karakter), ozet (2–3 cümle, ≤ 240 karakter, kendi cümlelerinle), kaynaklar.
3. Kartı üret ve kontrol et: `rm -rf ~/cikti && python3 motor/ozel.py ~/sondakika.json ~/cikti`, ardından Read ile aç.
4. Y'yi uygula (tur sondakika), sonra P'yi. Açıklama:
   ```
   🚨 SON DAKİKA | <TAKIM>

   <özet>

   Sen ne düşünüyorsun? Yorumlara yaz 👇

   Kaynak: <…>

   Daha fazlası için @ilk.onbir11'i takip et ⚽

   #<takım> #sondakika #ilk11 #futbol
   ```
5. KAYIT ve B adımlarını uygula.

### B) Demeçler (maç öncesi / maç sonrası röportajlar)
**Kimin sözleri:** takip edilen 5 takımın oyuncuları, teknik direktörleri, başkanları ve yöneticileri.

**Hangi sözler:** yalnız maçlarla ilgili olanlar:
- maç öncesi basın toplantısı ya da maç önü röportajı,
- maç sonu flaş röportaj ya da basın toplantısı.

> **MAÇ SONU DEMEÇLERİ ARTIK KART OLARAK PAYLAŞILMAZ** (sayfa sahibinin isteği, 2026-10-23). Maç sonu demeçleri videolu Reels olarak yapılır: motor/gorevler/demec_reels.md. Bu ortam videoyu kendisi indiremediği için bu görev maç sonu demeci bulduğunda **yalnız haber verir**:
> 1. KAYIT'ta aynı anahtarla (`TARIH-<ev>-<dep>-sonra-<takım>-N`) `demecvideo` ya da `demec` satırı varsa atla.
> 2. SendUserMessage ile şu mesajı gönder (kart üretme, Metricool'a bir şey gönderme):
>    ```
>    🎥 MAÇ SONU DEMEÇ VAR · <EV> <SKOR> <DEP>
>    <Kim, rol> — <ne dediğinin 1 cümlelik özeti, kendi cümlenle> (<flaş röportaj / basın toplantısı>)
>    Video: <resmî kulüp/yayıncı/UEFA sayfasında video varsa bağlantısı; yoksa "videoyu sosyal medyada bulabilirsin">
>    Klibi bu sohbete gönder, İLK 11 Reels'ine çevireyim.
>    ```
>    Kaynak bağlantılarını ([Başlık](URL)) mesajın altına ekle. Aynı maçın aynı anı için birden çok kişi konuştuysa tek mesajda alt alta yaz.
> 3. KAYIT'a `YYYY-AA-GG SS:DD demecvideo <anahtar> | <Kişi> maç sonu (video bekleniyor)` satırını ekle (aynı haber tekrar gönderilmez).
> 4. Sayfa sahibi bu oturumda klip gönderirse motor/gorevler/demec_reels.md'yi baştan sona uygula.
> Bu haber mesajları "demeç gönderisi" sınırına sayılmaz; bir takımın bir maçı için en fazla 2 haber (ör. flaş röportaj, basın toplantısı) gönderilir. Aşağıdaki kart kuralları (Kaynak şartı, Kartlara dağıtım, Gruplama, Her gönderi için) artık yalnız **MAÇ ÖNCESİ** demeçler için geçerlidir.

**Kaynak şartı:**
- Demeç **TAM METİN** verilir: kişinin kaynakta yer alan sözlerinin hepsi, kaynaktaki sırayla. Seçme ya da kısa alıntı yapılmaz (sayfa sahibinin isteği).
- Söz kaynaktakiyle **birebir** aynı olur; kelime asla değiştirilmez, söz uydurulmaz.
- Tam metin şu kaynaklardan birinden alınır: resmî kaynak (kulübün resmî sitesi/hesabı, UEFA, TFF yayını) ya da tam metni veren güvenilir bir haber (tercihen AA/İHA/DHA metni). Metin, ikinci bağımsız güvenilir kaynakla karşılaştırılır.
- Kaynaklarda farklı geçen cümle olursa: resmî kaynaktaki hâli kullanılır; resmî kaynak yoksa yalnız iki kaynakta aynı geçen cümleler verilir ve çıkarılan yerler "…" ile gösterilir.
- Kaynakta yazar/muhabir yorumuyla aktarılan (dolaylı) kısımlar söz gibi verilmez; yalnız tırnak içindeki ya da doğrudan aktarılan sözler alınır.
- Çeviri sözlerde (yabancı teknik direktör ya da oyuncu) Türkçe basının ortak aktardığı metin kullanılır; çevirisi kaynaklar arasında farklıysa resmî kulüp çevirisi, o yoksa tam metni veren tek güvenilir kaynak (kaynak adı belirtilerek) kullanılır ve diğer kaynakla anlamca aynı olduğu kontrol edilir.
- Web aracı haber sitelerinden çoğu zaman yalnız kısa alıntı döndürür. Tam metin alınamazsa kaynakta birebir bulunduğu teyit edilen **bütün** cümleler kaynaktaki sırayla verilir, aralarına "…" konur. Kısa tutmak için cümle elenmez.
- Gazeteci soruları gerekirse kısa "Soru: …" satırı olarak eklenebilir.

**Çıkarılacak kısımlar:**
- Hakaret, küfür ya da bir kişiyi suçla itham eden ifadeler metinden çıkarılır ve yerine "…" konur. Bunlar metnin ana kısmıysa o demeç hiç paylaşılmaz.
- Hakem ve federasyon eleştirileri, kaynakta nasıl söylendiyse öyle ve yorum katmadan verilir.

**Kartlara dağıtım:**
- Gönderide uzun demeç birkaç karta bölünür; `motor/ozel.py` bunu cümle sınırlarından otomatik yapar (kart başına ≈ 360 karakter). Devam eden kart "…" ile başlar.
- Instagram en fazla 20 görsel alır (19 demeç kartı + takip kartı). Daha uzunsa demeçler iki gönderiye ayrılır (ör. teknik direktör ayrı, oyuncular ayrı; anahtarlar `-1`, `-2`).
- **Hikâyede bütün demeçler TEK ekranda** verilir; `motor/ozel.py` hikaye.jpg'yi yazı boyunu otomatik küçülterek üretir. Read ile aç ve okunurluğu kontrol et; sığmazsa betik hata verir: o durumda hikâyeyi her kişi için ayrı tek ekran olarak üret (her kişiyle ayrı demec.json) ve hepsini sırayla hikâye olarak paylaş.

**Gruplama:**
- Aynı maça ve aynı ana (maç öncesi ya da maç sonu) ait demeçler TEK gönderide toplanır (karakter sınırı içinde).
- Bir takım için bir maçta en fazla 1 "maç öncesi" ve 2 "maç sonu" demeç gönderisi paylaşılır (ör. önce flaş röportaj, sonra basın toplantısı).
- Anahtar biçimi: `TARIH-<ev>-<dep>-once-<takım>` veya `TARIH-<ev>-<dep>-sonra-<takım>-1/2`.

Her gönderi için:
1. `~/demec.json` yaz. Biçim motor/ozel.py başındaki "4) DEMEÇ" bölümünde. baslik "MAÇ ÖNCESİ" ya da "MAÇ SONU" olur; mac alanı "EV – DEP · TURNUVA" biçimindedir.
2. Kartları üret ve kontrol et (yukarıdaki gibi).
3. Y'yi uygula (tur demec), sonra P'yi. Hikâye adımında media'ya hikaye.jpg (gerekirse kişi başına ayrı hikâyeler, sırayla +5, +6… dk) konur. Açıklama:
   ```
   🎙️ <MAÇ SONU / MAÇ ÖNCESİ> KONUŞTULAR | <EV> – <DEP>

   <Kim, rol>: "<demecin tam metni>"
   (her kişi için bir paragraf)

   Sence haklılar mı? Yorumlara yaz 👇

   Kaynak: <…>

   Daha fazlası için @ilk.onbir11'i takip et ⚽

   #<takım> #<turnuva> #ilk11 #futbol
   ```
   Instagram açıklaması en fazla 2.200 karakterdir. Tam metin sığmazsa açıklamada her kişinin ilk 1–2 cümlesi birebir verilir ve "Demeçlerin tamamı kartlarda 👉" satırı eklenir; tam metin her durumda kartlarda ve hikâyede bulunur.
4. KAYIT ve B adımlarını uygula.

## FİKSTÜR / KALAN MAÇLAR
Kullanıcı istediğinde (ya da yeni tur kurası çekildiğinde) Avrupa'daki ya da bir turnuvadaki kalan maçlar paylaşılır.
1. K0'ı uygula. Anahtar `TARIH-avrupa-kalan-maclar` (ya da `TARIH-<turnuva>-kalan-maclar`). Kayıtta `fikstur <anahtar>` varsa dur.
2. Her takımın kalan maçlarını (tarih, ev, deplasman) resmî kaynaktan ya da iki bağımsız kaynaktan doğrula. Saat yalnız iki kaynakta aynıysa yazılır.
3. `fikstur.json` yaz (biçim motor/ozel.py başındaki "6) FİKSTÜR"), rakip logosu yoksa motor/logolar/KAYNAK.txt'e göre ekle; üret ve Read ile kontrol et.
4. Y'yi uygula (tur fikstur), sonra P'yi. Açıklama: `📅 AVRUPA'DA KALAN MAÇLAR | …`, her takım için "TAKIM · Turnuva" başlığı ve altında `Gün Ay: Ev – Dep` satırları, soru, Kaynak, takip satırı, en fazla 5 hashtag.
5. KAYIT ve B adımlarını uygula.

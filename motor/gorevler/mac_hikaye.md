# İLK 11 – Maç Hikâyeleri görev talimatı (skor · puan durumu · maçtaki olaylar)

Sayfa sahibinin isteği (2026-10-23): seçtiği maçlar bittikten **30–45 dk sonra** maçın sonucu, puan durumu ve maçta yaşanan haber değeri taşıyan **bütün olaylar**, **her biri ayrı bir Instagram hikâyesi** olarak hazırlanır. Hikâyeleri sayfa sahibi kendisi paylaşır: bu görev Metricool'a hiçbir şey göndermez, görselleri ve kısa notu sohbete gönderir. Örnek: motor/ornekler/mac_alanya_kocaeli.json (Alanyaspor 1-2 Kocaelispor).

Bu otomatik bir çalışmadır; kullanıcıya soru sorma. Görev metni şunları verir: EV, DEP, TURNUVA, TARİH, başlama saati.

## ADIM 0 — Hazırlık
- `TZ=Europe/Istanbul date '+%F %H:%M'`. ToolSearch: "select:SendUserFile,SendUserMessage,mcp__claude-code-remote__create_trigger".
- Depo: add_repo (owner "zfraktas65-oss", repo "ilk11-medya", access "push"), `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya` (timeout 600000), `git config user.name "Claude" && git config user.email "noreply@anthropic.com"`. Playwright + Chromium hazırdır (eksikse pip ile kur).
- motor/paylasilan.txt'de `machikaye <TARIH>-<ev>-<dep>` satırı varsa dur (aynı maç ikinci kez gönderilmez).

## ADIM 1 — Maç bitti mi?
"<EV> <DEP> maç sonucu" diye ara. Bitmediyse (uzatma, gecikme, ertelenmiş başlama): create_trigger ile bu görev metninin aynısıyla tek seferlik yeni görev kur — run_once_at = şimdi + 15 dk, ad aynı, initiation "human_schedule", notifications {"push": true} — ve dur. Başlama saatinden 4 saat sonrasını geçtiyse yeniden kurma; SendUserMessage ile durumu bildir. Maç ertelendi/tatil edildiyse yalnız bunu (resmî kaynakla) bildir.

## ADIM 2 — Doğrula (her bilgi en az iki bağımsız güvenilir kaynakta aynı olmalı; resmî kaynak — TFF, kulüp, valilik — tek başına yeter)
- **Skor** ve varsa **ilk yarı skoru**.
- **Goller:** dakika + oyuncu; penaltı "P", kendi kalesine "KK". İki kaynak golcüde ayrışırsa o golü dakikasıyla yaz, adı yazma; hiçbiri doğrulanamazsa `goller` boş kalır.
- **Kırmızı kartlar** (`kartlar`): dakika + oyuncu.
- **Puan durumu:** iki takımın maç sonrası sırası ve puanı (TFF puan tablosu ya da iki kaynak). Haftanın diğer maçları bitmediyse `puan_alt` "9. HAFTA · CUMARTESİ MAÇLARI SONRASI" gibi yazılır ve `puan_not` "Hafta sürüyor; sıralama diğer maçlarla değişebilir." olur. Sırası yükselen takıma "▲", düşene "▼"; kazanan ya da sıralamada öne çıkan takım `vurgu`.
- **Olaylar** (`olaylar`, her biri ayrı hikâye, en fazla 5): maçta ya da maç günü yaşanan, haber değeri taşıyan her şey —
  taraftar olayları (stada alınmama, protesto, koreografi, pankart, saha karışıklığı, seyirci rekoru), kırmızı kart ve tartışmalı pozisyonlar (VAR, iptal edilen gol, verilmeyen penaltı), kaçan penaltı, maçtan çıkaran sakatlık, rekor/ilk (ilk gol, seri, kulüp rekoru), teknik direktör/başkan/futbolcunun maç sonu çarpıcı açıklaması (söz kaynaktakiyle birebir, tırnak içinde), maçın durması/gecikmesi, güvenlik kararları.
  Kurallar: yalnız doğrulanmış olaylar; söylenti yok; tek kaynakta geçen ya da kaynakların çeliştiği ayrıntıyı (dakika, sayı) yazma ya da genel ifade kullan. Bireysel taraftarları adıyla anma, şiddet görüntüsü/ayrıntısı verme, hakaret içeren sözleri aktarma. Hakem kararlarını yorumsuz, kaynakta nasıl geçtiyse öyle ver.
  Her olay: `etiket` (≤ 14 harf: TARAFTAR, KIRMIZI KART, VAR, SAKATLIK, REKOR, AÇIKLAMA, MAÇ ÖNCESİ…; kırmızı kart/olumsuz olayda `"kirmizi": true`), `baslik` (≤ 45 karakter, kendi cümlen), `metin` (2–3 cümle, ≤ 260 karakter, `<b>vurgu</b>` olabilir), isteğe bağlı `takim`, `dk`.
  Haber değeri taşıyan olay yoksa yalnız skor ve puan hikâyeleri hazırlanır.

## ADIM 3 — Görseller
`~/mac.json` yaz (biçim: motor/mac_hikaye.py başı; `"bicim": "ayri"`). Takım adları büyük harf, Türkçe karakterle; kısa ad kullan (ör. "AMEDSPOR", "GAZİANTEP FK", "ERZURUMSPOR FK"). Logolar motor/logolar/<sade-ad>.png'den otomatik gelir (ör. gaziantepfk.png); yoksa `renkler` ile renk rozeti çizilir. Bilinen renkler: EYÜPSPOR ["#5B2C83","#FFD200"], KASIMPAŞA ["#1B3A8C","#FFFFFF"], GAZİANTEP FK ["#D71920","#111111"], ERZURUMSPOR FK ["#0057A8","#FFFFFF"], SAMSUNSPOR ["#E30613","#FFFFFF"], AMEDSPOR ["#C8102E","#007A3D"], ALANYASPOR ["#F47C20","#00843D"], KOCAELİSPOR ["#00A651","#111111"].
`python3 ~/ilk11-medya/motor/mac_hikaye.py ~/mac.json ~/mac_cikti` → 01_skor.jpg, 02_puan.jpg, 03_olay.jpg… Her görseli Read ile aç: taşma, yanlış isim/skor/sıra, boş alan sorunu varsa düzelt ve tekrar üret.

## ADIM 4 — Gönder
- SendUserFile (status "proactive") ile görselleri sırayla gönder; caption: "<EV> <skor> <DEP> · hikâyeler sırayla (1/N …)".
- SendUserMessage: ilk satır `📲 HİKÂYELER HAZIR · <EV> <skor> <DEP>`; ardından her hikâyenin tek satırlık özeti (1. skor, 2. puan durumu, 3. …), doğrulanamadığı için konmayan önemli bir iddia varsa tek satırla belirt, en altta kaynaklar ([Başlık](URL)). Logosu eksik takım varsa "logosunu gönderirsen sonrakilerde kullanırım" notu.

## ADIM 5 — Kayıt
`cd ~/ilk11-medya && git pull --rebase -q`, motor/paylasilan.txt'ye `YYYY-AA-GG SS:DD machikaye <TARIH>-<ev>-<dep> | <EV> <skor> <DEP> (manuel)` ekle; commit ("kayıt") ve push. Çakışma olursa en fazla 3 kez tekrar dene.

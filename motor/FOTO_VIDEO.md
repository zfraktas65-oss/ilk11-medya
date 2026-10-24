# İLK 11 · Kişi fotoğrafı ve video kuralı (sayfa sahibinin isteği, 2026-10-24)

Bu kural BÜTÜN İLK 11 paylaşımlarında geçerlidir: Reels (hikâye, portre, demeç), kaydırmalı gönderiler, son dakika/demeç kartları, maç hikâyeleri.

## 1. Kişiler arka planı kaldırılmış fotoğrafla gösterilir
- İçerikte öne çıkan gerçek bir kişi (oyuncu, teknik direktör, başkan…) varsa, fotoğrafı **arka planı kaldırılmış (kesik, şeffaf PNG)** hâliyle kullanılır. Kişi çerçevesiz, sayfanın yeşil zemininin önünde durur.
- Kesik dosya: `motor/fotolar/kesik/<ad>.png`. Yoksa üret:
  `pip install --break-system-packages -q "rembg[cpu]"` (bir kez) → `python3 ~/ilk11-medya/motor/kesik.py ~/ilk11-medya/motor/fotolar/<ad>.jpg`
  Üretilen PNG'yi Read ile aç (kişi eksiksiz mi, arka plan kalmış mı); iyiyse `git add motor/fotolar/kesik && git commit -qm "kesik foto" && git push -q`.
- Motorlar `.png` uzantılı fotoğrafı otomatik kesik düzende çizer:
  - Reels (hikaye.py): `{"tip":"foto","foto":"<ad>.png",...}` → kişi büyük, altyazı bandının üstünde. Dosyayı senaryo.json'un klasörüne kopyala ya da mutlak yol ver.
  - Kartlar (foto_hikaye.py — demeç / son dakika): `"foto": "/root/ilk11-medya/motor/fotolar/kesik/<ad>.png"`.
- Reels'te kişi varsa en az bir `foto` sahnesi kesik fotoğrafla olur (tercihen kanca ya da 2. sahne — görüntüyü erkenden değiştirir, ilk 8 saniyede izleyiciyi tutar).

## 2. Fotoğrafın kaynağı (değişmedi)
- YALNIZ kullanım hakkı olan dosyalar: `motor/fotolar/` içindeki, `motor/fotolar/KAYNAK.txt`'ye kayıtlı Wikimedia Commons CC / kamu malı fotoğraflar ya da sayfa sahibinin sohbete gönderdiği fotoğraflar (sayfa sahibinin verdiği kredi ile; KAYNAK.txt'ye "sayfa sahibinden" diye eklenir).
- Haber sitelerinden, Getty/AA/AP gibi ajanslardan, Instagram'dan ya da Google Görseller'den fotoğraf ALINMAZ. Kredi (yazar + lisans) videoda/kartta ve açıklamada yazılır.
- Bulut ortamı Wikimedia'ya erişemez. Kişinin uygun fotoğrafı depoda yoksa içeriği fotoğrafsız (ikon/bayrak/renk şeridi ile) üret ve bildirimin sonuna şu notu ekle: "📷 <Kişi> için depoda lisanslı fotoğraf yok — gönderirsen arka planını kaldırıp ekleyeyim."

## 3. Video varsa o da paylaşılır
- İçerikle ilgili bir video varsa (sayfa sahibinin sohbete gönderdiği klip — basın toplantısı, maç anı, röportaj; ya da üretilen Reels mp4'ü), görsellerle birlikte o video da hazırlanır ve gönderilir:
  - Demeç/basın toplantısı klibi → `motor/gorevler/demec_reels.md` ile Reels üret; kart paylaşımına ek olarak videoyu da gönder.
  - Manuel modda: videoyu SendUserFile ile kartlarla aynı pakette gönder ve "📲 ELLE PAYLAŞ" mesajında videonun nasıl paylaşılacağını (Reels / hikâye) yaz.
- Bu ortam TikTok/Instagram/YouTube'dan video İNDİREMEZ; video uydurulmaz. Klip yoksa yalnız görselleri paylaş.

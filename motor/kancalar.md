# İLK 11 · Kanca kütüphanesi

Kanca, videonun ilk 1–3 saniyesidir: Hoca'nın söylediği **ilk cümle** + kanca sahnesinin **ekran başlığı** (`baslik`). İzleyicinin parmağını durdurur. Hikâye (19:00) ve portre (13:00) Reels'leri her gün buradaki bir formülle açılır; hangi formülün kullanıldığı `motor/kanca_kayit.txt`'ye yazılır, istatistik gelince hangisinin tuttuğu görülür.

## Kurallar (her formülde geçerli)
1. **Sonucu söyleme, merak aç.** Sonuç son 1–2 cümlede açıklanır.
2. **Kısa:** ses ≤ 12 kelime (≈ 2–3 sn); ekran başlığı ≤ 5 kelime ve sesle aynı şeyi söylemez, tamamlar (ör. ses gerilimi anlatır, ekranda soru ya da rakam durur).
3. **En güçlü kelime başta:** rakam, isim, skor, çarpıcı nesne. "Bugün size…", "Merhaba", "Biliyor muydunuz" ile açılmaz.
4. **Doğru olmalı:** kancadaki her iddia ADIM 2'de doğrulanmış bilgiye dayanır. Abartı, uydurma ve "inanamayacaksın" gibi boş tıklama tuzakları yok. Rekor ve "ilk/tek" iddiaları yayın günü yeniden doğrulanır.
5. İlk iki cümlede arka plan (doğum yeri, yıl, kulüp geçmişi) yok.
6. Örnekler yalnız biçimi gösterir; konuya uydururken kelimeleri değiştir, kalıbı koru.

## Seçim (rotasyon)
1. `motor/kanca_kayit.txt`'nin son 6 satırındaki formülleri kullanma (iki seri birlikte sayılır).
2. Konuya en doğal oturan formülü seç; eşitlikte hiç kullanılmamış ya da "Öne çıkanlar"daki formülü tercih et.
3. Seçtiğin formülle 2 aday kanca yaz; daha kısa ve daha somut olanı al.
4. Kayıt (ADIM 8'deki kayıt commit'iyle birlikte): `TARIH | hikaye/portre | <konu-kodu> | <ID> | <kanca cümlesi> | sonuç: -`

Uygun seri: **H** = hikâye, **P** = portre.

## A · Merak boşluğu
- **K01** · "<Sıradan nesne/kişi>, <büyük şeyi> belirleyecekti." — "Dünya Kupası biletini, gözleri bağlı bir çocuk belirleyecekti." · H
- **K02** · "<Sıradan nesne>, futbol tarihini değiştirecekti." — "Bir kâğıt peçete, futbol tarihini değiştirecekti." · H P
- **K03** · "<Kısa süre>. Sonra hiçbir şey eskisi gibi olmadı." — "Altı dakika. Sonra hiçbir şey eskisi gibi olmadı." · H
- **K04** · "<Ünlü şeyin> arkasında bambaşka bir hikâye var." — "Sarı ve kırmızı kartın arkasında bir trafik lambası var." · H
- **K05** · "Bu <kural/gelenek> aslında bir <beklenmedik kişinin> fikriydi." — "Penaltı aslında bir kalecinin fikriydi." · H

## B · Rakamla açılış
- **K06** · "<Oran/rakam>." (tek başına, sonra kısa açıklama) — "Beş binde bir. Bahisçilerin bu takıma verdiği şans buydu." · H
- **K07** · "<Rakam> <birim>. Tek bir <turnuva/sezon/maç>." — "On üç gol. Tek bir turnuvada." · H P
- **K08** · "<Skor> geride. <Kalan süre> kaldı." — "Sıfır iki geride. On beş dakika kaldı." · H
- **K09** · "<Rakam> dakika arayla, aynı adamdan iki <zıt şey>." — "Dört dakika arayla, aynı adamdan iki efsane gol." · H P

## C · Sahnenin ortasından (in medias res)
- **K10** · "<An>. Skor <skor>. <Duygu/sessizlik>." — "Devre arası. Skor sıfır üç. Soyunma odasında çıt yok." · H
- **K11** · "Doksan dakika bitti. <Takım> hâlâ geride." — "Doksan dakika bitti. Manchester United hâlâ geride." · H
- **K12** · "<Kişi> yere yığıldı. Ama oyundan çıkmadı." — "Kaleci yere yığıldı. Ama oyundan çıkmadı." · H P
- **K13** · "<Yer>. <Kalabalık>. Ve sonra sessizlik." — "Maracanã. Dev bir kalabalık. Ve sonra sessizlik." · H

## D · İzleyiciye soru
- **K14** · "Sence bir <büyük şey> <tuhaf yöntemle> belirlenebilir mi?" — "Sence bir Dünya Kupası bileti kurayla belirlenebilir mi?" · H
- **K15** · "<İmkânsız görünen şey> yapılabilir mi?" — "Kırık bir boyunla maç bitirilebilir mi?" · H P
- **K16** · "Bir takımı turnuvaya <ne kadar> önce çağırsalar ne yapar?" — "Bir takımı turnuvaya on gün kala çağırsalar ne yapar?" · H
- **K17** · "Hayatının <maçını/golünü> attıktan sonra ilk ne yaparsın?" — "Dünya Kupası finalinde gol atınca ilk ne yaparsın?" · H P

## E · Uyarı / "dur"
- **K18** · "Bunu duymadan bir daha <yaygın davranış> yapma." — "Bunu duymadan bir daha maçı devre arasında kapatma." · H
- **K19** · "<Etiket> deme. Önce bunu dinle." — "'Bitti' deme. Önce bunu dinle." · H

## F · Ters köşe / zıtlık
- **K20** · "Herkes <yaygın inanç> sanır. Gerçek çok daha tuhaf." — "Herkes kartları bir hakemin icat ettiğini sanır. Gerçek çok daha tuhaf." · H
- **K21** · "Onu herkes <olumsuz etiket> buluyordu." — "Onu herkes fazla kısa buluyordu." · P
- **K22** · "<Kişi/takım> için kimse tek kuruş vermiyordu." — "Bu takım için kimse tek kuruş vermiyordu." · H P
- **K23** · "Kazanacağı hiçbir şey yokmuş gibi görünüyordu." · H P

## G · Rekor / ilk / tek
- **K24** · "Bunu başaran tek <rol> o." — "Bunu başaran tek kaleci o." · P
- **K25** · "<Kapsam>da bunu ilk kez bir <takım/kişi> yaptı." — "İstanbul dışından ilk kez bir takım bunu yaptı." · H
- **K26** · "<Yer> bunu daha önce hiç görmemişti." — "Avrupa, bir Türk takımını bu kupayla hiç görmemişti." · H

## H · Gizli ayrıntı
- **K27** · "Bu <formanın/kâğıdın/topun> altında bir sır vardı." — "Bu formanın altında bir mesaj vardı." · H P
- **K28** · "Herkes golü izledi. Kimse <ayrıntıyı> fark etmedi." · H P
- **K29** · "Sözleşmesi bir <beklenmedik nesneye> yazıldı." — "Sözleşmesi bir peçeteye yazıldı." · P

## I · Portre (lakap, insan)
- **K30** · "Ona '<lakap>' dediler. Ama neden?" — "Ona 'Taçsız Kral' dediler. Ama neden taçsız?" · P
- **K31** · "Bir ülke onu '<lakap>' diye andı." — "Bir ülke onu 'Karpatların Maradonası' diye andı." · P
- **K32** · "<Rakip/şehir> onun adını duyunca titriyordu." · P
- **K33** · "Bir <engel> yüzünden herkes onu silmişti." · P
- **K34** · "Bu forma ona <beklenmedik süre/yaşta> geldi." — "A takım forması ona on altı yaşında geldi." · P

## J · Sen dili (POV)
- **K35** · "Sen <rol>sün. <Gerilim anı>." — "Sen kalecisin. Skor iki iki. Penaltı yok." · H
- **K36** · "Düşün: <sıra dışı durum>." — "Düşün: Dünya Kupası'na gitmek için torbadan bir kâğıt çekiliyor." · H

## Öne çıkanlar
Sayfa sahibi istatistik gönderdikçe güncellenir: geçme oranı düşük ve 3. saniye tutması yüksek formüller buraya yazılır, seçimde öncelik alır.
- 2026-10-29 verisi (4 Reels): en düşük geçme 1954 kura %31,4 ve Hagi %32,6; en yüksek Modrić K21 %44,8 (yabancı yıldız + 'fazla çelimsiz' kancası tutmadı). Etkileşimde en iyisi Alex K07 (beğeni %2,6, 6 paylaşım, 7 kayıt). Hepsinde izleyicinin ~yarısı ilk 8–10 sn'de gidiyor, kalanların çoğu sona kadar kalıyor. Hiçbir Reels takip getirmedi.
- Şimdilik öncelik: Türk futbolu bağlantılı konu + somut rakam/an ile açılan kanca (K07, K06, K10). K21 tek örnekte zayıf.

# İLK 11 – Maç Sonu Demeç Reels (videodan) görev talimatı

Sayfa sahibinin isteği (2026-10-23): **maç sonu açıklamaları artık kart olarak değil, bu Reels formatında paylaşılır.** Örnek: Italiano, Beşiktaş 2-2 Crystal Palace basın toplantısı (motor/ornekler/demec_italiano.json).

Ne zaman: sayfa sahibi bir maç sonu basın toplantısı / flaş röportaj klibini sohbete gönderdiğinde (çoğu zaman SON DAKİKA görevinin "🎥 MAÇ SONU DEMEÇ VAR" mesajına cevap olarak). Bu ortam TikTok/Instagram/YouTube'dan video İNDİREMEZ; klip her zaman sayfa sahibinden gelir. Klip yoksa video uydurma, fotoğraf/ses üretme; yalnız klibi iste.

Çıktı: 9:16 Reels — üstte "MAÇ SONU KONUŞTU" bandı, kişi + skor satırı, en çarpıcı söz (lime), ortada yeşil çerçeveli video penceresi, kelime kelime vurgulu büyük Türkçe altyazı, altta kaynak notu ve @ilk.onbir11, sonda Hoca'nın takip çağrısı.

## ADIM 0 — Kurulum
- Depo: add_repo (owner "zfraktas65-oss", repo "ilk11-medya", access "push") ve `git clone --depth 1 https://github.com/zfraktas65-oss/ilk11-medya ~/ilk11-medya` (timeout 600000). `git config user.name "Claude" && git config user.email "noreply@anthropic.com"`.
- `pip install --break-system-packages -q sherpa-onnx soundfile`. Playwright + Chromium + ffmpeg ortamda hazırdır (eksikse pip ile kur; PLAYWRIGHT_BROWSERS_PATH varsa `playwright install` çalıştırma).
- Klibi `~/demec/kaynak.mp4` olarak kopyala (orijinal eki değiştirme).

## ADIM 1 — Klibi tanı
- `ffprobe` ile süre/çözünürlük. 12 kare çıkarıp tek tabloya koy ve Read ile bak: kim konuşuyor, hangi maç (arka plan panosu: UEFA/TFF), filigran/kaynak hesap (ör. TikTok @hesap), sonda kapanış kartı var mı.
- Maçı, skoru ve kişiyi WebSearch ile doğrula (en az bir güvenilir kaynak; tercihen iki). Doğrulayamadığın skoru ya da kişiyi yazma, sayfa sahibine sor.
- Kapanış kartı (TikTok/Instagram bitişi) varsa başladığı anı bul: `ffmpeg -ss <son-4> -i kaynak.mp4 -t 4.5 -vf "select='gt(scene,0.15)',showinfo" -f null -` ; `son` bu anın ~0,1 sn öncesi olur. Konuşmanın bittiği yerden sonrasını da kes.

## ADIM 2 — Yazıya dök
- `python3 ~/ilk11-medya/motor/yazi.py ~/demec/kaynak.mp4 ~/demec/ham.json --dil tr --son <son>` (ilk çalıştırmada model ~560 MB iner; ~3–5 dk sürer, gerekirse run_in_background).
- Ham metni düzelt ve `ifadeler`e koy. Kurallar:
  - Söylenen sözler **birebir** kalır; kelime ekleme, cümle uydurma, anlam değiştirme yok. Yalnız tanıma hatalarını düzelt (ör. "namalubuz" → "namağlubuz", "karşılandık" → "karşılaştık", "elimle etmek" → "elimine etmek") ve noktalama koy.
  - Oyuncu/kişi adlarını kadrodan doğrula ve doğru yaz (ör. Černý, Olaitan, Vlahović). Emin olamadığın kelimeyi o aralığı farklı pencerelerle (±1 sn) yeniden çözerek kontrol et; yine çözülmezse o kısmı altyazıdan çıkar (aralık boş kalır), tahmin yazma.
  - Konuşma yabancı dildeyse ve klipte Türkçe çeviri sesi yoksa: altyazıya kendi çevirini koyma; sayfa sahibine Türkçe çevirisi olan klip iste ya da Türkçe basında yayımlanmış tam metni (SON DAKİKA B'deki kaynak kurallarıyla) kullanıp zamanlamayı ona göre yap.
  - Küfür/hakaret/suç itham eden söz varsa o kısmı videodan kes (bas/son ya da ayrı klip) — altyazıyı silmek yetmez, ses de duyulur.
  - Her ifadenin `a`/`b` zamanı, yazi.py'nin verdiği aralıktır; birleştirdiğin/böldüğün ifadelerde sessizlik sınırlarını kullan.

## ADIM 3 — ~/demec/senaryo.json
Örnek: motor/ornekler/demec_italiano.json. Alanlar:
- `slug`: `TARIH-<soyad>-<ev>-<dep>`; `video`: "kaynak.mp4"; `bas`, `son` (kaynak saniyesi).
- `kirp`: [x, y, w, h] — kaynakta pencereye girecek bölge; oran ≈ 1020:1060. Yüz pencerenin üst-orta kısmında, ağız/göğüs altyazı bandının (pencerenin alt %30'u) üstünde kalsın. 1080×1920 kaynakta genelde [0, 70, 1080, 1123].
- `ust`: "MAÇ SONU KONUŞTU" (flaş röportajsa da aynı).
- `kim`: "<SOYAD ya da bilinen ad> · <EV> <SKOR> <DEP>" (ör. "ITALIANO · BEŞİKTAŞ 2-2 CRYSTAL PALACE").
- `soz`: klipte birebir geçen en çarpıcı kısa söz, tırnaklı (≤ 26 karakter; ör. "“ÇOK KOLAY GOLLER YİYORUZ”"). Bağlamından koparıp anlamını değiştirecek söz seçme.
- `kredi`: "Görüntü: <kaynak>" — videonun geldiği hesap/yayıncı HER ZAMAN yazılır (ör. "Görüntü: TikTok @futbolarena"). Filigranı silmeye/gizlemeye çalışma.
- `soru`: kapanıştaki soru (≤ 44 karakter; ör. "Sence bu bir puan yeterli mi?").
- `kapak_sn`: kişinin kameraya baktığı bir an (≈ 2–4).
- `ifadeler`: ADIM 2'deki liste.

## ADIM 4 — Önizleme ve kontrol
`cd ~/demec && python3 ~/ilk11-medya/motor/demec_reels.py senaryo.json cikti --onizleme` (≈ 10 sn). cikti/onizleme.jpg ve cikti/onizleme_tam.jpg'yi Read ile aç: başlık taşmıyor mu, yüz pencerede mi, altyazı okunuyor mu, skor/isim doğru mu. `onizleme_sn` ile farklı anlara bak. Gerekirse düzeltip tekrarla.

## ADIM 5 — Video
`cd ~/demec && python3 ~/ilk11-medya/motor/demec_reels.py senaryo.json cikti` (≈ 3–4 dk; timeout 900000). Çıktılar: cikti/<slug>.mp4, cikti/kapak_temiz.jpg (altyazısız kapak). Kontrol: süre (= son − bas + ~4,5 sn kapanış), son 2 sn'de kaynak kapanış kartı GÖRÜNMEMELİ, 6–8 kare çıkarıp altyazının konuşmayla eşleştiğine bak, `ebur128` ile ≈ −14 LUFS.

## ADIM 6 — Paylaşım
Açıklama metni:
```
🎙️ MAÇ SONU KONUŞTU | <EV> – <DEP>

<Kim, rol>: "<klipteki en önemli 2–4 cümle, birebir; aralar … ile>"

<Soru> Yorumlara yaz 👇

🎥 Görüntü: <kaynak>

Daha fazlası için @ilk.onbir11'i takip et ⚽

#<takım> #<turnuva> #<kişi> #ilk11 #futbol
```
- **MANUEL MOD** (motor/MANUEL_MOD varsa): Metricool'a gönderme. SendUserFile ile mp4 + kapak_temiz.jpg; SendUserMessage ile ilk satırı "📲 ELLE PAYLAŞ · Instagram Reels · şimdi" olan mesaj, açıklama tek kod bloğunda, "Kapak: kapak_temiz.jpg (ya da videonun <kapak_sn>. saniyesi)" ve doğrulama kaynakları.
- **Normal akış**: hikaye_reels.md ADIM 8'deki gibi videoyu `medya-demec-<slug>` yetim dalına yükle (SHA'lı raw bağlantı, 200 kontrolü), sonra createScheduledPost: blogId "7504196", tarih şimdi + 10 dk, instagramData {"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}, videoCoverMilliseconds = (kapak_sn − bas) × 1000, autoPublish true; diğer alanlar hikaye_reels.md ADIM 9 ile aynı. Ardından SendUserMessage ile kısa bildirim.

## ADIM 7 — Kayıt
`cd ~/ilk11-medya && git pull --rebase -q`, motor/paylasilan.txt'ye `YYYY-AA-GG SS:DD demec <TARIH-ev-dep-sonra-takım-N> | <Kişi> maç sonu (Reels)` (manuel moddaysa sonuna ` (manuel)`) ekle, commit ve push. Aynı maç için daha önce "demecvideo" satırı varsa o haber kapanmış sayılır.

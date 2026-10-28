// İLK 11 · KARAKTERLİ ÇİZGİ FİLM sahneleri (2026-10-28'den itibaren Reels'in varsayılan stili).
// hikaye.py her c* sahnesi için <g class="cizgi" data-p="{...}"> yer tutucusu üretir; oynat.js her karede
// CIZGI.draw(p, t, d, i) çağırır (t: sahne içi saniye, d: sahne süresi, i: sahne sırası). Tüm "at" değerleri
// Python'da sahne içi saniyeye çevrilmiş gelir. Ekran bantları: 204–400 rozet/etiket/soru, 1170–1500 altyazı.
const CIZGI = (() => {
  const LIME = '#C6FF00', INK = '#0A0F0A', RED = '#E30A17', WHITE = '#FFFFFF', SKIN0 = '#F3B78F';
  const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const seg = (t, a, b) => cl((t - a) / (b - a));
  const eo = x => 1 - Math.pow(1 - cl(x), 3);
  const eio = x => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const back = (x, s = 1.70158) => { x = cl(x); return 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); };
  const elastic = x => { x = cl(x); if (x === 0 || x === 1) return x; return Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * 2 * Math.PI / 3) + 1; };
  const pop = (t, a, d = .42, s = 2.4) => (t < a ? 0 : back(seg(t, a, a + d), s));
  const f1 = n => (+n).toFixed(1);
  const rad = d => d * Math.PI / 180;
  const tr = (x, y, s = 1, r = 0) => `translate(${f1(x)} ${f1(y)}) rotate(${(+r).toFixed(2)}) scale(${(+s).toFixed(3)})`;
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  function R(seed) { let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function shakeAt(t, times, amp = 20, dur = .4) {
    let dx = 0, dy = 0;
    for (const a of times) { if (a == null) continue; const k = seg(t, a, a + dur); if (t >= a && k < 1) { const e = Math.pow(1 - k, 2) * amp; dx += Math.sin(t * 97 + a) * e; dy += Math.cos(t * 83 + a) * e * .8; } }
    return [dx, dy];
  }
  let UID = 0, PFX = 'cz';
  const uid = () => `${PFX}_${UID++}`;

  // ------------------------------------------------------------ forma / karakter tanımı
  const TEN = { acik: '#F3B78F', bugday: '#D99A6C', esmer: '#A8693F', koyu: '#6B4226' };
  const SAC = { siyah: '#1E140C', kahve: '#3A2A1E', sari: '#D9B25B', kizil: '#B5532A', gri: '#9DA3A6', beyaz: '#E8E8E8', yok: 'yok' };
  const TAKIM = {
    tr: { forma: RED, sort: WHITE, corap: RED },
    gs: { forma: '#FDB912', forma2: '#A90432', desen: 'parcali', sort: '#A90432', corap: '#A90432' },
    fb: { forma: '#FFED00', forma2: '#002D72', desen: 'cubuk', sort: WHITE, corap: WHITE },
    bjk: { forma: WHITE, sort: '#111111', corap: '#111111' },
    ts: { forma: '#7A1C3E', forma2: '#5FA8E0', desen: 'cubuk', sort: '#7A1C3E', corap: '#7A1C3E' },
    kaleci: { forma: LIME, sort: INK, corap: LIME, eldiven: WHITE },
    kirmizi: { forma: RED, sort: RED, corap: RED }, beyaz: { forma: '#F4F4F4', sort: '#F4F4F4', corap: '#F4F4F4' },
    siyah: { forma: '#1A1A1A', sort: '#1A1A1A', corap: '#1A1A1A' }, mavi: { forma: '#1D5BD8', sort: WHITE, corap: '#1D5BD8' },
    sari: { forma: '#FFD100', sort: '#1A1A1A', corap: '#FFD100' }, lacivert: { forma: '#14213D', sort: '#14213D', corap: '#14213D' },
  };
  const lum = h => { const m = /^#?([0-9a-f]{6})$/i.exec(h || ''); if (!m) return .5; const n = parseInt(m[1], 16); return (.299 * (n >> 16 & 255) + .587 * (n >> 8 & 255) + .114 * (n & 255)) / 255; };
  function kit(o, def = 'kirmizi') {
    o = o || {}; const base = Object.assign({}, TAKIM[o.takim || def] || TAKIM.kirmizi);
    for (const k of ['forma', 'forma2', 'desen', 'sort', 'corap', 'eldiven']) if (o[k] != null) base[k] = o[k];
    if (typeof base.forma === 'string' && base.forma.includes(',')) { const [a, b] = base.forma.split(','); base.forma = a.trim(); base.forma2 = base.forma2 || b.trim(); base.desen = base.desen || 'cubuk'; }
    const sac = o.sac == null ? '#3A2A1E' : (SAC[o.sac] || o.sac), ten = o.ten == null ? SKIN0 : (TEN[o.ten] || o.ten);
    return { shirt: base.forma, shirt2: base.forma2 || null, desen: base.desen || null, shorts: base.sort || base.forma, socks: base.corap || base.forma,
      glove: base.eldiven || WHITE, boot: INK, num: o.no != null ? String(o.no) : '', numc: lum(base.forma) > .62 ? INK : WHITE, hair: sac, skin: ten,
      ad: o.ad || '', sakal: !!o.sakal };
  }
  const IFADE = { uzgun: 'sad', kararli: 'focus', bagir: 'shout', mutlu: 'happy', saskin: 'surprised', sad: 'sad', focus: 'focus', shout: 'shout', happy: 'happy', surprised: 'surprised' };
  const ifade = s => IFADE[s] || 'focus';

  // ------------------------------------------------------------ kalem (kalın kontürlü çizgi film)
  const OLW = 7;
  const P = {
    limb: (x1, y1, x2, y2, w, c) => `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${INK}" stroke-width="${w + 2 * OLW}" stroke-linecap="round"/>` +
      `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`,
    circle: (cx, cy, r, c) => `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="${c}" stroke="${INK}" stroke-width="${OLW}"/>`,
    path: (d, c) => `<path d="${d}" fill="${c}" stroke="${INK}" stroke-width="${OLW}" stroke-linejoin="round"/>`,
  };
  // gövde: düz, çubuklu ya da parçalı forma
  function torso(d, k) {
    if (!k.shirt2 || !k.desen) return P.path(d, k.shirt);
    const id = uid(); let pat = '';
    if (k.desen === 'parcali') pat = `<rect x="0" y="-600" width="300" height="1200" fill="${k.shirt2}"/>`;
    else for (let x = -120; x < 140; x += 36) pat += `<rect x="${x}" y="-600" width="16" height="1200" fill="${k.shirt2}"/>`;
    return `<defs><clipPath id="${id}"><path d="${d}"/></clipPath></defs><path d="${d}" fill="${k.shirt}"/><g clip-path="url(#${id})">${pat}</g>` +
      `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${OLW}" stroke-linejoin="round"/>`;
  }
  function legPts(hip, a, b, L1, L2) {
    const kn = [hip[0] + Math.sin(a) * L1, hip[1] + Math.cos(a) * L1];
    return [kn, [kn[0] + Math.sin(a - b) * L2, kn[1] + Math.cos(a - b) * L2]];
  }
  // Oyuncu (yan görünüş, sağa bakar, orijin ayak hizası). k: vuruş evresi; o.poz: 'dur' | 'yumruk' | 'kos' | 'sut'
  function player(k, K, o = {}) {
    const hr = o.head || 78, L1 = 48, L2 = 46, tor = 92, tw = 88;
    const hip = [0, -(L1 + L2)], sh = [8, hip[1] - tor];
    let aK, bK, aS, bS, armF, armB;
    const poz = o.poz || 'sut';
    if (poz === 'dur' || poz === 'yumruk') {
      aK = rad(9); bK = rad(4); aS = rad(-9); bS = rad(4); armF = rad(14); armB = rad(-8);
      if (poz === 'yumruk') armF = rad(150 + 8 * Math.sin((o.t || 0) * 9));
    } else if (poz === 'kos') {
      const p = (o.t || 0) * 2 * Math.PI * 2.2;
      aK = rad(38 * Math.sin(p)); bK = rad(35 + 30 * Math.max(0, -Math.cos(p))); aS = rad(-38 * Math.sin(p)); bS = rad(35 + 30 * Math.max(0, Math.cos(p)));
      armF = rad(-40 * Math.sin(p)); armB = rad(40 * Math.sin(p));
    } else {
      aK = rad(k < .5 ? lerp(-60, 10, eio(k * 2)) : lerp(10, 85, eo((k - .5) * 2)));
      bK = rad(k < .5 ? lerp(100, 25, k * 2) : lerp(25, 5, (k - .5) * 2));
      aS = rad(-6); bS = rad(14); armF = rad(lerp(-30, 60, k)); armB = rad(lerp(60, -50, k));
    }
    const [kS, fS] = legPts(hip, aS, bS, L1, L2), [kK, fK] = legPts(hip, aK, bK, L1, L2);
    const arm = a => { const el = [sh[0] + Math.sin(a) * 50, sh[1] + 12 + Math.cos(a) * 50], h = [el[0] + Math.sin(a - rad(50)) * 46, el[1] + Math.cos(a - rad(50)) * 46];
      return P.limb(sh[0], sh[1] + 12, el[0], el[1], 30, K.shirt) + P.limb(el[0], el[1], h[0], h[1], 22, K.skin); };
    const leg = (kk, ff) => P.limb(hip[0], hip[1], kk[0], kk[1], 36, K.shorts) + P.limb(kk[0], kk[1], ff[0], ff[1], 28, K.socks) +
      P.path(`M${f1(ff[0] - 10)} ${f1(ff[1] - 10)} h40 a12 12 0 0 1 0 22 h-46 z`, K.boot);
    let s = arm(armB) + leg(kS, fS);
    s += torso(`M${f1(-tw / 2)} ${f1(hip[1] + 12)} L${f1(-tw / 2 + 4)} ${f1(sh[1] + 10)} Q${f1(sh[0])} ${f1(sh[1] - 18)} ${f1(tw / 2 + 4)} ${f1(sh[1] + 10)} L${f1(tw / 2)} ${f1(hip[1] + 12)} Z`, K);
    if (K.num && !o.mirror) s += `<text x="${f1(sh[0] - 2)}" y="${f1(hip[1] - tor * .38)}" text-anchor="middle" font-family="Anton" font-size="40" fill="${K.numc}" stroke="${K.numc === WHITE ? INK : WHITE}" stroke-width="3" paint-order="stroke">${esc(K.num)}</text>`;
    s += leg(kK, fK) + arm(armF);
    return s + head(sh[0] + 6, sh[1] - hr + 6, hr, K, o.face || 'focus');
  }
  // Kafa + yüz ifadesi: sad · focus · shout · happy · surprised
  function head(x, y, r, K, face) {
    let s = P.circle(x - r * .02, y + r * .1, r * .2, K.skin) + P.circle(x, y, r, K.skin); // kulak + kafa
    if (K.hair !== 'yok') s += P.path(`M${f1(x - r * .98)} ${f1(y - r * .05)} C${f1(x - r)} ${f1(y - r * 1.25)} ${f1(x + r)} ${f1(y - r * 1.25)} ${f1(x + r * .98)} ${f1(y - r * .2)} C${f1(x + r * .5)} ${f1(y - r * .55)} ${f1(x - r * .3)} ${f1(y - r * .5)} ${f1(x - r * .98)} ${f1(y - r * .05)}Z`, K.hair);
    if (K.sakal) s += `<path d="M${f1(x - r * .1)} ${f1(y + r * .55)} Q${f1(x + r * .4)} ${f1(y + r * 1.02)} ${f1(x + r * .85)} ${f1(y + r * .45)} Q${f1(x + r * .4)} ${f1(y + r * .75)} ${f1(x - r * .1)} ${f1(y + r * .55)}Z" fill="${K.hair === 'yok' ? '#3A2A1E' : K.hair}" opacity=".85"/>`;
    const ex = [x + r * .12, x + r * .58], ey = y + r * .12, er = r * .2;
    for (const e of ex) {
      if (face === 'happy') s += `<path d="M${f1(e - er)} ${f1(ey + 2)} Q${f1(e)} ${f1(ey - er * 1.3)} ${f1(e + er)} ${f1(ey + 2)}" stroke="${INK}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
      else { const big = face === 'surprised' ? 1.25 : 1; s += `<ellipse cx="${f1(e)}" cy="${f1(ey)}" rx="${f1(er * .82 * big)}" ry="${f1(er * big)}" fill="#fff" stroke="${INK}" stroke-width="4"/>`;
        const py = face === 'sad' ? ey + er * .35 : ey, pr = face === 'surprised' ? .38 : .5; s += `<circle cx="${f1(e + er * .25)}" cy="${f1(py)}" r="${f1(er * pr)}" fill="${INK}"/><circle cx="${f1(e + er * .38)}" cy="${f1(py - er * .25)}" r="${f1(er * .17)}" fill="#fff"/>`; }
    }
    const bw = 10;
    if (face === 'sad') s += `<path d="M${f1(ex[0] - er)} ${f1(ey - er * 1.3)} L${f1(ex[0] + er)} ${f1(ey - er * 1.9)} M${f1(ex[1] - er)} ${f1(ey - er * 1.9)} L${f1(ex[1] + er)} ${f1(ey - er * 1.3)}" stroke="${INK}" stroke-width="${bw}" stroke-linecap="round"/>`;
    else if (face === 'focus' || face === 'shout') s += `<path d="M${f1(ex[0] - er)} ${f1(ey - er * 1.9)} L${f1(ex[0] + er)} ${f1(ey - er * 1.2)} M${f1(ex[1] - er)} ${f1(ey - er * 1.2)} L${f1(ex[1] + er)} ${f1(ey - er * 1.9)}" stroke="${INK}" stroke-width="${bw}" stroke-linecap="round"/>`;
    else if (face === 'surprised') s += `<path d="M${f1(ex[0] - er)} ${f1(ey - er * 2.1)} Q${f1(ex[0])} ${f1(ey - er * 2.6)} ${f1(ex[0] + er)} ${f1(ey - er * 2.1)} M${f1(ex[1] - er)} ${f1(ey - er * 2.1)} Q${f1(ex[1])} ${f1(ey - er * 2.6)} ${f1(ex[1] + er)} ${f1(ey - er * 2.1)}" stroke="${INK}" stroke-width="${bw - 2}" fill="none" stroke-linecap="round"/>`;
    const mx = x + r * .38, my = y + r * .58;
    if (face === 'sad') s += `<path d="M${f1(mx - r * .2)} ${f1(my + r * .06)} Q${f1(mx)} ${f1(my - r * .14)} ${f1(mx + r * .2)} ${f1(my + r * .06)}" stroke="${INK}" stroke-width="7" fill="none" stroke-linecap="round"/>` +
      `<path d="M${f1(ex[1] + er * .2)} ${f1(ey + er * 1.1)} q-9 18 0 26 q9 -8 0 -26z" fill="#7FD3FF"/>`;
    else if (face === 'focus') s += `<path d="M${f1(mx - r * .2)} ${f1(my)} L${f1(mx + r * .18)} ${f1(my - r * .04)}" stroke="${INK}" stroke-width="8" stroke-linecap="round"/>`;
    else if (face === 'shout' || face === 'surprised') s += `<ellipse cx="${f1(mx)}" cy="${f1(my)}" rx="${f1(r * (face === 'shout' ? .2 : .13))}" ry="${f1(r * (face === 'shout' ? .24 : .17))}" fill="#7A2E22" stroke="${INK}" stroke-width="5"/>`;
    else if (face === 'happy') s += `<path d="M${f1(mx - r * .26)} ${f1(my - r * .06)} Q${f1(mx)} ${f1(my + r * .34)} ${f1(mx + r * .26)} ${f1(my - r * .06)}Z" fill="#7A2E22" stroke="${INK}" stroke-width="5"/>` +
      `<ellipse cx="${f1(x + r * .02)}" cy="${f1(y + r * .42)}" rx="${f1(r * .14)}" ry="${f1(r * .08)}" fill="#E8745E" opacity=".55"/>`;
    return s;
  }
  // Kaleci (dik çizilir; dalış için döndürülür) — kollar yukarıda, iri eldivenler. Eldiven merkezi ≈ (±73, −314)
  function keeper(K, o = {}) {
    const hr = o.head || 76, L = 94, tor = 92, tw = 88, hip = [0, -L], sh = [0, -L - tor];
    const leg = dx => P.limb(dx * .3, hip[1], dx, hip[1] + L * .5, 36, K.shorts) + P.limb(dx, hip[1] + L * .5, dx * 1.4, 0, 28, K.socks);
    const arm = dx => P.limb(dx * .4, sh[1] + 14, dx, sh[1] - 50, 30, K.shirt) + P.limb(dx, sh[1] - 50, dx * 1.15, sh[1] - 110, 24, K.shirt) + P.circle(dx * 1.18, sh[1] - 128, 34, K.glove);
    let s = leg(-34) + leg(34) + arm(-62);
    s += torso(`M${-tw / 2} ${hip[1] + 12} L${-tw / 2 + 4} ${sh[1] + 10} Q0 ${sh[1] - 18} ${tw / 2 + 4} ${sh[1] + 10} L${tw / 2} ${hip[1] + 12} Z`, K);
    if (K.num) s += `<text x="0" y="${f1(hip[1] - tor * .38)}" text-anchor="middle" font-family="Anton" font-size="40" fill="${K.numc}">${esc(K.num)}</text>`;
    return s + arm(62) + head(0, sh[1] - hr + 8, hr, K, o.face || 'focus');
  }
  function ballG(r, rot = 0) {
    const k = r / 46, pts = [];
    for (let i = 0; i < 5; i++) { const a = rad(-90 + i * 72); pts.push(`${f1(Math.cos(a) * 16 * k)},${f1(Math.sin(a) * 16 * k)}`); }
    let s = `<g transform="rotate(${f1(rot)})">${P.circle(0, 0, r, WHITE)}<polygon points="${pts.join(' ')}" fill="${INK}"/>`;
    for (let i = 0; i < 5; i++) { const a = rad(-90 + i * 72); s += `<line x1="${f1(Math.cos(a) * 16 * k)}" y1="${f1(Math.sin(a) * 16 * k)}" x2="${f1(Math.cos(a) * r * .92)}" y2="${f1(Math.sin(a) * r * .92)}" stroke="${INK}" stroke-width="${f1(3.5 * k)}"/><circle cx="${f1(Math.cos(a) * r * .98)}" cy="${f1(Math.sin(a) * r * .98)}" r="${f1(10 * k)}" fill="${INK}"/>`; }
    return s + '</g>';
  }
  function goalNet(x0, y0, x1, y1, bx, by, bulge, o = {}) {
    const nc = o.net || 'rgba(255,255,255,.55)', step = o.step || 34, pw = o.pw || 16;
    const def = (x, y) => { const dx = x - bx, dy = y - by, d = Math.hypot(dx, dy) + 1e-3, f = bulge * 60 * Math.exp(-d * d / 9000); return [x - dx / d * f * .35, y - dy / d * f * .35 - f * .15]; };
    let s = '';
    for (let x = x0 + step; x < x1; x += step) { let d = ''; for (let y = y0; y <= y1; y += 12) { const p = def(x, y); d += (d ? 'L' : 'M') + f1(p[0]) + ' ' + f1(p[1]); } s += `<path d="${d}" stroke="${nc}" stroke-width="3" fill="none"/>`; }
    for (let y = y0 + step; y < y1; y += step) { let d = ''; for (let x = x0; x <= x1; x += 12) { const p = def(x, y); d += (d ? 'L' : 'M') + f1(p[0]) + ' ' + f1(p[1]); } s += `<path d="${d}" stroke="${nc}" stroke-width="3" fill="none"/>`; }
    return s + `<path d="M${x0} ${y1} L${x0} ${y0} L${x1} ${y0} L${x1} ${y1}" stroke="${INK}" stroke-width="${pw + 12}" fill="none" stroke-linejoin="round"/>` +
      `<path d="M${x0} ${y1} L${x0} ${y0} L${x1} ${y0} L${x1} ${y1}" stroke="#fff" stroke-width="${pw}" fill="none" stroke-linejoin="round"/>`;
  }
  // Kupa (orijin taban ortası, yükseklik ≈ 420). tip: kulakli (Şampiyonlar Ligi) | klasik
  function trophy(tip = 'kulakli') {
    const c = '#DDE3E8', c2 = '#AEB8C0';
    const ear = sx => tip === 'kulakli' ? P.path(`M${sx * 70} -330 C${sx * 210} -400 ${sx * 230} -200 ${sx * 80} -200 L${sx * 80} -232 C${sx * 180} -238 ${sx * 168} -350 ${sx * 72} -296 Z`, c2)
      : P.path(`M${sx * 100} -330 C${sx * 170} -330 ${sx * 170} -250 ${sx * 96} -240 L${sx * 92} -262 C${sx * 140} -268 ${sx * 140} -310 ${sx * 102} -308 Z`, '#E9C46A');
    const body = tip === 'kulakli' ? c : '#F2C94C', base = tip === 'kulakli' ? c2 : '#C89B2C';
    return ear(-1) + ear(1) + P.path(`M-60 0 L60 0 L48 -46 L-48 -46 Z`, base) + P.path(`M-22 -46 L22 -46 L16 -150 L-16 -150 Z`, body) +
      P.path(`M-110 -360 C-110 -230 -70 -160 0 -150 C70 -160 110 -230 110 -360 Z`, body) +
      `<path d="M-74 -345 C-74 -260 -50 -205 -24 -186" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/>`;
  }
  function burstPts(r1, r2, n, seed, rot = 0) {
    const rr = R(seed), p = [];
    for (let i = 0; i < n * 2; i++) { const a = rad(rot + i * 180 / n), r = i % 2 ? r2 * (.85 + rr() * .3) : r1 * (.9 + rr() * .2); p.push(f1(Math.cos(a) * r) + ',' + f1(Math.sin(a) * r)); }
    return p.join(' ');
  }
  function jersey(x, y, s, K) { // küçük forma ikonu (tabela)
    const d = 'M-60 -50 L-25 -62 Q0 -48 25 -62 L60 -50 L78 -10 L52 0 L48 62 L-48 62 L-52 0 L-78 -10 Z';
    return `<g transform="${tr(x, y, s)}">${torso(d, K)}</g>`;
  }

  // ------------------------------------------------------------ dekor
  const DEFS = () => `<defs><linearGradient id="${PFX}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050806"/><stop offset="1" stop-color="#14231A"/></linearGradient>
<radialGradient id="${PFX}lamp"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".4" stop-color="${LIME}" stop-opacity=".35"/><stop offset="1" stop-color="${LIME}" stop-opacity="0"/></radialGradient>
<linearGradient id="${PFX}beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="${PFX}grass" width="200" height="200" patternUnits="userSpaceOnUse"><rect width="100" height="200" fill="#1A3A16"/><rect x="100" width="100" height="200" fill="#163212"/></pattern></defs>`;
  // Stadyum: gece göğü, ışık kuleleri, coşabilen tribün, İLK 11 reklam panosu, çim. jump 0..1 tribün coşkusu
  function stadium(t, jump = 0, cols) {
    let s = `<rect x="-400" y="-400" width="1880" height="2720" fill="url(#${PFX}sky)"/>`;
    for (const x of [110, 970]) {
      s += `<polygon points="${x - 40},420 ${x + 40},420 ${x + (x < 540 ? 520 : -520)},1500 ${x + (x < 540 ? 120 : -120)},1500" fill="url(#${PFX}beam)"/>`;
      s += `<rect x="${x - 10}" y="420" width="20" height="300" fill="#1C241F"/><rect x="${x - 70}" y="380" width="140" height="62" rx="8" fill="#232B26" stroke="${INK}" stroke-width="5"/>`;
      for (let i = 0; i < 4; i++) s += `<circle cx="${x - 48 + i * 32}" cy="411" r="11" fill="#fff"/>`;
      s += `<circle cx="${x}" cy="411" r="150" fill="url(#${PFX}lamp)" opacity="${f1((.75 + .1 * Math.sin(t * 9 + x)) * 100) / 100}"/>`;
    }
    s += `<path d="M-300 640 Q540 560 1380 640 L1380 1000 L-300 1000 Z" fill="#101612"/><path d="M-300 850 Q540 810 1380 850 L1380 1000 L-300 1000Z" fill="#0C110E"/>`;
    const r = R(12), C = cols && cols.length ? cols : [RED, '#fff', LIME, RED, '#7A0A10', '#fff'];
    for (let row = 0; row < 8; row++) { const y0 = 680 + row * 38 + (row > 4 ? 18 : 0);
      for (let x = -290 + (row % 2) * 13; x < 1370; x += 27) { const c = C[Math.floor(r() * C.length)], ph = r() * 6.28, up = r() > .7, arm = r() > .86;
        const jy = -Math.abs(Math.sin(t * 11 + ph)) * 16 * jump - (jump > .3 && up ? 10 : 0);
        s += `<rect x="${x - 9}" y="${f1(y0 + jy + 6)}" width="18" height="18" rx="5" fill="${c}" opacity=".9"/><circle cx="${x}" cy="${f1(y0 + jy)}" r="9" fill="#E6B48E" opacity=".85"/>`;
        if (jump > .3 && arm) s += `<line x1="${x - 7}" y1="${f1(y0 + jy + 4)}" x2="${x - 16}" y2="${f1(y0 + jy - 20)}" stroke="#E6B48E" stroke-width="6" stroke-linecap="round"/>`; } }
    s += `<rect x="-300" y="990" width="1680" height="46" fill="${INK}"/><text x="540" y="1025" text-anchor="middle" font-family="Anton" font-size="34" letter-spacing="30" fill="${LIME}" opacity=".85">İLK 11 · İLK 11 · İLK 11</text>`;
    return s + `<rect x="-400" y="1036" width="1880" height="1300" fill="url(#${PFX}grass)"/><rect x="-400" y="1036" width="1880" height="8" fill="#fff" opacity=".6"/>` +
      `<g fill="none" stroke="#fff" stroke-width="8" opacity=".32"><path d="M-400 1620 H1480"/><ellipse cx="540" cy="1620" rx="340" ry="92"/><path d="M120 1036 L40 1250 H1040 L960 1036"/></g><circle cx="540" cy="1620" r="10" fill="#fff" opacity=".4"/>`;
  }
  const cam = (z, cx, cy, inner) => `<g transform="translate(540 960) scale(${z.toFixed(4)}) translate(${f1(-cx)} ${f1(-cy)})">${inner}</g>`;
  // *vurgu*'lu, harf harf zıplayan, genişliğe sığdırılan başlık
  const CW = c => (/[İI1!'.,·:;|]/.test(c) ? .3 : c === ' ' ? .28 : /[MWĞÖÜ]/.test(c) ? .6 : /[0-9]/.test(c) ? .5 : .5);
  function bounce(txt, x, y, size, a, t, o = {}) {
    const ch = [], hl = []; let on = false;
    for (const c of String(txt || '')) { if (c === '*') { on = !on; continue; } ch.push(c); hl.push(on); }
    if (!ch.length) return '';
    const wOf = sz => ch.reduce((p, c) => p + CW(c) * sz, 0) + (ch.length - 1) * 3;
    const maxw = o.maxw || 980; if (wOf(size) > maxw) size = size * maxw / wOf(size);
    let cx = x - wOf(size) / 2, s = '';
    ch.forEach((c, i) => { const w = CW(c) * size; if (c !== ' ') { const k = pop(t, a + i * (o.step || .025), .38, 2.6), wob = Math.sin(t * 6 + i) * size * .025;
        if (k > 0) s += `<g transform="${tr(cx + w / 2, y + wob, k, Math.sin(i * 1.7) * 3)}"><text x="0" y="0" text-anchor="middle" font-family="Anton" font-size="${f1(size)}" fill="${hl[i] ? LIME : (o.col || '#fff')}" stroke="${INK}" stroke-width="${f1(size * .18)}" stroke-linejoin="round" paint-order="stroke">${esc(c)}</text></g>`; }
      cx += w + 3; });
    return s;
  }
  function wrap(txt, max) { const w = String(txt).split(/\s+/), out = []; let l = '';
    for (const x of w) { if ((l + ' ' + x).trim().length > max && l) { out.push(l); l = x; } else l = (l + ' ' + x).trim(); } if (l) out.push(l); return out; }
  function bubble(x, y, txt, k, tail, o = {}) {
    if (k <= 0 || !txt) return ''; const lines = wrap(String(txt).toLocaleUpperCase('tr-TR'), o.max || 14), size = o.size || 58;
    const w = Math.max(...lines.map(l => l.length)) * size * .5 + size * 1.4, h = lines.length * size * 1.08 + size * .9;
    let tx = ''; lines.forEach((l, i) => { tx += `<text x="0" y="${f1(size * .36 + (i - (lines.length - 1) / 2) * size * 1.06)}" text-anchor="middle" font-family="Anton" font-size="${size}" fill="${INK}">${esc(l)}</text>`; });
    const [tx0, ty0] = tail || [-w * .3, h * .9];
    return `<g transform="${tr(x, y, k)}"><path d="M${f1(tx0)} ${f1(ty0)} L${f1(-w * .14)} ${f1(h * .3)} L${f1(w * .08)} ${f1(h * .38)} Z" fill="#fff" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/>` +
      `<rect x="${f1(-w / 2)}" y="${f1(-h / 2)}" width="${f1(w)}" height="${f1(h)}" rx="${f1(Math.min(h / 2.2, 60))}" fill="#fff" stroke="${INK}" stroke-width="8"/>` +
      `<path d="M${f1(-w * .14 + 9)} ${f1(h * .3 - 6)} L${f1(w * .08 - 7)} ${f1(h * .38 - 10)}" stroke="#fff" stroke-width="16"/>${tx}</g>`;
  }
  function pill(x, y, txt, k, o = {}) {
    if (k <= 0 || !txt) return ''; const size = o.size || 52, w = Math.min(o.maxw || 980, [...String(txt)].length * size * .5 + size * 1.6), h = size * 1.55;
    const fs = Math.min(size, (w - size * 1.2) / Math.max(1, [...String(txt)].length * .5));
    return `<g transform="${tr(x, y, k, o.rot || 0)}"><rect x="${f1(-w / 2)}" y="${f1(-h / 2)}" width="${f1(w)}" height="${f1(h)}" rx="${f1(h / 2)}" fill="${o.bg || LIME}" stroke="${INK}" stroke-width="7"/>` +
      `<text x="0" y="${f1(fs * .36)}" text-anchor="middle" font-family="Anton" font-size="${f1(fs)}" letter-spacing="2" fill="${o.fg || INK}">${esc(txt)}</text></g>`;
  }
  function stamp(x, y, txt, k, o = {}) { // damga: eğik, kalın çerçeveli
    if (k <= 0 || !txt) return ''; const size = o.size || 76, w = [...String(txt)].length * size * .52 + 70, c = o.renk || RED;
    const sc = lerp(2.2, 1, eo(Math.min(1, k)));
    return `<g transform="${tr(x, y, sc, o.rot == null ? -8 : o.rot)}" opacity="${f1(Math.min(1, k * 2) * 100) / 100}"><rect x="${f1(-w / 2)}" y="${f1(-size * .78)}" width="${f1(w)}" height="${f1(size * 1.56)}" rx="12" fill="${INK}" fill-opacity=".72" stroke="${c}" stroke-width="10"/>` +
      `<text y="${f1(size * .36)}" text-anchor="middle" font-family="Anton" font-size="${size}" letter-spacing="4" fill="${c === RED ? '#fff' : c}">${esc(txt)}</text></g>`;
  }
  function scorebug(sk, t, y = 650) { // TV skor bandı: {sol, sag, deger} ya da {once, sonra, at}
    if (!sk) return ''; const v = sk.sonra != null && t >= (sk.at || 0) + .1 ? sk.sonra : (sk.deger != null ? sk.deger : (sk.once || '0-0'));
    const flip = sk.sonra != null && t >= (sk.at || 0) + .1 ? pop(t, (sk.at || 0) + .1, .35, 3) : 1;
    const [a, b] = String(v).split('-');
    return `<g transform="translate(540 ${y})"><rect x="-230" y="-36" width="460" height="72" rx="14" fill="${INK}" stroke="${LIME}" stroke-width="5"/>` +
      `<text x="-135" y="16" text-anchor="middle" font-family="Anton" font-size="44" letter-spacing="2" fill="#fff">${esc(sk.sol || '')}</text>` +
      `<g transform="translate(0 0) scale(${f1(flip * 100) / 100})"><text x="0" y="18" text-anchor="middle" font-family="Anton" font-size="52" fill="${LIME}">${esc(a || '')} - ${esc(b || '')}</text></g>` +
      `<text x="135" y="16" text-anchor="middle" font-family="Anton" font-size="44" letter-spacing="2" fill="#fff">${esc(sk.sag || '')}</text>` +
      (sk.etiket ? `<rect x="236" y="-26" width="${[...sk.etiket].length * 22 + 30}" height="52" rx="9" fill="${RED}"/><text x="${251 + [...sk.etiket].length * 11}" y="14" text-anchor="middle" font-family="Anton" font-size="36" fill="#fff">${esc(sk.etiket)}</text>` : '') + `</g>`;
  }
  function stars(cx, cy, r, t, k) { if (k <= 0) return ''; let s = ''; for (let i = 0; i < 5; i++) { const a = t * 4 + i * 1.256, x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r * .35;
    s += `<path d="M${f1(x)} ${f1(y - 22)} L${f1(x + 7)} ${f1(y - 7)} L${f1(x + 22)} ${f1(y)} L${f1(x + 7)} ${f1(y + 7)} L${f1(x)} ${f1(y + 22)} L${f1(x - 7)} ${f1(y + 7)} L${f1(x - 22)} ${f1(y)} L${f1(x - 7)} ${f1(y - 7)}Z" fill="#FFD54A" stroke="${INK}" stroke-width="4" opacity="${f1(k * 100) / 100}"/>`; } return s; }
  function confetti(t, a, n, seed) {
    if (t < a) return ''; const r = R(seed); let s = ''; const C = [RED, '#fff', LIME, '#FFD54A'];
    for (let i = 0; i < n; i++) { const x0 = r() * 1080, v = 380 + r() * 420, d = r() * .5, sp = (r() - .5) * 900, w = 14 + r() * 14, h = 8 + r() * 8, tt = t - a - d; if (tt < 0) continue;
      const y = -40 + tt * v, x = x0 + 40 * Math.sin(tt * 2.2 + i); s += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="${C[i % 4]}" transform="rotate(${f1(sp * tt)} ${f1(x)} ${f1(y)})"/>`; }
    return s;
  }
  function fireworks(t, a) { let s = '';
    for (let k = 0; k < 3; k++) { const ft = a + .2 + k * .5, x = [250, 830, 540][k], y = [520, 490, 430][k], e = seg(t, ft, ft + 1);
      if (e > 0 && e < 1) for (let j = 0; j < 14; j++) { const an = j * .449, q = eo(e) * 150; s += `<circle cx="${f1(x + Math.cos(an) * q)}" cy="${f1(y + Math.sin(an) * q + e * e * 60)}" r="${f1(9 * (1 - e) + 2)}" fill="${[LIME, RED, '#FFD54A'][k]}"/>`; } }
    return s; }
  function effect(kind, x, y, t, k) { // kafa üstü efektleri
    if (!kind || k <= 0) return ''; let s = `<g opacity="${f1(k * 100) / 100}">`;
    if (kind === 'bulut') { const bx = x + Math.sin(t * 2) * 10; s += `<g transform="translate(${f1(bx)} ${f1(y)})"><path d="M-120 30 Q-150 -30 -80 -40 Q-60 -100 10 -80 Q60 -120 100 -60 Q160 -60 140 20 Z" fill="#3B4540" stroke="${INK}" stroke-width="7"/>`;
      for (let i = 0; i < 7; i++) { const yy = ((t * 900 + i * 47) % 150); s += `<line x1="${-100 + i * 32}" y1="${f1(40 + yy)}" x2="${-106 + i * 32}" y2="${f1(62 + yy)}" stroke="#7FD3FF" stroke-width="6" stroke-linecap="round"/>`; } s += '</g>'; }
    else if (kind === 'soru' || kind === 'unlem') { const g = kind === 'soru' ? '?' : '!'; for (let i = 0; i < 3; i++) { const b = Math.sin(t * 6 + i * 2) * 10;
      s += `<text x="${f1(x + 210 + i * 62)}" y="${f1(y + 150 - i * 70 + b)}" text-anchor="middle" font-family="Anton" font-size="${[90, 120, 100][i]}" fill="${i === 1 ? LIME : '#fff'}" stroke="${INK}" stroke-width="12" paint-order="stroke" transform="rotate(${12 + i * 4} ${f1(x + 210 + i * 62)} ${f1(y + 150 - i * 70)})">${g}</text>`; } }
    else if (kind === 'ter') { for (let i = 0; i < 3; i++) { const yy = ((t * 120 + i * 40) % 90); s += `<path d="M${x + 120 + i * 26} ${f1(y + 80 + yy)} q-12 22 0 32 q12 -10 0 -32z" fill="#7FD3FF" stroke="${INK}" stroke-width="4"/>`; } }
    else if (kind === 'yildiz') s += stars(x, y + 40, 130, t, 1);
    return s + '</g>';
  }

  // ------------------------------------------------------------ sahneler (p: parametreler, t: sahne içi sn, d: süre)
  const S = {};
  // KARAKTER / KANCA: tek karakter yakın plan, ifade değişimi, efekt, balon, damga, skor bandı
  S.ckarakter = (p, t, d) => {
    const K = kit(p.oyuncu), a2 = p.ifade2_at, ch = a2 != null && t >= a2;
    const face = ifade(ch ? (p.ifade2 || 'kararli') : (p.ifade || 'kararli')), poz = ch ? (p.poz2 || p.poz || 'dur') : (p.poz || 'dur');
    const happy = face === 'happy';
    let w = stadium(t, happy ? .6 : (ch ? .25 : 0), p.tribun);
    const sq = ch ? 1 + .12 * Math.sin((t - a2) * 20) * Math.exp(-(t - a2) * 5) : 1;
    w += `<ellipse cx="540" cy="1425" rx="230" ry="32" fill="#000" opacity=".35"/>`;
    w += `<g transform="translate(540 1420) scale(${f1(2 / sq * 100) / 100} ${f1(2 * sq * 100) / 100})">${player(0, K, { poz, face, t })}</g>`;
    const efBit = p.efekt_bitis_at != null ? p.efekt_bitis_at : ((p.efekt === 'bulut' || p.efekt2) && a2 != null ? a2 : 1e9);
    if (p.efekt && t < efBit) w += effect(p.efekt, 575, 690, t, Math.min(1, t / .25));
    else if (p.efekt === 'bulut' && t < efBit + .4) { const k = seg(t, efBit, efBit + .4); for (let i = 0; i < 6; i++) { const an = i * 1.05; w += `<circle cx="${f1(560 + Math.cos(an) * k * 220)}" cy="${f1(700 + Math.sin(an) * k * 120)}" r="${f1(40 * (1 - k))}" fill="#3B4540"/>`; } }
    if (p.efekt2 && ch) w += effect(p.efekt2, 575, 690, t, 1);
    const z = lerp(1.1, 1.02, eio(seg(t, 0, Math.max(1, d * .6)))) + (ch ? .05 * Math.exp(-(t - a2) * 4) : 0);
    let s = cam(z, 540, 1000, w);
    if (p.baslik) s += bounce(p.baslik, 540, 545, 104, .05, t, { step: .02 });
    if (p.ust) s += pill(540, p.baslik ? 640 : 560, p.ust, pop(t, .15, .35), { size: 44 });
    if (p.skor) s += scorebug(p.skor, t, p.ad || p.damga ? (p.baslik ? (p.ust ? 725 : 640) : 560) : 1110);
    if (p.balon) s += bubble(830, 730, p.balon.metin, pop(t, p.balon.at != null ? p.balon.at : .6, .4), [-200, 90]);
    if (p.ad) s += pill(540, 1110, p.ad, pop(t, p.ad_at != null ? p.ad_at : .3, .35), { size: 46, bg: INK, fg: LIME });
    if (p.damga) s += stamp(560, 1100, p.damga.metin, seg(t, p.damga.at, p.damga.at + .3), { renk: p.damga.renk });
    return s;
  };
  S.ckanca = S.ckarakter;
  // GOL: yandan şut → file sallanır, kaleci ters köşe, tribün coşar, skor bandı güncellenir
  S.cgol = (p, t, d) => {
    const g = p.at, A = kit(p.atan, 'kirmizi'), Kc = kit(p.kaleci, 'beyaz');
    const jump = t >= g ? Math.exp(-(t - g) * 1.4) : 0;
    let w = stadium(t, jump, p.tribun);
    const bulge = t >= g ? Math.exp(-(t - g) * 4) * Math.cos((t - g) * 18) : 0, imp = [960, p.yukseklik === 'alcak' ? 1250 : 1030];
    w += goalNet(740, 900, 1130, 1330, imp[0], imp[1], bulge, { pw: 16, net: 'rgba(255,255,255,.6)' });
    const dk = eo(seg(t, g - .3, g + .1)), kd = p.kaleci_yon === 'sag' ? 1 : -1;
    w += `<ellipse cx="930" cy="1335" rx="100" ry="16" fill="#000" opacity=".3"/>`;
    w += `<g transform="${tr(930 + kd * 60 * dk, 1330 - Math.sin(dk * Math.PI) * 50, .95, kd * 72 * dk)}">${keeper(Kc, { face: t > g ? 'sad' : 'focus' })}</g>`;
    const cele = t > g + .35, kk = seg(t, g - .85, g - .35);
    w += `<ellipse cx="280" cy="1335" rx="130" ry="20" fill="#000" opacity=".3"/>`;
    w += `<g transform="translate(280 ${f1(1330 - (cele ? Math.abs(Math.sin((t - g) * 8)) * 40 : 0))}) scale(1.6)">${player(kk, A, { poz: cele ? 'yumruk' : 'sut', face: t > g ? 'happy' : 'shout', t })}</g>`;
    const src = [385, 1312], pathAt = e => [lerp(src[0], imp[0], e), lerp(src[1], imp[1], e) - Math.sin(e * Math.PI) * (imp[1] < 1150 ? 170 : 60)];
    let bx, by, bs;
    if (t < g - .6) { [bx, by] = src; bs = 1; } else if (t < g) { const e = eo(seg(t, g - .6, g)); [bx, by] = pathAt(e); bs = lerp(1, .85, e); } else { bx = imp[0] + bulge * 14; by = imp[1]; bs = .85; }
    if (t > g - .6 && t < g) for (let j = 1; j < 5; j++) { const e = eo(seg(t - j * .03, g - .6, g)), q = pathAt(e); w += `<circle cx="${f1(q[0])}" cy="${f1(q[1])}" r="${30 - j * 5}" fill="#fff" opacity="${f1((.35 - j * .07) * 100) / 100}"/>`; }
    w += `<g transform="${tr(bx, by, bs)}">${ballG(34, t * 900)}</g>`;
    const z = t >= g ? 1.0 + .1 * Math.exp(-(t - g) * 3) : 1.0, [sx, sy] = shakeAt(t, [g], 18);
    let s = cam(z, 600 + sx, 1060 + sy, w);
    if (p.baslik) s += bounce(p.baslik, 540, 545, 100, .05, t, { step: .02 });
    const etiket = [p.dakika, A.ad].filter(Boolean).join('  ');
    let yy = p.baslik ? 640 : 560;
    if (p.skor) { s += scorebug(Object.assign({ at: g }, p.skor), t, yy); yy += 85; }
    if (etiket) s += pill(540, yy, etiket, pop(t, .1, .35), { size: 46 });
    if (t >= g) s += `<g transform="${tr(640, 1000, 1 + .04 * Math.sin(t * 20))}">${bounce(p.metin || 'GOL!', 0, 0, 210, g, t, { step: .05, col: LIME })}</g>`;
    return s;
  };
  // KURTARIŞ: önden kale, kaleci uçar, top eldivenden döner, yıldızlar
  S.ckurtaris = (p, t, d) => {
    const a = p.at, K = kit(p.kaleci, 'kaleci'), sv = t >= a, sgn = p.yon === 'sag' ? 1 : -1;
    let w = stadium(t, sv ? Math.exp(-(t - a) * 1.2) : 0, p.tribun);
    w += goalNet(140, 760, 940, 1330, 540 + sgn * 180, 960, sv ? Math.exp(-(t - a) * 6) * .2 : 0, { pw: 20, net: 'rgba(255,255,255,.45)' });
    const dk = eo(seg(t, a - .5, a + .04)), sway = t < a - .5 ? Math.sin(t * 7) * 16 : 0, hop = t < a - .5 ? -Math.abs(Math.sin(t * 7)) * 10 : 0;
    const kx = 540 - sgn * 20 * dk + sway, ky = lerp(1330, 1210, dk) - Math.sin(dk * Math.PI) * 70 + hop, kr = sgn * 62 * dk, sc = 1.45;
    w += `<ellipse cx="${f1(kx)}" cy="1335" rx="120" ry="20" fill="#000" opacity=".3"/>`;
    w += `<g transform="${tr(kx, ky, sc, kr)}">${keeper(K, { face: sv ? 'happy' : 'focus' })}</g>`;
    const gang = rad((sgn < 0 ? -100 : -80) + kr), glove = [kx + Math.cos(gang) * sc * 322, ky + Math.sin(gang) * sc * 322];
    let bx, by, bs;
    if (!sv) { const e = eo(seg(t, a - .5, a)); bx = lerp(540, glove[0], e); by = lerp(1900, glove[1], e); bs = lerp(2.4, 1, e); }
    else { const k = seg(t, a, a + .6); bx = lerp(glove[0], 540 + sgn * 700, eo(k)); by = lerp(glove[1], 560, eo(k)) - Math.sin(k * Math.PI) * 90; bs = 1; }
    if (t > a - .5) w += `<g transform="${tr(bx, by, bs)}">${ballG(36, t * 1100)}</g>`;
    if (sv) w += stars(glove[0], glove[1] - 40, 90, t, 1 - seg(t, a + 1, a + 1.3));
    const z = sv ? 1.06 + .08 * Math.exp(-(t - a) * 3) : lerp(1.0, 1.12, eio(seg(t, 0, a))), [sx, sy] = shakeAt(t, [a], 22);
    let s = cam(z, 540 + sx, 1080 + sy, w);
    if (p.baslik) s += bounce(p.baslik, 540, 545, 96, .05, t, { step: .02 });
    if (p.skor) s += scorebug(p.skor, t, p.baslik ? 640 : 560);
    if (sv) s += `<g transform="${tr(540 - sgn * 60, 900, 1, -4 * sgn)}">${bounce(p.metin || 'KURTARDI!', 0, 0, 160, a, t, { step: .035, col: LIME, maxw: 900 })}</g>`;
    if (p.alt) s += pill(540, 1100, p.alt, pop(t, p.alt_at != null ? p.alt_at : a + .45, .35), { size: 50, bg: '#fff' });
    return s;
  };
  // KUPA: ortadaki oyuncu kupayı kaldırır, yanlarda zıplayanlar, konfeti + havai fişek
  S.ckupa = (p, t, d) => {
    const a = p.at != null ? p.at : .3, L = (p.oyuncular && p.oyuncular.length ? p.oyuncular : [p.oyuncu || {}, p.oyuncu || {}, p.oyuncu || {}]);
    const Ks = [0, 1, 2].map(i => kit(Object.assign({}, L[Math.min(i, L.length - 1)], i !== 1 && !(p.oyuncular && p.oyuncular[i]) ? { sac: ['kahve', 'siyah', 'kizil'][i], no: '' } : {})));
    let w = stadium(t, t >= a ? 1 : .2, p.tribun) + fireworks(t, a);
    const hop = i => (t >= a ? -Math.abs(Math.sin(t * 7 + i * 1.3)) * 50 : 0);
    w += `<ellipse cx="215" cy="1385" rx="115" ry="18" fill="#000" opacity=".3"/><g transform="translate(215 ${f1(1380 + hop(1))}) scale(1.28)">${player(0, Ks[0], { poz: 'yumruk', face: 'happy', t })}</g>`;
    w += `<ellipse cx="865" cy="1385" rx="115" ry="18" fill="#000" opacity=".3"/><g transform="translate(865 ${f1(1380 + hop(2))}) scale(-1.28 1.28)">${player(0, Ks[2], { poz: 'yumruk', face: 'happy', t: t + .3, mirror: true })}</g>`;
    const lift = elastic(seg(t, a, a + .8)), HK = Object.assign({}, Ks[1], { glove: Ks[1].skin });
    w += `<ellipse cx="540" cy="1385" rx="140" ry="20" fill="#000" opacity=".3"/><g transform="translate(540 ${f1(1380 + hop(0) * .4)}) scale(1.35)">${keeper(HK, { face: 'happy' })}</g>`;
    const ty = 1380 + hop(0) * .4 - 1.35 * 318;
    w += `<circle cx="540" cy="${f1(ty - 130)}" r="${f1(230 * lift)}" fill="url(#${PFX}lamp)" opacity=".8"/>`;
    w += `<g transform="${tr(540, ty + (1 - lift) * 200, .64 * lift, Math.sin(t * 5) * 4)}">${trophy(p.kupa || 'kulakli')}</g>`;
    let s = cam(lerp(1.1, 1.0, eo(seg(t, 0, 1.2))), 540, 1000, w);
    if (p.kelime) s += bounce(p.kelime, 540, 575, 112, a, t, { step: .03, col: '#fff' });
    if (p.alt) s += pill(540, 660, p.alt, pop(t, p.alt_at != null ? p.alt_at : a + .5, .35), { size: 44, bg: RED, fg: '#fff' });
    return s + confetti(t, a + .05, 80, 43);
  };
  // İKİLİ: iki karakter karşı karşıya (rakipler, hoca–oyuncu, transfer), VS rozeti, balonlar
  S.cikili = (p, t, d) => {
    const A = p.sol || {}, B = p.sag || {}, KA = kit(A, 'kirmizi'), KB = kit(B, 'beyaz');
    const fa = ifade((A.ifade2_at != null && t >= A.ifade2_at) ? A.ifade2 : A.ifade), fb = ifade((B.ifade2_at != null && t >= B.ifade2_at) ? B.ifade2 : B.ifade);
    const ia = Math.min(1, eo(seg(t, 0, .45))), ib = Math.min(1, eo(seg(t, .15, .6)));
    let w = stadium(t, .1, p.tribun);
    w += `<ellipse cx="280" cy="1355" rx="130" ry="20" fill="#000" opacity=".3"/><g transform="translate(${f1(lerp(-200, 280, ia))} 1350) scale(1.6)">${player(0, KA, { poz: A.poz || 'dur', face: fa, t })}</g>`;
    w += `<ellipse cx="800" cy="1355" rx="130" ry="20" fill="#000" opacity=".3"/><g transform="translate(${f1(lerp(1280, 800, ib))} 1350) scale(-1.6 1.6)">${player(0, KB, { poz: B.poz || 'dur', face: fb, t: t + .4, mirror: true })}</g>`;
    let s = cam(lerp(1.08, 1.0, eo(seg(t, 0, 1))), 540, 1000, w);
    if (p.baslik) s += bounce(p.baslik, 540, 545, 100, .05, t, { step: .02 });
    if (p.vs !== '') { const va = p.vs_at != null ? p.vs_at : .55, k = pop(t, va, .35, 3), [sx, sy] = shakeAt(t, [va], 10);
      if (k > 0) s += `<g transform="${tr(540 + sx, 960 + sy, k, -8)}"><polygon points="${burstPts(115, 80, 12, 5)}" fill="${LIME}" stroke="${INK}" stroke-width="8"/><text y="30" text-anchor="middle" font-family="Anton" font-size="96" fill="${INK}">${esc(p.vs || 'VS')}</text></g>`; }
    if (A.balon) s += bubble(290, 700, A.balon.metin, pop(t, A.balon.at != null ? A.balon.at : .8, .4), [-40, 120], { size: 50, max: 13 });
    if (B.balon) s += bubble(790, 700, B.balon.metin, pop(t, B.balon.at != null ? B.balon.at : 1.4, .4), [40, 120], { size: 50, max: 13 });
    if (KA.ad) s += pill(280, 1115, KA.ad, pop(t, .4, .35), { size: 42, bg: INK, fg: LIME, maxw: 480 });
    if (KB.ad) s += pill(800, 1115, KB.ad, pop(t, .55, .35), { size: 42, bg: INK, fg: LIME, maxw: 480 });
    return s;
  };
  // SAYI: dev sayı/istatistik (ışıltı + yıldız), isteğe bağlı şaşkın karakter
  S.csayi = (p, t, d) => {
    const a = p.at != null ? p.at : .4;
    let w = stadium(t, t >= a ? .35 : 0, p.tribun);
    if (p.oyuncu) w += `<ellipse cx="165" cy="1405" rx="110" ry="16" fill="#000" opacity=".3"/><g transform="translate(165 1400) scale(1.3)">${player(0, kit(p.oyuncu), { poz: p.poz || 'yumruk', face: ifade(p.ifade || 'saskin'), t })}</g>`;
    let s = cam(lerp(1.06, 1.0, eo(seg(t, 0, 1))), 540, 1000, w);
    const k = pop(t, a, .5, 2);
    s += `<circle cx="540" cy="800" r="${f1(330 * Math.min(1, k))}" fill="url(#${PFX}lamp)" opacity=".55"/>`;
    if (p.ust) s += pill(540, 560, p.ust, pop(t, .1, .35), { size: 46 });
    if (k > 0) s += `<g transform="${tr(540, 880, 1 + .03 * Math.sin(t * 8))}">${bounce(p.sayi, 0, 0, 240, a, t, { step: .05, col: LIME, maxw: 940 })}</g>` + stars(540, 760, 380, t, Math.min(1, seg(t, a + .3, a + .6)));
    if (p.etiket) s += pill(540, 975, p.etiket, pop(t, p.etiket_at != null ? p.etiket_at : a + .45, .35), { size: 46, bg: '#fff', maxw: 760 });
    if (p.damga) s += stamp(720, 1100, p.damga.metin, seg(t, p.damga.at, p.damga.at + .3), { renk: p.damga.renk });
    return s;
  };
  // TABELA: stadyumun dev skor tabelası, forma ikonları, skor yanıp söner
  S.ctabela = (p, t, d) => {
    const a = p.at != null ? p.at : .6, KA = kit(p.sol_forma || { forma: '#E30A17' }), KB = kit(p.sag_forma || { forma: '#F4F4F4' });
    let w = stadium(t, t >= a ? .5 : .05, p.tribun);
    let s = cam(lerp(1.05, 1.0, eo(seg(t, 0, 1))), 540, 1000, w);
    const k = eo(seg(t, 0, .35));
    s += `<g transform="${tr(540, 860, lerp(.85, 1, k))}" opacity="${f1(k * 100) / 100}"><rect x="-450" y="-235" width="900" height="460" rx="26" fill="${INK}" stroke="${LIME}" stroke-width="10"/>`;
    for (let i = 0; i < 14; i++) s += `<circle cx="${-390 + i * 60}" cy="-205" r="9" fill="${LIME}" opacity="${(Math.floor(t * 8) + i) % 3 === 0 ? 1 : .3}"/>`;
    const name = (txt, x) => { const n = [...String(txt || '')].length, fs = Math.min(60, 380 / Math.max(1, n * .5)); return `<text x="${x}" y="-130" text-anchor="middle" font-family="Anton" font-size="${f1(fs)}" letter-spacing="2" fill="#fff">${esc(txt || '')}</text>`; };
    s += name(p.sol, -225) + name(p.sag, 225) + jersey(-225, -40, .7, KA) + jersey(225, -40, .7, KB);
    const [x1, x2] = String(p.skor || '-').split('-'), dk = pop(t, a, .45, 2.6);
    if (t < a) s += `<text x="0" y="150" text-anchor="middle" font-family="Anton" font-size="200" fill="#fff" opacity=".35">– –</text>`;
    else s += `<g transform="translate(0 80) scale(${f1(dk * 100) / 100})"><text x="0" y="70" text-anchor="middle" font-family="Anton" font-size="210" letter-spacing="8" fill="${LIME}">${esc((x1 || '').trim())} - ${esc((x2 || '').trim())}</text></g>`;
    s += `</g>`;
    if (p.ust) s += pill(540, 555, p.ust, pop(t, .1, .35), { size: 46 });
    if (p.damga) s += stamp(730, 1110, p.damga.metin, seg(t, p.damga.at, p.damga.at + .3), { renk: p.damga.renk });
    return s;
  };
  // Yalnız stadyum (foto sahnesinde "arka": "stadyum")
  S.stadyum = (p, t) => stadium(t, .15, p.tribun);

  function draw(p, t, d, i) {
    UID = 0; PFX = 'cz' + i;
    const f = S[p.tip] || S.stadyum;
    return DEFS() + f(p, Math.max(0, t), d);
  }
  return { draw, kit, TAKIM };
})();

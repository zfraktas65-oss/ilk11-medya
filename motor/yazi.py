# -*- coding: utf-8 -*-
"""Videodaki konuşmayı ifade ifade yazıya döker (Whisper turbo, sherpa-onnx, çevrimdışı).

Kullanım:
  python3 motor/yazi.py kaynak.mp4 ifadeler.json [--dil tr] [--bas 0] [--son 59.8]
Çıktı: [{"a": sn, "b": sn, "metin": "..."}]  (kaynak videonun zamanına göre)
Bu ham metindir: senaryo.json'a koymadan önce isimleri ve yazım hatalarını düzelt (bkz. gorevler/demec_reels.md).
Gerekenler: pip install --break-system-packages sherpa-onnx soundfile ; model ilk çalıştırmada GitHub'dan iner (~560 MB).
"""
import argparse, json, os, re, subprocess

MODELS = os.environ.get("ASR_MODELS", os.path.expanduser("~/models"))
M = os.path.join(MODELS, "sherpa-onnx-whisper-turbo")
URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2"


def ensure_model():
    if not os.path.exists(os.path.join(M, "turbo-encoder.int8.onnx")):
        os.makedirs(MODELS, exist_ok=True)
        subprocess.run(f"curl -sSL -m 900 '{URL}' | tar xj -C '{MODELS}'", shell=True, check=True)


def segments(wav, bas, son, min_len=1.2, max_len=24.0):
    """Sessizliklerden ifade aralıkları çıkarır."""
    log = subprocess.run(["ffmpeg", "-v", "info", "-i", wav, "-af", "silencedetect=n=-32dB:d=0.18", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = [(a, b) for a, b in zip(st, en) if b > bas and a < son]
    segs, t = [], bas
    for a, b in sil:
        if a > t + .05:
            segs.append([t, min(a, son)])
        t = max(t, b)
    if t < son - .2:
        segs.append([t, son])
    # kısa parçaları komşusuna kat, uzunları böl
    out = []
    for s in segs:
        if out and (s[1] - s[0] < min_len or out[-1][1] - out[-1][0] < min_len) and s[1] - out[-1][0] <= max_len:
            out[-1][1] = s[1]
        else:
            out.append(s)
    res = []
    for a, b in out:
        n = int((b - a) // max_len) + 1
        for k in range(n):
            res.append([a + (b - a) * k / n, a + (b - a) * (k + 1) / n])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("cikti")
    ap.add_argument("--dil", default="tr"); ap.add_argument("--bas", type=float, default=0.0)
    ap.add_argument("--son", type=float, default=None)
    a = ap.parse_args()
    import numpy as np, soundfile as sf, sherpa_onnx
    ensure_model()
    wav = os.path.splitext(a.cikti)[0] + "_16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-ac", "1", "-ar", "16000", wav], check=True)
    s, sr = sf.read(wav, dtype="float32")
    son = a.son if a.son else len(s) / sr
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{M}/turbo-encoder.int8.onnx", decoder=f"{M}/turbo-decoder.int8.onnx", tokens=f"{M}/turbo-tokens.txt",
        language=a.dil, task="transcribe", num_threads=8, tail_paddings=2000)
    out = []
    for x, y in segments(wav, a.bas, son):
        stm = rec.create_stream()
        stm.accept_waveform(sr, s[int(x * sr):int(y * sr)])
        rec.decode_stream(stm)
        txt = stm.result.text.strip()
        print(f"[{x:6.2f}-{y:6.2f}] {txt}", flush=True)
        if txt:
            out.append({"a": round(x, 2), "b": round(y, 2), "metin": txt})
    json.dump(out, open(a.cikti, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Kaydedildi:", a.cikti, "| ifade:", len(out))


if __name__ == "__main__":
    main()

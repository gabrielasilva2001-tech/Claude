"""Gera audio/fala.json: intervalos com FALA de verdade (detector de voz Silero + volume),
sem pausas de pensamento nem respiros."""
from silero_vad import load_silero_vad, get_speech_timestamps
import json, wave, numpy as np, torch, sys
m = load_silero_vad()
out = {}
for f in sys.argv[1:]:
    w = wave.open(f"audio/{f}.wav"); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    vad = get_speech_timestamps(torch.from_numpy(x), m, sampling_rate=16000, return_seconds=True, threshold=0.5,
                                min_silence_duration_ms=100, speech_pad_ms=30, min_speech_duration_ms=100)
    fr = 160; n = len(x) // fr
    db = 10 * np.log10((x[:n * fr].reshape(n, fr) ** 2).mean(1) + 1e-10)
    thr = np.percentile(db, 90) - 19
    low = db < thr
    # trechos baixos >= 0.20 s viram corte (pausa curta / respiro), deixando 30 ms de margem
    holes, i = [], 0
    while i < n:
        if low[i]:
            j = i
            while j < n and low[j]: j += 1
            if (j - i) >= 16: holes.append(((i + 3) / 100, (j - 3) / 100))
            i = j
        else: i += 1
    keep = []
    for t in vad:
        a, b = t["start"], t["end"]
        cur = [(a, b)]
        for ha, hb in holes:
            nxt = []
            for ca, cb in cur:
                if hb <= ca or ha >= cb: nxt.append((ca, cb)); continue
                if ha > ca: nxt.append((ca, ha))
                if hb < cb: nxt.append((hb, cb))
            cur = nxt
        keep += [(round(ca, 3), round(cb, 3)) for ca, cb in cur if cb - ca >= 0.08]
    out[f] = keep
    print(f, len(keep), "trechos, fala total %.1fs, thr %.0f dB" % (sum(b - a for a, b in keep), thr))
json.dump(out, open("audio/fala.json", "w"))

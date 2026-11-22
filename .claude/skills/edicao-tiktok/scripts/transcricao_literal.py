import sys, json, os, re, subprocess, whisper, torch, numpy as np
torch.set_num_threads(2)
S = "calcas"
src = open(f"{S}/editar_calcas.py").read()
block = src[src.index("SEGS = ["):src.index("]\nFILES") + 1]
ns = {}; exec(block, ns); SEGS = ns["SEGS"]
part, nparts = int(sys.argv[1]), int(sys.argv[2])
m = whisper.load_model("medium")
PROMPT = "Ah, então, essa daqui, essa daqui é... é, tipo, essa calça, essa calça aqui, né? Ãhn, aí, aí eu, eu acho que, que ela fica."
for i, (f, a, b) in enumerate(SEGS):
    if i % nparts != part: continue
    out = f"{S}/audio/verb_{f}_{a:.2f}_{b:.2f}.json"
    if os.path.exists(out): continue
    a0 = max(a - 0.4, 0)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a0}", "-to", f"{b+0.6}", "-i", f"{S}/audio/IMG_{f}.wav",
                          "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    r = m.transcribe(x, language="pt", word_timestamps=True, fp16=False, condition_on_previous_text=False,
                     initial_prompt=PROMPT, temperature=0)
    ws = [{"word": w["word"], "start": w["start"] + a0, "end": w["end"] + a0} for s in r["segments"] for w in s["words"]]
    json.dump(ws, open(out, "w"), ensure_ascii=False)
    print(f, a, b, " ".join(w["word"].strip() for w in ws), flush=True)

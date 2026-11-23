import sys, json, whisper
m = whisper.load_model("medium")
for p in sys.argv[1:]:
    r = m.transcribe(p, language="pt", word_timestamps=True, fp16=False, condition_on_previous_text=False)
    json.dump(r["segments"], open(p.replace(".wav", ".m.json"), "w"), ensure_ascii=False)
    with open(p.replace(".wav", ".txt"), "w") as f:
        for s in r["segments"]:
            f.write(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}\n")
    print("done", p, flush=True)

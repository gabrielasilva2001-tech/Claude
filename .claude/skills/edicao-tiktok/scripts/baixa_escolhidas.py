import sys, json, time, os, urllib.request, urllib.error
UA = {"User-Agent": "VideoEditBot/1.0 (generic client; low volume)"}
F = sys.argv[1]; picks = sys.argv[2:]   # key_idx
cred = []
for p in picks:
    k, i = p.rsplit("_", 1); x = json.load(open(f"{F}/cand/{k}.json"))[int(i)]
    dst = f"{F}/{p}.jpg"
    if not (os.path.exists(dst) and os.path.getsize(dst) > 1000):
        for n in range(10):
            try:
                data = urllib.request.urlopen(urllib.request.Request(x["thumb"], headers=UA), timeout=90).read()
                if len(data) > 1000: open(dst, "wb").write(data); break
            except urllib.error.HTTPError as e:
                if e.code != 429: print("ERR", p, e.code, flush=True); break
            time.sleep(20 * (n + 1))
    print("ok" if os.path.exists(dst) else "FALHOU", p, flush=True)
    with open(f"{F}/creditos.txt", "a") as c: c.write(f"{p}: {x['title']} — {x['lic']}\n")
    time.sleep(3)

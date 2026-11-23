import sys, json, time, urllib.request, urllib.parse, urllib.error
UA = {"User-Agent": "VideoEditBot/1.0 (generic client; low volume)"}
OUT = sys.argv[1]
TERMS = [l.split(" ",1) for l in open(sys.argv[2]).read().strip().splitlines()]
def get(url):
    for k in range(12):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(30 * (k + 1))
    raise SystemExit("rate limited")
for key, term in TERMS:
    p = {"action":"query","format":"json","generator":"search","gsrsearch":f"filetype:bitmap {term}","gsrnamespace":6,"gsrlimit":8,
         "prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":1400,"maxlag":5}
    r = json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p)))
    res = []
    for pg in sorted(r.get("query",{}).get("pages",{}).values(), key=lambda x: x.get("index",0)):
        ii = pg["imageinfo"][0]; md = ii.get("extmetadata",{})
        res.append(dict(title=pg["title"], thumb=ii.get("thumburl"), w=ii["width"], h=ii["height"],
                        lic=md.get("LicenseShortName",{}).get("value",""), artist=md.get("Artist",{}).get("value","")[:120]))
    json.dump(res, open(f"{OUT}/{key}.json","w"), ensure_ascii=False)
    print(key, len(res), flush=True)
    time.sleep(25)
print("FIM", flush=True)

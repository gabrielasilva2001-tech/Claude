"""Banho da Lúcia — v4.
Mudanças pedidas por ela sobre a v3:
- sem a olhadinha no relógio no 2º take; parte acelerada sem ela arrumando a câmera;
- entra "mostra que você é inteligente e fica longe da orelhinha";
- ênfase: zoom que ANDA até a Lúcia quando ela fala da Lúcia;
- final: assim que ela termina de falar, o enquadramento anda até a carinha da Lúcia (sem congelar);
- sons com padrão fixo por situação; título mais perto da referência (etiquetas + adesivos).
Cópias de trabalho em proxyR/ já endireitadas (V1 6,5°, V2 5,5°, V3 6°).
"""
import json, subprocess, os

S = os.environ["EDIT_WORK"]
PROXY, OUT = f"{S}/proxyR", f"{S}/render"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONTS = "/home/user/Claude/.claude/skills/edicao-tiktok/fonts"

# nome, arquivo, início, fim, velocidade, zoom fixo, mudo, legenda ("top"/"bot"/None),
# ênfase = (início do movimento no bruto, duração, alvo x, alvo y [coord. 1080x1920], zoom final)
SEGS = [
    ("gancho",   "V1", 54.05, 60.05, 1, 1.00, False, "bot", None),
    ("melhor",   "V2", 1.70, 7.45, 1, 1.00, False, "bot", (5.40, 0.5, 560, 700, 1.55)),  # sem olhar o relógio
    ("fugir",    "V2", 8.85, 14.05, 1, 1.00, False, "bot", None),
    ("molha1",   "V2", 40.5, 45.0, 4, 1.00, True, None, None),   # sem ela arrumando a câmera
    ("molha2",   "V2", 50.0, 55.5, 4, 1.00, True, None, None),
    ("cansa",    "V2", 65.55, 69.35, 1, 1.00, False, "top", None),
    ("joelho",   "V2", 73.75, 76.35, 1, 1.10, False, "top", None),
    ("orelha",   "V2", 125.25, 127.66, 1, 1.00, False, "top", None),
    ("querdizer","V2", 127.66, 129.75, 1, 1.16, False, "top", None),
    ("dica",     "V2", 150.65, 155.65, 1, 1.00, False, "top", None),
    ("esfrega",  "V2", 176.0, 192.0, 4, 1.00, True, None, None),
    ("suja",     "V2", 295.6, 297.25, 1, 1.00, False, "top", (295.75, 0.45, 460, 1270, 1.7)),
    ("pose",     "V2", 302.4, 305.0, 1, 1.00, False, None, None),
    ("eu_banho", "V2", 314.25, 317.45, 1, 1.10, False, "top", None),
    ("lagrima",  "V2", 386.35, 389.85, 1, 1.00, False, "top", (386.6, 0.6, 340, 1480, 1.6)),
    ("esperta",  "V2", 438.05, 442.75, 1, 1.00, False, "auto", (439.0, 0.6, 400, 1400, 1.7)),
    ("balanca",  "V2", 462.85, 466.75, 1, 1.00, False, "bot", None),
    ("limpeza",  "V2", 475.8, 480.2, 1, 1.08, False, "top", None),
    ("rosto",    "V3", 2.65, 4.6, 1, 1.00, False, None, None),     # transcrição incerta: sem legenda
    ("final",    "V3", 20.35, 25.70, 1, 1.00, False, "bot", (22.25, 0.7, 505, 715, 2.3)),
]
IDX = {s[0]: i for i, s in enumerate(SEGS)}
FIX_TEXT = {"para": "pra", "Aja": "Haja", "aja": "haja", "balancar": "balançar"}

words = {f: [w for s in json.load(open(f"{S}/audio/{f}.m.json")) for w in s["words"]] for f in ("V1", "V2", "V3")}

def ts(t):
    t = max(t, 0); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

timeline, t = [], 0.0
for seg in SEGS:
    d = (seg[3] - seg[2]) / seg[4]; timeline.append((seg, t, d)); t += d
TOTAL = t
def at(name, src):
    seg, o, d = timeline[IDX[name]]; return o + (src - seg[2]) / seg[4]
def so(name): return timeline[IDX[name]][1]
def sd(name): return timeline[IDX[name]][2]

# ---------- legendas ----------
caps = []
for i, (seg, o, d) in enumerate(timeline):
    name, f, a, b, sp, z, mute, pos, emph = seg
    if mute or pos is None: continue
    chunk, segcaps = [], []
    for w in [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.05]:
        txt = w["word"].strip(); txt = FIX_TEXT.get(txt, txt)
        if not txt: continue
        chunk.append((txt, at(name, w["start"]), at(name, min(w["end"], w["start"] + 0.8, b))))
        if len(chunk) >= 3 or txt[-1] in ",.?!":
            segcaps.append(chunk); chunk = []
    if chunk: segcaps.append(chunk)
    if pos == "auto":
        zt = at(name, emph[0])
        caps += [(c, o + d, c[0][1] < zt) for c in segcaps]
    else:
        caps += [(c, o + d, pos == "top") for c in segcaps]
fixed = []
for k, (ch, send, top) in enumerate(caps):
    a, b = ch[0][1], ch[-1][2]
    nxt = caps[k + 1][0][0][1] if k + 1 < len(caps) else TOTAL
    fixed.append((a, min(max(b + 0.15, a + 0.35), nxt, b + 0.4, send), ch, top))
caps = fixed
ZF0 = at("final", SEGS[IDX["final"]][8][0])
caps = [(a, min(b, ZF0) if a < ZF0 else b, ch, top) for a, b, ch, top in caps]

# ---------- título (referência dela: "a day in my life") ----------
PINK, WHITE = "&HB45CFF&", "&HFFFFFF&"
SLAP = r"\fscx0\fscy0\t(%d,%d,\fscx116\fscy116)\t(%d,%d,\fscx100\fscy100)"
def slap(t0, size=100):
    return r"\fscx0\fscy0\t(%d,%d,\fscx%d\fscy%d)\t(%d,%d,\fscx%d\fscy%d)" % (
        t0, t0 + 110, size * 1.16, size * 1.16, t0 + 110, t0 + 190, size, size)
def circle(r, cx=0, cy=0):
    k = 0.5523 * r
    return (f"m {cx} {cy-r} b {cx+k} {cy-r} {cx+r} {cy-k} {cx+r} {cy} b {cx+r} {cy+k} {cx+k} {cy+r} {cx} {cy+r} "
            f"b {cx-k} {cy+r} {cx-r} {cy+k} {cx-r} {cy} b {cx-r} {cy-k} {cx-k} {cy-r} {cx} {cy-r}")
def ellipse(rx, ry, cx, cy):
    kx, ky = 0.5523 * rx, 0.5523 * ry
    return (f"m {cx} {cy-ry} b {cx+kx} {cy-ry} {cx+rx} {cy-ky} {cx+rx} {cy} b {cx+rx} {cy+ky} {cx+kx} {cy+ry} {cx} {cy+ry} "
            f"b {cx-kx} {cy+ry} {cx-rx} {cy+ky} {cx-rx} {cy} b {cx-rx} {cy-ky} {cx-kx} {cy-ry} {cx} {cy-ry}")
STAR = "m 0 -56 b 8 -8 8 -8 56 0 b 8 8 8 8 0 56 b -8 8 -8 8 -56 0 b -8 -8 -8 -8 0 -56"
import math
PETALS = " ".join(ellipse(17, 17, round(30 * math.cos(a), 1), round(30 * math.sin(a), 1))
                  for a in [i * math.pi / 4 for i in range(8)])
SMILE = "m -24 6 b -16 30 16 30 24 6 b 14 18 -14 18 -24 6"
T_IN, T_OUT = 0.05, 3.7
def sticker_layer(x, y, color, draw, t0, extra="", size=100, layer_rot=r"\frz-8"):
    return (T_IN, T_OUT, "Draw", r"{\pos(%d,%d)\fad(0,180)\1c%s%s%s%s\p1}%s{\p0}" % (x, y, color, layer_rot, slap(t0, size), extra, draw))
overlays = [
    (T_IN, T_OUT, "Sticker", r"{\pos(500,1215)\frz4\fad(0,180)%s}dia de banho" % slap(0)),
    (T_IN, T_OUT, "Sticker", r"{\pos(600,1350)\frz4\fad(0,180)\3c&H8AF0F6&%s}da Lúcia" % slap(160)),
    # carinha sorrindo (adesivo amarelo) no canto da 1ª etiqueta
    sticker_layer(178, 1130, "&H2DD5FF&", circle(42), 330, r"\bord5\3c&HFFFFFF&"),
    sticker_layer(178, 1130, "&H1A1A1A&", ellipse(6, 9, -14, -10) + " " + ellipse(6, 9, 14, -10) + " " + SMILE, 330),
    # florzinha (margarida) no canto da 2ª etiqueta
    sticker_layer(905, 1420, "&HFFFFFF&", PETALS, 420, r"\bord3\3c&HDDDDDD&\t(500,3600,\frz-70)", layer_rot=""),
    sticker_layer(905, 1420, "&H2DC8FF&", circle(15), 420, layer_rot=""),
    # brilhinhos
    (T_IN, T_OUT, "Draw", r"{\pos(860,1120)\fad(0,180)\1c&H3DD9FF&%s\t(400,3600,\frz200)\p1}%s{\p0}" % (slap(470, 80), STAR)),
    (T_IN, T_OUT, "Draw", r"{\pos(300,1440)\fad(0,180)\1c&HB45CFF&%s\t(450,3600,\frz-160)\p1}%s{\p0}" % (slap(520, 70), STAR)),
    (T_IN, T_OUT, "Draw", r"{\pos(990,1250)\fad(0,180)\1c&HFFFFFF&%s\p1}%s{\p0}" % (slap(560, 45), STAR)),
    # 4x
    (so("molha1"), so("molha2") + sd("molha2"), "Tag", r"{\pos(960,230)\fad(60,60)}4x"),
    (so("esfrega"), so("esfrega") + sd("esfrega"), "Tag", r"{\pos(960,230)\fad(60,60)}4x"),
    # dica
    (so("dica") + 0.25, so("dica") + sd("dica"), "Info",
     r"{\pos(540,640)\fad(80,120)\fscx90\fscy90\t(0,140,\fscx100\fscy100)}" + r"{\c%s}[ {\c%s}1 semana em casa · 1 no pet shop {\c%s}]" % (PINK, WHITE, PINK)),
]

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins SemiBold,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.5,1.5,2,90,90,360,1
Style: CapTop,Poppins SemiBold,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.5,1.5,8,90,90,380,1
Style: Sticker,Fredoka,100,&H001A1A1A,&H001A1A1A,&H00FFB8C9,&H96000000,-1,0,0,0,100,100,0,0,3,20,8,5,40,40,0,1
Style: Draw,Fredoka,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,3,7,0,0,0,1
Style: Tag,Montserrat Thin ExtraBold,56,&H00FFFFFF,&H00FFFFFF,&H50000000,&H00000000,0,0,0,0,100,100,0,0,3,14,0,5,40,40,0,1
Style: Info,Poppins SemiBold,52,&H00FFFFFF,&H00FFFFFF,&H001A1A1A,&H00000000,0,0,0,0,100,100,0,0,3,18,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for a, b, ch, top in caps:
    for j, (wtxt, wa, wb) in enumerate(ch):
        ea = a if j == 0 else wa
        eb = ch[j + 1][1] if j + 1 < len(ch) else b
        if eb <= ea: continue
        body = []
        for m, (t2, _, _) in enumerate(ch):
            t2 = t2.rstrip(".,") if m == len(ch) - 1 else t2
            body.append("{\\c&H3DD9FF&}" + t2 + "{\\c&HFFFFFF&}" if m == j else t2)
        enter = "{\\fad(60,0)\\fscx94\\fscy94\\t(0,100,\\fscx100\\fscy100)}" if j == 0 else ""
        style = "CapTop" if top else "Cap"
        ass += f"Dialogue: 0,{ts(ea)},{ts(eb)},{style},,0,0,0,,{enter}{' '.join(body)}\n"
for k, (a, b, st, txt) in enumerate(overlays):
    ass += f"Dialogue: {2 + k if st == 'Draw' else 1},{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

# ---------- sons: PADRÃO FIXO por situação ----------
# ênfase na Lúcia (zoom andando) -> "swish" suave | parte acelerada -> whoosh | dica -> ding
# humor/absurdo -> arranhão de disco | frase de impacto -> boom | foto/pose -> obturador
# zoom final -> apito subindo (som zoado)
def synth(name, expr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *expr, f"{OUT}/{name}.wav"], check=True)
synth("whoosh", ["-f", "lavfi", "-i", "anoisesrc=d=0.6:c=pink:a=0.8:r=48000", "-af",
                 "highpass=f=300,lowpass=f=5000,afade=t=in:d=0.3:curve=exp,afade=t=out:st=0.3:d=0.3:curve=exp,"
                 "pan=stereo|c0=c0|c1=c0,aeval=val(0)*(1-t/0.6)|val(1)*(t/0.6):c=stereo"])
synth("swish", ["-f", "lavfi", "-i", "anoisesrc=d=0.35:c=white:a=0.7:r=48000", "-af",
                "highpass=f=1800,lowpass=f=9000,afade=t=in:d=0.2:curve=exp,afade=t=out:st=0.2:d=0.15,pan=stereo|c0=c0|c1=c0"])
def bell(name, notes, d=0.7):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    synth(name, ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                 f"afade=t=in:d=0.003,aecho=0.8:0.35:40:0.2,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0"])
bell("ding", [(2093, 0.6, 6, 0), (4186, 0.15, 10, 0)], d=0.9)
synth("shutter", ["-f", "lavfi", "-i",
                  "aevalsrc='(random(0)*2-1)*(exp(-300*t)+0.8*exp(-300*(t-0.075))*gte(t,0.075))':s=48000:d=0.16",
                  "-af", "highpass=f=1200,pan=stereo|c0=c0|c1=c0"])
synth("scratch", ["-f", "lavfi", "-i",
                  "aevalsrc='(0.55+0.45*(random(0)*2-1))*sin(2*PI*(700*t-450*cos(2*PI*5.5*t)/(2*PI*5.5)))*exp(-3*t)':s=48000:d=0.36",
                  "-af", "highpass=f=200,lowpass=f=3500,afade=t=in:d=0.01,afade=t=out:st=0.28:d=0.08,pan=stereo|c0=c0|c1=c0"])
synth("boom", ["-f", "lavfi", "-i",
               "aevalsrc='tanh(2.2*sin(2*PI*(62*t-10*t*t))*exp(-3.2*t))+0.3*sin(2*PI*124*t)*exp(-6*t)':s=48000:d=1.0",
               "-af", "lowpass=f=900,afade=t=out:st=0.8:d=0.2,pan=stereo|c0=c0|c1=c0"])
synth("zoom", ["-f", "lavfi", "-i",
               "aevalsrc='0.6*sin(2*PI*(520*t+2600*t*t+0.8*sin(2*PI*14*t)))*min(1,t/0.02)*if(lt(t,0.3),1,exp(-14*(t-0.3)))':s=48000:d=0.55",
               "-af", "lowpass=f=6000,aecho=0.7:0.3:35:0.2,pan=stereo|c0=c0|c1=c0"])
sfx = [
    ("whoosh", so("molha1") - 0.3, 0.35),
    ("whoosh", so("esfrega") - 0.3, 0.35),
    ("ding", so("dica") + 0.25, 0.28),
    ("scratch", at("querdizer", 127.70), 0.28),
    ("scratch", at("eu_banho", 315.55), 0.3),
    ("boom", at("lagrima", 389.15), 0.5),
    ("shutter", at("pose", 303.0), 0.5),
    ("zoom", at("final", 22.25), 0.45),
]
for seg in SEGS:
    if seg[8] and seg[0] != "final":
        sfx.append(("swish", at(seg[0], seg[8][0]), 0.22))

# ---------- render ----------
inputs, fc, labels = [], [], []
FLASH = ",drawbox=t=fill:c=white@0.85:enable='between(t,0.58,0.62)',drawbox=t=fill:c=white@0.4:enable='between(t,0.62,0.66)'"
LOOK = "eq=contrast=1.05:saturation=1.12:brightness=0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03:rm=0.02:bm=-0.02"
for i, (seg, o, d) in enumerate(timeline):
    name, f, a, b, sp, z, mute, pos, emph = seg
    k = sum(1 for x in inputs if x == "-i"); inputs += ["-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", f"{PROXY}/{f}.mp4"]
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    chain = f"[{k}:v]setpts=(PTS-STARTPTS)/{sp},crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2.6,scale={W}:{H},fps=30,setsar=1"
    if emph:
        t0, dur, tx, ty, zm = emph
        t0 -= a
        p = f"min(1,max(0,(it-{t0:.3f})/{dur}))"
        zexpr = f"1+({zm}-1)*{p}*{p}*(3-2*{p})"   # movimento suave (acelera e assenta)
        chain += (f",scale=2160:3840,zoompan=z='{zexpr}':x='max(0,min(iw-iw/zoom,{tx*2}-iw/zoom/2))'"
                  f":y='max(0,min(ih-ih/zoom,{ty*2}-ih/zoom/2))':d=1:s={W}x{H}:fps=30,setsar=1")
    if name == "pose": chain += FLASH
    fc.append(chain + f"[v{i}]")
    if mute:
        fc.append(f"[{k}:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  f"asetrate=96000,aresample=48000,atempo=2.0,volume=0.5,atrim=0:{d:.3f},apad=whole_dur={d:.3f},"
                  f"afade=t=in:d=0.08,afade=t=out:st={max(d-0.1,0):.3f}:d=0.1[a{i}]")
    else:
        fc.append(f"[{k}:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  f"afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03[a{i}]")
    labels.append(f"[v{i}][a{i}]")
ass_path = f"{OUT}/legendas.ass".replace(":", r"\:")
fc.append("".join(labels) + f"concat=n={len(timeline)}:v=1:a=1[vc][ac]")
fc.append(f"[vc]{LOOK},subtitles='{ass_path}':fontsdir={FONTS},fade=t=out:st={TOTAL-0.6:.2f}:d=0.6[vout]")
mix = ["[ac]"]
for j, (nm, when, vol) in enumerate(sfx):
    idx = sum(1 for x in inputs if x == "-i"); inputs += ["-i", f"{OUT}/{nm}.wav"]
    ms = int(max(when, 0) * 1000)
    fc.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL-0.6:.2f}:d=0.6[aout]")
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/banho_lucia_v4.mp4"]
subprocess.run(cmd, check=True)
print(f"OK duração {TOTAL:.1f}s, {len(caps)} legendas")
for i, (seg, o, d) in enumerate(timeline): print(f"{seg[0]:10s} {o:6.2f} {d:5.2f}")
for a, b, ch, top in caps: print(f"{a:6.2f} {'T' if top else 'B'} {' '.join(c[0] for c in ch)}")

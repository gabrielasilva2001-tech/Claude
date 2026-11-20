"""Banho da Lúcia — v1 (primeiro corte, visual provisório seguindo DIRETRIZES.md)."""
import json, subprocess, os

S = os.environ["EDIT_WORK"]
PROXY, OUT = f"{S}/proxy", f"{S}/render"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONTS = "/home/user/Claude/.claude/skills/edicao-tiktok/fonts"

# (arquivo, início, fim, velocidade, zoom, mudo)
SEGS = [
    ("V1", 54.05, 60.05, 1, 1.00, False),   # 0 gancho: cheiro de Cheetos
    ("V2", 0.95, 7.45, 1, 1.08, False),     # 1 melhor cachorra pra tomar banho
    ("V2", 8.85, 14.05, 1, 1.00, False),    # 2 tenta fugir / porta aberta
    ("V2", 40.0, 64.0, 4, 1.00, True),      # 3 molhando (4x)
    ("V2", 65.55, 69.35, 1, 1.00, False),   # 4 cansa mais a mamãe
    ("V2", 73.75, 76.35, 1, 1.10, False),   # 5 haja joelho
    ("V2", 125.25, 129.75, 1, 1.00, False), # 6 orelha
    ("V2", 150.65, 155.65, 1, 1.08, False), # 7 1 semana em casa / 1 no pet shop
    ("V2", 176.0, 192.0, 4, 1.00, True),    # 8 esfregando (4x)
    ("V2", 295.6, 297.25, 1, 1.00, False),  # 9 ficando mais suja
    ("V2", 302.4, 305.0, 1, 1.00, False),   # 10 pose com ela molhada
    ("V2", 314.25, 317.45, 1, 1.10, False), # 11 eu que tô tomando banho?
    ("V2", 386.35, 389.85, 1, 1.00, False), # 12 lágrima ácida
    ("V2", 462.85, 466.75, 1, 1.00, False), # 13 balançar de novo (ela se esquivando)
    ("V2", 475.8, 480.2, 1, 1.08, False),   # 14 só uma limpeza até semana que vem
    ("V3", 2.65, 4.6, 1, 1.00, False),      # 15 molhou o rosto (sem legenda: transcrição incerta)
    ("V3", 20.35, 24.55, 1, 1.00, False),   # 16 conta pro pessoal -> congela no sorriso
]
NOCAP = {15}
FIX_TEXT = {"para": "pra", "Aja": "Haja", "aja": "haja", "balancar": "balançar"}

words = {f: [w for s in json.load(open(f"{S}/audio/{f}.m.json")) for w in s["words"]] for f in ("V1", "V2", "V3")}

def ts(t):
    t = max(t, 0); return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

timeline, t = [], 0.0
for seg in SEGS:
    d = (seg[2] - seg[1]) / seg[3]; timeline.append((seg, t, d)); t += d
TOTAL, END = t, 1.6
def out_time(i, src):
    seg, o, d = timeline[i]; return o + (src - seg[1]) / seg[3]
def at(i, src): return out_time(i, src)

# ---------- legendas ----------
caps, seg_end = [], []
for i, (seg, o, d) in enumerate(timeline):
    f, a, b, sp, z, mute = seg
    if mute or i in NOCAP: continue
    chunk = []
    for w in [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.05]:
        txt = w["word"].strip(); txt = FIX_TEXT.get(txt, txt)
        if not txt: continue
        chunk.append((txt, out_time(i, w["start"]), out_time(i, min(w["end"], b))))
        if len(chunk) >= 3 or txt[-1] in ",.?!":
            caps.append(chunk); seg_end.append(o + d); chunk = []
    if chunk: caps.append(chunk); seg_end.append(o + d)
fixed = []
for k, ch in enumerate(caps):
    a, b = ch[0][1], ch[-1][2]
    nxt = caps[k + 1][0][1] if k + 1 < len(caps) else TOTAL
    fixed.append((a, min(max(b + 0.15, a + 0.35), nxt, b + 0.4, seg_end[k]), ch))
caps = fixed

PINK, YEL, WHITE = "&HB45CFF&", "&H3DD9FF&", "&HFFFFFF&"
def so(i): return timeline[i][1]
def sd(i): return timeline[i][2]
RISE = r"{\fad(80,120)\fscx90\fscy90\t(0,140,\fscx100\fscy100)}"

overlays = [
    # gancho: duas linhas sobem em sequência (sem digitação dessa vez)
    (0.10, 3.6, "Title", r"{\move(540,250,540,215,0,180)\fad(120,200)}DIA DE BANHO"),
    (0.30, 3.6, "Title", r"{\move(540,330,540,295,0,180)\fad(120,200)\fs84\c%s}da LÚCIA" % PINK),
    # 4x: etiqueta pequena no canto, sem cobrir o rosto
    (so(3), so(3) + sd(3), "Tag", r"{\pos(960,230)\fad(60,60)}4x"),
    (so(8), so(8) + sd(8), "Tag", r"{\pos(960,230)\fad(60,60)}4x"),
    # dica: alternância casa / pet shop
    (so(7) + 0.25, so(7) + sd(7), "Info", r"{\pos(540,560)}" + RISE + r"{\c%s}[ {\c%s}1 semana em casa · 1 no pet shop {\c%s}]" % (PINK, WHITE, PINK)),
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
Style: Title,Montserrat Thin ExtraBold,78,&H00FFFFFF,&H00FFFFFF,&H00141414,&H64000000,0,0,0,0,100,100,1,0,1,3.5,3,5,60,60,0,1
Style: Tag,Montserrat Thin ExtraBold,56,&H00FFFFFF,&H00FFFFFF,&H50000000,&H00000000,0,0,0,0,100,100,0,0,3,14,0,5,40,40,0,1
Style: Info,Poppins SemiBold,52,&H00FFFFFF,&H00FFFFFF,&H001A1A1A,&H00000000,0,0,0,0,100,100,0,0,3,18,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for a, b, ch in caps:
    for j, (wtxt, wa, wb) in enumerate(ch):
        ea = a if j == 0 else wa
        eb = ch[j + 1][1] if j + 1 < len(ch) else b
        if eb <= ea: continue
        body = []
        for m, (t2, _, _) in enumerate(ch):
            t2 = t2.rstrip(".,") if m == len(ch) - 1 else t2
            body.append("{\\c&H3DD9FF&}" + t2 + "{\\c&HFFFFFF&}" if m == j else t2)
        enter = "{\\fad(60,0)\\fscx94\\fscy94\\t(0,100,\\fscx100\\fscy100)}" if j == 0 else ""
        ass += f"Dialogue: 0,{ts(ea)},{ts(eb)},Cap,,0,0,0,,{enter}{' '.join(body)}\n"
for a, b, st, txt in overlays:
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

# ---------- sons (curtos, cada um uma vez, abaixo da voz) ----------
def synth(name, expr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *expr, f"{OUT}/{name}.wav"], check=True)
synth("whoosh", ["-f", "lavfi", "-i", "anoisesrc=d=0.6:c=pink:a=0.8:r=48000", "-af",
                 "highpass=f=300,lowpass=f=5000,afade=t=in:d=0.3:curve=exp,afade=t=out:st=0.3:d=0.3:curve=exp,"
                 "pan=stereo|c0=c0|c1=c0,aeval=val(0)*(1-t/0.6)|val(1)*(t/0.6):c=stereo"])
def bell(name, notes, d=0.7):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    synth(name, ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                 f"afade=t=in:d=0.003,aecho=0.8:0.35:40:0.2,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0"])
bell("ding", [(2093, 0.6, 6, 0), (4186, 0.15, 10, 0)], d=0.9)
# obturador: dois cliques secos
synth("shutter", ["-f", "lavfi", "-i",
                  "aevalsrc='(random(0)*2-1)*(exp(-300*t)+0.8*exp(-300*(t-0.075))*gte(t,0.075))':s=48000:d=0.16",
                  "-af", "highpass=f=1200,pan=stereo|c0=c0|c1=c0"])
# arranhão de disco: ida e volta rápida de afinação com textura de ruído
synth("scratch", ["-f", "lavfi", "-i",
                  "aevalsrc='(0.55+0.45*(random(0)*2-1))*sin(2*PI*(700*t-450*cos(2*PI*5.5*t)/(2*PI*5.5)))*exp(-3*t)':s=48000:d=0.36",
                  "-af", "highpass=f=200,lowpass=f=3500,afade=t=in:d=0.01,afade=t=out:st=0.28:d=0.08,pan=stereo|c0=c0|c1=c0"])
# vine boom: grave encorpado que decai
synth("boom", ["-f", "lavfi", "-i",
               "aevalsrc='tanh(2.2*sin(2*PI*(62*t-10*t*t))*exp(-3.2*t))+0.3*sin(2*PI*124*t)*exp(-6*t)':s=48000:d=1.0",
               "-af", "lowpass=f=900,afade=t=out:st=0.8:d=0.2,pan=stereo|c0=c0|c1=c0"])
# (nome, momento na timeline, volume)
sfx = [
    ("whoosh", so(3) - 0.3, 0.35),            # entra a parte acelerada
    ("ding", so(7) + 0.25, 0.28),             # dica casa/pet shop aparece
    ("shutter", at(10, 303.0), 0.5),          # ela posa com a Lúcia molhada
    ("scratch", at(11, 315.55), 0.3),         # "eu que tô tomando banho?" -> pausa absurda
    ("boom", at(12, 389.15), 0.5),            # "...desse planeta"
]

# ---------- render ----------
inputs, fc, labels = [], [], []
LOOK = "eq=contrast=1.05:saturation=1.12:brightness=0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.03:rm=0.02:bm=-0.02"
for i, (seg, o, d) in enumerate(timeline):
    f, a, b, sp, z, mute = seg
    k = sum(1 for x in inputs if x == "-i"); inputs += ["-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", f"{PROXY}/{f}.mp4"]
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    fc.append(f"[{k}:v]setpts=(PTS-STARTPTS)/{sp},crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2.6,scale={W}:{H},fps=30,setsar=1[v{i}]")
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
fc.append(f"[vc]tpad=stop_mode=clone:stop_duration={END},{LOOK},subtitles='{ass_path}':fontsdir={FONTS},fade=t=out:st={TOTAL+END-0.6:.2f}:d=0.6[vout]")
fc.append(f"[ac]apad=pad_dur={END}[acp]")
mix = ["[acp]"]
for j, (name, when, vol) in enumerate(sfx):
    idx = sum(1 for x in inputs if x == "-i"); inputs += ["-i", f"{OUT}/{name}.wav"]
    ms = int(max(when, 0) * 1000)
    fc.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL+END-0.6:.2f}:d=0.6[aout]")
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/banho_lucia_v1.mp4"]
subprocess.run(cmd, check=True)
print(f"OK duração {TOTAL+END:.1f}s, {len(caps)} legendas")
for i, (seg, o, d) in enumerate(timeline): print(f"seg{i:2d} {o:6.2f}")
for a, b, ch in caps: print(f"{a:6.2f} {' '.join(c[0] for c in ch)}")

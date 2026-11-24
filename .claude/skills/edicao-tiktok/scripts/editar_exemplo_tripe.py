"""Edição de referência APROVADA: unboxing do tripé com IA (versão 11, postada).
Use como modelo para os próximos vídeos: troque SEGS, FIX, overlays e sfx.
Gera: cortes (zoom/velocidade), legendas ASS dinâmicas, títulos/rótulos, sons e render 1080x1920.

Pastas esperadas dentro de WORK (variável de ambiente EDIT_WORK):
  proxy/<nome>.mp4   cópias 1080x1920 dos brutos
  audio/<nome>.m.json transcrição com palavras (scripts/transcrever.py, modelo medium)
  render/            saída
"""
import json, subprocess, os

S = os.environ.get("EDIT_WORK", os.getcwd())
PROXY = f"{S}/proxy"
OUT = f"{S}/render"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")  # Montserrat, Caveat, Poppins (OFL)

# (arquivo, início, fim, velocidade, zoom, mudo)
SEGS = [
    ("IMG_6185", 0.00, 7.40, 1, 1.00, False),   # chegada + gancho
    ("IMG_6185", 8.40, 12.05, 1, 1.15, False),  # não acredito que comprei (sem o 1º "é um tripé")
    ("IMG_6185", 15.20, 19.30, 1, 1.00, False), # não é TikTok Shop, mas tem na vitrine
    ("IMG_6185", 26.35, 27.50, 1, 1.12, False), # olha isso aqui
    ("IMG_6185", 28.95, 34.50, 1, 1.00, False), # tripé com IA + reação
    ("IMG_6185", 34.65, 37.00, 1, 1.20, False), # dá um close
    ("IMG_6185", 38.85, 41.60, 1, 1.00, False), # o babado (sensor)
    ("IMG_6187", 6.90, 9.95, 1, 1.12, False),   # não peguei automático
    ("IMG_6187", 10.60, 16.95, 1, 1.00, False), # tenho medo de quebrar
    ("IMG_6187", 17.00, 27.90, 4, 1.00, True),  # montagem acelerada
    ("IMG_6187", 37.95, 41.00, 1, 1.15, False), # vou ligar (sem repetir "babado")
    ("IMG_6187", 42.50, 44.20, 1, 1.00, False), # tem que reconhecer
    ("IMG_6187", 57.60, 61.20, 1, 1.18, False), # joinha (gesto em 58.1)
    ("IMG_6187", 64.60, 65.70, 1, 1.00, False), # por que não tá me seguindo
    ("IMG_6187", 71.80, 80.90, 1, 1.10, False), # final: ele segue, congela no sorriso
]

# Correções de transcrição (arquivo, tempo da palavra) -> texto
FIX = {
    ("IMG_6185", 9.72): "tô",
    ("IMG_6187", 15.06): "na mão,",
    ("IMG_6187", 40.78): "",          # palavra duplicada pelo whisper
    ("IMG_6185", 4.62): "pra",
    ("IMG_6185", 16.2): "carrinho", ("IMG_6185", 16.34): "", ("IMG_6185", 16.52): "laranja,",
    ("IMG_6185", 16.86): "pra", ("IMG_6185", 17.24): "ficarem",
    ("IMG_6187", 36.6): "", ("IMG_6187", 37.02): "",
    ("IMG_6187", 40.56): "", ("IMG_6187", 40.66): "tá", ("IMG_6187", 40.68): "funcionando,",
    ("IMG_6187", 78.02): "tá vendo?", ("IMG_6187", 78.44): "olha", ("IMG_6187", 78.72): "isso!",
    ("IMG_6187", 78.9): "", ("IMG_6187", 79.06): "", ("IMG_6187", 79.3): "",
}
FIX_TEXT = {"Ó,": "Ó,", "está": "tá"}

words = {f: [w for s in json.load(open(f"{S}/audio/{f}.wav".replace(".wav", ".m.json"))) for w in s["words"]]
         for f in ("IMG_6185", "IMG_6187")}

def ts(t):
    t = max(t, 0)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# ---------- timeline ----------
timeline = []  # (seg, out_start, out_dur)
t = 0.0
for seg in SEGS:
    d = (seg[2] - seg[1]) / seg[3]
    timeline.append((seg, t, d)); t += d
TOTAL = t
END = 3.0  # fechamento: imagem congelada no sorriso + "vale cada centavo", escurecendo até o preto

def out_time(i, src_t):
    seg, o, d = timeline[i]
    return o + (src_t - seg[1]) / seg[3]

# ---------- legendas das falas (dinâmicas: palavra falada em amarelo) ----------
caps = []  # (início, fim, [(palavra, t_ini, t_fim)])
seg_end = []
for i, (seg, o, d) in enumerate(timeline):
    f, a, b, sp, z, mute = seg
    if mute: continue
    chunk = []
    ws = [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.05]
    for w in ws:
        txt = FIX.get((f, round(w["start"], 2)), w["word"].strip())
        txt = FIX_TEXT.get(txt, txt)
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

# ---------- títulos e rótulos (tempo na timeline de saída) ----------
def seg_start(i): return timeline[i][1]
POP = r"{\fscx30\fscy30\t(0,110,\fscx112\fscy112)\t(110,190,\fscx100\fscy100)}"
YEL, PINK, CREAM = r"{\c&H3DD9FF&}", r"{\c&HB45CFF&}", r"{\c&HC8F4FF&}"
WHITE = r"{\c&HFFFFFF&}"
# ---- fechamento: "Isso daqui vale cada centavo" (palavras chegam uma a uma, com pulinho) ----
def bounce_line(words, t_first, step, color_of):
    out, t = "", 0
    for k, w in enumerate(words):
        ms = int((t_first + k * step) * 1000)
        out += (r"{\alpha&HFF&\fscy35\blur6\c%s" % color_of(k)
                + r"\t(%d,%d,\alpha&H00&\fscy128\blur0)\t(%d,%d,\fscy92)\t(%d,%d,\fscy100)}" % (ms, ms + 110, ms + 110, ms + 190, ms + 190, ms + 260)
                + w + (" " if k + 1 < len(words) else ""))
    return out
END_TEXT_T0 = 0.15  # depois que a imagem congela
l1 = bounce_line(["Isso", "daqui", "vale"], END_TEXT_T0, 0.17, lambda k: "&HFFFFFF&")
l2 = bounce_line(["CADA", "CENTAVO"], END_TEXT_T0 + 0.6, 0.2, lambda k: "&HB45CFF&")
END_TEXT = [
    (TOTAL, TOTAL + END, "Title", 540, 300, r"{\fad(0,250)}" + l1),
    (TOTAL, TOTAL + END, "Title", 540, 390, r"{\fad(0,250)\fs86}" + l2),
]
overlays = [
    # gancho (estilo "Melhor DICA pra sua PROVA")
    (seg_start(2) + 2.75, seg_start(2) + 4.1, "Label", 560, 520, r"{\frz-5}" + POP + "tem na vitrine!"),
    (seg_start(4) + 0.2, seg_start(4) + 3.0, "Label", 540, 480, r"{\frz4}" + POP + "com IA?!"),
    (seg_start(6) + 0.3, seg_start(6) + 2.75, "Info", 540, 470, POP + r"{\c&HB45CFF&}[ {\c&HFFFFFF&}sensor de rastreamento {\c&HB45CFF&}]"),
    (seg_start(9), seg_start(9) + timeline[9][2], "Label", 540, 470, r"{\frz-3}" + POP + "montando... (4x)"),
    (seg_start(10) + 0.3, seg_start(10) + 3.0, "Label", 540, 470, r"{\frz3}" + POP + "ligando"),
    (seg_start(12) + 0.5, seg_start(12) + 3.3, "Label", 560, 470, r"{\frz-6}" + POP + "joinha!"),
    (seg_start(13), seg_start(13) + 1.1, "Label", 540, 470, r"{\frz5}" + POP + "ué?"),
    (seg_start(14) + 4.0, TOTAL, "Title", 540, 330, r"{\fad(150,150)}" + r"ELE TÁ " + PINK + r"ME SEGUINDO"),
] + END_TEXT + [
]

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins SemiBold,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,4,2,2,80,80,620,1
Style: Title,Montserrat Thin Black,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,-1,0,0,100,100,-2,0,1,0,6,5,60,60,0,1
Style: Label,Caveat,104,&H00C8F4FF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,0,5,5,60,60,0,1
Style: Info,Poppins SemiBold,56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,4,5,60,60,0,1

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
            body.append("{\\c&H3DD9FF&\\fscx108\\fscy108}" + t2 + "{\\c&HFFFFFF&\\fscx100\\fscy100}" if m == j else t2)
        pop = "{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
        ass += f"Dialogue: 0,{ts(ea)},{ts(eb)},Cap,,0,0,0,,{pop}{' '.join(body)}\n"
for a, b, st, x, y, txt in overlays:
    pos = "" if "\\move" in txt else f"{{\\pos({x},{y})}}"
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},{st},,0,0,0,,{pos}{txt}\n"
TYPE_START, TYPE_STEP, TYPE_END = 0.20, 0.045, 3.6
parts = [("&HFFFFFF&", "Comprei um tripé com"), ("&HFFFFFF&", "\n"), ("&HB45CFF&", "INTELIGÊNCIA "), ("&H3DD9FF&", "ARTIFICIAL")]
chars = [(c, ch) for c, txt in parts for ch in txt]
typed = [i for i, (c, ch) in enumerate(chars) if ch not in " \n"]
key_times = []
for k, n in enumerate(typed):
    a = TYPE_START + k * TYPE_STEP
    b = TYPE_START + (k + 1) * TYPE_STEP if k + 1 < len(typed) else TYPE_END
    key_times.append(a)
    body = ""
    for i, (c, ch) in enumerate(chars):
        vis = i <= n
        tok = r"\N" if ch == "\n" else ch
        body += ("{\\c%s\\alpha&H00&}" % c if vis else "{\\alpha&HFF&}") + tok
    fade = r"{\fad(0,200)}" if k + 1 == len(typed) else ""
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},Title,,0,0,0,,{{\\pos(540,330)}}{fade}{body}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

# ---------- efeitos sonoros sintetizados ----------
def synth(name, expr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *expr, f"{OUT}/{name}.wav"], check=True)
synth("pop", ["-f", "lavfi", "-i", "sine=f=900:d=0.09", "-af", "volume=0.6,afade=t=out:st=0.02:d=0.07,asetrate=44100*1.0,aresample=48000"])
# "passando": ruído que cresce e some, atravessando da esquerda pra direita
synth("whoosh", ["-f", "lavfi", "-i", "anoisesrc=d=0.7:c=brown:a=0.8:r=48000", "-af",
                 "highpass=f=250,lowpass=f=4500,equalizer=f=1800:t=q:w=1:g=6,"
                 "afade=t=in:d=0.38:curve=exp,afade=t=out:st=0.38:d=0.32:curve=exp,"
                 "pan=stereo|c0=c0|c1=c0,aeval=val(0)*(1-t/0.7)|val(1)*(t/0.7):c=stereo,volume=0.45"])
# sons dela (gravação do CapCut): (arquivo, momento do pico na timeline, pico dentro do som, volume)
SONS = f"{S}/sons"
# o som segue a imagem: cada coisa que aparece tem o seu som
def bell(name, notes, d=0.7, vol=1.6):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    synth(name, ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                 f"afade=t=in:d=0.003,aecho=0.8:0.4:45|90:0.25|0.12,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0,volume={vol}"])
bell("plim", [(1568, 0.5, 7, 0), (2349, 0.3, 9, 0), (3136, 0.12, 12, 0)])
bell("bling", [(1318.5, 0.45, 9, 0), (1975.5, 0.5, 7, 0.07), (2637, 0.15, 11, 0.07)], d=0.8)
sfx = [("bling", seg_start(2) + 2.75, 0.0, 0.5, "out"),                 # "tem na vitrine!"
       ("plim", seg_start(4) + 0.2, 0.0, 0.35, "out"),                   # "com IA?!"
       ("plim", seg_start(6) + 0.3, 0.0, 0.3, "out"),                    # "[ sensor de rastreamento ]"
       ("plim", seg_start(12) + 0.5, 0.0, 0.55, "out"),                  # joinha!
       ("plim", TOTAL + END_TEXT_T0 + 0.6 + 0.4, 0.0, 0.5, "out")]       # "CENTAVO" chegando

# ---------- render ----------
BW, BW_SEGS = ",hue=s=0", {13}  # quando algo dá errado: preto e branco ("por que ele não tá me seguindo?")
inputs, fc, vlabels, alabels = [], [], [], []
srcidx = {}
for f in ("IMG_6185", "IMG_6187"):
    srcidx[f] = len(inputs) // 2; inputs += ["-i", f"{PROXY}/{f}.mp4"]
LOOK = "eq=contrast=1.06:saturation=1.14:brightness=0.01,colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03"
for i, (seg, o, d) in enumerate(timeline):
    f, a, b, sp, z, mute = seg
    k = srcidx[f]
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    fc.append(f"[{k}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2.6,scale={W}:{H},fps=30,setsar=1{BW if i in BW_SEGS else ''}[v{i}]")
    if mute:
        # som de acelerada: o áudio real acelerado (4x mais rápido, uma oitava acima)
        fc.append(f"[{k}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  f"asetrate=96000,aresample=48000,atempo=2.0,volume=0.55,atrim=0:{d:.3f},apad=whole_dur={d:.3f},"
                  f"afade=t=in:d=0.08,afade=t=out:st={max(d-0.1,0):.3f}:d=0.1[a{i}]")
    else:
        fc.append(f"[{k}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  f"afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03[a{i}]")
    vlabels.append(f"[v{i}][a{i}]")
n = len(timeline)
ass_path = f"{OUT}/legendas.ass".replace(":", r"\:")
fc.append("".join(vlabels) + f"concat=n={n}:v=1:a=1[vc][ac]")
fc.append(f"[vc]tpad=stop_mode=clone:stop_duration={END},{LOOK},subtitles='{ass_path}':fontsdir={FONTS},fade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[vout]")
fc.append(f"[ac]apad=pad_dur={END}[acp]")
mix = ["[acp]"]
for j, (name, peak, inner, vol, where) in enumerate(sfx):
    idx = len(inputs) // 2; inputs += ["-i", f"{SONS if where == 'sons' else OUT}/{name}.wav"]
    start = peak - inner
    cut = max(-start, 0)
    ms = int(max(start, 0) * 1000)
    fc.append(f"[{idx}:a]atrim=start={cut:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[aout]")

cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/tripe_v11.mp4"]
subprocess.run(cmd, check=True)
print(f"OK duração {TOTAL:.1f}s, {len(caps)} legendas")
for a, b, ch in caps: print(f"{a:6.2f} {' '.join(c[0] for c in ch)}")

"""Arrume-sisi comigo — torneio relâmpago de beach tennis (brutos IMG_6257..6264).
Adaptado de editar_exemplo_tripe.py (estilo aprovado) + MANUAL_SONS.md.
Biblioteca de sons dela NÃO estava disponível: só som real, áudio acelerado real,
o "plim" aprovado e um whoosh suave sintetizado (substituto, avisado no relatório).
"""
import json, subprocess, os

S = os.environ.get("EDIT_WORK", os.getcwd())
PROXY, OUT = f"{S}/proxy", f"{S}/render"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONTS = "/home/user/Claude/.claude/skills/edicao-tiktok/fonts"
FILES = ("IMG_6257", "IMG_6258", "IMG_6259", "IMG_6262", "IMG_6263", "IMG_6264")

# (arquivo, início, fim, velocidade, zoom, mudo)
SEGS = [
    ("IMG_6257", 8.50, 11.35, 1, 1.00, False),   # 0 gancho: arrume-se comigo p/ torneio relâmpago (2ª tomada)
    ("IMG_6257", 17.55, 20.75, 1, 1.15, False),  # 1 olha que eu tenho um tripé que me segue agora
    ("IMG_6257", 21.55, 23.10, 1, 1.00, False),  # 2 não, silêncio, deixa eu blogueira
    ("IMG_6257", 32.90, 35.30, 1, 1.12, False),  # 3 fim de semana agitado
    ("IMG_6257", 36.15, 41.10, 1, 1.00, False),  # 4 mista de manhã, feminina à tarde
    ("IMG_6257", 41.80, 44.10, 1, 1.15, False),  # 5 sábado descansar e talvez treinar
    ("IMG_6257", 44.45, 46.40, 1, 1.00, False),  # 6 não, na verdade talvez não. tenho que treinar (quebra)
    ("IMG_6257", 46.80, 50.75, 1, 1.15, False),  # 7 domingo APENAS uma corrida
    ("IMG_6257", 55.40, 59.20, 1, 1.00, False),  # 8 Garmin mandou descansar
    ("IMG_6257", 59.95, 60.95, 1, 1.18, False),  # 9 tadinho dele
    ("IMG_6258", 6.85, 10.45, 1, 1.00, False),   # 10 minha roupa vai ser um conjunto
    ("IMG_6258", 27.90, 33.80, 1, 1.00, False),  # 12 sustentação absurda... fica 10
    ("IMG_6259", 13.30, 14.60, 1, 1.00, False),  # 13 REVELAÇÃO: vestida (mãos na cintura 13.8)
    ("IMG_6259", 20.00, 23.20, 1, 1.12, False),  # 14 esse conjunto é maravilhoso
    ("IMG_6259", 23.50, 25.20, 1, 1.00, False),  # 15 me sinto a bailarina (braços pra cima)
    ("IMG_6259", 29.15, 31.10, 1, 1.12, False),  # 16 não nasci com coordenação
    ("IMG_6259", 36.05, 40.70, 1, 1.00, False),  # 17 balé, jazz, hip hop, nada deu certo
    ("IMG_6262", 10.90, 12.95, 1, 1.00, False),  # 18 bora arrumar a cara em dois segundos
    ("IMG_6262", 13.80, 16.40, 1, 1.15, False),  # 19 adivinha? atrasada!
    ("IMG_6262", 23.30, 25.00, 1, 1.00, False),  # 20 vou arrumar o meu cabelo
    ("IMG_6262", 31.65, 34.90, 1, 1.12, False),  # 21 não vai dar pra fazer o que eu queria
    ("IMG_6262", 35.00, 39.40, 4, 1.00, True),   # 22 prendendo o cabelo (4x)
    ("IMG_6262", 64.05, 70.75, 1, 1.15, False),  # 23 colar do TikTok Shop
    ("IMG_6262", 84.85, 86.70, 1, 1.15, False),  # 25 ah não, esqueci a xuxinha
    ("IMG_6263", 0.40, 3.15, 1, 1.00, False),    # 26 blushzinho
    ("IMG_6263", 3.20, 7.45, 1, 1.12, False),    # 27 prendi o cabelo, sem criatividade
    ("IMG_6263", 8.80, 11.95, 1, 1.00, False),   # 28 e sem tempo, como sempre
    ("IMG_6263", 12.35, 14.20, 1, 1.15, False),  # 29 agora fala uma novidade
    ("IMG_6263", 21.85, 25.40, 1, 1.00, False),  # batidinha de pó e bora
    ("IMG_6264", 0.55, 5.70, 1, 1.00, False),    # 32 pronto gente: look final
    ("IMG_6264", 9.75, 14.85, 1, 1.12, False),   # 33 grips SpinGrip, na vitrine
    ("IMG_6264", 23.80, 26.05, 1, 1.00, False),  # 34 hoje foi express, beijo! (congela no beijo)
]
NOCAP = {12}  # fala ininteligível na revelação: sem legenda

FIX = {
    ("IMG_6257", 8.62): "Arrume-sisi", ("IMG_6257", 8.88): "", ("IMG_6257", 8.98): "",
    ("IMG_6257", 9.38): "pra", ("IMG_6257", 10.5): "beach tennis?",
    ("IMG_6257", 56.04): "Garmin",
    ("IMG_6258", 33.4): "10!",
    ("IMG_6259", 36.78): "viu,", ("IMG_6259", 36.36): "tentou,",
    ("IMG_6259", 38.08): "balé,", ("IMG_6259", 38.58): "jazz,", ("IMG_6259", 39.32): "hop...",
    ("IMG_6259", 30.58): "pra",
    ("IMG_6262", 86.11): "xuxinha!",
    ("IMG_6263", 6.0): "tô", ("IMG_6263", 9.26): "tempo,", ("IMG_6263", 21.98): "batidinha",
    ("IMG_6263", 4.36): "só,", ("IMG_6263", 2.44): "aqui,",
    ("IMG_6264", 24.82): "express.", ("IMG_6264", 23.88): "Arrume-sisi", ("IMG_6264", 24.04): "",
    ("IMG_6259", 29.22): "",
}
FIX_TEXT = {"para": "pra", "está": "tá", "estava": "tava"}

words = {f: [w for s in json.load(open(f"{S}/audio/{f}.m.json")) for w in s["words"]] for f in FILES}

def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

timeline, t = [], 0.0
for seg in SEGS:
    d = (seg[2] - seg[1]) / seg[3]; timeline.append((seg, t, d)); t += d
TOTAL = t
END = 3.0

def out_time(i, src_t):
    seg, o, d = timeline[i]; return o + (src_t - seg[1]) / seg[3]

caps, seg_end = [], []
for i, (seg, o, d) in enumerate(timeline):
    f, a, b, sp, z, mute = seg
    if mute or i in NOCAP: continue
    chunk = []
    for w in [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.05]:
        txt = FIX.get((f, round(w["start"], 2)), w["word"].strip())
        txt = FIX_TEXT.get(txt, txt)
        if not txt: continue
        chunk.append((txt, out_time(i, max(w["start"], a)), out_time(i, min(w["end"], b))))
        if len(chunk) >= 3 or txt[-1] in ",.?!":
            caps.append(chunk); seg_end.append(o + d); chunk = []
    if chunk: caps.append(chunk); seg_end.append(o + d)
fixed = []
for k, ch in enumerate(caps):
    a, b = ch[0][1], ch[-1][2]
    nxt = caps[k + 1][0][1] if k + 1 < len(caps) else TOTAL
    fixed.append((a, min(max(b + 0.15, a + 0.35), nxt, b + 0.4, seg_end[k]), ch))
caps = fixed

def ss(i): return timeline[i][1]
def sd(i): return timeline[i][2]
def at(i, src_t): return out_time(i, src_t)
POP = r"{\fscx30\fscy30\t(0,110,\fscx112\fscy112)\t(110,190,\fscx100\fscy100)}"
PINK, WHITE = r"{\c&HB45CFF&}", r"{\c&HFFFFFF&}"

def bounce_line(ws, t_first, step, color_of):
    out = ""
    for k, w in enumerate(ws):
        ms = int((t_first + k * step) * 1000)
        out += (r"{\alpha&HFF&\fscy35\blur6\c%s" % color_of(k)
                + r"\t(%d,%d,\alpha&H00&\fscy128\blur0)\t(%d,%d,\fscy92)\t(%d,%d,\fscy100)}" % (ms, ms + 110, ms + 110, ms + 190, ms + 190, ms + 260)
                + w + (" " if k + 1 < len(ws) else ""))
    return out
END_T0 = 0.15
l1 = bounce_line(["Arrume-sisi", "comigo"], END_T0, 0.17, lambda k: "&HFFFFFF&")
l2 = bounce_line(["EXPRESS", "✦"], END_T0 + 0.45, 0.2, lambda k: "&H3DD9FF&" if k == 1 else "&HB45CFF&")

overlays = [
    (at(6, 44.54), at(6, 46.30), "Label", 560, 470, r"{\frz-5}" + POP + "mudou de ideia"),
    (at(7, 47.95), ss(7) + sd(7), "Label", 540, 470, r"{\frz4}" + POP + "apenas?!"),
    (at(12, 13.75), ss(12) + sd(12), "Label", 560, 470, r"{\frz-5}" + POP + "fica 10!"),
    (at(14, 23.95), ss(14) + sd(14), "Label", 540, 470, r"{\frz4}" + POP + "bailarina?"),
    (at(18, 15.70), ss(18) + sd(18), "Label", 540, 470, r"{\frz-4}" + POP + "atrasada!"),
    (ss(21), ss(21) + sd(21), "Label", 540, 470, r"{\frz-3}" + POP + "prendendo... (4x)"),
    (at(22, 65.6), at(22, 69.0), "Info", 540, 470, POP + PINK + "[ " + WHITE + "colar do TikTok Shop " + PINK + "]"),
    (at(29, 2.5), ss(29) + sd(29), "Label", 540, 470, r"{\frz-5}" + POP + "look pronto!"),
    (at(30, 11.2), at(30, 14.8), "Info", 540, 470, POP + PINK + "[ " + WHITE + "grips SpinGrip • na vitrine " + PINK + "]"),
    (TOTAL, TOTAL + END, "Title", 540, 300, r"{\fad(0,250)}" + l1),
    (TOTAL, TOTAL + END, "Title", 540, 390, r"{\fad(0,250)\fs86}" + l2),
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
Style: Info,Poppins SemiBold,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,4,5,60,60,0,1

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
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},{st},,0,0,0,,{{\\pos({x},{y})}}{txt}\n"
# gancho digitado letra por letra (sem som de teclado)
TYPE_START, TYPE_STEP, TYPE_END = 0.20, 0.045, ss(1) + 0.4
parts = [("&HFFFFFF&", "Arrume-sisi comigo pro"), ("&HFFFFFF&", "\n"), ("&HB45CFF&", "TORNEIO "), ("&H3DD9FF&", "RELÂMPAGO ✦")]
chars = [(c, ch) for c, txt in parts for ch in txt]
typed = [i for i, (c, ch) in enumerate(chars) if ch not in " \n"]
for k, n in enumerate(typed):
    a = TYPE_START + k * TYPE_STEP
    b = TYPE_START + (k + 1) * TYPE_STEP if k + 1 < len(typed) else TYPE_END
    body = ""
    for i, (c, ch) in enumerate(chars):
        tok = r"\N" if ch == "\n" else ch
        body += ("{\\c%s\\alpha&H00&}" % c if i <= n else "{\\alpha&HFF&}") + tok
    fade = r"{\fad(0,200)}" if k + 1 == len(typed) else ""
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},Title,,0,0,0,,{{\\pos(540,330)}}{fade}{body}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

def synth(name, expr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *expr, f"{OUT}/{name}.wav"], check=True)
def bell(name, notes, d=0.7, vol=1.6):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    synth(name, ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                 f"afade=t=in:d=0.003,aecho=0.8:0.4:45|90:0.25|0.12,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0,volume={vol}"])
bell("plim", [(1568, 0.5, 7, 0), (2349, 0.3, 9, 0), (3136, 0.12, 12, 0)])
# whoosh SUAVE sintetizado (substituto do whoosh_soft.wav que não veio): curto, abafado, passa da esq. p/ dir.
synth("whoosh_suave", ["-f", "lavfi", "-i", "anoisesrc=d=0.5:c=pink:a=0.6:r=48000", "-af",
                       "highpass=f=300,lowpass=f=2500,afade=t=in:d=0.28:curve=exp,afade=t=out:st=0.28:d=0.22:curve=exp,"
                       "pan=stereo|c0=c0|c1=c0,aeval=val(0)*(1-t/0.5)|val(1)*(t/0.5):c=stereo,volume=0.35"])
# (som, momento do pico na timeline, pico dentro do som, volume)
sfx = [
    ("plim", at(12, 13.80), 0.0, 0.45),            # revelação do look (mãos na cintura)
    ("whoosh_suave", ss(17) - 0.12, 0.28, 0.5),           # muda de ambiente: closet -> penteadeira
    ("whoosh_suave", ss(29) - 0.12, 0.28, 0.5),           # muda de ambiente: penteadeira -> look pronto
    ("plim", at(30, 11.2), 0.0, 0.3),              # grips aparecem em destaque
    ("plim", TOTAL + END_T0 + 0.45 + 0.1, 0.0, 0.5),  # "EXPRESS" chegando
]

BW_SEGS = set()
LOOK = "eq=contrast=1.06:saturation=1.14:brightness=0.01,colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03"
SEGDIR = f"{OUT}/segs"; os.makedirs(SEGDIR, exist_ok=True)
def render_segs():
    lst = []
    for i, (seg, o, d) in enumerate(timeline):
        f, a, b, sp, z, mute = seg
        cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
        vf = f"setpts=(PTS-STARTPTS)/{sp},crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2.6,scale={W}:{H},fps=30,setsar=1"
        if mute:
            af = (f"asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,asetrate=96000,aresample=48000,atempo=2.0,"
                  f"volume=0.55,atrim=0:{d:.3f},apad=whole_dur={d:.3f},afade=t=in:d=0.08,afade=t=out:st={max(d-0.1,0):.3f}:d=0.1")
        else:
            af = f"asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03"
        o_ = f"{SEGDIR}/s{i:02d}.mkv"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a}", "-t", f"{b-a:.3f}", "-i", f"{PROXY}/{f}.mp4",
                        "-vf", vf, "-af", af, "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                        "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", o_], check=True)
        lst.append(f"file '{o_}'")
    open(f"{SEGDIR}/list.txt", "w").write("\n".join(lst) + "\n")

ass_path = f"{OUT}/legendas.ass".replace(":", r"\:")
inputs = ["-f", "concat", "-safe", "0", "-i", f"{SEGDIR}/list.txt"]
fc = [f"[0:v]tpad=stop_mode=clone:stop_duration={END},{LOOK},subtitles='{ass_path}':fontsdir={FONTS},fade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[vout]",
      f"[0:a]apad=pad_dur={END}[acp]"]
mix = ["[acp]"]
for j, (name, peak, inner, vol) in enumerate(sfx):
    idx = len(inputs) // 2 - 2; inputs += ["-i", f"{OUT}/{name}.wav"]
    start = peak - inner; cut = max(-start, 0); ms = int(max(start, 0) * 1000)
    fc.append(f"[{idx}:a]atrim=start={cut:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[aout]")

if os.environ.get("DRY"):
    print(f"duração {TOTAL+END:.1f}s")
    for a, b, ch in caps: print(f"{a:6.2f} {' '.join(c[0] for c in ch)}")
    for name, peak, inner, vol in sfx: print(f"SFX {peak:6.2f} {name}")
    raise SystemExit
if not os.environ.get("SKIPSEGS"): render_segs()
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/grwm_beach_tennis_v1.mp4"]
subprocess.run(cmd, check=True)
print(f"OK duração {TOTAL+END:.1f}s")

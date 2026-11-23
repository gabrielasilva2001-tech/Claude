"""Edição APROVADA e postada: "Construindo uma Arena" (crítica irônica com fotos de exemplo).
Modelo para vídeos no formato "fala + fotos de exemplo aparecendo". Copie e troque SEGS, FIX, fotos e rótulos.
Entradas em EDIT_WORK: brutos/<bruto>.mov, audio/<bruto>.m.json, fotos/escolhidas.json, fotos/rotulos.json, fotos/<imagens>.
Use --preview para uma prévia rápida em 1080 antes do 4K.

Arena de beach tennis (crítica irônica) — fotos de exemplo, legenda simples, título "Construindo uma Arena".
Render final direto do .mov original em 4K vertical (2160x3840), sem perda de qualidade.
"""
import json, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFilter

S = os.environ["EDIT_WORK"]
SRC = f"{S}/brutos/IMG_6578.mov"
OUT = f"{S}/render"; os.makedirs(OUT, exist_ok=True)
CARDS = f"{S}/fotos/cards"; os.makedirs(CARDS, exist_ok=True)
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")  # Montserrat, Caveat, Poppins (OFL)
W, H = 2160, 3840          # saída 4K vertical
PW, PH = 1080, 1920        # coordenadas das legendas (libass escala)
PREVIEW = "--preview" in sys.argv   # render rápido em 1080 só para conferir

# (início, fim, zoom) no tempo do bruto
SEGS = [
    (14.28, 17.50, 1.00),   # aqui a gente vai abrir uma arena de beach tennis
    (19.78, 20.72, 1.12),   # então vamos lá
    (24.12, 26.56, 1.00),   # primeiro a gente vai escolher um terreno bem pequeno
    (27.48, 36.06, 1.12),   # porque não precisa de muito espaço... quadra do lado da outra... reflexo
    (37.55, 45.85, 1.00),   # areia grossa, pedrinha, joelho esfolado
    (55.00, 62.56, 1.12),   # arquibancada para cinco pessoas... em pé mesmo
    (79.20, 85.12, 1.00),   # banheiro feminino, um só
    (87.30, 93.38, 1.12),   # chuveiro sem porta
    (97.82, 103.22, 1.00),  # como só tem um banheiro, fecha inteiro
    (107.00, 114.20, 1.12), # torneio 150 de inscrição, premiação 80
    (123.45, 125.68, 1.00), # porque o importante é participar e fazer amizade
    (145.56, 149.84, 1.12), # torneio sem horário para acabar
    (151.08, 152.64, 1.00), # porque o importante é viver o momento
    (155.45, 158.56, 1.12), # organização decide os horários em cima da hora
    (159.66, 165.20, 1.00), # nada melhor do que ficar o dia inteiro sem saber
    (191.45, 195.52, 1.12), # posição das quadras diretamente para o sol
    (196.44, 197.98, 1.00), # porque a graça é usar o óculos
    (224.20, 232.85, 1.12), # para finalizar... experiência inesquecível... não vai esquecer
    (234.08, 237.40, 1.00), # pronto, agora é só abrir as portas (olha pra câmera)
]

# correções da transcrição (tempo da palavra no bruto) -> texto
FIX = {17.18: "beach", 17.38: "tennis.", 28.96: "espaço,", 232.50: "esquecer.",
       14.28: "Aqui", 155.50: "E", 224.50: "Para", 145.54: "Sobre"}

words = [w for s in json.load(open(f"{S}/audio/IMG_6578.m.json")) for w in s["words"]]
# a retomada do "primeiro a gente vai escolher..." (24.1s) não foi separada pelo whisper: texto manual
MANUAL = {2: [("Primeiro", 24.15), ("a", 24.45), ("gente", 24.52), ("vai", 24.70), ("escolher", 24.82),
              ("um", 25.20), ("terreno", 25.30), ("bem", 25.80), ("pequeno,", 26.00)]}

timeline, t = [], 0.0
SEGS = [(a - 0.04, b + 0.25, z) for a, b, z in SEGS]
for seg in SEGS:
    d = round((seg[1] - seg[0]) * 30) / 30; timeline.append((seg, t, d)); t += d
TOTAL = t
def out_t(i, src): seg, o, d = timeline[i]; return o + (src - seg[0])
def ts(x):
    x = max(x, 0); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"

# ---------- legenda simples: 2–4 palavras, branca com contorno ----------
caps = []
for i, (seg, o, d) in enumerate(timeline):
    a, b, _ = seg
    if i in MANUAL:
        ws = [(txt, ws_) for txt, ws_ in MANUAL[i]]
        ends = [x[1] for x in ws[1:]] + [b]
        ws = [(txt, s0, e0) for (txt, s0), e0 in zip(ws, ends)]
    else:
        ws = [(FIX.get(round(w["start"], 2), w["word"].strip()), w["start"], min(w["end"], b))
              for w in words if a - 0.05 <= w["start"] < b - 0.08]
    chunk = []
    for txt, s0, e0 in ws:
        if not txt: continue
        chunk.append((txt, out_t(i, max(s0, a)), out_t(i, e0)))
        if len(chunk) >= 4 or (len(chunk) >= 2 and txt[-1] in ",.?!"):
            caps.append((chunk, o + d)); chunk = []
    if chunk: caps.append((chunk, o + d))
cap_ev = []
for k, (ch, seg_end) in enumerate(caps):
    a = ch[0][1]; b = ch[-1][2]
    nxt = caps[k + 1][0][0][1] if k + 1 < len(caps) else TOTAL
    cap_ev.append((a, min(max(b + 0.25, a + 0.5), nxt, seg_end), " ".join(c[0] for c in ch).rstrip(",")))

# ---------- fotos de exemplo (aparecem na parede, acima dela) ----------
def at(src):  # tempo do bruto -> tempo de saída
    for i, (seg, o, d) in enumerate(timeline):
        if seg[0] - 0.01 <= src <= seg[1] + 0.01: return out_t(i, src)
    raise ValueError(src)
FOTOS = json.load(open(f"{S}/fotos/escolhidas.json"))   # [{key, file, t0, t1, rot}]
def make_card(src_path, rot, dst):
    im = Image.open(src_path).convert("RGB")
    maxw, maxh = 1080, 820
    im.thumbnail((maxw, maxh), Image.LANCZOS) if im.width > maxw or im.height > maxh else None
    sc = min(maxw / im.width, maxh / im.height); im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    bd = 20
    card = Image.new("RGBA", (im.width + 2 * bd, im.height + 2 * bd), (255, 255, 255, 255))
    card.paste(im, (bd, bd))
    mask = Image.new("L", card.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, *card.size], 34, fill=255)
    card.putalpha(mask)
    pad = 80
    canvas = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); shm = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(shm).rounded_rectangle([pad, pad + 18, pad + card.width, pad + card.height + 18], 34, fill=120)
    sh.putalpha(shm.filter(ImageFilter.GaussianBlur(28)))
    canvas = Image.alpha_composite(sh, canvas); canvas.alpha_composite(card, (pad, pad))
    canvas = canvas.rotate(rot, resample=Image.BICUBIC, expand=True)
    canvas.save(dst)

# ---------- títulos / rótulos (coordenadas 1080x1920) ----------
POP = r"{\fscx30\fscy30\t(0,110,\fscx112\fscy112)\t(110,190,\fscx100\fscy100)}"
LABELS = json.load(open(f"{S}/fotos/rotulos.json"))     # [{t0 (bruto), t1 (bruto), x, y, rot, style, text}]

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {PW}
PlayResY: {PH}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins SemiBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,4,1,2,90,90,560,1
Style: Title,Montserrat Thin Black,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,-1,0,0,100,100,-2,0,1,0,6,5,60,60,0,1
Style: Label,Caveat,100,&H00C8F4FF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,0,5,5,60,60,0,1
Style: Info,Poppins SemiBold,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,4,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for a, b, txt in cap_ev:
    ass += f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{txt}\n"
for L in LABELS:
    a, b = at(L["t0"]), at(L["t1"])
    ass += f"Dialogue: 2,{ts(a)},{ts(b)},{L['style']},,0,0,0,,{{\\pos({L['x']},{L['y']})\\frz{L['rot']}}}{POP}{L['text']}\n"

# título digitado letra por letra: "Construindo / uma ARENA ✦"
TYPE_START, TYPE_STEP, TYPE_END = 0.10, 0.055, 2.10
parts = [("&HFFFFFF&", "Construindo"), ("&HFFFFFF&", "\n"), ("&HFFFFFF&", "uma "), ("&HB45CFF&", "ARENA")]
chars = [(c, ch) for c, txt in parts for ch in txt]
typed = [i for i, (c, ch) in enumerate(chars) if ch not in " \n"]
for k, n in enumerate(typed):
    a = TYPE_START + k * TYPE_STEP
    b = TYPE_START + (k + 1) * TYPE_STEP if k + 1 < len(typed) else TYPE_END
    body = "".join((("{\\c%s\\alpha&H00&}" % c) if i <= n else "{\\alpha&HFF&}") + (r"\N" if ch == "\n" else ch)
                   for i, (c, ch) in enumerate(chars))
    fade = r"{\fad(0,250)}" if k + 1 == len(typed) else ""
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},Title,,0,0,0,,{{\\pos(540,470)}}{fade}{body}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

# ---------- render ----------
ow, oh = (PW, PH) if PREVIEW else (W, H)
k2 = ow / W
LOOK = "eq=contrast=1.05:saturation=1.10,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02"
# etapa 1: cada trecho vira um arquivo intermediário quase sem perda (CRF 10) — evita decodificar o 4K várias vezes
SEGDIR = f"{OUT}/segs_{ow}"; os.makedirs(SEGDIR, exist_ok=True)
lst = []
for i, (seg, o, d) in enumerate(timeline):
    a, b, z = seg
    cw, ch = int(ow / z) // 2 * 2, int(oh / z) // 2 * 2
    nf = round(d * 30)
    dst = f"{SEGDIR}/s{i:02d}_{a}_{b}_{z}.mkv"
    if not os.path.exists(dst):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a}", "-i", SRC, "-t", f"{d:.3f}",
            "-vf", f"scale={ow}:{oh}:flags=lanczos,crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2.6,scale={ow}:{oh}:flags=lanczos,fps=30,setsar=1,{LOOK}",
            "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03",
            "-frames:v", str(nf), "-c:v", "libx264", "-preset", "fast", "-crf", "10", "-pix_fmt", "yuv420p", "-threads", "4",
            "-c:a", "pcm_s16le", dst + ".tmp.mkv"], check=True)
        os.rename(dst + ".tmp.mkv", dst)
    lst.append(f"file '{dst}'")
open(f"{SEGDIR}/lista.txt", "w").write("\n".join(lst) + "\n")
inputs = ["-f", "concat", "-safe", "0", "-i", f"{SEGDIR}/lista.txt"]; fc = []; nin = 1
fc.append("[0:a]aresample=async=1[ac]")
cur = "[0:v]"
for j, F in enumerate(FOTOS):
    card = f"{CARDS}/{F['key']}.png"
    make_card(f"{S}/fotos/{F['file']}", F.get("rot", 0), card)
    a, b = at(F["t0"]), at(F["t1"])
    idx = nin; nin += 1; inputs += ["-loop", "1", "-framerate", "30", "-t", f"{b - a + 0.1:.2f}", "-i", card]
    cx, cy = int(ow * 0.5), int(oh * F.get("y", 0.25))
    # pulinho: 60% -> 106% -> 100% em 0,25 s; some com fade rápido
    s = "if(lt(t,0.15),0.6+0.46*t/0.15,if(lt(t,0.25),1.06-0.06*(t-0.15)/0.1,1))"
    fc.append(f"[{idx}:v]format=rgba,scale=w='trunc(iw*{k2}*({s})/2)*2':h='trunc(ih*{k2}*({s})/2)*2':eval=frame:flags=bicubic,"
              f"fade=t=out:st={b - a - 0.12:.2f}:d=0.12:alpha=1,setpts=PTS-STARTPTS+{a:.3f}/TB[p{j}]")
    fc.append(f"{cur}[p{j}]overlay=x='{cx}-w/2':y='{cy}-h/2':eval=frame:enable='between(t,{a:.3f},{b:.3f})'[o{j}]")
    cur = f"[o{j}]"
ass_path = f"{OUT}/legendas.ass"
fc.append(f"{cur}subtitles='{ass_path}':fontsdir={FONTS},fade=t=out:st={TOTAL-0.5:.2f}:d=0.5[vout]")
fc.append(f"[ac]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL-0.5:.2f}:d=0.5[aout]")
name = "arena_preview.mp4" if PREVIEW else "arena_4k.mp4"
venc = (["-c:v", "libx264", "-preset", "veryfast", "-crf", "23"] if PREVIEW else
        ["-c:v", "libx264", "-preset", "fast", "-crf", "16", "-profile:v", "high", "-level", "5.2"])
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", *venc, "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-colorspace", "bt709", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/{name}"]
subprocess.run(cmd, check=True)
print(f"OK {name} duração {TOTAL:.1f}s, {len(cap_ev)} legendas")
for a, b, txt in cap_ev: print(f"{a:6.2f}-{b:6.2f} {txt}")

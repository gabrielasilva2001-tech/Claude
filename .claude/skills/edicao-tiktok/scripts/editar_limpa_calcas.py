"""Uma limpa no guarda-roupa — ep. 1: Calças.
Baseado em scripts/editar_exemplo_tripe.py, no formato da referência (texto amarelo-creme arredondado,
título digitado ATRÁS dela, cartão de categoria com ✨, veredito "fica"/"vai embora")."""
import json, subprocess, os

S = os.path.dirname(os.path.abspath(__file__))
PROXY, OUT = f"{S}/proxy", f"{S}/render"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONTS = "/home/user/Claude/.claude/skills/edicao-tiktok/fonts"
VERSAO = os.environ.get("VERSAO", "v1")

# (arquivo, início, fim)   — zoom alterna sozinho a cada corte
SEGS = [
    ("6380", 4.50, 9.95),    # intro: quantidade considerável de calças... o que vai ficar, o que vai sair
    ("6385", 9.74, 15.95),   # primeira calça cintura baixa depois que emagreci, apego emocional
    ("6385", 23.15, 25.10),  # então ela fica
    ("6388", 6.50, 9.85),    # de quando eu era bem gordinha
    ("6388", 13.10, 14.80),  # porque eu amava calça com bolso
    ("6388", 23.10, 26.90),  # hoje eu já não amo, então ela vai sair
    ("6389", 3.75, 8.85),    # calça sujinha, eu amo ela, só que olha o tamanho dessa barra
    ("6389", 35.75, 40.00),  # mas ela fica por enquanto, se eu não arrumar, tchau
    ("6390", 17.40, 21.70),  # apego emocional, adoro usar em tempos chuvosos
    ("6390", 22.15, 26.60),  # tá ficando branca, vai ter que sair
    ("6391", 1.75, 3.95),    # essa daqui eu uso pra trabalhar
    ("6391", 8.65, 12.10),   # tá vendo aqui? fazendo até onda de tão usada
    ("6391", 12.90, 14.30),  # vai ter que sair
    ("6393", 1.90, 3.05),    # outra de trabalho
    ("6393", 4.86, 7.85),    # a não ser essa boca de sino no meio da canela
    ("6393", 16.50, 17.90),  # então ela vai sair
    ("6394", 7.30, 10.65),   # comprei no desespero pra ir pro Chile, ela é G
    ("6394", 24.80, 26.20),  # ela vai ficar
    ("6395", 8.25, 9.95),    # mesma história, bolso
    ("6395", 28.10, 31.95),  # o problema mesmo é esse bolso
    ("6395", 36.05, 37.30),  # então ela sai
    ("6396", 11.85, 13.40),  # calça preta de camurça
    ("6396", 15.90, 17.85),  # mas mesma história, cheia de bolso
    ("6396", 20.10, 24.10),  # tá saindo a cor, coitada... então ela sai
    ("6396", 39.20, 40.10),  # olha isso aqui
    ("6396", 46.10, 48.40),  # já saiu a maioria das tachinhas que tinha aqui
    ("6396", 52.00, 53.60),  # infelizmente vai ter que sair
    ("6396", 67.95, 69.90),  # gente, que tanta coisa que tá saindo
    ("6397", 12.15, 15.95),  # só coloquei no corpo pra verem o tanto que ela é icônica
    ("6398", 11.10, 13.95),  # maravilhosa, tem pelinho por dentro
    ("6398", 15.05, 16.80),  # ela com certeza fica
    ("6399", 1.65, 5.95),    # outra que nem vou experimentar, enorme, preto desbotado
    ("6399", 9.40, 11.10),   # e vai sair
    ("6401", 8.35, 12.05),   # amo essa calça pra ir em rodeio
    ("6401", 25.50, 26.95),  # gosto do brilho, brilho sutil
    ("6401", 31.50, 33.20),  # e ela fica
    ("6403", 1.90, 3.55),    # essa calça aqui foi um
    ("6403", 6.95, 11.50),   # acontecimento quando eu comprei, abalou as estruturas
    ("6403", 24.10, 25.10),  # fica
    ("6404", 9.25, 11.05),   # eu amei, fiquei obcecada nessa calça
    ("6404", 13.75, 17.75),  # às vezes é bom dar uma ousadinha com a calça diferente
    ("6404", 21.78, 22.50),  # eu comprei outra
    ("6405", 37.45, 42.95),  # a que eu queria era aquela rosinha com vermelho, listrada
    ("6405", 43.40, 44.30),  # mas essa azul
    ("6405", 49.75, 51.80),  # então, eu amei
    ("6406", 2.45, 5.40),    # paguei caríssimo nela
    ("6406", 8.15, 9.60),    # mas ela tá muito larga
    ("6406", 10.40, 11.95),  # não me valorizou muito
    ("6406", 33.80, 35.90),  # essa aqui vocês vão ter que me ajudar
    ("6407", 4.05, 7.60),    # tava em uma pegada de bolso, né galera?
    ("6407", 13.60, 16.95),  # mas esses bolsos me pegam um pouco
    ("6407", 21.05, 23.10),  # vai ficar só porque ela é marrom
    ("6407", 25.00, 27.30),  # mas eu não amo ela
    ("6408", 22.15, 31.40),  # tenho comprado cintura baixa, autoestima elevada... ela vai ficar
    ("6409", 1.15, 4.45),    # calça de couro pro Chile, não usei
    ("6409", 11.70, 13.40),  # então eu gosto, ela vai ficar
    ("6409", 14.65, 18.40),  # paguei tipo 40 reais no TikTok Shop
    ("6412", 2.20, 3.35),    # essa calça branca
    ("6412", 4.45, 5.70),    # eu uso muito na praia
    ("6412", 7.95, 10.35),   # só praia mesmo, ela vai ficar
    ("6412", 10.50, 14.45),  # comprei na Shein há uns 5, 6 anos, toda surrada
    ("6412", 15.05, 20.15),  # gosto muito dela, mas não sei se vai ou se fica
    ("6412", 46.20, 47.70),  # isso foi tudo que saiu
    ("6412", 61.50, 66.50),  # ainda tenho muita coisa pra tirar... cropped, blusinha
    ("6412", 80.50, 81.05),  # beijo! (congela no sorriso)
]
FILES = sorted({s[0] for s in SEGS})

FIX = {
    ("6396", 12.90): "camurça,", ("6396", 50.20): "surradinho",
    ("6401", 10.96): "rodeio", ("6390", 21.24): "chuvosos,",
    ("6412", 11.40): "Shein", ("6407", 11.42): "deixa",
}
words = {f: [w for s in json.load(open(f"{S}/audio/IMG_{f}.m.json")) for w in s["words"]] for f in FILES}

def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# tira as pausas dentro de cada trecho (corte seco), mantendo o "rabinho" depois da última palavra
GAP, PRE, POST = 0.42, 0.08, 0.14
pieces = []
for f, a, b in SEGS:
    ws = [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.05]
    cur = a
    for w1, w2 in zip(ws, ws[1:]):
        if w2["start"] - w1["end"] > GAP and f != "6380":
            pieces.append((f, cur, w1["end"] + POST)); cur = w2["start"] - PRE
    pieces.append((f, cur, b))
SEGS = [(f, round(a * 30) / 30, round(b * 30) / 30) for f, a, b in pieces]   # grade de quadros (30 fps)
timeline, t = [], 0.0
for i, seg in enumerate(SEGS):
    d = seg[2] - seg[1]
    z = 1.0 if i % 2 == 0 else 1.08
    timeline.append((seg, t, d, z)); t += d
TOTAL = t
END = 3.0
INTRO = timeline[0][2]

def at(f, src_t):
    for seg, o, d, z in timeline:
        if seg[0] == f and seg[1] - 0.01 <= src_t <= seg[2] + 0.01:
            return o + src_t - seg[1]
    raise ValueError((f, src_t))
def seg_end_at(f, src_t):
    for seg, o, d, z in timeline:
        if seg[0] == f and seg[1] - 0.01 <= src_t <= seg[2] + 0.01:
            return o + d

# ---------- legendas das falas (dinâmicas) — não na intro (lá entram as palavras grandes) ----------
caps, seg_end = [], []
for i, (seg, o, d, z) in enumerate(timeline):
    if i == 0: continue
    f, a, b = seg
    chunk = []
    for w in [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.05]:
        txt = FIX.get((f, round(w["start"], 2)), w["word"].strip())
        if not txt: continue
        if txt.startswith("-") and chunk:
            p = chunk[-1]; chunk[-1] = (p[0] + txt, p[1], o + min(w["end"], b) - a); continue
        st = o + w["start"] - a
        if chunk and st <= chunk[-1][1] + 0.1: st = chunk[-1][1] + 0.12
        chunk.append((txt, st, max(o + min(w["end"], b) - a, st + 0.1)))
        if len(chunk) >= 3 or txt[-1] in ",.?!":
            caps.append(chunk); seg_end.append(o + d); chunk = []
    if chunk: caps.append(chunk); seg_end.append(o + d)
fixed = []
for k, ch in enumerate(caps):
    a, b = ch[0][1], ch[-1][2]
    nxt = caps[k + 1][0][1] if k + 1 < len(caps) else TOTAL
    fixed.append((a, min(max(b + 0.15, a + 0.35), nxt, b + 0.4, seg_end[k]), ch))
caps = fixed

CREAM = "&HA6F3FF&"   # amarelo-creme da referência (#FFF3A6)
POP = r"{\fscx30\fscy30\t(0,110,\fscx112\fscy112)\t(110,190,\fscx100\fscy100)}"

# ---------- intro: palavras grandes uma a uma acompanhando a fala ----------
BIG = [("quantidade", 5.12), ("considerável", 5.52), ("de calças", 6.22), ("preciso", 7.16),
       ("da sua ajuda", 7.36), ("o que vai ficar", 8.36), ("o que vai sair", 9.12)]
overlays = []
for k, (txt, st) in enumerate(BIG):
    a = at("6380", st); b = at("6380", BIG[k + 1][1]) if k + 1 < len(BIG) else INTRO
    overlays.append((a, b, "Big", 540, 1290, txt))

# ---------- veredito ----------
VERD = [  # (arquivo, tempo da palavra, texto)
    ("6385", 24.00, "fica"), ("6388", 25.66, "vai embora"), ("6389", 36.38, "fica|(por enquanto)"),
    ("6390", 25.06, "vai embora"), ("6391", 12.98, "vai embora"), ("6393", 16.84, "vai embora"),
    ("6394", 25.12, "fica"), ("6395", 36.34, "vai embora"), ("6396", 23.02, "vai embora"),
    ("6396", 52.56, "vai embora"), ("6398", 15.56, "fica"), ("6399", 10.02, "vai embora"),
    ("6401", 32.28, "fica"), ("6403", 24.16, "fica"), ("6405", 50.86, "fica"),
    ("6406", 33.84, "fica ou|vai embora?"), ("6407", 21.56, "fica"), ("6408", 30.36, "fica"),
    ("6409", 12.46, "fica"),     ("6412", 9.20, "fica"), ("6412", 18.30, "fica ou|vai embora?"),
]
EXTEND = {("6407", 21.56): ("6407", 26.30)}  # segura até o fim da peça
sfx = []
for f, wt, txt in VERD:
    a = at(f, wt)
    b = seg_end_at(*EXTEND[(f, wt)]) if (f, wt) in EXTEND else seg_end_at(f, wt)
    l = txt.split("|")
    body = l[0] if len(l) == 1 else (l[0] + r"\N{\fs58}" + l[1] if l[1].startswith("(") else l[0] + r"\N" + l[1])
    overlays.append((a, b, "Verd", 540, 330, r"{\frz-3}" + POP + body))
    if txt == "fica": sfx.append(("plim", a, 0.0, 0.45))
    elif txt == "vai embora": sfx.append(("tchau", a, 0.0, 0.5))
# "R$ 40 no TikTok Shop"
a = at("6409", 16.0)
overlays.append((a, seg_end_at("6409", 16.0), "Info", 540, 330, POP + r"{\c&HA6F3FF&}[ {\c&HFFFFFF&}R$ 40 no TikTok Shop {\c&HA6F3FF&}]"))
sfx.append(("bling", a, 0.0, 0.4))

# ---------- cartão de categoria "calças ✨" ----------
CARD_A, CARD_B = timeline[1][1], timeline[1][1] + 1.8
overlays.append((CARD_A, CARD_B, "Card", 540, 1010, r"{\fad(0,200)}" + POP + "calças"))
sfx.append(("bling", CARD_A + 0.1, 0.0, 0.45))
SPARK = [  # (x, y, tamanho, atraso)
    (175, 880, 100, 0.10), (850, 900, 80, 0.16), (220, 1080, 64, 0.22), (880, 1075, 104, 0.12), (585, 860, 56, 0.26),
]

# ---------- fechamento ----------
def bounce_line(ws, t_first, step):
    out = ""
    for k, w in enumerate(ws):
        ms = int((t_first + k * step) * 1000)
        out += (r"{\alpha&HFF&\fscy35\blur6" + r"\t(%d,%d,\alpha&H00&\fscy128\blur0)\t(%d,%d,\fscy92)\t(%d,%d,\fscy100)}" %
                (ms, ms + 110, ms + 110, ms + 190, ms + 190, ms + 260) + w + (" " if k + 1 < len(ws) else ""))
    return out
END_T0 = 0.15
overlays += [
    (TOTAL, TOTAL + END, "End", 540, 300, r"{\fad(0,250)}" + bounce_line(["vem", "aí", "o"], END_T0, 0.17)),
    (TOTAL, TOTAL + END, "End", 520, 440, r"{\fad(0,250)\fs150}" + bounce_line(["ep.", "2"], END_T0 + 0.6, 0.2)),
]
EP2_T = TOTAL + END_T0 + 0.6 + 0.2
sfx.append(("plim", EP2_T, 0.0, 0.5))

STY = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins SemiBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,4,2,8,80,80,470,1
Style: Big,Nunito Black,124,&H00A6F3FF,&H00FFFFFF,&H00000000,&H9A3A2A1A,0,0,0,0,100,100,-3,0,1,0,5,5,40,40,0,1
Style: Title,Nunito Black,124,&H00A6F3FF,&H00FFFFFF,&H00000000,&H9A3A2A1A,0,0,0,0,100,100,-3,0,1,0,5,5,40,40,0,1
Style: Verd,Nunito Black,96,&H00A6F3FF,&H00FFFFFF,&H00000000,&H9A3A2A1A,0,0,0,0,100,100,-2,0,1,0,5,5,40,40,0,1
Style: Card,Nunito Black,180,&H00A6F3FF,&H00FFFFFF,&H00000000,&H9A3A2A1A,0,0,0,0,100,100,-4,0,1,0,6,5,40,40,0,1
Style: End,Nunito Black,96,&H00A6F3FF,&H00FFFFFF,&H00000000,&H9A3A2A1A,0,0,0,0,100,100,-3,0,1,0,6,5,40,40,0,1
Style: Info,Poppins SemiBold,56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,4,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass = STY
for a, b, ch in caps:
    for j, (wtxt, wa, wb) in enumerate(ch):
        ea = a if j == 0 else wa
        eb = ch[j + 1][1] if j + 1 < len(ch) else b
        if eb <= ea: continue
        body = []
        for m, (t2, _, _) in enumerate(ch):
            t2 = t2.rstrip(".,") if m == len(ch) - 1 else t2
            body.append("{\\c" + CREAM + "\\fscx108\\fscy108}" + t2 + "{\\c&HFFFFFF&\\fscx100\\fscy100}" if m == j else t2)
        pop = "{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
        ass += f"Dialogue: 0,{ts(ea)},{ts(eb)},Cap,,0,0,0,,{pop}{' '.join(body)}\n"
for a, b, st, x, y, txt in overlays:
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},{st},,0,0,0,,{{\\pos({x},{y})}}{txt}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

# ---------- título digitado (camada que fica ATRÁS dela) ----------
tass = STY
TYPE_START, TYPE_STEP = 0.25, 0.045
lines = ["uma limpa no", "guarda-roupa"]
chars = [ch for ch in "\n".join(lines)]
typed = [i for i, ch in enumerate(chars) if ch not in " \n"]
def title_body(n, cursor):
    out = ""
    for i, ch in enumerate(chars):
        tok = r"\N" if ch == "\n" else ch
        out += ("{\\alpha&H00&}" if i <= n else "{\\alpha&HFF&}") + tok
        if i == n and cursor: out += "{\\alpha&H00&}|"
        elif i == n: out += "{\\alpha&HFF&}|"
    return out
for k, n in enumerate(typed):
    a = TYPE_START + k * TYPE_STEP
    b = TYPE_START + (k + 1) * TYPE_STEP if k + 1 < len(typed) else None
    if b is None: break
    tass += f"Dialogue: 0,{ts(a)},{ts(b)},Title,,0,0,0,,{{\\pos(540,690)}}{title_body(n, True)}\n"
TYPE_DONE = TYPE_START + (len(typed) - 1) * TYPE_STEP
t, on = TYPE_DONE, True     # cursor piscando depois de digitar
while t < 2.6:
    tass += f"Dialogue: 0,{ts(t)},{ts(t+0.3)},Title,,0,0,0,,{{\\pos(540,690)}}{title_body(typed[-1], on)}\n"
    t += 0.3; on = not on
tass += f"Dialogue: 0,{ts(t)},{ts(INTRO)},Title,,0,0,0,,{{\\pos(540,690)\\fad(0,200)}}{title_body(typed[-1], False)}\n"
tass += f"Dialogue: 0,{ts(TYPE_DONE+0.25)},{ts(INTRO)},Title,,0,0,0,,{{\\pos(800,835)\\fs58\\fad(0,200)}}{POP}ep. 1\n"
open(f"{OUT}/titulo.ass", "w").write(tass)

# ---------- sons sintetizados ----------
def synth(name, expr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *expr, f"{OUT}/{name}.wav"], check=True)
def bell(name, notes, d=0.7, vol=1.6):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    synth(name, ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                 f"afade=t=in:d=0.003,aecho=0.8:0.4:45|90:0.25|0.12,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0,volume={vol}"])
bell("plim", [(1568, 0.5, 7, 0), (2349, 0.3, 9, 0), (3136, 0.12, 12, 0)])
bell("bling", [(1318.5, 0.45, 9, 0), (1975.5, 0.5, 7, 0.07), (2637, 0.15, 11, 0.07)], d=0.8)
bell("tchau", [(987.8, 0.5, 8, 0), (659.3, 0.55, 6, 0.11)], d=0.8)   # duas notas descendo: "vai embora"

# ---------- render ----------
LOOK = "eq=contrast=1.06:saturation=1.12:brightness=0.01,colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03"
# 1) cada corte vira um arquivo (evita estourar a memória com dezenas de trims do mesmo arquivo)
PCS = f"{OUT}/pecas"; os.makedirs(PCS, exist_ok=True)
lst = []
for i, (seg, o, d, z) in enumerate(timeline):
    f, a, b = seg
    cw, chh = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    n = round(d * 30)
    pf = f"{PCS}/{i:03d}.mkv"; lst.append(f"file '{pf}'")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(a-1,0):.3f}", "-i", f"{PROXY}/IMG_{f}.mp4",
        "-filter_complex", f"[0:v]trim=start={a-max(a-1,0):.4f},setpts=PTS-STARTPTS,crop={cw}:{chh}:(iw-{cw})/2:(ih-{chh})*0.62,scale={W}:{H},fps=30,setsar=1,format=yuv420p,trim=end_frame={n}[v];"
        f"[0:a]atrim=start={a-max(a-1,0):.4f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,atrim=end={n/30:.4f},apad=whole_dur={n/30:.4f},"
        f"afade=t=in:d=0.02,afade=t=out:st={max(n/30-0.03,0):.3f}:d=0.03[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-c:a", "pcm_s16le", pf], check=True)
open(f"{OUT}/pecas.txt", "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/pecas.txt",
                "-c", "copy", f"{OUT}/base.mkv"], check=True)
print("peças ok", flush=True)
inputs, fc = ["-i", f"{OUT}/base.mkv"], []
mi = inputs.count("-i"); inputs += ["-i", f"{OUT}/mask_intro.mkv"]
si = inputs.count("-i"); inputs += ["-loop", "1", "-i", f"{OUT}/sparkle.png"]
esc = lambda p: p.replace(":", r"\:")
fc.append("[0:v]setpts=PTS-STARTPTS[vc]"); fc.append("[0:a]asetpts=PTS-STARTPTS[ac]")
fc.append(f"[vc]{LOOK},split=2[base][forp]")
fc.append(f"[{mi}:v]format=gray,setpts=PTS-STARTPTS,tpad=stop_mode=add:stop_duration={TOTAL:.2f}:color=black[m]")
fc.append(f"[forp][m]alphamerge[person]")
fc.append(f"color=c=black@0.0:s={W}x{H}:r=30:d={INTRO:.3f},format=rgba,subtitles='{esc(OUT)}/titulo.ass':fontsdir={FONTS}:alpha=1[tl]")
fc.append(f"[base][tl]overlay=eof_action=pass:format=auto[bt]")
fc.append(f"[bt][person]overlay=enable='lt(t,{INTRO:.3f})':format=auto,format=yuv420p[b2]")
fc.append(f"[b2]tpad=stop_mode=clone:stop_duration={END},subtitles='{esc(OUT)}/legendas.ass':fontsdir={FONTS}[v0s]")
# ✨ do cartão + ✨ do fechamento
nsp = len(SPARK) + 1
fc.append(f"[{si}:v]format=rgba,split={nsp}" + "".join(f"[sp{j}]" for j in range(nsp)))
cur = "v0s"
for j, (x, y, size, dl) in enumerate(SPARK + [(800, 440, 110, 0.0)]):
    if j < len(SPARK):
        a, b = CARD_A + dl, CARD_B
    else:
        a, b = EP2_T + 0.1, TOTAL + END
    fc.append(f"[sp{j}]scale={size}:-1,fade=t=in:st={a:.2f}:d=0.15:alpha=1,fade=t=out:st={b-0.2:.2f}:d=0.2:alpha=1[spx{j}]")
    fc.append(f"[{cur}][spx{j}]overlay=x={x}-w/2:y={y}-h/2:enable='between(t,{a:.2f},{b:.2f})':shortest=1[ov{j}]")
    cur = f"ov{j}"
fc.append(f"[{cur}]fade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8,format=yuv420p[vout]")
fc.append(f"[ac]apad=pad_dur={END}[acp]")
mix = ["[acp]"]
for j, (name, peak, inner, vol) in enumerate(sfx):
    k = inputs.count("-i"); inputs += ["-i", f"{OUT}/{name}.wav"]
    ms = int(max(peak - inner, 0) * 1000)
    fc.append(f"[{k}:a]volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[aout]")
open(f"{OUT}/graph.txt", "w").write(";\n".join(fc))
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex_script", f"{OUT}/graph.txt",
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{TOTAL+END:.2f}",
       f"{OUT}/limpa_calcas_{VERSAO}.mp4"]
print(f"duração {TOTAL+END:.1f}s, {len(caps)} legendas", flush=True)
if os.environ.get("DRY"): raise SystemExit
subprocess.run(cmd, check=True)
print("OK")

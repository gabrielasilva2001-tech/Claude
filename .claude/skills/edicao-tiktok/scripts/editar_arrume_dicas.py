"""APROVADO (v3, "como entrar num banco ou cooperativa"). Arrume-se comigo — formato DICAS NUMERADAS falando perto da câmera.
Tema: coisas que eu faria se quisesse entrar num banco/cooperativa.
Base: editar_exemplo_tripe.py (estilo aprovado) + ideias da referência (lista #1, #2... no topo durante cada dica).
"""
import json, subprocess, os, sys

S = os.environ.get("EDIT_WORK", os.getcwd())
PROXY, OUT = f"{S}/proxy", f"{S}/render"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v1"

FILES = ["IMG_6337", "IMG_6338", "IMG_6340", "IMG_6341", "IMG_6342", "IMG_6348"]
words = {f: [w for s in json.load(open(f"{S}/audio/{f}.json")) for w in s["words"]] for f in FILES}

def find(f, t):
    ws = words[f]
    k = min(range(len(ws)), key=lambda i: abs(ws[i]["start"] - t))
    return k

def cut(f, t_first, t_last, z=1.0, extra_end=None, tag=None):
    """Corte do 1º ao último word (por tempo de início), com folga sem pegar palavra vizinha."""
    ws = words[f]
    i, j = find(f, t_first), find(f, t_last)
    # se houver palavras com o mesmo início, pega a última
    while j + 1 < len(ws) and abs(ws[j + 1]["start"] - ws[j]["start"]) < 0.01: j += 1
    prev_end = ws[i - 1]["end"] if i > 0 else 0
    a = max(ws[i]["start"] - 0.10, prev_end + 0.02, 0)
    nxt = ws[j + 1]["start"] if j + 1 < len(ws) else 1e9
    b = min(ws[j]["end"] + 0.18, nxt - 0.05)
    if extra_end: b = extra_end
    return dict(f=f, a=round(a, 2), b=round(b, 2), z=z, wi=i, wj=j, tag=tag)

# ---------- decupagem ----------
SEGS = [
    # gancho
    cut("IMG_6337", 1.74, 3.16, 1.00),                 # Já que vocês vivem me perguntando,
    cut("IMG_6337", 5.14, 9.50, 1.12),                 # coisas que eu faria se eu quisesse entrar...
    # contexto
    cut("IMG_6337", 33.82, 35.44, 1.00),               # Eu entrei em uma cooperativa, estou até hoje,
    cut("IMG_6338", 22.94, 25.30, 1.15),               # mas a maioria das dicas vale pra banco comercial também
    # 1 Instagram
    cut("IMG_6338", 31.34, 34.60, 1.00, tag="t1"),     # Primeira coisa, acompanharia o Instagram das cooperativas
    cut("IMG_6338", 48.50, 49.22, 1.15),               # pelo menos todas
    cut("IMG_6338", 50.60, 53.28, 1.15),               # as vagas em que eu participei estavam no Instagram
    cut("IMG_6338", 75.28, 78.08, 1.00),               # o que eles mais fazem é utilizar as redes...
    # 2 LinkedIn
    cut("IMG_6340", 0.80, 4.54, 1.12, tag="t2"),       # Atualizando o LinkedIn...
    cut("IMG_6340", 4.82, 7.44, 1.00, tag="desculpa"), # Ai, mas o LinkedIn nunca me chama...
    cut("IMG_6340", 8.76, 10.02, 1.18),                # Gente, vocês vão continuar dando desculpa.
    cut("IMG_6340", 23.50, 24.64, 1.00),               # Gente, mas não vai ser de primeira.
    cut("IMG_6340", 25.62, 25.84, 1.12),               # Vamos tentar,
    # 3 reputação
    cut("IMG_6341", 1.12, 6.54, 1.00, tag="t3"),       # bom relacionamento com quem trabalha...
    cut("IMG_6341", 7.78, 9.10, 1.15),                 # Principalmente em cidade pequena.
    cut("IMG_6341", 10.04, 13.56, 1.00),               # Se você não tiver um bom nome, um bom comportamento na sociedade,
    cut("IMG_6341", 14.72, 15.36, 1.15),               # você não vai ser contratado.
    cut("IMG_6341", 27.22, 29.58, 1.00),               # A primeira coisa que eles fazem é olhar o seu Instagram.
    cut("IMG_6341", 30.88, 31.68, 1.18, tag="sinto"),  # Sinto muito em informar.
    # 4 conta
    cut("IMG_6341", 47.40, 50.38, 1.00, tag="t4"),     # pode parecer bobo, mas eu abriria uma conta nesse lugar.
    cut("IMG_6341", 51.40, 51.72, 1.15),               # Por quê?
    cut("IMG_6341", 64.00, 67.52, 1.00),               # só de você precisar às vezes ir lá alguém já vai ter visto sua cara lá.
    # 5 qualquer vaga
    cut("IMG_6342", 0.00, 2.32, 1.12, tag="t5"),       # Eu tentaria toda e qualquer vaga.
    cut("IMG_6342", 18.36, 20.18, 1.00),               # Tentei no Sicoob cinco vezes,
    cut("IMG_6342", 27.16, 28.16, 1.15, tag="nunca"),  # nunca me chamaram pra nada. (P&B)
    cut("IMG_6342", 32.08, 34.52, 1.00),               # No Sicredi, com 21 anos, eu tentei pra jovem aprendiz.
    cut("IMG_6342", 47.96, 51.46, 1.15, tag="metade"), # eu ia sair de um salário de R$1.500 pra ganhar metade disso.
    cut("IMG_6342", 66.42, 68.38, 1.00),               # vou pôr a cara, vou ganhar menos,
    cut("IMG_6342", 71.62, 72.46, 1.15),               # mas eu vou entrar
    # 6 curso na área
    cut("IMG_6348", 0.00, 3.64, 1.00, tag="t6"),       # Dê preferência para cursos na área. Administração, contabilidade,
    cut("IMG_6348", 7.20, 10.74, 1.12),                # Ai, precisa ser na melhor faculdade do planeta inteiro? Não precisa,
    cut("IMG_6348", 11.86, 12.54, 1.00),               # Ninguém vai te perguntar.
    cut("IMG_6348", 21.52, 23.04, 1.15),               # você só precisa ser formado.
    # 7 certificações
    cut("IMG_6348", 25.60, 26.08, 1.00, tag="t7"),     # Tenha CPA.
    cut("IMG_6348", 32.64, 33.90, 1.12, tag="cpa"),    # CPA 10, CPA 20, CEA.
    cut("IMG_6348", 46.76, 49.22, 1.00),               # Isso é uma coisa que vai incrementar muito seu currículo
    cut("IMG_6348", 54.10, 57.32, 1.15),               # Nossa, essa pessoa aí tá sabendo o que tá fazendo, pelo menos.
    # fechamento
    cut("IMG_6348", 89.14, 91.94, 1.00, tag="end"),    # Infelizmente, ninguém vai bater na sua porta
    cut("IMG_6348", 96.28, 96.74, 1.12),               # Então, corre atrás,
    cut("IMG_6348", 105.42, 109.96, 1.00),             # não desiste, porque eu recebi 5 ou mais nãos na minha vida
    cut("IMG_6348", 113.06, 119.00, 1.10, extra_end=119.85),  # Não vai ser de primeira... não desiste. (congela no sorriso)
]
BW_TAGS = {"nunca"}

# ---------- só fala: corta pausas de pensamento e respiros (audio/fala.json, gerado por fala.py) ----------
FALA = json.load(open(f"{S}/audio/fala.json"))
CUTS = SEGS
PIECES = []  # (ci, f, a, b, z, tag)
for ci, c in enumerate(CUTS):
    ps = []
    for fa, fb in FALA[c["f"]]:
        a, b = max(fa, c["a"]), min(fb, c["b"])
        if b - a >= 0.10: ps.append([a, b])
    merged = []
    for p in ps:
        if merged and p[0] - merged[-1][1] < 0.10: merged[-1][1] = p[1]
        else: merged.append(p)
    if not merged: merged = [[c["a"], c["b"]]]
    if c["b"] - merged[-1][1] < 0.6 and c is CUTS[-1]: merged[-1][1] = c["b"]   # fecha no sorriso
    z = c["z"]; alt = 1.0 if z > 1.0 else 1.12
    for k, (a, b) in enumerate(merged):
        PIECES.append(dict(ci=ci, f=c["f"], a=round(a, 3), b=round(b, 3), z=z, tag=c["tag"] if k == 0 else None))
        if b - a >= 1.0: z = alt if z == c["z"] else c["z"]   # zoom alterna a cada corte (exceto pedacinhos)

# Correções de transcrição: (arquivo, início da palavra) -> texto
FIX = {
    ("IMG_6337", 22.78): "Gabi,",
    ("IMG_6338", 22.94): "Mas",
    ("IMG_6338", 31.34): "Primeira",
    ("IMG_6338", 48.50): "Pelo",
    ("IMG_6338", 75.28): "O",
    ("IMG_6341", 1.12): "Bom",
    ("IMG_6341", 47.40): "Pode",
    ("IMG_6341", 64.00): "Só",
    ("IMG_6342", 19.04): "Sicoob",
    ("IMG_6342", 27.16): "nunca",
    ("IMG_6342", 27.90): "pra",
    ("IMG_6342", 32.08): "No",
    ("IMG_6342", 32.50): "Sicredi,",
    ("IMG_6342", 34.10): "pra",
    ("IMG_6342", 47.96): "Eu",
    ("IMG_6342", 49.10, "R"): "R$1.500", ("IMG_6342", 49.72, "$1"): "", ("IMG_6342", 49.72, ".500"): "",
    ("IMG_6342", 49.72, "para"): "pra",
    ("IMG_6342", 66.42): "Vou", ("IMG_6342", 67.06): "pôr",
    ("IMG_6342", 72.46): "entrar!",
    ("IMG_6348", 1.46): "pra",
    ("IMG_6348", 10.30): "inteiro?",
    ("IMG_6348", 21.52): "Você",
    ("IMG_6348", 32.64): "CPA-10,", ("IMG_6348", 32.96): "",
    ("IMG_6348", 33.26): "CPA-20,", ("IMG_6348", 33.52): "",
    ("IMG_6348", 33.90): "CEA.",
    ("IMG_6348", 96.28): "Então,",
    ("IMG_6348", 105.42): "Não", ("IMG_6348", 105.84): "desiste,",
    ("IMG_6348", 110.24): "",
}
FIX_TEXT = {"está": "tá", "para": "pra"}

def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# ---------- timeline ----------
timeline, t = [], 0.0
for pc in PIECES:
    d = round((pc["b"] - pc["a"]) * 30) / 30; pc["b"] = pc["a"] + d
    timeline.append((pc, t, d)); t += d
TOTAL = t
END = 3.0
cut_out = {}
for pc, o, d in timeline:
    ci = pc["ci"]; s0, e0 = cut_out.get(ci, (o, o)); cut_out[ci] = (min(s0, o), o + d)
def map_t(ci, x, side):
    """tempo no bruto -> tempo no vídeo final; se cair num pedaço cortado, encosta no vizinho"""
    ps = [(pc, o, d) for pc, o, d in timeline if pc["ci"] == ci]
    for pc, o, d in ps:
        if pc["a"] <= x <= pc["b"]: return o + x - pc["a"]
        if x < pc["a"]: return o if side == "start" else max(o - 0.001, ps[0][1])
    return ps[-1][1] + ps[-1][2]
def seg_start(tag):
    for ci, c in enumerate(CUTS):
        if c["tag"] == tag: return cut_out[ci][0]
def seg_dur(tag):
    for ci, c in enumerate(CUTS):
        if c["tag"] == tag: return cut_out[ci][1] - cut_out[ci][0]

# ---------- legendas dinâmicas ----------
caps, seg_end = [], []
for ci, c in enumerate(CUTS):
    f = c["f"]; chunk = []; cend = cut_out[ci][1]
    for k in range(c["wi"], c["wj"] + 1):
        w = words[f][k]
        raw = w["word"].strip()
        txt = FIX.get((f, round(w["start"], 2), raw), FIX.get((f, round(w["start"], 2)), raw))
        txt = FIX_TEXT.get(txt, txt)
        if not txt: continue
        ws_, we_ = map_t(ci, w["start"], "start"), map_t(ci, min(w["end"], c["b"]), "end")
        if we_ <= ws_ + 0.08: we_ = ws_ + 0.15
        chunk.append((txt, ws_, we_))
        if len(chunk) >= 3 or txt[-1] in ",.?!":
            caps.append(chunk); seg_end.append(cend); chunk = []
    if chunk: caps.append(chunk); seg_end.append(cend)
# palavras dentro do bloco em ordem crescente
for ch in caps:
    for m in range(1, len(ch)):
        if ch[m][1] < ch[m - 1][1] + 0.06: ch[m] = (ch[m][0], ch[m - 1][1] + 0.06, max(ch[m][2], ch[m - 1][1] + 0.2))
fixed = []
for k, ch in enumerate(caps):
    a, b = ch[0][1], ch[-1][2]
    nxt = caps[k + 1][0][1] if k + 1 < len(caps) else TOTAL
    fixed.append((max(a - 0.03, 0), min(max(b + 0.15, a + 0.35), nxt, b + 0.4, seg_end[k]), ch))
caps = fixed

# ---------- cabeçalho das dicas (#1, #2... fica no topo durante a dica) ----------
POP = r"{\fscx30\fscy30\t(0,110,\fscx112\fscy112)\t(110,190,\fscx100\fscy100)}"
PINK, YEL, WHITE = r"{\c&HB45CFF&}", r"{\c&H3DD9FF&}", r"{\c&HFFFFFF&}"
TIPS = [("t1", "siga a cooperativa", "no INSTAGRAM"),
        ("t2", "atualize o", "LINKEDIN"),
        ("t3", "cuide da sua", "REPUTAÇÃO"),
        ("t4", "abra uma", "CONTA LÁ"),
        ("t5", "tente", "QUALQUER VAGA"),
        ("t6", "faça curso", "NA ÁREA"),
        ("t7", "tenha", "CERTIFICAÇÕES")]
tip_bounds = []
for n, (tag, l1, l2) in enumerate(TIPS):
    a = seg_start(tag)
    b = seg_start(TIPS[n + 1][0]) if n + 1 < len(TIPS) else seg_start("end")
    tip_bounds.append((a, b))
overlays = []
for n, ((tag, l1, l2), (a, b)) in enumerate(zip(TIPS, tip_bounds)):
    overlays.append((a, b - 0.05, "Tip", 540, 300,
                     r"{\fad(0,150)}" + POP + PINK + f"#{n+1} " + WHITE + l1 + r"\N" + YEL + r"{\fs78}" + l2))

# ---------- rótulos soltos ----------
overlays += [
    (seg_start("desculpa") + 0.05, seg_start("desculpa") + seg_dur("desculpa"), "Label", 560, 520, r"{\frz-5}" + POP + "ai, mas..."),
    (seg_start("sinto"), seg_start("sinto") + seg_dur("sinto") + 0.4, "Label", 560, 520, r"{\frz4}" + POP + "sinto muito!"),
    (seg_start("nunca"), seg_start("nunca") + seg_dur("nunca"), "Label", 540, 520, r"{\frz5}" + POP + "5x não..."),
    (seg_start("metade") + 2.6, seg_start("metade") + seg_dur("metade"), "Label", 560, 520, r"{\frz-4}" + POP + "metade?!"),
    (seg_start("cpa"), seg_start("cpa") + seg_dur("cpa") + 1.2, "Info", 540, 520,
     POP + PINK + "[ " + WHITE + "CPA-10 · CPA-20 · CEA " + PINK + "]"),
]

# ---------- fechamento ----------
# ✨ é emoji colorido (o libass não desenha): no texto vai um "O" invisível guardando o lugar,
# e a imagem do ✨ é sobreposta exatamente ali (posição achada renderizando o "O" em verde).
SLOT = "{\\alpha&HFF&}O"
SLOT_MARK = "{\\alpha&H00&\\c&H00FF00&}O"
def bounce_line(ws, t_first, step, color_of):
    out = ""
    for k, w in enumerate(ws):
        if w == "✨":
            out += "@SLOT@"; continue
        ms = int((t_first + k * step) * 1000)
        out += (r"{\alpha&HFF&\fscy35\blur6\c%s" % color_of(k)
                + r"\t(%d,%d,\alpha&H00&\fscy128\blur0)\t(%d,%d,\fscy92)\t(%d,%d,\fscy100)}" % (ms, ms + 110, ms + 110, ms + 190, ms + 190, ms + 260)
                + w + (" " if k + 1 < len(ws) else ""))
    return out
END_TEXT_T0 = 0.15
l1 = bounce_line(["Corre", "atrás", "e"], END_TEXT_T0, 0.17, lambda k: "&HFFFFFF&")
l2 = bounce_line(["NÃO", "DESISTE", "✨"], END_TEXT_T0 + 0.6, 0.2, lambda k: "&H3DD9FF&" if k == 2 else "&HB45CFF&")
overlays += [
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
Style: Tip,Montserrat Thin Black,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,-1,0,0,100,100,-2,0,1,0,6,5,60,60,0,1
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
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},{st},,0,0,0,,{{\\pos({x},{y})}}{txt}\n"
# gancho digitado letra por letra (fica até o fim do 2º corte do gancho)
TYPE_START, TYPE_STEP = 0.20, 0.045
TYPE_END = cut_out[1][1]
parts = [("&HFFFFFF&", "Como entrar num banco"), ("&HFFFFFF&", "\n"), ("&HFFFFFF&", "ou "), ("&HB45CFF&", "COOPERATIVA "), ("&H3DD9FF&", "✨")]
chars = [(c, ch) for c, txt in parts for ch in txt]
typed = [i for i, (c, ch) in enumerate(chars) if ch not in " \n"]
for k, n in enumerate(typed):
    a = TYPE_START + k * TYPE_STEP
    b = TYPE_START + (k + 1) * TYPE_STEP if k + 1 < len(typed) else TYPE_END
    body = ""
    for i, (c, ch) in enumerate(chars):
        tok = r"\N" if ch == "\n" else ch
        if ch == "✨": body += "@SLOT@" if i <= n else SLOT; continue
        body += ("{\\c%s\\alpha&H00&}" % c if i <= n else "{\\alpha&HFF&}") + tok
    fade = r"{\fad(0,200)}" if k + 1 == len(typed) else ""
    ass += f"Dialogue: 1,{ts(a)},{ts(b)},Title,,0,0,0,,{{\\pos(540,330)}}{fade}{body}\n"
open(f"{OUT}/legendas.ass", "w").write(ass.replace("@SLOT@", SLOT))
open(f"{OUT}/legendas_mark.ass", "w").write(ass.replace("@SLOT@", SLOT_MARK))
EMO_HOOK = (TYPE_START + (len(typed) - 1) * TYPE_STEP, TYPE_END)          # entra quando é "digitado"
EMO_END = (TOTAL + END_TEXT_T0 + 0.6 + 2 * 0.2, TOTAL + END)              # chega depois de DESISTE

def emoji_png(path, h):
    from PIL import Image, ImageDraw, ImageFont
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), "✨", font=fnt, embedded_color=True)
    im = im.crop(im.getbbox())
    im.resize((round(im.width * h / im.height), h), Image.LANCZOS).save(path)

def slot_box(t):
    """renderiza o marcador verde num fundo preto e devolve o centro e a altura do 'O'"""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", f"color=black:s={W}x{H}:r=30:d={TOTAL+END+1}",
        "-vf", f"subtitles='{OUT}/legendas_mark.ass':fontsdir={FONTS}", "-ss", f"{t}", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(int)
    m = (im[:, :, 1] > 150) & (im[:, :, 0] < 90) & (im[:, :, 2] < 90)
    ys, xs = np.nonzero(m)
    return xs.min(), (ys.min() + ys.max()) / 2, ys.max() - ys.min()

# ---------- sons (sempre seguem a imagem) ----------
def synth(name, expr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *expr, f"{OUT}/{name}.wav"], check=True)
def bell(name, notes, d=0.7, vol=1.6):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    synth(name, ["-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                 f"afade=t=in:d=0.003,aecho=0.8:0.4:45|90:0.25|0.12,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0,volume={vol}"])
bell("plim", [(1568, 0.5, 7, 0), (2349, 0.3, 9, 0), (3136, 0.12, 12, 0)])
# "check": duas notinhas subindo, curtinho — toca quando cada número da lista entra
bell("check", [(1046.5, 0.45, 14, 0), (1568, 0.5, 11, 0.075)], d=0.45)
sfx = [("check", a, 0.25) for a, b in tip_bounds]
sfx += [("plim", seg_start("cpa"), 0.25),                       # [ CPA-10 · CPA-20 · CEA ]
        ("plim", TOTAL + END_TEXT_T0 + 0.6 + 0.2, 0.45)]        # "DESISTE" chegando

# ---------- render (em etapas, para não estourar memória) ----------
LOOK = "eq=contrast=1.06:saturation=1.14:brightness=0.01,colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03"
def render():
    os.makedirs(f"{OUT}/segs", exist_ok=True)
    lst = []
    for i, (seg, o, d) in enumerate(timeline):
        f, a, b, z = seg["f"], seg["a"], seg["b"], seg["z"]
        # direto do ORIGINAL 4K: recorta o zoom em 4K e só depois reduz (mais nitidez)
        cw, ch = int(2160 / z) // 2 * 2, int(3840 / z) // 2 * 2
        bw = ",hue=s=0" if CUTS[seg["ci"]]["tag"] in BW_TAGS else ""
        dst = f"{OUT}/segs/{i:03d}.mp4"
        lst.append(f"file '{dst}.mov'")
        if "--reuse" in sys.argv and os.path.exists(dst + ".mov"): continue
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a}", "-i", f"{S}/raw/{f}.mov", "-frames:v", str(round(d * 30)), "-t", f"{d:.4f}",
            "-vf", f"crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2.6,scale={W}:{H}:flags=lanczos,fps=30,setsar=1{bw}",
            "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03,apad,atrim=0:{d:.4f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-f", "mov", dst + ".mov"], check=True)
    open(f"{OUT}/segs/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/segs/list.txt",
                    "-c", "copy", f"{OUT}/concat.mov"], check=True)
    inputs = ["-i", f"{OUT}/concat.mov"]
    fc = [f"[0:v]tpad=stop_mode=clone:stop_duration={END},{LOOK},subtitles='{OUT}/legendas.ass':fontsdir={FONTS}[vs0]",
          f"[0:a]apad=pad_dur={END}[acp]"]
    # ✨ por cima, no lugar do marcador
    last = "vs0"
    for n, ((t0, t1), size_k) in enumerate([(EMO_HOOK, 1.7), (EMO_END, 1.7)]):
        x0, cy, hh = slot_box((t0 + t1) / 2)
        hpx = int(hh * size_k) // 2 * 2
        png = f"{OUT}/sparkle_{n}.png"; emoji_png(png, hpx)
        from PIL import Image
        ew = Image.open(png).width
        dur = t1 - t0
        idx = inputs.count("-i"); inputs += ["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", png]
        fc.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st={max(dur-0.2,0):.3f}:d=0.2:alpha=1,setpts=PTS+{t0:.3f}/TB[e{n}]")
        fc.append(f"[{last}][e{n}]overlay=x={x0 + 8:.0f}:y={cy - hpx/2:.0f}:eof_action=pass[vs{n+1}]")
        last = f"vs{n+1}"
        print(f"✨ {n}: x {x0 + 8:.0f}, y {cy:.0f} altura {hpx}px, {t0:.2f}-{t1:.2f}s")
    fc.append(f"[{last}]fade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[vout]")
    mix = ["[acp]"]
    for j, (name, at, vol) in enumerate(sfx):
        idx = inputs.count("-i"); inputs += ["-i", f"{OUT}/{name}.wav"]
        ms = int(max(at, 0) * 1000)
        fc.append(f"[{idx}:a]volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-12.8:TP=-1.5:LRA=11,afade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[aout]")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "6800k", "-bufsize", "13600k",
       "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/arrume_banco_{VERSION}.mp4"], check=True)

print(f"duração {TOTAL:.1f}s + {END}s fechamento, {len(caps)} legendas")
for a, b, ch in caps: print(f"{a:6.2f} {' '.join(c[0] for c in ch)}")
if "--dry" in sys.argv: sys.exit()
render()
print("OK")

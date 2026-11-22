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
    ("6380", 4.50, 9.95),    # intro
    ("6385", 9.74, 15.95),   # primeira calça cintura baixa depois que emagreci, apego emocional
    ("6385", 23.15, 25.10),  # então ela fica
    ("6388", 6.50, 12.95),   # de quando eu era bem gordinha, mandei arrumar na costureira
    ("6388", 13.10, 14.80),  # porque eu amava calça com bolso
    ("6388", 23.10, 26.90),  # hoje eu já não amo, então ela vai sair
    ("6389", 3.75, 8.85),    # calça sujinha, amo ela, só que olha o tamanho dessa barra
    ("6389", 25.00, 27.45),  # se eu não fizer a barra dessa calça aqui até
    ("6389", 28.40, 31.45),  # a semana que vem eu vou ter que tirar ela
    ("6389", 35.75, 40.00),  # mas ela fica por enquanto, se eu não arrumar, tchau
    ("6390", 16.40, 21.70),  # apego emocional, adoro usar em tempos chuvosos
    ("6390", 22.15, 26.60),  # tá ficando branca, vai ter que sair
    ("6391", 1.75, 4.20),    # essa daqui eu uso pra trabalhar
    ("6391", 8.65, 12.10),   # tá vendo aqui? fazendo até onda de tão usada
    ("6391", 12.90, 14.30),  # vai ter que sair
    ("6393", 1.90, 3.05),
    ("6393", 4.86, 13.10),   # outra de trabalho... boca de sino... pra mim não dá
    ("6393", 16.50, 17.90),  # então ela vai sair
    ("6394", 7.33, 14.60),   # comprei no desespero pro Chile, ela é G, uso cintura baixa e finge que tá tudo certo
    ("6394", 24.80, 26.20),  # ela vai ficar
    ("6395", 8.25, 15.55),   # mesma história, bolso, gosto da lavagem, se não tivesse o bolso eu ficaria
    ("6395", 28.10, 31.95),  # o problema mesmo é esse bolso
    ("6395", 36.05, 37.30),  # então ela sai
    ("6396", 11.85, 13.40),
    ("6396", 15.90, 17.85),
    ("6396", 20.10, 24.10),  # calça preta de camurça, usei muito, cheia de bolso, saindo a cor, ela sai
    ("6396", 39.20, 40.10),  # olha isso aqui
    ("6396", 46.10, 48.35),  # já saiu a maioria das tachinhas, tá surradinho o jeans
    ("6396", 52.00, 55.00),  # infelizmente vai ter que sair, ela que se acabou
    ("6396", 59.05, 59.95),  # mas ela era perfeita
    ("6396", 67.95, 69.90),  # gente, que tanta coisa que tá saindo
    ("6397", 12.15, 15.95),  # só coloquei no corpo pra verem o tanto que ela é icônica
    ("6397", 19.65, 23.60),  # nada convencional, sei nem que cor é isso, acho que é um vinho, perfeita
    ("6398", 7.35, 7.95),    # olha isso!
    ("6398", 11.10, 13.95),  # maravilhosa, pelinho por dentro
    ("6398", 15.05, 16.80),  # ela com certeza fica
    ("6399", 1.65, 5.95),
    ("6399", 9.40, 11.10),   # nem vou experimentar, enorme, desbotado, surrada, vai sair
    ("6401", 8.35, 12.05),   # amo essa calça pra ir em rodeio
    ("6401", 31.50, 33.20),  # e ela fica
    ("6403", 1.45, 3.12),    # essa calça aqui
    ("6403", 6.95, 11.50),
    ("6403", 15.30, 18.25),   # acontecimento... abalou as estruturas, tá sem cor mas ainda amo, não vai sair
    ("6403", 24.10, 25.10),  # fica
    ("6404", 9.25, 17.75),   # amei, obcecada, só tenho calça básica, uma ousadinha
    ("6404", 18.65, 19.95),  # e nessa mesma pegada
    ("6404", 21.78, 22.50),  # eu comprei outra
    ("6405", 13.30, 21.60),  # queria uma calça diferente, vários croppeds de uma cor só
    ("6405", 49.75, 51.80),  # então, eu amei
    ("6406", 2.45, 5.60),   # paguei caríssimo
    ("6406", 8.10, 11.95),   # paguei caríssimo, não lembro a loja, tá muito larga, não me valorizou
    ("6406", 19.65, 23.95),  # sinceramente não sei, vai ficar um ponto de interrogação
    ("6406", 33.80, 35.90),  # essa aqui vocês vão ter que me ajudar
    ("6407", 4.05, 7.60),    # pegada de bolso, né galera?
    ("6407", 8.40, 12.75),   # gosto dessa calça, me veste bem, bumbum bonitinho
    ("6407", 21.05, 23.10),  # vai ficar só porque ela é marrom
    ("6407", 25.40, 27.30),  # mas eu não amo ela
    ("6408", 2.05, 7.40),   # comprei com uma amiga, amo, super diferente, dá pra usar com parte de cima, me veste bem
    ("6408", 22.15, 31.40),  # tenho comprado cintura baixa, autoestima... ela vai ficar
    ("6409", 1.15, 4.45),    # couro pro Chile, não usei
    ("6409", 11.70, 13.40),  # então eu gosto, ela vai ficar
    ("6409", 14.65, 18.40),  # 40 reais no TikTok Shop
    ("6410", 24.75, 32.69),  # apesar de social nunca usei pra trabalhar, usei e gostei... ocupando espaço, agora vou usar
    ("6412", 2.20, 5.75),   # essa calça branca, uso muito na praia
    ("6412", 7.95, 10.35),   # calça branca, uso muito na praia, só praia, vai ficar
    ("6412", 10.50, 21.60),  # Shein há 5, 6 anos, surrada, gosto mas não sei se vai ou fica, ainda tô pensando
    ("6412", 47.30, 49.40),  # e isso foi tudo que saiu
    ("6412", 62.30, 64.75),  # ainda tenho muita coisa pra tirar: cropped, blusinha, short, saia, casaco
    ("6412", 80.50, 81.05),  # beijo! (congela no sorriso)
]
FILES = sorted({s[0] for s in SEGS})

FIX = {
    ("6396", 12.90): "camurça,", ("6396", 50.20): "surradinho",
    ("6401", 10.96): "rodeio", ("6390", 21.24): "chuvosos,",
    ("6412", 11.40): "Shein", ("6407", 11.42): "deixa",
}
FIXW = {"camorça": "camurça", "camuça": "camurça", "sorradinho": "surradinho", "surada": "surrada", "rodeia": "rodeio",
        "chen": "Shein", "deixe": "deixa", "chuvoso": "chuvosos", "emangreci": "emagreci", "pega": "apego"}
def fix_text(t):
    core = re.sub(r"[^\wà-úÀ-Ú-]", "", t)
    rep = FIXW.get(core.lower())
    return t.replace(core, rep) if rep else t
words = {f: [w for s in json.load(open(f"{S}/audio/IMG_{f}.m.json")) for w in s["words"]] for f in FILES}

def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# tira as pausas dentro de cada trecho (corte seco), mantendo o "rabinho" depois da última palavra
import sys, re; sys.path.insert(0, os.path.dirname(S)); from fala import speech
# Corte: transcrição LITERAL de cada trecho (pega "essa daqui, essa daqui"), tira a 1ª vez de toda repetição,
# depois tira pelo ÁUDIO toda pausa > 0.25 s e todo pedaço de fala sem palavra reconhecida.
PRE, POST, TAIL = 0.06, 0.10, 0.85
VERD_SRC = {("6385", 24.00), ("6388", 25.66), ("6389", 36.38), ("6390", 25.06), ("6391", 12.98), ("6393", 16.84),
            ("6394", 25.12), ("6395", 36.34), ("6396", 23.02), ("6396", 52.56), ("6398", 15.56), ("6399", 10.02),
            ("6401", 32.28), ("6403", 24.16), ("6404", 9.46), ("6405", 50.86), ("6406", 33.84), ("6407", 25.42),
            ("6408", 30.36), ("6409", 12.46), ("6410", 32.24), ("6412", 9.20), ("6412", 18.30)}
def norm(t): return re.sub(r"[^\wà-úÀ-Ú]", "", t.lower())
KEPT = {f: [] for f in FILES}
REPL = [("6394", ["puxar", "ele,"], ["pro", "Chile,"]), ("6401", ["por", "aí,", "enrodeia"], ["pra", "ir", "em", "rodeio"]),
        ("6396", ["camor,", "se"], ["camurça,"]), ("6396", ["portanto,"], ["coitada"]), ("6396", ["quis", "se"], ["que", "se"]),
        ("6397", ["fundo."], ["couro."]), ("6397", ["Perfeito."], ["Perfeita."]), ("6385", ["a", "cintura", "abaixo,"], ["cintura", "baixa,"]),
        ("6393", ["camela."], ["canela."]), ("6408", ["levada,"], ["elevada,"]), ("6405", ["croppedes"], ["croppeds"]),
        ("6409", ["R", "$40"], ["R$", "40"]), ("6394", ["fingo"], ["finge"]),
        ("6412", ["Da..."], ["ainda"]), ("6399", ["passado", "também,"], []),
        ("6396", ["camorceuzinho."], ["camurça."]), ("6396", ["cuidado,"], ["coitada,"]), ("6396", ["tostinhas"], ["tachinhas"])]
REMOVIDOS = []
pieces = []
for f, a, b in SEGS:
    VW = json.load(open(f"{S}/audio/verb_{f}_{a:.2f}_{b:.2f}.json"))
    nxt_after = [w["start"] for w in VW if w["start"] >= b - 0.02]
    VW = [w for w in VW if (a - 0.05 <= w["start"] or (w["end"] >= a + 0.10 and w["end"] - w["start"] > 0.05)) and w["start"] < b - 0.02]
    if not VW:
        VW = [dict(w) for w in words[f] if a - 0.05 <= w["start"] < b - 0.02]
    if not VW: continue
    first3 = {norm(w["word"]) for w in VW[:3]}
    extra = [dict(w) for w in words[f] if a - 0.05 <= w["start"] < VW[0]["start"] - 0.02 and norm(w["word"]) not in first3]
    VW = extra + VW
    for rf, old, new in REPL:
        if rf != f: continue
        for i in range(len(VW) - len(old) + 1):
            if [norm(w["word"]) for w in VW[i:i + len(old)]] == [norm(o) for o in old]:
                VW[i] = dict(VW[i], word=" ".join(new) if new else "")
                for k in range(1, len(old)): VW[i + k] = dict(VW[i + k], word="")
    VW = [w for w in VW if w["word"].strip()]
    tok = [norm(w["word"]) for w in VW]
    drop = set()
    for n in range(6, 0, -1):
        i = 0
        while i + 2 * n <= len(tok):
            if all(tok[i + k] and tok[i + k] == tok[i + n + k] for k in range(n)) and not drop & set(range(i, i + 2 * n)):
                drop.update(range(i, i + n)); REMOVIDOS.append((f, " ".join(tok[i:i + n]))); i += n
            else: i += 1
    hard_end = (min(nxt_after) - 0.04) if nxt_after else b + 0.6
    runs, cur = [], []
    for i, w in enumerate(VW):
        if i in drop:
            if cur: runs.append((cur, VW[i]["start"] - 0.03)); cur = []
        else: cur.append(w)
    if cur: runs.append((cur, hard_end))
    ivs, _ = speech(f, a - 0.2, b + 0.6)
    seg_pieces = []
    for ws, lim in runs:
        r0, r1 = max(a - 0.15, ws[0]["start"] - PRE), min(ws[-1]["end"] + POST, lim)
        for s0, e0 in ivs:
            lo, hi = max(r0, s0 - PRE), min(r1, e0 + POST)
            if hi - lo < 0.06: continue
            if not any(lo - 0.12 <= w["start"] <= hi for w in ws): continue
            if seg_pieces and (lo - seg_pieces[-1][1] < 0.10 or any(seg_pieces[-1][1] - 0.05 <= w["start"] <= lo for w in ws)):
                seg_pieces[-1][1] = hi
            else: seg_pieces.append([lo, hi])
        KEPT[f] += ws
    if not seg_pieces: continue
    if any(a <= vt <= b for vf, vt in VERD_SRC if vf == f):
        seg_pieces[-1][1] = min(max(seg_pieces[-1][1], seg_pieces[-1][1] - POST + TAIL), hard_end, b + 0.6)
    if f == "6412" and b > 81: seg_pieces[-1][1] = b
    for s0, e0 in seg_pieces:
        if pieces and pieces[-1][0] == f and s0 < pieces[-1][2]: s0 = pieces[-1][2]
        if e0 - s0 > 0.08: pieces.append((f, s0, e0))
print("repetições tiradas:", REMOVIDOS, flush=True)
ASSIGN, used = {}, set()
for k, (f, a, b) in enumerate(pieces):
    ASSIGN[k] = []
    for w in KEPT[f]:
        if id(w) in used: continue
        if w["start"] < b - 0.03 and w["end"] > a + 0.05:
            ASSIGN[k].append(w); used.add(id(w))
if os.environ.get("DRY"):
    for k, (f, a, b) in enumerate(pieces): print(f, round(a, 2), round(b, 2), " ".join(w["word"].strip() for w in ASSIGN[k]))
SEGS = [(f, round(a * 30) / 30, round(b * 30) / 30) for f, a, b in pieces]   # grade de quadros (30 fps)
SPEED = 1.25
timeline, t = [], 0.0
for i, seg in enumerate(SEGS):
    d = round((seg[2] - seg[1]) / SPEED * 30) / 30
    z = 1.0
    timeline.append((seg, t, d, z)); t += d
TOTAL = t
END = 3.0
INTRO = sum(d for seg, o, d, z in timeline if seg[0] == "6380")

def at(f, src_t):
    for seg, o, d, z in timeline:
        if seg[0] == f and seg[1] - 0.01 <= src_t <= seg[2] + 0.01:
            return o + (src_t - seg[1]) / SPEED
    nxt = [o for seg, o, d, z in timeline if seg[0] == f and seg[1] > src_t]
    if nxt: return min(nxt)
    raise ValueError((f, src_t))
def seg_end_at(f, src_t):
    for seg, o, d, z in timeline:
        if seg[0] == f and seg[1] - 0.01 <= src_t <= seg[2] + 0.01:
            return o + d
    nxt = [o + d for seg, o, d, z in timeline if seg[0] == f and seg[1] > src_t]
    return min(nxt)

# ---------- legendas das falas (dinâmicas) — não na intro (lá entram as palavras grandes) ----------
caps, seg_end = [], []
for i, (seg, o, d, z) in enumerate(timeline):
    f, a, b = seg
    if f == "6380": continue
    chunk = []
    for w in ASSIGN[i - 0]:
        txt = fix_text(w["word"].strip())
        if not txt: continue
        if txt.startswith("-") and chunk:
            p = chunk[-1]; chunk[-1] = (p[0] + txt, p[1], o + (min(w["end"], b) - a) / SPEED); continue
        st = max(o, o + (w["start"] - a) / SPEED)
        if chunk and st <= chunk[-1][1] + 0.1: st = chunk[-1][1] + 0.12
        chunk.append((txt, st, max(o + (min(w["end"], b) - a) / SPEED, st + 0.1)))
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
    ("6401", 32.28, "fica"), ("6403", 24.16, "fica"), ("6404", 9.46, "fica"), ("6405", 50.86, "fica"),
    ("6406", 33.84, "fica ou|vai embora?"), ("6407", 21.56, "fica"), ("6408", 30.36, "fica"),
    ("6409", 12.46, "fica"), ("6410", 32.24, "fica"),     ("6412", 9.20, "fica"), ("6412", 18.30, "fica ou|vai embora?"),
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
CARD_A = INTRO; CARD_B = INTRO + 1.8
overlays.append((CARD_A, CARD_B, "Card", 540, 1010, r"{\fad(0,200)}" + POP + "calças"))
sfx.append(("bling", CARD_A + 0.1, 0.0, 0.45))
SPARK = [  # (x, y, tamanho, atraso)
    (175, 880, 100, 0.10), (850, 900, 80, 0.16), (220, 1080, 64, 0.22), (880, 1075, 104, 0.12), (585, 860, 56, 0.26),
]

# ---------- placar fixo: ficou / saiu / ? ----------
ev = []
for f, wt, txt in VERD:
    k = "talvez" if txt.startswith("fica ou") else ("ficou" if txt.startswith("fica") else "saiu")
    ev.append((at(f, wt), k))
ev.sort()
cnt = {"ficou": 0, "saiu": 0, "talvez": 0}
GRAY = "&HFFFFFF&"
def placar(c, changed):
    def num(k):
        n = str(c[k])
        if k == changed:
            return r"{\fscx40\fscy40\t(0,120,\fscx135\fscy135)\t(120,220,\fscx100\fscy100)}" + n + r"{\fscx100\fscy100}"
        return n
    out = r"{\c&HFFFFFF&}ficou {\c&HA6F3FF&}" + num("ficou") + r"{\c&HFFFFFF&}   ·   saiu {\c&HA6F3FF&}" + num("saiu")
    if c["talvez"]: out += r"{\c&HFFFFFF&}   ·   ? {\c&HA6F3FF&}" + num("talvez")
    return out
t0, changed = INTRO, None
for t1, k in ev + [(None, None)]:
    b = t1 if t1 is not None else TOTAL + END
    overlays.append((t0, b, "Placar", 540, 230, (r"{\fad(200,0)}" if changed is None else "") + placar(cnt, changed)))
    if k is None: break
    cnt[k] += 1; t0, changed = t1, k
print("placar final:", cnt)

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
    (TOTAL, TOTAL + END, "End", 540, 400, r"{\fad(0,250)}" + bounce_line(["vem", "aí", "o"], END_T0, 0.17)),
    (TOTAL, TOTAL + END, "End", 520, 540, r"{\fad(0,250)\fs150}" + bounce_line(["ep.", "2"], END_T0 + 0.6, 0.2)),
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
Style: Placar,Nunito Black,50,&H00A6F3FF,&H00FFFFFF,&H00000000,&H9A3A2A1A,0,0,0,0,100,100,-1,0,1,0,4,5,40,40,0,1
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
    tass += f"Dialogue: 0,{ts(a)},{ts(b)},Title,,0,0,0,,{{\\pos(540,330)}}{title_body(n, True)}\n"
TYPE_DONE = TYPE_START + (len(typed) - 1) * TYPE_STEP
t, on = TYPE_DONE, True     # cursor piscando depois de digitar
while t < 2.6:
    tass += f"Dialogue: 0,{ts(t)},{ts(t+0.3)},Title,,0,0,0,,{{\\pos(540,330)}}{title_body(typed[-1], on)}\n"
    t += 0.3; on = not on
tass += f"Dialogue: 0,{ts(t)},{ts(INTRO)},Title,,0,0,0,,{{\\pos(540,330)\\fad(0,200)}}{title_body(typed[-1], False)}\n"
tass += f"Dialogue: 0,{ts(TYPE_DONE+0.25)},{ts(INTRO)},Title,,0,0,0,,{{\\pos(800,470)\\fs58\\fad(0,200)}}{POP}ep. 1\n"
open(f"{OUT}/legendas.ass", "a").write(tass[len(STY):])

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
if os.environ.get("DRY"): print(f"DRY duração {TOTAL+END:.1f}s, {len(timeline)} cortes"); raise SystemExit
# 1) cada corte vira um arquivo (evita estourar a memória com dezenas de trims do mesmo arquivo)
PCS = f"{OUT}/pecas"; os.makedirs(PCS, exist_ok=True)
lst = []
for i, (seg, o, d, z) in enumerate(timeline):
    f, a, b = seg
    cw, chh = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    n = round(d * 30)
    pf = f"{PCS}/{i:03d}.mkv"; lst.append(f"file '{pf}'")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(a-1,0):.3f}", "-i", f"{PROXY}/IMG_{f}.mp4",
        "-filter_complex", f"[0:v]trim=start={a-max(a-1,0):.4f},setpts=(PTS-STARTPTS)/{SPEED},crop={cw}:{chh}:(iw-{cw})/2:(ih-{chh})*0.62,scale={W}:{H},fps=30,setsar=1,format=yuv420p,trim=end_frame={n}[v];"
        f"[0:a]atrim=start={a-max(a-1,0):.4f},asetpts=PTS-STARTPTS,atempo={SPEED},aresample=48000,aformat=channel_layouts=stereo,atrim=end={n/30:.4f},apad=whole_dur={n/30:.4f},"
        f"afade=t=in:d=0.02,afade=t=out:st={max(n/30-0.03,0):.3f}:d=0.03[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-c:a", "pcm_s16le", pf], check=True)
open(f"{OUT}/pecas.txt", "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/pecas.txt",
                "-c", "copy", f"{OUT}/base.mkv"], check=True)
print("peças ok", flush=True)
inputs, fc = ["-i", f"{OUT}/base.mkv"], []
si = inputs.count("-i"); inputs += ["-loop", "1", "-i", f"{OUT}/sparkle.png"]
esc = lambda p: p.replace(":", r"\:")
fc.append("[0:v]setpts=PTS-STARTPTS[vc]"); fc.append("[0:a]asetpts=PTS-STARTPTS[ac]")
fc.append("[vc]null[b2]")
fc.append(f"[b2]tpad=stop_mode=clone:stop_duration={END},subtitles='{esc(OUT)}/legendas.ass':fontsdir={FONTS}[v0s]")
# ✨ do cartão + ✨ do fechamento
nsp = len(SPARK) + 1
fc.append(f"[{si}:v]format=rgba,split={nsp}" + "".join(f"[sp{j}]" for j in range(nsp)))
cur = "v0s"
for j, (x, y, size, dl) in enumerate(SPARK + [(800, 540, 110, 0.0)]):
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

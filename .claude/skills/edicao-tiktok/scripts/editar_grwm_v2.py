"""Arrume-sisi comigo — torneio relâmpago de beach tennis. VERSÃO 2.
Mudanças pedidas por ela + vídeo de referência (criadoras que ela gosta):
- cortes pelo ÁUDIO: tira pausas/respirações (silêncio >= 0,3 s) mas deixa a palavra terminar (folga 0,12 s)
- frases completas (não picotar a história)
- títulos no estilo da referência: nomeiam o que aparece, digitados letra a letra, serifa itálica / manuscrita,
  checklist com ✓ aparecendo, palavra espalhada várias vezes; sem emoji/símbolo estilo Android
- marca falada -> marca + cupom GABISILVA na tela (HIPY, Spin Grip)
- sons da biblioteca sons/ (CC0) só onde a imagem pede
"""
import json, subprocess, os, wave, math, random
import numpy as np

S = os.environ.get("EDIT_WORK", os.getcwd())
PROXY, OUT = f"{S}/proxy", f"{S}/render2"
os.makedirs(OUT, exist_ok=True)
SKILL = "/home/user/Claude/.claude/skills/edicao-tiktok"
FONTS, SONS = f"{SKILL}/fonts", f"{SKILL}/sons"
W, H = 1080, 1920
FILES = ("IMG_6257", "IMG_6258", "IMG_6259", "IMG_6262", "IMG_6263", "IMG_6264")

# Frases escolhidas (arquivo, início, fim, modo). modo: "fala" = corta silêncios por dentro;
# "inteiro" = sem cortes internos; "4x" = acelerado com o áudio real acelerado
PHRASES = [
    ("IMG_6257", 8.45, 11.40, "fala"),     # gancho (2ª tomada)
    ("IMG_6257", 14.25, 20.75, "fala"),    # e agora no nosso arrume-sisi comigo... tripé que me segue
    ("IMG_6257", 21.50, 23.20, "fala"),    # não, silêncio, deixa eu blogueira
    ("IMG_6257", 32.85, 46.45, "fala"),    # agenda do fim de semana (+ mudou de ideia)
    ("IMG_6257", 46.75, 50.85, "fala"),    # domingo apenas uma corrida
    ("IMG_6257", 55.35, 61.00, "fala"),    # Garmin + tadinho dele
    ("IMG_6258", 6.80, 11.45, "fala"),     # conjunto da HIPY
    ("IMG_6258", 13.55, 16.70, "fala"),    # tá na black e tem cupom
    ("IMG_6258", 27.85, 33.95, "fala"),    # sustentação absurda... fica 10
    ("IMG_6259", 13.30, 14.60, "inteiro"), # REVELAÇÃO vestida
    ("IMG_6259", 20.00, 23.30, "fala"),    # esse conjunto é maravilhoso
    ("IMG_6259", 23.50, 25.30, "inteiro"), # bailarina (braços)
    ("IMG_6259", 29.10, 31.20, "fala"),    # não nasci com coordenação
    ("IMG_6259", 36.00, 40.85, "fala"),    # balé, jazz, hip hop, nada deu certo
    ("IMG_6262", 10.85, 12.95, "fala"),    # bora arrumar a cara em dois segundos
    ("IMG_6262", 13.75, 16.50, "fala"),    # adivinha? atrasada!
    ("IMG_6262", 23.25, 25.05, "fala"),    # vou arrumar o meu cabelo
    ("IMG_6262", 31.60, 34.95, "fala"),    # não vai dar pra fazer o que eu queria
    ("IMG_6262", 35.00, 39.40, "4x"),      # prendendo o cabelo
    ("IMG_6262", 64.00, 70.85, "fala"),    # colar do TikTok Shop
    ("IMG_6262", 84.80, 86.85, "fala"),    # esqueci a xuxinha
    ("IMG_6263", 0.40, 14.35, "fala"),     # blush, sem criatividade, sem tempo, novidade
    ("IMG_6263", 21.80, 25.50, "fala"),    # batidinha de pó e bora
    ("IMG_6264", 0.50, 5.85, "fala"),      # pronto gente, look
    ("IMG_6264", 9.70, 17.60, "fala"),     # grips Spin Grip, vitrine, cupom no site
    ("IMG_6264", 23.75, 26.05, "inteiro"), # arrume-sisi comigo hoje foi express. beijo! (congela)
]
NOCAP_SRC = [("IMG_6259", 13.30, 14.60), ("IMG_6259", 23.50, 23.95)]  # fala ininteligível: sem legenda

FIX = {
    ("IMG_6257", 8.62): "Arrume-sisi", ("IMG_6257", 8.88): "", ("IMG_6257", 8.98): "",
    ("IMG_6257", 9.38): "pra", ("IMG_6257", 10.5): "beach tennis?",
    ("IMG_6257", 15.6): "arrume-sisi", ("IMG_6257", 15.88): "", ("IMG_6257", 16.0): "", ("IMG_6257", 16.1): "comigo",
    ("IMG_6257", 56.04): "Garmin",
    ("IMG_6258", 10.9): "HIPY,", ("IMG_6258", 15.34): "", ("IMG_6258", 15.48): "tem", ("IMG_6258", 15.64): "",
    ("IMG_6258", 15.84): ["cupom", ""], ("IMG_6258", 16.0): "de", ("IMG_6258", 33.4): "10!",
    ("IMG_6259", 36.36): "tentou,", ("IMG_6259", 36.78): "viu,",
    ("IMG_6259", 38.08): "balé,", ("IMG_6259", 38.58): "jazz,", ("IMG_6259", 39.32): "hop...",
    ("IMG_6259", 30.58): "pra", ("IMG_6259", 29.22): "",
    ("IMG_6262", 86.11): "xuxinha!",
    ("IMG_6263", 0.0): "", ("IMG_6263", 2.44): "aqui,", ("IMG_6263", 4.36): "só,", ("IMG_6263", 6.0): "tô",
    ("IMG_6263", 9.26): "tempo,", ("IMG_6263", 21.98): "batidinha",
    ("IMG_6264", 12.58): "Spin Grip,", ("IMG_6264", 16.28): "site,", ("IMG_6264", 16.56): "GABISILVA.",
    ("IMG_6264", 23.88): "Arrume-sisi", ("IMG_6264", 24.04): "", ("IMG_6264", 24.82): "express.",
}
FIX_TEXT = {"para": "pra", "está": "tá", "estava": "tava"}
words = {f: [w for s in json.load(open(f"{S}/audio/{f}.m.json")) for w in s["words"]] for f in FILES}

# ---------- energia do áudio (para achar pausas e respirações) ----------
ENV = {}
for f in FILES:
    wv = wave.open(f"{S}/audio/{f}.wav"); x = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(float) / 32768
    hop = 320; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    db = np.maximum.reduce([np.roll(db, k) for k in (-2, -1, 0, 1, 2)])  # suaviza 100 ms
    ENV[f] = (db, np.percentile(db, 90) - 22)  # limiar: 18 dB abaixo da fala

def speech_runs(f, a, b, min_sil=0.30, pad_end=0.12, pad_start=0.07):
    db, thr = ENV[f]; i0, i1 = int(a * 50), int(b * 50)
    loud = db[i0:i1] > thr
    for w in words[f]:  # nenhuma palavra pode ser cortada: o início de cada palavra conta como fala
        ws, we = w["start"] - 0.04, w["start"] + min(w["end"] - w["start"], 0.45)
        k0, k1 = max(int(ws * 50) - i0, 0), min(int(we * 50) - i0, len(loud))
        if k1 > k0: loud[k0:k1] = True
    runs, k = [], 0
    while k < len(loud):
        if loud[k]:
            j = k
            while j < len(loud) and loud[j]: j += 1
            runs.append([(i0 + k) / 50, (i0 + j) / 50]); k = j
        else: k += 1
    merged = []
    for r in runs:  # junta falas separadas por menos de min_sil
        if merged and r[0] - merged[-1][1] < min_sil: merged[-1][1] = r[1]
        else: merged.append(r)
    merged = [r for r in merged if r[1] - r[0] >= 0.12]  # descarta estalos
    return [(max(a, r[0] - pad_start), min(b, r[1] + pad_end)) for r in merged]

SEGS = []  # (arquivo, a, b, velocidade, zoom, mudo)
z_alt = [1.00, 1.12]
for f, a, b, mode in PHRASES:
    if mode == "4x":
        SEGS.append((f, a, b, 4, 1.00, True)); continue
    runs = [(a, b)] if mode == "inteiro" else speech_runs(f, a, b)
    for k, (ra, rb) in enumerate(runs):
        pieces = [(ra, rb)]
        if rb - ra > 4.2:  # fala longa: troca o zoom no meio, entre duas palavras (sem tirar nada)
            mid = [w["start"] for w in words[f] if ra + 1.8 < w["start"] < rb - 1.5]
            if mid:
                cut = min(mid, key=lambda x: abs(x - (ra + rb) / 2)) - 0.03
                pieces = [(ra, cut), (cut, rb)]
        for pa, pb in pieces:
            SEGS.append((f, round(pa, 2), round(pb, 2), 1, z_alt[len(SEGS) % 2], False))

def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

timeline, t = [], 0.0
for seg in SEGS:
    d = (seg[2] - seg[1]) / seg[3]; timeline.append((seg, t, d)); t += d
TOTAL, END = t, 3.0

def at(f, src_t):
    """tempo de saída de um instante do bruto (o segmento que contém, ou o mais próximo depois)"""
    best = None
    for seg, o, d in timeline:
        if seg[0] != f: continue
        if seg[1] - 0.02 <= src_t <= seg[2] + 0.02: return o + (min(max(src_t, seg[1]), seg[2]) - seg[1]) / seg[3]
        if seg[1] > src_t and (best is None or seg[1] < best[0]): best = (seg[1], o)
    return best[1] if best else None
def seg_end_of(f, src_t):
    for seg, o, d in timeline:
        if seg[0] == f and seg[1] - 0.02 <= src_t <= seg[2] + 0.02: return o + d
    return None

# ---------- legendas da fala (estilo aprovado) ----------
def nocap(f, t): return any(f == g and a <= t <= b for g, a, b in NOCAP_SRC)
caps, seg_end = [], []
USED = set()
for i, (seg, o, d) in enumerate(timeline):
    f, a, b, sp, z, mute = seg
    if mute: continue
    chunk = []
    for w in [w for w in words[f] if a - 0.05 <= w["start"] < b - 0.03]:
        if nocap(f, w["start"]): continue
        key = (f, round(w["start"], 2))
        if key in FIX and isinstance(FIX[key], list):
            n_ = sum(1 for u in USED if u[:2] == key); txt = FIX[key][n_] if n_ < len(FIX[key]) else w["word"].strip(); USED.add(key + (n_,))
        else:
            txt = FIX[key] if key in FIX and key not in USED else w["word"].strip()
            if key in FIX: USED.add(key)
        txt = FIX_TEXT.get(txt, txt)
        if not txt: continue
        wa = o + (max(w["start"], a) - a); wb = o + (min(w["end"], b) - a)
        chunk.append((txt, wa, max(wb, wa + 0.08)))
        if len(chunk) >= 3 or txt[-1] in ",.?!": caps.append(chunk); seg_end.append(o + d); chunk = []
    if chunk: caps.append(chunk); seg_end.append(o + d)
fixed = []
for k, ch in enumerate(caps):
    a, b = ch[0][1], ch[-1][2]; nxt = caps[k + 1][0][1] if k + 1 < len(caps) else TOTAL
    fixed.append((a, min(max(b + 0.2, a + 0.4), nxt, b + 0.5, seg_end[k] + 0.0), ch))
caps = fixed

# ---------- títulos no estilo da referência ----------
CREAM, YEL, PINK, WHITE = "&HC8F4FF&", "&H7FE6FF&", "&HB45CFF&", "&HFFFFFF&"
POP = r"{\fscx30\fscy30\t(0,110,\fscx112\fscy112)\t(110,190,\fscx100\fscy100)}"
EV = []  # (camada, início, fim, estilo, texto)
def typed(t0, t1, style, x, y, text, color=CREAM, step=0.045, extra=""):
    """aparece letra por letra (letras ainda não digitadas ficam invisíveis — o texto não pula)"""
    vis = [i for i, c in enumerate(text) if c not in " \n"]
    for k, n in enumerate(vis):
        a = t0 + k * step; b = t0 + (k + 1) * step if k + 1 < len(vis) else t1
        if a >= t1: break
        body = "".join(("{\\alpha&H00&}" if i <= n else "{\\alpha&HFF&}") + (r"\N" if c == "\n" else c) for i, c in enumerate(text))
        fade = r"\fad(0,180)" if k + 1 == len(vis) else ""
        EV.append((2, a, b, style, f"{{\\pos({x},{y})\\c{color}{extra}{fade}}}{body}"))
def label(t0, t1, style, x, y, text, color=CREAM, rot=0):
    EV.append((2, t0, t1, style, f"{{\\pos({x},{y})\\c{color}\\frz{rot}\\fad(0,150)}}{POP}{text}"))
def arc(t0, t1, style, cx, cy, text, radius=520, span=34, color=CREAM, fs=None):
    """texto em arco por cima (como "1 milhão de seguidores" da referência), letra a letra"""
    n = len(text)
    for i, c in enumerate(text):
        if c == " ": continue
        ang = math.radians(-span / 2 + span * i / max(n - 1, 1))
        x = cx + radius * math.sin(ang); y = cy - radius * math.cos(ang) + radius
        a = t0 + i * 0.03
        EV.append((2, a, t1, style, f"{{\\an5\\pos({x:.0f},{y:.0f})\\frz{-math.degrees(ang):.1f}\\c{color}"
                                     f"{'\\fs%d' % fs if fs else ''}\\fad(60,150)}}{c}"))
def scatter(t0, t1, style, word, n=6, seed=3, color=WHITE):
    """palavra repetida espalhada (como "Lindona", "Não não não" da referência)"""
    rnd = random.Random(seed)
    spots = [(260, 520), (800, 600), (330, 880), (760, 980), (540, 760), (240, 1150), (840, 1220)]
    for k in range(n):
        x, y = spots[k % len(spots)]; x += rnd.randint(-40, 40); y += rnd.randint(-30, 30)
        EV.append((2, t0 + k * 0.12, t1, style, f"{{\\pos({x},{y})\\frz{rnd.randint(-18, 18)}\\c{color}\\fad(0,150)}}{POP}{word}"))
CHECK = r"{\p1}m 0 0 b 0 -22 36 -22 36 0 b 36 22 0 22 0 0{\p0}"
def checklist(items, t_end, x=80, y0=300, dy=86):
    """lista no canto com ✓ aparecendo um a um (referência: "Percurso da prova / Altimetria...")"""
    for k, (t, txt) in enumerate(items):
        y = y0 + k * dy
        EV.append((2, t, t_end, "Check", f"{{\\an4\\pos({x},{y})\\fad(0,200)}}{POP}{{\\c{YEL}}}●"))
        EV.append((3, t + 0.05, t_end, "CheckMark", f"{{\\an4\\pos({x + 9},{y + 2})\\fad(0,200)}}✓"))
        EV.append((2, t, t_end, "List", f"{{\\an4\\pos({x + 70},{y})\\fad(0,200)}}{txt}"))
def coupon(t0, t1, brand, y=420):
    """marca + cupom (pedido dela: marca falada -> cupom GABISILVA na tela)"""
    typed(t0, t1, "Serif", 540, y, brand, color=YEL, step=0.05)
    EV.append((2, t0 + 0.35, t1, "Pill", f"{{\\pos(540,{y + 95})\\fad(120,150)}}{POP}cupom {{\\b1}}GABISILVA"))

# --- gancho: título digitado (estilo aprovado "Melhor DICA pra sua PROVA"), sem ✦
hook = [(WHITE, "Arrume-sisi comigo pro"), (WHITE, "\n"), (PINK, "TORNEIO "), (YEL, "RELÂMPAGO")]
chars = [(c, ch) for c, tx in hook for ch in tx]; vis = [i for i, (c, ch) in enumerate(chars) if ch not in " \n"]
HOOK_END = at("IMG_6257", 14.3) + 0.6
for k, n in enumerate(vis):
    a = 0.15 + k * 0.045; b = 0.15 + (k + 1) * 0.045 if k + 1 < len(vis) else HOOK_END
    body = "".join(("{\\c%s\\alpha&H00&}" % c if i <= n else "{\\alpha&HFF&}") + (r"\N" if ch == "\n" else ch) for i, (c, ch) in enumerate(chars))
    EV.append((2, a, b, "Title", f"{{\\pos(540,330)}}{r'{\\fad(0,200)}' if k + 1 == len(vis) else ''}{body}"))

# --- títulos ao longo do vídeo
arc(at("IMG_6257", 16.9), at("IMG_6257", 19.0), "Serif", 540, 360, "mais chiques", radius=420, span=40, color=YEL)
typed(at("IMG_6257", 19.4), seg_end_of("IMG_6257", 20.3), "Hand", 540, 470, "tripé que me segue", color=WHITE)
AG_END = seg_end_of("IMG_6257", 45.9)
checklist([(at("IMG_6257", 38.2), "mista · manhã"), (at("IMG_6257", 40.8), "feminina · tarde"),
           (at("IMG_6257", 41.85), "sábado · descansar?"), (at("IMG_6257", 47.3), "domingo · corrida")],
          seg_end_of("IMG_6257", 50.3))
typed(at("IMG_6257", 48.0), seg_end_of("IMG_6257", 50.3), "Serif", 790, 640, "apenas?!", color=YEL)
typed(at("IMG_6257", 56.04), seg_end_of("IMG_6257", 59.0), "Serif", 540, 420, "até o Garmin", color=CREAM)
coupon(at("IMG_6258", 10.5), seg_end_of("IMG_6258", 16.2), "conjunto HIPY")
typed(at("IMG_6258", 29.3), seg_end_of("IMG_6258", 30.1), "Hand", 540, 470, "sustentação absurda", color=WHITE)
label(at("IMG_6259", 13.75), seg_end_of("IMG_6259", 14.0), "Serif", 560, 420, "fica 10!", color=YEL, rot=-4)
typed(at("IMG_6259", 38.0), seg_end_of("IMG_6259", 39.0), "Serif", 540, 420, "balé · jazz · hip hop", color=CREAM, step=0.03)
scatter(at("IMG_6262", 15.75), seg_end_of("IMG_6262", 15.9), "Hand", "atrasada!", n=6)
typed(at("IMG_6262", 23.5), seg_end_of("IMG_6262", 24.4), "Serif", 540, 420, "cabelo", color=CREAM)
label(at("IMG_6262", 35.0), seg_end_of("IMG_6262", 35.5), "Hand", 540, 420, "prendendo... (4x)", color=WHITE, rot=-3)
typed(at("IMG_6262", 65.6), at("IMG_6262", 69.4), "Serif", 540, 400, "colar do TikTok Shop", color=YEL, step=0.035)
typed(at("IMG_6262", 85.9), seg_end_of("IMG_6262", 86.2), "Serif", 540, 420, "xuxinha", color=CREAM)
typed(at("IMG_6263", 1.4), seg_end_of("IMG_6263", 2.2), "Serif", 540, 400, "blush", color=CREAM)
typed(at("IMG_6263", 11.5), seg_end_of("IMG_6263", 11.6), "Hand", 560, 470, "como sempre", color=YEL)
typed(at("IMG_6263", 22.6), seg_end_of("IMG_6263", 23.3), "Serif", 540, 400, "pó", color=CREAM)
typed(at("IMG_6264", 2.4), seg_end_of("IMG_6264", 5.0), "Serif", 540, 400, "look pronto", color=YEL)
coupon(at("IMG_6264", 11.6), seg_end_of("IMG_6264", 17.0), "grips Spin Grip")
# fechamento: congela no beijo, palavras chegando com pulinho (aprovado), sem ✦
def bounce_line(ws, t_first, step, color_of):
    out = ""
    for k, w in enumerate(ws):
        ms = int((t_first + k * step) * 1000)
        out += (r"{\alpha&HFF&\fscy35\blur6\c%s" % color_of(k)
                + r"\t(%d,%d,\alpha&H00&\fscy128\blur0)\t(%d,%d,\fscy92)\t(%d,%d,\fscy100)}" % (ms, ms + 110, ms + 110, ms + 190, ms + 190, ms + 260)
                + w + (" " if k + 1 < len(ws) else ""))
    return out
END_T0 = 0.15
EV.append((2, TOTAL, TOTAL + END, "Title", r"{\pos(540,300)\fad(0,250)}" + bounce_line(["Arrume-sisi", "comigo"], END_T0, 0.17, lambda k: WHITE)))
EV.append((2, TOTAL, TOTAL + END, "Title", r"{\pos(540,395)\fad(0,250)\fs90}" + bounce_line(["EXPRESS"], END_T0 + 0.45, 0.2, lambda k: PINK)))

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,4,2,2,80,80,600,1
Style: Title,Montserrat Thin Black,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,-1,0,0,100,100,-2,0,1,0,6,5,60,60,0,1
Style: Serif,Instrument Serif,104,&H00C8F4FF,&H00FFFFFF,&H00000000,&H70000000,0,-1,0,0,100,100,0,0,1,0,4,5,60,60,0,1
Style: Hand,Patrick Hand,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,0,0,0,100,100,0,0,1,0,4,5,60,60,0,1
Style: List,Poppins SemiBold,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,0,0,0,100,100,0,0,1,0,3,4,60,60,0,1
Style: Check,Poppins SemiBold,64,&H007FE6FF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,60,60,0,1
Style: CheckMark,DejaVu Sans,40,&H00202020,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,4,60,60,0,1
Style: Pill,Poppins SemiBold,46,&H00FFFFFF,&H00FFFFFF,&H00B45CFF,&H00B45CFF,0,0,0,0,100,100,1,0,3,14,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for a, b, ch in caps:
    for j, (wtxt, wa, wb) in enumerate(ch):
        ea = a if j == 0 else wa; eb = ch[j + 1][1] if j + 1 < len(ch) else b
        if eb <= ea: continue
        body = []
        for m, (t2, _, _) in enumerate(ch):
            t2 = t2.rstrip(".,") if m == len(ch) - 1 else t2
            body.append("{\\c&H3DD9FF&\\fscx108\\fscy108}" + t2 + "{\\c&HFFFFFF&\\fscx100\\fscy100}" if m == j else t2)
        pop = "{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
        ass += f"Dialogue: 0,{ts(ea)},{ts(eb)},Cap,,0,0,0,,{pop}{' '.join(body)}\n"
for layer, a, b, st, txt in EV:
    if a is None or b is None or b <= a: continue
    ass += f"Dialogue: {layer},{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(f"{OUT}/legendas.ass", "w").write(ass)

# ---------- sons (biblioteca sons/, só com motivo na tela) ----------
def bell(name, notes, d=0.7, vol=1.6):
    expr = "+".join(f"{amp}*sin(2*PI*{fr}*(t-{st}))*exp(-{dec}*(t-{st}))*gte(t,{st})" for fr, amp, dec, st in notes)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d={d}", "-af",
                    f"afade=t=in:d=0.003,aecho=0.8:0.4:45|90:0.25|0.12,afade=t=out:st={d-0.15}:d=0.15,pan=stereo|c0=c0|c1=c0,volume={vol}",
                    f"{OUT}/plim.wav"], check=True)
bell("plim", [(1568, 0.5, 7, 0), (2349, 0.3, 9, 0), (3136, 0.12, 12, 0)])
TYPE_DUR = 0.045 * len(vis)  # teclado só enquanto o título do gancho é digitado
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{SONS}/keyboard_typing.wav", "-af",
                f"atrim=0:{TYPE_DUR:.3f},afade=t=in:d=0.03,afade=t=out:st={TYPE_DUR-0.15:.3f}:d=0.15", f"{OUT}/teclado_gancho.wav"], check=True)
def snd(n): return f"{OUT}/{n}.wav" if os.path.exists(f"{OUT}/{n}.wav") else f"{SONS}/{n}.wav"
# (som, momento na timeline, onde fica o pico dentro do som, volume, motivo)
SFX = [
    ("teclado_gancho", 0.15, 0.0, 0.10, "título do gancho sendo digitado (baixinho, pedido dela)"),
    ("click", at("IMG_6257", 10.34), 0.0, 0.35, "logo depois de 'torneio relâmpago' (pedido dela)"),
    ("click", at("IMG_6257", 38.2), 0.0, 0.35, "✓ mista aparece"),
    ("click", at("IMG_6257", 40.8), 0.0, 0.35, "✓ feminina aparece"),
    ("click", at("IMG_6257", 41.85), 0.0, 0.35, "✓ sábado aparece"),
    ("record_scratch", at("IMG_6257", 44.55), 0.02, 0.07, "'Não, na verdade talvez não' — quebra de expectativa"),
    ("click", at("IMG_6257", 47.3), 0.0, 0.35, "✓ domingo aparece"),
    ("pop", at("IMG_6258", 10.85), 0.0, 0.40, "cupom HIPY entra na tela"),
    ("whoosh_soft", at("IMG_6259", 13.30), 0.30, 0.55, "corte do closet pra ela vestida (mudança de cena)"),
    ("impact_soft", at("IMG_6259", 13.80), 0.0, 0.55, "look revelado (mãos na cintura)"),
    ("boing", at("IMG_6259", 23.95), 0.0, 0.06, "braços de bailarina (movimento exagerado)"),
    ("sad_trombone", at("IMG_6259", 39.80), 0.0, 0.30, "'nada deu certo' — expectativa frustrada"),
    ("whoosh_soft", at("IMG_6262", 10.85), 0.30, 0.55, "muda de ambiente: closet -> penteadeira"),
    ("sparkle", at("IMG_6262", 65.6), 0.0, 0.30, "colar em destaque"),
    ("whoosh_soft", at("IMG_6264", 0.50), 0.30, 0.55, "muda de ambiente: penteadeira -> look pronto"),
    ("pop", at("IMG_6264", 11.95), 0.0, 0.40, "cupom Spin Grip entra na tela"),
    ("plim", TOTAL + END_T0 + 0.45 + 0.1, 0.0, 0.50, "'EXPRESS' chega no fechamento"),
]

LOOK = "eq=contrast=1.06:saturation=1.14:brightness=0.01,colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03"
SEGDIR = f"{OUT}/segs"; os.makedirs(SEGDIR, exist_ok=True)
LISTDIR = os.environ.get("SEGLIST_DIR", SEGDIR)  # ex.: segs_bokeh (cortes com bokeh)
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
            af = f"asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.025,afade=t=out:st={max(d-0.05,0):.3f}:d=0.05"
        o_ = f"{SEGDIR}/s{i:03d}.mkv"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a}", "-t", f"{b-a:.3f}", "-i", f"{PROXY}/{f}.mp4",
                        "-vf", vf, "-af", af, "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                        "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", o_], check=True)
        lst.append(f"file '{o_}'")
    open(f"{SEGDIR}/list.txt", "w").write("\n".join(lst) + "\n")

ass_path = f"{OUT}/legendas.ass".replace(":", r"\:")
inputs = ["-f", "concat", "-safe", "0", "-i", f"{LISTDIR}/list.txt"]
fc = [f"[0:v]tpad=stop_mode=clone:stop_duration={END},{LOOK},subtitles='{ass_path}':fontsdir={FONTS},fade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[vout]",
      f"[0:a]apad=pad_dur={END}[acp]"]
mix = ["[acp]"]
for j, (name, peak, inner, vol, why) in enumerate(SFX):
    idx = len(inputs) // 2 - 2; inputs += ["-i", snd(name)]
    start = peak - inner; cut = max(-start, 0); ms = int(max(start, 0) * 1000)
    fc.append(f"[{idx}:a]atrim=start={cut:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{j}]"); mix.append(f"[s{j}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,afade=t=out:st={TOTAL+END-0.8:.2f}:d=0.8[aout]")

if os.environ.get("DRY"):
    print(f"duração {TOTAL+END:.1f}s, {len(SEGS)} cortes")
    for seg, o, d in timeline: print(f"  {o:6.2f} +{d:4.2f}  {seg[0]} {seg[1]:.2f}-{seg[2]:.2f}")
    for a, b, ch in caps: print(f"{a:6.2f} {' '.join(c[0] for c in ch)}")
    for name, peak, inner, vol, why in SFX: print(f"SFX {peak:6.2f} {name:15s} {why}")
    raise SystemExit
if not os.environ.get("SKIPSEGS"): render_segs()
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                "-c:a", "pcm_s16le", f"{OUT}/pre.mkv"], check=True)
# volume final -14 LUFS em duas passadas
j = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{OUT}/pre.mkv", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
m = json.loads(j[j.rindex("{"):j.rindex("}") + 1])
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{OUT}/pre.mkv", "-c:v", "copy", "-af",
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
                f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/" + os.environ.get("OUTNAME", "grwm_v2.mp4")], check=True)
print(f"OK duração {TOTAL+END:.1f}s")

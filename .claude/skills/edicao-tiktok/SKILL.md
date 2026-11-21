---
name: edicao-tiktok
description: Edita de verdade os vídeos brutos dela para TikTok/Reels (rotina, unboxing, falando pra câmera) no estilo aprovado — decupagem, legenda dinâmica, títulos, rótulos, cor, sons que seguem a imagem e fechamento. Use quando ela mandar vídeo bruto (upload ou pasta do Dropbox) para editar, ou pedir ajuste numa edição.
---

# Edição TikTok/Reels — estilo dela

Estilo construído e aprovado no vídeo "tripé com inteligência artificial" (versão 11, postada).
O script `scripts/editar_exemplo_tripe.py` é a edição aprovada completa: **copie e adapte**, não comece do zero.

**Leia também `MANUAL_SONS.md`** — o manual dela com a biblioteca oficial de efeitos (`sons/`),
quando usar cada um, regras obrigatórias e o relatório final com tempo de cada efeito. Vale para toda edição.

## Fluxo

1. **Receber os brutos.** Upload no chat aceita só ~30 s; vídeos maiores vêm por pasta do Dropbox
   (baixar o link da pasta com `dl=1`, que vem como .zip). Conferir se algum arquivo é cópia/trecho de outro
   (comparar a transcrição) e usar cada trecho uma vez só.
2. **Cópias de trabalho** 1080x1920 (`proxy/`), áudio 16 kHz mono (`audio/`).
3. **Transcrever** com `scripts/transcrever.py` (Whisper `medium`, palavra a palavra; o `small` erra muito).
   O Whisper erra gírias/termos: ex. ela disse "carrinho laranja" e ele ouviu "carro em laranja".
   **Nunca inventar fala**: trecho duvidoso fica sem legenda e eu pergunto pra ela.
4. **Decupar**: tirar pausas, falas repetidas (mesma frase dita duas vezes → fica uma) e tentativas.
   Ver quadros (folha de contato a 1 fps) para achar o momento exato de gestos (ex.: joinha) e do sorriso final.
5. **Montar** com o script (SEGS, FIX, overlays, sfx), renderizar, **conferir quadros e volume antes de mandar**.

## O que ela APROVOU

- **Nome do quadro:** "Arrume-sisi comigo" (é assim, com "sisi" — o Whisper escreve "arrumo-se se comigo"/"arrume-se comigo"; sempre corrigir na legenda e nos títulos).

- **Gancho:** título pequeno, 2 linhas no topo (y≈330), Montserrat Black Itálico 68 —
  linha 1 branca, linha 2 com palavras-chave em **rosa** (`&HB45CFF&`) e **amarelo** (`&H3DD9FF&`) + ✦.
  Entra **digitado letra por letra** (~45 ms/letra), letras não digitadas invisíveis (texto não pula).
  **Com som de teclado BAIXINHO** (sons/keyboard_typing.wav, vol ~0.10, só durante a digitação) — ela sempre usa; a voz tem que ser ouvida.
- **Legenda da fala (ela ama):** Poppins SemiBold 68, branca com contorno, 2–3 palavras por vez, centro-baixo (MarginV 620).
  **Dinâmica:** cada bloco entra com pulinho (85%→100%) e a **palavra falada fica amarela e 8% maior**.
  Termina dentro da própria cena.
- **Rótulos soltos no meio (ela gosta):** Caveat 104 creme, levemente inclinados, curtos e com personalidade:
  "com IA?!", "tem na vitrine!", "joinha!", "ué?", "ligando", "montando... (4x)".
  Informação técnica em Poppins com colchetes rosa: "[ sensor de rastreamento ]".
- **Cortes secos + zoom alternado** (1.0 ↔ 1.10–1.20 a cada corte). Tela renova a cada 1–2 s.
- **Partes longas de ação (montar algo):** acelerar 4x.
- **Cor:** levemente mais quente e saturada (`eq=contrast=1.06:saturation=1.14`, colorbalance quente).
- **Quando algo dá errado** ("por que ele não tá me seguindo?"): cena em **preto e branco** + rótulo "ué?".
- **Fechamento:** congelar no sorriso dela (no meio do quadro!), frase de fechamento no topo com
  **palavras chegando uma a uma com pulinho** (desfoque→nítido, estica e assenta), 2ª linha maior em rosa,
  "plim" quando a palavra-chave chega, escurecer até o preto (~3 s no total).
  Ex. aprovado: "Isso daqui vale / **CADA CENTAVO** ✦". Se ela não falou nada de fechamento, propor uma frase curta.
- **Volume:** normalizar para -14 LUFS.

## Feedback dela (21/11, vídeo "Arrume-sisi comigo" beach tennis) — PRIORIDADE

- **Cortes em cima da última palavra = confuso.** Deixar a palavra terminar (~0,15–0,25 s de folga depois do fim
  da última palavra, mais se a frase cai no tom) e começar o corte seguinte um respiro antes da 1ª palavra.
  Dinâmico SIM, mas a história tem que ser fácil de seguir: não picotar frases que dependem uma da outra.
- **Tirar sempre:** pausas, respirações, repetições (a mesma frase dita 2x → fica a melhor), "é…", tentativas.
  Tirar o que é desnecessário, NÃO o que conta a história.
- **Emoji:** ela detesta o visual de emoji Android (Noto) e qualquer símbolo que pareça isso (o ✦ incluso).
  A fonte de emoji da Apple não pode ser usada aqui (licença). Usar só emoji que ela mandar do iPhone
  (print/PNG) como figurinha, ou não usar emoji.
- **Texto na tela NÃO pode repetir o que ela fala** (legenda já mostra): sem título "conjunto HIPY" / "colar do TikTok Shop".
  Cupom = só a etiqueta rosa "MARCA · cupom GABISILVA". "tem na minha vitrine" só quando ela FALA isso.
- **Marca falada → cupom na tela.** Cupom de desconto é SEMPRE **GABISILVA** (ela fala "Gabi Silva").
  Marcas com cupom: **Spin Grip** e **HIPY** (ela fala "HIP"; escreve-se HIPY).
  Quando ela citar a marca, mostrar marca + "cupom GABISILVA" na tela.
- **Não quer rótulo explicando a piada** ("mudou de ideia", "bailarina?"): nesses momentos, só um som engraçado SUTIL
  (record_scratch / boing MUITO baixos: vol ~0.06–0.07, uns 12–15 dB abaixo da voz — 0.30 ela achou altíssimo) e deixar a cena falar.
- **Final: NÃO congelar.** Terminar logo depois da última fala dela (fade 0,35 s), com o último som (plim) na última palavra;
  título de fechamento entra durante a fala final. (Isso substitui o "congelar no sorriso" antigo.)
- **Palavra espalhada saltando ("atrasada!") → um pop baixinho por palavra** (vol 0.16→0.26).
- **sad_trombone ela achou HORRÍVEL** — para "deu errado" usar algo bem sutil (sons/peido_baixo.wav, vol ~0.08).
- Rótulos que só repetem a fala ("fica 10!", "mudou de ideia", "bailarina?") ela não quer.
- **Checklist com ✓ + click a cada item: ela AMOU** (vol 0.35). Repetir sempre que houver lista/agenda.
- **NÃO usar desfoque de fundo (bokeh com recorte da pessoa)** — ela odiou ("tira esse desfoque"). O "Bokeh" do CapCut
  que ela mostrou provavelmente é outro tipo de filtro; perguntar/ver exemplo antes de tentar imitar.
- **Fala lenta → acelerar só um pouco (1,12x, atempo mantém o tom)** em trechos explicativos/lentos (agenda, maquiagem).
  NÃO acelerar gancho, piadas e falas com marca/cupom.
- **Click no fim do título do gancho** (depois da última palavra da frase do gancho, ex. "...de beach tennis?").
- **Produto do TikTok Shop → rótulo "tem na minha vitrine"** (não escrever "TikTok Shop" no rótulo).
- **Fontes:** a serifada itálica (Instrument Serif) ela achou BREGA → títulos/rótulos em **Outfit SemiBold** (fonts/OutfitSemiBold.ttf);
  as "falinhas do meio" (Patrick Hand) ela aprovou; para destaque engraçado
  (palavra espalhada tipo "atrasada!") usar fonte moderna Bricolage Grotesque bold. Variar a fonte às vezes.
- **Título do gancho mais baixo (y≈520)** — no topo o TikTok põe "Seguindo | Para você". Fechamento em y≈345/440.
- **Emoji do iPhone LIBERADO por ela, mas SUTIL: no máximo 2–3 no vídeo todo** (ex. 🎾 no gancho, ⏰ no "atrasada!"); NÃO em todo corte. Imagens Apple 160 px:
  `curl https://cdn.jsdelivr.net/gh/iamcal/emoji-data@master/img-apple-160/<codigo>.png` (ex. 1f3be = 🎾).
  NÃO versionar as imagens no git (são da Apple); baixar na pasta de trabalho. No script: emoji_after(...) + overlay.
- **Silêncios longos: pode cortar** (min_sil 0,25 s), mas segurar a cena quando há uma piada visual (ex. "atrasada!" + café).
- **Títulos:** seguir a referência que ela mandar (criadoras que ela gosta); estudar o vídeo de referência
  antes de editar (ritmo de corte, tamanho/posição/animação dos títulos, uso de emoji, sons).

## Som: SEMPRE segue a imagem (regra mais importante)

Cada som precisa de um motivo na tela, no quadro exato. Um som por vez.
- Gesto (joinha) → **plim** no quadro em que o gesto aparece.
- Rótulo que merece destaque → plim/bling curto e baixo (não em todos os textos).
- Parte acelerada → **o próprio áudio acelerado** (asetrate 2x + atempo 2 = 4x, uma oitava acima), só durante a aceleração.
- Fechamento → plim na palavra-chave.
- "plim" e "bling" atuais são sintetizados no script (sinos com eco); ela aprovou o plim.

## O que ela NÃO quer (não repetir)

- O primeiro áudio que ela mandou (a gravação de "passando/whoosh" do CapCut) — **nunca usar**.
- "Pop" em todo texto que entra.
- Som de teclado sintetizado (o gravado, baixinho, no título do gancho, ela QUER).
- Som solto sem nada acontecendo na tela; som longo (tipo música inteira) em transição.
- Título grande ocupando a tela.
- Repetir "tem na minha vitrine" no final / cartão "Gostou? / me segue".
- Congelar o final num quadro vazio (sem ela).
- Legenda inventada quando a transcrição não tem certeza.

## Sons dela

Ela grava a tela do CapCut tocando sons. Gravações com voz por cima não dão para recortar limpo —
pedir os sons tocando sozinhos. A 2ª gravação dela (um vídeo de referência tocando no celular, narrado)
serviu para ensinar a regra: "se liga", "check" em cada item de lista, "bling", passando no corte de cena,
barulho de acelerada na parte acelerada.

## Ambiente

- Fontes em `fonts/` (Montserrat, Caveat, Poppins — licença OFL); o script aponta para essa pasta.
- Rede: Dropbox entrega arquivos por servidores com nome aleatório; Whisper baixa modelo de
  `openaipublic.azureedge.net`; instalar `openai-whisper` pelo PyPI (o servidor do PyTorch pode estar bloqueado).
- Renders longos: rodar em segundo plano (o processo pode reiniciar) e mandar o vídeo só depois de conferir quadros.

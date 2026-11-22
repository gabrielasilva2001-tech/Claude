---
name: edicao-tiktok
description: Edita de verdade os vídeos brutos dela para TikTok/Reels (rotina, unboxing, falando pra câmera) no estilo aprovado — decupagem, legenda dinâmica, títulos, rótulos, cor, sons que seguem a imagem e fechamento. Use quando ela mandar vídeo bruto (upload ou pasta do Dropbox) para editar, ou pedir ajuste numa edição.
---

# Edição TikTok/Reels — estilo dela

Estilo construído e aprovado no vídeo "tripé com inteligência artificial" (versão 11, postada).
O script `scripts/editar_exemplo_tripe.py` é a edição aprovada completa: **copie e adapte**, não comece do zero.

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

## Formato 2 (APROVADO): arrume-se comigo falando PERTO DA CÂMERA, dicas numeradas

Quando ela grava se arrumando/maquiando e conversando perto da câmera, com um tema de lista
("coisas que eu faria se…"). Script aprovado: `scripts/editar_arrume_dicas.py` (v2, "como entrar num
banco ou cooperativa") — **copie e adapte** (CUTS/SEGS, FIX, TIPS, rótulos). Inspirado num vídeo de
referência de outra criadora (lista "#1. …" no peito), mas no estilo dela.

- **Só fala, bem dinâmico (ela pediu e aprovou):** tirar TODA pausa de pensamento, silêncio e respiro.
  Não confiar nos tempos do Whisper (ele estica a palavra por cima da pausa). Rodar
  `scripts/fala.py <arquivos>` → `audio/fala.json` (detector de voz Silero + volume: corta trechos
  baixos ≥ 0,16 s, limiar = p90 − 19 dB). O script monta só com esses trechos e remapeia as legendas.
  `pip install silero-vad` (usa o torch do Whisper; carregar o áudio com `wave`, sem torchaudio).
- Cada corte de fala vira corte seco; zoom alterna 1.0 ↔ 1.12–1.18 (não alterna em pedacinho < 1 s).
- **Cabeçalho da dica no topo (y≈300) durante a dica inteira:** Montserrat Black Itálico 60,
  "**#1** siga a cooperativa" (número rosa, texto branco) + 2ª linha maior em amarelo ("no INSTAGRAM").
  Entra com pulinho + som de **"check"** (duas notinhas subindo, sintetizado no script).
- Gancho digitado de sempre ("Como entrar num banco / ou **COOPERATIVA** ✦"), legenda dinâmica,
  rótulos Caveat ("ai, mas...", "sinto muito!", "metade?!"), info em Poppins com colchetes rosa
  ("[ CPA-10 · CPA-20 · CEA ]" + plim), P&B quando algo deu errado ("nunca me chamaram" + "5x não...").
- Fechamento igual ao aprovado: congela no rosto dela centralizado, "Corre atrás e / **NÃO DESISTE** ✦".
- Aprovado com ~1:45. Tirar trechos que o Whisper não entendeu (nomes, siglas) e listar pra ela no final.
  Termos que ele erra aqui: Sicoob ("Ciccobi"), Sicredi ("Ciccred"), CEA ("CEPIA").
- **Render em etapas** (cada corte vira um arquivo, depois concat, depois legendas/sons): com 40+ cortes
  num filtro só o processo morre por falta de memória. Duração de cada corte arredondada em quadros
  (1/30 s) para a legenda não escorregar.
- **Estrela = emoji ✨** (ela pediu; nada de ✦). O libass não desenha emoji colorido: no texto fica um "O"
  invisível guardando o lugar, o script acha a posição renderizando esse "O" em verde e sobrepõe a imagem
  do ✨ (Noto Color Emoji via Pillow), 1,7× a altura do marcador, alinhado pelo começo do espaço.
- **Qualidade para baixar:** cortes renderizados direto do ORIGINAL 4K (zoom recortado em 4K, depois
  reduz com lanczos), intermediários crf 12, final x264 `-preset slow -crf 17 -maxrate 6800k` → ~92 MB
  em 1:46, abaixo de 100 MB. Entregar no chat **e** commitar em `videos/` (`git add -f`) para ela ter o
  link de download do GitHub (pelo chat o download de ~120 MB falhou).

## O que ela APROVOU

- **Gancho:** título pequeno, 2 linhas no topo (y≈330), Montserrat Black Itálico 68 —
  linha 1 branca, linha 2 com palavras-chave em **rosa** (`&HB45CFF&`) e **amarelo** (`&H3DD9FF&`) + ✨ (emoji; ver Formato 2).
  Entra **digitado letra por letra** (~45 ms/letra), **sem som de teclado**, letras não digitadas invisíveis (texto não pula).
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
- Som de teclado sintetizado.
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

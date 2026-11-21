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

## O que ela APROVOU

- **Gancho:** título pequeno, 2 linhas no topo (y≈330), Montserrat Black Itálico 68 —
  linha 1 branca, linha 2 com palavras-chave em **rosa** (`&HB45CFF&`) e **amarelo** (`&H3DD9FF&`).
  **Texto autêntico:** usar as palavras que ELA falou no vídeo (ex.: "não faço ideia do cheiro" → "SEM SABER O CHEIRO"),
  não frase de efeito inventada. Ela achou "NO ESCURO ✦" sem autenticidade.
  Entra **digitado letra por letra** (~45 ms/letra), **sem som de teclado**, letras não digitadas invisíveis (texto não pula).
- **Legenda da fala (ela ama):** Poppins SemiBold 68, branca com contorno, 2–3 palavras por vez, **bem embaixo, longe do rosto (MarginV 400)**.
  Ela achou MarginV 620 perto demais do rosto.
  **Dinâmica:** cada bloco entra com pulinho (85%→100%) e a **palavra falada fica amarela e 8% maior**.
  Termina dentro da própria cena.
- **Rótulos soltos no meio (ela gosta):** Caveat 104 creme, levemente inclinados, curtos e com personalidade:
  "com IA?!", "tem na vitrine!", "joinha!", "ué?", "ligando", "montando... (4x)".
  Informação técnica em Poppins com colchetes rosa: "[ sensor de rastreamento ]".
- **Cortes secos + zoom alternado** (1.0 ↔ 1.10–1.20 a cada corte). Tela renova a cada 1–2 s.
- **Partes longas de ação (montar algo):** acelerar 4x.
- **Cor:** levemente mais quente e saturada (`eq=contrast=1.06:saturation=1.14`, colorbalance quente).
- **Quando algo dá errado** ("por que ele não tá me seguindo?"): cena em **preto e branco** + rótulo "ué?".
- **Fechamento: FINAL NORMAL.** O vídeo termina na última fala dela, com corte seco e o vídeo rodando.
  **Sem** congelar a imagem, **sem** frase de fechamento na tela e **sem** escurecer até o preto.
  Ela odiou o final congelado com "Comprei no escuro e ARRASEI ✦" (vídeo da We Pink, nov/2026), mesmo
  com o tripé tendo usado esse final antes. O fechamento do tripé no script de exemplo **não vale mais**.
- **Imagem flutuante do produto (ela pediu):** quando ela fala de um produto, um cartão com a foto dele
  (recortada do próprio vídeo, no quadro em que o nome aparece nítido), borda branca arredondada, sombra,
  inclinado ±4°, entra deslizando da direita e fica boiando ~2 s no lado direito (x≈690, y≈430). Ver `cartoes.py`
  do vídeo da We Pink: recorte → cartão PNG → overlay no ffmpeg.
- **Do vídeo de referência dela (talking head, perto da câmera):** palavra/número gigante no peito por 1–2 s
  ("4 PERFUMES", "TEM PRESENÇA") e **tópico numerado** quando muda de assunto ("1 · FATAL BLACK").
- **Enquadramento:** aproximar (zoom 1.4–1.55) e tirar o que sobra (teto do carro); renderizar do original 4K.
  Câmera frontal grava espelhada → desespelhar (hflip) pra ler o nome das caixas.
- **Volume:** normalizar para -14 LUFS.

## Som: SEMPRE segue a imagem (regra mais importante)

Cada som precisa de um motivo na tela, no quadro exato. Um som por vez.
- Gesto (joinha) → **plim** no quadro em que o gesto aparece.
- Rótulo que merece destaque → plim/bling curto e baixo (não em todos os textos).
- Parte acelerada → **o próprio áudio acelerado** (asetrate 2x + atempo 2 = 4x, uma oitava acima), só durante a aceleração.
- "plim" e "bling" atuais são sintetizados no script (sinos com eco); ela aprovou o plim.

## O que ela NÃO quer (não repetir)

- O primeiro áudio que ela mandou (a gravação de "passando/whoosh" do CapCut) — **nunca usar**.
- "Pop" em todo texto que entra.
- Som de teclado sintetizado.
- Som solto sem nada acontecendo na tela; som longo (tipo música inteira) em transição.
- Título grande ocupando a tela.
- Repetir "tem na minha vitrine" no final / cartão "Gostou? / me segue".
- **Final congelado com frase de fechamento na tela e escurecendo** (ela odeia). Final é normal, corte seco na última fala.
- Legenda inventada quando a transcrição não tem certeza.
- **Emoji/símbolo "feio" (✦, emoji do Android/Google).** Ela só gosta de emoji do iPhone, e a fonte da Apple não existe
  aqui (é da Apple, não dá pra instalar). Então: **não colocar emoji nenhum**; se ela quiser emoji, ela põe no celular
  (CapCut/Edits), e eu deixo espaço/indico onde.

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

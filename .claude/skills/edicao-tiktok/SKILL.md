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
  linha 1 branca, linha 2 com palavras-chave em **rosa** (`&HB45CFF&`) e **amarelo** (`&H3DD9FF&`) + ✨.
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
  Ex. aprovado: "Isso daqui vale / **CADA CENTAVO** ✨". Se ela não falou nada de fechamento, propor uma frase curta.
- **Volume:** normalizar para -14 LUFS.

## Som: SEMPRE segue a imagem (regra mais importante)

Cada som precisa de um motivo na tela, no quadro exato. Um som por vez.
- Gesto (joinha) → **plim** no quadro em que o gesto aparece.
- Rótulo que merece destaque → plim/bling curto e baixo (não em todos os textos).
- Parte acelerada → **o próprio áudio acelerado** (asetrate 2x + atempo 2 = 4x, uma oitava acima), só durante a aceleração.
- Fechamento → plim na palavra-chave.
- "plim" e "bling" atuais são sintetizados no script (sinos com eco); ela aprovou o plim.

## O que ela NÃO quer (não repetir)

- **Pausas e repetições sobrando** (ela odiou a v2 do ep. 1 de calças). Os tempos do Whisper esticam palavras por cima
  das pausas e ele NÃO escreve repetição/tropeço. Cortar pelo ÁUDIO com `scripts/fala.py` (fala = trechos acima de
  p95−19 dB; só fica trecho que tem palavra reconhecida começando nele) e, no fim, **transcrever o vídeo pronto de novo**
  e conferir que não sobrou frase repetida nem palavra cortada no meio.
- Vídeo longo: ela prefere **fala acelerada 1,2x** (atempo, sem afinar a voz) e só o essencial de cada item.
- **Repetição tipo "essa daqui, essa daqui"**: o Whisper normal NÃO escreve. Usar `scripts/transcricao_literal.py`
  (Whisper com prompt cheio de repetições → transcreve literal) em cada trecho, tirar a 1ª ocorrência de toda
  sequência repetida, e conferir o vídeo final com a mesma transcrição literal.
- **Filtro de cor e zoom alternando** — no quadro da limpa ela achou péssimo: imagem natural, sem zoom.
- **Cortar demais** o que dá sentido (o porquê de cada peça). Tirar só pausa/repetição/tropeço e detalhe lateral.
- **Respiro no fim da fala** e "rabinho" depois do veredito: aparar começo/fim de cada corte pelo volume
  (respiração < p95−19 dB), sem nunca cortar dentro da primeira/última palavra; conferir com transcrição literal.
- **Aparecer tirando a calça / se trocando**: olhar o último quadro de cada corte e cortar antes.
- **Clipes azulados**: corrigir balanço de branco por clipe pelo piso branco (colorchannelmixer), sem filtro.
- **Texto passando atrás da cabeça dela** (recorte da pessoa) — achou horroroso. Título fica no alto, livre.

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

## Quadros / séries

- **"Uma limpa no guarda-roupa"** (ep. 1 = Calças): formato do título e rótulos em `quadro-limpa-guarda-roupa.md`.
  Esse quadro usa o estilo da referência dela (amarelo-creme, minúsculas, texto atrás dela, "fica"/"vai embora"),
  não o gancho rosa/amarelo do vídeo do tripé.
- **Estrela: sempre o emoji ✨** (colorido, fonte Noto Color Emoji), nunca ✦ — pedido dela, vale para todos os vídeos.

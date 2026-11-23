---
name: edicao-tiktok
description: Edita de verdade os vídeos brutos dela para TikTok/Reels (rotina, unboxing, falando pra câmera) no estilo aprovado — decupagem, legenda dinâmica, títulos, rótulos, cor, sons que seguem a imagem e fechamento. Use quando ela mandar vídeo bruto (upload ou pasta do Dropbox) para editar, ou pedir ajuste numa edição.
---

# Edição TikTok/Reels — estilo dela

Estilo construído e aprovado no vídeo "tripé com inteligência artificial" (versão 11, postada).
O script `scripts/editar_exemplo_tripe.py` é a edição aprovada completa: **copie e adapte**, não comece do zero.
Para vídeos "falando + fotos de exemplo" (crítica irônica), use o **Formato 2** abaixo e `scripts/editar_exemplo_arena.py`.

## Fluxo

1. **Receber os brutos.** Upload no chat aceita só ~30 s; vídeos maiores vêm por pasta do Dropbox
   (baixar o link da pasta com `dl=1`, que vem como .zip). Conferir se algum arquivo é cópia/trecho de outro
   (comparar a transcrição) e usar cada trecho uma vez só.
2. **Cópias de trabalho** 1080x1920 (`proxy/`), áudio 16 kHz mono (`audio/`).
3. **Transcrever** com `scripts/transcrever.py` (Whisper `medium`, palavra a palavra; o `small` erra muito).
   Trechos duvidosos: recortar 2–3 s e transcrever de novo isolado (ex.: "não vai seguir" era "não vai esquecer").
   Retomadas no meio da frase às vezes viram uma palavra só esticada no Whisper — conferir com `silencedetect`.
   O Whisper erra gírias/termos: ex. ela disse "carrinho laranja" e ele ouviu "carro em laranja".
   **Nunca inventar fala**: trecho duvidoso fica sem legenda e eu pergunto pra ela.
4. **Decupar**: tirar pausas, falas repetidas (mesma frase dita duas vezes → fica uma) e tentativas.
   Ver quadros (folha de contato a 1 fps) para achar o momento exato de gestos (ex.: joinha) e do sorriso final.
5. **Montar** com o script (SEGS, FIX, overlays, sfx), renderizar, **conferir quadros e volume antes de mandar**.

## O que ela APROVOU

- **Gancho:** título pequeno, 2 linhas no topo (y≈330), Montserrat Black Itálico 68 —
  linha 1 branca, linha 2 com palavras-chave em **rosa** (`&HB45CFF&`) e **amarelo** (`&H3DD9FF&`) + ✦.
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

## Formato 2: "fala + fotos de exemplo" (crítica irônica) — APROVADO e postado

Modelo: vídeo "Construindo uma Arena" (crítica irônica a arena de beach tennis, ela sentada "projetando" no tablet).
Script: `scripts/editar_exemplo_arena.py` (+ `scripts/exemplo_arena/escolhidas.json` e `rotulos.json`). Copie e adapte.
Ela copia o formato de outra criadora: enquanto fala, **fotos de exemplo** do que ela está dizendo aparecem na tela.

- **Título** no começo, digitado letra por letra, 2 linhas (ex.: "Construindo / uma **ARENA**" com ARENA em rosa).
  **Sem estrela ✦** nesse formato.
- **Legenda bem simples:** Poppins SemiBold 66, branca com contorno, 2–4 palavras, **sem** destaque amarelo nem pulinho.
- **Fotos:** cartão com borda branca, cantos arredondados, sombra, leve inclinação (±2°), entram com pulinho e somem rápido.
  **Pequenas** (máx. ~1080x820 px no 4K, ≈ metade da largura) e na parede acima da cabeça dela.
  Cada foto entra **na palavra** que ela ilustra e fica até o fim da frase.
- **Área segura do Instagram:** fotos, título e rótulos **mais para baixo** (centro das fotos em ~27,5% da altura; título em y≈470 de 1920),
  senão o Instagram corta.
- **Rótulos** só quando não há foto boa ("[ término: ??? ]", "esperando desde as 7h...", "[ arquibancada: 5 lugares ]" abaixo da foto).
  Quando existe uma foto que mostra, ela prefere **foto** a texto (ex.: "usar o óculos" → foto de óculos de beach tennis, não "óculos obrigatório").
- **Cortes:** tirar todas as repetições/retomadas (fica a última tomada boa). **Deixar folga de ~0,25 s no fim de cada trecho**:
  ela reclamou quando a última palavra antes do corte foi comida. Zoom alternado 1.0 ↔ 1.12 a cada corte.
- **Final:** ela olhando para a câmera depois da última frase; sem cartão extra.
- **Sem efeitos sonoros** nesse formato (ela pediu simples).

### Fotos: o que ela quer em cada tipo de fala
- Seja **literal e específica**: "chuveiro sem porta" = banheiro com paredes, **vaso e chuveiro no mesmo cômodo, sem box**
  (não chuveiro de praia). "Areia bem grossa" = areia grossa de verdade (ela mandou foto de mão com areia de construção),
  **antes** da foto de pedrinhas. "Arquibancada pequena" = estrutura de arena (ela usou foto de uma mesa com bancos dentro da arena),
  nada de banquinho/portátil. "Posição das quadras pro sol" = foto de **sol bem forte**.
  "150 de inscrição / 80 de premiação" = foto de **muito dinheiro** (notas de 50/100) e depois de **pouco** (moedas e notas de 2).
- Nada de foto de machucado (ela vetou o "joelho esfolado").
- **Pedir as fotos a ela cedo**: ela manda prontas em minutos ("qualquer coisa já te mando pronto"). Mais rápido que buscar.
- Busca em licença livre: Wikimedia Commons (`scripts/busca.py`, `scripts/baixa_escolhidas.py`). Limita muito (erro 429):
  buscas espaçadas (~25 s), termos simples em inglês, baixar só as escolhidas. Unsplash/Pexels/Pixabay não estão acessíveis.
  Guardar os créditos (`fotos/creditos.txt`).

### Qualidade e entrega
- Ela edita no CapCut se perder qualidade: **render final direto do .mov original em 4K (2160x3840)**.
- Duas etapas (senão estoura a memória): cada trecho vira intermediário CRF 10; depois junta + fotos + legendas (CRF 16, preset fast).
  Trechos já prontos ficam em cache: refazer só a etapa final leva ~4 min.
- Prévias em 1080 (`--preview`) para ela aprovar antes do 4K.
- O 4K (~180 MB) **não baixa no app**: mandar também uma versão 1080x1920 (~50 MB, CRF 17) — é a que ela posta.
- Ela costuma ter **horário para postar**: perguntar o prazo e entregar o essencial a tempo.

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

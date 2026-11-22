# Quadro "Uma limpa no guarda-roupa"

Série dela. Ep. 1 = **Calças** (vídeo bruto ainda não recebido em 21/11/2026).
Formato tirado de um vídeo de referência (provador de jaquetas, 90 s, 576x1024) que ela mandou para imitar.

## Como o texto funciona na referência

- **Cor única:** amarelo-creme claro (~`#FFF3A6`, em ASS `&HA6F3FF&`), sem contorno, só uma sombra/brilho
  bem suave. Fonte sans **pesada e arredondada, toda minúscula, letras bem juntas** (tipo Arial Rounded Bold;
  aqui usar Poppins ExtraBold/Black ou Montserrat Black com espaçamento -2, minúsculas).
- **Abertura em 3 tempos (≈5 s), acompanhando a fala:**
  1. Palavras **grandes, uma de cada vez**, no centro-baixo (y≈1080 em 1920): "provando" → "todas" → "as" → "roupas".
     Troca seca no ritmo da fala, sem animação de entrada.
  2. Frase **no topo digitada letra por letra com cursor "|" piscando**: "até ficar só".
     Na referência o texto fica atrás dela, MAS ELA NÃO GOSTOU disso no vídeo dela: título sempre no alto (y≈330), sem recorte.
  3. Complemento pequeno abaixo à direita "com o que" + palavras grandes embaixo "realmente" / "uso" empilhando.
- **Cartão de categoria:** quando ela mostra o monte de peças, o nome da categoria grande no meio
  ("jaquetas") rodeado de **estrelinhas ✨ (emoji, colorido)** espalhadas (4–6, tamanhos variados). Ela pediu: estrela = sempre ✨, nunca ✦.
- **Veredito por peça:** rótulo pequeno no canto superior (mesma fonte/cor, ~40 px):
  **"fica"** ou **"vai embora"**, aparece quando ela decide.
- Cada peça = um provador rápido (cortes secos, 3–6 s por peça).

## Título proposto para o Ep. 1 — Calças

Mesmo esquema, ajustando para a série (validar com a fala dela quando o bruto chegar; não inventar fala):
1. Topo, digitado com cursor, atrás dela: **"uma limpa no"** / **"guarda-roupa"**
2. Pequeno abaixo à direita: **"ep. 1"**
3. Cartão de categoria com estrelinhas: **"calças"** ✨
4. Durante as provas: "fica" / "vai embora" em cada calça.
Se ela falar a introdução tipo a referência ("provando todas as calças até ficar só com as que eu realmente uso"),
usar as palavras grandes uma a uma acompanhando a fala.

## Ep. 1 feito (v2, 21/11/2026) — `scripts/editar_limpa_calcas.py`

- Fonte do quadro: **Nunito Black** (`fonts/Nunito-Black.ttf`), cor `&HA6F3FF&`, espaçamento -3.
- Título "uma limpa no / guarda-roupa" digitado com cursor, na altura da cabeça dela (y≈690) para a cabeça
  passar na frente: máscara da pessoa com `scripts/mascara_pessoa.py` (mediapipe selfie_multiclass; precisa de
  `apt-get install libegl1 libgles2`), camada do título renderizada à parte e a pessoa recortada por cima.
- Palavras grandes na intro acompanhando a fala; legendas da fala no ALTO (acima da cabeça), pra não cobrir a calça.
- Veredito no topo (y=330) com plim no "fica" e duas notas descendo ("tchau") no "vai embora".
- ✨ é PNG (Noto Color Emoji) sobreposto — o libass não desenha emoji colorido.
- Pausas dentro das falas são cortadas automaticamente (corte seco, zoom alterna 1.0/1.08).
- Render: cada corte vira um arquivo e depois concatena (dezenas de trims do mesmo arquivo estouram a memória).
- Trechos com fala incerta ficaram de fora: IMG_6392 ("esse sabor"?), início do 6394 ("calça de cor/couro"?),
  nome da loja em 6404, final de 6405, Shopee em 6403. 6410 e 6411 cortados por tempo.

## v4 (aprovação pendente) — o que mudou depois da reclamação
- Título no alto, sem efeito atrás da cabeça. Cortes pelo áudio (`scripts/fala.py`), fala 1,2x, falas enxugadas: 2:04.
- Conferência final: Whisper no `base.mkv` — sem repetições.

## v5 — pedidos dela
- **Placar fixo o vídeo todo** no topo: "ficou N · saiu N" (+ "? N" quando houver talvez), sobe com pulinho
  no momento em que ela diz fica/sai.
- Sem filtro de cor, sem zoom. Fala 1,25x. Explicações de cada calça de volta (3:07).

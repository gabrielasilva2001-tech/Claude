# Diretrizes de edição — escritas por ela (20/11/2026)

**Estas diretrizes valem acima de tudo o que está no SKILL.md.** Onde houver conflito, vale isto aqui.

Quero uma edição jovem, moderna, dinâmica e natural. Não quero que meus vídeos tenham aparência de edição
automática de inteligência artificial ou excesso de efeitos.
O objetivo é prender a atenção nos primeiros segundos, valorizar minha personalidade e deixar o conteúdo gostoso de assistir.

## 1. Efeitos sonoros

Populares de TikTok/Reels, com moderação e contexto.

- **Humor e reações:** Record Scratch (interrupção inesperada / situação absurda), Vine Boom (expressão ou
  informação impactante), Bruh (decepção, ironia, frustração), Boing (movimentos engraçados),
  Crowd Laugh (momentos de humor), Cartoon Pop (pequenas situações cômicas).
- **Transições e movimentos:** Whoosh (movimentos rápidos e mudança de cena), Swipe (transição entre cenas),
  Camera Shutter (fotos, poses, mudança de look), Pop (textos/elementos aparecendo).
- **Ênfase e suspense:** Ding (informação importante), Cinematic Hit (revelação/impacto), Riser (expectativa
  antes de uma cena), Drum Roll (preparar revelação), Notification (celular, mensagens).

Regras:
- Não usar som em todos os cortes; não repetir sempre os mesmos.
- Nada de som aleatório para preencher espaço.
- Efeito **nunca mais alto que a voz**; em fala importante, a voz em destaque.
- Evitar efeitos infantis, exagerados ou artificiais. Preferir curtos, sutis e sincronizados com a imagem.

## 2. Começo

Os primeiros 2 segundos são fundamentais.
- Começar direto com a melhor cena ou fala. Sem introdução demorada, vinheta, tela preta ou animação genérica.
- Frases curtas e interessantes na tela quando fizer sentido.
- Alternar: começar com fala, com cena curiosa ou com momento engraçado.
- **Não inventar frases** que não correspondam ao conteúdo.

## 3. Fontes e identidade visual

- Sem serifa, modernas, encorpadas mas não infantis. Hierarquia visual; palavras importantes destacadas.
- Legendas dinâmicas, sem precisar transcrever tudo. Animações rápidas e naturais.
- Texto **nunca esconde o rosto** dela.
- **Evitar fontes cursivas** (ex.: Caveat), delicadas demais ou corporativas.
- Consistência visual, mas **não a mesma animação em todos os vídeos**.
- **Fontes, cores, tamanhos e estilo definitivo: aguardar as referências visuais dela.**

## 4. Ritmo e dinâmica

- Cortes acompanham a fala e a cena. Tirar pausas, mas preservar a naturalidade.
- Zooms discretos em momentos estratégicos (não em todo corte).
- Alternar enquadramentos quando houver material.
- Aproveitar expressões, gestos e reações.
- Textos/grafismos só quando acrescentam. Não transformar cada segundo em transição.

## 5. O que ela NÃO quer

Edição genérica de IA · efeitos sonoros exagerados · transições chamativas sem necessidade ·
texto o tempo inteiro · legendas enormes · zooms repetitivos · fontes ultrapassadas · animações infantis ·
cara de apresentação corporativa · edição artificial que tire a espontaneidade.

## 6. Resultado esperado

Parecer editado por um editor profissional de TikTok: criativo, jovem, espontâneo, engraçado quando o
conteúdo permitir, visualmente interessante. **A personalidade dela é o destaque.**

**IMPORTANTE:** não aplicar todas as técnicas automaticamente. Analisar o conteúdo, achar os melhores
momentos e escolher só os recursos que fazem sentido para cada vídeo.

## Aprovado no "banho da Lúcia" (v1 aprovada: "amei, ficou ótimo")

- **Título inicial = etiquetas coladas** (referência dela: templates "a day in my life" do CapCut):
  texto em minúsculas, fonte arredondada encorpada (Fredoka Bold, `fonts/Fredoka-Bold.ttf`), preto sobre
  caixinhas coloridas (lilás `&H00FFB8C9` e amarelo-claro `&H008AF0F6`), levemente tortas (~4°), uma abaixo da
  outra e deslocadas, entrando com "tapinha" (0→116%→100%), + brilhinhos de 4 pontas (amarelo, rosa, branco)
  girando devagar. Script mais recente: `scripts/editar_banho_lucia_v4.py` (zoom de ênfase andando, padrão de sons, adesivos no título).
- **Legenda/título NUNCA no rosto dela** (ela reclamou duas vezes). Neste vídeo: rosto no alto → legenda e
  título embaixo; ela embaixo no quadro → legenda em cima. Conferir **cada legenda** num quadro antes de mandar
  (inclusive o título do começo). Nos próximos vídeos ela quer tentar manter um padrão fixo.
- **Vídeo reto:** se a gravação ficou torta (paredes/azulejos inclinados), endireitar. Medir com linhas verticais
  (OpenCV Hough) e gerar cópias de trabalho já endireitadas a partir do bruto 4K (rotate + zoom de compensação).
  Aqui foi V1 6,5°, V2 5,5°, V3 6°.
- **Efeitinhos:** ela liberou colocar quando eu achar que cabe (ex.: flash de câmera na pose, zoom de susto
  num "quer dizer..."), com a mesma moderação das diretrizes.
- **Final:** a última cena engraçadinha congela e leva um **zoom rápido** (punch-in) no rosto dela + o que
  estiver junto, com um **som zoado** de zoom (apito subindo). Neste vídeo o zoom foi **na carinha da cachorra**, não nela. **NUNCA risada** ("pelo amor de Deus").

## Nível de acabamento por tipo de vídeo (fala dela, 20/11/2026)

- Banho da Lúcia (v3) **aprovado**: "bem fluida", bom para um vídeo **não profissional** (rotina/vlog casual).
- Vídeos em que ela está **falando para a câmera** (conteúdo de fala) pedem acabamento **bem mais profissional**
  que esse. Antes de editar um desses, combinar com ela o que significa "profissional" (referências) e
  caprichar em: decupagem fina das falas, legenda mais elaborada, áudio tratado, cor e enquadramento.
- Depois ela completou: a edição do banho ficou **"bem simples"** (não precisou refazer). Nos próximos,
  ousar mais dentro das diretrizes: mais variedade de enquadramento/ritmo, grafismos e transições com
  propósito, títulos e legendas com mais personalidade — sem virar "edição de IA".

## Feedback detalhado do banho da Lúcia (o que faltou — aplicar nos próximos)

- **Dar ênfase onde a fala pede.** Quando ela comenta algo do pet/objeto/pessoa (ex.: "a Lúcia é...", "olha
  essa lágrima ácida"), a cena não pode ficar parada: **zoom (ou reenquadramento) no que ela está comentando**,
  no momento da palavra. Mapear na transcrição cada fala sobre algo e decidir a ênfase.
- **Zoom final ANDA até o alvo** (movimento suave/rápido do enquadramento até o rosto da cachorra), começando
  **logo que ela termina de falar** — não um corte seco para um quadro já ampliado no fim.
- **Sons: portfólio maior, mas com padrão fixo por situação.** Ter mais sons disponíveis e variar entre
  vídeos, mas dentro do vídeo manter a regra "situação X → som Y" (ex.: ênfase em fala = sempre o mesmo
  ding; humor/absurdo = sempre o mesmo scratch; revelação/zoom = sempre o mesmo; pose/foto = obturador).
  Montar a tabela situação→som no início de cada edição.
- **Título:** gostou das etiquetas da v2/v3, mas nos próximos puxar **mais forte** para a referência dela
  (templates "a day in my life"/"day in my life" do CapCut: etiquetas coloridas tortas, letras grandes e
  arredondadas, brilhinhos, emojis/adesivos tipo carinha e florzinha).
- **Cortes:** aprovados ("não cortou nada relevante").
- Cortes finos que ela pediu na v4: tirar momentos de **checagem** (olhar o relógio pra ver se a câmera está
  gravando, arrumar a câmera) mesmo no meio de partes aceleradas — manter só a ação e a fala.

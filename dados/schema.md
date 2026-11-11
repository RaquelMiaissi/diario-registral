# Esquema de dados — Diário Registral

Um único arquivo alimenta as duas páginas (a Jurisprudência Registral, no
Claude, e o site Diário Registral): `docs/dados.json`. Reescrito em 26/10/2026,
quando os diários oficiais passaram a ser a única fonte. O modelo anterior,
organizado por edição do serviço pago, está em `dados/arquivo/` (inativo).

## `acordaos[]` — decisões do CSM, do mais recente ao mais antigo

| campo | tipo | o que é |
|---|---|---|
| `ed` | text | data em que o acórdão saiu no DJEN, `dd/mm/aaaa` (é a data mostrada nas páginas) |
| `djen` | text | a mesma data em `AAAA-MM-DD`, para ordenar |
| `djenId` | int | `id` do item no DJEN — chave para não duplicar |
| `num` | text | "Apelação 1234567-89.2026.8.26.0405" ou "Embargos de Declaração …/50000" |
| `com` | text | comarca, em caixa alta |
| `titulo` | text | título curto em caixa alta, para o cartão |
| `resumo.tema` | text | título que entrega a conclusão |
| `resumo.corpo` | text[] | 2 a 4 parágrafos: o que foi decidido e por quê |
| `resumo.orientacao` | text ou text[] | o que o escrevente faz na qualificação; "apenas ciência" se não muda a rotina |
| `resumo.atencao` | text | só quando há exceção, limite ou tensão com lei ou precedente superior |
| `integra` | text | acórdão como publicado no DJEN — partes, relator, resultado e ementa; NÃO é o inteiro teor (relatório e voto não saem no diário). Sem nomes de advogados nem números de OAB. O nome do campo é herdado; nas páginas aparece como "acórdão publicado" |
| `fonte` | text | "DJEN — TJSP, órgão Intimação de Acordãos, dd/mm/aaaa" |
| `fonteUrl` | text | consulta oficial: `https://comunicaapi.pje.jus.br/api/v1/comunicacao?siglaTribunal=TJSP&numeroProcesso=<20 dígitos>` |

## `dias[]` — um por dia útil varrido, do mais recente ao mais antigo

| campo | tipo | o que é |
|---|---|---|
| `d` | text | data, `dd/mm/aaaa` |
| `wd` | text | dia da semana |
| `sem` | text ou null | motivo, quando o dia não foi varrido ou não houve edição |
| `nac` | int | acórdãos do CSM com `ed` igual a `d` |
| `fonte` | text | o que foi lido: "DJEN + DEJESP (edição NNNN)" |

Os dias anteriores a 23/10/2026 foram varridos pelo serviço pago então
assinado; `nac` deles foi recalculado pela data do DJEN em 26/10/2026 e o campo
`fonte` ficou vazio.

## `alertas[]` — alertas de fraude (comunicados CG), do mais recente ao mais antigo

| campo | tipo | o que é |
|---|---|---|
| `d` | text | data do DEJESP, `dd/mm/aaaa` |
| `ed` | int | edição do DEJESP |
| `num` | text | "CG 850/2026" |
| `proc` | text | processo CG |
| `origem` | text | quem comunicou (serventia, Corregedoria Permanente) |
| `serv` | text | serventia envolvida |
| `tipo` | text[] | selo falso, matrícula falsa, certidão falsa, procuração falsa… |
| `ri` | bool | toca Registro de Imóveis |
| `selos`, `matriculas` | text[] | números citados, para busca |
| `resumo` | text | redação própria, 1 a 3 frases |
| `obs` | text ou null | observação interna |
| `texto` | text | comunicado como publicado |
| `fonte` | text | "DEJESP, Caderno 1, edição NNNN, dd/mm/aaaa" |

## `assis[]` — publicações sobre a Comarca de Assis em matéria extrajudicial (desde 10/11/2026)

| campo | tipo | o que é |
|---|---|---|
| `d` | text | data da publicação, `dd/mm/aaaa` |
| `org` | text | órgão que publicou ("Foro de Assis – 1ª Vara Cível (Juízo Corregedor Permanente)", "DEJESP, Dicoge 5.2"…) |
| `num` | text | número do processo ou do ato |
| `cls` | text | classe ("Pedido de Providências — Registro de Imóveis", "Correição"…) |
| `parte` | text | serventia ou parte envolvida |
| `tema` | text | uma frase: o que é e em que ponto está |
| `texto` | text | despacho ou ato como publicado |
| `fonte` | text | "DJEN — TJSP, órgão … (código NNNNN)" ou "DEJESP, Caderno 1, edição NNNN" |
| `fonteUrl` | text | consulta oficial |

## `nacional[]` — normas e precedentes nacionais (desde 10/11/2026)

| campo | tipo | o que é |
|---|---|---|
| `d` | text | data de publicação/edição, `dd/mm/aaaa` |
| `org` | text | "CNJ", "STJ", "STF" ou "Receita Federal" |
| `tipo` | text | "Provimento", "Resolução", "Acórdão em informativo", "Tese repetitiva", "Repercussão geral", "Súmula", "Instrução Normativa" |
| `num` | text | "Provimento CN nº 259/2026", "REsp 2.189.786-TO — Informativo nº 908", "IN RFB nº 2.345/2026", "Tema 1316" |
| `forca` | text | "normativo" (ato que obriga), "vinculante" (precedente obrigatório: repetitivo, repercussão geral, súmula vinculante) ou "persuasivo" (decisão de turma/seção sem força obrigatória) |
| `vinculante` | bool | `true` para normativo e precedente vinculante; `false` para persuasivo |
| `situacao` | text ou ausente | "Vigente", "Alterado", "Revogado" (atos) |
| `ramo` | text ou ausente | ramo do direito indicado pelo tribunal (STJ: "Direito Notarial e Registral; Direito Civil") |
| `afeta` | text[] | "RI", "RTD", "RCPJ" |
| `titulo` | text | título curto em caixa alta, que já entrega a conclusão |
| `ementa` | text | ementa ou destaque como publicado |
| `resumo` | text | redação própria; quando o texto integral não foi lido, dizer isso |
| `orientacao` | text | o que muda na rotina; "apenas ciência" quando não muda |
| `fonte` | text | órgão, publicação e data |
| `fonteUrl` | text | página oficial do ato/informativo |
| `classe` | text ou ausente | `"comunicacao"` quando o ato altera uma norma listada em `comunicacoes[]` (alteração de regra de comunicação, não de qualificação) |
| `comunicacao` | text ou ausente | `id` da comunicação afetada (`doi`, `prefeituras`, `incra`, `estrangeiros`, `coaf`, `pep`, `itn003`, `mapa-estatisticas`, `arisp-estatisticas`, `papel-seguranca`) |

## `comunicacoes[]` — comunicações obrigatórias pós-registro (desde 11/11/2026)

Base fixa, gerada por `src/build/comunicacoes_base.py`; só muda por decisão do
Oficial. Lista vinda dos cabeçalhos da planilha interna "04 - Planilha para
comunicados mensais"; origem normativa conferida nas fontes oficiais.

| campo | tipo | o que é |
|---|---|---|
| `id` | text | chave curta (acima) |
| `planilha` | text | número do bloco na planilha 04 |
| `nome` | text | nome da comunicação |
| `destinatario` | text | quem recebe e por qual sistema |
| `gatilho` | text | ato registral ou situação que dispara a comunicação |
| `periodicidade` | text | "Mensal", "Trimestral", "Por operação"… |
| `prazo` | text | prazo com o dispositivo que o fixa |
| `meio` | text | canal/sistema de envio |
| `base[]` | obj[] | `norma`, `disp` (artigo/item), `o_que` (o que o dispositivo diz), `orgao`, `url` |
| `vigiar[]` | text[] | termos e normas que a varredura procura nos atos novos |
| `pendencias` | text | o que não foi confirmado nas fontes oficiais (vazio quando tudo foi conferido) |

`comunicacoes_fora[]` (`nome`, `prazo`, `base`, `url`): obrigações periódicas
encontradas nas normas que não estão na planilha 04, para o Oficial decidir.
`comunicacoes_conferido`: data da última conferência (`dd/mm/aaaa`).

## Firestore (quando a carga for feita)

- `acordaos/{djenId}` — um documento por acórdão, campos acima. Leitura pública.
- `edicoes/{AAAA-MM-DD}` — um por dia, campos de `dias[]`. Leitura pública.
- `atos/{id}` — atos da Corregedoria, quando passarem a ser guardados:
  `data`, `edicaoDejesp`, `secao` (Dicoge n), `titulo`, `texto`, `fonte`
  ("DEJESP"), `tocaServentia` (bool, interno). Leitura pública só com `fonte`
  em DEJESP/DJEN.
- `interno/**` — verificação de Assis, orientação interna, marcação de
  impacto. Só autenticado.
- `conferencia/{data}` — resultado da validação de set–out/2026. Só autenticado.

Escrita sempre fechada ao cliente (`firestore.rules`); só pelo Admin SDK, com
chave que nunca passa por conversa nem entra no repositório.

## Acesso

Acórdãos e atos de diário oficial aberto podem ser lidos por qualquer um. A
verificação de Assis, a marcação do que toca a rotina da serventia e qualquer
orientação interna são documento interno do cartório e ficam restritos a quem
estiver autenticado.

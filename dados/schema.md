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

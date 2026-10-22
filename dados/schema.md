# Modelo de dados

Vale para Firestore e para Postgres/Supabase. Em Firestore cada item abaixo é
uma coleção; em Postgres, uma tabela.

## `edicoes` — uma por dia útil
| campo | tipo | o que é |
|---|---|---|
| `data` | date | data da edição (chave) |
| `diaSemana` | text | segunda-feira, terça-feira… |
| `idInr` | int | id da edição no INR (nunca é previsível) |
| `idDejesp` | int | id da edição do DEJESP do mesmo dia |
| `totalAtos` | int | atos no índice — vem do índice, nunca da busca no texto |
| `semEdicao` | bool | true quando a edição não subiu |
| `assisVerificacao` | text | o que foi achado no Filtro 1, e o que foi descartado e por quê |
| `correcao` | text | se o dia foi revarrido, por que |

## `atos` — um por ato da edição
| campo | tipo | o que é |
|---|---|---|
| `data` | date | → `edicoes.data` |
| `classificador` | text | I, II, III, III-Especial, IV |
| `orgao` | text | nível 1 do índice |
| `secao` | text | nível 2 — Dicoge 5.1, SEMA 1.1.2, Caderno 3… |
| `titulo` | text | nível 3 — o ato |
| `tocaServentia` | bool | reflete na rotina de RI, RTD ou RCPJ |
| `fonte` | text | DEJESP, DJEN ou INR |
| `link` | text | url da fonte oficial |

## `acordaos` — decisões do CSM (Filtro 2)
| campo | tipo | o que é |
|---|---|---|
| `processo` | text | nº do processo (chave) |
| `data` | date | disponibilização |
| `comarca` | text | comarca de origem |
| `titulo` | text | a tese em poucas palavras |
| `tema` | text | título curto em caixa alta |
| `corpo` | text[] | síntese, 2 a 5 linhas por parágrafo |
| `orientacao` | text[] | o que o escrevente faz na qualificação |
| `atencao` | text | ressalva, quando o precedente é controvertido |
| `integra` | text | ementa estruturada como publicada |
| `fonte` | text | DJEN, órgão "Intimação de Acordãos" (orgaoId 92345) |
| `parcial` | bool | se a íntegra pode estar truncada |

## `conferencia` — resultado da varredura paralela
| campo | tipo | o que é |
|---|---|---|
| `data` | date | → `edicoes.data` |
| `filtro` | text | `acordaos` ou `corregedoria` |
| `totalInr` | int | atos que o INR publicou |
| `recuperados` | int | quantos as fontes abertas acharam |
| `perdidos` | text[] | atos do INR que a varredura aberta NÃO achou |
| `sobra` | int | achados a mais, só em contagem |

## Acesso

`acordaos` e os `atos` cuja `fonte` é DEJESP ou DJEN vêm de diário oficial
aberto — podem ser de leitura pública.

`edicoes.assisVerificacao`, `atos.tocaServentia` e qualquer orientação
interna são **documento interno da serventia**. Os `atos` com `fonte` = INR
reproduzem a compilação de um fornecedor contratado. Esses três ficam
restritos a quem estiver autenticado.

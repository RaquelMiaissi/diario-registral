# Diário Registral

Leitura diária dos diários oficiais em matéria registral, para o Cartório de
Registro de Imóveis, Títulos e Documentos e Civil de Pessoas Jurídicas da
Comarca de Assis/SP. Fontes: só o DJEN e o DEJESP, diários oficiais abertos.
Desde 26/10/2026 nenhuma fonte paga é usada.

Dois filtros, decididos em 15/09/2026 e mantidos desde então:

1. **ASSIS** — qualquer ato que se refira à comarca, em matéria extrajudicial.
2. **Decisões do CSM** — acórdãos do Conselho Superior da Magistratura de São
   Paulo, de qualquer comarca, porque são o precedente que orienta a
   qualificação registral.

## De onde vêm os dados

Duas fontes oficiais abertas, nenhuma delas com senha. Levantado e conferido
processo por processo em 22/10/2026; fonte única desde 26/10/2026.

| Conteúdo | Fonte | Endereço |
|---|---|---|
| Acórdãos do CSM | **DJEN** — Diário de Justiça Eletrônico Nacional, do CNJ, órgão "Intimação de Acordãos" (`orgaoId` 92345) | `comunicaapi.pje.jus.br/api/v1/comunicacao` |
| Atos da Corregedoria Geral | **DEJESP** — Caderno 1 Administrativo, Subseção III, seções Dicoge, bloco EXTRAJUDICIAL | `tjsp.jus.br/dejesp` |
| Atos da Presidência e da SEMA | **DEJESP** — Caderno 1, Seção I, Subseção I | idem |
| Decisões das 1ª e 2ª Varas de Registros Públicos da Capital (fora da triagem) | **DJEN**, `orgaoId` 93296 e 93416 | idem |

As duas fontes **não se sobrepõem**: os atos da Corregedoria não estão no
DJEN, e os acórdãos do CSM não estão no DEJESP. Quem quiser a informação
completa tem de ler as duas.

### O antigo DJe está morto

`dje.tjsp.jus.br/cdje` devolve sempre **22/07/2025**, qualquer que seja a data
pedida. Não é bloqueio nem defeito: é a última edição que existe. No dia
seguinte o Caderno 1 foi extinto e o DEJESP tomou o lugar. O DOE-SP
(`do-api-web-search.doe.sp.gov.br`) responde com o envelope certo e
`totalItems: 0` em toda tentativa — não é fonte utilizável.

## Como a leitura direta foi validada

Antes de virar fonte única, a leitura direta dos dois diários foi conferida
contra 35 edições do serviço de curadoria pago então assinado (INR, assinatura
encerrada em 26/10/2026), de 01/09 a 22/10/2026, processo por processo.

| Filtro | No serviço pago | Recuperados | Perda |
|---|---|---|---|
| Acórdãos do CSM (35 edições) | 30 | **30** | **0** |
| Corregedoria Geral (20, 21 e 22/10) | 32 | **32** | **0** |

O texto do DJEN é igual ou maior que o do serviço, e traz seções que ele cortava
("Legislação citada", "Jurisprudência citada"). E chega antes: o serviço
racionava 5 acórdãos por edição e empurrava o resto para os dias seguintes —
por isso, em 26/10/2026, a data de 10 acórdãos nas páginas passou para a data
real do DJEN. Os dados daquele período ficaram em `dados/arquivo/` (inativos).

**As Varas de Registros Públicos da Capital estão fora da triagem** por decisão de 22/10/2026 — é primeira
instância de outra comarca, não vincula Assis, e o que for relevante sobe por
apelação e aparece no CSM. `src/varredura/iv_regra.py` guarda a regra de
descarte por exclusão, para quando for preciso.

## Arquitetura

- **GitHub** — o código: a varredura, o construtor da página e a documentação.
- **Firebase / Firestore** — os dados: edições, atos, acórdãos e o resultado
  da conferência paralela. Escolhido em 22/10/2026 por não pausar o banco
  por inatividade, ao contrário do Supabase.

O desenho é deliberado. O código pode ser público; os dados, não
necessariamente. `dados/schema.md` marca o que é cada coisa, e `firestore.rules` é o que
implementa a separação:

- **Pode ser leitura pública** — acórdãos e atos cuja fonte é DEJESP ou DJEN.
  São diário oficial aberto.
- **Fica restrito a quem estiver autenticado** — a verificação do Filtro 1, a
  marcação do que toca a rotina da serventia, qualquer orientação interna, e os
  dados herdados do serviço pago (inativos, em `dados/arquivo/`).

```
src/varredura/    consultas às duas APIs (rodam no navegador)
src/build/        montagem da página a partir dos dados
dados/schema.md   modelo de dados, com a classificação de acesso
dados/seed/       os dados atuais, para carga inicial
docs/             o site publicado (GitHub Pages)
documentacao/     CLAUDE.md (a rotina) e o texto da tarefa agendada
```

## Armadilhas já pagas

Cada uma destas custou uma falha real. Não repetir.

- **As duas APIs não respondem do contêiner da sessão** (403 no proxy). Só
  pelo navegador do aplicativo. Nunca tentar por `curl` ou `python`.
- **O `count` do DJEN mente** — devolve o tamanho da página, não o total. Em
  22/10/2026 a 1ª Vara declarou `count: 100` e tinha 233 itens. Paginar sempre
  até vir menos que `itensPorPagina`.
- **O DJEN devolve HTML quando o ritmo aperta.** Conferir o `content-type`
  antes de interpretar, repetir com espera crescente, pausar entre páginas.
- **A busca do DEJESP por frase não existe** — é OU entre as palavras.
  `"Comarca de Assis"` devolveu 4.930 páginas. Buscar a palavra isolada e
  desambiguar depois.
- **`PROCESSO PJECOR Nº`** tem a sigla no meio do padrão. Sem o grupo opcional
  no regex, perdem-se os atos do Dicoge 3.1 — foram 8 em 20/10/2026.
- **Nunca adivinhar a faixa de páginas da Subseção III.** Usar as páginas das
  seções `Dicoge` da lista de seções. A heurística de fim de faixa leu 72
  páginas em vez de 7 em 20/10/2026.
- **Ritmo nas APIs.** O DJEN devolve HTML em vez de JSON quando o ritmo
  aperta: conferir o `content-type`, repetir com espera crescente, pausar
  ~350 ms. Em 22/10/2026 um site foi bloqueado por IP depois de dezenas de
  aberturas em poucos minutos — a lição vale para qualquer fonte.
- **"Não consta nada" significa nada em matéria extrajudicial** — não que o
  termo não apareça no diário. Menções reais a Assis (designação de juiz
  auxiliar, obra no fórum) existem no DEJESP e ficam fora por decisão de
  22/10/2026.

## Segurança

Nunca versionar chave, token, senha ou arquivo de conta de serviço. O
`.gitignore` já barra `.env`, `*-serviceAccount*.json` e `*-adminsdk-*.json`.
A chave de configuração do cliente Firebase pode ir no código — ela não é
segredo; **quem decide o acesso são as regras de segurança do banco**, e é
nelas que mora a separação entre o que é público e o que é interno.

## Como levantar

O passo a passo do Firebase está em
`documentacao/firebase-passo-a-passo.md` — inclusive o que **não** deve ser
colado em conversa nem versionado.

Sem banco configurado o site funciona do mesmo jeito: `docs/fonte.js` começa
no modo `seed`, lendo o `docs/dados.json` do próprio repositório, que contém
apenas material de diário oficial aberto.

# CLAUDE.md — Monitoramento do Diário Oficial (INR Publicações)

> Arquivo de instruções do projeto. Leia este arquivo antes de executar qualquer
> rotina de monitoramento do Diário Oficial.

---

## 1. Objetivo

Verificar **todos os dias** as publicações oficiais divulgadas pelo INR Publicações
e entregar à Raquel um resumo com:

1. **Tudo o que saiu no dia** (visão geral, por categoria).
2. **O recorte do que é relevante** para o Cartório de Registro de Imóveis,
   Títulos e Documentos e Civil de Pessoas Jurídicas da Comarca de Assis/SP.

---

## 2. Fonte

| Item | Valor |
|---|---|
| Fonte primária | INR Publicações — `https://inrpublicacoes.com.br` |
| Acesso | Área do Assinante (login + senha) |
| Credenciais | **Pendente.** Raquel solicitará à Letícia. Não há acesso em 15/09/2026. |
| Navegador | Navegador interno do Claude (painel do app desktop), perfil persistente |
| Permissão do site | Já concedida ao navegador interno (escopo permanente) |

**Regra de segurança:** Claude **nunca** digita a senha. O login é feito pela
Raquel no painel, com a opção "Mantenha-me conectado" marcada (o INR mantém a
sessão por até 15 dias sem acesso; depois exige login manual novamente).

### Fontes públicas de apoio — verificadas em 22/10/2026

O INR é recorte de **duas** fontes abertas, não de uma. Nenhuma pede senha.
Levantamento conferido processo por processo; o mapa completo está na aba
"De onde vem" da página *Jurisprudência Registral*.

| O que | Onde | Como consultar |
|---|---|---|
| Atos da Corregedoria Geral (Classificadores II e III) e atos da Presidência/SEMA (parte do I) | **DEJESP** — Diário Eletrônico da Justiça do Estado de SP, Caderno 1 Administrativo (`idCaderno` 10), Subseção III (JUDICIAL / EXTRAJUDICIAL, Dicoge 1/2/5.1) | `tjsp.jus.br/dejesp`. API: `GET /atcapi/dje/v1/caderno/descricoes/pesquisa-avancada?dataInicio=AAAA-MM-DD&dataFim=…&diarioFuturo=false` devolve a edição; depois `POST /atcapi/dje/v1/caderno/paginado/pesquisa-avancada` com `{dataInicio,dataFim,palavrasChave,skip,take,caderno}` devolve o texto das páginas |
| Acórdãos do CSM (Classificador I) e atos das 1ª/2ª Varas de Registros Públicos da Capital (Classificador IV) | **DJEN** — Diário de Justiça Eletrônico Nacional (CNJ), órgãos "Intimação de Acordãos" e "Foro Central Cível – 1ª/2ª Vara de Registros Públicos" | `comunicaapi.pje.jus.br/api/v1/comunicacao` com `siglaTribunal=TJSP` + `numeroProcesso` ou `dataDisponibilizacaoInicio/Fim` |

⚠️ **O antigo DJe (`dje.tjsp.jus.br/cdje`) está morto.** O Caderno 1 foi
extinto e a última edição é **22/07/2025**; o DEJESP assumiu em 23/07/2025.
Por isso aquela consulta devolve sempre 22/07/2025 — não é bloqueio.

⚠️ **O DOE-SP (`do-api-web-search.doe.sp.gov.br`) devolve `totalItems: 0`
em toda tentativa.** Não é fonte utilizável.

⚠️ **O campo `count` do DJEN mente.** Ele devolve o tamanho da página, não o
total. Em 22/10/2026 a 1ª Vara de Registros Públicos declarou `count: 100` e
tinha **233** itens. Sempre paginar até vir menos que `itensPorPagina`.

### Teste de reprodução — 22/10/2026 (edição 6716 do INR)

Reproduzidos **5 de 5 atos** da edição do INR usando só as fontes abertas,
sem nenhum acesso ao INR. Regra que acertou em cheio, sem falso positivo
nem perda:

- **Classificadores II/III** — DEJESP, Caderno 1, páginas da Subseção III.
  Devolveu exatamente `Dicoge 1 → CORREGEDORES PERMANENTES`,
  `Dicoge 5.1 → PROCESSO Nº 0000933-56.2026.8.26.0100` e
  `Dicoge 5.1 → PROCESSO Nº 1048130-24.2025.8.26.0100`. O INR descartou o
  `Dicoge 2` (bloco JUDICIAL) — o corte é por subseção.
- **Classificador IV** — DJEN, `orgaoId` 93296 (1ª Vara de Registros
  Públicos) e 93416 (2ª Vara). Filtro: `nomeClasse` em
  {Dúvida, Retificação de Registro de Imóvel, Pedido de Providências}
  **E** texto contendo decisão (`JULGO|Diante do exposto|DECIDO|homologo|
  defiro|indefiro|extingo`). De 233 itens, devolveu os 2 que o INR publicou.
  O filtro duplo é necessário: havia 1 Dúvida e 2 Retificações no dia que são
  só andamento ("Recepciono o recurso", "Abra-se vista") e o INR não pegou.

### Retrotestes contra as 35 edições arquivadas (01/09 a 22/10/2026)

**Filtro 2 — decisões do CSM: 30 de 30. Reprodução perfeita.**
O órgão **`orgaoId=92345`** do DJEN ("Intimação de Acordãos") contém
*exatamente* o conjunto que o INR publicou no período: 30 itens no DJEN,
30 no gabarito, zero perdidos e zero sobras. **Não precisa de filtro
nenhum — basta ler o órgão.** Só APELAÇÃO CÍVEL (26) e EMBARGOS DE
DECLARAÇÃO CÍVEL (4), todos com "(Corregedor(a) Geral)" e sinal registral.

O texto do DJEN é **igual ou maior** que o do INR, e traz seções que o INR
corta ("Legislação citada", "Jurisprudência citada", advogados):

| Acórdão | DJEN | INR |
|---|---|---|
| 1001998-69.2026.8.26.0100 | 3.562 car. | 3.424 car. |
| 1003618-59.2024.8.26.0271 | 1.217 car. | 1.276 car. |

E o DJEN é **mais rápido**: o INR raciona 5 acórdãos por edição e empurra o
resto. DJEN 08/09 tinha 8 → INR publicou 5 em 08/09 e 3 em 09/09. DJEN
28/09 tinha 10 → 5 em 28/09 e 5 em 29/09. DJEN 09/10 só chegou ao INR na
edição de **13/10**, quatro dias depois.

**Filtro 1 — ASSIS: mecanismo validado, com uma ressalva.**
Em 35 edições a Comarca de Assis apareceu **zero vezes**. As 20 ocorrências
do termo eram "assiste razão", "assistência/assistida", ou sobrenome
(Otaniel de Souza Assis, Luciano Francisco de Assis Farina, a citação
"ASSIS, Araken").
A busca do DEJESP por `palavrasChave` funciona: "Assis" devolve 283 páginas
em 52 dias (~5/dia), volume trabalhável.
⚠️ **A busca por frase NÃO funciona** — é OU entre as palavras.
"Comarca de Assis" devolveu 4.930 páginas (praticamente a edição inteira).
Então: buscar a palavra isolada, puxar as páginas e desambiguar o contexto
manualmente. Nunca confiar no `totalElementos` de uma busca multi-palavra.

**Classificador IV — a seleção do INR NÃO é mecânica.**
A primeira regra (classe registral + verbo de decisão) quebrou ao incluir a
2ª Vara: em 22/10 devolveu 5 onde o INR publicou 2; em 21/10 perdeu 2 que o
INR publicou. Itens idênticos em classe e forma são separados pelo
**assunto e pela relevância**, não por padrão de texto.

Regra adotada **para a nossa triagem** (decisão da Raquel em 22/10/2026:
"pode descartar no nosso tb"), implementada em `iv_regra.py` — invertida,
por **exclusão**, porque perder um ato é pior que incluir um a mais:

- Fora por assunto: `Cremação/Traslado`, `Translado de corpo`,
  `Petição intermediária`.
- Fora por ser mero andamento: "À parte interessada/requerente/
  representante", "facultada manifestação", "abra-se vista",
  "notifique(m)-se", "diligencie-se", "cumpra-se o alvará", "alvará
  disponível", "recolhimento dos emolumentos", "defiro a gratuidade",
  "defiro a habilitação", "defiro o prazo"/"prazo para cumprimento",
  "ciente das providências", "recepciono o recurso".
- Entra todo o resto.

Resultado em 19–22/10: **nunca perdeu um ato do INR (10 de 10)**. Captura a
mais (37 contra 10), mas o teste rodou sobre trechos de 150 caracteres, em
que a decisão muitas vezes nem aparece — com o texto inteiro a exclusão
pega bem mais. **A sobra não foi medida de forma confiável; a falta, sim.**

⚠️ Em 19/10 o INR publicou **zero** atos do Classificador IV, mas havia no
DJEN 8 itens registrais, inclusive o 1018097-17.2026.8.26.0100 (8.531
caracteres, "Trata-se de pedido de providências", Registro de Imóveis).
Pode ter ido para a edição de 23/10, que não está arquivada — verificar
antes de concluir que o INR perde atos.

---

## 2-B. Vigilância da tarefa agendada

A tarefa "Classificador INR — varredura diária (8h e 11h)"
(`trig_01VqHdvw33fduYVXzVmUKo3z`, cron `0 11,14 * * 1-5`, UTC) **já ficou
desligada sozinha**: em 14/10/2026 foi suspensa com
`suspension_reason: device_absent` e ninguém percebeu por oito dias. Os dias
15 a 22/10 só foram varridos porque a Raquel puxou o assunto nas conversas.

**Decisão dela em 22/10/2026: avisar sempre.** Em qualquer conversa sobre o
projeto, conferir antes de responder:

1. `list_triggers` e verificar se a tarefa está `enabled: true` e sem
   `suspension_reason`. Se estiver desligada ou suspensa, dizer isso em
   destaque no começo da resposta, com a data do último disparo.
2. Conferir se a página tem dia útil sem registro. Se tiver, dizer quais e
   desde quando.

Essa conferência não depende do computador estar ligado — é consulta à
configuração da tarefa. Fazer mesmo quando a conversa for sobre outro
assunto do projeto.

⚠️ **O texto (prompt) da tarefa só muda com aprovação da Raquel** numa
conversa ligada ao Mac, porque a tarefa exige aquele computador. Nome,
horário e ligar/desligar mudam sem aprovação — enviar essas alterações em
chamada separada, sem o prompt. **Nunca apagar e recriar a tarefa** para
contornar: isso perde o histórico de execuções e o vínculo com o computador.
O texto vigente proposto está em `prompt-tarefa-diaria.md`, nesta pasta.

---

## 2-A. Varredura paralela pelas fontes abertas

Aprovada pela Raquel em 22/10/2026. Roda **todo dia, junto** com a do INR, e
a página marca onde as duas divergem. Escopo: só o essencial — Filtro 2
(acórdãos do CSM), atos da Corregedoria Geral (Classificadores II e III) e
Filtro 1 (Assis). **Classificador IV fica fora da triagem** (ver seção 3).

⚠️ As duas APIs **não respondem do contêiner da sessão** (403 no proxy).
Só funcionam pelo navegador interno, com `javascript_tool`. Nunca tentar
por `curl`/`python` no contêiner.

⚠️ A API do DJEN devolve HTML em vez de JSON quando o ritmo aperta. Sempre
conferir o `content-type`, repetir até 4 vezes com espera crescente e
pausar ~350 ms entre páginas.

### Passo 1 — acórdãos do CSM (Filtro 2)

```
GET comunicaapi.pje.jus.br/api/v1/comunicacao
    ?siglaTribunal=TJSP&orgaoId=92345
    &dataDisponibilizacaoInicio=AAAA-MM-DD&dataDisponibilizacaoFim=AAAA-MM-DD
    &itensPorPagina=100&pagina=N
```
Sem filtro: o órgão é exatamente o conjunto. Paginar até vir menos de 100.

### Passo 2 — Corregedoria Geral (Classificadores II e III)

1. `GET /atcapi/dje/v1/caderno/descricoes/pesquisa-avancada?dataInicio=…&dataFim=…&diarioFuturo=false`
   → `idEdicao` / `idVolume`.
2. `GET /atcapi/dje/v1/caderno/descricoes/secoes?idCaderno=10&idVolume=…&idEdicao=…&v2=true&diarioFuturo=false`
   → filtrar as seções cujo nome casa `/^Dicoge/i` e pegar as páginas delas.
   **Usar as páginas das seções Dicoge, nunca tentar adivinhar a faixa da
   Subseção III** — em 20/10 a heurística de fim de faixa falhou e leu 72
   páginas em vez de 7.
3. `POST /atcapi/dje/v1/caderno/paginado/pesquisa-avancada` com
   `{dataInicio,dataFim,palavrasChave:"",skip:<pág.inicial−1>,take:<nº de págs+3>,caderno}`.
4. Extrair os atos com:
   `PROCESSO (PJECOR )?Nº …` · `COMUNICADO CG Nº …` ·
   `CORREIÇÃO (GERAL )?ORDINÁRIA` · `CORREGEDORES PERMANENTES` · `PORTARIA nº …`
   O `PJECOR` entra no meio do padrão (`PROCESSO PJECOR Nº`) — sem o grupo
   opcional, perde os 8 atos do Dicoge 3.1.
5. O INR descarta o bloco **JUDICIAL** (Dicoge 2). Nós também.

### Passo 3 — Assis (Filtro 1)

**Decisão da Raquel em 22/10/2026: o Filtro 1 só alcança matéria
extrajudicial.** Não varrer a edição inteira do DEJESP. Buscar "Assis"
apenas no material que os passos 1 e 2 já trouxeram — páginas das seções
Dicoge, acórdãos do CSM e os itens das Varas de Registros Públicos no DJEN.
Ficam **fora** da triagem, por decisão dela: movimentação de magistrados
(promoção, remoção, designação, inclusive Juiz de Direito Auxiliar de
Assis), obras e licitações do Fórum de Assis, e atos de servidores da
comarca.

Depois desambiguar o contexto à mão: descartar "assiste / assistência /
assistida", sobrenome e citação bibliográfica. Só conta quando se refere à
**comarca** — campo `Comarca:`, "Comarca de Assis", "Oficial de Registro …
da Comarca de Assis", "Juízo Corregedor Permanente de Assis".

⚠️ Não usar `palavrasChave:"Comarca de Assis"` — a busca é OU entre as
palavras e devolve a edição inteira (4.930 páginas no período testado).

### Resultado da 1ª rodada paralela — 20, 21 e 22/10/2026

Classificadores II e III, contra o índice do INR:

| Dia | Edição DEJESP | Atos no INR | Recuperados | Perda |
|---|---|---|---|---|
| 22/10 | 4545 | 3 | 3 | 0 |
| 21/10 | 4544 | 4 | 4 | 0 |
| 20/10 | 4543 | 25 | 25 | 0 |
| **Total** | | **32** | **32** | **0** |

Sobra conhecida, a refinar (nunca perda): citações de atos antigos dentro
do corpo de outro ato (Comunicado CG 575/2026, Portaria 6.812/2003), os
números administrativos internos dos comunicados, e a contagem de
"CORREIÇÃO ORDINÁRIA", que apareceu 8 vezes no texto contra 4 atos no INR.

Acórdãos: 20–22/10 não teve nenhum, nem no INR nem no DJEN. Consistente.

### ⚠️ Achado que muda o entendimento do Filtro 1

A busca "Assis" no DEJESP encontrou, **em texto literal**, ocorrências
reais da Comarca de Assis que **o INR não mostra**, porque estão fora dos
cinco classificadores — ficam na Seção I (movimentação de magistrados),
Seção III (Magistratura) e Seção VIII (SAAB, obras):

- **20/10** — "LUCAS SILVA BARRETTO, 1º Juiz de Direito Auxiliar da Comarca
  de Assis"; designações para a 1ª, 2ª e 3ª Vara Cível de Assis; "26ª C.J. —
  Assis, Dr. PEDRO DE CASTRO E SOUSA".
- **22/10** — promoção "ao cargo de 1º JUIZ DE DIREITO AUXILIAR DA COMARCA
  DE ASSIS"; "BRUNO CÉSAR GIOVANINI GARCIA, Juiz de Direito Auxiliar,
  Assis, para assumir remotamente…"; "reforma das instalações elétricas –
  Fase 2 do Fórum da Comarca de Assis".

Nos mesmos dias o INR registrou "o termo não aparece" (22/10) e "1
ocorrência descartada — assiste razão" (20/10).

**Consequência:** "a edição inteira" do INR ≠ a edição inteira do diário. O
INR já cortou ~95% do DEJESP antes de montar os classificadores, e o
Filtro 1 herdou esse corte sem que isso estivesse explícito.

**Decidido em 22/10/2026 — fica como está:** o Filtro 1 só alcança matéria
extrajudicial. Movimentação de magistrados em Assis, obras no fórum e atos
de servidores da comarca **não entram**. Ao escrever a triagem, dizer "não
consta nada" significa *nada em matéria extrajudicial*, não "nada no
diário" — não afirmar o segundo.

**Antes de qualquer decisão sobre a assinatura:** acumular 1–2 meses de
comparação, incluindo o primeiro dia em que Assis aparecer dentro dos
classificadores — o que não aconteceu em 35 edições.

> As duas fontes **não substituem** o INR, que faz a triagem: a edição do
> DEJESP de 22/10/2026 tem 286 páginas; a mesma edição do INR, 5 atos. E
> nenhuma das duas tem tudo — os atos da Corregedoria não estão no DJEN, e
> os acórdãos do CSM não estão no DEJESP. São recurso de contingência e de
> conferência.

---

## 3. Escopo — apenas DOIS filtros

Critério revisado pela Raquel em 15/09/2026. **Só entra no resumo o que passar
por um destes dois filtros. Nada além disso.**

### Filtro 1 — ASSIS

Buscar o termo **"ASSIS"** na edição inteira. Qualquer outra comarca não
interessa e não deve ser mencionada.

⚠️ **Cuidado com falso positivo:** "Assis" também é sobrenome de pessoa
(ex.: "Francisco Araujo de Assis Azevedo Learte"). Só conta quando se refere
à **comarca de Assis** — normalmente no campo `Comarca:` do item, ou no corpo
como "Comarca de Assis", "Oficial de Registro ... da Comarca de Assis",
"Juízo Corregedor Permanente de Assis".

### Filtro 2 — Decisões do CSM

Todas as decisões do **Conselho Superior da Magistratura do Estado de São
Paulo** (Classificador I), **independentemente da comarca de origem**, porque
são precedentes que orientam a qualificação registral.

- Contam: acórdãos do CSM (o item traz "CONSELHO SUPERIOR DA MAGISTRATURA -
  CSM" e "ACÓRDÃO").
- **Não** contam: "INTIMAÇÃO DE ACÓRDÃO" (é só a publicação da intimação dos
  mesmos acórdãos — duplicata); e atos administrativos publicados no
  Classificador I que não são do CSM, como as suspensões de expediente
  assinadas pela Presidência do TJSP (SEMA).

### Tudo o mais fica de fora

Comunicados CG, editais de correição, editais de corregedores permanentes,
atos da CGJ, decisões da 1ª e 2ª Varas de Registros Públicos da Capital —
**não entram**, salvo se citarem Assis (Filtro 1).

---

## 4. Onde procurar cada filtro

| Filtro | Onde |
|---|---|
| ASSIS | edição inteira, todos os 5 classificadores |
| Decisões do CSM | Classificador I |

---

## 5. Os dois produtos

### 5.1 — Triagem diária (uso interno da Raquel)

Duas seções, sempre nesta ordem. **Nada de lista de "demais publicações".**

```
CLASSIFICADOR INR SP — [data]

▸ ASSIS
   (item por item, ou a frase "Não consta nada.")

▸ DECISÕES DO CSM
   Apelação nº ... — Comarca
   Decisão:  (o que o CSM decidiu, 1 linha)
   Tese:     (a ementa em linguagem direta, 2–4 linhas)
   Aplicação prática: (uma frase)
   (ou a frase "Não consta nada.")
```

**Quando não houver nada, escrever exatamente: "Não consta nada."**
Sem explicação, sem lista do que foi descartado, sem contagem de itens.

### 5.2 — Periódico informativo (circula na equipe)

Padrão validado pela Raquel em 15/09/2026. Cada item vira um bloco:

```
TÍTULO CURTO EM CAIXA ALTA — A TESE EM POUCAS PALAVRAS

Síntese da decisão em 2 a 5 linhas: o que foi decidido e por quê,
já em linguagem direta, sem relatório processual.

Orientação prática: uma frase dizendo o que o escrevente faz na
qualificação a partir de agora.

Fonte: órgão – nº do processo – julgamento – DJEN dd/mm/aaaa.
```

**Quadro de ressalva** — usar quando a decisão conflita com lei expressa,
com jurisprudência superior ou com entendimento consolidado:

```
PONTO DE ATENÇÃO — PRECEDENTE CONTROVERTIDO

O que o tribunal decidiu e que deve ser observado na qualificação.
Onde está a tensão jurídica (dispositivo legal / precedente em sentido
diverso), em 2 a 3 linhas. Recomendação de acompanhamento.
```

**Nota crítica** (opcional, ~meia página) — só quando a decisão tiver
implicações maiores do que parece. Confronta o acórdão com a lei, com o
STJ e com a doutrina, e termina com uma conclusão explícita.

**Princípio editorial da Raquel:** separar sempre duas coisas —
*"foi assim que decidiram, logo observamos na qualificação"* de
*"isso não significa que a construção jurídica seja incontroversa"*.

### 5.3 — Regras de redação (valem para os dois)

- Português do Brasil, direto, sem juridiquês desnecessário.
- Toda sigla ou expressão em outra língua vem com o significado na frente
  (ex.: *in rem suam* — em causa própria).
- Título curto → síntese → orientação prática. Nessa ordem, sempre.
- **Nunca inventar.** Se não deu para ler o inteiro teor, escrever
  "não foi possível abrir o inteiro teor" e colar o link.
- Sempre citar número do ato/processo, órgão, data e link.
- Não transformar circunstância de caso concreto em regra geral sem dizer
  que aquilo era particularidade do caso.

---

## 6. Entrega

- **Frequência:** diária, em dias úteis, às 8h (tarefa agendada
  "Classificador INR — varredura diária (8h)").
- **Canal:** a página **única** "Classificadores INR SP" (Artifact), no desenho
  do Qualifica, atualizada a cada varredura.
  - URL: `https://claude.ai/artifact/5CB7iS7h31ufbkqj53ji1e`
  - Arquivo-fonte nesta sessão: `monitor-classificador-inr.html`,
    com o arquivo de apoio `dados.js`.
  - Para atualizar: republicar **o mesmo caminho de arquivo**, ou passar a URL
    acima como `url`. Publicar sem a URL cria uma página nova — erro a evitar.
    Omitir o parâmetro `files` preserva o `dados.js` já publicado.
  - Entrada nova entra **no topo**, acima do dia anterior; os contadores do
    cabeçalho (edições, citações de Assis, acórdãos do CSM, período) também.
- **Uma página só.** Índice e triagem ficam juntos: um cartão por dia, e dentro
  dele Assis → decisões do CSM → índice completo da edição, na hierarquia do INR
  (classificador → órgão → seção → ato). Os atos do índice que têm resumo
  detalhado são clicáveis e abrem o mesmo painel. **Nunca criar página separada**
  — a Raquel já corrigiu isso uma vez, em 16/09/2026.
- **Sobre a página:** é privada por padrão (só a Raquel vê). Se ela gerar o link
  de compartilhamento, quem tiver o link vê **sempre a versão mais recente** —
  as atualizações aparecem para todos automaticamente, sem reenviar link.

---

## 6-A. Controle de qualidade — conferência contra o índice

A contagem de acórdãos do CSM sai do **índice da edição**, nunca da busca no
texto. Em 11/09/2026 um acórdão foi perdido e o dia reportado como "não consta
nada". Causas: a busca por `Voto nº` diferenciava maiúsculas e a página trazia
`VOTO Nº`; e a página foi lida antes de terminar de carregar.

1. Esperar o carregamento completo antes de ler.
2. Extrair a árvore de `#indice_classificador`; a hierarquia está no
   `padding-left` dos `<p>` (20/40/60/80px).
3. Contar os atos sob `CONSELHO SUPERIOR DA MAGISTRATURA - CSM → ACÓRDÃO`.
   Esse número é a verdade do dia.
4. Só então buscar no texto. Texto menor que o índice = defeito na extração.
5. Busca sempre insensível a maiúsculas e a acentos.

**Edição ausente não é edição vazia.** Se a edição do dia ainda não subiu,
registrar "sem edição publicada" e recuperar o dia na varredura seguinte —
nunca escrever "não consta nada" sem ter varrido. Em 16/09 e 17/09/2026 a
edição não estava no ar às 8h.

---

## 7. Estado atual (17/09/2026)

| Item | Situação |
|---|---|
| Permissão do navegador para o INR | ✅ concedida |
| Login no INR | ✅ ativo no navegador interno (sessão do titular) |
| Critério de relevância | ✅ definido (seção 3) — dois filtros, nada além |
| Mapa de navegação do INR | ✅ levantado, em `memory.md` seção 3 |
| Formato do resumo | ✅ definido com a linguagem da Raquel (seção 5) |
| Canal de entrega | ✅ página única "Classificadores INR SP" |
| Automação diária | ✅ tarefa agendada, dias úteis às 8h, aprovação automática |
| E-mail do INR como fonte alternativa | ⛔ cadastro feito em 15/09, nada recebido até 17/09 |
| Horário de publicação do INR | ⏳ não confirmado; às 8h a edição costuma faltar |

---

## 8. Ordem de execução da rotina

1. Ler este arquivo e o `memory.md`.
2. Conferir se o último dia da página ficou como "sem edição publicada"; se
   ficou e a edição já subiu, recuperar aquele dia primeiro.
3. Tentar o e-mail do INR no Gmail. Se não servir, seguir pelo navegador.
4. Abrir o INR no navegador interno; confirmar que a sessão está ativa.
   Se tiver caído, **avisar a Raquel** — não tentar logar, não resolver reCAPTCHA.
5. Pegar o link da edição de hoje pelo índice (o id nunca é calculado).
6. Esperar o carregamento e extrair a árvore do índice (seção 6-A).
7. Aplicar os dois filtros da seção 3; conferir a contagem contra o índice.
8. Abrir o inteiro teor de cada acórdão.
9. Montar a triagem no formato da seção 5 e publicar na página única.
10. Registrar no `memory.md`: data, id da edição, fonte usada, o que foi
    encontrado em cada filtro e qualquer aprendizado novo.

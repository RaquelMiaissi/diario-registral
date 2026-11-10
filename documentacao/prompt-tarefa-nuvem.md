# Texto da tarefa agendada em nuvem — Diário Registral

> **Tarefa:** "Diário Registral — varredura diária em nuvem (8h10 e 9h10)", tipo Claude Code,
> repositório `RaquelMiaissi/diario-registral`, ambiente de nuvem "Default"
> (domínios liberados em 10/11/2026: comunicaapi.pje.jus.br, www.tjsp.jus.br,
> dje.cnj.jus.br, atos.cnj.jus.br, normas.receita.fazenda.gov.br, stj.jus.br, portal.stf.jus.br).
> **Criada em:** 10/11/2026. Substitui a tarefa antiga do tipo Chat
> (`trig_01VqHdvw33fduYVXzVmUKo3z`), que fica inativa, não apagada.

---

Varredura diária dos diários oficiais em matéria registral para o Cartório de Registro de Imóveis, Títulos e Documentos e Civil de Pessoas Jurídicas da Comarca de Assis/SP. Projeto: Diário Registral. Esta tarefa roda na nuvem, com o repositório `RaquelMiaissi/diario-registral` clonado no diretório de trabalho.

Fale em português do Brasil. Toda sigla ou palavra em outra língua vem com o significado na frente. Não suponha e não invente: o que não foi lido na fonte não entra.

## Antes de tudo

1. Leia `README.md` e `dados/schema.md` do repositório. Se existir a skill `diario-registral-assis`, invoque-a: ela é a fonte da verdade do formato e das regras de redação. Se o conector Google Drive estiver disponível, leia também o `CLAUDE.md` da pasta "04 Estudos e IA/Notion Workspace/Publicações_INR" (pasta mantida com o nome antigo); se não estiver, siga só por este texto.
2. Os dados do projeto estão em `docs/dados.json`: `acordaos[]` (cada um com `ed` = data em que saiu no DJEN em dd/mm/aaaa, `djen` em AAAA-MM-DD, `djenId`, `num`, `com`, `titulo`, `resumo{tema,corpo[],orientacao,atencao}`, `integra`, `fonte`, `fonteUrl`), `dias[]` (`d`, `wd`, `sem`, `nac`, `fonte`), `alertas[]` (comunicados CG de documentos falsos) e `assis[]` (publicações sobre a comarca). Veja o último dia útil em `dias`: a varredura cobre do dia seguinte a ele até hoje (fuso America/Sao_Paulo), inclusive. Se faltar mais de um dia útil, diga isso em DESTAQUE no começo da resposta, com as datas.

## Fontes — só estas duas

Diários oficiais abertos, sem senha. Nenhuma outra fonte. Acesse com `curl` ou `python` direto do contêiner, pelo proxy já configurado (variável `HTTPS_PROXY`; nunca desligar a verificação TLS).

- **DJEN** (Diário de Justiça Eletrônico Nacional, do CNJ): `https://comunicaapi.pje.jus.br/api/v1/comunicacao`.
- **DEJESP** (Diário Eletrônico da Justiça do Estado de São Paulo): base `https://www.tjsp.jus.br/atcapi/dje/v1/`.

Se o proxy devolver 403 "request blocked: no rule or allowlist entry allows host", ou qualquer outro erro impedir a leitura, avise em destaque que a varredura não pôde ser feita, com o erro exato (código e mensagem) e o domínio, e PARE: não invente resultado, não registre o dia como vazio, não altere arquivo nem página.

## Passo 1 — acórdãos do CSM (DJEN)

```
GET https://comunicaapi.pje.jus.br/api/v1/comunicacao
    ?siglaTribunal=TJSP&orgaoId=92345
    &dataDisponibilizacaoInicio=AAAA-MM-DD&dataDisponibilizacaoFim=AAAA-MM-DD
    &itensPorPagina=100&pagina=N
```

O órgão 92345 ("Intimação de Acordãos") é exatamente o conjunto dos acórdãos registrais do Conselho Superior da Magistratura (CSM) — não precisa de filtro. Paginar até vir menos de 100 itens; o campo `count` mente. A API devolve HTML em vez de JSON quando o ritmo aperta: conferir o `content-type`, repetir até 4 vezes com espera crescente e pausar ~350 ms entre chamadas.

De cada item: `numeroProcesso` (formatar "Apelação NNNNNNN-DD.AAAA.8.26.FFFF" ou "Embargos de Declaração …" conforme `nomeClasse`), comarca (no `texto`, depois de "Comarca:" ou no nome do foro), `data_disponibilizacao` (→ `ed` e `djen`), `id` (→ `djenId`), `texto` inteiro (→ `integra`, retirando nomes de advogados e números de OAB), `fonte` = "DJEN — TJSP, órgão Intimação de Acordãos, dd/mm/aaaa", `fonteUrl` = `https://comunicaapi.pje.jus.br/api/v1/comunicacao?siglaTribunal=TJSP&numeroProcesso=<20 dígitos>`. Acórdão com `djenId` já existente não entra de novo.

## Passo 2 — Corregedoria Geral (DEJESP)

1. `GET caderno/descricoes/pesquisa-avancada?dataInicio=AAAA-MM-DD&dataFim=AAAA-MM-DD&diarioFuturo=false` → `idEdicao` e `idVolume` do Caderno 1 Administrativo (`idCaderno` 10). Sem edição para a data = feriado, registrar "sem edição".
2. `GET caderno/descricoes/secoes?idCaderno=10&idVolume=…&idEdicao=…&v2=true&diarioFuturo=false` → só as seções cujo `descricaoSecao` casa `/^Dicoge/i` e as páginas delas. NUNCA adivinhar a faixa de páginas.
3. `POST caderno/paginado/pesquisa-avancada` com `{dataInicio, dataFim, palavrasChave:"", skip:<página inicial − 1>, take:<nº de páginas + 3>, caderno}` — `caderno` é o objeto completo devolvido no item 1 (`idCaderno`, `descricao`, `edicoes` com `data`, `idEdicao`, `idVolume`, `v2`); passar só o número dá erro 400.
4. Extrair os atos com `PROCESSO (PJECOR |SEI )?Nº …`, `COMUNICADO CG Nº …`, `CORREIÇÃO (GERAL )?ORDINÁRIA`, `CORREGEDORES PERMANENTES`, `PORTARIA nº …`. Cortar cada ato só em `PROCESSO (PJECOR |SEI )?Nº \d{7}-\d{2}\.\d{4}` — o cabeçalho também contém "PROCESSO Nº".
5. O bloco JUDICIAL (Dicoge 2) fica fora. Só o EXTRAJUDICIAL.
6. Comunicados CG de documentos falsos (selo, matrícula, certidão, procuração, escritura falsos) entram em `alertas[]`: `d`, `ed`, `num` ("CG 850/2026"), `proc`, `origem`, `serv`, `tipo[]`, `ri` (bool), `selos[]`, `matriculas[]`, `resumo` (redação própria, 1 a 3 frases), `obs`, `texto`, `fonte` ("DEJESP, Caderno 1, edição NNNN, dd/mm/aaaa").

## Passo 3 — Assis (três canais, só matéria extrajudicial)

Movimentação de magistrados, obras do fórum e atos de servidores da comarca ficam fora. Registrar quantas ocorrências foram descartadas e por quê. "Não consta nada" = nada em matéria extrajudicial.

1. Material dos passos 1 e 2: "Assis" insensível a maiúsculas e acentos, lendo o contexto. "Assis" também é sobrenome e aparece dentro de "assiste", "assistida", "assistência" — não contam.
2. Caderno 1 inteiro do DEJESP: `POST caderno/paginado/pesquisa-avancada` com `palavrasChave:"Assis"` (uma palavra só — NUNCA "Comarca de Assis", a busca é OU) e o objeto `caderno` completo. Vêm só as páginas com ocorrência. Entra o que for Subseção III, Seção II, correição, repreensão, perda de prazo ou determinação dirigida à comarca ou às serventias.
3. Foro de Assis no DJEN: `GET comunicacao?siglaTribunal=TJSP&orgaoId=…&dataDisponibilizacaoInicio=…&dataDisponibilizacaoFim=…` para os órgãos 91968 (1ª Vara Cível — Juízo Corregedor Permanente do RI), 92075, 92199, 91824 e 110327. Entra Pedido de Providências, Dúvida, Retificação, Processo Administrativo ou texto que cite o Registro de Imóveis, a Corregedoria Permanente ou correição.

O que entrar vai para `assis[]`: `d`, `org`, `num`, `cls`, `parte`, `tema`, `texto`, `fonte`, `fonteUrl`.

## Redação dos acórdãos novos

Ler o texto publicado no DJEN (partes, relator, resultado e ementa — o inteiro teor não sai no diário; nas páginas o campo `integra` aparece como "acórdão publicado", nunca "íntegra") e escrever `resumo`: `tema` (título que já entrega a conclusão), `corpo` (2 a 4 parágrafos em prosa direta: o que foi decidido e por quê), `orientacao` (o que o escrevente faz na qualificação; "apenas ciência" se não muda a rotina), `atencao` (só com exceção, limite ou tensão com lei ou precedente superior). Mais `titulo` curto em caixa alta. Não deduzir teor de ementa truncada: dizer isso.

## Entrega

1. **Dados.** Acrescentar em `docs/dados.json` os acórdãos novos no começo de `acordaos`, alertas novos no começo de `alertas`, publicações de Assis no começo de `assis`, e um registro por dia varrido no começo de `dias` (`d` dd/mm/aaaa, `wd` dia da semana, `sem` null ou motivo, `nac` acórdãos daquele dia, `fonte` "DJEN + DEJESP (edição NNNN)"). Manter indentação de 1 espaço e `ensure_ascii=False`.
2. **Site.** Rodar `python3 src/build/site.py` (injeta o JSON em `docs/index.html`).
3. **Página Jurisprudência Registral.** Rodar `python3 src/build/limpo.py docs/dados.json /tmp/jurisprudencia-registral.html` e republicar esse arquivo com a ferramenta Artifact passando `url: https://claude.ai/artifact/YRiR1psiC9xaPJeCXVA1GQ` (ler antes com `read`). Publicar sem a `url` cria página duplicada — erro a evitar. Nunca criar página separada.
4. **Git.** `git checkout -B varredura-automatica`, `git add docs/dados.json docs/index.html`, commit com mensagem "dd/mm/aaaa: DJEN (N acórdãos) + DEJESP edição NNNN" e `git push -u origin varredura-automatica --force-with-lease`. NUNCA fazer push em `main`: quem leva para `main` é a Raquel.
5. **Resposta** em quatro blocos: ASSIS (item por item ou "Não consta nada." + verificação dos descartes), DECISÕES DO CSM (por acórdão: decisão em 1 linha, tese em 2–4 linhas, aplicação prática em 1 frase; ou "Não consta nada."), ATOS DA CORREGEDORIA (uma linha por ato; ▲ quando toca rotina de RI, RTD ou RCPJ; "— apenas ciência" quando não tem reflexo na serventia), ALERTAS DE FRAUDE (uma linha por comunicado novo, ou "Nenhum comunicado novo."). Uma linha com os dias varridos e a edição do DEJESP de cada um, e uma linha lembrando que o ramo `varredura-automatica` aguarda o merge dela em `main`.
6. Se o conector de memória existir, registrar em `/areas/diario-oficial-inr.md`: data, edição do DEJESP, acórdãos, atos, alertas novos e o resultado de Assis. Se não existir, pular sem avisar erro.

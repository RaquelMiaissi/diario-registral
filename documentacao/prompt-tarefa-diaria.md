# Texto proposto para a tarefa agendada

> **Tarefa:** "Classificador INR — varredura diária (8h e 11h)"
> **ID:** `trig_01VqHdvw33fduYVXzVmUKo3z`
> **Escrito em:** 22/10/2026
> **Situação:** aguardando aprovação da Raquel numa conversa ligada ao Mac.
> Até ser aprovado, a tarefa roda com o texto antigo — que **não** tem a
> regra de ritmo no INR nem a varredura paralela.
>
> Para aplicar: aprovar a troca numa conversa do Cowork ligada a este
> computador, ou colar este texto direto na tarefa, pelo aplicativo Claude
> no Mac.

---

Varredura diária do Classificador INR SP para o Cartório de Registro de Imóveis, Títulos e Documentos e Civil de Pessoas Jurídicas da Comarca de Assis/SP.

Invoque a skill `diario-oficial-inr-assis` e siga o roteiro dela. A skill é a fonte da verdade do formato; este prompt acrescenta o que é específico desta rotina.

Leia também o `CLAUDE.md` do projeto, na pasta do Drive "04 Estudos e IA/Notion Workspace/Publicações_INR" — a seção 2-A tem a rotina da varredura paralela em detalhe, com os endpoints e as armadilhas.

## FORMATO — quatro blocos

1. ASSIS — item por item, ou "Não consta nada." + a verificação das ocorrências descartadas.
2. DECISÕES DO CSM — por acórdão: decisão em 1 linha, tese em 2–4 linhas, aplicação prática em 1 frase. Ou "Não consta nada."
3. RESUMO DA EDIÇÃO — todos os atos, agrupados por classificador (I, II, III, III Especial, IV), uma linha cada, dizendo o que o ato resolve ou comunica. Ato que toca rotina de RI, RTD ou RCPJ leva ▲ no começo da linha. Ato sem reflexo na serventia fecha com "— apenas ciência". Ato já tratado em destaque: só "ver destaque acima".
4. CONFERÊNCIA PARALELA — ver a seção própria abaixo.

"Não consta nada." é frase exclusiva dos dois filtros. O resumo da edição nunca sai vazio, salvo edição ausente.

## PRIMEIRO PASSO DE TODO DIA — conferir os dias anteriores

Antes de varrer hoje, olhe a página publicada e veja se (a) o último dia registrado ficou como "sem edição publicada" ou "varredura pendente", ou (b) algum dia útil ficou sem registro.

Se a página estiver mais de um dia útil atrasada, diga isso em DESTAQUE no começo da resposta, com as datas e desde quando — a tarefa já ficou suspensa por ausência do computador entre 09/10 e 14/10/2026 e ninguém percebeu por oito dias.

Recupere no máximo DUAS edições atrasadas por execução, as mais antigas primeiro, e avise quantas ainda faltam. Não tente recuperar tudo de uma vez: em 22/10/2026 o IP foi bloqueado pelo INR ("Verificação de segurança") porque uma execução abriu oito edições quatro vezes cada em poucos minutos.

## REGRA DE RITMO NO INR — não quebre

Abra cada edição do INR UMA vez e guarde o conteúdo em memória para reusar. Nunca reabra a mesma edição para pegar outro pedaço.

Se aparecer a tela "Verificação de segurança" pedindo para liberar o IP: NÃO resolva o desafio de imagem, NÃO digite nada. Deixe o painel nessa tela, avise a Raquel que o IP precisa ser liberado por ela, registre o dia como não varrido e PARE.

## Caminho A — e-mail do INR (tente primeiro, não depende do computador)

Procure no Gmail a mensagem de HOJE de `inr@boletiminr.com.br`, assunto "Classificadores - SP/PR/RS". Abra com `get_thread`. De 15/09 a 14/10/2026 esse e-mail trouxe só os links, sem o texto dos atos — se continuar assim, registre em uma linha e siga para o Caminho B. Se um dia trouxer o conteúdo, use-o e registre "fonte: e-mail do INR".

## Caminho B — navegador interno

1. Abra `https://inrpublicacoes.com.br/site/boletim/classificadoresINR-SP` no navegador interno do Claude.
2. Confirme que a sessão de assinante está ativa. Sinais de sessão caída: redireciona para `/site/area-assinante`, ou a edição abre só com o índice e a frase "Acesse a Área do Assinante e veja o conteúdo completo". Se caiu, deixe o painel na página de login, avise a Raquel e PARE. Nunca digite a senha, nunca resolva reCAPTCHA.
3. No índice, pegue o link da edição pela data (o id da URL não é previsível — nunca calcule).

Se nenhum navegador estiver alcançável e o e-mail não tiver servido, avise que a varredura não pôde ser feita e por quê. Não invente resultado e não registre o dia como vazio.

## Os dois filtros (destaques)

- **ASSIS**: buscar o termo na edição do INR, insensível a maiúsculas e acentos, lendo o contexto de cada ocorrência. "Assis" também é sobrenome de parte, de advogado e de autor citado, e aparece dentro de "assiste", "assistida", "assistência", "Previdência e Assistência Social", "Compra Assistida" — esses não contam. Só vale a comarca de Assis. Registre quantas ocorrências foram descartadas e por quê.
  - **Escopo decidido pela Raquel em 22/10/2026: o filtro só alcança matéria extrajudicial.** Ficam FORA: movimentação de magistrados (promoção, remoção, designação, inclusive Juiz de Direito Auxiliar de Assis), obras e licitações do Fórum de Assis, atos de servidores da comarca. Essas menções existem no DEJESP e o INR não as mostra.
  - Ao escrever "Não consta nada", isso significa *nada em matéria extrajudicial* — nunca afirmar que o termo não aparece no diário.
- **Decisões do CSM**: acórdãos do Conselho Superior da Magistratura (Classificador I), de qualquer comarca. Não contam como acórdão: "INTIMAÇÃO DE ACÓRDÃO" (duplicata), os atos administrativos da Presidência do TJSP no mesmo classificador (SEMA 1.2.1 — suspensão de expediente), nem pauta de julgamento virtual ou resultado de sessão (SEMA 1.1.2). Esses entram no resumo da edição como qualquer outro ato.

## Conferência obrigatória contra o índice — não pule

As contagens saem do ÍNDICE da edição, nunca da busca no texto. Em 11/09/2026 um acórdão do CSM foi perdido e o dia reportado como "não consta nada"; a busca procurava "Voto nº" diferenciando maiúsculas e a página trazia "VOTO Nº", e a página foi lida antes de terminar de carregar.

1. Espere a página carregar por inteiro antes de ler.
2. Extraia a árvore de `#indice_classificador`. A hierarquia está no `padding-left` dos `<p>`: 20px = classificador, 40px = órgão, 60px = seção, 80px = ato.
3. Conte os nós sob `CONSELHO SUPERIOR DA MAGISTRATURA - CSM → ACÓRDÃO`. Esse número é quantos acórdãos o dia tem.
4. Conte TODOS os nós de nível ato (80px). Esse número é quantas linhas o resumo da edição tem de ter. Se vier menos, falta ato — corrija antes de fechar o dia.
5. Só então busque cada acórdão no texto. Texto menor que o índice = defeito na extração; corrija, não reporte a menos.

## VARREDURA PARALELA pelas fontes abertas — fazer todo dia

Rodar junto com a do INR e comparar. Objetivo: medir se as fontes abertas entregam o mesmo, para decidir no futuro sobre a assinatura. NÃO sugerir cancelar a assinatura; só reportar os números.

As duas APIs NÃO respondem do contêiner da sessão (403 no proxy). Só funcionam pelo navegador interno, com `javascript_tool`. Nunca tentar por curl ou python.

A API do DJEN devolve HTML em vez de JSON quando o ritmo aperta: conferir o `content-type`, repetir até 4 vezes com espera crescente, pausar ~350 ms entre páginas.

**Passo 1 — acórdãos do CSM.** `GET https://comunicaapi.pje.jus.br/api/v1/comunicacao?siglaTribunal=TJSP&orgaoId=92345&dataDisponibilizacaoInicio=AAAA-MM-DD&dataDisponibilizacaoFim=AAAA-MM-DD&itensPorPagina=100&pagina=N`. Sem filtro nenhum: esse órgão é exatamente o conjunto dos acórdãos registrais do CSM. Paginar até vir menos de 100 — o campo `count` mente, devolve o tamanho da página.

**Passo 2 — Corregedoria Geral (Classificadores II e III), no DEJESP.**
Base: `https://www.tjsp.jus.br/atcapi/dje/v1/`

1. `GET caderno/descricoes/pesquisa-avancada?dataInicio=AAAA-MM-DD&dataFim=AAAA-MM-DD&diarioFuturo=false` → `idEdicao`/`idVolume` do Caderno 1 Administrativo (`idCaderno` 10).
2. `GET caderno/descricoes/secoes?idCaderno=10&idVolume=…&idEdicao=…&v2=true&diarioFuturo=false` → filtrar as seções cujo nome casa `/^Dicoge/i` e usar as páginas delas. NUNCA adivinhar a faixa da Subseção III: em 20/10/2026 a heurística de fim de faixa falhou e leu 72 páginas em vez de 7.
3. `POST caderno/paginado/pesquisa-avancada` com `{dataInicio,dataFim,palavrasChave:"",skip:<página inicial−1>,take:<nº de páginas+3>,caderno}`.
4. Extrair os atos com: `PROCESSO (PJECOR )?Nº …`, `COMUNICADO CG Nº …`, `CORREIÇÃO (GERAL )?ORDINÁRIA`, `CORREGEDORES PERMANENTES`, `PORTARIA nº …`. O `PJECOR` entra no meio do padrão — sem o grupo opcional, perdem-se os atos do Dicoge 3.1.
5. O INR descarta o bloco JUDICIAL (Dicoge 2). Nós também.

**Passo 3 — Assis.** Buscar "Assis" apenas no material que os passos 1 e 2 trouxeram, respeitando o escopo extrajudicial decidido acima. Não varrer a edição inteira do DEJESP. NUNCA usar `palavrasChave:"Comarca de Assis"` — a busca é OU entre as palavras e devolve a edição inteira.

**Bloco 4 da entrega — CONFERÊNCIA PARALELA.** Uma tabela curta: atos do INR nos Classificadores I (acórdãos), II e III; quantos a varredura aberta recuperou; e a perda. Listar nominalmente qualquer ato que o INR publicou e a varredura aberta NÃO achou — essa é a informação que importa. Sobra (ato que a varredura achou e o INR não) só em contagem, salvo se for ato extrajudicial relevante, e aí nomear.

Referência acumulada até 22/10/2026: acórdãos do CSM 30 de 30 em 35 edições; Classificadores II e III 32 de 32 em 20, 21 e 22/10. Perda zero nos dois. Se algum dia der perda, isso é o achado do dia e vai no topo da resposta.

## Entrega

1. Atualize a página única "Classificadores INR SP", em `https://claude.ai/artifact/5CB7iS7h31ufbkqj53ji1e`. Índice, triagem e resumo ficam na MESMA página — nunca crie página separada. Leia a versão publicada com a ação `read` do Artifact (ela pode ter sido alterada por outra execução), acrescente o dia NOVO NO TOPO mantendo o padrão visual e de redação dos dias anteriores, atualize os contadores do topo e o período varrido, e republique na MESMA URL passando-a como `url`. Publicar sem a `url` cria página duplicada — erro a evitar. O `dados.js` é publicado junto; se não alterá-lo, omita o parâmetro `files` para preservá-lo.
   - O resumo da edição é o campo `resumo` de cada dia em `DIAS`: lista de `[classificador, [linhas]]`. Só aparece nos dias que têm o campo — não inventar resumo para dia antigo que não foi reaberto.
   - Dia sem nada nos dois filtros: Assis e CSM levam "Não consta nada." e o resumo da edição vem completo.

2. Atualize também a página "Jurisprudência Registral", em `https://claude.ai/artifact/YRiR1psiC9xaPJeCXVA1GQ`, quando o dia tiver acórdão do CSM novo: mesma mecânica (ler com `read`, republicar com a `url`).

3. Redija no padrão da skill: tema que já entrega a conclusão, tese em prosa direta, e o que muda na qualificação. Ponto de atenção quando houver exceção, limite ou tensão com lei ou precedente superior. Não invente: se o inteiro teor não abrir, diga isso e cole o link; não deduza o assunto de um ato pelo número do processo.

4. Responda no chat com os quatro blocos, dizendo em uma linha qual caminho funcionou (e-mail ou navegador) e se algum dia anterior foi recuperado.

5. Registre no arquivo de memória do projeto (`/areas/diario-oficial-inr.md`): data, id da edição, fonte usada, total de atos, o que foi encontrado em cada filtro e o resultado da conferência paralela.

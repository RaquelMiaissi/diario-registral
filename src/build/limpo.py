import json
import os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, 'docs', 'dados.json')
SAIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, 'docs', 'jurisprudencia-registral.html')
D = json.load(open(DADOS, encoding='utf-8'))

ORIGEM = [
 {"cls":"1","st":"em uso","stc":"ok","nome":"DJEN — acórdãos do Conselho Superior da Magistratura",
  "secoes":["DJEN","CNJ","TJSP","Intimação de Acordãos","órgão 92345"],
  "onde":"Diário de Justiça Eletrônico Nacional, mantido pelo Conselho Nacional de Justiça (CNJ). O Tribunal de Justiça de São Paulo publica ali a intimação de cada acórdão do Conselho Superior em matéria registral, no órgão “Intimação de Acordãos” (código 92345). Esse órgão contém exatamente o conjunto dos acórdãos registrais — não precisa de filtro nenhum: tudo o que sai nele é apelação cível ou embargos de declaração em dúvida, suscitação, retificação ou procedimento registral, com o(a) Corregedor(a) Geral como relator(a).",
  "traz":"Partes, comarca, relator(a), resultado do julgamento (“Deram provimento ao recurso. V. U.”), a ementa inteira e, quando há, as seções “Legislação citada” e “Jurisprudência citada”. É o texto da aba Acórdãos publicados. Média de 1.300 caracteres por decisão.",
  "nao":"O inteiro teor — relatório e voto — não é publicado em diário nenhum; fica nos autos. Também não traz o número do voto.",
  "acesso":"Consulta pública, sem senha, pela interface de comunicações do PJe: comunicaapi.pje.jus.br/api/v1/comunicacao, com siglaTribunal=TJSP e orgaoId=92345, filtrando por dataDisponibilizacaoInicio e dataDisponibilizacaoFim; ou por numeroProcesso (20 dígitos) para um processo específico — é o que o botão “Ver no DJEN” abre. Página de 100 itens; o campo count da resposta devolve o tamanho da página, não o total, então se pagina até vir menos de 100. Sob consultas rápidas em sequência a API devolve HTML em vez de JSON: conferir o tipo da resposta e repetir com pausa.",
  "ritmo":"Os acórdãos saem em lotes, no dia em que o Tribunal libera a intimação — em setembro e outubro de 2026: 08/09 (8), 11/09 (1), 14/09 (5), 28/09 (10), 09/10 (2), 19/10 (4) e 26/10 (10). Há dias e semanas sem nenhum. Embargos de declaração ficam sob o número do processo principal, sem o sufixo /50000.",
  "prova":"Conferido processo por processo: os 40 acórdãos desta página foram localizados no DJEN pelo número, e a data de cada um é a da publicação lá (data_disponibilizacao). De 01/09 a 22/10/2026 o órgão 92345 reproduziu 30 de 30 acórdãos que o serviço de curadoria então assinado havia publicado, sem perda e sem sobra.",
  "alinea":"Alimenta a alínea <b>a</b> do item 65 das NSCGJ"},
 {"cls":"2","st":"em uso","stc":"ok","nome":"DEJESP — atos da Corregedoria Geral da Justiça",
  "secoes":["DEJESP","TJSP","Caderno 1 — Administrativo","idCaderno 10","Subseção III","EXTRAJUDICIAL","Dicoge 1","Dicoge 3.1","Dicoge 5.1"],
  "onde":"Diário Eletrônico da Justiça do Estado de São Paulo, publicado pelo próprio Tribunal em tjsp.jus.br/dejesp. Entrou no ar em 23/07/2025 e substituiu o Caderno 1 — Administrativo do antigo DJe. Os atos da Corregedoria estão no Caderno 1 — Administrativo, Seção I, Subseção III (Atos e comunicados da Corregedoria Geral da Justiça), dividida em dois blocos: JUDICIAL (Dicoge 2 — fica fora) e EXTRAJUDICIAL (Dicoge 1, 3.1 e 5.1 — é o que se lê). Dicoge é a Diretoria da Corregedoria Geral; o número identifica a divisão de origem.",
  "traz":"Processos CG e PJECOR (decisões da Corregedora-Geral: vacâncias, interinidades, recursos administrativos), comunicados CG (alertas de fraude em reconhecimento de firma, procuração, certidão; bloqueios de cartão de firma; orientações gerais), portarias, editais de correição ordinária e designações de corregedores permanentes.",
  "nao":"Não traz acórdão do Conselho Superior — esses estão só no DJEN. Em dia sem expediente não há edição (em 30/10/2026 não houve Caderno 1; a última edição foi a 4550, de 29/10).",
  "acesso":"Consulta pública, sem senha, em três passos pela API do diário (www.tjsp.jus.br/atcapi/dje/v1/): (1) caderno/descricoes/pesquisa-avancada, por data, devolve a edição do dia (idEdicao, idVolume); (2) caderno/descricoes/secoes, com idCaderno=10 e a edição, devolve o sumário com a página de cada seção — daí se pegam só as seções Dicoge; (3) caderno/paginado/pesquisa-avancada (POST) devolve o texto corrido das páginas pedidas. Nunca se adivinha faixa de páginas: em 20/10/2026 uma heurística leu 72 páginas em vez de 7. A busca por palavra é OU entre os termos — “Comarca de Assis” devolve a edição inteira —, por isso a busca por Assis é feita no texto já extraído.",
  "ritmo":"Uma edição por dia útil, numerada em sequência (4545 em 22/10, 4547 em 26/10, 4548 em 27/10, 4549 em 28/10, 4550 em 29/10/2026). O bloco EXTRAJUDICIAL varia de zero a dezenas de atos; a edição de 20/10 trouxe 25.",
  "prova":"Conferido na edição 4545, de 22/10/2026: o Processo nº 0000933-56.2026.8.26.0100 está na página 21, sob EXTRAJUDICIAL → Dicoge 5.1; o mesmo processo buscado no DJEN devolve zero. Nas edições de 20, 21 e 22/10/2026 a leitura direta recuperou 32 de 32 atos que o serviço de curadoria então assinado havia publicado.",
  "alinea":"Alimenta a alínea <b>b</b> do item 65 das NSCGJ"},
 {"cls":"3","st":"lido — só ciência","stc":"meio","nome":"DEJESP — Presidência, SEMA e sessões do Conselho Superior",
  "secoes":["DEJESP","Caderno 1 — Administrativo","Seção I","Subseção I","SEMA 1.1.2","SEMA 1.3","Seção II"],
  "onde":"No mesmo Caderno 1 do DEJESP: a Seção I, Subseção I (Atos e comunicados da Presidência) e a Seção II (Conselho Superior da Magistratura — Julgamentos, rótulo SEMA 1.1.2). SEMA é a Secretaria da Magistratura do Tribunal.",
  "traz":"Suspensões de expediente e comunicados da Presidência (SEMA 1.3); resultados das sessões virtuais do Conselho Superior (SEMA 1.1.2) — ofícios de diretores de fórum, permutas de juízes, auxílio-sentença, autorizações de residência.",
  "nao":"O resultado de sessão não é acórdão: lista pedidos administrativos deferidos ou negados, sem ementa nem tese. Os acórdãos em matéria registral saem só no DJEN.",
  "acesso":"Mesma API do DEJESP; essas seções aparecem no sumário da edição com as suas páginas.",
  "prova":"Conferido na edição 4545, de 22/10/2026 (comunicados nº 284 e 285/2026 da Presidência, página 11) e na 4548, de 27/10/2026 (resultado da 52ª sessão virtual do CSM, página 13).",
  "alinea":"Entra na triagem como ciência quando toca o expediente das serventias (suspensão de expediente, por exemplo); não gera destaque"},
 {"cls":"4","st":"fora da triagem","stc":"fora","nome":"DJEN — 1ª e 2ª Varas de Registros Públicos da Capital",
  "secoes":["DJEN","Foro Central Cível","1ª Vara de Registros Públicos — órgão 93296","2ª Vara de Registros Públicos — órgão 93416"],
  "onde":"No DJEN, os órgãos “Foro Central Cível — 1ª Vara de Registros Públicos” (código 93296) e “2ª Vara de Registros Públicos” (código 93416).",
  "traz":"Movimentação processual de primeira instância: dúvidas, retificações de registro, pedidos de providências — mais de duzentos itens por dia, a maior parte andamento (“abra-se vista”, “defiro o prazo”, “defiro a gratuidade”).",
  "nao":"Não são precedente. São decisões do juiz corregedor permanente da Capital, que valem para as serventias da Capital e não vinculam outra comarca.",
  "acesso":"Mesma API do DJEN, trocando o orgaoId. A seleção do que importaria ali é editorial, não mecânica: uma regra de exclusão por assunto e por verbo de andamento foi estudada (iv_regra.py) e guardada inativa.",
  "prova":"Conferido pelo número do processo: 1015423-66.2026.8.26.0100 (1ª Vara) e 1003789-73.2026.8.26.0100 (2ª Vara) aparecem no DJEN em 15/09/2026.",
  "alinea":"Fora da triagem por decisão de 22/10/2026: o que for relevante sobe por apelação e chega como acórdão do Conselho Superior (fonte 1)"},
 {"cls":"5","st":"não publicado","stc":"fora","nome":"Inteiro teor dos acórdãos (relatório e voto)",
  "secoes":["autos do processo","e-SAJ — consulta de julgados (não testado)"],
  "onde":"Não está em diário oficial nenhum. O que o DJEN publica é a intimação do acórdão (fonte 1); o relatório e o voto ficam nos autos. O Tribunal mantém uma consulta pública de julgados de segundo grau (e-SAJ), que disponibiliza o PDF dos acórdãos.",
  "traz":"Nos autos: o acórdão completo, com número do voto, relatório e fundamentação — no caso de Andradina, 11 páginas contra 1.300 caracteres na intimação.",
  "nao":"Não se sabe, sem testar, se os acórdãos do Conselho Superior em dúvida registral estão disponíveis na consulta de julgados e se o PDF abre sem verificação de segurança. Enquanto não for testado, não é fonte.",
  "acesso":"Pendente de teste. Se houver verificação de segurança (CAPTCHA), o acesso não é automatizado.",
  "prova":"",
  "alinea":"Não utilizado. A aba Acórdãos publicados avisa, em cada texto, que mostra o acórdão como publicado, não o inteiro teor"},
 {"cls":"6","st":"encerrado em 22/07/2025","stc":"enc","nome":"DJe antigo — Caderno 1 Administrativo",
  "secoes":["dje.tjsp.jus.br/cdje"],
  "onde":"O antigo Diário da Justiça Eletrônico do TJSP. O Caderno 1 — Administrativo foi extinto e a última edição é a de 22/07/2025; no dia seguinte o DEJESP (fonte 2) tomou o lugar.",
  "traz":"Só o acervo até 22/07/2025.",
  "nao":"A consulta por data devolve sempre 22/07/2025, qualquer que seja a data pedida. Não é bloqueio nem defeito: é a última edição que existe.",
  "acesso":"Consulta pública; serve apenas para atos anteriores a 23/07/2025.",
  "prova":"Conferido em 22/10/2026 pedindo várias datas de 2026 — todas devolveram 22/07/2025.",
  "alinea":"Fonte histórica. Não entra na varredura diária"},
 {"cls":"7","st":"não utilizável","stc":"enc","nome":"DOE-SP — Diário Oficial do Estado",
  "secoes":["do-api-web-search.doe.sp.gov.br"],
  "onde":"O Diário Oficial do Estado de São Paulo, da Imprensa Oficial. Os atos do Judiciário paulista não saem nele — saem no DEJESP.",
  "traz":"Nada do que interessa à varredura: a consulta respondeu com o envelope correto e totalItems igual a zero em todas as tentativas.",
  "nao":"Não traz atos da Corregedoria nem acórdãos do Conselho Superior.",
  "acesso":"Consulta pública testada em 22/10/2026.",
  "prova":"Todas as buscas devolveram zero resultados.",
  "alinea":"Descartado"},
 {"cls":"8","st":"assinatura encerrada em 26/10/2026","stc":"enc","nome":"INR Publicações — Classificador INR SP",
  "secoes":["serviço pago","recorte do DJEN e do DEJESP","cinco classificadores"],
  "onde":"Boletim diário pago que recortava os dois diários oficiais (fontes 1 e 2) e agrupava os atos em cinco classificadores: I (CSM e Presidência), II e III (Corregedoria), III Especial (escrituras e procurações) e IV (Varas de Registros Públicos). Não produzia ato nenhum; cada item trazia a marcação da fonte de origem e da data.",
  "traz":"Trazia a seleção pronta e, nos acórdãos, trechos do inteiro teor montados à mão (com número do voto). Racionava cinco acórdãos por edição e publicava o restante nos dias seguintes — por isso, em 26/10/2026, a data de 10 acórdãos desta página voltou para a data real do DJEN.",
  "nao":"Era a única fonte com custo e com senha; sofria bloqueios por IP (“Verificação de segurança”, 22 e 23/10/2026) e dependia de sessão de assinante.",
  "acesso":"Encerrado por decisão do Oficial e da coordenação em 26/10/2026, depois de a leitura direta dos diários ter reproduzido 30 de 30 acórdãos e 32 de 32 atos da Corregedoria, com perda zero. O material do período (01/09 a 26/10/2026) está guardado como arquivo inativo, fora das páginas.",
  "prova":"Validação de 01/09 a 22/10/2026, processo por processo, contra 35 edições. O texto do DJEN é igual ou maior que o do boletim e traz “Legislação citada” e “Jurisprudência citada”, que ele cortava.",
  "alinea":"Fonte anterior do projeto. Nada do que ele produzia é usado desde 26/10/2026"},
]

HTML = r'''<title>Jurisprudência Registral</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Coluna única. Jurisprudência primeiro, registro das edições depois. Tinta sobre papel de livro. */
:root{
  --paper:#FAF9F7; --card:#FFFFFF; --sunk:#F1EFEB;
  --ink:#1A1A1C; --ink-2:#55555C; --ink-3:#8A8A93;
  --rule:#E2DFD9; --rule-2:#CFCBC3;
  --accent:#7A2230; --accent-2:#5C1A24; --accent-soft:#F6EBEC;
  --ok-bg:#E6EEE6; --ok-fg:#36603A;
  --warn-bg:#FAEEDA; --warn-fg:#7A5312;
  --info-bg:#E6EDF3; --info-fg:#2F5676;
  --mark:#F6E6A8; --mark-ink:#473A08;
  --fd:"Source Serif 4",Georgia,"Times New Roman",serif;
  --fb:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  --fm:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#15151A; --card:#1D1D23; --sunk:#25252D;
  --ink:#EDECEA; --ink-2:#AFAEB4; --ink-3:#7C7B83;
  --rule:#2E2E37; --rule-2:#3D3D47;
  --accent:#E79AA5; --accent-2:#F3C2C9; --accent-soft:#302124;
  --ok-bg:#20331F; --ok-fg:#A5CBA2;
  --warn-bg:#3A2D12; --warn-fg:#E2C083;
  --info-bg:#1E2B38; --info-fg:#A8C6E0;
  --mark:#5E5214; --mark-ink:#FAF0C4;
  color-scheme: dark;
}}
:root[data-theme="dark"]{
  --paper:#15151A; --card:#1D1D23; --sunk:#25252D;
  --ink:#EDECEA; --ink-2:#AFAEB4; --ink-3:#7C7B83;
  --rule:#2E2E37; --rule-2:#3D3D47;
  --accent:#E79AA5; --accent-2:#F3C2C9; --accent-soft:#302124;
  --ok-bg:#20331F; --ok-fg:#A5CBA2;
  --warn-bg:#3A2D12; --warn-fg:#E2C083;
  --info-bg:#1E2B38; --info-fg:#A8C6E0;
  --mark:#5E5214; --mark-ink:#FAF0C4;
  color-scheme: dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--fb);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
a{color:var(--accent)}
code{font-family:var(--fm);font-size:.85em;background:var(--sunk);padding:1px 5px;border-radius:4px}
mark{background:var(--mark);color:var(--mark-ink);border-radius:2px;padding:0 2px}
.wrap{max-width:54rem;margin:0 auto;
  padding-left:max(16px,env(safe-area-inset-left,0px));
  padding-right:max(16px,env(safe-area-inset-right,0px))}

header.top{border-bottom:1px solid var(--rule);background:var(--card)}
header.top .wrap{padding-block:30px 22px}
.serventia{font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin:0}
h1{font-family:var(--fd);font-weight:700;font-size:clamp(2rem,5.5vw,2.8rem);line-height:1.08;margin:8px 0 0;letter-spacing:-.02em;text-wrap:balance}
.lead{margin:12px 0 0;max-width:58ch;color:var(--ink-2)}
.nums{display:flex;flex-wrap:wrap;gap:6px 30px;margin-top:22px;padding-top:16px;border-top:1px solid var(--rule)}
.nums div{display:flex;flex-direction:column;min-width:0}
.nums .n{font-family:var(--fd);font-size:1.5rem;font-weight:700;line-height:1.1;font-variant-numeric:tabular-nums}
.nums .n.z{color:var(--ink-3)}
.nums .n.a{color:var(--accent)}
.nums .k{font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);font-weight:600}

nav.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:var(--card);border-bottom:1px solid var(--rule-2)}
nav.tabs .wrap{display:flex;gap:4px;padding-block:0;overflow-x:auto;scrollbar-width:none}
nav.tabs .wrap::-webkit-scrollbar{display:none}
.tab{padding:14px 14px 11px;background:none;border:none;border-bottom:3px solid transparent;cursor:pointer;
  font-size:.9rem;color:var(--ink-2);white-space:nowrap}
.tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:20;background:var(--card)}

main .wrap{padding-block:26px 64px}
.busca{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin-bottom:22px}
.busca input{flex:1 1 220px;min-width:0;padding:10px 13px;background:var(--card);border:1px solid var(--rule-2);border-radius:8px}
.busca select{padding:10px 11px;background:var(--card);border:1px solid var(--rule-2);border-radius:8px;max-width:100%}
.busca .c{margin-left:auto;font-size:.85rem;color:var(--ink-2);white-space:nowrap}
.busca .c b{color:var(--ink);font-variant-numeric:tabular-nums}

/* acórdão */
.ac{border-top:1px solid var(--rule);padding:0}
.ac:last-of-type{border-bottom:1px solid var(--rule)}
.ac-h{width:100%;display:grid;gap:5px;padding:20px 2px;background:none;border:none;text-align:left;cursor:pointer}
.ac-h:hover{background:var(--sunk)}
.ac-meta{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;font-size:.78rem}
.ac-data{font-variant-numeric:tabular-nums;color:var(--ink-3);letter-spacing:.03em}
.ac-com{letter-spacing:.09em;text-transform:uppercase;color:var(--accent);font-weight:600}
.ac-num{font-family:var(--fm);font-size:.74rem;color:var(--ink-3);overflow-wrap:anywhere}
.ac-tit{font-family:var(--fd);font-size:1.18rem;font-weight:600;line-height:1.3;margin:0;max-width:46ch;text-wrap:pretty}
.ac[data-open="0"] .ac-b{display:none}
.ac-b{padding:0 2px 26px}
.tema{font-family:var(--fd);font-weight:700;font-size:1rem;line-height:1.35;margin:0 0 14px;max-width:52ch;
  padding-left:14px;border-left:3px solid var(--accent)}
.corpo p{margin:0 0 12px;color:var(--ink-2);max-width:62ch}
.bloco{margin-top:16px;padding:14px 16px;border-radius:9px;max-width:62ch}
.bloco .lbl{font-size:.63rem;letter-spacing:.13em;text-transform:uppercase;font-weight:700;display:block;margin-bottom:7px}
.b-or{background:var(--accent-soft)}
.b-or .lbl{color:var(--accent)}
.b-or ul{margin:0;padding-left:1.1rem}
.b-or li{margin-bottom:6px;color:var(--ink-2)}
.b-or li:last-child{margin-bottom:0}
.b-or p{margin:0;color:var(--ink-2)}
.b-at{background:var(--warn-bg)}
.b-at .lbl{color:var(--warn-fg)}
.b-at p{margin:0;color:var(--warn-fg)}
.acoes{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;align-items:center}
.bt{padding:7px 13px;border-radius:7px;border:1px solid var(--rule-2);background:var(--card);cursor:pointer;font-size:.84rem}
.bt:hover{border-color:var(--accent);color:var(--accent)}
.bt[data-done="1"]{background:var(--ok-bg);border-color:var(--ok-fg);color:var(--ok-fg)}
.integra{display:none;white-space:pre-wrap;font-size:.9rem;line-height:1.65;color:var(--ink-2);max-width:66ch;
  max-height:26rem;overflow:auto;margin-top:14px;padding:16px 18px;background:var(--sunk);border-radius:9px}
.integra.on{display:block}
.parc{margin:0 0 10px;font-size:.8rem;color:var(--warn-fg);background:var(--warn-bg);padding:8px 11px;border-radius:7px}

/* edições */
.ed{border-top:1px solid var(--rule)}
.ed:last-of-type{border-bottom:1px solid var(--rule)}
.ed-h{width:100%;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;padding:14px 2px;background:none;border:none;text-align:left;cursor:pointer}
.ed-h:hover{background:var(--sunk)}
.ed-d{font-family:var(--fd);font-weight:600;font-size:1.05rem;font-variant-numeric:tabular-nums}
.ed-w{font-size:.8rem;color:var(--ink-3)}
.ed-t{margin-left:auto;display:flex;flex-wrap:wrap;gap:5px}
.pill{font-size:.69rem;font-weight:600;padding:2px 9px;border-radius:999px;white-space:nowrap}
.p-n{background:var(--sunk);color:var(--ink-2)}
.p-c{background:var(--info-bg);color:var(--info-fg)}
.p-z{background:var(--sunk);color:var(--ink-3)}
.p-w{background:var(--warn-bg);color:var(--warn-fg)}
.ed[data-open="0"] .ed-b{display:none}
.ed-b{padding:2px 2px 22px}
.nota{margin:0 0 12px;font-size:.84rem;line-height:1.55;color:var(--ink-3)}
.nota.w{color:var(--warn-fg);background:var(--warn-bg);padding:10px 13px;border-radius:8px}
.arv{font-size:.9rem}
.a0{font-weight:700;font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;color:var(--accent);margin-top:16px;padding-top:10px;border-top:1px solid var(--rule)}
.arv > div:first-child{margin-top:0;padding-top:0;border-top:none}
.a1{padding-left:14px;color:var(--ink-2);font-size:.86rem;margin-top:8px}
.a2{padding-left:28px;color:var(--ink-3);font-size:.78rem;letter-spacing:.05em;font-weight:600;margin-top:6px}
.a3{padding-left:42px;font-size:.88rem;padding-block:2px}

/* origem */
.org{border-top:1px solid var(--rule);padding:20px 0}
.org:first-of-type{border-top:none}
.org-t{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline;margin-bottom:8px}
.org-c{font-family:var(--fd);font-size:1.5rem;font-weight:700;color:var(--accent);line-height:1}
.org-n{font-family:var(--fd);font-size:1.05rem;font-weight:600}
.org p{margin:0 0 10px;color:var(--ink-2);max-width:64ch}
.secs{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.sec-pill{font-family:var(--fm);font-size:.74rem;padding:3px 9px;border-radius:6px;background:var(--sunk);color:var(--ink-2)}
.al{font-size:.86rem;color:var(--ink-3)}
.st{font-family:var(--fm);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:999px;border:1px solid var(--rule);color:var(--ink-2)}
.st.ok{background:var(--accent);color:#fff;border-color:var(--accent)}
.st.meio{background:var(--sunk)}
.st.fora{color:var(--ink-3)}
.st.enc{text-decoration:line-through;color:var(--ink-3)}
.org dl{margin:10px 0 0;display:grid;grid-template-columns:minmax(90px,max-content) 1fr;gap:6px 14px;font-size:.92rem}
.org dt{font-family:var(--fm);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);padding-top:3px}
.org dd{margin:0;min-width:0}
@media (max-width:520px){.org dl{grid-template-columns:1fr}.org dt{padding-top:6px}}
.prova{font-size:.88rem;border-left:2px solid var(--accent);padding:2px 0 2px 12px;margin:10px 0 !important}
.prova b{font-family:var(--fm);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);display:block;margin-bottom:3px;font-weight:500}
.prosa h2{font-family:var(--fd);font-size:1.45rem;margin:0 0 6px;font-weight:700}
.prosa .sub{margin:0 0 20px;color:var(--ink-3);font-size:.92rem}
.prosa h3{font-size:.68rem;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);margin:26px 0 8px;font-weight:700}
.prosa p{margin:0 0 11px;color:var(--ink-2);max-width:64ch}
.prosa ul{margin:0 0 11px;padding-left:1.15rem}
.prosa li{margin-bottom:6px;color:var(--ink-2);max-width:62ch}
.in{border-top:1px solid var(--rule);padding:22px 2px}
.in:first-child{border-top:none}
.in-full{font-family:var(--fd);font-size:1rem;line-height:1.68;white-space:pre-wrap;color:var(--ink);max-width:66ch;margin:10px 0 0}
.in-fonte{font-size:.8rem;color:var(--ink-3);margin:10px 0 0}
.in-fonte a{color:var(--accent)}
.vazio{padding:40px 18px;text-align:center;color:var(--ink-2)}
.vazio b{display:block;font-family:var(--fd);font-size:1.15rem;color:var(--ink);margin-bottom:6px}
[hidden]{display:none!important}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
</style>

<header class="top">
  <div class="wrap">
    <p class="serventia">Registro de Imóveis, Títulos e Documentos e Civil de Pessoas Jurídicas — Assis/SP</p>
    <h1>Jurisprudência Registral</h1>
    <p class="lead">O que o Conselho Superior da Magistratura decidiu, lido e resumido para a qualificação. Cada acórdão traz a data em que saiu no Diário de Justiça Eletrônico Nacional. Abaixo, o registro dos dias varridos.</p>
    <div class="nums" id="nums"></div>
  </div>
</header>

<nav class="tabs" aria-label="Seções">
  <div class="wrap">
    <button class="tab" id="t-ac" type="button" role="tab" aria-selected="true">Decisões do CSM</button>
    <button class="tab" id="t-in" type="button" role="tab" aria-selected="false">Acórdãos publicados</button>
    <button class="tab" id="t-ed" type="button" role="tab" aria-selected="false">Dias varridos</button>
    <button class="tab" id="t-or" type="button" role="tab" aria-selected="false">De onde vem</button>
  </div>
</nav>

<main>
  <div class="wrap">

    <section id="p-ac">
      <div class="busca">
        <input id="q" type="search" placeholder="Buscar tema, comarca, processo, texto…" autocomplete="off">
        <select id="f-com" aria-label="Comarca"></select>
        <span class="c" id="c-ac"></span>
      </div>
      <div id="lista-ac"></div>
    </section>

    <section id="p-in" hidden>
      <div class="busca">
        <input id="q-in" type="search" placeholder="Buscar no texto publicado: comarca, processo, palavra…" autocomplete="off">
        <span class="c" id="c-in"></span>
      </div>
      <div id="lista-in"></div>
    </section>

    <section id="p-ed" hidden>
      <div class="busca"><span class="c" id="c-ed"></span></div>
      <div id="lista-ed"></div>
    </section>

    <section id="p-or" hidden class="prosa">
      <h2>De onde vem a informação</h2>
      <p class="sub">Mapa das fontes do projeto, atualizado em 02/11/2026: as duas em uso, as que são lidas só para ciência, as que ficaram fora da triagem e as encerradas. Tudo o que está nesta página vem de diário oficial aberto, sem senha; conferido ato por ato, pelo número do processo, em 22/10/2026, e em uso como fonte única desde 26/10/2026.</p>

      <h3>As duas fontes, e o que cada uma tem</h3>
      <p><b>DJEN</b> — Diário de Justiça Eletrônico Nacional, do Conselho Nacional de Justiça, em <code>comunica.pje.jus.br</code>. Daí vêm os <b>acórdãos do Conselho Superior da Magistratura</b>: o Tribunal de Justiça de São Paulo publica cada um no órgão “Intimação de Acordãos”, com partes, relator, resultado e a <b>ementa inteira</b>. É o texto da aba Acórdãos publicados — o acórdão como publicado, não o inteiro teor: relatório e voto não saem no diário e ficam nos autos. A data mostrada em cada acórdão é a data dessa publicação.</p>
      <p><b>DEJESP</b> — Diário Eletrônico da Justiça do Estado de São Paulo, em <code>tjsp.jus.br/dejesp</code>. Entrou no ar em <b>23/07/2025</b> e substituiu o Caderno 1 — Administrativo do antigo DJe. É onde a <b>Corregedoria Geral</b> e a Presidência publicam: processos CG, comunicados CG, portarias, correições e designações de corregedores permanentes.</p>
      <p>As duas não se sobrepõem: os atos da Corregedoria <b>não</b> estão no DJEN, e os acórdãos do Conselho Superior <b>não</b> estão no DEJESP. Quem quiser a informação completa tem de ler as duas — e é o que a varredura diária faz.</p>

      <h3>O antigo diário acabou</h3>
      <p>A busca do antigo DJe devolve sempre <b>22/07/2025</b>, qualquer que seja a data pedida. Não é bloqueio nem defeito: <b>22/07/2025 é a última edição que existe.</b> No dia seguinte o Caderno 1 foi extinto e o DEJESP tomou o lugar.</p>

      <h3>Como a leitura direta foi conferida</h3>
      <p>Antes de virar fonte única, a leitura direta dos dois diários foi testada contra 35 edições de um serviço de curadoria pago, de 01/09 a 22/10/2026, acórdão por acórdão, pelo número do processo. Acórdãos do Conselho Superior: <b>30 de 30</b> recuperados. Atos da Corregedoria Geral, em três edições: <b>32 de 32</b>. Perda zero nos dois. O texto do DJEN é igual ou maior que o do serviço, e traz “Legislação citada” e “Jurisprudência citada”, que ele cortava. E chega antes: o serviço racionava cinco acórdãos por edição e empurrava o resto para os dias seguintes — por isso a data de alguns acórdãos nesta página mudou para trás em 26/10/2026, quando passaram a carregar a data do próprio diário.</p>

      <h3>O mapa, fonte por fonte</h3>
      <p>Oito fontes foram examinadas. Duas sustentam a página (1 e 2); uma é lida só para ciência (3); uma ficou fora da triagem por decisão (4); uma não está em diário nenhum (5); três estão encerradas ou descartadas (6, 7 e 8). Em cada bloco: onde fica, o que traz, o que não traz, como se consulta, o ritmo de publicação e como foi conferido.</p>
      <div id="origem"></div>

      <h3>O que não está aqui</h3>
      <p>As decisões de primeira instância das Varas de Registros Públicos da Capital ficam fora da triagem, por decisão de 22/10/2026. São decisões do juiz corregedor permanente da Capital, que valem para as serventias da Capital: não vinculam outra comarca e não são precedente. O que for relevante sobe por apelação e aparece como acórdão do Conselho Superior — ou seja, chega aqui de todo jeito.</p>

      <h3>Ressalva</h3>
      <p>As sínteses e as orientações práticas são leitura dos acórdãos, não texto oficial. Para citar em processo ou em nota de devolução, use o inteiro teor na fonte: o número do processo está em cada item e o botão “Ver no DJEN” abre a consulta oficial.</p>
    </section>

  </div>
</main>

<script>
const D = __DATA__;
const AC = D.acordaos, DIAS = D.dias, ORIGEM = D.origem;
const $ = s => document.querySelector(s);
const esc = s => String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const lista = v => Array.isArray(v) ? v : (v==null?[]:[v]);
const norm = s => String(s==null?"":s).normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
const tit = s => s ? s[0]+s.slice(1).toLowerCase() : s;
const semTag = s => String(s||"").replace(/<[^>]+>/g,"");

AC.forEach(a => a._b = norm([a.num,a.com,a.titulo,a.resumo&&a.resumo.tema,
  a.resumo&&lista(a.resumo.corpo).join(" "), a.resumo&&lista(a.resumo.orientacao).join(" "),
  a.resumo&&a.resumo.atencao, a.integra].filter(Boolean).join("  ")));

let F={q:"",com:""}, abAc=new Set(), abEd=new Set(), aba="ac";
try{const s=localStorage.getItem("jr.f"); if(s) F=Object.assign(F,JSON.parse(s));}catch(e){}
const salva=()=>{try{localStorage.setItem("jr.f",JSON.stringify(F));}catch(e){}};

$("#f-com").innerHTML='<option value="">Todas as comarcas</option>'+
  [...new Set(AC.map(a=>a.com))].sort((a,b)=>a.localeCompare(b,"pt-BR"))
   .map(c=>'<option value="'+esc(c)+'"'+(c===F.com?" selected":"")+'>'+esc(tit(c))+'</option>').join("");
$("#q").value=F.q;

function marca(t,q){
  if(!q) return esc(t);
  const a=String(t==null?"":t), n=norm(a), nq=norm(q);
  let o="",i=0;
  while(true){const j=n.indexOf(nq,i); if(j<0){o+=esc(a.slice(i));break;}
    o+=esc(a.slice(i,j))+"<mark>"+esc(a.slice(j,j+nq.length))+"</mark>"; i=j+nq.length;}
  return o;
}

function copiaTexto(a){
  const r=a.resumo;
  let t=r.tema+"\n\n"+lista(r.corpo).join("\n\n");
  if(r.orientacao) t+="\n\nOrientação prática:\n"+lista(r.orientacao).map(x=>"• "+semTag(x)).join("\n");
  if(r.atencao) t+="\n\nPonto de atenção: "+r.atencao;
  t+="\n\nCSM/SP – "+a.num+" – "+tit(a.com)+" – DJEN de "+a.ed+".";
  return t;
}

function renderAc(){
  const q=F.q.trim();
  const vis=AC.map((a,i)=>({a,i})).filter(x=>(!F.com||x.a.com===F.com)&&(!q||x.a._b.includes(norm(q))));
  $("#c-ac").innerHTML = (F.com||q) ? '<b>'+vis.length+'</b> de '+AC.length : '<b>'+AC.length+'</b> acórdãos';
  if(!vis.length){
    $("#lista-ac").innerHTML='<div class="vazio"><b>Nenhum acórdão com esse filtro.</b>São '+AC.length+' decisões, de 21 comarcas.</div>';
    return;
  }
  $("#lista-ac").innerHTML = vis.map(x=>{
    const a=x.a, ab=abAc.has(x.i), r=a.resumo;
    return '<article class="ac" data-open="'+(ab?1:0)+'">'
      +'<button class="ac-h" type="button" data-ac="'+x.i+'" aria-expanded="'+ab+'">'
      +'<span class="ac-meta"><span class="ac-com">'+marca(tit(a.com),q)+'</span>'
      +'<span class="ac-data">'+a.ed+'</span><span class="ac-num">'+marca(a.num,q)+'</span></span>'
      +'<h3 class="ac-tit">'+marca(a.titulo,q)+'</h3>'
      +'</button>'
      +(ab?('<div class="ac-b">'
        +'<p class="tema">'+marca(r.tema,q)+'</p>'
        +'<div class="corpo">'+lista(r.corpo).map(p=>'<p>'+marca(p,q)+'</p>').join("")+'</div>'
        +(r.orientacao?('<div class="bloco b-or"><span class="lbl">Orientação prática</span>'
            +(Array.isArray(r.orientacao)?'<ul>'+r.orientacao.map(o=>'<li>'+marca(semTag(o),q)+'</li>').join("")+'</ul>'
                                         :'<p>'+marca(semTag(r.orientacao),q)+'</p>')+'</div>'):'')
        +(r.atencao?('<div class="bloco b-at"><span class="lbl">Ponto de atenção</span><p>'+marca(r.atencao,q)+'</p></div>'):'')
        +'<div class="acoes">'
        +'<button class="bt" type="button" data-cp="'+x.i+'">Copiar resumo</button>'
        +'<button class="bt" type="button" data-in="'+x.i+'">Ver texto publicado</button>'
        +(a.fonteUrl?'<a class="bt" href="'+esc(a.fonteUrl)+'" target="_blank" rel="noopener">Ver no DJEN</a>':'')
        +'</div>'
        +'<div class="integra" id="int-'+x.i+'">'
        +'<p class="parc">Publicação do acórdão no DJEN: partes, relator, resultado do julgamento e ementa. O inteiro teor — relatório e voto — não é publicado no diário e está nos autos.</p>'
        +marca(a.integra,q)+'</div>'
        +'</div>'):'')
      +'</article>';
  }).join("");
  liga();
}

function renderEd(){
  const varridos=DIAS.filter(d=>!d.sem).length;
  $("#c-ed").innerHTML='<b>'+varridos+'</b> dias varridos · '+DIAS.reduce((s,d)=>s+(d.nac||0),0)+' acórdãos do CSM';
  $("#lista-ed").innerHTML = DIAS.map((d,i)=>{
    return '<article class="ed" data-open="0">'
      +'<div class="ed-h" style="cursor:default">'
      +'<span class="ed-d">'+d.d+'</span><span class="ed-w">'+esc(d.wd||"")+'</span>'
      +'<span class="ed-t">'
      +(d.sem?'<span class="pill p-w">sem edição</span>'
             :'<span class="pill p-n">'+esc(d.fonte||"DJEN")+'</span>'
              +(d.nac?'<span class="pill p-c">'+d.nac+(d.nac===1?' acórdão':' acórdãos')+'</span>':'<span class="pill p-z">sem acórdão</span>'))
      +'</span></div>'
      +(d.sem?'<div class="ed-b"><p class="nota w">'+esc(d.sem)+'</p></div>':'')
      +'</article>';
  }).join("");
}

function liga(){
  document.querySelectorAll("[data-ac]").forEach(b=>b.addEventListener("click",()=>{
    const i=+b.dataset.ac; abAc.has(i)?abAc.delete(i):abAc.add(i); renderAc();
  }));
  document.querySelectorAll("[data-ed]").forEach(b=>b.addEventListener("click",()=>{
    const i=+b.dataset.ed; abEd.has(i)?abEd.delete(i):abEd.add(i); renderEd();
  }));
  document.querySelectorAll("[data-in]").forEach(b=>b.addEventListener("click",e=>{
    e.stopPropagation();
    const el=$("#int-"+b.dataset.in); const on=el.classList.toggle("on");
    b.textContent=on?"Ocultar texto publicado":"Ver texto publicado";
  }));
  document.querySelectorAll("[data-cp]").forEach(b=>b.addEventListener("click",async e=>{
    e.stopPropagation();
    const a=AC[+b.dataset.cp], rot=b.textContent;
    try{ await navigator.clipboard.writeText(copiaTexto(a)); b.textContent="Copiado"; b.dataset.done="1"; }
    catch(err){
      const t=b.closest(".ac-b").querySelector(".tema");
      if(t){const r=document.createRange();r.selectNodeContents(t);
        const s=getSelection();s.removeAllRanges();s.addRange(r);}
      b.textContent="Selecionado — Cmd+C";
    }
    setTimeout(()=>{b.textContent=rot;delete b.dataset.done;},2000);
  }));
}

$("#nums").innerHTML =
   '<div><span class="n a">'+AC.length+'</span><span class="k">Acórdãos do CSM</span></div>'
 + '<div><span class="n">'+DIAS.filter(d=>!d.sem).length+'</span><span class="k">Dias varridos</span></div>'
 + '<div><span class="n">'+[...new Set(AC.map(a=>a.com))].length+'</span><span class="k">Comarcas</span></div>'
 + '<div><span class="n z">0</span><span class="k">Citações de Assis</span></div>'
 + '<div><span class="n">'+(DIAS.length?DIAS[DIAS.length-1].d.slice(0,5)+'–'+DIAS[0].d.slice(0,5):'—')+'</span><span class="k">Período</span></div>';

$("#origem").innerHTML = ORIGEM.map(o=>
  '<div class="org"><div class="org-t"><span class="org-c">'+esc(o.cls)+'</span>'
  +'<span class="org-n">'+esc(o.nome)+'</span><span class="st '+esc(o.stc)+'">'+esc(o.st)+'</span></div>'
  +'<p>'+esc(o.onde)+'</p>'
  +'<div class="secs">'+o.secoes.map(s=>'<span class="sec-pill">'+esc(s)+'</span>').join("")+'</div>'
  +'<dl>'
  +(o.traz?'<dt>O que traz</dt><dd>'+esc(o.traz)+'</dd>':'')
  +(o.nao?'<dt>O que não traz</dt><dd>'+esc(o.nao)+'</dd>':'')
  +(o.acesso?'<dt>Como se consulta</dt><dd>'+esc(o.acesso)+'</dd>':'')
  +(o.ritmo?'<dt>Ritmo</dt><dd>'+esc(o.ritmo)+'</dd>':'')
  +'</dl>'
  +(o.prova?'<p class="prova"><b>Como foi conferido</b>'+esc(o.prova)+'</p>':'')
  +'<p class="al">'+o.alinea+'.</p></div>').join("");

function renderIn(){
  const q=($("#q-in").value||"").trim();
  const vis=AC.filter(a=>!q||norm((a.com||"")+" "+(a.num||"")+" "+(a.titulo||"")+" "+(a.integra||"")).includes(norm(q)));
  $("#c-in").innerHTML = q ? '<b>'+vis.length+'</b> de '+AC.length : '<b>'+AC.length+'</b> acórdãos como publicados no DJEN — partes, relator, resultado e ementa; o inteiro teor (relatório e voto) não sai no diário';
  $("#lista-in").innerHTML = vis.length ? vis.map(a=>'<article class="in">'
      +'<span class="ac-meta"><span class="ac-com">'+esc(tit(a.com))+'</span>'
      +'<span class="ac-data">'+esc(a.ed)+'</span><span class="ac-num">'+esc(a.num)+'</span></span>'
      +'<h3 class="ac-tit">'+marca(a.titulo,q)+'</h3>'
      +'<div class="in-full">'+marca(a.integra||"Texto não disponível.",q)+'</div>'
      +(a.fonteUrl?'<p class="in-fonte">Fonte oficial: <a href="'+esc(a.fonteUrl)+'" target="_blank" rel="noopener">'+esc(a.fonte||"DJEN")+'</a></p>':'')
      +'</article>').join("")
    : '<div class="vazio"><b>Nada encontrado.</b>Tente outra palavra.</div>';
}
$("#q-in").addEventListener("input",renderIn);

const abas={ac:["#t-ac","#p-ac"],in:["#t-in","#p-in"],ed:["#t-ed","#p-ed"],or:["#t-or","#p-or"]};
function vai(k){
  aba=k;
  Object.entries(abas).forEach(([n,[t,p]])=>{
    $(t).setAttribute("aria-selected",String(n===k));
    $(p).hidden = n!==k;
  });
  if(k==="ed") renderEd();
  if(k==="in") renderIn();
}
Object.keys(abas).forEach(k=>$(abas[k][0]).addEventListener("click",()=>vai(k)));
$("#q").addEventListener("input",e=>{F.q=e.target.value;salva();renderAc();});
$("#f-com").addEventListener("change",e=>{F.com=e.target.value;salva();renderAc();});

renderAc();
</script>
'''

D["origem"] = ORIGEM
out = HTML.replace('__DATA__', json.dumps(D, ensure_ascii=False))
open(SAIDA,'w',encoding='utf-8').write(out)
print('bytes:', len(out.encode('utf-8')))

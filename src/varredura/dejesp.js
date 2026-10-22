// Varredura do DEJESP — Diário Eletrônico da Justiça do Estado de São Paulo.
// Entrou no ar em 23/07/2025 e substituiu o Caderno 1 (Administrativo) do
// antigo DJe, cuja última edição é 22/07/2025. É por isso que a busca do DJe
// devolvia sempre aquela data: não era bloqueio, a publicação acabou ali.
//
// Fonte dos Classificadores II e III (Corregedoria Geral) e dos atos da
// Presidência/SEMA que compõem parte do Classificador I.
// Roda no navegador. A API NÃO responde de fora (403 no proxy do contêiner).

export const BASE = 'https://www.tjsp.jus.br/atcapi/dje/v1/';
export const CADERNO_ADMINISTRATIVO = 10;

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function req(url, opts, tentativas = 4) {
  for (let k = 0; k < tentativas; k++) {
    try {
      const r = await fetch(url, opts);
      if (r.ok && /json/i.test(r.headers.get('content-type') || '')) return await r.json();
    } catch (_) { /* tenta de novo */ }
    await sleep(900 * (k + 1));
  }
  return null;
}

// Data em AAAA-MM-DD. O formato dd/mm/aaaa é rejeitado com 400.
export async function edicaoDoDia(dataISO) {
  const j = await req(`${BASE}caderno/descricoes/pesquisa-avancada`
    + `?dataInicio=${dataISO}&dataFim=${dataISO}&diarioFuturo=false`);
  const c = (j || [])[0];
  if (!c || !c.edicoes?.length) return null;
  const e = c.edicoes[0];
  return {
    idCaderno: c.idCaderno, descricao: c.descricao, descricaoCaderno: c.descricao,
    idVolume: e.idVolume, idEdicao: e.idEdicao, v2: e.v2,
    diarioFuturo: false, edicoes: c.edicoes,
  };
}

export async function secoes(cad) {
  return await req(`${BASE}caderno/descricoes/secoes`
    + `?idCaderno=${cad.idCaderno}&idVolume=${cad.idVolume}`
    + `&idEdicao=${cad.idEdicao}&v2=${cad.v2}&diarioFuturo=false`) || [];
}

export async function paginas(cad, dataISO, { palavrasChave = '', skip = 0, take = 10 } = {}) {
  const j = await req(`${BASE}caderno/paginado/pesquisa-avancada`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dataInicio: dataISO, dataFim: dataISO, palavrasChave, skip, take, caderno: cad }),
  });
  return { total: j?.totalElementos ?? null, dados: j?.dados || [] };
}

// Padrões dos atos da Corregedoria. O `PJECOR` entra NO MEIO do padrão
// ("PROCESSO PJECOR Nº"); sem o grupo opcional perdem-se os atos do Dicoge 3.1
// — foram 8 em 20/10/2026.
const PADRAO_ATO = /(PROCESSO\s+(?:PJECOR\s+)?N[ºO°]\s*[\d.\-\/]{10,34}|COMUNICADO\s+CG\s+N[ºO°]\s*[\d.\/]+|CORREI[ÇC][ÃA]O(?:\s+GERAL)?\s+ORDIN[ÁA]RIA|CORREGEDORES\s+PERMANENTES|PORTARIA\s+n[ºO°]\s*[\d.\/]+)/gi;

// Classificadores II e III de um dia.
// Usa as PÁGINAS DAS SEÇÕES Dicoge. Nunca tentar adivinhar a faixa da
// Subseção III: em 20/10/2026 a heurística de fim de faixa falhou e leu 72
// páginas em vez de 7.
export async function corregedoriaDoDia(dataISO) {
  const cad = await edicaoDoDia(dataISO);
  if (!cad) return { semEdicao: true };
  const secs = await secoes(cad);
  const dic = secs
    .map(s => ({ nome: s.descricaoSecao || s.descricao || '', pagina: s.pagina }))
    .filter(s => /^Dicoge/i.test(s.nome));
  if (!dic.length) return { idEdicao: cad.idEdicao, secoesDicoge: [], atos: [] };

  const nums = dic.map(s => s.pagina).filter(n => n != null);
  const ini = Math.min(...nums), fim = Math.max(...nums) + 3;
  const { dados } = await paginas(cad, dataISO, { skip: ini - 1, take: fim - ini + 1 });
  const txt = dados.map(p => p.texto).join('\n');

  const cont = {};
  (txt.match(PADRAO_ATO) || [])
    .map(x => x.replace(/\s+/g, ' ').trim().toUpperCase())
    .forEach(a => { cont[a] = (cont[a] || 0) + 1; });

  return {
    idEdicao: cad.idEdicao,
    secoesDicoge: dic,
    paginasLidas: dados.map(p => p.id),
    atos: Object.entries(cont).map(([ato, vezes]) => ({ ato, vezes })),
    // O INR descarta o bloco JUDICIAL (Dicoge 2). Nós também.
    textoBruto: txt,
  };
}

// Filtro 1 — Assis.
// Escopo decidido pela Raquel em 22/10/2026: SÓ matéria extrajudicial. Não
// varrer a edição inteira. Ficam fora movimentação de magistrados, obras do
// fórum e atos de servidores da comarca — que existem no DEJESP e o INR não
// mostra.
//
// NUNCA usar palavrasChave:"Comarca de Assis": a busca é OU entre as palavras
// e devolveu 4.930 páginas no período testado, praticamente a edição inteira.
const FALSO_POSITIVO = /assist(e|i|ê|e-)|assistência|assistida|assistindo|assiste-lhes/i;

export function ocorrenciasAssis(texto, janela = 90) {
  const t = String(texto || '').replace(/\s+/g, ' ');
  const re = new RegExp(`.{0,${janela}}Assis.{0,${janela}}`, 'gi');
  return (t.match(re) || []).map(trecho => ({
    trecho,
    provavelFalsoPositivo: FALSO_POSITIVO.test(trecho),
    // Sobrenome e citação bibliográfica também não contam. A conferência final
    // é humana: só vale quando se refere à COMARCA de Assis.
    precisaConferir: true,
  }));
}

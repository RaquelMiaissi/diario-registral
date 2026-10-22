// Varredura do DJEN — Diário de Justiça Eletrônico Nacional (CNJ).
// Fonte dos acórdãos do CSM/SP e dos atos das Varas de Registros Públicos da Capital.
//
// Levantado e conferido em 22/10/2026 contra 35 edições do INR (01/09 a 22/10/2026).
// Roda no navegador. A API NÃO responde de fora (403 no proxy do contêiner).

export const API = 'https://comunicaapi.pje.jus.br/api/v1/comunicacao';

export const ORGAOS = {
  // Contém EXATAMENTE os acórdãos registrais do CSM. 30 de 30 conferidos,
  // sem perda e sem sobra. Não precisa de filtro nenhum além do órgão.
  acordaosCSM: 92345,
  // Classificador IV. Fora da triagem por decisão da Raquel em 22/10/2026.
  vara1RegistrosPublicos: 93296,
  vara2RegistrosPublicos: 93416,
};

const sleep = ms => new Promise(r => setTimeout(r, ms));

// A API devolve HTML em vez de JSON quando o ritmo aperta. Sempre conferir o
// content-type: sem isso, o JSON.parse estoura com "Unexpected token '<'".
async function getJSON(url, tentativas = 4) {
  for (let k = 0; k < tentativas; k++) {
    try {
      const r = await fetch(url);
      if (r.ok && /json/i.test(r.headers.get('content-type') || '')) return await r.json();
    } catch (_) { /* rede instável: tenta de novo */ }
    await sleep(900 * (k + 1));
  }
  return null;
}

// Pagina até vir menos que o tamanho da página.
// ATENÇÃO: o campo `count` da resposta MENTE — devolve o tamanho da página,
// não o total. Em 22/10/2026 a 1ª Vara declarou count:100 e tinha 233 itens.
export async function porOrgaoEData(orgaoId, dataISO, { porPagina = 100, maxPaginas = 40 } = {}) {
  const itens = [];
  for (let pagina = 1; pagina <= maxPaginas; pagina++) {
    const u = `${API}?siglaTribunal=TJSP&orgaoId=${orgaoId}`
      + `&dataDisponibilizacaoInicio=${dataISO}&dataDisponibilizacaoFim=${dataISO}`
      + `&itensPorPagina=${porPagina}&pagina=${pagina}`;
    const j = await getJSON(u);
    if (!j) break;
    const lote = j.items || [];
    itens.push(...lote);
    if (lote.length < porPagina) break;
    await sleep(350);
  }
  return itens;
}

export async function porProcesso(numeroSemPontuacao) {
  const j = await getJSON(`${API}?siglaTribunal=TJSP&numeroProcesso=${numeroSemPontuacao}&itensPorPagina=30`);
  return j?.items || [];
}

export const semTags = html => String(html || '')
  .replace(/<[^>]*>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();

// Acórdãos do CSM de um dia. Sem filtro: o órgão já é o conjunto.
export async function acordaosDoDia(dataISO) {
  const itens = await porOrgaoEData(ORGAOS.acordaosCSM, dataISO);
  return itens.map(i => {
    const t = semTags(i.texto);
    return {
      processo: i.numeroprocessocommascara || i.numero_processo,
      data: i.datadisponibilizacao,
      classe: i.nomeClasse,
      integra: t,
      // O texto do DJEN é igual ou MAIOR que o do INR e traz "Legislação
      // citada" e "Jurisprudência citada", que o INR corta.
      caracteres: t.length,
      fonte: 'DJEN — Intimação de Acordãos',
    };
  });
}

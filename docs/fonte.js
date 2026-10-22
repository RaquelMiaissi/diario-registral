// Camada de dados do site. Troca de banco sem mexer na página.
//
// Três adaptadores: `seed` (JSON no próprio repositório, funciona sem banco),
// `firestore` e `supabase`. A página chama sempre `Fonte.carregar()`.
//
// Nenhuma credencial entra neste arquivo além da chave pública do cliente,
// que não é segredo. Quem decide o acesso são as REGRAS do banco.

export const Fonte = {
  modo: 'seed',
  config: null,

  usar(modo, config = null) { this.modo = modo; this.config = config; return this; },

  async carregar() {
    switch (this.modo) {
      case 'seed':      return this._seed();
      case 'firestore': return this._firestore();
      case 'supabase':  return this._supabase();
      default: throw new Error('modo de fonte desconhecido: ' + this.modo);
    }
  },

  // Dados versionados junto com o código. Só deve conter o que é público:
  // acórdãos e atos de fonte DEJESP/DJEN. Ver dados/schema.md.
  async _seed() {
    const r = await fetch('./dados.json');
    if (!r.ok) throw new Error('não foi possível ler dados.json: ' + r.status);
    return r.json();
  },

  // Firestore pela API REST — sem SDK, para a página seguir sendo um arquivo só.
  // config: { projectId, apiKey }
  async _firestore() {
    const { projectId, apiKey } = this.config || {};
    if (!projectId) throw new Error('firestore exige projectId');
    const base = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents`;
    const chave = apiKey ? `?key=${apiKey}` : '';
    const colecao = async nome => {
      const r = await fetch(`${base}/${nome}${chave}`);
      if (!r.ok) throw new Error(`${nome}: ${r.status}`);
      const j = await r.json();
      return (j.documents || []).map(d => destravarFirestore(d.fields));
    };
    const [acordaos, edicoes] = await Promise.all([colecao('acordaos'), colecao('edicoes')]);
    return { acordaos, dias: edicoes };
  },

  // Supabase pela API REST. config: { url, anonKey }
  // A anonKey é pública por desenho; o acesso é controlado por RLS
  // (Row Level Security — segurança por linha) no próprio banco.
  async _supabase() {
    const { url, anonKey } = this.config || {};
    if (!url || !anonKey) throw new Error('supabase exige url e anonKey');
    const tabela = async nome => {
      const r = await fetch(`${url}/rest/v1/${nome}?select=*`, {
        headers: { apikey: anonKey, Authorization: `Bearer ${anonKey}` },
      });
      if (!r.ok) throw new Error(`${nome}: ${r.status}`);
      return r.json();
    };
    const [acordaos, edicoes] = await Promise.all([tabela('acordaos'), tabela('edicoes')]);
    return { acordaos, dias: edicoes };
  },
};

// O Firestore embrulha todo valor em { stringValue }, { integerValue }, etc.
function destravarFirestore(fields) {
  const saida = {};
  for (const [k, v] of Object.entries(fields || {})) saida[k] = valorFirestore(v);
  return saida;
}
function valorFirestore(v) {
  if (v == null) return null;
  if ('stringValue'  in v) return v.stringValue;
  if ('integerValue' in v) return Number(v.integerValue);
  if ('doubleValue'  in v) return v.doubleValue;
  if ('booleanValue' in v) return v.booleanValue;
  if ('timestampValue' in v) return v.timestampValue;
  if ('nullValue'    in v) return null;
  if ('arrayValue'   in v) return (v.arrayValue.values || []).map(valorFirestore);
  if ('mapValue'     in v) return destravarFirestore(v.mapValue.fields);
  return null;
}

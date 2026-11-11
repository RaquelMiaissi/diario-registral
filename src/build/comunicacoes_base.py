# -*- coding: utf-8 -*-
"""Base das comunicações obrigatórias pós-registro (pedido do Oficial Vinicius, 10/11/2026).

Fonte interna: cabeçalhos da "04 - Planilha para comunicados mensais - Campo Prefeitura.docx"
(Drive, pasta Publicações_INR). Só entram os blocos que são comunicação a terceiro com
previsão normativa; rotina interna (tabela SINDUSCON, livro protocolo) fica fora.

Origem normativa conferida em 10–11/11/2026 nas fontes oficiais indicadas em cada item.
O que não foi confirmado está em `pendencias` — não foi preenchido por suposição.

Uso:  python3 src/build/comunicacoes_base.py   -> grava docs/dados.json (chave comunicacoes)
"""
import json, sys, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, 'docs', 'dados.json')

CNN = "https://atos.cnj.jus.br/atos/detalhar/5243"
NSCGJ = "https://www.tjsp.jus.br/Corregedoria/Comunicados/NormasExtrajudiciais"
CONFERIDO = "11/11/2026"

COMUNICACOES = [
  {
    "id": "doi",
    "planilha": "2",
    "nome": "DOI — Declaração sobre Operações Imobiliárias",
    "destinatario": "Receita Federal do Brasil (sistema DOI-Web, pelo e-CAC)",
    "gatilho": "Operação de aquisição ou alienação de imóvel, qualquer que seja o valor (IN RFB 2.186/2024, art. 4º). No Registro de Imóveis, quando o título for: instrumento particular, inclusive com força de escritura pública; título judicial de adjudicação, herança, legado ou meação; alienação por iniciativa particular ou leilão judicial; título da União, estado, município ou DF em regularização fundiária ou habitação de interesse social; ou escritura de notas ou de consulado, mesmo que já tenha havido DOI (art. 4º, II, a a f). No Registro de Títulos e Documentos, quando registrar instrumento particular dessas operações (art. 4º, III).",
    "periodicidade": "Mensal",
    "prazo": "Até o último dia útil do mês subsequente ao do registro ou averbação (IN RFB 2.186/2024, art. 5º).",
    "meio": "Sistema DOI-Web, no portal gov.br, com conta gov.br prata ou ouro, restrito aos titulares ou procuradores, assinatura com certificado ICP-Brasil; uma declaração por imóvel (art. 4º, § 1º; art. 5º, §§ 1º a 3º).",
    "base": [
      {"norma": "Lei nº 10.426/2002", "disp": "art. 8º", "o_que": "Cria a obrigação de os serventuários da Justiça informarem à Receita as operações imobiliárias (fundamento da DOI).", "orgao": "União", "url": "https://www2.camara.leg.br/legin/fed/lei/2002/lei-10426-24-abril-2002-404256-normaatualizada-pl.pdf"},
      {"norma": "Instrução Normativa RFB nº 2.186/2024", "disp": "arts. 1º, 2º, 4º (incs. II e III), 5º e 10", "o_que": "Regula a DOI; art. 4º, II obriga o registro de imóveis nas hipóteses das alíneas a a f e art. 4º, III o registro de títulos e documentos; art. 5º fixa o prazo e o meio; art. 10 revoga as IN 1.112/2010, 1.193/2011 e 1.239/2012. Publicada em 16/04/2024 (retificada em 24/04/2024), vigente desde 01/06/2024; marcada como vigente e sem alteração no portal Normas da Receita em 11/11/2026.", "orgao": "Receita Federal", "url": "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/137341"},
      {"norma": "NSCGJ-SP, Capítulo XX", "disp": "itens 144, 144.1 e 137 'l'", "o_que": "O oficial comunica as operações registradas à Receita pela DOI 'de conformidade com as instruções normativas vigentes'; recibos arquivados em papel ou formato eletrônico; classificador próprio para os recibos.", "orgao": "CGJ-SP", "url": NSCGJ}
    ],
    "vigiar": ["IN RFB 2186/2024", "DOI", "Declaração sobre Operações Imobiliárias", "Lei 10.426/2002 art. 8", "NSCGJ Cap. XX item 144"],
    "pendencias": ""
  },
  {
    "id": "prefeituras",
    "planilha": "11",
    "nome": "Mudanças de titularidade às Prefeituras",
    "destinatario": "Município da situação do imóvel, por meio da plataforma do ONR (Ofício Eletrônico — Comunicação de Transações às Prefeituras)",
    "gatilho": "Mesmas hipóteses da DOI: todo ato que muda a titularidade do imóvel (compra e venda, doação, usucapião etc.).",
    "periodicidade": "Mensal",
    "prazo": "Até o último dia útil do mês subsequente à prática dos atos (CNN, art. 184-A, caput).",
    "meio": "Envio eletrônico com recibo de entrega à plataforma mantida pelo ONR (art. 184-A, § 2º, II); arquivo no formato do manual técnico do ONR (§ 6º).",
    "base": [
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 184-A, incluído pelo Prov. CN 174/2024; § 9º com redação do Prov. CN 212/2026", "o_que": "Obrigação nacional de informar aos municípios, mensalmente, todas as mudanças de titularidade, com indicação do ato que as originou (§ 3º); fornecimento sem custas ou emolumentos (§ 9º). O Prov. CN 189/2025 ajustou prazos do envio retroativo.", "orgao": "CNJ — Corregedoria Nacional", "url": CNN},
      {"norma": "Resolução CNJ nº 547/2024", "disp": "art. 4º", "o_que": "Citada no caput do art. 184-A como fundamento da atualização cadastral dos contribuintes municipais.", "orgao": "CNJ", "url": "https://atos.cnj.jus.br/atos?atos=sim&numero=547&ano=2024&argumento=&origem=&situacao=&tema="},
      {"norma": "NSCGJ-SP, Capítulo XX", "disp": "itens 139 a 141 e 137 'k'", "o_que": "Negócios imobiliários 'deverão ser sempre comunicados' às Prefeituras para atualização cadastral, por listagem diária, semanal ou mensal; eventual dispensa pela Prefeitura fica documentada em cartório (item 141).", "orgao": "CGJ-SP", "url": NSCGJ}
    ],
    "vigiar": ["art. 184-A", "Provimento 174/2024", "Provimento 189/2025", "Comunicação de Transações às Prefeituras", "Resolução 547/2024", "NSCGJ Cap. XX itens 139 a 141"],
    "pendencias": ""
  },
  {
    "id": "incra",
    "planilha": "4",
    "nome": "Comunicação mensal ao INCRA — imóveis rurais",
    "destinatario": "INCRA (Superintendência Regional de São Paulo)",
    "gatilho": "Mudança de titularidade, parcelamento, desmembramento, loteamento, remembramento/unificação, retificação de área, reserva legal, RPPN e outras limitações ambientais ou dominiais em imóvel rural, inclusive os destacados do patrimônio público.",
    "periodicidade": "Mensal",
    "prazo": "Até o 30º dia do mês subsequente à modificação (Decreto 4.449/2002, art. 4º, § 1º).",
    "meio": "Na forma fixada por ato do INCRA (Decreto 4.449/2002, art. 4º, § 1º). A IN INCRA 12/2003 (Anexo I, item 6) prevê ofício no modelo do Anexo II; a rotina do cartório usa e-mail à Superintendência.",
    "base": [
      {"norma": "Lei nº 4.947/1966", "disp": "art. 22, § 7º (redação da Lei nº 10.267/2001)", "o_que": "Os serviços de registro de imóveis ficam obrigados a encaminhar ao INCRA, mensalmente, as modificações ocorridas nas matrículas de imóveis rurais; § 8º: o INCRA devolve mensalmente os códigos dos imóveis para averbação de ofício.", "orgao": "União", "url": "https://www2.camara.leg.br/legin/fed/lei/2001/lei-10267-28-agosto-2001-391397-publicacaooriginal-1-pl.html"},
      {"norma": "Decreto nº 4.449/2002", "disp": "art. 4º, caput e § 1º; art. 6º", "o_que": "Comunicação mensal ao INCRA até o 30º dia do mês subsequente, na forma de ato normativo do INCRA; aplica-se também aos imóveis destacados do patrimônio público.", "orgao": "União", "url": "https://www2.camara.leg.br/legin/fed/decret/2002/decreto-4449-30-outubro-2002-484374-normaatualizada-pe.html"},
      {"norma": "Instrução Normativa INCRA nº 12/2003", "disp": "Anexo I, item 6, e Anexo II", "o_que": "Modelo de ofício mensal ao INCRA (ato, matrícula, código INCRA, denominação, área, município, dados do proprietário).", "orgao": "INCRA", "url": "https://www.gov.br/incra/pt-br/centrais-de-conteudos/legislacao/in_12_2003.pdf"},
      {"norma": "NSCGJ-SP, Capítulo XX", "disp": "item 137, alíneas 'p' e 'q'", "o_que": "Classificador das comunicações mensais enviadas ao INCRA e das comunicações recebidas dele (códigos para averbação).", "orgao": "CGJ-SP", "url": NSCGJ}
    ],
    "vigiar": ["Decreto 4.449/2002", "Lei 10.267/2001", "Lei 4.947/1966 art. 22", "Instrução Normativa INCRA", "comunicação mensal ao INCRA", "SIGEF", "SNCR"],
    "pendencias": "Não confirmei se a IN INCRA 12/2003 continua vigente (o portal do INCRA só foi lido por cópia de 2003); a lei e o decreto estão confirmados."
  },
  {
    "id": "estrangeiros",
    "planilha": "8",
    "nome": "Aquisição de imóvel rural por estrangeiro — comunicação trimestral",
    "destinatario": "Corregedoria Geral da Justiça (Portal do Extrajudicial) e INCRA; Conselho de Defesa Nacional quando o imóvel está em área indispensável à segurança nacional",
    "gatilho": "Aquisição de imóvel rural por pessoa física ou jurídica estrangeira (ou equiparada), ainda que inaplicáveis as restrições da Lei 5.709/71; inexistência também se comunica (negativa).",
    "periodicidade": "Trimestral (janeiro, abril, julho e outubro, relativos ao trimestre anterior)",
    "prazo": "Trimestral, 'sob pena de perda do cargo' (Lei 5.709/71, art. 11). As NSCGJ não fixam dia; a rotina interna faz no mês seguinte ao fechamento do trimestre.",
    "meio": "Cadastramento de planilhas no Portal do Extrajudicial com cópia da matrícula (NSCGJ Cap. XX, 98.2); alterações do cadastro em nome do estrangeiro: e-mail dicoge5.1@tjsp.jus.br, tão logo ocorram (98.3); ao INCRA por ofício.",
    "base": [
      {"norma": "Lei nº 5.709/1971", "disp": "arts. 10 e 11", "o_que": "Cadastro especial em livro auxiliar das aquisições por estrangeiros (art. 10) e remessa trimestral da relação à Corregedoria e ao Ministério da Agricultura (hoje INCRA), sob pena de perda do cargo (art. 11).", "orgao": "União", "url": "https://legis.senado.leg.br/norma/547582/publicacao/15773468"},
      {"norma": "Decreto nº 74.965/1974", "disp": "arts. 15 e 16", "o_que": "Regulamento da Lei 5.709/71; citado nas notas das NSCGJ como base do cadastro e da comunicação trimestral.", "orgao": "União", "url": "https://www.planalto.gov.br/ccivil_03/decreto/1970-1979/d74965.htm"},
      {"norma": "NSCGJ-SP, Capítulo XX", "disp": "itens 98 a 98.4, 100 e 137 'h' e 'i'", "o_que": "Comunicação trimestral obrigatória ao INCRA e à CGJ; comunicação negativa trimestral à CGJ (98.1); planilhas no Portal do Extrajudicial (98.2); alterações do cadastro por e-mail (98.3); Conselho de Defesa Nacional (98.4); controle das áreas por nacionalidade (100).", "orgao": "CGJ-SP", "url": NSCGJ},
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 436", "o_que": "Obrigação paralela: comunicação trimestral à CGJ e ao INCRA dos atos de arrendamento de imóvel rural por estrangeiro.", "orgao": "CNJ — Corregedoria Nacional", "url": CNN}
    ],
    "vigiar": ["Lei 5.709", "Decreto 74.965", "aquisição de imóvel rural por estrangeiro", "NSCGJ Cap. XX item 98", "CNN art. 436", "arrendamento por estrangeiro"],
    "pendencias": "Não li o Decreto 74.965/74 diretamente (o Planalto bloqueia o acesso automático); os artigos 15 e 16 vêm das notas de rodapé das NSCGJ."
  },
  {
    "id": "coaf",
    "planilha": "5",
    "nome": "Comunicações ao COAF/UIF (prevenção à lavagem de dinheiro)",
    "destinatario": "Unidade de Inteligência Financeira — COAF, pelo Siscoaf",
    "gatilho": "Comunicação automática: registro de título com declaração de pagamento em espécie ou por título ao portador de valor igual ou superior a R$ 100.000,00 (CNN, art. 161). Comunicação após análise: qualquer operação com indício de lavagem ou financiamento do terrorismo (arts. 151, I, 156 e 162).",
    "periodicidade": "Por operação; comunicação de não ocorrência anual",
    "prazo": "Automáticas: seleção em até 30 dias da operação e comunicação em 24 horas depois disso (art. 151, § 1º). Analisadas: no dia útil seguinte ao fim da análise. Não ocorrência: até 31 de janeiro do ano seguinte, à CGJ (art. 153).",
    "meio": "Siscoaf — comunicação em lote por XML exportado do sistema do RI; número do recibo guardado no sistema.",
    "base": [
      {"norma": "Lei nº 9.613/1998", "disp": "art. 9º, parágrafo único, XIII; arts. 10 e 11", "o_que": "Registros públicos são pessoas obrigadas; deveres de identificação, registro e comunicação ao COAF.", "orgao": "União", "url": "https://planalto.gov.br/ccivil_03/leis/l9613compilado.htm"},
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "arts. 137 a 181 — em especial 151, 153, 154, 156, 161 e 162 (redação do Prov. CN 161/2024, vigente desde 02/05/2024)", "o_que": "Incorpora o antigo Prov. 88/2019. Art. 161: única hipótese automática do RI hoje é pagamento em espécie/título ao portador ≥ R$ 100 mil (as hipóteses de 50% e 100% foram revogadas e viraram indícios do art. 162). Art. 153: comunicação de não ocorrência anual à CGJ. Art. 154: sigilo.", "orgao": "CNJ — Corregedoria Nacional", "url": CNN},
      {"norma": "NSCGJ-SP, Capítulo XIII, Seção IX", "disp": "itens 155 a 163 (Prov. CG 25/2026)", "o_que": "Política de PLD/FTP da serventia; 155.4 remete hipóteses, prazos e valores ao CNN; 161.2 comunicação de não ocorrência; 163 treinamento anual, preferencialmente em janeiro.", "orgao": "CGJ-SP", "url": NSCGJ}
    ],
    "vigiar": ["Provimento 88/2019", "Provimento 161/2024", "CNN art. 151", "CNN art. 161", "lavagem de dinheiro", "COAF", "UIF", "Siscoaf", "NSCGJ Cap. XIII item 155", "Resolução Coaf"],
    "pendencias": ""
  },
  {
    "id": "pep",
    "planilha": "13",
    "nome": "Relação de Pessoas Expostas Politicamente (PEP) do COAF",
    "destinatario": "Não é uma comunicação: é importação da lista do COAF para o cadastro do RI (dever de identificação)",
    "gatilho": "Todo ato com conteúdo econômico: o cadastro das partes deve registrar a condição de PEP, familiar ou estreito colaborador.",
    "periodicidade": "Mensal (rotina interna); a norma exige cadastro atualizado no momento do ato",
    "prazo": "Não há prazo fixado para a importação; o dever é manter o cadastro atual quando o ato é praticado.",
    "meio": "Download da Relação de PEP no portal do COAF com certificado do Oficial e importação no sistema (Exportações › SISCOAF › Central de Arquivo PEP).",
    "base": [
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 145, § 1º, 'k' e § 6º; art. 141 (redação do Prov. CN 161/2024)", "o_que": "Cadastro deve anotar a condição de PEP 'nos termos da norma editada a respeito pela UIF'; para o enquadramento, consultar o cadastro eletrônico de PEP pelo Siscoaf ou colher declaração das partes; atenção especial às operações com PEP.", "orgao": "CNJ — Corregedoria Nacional", "url": CNN},
      {"norma": "Resolução Coaf nº 40/2021", "disp": "íntegra", "o_que": "Define quem é pessoa exposta politicamente (citada no art. 145 do CNN).", "orgao": "COAF", "url": "https://www.gov.br/coaf/pt-br"},
      {"norma": "NSCGJ-SP, Capítulo XIII", "disp": "itens 157.1, VI e 163.2, III", "o_que": "Exposição a PEP como fator de risco e conteúdo obrigatório do treinamento.", "orgao": "CGJ-SP", "url": NSCGJ}
    ],
    "vigiar": ["pessoa exposta politicamente", "PEP", "Resolução Coaf 40", "CNN art. 145"],
    "pendencias": ""
  },
  {
    "id": "itn003",
    "planilha": "6",
    "nome": "Comunicação de atos ao ONR — ITN 003/2025 (ONR-CAD / Mapa do RI)",
    "destinatario": "ONR — Operador Nacional do Sistema de Registro Eletrônico de Imóveis (portal mapa.onr.org.br)",
    "gatilho": "Atos do mês sobre imóveis rurais (sempre) e sobre imóveis urbanos em que a União, autarquias ou fundações federais sejam parte: abertura de matrícula, transmissões, alteração de relação jurídica e alteração do imóvel.",
    "periodicidade": "Mensal",
    "prazo": "Até o último dia útil do mês seguinte; meses sem movimento exigem declaração de inexistência (exigida desde 30/06/2026).",
    "meio": "Arquivo JSON gerado no sistema do RI e enviado manualmente no Mapa do Registro de Imóveis (Incluir Atos e Dados ITN 003).",
    "base": [
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 320-O e § 1º (manual técnico do ONR); arts. 343-A a 343-C (IERI-e); art. 104; art. 329, § 3º (ITN do ONR) — incluídos pelo Prov. CN 195/2025", "o_que": "Módulos do SREI geridos pelo ONR (CNIB, Saec, IERI-e, SIG-RI); o IERI-e é a base estatística do RI e os sistemas de automação devem viabilizar seu preenchimento automático (343-B, § 2º); registradores remetem dados estatísticos anonimizados às entidades previstas em lei ou regulamento (104).", "orgao": "CNJ — Corregedoria Nacional", "url": CNN},
      {"norma": "ITN 003/2025/ONR", "disp": "íntegra", "o_que": "Instrução Técnica de Normalização que define o envio mensal dos atos ao ONR-CAD (cadastro nacional de imóveis do ONR).", "orgao": "ONR", "url": "https://mapa.onr.org.br/sigri/inicio"},
      {"norma": "Lei nº 13.465/2017", "disp": "art. 76", "o_que": "Cria o SREI e o ONR, que edita as ITNs.", "orgao": "União", "url": "https://legis.senado.leg.br/norma/17723904"}
    ],
    "vigiar": ["ITN 003", "ITN/ONR", "ONR-CAD", "Provimento 195/2025", "SIG-RI", "IERI-e", "Mapa do Registro de Imóveis", "CNN art. 320-O", "CNN art. 343"],
    "pendencias": "Não acessei o texto da ITN 003/2025 no site do ONR (bloqueado ao acesso automático). Escopo, prazo e a exigência de declaração de inexistência vêm de descrição de terceiro (blog RI-Online, 12/07/2026) e precisam ser conferidos na ITN. O artigo doutrinário (IRIB/Migalhas, 08/2026) descreve a ITN 003 como padronização dos dados territoriais (polígono georreferenciado) e a ITN 004 como modelagem da matrícula eletrônica."
  },
  {
    "id": "mapa-estatisticas",
    "planilha": "12",
    "nome": "Arquivo de estatísticas no Mapa do Registro de Imóveis (Relatório do Indicador Real)",
    "destinatario": "ONR — Mapa do Registro de Imóveis do Brasil (SIG-RI / IERI-e)",
    "gatilho": "Transações imobiliárias do mês (a planilha usa o mesmo arquivo JSON da DOI).",
    "periodicidade": "Mensal",
    "prazo": "Não localizado em norma com esse nome; ver pendências.",
    "meio": "Login com certificado do Oficial › Envio de Arquivos › Enviar Arquivo de Estatísticas (JSON).",
    "base": [
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 320-O, § 2º (Mapa como ferramenta do SIG-RI); arts. 343-A a 343-C (IERI-e) — Prov. CN 195/2025", "o_que": "O Mapa é a plataforma gráfica dos imóveis registrados; o IERI-e é a base estatística do RI mantida pelo ONR, alimentada pelos sistemas das serventias conforme manual técnico do ONR.", "orgao": "CNJ — Corregedoria Nacional", "url": CNN},
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 184-A, § 2º, II", "o_que": "Se o arquivo enviado é o mesmo da DOI, pode tratar-se da própria comunicação às prefeituras pela plataforma do ONR (ver item Prefeituras).", "orgao": "CNJ — Corregedoria Nacional", "url": CNN}
    ],
    "vigiar": ["Indicador Real", "Mapa do Registro de Imóveis", "Provimento 195/2025", "IERI-e", "manual técnico ONR"],
    "pendencias": "Não encontrei norma que use o nome 'Relatório do Indicador Real'. O Mapa é ferramenta do SIG-RI (CNN art. 320-O, § 2º, Prov. 195/2025), então a origem provável é o Prov. 195/2025 e o manual técnico do ONR (art. 320-O, § 1º); mas, como a planilha diz que o arquivo é o mesmo JSON da DOI, pode ser a remessa do art. 184-A. Fica registrado com as duas origens até o manual do ONR ser lido."
  },
  {
    "id": "arisp-estatisticas",
    "planilha": "3 e 9",
    "nome": "Informações estatísticas à ARISP / Central Registradores de Imóveis",
    "destinatario": "Central Registradores de Imóveis (ARISP); dados ficam disponíveis ao IRIB e, anonimizados, ao Banco Central",
    "gatilho": "Movimento do mês anterior: intimações de alienação fiduciária (iniciadas, purgadas, canceladas, consolidadas, valores, credor), incorporações e instituições de condomínio, loteamentos e parcelamentos, retificações de registro, usucapião extrajudicial; e dados sobre operações imobiliárias (arquivo XML das transações).",
    "periodicidade": "Mensal",
    "prazo": "Até o dia 15 de cada mês, relativos ao mês anterior (NSCGJ Cap. XX, item 414).",
    "meio": "Informação eletrônica na Central Registradores de Imóveis (sistema ARISP); XML gerado no sistema do RI para as transações.",
    "base": [
      {"norma": "NSCGJ-SP, Capítulo XX, Subseção XVI 'Das informações estatísticas'", "disp": "itens 414, 414.1, 414.2, 414.2.1 e 415 (Prov. CG 22/2019)", "o_que": "Lista os dados a informar até o dia 15; ARISP guarda e anonimiza; IRIB recebe iguais informações; Banco Central acessa dados anonimizados sobre crédito imobiliário.", "orgao": "CGJ-SP", "url": NSCGJ},
      {"norma": "Código Nacional de Normas (Prov. CN 149/2023)", "disp": "art. 104", "o_que": "Registradores remetem dados para indicadores estatísticos às entidades previstas em lei ou regulamento, anonimizados na origem (LGPD).", "orgao": "CNJ — Corregedoria Nacional", "url": CNN}
    ],
    "vigiar": ["NSCGJ Cap. XX item 414", "informações estatísticas", "Central Registradores de Imóveis", "ARISP", "Provimento CG 22/2019"],
    "pendencias": "O bloco 3 da planilha ('estatísticas de transações imobiliárias', só atos classificados como DOI) não tem item próprio nas NSCGJ atuais: a versão anterior tinha o item 406 (Prov. CG 37/2013 e Com. CG 602/2013, 'dados sobre operações imobiliárias à ARISP'), hoje absorvido nos itens 414/415."
  },
  {
    "id": "papel-seguranca",
    "planilha": "10",
    "nome": "Papel de segurança — fechamento mensal no Portal do Extrajudicial",
    "destinatario": "Corregedoria Geral da Justiça (Portal do Extrajudicial)",
    "gatilho": "Folhas de papel de segurança utilizadas e danificadas no mês; extravio ou subtração se comunica à Corregedoria Permanente tão logo ocorra.",
    "periodicidade": "Mensal",
    "prazo": "Até o último dia útil do mês subsequente (NSCGJ Cap. XX, item 157.1.12).",
    "meio": "Lançamento no Portal do Extrajudicial pelo responsável pela delegação.",
    "base": [
      {"norma": "NSCGJ-SP, Capítulo XX", "disp": "itens 157.1.6, 157.1.9, 157.1.11 e 157.1.12", "o_que": "Classificador com folhas entregues, utilizadas e estoque (157.1.6); fabricante informa as aquisições pelo Portal (157.1.9); extravio/subtração ao Corregedor Permanente (157.1.11); informe mensal de utilizados e danificados (157.1.12).", "orgao": "CGJ-SP", "url": NSCGJ},
      {"norma": "NSCGJ-SP, Capítulo XIII", "disp": "item 14.3", "o_que": "Atualizações do Portal do Extrajudicial até o último dia útil do mês subsequente, sob pena de responsabilidade; Justiça Aberta no prazo do CNJ.", "orgao": "CGJ-SP", "url": NSCGJ}
    ],
    "vigiar": ["papel de segurança", "Portal do Extrajudicial", "NSCGJ Cap. XX item 157", "NSCGJ Cap. XIII item 14.3"],
    "pendencias": ""
  }
]

# Outras obrigações de comunicação encontradas nas normas e que NÃO estão na planilha 04 — vigiadas do mesmo modo.
# (3 itens; o treinamento anual de PLD foi retirado em 11/11/2026, ver abaixo)
FORA_DA_PLANILHA = [
  {"nome": "Sistema Justiça Aberta (CNJ)", "prazo": "Mensal, até o 15º dia do mês subsequente; e semestral até o 10º dia útil de janeiro e julho (produtividade e arrecadação).", "base": "CNN, art. 136-A, § 1º (redação do Prov. CN 218/2026); NSCGJ Cap. XIII, item 14.3.", "url": CNN},
  {"nome": "Comunicação de não ocorrência ao COAF (à CGJ)", "prazo": "Anual, até 31 de janeiro do ano seguinte, quando não houve nenhuma comunicação à UIF no ano civil.", "base": "CNN, art. 153 (redação do Prov. CN 161/2024); NSCGJ Cap. XIII, item 161.2.", "url": CNN},
  {"nome": "Arrendamento de imóvel rural por estrangeiro", "prazo": "Trimestral, à CGJ e ao INCRA.", "base": "CNN, art. 436.", "url": CNN},
  # Inativo desde 11/11/2026 (pedido da Raquel: "pode retirar o treinamento") — não é comunicação a terceiro:
  # {"nome": "Treinamento anual de PLD/FTP", "prazo": "Anual, preferencialmente em janeiro.", "base": "NSCGJ Cap. XIII, item 163 (Prov. CG 25/2026).", "url": NSCGJ}
]

if __name__ == '__main__':
    d = json.load(open(DADOS, encoding='utf-8'))
    d['comunicacoes'] = COMUNICACOES
    d['comunicacoes_fora'] = FORA_DA_PLANILHA
    d['comunicacoes_conferido'] = CONFERIDO
    json.dump(d, open(DADOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('comunicacoes:', len(COMUNICACOES), '| fora da planilha:', len(FORA_DA_PLANILHA))

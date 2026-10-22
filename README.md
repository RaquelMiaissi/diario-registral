# Monitoramento do Classificador INR SP

Varredura diária das publicações oficiais de interesse do Cartório de Registro
de Imóveis, Títulos e Documentos e Civil de Pessoas Jurídicas da Comarca de
Assis/SP.

Dois filtros, decididos em 15/09/2026 e mantidos desde então:

1. **ASSIS** — qualquer ato que se refira à comarca, em matéria extrajudicial.
2. **Decisões do CSM** — acórdãos do Conselho Superior da Magistratura de São
   Paulo, de qualquer comarca, porque são o precedente que orienta a
   qualificação registral.

## De onde vêm os dados

O INR Publicações não produz ato nenhum: o Classificador INR SP é recorte de
**duas** fontes oficiais abertas, nenhuma delas com senha. Levantado e
conferido processo por processo em 22/10/2026.

| Conteúdo | Fonte | Endereço |
|---|---|---|
| Acórdãos do CSM (Classificador I) | **DJEN** — Diário de Justiça Eletrônico Nacional, do CNJ, órgão "Intimação de Acordãos" (`orgaoId` 92345) | `comunicaapi.pje.jus.br/api/v1/comunicacao` |
| Atos da Corregedoria Geral (Classificadores II e III) | **DEJESP** — Caderno 1 Administrativo, Subseção III, seções Dicoge | `tjsp.jus.br/dejesp` |
| Atos da Presidência e da SEMA (parte do Classificador I) | **DEJESP** — Caderno 1, Seção I, Subseção I | idem |
| Atos das 1ª e 2ª Varas de Registros Públicos da Capital (Classificador IV) | **DJEN**, `orgaoId` 93296 e 93416 | idem |

As duas fontes **não se sobrepõem**: os atos da Corregedoria não estão no
DJEN, e os acórdãos do CSM não estão no DEJESP. Quem quiser a informação
completa tem de ler as duas.

### O antigo DJe está morto

`dje.tjsp.jus.br/cdje` devolve sempre **22/07/2025**, qualquer que seja a data
pedida. Não é bloqueio nem defeito: é a última edição que existe. No dia
seguinte o Caderno 1 foi extinto e o DEJESP tomou o lugar. O DOE-SP
(`do-api-web-search.doe.sp.gov.br`) responde com o envelope certo e
`totalItems: 0` em toda tentativa — não é fonte utilizável.

## Quanto a varredura aberta reproduz do INR

Retrotestado contra as 35 edições arquivadas de 01/09 a 22/10/2026.

| Filtro | Atos no INR | Recuperados | Perda |
|---|---|---|---|
| Acórdãos do CSM (35 edições) | 30 | **30** | **0** |
| Corregedoria, Classif. II e III (20, 21 e 22/10) | 32 | **32** | **0** |

O texto do DJEN é igual ou maior que o do INR, e traz seções que o INR corta
("Legislação citada", "Jurisprudência citada", advogados):

| Acórdão | DJEN | INR |
|---|---|---|
| 1001998-69.2026.8.26.0100 | 3.562 car. | 3.424 car. |
| 1003618-59.2024.8.26.0271 | 1.217 car. | 1.276 car. |

E chega antes: o INR raciona 5 acórdãos por edição e empurra o resto. O lote
do DJEN de 09/10 só saiu na edição do INR de **13/10**, quatro dias depois.

**O Classificador IV não é reproduzível por regra.** A seleção do INR ali é
editorial: itens idênticos em classe e forma são separados pelo assunto e pela
relevância. Está fora da triagem por decisão de 22/10/2026 — é primeira
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
  atos cuja fonte é o INR, que reproduzem a compilação de um fornecedor
  contratado.

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
- **Ritmo no INR.** Abrir cada edição uma vez e guardar. Em 22/10/2026 o IP foi
  bloqueado ("Verificação de segurança") porque uma execução abriu 8 edições
  quatro vezes cada em poucos minutos.
- **A contagem sai do índice da edição, nunca da busca no texto.** Em
  11/09/2026 um acórdão foi perdido e o dia reportado como "não consta nada".
- **"Não consta nada" significa nada em matéria extrajudicial** — não que o
  termo não apareça no diário. O INR corta ~95% do DEJESP antes de montar os
  classificadores, e menções reais a Assis (designação de juiz auxiliar, obra
  no fórum) ficam fora dos cinco classificadores.

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

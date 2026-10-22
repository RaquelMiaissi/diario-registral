# Firebase — o que a Raquel precisa fazer

Eu não consigo fazer estes passos: exigem a sua conta e, em alguns deles, a
sua senha. **Eu não digito senha, token nem chave de acesso sua em lugar
nenhum** — então esta parte é sua, e depois eu sigo daqui.

## 1. Criar o projeto

1. Entre em <https://console.firebase.google.com> com a conta
   `rmiaissi@gmail.com`.
2. **Adicionar projeto** → nome sugerido: `classificador-inr-assis`.
3. Google Analytics: pode **desativar**. Não serve para nada aqui e simplifica.

## 2. Criar o banco

1. No menu lateral: **Build → Firestore Database → Criar banco de dados**.
2. Escolha **modo de produção** (não o modo de teste — o modo de teste libera
   leitura e escrita para qualquer pessoa por 30 dias, e os nossos dados têm
   parte interna).
3. Local: **southamerica-east1 (São Paulo)**.

## 3. Publicar as regras de acesso

1. Aba **Regras**, dentro do Firestore.
2. Apague o que estiver lá e cole o conteúdo de `firestore.rules`, na raiz
   deste repositório.
3. **Publicar**.

Essas regras são a peça que separa o que é público do que é interno. Sem
elas, ou o banco fica fechado para o site, ou abre a triagem interna do
cartório para a internet.

## 4. Pegar a configuração do site

1. **Visão geral do projeto** → ícone `</>` (Web) → registrar um app web
   chamado, por exemplo, `site`.
2. Ele mostra um bloco `firebaseConfig`. Preciso só de dois valores:
   **`projectId`** e **`apiKey`**.
3. Esses dois **podem** ser colados aqui na conversa: não são segredo. A
   `apiKey` do cliente Firebase só identifica o projeto; quem controla o
   acesso são as regras do passo 3. É assim por desenho do Firebase.

## 5. A chave de escrita — essa NÃO passa por mim

Para gravar no banco é preciso uma **conta de serviço** (um arquivo JSON que o
Firebase gera em *Configurações do projeto → Contas de serviço → Gerar nova
chave privada*).

Esse arquivo é credencial de verdade: quem tem ele escreve e apaga o que
quiser no banco, ignorando as regras. Então:

- **Não cole o conteúdo dele na conversa.** Eu não vou pedir e não vou usar.
- **Não comite no repositório.** O `.gitignore` já barra
  `*-serviceAccount*.json` e `*-adminsdk-*.json`, mas a regra vale sempre.
- Guarde fora do repositório, numa pasta só sua.

### Quem grava os dados, então?

Duas saídas limpas, e você escolhe:

**(a) Pelo GitHub, sem Firebase na escrita.** A varredura diária grava o
`dados.json` na sua pasta do Drive e envia para o repositório. O site lê do
próprio repositório. O Firestore fica só com a parte interna, que você
alimenta quando quiser. Mais simples, e não precisa de conta de serviço
nenhuma.

**(b) Pela sua máquina, com a conta de serviço.** Você instala o arquivo da
conta de serviço num lugar fixo do seu computador e eu rodo ali um script que
lê esse arquivo do disco e grava no Firestore. Eu nunca vejo o conteúdo da
chave — o script lê do caminho, não de mim. Mais completo, e deixa o site
sempre em dia sem passar pelo Git.

Minha sugestão é começar pela **(a)** e migrar para a **(b)** se o volume
crescer. Mas é sua decisão.

## 6. O que me mandar quando terminar

Só isto:

- `projectId`
- `apiKey`
- se escolheu a saída (a) ou a (b) do passo 5

Com esses três eu configuro o site e ele passa a ler do banco.

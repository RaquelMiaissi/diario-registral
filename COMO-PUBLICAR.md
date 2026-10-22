# Como publicar no GitHub

O repositório já está pronto e com dois commits, em `~/Sites/classificador-inr`
no seu Mac. Falta só criar o repositório no GitHub e enviar.

**Eu não faço estes passos** porque exigem a sua credencial, e eu não digito
token nem senha sua em lugar nenhum. São três comandos.

## 1. Criar o repositório vazio no GitHub

Em <https://github.com/new>:

- **Repository name:** `classificador-inr`
- **Public** — precisa ser público para o GitHub Pages funcionar no plano
  gratuito. O que está neste repositório foi preparado para ser público:
  só código, documentação e material de diário oficial aberto.
- **NÃO** marque "Add a README file", "Add .gitignore" nem "Choose a license".
  O repositório local já tem o seu próprio histórico, e marcar isso cria um
  commit no GitHub que conflita com o nosso.

Clique em **Create repository** e não feche a página.

## 2. Enviar, pelo Terminal do seu Mac

Abra o Terminal (⌘ + espaço, digite "Terminal") e cole, uma linha por vez:

```sh
cd ~/Sites/classificador-inr
git remote add origin https://github.com/SEU-USUARIO/classificador-inr.git
git push -u origin main
```

Troque `SEU-USUARIO` pelo seu nome de usuário no GitHub.

No `git push` ele vai pedir autenticação. O Mac normalmente abre uma janela do
GitHub para você entrar; se em vez disso ele pedir usuário e senha no próprio
Terminal, a senha **não** é a da sua conta — é um *personal access token*
(chave de acesso pessoal), que você gera em
<https://github.com/settings/tokens> marcando a permissão `repo`.

Se der erro dizendo `remote origin already exists`, use
`git remote set-url origin ...` em vez de `git remote add origin ...`.

## 3. Ligar o site

No repositório no GitHub: **Settings → Pages**.

- **Source:** Deploy from a branch
- **Branch:** `main`, pasta **`/docs`**
- **Save**

Em um ou dois minutos o site fica no ar em
`https://SEU-USUARIO.github.io/classificador-inr/`.

## Depois, no dia a dia

Eu continuo fazendo os commits aqui — você só precisa dar o push:

```sh
cd ~/Sites/classificador-inr && git push
```

## Não esqueça

O Firebase ainda está pendente. O passo a passo está em
`documentacao/firebase-passo-a-passo.md`, e quando terminar me mande o
`projectId` e a `apiKey` (esses dois podem vir pela conversa — não são
segredo). **A chave da conta de serviço, não**: aquela fica só com você.

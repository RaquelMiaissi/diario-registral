# Como publicar no GitHub

Situação em 22/10/2026:

- Repositório criado no GitHub: **github.com/RaquelMiaissi/diario-registral**
  (público, sem README — como precisava).
- Repositório local em `~/Sites/diario-registral`, já apontando para o remoto.

Falta **um comando**, que só você pode dar, porque exige a sua credencial e
eu não digito token nem senha sua em lugar nenhum.

## O comando

Abra o Terminal (⌘ + espaço, digite "Terminal") e cole:

```sh
cd ~/Sites/diario-registral && git push -u origin main
```

O Mac normalmente abre uma janela do GitHub para você autorizar. Se em vez
disso pedir usuário e senha no próprio Terminal, a senha **não** é a da sua
conta — é um *personal access token* (chave de acesso pessoal), que você gera
em <https://github.com/settings/tokens> marcando a permissão `repo`.

## Ligar o site

Depois do push, em <https://github.com/RaquelMiaissi/diario-registral/settings/pages>:

- **Source:** Deploy from a branch
- **Branch:** `main`, pasta **`/docs`**
- **Save**

Em um ou dois minutos o site fica no ar em
**https://raquelmiaissi.github.io/diario-registral/**

## Depois, no dia a dia

Eu faço os commits aqui; você só dá o push:

```sh
cd ~/Sites/diario-registral && git push
```

## Firebase

Projeto, Firestore (São Paulo) e regras já estão feitos e testados — ver
`documentacao/firebase-passo-a-passo.md`. O que falta é a carga inicial dos
dados internos, que exige a conta de serviço: essa fica só com você.

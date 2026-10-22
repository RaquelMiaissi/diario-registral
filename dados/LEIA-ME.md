# Dados

`schema.md` descreve o modelo. Os dados em si **não ficam neste repositório**:

- O que é público (acórdãos e atos de diário oficial) está em `docs/dados.json`,
  que o site lê.
- O que é interno (verificação do Filtro 1, triagem da serventia, qualquer
  reprodução do compilador pago) vai para o Firestore, atrás das regras de
  `firestore.rules`. A carga inicial está na pasta do projeto no Google Drive
  (`Publicações_INR/dados-limpo.json`), nunca aqui.

A pasta `dados/seed/` está no `.gitignore` por isso.

#!/usr/bin/env python3
"""Injeta docs/dados.json dentro de docs/index.html (bloco <script id="dados-inline">).

Uso:  python3 src/build/site.py [docs/dados.json] [docs/index.html]

O site Diário Registral é auto-contido: os dados ficam embutidos no HTML.
Depois de alterar dados.json, rodar este script e commitar os dois arquivos.
"""
import json
import re
import sys

dados = sys.argv[1] if len(sys.argv) > 1 else "docs/dados.json"
html = sys.argv[2] if len(sys.argv) > 2 else "docs/index.html"

with open(dados, encoding="utf-8") as f:
    d = json.load(f)
compact = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

with open(html, encoding="utf-8") as f:
    h = f.read()

h, n = re.subn(
    r'(<script type="application/json" id="dados-inline">).*?(</script>)',
    lambda m: m.group(1) + compact + m.group(2),
    h,
    flags=re.S,
)
if n != 1:
    sys.exit("bloco dados-inline não encontrado (ou encontrado mais de uma vez) em " + html)

with open(html, "w", encoding="utf-8") as f:
    f.write(h)
print(f"ok: {len(d.get('acordaos', []))} acórdãos, {len(d.get('dias', []))} dias, "
      f"{len(d.get('alertas', []))} alertas, {len(d.get('assis', []))} assis → {html}")

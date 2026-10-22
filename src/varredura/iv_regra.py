# -*- coding: utf-8 -*-
import re, json

# assuntos que nao sao materia registral
ASSUNTO_FORA = re.compile(r'crema[çc][ãa]o|traslado|translado de corpo|peti[çc][ãa]o intermedi[áa]ria', re.I)

# corpo que e mero andamento / expediente, nao decide materia registral
ANDAMENTO = re.compile(
    r'(À\s+parte\s+(interessada|requerente|representante|re[uú])'
    r'|facultada\s+manifesta[çc][ãa]o'
    r'|para\s+manifesta[çc][ãa]o'
    r'|abra-se\s+vista'
    r'|notifiquem-se|notifique-se'
    r'|diligencie-se'
    r'|cumpra-se\s+o\s+alvar[áa]|alvar[áa]\s+dispon[íi]vel'
    r'|recolhimento\s+dos\s+emolumentos'
    r'|defiro\s+a\s+gratuidade'
    r'|defiro\s+a\s+habilita[çc][ãa]o'
    r'|defiro\s+o\s+prazo|prazo\s+para\s+cumprimento'
    r'|ciente\s+das\s+provid[êe]ncias'
    r'|recepciono\s+o\s+recurso'
    r'|ante\s+o\s+teor\s+d[ao]s?\s+(f|peti)'
    r')', re.I)

def triagem(it):
    """it: {p, v, cls, assunto, corpo}. Devolve (entra:bool, motivo:str)"""
    if ASSUNTO_FORA.search(it['assunto']):
        return False, 'assunto fora da materia registral: '+it['assunto']
    m = ANDAMENTO.search(it['corpo'])
    if m:
        return False, 'mero andamento: "'+m.group(0).strip()+'"'
    return True, 'decide materia registral'

if __name__ == '__main__':
    dados = json.load(open('iv_dias.json', encoding='utf-8'))
    gt = {"2026-10-22":["0031263-36.2026.8.26.0100","1016602-35.2026.8.26.0100"],
          "2026-10-21":["0018235-74.2021.8.26.0100","1013200-43.2026.8.26.0100",
                        "1016487-14.2026.8.26.0100","1018252-20.2026.8.26.0100"],
          "2026-10-20":["0031089-27.2026.8.26.0100","0032424-81.2026.8.26.0100",
                        "1015890-45.2026.8.26.0100","1017717-91.2026.8.26.0100"],
          "2026-10-19":[]}
    for d in sorted(dados, reverse=True):
        rows = dados[d]
        entra = [r for r in rows if triagem(r)[0]]
        fora  = [(r, triagem(r)[1]) for r in rows if not triagem(r)[0]]
        g = set(gt.get(d, []))
        e = set(r['p'] for r in entra)
        print('='*72)
        print(d, '| candidatos', len(rows), '-> nossa triagem', len(entra), '| INR', len(g))
        print('  coincidem com o INR :', len(e & g))
        print('  nossos a mais       :', sorted(e - g) or '-')
        print('  INR tem, nos nao    :', sorted(g - e) or '-')
        print('  --- entram ---')
        for r in entra:
            print('   %dª V | %-28s | %s' % (r['v'], r['assunto'][:28], r['p']), '<-- INR tb' if r['p'] in g else '')
        print('  --- descartados (%d) ---' % len(fora))
        for r, mot in fora[:40]:
            mk = '  <<< INR PUBLICOU!' if r['p'] in g else ''
            print('   %dª V | %-28s | %s | %s%s' % (r['v'], r['assunto'][:28], r['p'], mot[:58], mk))

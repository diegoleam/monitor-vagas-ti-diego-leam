"""Teste ONLINE sem Telegram: usa coleta geral e termos TI, com moderação."""
from coletores.gupy import coletar

if __name__ == '__main__':
    vagas = coletar(max_paginas=2)
    print(f'Vagas únicas de TI: {len(vagas)}')
    for vaga in vagas[:30]:
        print(f'{vaga.modalidade} | {vaga.titulo} | {vaga.empresa} | {vaga.publicada_em}')
        print(vaga.url)
    if not vagas:
        print('AVISO: nenhuma vaga reconhecida. Verifique acesso à API e filtros.')

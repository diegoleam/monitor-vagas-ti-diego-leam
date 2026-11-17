"""Teste offline: utiliza o JSON salvo, sem internet e sem Telegram.

Execute na raiz do projeto: python -m testes.testar_gupy_json
"""
import json
from pathlib import Path
from coletores.interpretador_gupy import interpretar_resposta

if __name__ == '__main__':
    arquivo = Path(__file__).resolve().parents[1] / 'dados' / 'exemplo_gupy.json'
    dados = json.loads(arquivo.read_text(encoding='utf-8'))
    vagas, paginacao = interpretar_resposta(dados)
    print(f'Registros recebidos nesta página: {len(dados["data"])}')
    print(f'Total informado pelo portal: {paginacao.get("total", "?")}')
    print(f'Limite: {paginacao.get("limit", "?")} | Offset: {paginacao.get("offset", "?")}')
    print(f'Vagas classificadas como TI: {len(vagas)}')
    for vaga in vagas:
        print(f'- {vaga.titulo} | {vaga.empresa} | {vaga.modalidade} | {vaga.publicada_em}')
        print(f'  {vaga.url}')
    assert vagas, 'Nenhuma vaga de TI reconhecida no arquivo de exemplo.'
    assert all(v.url.startswith('https://') for v in vagas)
    print('TESTE OFFLINE CONCLUÍDO COM SUCESSO')

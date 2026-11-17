"""Teste isolado: busca geral, termos, paginação, deduplicação e prioridades."""
from unittest.mock import patch
from coletores.gupy import coletar, TERMOS_TI

class Resposta:
    def __init__(self, dados): self.dados = dados
    def json(self): return self.dados

chamadas = []
def requisicao(url, params=None):
    chamadas.append(params.copy())
    offset = params['offset']
    termo = params.get('jobName')
    # Busca geral: 25 vagas, incluindo modalidades diferentes.
    if not termo:
        registros = [registro(i, ('remote', 'hybrid', 'on-site')[i % 3])
                     for i in range(offset, min(offset + 12, 25))]
        total = 25
    else:
        # Repetir um identificador da busca geral para verificar deduplicação.
        registros = [registro(0, 'remote'), registro(100 + TERMOS_TI.index(termo), 'on-site')]
        total = 2
    return Resposta({'data': registros, 'pagination': {'total': total, 'limit': 12, 'offset': offset}})

def registro(i, modalidade):
    return {'id': i, 'name': 'Analista de Suporte Técnico',
            'jobUrl': f'https://empresa.gupy.io/job/{i}',
            'careerPageName': 'Empresa', 'workplaceType': modalidade,
            'publishedDate': '2026-11-16T10:00:00Z'}

with patch('coletores.gupy.requisitar', side_effect=requisicao), patch('coletores.gupy.time.sleep'):
    vagas = coletar()
assert len(vagas) == 25 + len(TERMOS_TI), len(vagas)
assert [x['offset'] for x in chamadas[:3]] == [0, 12, 24], chamadas
assert 'jobName' not in chamadas[0] and 'workplaceType' not in chamadas[0]
assert len(chamadas) == 3 + len(TERMOS_TI)
assert vagas[0].modalidade == 'Remoto'
assert {'Remoto', 'Híbrido', 'Presencial'} <= {v.modalidade for v in vagas}
print('TESTE SIMULADO APROVADO: geral + termos TI, todas modalidades, sem duplicatas')

"""Coletor Gupy: vagas gerais recentes e buscas específicas de TI.

Sem filtros de cidade ou modalidade. Prioriza remoto na lista devolvida.
Consultas moderadas; não contorna recusas/bloqueios do portal.
"""
import time
from coletores.base import requisitar
from coletores.interpretador_gupy import interpretar_resposta
from servicos.prioridades import ordenar_vagas

ENDPOINT = 'https://portal.gupy.io/api/job-search/jobs'
LIMITE = 12
MAX_PAGINAS = 5
INTERVALO_SEGUNDOS = 1.0
# Buscas ampliadas para informática, manutenção e suporte; uma página por termo.
TERMOS_TI = (
    'informática', 'suporte', 'manutenção', 'técnico de informática',
    'desenvolvedor', 'estágio', 'infraestrutura', 'redes', 'dados',
    'programador',
)

def coletar(termo=None, modalidade=None, max_paginas=3):
    """Sem termo: busca geral + termos de TI; com termo: apenas esse termo.

    modalidade=None não filtra remoto/presencial/híbrido. max_paginas
    limita a busca geral ou uma pesquisa específica (1 página por termo
    adicional no modo geral), evitando varredura ilimitada.
    """
    if not isinstance(max_paginas, int) or not 1 <= max_paginas <= MAX_PAGINAS:
        raise ValueError(f'max_paginas deve estar entre 1 e {MAX_PAGINAS}')
    if termo is not None and not isinstance(termo, str):
        raise ValueError('termo deve ser texto ou None')
    buscas = [(termo.strip(), max_paginas)] if termo and termo.strip() else [('', max_paginas)] + [(x, 1) for x in TERMOS_TI]
    encontradas = {}
    for indice, (palavra, paginas) in enumerate(buscas):
        offset = 0
        for pagina in range(paginas):
            parametros = {'limit': LIMITE, 'offset': offset, 'sortBy': 'publishedDate'}
            if palavra:
                parametros['jobName'] = palavra
            if modalidade:
                parametros['workplaceType'] = modalidade
            if indice or pagina:
                time.sleep(INTERVALO_SEGUNDOS)
            resposta = requisitar(ENDPOINT, params=parametros)
            try:
                dados = resposta.json()
            except ValueError as exc:
                raise RuntimeError('Gupy retornou JSON inválido') from exc
            if not isinstance(dados, dict) or not isinstance(dados.get('data'), list):
                raise RuntimeError('Formato da resposta Gupy mudou: campo data ausente')
            registros = dados['data']
            vagas, paginacao = interpretar_resposta(dados)
            for vaga in vagas:
                encontradas[vaga.id] = vaga
            print(f'Gupy: busca {palavra or "GERAL"}, página {pagina+1}, '
                  f'{len(registros)} registros, {len(vagas)} de TI')
            if not registros:
                break
            try:
                total = paginacao.get('total')
                total = int(total) if total is not None else None
                passo = int(paginacao.get('limit') or LIMITE)
            except (ValueError, TypeError) as exc:
                raise RuntimeError('Paginação Gupy inválida') from exc
            if passo <= 0:
                raise RuntimeError('Limite de paginação Gupy inválido')
            offset += len(registros)
            if (total is not None and offset >= total) or len(registros) < passo:
                break
    return ordenar_vagas(encontradas.values())

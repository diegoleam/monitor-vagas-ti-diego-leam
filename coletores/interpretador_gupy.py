"""Converte respostas JSON de vagas da Gupy para o modelo comum do projeto.

Este módulo NÃO acessa a internet. A origem da requisição ainda precisa
ser confirmada e ter sua utilização automatizada avaliada separadamente.
"""
from servicos.modelos import Vaga
from servicos.filtros import eh_ti

MODALIDADES = {'remote': 'Remoto', 'hybrid': 'Híbrido', 'on-site': 'Presencial', 'onsite': 'Presencial'}


def interpretar_resposta(dados: dict) -> tuple[list[Vaga], dict]:
    """Devolve (vagas válidas de TI, metadados de paginação)."""
    if not isinstance(dados, dict) or not isinstance(dados.get('data'), list):
        raise ValueError('Resposta Gupy inválida: esperado objeto com lista data.')
    paginacao = dados.get('pagination') or {}
    vagas = []
    ids = set()
    for registro in dados['data']:
        if not isinstance(registro, dict):
            continue
        titulo = str(registro.get('name') or '').strip()
        url = str(registro.get('jobUrl') or '').strip()
        identificador = registro.get('id')
        if not titulo or not url.startswith('https://') or identificador is None:
            continue
        if not eh_ti(titulo, str(registro.get("description") or "")):
            continue
        chave = str(identificador)
        if chave in ids:
            continue
        ids.add(chave)
        cidade = str(registro.get('city') or '').strip()
        estado = str(registro.get('state') or '').strip()
        local = ' / '.join(parte for parte in (cidade, estado) if parte) or 'Não informada'
        vagas.append(Vaga(
            portal='Gupy', titulo=titulo,
            empresa=str(registro.get('careerPageName') or 'Não informada'),
            url=url,
            publicada_em=registro.get('publishedDate'),
            modalidade=MODALIDADES.get(str(registro.get('workplaceType') or '').lower(), 'Não informada'),
            localizacao=local,
        ))
    return vagas, paginacao

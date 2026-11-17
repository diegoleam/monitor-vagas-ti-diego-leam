"""Classificação explicável: confirmado, provável ou não identificado."""
import re
import unicodedata
from servicos.dicionario_ti import CARGOS_TI, CONTEXTO_FORTE, CONTEXTO_TECNICO, TITULOS_AMBIGUOS

def normalizar(texto):
    texto = unicodedata.normalize('NFKD', str(texto or '').casefold())
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return ' '.join(re.findall(r'[a-z0-9]+', texto))

def contem(texto, termo):
    return f' {normalizar(termo)} ' in f' {normalizar(texto)} '

def classificar(titulo, descricao=''):
    """Retorna (classe, justificativa). 'provavel' é mantida na coleta."""
    t, d = normalizar(titulo), normalizar(descricao)
    if any(contem(t, termo) for termo in CARGOS_TI):
        return 'confirmada', 'Cargo de TI identificado no título'
    # Ex.: 'Pessoa Estagiária de Suporte' exige contexto técnico verificável.
    # Evita que cargos explicitamente comerciais/logísticos virem TI só por citar software.
    nao_ti = ('importacao', 'exportacao', 'vendas', 'comercial', 'marketing', 'logistica')
    if any(contem(t, termo) for termo in nao_ti):
        return 'nao_identificada', 'Cargo predominantemente fora de TI'
    ambiguo = any(contem(t, termo) for termo in TITULOS_AMBIGUOS)
    forte = [x for x in CONTEXTO_FORTE if contem(d, x)]
    tecnicos = [x for x in CONTEXTO_TECNICO if contem(d, x)]
    if ambiguo and (forte or len(set(tecnicos)) >= 2):
        return 'provavel', 'Título genérico com evidências de TI na descrição'
    # Título genérico sem contexto de TI: não disparar alerta.
    return 'nao_identificada', 'Sem evidência suficiente de cargo de TI'

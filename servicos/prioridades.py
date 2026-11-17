"""Ordena oportunidades sem excluir nenhuma vaga de TI.

Preferência atual: suporte remoto > outras remotas > híbridas > presenciais.
Estágios de suporte remoto também recebem prioridade máxima.
"""
from servicos.classificador_ti import normalizar

TERMOS_SUPORTE = (
    'suporte', 'help desk', 'service desk', 'it support',
    'technical support', 'support analyst', 'support specialist',
    'sustentacao', 'atendimento tecnico',
)


def eh_suporte(titulo):
    """Identifica suporte pelo cargo, sem depender da descrição genérica."""
    texto = f' {normalizar(titulo)} '
    return any(f' {normalizar(termo)} ' in texto for termo in TERMOS_SUPORTE)


def nivel_prioridade(vaga):
    """Aceita objetos Vaga ou dicionários persistidos no histórico."""
    campo = lambda chave: vaga.get(chave, '') if isinstance(vaga, dict) else getattr(vaga, chave, '')
    modalidade = normalizar(campo('modalidade'))
    if modalidade == 'remoto':
        return 0 if eh_suporte(campo('titulo')) else 1
    if modalidade == 'hibrido':
        return 2
    if modalidade == 'presencial':
        return 3
    return 4


def rotulo_prioridade(vaga):
    nivel = nivel_prioridade(vaga)
    return ('⭐ PRIORIDADE MÁXIMA — SUPORTE REMOTO' if nivel == 0 else
            '🏠 VAGA REMOTA DE TI' if nivel == 1 else
            '🔄 VAGA HÍBRIDA DE TI' if nivel == 2 else
            '🏢 VAGA PRESENCIAL DE TI' if nivel == 3 else
            '💻 NOVA VAGA DE TI')


def ordenar_vagas(vagas):
    """Ordenação estável: prioridade, depois data mais recente."""
    resultado = list(vagas)
    def publicada(v):
        return (v.get('publicada_em') if isinstance(v, dict) else v.publicada_em) or ''
    resultado.sort(key=publicada, reverse=True)
    resultado.sort(key=nivel_prioridade)
    return resultado

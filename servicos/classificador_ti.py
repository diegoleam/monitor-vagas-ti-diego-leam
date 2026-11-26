"""Classificação explicável de vagas de TI.

Compatível com classificar(titulo, descricao='') e seus três estados:
'confirmada', 'provavel' e 'nao_identificada'.
"""
import re
import unicodedata

from servicos.dicionario_ti import (
    CARGOS_TI, CONTEXTO_FORTE, CONTEXTO_TECNICO,
    TITULOS_AMBIGUOS, TERMOS_EXIGEM_CONTEXTO,
)


def normalizar(texto):
    """Remove acentos e pontuação, preservando limites entre palavras."""
    texto = unicodedata.normalize('NFKD', str(texto or '').casefold())
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return ' '.join(re.findall(r'[a-z0-9]+', texto))


def contem(texto, termo):
    """Busca expressão completa, sem aceitar trechos de outras palavras."""
    termo = normalizar(termo)
    return bool(termo) and f' {termo} ' in f' {normalizar(texto)} '


# Evidências inequívocas de informática no título, mesmo em cargos de estágio.
MARCADORES_TI_TITULO = (
    'informatica', 'tecnologia da informacao', 'ti', 't i',
    'redes de computadores', 'infraestrutura de ti', 'infraestrutura de redes',
    'suporte de ti', 'suporte em ti', 'suporte de informatica',
    'manutencao de computadores', 'manutencao de hardware',
    'manutencao e suporte em informatica', 'manutencao e suporte de informatica',
    'sistemas de informacao', 'sistemas computacionais',
    'desenvolvimento de software', 'engenharia de software',
    'desenvolvimento web', 'desenvolvimento de sistemas',
    'programacao', 'python', 'java', 'javascript', 'typescript',
    'banco de dados', 'ciencia de dados', 'engenharia de dados',
    'seguranca da informacao', 'ciberseguranca',
    'computacao', 'computadores', 'help desk', 'helpdesk',
    'service desk', 'servicedesk', 'devops', 'cloud engineer',
    'qa engineer', 'testes de software', 'automacao de testes',
    'power bi', 'business intelligence', 'rpa',
)

# Títulos cuja área é explicitamente diferente de TI.
# A exclusão é aplicada ANTES de qualquer aprovação genérica.
AREAS_NAO_TI = (
    'recursos humanos', 'gestao de pessoas', 'desenvolvimento humano',
    'departamento pessoal', 'administracao', 'administrativo',
    'marketing', 'comercial', 'vendas', 'logistica',
    'importacao', 'exportacao', 'contabilidade', 'contabil',
    'financeiro', 'financas', 'juridico', 'direito',
    'enfermagem', 'farmacia', 'odontologia', 'psicologia',
    'pedagogia', 'nutricao', 'agronomia', 'agricola',
    'engenharia civil', 'infraestrutura predial',
    'manutencao predial', 'engenharia mecanica',
    'qualidade de alimentos', 'atendimento ao cliente',
    'relacionamento com cliente', 'customer success',
)

# Palavras muito comuns em descrições administrativas não podem,
# isoladamente, transformar uma vaga em TI.
TECNICOS_FRACOS = (
    'software', 'sistemas', 'erp', 'api', 'apis', 'git',
    'office 365', 'microsoft 365', 'impressoras', 'windows',
    'excel', 'office', 'hardware', 'servidores', 'cloud',
)

# Algumas expressões do dicionário são genéricas mesmo quando presentes
# em um título. Uma evidência específica de TI ainda pode confirmá-las.
TERMOS_AMBIGUOS = tuple(set(TERMOS_EXIGEM_CONTEXTO) | {
    'estagio em desenvolvimento', 'estagio em infraestrutura',
    'estagio em sistemas', 'estagio em tecnologia',
    'estagio em suporte tecnico', 'suporte tecnico',
    'analista de suporte', 'tecnico de campo',
    'tecnico de infraestrutura', 'tecnico em infraestrutura',
    'tecnico de manutencao e suporte',
    'tecnico em manutencao e suporte',
    'tecnica de manutencao e suporte',
    'tecnica em manutencao e suporte',
})


def classificar(titulo, descricao=''):
    """Retorna (classe, justificativa); vagas prováveis continuam elegíveis.

    Regras:
    1. Título com evidência explícita de informática: confirmado.
    2. Título explicitamente de outra área: rejeitado.
    3. Termos de cargo específicos: confirmado.
    4. Título ambíguo: exige descrição com evidência de TI.
    """
    t, d = normalizar(titulo), normalizar(descricao)
    if not t:
        return 'nao_identificada', 'Título ausente'

    titulo_ti = any(contem(t, x) for x in MARCADORES_TI_TITULO)
    titulo_outra_area = any(contem(t, x) for x in AREAS_NAO_TI)

    # Um título de outra área não deve ser aprovado só por citar
    # software ou ferramentas. A evidência explícita de TI prevalece.
    if titulo_outra_area and not titulo_ti:
        return 'nao_identificada', 'Título indica outra área profissional'

    if titulo_ti:
        return 'confirmada', 'Área de TI identificada explicitamente no título'

    # Prioriza termos específicos; termos genéricos não confirmam sozinhos.
    cargos_especificos = (
        termo for termo in CARGOS_TI
        if not any(contem(termo, ambiguo) for ambiguo in TERMOS_AMBIGUOS)
    )
    if any(contem(t, termo) for termo in cargos_especificos):
        return 'confirmada', 'Cargo específico de TI identificado no título'

    ambiguo = any(contem(t, x) for x in TITULOS_AMBIGUOS) or any(
        contem(t, x) for x in TERMOS_AMBIGUOS
    )
    if not ambiguo:
        return 'nao_identificada', 'Sem evidência suficiente de cargo de TI'

    fortes = {x for x in CONTEXTO_FORTE if contem(d, x)}
    tecnicos = {
        x for x in CONTEXTO_TECNICO
        if x not in TECNICOS_FRACOS and contem(d, x)
    }
    if fortes or len(tecnicos) >= 2:
        return 'provavel', 'Título genérico com evidências de TI na descrição'

    return 'nao_identificada', 'Título genérico sem contexto técnico suficiente'

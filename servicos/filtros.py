"""Interface estável para os coletores; vocabulário em módulos próprios."""
from servicos.classificador_ti import classificar, normalizar, contem

def eh_ti(titulo: str, descricao: str = '') -> bool:
    return classificar(titulo, descricao)[0] in ('confirmada', 'provavel')

"""Testes locais sem rede e sem Telegram."""
from servicos.prioridades import ordenar_vagas, nivel_prioridade, eh_suporte
from telegram.mensagens import mensagem_vaga


def test_ordem_sem_exclusoes():
    vagas = [
        {'titulo':'Desenvolvedor', 'modalidade':'Presencial','publicada_em':'2026-11-16'},
        {'titulo':'Estágio em Suporte Técnico','modalidade':'Remoto','publicada_em':'2026-11-15'},
        {'titulo':'Desenvolvedor Java','modalidade':'Remoto','publicada_em':'2026-11-16'},
        {'titulo':'Analista de Dados','modalidade':'Híbrido','publicada_em':'2026-11-16'},
        {'titulo':'Service Desk Analyst','modalidade':'Remoto','publicada_em':'2026-11-14'},
    ]
    resultado = ordenar_vagas(vagas)
    assert len(resultado) == len(vagas)
    assert [nivel_prioridade(v) for v in resultado] == [0, 0, 1, 2, 3]
    assert eh_suporte('Pessoa Estagiária de Suporte')


def test_mensagem_segura_e_destaque():
    vaga = {'titulo':'Estágio em Suporte <TI>', 'empresa':'Exemplo',
            'modalidade':'Remoto', 'localizacao':'Brasil', 'portal':'Gupy',
            'publicada_em':'2026-11-16T20:39:32Z', 'url':'https://example.org/vaga'}
    mensagem = mensagem_vaga(vaga)
    assert 'PRIORIDADE MÁXIMA' in mensagem
    assert '&lt;TI&gt;' in mensagem
    assert '17:39 (Brasília)' in mensagem
    assert 'Desenvolvido por Diego Leam' in mensagem

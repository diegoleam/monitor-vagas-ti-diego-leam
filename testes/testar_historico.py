"""Teste unitário de deduplicação e persistência em diretório temporário."""
from datetime import datetime, timezone
from servicos.modelos import Vaga
from servicos.historico import atualizar, ler

def test_deduplicacao(tmp_path):
    vagas=tmp_path/'vagas.json'; historico=tmp_path/'historico.json'
    v=Vaga('teste','Analista de Suporte','Exemplo','https://example.org/vaga/1')
    assert len(atualizar([v],vagas,historico)) == 1
    assert len(atualizar([v],vagas,historico)) == 0
    assert len(ler(vagas,[])) == 1

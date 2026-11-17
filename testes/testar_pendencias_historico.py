"""Testes isolados de recuperação de notificações sem rede nem Telegram."""
from pathlib import Path
from tempfile import TemporaryDirectory
from servicos.modelos import Vaga
from servicos.historico import atualizar, listar_pendentes, marcar_notificadas, ler

def executar():
    with TemporaryDirectory() as pasta:
        vagas = Path(pasta) / 'vagas.json'
        historico = Path(pasta) / 'historico.json'
        a = Vaga('teste', 'Estágio em Suporte TI', 'Empresa A', 'https://example.org/1')
        b = Vaga('teste', 'Desenvolvedor Python', 'Empresa B', 'https://example.org/2')
        assert len(atualizar([a], vagas, historico)) == 1
        assert len(listar_pendentes(vagas, historico)) == 1
        print('OK 1: primeira vaga aguarda notificação')
        assert len(atualizar([a], vagas, historico)) == 0
        assert len(listar_pendentes(vagas, historico)) == 1
        print('OK 2: vaga não notificada continua pendente após nova execução')
        marcar_notificadas([a.dicionario()], historico)
        assert listar_pendentes(vagas, historico) == []
        print('OK 3: vaga confirmada não reaparece')
        assert len(atualizar([a,b], vagas, historico)) == 1
        pendentes = listar_pendentes(vagas, historico)
        assert len(pendentes) == 1 and pendentes[0]['id'] == b.id
        print('OK 4: apenas a segunda vaga fica pendente')
        # Simula falha de envio: nenhuma marcação é realizada.
        assert len(listar_pendentes(vagas, historico)) == 1
        print('OK 5: falha de envio preserva pendência no JSON')
        marcar_notificadas(pendentes, historico)
        assert not listar_pendentes(vagas, historico)
        print('OK 6: após confirmação, fila fica vazia')
    print('TESTE CONCLUÍDO: sem alterar arquivos reais ou enviar Telegram')

if __name__ == '__main__':
    executar()

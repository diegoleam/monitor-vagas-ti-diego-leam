"""Diagnóstico seguro do histórico: usa somente diretório temporário."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from servicos.modelos import Vaga
from servicos.historico import atualizar, ler, marcar_notificadas

def vaga(numero, dias=0):
    data = (datetime.now(timezone.utc) - timedelta(days=dias)).isoformat()
    return Vaga('gupy', 'Estágio em Suporte de TI', 'Empresa Exemplo', f'https://example.org/vaga/{numero}', publicada_em=data)

def executar():
    with TemporaryDirectory(prefix='teste_historico_') as pasta:
        vagas, historico = Path(pasta)/'vagas.json', Path(pasta)/'historico.json'
        v1, v2 = vaga(1), vaga(2)
        assert len(atualizar([v1], vagas, historico)) == 1
        print('OK 1: primeira descoberta')
        assert atualizar([v1], vagas, historico) == []
        print('OK 2: duplicata ignorada')
        assert len(atualizar([v1,v2], vagas, historico)) == 1
        print('OK 3: somente nova vaga detectada')
        assert len(ler(vagas, [])) == 2
        print('OK 4: JSON persistido e relido')
        marcar_notificadas([v1.dicionario()], historico)
        assert v1.id in ler(historico, {})
        print('OK 5: marcação de notificada')
        assert atualizar([vaga(99, dias=20)], vagas, historico) == []
        print('OK 6: vaga antiga ignorada')
        # Simula envio com falha: vaga é registrada, mas não marcada como notificada.
        v3 = vaga(3)
        assert len(atualizar([v3], vagas, historico)) == 1
        assert v3.id not in ler(historico,{})
        repeticao = atualizar([v3], vagas, historico)
        if not repeticao:
            print('ATENÇÃO 7: falha no envio NÃO gera nova tentativa na execução seguinte')
        else:
            print('OK 7: tentativa de reenvio disponível')
        print('TESTE FINALIZADO: arquivos reais e Telegram preservados')

if __name__ == '__main__':
    executar()

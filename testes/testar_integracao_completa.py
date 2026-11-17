
"""
Monitor Vagas TI — Diego Leam
Teste integrado: Gupy + Histórico + Telegram.

Não acessa a internet, não envia mensagens reais
e não modifica os arquivos JSON do projeto.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from servicos.modelos import Vaga
from servicos.historico import (
    atualizar,
    listar_pendentes,
    marcar_notificadas,
)
from servicos.prioridades import ordenar_vagas
from telegram.mensagens import mensagem_vaga


def executar():
    # Simulamos três vagas encontradas pela Gupy.
    vagas_gupy = [
        Vaga(
            portal="Gupy",
            titulo="Estágio em Suporte Técnico",
            empresa="Empresa A",
            modalidade="Remoto",
            localizacao="Brasil",
            url="https://example.com/vaga/101",
        ),
        Vaga(
            portal="Gupy",
            titulo="Desenvolvedor Python",
            empresa="Empresa B",
            modalidade="Remoto",
            localizacao="Brasil",
            url="https://example.com/vaga/102",
        ),
        Vaga(
            portal="Gupy",
            titulo="Analista de Redes",
            empresa="Empresa C",
            modalidade="Presencial",
            localizacao="Recife - PE",
            url="https://example.com/vaga/103",
        ),
    ]

    # Os arquivos são criados em uma pasta temporária.
    with TemporaryDirectory() as pasta:
        arquivo_vagas = Path(pasta) / "vagas.json"
        arquivo_historico = Path(pasta) / "historico.json"

        # TESTE 1: primeira descoberta
        novas = atualizar(
            vagas_gupy,
            arquivo_vagas,
            arquivo_historico,
        )
        assert len(novas) == 3
        print("OK 1: três vagas descobertas")

        # TESTE 2: prioridade
        pendentes = listar_pendentes(
            arquivo_vagas,
            arquivo_historico,
        )
        ordenadas = ordenar_vagas(pendentes)

        assert ordenadas[0]["titulo"] == "Estágio em Suporte Técnico"
        assert ordenadas[1]["titulo"] == "Desenvolvedor Python"
        assert ordenadas[2]["titulo"] == "Analista de Redes"

        print("OK 2: suporte remoto recebe prioridade máxima")

        # TESTE 3: preparação das mensagens
        mensagens = [mensagem_vaga(v) for v in ordenadas]

        assert len(mensagens) == 3
        assert "PRIORIDADE MÁXIMA" in mensagens[0]
        assert "Desenvolvido por Diego Leam" in mensagens[0]

        print("OK 3: mensagens preparadas corretamente")

        # TESTE 4: simular envio de duas vagas e falha na terceira
        mensagens_enviadas = []

        def enviar_simulado(vaga, mensagem, falhar=False):
            if falhar:
                raise ConnectionError("Falha simulada do Telegram")

            mensagens_enviadas.append(vaga["id"])
            return {"ok": True}

        for indice, vaga in enumerate(ordenadas):
            try:
                enviar_simulado(
                    vaga,
                    mensagens[indice],
                    falhar=(indice == 2),
                )
            except ConnectionError:
                print("INFO: falha simulada na terceira vaga")
            else:
                marcar_notificadas(
                    [vaga],
                    arquivo_historico,
                )

        assert len(mensagens_enviadas) == 2

        print("OK 4: duas notificações confirmadas")

        # TESTE 5: vaga que falhou permanece pendente
        pendentes = listar_pendentes(
            arquivo_vagas,
            arquivo_historico,
        )

        assert len(pendentes) == 1
        assert pendentes[0]["titulo"] == "Analista de Redes"

        print("OK 5: vaga com falha continua pendente")

        # TESTE 6: nova execução não duplica descobertas
        novas = atualizar(
            vagas_gupy,
            arquivo_vagas,
            arquivo_historico,
        )

        assert len(novas) == 0

        print("OK 6: nenhuma vaga repetida foi descoberta")

        # TESTE 7: recuperar notificação pendente
        vaga_pendente = pendentes[0]

        resposta = enviar_simulado(
            vaga_pendente,
            mensagem_vaga(vaga_pendente),
        )

        assert resposta["ok"] is True

        marcar_notificadas(
            [vaga_pendente],
            arquivo_historico,
        )

        assert listar_pendentes(
            arquivo_vagas,
            arquivo_historico,
        ) == []

        print("OK 7: notificação pendente recuperada")

        # TESTE 8: próxima execução sem novas notificações
        assert len(atualizar(
            vagas_gupy,
            arquivo_vagas,
            arquivo_historico,
        )) == 0

        assert listar_pendentes(
            arquivo_vagas,
            arquivo_historico,
        ) == []

        print("OK 8: execução seguinte sem duplicatas")

    print()
    print("INTEGRAÇÃO APROVADA: 8 testes concluídos")
    print("Nenhuma mensagem real enviada.")
    print("Histórico real preservado.")


if __name__ == "__main__":
    executar()


"""Teste seguro do Telegram: não usa token real, internet ou histórico."""

from unittest.mock import patch

from telegram import bot
from telegram.mensagens import mensagem_vaga
from servicos.prioridades import ordenar_vagas


VAGA = {
    "id": "teste-telegram-001",
    "portal": "Gupy",
    "titulo": "Estágio em Suporte Técnico <TI> & Sistemas",
    "empresa": "Empresa Exemplo & Filhos",
    "modalidade": "Remoto",
    "localizacao": "Brasil",
    "publicada_em": "2026-11-16T20:39:32.776Z",
    "url": "https://exemplo.com/vaga?a=1&b=2",
}


class RespostaFalsa:
    """Simula uma resposta da API do Telegram."""

    def __init__(self, status=200, dados=None):
        self.status = status
        self.dados = dados if dados is not None else {
            "ok": True,
            "result": {"message_id": 123},
        }

    def raise_for_status(self):
        if self.status >= 400:
            import requests
            raise requests.HTTPError(f"HTTP {self.status}")

    def json(self):
        return self.dados


def testar():
    # TESTE 1: formatação da mensagem
    texto = mensagem_vaga(VAGA)

    assert "PRIORIDADE MÁXIMA" in texto
    assert "&lt;TI&gt; &amp; Sistemas" in texto
    assert "Empresa Exemplo &amp; Filhos" in texto
    assert "a=1&amp;b=2" in texto
    assert "16/11/2026" in texto
    assert "Desenvolvido por Diego Leam" in texto
    assert "https://www.linkedin.com/in/diegoleam" in texto

    print("OK 1: mensagem, prioridade, data, link e assinatura")

    # TESTE 2: prioridade para suporte remoto
    outras = [
        dict(
            VAGA,
            id="2",
            titulo="Desenvolvedor Python",
            modalidade="Remoto",
        ),
        dict(
            VAGA,
            id="3",
            titulo="Analista de Redes",
            modalidade="Presencial",
        ),
        dict(
            VAGA,
            id="4",
            titulo="Estágio em Dados",
            modalidade="Híbrido",
        ),
    ]

    ordenadas = ordenar_vagas(outras + [VAGA])

    assert [v["id"] for v in ordenadas] == [
        "teste-telegram-001",
        "2",
        "4",
        "3",
    ]

    print("OK 2: suporte remoto primeiro, sem excluir outras modalidades")

    # TESTE 3: simulação de envio
    chamadas = []

    def post_falso(url, json, timeout):
        chamadas.append((url, json, timeout))
        return RespostaFalsa()

    with (
        patch.object(bot, "TOKEN", "TOKEN_FICTICIO_NAO_REAL"),
        patch.object(bot.requests, "post", side_effect=post_falso),
    ):
        retorno = bot.enviar("CHAT_FICTICIO", texto)

    assert retorno["ok"] is True
    assert len(chamadas) == 1
    assert chamadas[0][1]["chat_id"] == "CHAT_FICTICIO"
    assert chamadas[0][1]["parse_mode"] == "HTML"
    assert chamadas[0][1]["disable_web_page_preview"] is True

    print("OK 3: envio simulado com formato HTML correto")

    # TESTE 4: erro retornado pela API
    with (
        patch.object(bot, "TOKEN", "TOKEN_FICTICIO_NAO_REAL"),
        patch.object(
            bot.requests,
            "post",
            return_value=RespostaFalsa(
                200,
                {"ok": False, "description": "falha simulada"},
            ),
        ),
    ):
        try:
            bot.enviar("CHAT_FICTICIO", texto)
        except RuntimeError:
            pass
        else:
            raise AssertionError("A falha da API deveria gerar exceção")

    print("OK 4: falha lógica da API detectada")

    # TESTE 5: erro HTTP
    with (
        patch.object(bot, "TOKEN", "TOKEN_FICTICIO_NAO_REAL"),
        patch.object(
            bot.requests,
            "post",
            return_value=RespostaFalsa(500),
        ),
    ):
        try:
            bot.enviar("CHAT_FICTICIO", texto)
        except Exception:
            pass
        else:
            raise AssertionError("HTTP 500 deveria gerar exceção")

    print("OK 5: falha HTTP detectada")

    # TESTE 6: impedir envio sem token
    with patch.object(bot, "TOKEN", ""):
        try:
            bot.enviar("CHAT_FICTICIO", texto)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Token ausente deveria gerar exceção")

    print("OK 6: token ausente bloqueia envio")

    print(
        "TESTE APROVADO: nenhuma mensagem real enviada "
        "e nenhum JSON alterado"
    )


if __name__ == "__main__":
    testar()

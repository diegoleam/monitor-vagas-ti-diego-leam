
"""
Monitor Vagas TI — Diego Leam
Versão 0.5 — Integração Gupy + Histórico + Telegram

Modos:
    --simular      Consulta vagas sem alterar JSON ou Telegram.
    --inicializar   Registra vagas atuais sem enviar notificações.
    --enviar        Publica vagas pendentes no canal privado.

Segurança:
    - Não envia mensagens durante a inicialização.
    - Limita a quantidade de notificações por execução.
    - Marca uma vaga como notificada somente após envio confirmado.
    - Preserva vagas pendentes quando o Telegram falha.
"""

import argparse
import logging
import os

from pathlib import Path
from dotenv import load_dotenv

from coletores import gupy, via2
from config.configuracoes import ARQUIVO_VAGAS, ARQUIVO_HISTORICO
from servicos.historico import (
    atualizar,
    marcar_notificadas,
    listar_pendentes,
)
from servicos.prioridades import ordenar_vagas
from telegram.bot import enviar
from telegram.mensagens import mensagem_vaga


# --------------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------------

RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

CANAL_TELEGRAM = os.getenv("TELEGRAM_CHAT_TESTE")

COLETORES = {
    "gupy": gupy.coletar,
    "2via": via2.coletar,
}

LIMITE_PADRAO = 1


# --------------------------------------------------
# COLETA
# --------------------------------------------------

def coletar_vagas(portais):
    """Executa os coletores sem interromper os demais."""

    todas = []
    sucessos = 0

    for portal in portais:
        try:
            vagas = COLETORES[portal]()

            # Uma coleta vazia pode ser válida.
            if vagas is None:
                raise ValueError("Coletor retornou None")

            sucessos += 1

            logging.info(
                "%s: %d vagas de TI coletadas",
                portal,
                len(vagas),
            )

            for vaga in vagas[:5]:
                logging.info(
                    "AMOSTRA | %s | %s",
                    vaga.titulo,
                    vaga.url,
                )

            todas.extend(vagas)

        except Exception:
            logging.exception(
                "Falha no coletor %s",
                portal,
            )

    return todas, sucessos


# --------------------------------------------------
# SIMULAÇÃO
# --------------------------------------------------

def simular(portais):
    """Consulta vagas sem modificar o histórico."""

    vagas, sucessos = coletar_vagas(portais)

    logging.info(
        "SIMULAÇÃO: %d vagas coletadas",
        len(vagas),
    )

    logging.info(
        "Nenhum JSON alterado. Nenhuma mensagem enviada."
    )

    if sucessos == 0:
        logging.error("Nenhum coletor funcionou.")
        return 1

    return 0


# --------------------------------------------------
# INICIALIZAÇÃO
# --------------------------------------------------

def inicializar(portais):
    """
    Registra as vagas atuais sem enviar mensagens.

    IMPORTANTE:
    Deve ser utilizado somente na primeira ativação.
    """

    vagas, sucessos = coletar_vagas(portais)

    if sucessos == 0:
        logging.error(
            "Inicialização cancelada: nenhum coletor funcionou."
        )
        return 1

    if not vagas:
        logging.warning(
            "Nenhuma vaga encontrada. Inicialização cancelada."
        )
        return 1

    novas = atualizar(
        vagas,
        ARQUIVO_VAGAS,
        ARQUIVO_HISTORICO,
    )

    pendentes = listar_pendentes(
        ARQUIVO_VAGAS,
        ARQUIVO_HISTORICO,
    )

    if pendentes:
        marcar_notificadas(
            pendentes,
            ARQUIVO_HISTORICO,
        )

    logging.info(
        "INICIALIZAÇÃO CONCLUÍDA"
    )

    logging.info(
        "Vagas novas registradas: %d",
        len(novas),
    )

    logging.info(
        "Vagas existentes marcadas como notificadas: %d",
        len(pendentes),
    )

    logging.info(
        "Nenhuma mensagem enviada ao Telegram."
    )

    return 0


# --------------------------------------------------
# PRODUÇÃO
# --------------------------------------------------

def produzir(portais, limite):
    """Coleta, identifica e publica vagas pendentes."""

    if not CANAL_TELEGRAM:
        logging.error(
            "TELEGRAM_CHAT_TESTE não configurado no .env"
        )
        return 1

    vagas, sucessos = coletar_vagas(portais)

    if sucessos == 0:
        logging.error(
            "Envio cancelado: nenhum coletor funcionou."
        )
        return 1

    novas = atualizar(
        vagas,
        ARQUIVO_VAGAS,
        ARQUIVO_HISTORICO,
    )

    pendentes = listar_pendentes(
        ARQUIVO_VAGAS,
        ARQUIVO_HISTORICO,
    )

    ordenadas = ordenar_vagas(pendentes)

    logging.info(
        "Novas vagas: %d | Pendentes: %d",
        len(novas),
        len(ordenadas),
    )

    if not ordenadas:
        logging.info(
            "Nenhuma vaga pendente. Monitor atualizado."
        )
        return 0

    enviadas = 0
    falhas = 0

    for vaga in ordenadas[:limite]:
        try:
            texto = mensagem_vaga(vaga)

            # O módulo oficial realiza o envio.
            enviar(CANAL_TELEGRAM, texto)

            # Registrar somente após envio confirmado.
            marcar_notificadas(
                [vaga],
                ARQUIVO_HISTORICO,
            )

            enviadas += 1

            logging.info(
                "ENVIADA | %s | %s",
                vaga["titulo"],
                vaga["url"],
            )

        except Exception:
            falhas += 1

            logging.exception(
                "Falha na notificação da vaga %s",
                vaga.get("id", "desconhecida"),
            )

    logging.info(
        "RESUMO | Enviadas: %d | Falhas: %d",
        enviadas,
        falhas,
    )

    return 1 if falhas else 0


# --------------------------------------------------
# EXECUÇÃO PRINCIPAL
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Monitor Vagas TI — Diego Leam v0.5"
    )

    parser.add_argument(
        "--portal",
        choices=["gupy", "2via", "todos"],
        default="todos",
    )

    modos = parser.add_mutually_exclusive_group()

    modos.add_argument(
        "--simular",
        action="store_true",
        help="Consulta vagas sem modificar JSON ou Telegram",
    )

    modos.add_argument(
        "--inicializar",
        action="store_true",
        help="Registra vagas atuais sem notificações",
    )

    modos.add_argument(
        "--enviar",
        action="store_true",
        help="Publica vagas pendentes no canal Telegram",
    )

    parser.add_argument(
        "--limite",
        type=int,
        default=LIMITE_PADRAO,
        help="Máximo de notificações por execução",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    if args.limite < 1:
        parser.error("--limite deve ser maior que zero")

    portais = (
        list(COLETORES)
        if args.portal == "todos"
        else [args.portal]
    )

    if args.inicializar:
        return inicializar(portais)

    if args.enviar:
        return produzir(portais, args.limite)

    return simular(portais)


if __name__ == "__main__":
    raise SystemExit(main())

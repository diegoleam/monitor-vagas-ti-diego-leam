
"""
Monitor Vagas TI — Diego Leam
Teste de publicação de uma vaga real no canal Telegram.

- Envia somente uma mensagem.
- Não consulta a API da Gupy.
- Não modifica o histórico JSON.
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from servicos.modelos import Vaga
from telegram.mensagens import mensagem_vaga


# Carregar configurações
RAIZ = Path(__file__).resolve().parents[1]
load_dotenv(RAIZ / ".env")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_TESTE")

if not TOKEN or not CHAT_ID:
    raise RuntimeError(
        "Configure TELEGRAM_TOKEN e TELEGRAM_CHAT_TESTE no .env"
    )


# Vaga real encontrada no teste da Gupy
vaga = Vaga(
    portal="Gupy",
    titulo="ANALISTA DE SUPORTE TÉCNICO BILINGUE",
    empresa="IT Universe",
    modalidade="Remoto",
    localizacao="Não informada",
    publicada_em="2026-11-16T20:39:32.776Z",
    url=(
        "https://ituniverse.gupy.io/job/"
        "eyJqb2JJZCI6MTI4NzYxMjIsInNvdXJjZSI6"
        "Imd1cHlfcG9ydGFsIn0="
        "?jobBoardSource=gupy_portal"
    ),
)

# Utilizar o formatador oficial do projeto.
mensagem = mensagem_vaga(vars(vaga))

print("Vaga selecionada:", vaga.titulo)
print("Empresa:", vaga.empresa)
print("Modalidade:", vaga.modalidade)
print("Destino: canal privado configurado")
print()

confirmacao = input(
    "Deseja publicar esta única vaga no canal? (S/N): "
).strip().lower()

if confirmacao != "s":
    print("Teste cancelado. Nenhuma mensagem enviada.")
    raise SystemExit(0)


# Enviar uma única mensagem
url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

resposta = requests.post(
    url_api,
    json={
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    },
    timeout=20,
)

resposta.raise_for_status()
dados = resposta.json()

if not dados.get("ok"):
    raise RuntimeError(
        dados.get("description", "Falha ao publicar vaga")
    )

print("SUCESSO: vaga publicada no canal!")
print("Message ID:", dados["result"]["message_id"])
print("Histórico preservado.")

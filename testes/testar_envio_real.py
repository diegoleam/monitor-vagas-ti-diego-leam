
"""Envia uma única mensagem real ao canal do Telegram."""

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Localiza o .env na raiz do projeto.
RAIZ = Path(__file__).resolve().parents[1]
load_dotenv(RAIZ / ".env")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_TESTE")

if not TOKEN or not CHAT_ID:
    raise RuntimeError(
        "Configure TELEGRAM_TOKEN e TELEGRAM_CHAT_TESTE no .env"
    )

mensagem = (
    "✅ TESTE DE CONEXÃO REALIZADO!\n\n"
    "🤖 Monitor Vagas TI — Diego Leam\n\n"
    "💻 Monitoramento de vagas de TI e estágios.\n"
    "⭐ Prioridade: suporte remoto.\n"
    "🏠 Remoto | 🔄 Híbrido | 🏢 Presencial\n\n"
    "🚀 Canal conectado com sucesso!\n\n"
    "Desenvolvido por Diego Leam\n"
    "https://www.linkedin.com/in/diegoleam"
)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

resposta = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": mensagem,
        "disable_web_page_preview": True,
    },
    timeout=20,
)

resposta.raise_for_status()
dados = resposta.json()

if not dados.get("ok"):
    raise RuntimeError(
        dados.get("description", "Erro no envio ao Telegram")
    )

print("SUCESSO: mensagem enviada ao canal do Telegram!")

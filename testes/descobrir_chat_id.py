
import os
import requests
from dotenv import load_dotenv

# Carrega o token do arquivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN não configurado no .env")

# Consulta as atualizações recebidas pelo bot
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

resposta = requests.get(url, timeout=20)
resposta.raise_for_status()

dados = resposta.json()

if not dados.get("ok"):
    raise RuntimeError("Erro ao consultar a API do Telegram")

encontrado = False

for atualizacao in dados.get("result", []):
    mensagem = atualizacao.get("channel_post", {})
    canal = mensagem.get("chat", {})

    if canal:
        print("Canal:", canal.get("title"))
        print("Chat ID:", canal.get("id"))
        encontrado = True

if not encontrado:
    print("Nenhuma publicação do canal encontrada.")
    print("Publique uma nova mensagem no canal e tente novamente.")

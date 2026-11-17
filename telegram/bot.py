"""Cliente mínimo da API oficial do Telegram, sem dependências extras."""
import requests
from config.configuracoes import TOKEN

def enviar(chat_id, mensagem):
    if not TOKEN: raise RuntimeError('TELEGRAM_TOKEN não configurado')
    r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                      json={'chat_id':chat_id,'text':mensagem,'parse_mode':'HTML',
                            'disable_web_page_preview':True},timeout=20)
    r.raise_for_status()
    dados = r.json()
    if not dados.get('ok'): raise RuntimeError(f'Falha Telegram: {dados.get("description")}')
    return dados

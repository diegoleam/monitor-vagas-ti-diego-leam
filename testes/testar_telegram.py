"""Envio controlado APENAS ao chat de teste, mediante --enviar."""
import argparse
from config.configuracoes import CHAT_TESTE
from telegram.bot import enviar
from telegram.mensagens import com_rodape
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--enviar',action='store_true')
    args=parser.parse_args()
    mensagem=com_rodape('🧪 <b>TESTE — NÃO É UMA NOVA NOTIFICAÇÃO</b>\nIntegração Telegram operacional.')
    if not args.enviar: print('SIMULAÇÃO:', mensagem)
    elif not CHAT_TESTE: raise SystemExit('Configure TELEGRAM_CHAT_TESTE no .env')
    else: enviar(CHAT_TESTE,mensagem); print('Teste enviado ao chat configurado')

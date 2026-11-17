"""Configurações centrais do projeto, sem dados sensíveis no código."""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / 'dados'
DADOS.mkdir(exist_ok=True)
ARQUIVO_VAGAS = DADOS / 'vagas.json'
ARQUIVO_HISTORICO = DADOS / 'historico.json'
ARQUIVO_USUARIOS = DADOS / 'usuarios.json'
DIAS_VAGAS = 14
DIAS_HISTORICO = 30
LINKEDIN = 'https://www.linkedin.com/in/diegoleam'
TOKEN = os.getenv('TELEGRAM_TOKEN', '')
CHAT_TESTE = os.getenv('TELEGRAM_CHAT_TESTE', '')
VIA2_FEED = os.getenv('VIA2_FEED', 'https://2viabr.com.br/feed/')
GUPY_TERMO = os.getenv('GUPY_TERMO', 'tecnologia')

"""Utilitários de rede compartilhados. Cada coletor é independente."""
import requests
from bs4 import BeautifulSoup
AGENTE = 'MonitorVagasTI-DiegoLeam/0.1 (coleta moderada de paginas publicas)'
def requisitar(url, params=None):
    resposta = requests.get(url, params=params, headers={'User-Agent':AGENTE}, timeout=20)
    resposta.raise_for_status()
    return resposta

def texto(elemento): return elemento.get_text(' ', strip=True) if elemento else ''

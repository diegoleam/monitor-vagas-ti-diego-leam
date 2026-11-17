"""Teste local de coleta, sem escrita no histórico e sem Telegram."""
from coletores.gupy import coletar
if __name__ == '__main__':
    vagas = coletar()
    print(f'Gupy: {len(vagas)} vagas encontradas')
    for v in vagas[:10]: print(v.titulo, '|', v.empresa, '|', v.url)

"""Teste independente das prioridades e da formatação de mensagens."""
from testes.test_prioridades import test_ordem_sem_exclusoes, test_mensagem_segura_e_destaque

def main():
    test_ordem_sem_exclusoes()
    test_mensagem_segura_e_destaque()
    print('PRIORIDADES E MENSAGENS: TESTES APROVADOS (sem envio Telegram)')

if __name__ == '__main__':
    main()

"""Cadastro de inscritos. Comandos /start e /parar serão ativados em fase posterior.

Nunca trate a mera existência do chat como consentimento para notificações.
"""
from servicos.historico import ler, salvar
from config.configuracoes import ARQUIVO_USUARIOS

def inscritos():
    return [chat for chat, ativo in ler(ARQUIVO_USUARIOS, {}).items() if ativo is True]

def alterar_inscricao(chat_id, ativo):
    dados = ler(ARQUIVO_USUARIOS, {})
    dados[str(chat_id)] = bool(ativo)
    salvar(ARQUIVO_USUARIOS, dados)

"""Formatação HTML para Telegram, com preferência por suporte remoto."""
from datetime import datetime
from html import escape
from config.configuracoes import LINKEDIN
from servicos.prioridades import rotulo_prioridade

RODAPE = f'💻 Desenvolvido por Diego Leam\n🔗 <a href="{LINKEDIN}">Conheça meus projetos no LinkedIn</a>'


def com_rodape(corpo):
    return corpo + '\n\n' + RODAPE


def data_legivel(valor):
    if not valor:
        return 'Não informada'
    try:
        # A API usa UTC; converter para o horário de Brasília (UTC-3).
        from datetime import timezone, timedelta
        data = datetime.fromisoformat(str(valor).replace('Z', '+00:00'))
        if data.tzinfo:
            data = data.astimezone(timezone(timedelta(hours=-3)))
        return data.strftime('%d/%m/%Y às %H:%M (Brasília)')
    except (ValueError, TypeError):
        return str(valor)


def mensagem_vaga(v):
    """Recebe dicionário de vaga; nunca incorpora HTML não escapado."""
    def campo(chave):
        return escape(str(v.get(chave) or 'Não informado'))
    cabecalho = escape(rotulo_prioridade(v))
    publicacao = escape(data_legivel(v.get('publicada_em')))
    link = escape(str(v.get('url') or ''), quote=True)
    corpo = (f'<b>{cabecalho}</b>\n\n'
             f'💼 <b>Cargo:</b> {campo("titulo")}\n'
             f'🏢 <b>Empresa:</b> {campo("empresa")}\n'
             f'🏠 <b>Modalidade:</b> {campo("modalidade")}\n'
             f'📍 <b>Localização:</b> {campo("localizacao")}\n'
             f'📅 <b>Publicação:</b> {publicacao}\n'
             f'🌐 <b>Portal:</b> {campo("portal")}\n'
             f'🔗 <a href="{link}">Ver oportunidade</a>')
    return com_rodape(corpo)

"""Coletor experimental 2via: usa RSS público, se disponível.

IMPORTANTE: feed e estrutura podem mudar; testar contra o site antes de produção.
Não contorna bloqueios nem autenticação.
"""
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from config.configuracoes import VIA2_FEED
from coletores.base import requisitar
from servicos.modelos import Vaga
from servicos.filtros import eh_ti

def coletar():
    resposta = requisitar(VIA2_FEED)
    raiz = ET.fromstring(resposta.content)
    vagas = []
    for item in raiz.findall('.//channel/item'):
        titulo = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        data = item.findtext('pubDate')
        if not titulo or not link or not eh_ti(titulo): continue
        publicada = None
        if data:
            try: publicada = parsedate_to_datetime(data).astimezone(timezone.utc).isoformat()
            except (TypeError, ValueError): pass
        vagas.append(Vaga(portal='2via', titulo=titulo, empresa='Não informada', url=link,
                          publicada_em=publicada))
    if raiz.find('.//channel') is None:
        raise RuntimeError('A resposta da 2via não parece um feed RSS válido')
    return vagas

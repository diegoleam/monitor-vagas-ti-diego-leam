"""Formato único: todo coletor entrega uma lista de Vaga."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import hashlib

def url_limpa(url: str) -> str:
    """Remove parâmetros de rastreamento, preservando parâmetros úteis."""
    u = urlsplit(url.strip())
    pares = [(k,v) for k,v in parse_qsl(u.query) if not k.lower().startswith('utm_')]
    return urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path.rstrip('/'),urlencode(pares),''))

@dataclass
class Vaga:
    portal: str
    titulo: str
    empresa: str
    url: str
    publicada_em: str | None = None  # ISO-8601, se o portal fornecer
    modalidade: str = 'Não informada'
    localizacao: str = 'Não informada'
    identificada_em: str = ''
    id: str = ''
    def __post_init__(self):
        self.url = url_limpa(self.url)
        if not self.identificada_em:
            self.identificada_em = datetime.now(timezone.utc).isoformat()
        if not self.id:
            # Identificador estável; mesmo link em portais distintos pode gerar IDs diferentes.
            self.id = hashlib.sha256(self.url.encode('utf-8')).hexdigest()[:24]
    def dicionario(self): return asdict(self)

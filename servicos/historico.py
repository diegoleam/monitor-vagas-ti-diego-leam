"""Persistência JSON com escrita atômica e expiração de registros."""
import json, os, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from config.configuracoes import DIAS_VAGAS, DIAS_HISTORICO

def ler(caminho: Path, padrao):
    if not caminho.exists(): return padrao
    try:
        return json.loads(caminho.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise RuntimeError(f'JSON inválido em {caminho}; não será sobrescrito') from erro

def salvar(caminho: Path, dados):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    # Substituição atômica reduz risco de arquivo parcialmente gravado.
    fd, temporario = tempfile.mkstemp(dir=caminho.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        os.replace(temporario, caminho)
    finally:
        if os.path.exists(temporario): os.unlink(temporario)

def recente(iso, dias):
    if not iso: return False
    try:
        data = datetime.fromisoformat(iso.replace('Z', '+00:00'))
        if data.tzinfo is None: data = data.replace(tzinfo=timezone.utc)
        return data >= datetime.now(timezone.utc) - timedelta(days=dias)
    except ValueError: return False

def atualizar(vagas_novas, caminho_vagas, caminho_historico, dias_vagas=DIAS_VAGAS):
    """Retorna somente vagas inéditas. Não envia Telegram aqui."""
    atuais = ler(caminho_vagas, [])
    historico = ler(caminho_historico, {})
    atuais = [v for v in atuais if recente(v.get('publicada_em') or v.get('identificada_em'), dias_vagas)]
    historico = {k:v for k,v in historico.items() if recente(v, DIAS_HISTORICO)}
    ids = {v['id'] for v in atuais}
    novas = []
    for vaga in vagas_novas:
        v = vaga.dicionario()
        if v['id'] not in ids and v['id'] not in historico:
            # Não confundir 'primeira descoberta' com 'publicação'.
            if v['publicada_em'] and not recente(v['publicada_em'], dias_vagas): continue
            atuais.append(v); ids.add(v['id']); novas.append(v)
    salvar(caminho_vagas, atuais)
    salvar(caminho_historico, historico)
    return novas

def marcar_notificadas(vagas, caminho_historico):
    historico = ler(caminho_historico, {})
    agora = datetime.now(timezone.utc).isoformat()
    for v in vagas: historico[v['id']] = agora
    salvar(caminho_historico, historico)


def listar_pendentes(caminho_vagas, caminho_historico):
    """Retorna vagas descobertas e ainda sem confirmação de envio.

    Consulta o JSON persistido, inclusive após reiniciar o programa.
    Não altera os arquivos e não chama o Telegram.
    """
    vagas = ler(caminho_vagas, [])
    notificadas = ler(caminho_historico, {})
    return [vaga for vaga in vagas if vaga.get('id') and vaga['id'] not in notificadas]

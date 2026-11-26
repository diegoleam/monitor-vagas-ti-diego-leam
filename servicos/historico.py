
"""Persistência JSON com escrita atômica e expiração de registros.

Monitor Vagas TI — Diego Tech

Funcionalidades:
- Leitura e gravação segura de arquivos JSON.
- Controle de vagas já identificadas.
- Histórico de notificações para evitar duplicidades.
- Limpeza de registros conforme configuração existente.
- Notificação apenas de vagas publicadas nas últimas 48 horas.
- Bloqueio de vagas antigas que ainda estejam pendentes.
- Compatibilidade com as funções já utilizadas pelo projeto.
"""

import json
import os
import tempfile

from datetime import datetime, timedelta, timezone
from pathlib import Path

from config.configuracoes import DIAS_VAGAS, DIAS_HISTORICO


# ============================================================
# CONFIGURAÇÃO DO FILTRO DE PUBLICAÇÃO
# ============================================================

# Somente vagas publicadas nas últimas 48 horas
# poderão entrar na fila de notificações.
HORAS_MAXIMAS_PUBLICACAO = 48


# ============================================================
# LEITURA DO JSON
# ============================================================

def ler(caminho: Path, padrao):
    """Lê o arquivo JSON sem sobrescrever dados inválidos."""

    if not caminho.exists():
        return padrao

    try:
        return json.loads(
            caminho.read_text(encoding='utf-8')
        )

    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise RuntimeError(
            f'JSON inválido em {caminho}; não será sobrescrito'
        ) from erro


# ============================================================
# SALVAMENTO ATÔMICO
# ============================================================

def salvar(caminho: Path, dados):
    """Salva JSON de forma atômica para reduzir riscos de corrupção."""

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fd, temporario = tempfile.mkstemp(
        dir=caminho.parent,
        suffix='.tmp'
    )

    try:
        with os.fdopen(
            fd,
            'w',
            encoding='utf-8'
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=2
            )

        os.replace(
            temporario,
            caminho
        )

    finally:
        if os.path.exists(temporario):
            os.unlink(temporario)


# ============================================================
# CONVERSÃO SEGURA DE DATAS
# ============================================================

def converter_data(iso):
    """Converte datas ISO 8601 para UTC.

    Aceita:
    - Datas com Z.
    - Datas com fuso horário.
    - Datas sem fuso, interpretadas como UTC.

    Retorna None quando a data é inválida.
    """

    if not iso:
        return None

    try:
        data = datetime.fromisoformat(
            str(iso).strip().replace('Z', '+00:00')
        )

        if data.tzinfo is None:
            data = data.replace(
                tzinfo=timezone.utc
            )

        return data.astimezone(
            timezone.utc
        )

    except (ValueError, TypeError, OverflowError):
        return None


# ============================================================
# VERIFICAÇÃO DE RECÊNCIA
# ============================================================

def recente(iso, dias):
    """Verifica se uma data está dentro do período informado.

    Mantida para compatibilidade com o projeto original.
    """

    data = converter_data(iso)

    if data is None:
        return False

    agora = datetime.now(timezone.utc)

    return (
        agora - timedelta(days=dias)
        <= data
        <= agora
    )


# ============================================================
# NOVA REGRA: PUBLICAÇÃO NAS ÚLTIMAS 48 HORAS
# ============================================================

def publicada_nas_ultimas_48h(iso):
    """Verifica se a vaga foi publicada nas últimas 48 horas.

    Regras:
    - Aceita publicações dentro das últimas 48 horas.
    - Rejeita publicações anteriores a esse período.
    - Rejeita datas futuras.
    - Rejeita datas ausentes ou inválidas.
    - Não utiliza a data de descoberta como publicação.
    """

    data_publicacao = converter_data(iso)

    if data_publicacao is None:
        return False

    agora = datetime.now(timezone.utc)

    limite = agora - timedelta(
        hours=HORAS_MAXIMAS_PUBLICACAO
    )

    return limite <= data_publicacao <= agora


# ============================================================
# ATUALIZAÇÃO DE VAGAS E HISTÓRICO
# ============================================================

def atualizar(
    vagas_novas,
    caminho_vagas,
    caminho_historico,
    dias_vagas=DIAS_VAGAS
):
    """Atualiza os registros e retorna somente vagas inéditas.

    Preserva:
    - Deduplicação por ID.
    - Histórico de notificações.
    - Retenção configurada.
    - Salvamento atômico.

    Nova regra:
    - Somente vagas publicadas nas últimas 48 horas
      poderão ser adicionadas à fila de notificações.
    """

    atuais = ler(
        caminho_vagas,
        []
    )

    historico = ler(
        caminho_historico,
        {}
    )

    # Mantém a política original de retenção de vagas.
    # Registros antigos continuam sendo removidos conforme
    # DIAS_VAGAS, sem confundir descoberta com publicação.
    atuais = [
        vaga for vaga in atuais
        if recente(
            vaga.get('publicada_em')
            or vaga.get('identificada_em'),
            dias_vagas
        )
    ]

    # Mantém a retenção original do histórico de notificações.
    historico = {
        chave: data
        for chave, data in historico.items()
        if recente(
            data,
            DIAS_HISTORICO
        )
    }

    ids = {
        vaga['id']
        for vaga in atuais
    }

    novas = []

    for vaga in vagas_novas:

        dados_vaga = vaga.dicionario()

        identificador = dados_vaga['id']

        # Evita duplicidade na lista atual.
        if identificador in ids:
            continue

        # Evita notificar vagas já registradas no histórico.
        if identificador in historico:
            continue

        # NOVO FILTRO:
        # Só aceita vagas com publicação comprovada
        # dentro das últimas 48 horas.
        if not publicada_nas_ultimas_48h(
            dados_vaga.get('publicada_em')
        ):
            continue

        atuais.append(
            dados_vaga
        )

        ids.add(
            identificador
        )

        novas.append(
            dados_vaga
        )

    # Preserva o salvamento original dos arquivos.
    salvar(
        caminho_vagas,
        atuais
    )

    salvar(
        caminho_historico,
        historico
    )

    return novas


# ============================================================
# REGISTRO DE VAGAS NOTIFICADAS
# ============================================================

def marcar_notificadas(
    vagas,
    caminho_historico
):
    """Registra as vagas notificadas para evitar novos envios."""

    historico = ler(
        caminho_historico,
        {}
    )

    agora = datetime.now(
        timezone.utc
    ).isoformat()

    for vaga in vagas:
        historico[vaga['id']] = agora

    salvar(
        caminho_historico,
        historico
    )


# ============================================================
# RECUPERAÇÃO DE VAGAS PENDENTES
# ============================================================

def listar_pendentes(
    caminho_vagas,
    caminho_historico
):
    """Retorna vagas ainda não notificadas.

    Preserva:
    - Leitura dos registros persistidos.
    - Verificação do histórico de notificações.
    - Ausência de alterações nos arquivos.
    - Ausência de chamadas ao Telegram.

    Nova regra:
    - Impede o envio de vagas publicadas há mais
      de 48 horas, mesmo que já estejam armazenadas.
    """

    vagas = ler(
        caminho_vagas,
        []
    )

    notificadas = ler(
        caminho_historico,
        {}
    )

    pendentes = []

    for vaga in vagas:

        identificador = vaga.get('id')

        if not identificador:
            continue

        # Vaga já notificada anteriormente.
        if identificador in notificadas:
            continue

        # Impede recuperar vagas antigas da fila.
        if not publicada_nas_ultimas_48h(
            vaga.get('publicada_em')
        ):
            continue

        pendentes.append(
            vaga
        )

    return pendentes

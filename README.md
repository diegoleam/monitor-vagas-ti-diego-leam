# Monitor Vagas TI — Diego Leam | v0.4 integrada

Projeto independente do Monitor IFs — Diego Tech. Esta pasta reúne os arquivos originais e as melhorias das versões v0.2/v0.3, mais a priorização de suporte remoto.

## Funcionalidades

- Gupy: busca geral por publicação e buscas complementares (`suporte`, `desenvolvedor`, `estágio`, `infraestrutura`, `dados`, `redes`), sem filtro geográfico ou de modalidade.
- Dicionário/classificador de TI abrangente, inclusive estágios, aprendiz e cargos em inglês.
- Ordenação: **suporte remoto** > outras vagas remotas > híbridas > presenciais > modalidade desconhecida. Nenhuma vaga é excluída por prioridade.
- Mensagem HTML do Telegram com prioridade, data legível, link e assinatura **Desenvolvido por Diego Leam**.
- 2via preservado do projeto original; seu funcionamento online ainda requer validação independente.
- Histórico JSON local e testes isolados. Workflow GitHub Actions permanece **em modo seguro**, sem envio real.

## Instalação no Windows / VS Code

1. Faça backup do projeto atual. Extraia a pasta `monitor_vagas_diego_leam` e substitua a pasta antiga, **preservando seu `.env` e os arquivos JSON de `dados/`**.
2. No terminal, na raiz do projeto, instale dependências: `python -m pip install -r requirements.txt`.
3. Teste, nesta ordem:

```powershell
python -m testes.testar_classificador_ti
python -m testes.testar_prioridades
python -m testes.testar_gupy_simulado
python -m testes.testar_gupy_json
python -m testes.testar_gupy_online
python -m pytest -q
python main.py --portal gupy
```

O último comando é uma simulação: não envia mensagens e não altera o histórico.

## Avisos antes da produção

- O endpoint da Gupy foi validado no ambiente do usuário, mas disponibilidade e condições de uso podem mudar. Não contornar bloqueios do portal.
- O Telegram `/start`, `/ajuda` e `/parar` ainda não estão ativados; o cadastro de inscritos exige implementação/testes adicionais.
- A persistência dos JSON **entre execuções do GitHub Actions** ainda não está resolvida; não ativar o envio automático até isso ser validado.
- O histórico inicial e entregas parciais por usuário ainda precisam de testes de ponta a ponta. **Não execute `python main.py --enviar` sem configurar e validar isso.**
- A coleta não garante capturar todas as vagas da plataforma, pois a busca é paginada e limitada.

**Desenvolvido por Diego Leam** — https://www.linkedin.com/in/diegoleam

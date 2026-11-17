"""Teste local do dicionário: inclui estágio e evita falso positivo óbvio."""
from servicos.classificador_ti import classificar

positivas = [
    ('Estágio em TI', ''), ('Pessoa Estagiária de Suporte', 'Atuação em help desk'),
    ('IT Support Specialist', ''), ('Desenvolvedor Full Stack', ''),
    ('Analista de Redes', ''), ('Estágio em Segurança da Informação', ''),
    ('Analista de Suporte Sistemas Junior', ''),
    ('Estágio em Dados', 'Atuação com Python, SQL e banco de dados'),
]
negativas = [
    ('Suporte ao Cliente', 'Atendimento de clientes e uso de Excel'),
    ('Estágio em Marketing', 'Criação de campanhas'),
    ('Analista Comercial', 'Relatórios em Excel'),
]
for titulo, descricao in positivas:
    classe, motivo = classificar(titulo, descricao)
    assert classe != 'nao_identificada', (titulo, motivo)
for titulo, descricao in negativas:
    classe, motivo = classificar(titulo, descricao)
    assert classe == 'nao_identificada', (titulo, motivo)
print('TESTE DO DICIONÁRIO APROVADO: estágios e cargos de TI reconhecidos')

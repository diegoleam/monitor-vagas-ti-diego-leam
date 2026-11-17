"""Vocabulário extensível de TI. Termos normalizados sem acentos.

Não trate palavras isoladas como 'dados', 'suporte' ou 'estagio' como prova de TI.
"""
CARGOS_TI = (
    'tecnologia da informacao', 'informatica', 'analista de ti', 'tecnico de ti',
    'estagio em ti', 'estagiario de ti', 'estagiaria de ti', 'aprendiz de ti',
    'estagio em tecnologia da informacao', 'estagio em informatica',
    'estagio em desenvolvimento', 'estagio em programacao', 'estagio em redes',
    'estagio em infraestrutura', 'estagio em seguranca da informacao',
    'estagio em ciencia de dados', 'estagio em engenharia de software',
    'estagio em sistemas', 'estagio em suporte tecnico',
    'suporte tecnico', 'suporte de sistemas', 'suporte sistemas',
    'suporte n1', 'suporte n2', 'suporte n3', 'suporte jr', 'suporte pl',
    'help desk', 'service desk', 'it support', 'technical support',
    'desenvolvedor', 'desenvolvedora', 'developer', 'programador', 'programadora',
    'software engineer', 'engenheiro de software', 'engenheira de software',
    'front end', 'back end', 'full stack', 'frontend', 'backend', 'fullstack',
    'mobile developer', 'analista de sistemas', 'system analyst',
    'analista de infraestrutura', 'administrador de sistemas', 'sysadmin',
    'analista de redes', 'administrador de redes', 'network engineer',
    'redes de computadores', 'noc', 'devops', 'site reliability engineer', 'sre',
    'cloud engineer', 'cloud architect', 'engenheiro de nuvem',
    'seguranca da informacao', 'ciberseguranca', 'cybersecurity',
    'security engineer', 'analista soc', 'pentest', 'analista de dados',
    'cientista de dados', 'engenheiro de dados', 'data analyst', 'data engineer',
    'data scientist', 'business intelligence', 'analista de bi',
    'administrador de banco de dados', 'database administrator', 'dba',
    'qa engineer', 'quality assurance', 'testes de software', 'tester de software',
    'automacao de testes', 'analista de qualidade de software',
    'analista de sustentacao', 'sustentacao de sistemas', 'analista de erp',
    'consultor sap', 'consultora sap', 'analista protheus',
    'tech lead', 'lider tecnico', 'lider tecnica', 'coordenador de ti',
    'coordenadora de ti', 'gerente de ti', 'gerente de tecnologia',
    'product owner tecnico', 'product owner tecnica',
)
# Termos fortes para identificar TI na descrição de títulos genéricos.
CONTEXTO_FORTE = (
    'tecnologia da informacao', 'suporte tecnico', 'help desk', 'service desk',
    'desenvolvimento de software', 'engenharia de software', 'sistemas de informacao',
    'redes de computadores', 'seguranca da informacao', 'infraestrutura de ti',
    'banco de dados', 'programacao', 'desenvolvimento web', 'automacao de testes',
    'analise de sistemas', 'administracao de sistemas',
)
CONTEXTO_TECNICO = (
    'python', 'javascript', 'typescript', 'java', 'sql', 'linux', 'windows server',
    'active directory', 'api', 'apis', 'docker', 'kubernetes', 'aws', 'azure',
    'git', 'github', 'firewall', 'servidores', 'software', 'hardware',
    'sistemas', 'cloud', 'cisco', 'mikrotik', 'power bi', 'etl', 'erp',
)
TITULOS_AMBIGUOS = (
    'suporte', 'sustentacao', 'estagio', 'estagiario', 'estagiaria',
    'intern', 'internship', 'trainee', 'aprendiz', 'analista de operacoes',
    'analista de atendimento', 'analista de implantacao',
)
# Para impedir que 'suporte ao cliente' seja aceito apenas por citar sistemas.
CONTEXTO_GENERICO = ('excel', 'office', 'atendimento', 'cliente', 'clientes')

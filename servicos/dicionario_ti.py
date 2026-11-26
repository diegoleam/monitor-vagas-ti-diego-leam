"""Vocabulário extensível de TI. Termos normalizados sem acentos.

Não trate palavras isoladas como 'dados', 'suporte' ou 'estagio' como prova de TI.
"""
CARGOS_TI = (
    # --- SEUS TERMOS ORIGINAIS (MANTIDOS INTEGRALMENTE) ---
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

    # --- NOVAS ADIÇÕES: TÉCNICOS (INFORMÁTICA, REDES, CAMPO, HARDWARE) ---
    'tecnica de ti', 'tecnico em ti', 'tecnica em ti',
    'tecnico de informatica', 'tecnica de informatica',
    'tecnico em informatica', 'tecnica em informatica',
    'tecnico de redes', 'tecnica de redes',
    'tecnico em redes', 'tecnica em redes',
    'tecnico de redes de computadores', 'tecnico em redes de computadores',
    'tecnico de infraestrutura', 'tecnico em infraestrutura',
    'tecnico de suporte', 'tecnica de suporte',
    'tecnico em suporte', 'tecnica em suporte',
    'tecnico de sistemas', 'tecnico em sistemas',
    'tecnico de campo', 'field service', 'analista de field service',
    'tecnico de hardware', 'tecnico em hardware',
    'tecnico de manutencao de computadores', 'tecnico em manutencao de computadores',
    'tecnico de telecomunicacoes', 'tecnico em telecomunicacoes', 'tecnico telecom',
    'tecnico de fibra optica', 'tecnico em fibra optica', 'instalador de fibra',
    'tecnico de cftv', 'tecnico em cftv', 'tecnico de datacenter',

    # --- NOVAS ADIÇÕES: ENTRADA, ESTÁGIO E SUPORTE ---
    'analista ti', 'assistente de ti', 'assistente ti', 'auxiliar de ti', 'auxiliar ti',
    'estagio de ti', 'estagiario em ti', 'estagiaria em ti', 'jovem aprendiz ti',
    'estagiario de informatica', 'estagiaria de informatica',
    'estagiario de redes', 'estagiaria de redes',
    'estagiario de infraestrutura', 'estagiaria de infraestrutura',
    'estagiario de suporte tecnico',
    'suporte de ti', 'suporte em ti', 'suporte de redes', 'suporte de infraestrutura',
    'suporte computacional', 'suporte local', 'suporte presencial', 'suporte remoto',
    'suporte ao usuario', 'suporte nivel 1', 'suporte nivel 2', 'suporte nivel 3',
    'suporte junior', 'suporte pleno', 'suporte sr',
    'analista de suporte', 'analista de suporte tecnico',
    'helpdesk', 'servicedesk', 'desktop support',
    'analista noc', 'operador de noc', 'engenheiro de redes', 'engenheira de redes',
)

# Termos fortes para identificar TI na descrição de títulos genéricos.
CONTEXTO_FORTE = (
    # --- SEUS TERMOS ORIGINAIS ---
    'tecnologia da informacao', 'suporte tecnico', 'help desk', 'service desk',
    'desenvolvimento de software', 'engenharia de software', 'sistemas de informacao',
    'redes de computadores', 'seguranca da informacao', 'infraestrutura de ti',
    'banco de dados', 'programacao', 'desenvolvimento web', 'automacao de testes',
    'analise de sistemas', 'administracao de sistemas',

    # --- NOVAS ADIÇÕES ---
    'helpdesk', 'servicedesk', 'manutencao de computadores', 'manutencao de hardware',
    'field service', 'cabeamento estruturado', 'configuracao de redes',
    'suporte ao usuario', 'gestao de ativos de ti', 'administracao de redes',
)

CONTEXTO_TECNICO = (
    # --- SEUS TERMOS ORIGINAIS ---
    'python', 'javascript', 'typescript', 'java', 'sql', 'linux', 'windows server',
    'active directory', 'api', 'apis', 'docker', 'kubernetes', 'aws', 'azure',
    'git', 'github', 'firewall', 'servidores', 'software', 'hardware',
    'sistemas', 'cloud', 'cisco', 'mikrotik', 'power bi', 'etl', 'erp',

    # --- NOVAS ADIÇÕES (INFRA, REDES, SUPORTE E FERRAMENTAS) ---
    'ubuntu', 'debian', 'centos', 'macos', 'azure ad', 'entra id',
    'vmware', 'hyper-v', 'proxmox', 'office 365', 'microsoft 365', 'intune',
    'glpi', 'jira', 'zabbix', 'grafana', 'ubiquiti', 'unifi', 'fortigate', 'pfsense',
    'tcp/ip', 'dns', 'dhcp', 'vpn', 'vlan', 'wan', 'lan', 'wi-fi',
    'switch', 'switches', 'roteador', 'roteadores', 'access point',
    'fibra optica', 'patch panel', 'rack', 'nobreak', 'impressoras',
    'formatacao', 'backup', 'antivirus', 'endpoint',
)

TITULOS_AMBIGUOS = (
    # --- SEUS TERMOS ORIGINAIS ---
    'suporte', 'sustentacao', 'estagio', 'estagiario', 'estagiaria',
    'intern', 'internship', 'trainee', 'aprendiz', 'analista de operacoes',
    'analista de atendimento', 'analista de implantacao',

    # --- NOVAS ADIÇÕES (PARA DESAMBIGUAR VAGAS GENÉRICAS PELO CONTEXTO) ---
    'tecnico', 'tecnica', 'assistente', 'auxiliar', 'instalador',
)

# Para impedir que 'suporte ao cliente' seja aceito apenas por citar sistemas.
CONTEXTO_GENERICO = ('excel', 'office', 'atendimento', 'cliente', 'clientes')

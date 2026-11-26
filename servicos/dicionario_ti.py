"""Vocabulário extensível para classificação de vagas de Tecnologia da Informação.

Os termos são armazenados em minúsculas e sem acentos para serem compatíveis
com o normalizador utilizado pelo projeto.

IMPORTANTE:
- CARGOS_TI contém títulos e expressões de busca; alguns são ambíguos.
- TITULOS_AMBIGUOS e TERMOS_EXIGEM_CONTEXTO sinalizam expressões que
  precisam de confirmação por contexto técnico no classificador.
- Adicionar termos a este arquivo não altera, por si só, a lógica de classificação
  nem as consultas realizadas aos portais de emprego.
"""

CARGOS_TI = (
    # --- TERMOS ORIGINAIS (PRESERVADOS) ---
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

    # --- TECNICOS, INFORMATICA, REDES, CAMPO E HARDWARE (PRESERVADOS) ---
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

    # --- ENTRADA, ESTAGIO E SUPORTE (PRESERVADOS) ---
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

    # --- NOVO: MANUTENCAO E SUPORTE EM INFORMATICA ---
    'tecnico em manutencao e suporte em informatica',
    'tecnica em manutencao e suporte em informatica',
    'tecnico de manutencao e suporte em informatica',
    'tecnica de manutencao e suporte em informatica',
    'tecnico em manutencao e suporte de informatica',
    'tecnica em manutencao e suporte de informatica',
    'tecnico de manutencao e suporte de informatica',
    'tecnica de manutencao e suporte de informatica',
    'tecnico em manutencao e suporte', 'tecnica em manutencao e suporte',
    'tecnico de manutencao e suporte', 'tecnica de manutencao e suporte',
    'manutencao e suporte em informatica',
    'manutencao e suporte de informatica',
    'manutencao de computadores', 'manutencao de microcomputadores',
    'manutencao de equipamentos de informatica',
    'tecnico de microinformatica', 'tecnico em microinformatica',
    'tecnica de microinformatica', 'tecnica em microinformatica',
    'tecnico de microcomputadores', 'tecnico em microcomputadores',
    'tecnico de suporte em informatica', 'tecnico de suporte de informatica',
    'tecnico em suporte de informatica', 'tecnico em suporte em informatica',
    'tecnica de suporte em informatica', 'tecnica em suporte de informatica',
    'analista de suporte em informatica', 'assistente de informatica',
    'auxiliar de informatica', 'auxiliar tecnico de informatica',
    'auxiliar tecnico em informatica', 'operador de microcomputador',
    'operador de microcomputadores',
    'tecnico em manutencao de hardware', 'tecnico de manutencao de hardware',
    'tecnico de suporte de computadores', 'tecnico em suporte de computadores',
    'tecnico de suporte de ti', 'tecnico em suporte de ti',
    'tecnico de suporte n1', 'tecnico de suporte n2',
    'analista de suporte n1', 'analista de suporte n2',
    'analista de suporte n3', 'suporte de informatica',
    'suporte em informatica', 'suporte de microinformatica',
    'suporte em microinformatica',

    # --- NOVO: ESTAGIOS DE TI MAIS ESPECIFICOS ---
    'estagio em manutencao e suporte em informatica',
    'estagio em manutencao de computadores',
    'estagio em suporte de ti', 'estagio em suporte de informatica',
    'estagio em suporte de sistemas', 'estagio em suporte de redes',
    'estagio em redes de computadores',
    'estagio em infraestrutura de ti', 'estagio em infraestrutura de redes',
    'estagio em tecnologia', 'estagio em sistemas de informacao',
    'estagio em analise e desenvolvimento de sistemas',
    'estagio em desenvolvimento de software',
    'estagio em desenvolvimento web', 'estagio em desenvolvimento backend',
    'estagio em desenvolvimento frontend', 'estagio em ciencia da computacao',
    'estagio em engenharia da computacao',
    'estagio em engenharia de computacao',
    'estagio em seguranca cibernetica', 'estagio em ciberseguranca',
    'estagio em banco de dados', 'estagio em qa',
    'estagio em testes de software', 'estagio em automacao de testes',
    'estagio em devops', 'estagio em cloud computing',
    'estagio em dados', 'estagio em bi',
    'estagiario em informatica', 'estagiaria em informatica',
    'estagiario em suporte de ti', 'estagiaria em suporte de ti',
    'estagiario em desenvolvimento de software',
    'estagiaria em desenvolvimento de software',
    'estagiario em manutencao e suporte em informatica',
    'estagiaria em manutencao e suporte em informatica',
    'aprendiz em informatica', 'aprendiz em ti',
    'jovem aprendiz em informatica', 'jovem aprendiz em ti',

    # --- NOVO: DESENVOLVIMENTO, AUTOMACAO E INFRAESTRUTURA ---
    'desenvolvedor python', 'desenvolvedora python',
    'desenvolvedor de software', 'desenvolvedora de software',
    'analista desenvolvedor', 'analista desenvolvedora',
    'analista de desenvolvimento de sistemas',
    'analista de automacao de processos', 'desenvolvedor rpa',
    'desenvolvedora rpa', 'analista de rpa',
    'analista de infraestrutura de ti',
    'analista de infraestrutura de redes',
    'analista de microinformatica', 'tecnico de service desk',
    'tecnico de help desk', 'analista de service desk',
    'analista de help desk', 'it technician',
    'computer technician', 'desktop technician',
    'network technician', 'it helpdesk', 'it service desk',
)

CONTEXTO_FORTE = (
    # --- TERMOS ORIGINAIS (PRESERVADOS) ---
    'tecnologia da informacao', 'suporte tecnico', 'help desk', 'service desk',
    'desenvolvimento de software', 'engenharia de software', 'sistemas de informacao',
    'redes de computadores', 'seguranca da informacao', 'infraestrutura de ti',
    'banco de dados', 'programacao', 'desenvolvimento web', 'automacao de testes',
    'analise de sistemas', 'administracao de sistemas',
    'helpdesk', 'servicedesk', 'manutencao de computadores', 'manutencao de hardware',
    'field service', 'cabeamento estruturado', 'configuracao de redes',
    'suporte ao usuario', 'gestao de ativos de ti', 'administracao de redes',

    # --- NOVO: EVIDENCIAS MAIS ESPECIFICAS ---
    'manutencao e suporte em informatica',
    'manutencao e suporte de informatica',
    'suporte em informatica', 'suporte de informatica',
    'suporte de ti', 'suporte em ti',
    'suporte a computadores', 'suporte a microcomputadores',
    'manutencao de microcomputadores',
    'manutencao de equipamentos de informatica',
    'microinformatica', 'montagem de computadores',
    'diagnostico de hardware', 'instalacao de sistemas operacionais',
    'configuracao de computadores', 'infraestrutura de redes',
    'administracao de servidores', 'desenvolvimento de sistemas',
    'analise e desenvolvimento de sistemas',
    'engenharia da computacao', 'ciencia da computacao',
    'seguranca cibernetica', 'automacao de processos com python',
)

CONTEXTO_TECNICO = (
    # --- TERMOS ORIGINAIS (PRESERVADOS) ---
    'python', 'javascript', 'typescript', 'java', 'sql', 'linux', 'windows server',
    'active directory', 'api', 'apis', 'docker', 'kubernetes', 'aws', 'azure',
    'git', 'github', 'firewall', 'servidores', 'software', 'hardware',
    'sistemas', 'cloud', 'cisco', 'mikrotik', 'power bi', 'etl', 'erp',
    'ubuntu', 'debian', 'centos', 'macos', 'azure ad', 'entra id',
    'vmware', 'hyper-v', 'proxmox', 'office 365', 'microsoft 365', 'intune',
    'glpi', 'jira', 'zabbix', 'grafana', 'ubiquiti', 'unifi', 'fortigate', 'pfsense',
    'tcp/ip', 'dns', 'dhcp', 'vpn', 'vlan', 'wan', 'lan', 'wi-fi',
    'switch', 'switches', 'roteador', 'roteadores', 'access point',
    'fibra optica', 'patch panel', 'rack', 'nobreak', 'impressoras',
    'formatacao', 'backup', 'antivirus', 'endpoint',

    # --- NOVO: TECNOLOGIAS E FERRAMENTAS ESPECIFICAS ---
    'windows 10', 'windows 11', 'windows server 2022',
    'powershell', 'bash', 'shell script', 'mysql', 'postgresql',
    'sql server', 'mongodb', 'sqlite', 'node.js', 'react',
    'angular', 'vue.js', 'django', 'flask', 'fastapi',
    'spring boot', 'dotnet', 'c#', 'php', 'typescript',
    'ansible', 'terraform', 'jenkins', 'ci/cd', 'github actions',
    'gitlab ci', 'prometheus', 'grafana', 'observabilidade',
    'virtualizacao', 'hypervisor', 'servidor de arquivos',
    'sistema operacional', 'sistemas operacionais',
    'montagem de pc', 'manutencao de pc', 'microcomputadores',
    'desktop', 'notebook', 'impressora de rede',
    'rede local', 'rede corporativa', 'redes tcp/ip',
    'suporte remoto', 'acesso remoto', 'remote desktop',
    'rpa', 'selenium', 'playwright', 'pytest',
)

TITULOS_AMBIGUOS = (
    # --- TERMOS ORIGINAIS (PRESERVADOS) ---
    'suporte', 'sustentacao', 'estagio', 'estagiario', 'estagiaria',
    'intern', 'internship', 'trainee', 'aprendiz', 'analista de operacoes',
    'analista de atendimento', 'analista de implantacao',
    'tecnico', 'tecnica', 'assistente', 'auxiliar', 'instalador',

    # --- NOVO: TERMOS GENERICOS ---
    'desenvolvimento', 'infraestrutura', 'sistemas',
    'tecnologia', 'analista de suporte', 'suporte tecnico',
    'tecnico de campo', 'tecnico de infraestrutura',
)

# Mantido exatamente para compatibilidade com o classificador existente.
CONTEXTO_GENERICO = ('excel', 'office', 'atendimento', 'cliente', 'clientes')

# --- NOVO: LISTA AUXILIAR, OPCIONAL ---
# O classificador atual somente usara esta lista se for adaptado para consulta-la.
# Preservamos os termos em CARGOS_TI para evitar quebra de compatibilidade.
TERMOS_EXIGEM_CONTEXTO = (
    'estagio em desenvolvimento', 'estagio em infraestrutura',
    'estagio em sistemas', 'estagio em tecnologia',
    'estagio em suporte tecnico', 'estagio em dados',
    'estagio em bi', 'estagio em qa',
    'suporte tecnico', 'analista de suporte',
    'tecnico de campo', 'tecnico de infraestrutura',
    'tecnico em infraestrutura', 'tecnico em manutencao e suporte',
    'tecnico de manutencao e suporte',
    'tecnica em manutencao e suporte',
    'tecnica de manutencao e suporte',
)

# -*- coding: utf-8 -*-
"""Conteúdo do site AgroAmbient. Edite aqui textos, serviços, FAQ e artigos; depois rode `python3 build.py`.

Itens marcados com TBD("...") aparecem no site com a etiqueta "a confirmar".
"""

def TBD(text):
    """Marca um conteúdo como pendente de confirmação (aparece com a etiqueta \"a confirmar\")."""
    return "[[" + text + "]]"


# ---------------------------------------------------------------------------
# Configuração geral
# ---------------------------------------------------------------------------
SITE = {
    # Troque para https://www.agroambient.com.br quando o domínio estiver apontado para a Vercel.
    "url": "https://agroambient-site.vercel.app",
    "name": "AgroAmbient",
    "legal_name": "AgroAmbient Assessoria Agroambiental",
    "slogan": "Preservação ambiental, plante esta ideia.",
    "description": "Consultoria ambiental especializada em estudos de fauna terrestre e aquática, licenciamento ambiental e assessoria agroambiental. Base em Rio Paranaíba (MG), atuação em todo o Brasil.",
    "phone": "(34) 3855-1197",
    "phone_e164": "+553438551197",
    "whatsapp_e164": "5534998067566",
    "whatsapp": "(34) 99806-7566",
    "email": "agroambient@gmail.com",
    "street": "Rua Joaquim Lopes da Silva, 291",
    "city": "Rio Paranaíba",
    "region": "MG",
    "postal": "38810-000",
    "geo": (-19.1936, -46.2475),
    "founded": "2015",
    "cnpj": "21.630.431/0001-01",
    "ctf": "7856773",          # Cadastro Técnico Federal do IBAMA
    "crbio": "000944-04/2021", # registro da empresa no CRBio-04
    "founder_title": "Biólogo, mestre e especialista em Zoologia com ênfase em ictiofauna",
    "portfolio_pdf": "/static/portfolio-agroambient-estudos-de-fauna.pdf",
    "facebook": "https://www.facebook.com/AgroAmbient",
    "instagram": "",  # a confirmar
    "founder": "Willian Lopes Silva",
    # Medição. Preencha e publique; com IDs vazios nada do Google é carregado.
    "ga4": "",            # ex.: "G-ABC123XYZ"
    "ads": "",            # ex.: "AW-123456789"
    "ads_lead_label": "", # rótulo da conversão de lead no Google Ads
    "gsc_verification": "",  # código da meta google-site-verification, se usar verificação por HTML
}

WIX = "https://static.wixstatic.com/media/"
F = "/static/fotos/"
# Fotos do portfólio da AgroAmbient (static/fotos). As do Wix ficam só onde o portfólio não tem foto equivalente.
PHOTOS = {
    "equipe": F + "pesquisador-campo.jpg",
    "monitoramento": F + "armadilha-fotografica.jpg",
    "inventario": F + "tamandua-bandeira.jpg",
    "resgate": F + "tamandua-mirim.jpg",
    "ictio": F + "caiaque-reservatorio.jpg",
    "biota": F + "biota-aquatica.jpg",
    "rio": F + "rio-cerrado.jpg",
    "cascavel": F + "cascavel.jpg",
    "eia": F + "eia-rima-campo.jpg",
    "macrofitas": F + "macrofitas.jpg",
    "drone": F + "drone.jpg",
    "necropsia": F + "necropsia-peixes.jpg",
    "amostras": F + "amostras-laboratorio.jpg",
    "manejo": F + "manejo-fauna.jpg",
    "educacao": F + "palestra.jpg",
    "cursos": F + "palestra.jpg",
    "viveiro": WIX + "57a0dc_4b4271099d1f4ad8ad1c32b2cc58fc14.jpg",
    "licenciamento": WIX + "57a0dc_ceb6e89f9adb4707a177bebdee4a3c93.jpg",
    "campo2": WIX + "57a0dc_8ec79b557e4242ab8d326700e71c3d93~mv2.jpg",
}

# Clientes e parceiros (do portfólio)
PARTNERS = ["Mosaic Fertilizantes", "IBAR", "Serra Mar Ambiental", "RHI Magnesita", "Água e Terra Análise Ambiental",
            "Verde Cerrado Consultoria", "EuroChem Fertilizantes Tocantins", "Viver Minas Mineração", "Bio Golden Consultoria Ambiental e Mineral"]
SECTORS = ["Mineração", "Energia", "Agropecuária", "Indústria", "Consultorias e gestão ambiental"]
DIFERENCIAIS = ["Atuação em todo o território nacional", "Alto padrão técnico e científico", "Atendimento personalizado",
                "Cumprimento de prazos", "Equipe qualificada e equipada", "Todos os grupos animais"]

AREAS = [
    ("fauna", "Estudos de fauna", "Levantamentos de fauna terrestre e aquática para licenciamento, condicionantes e obras."),
    ("licenciamento", "Assessoria e licenciamento", "Estudos e documentos exigidos para regularizar o empreendimento, com acompanhamento do processo."),
    ("agro", "Agro e produção", "Assessoria agrícola que une produtividade e conservação do solo, da água e da biodiversidade."),
    ("educacao", "Educação ambiental", "Programas, cursos e palestras para escolas, empresas, produtores e comunidades."),
]

# ---------------------------------------------------------------------------
# Serviços (cada um vira /servicos/<slug>/)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "monitoramento-de-fauna", "area": "fauna", "hero": "cerrado", "photo": "monitoramento",
        "name": "Monitoramento de fauna",
        "title": "Monitoramento de fauna para licenciamento ambiental",
        "short": "Campanhas periódicas para acompanhar como a fauna responde à instalação e à operação do empreendimento.",
        "summary": "O monitoramento de fauna repete o levantamento das mesmas áreas ao longo do tempo, com os mesmos métodos, para mostrar ao órgão ambiental se o empreendimento está afetando as populações de animais e se as medidas de controle funcionam.",
        "intro": [
            "Ele costuma aparecer como condicionante da licença de instalação ou de operação. A diferença para o inventário é o tempo: o inventário retrata a área uma vez, o monitoramento acompanha a mudança.",
            "Planejamos o desenho amostral pensando na comparação: pontos fixos, mesmo esforço por campanha e registros georreferenciados, para que os relatórios sejam comparáveis entre si e respondam ao que o órgão pediu.",
        ],
        "when": [
            "A licença do empreendimento traz condicionante de monitoramento de fauna.",
            "O órgão pediu um Programa de Monitoramento de Fauna dentro do PBA ou do PCA.",
            "Há obras em etapas, supressão de vegetação ou enchimento de reservatório.",
            "A empresa quer dados próprios para acompanhar áreas de reserva ou recuperação.",
        ],
        "how": [
            ("Plano de trabalho", "Definição de grupos, métodos, pontos amostrais e periodicidade (seca e chuva), alinhada à condicionante."),
            ("Autorização de manejo", "Solicitação da autorização para captura, coleta e transporte de fauna junto ao órgão competente, quando há captura."),
            ("Campanhas de campo", "Armadilhas fotográficas, busca ativa, pontos de escuta, armadilhas de interceptação e queda, redes, conforme o grupo."),
            ("Relatórios por campanha e consolidado", "Riqueza, abundância, espécies ameaçadas e endêmicas, comparação entre campanhas e recomendações."),
        ],
        "deliverables": ["Plano de trabalho", "Relatórios de campanha", "Relatório consolidado anual", "Banco de dados e registros fotográficos", "Responsável técnico com anotação de responsabilidade"],
        "faq": [
            ("Com que frequência são feitas as campanhas?", "Depende da condicionante. O mais comum é cobrir a estação seca e a chuvosa em cada ano, para captar a variação sazonal da fauna."),
            ("Qual a diferença entre monitoramento e inventário de fauna?", "O inventário levanta quais espécies existem na área em um momento. O monitoramento repete o levantamento ao longo do tempo para medir mudanças e avaliar impactos."),
        ],
        "related": ["inventario-de-fauna", "resgate-de-fauna", "licenciamento-ambiental"],
    },
    {
        "slug": "inventario-de-fauna", "area": "fauna", "hero": "cerrado", "photo": "inventario",
        "name": "Inventariamento de fauna",
        "title": "Inventário de fauna (levantamento de fauna)",
        "short": "Levantamento das espécies de mamíferos, aves, répteis, anfíbios e peixes da área do empreendimento.",
        "summary": "O inventário de fauna identifica quais espécies vivem na área de influência do empreendimento, com destaque para espécies ameaçadas, endêmicas e de interesse, e serve de base para o diagnóstico do meio biótico.",
        "intro": [
            "É o ponto de partida dos estudos ambientais: sem saber o que existe na área, não é possível avaliar impacto nem propor medidas. O resultado entra no EIA, no RCA ou em outros estudos pedidos no licenciamento.",
            "Combinamos dados secundários (literatura e bases regionais) com campanhas de campo, para que o levantamento seja completo e defensável diante do órgão ambiental.",
        ],
        "when": [
            "O empreendimento precisa de diagnóstico do meio biótico para obter a licença.",
            "O termo de referência do órgão pede levantamento de fauna.",
            "Há pedido de supressão de vegetação nativa.",
            "A propriedade quer conhecer sua fauna para planos de manejo ou certificações.",
        ],
        "how": [
            ("Dados secundários", "Levantamento bibliográfico e de bases de dados para a região, que orienta o esforço em campo."),
            ("Campanhas de campo", "Métodos específicos para cada grupo de fauna, em estações seca e chuvosa quando exigido."),
            ("Identificação", "Identificação taxonômica das espécies e checagem em listas oficiais de ameaça (estadual, nacional e IUCN)."),
            ("Relatório técnico", "Lista de espécies, status de conservação, análise de riqueza e recomendações para o licenciamento."),
        ],
        "deliverables": ["Lista de espécies com status de conservação", "Mapas de pontos amostrais", "Relatório técnico para o órgão", "Registros fotográficos"],
        "faq": [
            ("Quanto tempo leva um inventário de fauna?", "Depende do tamanho da área e do que o termo de referência exige. Quando são pedidas campanhas na seca e na chuva, o estudo acompanha esse calendário."),
            ("O inventário inclui peixes?", "Pode incluir. Quando há cursos d'água ou reservatórios na área, o levantamento da ictiofauna costuma fazer parte do diagnóstico."),
        ],
        "related": ["monitoramento-de-fauna", "estudos-ictiologicos", "diagnostico-ambiental"],
    },
    {
        "slug": "resgate-de-fauna", "area": "fauna", "hero": "cerrado", "photo": "resgate",
        "name": "Resgate de fauna",
        "title": "Resgate e afugentamento de fauna terrestre e aquática",
        "short": "Equipe em campo durante supressão de vegetação, obras e enchimento de reservatórios para afugentar, resgatar e destinar os animais.",
        "summary": "O resgate de fauna acompanha as frentes de obra para afugentar os animais antes da intervenção e, quando necessário, capturá-los, avaliá-los e soltá-los em áreas adequadas, conforme a autorização do órgão ambiental.",
        "intro": [
            "A prioridade é o afugentamento: conduzir os animais para fora da área antes da máquina chegar. O resgate entra para quem não consegue sair sozinho, como filhotes, ninhos, animais de baixa mobilidade e peixes em áreas que secam.",
            "Trabalhamos junto da equipe de obra, com plano de ação, rotas de fuga, áreas de soltura definidas previamente e registro de cada ocorrência.",
        ],
        "when": [
            "Supressão de vegetação autorizada.",
            "Obras lineares, como estradas, linhas de transmissão e dutos.",
            "Enchimento ou esvaziamento de reservatórios e manutenção de barragens.",
            "Drenagem de lagoas, canais e tanques.",
        ],
        "how": [
            ("Plano de resgate", "Programa com métodos, equipe, áreas de soltura e destinação, para aprovação e autorização do órgão."),
            ("Afugentamento", "Vistoria prévia e condução dos animais para áreas vizinhas antes da frente de obra."),
            ("Resgate e triagem", "Captura com técnicas adequadas a cada grupo, avaliação clínica e registro."),
            ("Soltura e relatório", "Soltura em áreas pré-definidas e relatório com todos os registros para o órgão."),
        ],
        "deliverables": ["Programa de afugentamento e resgate", "Equipe técnica acompanhando a obra", "Relatórios de atividades", "Relatório final ao órgão"],
        "faq": [
            ("O resgate de fauna é obrigatório?", "Quando a licença ou a autorização de supressão exige, sim. Em geral é pedido sempre que a intervenção pode atingir animais silvestres."),
            ("Para onde vão os animais resgatados?", "Para áreas de soltura definidas no plano e aprovadas pelo órgão, de preferência próximas e com ambiente semelhante. Animais feridos seguem para atendimento veterinário."),
        ],
        "related": ["monitoramento-de-fauna", "transposicao-de-peixes", "licenciamento-ambiental"],
    },
    {
        "slug": "estudos-ictiologicos", "area": "fauna", "hero": "river", "photo": "ictio",
        "name": "Estudos ictiológicos",
        "title": "Estudos ictiológicos e monitoramento de ictiofauna",
        "short": "Coleta, identificação e análise das comunidades de peixes em rios, reservatórios e barramentos, com especialistas em ecologia e taxonomia.",
        "summary": "Os estudos ictiológicos levantam e monitoram as espécies de peixes de um rio ou reservatório, avaliando como barramentos, captações e lançamentos afetam a ictiofauna, inclusive espécies migradoras.",
        "intro": [
            "Peixes respondem rápido a mudanças na água, por isso são indicadores importantes em empreendimentos hidrelétricos, de irrigação, de mineração e de saneamento.",
            "Nossa equipe tem especialistas em ecologia e taxonomia de peixes, o que garante identificação correta das espécies e análises que fazem sentido para o órgão ambiental.",
        ],
        "when": [
            "PCHs, CGHs, UHEs e barragens de irrigação ou abastecimento.",
            "Licenciamento de captação e lançamento em cursos d'água.",
            "Condicionante de monitoramento de ictiofauna ou de ictioplâncton.",
            "Avaliação de mortandade de peixes.",
        ],
        "how": [
            ("Desenho amostral", "Pontos a montante e a jusante, no reservatório e em tributários, conforme o empreendimento."),
            ("Coleta", "Redes de espera, tarrafas, arrasto e outros métodos autorizados, com padronização de esforço."),
            ("Identificação e biometria", "Identificação taxonômica, medidas, peso e, quando previsto, análise reprodutiva."),
            ("Análise e relatório", "Riqueza, abundância, espécies migradoras e ameaçadas, comparação entre pontos e campanhas."),
        ],
        "deliverables": ["Relatório técnico de ictiofauna", "Lista de espécies e status", "Base de dados biométricos", "Recomendações de manejo"],
        "faq": [
            ("O que é ictiofauna?", "É o conjunto de espécies de peixes de um rio, lago ou região."),
        ],
        "related": ["transposicao-de-peixes", "resgate-de-fauna", "outorga-de-agua"],
    },
    {
        "slug": "transposicao-de-peixes", "area": "fauna", "hero": "river", "photo": "biota",
        "name": "Transposição de peixes",
        "title": "Transposição de peixes em barragens e reservatórios",
        "short": "Planejamento e execução de operações que ajudam os peixes a vencer barramentos e manter seus deslocamentos.",
        "summary": "A transposição de peixes leva os peixes de um lado para o outro de uma barragem, por meio de mecanismos como escadas e elevadores ou por captura e transporte, para manter os deslocamentos de espécies que dependem deles.",
        "intro": [
            "Muitas espécies de peixes de água doce se deslocam ao longo do rio em parte do ciclo de vida. Barramentos interrompem esse caminho, e a transposição é uma das medidas para reduzir o impacto.",
            "Atuamos no planejamento, na operação e no monitoramento da transposição, com equipe que conhece as espécies da bacia.",
        ],
        "when": [
            "Condicionante de licença de barragens e hidrelétricas.",
            "Operação de sistemas de transposição já instalados.",
            "Programas de captura e transporte de peixes a jusante e a montante.",
            "Avaliação da eficiência de mecanismos de transposição.",
        ],
        "how": [
            ("Diagnóstico", "Levantamento das espécies e dos períodos de deslocamento na bacia."),
            ("Plano de operação", "Métodos, calendário, equipe e protocolos de manejo e transporte."),
            ("Operação", "Captura, triagem, transporte e soltura, com registro de cada lote."),
            ("Monitoramento", "Avaliação dos resultados e relatórios ao órgão."),
        ],
        "deliverables": ["Plano de transposição", "Relatórios de operação", "Monitoramento de eficiência"],
        "faq": [
            ("Toda barragem precisa de transposição de peixes?", "Não necessariamente. A exigência depende do licenciamento, das espécies presentes e da legislação aplicável a cada caso."),
        ],
        "related": ["estudos-ictiologicos", "resgate-de-fauna", "monitoramento-de-fauna"],
    },
    {
        "slug": "biota-aquatica-e-ictioplancton", "area": "fauna", "hero": "river", "photo": "biota",
        "name": "Biota aquática e ictioplâncton",
        "title": "Inventário e monitoramento de biota aquática e ictioplâncton",
        "short": "Coleta e análise de comunidades aquáticas, ovos e larvas de peixes em rios e reservatórios.",
        "summary": "Inventariamos e monitoramos a biota aquática (plâncton, macroinvertebrados bentônicos e outras comunidades) e o ictioplâncton, que são os ovos e as larvas de peixes. Esses dados mostram a qualidade ambiental do corpo d'água e onde e quando os peixes se reproduzem.",
        "intro": [
            "A biota aquática responde rápido a mudanças na água, por isso é usada como indicadora nos estudos de barragens, captações, mineração e efluentes.",
            "O ictioplâncton indica áreas e períodos de desova. É informação central para hidrelétricas, sistemas de transposição e planos de conservação de peixes migradores.",
        ],
        "when": [
            "Licenciamento ou condicionante de barragem, PCH ou reservatório.",
            "Programas de monitoramento da qualidade da água com bioindicadores.",
            "Avaliação de áreas de desova e de rotas de peixes migradores.",
        ],
        "how": [
            ("Plano amostral", "Pontos, períodos e métodos de coleta definidos com base no termo de referência."),
            ("Coleta", "Redes de plâncton, amostradores de fundo e coletas noturnas de ictioplâncton, com registro georreferenciado."),
            ("Triagem e identificação", "Separação e identificação em laboratório por especialistas."),
            ("Análise e relatório", "Índices ecológicos, comparação entre campanhas e relatório no formato do órgão."),
        ],
        "deliverables": ["Relatório técnico por campanha", "Banco de dados das coletas", "Mapas dos pontos amostrais", "Responsável técnico"],
        "faq": [
            ("O que é ictioplâncton?", "São os ovos e as larvas de peixes que ficam à deriva na água. Estudá-lo mostra onde e quando os peixes se reproduzem."),
        ],
        "related": ["estudos-ictiologicos", "transposicao-de-peixes", "manejo-de-macrofitas"],
    },
    {
        "slug": "laudos-periciais-e-necropsia", "area": "fauna", "hero": "river", "photo": "necropsia",
        "name": "Laudos periciais e necropsia",
        "title": "Laudos periciais ambientais e necropsia de peixes e outros animais",
        "short": "Laudos técnicos para mortandade de peixes, perícias ambientais e investigação da causa da morte de animais.",
        "summary": "Elaboramos laudos periciais ambientais e laudos de necropsia (autópsia) de peixes e outros animais. Eles ajudam a esclarecer a causa de mortandades e a embasar defesas, processos e respostas ao órgão ambiental.",
        "intro": [
            "Quando há mortandade de peixes ou de outros animais, a resposta rápida faz diferença: a coleta e a conservação das amostras precisam começar cedo para que o laudo seja conclusivo.",
        ],
        "when": [
            "Mortandade de peixes em rios, lagos, tanques ou reservatórios.",
            "Processos judiciais ou administrativos que pedem perícia ambiental.",
            "Investigação de causa de morte de animais silvestres ou de criação.",
        ],
        "how": [
            ("Atendimento à ocorrência", "Vistoria do local, registro fotográfico e coleta de amostras."),
            ("Necropsia e análises", "Exame dos animais em laboratório e, quando necessário, análises complementares."),
            ("Laudo", "Conclusões técnicas fundamentadas, com responsável técnico."),
        ],
        "deliverables": ["Laudo pericial ou de necropsia", "Registro fotográfico", "Cadeia de custódia das amostras", "Responsável técnico"],
        "faq": [],
        "related": ["estudos-ictiologicos", "biota-aquatica-e-ictioplancton", "diagnostico-ambiental"],
    },
    {
        "slug": "licenciamento-ambiental", "area": "licenciamento", "hero": "cerrado", "photo": "licenciamento",
        "name": "Licenciamento ambiental",
        "title": "Licenciamento ambiental em Minas Gerais e em todo o Brasil",
        "short": "Organizamos os estudos, protocolamos e acompanhamos o processo até a emissão da licença.",
        "summary": "Licenciamento ambiental é o procedimento pelo qual o órgão ambiental autoriza a localização, instalação e operação de atividades que usam recursos naturais ou podem causar degradação. Cuidamos dos estudos, do protocolo e do acompanhamento.",
        "intro": [
            "Em Minas Gerais, a modalidade de licenciamento é definida pelo porte e pelo potencial poluidor da atividade, conforme a Deliberação Normativa COPAM nº 217/2017. Pode ser simplificado (LAS), concomitante (LAC) ou trifásico (LAT), com licença prévia, de instalação e de operação.",
            "Começamos entendendo a atividade e enquadrando corretamente o empreendimento. Isso evita estudos desnecessários e pedidos de informação complementar que atrasam a licença.",
        ],
        "when": [
            "Nova atividade agropecuária, industrial, de mineração ou de infraestrutura.",
            "Ampliação ou mudança de uma atividade já licenciada.",
            "Renovação de licença de operação.",
            "Regularização de atividade que opera sem licença.",
        ],
        "how": [
            ("Enquadramento", "Análise da atividade, porte, potencial poluidor e localização para definir a modalidade e o órgão competente."),
            ("Estudos", "Elaboração dos estudos pedidos (RAS, RCA, PCA, EIA/RIMA e outros), incluindo os levantamentos de campo."),
            ("Protocolo", "Montagem e protocolo do processo no sistema do órgão ambiental."),
            ("Acompanhamento", "Respostas a pedidos de informação complementar e acompanhamento das condicionantes depois da licença."),
        ],
        "deliverables": ["Enquadramento do empreendimento", "Estudos ambientais", "Protocolo do processo", "Gestão de condicionantes"],
        "faq": [
            ("Quanto tempo demora uma licença ambiental?", "Varia com a modalidade, o órgão e a qualidade dos estudos. Um processo bem enquadrado e completo reduz os pedidos de complementação, que são a principal causa de atraso."),
            ("Quem emite a licença: município, estado ou União?", "Depende do tipo e da localização do empreendimento. A Lei Complementar nº 140/2011 distribui essa competência entre União, estados e municípios."),
        ],
        "related": ["diagnostico-ambiental", "estudos-tecnicos", "outorga-de-agua"],
    },
    {
        "slug": "outorga-de-agua", "area": "licenciamento", "hero": "river", "photo": "campo2",
        "name": "Outorga de uso de água",
        "title": "Outorga de direito de uso de recursos hídricos",
        "short": "Regularização de captações, barramentos, poços e lançamentos em cursos d'água.",
        "summary": "A outorga é a autorização do poder público para usar água de rios, lagos ou do subsolo, ou para intervir em cursos d'água. Em Minas Gerais, a análise é feita pelo IGAM. Preparamos os estudos e o pedido.",
        "intro": [
            "A outorga é prevista na Política Nacional de Recursos Hídricos (Lei nº 9.433/1997) e, em Minas Gerais, na Lei Estadual nº 13.199/1999. Usos considerados insignificantes também precisam de cadastro.",
            "Para irrigação, dessedentação animal, piscicultura e indústria, a outorga costuma ser exigida junto com o licenciamento ambiental.",
        ],
        "when": [
            "Captação em rio, córrego ou represa.",
            "Perfuração e uso de poço tubular.",
            "Construção de barramento ou travessia em curso d'água.",
            "Lançamento de efluentes.",
            "Renovação ou retificação de outorga existente.",
        ],
        "how": [
            ("Levantamento", "Vistoria, identificação dos usos e da disponibilidade hídrica."),
            ("Estudos", "Cálculo de vazões, estudos hidrológicos e documentação técnica exigida."),
            ("Pedido", "Protocolo do requerimento de outorga ou do cadastro de uso insignificante."),
            ("Acompanhamento", "Respostas ao órgão e controle de prazos de validade."),
        ],
        "deliverables": ["Estudo e requerimento de outorga", "Cadastro de uso insignificante", "Controle de vencimentos"],
        "faq": [
            ("Uso pequeno de água precisa de outorga?", "Usos considerados insignificantes pela regra estadual são dispensados de outorga, mas ainda precisam ser cadastrados."),
        ],
        "related": ["licenciamento-ambiental", "estudos-ictiologicos", "assessoria-agricola"],
    },
    {
        "slug": "diagnostico-ambiental", "area": "licenciamento", "hero": "cerrado", "photo": "rio",
        "name": "Diagnóstico ambiental",
        "title": "Diagnóstico ambiental de áreas e propriedades",
        "short": "Retrato técnico do meio físico e biótico de uma área, para licenciamento, compra de terras ou planejamento.",
        "summary": "O diagnóstico ambiental descreve as condições de uma área (vegetação, fauna, água, solo, áreas protegidas e passivos) para embasar decisões e estudos de licenciamento.",
        "intro": [
            "Serve tanto para o licenciamento quanto para decisões de negócio, como comprar uma área, planejar a expansão de uma lavoura ou identificar passivos antes que virem autuação.",
        ],
        "when": [
            "Fase de planejamento de um empreendimento.",
            "Compra ou arrendamento de propriedade rural.",
            "Identificação de APPs, reserva legal e passivos ambientais.",
            "Base para estudos exigidos pelo órgão.",
        ],
        "how": [
            ("Análise documental", "Mapas, imagens de satélite, CAR e licenças existentes."),
            ("Vistoria de campo", "Verificação de vegetação, fauna, recursos hídricos e uso do solo."),
            ("Relatório", "Diagnóstico com mapas, restrições e recomendações."),
        ],
        "deliverables": ["Relatório de diagnóstico", "Mapas temáticos", "Lista de restrições e recomendações"],
        "faq": [],
        "related": ["inventario-de-fauna", "licenciamento-ambiental", "planos-de-manejo"],
    },
    {
        "slug": "planos-de-manejo", "area": "licenciamento", "hero": "cerrado", "photo": "cascavel",
        "name": "Planos de manejo",
        "title": "Planos de manejo e programas ambientais",
        "short": "Planejamento do uso e da conservação de áreas naturais, reservas e unidades de conservação.",
        "summary": "Um plano de manejo define como uma área natural deve ser usada e conservada, com zoneamento, regras e programas de ação. É exigido para unidades de conservação e útil para reservas particulares.",
        "intro": [
            "Também elaboramos programas ambientais que acompanham a licença, como programas de fauna, de recuperação de áreas e de educação ambiental.",
        ],
        "when": [
            "Criação ou gestão de unidade de conservação, incluindo RPPN.",
            "Programas ambientais exigidos como condicionante.",
            "Planejamento de áreas de reserva legal e APPs.",
        ],
        "how": [
            ("Diagnóstico", "Levantamento do meio físico, biótico e socioeconômico."),
            ("Zoneamento", "Definição de zonas e usos permitidos."),
            ("Programas", "Ações de proteção, pesquisa, uso público e monitoramento."),
        ],
        "deliverables": ["Plano de manejo", "Programas ambientais", "Mapas de zoneamento"],
        "faq": [],
        "related": ["diagnostico-ambiental", "estudos-tecnicos", "educacao-ambiental"],
    },
    {
        "slug": "estudos-tecnicos", "area": "licenciamento", "hero": "cerrado", "photo": "eia",
        "name": "EIA/RIMA, PCA, RAP e outros estudos",
        "title": "Estudos técnicos: EIA/RIMA, PCA, RAP, EVA, PRAD, PTRF e PAE",
        "short": "Elaboração dos estudos e planos técnicos pedidos no licenciamento e na recuperação de áreas.",
        "summary": "Elaboramos os principais estudos exigidos pelos órgãos ambientais: EIA/RIMA para empreendimentos de impacto significativo, PCA e RAP no licenciamento, EVA para avaliar a viabilidade ambiental, PRAD e PTRF para recuperar áreas e vegetação e PAE para situações de emergência.",
        "intro": [
            "Cada sigla corresponde a um documento com finalidade própria. A tabela abaixo resume quando cada um costuma ser pedido.",
        ],
        "table": [
            ("EIA/RIMA", "Estudo de Impacto Ambiental e Relatório de Impacto Ambiental", "Empreendimentos com potencial de impacto significativo (Resolução CONAMA nº 001/1986)."),
            ("PCA", "Plano de Controle Ambiental", "Medidas e programas para controlar os impactos do empreendimento, comum na licença de instalação."),
            ("RAP", "Relatório Ambiental Preliminar", "Estudo simplificado pedido em alguns licenciamentos para atividades de menor impacto."),
            ("EVA", "Estudo de Viabilidade Ambiental", "Avaliação inicial das restrições e dos riscos ambientais antes de decidir pelo projeto ou pelo local."),
            ("PRAD", "Plano de Recuperação de Áreas Degradadas", "Recuperação de áreas alteradas por obra, mineração ou uso agrícola."),
            ("PTRF", "Projeto Técnico de Reconstituição da Flora", "Recomposição de vegetação nativa, compensações e APPs."),
            ("PAE", "Plano de Ação de Emergência", "Barragens e reservatórios, com ações para emergências."),
        ],
        "when": [
            "O termo de referência do órgão pede um desses estudos.",
            "Há auto de infração ou termo de ajuste que exige recuperação.",
            "Compensação ambiental por supressão de vegetação.",
        ],
        "how": [
            ("Termo de referência", "Leitura do que o órgão pede e planejamento do estudo."),
            ("Levantamentos", "Campo, dados secundários e mapeamento."),
            ("Elaboração", "Redação técnica com equipe multidisciplinar."),
            ("Protocolo e respostas", "Entrega ao órgão e respostas a complementações."),
        ],
        "deliverables": ["Estudo completo no formato do órgão", "Mapas e anexos", "Responsável técnico"],
        "faq": [],
        "related": ["licenciamento-ambiental", "planos-de-manejo", "diagnostico-ambiental"],
    },
    {
        "slug": "manejo-de-macrofitas", "area": "licenciamento", "hero": "river", "photo": "macrofitas",
        "name": "Manejo de macrófitas",
        "title": "Manejo de macrófitas aquáticas em reservatórios",
        "short": "Diagnóstico e controle de plantas aquáticas que tomam reservatórios, lagos e canais.",
        "summary": "Macrófitas são plantas aquáticas que, em excesso, cobrem a superfície de reservatórios, prejudicam a qualidade da água, a geração de energia, a captação e o uso múltiplo. Fazemos o diagnóstico das espécies e da área afetada e o plano de manejo para controlá-las.",
        "intro": [
            "O crescimento descontrolado costuma estar ligado ao excesso de nutrientes na água. Por isso o manejo combina a retirada das plantas com o entendimento da causa.",
        ],
        "when": [
            "Reservatórios de hidrelétricas, irrigação ou abastecimento com infestação de plantas aquáticas.",
            "Condicionante de licença que pede monitoramento ou controle de macrófitas.",
            "Problemas em tomadas d'água, bombas ou navegação.",
        ],
        "how": [
            ("Diagnóstico", "Identificação das espécies, mapeamento da área coberta e avaliação da causa."),
            ("Plano de manejo", "Métodos de controle adequados ao local e ao uso da água."),
            ("Acompanhamento", "Monitoramento da área e dos resultados ao longo do tempo."),
        ],
        "deliverables": ["Diagnóstico das macrófitas", "Plano de manejo", "Mapas da infestação", "Relatórios de monitoramento"],
        "faq": [],
        "related": ["biota-aquatica-e-ictioplancton", "mapeamento-com-drone", "diagnostico-ambiental"],
    },
    {
        "slug": "mapeamento-com-drone", "area": "licenciamento", "hero": "cerrado", "photo": "drone",
        "name": "Mapeamento com drone",
        "title": "Aeromapeamento e avaliação ambiental com drone",
        "short": "Imagens aéreas e mapas atualizados para diagnósticos, licenciamento e monitoramento.",
        "summary": "Usamos drones para mapear áreas de estudo, gerar ortofotos atualizadas e acompanhar mudanças no uso do solo, na vegetação, em margens de reservatórios e em áreas em recuperação.",
        "intro": [
            "O drone dá uma visão atual e detalhada da área, mais precisa que imagens de satélite antigas, e ajuda a planejar campanhas de campo e a documentar resultados.",
        ],
        "when": [
            "Diagnóstico ambiental e mapeamento de uso do solo.",
            "Acompanhamento de áreas em recuperação, supressão ou obras.",
            "Mapeamento de macrófitas, margens e áreas de difícil acesso.",
        ],
        "how": [
            ("Planejamento de voo", "Área, resolução e período do levantamento."),
            ("Voo e processamento", "Captura das imagens e geração de ortofotos e mapas."),
            ("Análise", "Interpretação das imagens e integração ao estudo ambiental."),
        ],
        "deliverables": ["Ortofoto da área", "Mapas temáticos", "Relatório de análise"],
        "faq": [],
        "related": ["diagnostico-ambiental", "manejo-de-macrofitas", "estudos-tecnicos"],
    },
    {
        "slug": "assessoria-agricola", "area": "agro", "hero": "cerrado", "photo": "viveiro",
        "name": "Assessoria agrícola",
        "title": "Assessoria agrícola e agroambiental",
        "short": "Apoio técnico ao produtor rural para produzir mais e manter a propriedade regular.",
        "summary": "A assessoria agroambiental une a parte produtiva e a parte ambiental da propriedade rural: regularização (CAR, outorga, licenças), conservação de solo e água e projetos produtivos.",
        "intro": [
            "Nascemos no Alto Paranaíba, uma das regiões agrícolas mais fortes de Minas Gerais. Conhecemos a rotina do produtor e sabemos que regularidade ambiental hoje também abre portas para crédito e mercado.",
        ],
        "when": [
            "Regularização ambiental da propriedade.",
            "Projetos de irrigação que precisam de outorga e licença.",
            "Projetos de piscicultura " + "[[a confirmar]]" + ".",
            "Sistemas agroflorestais " + "[[a confirmar]]" + ".",
        ],
        "how": [
            ("Visita técnica", "Diagnóstico da propriedade e das pendências."),
            ("Plano de ação", "Prioridades, prazos e custos."),
            ("Execução", "Estudos, pedidos e projetos."),
        ],
        "deliverables": ["Diagnóstico da propriedade", "Plano de regularização", "Projetos técnicos"],
        "faq": [],
        "related": ["outorga-de-agua", "licenciamento-ambiental", "diagnostico-ambiental"],
    },
    {
        "slug": "educacao-ambiental", "area": "educacao", "hero": "cerrado", "photo": "educacao",
        "name": "Educação ambiental",
        "title": "Programas de educação ambiental",
        "short": "Programas para comunidades, escolas e trabalhadores, inclusive os exigidos no licenciamento.",
        "summary": "Elaboramos e executamos programas de educação ambiental para empresas, escolas e comunidades, incluindo os programas exigidos como condicionante de licença.",
        "intro": [
            "A educação ambiental faz parte da nossa missão desde o início: instruir a sociedade a respeito da preservação ambiental, aliada ao desenvolvimento econômico e sustentável.",
        ],
        "when": [
            "Condicionante de licença que exige programa de educação ambiental.",
            "Treinamento de trabalhadores de obra sobre fauna e meio ambiente.",
            "Ações em escolas e comunidades do entorno.",
        ],
        "how": [
            ("Diagnóstico do público", "Quem participa e o que precisa aprender."),
            ("Plano do programa", "Temas, atividades, materiais e indicadores."),
            ("Execução e relatório", "Atividades e relatório com resultados para o órgão."),
        ],
        "deliverables": ["Programa de educação ambiental", "Materiais de apoio", "Relatórios de execução"],
        "faq": [],
        "related": ["resgate-de-fauna", "planos-de-manejo", "licenciamento-ambiental"],
    },
]

# ---------------------------------------------------------------------------
# Glossário de siglas (página de serviços e home)
# ---------------------------------------------------------------------------
GLOSS = [
    ["EIA/RIMA", "Estudo de Impacto Ambiental e Relatório de Impacto Ambiental", "Exigido para empreendimentos com potencial de causar impacto significativo. Reúne diagnóstico do meio físico, biótico e socioeconômico, inclusive levantamento de fauna.", "/servicos/estudos-tecnicos/"],
    ["PCA", "Plano de Controle Ambiental", "Conjunto de medidas e programas para controlar os impactos do empreendimento, comum na licença de instalação.", "/servicos/estudos-tecnicos/"],
    ["RAP", "Relatório Ambiental Preliminar", "Estudo simplificado pedido em alguns licenciamentos para atividades de menor impacto.", "/servicos/estudos-tecnicos/"],
    ["PRAD", "Plano de Recuperação de Áreas Degradadas", "Define como uma área alterada por obra, mineração ou atividade agrícola volta a ter cobertura e funções ecológicas.", "/servicos/estudos-tecnicos/"],
    ["PTRF", "Projeto Técnico de Reconstituição da Flora", "Projeto de recomposição da vegetação nativa, comum em compensações e em Áreas de Preservação Permanente.", "/servicos/estudos-tecnicos/"],
    ["PAE", "Plano de Ação de Emergência", "Procedimentos para situações de emergência, como em barragens e reservatórios, incluindo ações com a fauna afetada.", "/servicos/estudos-tecnicos/"],
    ["Outorga", "Outorga de direito de uso de recursos hídricos", "Autorização para captar água ou intervir em cursos d'água. Em Minas Gerais, é analisada pelo IGAM.", "/servicos/outorga-de-agua/"],
    ["CTF", "Cadastro Técnico Federal do IBAMA", "Registro obrigatório para pessoas e empresas que exercem atividades potencialmente poluidoras ou de defesa ambiental. A AgroAmbient é certificada (CTF 7856773).", "/sobre/"],
    ["AAF", "Autorização Ambiental de Funcionamento", "Antiga modalidade de regularização simplificada em Minas Gerais, hoje substituída pelo Licenciamento Ambiental Simplificado (LAS).", "/servicos/licenciamento-ambiental/"],
]

# ---------------------------------------------------------------------------
# Perguntas frequentes (página /perguntas-frequentes/ e dados estruturados)
# ---------------------------------------------------------------------------
FAQ = [
    ("Sobre a AgroAmbient", [
        ("O que a AgroAmbient faz?", "A AgroAmbient é uma consultoria ambiental especializada em estudos de fauna terrestre e aquática. Também faz licenciamento ambiental, outorga de água, diagnósticos, planos de manejo, assessoria agrícola, educação ambiental, cursos e palestras."),
        ("Onde a AgroAmbient atende?", "A sede fica em Rio Paranaíba, no Alto Paranaíba (MG), e a empresa atende em todo o território nacional, com equipe que se desloca até o empreendimento."),
        ("Desde quando a empresa atua?", "A AgroAmbient foi fundada em 2015 e atua com estudos e serviços ambientais voltados à fauna terrestre e aquática."),
        ("A AgroAmbient é registrada nos órgãos competentes?", "Sim. A empresa tem CNPJ 21.630.431/0001-01, é certificada no Cadastro Técnico Federal do IBAMA (CTF 7856773) e registrada no Conselho Regional de Biologia (CRBio-04 000944-04/2021)."),
        ("Quem é o responsável técnico?", "A direção técnica é do biólogo Willian Lopes Silva, mestre e especialista em Zoologia com ênfase em ictiofauna, com equipe multidisciplinar de biólogos especialistas nas diversas áreas da zoologia e da gestão ambiental."),
        ("Para quais setores a AgroAmbient trabalha?", "Para empresas de consultoria e gestão ambiental e para os setores minerário, energético, agropecuário e industrial."),
    ]),
    ("Estudos de fauna", [
        ("Qual a diferença entre inventário e monitoramento de fauna?", "O inventário levanta as espécies que existem na área em um momento. O monitoramento repete o levantamento ao longo do tempo, com os mesmos métodos, para medir mudanças e avaliar impactos do empreendimento."),
        ("Preciso de autorização para capturar fauna no estudo?", "Sim. Estudos que envolvem captura, coleta ou transporte de animais silvestres dependem de autorização do órgão ambiental competente. A AgroAmbient prepara e solicita essa autorização."),
        ("Quando o resgate de fauna é exigido?", "Normalmente quando há supressão de vegetação, obras ou enchimento de reservatórios que podem atingir animais silvestres, conforme a licença ou a autorização emitida."),
        ("Vocês trabalham com peixes?", "Sim. Fazemos estudos ictiológicos, inventário e monitoramento de biota aquática e de ictioplâncton, resgate de ictiofauna, transposição de peixes e laudos de necropsia de peixes. A direção técnica é especializada em ictiofauna."),
        ("Vocês fazem laudos periciais?", "Sim. Elaboramos laudos periciais ambientais e laudos de necropsia de peixes e outros animais, por exemplo em casos de mortandade."),
    ]),
    ("Licenciamento e documentos", [
        ("Como sei se meu empreendimento precisa de licença ambiental?", "Depende da atividade, do porte e da localização. Em Minas Gerais, o enquadramento segue a Deliberação Normativa COPAM nº 217/2017. Fazemos essa análise no primeiro contato."),
        ("O que é outorga de água?", "É a autorização para usar água de rios, lagos ou poços, ou para intervir em cursos d'água. Em Minas Gerais, é analisada pelo IGAM. Usos insignificantes precisam de cadastro."),
        ("Os estudos têm responsável técnico?", "Sim. Todos os estudos são assinados por profissional habilitado, com a anotação de responsabilidade técnica no respectivo conselho de classe."),
    ]),
    ("Orçamento e prazos", [
        ("Quanto custa um estudo ambiental?", "O valor depende do tipo de estudo, da área, dos grupos de fauna, do número de campanhas e da distância. Enviamos uma proposta depois de entender o empreendimento."),
        ("Quanto tempo leva?", "Estudos de campo seguem o calendário de campanhas pedido pelo órgão, muitas vezes cobrindo seca e chuva. Documentos sem campo costumam ser mais rápidos. O prazo vai detalhado na proposta."),
        ("Como peço um orçamento?", "Pelo formulário da página de contato, que abre o WhatsApp (34) 99806-7566 com a mensagem pronta, ou pelo telefone (34) 3855-1197. Conte o tipo de empreendimento, a cidade e o que o órgão pediu."),
    ]),
]

# ---------------------------------------------------------------------------
# Artigos do blog
# ---------------------------------------------------------------------------
POSTS = [
    {
        "slug": "quando-o-licenciamento-exige-estudo-de-fauna",
        "title": "Quando o licenciamento ambiental exige estudo de fauna?",
        "description": "Entenda em que situações o órgão ambiental pede levantamento, monitoramento ou resgate de fauna e como se preparar.",
        "date": "2026-11-12",
        "summary": "O estudo de fauna é pedido quando o empreendimento pode afetar animais silvestres: em geral, nos estudos para a licença (diagnóstico do meio biótico), nas condicionantes de monitoramento e sempre que há supressão de vegetação ou intervenção em cursos d'água.",
        "body": [
            ("h2", "Por que o órgão pede estudo de fauna"),
            ("p", "O licenciamento ambiental avalia os impactos de uma atividade sobre o meio físico, biótico e socioeconômico. A fauna é parte do meio biótico, e conhecer quais espécies vivem na área é o que permite prever impactos e propor medidas para evitá-los ou reduzi-los."),
            ("p", "Em nível federal, a Instrução Normativa IBAMA nº 146/2007 estabelece critérios para o manejo de fauna silvestre (levantamento, monitoramento, salvamento, resgate e destinação) em empreendimentos sujeitos ao licenciamento. Estados e municípios têm regras próprias que se somam a ela."),
            ("h2", "As situações mais comuns"),
            ("ul", [
                "<strong>Estudos para obter a licença.</strong> O EIA/RIMA e outros estudos costumam exigir diagnóstico de fauna, com dados de campo.",
                "<strong>Condicionantes de licença.</strong> Programas de monitoramento de fauna durante a instalação e a operação.",
                "<strong>Supressão de vegetação.</strong> Afugentamento e resgate de fauna acompanhando a frente de desmate.",
                "<strong>Barragens e cursos d'água.</strong> Estudos de ictiofauna, resgate de peixes e, em alguns casos, transposição.",
            ]),
            ("h2", "Inventário, monitoramento ou resgate?"),
            ("table", [("Estudo", "Para que serve", "Quando aparece"),
                       ("Inventário", "Saber quais espécies existem na área", "Antes da licença, no diagnóstico"),
                       ("Monitoramento", "Acompanhar mudanças ao longo do tempo", "Condicionante da LI e da LO"),
                       ("Resgate", "Proteger os animais durante a intervenção", "Supressão, obras, enchimento de reservatórios")]),
            ("h2", "Como se preparar"),
            ("ol", [
                "Leia o termo de referência ou as condicionantes com atenção: eles dizem quais grupos e métodos são esperados.",
                "Planeje o calendário. Muitos órgãos pedem campanhas na seca e na chuva, o que define o prazo mínimo do estudo.",
                "Considere o tempo da autorização de manejo de fauna, que precisa sair antes da campanha com captura.",
                "Contrate uma equipe com especialistas nos grupos exigidos e responsável técnico habilitado.",
            ]),
            ("p", "Se você não sabe se o seu caso exige estudo de fauna, <a href=\"/contato/?assunto=Estudos%20de%20fauna\">fale com a AgroAmbient</a>. Analisamos o enquadramento sem compromisso."),
        ],
        "related": ["inventario-de-fauna", "monitoramento-de-fauna", "resgate-de-fauna"],
    },
    {
        "slug": "o-que-e-resgate-de-fauna",
        "title": "O que é resgate de fauna e como ele funciona na prática",
        "description": "Afugentamento, captura, triagem e soltura: veja como funciona o resgate de fauna em obras e supressão de vegetação.",
        "date": "2026-11-12",
        "summary": "Resgate de fauna é o conjunto de ações para proteger os animais silvestres durante uma intervenção, como supressão de vegetação ou enchimento de reservatório. A prioridade é afugentar; capturar e soltar em outro lugar fica para quem não consegue sair sozinho.",
        "body": [
            ("h2", "Afugentar primeiro, resgatar depois"),
            ("p", "Antes de a máquina entrar, a equipe vistoria a área e conduz os animais para fragmentos vizinhos. Esse é o afugentamento, e ele resolve a maior parte dos casos com menos estresse para os animais."),
            ("p", "O resgate entra para quem não consegue fugir: filhotes, ninhos, animais lentos, como alguns répteis e anfíbios, e peixes em poças que secam durante a drenagem de um reservatório."),
            ("h2", "Etapas de um programa de resgate"),
            ("ol", [
                "<strong>Plano de afugentamento e resgate</strong>, com métodos, equipe, áreas de soltura e destinação, aprovado e autorizado pelo órgão ambiental.",
                "<strong>Vistoria prévia</strong> da área e definição das rotas de fuga, no sentido dos fragmentos que serão mantidos.",
                "<strong>Acompanhamento da frente de obra</strong>, com a equipe técnica junto do operador.",
                "<strong>Captura, triagem e soltura</strong>, com registro de cada animal e encaminhamento veterinário quando necessário.",
                "<strong>Relatório ao órgão</strong>, com todas as ocorrências e a destinação dos animais.",
            ]),
            ("h2", "O que dá errado quando o resgate é mal planejado"),
            ("ul", [
                "A frente de obra para porque a equipe de fauna não estava pronta.",
                "Não há área de soltura definida e aprovada.",
                "Faltam registros, e o relatório não atende ao órgão.",
            ]),
            ("p", "A AgroAmbient faz <a href=\"/servicos/resgate-de-fauna/\">resgate de fauna terrestre e aquática</a> integrado ao cronograma da obra."),
        ],
        "related": ["resgate-de-fauna", "estudos-ictiologicos", "licenciamento-ambiental"],
    },
    {
        "slug": "outorga-de-agua-em-minas-gerais",
        "title": "Outorga de água em Minas Gerais: o básico para o produtor rural",
        "description": "Quem precisa de outorga, o que é uso insignificante e quais cuidados tomar antes de captar água ou construir uma barragem em MG.",
        "date": "2026-11-12",
        "summary": "Em Minas Gerais, quem capta água de rios, represas ou poços, constrói barramentos ou lança efluentes precisa de outorga do IGAM ou, para usos insignificantes, de cadastro. Sem ela, a atividade fica irregular e a licença ambiental pode ser travada.",
        "body": [
            ("h2", "O que é outorga"),
            ("p", "A outorga de direito de uso de recursos hídricos é o instrumento da Política Nacional de Recursos Hídricos (Lei nº 9.433/1997) que autoriza o uso da água por um prazo e em uma quantidade definidos. Em Minas Gerais, a Lei Estadual nº 13.199/1999 rege o tema, e a análise é feita pelo IGAM."),
            ("h2", "Quem precisa"),
            ("ul", [
                "Captação em rio, córrego, lago ou represa para irrigação, dessedentação, piscicultura ou indústria.",
                "Uso de água subterrânea por poço tubular.",
                "Construção de barramentos, travessias e canalizações.",
                "Lançamento de efluentes em cursos d'água.",
            ]),
            ("h2", "Uso insignificante"),
            ("p", "Usos de pequeno volume, definidos nas normas estaduais, são considerados insignificantes. Eles dispensam a outorga, mas precisam de cadastro. Os limites variam conforme a região e o tipo de uso, por isso vale conferir caso a caso."),
            ("h2", "Cuidados antes de pedir"),
            ("ol", [
                "Verifique a disponibilidade hídrica da bacia, porque em áreas de conflito os pedidos são mais restritos.",
                "Organize documentos da propriedade e do CAR.",
                "Planeje a outorga junto com o licenciamento da atividade, para não travar um processo pelo outro.",
                "Controle o vencimento: outorgas têm prazo e precisam ser renovadas.",
            ]),
            ("p", "Precisa regularizar o uso de água? Veja como funciona nossa <a href=\"/servicos/outorga-de-agua/\">assessoria em outorga</a>."),
        ],
        "related": ["outorga-de-agua", "assessoria-agricola", "licenciamento-ambiental"],
    },
]


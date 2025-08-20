import streamlit as st
import streamlit.components.v1 as components
import random
import json

st.set_page_config(page_title="Jogo ODS", page_icon="🌍", layout="wide")

st.markdown("""
    <style>

    /* Fundo geral */
    .stApp {
        background-color: #FEF7DD;
        font-family: 'Nunito', sans-serif;
        color: #154C6E; /* cor padrão do texto */
    }

    /* Títulos */
    h1, h2, h3, h4 {
        color: #154C6E !important;
        font-weight: 900;
    }

    /* Texto normal */
    p, span, label, .stRadio, .stMarkdown {
        color: #154C6E !important;
        font-size: 16px;
        font-weight: 600;
    }

    /* Perguntas (card azul) */
    .question-box {
        background-color: #1A96D4;
        color: white !important;
        padding: 20px;
        border-radius: 18px;
        border: 4px solid #154C6E;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Caixa do placar */
    .score-box {
        background-color: #E8D0A6;
        color: #154C6E !important;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #4BA547;
        margin-bottom: 12px;
        font-size: 16px;
    }

    /* Botões */
    .stButton>button {
        background-color: #F04E39;
        color: white !important;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.25);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #E1206F;
        transform: scale(1.07);
    }

    /* Barrinha de pontos */
    .progress {
        height: 12px;
        border-radius: 6px;
        background-color: #ddd;
        margin-top: 6px;
    }
    .progress-bar {
        height: 12px;
        border-radius: 6px;
        background-color: #4BA547;
    }
    </style>
""", unsafe_allow_html=True)


ARQUIVO_DADOS = "dados_quiz_missoes.json"

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "quiz": {"players": [], "scores": {}, "history": []},
            "missions": {"students": [], "scores": {}, "history": {}}
        }

def salvar_dados():
    json_dados = {
        "quiz": {
            "players": st.session_state.players,
            "scores": st.session_state.scores_quiz,
            "history": st.session_state.quiz_history
        },
        "missions": {
            "students": st.session_state.students,
            "scores": st.session_state.scores_missions,
            "history": st.session_state.mission_history
        }
    }
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(json_dados, f)

dados = carregar_dados()

if "players" not in st.session_state:
    st.session_state.players = dados["quiz"]["players"]
if "scores_quiz" not in st.session_state:
    st.session_state.scores_quiz = dados["quiz"]["scores"]
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = dados["quiz"]["history"]
if "questions" not in st.session_state:
    st.session_state.questions = [
        {"pergunta": "Qual o objetivo do ODS 1?",
         "alternativas": ["acabar com a fome", "Erradicar a pobreza", "Garantir energia limpa"],
         "correta": "Erradicar a pobreza"},
        {"pergunta": "A pobreza é considerada um fenômeno multidimensional porque:",
         "alternativas": ["Afeta apenas a renda das pessoas", "Está ligada somente ao desemprego", "Envolve falta de acesso à educação, saúde e moradia"],
         "correta": "Envolve falta de acesso à educação, saúde e moradia"},
        {"pergunta": "Como diferentes dimensões da pobreza (educação, saúde e trabalho) se relacionam para perpetuar ciclos de desigualdade?",
         "alternativas": ["A falta de educação limita oportunidades de trabalho, que por sua vez impede acesso a serviços de saúde de qualidade.", "Saúde, educação e trabalho são independentes; problemas em um não afetam os outros.", "Apenas a renda é suficiente para quebrar o ciclo da pobreza."],
         "correta": "A falta de educação limita oportunidades de trabalho, que por sua vez impede acesso a serviços de saúde de qualidade."},
        {"pergunta": "O que o ODS 2 deseja acabar?",
         "alternativas": ["O turismo", "A fome", "A agricultura"],
         "correta": "A fome"},
        {"pergunta": "Por que a agricultura sustentável é essencial para o futuro?",
         "alternativas": ["Porque aumenta a produção de alimentos sem destruir os recursos naturais", "Porque reduz o preço do combustível",
                          "Porque facilita o transporte urbano"],
         "correta": "Porque aumenta a produção de alimentos sem destruir os recursos naturais"},
        {"pergunta": "Qual é o principal desafio que uma cidade enfrenta com o aumento da população urbana em relação ao ODS 2",
         "alternativas": ["Falta de infraestrutura de transportes urbanos", "Promoção de atividades agrícolas sustentáveis",
                          "Insegurança alimentar"],
         "correta": "Insegurança alimentar"},
        {"pergunta": "O ODS 3 busca garantir:",
         "alternativas": ["Saúde e bem-estar para todos", "Esportes de alto rendimento", "Novas redes sociais"],
         "correta": "Saúde e bem-estar para todos"},

        {"pergunta": "Por que a vacinação é considerada uma das maiores conquistas da saúde pública?",
         "alternativas": ["Porque cura todas as doenças de uma vez",
                          "Porque previne doenças e protege comunidades inteiras",
                          "Porque substitui qualquer outro tratamento médico"],
         "correta": "Porque previne doenças e protege comunidades inteiras"},

        {"pergunta": "Por que fatores sociais e econômicos são tão importantes para a saúde de uma população?",
         "alternativas": [
             "Porque desigualdades sociais, pobreza e acesso limitado a serviços básicos aumentam riscos de doenças e reduzem expectativa de vida.",
             "Porque saúde depende apenas de medicamentos e hospitais.",
             "Porque fatores econômicos não influenciam doenças transmissíveis."],
         "correta": "Porque desigualdades sociais, pobreza e acesso limitado a serviços básicos aumentam riscos de doenças e reduzem expectativa de vida."},

        # ODS 4 - Educação de Qualidade
        {"pergunta": "Aprender a ler e escrever faz parte do direito à:",
         "alternativas": ["Educação básica", "Educação superior", "Educação informal"],
         "correta": "Educação básica"},

        {
            "pergunta": "Qual foi o impacto da Conferência das Nações Unidas sobre Meio Ambiente e Desenvolvimento (Rio-92) na Educação Ambiental?",
            "alternativas": [
                "Estabeleceu a importância da Educação Ambiental como ferramenta essencial para o desenvolvimento sustentável, resultando na criação do Programa de Educação Ambiental da UNESCO.",
                "Promoveu a conscientização sobre questões ambientais, mas teve pouco impacto na Educação Ambiental.",
                "Ignorou completamente a importância da Educação Ambiental no contexto do desenvolvimento sustentável."],
            "correta": "Estabeleceu a importância da Educação Ambiental como ferramenta essencial para o desenvolvimento sustentável, resultando na criação do Programa de Educação Ambiental da UNESCO."},

        {
            "pergunta": "Qual foi o impacto da Conferência das Nações Unidas sobre Meio Ambiente e Desenvolvimento (Rio-92) na Educação Ambiental?",
            "alternativas": [
                "Estabeleceu a importância da Educação Ambiental como ferramenta essencial para o desenvolvimento sustentável, resultando na criação do Programa de Educação Ambiental da UNESCO.",
                "Promoveu a conscientização sobre questões ambientais, mas teve pouco impacto na Educação Ambiental.",
                "Ignorou completamente a importância da Educação Ambiental no contexto do desenvolvimento sustentável."],
            "correta": "Ignorou completamente a importância da Educação Ambiental no contexto do desenvolvimento sustentável."},

        # ODS 5 - Igualdade de Gênero
        {"pergunta": "Uma forma de promover a igualdade de gênero é:",
         "alternativas": ["Garantir salários iguais para trabalho igual", "Oferecer empregos apenas para homens",
                          "Incentivar que mulheres trabalhem sem direitos"],
         "correta": "Garantir salários iguais para trabalho igual"},

        {"pergunta": "Por que a igualdade de gênero é essencial para o desenvolvimento sustentável?",
         "alternativas": ["Porque não ajuda na democratização", "Porque diminui o uso de energia",
                          "Porque permite que metade da população participe plenamente da sociedade e da economia"],
         "correta": "Porque permite que metade da população participe plenamente da sociedade e da economia"},

        {"pergunta": "Quais são os efeitos da desigualdade de gênero no mercado de trabalho e na sociedade?",
         "alternativas": ["Apenas influencia escolhas pessoais, sem afetar a economia ou a sociedade.",
                          "Limita oportunidades profissionais para mulheres, aumenta desigualdade social e reduz potencial econômico da comunidade.",
                          "Favorece homens e mulheres igualmente em todos os setores."],
         "correta": "Limita oportunidades profissionais para mulheres, aumenta desigualdade social e reduz potencial econômico da comunidade"},

        # ODS 6 - Água Potável e Saneamento
        {"pergunta": "Por que o saneamento é fundamental para a saúde pública?",
         "alternativas": ["Porque reduz a poluição visual",
                          "Porque evita doenças causadas pela falta de higiene e contaminação da água",
                          "Porque deixa a cidade mais bonita"],
         "correta": "Porque evita doenças causadas pela falta de higiene e contaminação da água"},

        {"pergunta": "O que faz parte do saneamento básico?",
         "alternativas": ["Coleta de esgoto, abastecimento de água e manejo de resíduos sólidos",
                          "Construção de reservatórios de água sem tratamento e abertura de canais de drenagem improvisados",
                          "Limpeza de ruas e manutenção de parques"],
         "correta": "Coleta de esgoto, abastecimento de água e manejo de resíduos sólidos"},

        {"pergunta": "Qual foi o impacto da Declaração de Dublin de 1992 sobre a gestão integrada dos recursos hídricos?",
        "alternativas": ["Propôs a privatização completa dos recursos hídricos para garantir sua gestão eficiente.",
                        "Ignorou a necessidade de cooperação internacional na gestão dos recursos hídricos.",
                        "Estabeleceu os princípios da gestão integrada dos recursos hídricos, reconhecendo a água como um bem econômico e social."],
        "correta": "Estabeleceu os princípios da gestão integrada dos recursos hídricos, reconhecendo a água como um bem econômico e social."},
        # ODS 7 - Energia Limpa e Acessível
        {"pergunta": "Um exemplo de energia renovável é:",
         "alternativas": ["Petróleo", "Carvão", "Solar"],
         "correta": "Solar"},

        {"pergunta": "Qual é a principal vantagem da energia renovável?",
         "alternativas": ["É ilimitada e sem custo algum", "Não polui e pode ser usada de forma contínua",
                          "Funciona só em países ricos"],
         "correta": "Não polui e pode ser usada de forma contínua"},

        {"pergunta": "Como a escolha de uma matriz energética sustentável afeta sociedade e meio ambiente?",
         "alternativas": [
             "Permite fornecimento confiável de energia, reduz emissões, preserva recursos naturais e melhora qualidade de vida.",
             "Foca apenas na redução de custos, ignorando impactos ambientais.",
             "Depende exclusivamente de combustíveis fósseis para atender demanda industrial."],
         "correta": "Permite fornecimento confiável de energia, reduz emissões, preserva recursos naturais e melhora qualidade de vida."},

        # ODS 8 - Trabalho Decente e Crescimento Econômico
        {"pergunta": "Por que incentivar a economia local fortalece o desenvolvimento sustentável?",
         "alternativas": ["Porque gera empregos, reduz desigualdades e estimula o consumo consciente",
                          "Porque substitui todas as importações",
                          "Porque evita o uso de tecnologia"],
         "correta": "Porque gera empregos, reduz desigualdades e estimula o consumo consciente"},

        {
            "pergunta": "Qual é o termo usado para descrever o trabalho que é realizado em condições seguras, justas e dignas, com salários justos e proteção social para os trabalhadores?",
            "alternativas": ["Emprego informal", "Trabalho decente", "Trabalho precário"],
            "correta": "Trabalho decente"},

        {"pergunta": "Qual das seguintes práticas pode contribuir mais para alcançar a ODS 8?",
         "alternativas": ["Reduzir o consumo de energia e água nas operações da empresa.",
                          "Implementar políticas de igualdade de gênero no ambiente de trabalho.",
                          "Criar programas de capacitação profissional para comunidades de baixa renda"],
         "correta": "Reduzir o consumo de energia e água nas operações da empresa."},

        # ODS 9 - Indústria, Inovação e Infraestrutura
        {"pergunta": "Um exemplo de inovação tecnológica é:",
         "alternativas": ["Impressora 3D", "Lâmpada a óleo", "Máquina de escrever"],
         "correta": "Impressora 3D"},

        {"pergunta": "O que significa 'inovação social'?",
         "alternativas": ["Criar aplicativos de celular para empresas",
                          "Desenvolver soluções que atendem necessidades da sociedade e melhoram a vida das pessoas",
                          "Inventar produtos apenas para consumo rápido"],
         "correta": "Desenvolver soluções que atendem necessidades da sociedade e melhoram a vida das pessoas"},

        {
            "pergunta": "Como a inovação e o desenvolvimento de infraestrutura sustentável podem reduzir desigualdades e gerar impacto social positivo?",
            "alternativas": [
                "Permitindo que comunidades tenham acesso a tecnologias, transporte, energia e serviços que melhoram qualidade de vida e oportunidades econômicas.",
                "Concentrando tecnologia e infraestrutura apenas em grandes centros urbanos, favorecendo crescimento econômico rápido.",
                "Substituindo antigas indústrias sem considerar como isso afeta empregos e comunidades locais."],
            "correta": "Permitindo que comunidades tenham acesso a tecnologias, transporte, energia e serviços que melhoram qualidade de vida e oportunidades econômicas."},

        # ODS 10 - Redução das Desigualdades
        {"pergunta": "Qual grupo social está diretamente relacionado ao ODS 10?",
         "alternativas": ["Apenas trabalhadores do setor privado",
                          "Pessoas em situação de vulnerabilidade, como pobres, migrantes e minorias",
                          "Exclusivamente governos e políticos"],
         "correta": "Pessoas em situação de vulnerabilidade, como pobres, migrantes e minorias"},

        {
            "pergunta": "O que diferencia a abordagem da ODS 10, focada na redução da desigualdade, da ODS 1, focada na erradicação da pobreza?",
            "alternativas": [
                "A ODS 10 foca apenas em países desenvolvidos, enquanto a ODS 1 se aplica a todos os países.",
                "A ODS 10 lida com a diferença entre os grupos, incluindo os mais ricos e os mais pobres, enquanto a ODS 1 lida com a situação absoluta de quem vive abaixo da linha da pobreza.",
                "A ODS 10 é uma meta social, enquanto a ODS 1 é uma meta puramente econômica."],
            "correta": "A ODS 10 lida com a diferença entre os grupos, incluindo os mais ricos e os mais pobres, enquanto a ODS 1 lida com a situação absoluta de quem vive abaixo da linha da pobreza."},

        {
            "pergunta": "Uma das metas do ODS 10 é aumentar a renda da população mais pobre. Qual é a referência usada pela ONU para isso?",
            "alternativas": ["Crescer a renda dos 10% mais ricos acima da média nacional",
                             "Crescer a renda dos 40% mais pobres acima da média nacional",
                             "Crescer a renda dos 20% mais pobres igual à média nacional"],
            "correta": "Crescer a renda dos 40% mais pobres acima da média nacional"},

        # ODS 11 - Cidades e Comunidades Sustentáveis
        {"pergunta": "Qual meio de transporte é considerado sustentável?",
         "alternativas": ["Bicicleta", "Carro", "Moto"],
         "correta": "Bicicleta"},

        {"pergunta": "Qual órgão responsável pela proteção do patrimônio cultural no Brasil?",
         "alternativas": ["UNICEF", "UNESCO", "IPHAN"],
         "correta": "IPHAN"},

        {"pergunta": "Qual é uma das metas específicas do ODS 11 para 2030 relacionada à moradia?",
         "alternativas": ["Garantir que apenas 50% da população urbana tenha acesso a moradia adequada",
                          "Garantir o acesso de todos a habitação segura, adequada e a preço acessível, e melhorar favelas",
                          "Aumentar o número de prédios residenciais em áreas urbanas sem considerar o preço"],
         "correta": "Garantir o acesso de todos a habitação segura, adequada e a preço acessível, e melhorar favelas"},

        # ODS 12 - Consumo e Produção Responsáveis
        {"pergunta": "Um exemplo de consumo responsável é:",
         "alternativas": ["Reaproveitar materiais e reciclar resíduos", "Descartar lixo em qualquer lugar",
                          "Usar produtos descartáveis todos os dias"],
         "correta": "Reaproveitar materiais e reciclar resíduos"},

        {"pergunta": "Uma das metas do ODS 12 é promover práticas de compras públicas sustentáveis. Isso significa:",
         "alternativas": ["O governo comprar somente de empresas locais",
                          "O governo priorizar aquisições que levem em conta critérios ambientais e sociais",
                          "O governo aumentar o número de licitações abertas"],
         "correta": "O governo priorizar aquisições que levem em conta critérios ambientais e sociais"},

        {
            "pergunta": "Qual desses relatórios globais é utilizado pela ONU como referência para monitorar o progresso do ODS 12?",
            "alternativas": ["Relatório Global de Desenvolvimento Humano (PNUD)",
                             "Relatório Mundial da Educação (UNESCO)",
                             "Relatório Global de Produção e Consumo Sustentáveis (ONU Meio Ambiente)"],
            "correta": "Relatório Global de Produção e Consumo Sustentáveis (ONU Meio Ambiente)"},

        # ODS 13 - Ação Contra a Mudança Global do Clima
        {"pergunta": "Qual é a principal causa das mudanças climáticas?",
         "alternativas": ["Atividade humana", "Aumento da rotação da Terra", "Movimento das placas tectônicas"],
         "correta": "Atividade humana"},

        {"pergunta": "O Acordo de Paris, fundamental para o ODS 13, foi assinado em:",
         "alternativas": ["2015", "2005", "1992"],
         "correta": "2015"},

        {
            "pergunta": "A expressão 'descarbonização da economia' está diretamente ligada ao ODS 13. O que ela significa?",
            "alternativas": ["Substituir todo o transporte público por veículos particulares elétricos",
                             "Eliminar o carbono presente nos organismos vivos",
                             "Reduzir gradualmente a dependência de combustíveis fósseis e incentivar fontes de energia limpa"],
            "correta": "Reduzir gradualmente a dependência de combustíveis fósseis e incentivar fontes de energia limpa"},

        # ODS 14 - Vida na Água
        {"pergunta": "Por que as tartarugas comem saco plástico?",
         "alternativas": ["Faz parte da alimentação da espécie",
                          "Comem para diminuir a quantidade de poluição no oceano", "Confundem com água viva"],
         "correta": "Confundem com água viva"},

        {"pergunta": "O que caracteriza a pesca ilegal?",
         "alternativas": [
             "Pesca realizada sem respeitar regras e regulamentações, como cotas, áreas proibidas ou espécies protegidas",
             "Pesca feita apenas em rios e lagos de propriedade privada",
             "Pesca artesanal realizada com métodos tradicionais e sustentáveis"],
         "correta": "Pesca realizada sem respeitar regras e regulamentações, como cotas, áreas proibidas ou espécies protegidas"},

        {"pergunta": "Qual é um dos principais impactos do aumento da acidificação dos oceanos?",
         "alternativas": ["Diminuição da temperatura média global",
                          "Comprometimento do crescimento de corais e organismos calcários, afetando ecossistemas marinhos",
                          "Redução do nível do mar nas regiões costeiras"],
         "correta": "Comprometimento do crescimento de corais e organismos calcários, afetando ecossistemas marinhos"},

        # ODS 15 - Vida Terrestre
        {"pergunta": "O que a ODS 15 busca combater, principalmente, para proteger a biodiversidade?",
         "alternativas": ["O desmatamento e a desertificação.", "A poluição plástica nos oceanos.",
                          "A emissão de gases de efeito estufa."],
         "correta": "O desmatamento e a desertificação."},

        {"pergunta": "Qual é a principal conexão entre a ODS 15 e a agricultura?",
         "alternativas": [
             "A ODS 15 promove a conservação da terra e do solo, o que é fundamental para a agricultura sustentável e a segurança alimentar.",
             "A ODS 15 ignora a agricultura, pois ela é tratada na ODS 2.",
             "A ODS 15 promove o uso de fertilizantes químicos para aumentar a produtividade agrícola."],
         "correta": "A ODS 15 promove a conservação da terra e do solo, o que é fundamental para a agricultura sustentável e a segurança alimentar."},

        {
            "pergunta": "Qual dos seguintes cenários melhor representa a 'degradação da terra' que a ODS 15 busca combater?",
            "alternativas": ["Obras de arte em galerias.",
                             "A erosão do solo em uma área que foi desmatada para a agricultura, tornando a terra infértil.",
                             "A construção de um novo edifício em uma área urbana abandonada."],
            "correta": "A erosão do solo em uma área que foi desmatada para a agricultura, tornando a terra infértil."},

        # ODS 16 - Paz, Justiça e Instituições Eficazes
        {"pergunta": "Como o ODS 16 se relaciona com o combate à corrupção?",
         "alternativas": [
             "Incentivando práticas transparentes e reduzindo a corrupção em instituições públicas e privadas",
             "Permitindo que apenas pequenas corrupções sejam toleradas",
             "Focando apenas em assuntos de segurança sem abordar a corrupção"],
         "correta": "Incentivando práticas transparentes e reduzindo a corrupção em instituições públicas e privadas"},

        {"pergunta": "Como o ODS 16 aborda a prevenção de conflitos e violência?",
         "alternativas": [
             "Por meio de políticas de governança, educação, redução de desigualdades e fortalecimento de instituições legais",
             "Incentivando apenas o aumento da presença militar em áreas de risco",
             "Promovendo exclusivamente vigilância digital sobre cidadãos"],
         "correta": "Por meio de políticas de governança, educação, redução de desigualdades e fortalecimento de instituições legais"},

        {
            "pergunta": "Qual indicador internacional é frequentemente usado para medir corrupção e está relacionado ao ODS 16?",
            "alternativas": ["Índice de Percepção da Corrupção (CPI) da Transparency International",
                             "Produto Interno Bruto (PIB)", "Índice de Desenvolvimento Humano (IDH)"],
            "correta": "Índice de Percepção da Corrupção (CPI) da Transparency International"},

        # ODS 17 - Parcerias e Meios de Implementação
        {
            "pergunta": "A ODS 17 foca em diferentes tipos de parceria. Qual dos seguintes não é um tipo de parceria mencionado nos objetivos?",
            "alternativas": ["Parcerias público-público.", "Parcerias público-privadas.",
                             "Parcerias com a sociedade civil."],
            "correta": "Parcerias público-público."},

        {"pergunta": "Qual a diferença entre a cooperação Norte-Sul e a cooperação Sul-Sul?",
         "alternativas": [
             "A cooperação Norte-Sul envolve apenas acordos de tecnologia, enquanto a Sul-Sul lida com finanças.",
             "A cooperação Norte-Sul é entre países ricos e pobres, enquanto a Sul-Sul é entre os próprios países em desenvolvimento.",
             "A cooperação Norte-Sul é obrigatória, enquanto a Sul-Sul é opcional."],
         "correta": "A cooperação Norte-Sul é entre países ricos e pobres, enquanto a Sul-Sul é entre os próprios países em desenvolvimento."},

        {
            "pergunta": "Por que a ODS 17 é considerada um 'meio de implementação' e não um objetivo temático como a ODS 1 (Pobreza) ou a ODS 13 (Clima)?",
            "alternativas": ["Porque trata apenas de acordos de paz.",
                             "Porque as parcerias e o financiamento são as ferramentas e mecanismos necessários para que todos os outros ODS sejam alcançados.",
                             "Porque é o objetivo mais fácil de ser implementado por todos os países."],
            "correta": "Porque as parcerias e o financiamento são as ferramentas e mecanismos necessários para que todos os outros ODS sejam alcançados."}

    ]
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

if "students" not in st.session_state:
    st.session_state.students = dados["missions"]["students"]
if "scores_missions" not in st.session_state:
    st.session_state.scores_missions = dados["missions"]["scores"]
if "mission_history" not in st.session_state:
    st.session_state.mission_history = dados["missions"]["history"]
if "missions" not in st.session_state:
    st.session_state.missions = {
        "Plantar uma árvore 🌳": 3,
        "Apresentar trabalho sobre reciclagem ♻️": 2,
        "Reduzir o uso de plástico 🛍️": 2,
        "Economizar água em casa 💧": 1,
        "Participar de ação de voluntariado 🤝": 3
    }

st.title("🌍 ODS em Ação: Trilha Sustentável")
tab_quiz, tab_missoes = st.tabs(["🎲 Quiz ODS", "🌱 Missões ODS"])


with tab_quiz:
    st.header("🎲 Quiz ODS")

    with st.expander("➕ Adicionar jogadores"):
        nome = st.text_input("Nome do jogador", key="novo_jogador_quiz")
        if st.button("Adicionar jogador ao Quiz"):
            if nome and nome not in st.session_state.players:
                st.session_state.players.append(nome)
                st.session_state.scores_quiz[nome] = 0
                salvar_dados()

    st.subheader("📊 Placar do Jogo")
    if st.session_state.scores_quiz:
        for jogador, pontos in st.session_state.scores_quiz.items():
            st.write(f"**{jogador}**: {pontos} pontos")
    else:
        st.info("Nenhum jogador adicionado ainda.")

    if st.button("Nova pergunta"):
        st.session_state.current_question = random.choice(st.session_state.questions)
        st.session_state.selected_answer = None

    if st.button("➡️ Passar pergunta"):
        st.session_state.current_question = random.choice(st.session_state.questions)
        st.session_state.selected_answer = None

    if st.session_state.current_question:
        pergunta = st.session_state.current_question
        st.info(f"**Pergunta:** {pergunta['pergunta']}")

        st.session_state.selected_answer = st.radio(
            "Escolha uma resposta:",
            pergunta["alternativas"],
            index=None,
            key="quiz_resposta"
        )

        if st.session_state.selected_answer:
            if st.session_state.selected_answer == pergunta["correta"]:
                st.success("✅ Resposta correta!")

                st.write("Quem acertou?")
                for jogador in st.session_state.players:
                    if st.button(f"{jogador} +1 ponto", key=f"quiz_{jogador}"):
                        st.session_state.scores_quiz[jogador] += 1
                        st.session_state.quiz_history.append({"jogador": jogador, "pergunta": pergunta["pergunta"], "acertou": True})
                        salvar_dados()
                        st.session_state.current_question = None
                        st.rerun()
            else:
                st.error(f"❌ Resposta errada! A correta era: **{pergunta['correta']}**")
                st.session_state.quiz_history.append({"jogador": "Ninguém", "pergunta": pergunta["pergunta"], "acertou": False})
                st.session_state.current_question = None
                salvar_dados()

    if st.button("🔄 Reiniciar Quiz"):
        st.session_state.current_question = None
        st.session_state.selected_answer = None
        st.session_state.players = []
        st.session_state.scores_quiz = {}
        st.session_state.quiz_history = []
        salvar_dados()
        st.success("Jogo reiniciado!")

with tab_missoes:
    st.header("🌱 Missões ODS")

    with st.expander("➕ Adicionar alunos (Missões)"):
        nome = st.text_input("Nome do aluno", key="novo_aluno_missao")
        if st.button("Adicionar aluno às Missões"):
            if nome and nome not in st.session_state.scores_missions:
                st.session_state.students.append(nome)
                st.session_state.scores_missions[nome] = 0
                st.session_state.mission_history[nome] = []
                salvar_dados()

    st.subheader("📊 Placar das Missões")
    if st.session_state.scores_missions:
        for aluno, pontos in st.session_state.scores_missions.items():
            st.write(f"**{aluno}**: {pontos} pontos")
    else:
        st.info("Nenhum aluno registrado ainda.")

    st.subheader("✅ Registrar nova missão")
    if st.session_state.scores_missions:
        missao = st.selectbox("Selecione a missão:", list(st.session_state.missions.keys()))
        aluno = st.selectbox("Selecione o aluno:", list(st.session_state.scores_missions.keys()))

        if st.button("Registrar missão"):
            pontos = st.session_state.missions[missao]
            st.session_state.scores_missions[aluno] += pontos
            st.session_state.mission_history[aluno].append(missao)
            st.success(f"{aluno} ganhou {pontos} pontos pela missão: {missao}")
            salvar_dados()
            st.rerun()

    st.subheader("📜 Histórico de Missões")
    for aluno, missoes in st.session_state.mission_history.items():
        st.markdown(f"**{aluno}**")
        if missoes:
            for m in missoes:
                st.write(f"- {m}")
        else:
            st.write("Nenhuma missão registrada ainda.")


import streamlit as st
import random

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
        color: white !important;   /* texto branco dentro da pergunta */
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
        color: #154C6E !important; /* texto escuro no placar */
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


if "players" not in st.session_state:
    st.session_state.players = []
if "scores_quiz" not in st.session_state:
    st.session_state.scores_quiz = {}
if "scores_missions" not in st.session_state:
    st.session_state.scores_missions = {}
if "mission_history" not in st.session_state:
    st.session_state.mission_history = {}
if "questions" not in st.session_state:
    st.session_state.questions = [
        {"pergunta": "O que significa ODS?",
         "alternativas": ["Objetivos de Desenvolvimento Sustentável", "Organização de Desenvolvimento Social", "Ordem de Dados Sustentáveis"],
         "correta": "Objetivos de Desenvolvimento Sustentável"},
        {"pergunta": "Quantos ODS existem?",
         "alternativas": ["15", "17", "20"],
         "correta": "17"},
        {"pergunta": "Qual ODS trata de energia limpa e acessível?",
         "alternativas": ["ODS 5", "ODS 7", "ODS 9"],
         "correta": "ODS 7"}
    ]
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
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

    st.subheader("📊 Placar do Jogo")
    if st.session_state.scores_quiz:
        for jogador, pontos in st.session_state.scores_quiz.items():
            st.write(f"**{jogador}**: {pontos} pontos")
    else:
        st.info("Nenhum jogador adicionado ainda.")

    if st.button("Nova pergunta"):
        st.session_state.current_question = random.choice(st.session_state.questions)

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
                        st.session_state.current_question = None
                        st.rerun()
            else:
                st.error(f"❌ Resposta errada! A correta era: **{pergunta['correta']}**")
                st.session_state.current_question = None

    if st.button("🔄 Reiniciar Quiz"):
        st.session_state.current_question = None
        st.session_state.selected_answer = None
        st.session_state.scores_quiz = {}
        st.session_state.players = []
        st.success("Jogo reiniciado!")

with tab_missoes:
    st.header("🌱 Missões ODS")

    with st.expander("➕ Adicionar alunos (Missões)"):
        nome = st.text_input("Nome do aluno", key="novo_aluno_missao")
        if st.button("Adicionar aluno às Missões"):
            if nome and nome not in st.session_state.scores_missions:
                st.session_state.scores_missions[nome] = 0
                st.session_state.mission_history[nome] = []

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
            st.rerun()

    st.subheader("📜 Histórico de Missões")
    for aluno, missoes in st.session_state.mission_history.items():
        st.markdown(f"**{aluno}**")
        if missoes:
            for m in missoes:
                st.write(f"- {m}")
        else:
            st.write("Nenhuma missão registrada ainda.")


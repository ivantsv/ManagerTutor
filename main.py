import time

import streamlit as st
import json
import os
from llm_agents.role_agent import RoleAgent
from llm_agents.evaluation_agent import EvaluationAgent
from llm_agents.mentor_agent import MentorAgent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="ManagerTutor", page_icon="💬", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None
if 'lesson_step' not in st.session_state:
    st.session_state.lesson_step = 'theory'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mentor_chat_history' not in st.session_state:
    st.session_state.mentor_chat_history = []
if 'lesson_scores' not in st.session_state:
    st.session_state.lesson_scores = {}
if 'current_role_agent' not in st.session_state:
    st.session_state.role_agent = None
if 'current_mentor_agent' not in st.session_state:
    st.session_state.mentor_agent = None

ranks = {
    20: "Начинающий 😃",
    50: "Любитель 😊",
    70: "Профи 😐",
    100: "Эксперт 👿"
}

def metric_text(label: str, value: str):
    """
    Отображает "текстовую метрику" — аналог st.metric, но для строковых значений.
    Автоматически подстраивается под тему (светлую/тёмную).
    """
    bg_color = "rgba(240, 242, 246, 0.8)" if st.get_option("theme.base") == "light" else "rgba(38, 39, 48, 0.5)"
    text_color = "#000000" if st.get_option("theme.base") == "light" else "#FFFFFF"

    st.markdown(f"""
    <div style="
        background-color:{bg_color};
        border-radius:10px;
        padding:16px;
        text-align:center;
        box-shadow:0 1px 3px rgba(0,0,0,0.1);
        color:{text_color};
    ">
        <div style="font-size:14px; opacity:0.7;">{label}</div>
        <div style="font-size:28px; font-weight:600;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

PATH_TO_LESSONS = "lessons/"

LESSONS = {}
for filename in os.listdir(PATH_TO_LESSONS):
    file_path = os.path.join(PATH_TO_LESSONS, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            LESSONS[filename.removesuffix(".json")] = json.load(f)


with st.sidebar:
    st.title("💬 ManagerTutor")
    st.markdown("---")

    if st.button("🏠 Главная", use_container_width=True):
        st.session_state.page = 'home'
        st.session_state.role_agent = None
        st.rerun()

    if st.button("🤓 Чат с ментором", use_container_width=True):
        st.session_state.page = 'mentor_chat'
        st.session_state.role_agent = None
        st.rerun()

    if st.button("📚 Уроки", use_container_width=True):
        st.session_state.page = 'lessons'
        st.session_state.role_agent = None
        st.rerun()

    if st.button("📖 Глоссарий", use_container_width=True):
        st.session_state.page = 'glossary'
        st.session_state.role_agent = None
        st.rerun()

    if st.button("📊 Прогресс", use_container_width=True):
        st.session_state.page = 'progress'
        st.session_state.role_agent = None
        st.rerun()

    if st.button("📝 Информация", use_container_width=True):
        st.session_state.page = 'info'
        st.session_state.role_agent = None
        st.rerun()

    st.markdown("---")

    st.markdown(f"""
        <a href="{os.getenv("TELEGRAM_BOT_URL")}" target="_blank">
            <button style="
                width: 100%;
                padding: 0.5rem 1rem;
                background-color: #0088cc;
                color: white;
                border: none;
                border-radius: 0.5rem;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 500;
            ">
                📱 Открыть в Telegram
            </button>
        </a>
        """, unsafe_allow_html=True)

if st.session_state.page == 'home':
    st.title("Добро пожаловать в ManagerTutor! 👋")
    st.markdown("### Научитесь давать экологичную обратную связь")

    col1, col2, col3 = st.columns(3)

    with col1:
        lessons_solved = len(st.session_state.lesson_scores.keys())
        st.metric("Пройдено уроков", lessons_solved)
    with col2:
        avg_score = sum(st.session_state.lesson_scores.values()) / len(
            st.session_state.lesson_scores.keys()) if st.session_state.lesson_scores else 0
        st.metric("Средний балл", f"{avg_score:.1f}")
    with col3:
        percent = (len(st.session_state.lesson_scores.keys()) /
                   len(LESSONS) if st.session_state.lesson_scores else 0) * 100

        rank = None
        for p in ranks:
            if percent <= p:
                rank = ranks[p]
                break

        metric_text("Статус", rank)

    st.markdown("---")
    st.markdown("### 🎯 Что вы получите:")
    st.markdown("""
    - **Структурированные уроки** по проверенным методикам (SBI, Radical Candor, BOFF)
    - **Практику с ИИ-собеседником**, который ведёт себя как реальный сотрудник
    - **Объективную оценку** ваших навыков с метриками
    - **Библиотеку ресурсов** для дальнейшего развития
    - **Чат с ИИ-ментором**, который поможет решить проблемы
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 Начать обучение", use_container_width=True, type="primary"):
            st.session_state.page = 'lessons'
            st.rerun()
    with col2:
        if st.button("🤓 Поговорить с ментором", use_container_width=True, type="primary"):
            st.session_state.page = 'mentor_chat'
            st.rerun()
    with col3:
        st.markdown(f"""
                <a href="{os.getenv("TELEGRAM_BOT_URL")}" target="_blank" style="text-decoration: none;">
                    <button style="
                        width: 100%;
                        padding: 0.5rem 1rem;
                        background-color: #0088cc;
                        color: white;
                        border: none;
                        border-radius: 0.5rem;
                        cursor: pointer;
                        font-size: 1rem;
                        font-weight: 500;
                        margin-top: 0;
                    ">
                        🤓 Поговорить с ментором в Telegram
                    </button>
                </a>
                """, unsafe_allow_html=True)

elif st.session_state.page == 'lessons':
    st.title("📚 Уроки")

    for lesson_id, (lesson_name, lesson) in enumerate(LESSONS.items()):
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(f"{lesson_id + 1}. {lesson['title']}")
                st.markdown(f"*{lesson['description']}*")
                st.caption(f"{lesson['difficulty']} • ⏱️ {lesson['duration']}")

            with col2:
                if lesson_name in st.session_state.lesson_scores:
                    st.success(f"✅ {st.session_state.lesson_scores[lesson_name]}/100")

                if st.button("Начать урок", key=f"lesson_{lesson_name}", use_container_width=True):
                    st.session_state.current_lesson = lesson_name
                    st.session_state.role_agent = None
                    st.session_state.eval_agent = None
                    st.session_state.lesson_step = 'theory'
                    st.session_state.chat_history = []
                    st.session_state.page = 'lesson_view'
                    st.rerun()

            st.markdown("---")

elif st.session_state.page == 'lesson_view':
    lesson = LESSONS[st.session_state.current_lesson]

    if st.session_state.lesson_step == 'theory':
        progress = 0.3
    elif st.session_state.lesson_step == 'practice':
        progress = 0.7
    else:
        progress = 1.0

    st.progress(progress)

    if st.session_state.lesson_step == 'theory':
        st.title(f"📖 {lesson['title']}")

        for section in lesson['theory']:
            st.markdown(f"### {section['heading']}")
            st.markdown(section['text'])
            st.markdown("")

        if st.button("Перейти к практике →", type="primary", use_container_width=True):
            st.session_state.lesson_step = 'practice'
            st.rerun()

    elif st.session_state.lesson_step == 'practice':
        st.title("💼 Практический кейс")

        st.info(f"**Ситуация:** {lesson['case']['scenario']}")

        if 'current_role_agent' not in st.session_state or st.session_state.role_agent is None:
            st.session_state.role_agent = RoleAgent(
                mistralai_api_key=os.getenv("MISTRAL_API_KEY"),
                scenario=lesson['case']['scenario'],
                ai_role=lesson['case']['ai_role'],
                skill_name=lesson['case']['skill_name']
            )

        st.markdown("### 💬 Разговор с сотрудником")
        st.caption("ИИ-сотрудник будет реагировать на вашу обратную связь. Постарайтесь применить изученную модель.")

        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.chat_message("user").markdown(msg['content'])
            else:
                st.chat_message("assistant").markdown(msg['content'])

        user_input = st.chat_input("Ваш ответ...")

        if user_input:
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Думаю..."):
                    while True:
                        try:
                            ai_response = st.session_state.role_agent.answer(user_message=user_input)
                            break
                        except:
                            time.sleep(1)
                            continue

                st.markdown(ai_response)

            st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response})
            st.rerun()

        st.markdown("---")
        if len(st.session_state.chat_history) >= 4:
            if st.button("Завершить практику и получить оценку", type="primary", use_container_width=True):
                st.session_state.lesson_step = 'results'
                st.rerun()

    elif st.session_state.lesson_step == 'results':
        st.title("📊 Результаты")

        if 'evaluation' not in st.session_state:
            with st.spinner("Анализирую вашу обратную связь..."):
                eval_agent = EvaluationAgent(
                    mistralai_api_key=os.getenv("MISTRAL_API_KEY"),
                    expected_framework=lesson['case']['skill_name']
                )

                while True:
                    try:
                        evaluation = eval_agent.analyze(st.session_state.chat_history)
                        break
                    except:
                        time.sleep(1)
                        continue

            st.session_state.evaluation = evaluation
            st.session_state.lesson_scores[st.session_state.current_lesson] = evaluation['total_score']
        else:
            evaluation = st.session_state.evaluation

        score = evaluation['total_score']
        st.session_state.lesson_scores[st.session_state.current_lesson] = score

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.metric("Общий балл", f"{score}/100")

        st.markdown("---")

        st.markdown("### 📊 Детальная оценка")
        cols = st.columns(5)
        metric_names = {
            'specificity': 'Конкретность',
            'structure': 'Структура',
            'empathy': 'Эмпатия',
            'actionability': 'Действенность',
            'timing': 'Своевременность'
        }

        for idx, (metric_key, metric_name) in enumerate(metric_names.items()):
            with cols[idx]:
                metric_data = evaluation['metrics'][metric_key]
                st.metric(metric_name, f"{metric_data['score']}/10")
                st.caption(metric_data['comment'])

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Сильные стороны")
            for strength in evaluation['strengths']:
                st.success(f"• {strength}")

        with col2:
            st.markdown("### 📈 Области для улучшения")
            for improvement in evaluation['areas_for_improvement']:
                st.warning(f"• {improvement}")

        st.markdown("---")
        st.markdown("### 💡 Пример улучшенной обратной связи")
        st.info(evaluation['example_feedback'])

        if st.button("Вернуться к урокам", use_container_width=True):
            st.session_state.page = 'lessons'
            st.session_state.current_lesson = None
            st.session_state.current_role_agent = None
            st.session_state.pop('evaluation', None)
            st.rerun()

elif st.session_state.page == 'glossary':
    st.title("📖 Глоссарий и ресурсы")

    tab1, tab2 = st.tabs(["📚 Модели обратной связи", "🔗 Полезные ресурсы"])

    with tab1:
        st.markdown("""
        ### SBI (Situation-Behavior-Impact)
        Структурированный подход: опишите ситуацию, поведение и его влияние.

        ### BOFF (Behavior-Outcome-Feelings-Future)
        Фокус на поведении, результате, чувствах и будущих действиях.

        ### Radical Candor (Ким Скотт)
        Баланс между личной заботой и прямым вызовом.

        ### NVC (Ненасильственное общение, Маршалл Розенберг)
        Наблюдение → Чувства → Потребности → Просьба

        ### GROW (Goal-Reality-Options-Will)
        Коучинговая модель для развивающих разговоров.

        ### Модель "бутерброда"
        Позитив → Конструктивная критика → Позитив
        """)

    with tab2:
        st.markdown("""
        ### 📖 Книги

        ### 🎥 Видео и курсы

        ### 📝 Статьи
        - [3 Brilliant Examples of the SBI Feedback Model](https://managebetter.com/blog/sbi-model-feedback-examples)
        - [Improve Talent Development With Our SBI Feedback Model](https://www.ccl.org/articles/leading-effectively-articles/sbi-feedback-model-a-quick-win-to-improve-talent-conversations-development/)
        """)

elif st.session_state.page == 'progress':
    st.title("📊 Ваш прогресс")

    completed = len(st.session_state.lesson_scores)
    total = len(LESSONS)

    st.metric("Завершено уроков", f"{completed}/{total}")
    st.progress(completed / total)

    if st.session_state.lesson_scores:
        st.markdown("### 🎯 Баллы по урокам")
        for lesson_id, score in st.session_state.lesson_scores.items():
            lesson_title = LESSONS[lesson_id]['title']
            st.markdown(f"**{lesson_title}**: {score}/100")
    else:
        st.info("Пройдите первый урок, чтобы увидеть прогресс!")

elif st.session_state.page == 'info':
    st.title("📝 Информация")

    st.markdown("### 🧠 Используемый вендор: Mistral AI")

elif st.session_state.page == 'mentor_chat':
    st.title("🤓 Чат с ментором")

    st.info("Здесь вы можете получить совет по конкретной ситуации от ИИ-ментора")

    if 'current_mentor_agent' not in st.session_state or st.session_state.mentor_agent is None:
        st.session_state.mentor_agent = MentorAgent(
            mistralai_api_key=os.getenv("MISTRAL_API_KEY")
        )

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown("### 💬 Разговор с ментором")
        st.caption("Задавайте вопросы и/или описывайте ситуацию.")

    with col2:
        st.markdown(f"""
                <a href="{os.getenv("TELEGRAM_BOT_URL")}" target="_blank" style="text-decoration: none;">
                    <button style="
                        width: 100%;
                        padding: 0.5rem 0.75rem;
                        background-color: #0088cc;
                        color: white;
                        border: none;
                        border-radius: 0.5rem;
                        cursor: pointer;
                        font-size: 0.9rem;
                        font-weight: 500;
                        margin-top: 1rem;
                    ">
                        📱 В Telegram
                    </button>
                </a>
                """, unsafe_allow_html=True)

        if st.button("🧹 Очистить историю чата", use_container_width=True, type="secondary"):
            st.session_state.mentor_chat_history = []
            if st.session_state.mentor_agent:
                st.session_state.mentor_agent.clear_memory()
            st.rerun()

    for msg in st.session_state.mentor_chat_history:
        if msg['role'] == 'user':
            st.chat_message("user").markdown(msg['content'])
        else:
            st.chat_message("assistant").markdown(msg['content'])

    user_input = st.chat_input("Ваш ответ...")

    if user_input:
        st.session_state.mentor_chat_history.append({'role': 'user', 'content': user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                while True:
                    try:
                        ai_response = st.session_state.mentor_agent.answer(user_message=user_input)
                        break
                    except:
                        time.sleep(1)
                        continue

            st.markdown(ai_response)

        st.session_state.mentor_chat_history.append({'role': 'assistant', 'content': ai_response})
        st.rerun()
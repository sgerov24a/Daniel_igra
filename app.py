import streamlit as st

st.set_page_config(page_title="Въпроси", page_icon="❓", layout="centered")

# ------------------------------------------------------------------
# ДАННИ – тук въвеждаш въпросите, отговорите и верния отговор
# correct: 0 = А, 1 = Б, 2 = В, 3 = Г
# ------------------------------------------------------------------
QUESTIONS = [
    {
        "question": "Коя от посочените думи в изречението има преносно значение?",
        "options": [")Златно сърце ", ")Слънцето грее", ")Ледена вода", ")Дървена маса"],
        "correct": 0,
    },
    {
        "question": "Коя от посочените думи в изречението има преносно значение?",
        "options": [")Сладка ябълка", ")Планина от проблеми", ")Остър нож", ")Разцъфнало цвете"],
        "correct": 1,
    },
    {
        "question": "Коя от посочените думи в изречението има преносно значение?",
        "options": [")Черна котка", ")Морски бряг", ")Желязна воля", ")Каменно стълбище"],
        "correct": 2,
    },
    {
        "question": "Коя от посочените думи в изречението има преносно значение?",
        "options": [")Студена зима", ")Слънчев ден", ")Бурен вятър", ")Море от хора"],
        "correct": 3,
    },
    {
        "question": "/Тук се пише самия въпрос/",
        "options": [")Студен поглед", ")Горчив шоколад", ")Разцъфнало цвете", ")Светла стая"],
        "correct": 0,
    },
]

LETTERS = ["А", "Б", "В", "Г"]
TOTAL = len(QUESTIONS)

# Цветове
BG = "#7FD6FF"        # светло синьо (фон и полета)
PANEL = "#00A8F0"     # наситено синьо (панели)
BORDER = "#000000"
GREEN = "#2ECC40"
RED = "#FF4136"

# ------------------------------------------------------------------
# СЪСТОЯНИЕ
# ------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0          # 0..4 = въпроси, 5 = резултат
if "answers" not in st.session_state:
    st.session_state.answers = {}      # {номер_на_въпрос: избран_индекс}


def restart():
    st.session_state.page = 0
    st.session_state.answers = {}


def next_page():
    st.session_state.page += 1


def score():
    return sum(
        1
        for q, a in st.session_state.answers.items()
        if QUESTIONS[q]["correct"] == a
    )


# ------------------------------------------------------------------
# ОБЩ СТИЛ
# ------------------------------------------------------------------
BASE_CSS = f"""
<style>
#MainMenu, header, footer {{visibility: hidden;}}
.stApp {{ background: {BG}; }}
.block-container {{ max-width: 900px; padding-top: 2rem; }}

.title-pill {{
    background: {PANEL};
    border: 5px solid {BORDER};
    border-radius: 22px;
    width: 65%;
    margin: 0 auto 2.2rem auto;
    padding: 0.7rem 1rem;
    text-align: center;
    font-size: 2.2rem;
    color: #111;
}}

.st-key-panel {{
    background: {PANEL};
    border: 6px solid {BORDER} !important;
    border-radius: 40px !important;
    padding: 2rem 2.2rem 1.6rem 2.2rem;
}}

.question-box {{
    background: {BG};
    border: 5px solid {BORDER};
    border-radius: 22px;
    padding: 1.6rem 1rem;
    text-align: center;
    font-size: 1.9rem;
    color: #111;
    margin-bottom: 1.8rem;
}}

.big-text {{
    text-align: center;
    font-size: 2.2rem;
    color: #111;
}}
.score-text {{
    text-align: center;
    font-size: 4rem;
    font-weight: 700;
    color: #111;
    margin: 0.5rem 0 1rem 0;
}}

/* Всички бутони – същият стил като в дизайна */
.stButton > button {{
    background: {BG};
    color: #111;
    border: 5px solid {BORDER};
    border-radius: 20px;
    width: 100%;
    min-height: 3.4rem;
    font-size: 1.5rem;
    justify-content: flex-start;
    text-align: left;
    padding: 0.3rem 1rem;
}}
.stButton > button:hover {{
    border-color: {BORDER};
    color: #111;
    background: #A8E4FF;
}}
.stButton > button:disabled {{
    opacity: 1 !important;
    color: #111 !important;
}}
.stButton > button p {{ font-size: 1.5rem; }}

/* Бутон "Напред" / "Отначало" – центриран */
.st-key-nav .stButton > button {{
    justify-content: center;
    text-align: center;
    margin-top: 1rem;
}}
</style>
"""
st.markdown(BASE_CSS, unsafe_allow_html=True)


def answer_colors_css(q, chosen):
    """Оцветява избрания отговор в зелено (верен) или червено (грешен)."""
    if chosen is None:
        return ""
    color = GREEN if QUESTIONS[q]["correct"] == chosen else RED
    return f"""
    <style>
    .st-key-ans_{q}_{chosen} button,
    .st-key-ans_{q}_{chosen} button:disabled,
    .st-key-ans_{q}_{chosen} button:hover {{
        background: {color} !important;
        color: #111 !important;
    }}
    </style>
    """


# ------------------------------------------------------------------
# СТРАНИЦИ С ВЪПРОСИ (1–5)
# ------------------------------------------------------------------
def question_page(q):
    data = QUESTIONS[q]
    chosen = st.session_state.answers.get(q)
    answered = chosen is not None

    st.markdown(
        f'<div class="title-pill">Въпрос {q + 1}/{TOTAL}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(answer_colors_css(q, chosen), unsafe_allow_html=True)

    with st.container(border=True, key="panel"):
        st.markdown(
            f'<div class="question-box">{data["question"]}</div>',
            unsafe_allow_html=True,
        )

        left, right = st.columns(2, gap="large")
        # Ляво: А, Б  |  Дясно: В, Г
        layout = [(left, [0, 1]), (right, [2, 3])]
        for col, indexes in layout:
            with col:
                for i in indexes:
                    label = f"{LETTERS[i]}  {data['options'][i]}"
                    if st.button(
                        label,
                        key=f"ans_{q}_{i}",
                        disabled=answered,
                        use_container_width=True,
                    ):
                        st.session_state.answers[q] = i
                        st.rerun()

        if answered:
            with st.container(key="nav"):
                _, mid, _ = st.columns([1, 2, 1])
                with mid:
                    text = "Напред →" if q < TOTAL - 1 else "Виж резултата →"
                    st.button(text, key=f"next_{q}", on_click=next_page,
                              use_container_width=True)


# ------------------------------------------------------------------
# СТРАНИЦА 6 – РЕЗУЛТАТ
# ------------------------------------------------------------------
def result_page():
    s = score()
    st.markdown('<div class="title-pill">Резултат</div>', unsafe_allow_html=True)

    if s == TOTAL:
        msg = "Браво! Отличен резултат!"
    elif s >= 3:
        msg = "Браво! Добър резултат!"
    else:
        msg = "Опитай пак, можеш по-добре!"

    with st.container(border=True, key="panel"):
        st.markdown(f'<div class="question-box">{msg}</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-text">Верни отговори:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-text">{s}/{TOTAL}</div>', unsafe_allow_html=True)

        with st.container(key="nav"):
            _, mid, _ = st.columns([1, 2, 1])
            with mid:
                st.button("Опитай отново ↺", key="restart", on_click=restart,
                          use_container_width=True)


# ------------------------------------------------------------------
# РОУТИНГ
# ------------------------------------------------------------------
page = st.session_state.page
if page < TOTAL:
    question_page(page)
else:
    result_page()

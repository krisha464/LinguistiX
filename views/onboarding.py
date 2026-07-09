import streamlit as st
from utils.translator import SUPPORTED_LANGS

# ── Language list (exclude auto-detect for "I speak") ──────────────────────
SPEAK_LANGS = {k: v for k, v in SUPPORTED_LANGS.items() if k != "auto"}
LEARN_LANGS = {k: v for k, v in SUPPORTED_LANGS.items() if k != "auto"}

# Quick-win phrase shown on screen 4
QUICK_WIN_PHRASE = "Hello, how are you?"
QUICK_WIN_TRANSLATIONS = {
    "es": "Hola, ¿cómo estás?",
    "fr": "Bonjour, comment allez-vous?",
    "de": "Hallo, wie geht es Ihnen?",
    "it": "Ciao, come stai?",
    "ja": "こんにちは、お元気ですか？",
    "ko": "안녕하세요, 어떻게 지내세요?",
    "zh-CN": "你好，你好吗？",
    "hi": "नमस्ते, आप कैसे हैं?",
    "pt": "Olá, como vai você?",
    "ru": "Привет, как дела?",
    "ar": "مرحبا، كيف حالك؟",
}

TOTAL_STEPS = 4


def _inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

    /* ── Full-page reset ── */
    .stApp {
        background: linear-gradient(145deg, #F0F7FF 0%, #EAF4FF 50%, #F5F0FF 100%) !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh;
    }
    .stMainBlockContainer {
        background: transparent !important;
        padding: 2rem 1rem 3rem !important;
        max-width: 640px !important;
        margin: 0 auto !important;
    }

    /* ── Ambient blobs ── */
    .ob-blob {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.45;
        pointer-events: none;
        z-index: 0;
        animation: ob-drift 10s ease-in-out infinite;
    }
    @keyframes ob-drift {
        0%,100% { transform: scale(1) translate(0,0); }
        50%      { transform: scale(1.08) translate(12px,-14px); }
    }

    /* ── Card shell ── */
    .ob-card {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border: 1px solid rgba(255,255,255,0.95);
        border-radius: 32px;
        padding: 40px 40px 32px;
        box-shadow: 0 24px 64px rgba(15,23,42,0.10), 0 4px 16px rgba(15,23,42,0.05);
        position: relative;
        overflow: hidden;
        z-index: 1;
        animation: ob-fadein 0.35s ease-out both;
    }
    @keyframes ob-fadein {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .ob-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(99,102,241,0.08), transparent 50%),
                    radial-gradient(circle at bottom right, rgba(59,130,246,0.07), transparent 50%);
        pointer-events: none;
    }

    /* ── Progress dots ── */
    .ob-progress {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin-bottom: 36px;
    }
    .ob-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        transition: all 0.3s ease;
        flex-shrink: 0;
    }
    .ob-dot.done    { background: #4F46E5; }
    .ob-dot.active  { background: #4F46E5; width: 24px; border-radius: 999px; box-shadow: 0 0 0 4px rgba(79,70,229,0.15); }
    .ob-dot.future  { background: #CBD5E1; }
    .ob-connector {
        height: 2px;
        width: 36px;
        flex-shrink: 0;
        transition: background 0.3s ease;
    }
    .ob-connector.done   { background: #4F46E5; }
    .ob-connector.future { background: #E2E8F0; }

    /* ── Step label ── */
    .ob-step-label {
        text-align: center;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #4F46E5;
        margin-bottom: 10px;
    }

    /* ── Headings ── */
    .ob-h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 1.85rem;
        font-weight: 900;
        color: #0F172A;
        margin: 0 0 8px;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .ob-h1 span { color: #4F46E5; }
    .ob-sub {
        font-size: 0.92rem;
        color: #64748B;
        margin: 0 0 28px;
        line-height: 1.6;
    }

    /* ── Language selects ── */
    .ob-lang-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }
    .ob-lang-arrow {
        font-size: 1.3rem;
        color: #4F46E5;
        flex-shrink: 0;
        font-weight: 700;
    }
    .stSelectbox label { font-size: 0.78rem !important; font-weight: 700 !important; color: #475569 !important; text-transform: uppercase; letter-spacing: 0.8px; }
    .stSelectbox [data-baseweb="select"] {
        background: #F8FAFC !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 14px !important;
    }
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
    }

    /* ── Skill-level cards ── */
    .ob-level-grid {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 24px;
    }
    .ob-level-card {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 16px 18px;
        border-radius: 16px;
        border: 2px solid #E2E8F0;
        background: #FAFAFA;
        cursor: pointer;
        transition: all 0.18s ease;
        position: relative;
        overflow: hidden;
    }
    .ob-level-card:hover { border-color: #A5B4FC; background: #F5F3FF; transform: translateX(3px); }
    .ob-level-card.selected {
        border-color: #4F46E5;
        background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
        box-shadow: 0 0 0 1px #4F46E5;
    }
    .ob-level-icon {
        width: 46px; height: 46px;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
    }
    .ob-level-body .ob-level-title { font-size: 0.97rem; font-weight: 800; color: #0F172A; }
    .ob-level-body .ob-level-desc  { font-size: 0.8rem; color: #64748B; margin-top: 2px; }
    .ob-level-check {
        margin-left: auto;
        width: 22px; height: 22px;
        border-radius: 50%;
        border: 2px solid #CBD5E1;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem;
        color: transparent;
        flex-shrink: 0;
        transition: all 0.18s;
    }
    .ob-level-card.selected .ob-level-check {
        background: #4F46E5;
        border-color: #4F46E5;
        color: white;
    }

    /* ── Goal tiles ── */
    .ob-goal-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 24px;
    }
    .ob-goal-tile {
        padding: 20px 16px;
        border-radius: 18px;
        border: 2px solid #E2E8F0;
        background: #FAFAFA;
        cursor: pointer;
        transition: all 0.18s ease;
        text-align: center;
    }
    .ob-goal-tile:hover { border-color: #A5B4FC; transform: translateY(-2px); }
    .ob-goal-tile.selected {
        border-color: #4F46E5;
        background: linear-gradient(145deg, #EEF2FF, #F5F3FF);
        box-shadow: 0 0 0 1px #4F46E5;
    }
    .ob-goal-emoji { font-size: 1.9rem; display: block; margin-bottom: 8px; }
    .ob-goal-label { font-size: 0.88rem; font-weight: 800; color: #1E293B; }
    .ob-goal-hint  { font-size: 0.73rem; color: #64748B; margin-top: 3px; }

    /* ── Daily minute pills ── */
    .ob-minute-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 24px;
    }
    .ob-min-pill {
        padding: 10px 20px;
        border-radius: 999px;
        border: 2px solid #E2E8F0;
        background: #F8FAFC;
        font-size: 0.88rem;
        font-weight: 700;
        color: #475569;
        cursor: pointer;
        transition: all 0.18s;
    }
    .ob-min-pill:hover { border-color: #A5B4FC; color: #4F46E5; }
    .ob-min-pill.selected {
        background: #4F46E5;
        border-color: #4F46E5;
        color: #fff;
        box-shadow: 0 4px 14px rgba(79,70,229,0.3);
    }

    /* ── Quick-win box ── */
    .ob-quickwin {
        background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
        border: 1.5px solid #C7D2FE;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 24px;
    }
    .ob-quickwin-label {
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #4F46E5;
        margin-bottom: 8px;
    }
    .ob-quickwin-phrase {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 14px;
    }
    .ob-quickwin-success {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 14px;
        background: rgba(34,197,94,0.1);
        border: 1.5px solid rgba(34,197,94,0.3);
        border-radius: 12px;
        color: #15803D;
        font-weight: 700;
        font-size: 0.9rem;
    }

    /* ── CTA Button override ── */
    .ob-cta-wrap .stButton button {
        background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 14px 24px !important;
        height: auto !important;
        min-height: 54px !important;
        box-shadow: 0 8px 24px rgba(79,70,229,0.28) !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease !important;
    }
    .ob-cta-wrap .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 32px rgba(79,70,229,0.38) !important;
        filter: brightness(1.06) !important;
    }
    .ob-back-wrap .stButton button {
        background: transparent !important;
        color: #64748B !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 8px 0 !important;
        min-height: 0 !important;
        height: auto !important;
    }
    .ob-back-wrap .stButton button:hover {
        color: #4F46E5 !important;
        transform: none !important;
    }

    /* ── Floating emoji deco ── */
    .ob-deco {
        position: absolute;
        font-size: 2rem;
        opacity: 0.07;
        pointer-events: none;
        animation: ob-drift 7s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)


def _progress_dots(current_step: int):
    """Renders the shared top progress-dots bar."""
    parts = []
    for i in range(1, TOTAL_STEPS + 1):
        if i < current_step:
            dot_cls = "done"
        elif i == current_step:
            dot_cls = "active"
        else:
            dot_cls = "future"
        parts.append(f"<div class='ob-dot {dot_cls}'></div>")
        if i < TOTAL_STEPS:
            conn_cls = "done" if i < current_step else "future"
            parts.append(f"<div class='ob-connector {conn_cls}'></div>")

    st.markdown(f"""
    <div class='ob-step-label'>Step {current_step} of {TOTAL_STEPS}</div>
    <div class='ob-progress'>{''.join(parts)}</div>
    """, unsafe_allow_html=True)


def _ambient():
    st.markdown("""
    <div class='ob-blob' style='width:380px;height:380px;top:-80px;left:-100px;background:rgba(99,102,241,0.18);'></div>
    <div class='ob-blob' style='width:300px;height:300px;bottom:-60px;right:-80px;background:rgba(59,130,246,0.14);animation-delay:2s;'></div>
    <div class='ob-blob' style='width:220px;height:220px;top:40%;left:55%;background:rgba(236,72,153,0.08);animation-delay:4s;'></div>
    """, unsafe_allow_html=True)


# ───────────────────────────────────────────────
# SCREEN 1 — Language Pair
# ───────────────────────────────────────────────
def _screen_language():
    lang_options = list(SPEAK_LANGS.values())
    lang_keys    = list(SPEAK_LANGS.keys())

    st.markdown("""
    <div class='ob-card'>
        <div class='ob-deco' style='top:16px;right:24px;'>🌍</div>
        <div class='ob-deco' style='bottom:24px;left:20px;animation-delay:2s;'>🗣️</div>
    """, unsafe_allow_html=True)

    _progress_dots(1)

    st.markdown("""
        <div class='ob-h1'>Let's set you up,<br><span>one tap at a time.</span></div>
        <div class='ob-sub'>Tell us your starting language and the one you want to conquer — we'll personalise everything from here.</div>
    """, unsafe_allow_html=True)

    col_speak, col_arrow, col_learn = st.columns([5, 1, 5])
    with col_speak:
        default_speak = lang_keys.index("en") if "en" in lang_keys else 0
        speak_val = st.session_state.get("onboard_native_lang", "en")
        speak_idx = lang_keys.index(speak_val) if speak_val in lang_keys else default_speak
        native = st.selectbox("I speak", options=lang_options, index=speak_idx, key="ob_native_sel")

    with col_arrow:
        st.markdown("<div style='text-align:center;padding-top:32px;font-size:1.4rem;color:#4F46E5;'>→</div>", unsafe_allow_html=True)

    with col_learn:
        default_learn = lang_keys.index("es") if "es" in lang_keys else 1
        learn_val = st.session_state.get("onboard_target_lang", "es")
        learn_idx = lang_keys.index(learn_val) if learn_val in lang_keys else default_learn
        target = st.selectbox("I want to learn", options=lang_options, index=learn_idx, key="ob_target_sel")

    st.markdown("</div>", unsafe_allow_html=True)  # close ob-card

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='ob-cta-wrap'>", unsafe_allow_html=True)
    if st.button("Continue →", key="ob_s1_next", use_container_width=True):
        native_key  = lang_keys[lang_options.index(native)]
        target_key  = lang_keys[lang_options.index(target)]
        if native_key == target_key:
            st.error("Please choose two different languages.")
        else:
            st.session_state.onboard_native_lang = native_key
            st.session_state.onboard_target_lang = target_key
            st.session_state.onboarding_step = 2
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────
# SCREEN 2 — Skill Level
# ───────────────────────────────────────────────
def _screen_level():
    levels = [
        {"key": "beginner",     "icon": "🌱", "title": "Beginner",     "desc": "Just starting out — I know a few words at most.", "bg": "#ECFDF5", "color": "#059669"},
        {"key": "intermediate", "icon": "📚", "title": "Intermediate",  "desc": "I can hold a basic conversation but want to get sharper.", "bg": "#EFF6FF", "color": "#2563EB"},
        {"key": "advanced",     "icon": "🏆", "title": "Advanced",      "desc": "I'm fluent-ish and want to polish the finer points.", "bg": "#FFF7ED", "color": "#D97706"},
    ]
    selected = st.session_state.get("onboard_level", "")

    st.markdown("<div class='ob-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ob-deco' style='top:14px;right:22px;animation-delay:1s;'>📖</div>", unsafe_allow_html=True)

    _progress_dots(2)

    target_name = LEARN_LANGS.get(st.session_state.get("onboard_target_lang", "es"), "your language")
    st.markdown(f"""
        <div class='ob-h1'>How well do you<br><span>know {target_name}?</span></div>
        <div class='ob-sub'>We'll calibrate the difficulty of every game and exercise to exactly where you are right now.</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='ob-level-grid'>", unsafe_allow_html=True)
    for lvl in levels:
        sel_cls = "selected" if selected == lvl["key"] else ""
        check_content = "✓" if selected == lvl["key"] else ""
        st.markdown(f"""
        <div class='ob-level-card {sel_cls}' onclick='void(0)'>
            <div class='ob-level-icon' style='background:{lvl["bg"]};color:{lvl["color"]};'>{lvl["icon"]}</div>
            <div class='ob-level-body'>
                <div class='ob-level-title'>{lvl["title"]}</div>
                <div class='ob-level-desc'>{lvl["desc"]}</div>
            </div>
            <div class='ob-level-check'>{check_content}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"  {lvl['icon']}  {lvl['title']}", key=f"ob_lvl_{lvl['key']}", use_container_width=True):
            st.session_state.onboard_level = lvl["key"]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close ob-card

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 3])
    with col_back:
        st.markdown("<div class='ob-back-wrap'>", unsafe_allow_html=True)
        if st.button("← Back", key="ob_s2_back", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_next:
        st.markdown("<div class='ob-cta-wrap'>", unsafe_allow_html=True)
        if st.button("Continue →", key="ob_s2_next", use_container_width=True):
            if not st.session_state.get("onboard_level"):
                st.error("Please choose your level to continue.")
            else:
                st.session_state.onboarding_step = 3
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────
# SCREEN 3 — Goal
# ───────────────────────────────────────────────
def _screen_goal():
    goals = [
        {"key": "travel",  "emoji": "✈️", "label": "Travel",      "hint": "Order food, ask directions, explore"},
        {"key": "work",    "emoji": "💼", "label": "Work",         "hint": "Emails, meetings, presentations"},
        {"key": "exams",   "emoji": "📚", "label": "Exams",        "hint": "DELF, IELTS, JLPT preparation"},
        {"key": "fun",     "emoji": "😄", "label": "Just for fun", "hint": "Watch shows, read, enjoy culture"},
    ]
    selected = st.session_state.get("onboard_goal", "")

    st.markdown("<div class='ob-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ob-deco' style='top:14px;right:22px;animation-delay:0.5s;'>🎯</div>", unsafe_allow_html=True)

    _progress_dots(3)

    st.markdown("""
        <div class='ob-h1'>What's your <span>main goal?</span></div>
        <div class='ob-sub'>This quietly shapes which games and lessons get surfaced for you first — you can change it any time.</div>
        <div class='ob-goal-grid'>
    """, unsafe_allow_html=True)

    for goal in goals:
        sel_cls = "selected" if selected == goal["key"] else ""
        st.markdown(f"""
        <div class='ob-goal-tile {sel_cls}'>
            <span class='ob-goal-emoji'>{goal["emoji"]}</span>
            <div class='ob-goal-label'>{goal["label"]}</div>
            <div class='ob-goal-hint'>{goal["hint"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close goal-grid

    # Actual interactive buttons overlaid (Streamlit limitation workaround)
    g_col1, g_col2 = st.columns(2)
    for i, goal in enumerate(goals):
        col = g_col1 if i % 2 == 0 else g_col2
        with col:
            if st.button(f"{goal['emoji']} {goal['label']}", key=f"ob_goal_{goal['key']}", use_container_width=True):
                st.session_state.onboard_goal = goal["key"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # close ob-card

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 3])
    with col_back:
        st.markdown("<div class='ob-back-wrap'>", unsafe_allow_html=True)
        if st.button("← Back", key="ob_s3_back", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_next:
        st.markdown("<div class='ob-cta-wrap'>", unsafe_allow_html=True)
        if st.button("Continue →", key="ob_s3_next", use_container_width=True):
            if not st.session_state.get("onboard_goal"):
                st.error("Pick a goal to continue.")
            else:
                st.session_state.onboarding_step = 4
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────
# SCREEN 4 — Daily Goal + Quick Win
# ───────────────────────────────────────────────
def _screen_daily():
    minute_opts = [5, 10, 15, 20]
    selected_min = st.session_state.get("onboard_daily_minutes", 10)
    quick_done   = st.session_state.get("onboard_quick_win_done", False)

    target_key   = st.session_state.get("onboard_target_lang", "es")
    target_name  = LEARN_LANGS.get(target_key, "your language")
    correct_ans  = QUICK_WIN_TRANSLATIONS.get(target_key, "Hello, how are you?")

    st.markdown("<div class='ob-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ob-deco' style='top:14px;right:22px;animation-delay:1.5s;'>⚡</div>", unsafe_allow_html=True)

    _progress_dots(4)

    st.markdown(f"""
        <div class='ob-h1'>Almost there —<br><span>set your daily goal.</span></div>
        <div class='ob-sub'>Even 5 minutes a day builds a habit. Pick what feels achievable for you right now.</div>
    """, unsafe_allow_html=True)

    # Minute pills (rendered as buttons)
    st.markdown("<div class='ob-minute-row'>", unsafe_allow_html=True)
    min_cols = st.columns(len(minute_opts))
    for col, mins in zip(min_cols, minute_opts):
        with col:
            sel_cls = "selected" if selected_min == mins else ""
            st.markdown(f"<div class='ob-min-pill {sel_cls}' style='text-align:center;'>{mins} min</div>", unsafe_allow_html=True)
            if st.button(f"{mins} min", key=f"ob_min_{mins}", use_container_width=True):
                st.session_state.onboard_daily_minutes = mins
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick-win task
    st.markdown(f"""
    <div class='ob-quickwin'>
        <div class='ob-quickwin-label'>⚡ Your first win — right now</div>
        <div class='ob-quickwin-phrase'>How do you say "{QUICK_WIN_PHRASE}" in {target_name}?</div>
    """, unsafe_allow_html=True)

    if quick_done:
        st.markdown(f"""
        <div class='ob-quickwin-success'>
            ✅ &nbsp; Perfect! <strong>{correct_ans}</strong> — you're already learning!
        </div>
        """, unsafe_allow_html=True)
    else:
        user_ans = st.text_input(
            "Type your answer",
            placeholder=f"Type in {target_name}…",
            key="ob_quickwin_input",
            label_visibility="collapsed"
        )
        if st.button("Check ✓", key="ob_quickwin_check", use_container_width=True):
            if user_ans.strip().lower() == correct_ans.lower():
                st.session_state.onboard_quick_win_done = True
                st.rerun()
            else:
                st.error(f"Not quite — the answer is: **{correct_ans}**")
                st.info("You can still continue — this is just a warm-up!")

    st.markdown("</div>", unsafe_allow_html=True)   # close quickwin
    st.markdown("</div>", unsafe_allow_html=True)   # close ob-card

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 3])
    with col_back:
        st.markdown("<div class='ob-back-wrap'>", unsafe_allow_html=True)
        if st.button("← Back", key="ob_s4_back", use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_next:
        cta_label = "🎉 Enter LinguistiX →" if quick_done else "Skip & Enter LinguistiX →"
        st.markdown("<div class='ob-cta-wrap'>", unsafe_allow_html=True)
        if st.button(cta_label, key="ob_s4_finish", use_container_width=True):
            st.session_state.onboard_done        = True
            st.session_state.page                = "main"
            # Persist daily goal into session for other parts of the app to read
            st.session_state.onboard_daily_minutes = selected_min
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ───────────────────────────────────────────────
# ENTRY POINT
# ───────────────────────────────────────────────
def render_onboarding():
    _inject_styles()
    _ambient()

    step = st.session_state.get("onboarding_step", 1)

    if step == 1:
        _screen_language()
    elif step == 2:
        _screen_level()
    elif step == 3:
        _screen_goal()
    elif step == 4:
        _screen_daily()
    else:
        # Safety fallback
        st.session_state.onboarding_step = 1
        st.rerun()

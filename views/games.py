import base64
import io
import random
import struct
import time
import wave

import streamlit as st

from utils.speech import text_to_speech

GAME_LENGTH = 8

GAME_LIBRARY = [
    {
        "id": "word_quest",
        "label": "Word Quest",
        "description": "Choose the correct translation from smart multiple-choice options.",
        "icon": "🧠",
        "accent": "#4F46E5",
        "background": "#EEF2FF",
        "watermark": "🧠",
        "level": "beginner",
    },
    {
        "id": "story_master",
        "label": "Story Master",
        "description": "Fill the blank with the word that fits the context best.",
        "icon": "📖",
        "accent": "#F59E0B",
        "background": "#FFFBEB",
        "watermark": "📚",
        "level": "intermediate",
    },
    {
        "id": "lightning_blitz",
        "label": "Lightning Blitz",
        "description": "Race the clock with quick-fire translation prompts.",
        "icon": "⚡",
        "accent": "#EF4444",
        "background": "#FEF2F2",
        "watermark": "⚡",
        "level": "beginner",
    },
    {
        "id": "word_detective",
        "label": "Word Detective",
        "description": "Use clues and deduction to crack the hidden word.",
        "icon": "🕵️",
        "accent": "#10B981",
        "background": "#ECFDF5",
        "watermark": "🔎",
        "level": "advanced",
    },
    {
        "id": "sentence_scramble",
        "label": "Sentence Scramble",
        "description": "Rebuild the sentence by ordering shuffled word chips.",
        "icon": "🧩",
        "accent": "#06B6D4",
        "background": "#ECFEFF",
        "watermark": "🧩",
        "level": "intermediate",
    },
    {
        "id": "listening_ear",
        "label": "Listening Ear",
        "description": "Hear a phrase and pick the meaning you hear.",
        "icon": "🎧",
        "accent": "#8B5CF6",
        "background": "#F5F3FF",
        "watermark": "🎧",
        "level": "intermediate",
    },
    {
        "id": "grammar_gauntlet",
        "label": "Grammar Gauntlet",
        "description": "Spot the error, then choose the fix that makes the sentence right.",
        "icon": "📝",
        "accent": "#EC4899",
        "background": "#FDF2F8",
        "watermark": "✍️",
        "level": "advanced",
    },
    {
        "id": "picture_match",
        "label": "Picture Match",
        "description": "Match the visual cue to the correct word without reading the source.",
        "icon": "🖼️",
        "accent": "#0EA5E9",
        "background": "#F0F9FF",
        "watermark": "🖼️",
        "level": "beginner",
    },
]

GAME_THEMES = {game["id"]: game for game in GAME_LIBRARY}

WORD_QUEST_BANK = [
    {"word": "Bonjour", "correct_translation": "Hello", "wrong_options": ["Goodbye", "House", "River"], "difficulty": "beginner", "language_pair": "fr→en"},
    {"word": "Libro", "correct_translation": "Book", "wrong_options": ["Door", "Moon", "Apple"], "difficulty": "beginner", "language_pair": "es→en"},
    {"word": "Mañana", "correct_translation": "Tomorrow", "wrong_options": ["Yesterday", "Today", "Morning"], "difficulty": "intermediate", "language_pair": "es→en"},
    {"word": "Courage", "correct_translation": "Bravery", "wrong_options": ["Silence", "Weather", "Fury"], "difficulty": "advanced", "language_pair": "fr→en"},
]

STORY_BANK = [
    {"prompt": "The rain fell softly across the ______ field.", "answer": "quiet", "options": ["quiet", "bright", "tasty", "rapid"], "hint": "adjective"},
    {"prompt": "She decided to ______ the old lantern before sunset.", "answer": "repair", "options": ["repair", "borrow", "ignore", "scream"], "hint": "verb"},
    {"prompt": "The chef served a ______ meal to the guests.", "answer": "delicious", "options": ["delicious", "metal", "ancient", "curly"], "hint": "adjective"},
]

LIGHTNING_BANK = [
    {"prompt": "Translate 'Water' to Spanish", "answer": "Agua", "options": ["Agua", "Tierra", "Cielo", "Fuego"]},
    {"prompt": "Translate 'Friend' to French", "answer": "Ami", "options": ["Ami", "Maison", "Voiture", "Lune"]},
    {"prompt": "Translate 'Sun' to Italian", "answer": "Sole", "options": ["Sole", "Mare", "Casa", "Pietra"]},
]

DETECTIVE_BANK = [
    {"definition": "A place where books are kept", "category": "building", "first_letter": "l", "example": "I borrowed a novel from the ________.", "answer": "library"},
    {"definition": "A person who writes stories", "category": "job", "first_letter": "a", "example": "The ________ published a new fairy tale.", "answer": "author"},
    {"definition": "A vehicle that carries people across water", "category": "transport", "first_letter": "b", "example": "We crossed the river by ________.", "answer": "boat"},
]

SCRAMBLE_BANK = [
    {"source": "I enjoy learning languages", "target": ["I", "enjoy", "learning", "languages"]},
    {"source": "She reads every morning", "target": ["She", "reads", "every", "morning"]},
    {"source": "We travel together often", "target": ["We", "travel", "together", "often"]},
]

LISTENING_BANK = [
    {"audio_text": "Good morning", "correct_translation": "Buenos días", "options": ["Buenos días", "Buenas noches", "Gracias", "Adiós"], "lang": "es"},
    {"audio_text": "Thank you", "correct_translation": "Merci", "options": ["Merci", "Bonjour", "Oui", "Non"], "lang": "fr"},
    {"audio_text": "Please wait", "correct_translation": "Por favor espere", "options": ["Por favor espere", "Pase por aquí", "Estoy listo", "No entiendo"], "lang": "es"},
]

GRAMMAR_BANK = [
    {"sentence": "She go to school every day.", "error_word_index": 1, "correct_word": "goes", "options": ["go", "goes", "gone", "going"]},
    {"sentence": "They has finished the task.", "error_word_index": 1, "correct_word": "have", "options": ["has", "have", "had", "having"]},
    {"sentence": "I am reading a interesting book.", "error_word_index": 4, "correct_word": "interesting", "options": ["interesting", "interest", "interested", "interestingly"]},
]

PICTURE_BANK = [
    {"emoji": "🍎", "word": "apple", "options": ["apple", "car", "book", "house"]},
    {"emoji": "🚗", "word": "car", "options": ["car", "tree", "cat", "sun"]},
    {"emoji": "🏠", "word": "house", "options": ["house", "shoe", "chair", "river"]},
]


def _theme_for(game_id):
    return GAME_THEMES.get(game_id, GAME_LIBRARY[0])


def _generate_tone_bytes(frequency=880, duration_ms=140, volume=0.2):
    sample_rate = 22050
    total_samples = int(sample_rate * duration_ms / 1000)
    amplitude = int(32767 * volume)
    data = bytearray()
    for i in range(total_samples):
        value = int(amplitude * (0.5 + 0.5 * (i / max(total_samples, 1))))
        if frequency:
            value = int(value * (0.5 + 0.5 * (1 + 0.5 * (i % 2))))
        data.extend(struct.pack("<h", value))
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data)
    return wav_buffer.getvalue()


def _play_sound(correct=True):
    freq = 880 if correct else 320
    sound_bytes = _generate_tone_bytes(frequency=freq)
    b64_audio = base64.b64encode(sound_bytes).decode("ascii")
    st.components.v1.html(
        f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{b64_audio}" type="audio/wav">
        </audio>
        """,
        height=0,
    )


def _render_hearts(game_id):
    hearts = st.session_state.get(f"{game_id}_hearts", 3)
    return f"<div style='font-size:1.1rem; margin-bottom:10px;'>{'❤️' * hearts}{'🤍' * max(0, 3 - hearts)}</div>"


def _reset_game_state(game_id):
    st.session_state[f"{game_id}_hearts"] = 3
    st.session_state[f"{game_id}_game_over"] = False


def _ensure_stats(game_id):
    stats = st.session_state.setdefault("game_stats", {})
    state = stats.setdefault(game_id, {"score": 0, "total": 0, "streak": 0, "best_streak": 0, "xp": 0})
    return state


def _render_game_header(game_id, title, subtitle, step, total_steps, stats):
    theme = _theme_for(game_id)
    return f"""
    <div style='background: linear-gradient(135deg, {theme['accent']}22, {theme['background']}); border:1px solid {theme['accent']}33; border-radius:24px; padding:18px; margin-bottom:16px;'>
        <div class='game-header-row'>
            <div style='display:flex; align-items:center; gap:12px;'>
                <div style='width:44px; height:44px; border-radius:16px; display:flex; align-items:center; justify-content:center; background: linear-gradient(135deg, {theme['accent']}, {theme['accent']}); color:#fff; font-size:1.25rem;'>
                    {theme['icon']}
                </div>
                <div>
                    <div style='font-size:1.05rem; color:var(--text-primary); font-weight:800;'>{title}</div>
                    <div style='font-size:0.95rem; color:var(--text-secondary); margin-top:2px;'>{subtitle}</div>
                </div>
            </div>
            <div class='game-meta'>
                <span class='game-status-pill' style='border-color:{theme['accent']}; color:{theme['accent']};'>Round {step}/{total_steps}</span>
                <span class='game-status-pill' style='border-color:{theme['accent']}; color:{theme['accent']};'>🏆 {stats['score']}/{stats['total']}</span>
                <span class='game-status-pill' style='border-color:{theme['accent']}; color:{theme['accent']};'>⚡ {stats['streak']} streak</span>
            </div>
        </div>
    </div>
    """


def _render_question_shell(game_id, title, subtitle):
    theme = _theme_for(game_id)
    return f"""
    <div class='game-question-shell' style='background:{theme['background']}; border:1px solid {theme['accent']}33; position:relative; overflow:hidden;'>
        <div style='position:absolute; right:18px; bottom:14px; font-size:72px; opacity:0.06; pointer-events:none;'>{theme['watermark']}</div>
        <div style='position:relative; z-index:1;'>
            <h2 style='margin:0; color:var(--text-primary); line-height:1.35;'>{title}</h2>
            <p style='margin:10px 0 0; color:var(--text-secondary); font-size:0.96rem;'>{subtitle}</p>
        </div>
    </div>
    """


def _update_score(game_id, correct, xp_gain):
    stats = _ensure_stats(game_id)
    stats["total"] += 1
    if correct:
        stats["score"] += 1
        stats["streak"] += 1
        stats["best_streak"] = max(stats["best_streak"], stats["streak"])
        stats["xp"] += xp_gain
        return True
    stats["streak"] = 0
    hearts = st.session_state.get(f"{game_id}_hearts", 3)
    st.session_state[f"{game_id}_hearts"] = max(0, hearts - 1)
    if st.session_state[f"{game_id}_hearts"] == 0:
        st.session_state[f"{game_id}_game_over"] = True
    return False


@st.dialog("🎮 Game Zone", width="large")
def render_word_games():
    if "word_games_selected" not in st.session_state:
        st.session_state.word_games_selected = None

    game_id = st.session_state.word_games_selected

    st.markdown("""
    <style>
        .game-shell {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 10px 24px var(--glow);
            margin-bottom: 16px;
        }
        .game-choice {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 8px;
            border: 1px solid var(--border);
            background: var(--panel);
            color: var(--text-primary);
        }
        .game-choice.choice-correct { border-color: var(--accent); color: var(--accent); }
        .game-choice.choice-incorrect { border-color: var(--accent-secondary); color: var(--text-primary); }
        .game-header-row {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            align-items: center;
        }
        .game-meta {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .game-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.88);
            color: var(--text-primary);
            font-weight: 700;
            font-size: 0.9rem;
        }
        .game-question-shell {
            padding: 18px;
            border-radius: 20px;
            background: #FFFFFF;
            border: 1px solid rgba(209, 213, 219, 0.6);
            box-shadow: 0 16px 34px rgba(15, 23, 42, 0.08);
            margin-bottom: 16px;
        }
        .game-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border-radius: 999px;
            margin: 4px;
            border: 1px solid var(--border);
            background: var(--panel);
        }
    </style>
    """, unsafe_allow_html=True)

    if not game_id:
        st.markdown("<p style='font-size:1.1rem; color:var(--accent); font-weight:700;'>Pick a challenge and start practicing.</p>", unsafe_allow_html=True)
        grouped_games = {
            "🌱 Beginner": [game for game in GAME_LIBRARY if game.get("level") == "beginner"],
            "📚 Intermediate": [game for game in GAME_LIBRARY if game.get("level") == "intermediate"],
            "🏆 Advanced": [game for game in GAME_LIBRARY if game.get("level") == "advanced"],
        }
        for section_title, games in grouped_games.items():
            st.markdown(f"<div style='font-size:1rem; font-weight:800; color:var(--text-primary); margin:16px 0 8px;'>{section_title}</div>", unsafe_allow_html=True)
            for game in games:
                theme = _theme_for(game["id"])
                st.markdown(f"""
                <div class='game-shell' style='border-top:4px solid {theme['accent']};'>
                    <div style='display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;'>
                        <div>
                            <div style='font-size:1rem; font-weight:800; color:var(--text-primary);'>{game['icon']} {game['label']}</div>
                            <div style='font-size:0.92rem; color:var(--text-secondary); margin-top:4px;'>{game['description']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{game['icon']} {game['label']}", key=f"launch_{game['id']}", use_container_width=True):
                    _reset_game_state(game["id"])
                    st.session_state.word_games_selected = game["id"]
                    st.rerun()
        return

    theme = _theme_for(game_id)
    stats = _ensure_stats(game_id)
    if f"{game_id}_hearts" not in st.session_state:
        _reset_game_state(game_id)

    if game_id == "word_quest":
        if f"{game_id}_question" not in st.session_state:
            q = random.choice(WORD_QUEST_BANK)
            st.session_state[f"{game_id}_question"] = q
            st.session_state[f"{game_id}_feedback"] = None
            st.session_state[f"{game_id}_selected_answer"] = None

        q = st.session_state[f"{game_id}_question"]
        st.markdown(_render_game_header(game_id, "Word Quest", f"Choose the best translation for {q['word']}", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, f"What does '{q['word']}' mean?", "Pick the correct translation from four options."), unsafe_allow_html=True)

        options = [q["correct_translation"], *q["wrong_options"]]
        random.shuffle(options)
        feedback = st.session_state[f"{game_id}_feedback"]
        for option in options:
            if feedback is None:
                if st.button(option, key=f"{game_id}_{option}", use_container_width=True):
                    st.session_state[f"{game_id}_selected_answer"] = option
                    correct = option == q["correct_translation"]
                    answered_correctly = _update_score(game_id, correct, 60)
                    if correct:
                        _play_sound(True)
                        st.session_state[f"{game_id}_feedback"] = "correct"
                        if stats["score"] == stats["total"] and stats["total"] > 0:
                            st.balloons()
                    else:
                        _play_sound(False)
                        st.session_state[f"{game_id}_feedback"] = "incorrect"
                    st.rerun()
            else:
                cls = "choice-correct" if option == q["correct_translation"] else "choice-incorrect" if option == st.session_state[f"{game_id}_selected_answer"] else ""
                icon = "✅" if option == q["correct_translation"] else "❌" if option == st.session_state[f"{game_id}_selected_answer"] else "•"
                st.markdown(f"<div class='game-choice {cls}'>{icon} {option}</div>", unsafe_allow_html=True)

        if feedback is not None:
            if feedback == "correct":
                st.success(f"Correct! +60 XP • {q['word']} means {q['correct_translation']}.")
            else:
                st.error(f"Not quite. The best answer was {q['correct_translation']}.")
                if st.session_state[f"{game_id}_hearts"] == 0:
                    st.error("Hearts exhausted. Reset to try again.")
            c1, c2 = st.columns([2, 1])
            with c1:
                if st.button("Next question", key=f"{game_id}_next"):
                    st.session_state[f"{game_id}_question"] = random.choice(WORD_QUEST_BANK)
                    st.session_state[f"{game_id}_feedback"] = None
                    st.session_state[f"{game_id}_selected_answer"] = None
                    st.rerun()
            with c2:
                if st.button("Back", key=f"{game_id}_back"):
                    st.session_state.word_games_selected = None
                    st.rerun()

    elif game_id == "story_master":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(STORY_BANK)
            st.session_state[f"{game_id}_feedback"] = None
            st.session_state[f"{game_id}_selected_answer"] = None
            st.session_state[f"{game_id}_show_hint"] = False

        q = st.session_state[f"{game_id}_question"]
        st.markdown(_render_game_header(game_id, "Story Master", "Fill the blank with the word that fits best", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, q["prompt"], "Choose the best word from the list."), unsafe_allow_html=True)

        if st.session_state[f"{game_id}_show_hint"]:
            st.info(f"Hint: the missing word is a {q['hint']}.")

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("💡 Show hint", key=f"{game_id}_hint"):
                st.session_state[f"{game_id}_show_hint"] = True
                st.rerun()
        with col2:
            if st.button("Skip", key=f"{game_id}_skip"):
                st.session_state[f"{game_id}_question"] = random.choice(STORY_BANK)
                st.session_state[f"{game_id}_show_hint"] = False
                st.session_state[f"{game_id}_feedback"] = None
                st.session_state[f"{game_id}_selected_answer"] = None
                st.rerun()

        feedback = st.session_state[f"{game_id}_feedback"]
        for option in q["options"]:
            if feedback is None:
                if st.button(option, key=f"{game_id}_option_{option}", use_container_width=True):
                    correct = option == q["answer"]
                    _update_score(game_id, correct, 55)
                    st.session_state[f"{game_id}_selected_answer"] = option
                    if correct:
                        _play_sound(True)
                        st.session_state[f"{game_id}_feedback"] = "correct"
                    else:
                        _play_sound(False)
                        st.session_state[f"{game_id}_feedback"] = "incorrect"
                    st.rerun()
            else:
                cls = "choice-correct" if option == q["answer"] else "choice-incorrect" if option == st.session_state[f"{game_id}_selected_answer"] else ""
                icon = "✅" if option == q["answer"] else "❌" if option == st.session_state[f"{game_id}_selected_answer"] else "•"
                st.markdown(f"<div class='game-choice {cls}'>{icon} {option}</div>", unsafe_allow_html=True)

        if feedback is not None:
            st.success("Nice job! The sentence now reads naturally.") if feedback == "correct" else st.error(f"The best fit was {q['answer']}.")
            if st.button("Next", key=f"{game_id}_next"):
                st.session_state[f"{game_id}_question"] = random.choice(STORY_BANK)
                st.session_state[f"{game_id}_feedback"] = None
                st.session_state[f"{game_id}_selected_answer"] = None
                st.session_state[f"{game_id}_show_hint"] = False
                st.rerun()

    elif game_id == "lightning_blitz":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(LIGHTNING_BANK)
            st.session_state[f"{game_id}_feedback"] = None
            st.session_state[f"{game_id}_selected_answer"] = None
            st.session_state[f"{game_id}_deadline"] = time.time() + 7
            st.session_state[f"{game_id}_response_time"] = None
            st.session_state[f"{game_id}_round_answers"] = 0
            st.session_state[f"{game_id}_round_correct"] = 0
            st.session_state[f"{game_id}_round_times"] = []

        q = st.session_state[f"{game_id}_question"]
        deadline = st.session_state[f"{game_id}_deadline"]
        remaining = max(0, int(deadline - time.time()))
        timer_color = "#16A34A" if remaining > 4 else "#D97706" if remaining > 2 else "#DC2626"
        st.markdown(_render_game_header(game_id, "Lightning Blitz", "Answer before the timer hits zero", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, q["prompt"], "Fast, simple, and focused on accuracy."), unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.1rem; font-weight:800; color:{timer_color}; margin-bottom:14px;'>⏱ {remaining}s remaining</div>", unsafe_allow_html=True)

        feedback = st.session_state[f"{game_id}_feedback"]
        for option in q["options"]:
            if feedback is None:
                if st.button(option, key=f"{game_id}_{option}", use_container_width=True):
                    elapsed = round(time.time() - (deadline - 7), 2)
                    correct = option == q["answer"]
                    st.session_state[f"{game_id}_response_time"] = elapsed
                    st.session_state[f"{game_id}_round_answers"] += 1
                    if correct:
                        st.session_state[f"{game_id}_round_correct"] += 1
                    st.session_state[f"{game_id}_round_times"].append(elapsed)
                    _update_score(game_id, correct, 45)
                    if correct:
                        _play_sound(True)
                        st.session_state[f"{game_id}_feedback"] = "correct"
                    else:
                        _play_sound(False)
                        st.session_state[f"{game_id}_feedback"] = "incorrect"
                    st.session_state[f"{game_id}_selected_answer"] = option
                    st.rerun()
            else:
                cls = "choice-correct" if option == q["answer"] else "choice-incorrect" if option == st.session_state[f"{game_id}_selected_answer"] else ""
                icon = "✅" if option == q["answer"] else "❌" if option == st.session_state[f"{game_id}_selected_answer"] else "•"
                st.markdown(f"<div class='game-choice {cls}'>{icon} {option}</div>", unsafe_allow_html=True)

        if remaining == 0 and feedback is None:
            st.warning("Time is up. The round ends here.")
            if st.button("Show summary", key=f"{game_id}_summary"):
                st.session_state[f"{game_id}_feedback"] = "timeout"
                st.rerun()

        if feedback in {"correct", "incorrect", "timeout"}:
            avg_time = round(sum(st.session_state[f"{game_id}_round_times"]) / len(st.session_state[f"{game_id}_round_times"]), 2) if st.session_state[f"{game_id}_round_times"] else 0
            st.markdown(f"<div class='game-shell'><strong>Round summary</strong><br>Answered: {st.session_state[f'{game_id}_round_answers']}<br>Average response time: {avg_time}s<br>Best streak: {stats['best_streak']}</div>", unsafe_allow_html=True)
            if st.button("Play again", key=f"{game_id}_again"):
                st.session_state[f"{game_id}_question"] = random.choice(LIGHTNING_BANK)
                st.session_state[f"{game_id}_feedback"] = None
                st.session_state[f"{game_id}_selected_answer"] = None
                st.session_state[f"{game_id}_deadline"] = time.time() + 7
                st.session_state[f"{game_id}_response_time"] = None
                st.session_state[f"{game_id}_round_answers"] = 0
                st.session_state[f"{game_id}_round_correct"] = 0
                st.session_state[f"{game_id}_round_times"] = []
                st.rerun()

    elif game_id == "word_detective":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(DETECTIVE_BANK)
            st.session_state[f"{game_id}_feedback"] = None
            st.session_state[f"{game_id}_guess"] = ""
            st.session_state[f"{game_id}_reveal_count"] = 0
            st.session_state[f"{game_id}_revealed_clues"] = []

        q = st.session_state[f"{game_id}_question"]
        st.markdown(_render_game_header(game_id, "Word Detective", "Use the clues to guess the hidden word", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, "Clues", f"Definition: {q['definition']}"), unsafe_allow_html=True)

        clues = [f"Category: {q['category']}"]
        if st.session_state[f"{game_id}_reveal_count"] >= 1:
            clues.append(f"First letter: {q['first_letter'].upper()}")
        if st.session_state[f"{game_id}_reveal_count"] >= 2:
            clues.append(f"Example: {q['example']}")

        for clue in clues:
            st.markdown(f"- {clue}")

        if st.button(f"Reveal clue (-10 XP)", key=f"{game_id}_reveal"):
            if stats["xp"] >= 10:
                st.session_state[f"{game_id}_reveal_count"] += 1
                stats["xp"] -= 10
                st.rerun()
            else:
                st.info("You need at least 10 XP to reveal a clue.")

        guess = st.text_input("Your guess", key=f"{game_id}_guess_input")
        if st.button("Submit guess", key=f"{game_id}_submit"):
            correct = guess.strip().lower() == q["answer"].lower()
            _update_score(game_id, correct, 70)
            if correct:
                _play_sound(True)
                st.session_state[f"{game_id}_feedback"] = "correct"
            else:
                _play_sound(False)
                st.session_state[f"{game_id}_feedback"] = "incorrect"
            st.rerun()

        if st.session_state[f"{game_id}_feedback"] == "correct":
            st.success(f"Correct! The answer was {q['answer']}.")
        elif st.session_state[f"{game_id}_feedback"] == "incorrect":
            st.error(f"Not quite. The answer was {q['answer']}.")
            if st.button("Try another", key=f"{game_id}_another"):
                st.session_state[f"{game_id}_question"] = random.choice(DETECTIVE_BANK)
                st.session_state[f"{game_id}_feedback"] = None
                st.session_state[f"{game_id}_guess"] = ""
                st.session_state[f"{game_id}_reveal_count"] = 0
                st.rerun()

    elif game_id == "sentence_scramble":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(SCRAMBLE_BANK)
            st.session_state[f"{game_id}_placed_words"] = []
            st.session_state[f"{game_id}_feedback"] = None

        q = st.session_state[f"{game_id}_question"]
        expected = q["target"]
        st.markdown(_render_game_header(game_id, "Sentence Scramble", "Rebuild the sentence by tapping the chips", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, "Arrange the words", "Tap words into the answer tray from left to right."), unsafe_allow_html=True)

        placed = st.session_state[f"{game_id}_placed_words"]
        bank = [word for word in expected if word not in placed]

        st.markdown("<div style='margin-bottom:10px;'><strong>Answer tray</strong></div>", unsafe_allow_html=True)
        if placed:
            for word in placed:
                if st.button(word, key=f"{game_id}_placed_{word}", use_container_width=False):
                    placed.remove(word)
                    st.session_state[f"{game_id}_placed_words"] = placed
                    st.rerun()
        else:
            st.caption("No words placed yet.")

        st.markdown("<div style='margin:10px 0;'><strong>Word bank</strong></div>", unsafe_allow_html=True)
        for word in bank:
            if st.button(word, key=f"{game_id}_bank_{word}"):
                placed.append(word)
                st.session_state[f"{game_id}_placed_words"] = placed
                st.rerun()

        if st.button("Undo", key=f"{game_id}_undo") and placed:
            placed.pop()
            st.session_state[f"{game_id}_placed_words"] = placed
            st.rerun()

        if st.button("Check order", key=f"{game_id}_check"):
            if placed:
                matched = sum(1 for idx, word in enumerate(placed) if idx < len(expected) and word == expected[idx])
                ratio = matched / len(expected)
                correct = placed == expected
                _update_score(game_id, correct, 40 + int(ratio * 20))
                if correct:
                    _play_sound(True)
                    st.session_state[f"{game_id}_feedback"] = "correct"
                else:
                    _play_sound(False)
                    st.session_state[f"{game_id}_feedback"] = "partial"
                st.rerun()

        if st.session_state[f"{game_id}_feedback"] == "correct":
            st.success("Perfect order! The sentence is rebuilt.")
        elif st.session_state[f"{game_id}_feedback"] == "partial":
            st.info("Very close! Your order is partially correct.")

        if st.button("New sentence", key=f"{game_id}_new"):
            st.session_state[f"{game_id}_question"] = random.choice(SCRAMBLE_BANK)
            st.session_state[f"{game_id}_placed_words"] = []
            st.session_state[f"{game_id}_feedback"] = None
            st.rerun()

    elif game_id == "listening_ear":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(LISTENING_BANK)
            st.session_state[f"{game_id}_feedback"] = None
            st.session_state[f"{game_id}_selected_answer"] = None
            st.session_state[f"{game_id}_replays"] = 0
            st.session_state[f"{game_id}_audio"] = None
            st.session_state[f"{game_id}_slow_mode"] = False

        q = st.session_state[f"{game_id}_question"]
        st.markdown(_render_game_header(game_id, "Listening Ear", "Listen and choose the translation you hear", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, f"Hear: {q['audio_text']}", "Use the replay button if you need another listen."), unsafe_allow_html=True)

        st.checkbox("Slow playback", value=st.session_state[f"{game_id}_slow_mode"], key=f"{game_id}_slow_toggle")

        if st.button("▶ Play audio", key=f"{game_id}_play"):
            audio_bytes = text_to_speech(q["audio_text"], lang=q["lang"])
            st.session_state[f"{game_id}_audio"] = audio_bytes
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")

        if st.session_state[f"{game_id}_audio"]:
            st.audio(st.session_state[f"{game_id}_audio"], format="audio/mp3")

        if st.button(f"Replay ({3 - st.session_state[f'{game_id}_replays']}/3)", key=f"{game_id}_replay") and st.session_state[f"{game_id}_replays"] < 3:
            st.session_state[f"{game_id}_replays"] += 1
            audio_bytes = text_to_speech(q["audio_text"], lang=q["lang"])
            st.session_state[f"{game_id}_audio"] = audio_bytes
            st.rerun()

        for option in q["options"]:
            if st.session_state[f"{game_id}_feedback"] is None:
                if st.button(option, key=f"{game_id}_choice_{option}", use_container_width=True):
                    correct = option == q["correct_translation"]
                    _update_score(game_id, correct, 50)
                    st.session_state[f"{game_id}_selected_answer"] = option
                    if correct:
                        _play_sound(True)
                        st.session_state[f"{game_id}_feedback"] = "correct"
                    else:
                        _play_sound(False)
                        st.session_state[f"{game_id}_feedback"] = "incorrect"
                    st.rerun()
            else:
                cls = "choice-correct" if option == q["correct_translation"] else "choice-incorrect" if option == st.session_state[f"{game_id}_selected_answer"] else ""
                icon = "✅" if option == q["correct_translation"] else "❌" if option == st.session_state[f"{game_id}_selected_answer"] else "•"
                st.markdown(f"<div class='game-choice {cls}'>{icon} {option}</div>", unsafe_allow_html=True)

        if st.session_state[f"{game_id}_feedback"] is not None:
            if st.session_state[f"{game_id}_feedback"] == "correct":
                st.success(f"Correct! The phrase means {q['correct_translation']}.")
            else:
                st.error(f"The correct meaning was {q['correct_translation']}.")
            if st.button("New prompt", key=f"{game_id}_new"):
                st.session_state[f"{game_id}_question"] = random.choice(LISTENING_BANK)
                st.session_state[f"{game_id}_feedback"] = None
                st.session_state[f"{game_id}_selected_answer"] = None
                st.session_state[f"{game_id}_replays"] = 0
                st.session_state[f"{game_id}_audio"] = None
                st.rerun()

    elif game_id == "grammar_gauntlet":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(GRAMMAR_BANK)
            st.session_state[f"{game_id}_feedback"] = None
            st.session_state[f"{game_id}_selected_word_index"] = None
            st.session_state[f"{game_id}_selected_fix"] = None

        q = st.session_state[f"{game_id}_question"]
        st.markdown(_render_game_header(game_id, "Grammar Gauntlet", "Tap the incorrect word, then choose the correction", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        words = q["sentence"].split()
        st.markdown(_render_question_shell(game_id, q["sentence"], "Choose the mistaken word first."), unsafe_allow_html=True)

        for idx, word in enumerate(words):
            if st.button(word, key=f"{game_id}_word_{idx}"):
                st.session_state[f"{game_id}_selected_word_index"] = idx
                st.rerun()

        if st.session_state[f"{game_id}_selected_word_index"] is not None:
            st.info(f"Selected word index: {st.session_state[f'{game_id}_selected_word_index'] + 1}")
            for option in q["options"]:
                if st.button(option, key=f"{game_id}_fix_{option}"):
                    correct = option == q["correct_word"]
                    _update_score(game_id, correct, 60)
                    st.session_state[f"{game_id}_selected_fix"] = option
                    if correct:
                        _play_sound(True)
                        st.session_state[f"{game_id}_feedback"] = "correct"
                    else:
                        _play_sound(False)
                        st.session_state[f"{game_id}_feedback"] = "incorrect"
                    st.rerun()

        if st.session_state[f"{game_id}_feedback"] == "correct":
            st.success(f"Correct fix: {q['correct_word']}")
        elif st.session_state[f"{game_id}_feedback"] == "incorrect":
            st.error(f"The right correction was {q['correct_word']}.")

    elif game_id == "picture_match":
        if f"{game_id}_question" not in st.session_state:
            st.session_state[f"{game_id}_question"] = random.choice(PICTURE_BANK)
            st.session_state[f"{game_id}_feedback"] = None

        q = st.session_state[f"{game_id}_question"]
        st.markdown(_render_game_header(game_id, "Picture Match", "Match the visual to the best word", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:5rem; text-align:center; margin:18px 0;'>{q['emoji']}</div>", unsafe_allow_html=True)
        for option in q["options"]:
            if st.session_state[f"{game_id}_feedback"] is None:
                if st.button(option, key=f"{game_id}_{option}", use_container_width=True):
                    correct = option == q["word"]
                    _update_score(game_id, correct, 50)
                    if correct:
                        _play_sound(True)
                        st.session_state[f"{game_id}_feedback"] = "correct"
                    else:
                        _play_sound(False)
                        st.session_state[f"{game_id}_feedback"] = "incorrect"
                    st.rerun()
            else:
                cls = "choice-correct" if option == q["word"] else "choice-incorrect" if option == q["word"] else ""
                st.markdown(f"<div class='game-choice {cls}'>{option}</div>", unsafe_allow_html=True)

        if st.session_state[f"{game_id}_feedback"] is not None:
            if st.session_state[f"{game_id}_feedback"] == "correct":
                st.success("Perfect match!")
            else:
                st.error("Try another one.")
            if st.button("Next image", key=f"{game_id}_next"):
                st.session_state[f"{game_id}_question"] = random.choice(PICTURE_BANK)
                st.session_state[f"{game_id}_feedback"] = None
                st.rerun()

    if st.button("← Back to games", key=f"{game_id}_close"):
        st.session_state.word_games_selected = None
        st.rerun()

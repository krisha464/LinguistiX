import base64
import io
import random
import struct
import time
import wave

import streamlit as st

from utils.speech import text_to_speech
from data.game_banks import (
    WORD_QUEST_BANK,
    STORY_BANK,
    LIGHTNING_BANK,
    DETECTIVE_BANK,
    SCRAMBLE_BANK,
    LISTENING_BANK,
    GRAMMAR_BANK,
    PICTURE_BANK
)

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
        }
]

GAME_THEMES = {game["id"]: game for game in GAME_LIBRARY}


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


def _render_game_header(game_id, main_title, subtitle, description, step, total_steps, stats):
    theme = _theme_for(game_id)
    accent = theme.get('accent', '#10b981')
    progress_pct = int((step / max(total_steps, 1)) * 100)
    return f"""
    <div class='game-header-card'>
        <div class='game-header-row'>
            <div class='game-header-left'>
                <div class='game-icon-box' style='background: {accent}22; color: {accent};'>
                    🎮
                </div>
                <div>
                    <div class='game-title'>{main_title}</div>
                    <div class='game-subtitle' style='color: {accent};'>{subtitle}</div>
                    <div style='font-size: 0.8rem; color: #64748b; margin-top: 2px; font-weight: 500;'>{description}</div>
                </div>
            </div>
            <div class='game-meta'>
                <span class='game-status-pill primary' style='background: {accent}11; border-color: {accent}44; color: {accent};'>
                    📄 Question {step} / {total_steps}
                </span>
                <span class='game-status-pill secondary' style='border-color: {accent}44; color: {accent};'>
                    ⏱️ 25s
                </span>
                <span class='game-status-pill warning'>
                    🏆 {stats['score']}/{stats['total']}
                </span>
            </div>
        </div>
        <div class='game-progress-track' style='background: {accent}22;'>
            <div class='game-progress-fill' style='width:{progress_pct}%; background: {accent};'></div>
        </div>
    </div>
    """


def _render_question_shell(game_id, title, subtitle):
    theme = _theme_for(game_id)
    accent = theme.get('accent', '#10b981')
    return f"""
    <div class='game-question-shell' style='background: {accent}08; border-color: {accent}22;'>
        <div class='game-q-icon' style='background: {accent}22; color: {accent};'>
            {theme['icon']}
        </div>
        <div class='game-wm' style='color: {accent};'>{theme.get('watermark', '📖')}</div>
        <div class='game-q-box'>"{subtitle}"</div>
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
        /* ═══════════════════════════════════════════
           GAME ZONE — Light Card Theme
           ═══════════════════════════════════════════ */

        /* Override the modal background to a clean white */
        [data-testid="stModalBody"], div[role="dialog"] {
            background: #ffffff !important;
        }

        /* ── Card shell (generic) ── */
        .game-shell {
            background: rgba(255,255,255,0.85);
            border: 1px solid rgba(209,213,219,0.5);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.07);
            margin-bottom: 14px;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .game-shell:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        }

        /* ── Game selection card ── */
        .gcard-container {
            position: relative;
            margin-bottom: 12px;
        }
        .gcard-container .stButton {
            position: absolute;
            inset: 0;
            opacity: 0.01;
            z-index: 10;
        }
        .gcard-container .stButton button {
            width: 100%;
            height: 100%;
            padding: 0;
        }
        
        .gcard {
            background: #ffffff;
            border-radius: 18px;
            padding: 0;
            display: flex;
            align-items: stretch;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
            position: relative;
            height: 100%;
        }
        .gcard:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 28px rgba(0,0,0,0.13);
        }
        .gcard-accent-bar {
            width: 5px;
            flex-shrink: 0;
            border-radius: 18px 0 0 18px;
        }
        .gcard-inner {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px 18px;
            flex: 1;
            min-width: 0;
            position: relative;
        }
        /* soft diagonal gradient fill tinted by accent color */
        .gcard-gradient {
            position: absolute;
            inset: 0;
            border-radius: 0 18px 18px 0;
            pointer-events: none;
        }
        .gcard-icon {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
            position: relative;
            z-index: 1;
        }
        .gcard-body {
            flex: 1;
            min-width: 0;
            position: relative;
            z-index: 1;
        }
        .gcard-title {
            font-size: 0.97rem;
            font-weight: 800;
            color: #1e293b;
            line-height: 1.3;
        }
        .gcard-desc {
            font-size: 0.81rem;
            color: #64748b;
            margin-top: 3px;
            line-height: 1.45;
        }
        .gcard-level {
            flex-shrink: 0;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-radius: 999px;
            padding: 4px 11px;
            white-space: nowrap;
            position: relative;
            z-index: 1;
        }

        /* ── Section heading ── */
        .gsection {
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.4px;
            color: #94a3b8;
            margin: 22px 0 8px;
            padding-left: 2px;
        }

        /* ── In-game header ── */
        .game-header-card {
            background: #ffffff;
            border-radius: 20px;
            margin-bottom: 14px;
        }
        .game-header-row {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
            width: 100%;
            margin-bottom: 16px;
        }
        .game-header-left {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .game-icon-box {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        .game-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #0f172a;
        }
        .game-subtitle {
            font-size: 0.88rem;
            font-weight: 600;
            margin-top: 2px;
        }
        .game-meta {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .game-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.88rem;
        }
        .game-status-pill.primary {
            border: 1px solid;
        }
        .game-status-pill.secondary {
            background: #ffffff;
            border: 1px solid;
        }
        .game-status-pill.warning {
            background: #fefce8;
            border: 1px solid #fef08a;
            color: #ca8a04;
        }

        /* ── Progress bar ── */
        .game-progress-track {
            height: 8px;
            border-radius: 999px;
            overflow: hidden;
            width: 100%;
        }
        .game-progress-fill {
            height: 100%;
            border-radius: 999px;
            transition: width 0.4s ease;
        }

        /* ── Question shell ── */
        .game-question-shell {
            border: 1px solid;
            border-radius: 20px;
            padding: 32px 64px;
            margin-bottom: 24px;
            position: relative;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 140px;
        }
        .game-q-box {
            color: #0f172a;
            font-size: 1.25rem;
            font-weight: 800;
            line-height: 1.6;
            max-width: 80%;
            margin: 0 auto;
        }
        .game-wm {
            position: absolute;
            right: 48px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 100px;
            opacity: 0.05;
            pointer-events: none;
        }
        .game-q-icon {
            position: absolute;
            left: 32px;
            top: 50%;
            transform: translateY(-50%);
            width: 56px;
            height: 56px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
        }

        /* ── Choice buttons (answer options) ── */
        .game-choice {
            padding: 16px 20px;
            border-radius: 16px;
            border: 1.5px solid #f1f5f9;
            background: #ffffff;
            color: #475569;
            font-size: 0.92rem;
            display: flex;
            align-items: center;
            gap: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            transition: all 0.2s;
            height: 100%;
        }
        .game-choice:hover {
            border-color: #cbd5e1;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .game-choice-title {
            font-weight: 800;
            color: #0f172a;
            font-size: 1.05rem;
            margin-bottom: 2px;
        }
        .game-choice-icon {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #f0fdf4;
            color: #16a34a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
        }
        .game-choice.choice-correct {
            border-color: #22c55e;
            background: #f0fdf4;
        }
        .game-choice.choice-correct .game-choice-icon {
            background: #22c55e;
            color: #ffffff;
        }
        .game-choice.choice-correct .game-choice-title {
            color: #16a34a;
        }
        .game-choice.choice-incorrect {
            border-color: #fca5a5;
            background: #fef2f2;
        }
        
        .choice-card-container {
            position: relative;
            margin-bottom: 12px;
            height: 84px;
        }
        .choice-card-container .stButton {
            position: absolute;
            inset: 0;
            opacity: 0.01; /* Invisible but clickable */
            z-index: 10;
        }
        .choice-card-container .stButton button {
            width: 100%;
            height: 100%;
            padding: 0;
        }

        /* ── Answer tray and chips ── */
        .game-answer-tray {
            border: 2px dashed #cbd5e1;
            border-radius: 16px;
            padding: 16px;
            min-height: 64px;
            margin-bottom: 16px;
            background: #f8fafc;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }
        .game-answer-tray-label {
            font-size: 0.82rem;
            color: #94a3b8;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .game-word-bank {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 16px;
        }
        .game-chip {
            display: inline-flex;
            align-items: center;
            padding: 10px 18px;
            border-radius: 12px;
            border: 1.5px solid #e2e8f0;
            background: #ffffff;
            color: #334155;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }
        .game-chip:hover {
            border-color: #94a3b8;
        }
        .game-chip.placed {
            background: #f1f5f9;
            border-color: #cbd5e1;
            color: #94a3b8;
        }

        /* ── Action Buttons ── */
        .game-action-btn-wrap .stButton button {
            background: #f0fdf4 !important;
            color: #16a34a !important;
            border: 1px solid #dcfce7 !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            padding: 10px 20px !important;
            transition: all 0.2s !important;
        }
        .game-action-btn-wrap .stButton button:hover {
            border-color: #bbf7d0 !important;
            background: #dcfce7 !important;
        }
        .game-back-btn-wrap .stButton button {
            background: #16a34a !important;
            color: white !important;
            border: none !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            padding: 12px 28px !important;
            box-shadow: 0 4px 14px rgba(22,163,74,0.3) !important;
            transition: all 0.2s !important;
        }
        .game-back-btn-wrap .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(22,163,74,0.4) !important;
            background: #15803d !important;
        }
    </style>

    """, unsafe_allow_html=True)

    if not game_id:
        st.markdown("<p style='font-size:0.85rem; color:#64748b; font-weight:600; margin-bottom:16px;'>Explore our mini-games and start practising.</p>", unsafe_allow_html=True)
        
        if "shuffled_games" not in st.session_state:
            shuffled = list(GAME_LIBRARY)
            random.shuffle(shuffled)
            st.session_state.shuffled_games = shuffled
            
        cols = st.columns(2)
        for i, game in enumerate(st.session_state.shuffled_games):
            theme = _theme_for(game["id"])
            accent = theme["accent"]
            bg_color = theme.get("background", "#F8FAFC")
            
            with cols[i % 2]:
                st.markdown("<div class='gcard-container'>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='gcard'>
                    <div class='gcard-accent-bar' style='background:{accent};'></div>
                    <div class='gcard-inner'>
                        <div class='gcard-gradient' style='background: linear-gradient(135deg, {accent}12 0%, {bg_color}cc 60%, #ffffff 100%);'></div>
                        <div class='gcard-icon' style='background:{accent}18; border:1.5px solid {accent}33;'>
                            {game["icon"]}
                        </div>
                        <div class='gcard-body'>
                            <div class='gcard-title'>{game["label"]}</div>
                            <div class='gcard-desc'>{game["description"]}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"launch_hidden_{game['id']}", key=f"launch_{game['id']}", use_container_width=True):
                    _reset_game_state(game["id"])
                    st.session_state.word_games_selected = game["id"]
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Word Quest", f"Choose the best translation for {q['word']}", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Story Master", "Pick the best word for the sentence", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
        st.markdown(_render_hearts(game_id), unsafe_allow_html=True)
        st.markdown(_render_question_shell(game_id, q["prompt"], "Choose the best word from the list."), unsafe_allow_html=True)

        if st.session_state[f"{game_id}_show_hint"]:
            st.info(f"Hint: the missing word is a {q['hint']}.")

        feedback = st.session_state[f"{game_id}_feedback"]
        
        # 2x2 grid for options using columns
        opt_cols = st.columns(2)
        
        for i, opt_data in enumerate(q["options"]):
            is_dict = isinstance(opt_data, dict)
            option = opt_data["title"] if is_dict else opt_data
            desc = opt_data.get("desc", "") if is_dict else ""
            opt_icon = opt_data.get("icon", "•") if is_dict else "•"
            
            with opt_cols[i % 2]:
                st.markdown("<div class='choice-card-container'>", unsafe_allow_html=True)
                
                # The visual card (underneath)
                cls = ""
                icon = opt_icon
                if feedback is not None:
                    if option == q["answer"]:
                        cls = "choice-correct"
                        icon = "✅"
                    elif option == st.session_state[f"{game_id}_selected_answer"]:
                        cls = "choice-incorrect"
                        icon = "❌"
                        
                st.markdown(f"""
                <div class='game-choice {cls}'>
                    <div class='game-choice-icon'>{icon}</div>
                    <div class='game-choice-text'>
                        <div class='game-choice-title'>{option}</div>
                        <div style='font-size: 0.8rem; color:#64748b;'>{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # The invisible clickable button (on top)
                if feedback is None:
                    if st.button(f"hidden_{option}", key=f"{game_id}_option_{option}", use_container_width=True):
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
                
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        
        # Bottom actions row
        c_left, c_space, c_right = st.columns([2, 1, 1])
        with c_left:
            sub_c1, sub_c2 = st.columns(2)
            with sub_c1:
                st.markdown("<div class='game-action-btn-wrap'>", unsafe_allow_html=True)
                if st.button("💡 Hint", key=f"{game_id}_hint", use_container_width=True):
                    st.session_state[f"{game_id}_show_hint"] = True
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with sub_c2:
                st.markdown("<div class='game-action-btn-wrap'>", unsafe_allow_html=True)
                if st.button("⏩ Skip  -5⭐", key=f"{game_id}_skip", use_container_width=True):
                    st.session_state[f"{game_id}_question"] = random.choice(STORY_BANK)
                    st.session_state[f"{game_id}_show_hint"] = False
                    st.session_state[f"{game_id}_feedback"] = None
                    st.session_state[f"{game_id}_selected_answer"] = None
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        
        with c_right:
            st.markdown("<div class='game-back-btn-wrap'>", unsafe_allow_html=True)
            if feedback is not None:
                if st.button("Next ➔", key=f"{game_id}_next", use_container_width=True):
                    st.session_state[f"{game_id}_question"] = random.choice(STORY_BANK)
                    st.session_state[f"{game_id}_feedback"] = None
                    st.session_state[f"{game_id}_selected_answer"] = None
                    st.session_state[f"{game_id}_show_hint"] = False
                    st.rerun()
            else:
                if st.button("← Back to Games", key=f"{game_id}_back", use_container_width=True):
                    st.session_state.word_games_selected = None
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown(_render_game_header(game_id, "Word Games", "Lightning Blitz", "Answer before the timer hits zero", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Word Detective", "Use the clues to guess the hidden word", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Sentence Scramble", "Rebuild the sentence by tapping the chips", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Listening Ear", "Listen and choose the translation you hear", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Grammar Gauntlet", "Tap the incorrect word, then choose the correction", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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
        st.markdown(_render_game_header(game_id, "Word Games", "Picture Match", "Match the visual to the best word", 1, GAME_LENGTH, stats), unsafe_allow_html=True)
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

    st.markdown("<div class='game-back-btn-wrap'>", unsafe_allow_html=True)
    if st.button("← Back to games", key=f"{game_id}_close", use_container_width=True):
        st.session_state.word_games_selected = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

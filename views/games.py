import streamlit as st
import random
from utils.dictionary import get_random_game_question

@st.dialog("🎮 Word Games", width="large")
def render_word_games():
    if 'word_games_selected' not in st.session_state:
        st.session_state.word_games_selected = None
    if 'explanation_word' not in st.session_state:
        st.session_state.explanation_word = None
        
    game = st.session_state.word_games_selected
    
    # Global Game Stats
    if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
    if 'quiz_total' not in st.session_state: st.session_state.quiz_total = 0
    if 'syn_score' not in st.session_state: st.session_state.syn_score = 0
    if 'syn_total' not in st.session_state: st.session_state.syn_total = 0
    if 'detect_score' not in st.session_state: st.session_state.detect_score = 0
    if 'detect_total' not in st.session_state: st.session_state.detect_total = 0
    if 'context_score' not in st.session_state: st.session_state.context_score = 0
    if 'context_total' not in st.session_state: st.session_state.context_total = 0
    if 'speed_score' not in st.session_state: st.session_state.speed_score = 0
    if 'speed_total' not in st.session_state: st.session_state.speed_total = 0
    if 'game_step' not in st.session_state: st.session_state.game_step = 1
    
    # Safeguard against stale widget keys
    for key in ['syn_ant_choice', 'quiz_choice']:
        if key in st.session_state:
            del st.session_state[key]

    st.markdown("""
    <style>
        .game-shell {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 12px 28px var(--glow);
            margin-bottom: 18px;
        }
        .game-panel-accent {
            background: linear-gradient(135deg, var(--panel), rgba(255,255,255,0.8));
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 10px 24px var(--glow);
        }
        .game-badge {
            background: var(--panel);
            color: var(--accent);
            border: 1px solid var(--border);
            padding: 4px 12px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 12px;
        }
        .game-choice {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 8px;
            border: 1px solid var(--border);
            display: flex;
            align-items: center;
            background: var(--panel);
            color: var(--text-primary);
        }
        .game-choice.choice-correct {
            border-color: var(--accent);
            background: linear-gradient(135deg, var(--panel), rgba(255,255,255,0.82));
            color: var(--accent);
        }
        .game-choice.choice-incorrect {
            border-color: var(--accent-secondary);
            background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9));
            color: var(--text-primary);
        }
        .game-choice.choice-muted {
            opacity: 0.82;
        }
        .stButton > button {
            border-radius: 999px !important;
            border: 1px solid var(--border) !important;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%) !important;
            color: white !important;
            box-shadow: 0 8px 18px var(--glow) !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 10px 22px var(--glow) !important;
        }
        .game-feedback {
            padding: 12px;
            border-radius: 10px;
            font-weight: 600;
            margin-bottom: 16px;
            font-size: 14px;
            border: 1px solid var(--border);
            background: var(--panel);
            color: var(--text-primary);
        }
    </style>
    """, unsafe_allow_html=True)

    if not game:
        st.markdown('<p style="font-size:1.1rem; color:var(--accent); font-weight:700;">Sharpen your language skills with fun games!</p>', unsafe_allow_html=True)
        
        total_played = st.session_state.quiz_total + st.session_state.syn_total + st.session_state.detect_total + st.session_state.context_total + st.session_state.speed_total
        total_correct = st.session_state.quiz_score + st.session_state.syn_score + st.session_state.detect_score + st.session_state.context_score + st.session_state.speed_score
        acc = int((total_correct / total_played) * 100) if total_played > 0 else 0
        
        st.markdown(f"""
        <div class='game-shell'>
            <h5 style='margin-top:0; color:var(--accent); margin-bottom:16px;'><i class='fas fa-chart-line'></i> Your Progress</h5>
            <div style='display:flex; justify-content:space-around; text-align:center;'>
                <div>
                    <h2 style='margin:0; color:var(--text-primary); font-weight:800;'>{total_played}</h2>
                    <small style='color:var(--text-secondary); font-weight:600;'>Words Practiced</small>
                </div>
                <div>
                    <h2 style='margin:0; color:var(--accent-secondary); font-weight:800;'>{acc}%</h2>
                    <small style='color:var(--text-secondary); font-weight:600;'>Accuracy</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        r1c1, r1c2, r1c3 = st.columns(3, gap="small")
        with r1c1:
            def qz(): st.session_state.word_games_selected = 'quiz'
            st.button('📝 Quiz', key='game_quiz_btn', width='stretch', on_click=qz)
        with r1c2:
            def sn(): st.session_state.word_games_selected = 'syn_ant'
            st.button('🔗 Synonyms', key='game_syn_btn', width='stretch', on_click=sn)
        with r1c3:
            def dt(): st.session_state.word_games_selected = 'lang_detect'
            st.button('🌍 Detective', key='game_det_btn', width='stretch', on_click=dt)
        
        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        r2c1, r2c2, r2c3 = st.columns(3, gap="small")
        with r2c1:
            def cm(): st.session_state.word_games_selected = 'context_master'
            st.button('📝 Context Master', key='game_cm_btn', width='stretch', on_click=cm)
        with r2c2:
            def st_game(): st.session_state.word_games_selected = 'speed_trans'
            st.button('⚡ Speed Translator', key='game_speed_btn', width='stretch', on_click=st_game)
        with r2c3:
            st.empty()
                
    elif game == 'quiz':
        if 'quiz_question' not in st.session_state or st.session_state.get('fetching_new'):
            with st.spinner("✨ AI generating challenge..."):
                q = get_random_game_question('quiz')
                if q:
                    st.session_state.quiz_question = q
                    st.session_state.fetching_new = False
                    st.session_state.quiz_feedback = None
                    st.session_state.quiz_choices = q['choices']
                else:
                    st.error("Connection issue. Try again.")
                    st.session_state.word_games_selected = None
                    return
        
        q = st.session_state.quiz_question
        
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
            <h4 style='margin:0; color:var(--text-primary);'>What does <span style='color:var(--accent); font-weight:800;'>{q['word']}</span> mean?</h4>
            <span class='game-badge'>Score: {st.session_state.quiz_score}/{st.session_state.quiz_total}</span>
        </div>
        <p style='color:var(--text-secondary); font-size:13px; font-weight:600; margin-bottom:16px;'>Question {st.session_state.game_step} / 10</p>
        """, unsafe_allow_html=True)
        
        if 'quiz_choices' not in st.session_state:
            st.session_state.quiz_choices = q['choices']
            
        choices = st.session_state.quiz_choices
        is_answered = st.session_state.quiz_feedback is not None
        
        for c in choices:
            if not is_answered:
                def handle_choice(choice_val=c):
                    # Use a local reference to the question to ensure synchronization
                    current_q = st.session_state.quiz_question
                    st.session_state.quiz_selected_answer = choice_val
                    st.session_state.quiz_total += 1
                    
                    # Normalize strings for comparison
                    if choice_val.strip().lower() == current_q['answer'].strip().lower():
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_feedback = "correct"
                    else:
                        st.session_state.quiz_feedback = "incorrect"
                
                st.button(f"⚪ {c}", key=f"quiz_btn_{c}_{st.session_state.game_step}", on_click=handle_choice, use_container_width=True)
            else:
                style_class = "choice-muted"
                icon = "⚫"
                if c.strip().lower() == q['answer'].strip().lower():
                    style_class = "choice-correct"
                    icon = "✅"
                elif c == st.session_state.get('quiz_selected_answer'):
                    style_class = "choice-incorrect"
                    icon = "❌"
                
                st.markdown(f"""
                <div class='game-choice {style_class}'>
                    <span style='margin-right:12px;'>{icon}</span> {c}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        
        if is_answered:
            if st.session_state.quiz_feedback == "correct":
                st.success(f"✨ Correct! '{q['word']}' means: {q['answer']}")
            else:
                st.error(f"❌ Not quite. '{q['word']}' actually means: {q['answer']}")
                
            c1, c2 = st.columns([2, 1])
            with c1:
                def next_quiz():
                    st.session_state.fetching_new = True
                    st.session_state.quiz_feedback = None
                    st.session_state.quiz_selected_answer = None
                    st.session_state.game_step = (st.session_state.game_step % 10) + 1
                st.button("Next Question", key='quiz_next', on_click=next_quiz, type='primary', width='stretch')
            
            with c2:
                def back_quiz():
                    st.session_state.word_games_selected = None
                    st.session_state.quiz_feedback = None
                    st.session_state.quiz_selected_answer = None
                    st.session_state.game_step = 1
                st.button("⬅️ Back", key='quiz_back', on_click=back_quiz, type='secondary', width='stretch')
        else:
            def back_quiz_early():
                st.session_state.word_games_selected = None
                st.session_state.game_step = 1
            st.button("⬅️ Back to Games", key='quiz_back_early', on_click=back_quiz_early, type='secondary')

    elif game == 'syn_ant':
        if 'syn_question' not in st.session_state or st.session_state.get('fetching_new_syn'):
            with st.spinner("💫 Finding connection..."):
                q = get_random_game_question('syn_ant')
                if q:
                    st.session_state.syn_question = q
                    st.session_state.fetching_new_syn = False
                    st.session_state.syn_feedback = None
                    st.session_state.syn_choices = q['choices']
                else:
                    st.error("Connection issue. Try again.")
                    st.session_state.word_games_selected = None
                    return
        
        q = st.session_state.syn_question
        
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
            <h4 style='margin:0; color:var(--text-primary);'>Select the synonym for <span style='color:var(--accent-secondary); font-weight:800;'>{q['word']}</span></h4>
            <span class='game-badge'>Score: {st.session_state.syn_score}/{st.session_state.syn_total}</span>
        </div>
        <p style='color:var(--text-secondary); font-size:13px; font-weight:600; margin-bottom:16px;'>Question {st.session_state.game_step} / 10</p>
        """, unsafe_allow_html=True)
        
        if 'syn_choices' not in st.session_state:
            st.session_state.syn_choices = q['choices']
            
        choices = st.session_state.syn_choices
        is_answered = st.session_state.syn_feedback is not None
        
        for c in choices:
            if not is_answered:
                def handle_syn(choice_val=c):
                    current_q = st.session_state.syn_question
                    st.session_state.syn_selected_answer = choice_val
                    st.session_state.syn_total += 1
                    if choice_val.strip().lower() == current_q['answer'].strip().lower():
                        st.session_state.syn_score += 1
                        st.session_state.syn_feedback = "correct"
                    else:
                        st.session_state.syn_feedback = "incorrect"
                st.button(f"⚪ {c}", key=f"syn_btn_{c}_{st.session_state.game_step}", on_click=handle_syn, use_container_width=True)
            else:
                style_class = "choice-muted"
                icon = "⚫"
                if c.strip().lower() == q['answer'].strip().lower():
                    style_class = "choice-correct"
                    icon = "✅"
                elif c == st.session_state.get('syn_selected_answer'):
                    style_class = "choice-incorrect"
                    icon = "❌"
                
                st.markdown(f"""
                <div class='game-choice {style_class}'>
                    <span style='margin-right:12px;'>{icon}</span> {c}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        
        if is_answered:
            if st.session_state.syn_feedback == "correct":
                st.success(f"✨ Perfect! '{c}' is indeed a synonym for '{q['word']}'.")
            else:
                st.error(f"❌ Incorrect. The correct synonym for '{q['word']}' is '{q['answer']}'.")
                
            c1, c2 = st.columns([2, 1])
            with c1:
                def next_syn():
                    st.session_state.fetching_new_syn = True
                    st.session_state.syn_feedback = None
                    st.session_state.syn_selected_answer = None
                    st.session_state.game_step = (st.session_state.game_step % 10) + 1
                st.button("Next Question", key='syn_next', on_click=next_syn, type='primary', width='stretch')
            
            with c2:
                def back_syn():
                    st.session_state.word_games_selected = None
                    st.session_state.syn_feedback = None
                    st.session_state.syn_selected_answer = None
                    st.session_state.game_step = 1
                st.button("⬅️ Back", key='syn_back', on_click=back_syn, type='secondary', width='stretch')
        else:
            def back_syn_early():
                st.session_state.word_games_selected = None
                st.session_state.game_step = 1
            st.button("⬅️ Back to Games", key='syn_back_early', on_click=back_syn_early, type='secondary')

    elif game == 'lang_detect':
        LANG_CHALLENGES = [
            {"phrase": "Bonjour! Enchanté.", "answer": "French", "options": ["French", "Spanish", "German", "Italian"]},
            {"phrase": "Hola! ¿Cómo estás?", "answer": "Spanish", "options": ["Spanish", "Portuguese", "Italian", "Latin"]},
            {"phrase": "Namaste! Aap kaise hain?", "answer": "Hindi", "options": ["Hindi", "Bengali", "Marathi", "Punjabi"]},
            {"phrase": "Namaskaram! Meeru ela unnaaru?", "answer": "Telugu", "options": ["Telugu", "Tamil", "Kannada", "Malayalam"]},
            {"phrase": "Konnichiwa! Genki desu ka?", "answer": "Japanese", "options": ["Japanese", "Chinese", "Korean", "Thai"]},
            {"phrase": "Guten Tag! Wie geht es dir?", "answer": "German", "options": ["German", "Dutch", "Danish", "Swedish"]},
            {"phrase": "Annyeonghaseyo! Jal jinaess-eoyo?", "answer": "Korean", "options": ["Korean", "Japanese", "Chinese", "Vietnamese"]},
            {"phrase": "Nǐ hǎo! Nǐ hǎo ma?", "answer": "Chinese", "options": ["Chinese", "Korean", "Thai", "Japanese"]},
            {"phrase": "Marhaba! Kayfa halak?", "answer": "Arabic", "options": ["Arabic", "Persian", "Urdu", "Turkish"]},
            {"phrase": "Privyet! Kak dela?", "answer": "Russian", "options": ["Russian", "Ukrainian", "Polish", "Czech"]},
            {"phrase": "Namaskar! Tumhi kase ahat?", "answer": "Marathi", "options": ["Marathi", "Hindi", "Gujarati", "Bengali"]},
            {"phrase": "Kem Cho? Majama?", "answer": "Gujarati", "options": ["Gujarati", "Marathi", "Hindi", "Bengali"]}
        ]

        if 'det_question' not in st.session_state or st.session_state.get('fetching_new_det'):
            q = random.choice(LANG_CHALLENGES)
            st.session_state.det_question = q
            st.session_state.fetching_new_det = False
            st.session_state.det_feedback = None
            opt = q['options'].copy()
            random.shuffle(opt)
            st.session_state.det_choices = opt
        
        q = st.session_state.det_question
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
            <h4 style='margin:0; color:var(--text-primary);'>Identify this language!</h4>
            <span class='game-badge'>Score: {st.session_state.detect_score}/{st.session_state.detect_total}</span>
        </div>
        <div class='game-panel-accent' style='text-align:center; margin-bottom:20px;'>
            <h2 style='margin:0; color:var(--text-primary); letter-spacing:-0.5px;'>"{q['phrase']}"</h2>
        </div>
        """, unsafe_allow_html=True)
        
        choices = st.session_state.det_choices
        is_answered = st.session_state.det_feedback is not None
        
        for c in choices:
            if not is_answered:
                def handle_det(choice=c):
                    st.session_state.det_selected_answer = choice
                    st.session_state.detect_total += 1
                    if choice == q['answer']:
                        st.session_state.detect_score += 1
                        st.session_state.det_feedback = "correct"
                    else:
                        st.session_state.det_feedback = "incorrect"
                st.button(f"🌐 {c}", key=f"det_btn_{c}_{st.session_state.game_step}", on_click=handle_det, width='stretch')
            else:
                style_class = "choice-muted"
                icon = "⚫"
                if c == q['answer']:
                    style_class = "choice-correct"
                    icon = "✅"
                elif c == st.session_state.get('det_selected_answer'):
                    style_class = "choice-incorrect"
                    icon = "❌"
                
                st.markdown(f"""
                <div class='game-choice {style_class}'>
                    <span style='margin-right:12px; font-size:1.2rem;'>{icon}</span> {c}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        if is_answered:
            if st.session_state.det_feedback == "correct":
                st.markdown("<div class='game-feedback' style='background:#F0FDF4; color:#166534; padding:12px; border-radius:10px; font-weight:500; margin-bottom:16px; font-size:14px;'><i class='fas fa-check-circle'></i> Accurate detection! Well done.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='game-feedback' style='background:#FEF2F2; color:#991B1B; padding:12px; border-radius:10px; font-weight:500; margin-bottom:16px; font-size:14px;'><i class='fas fa-info-circle'></i> This is <b>{q['answer']}</b>. Interesting phrase, isn't it?</div>", unsafe_allow_html=True)
                
            c1, c2 = st.columns([2, 1])
            with c1:
                def next_det():
                    st.session_state.fetching_new_det = True
                    st.session_state.det_feedback = None
                    st.session_state.game_step = (st.session_state.game_step % 10) + 1
                st.button("Next Round", key='det_next', on_click=next_det, type='primary', width='stretch')
            with c2:
                def back_det():
                    st.session_state.word_games_selected = None
                    st.session_state.det_feedback = None
                    st.session_state.game_step = 1
                st.button("⬅️ Back", key='det_back', on_click=back_det, type='secondary', width='stretch')
        else:
            def back_det_early():
                st.session_state.word_games_selected = None
            st.button("⬅️ Back to Games", key='det_back_early', on_click=back_det_early, type='secondary')

    elif game == 'context_master':
        CONTEXT_CHALLENGES = [
            {"sentence": "She gave an _______ speech that moved everyone to tears.", "answer": "Eloquent", "options": ["Eloquent", "Meticulous", "Pragmatic", "Zealous"]},
            {"sentence": "He is very _______ about detail; even the smallest error is noticed.", "answer": "Meticulous", "options": ["Meticulous", "Flippant", "Loquacious", "Ephemeral"]},
            {"sentence": "The _______ nature of fashion means trends never last long.", "answer": "Ephemeral", "options": ["Ephemeral", "Dogmatic", "Haughty", "Eloquent"]},
            {"sentence": "Let's be _______ and find a solution that works for everyone.", "answer": "Pragmatic", "options": ["Pragmatic", "Meticulous", "Eloquent", "Capricious"]}
        ]

        if 'cm_question' not in st.session_state or st.session_state.get('fetching_new_cm'):
            q = random.choice(CONTEXT_CHALLENGES)
            st.session_state.cm_question = q
            st.session_state.fetching_new_cm = False
            st.session_state.cm_feedback = None
            st.session_state.cm_choices = q['options']
        
        q = st.session_state.cm_question
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
            <h4 style='margin:0; color:var(--text-primary);'>Fill in the blank!</h4>
            <span class='game-badge'>Score: {st.session_state.context_score}/{st.session_state.context_total}</span>
        </div>
        <div class='game-panel-accent' style='text-align:center; margin-bottom:20px;'>
            <h2 style='margin:0; color:var(--text-primary); letter-spacing:-0.4px; line-height:1.4;'>"{q['sentence']}"</h2>
        </div>
        """, unsafe_allow_html=True)
        
        choices = st.session_state.cm_choices
        is_answered = st.session_state.cm_feedback is not None
        
        for c in choices:
            if not is_answered:
                def handle_cm(choice=c):
                    st.session_state.cm_selected_answer = choice
                    st.session_state.context_total += 1
                    if choice == q['answer']:
                        st.session_state.context_score += 1
                        st.session_state.cm_feedback = "correct"
                    else:
                        st.session_state.cm_feedback = "incorrect"
                st.button(f"✏️ {c}", key=f"cm_btn_{c}_{st.session_state.game_step}", on_click=handle_cm, width='stretch')
            else:
                style_class = "choice-muted"
                icon = "⚫"
                if c == q['answer']:
                    style_class = "choice-correct"
                    icon = "✅"
                elif c == st.session_state.get('cm_selected_answer'):
                    style_class = "choice-incorrect"
                    icon = "❌"
                
                st.markdown(f"""
                <div class='game-choice {style_class}'>
                    <span style='margin-right:12px; font-size:1.2rem;'>{icon}</span> {c}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        if is_answered:
            if st.session_state.cm_feedback == "correct":
                st.markdown("<div class='game-feedback' style='background:#F0FDF4; color:#166534; padding:12px; border-radius:10px; font-weight:500; margin-bottom:16px; font-size:14px;'><i class='fas fa-check-circle'></i> Accurate! Context understood.</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='game-feedback' style='background:#FEF2F2; color:#991B1B; padding:12px; border-radius:10px; font-weight:500; margin-bottom:16px; font-size:14px;'><i class='fas fa-info-circle'></i> The correct word is <b>{q['answer']}</b>. It fits the situation best.</div>", unsafe_allow_html=True)
                
            c1, c2 = st.columns([2, 1])
            with c1:
                def next_cm():
                    st.session_state.fetching_new_cm = True
                    st.session_state.cm_feedback = None
                    st.session_state.game_step = (st.session_state.game_step % 10) + 1
                st.button("Next Round", key='cm_next', on_click=next_cm, type='primary', width='stretch')
            with c2:
                def back_cm():
                    st.session_state.word_games_selected = None
                st.button("⬅️ Back", key='cm_back', on_click=back_cm, type='secondary', width='stretch')
        else:
            def back_cm_early():
                st.session_state.word_games_selected = None
            st.button("⬅️ Back to Games", key='cm_back_early', on_click=back_cm_early, type='secondary')

    elif game == 'speed_trans':
        SPEED_CHALLENGES = [
            {"word": "Good Morning", "target": "French", "answer": "Bonjour", "options": ["Bonjour", "Hola", "Ciao", "Allo"]},
            {"word": "Thank You", "target": "Hindi", "answer": "Dhanyavad", "options": ["Dhanyavad", "Shukriya", "Namaste", "Theek hai"]},
            {"word": "Beer", "target": "German", "answer": "Bier", "options": ["Bier", "Wein", "Wasser", "Milch"]},
            {"word": "Friend", "target": "Spanish", "answer": "Amigo", "options": ["Amigo", "Compañero", "Hermano", "Padre"]},
            {"word": "God", "target": "Arabic", "answer": "Allah", "options": ["Allah", "Rabb", "Khuda", "Deen"]},
            {"word": "Water", "target": "Telugu", "answer": "Neeru", "options": ["Neeru", "Annam", "Gaddi", "Illu"]}
        ]

        if 'speed_question' not in st.session_state or st.session_state.get('fetching_new_speed'):
            q = random.choice(SPEED_CHALLENGES)
            st.session_state.speed_question = q
            st.session_state.fetching_new_speed = False
            st.session_state.speed_feedback = None
            st.session_state.speed_choices = q['options']
        
        q = st.session_state.speed_question
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
            <h4 style='margin:0; color:var(--text-primary);'>Translate it!</h4>
            <span class='game-badge'>Score: {st.session_state.speed_score}/{st.session_state.speed_total}</span>
        </div>
        <div class='game-panel-accent' style='text-align:center; margin-bottom:20px;'>
            <p style='color:var(--text-secondary); font-weight:700; margin-bottom:8px;'>HOW DO YOU SAY "{q['word'].upper()}" IN {q['target'].upper()}?</p>
            <h1 style='margin:0; color:var(--accent);'>???</h1>
        </div>
        """, unsafe_allow_html=True)
        
        choices = st.session_state.speed_choices
        is_answered = st.session_state.speed_feedback is not None
        
        for c in choices:
            if not is_answered:
                def handle_speed(choice=c):
                    st.session_state.speed_selected_answer = choice
                    st.session_state.speed_total += 1
                    if choice == q['answer']:
                        st.session_state.speed_score += 1
                        st.session_state.speed_feedback = "correct"
                    else:
                        st.session_state.speed_feedback = "incorrect"
                st.button(f"⚡ {c}", key=f"speed_btn_{c}_{st.session_state.game_step}", on_click=handle_speed, width='stretch')
            else:
                style_class = "choice-muted"
                icon = "⚫"
                if c == q['answer']:
                    style_class = "choice-correct"
                    icon = "✅"
                elif c == st.session_state.get('speed_selected_answer'):
                    style_class = "choice-incorrect"
                    icon = "❌"
                
                st.markdown(f"""
                <div class='game-choice {style_class}'>
                    <span style='margin-right:12px; font-size:1.2rem;'>{icon}</span> {c}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        if is_answered:
            if st.session_state.speed_feedback == "correct":
                st.markdown("<div class='game-feedback' style='background:#F0FDF4; color:#166534; padding:12px; border-radius:10px; font-weight:500; margin-bottom:16px; font-size:14px;'><i class='fas fa-check-circle'></i> Speedy and Accurate!</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='game-feedback' style='background:#FEF2F2; color:#991B1B; padding:12px; border-radius:10px; font-weight:500; margin-bottom:16px; font-size:14px;'><i class='fas fa-info-circle'></i> Correct: <b>{q['answer']}</b>. Practice makes perfect!</div>", unsafe_allow_html=True)
                
            c1, c2 = st.columns([2, 1])
            with c1:
                def next_speed():
                    st.session_state.fetching_new_speed = True
                    st.session_state.speed_feedback = None
                    st.session_state.game_step = (st.session_state.game_step % 10) + 1
                st.button("Next Round", key='speed_next', on_click=next_speed, type='primary', width='stretch')
            with c2:
                def back_speed():
                    st.session_state.word_games_selected = None
                st.button("⬅️ Back", key='speed_back', on_click=back_speed, type='secondary', width='stretch')
        else:
            def back_speed_early():
                st.session_state.word_games_selected = None
            st.button("⬅️ Back to Games", key='speed_back_early', on_click=back_speed_early, type='secondary')

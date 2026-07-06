import streamlit as st
import datetime
import json
import streamlit.components.v1 as components
from utils.translator import detect_and_translate, SUPPORTED_LANGS
from utils.speech import text_to_speech
from utils.storage import save_data
from utils.session import swap_languages
from utils.nlp_advanced import check_grammar, correct_spelling

def render_translator(target_options, create_pdf):
    # Language Selection Row (Simplified, Swap removed)
    sel_col1, sel_col2, sel_col3, sel_col4 = st.columns([2, 2, 0.8, 1], gap="medium")
    with sel_col1:
        st.markdown("<p style='font-size:11px; font-weight:800; color:#94A3B8; margin-bottom:8px;'>FROM</p>", unsafe_allow_html=True)
        st.session_state.src_lang = st.selectbox("Source Language", options=list(SUPPORTED_LANGS.keys()), format_func=lambda x: SUPPORTED_LANGS[x], key="src_lang_dash", index=list(SUPPORTED_LANGS.keys()).index(st.session_state.src_lang), label_visibility="collapsed")
    with sel_col2:
        st.markdown("<p style='font-size:11px; font-weight:800; color:#94A3B8; margin-bottom:8px;'>TO</p>", unsafe_allow_html=True)
        st.session_state.tgt_lang = st.selectbox("Target Language", options=target_options, format_func=lambda x: SUPPORTED_LANGS[x], key="tgt_lang_dash", index=target_options.index(st.session_state.tgt_lang) if st.session_state.tgt_lang in target_options else 0, label_visibility="collapsed")
    with sel_col3:
        st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear", key="master_clear_btn", use_container_width=True):
            st.session_state.input_text = ""
            st.session_state.translation_result = ""
            if "input_dash" in st.session_state:
                del st.session_state["input_dash"]
            st.rerun()
    with sel_col4:
        st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
        st_clicked = st.button("🚀 Translate", key="main_tr_dash", type="primary", use_container_width=True)

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    # 2. Dual Box Layout (Side-by-Side)
    st.markdown("""
    <style>
        .stTextArea textarea {
            background: white !important;
            color: #1E293B !important;
            border: 2px solid var(--border) !important;
            border-radius: 16px !important;
            font-size: 16px !important;
        }
        .stTextArea textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--glow) !important;
        }
        /* Specifically target output box */
        textarea[aria-label="Output text"] {
            color: var(--accent) !important;
            -webkit-text-fill-color: var(--accent) !important;
            font-weight: 800 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    main_col1, main_col2 = st.columns([1, 1], gap="large")
    
    with main_col1:
        st.markdown(f"""
        <div style='background:white; border-radius:16px; border:2px solid var(--border); padding:15px; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.02);'>
            <span style='font-size:16px; font-weight:900; color:var(--text-primary); letter-spacing:1px; text-transform:uppercase;'>✏️ Input</span>
        </div>
        """, unsafe_allow_html=True)
        
        def update_input():
            st.session_state.input_text = st.session_state.input_dash

        input_text = st.text_area(
            "Input text",
            value=st.session_state.input_text,
            placeholder="Type or speak here...",
            key="input_dash",
            height=200,
            label_visibility="collapsed",
            on_change=update_input
        )
        
        st.markdown(f"<div style='text-align:right; margin-top:4px;'><span style='font-size:10px; color:#94A3B8;'>{len(input_text)} characters</span></div>", unsafe_allow_html=True)

        # Advanced NLP Features - Grammar & Spelling Check
        if input_text.strip():
            with st.expander("🔍 Grammar & Spelling Check"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Check Grammar", key="grammar_check", use_container_width=True):
                        grammar_result = check_grammar(input_text)
                        if grammar_result["error_count"] == 0:
                            st.success("✓ No grammar errors found!")
                        else:
                            st.warning(f"⚠️ Found {grammar_result['error_count']} grammar issue(s)")
                            for error in grammar_result["suggestions"][:3]:  # Show top 3
                                st.info(f"**{error['original']}** → **{error['suggestion']}**")
                
                with col2:
                    if st.button("✏️ Fix Spelling", key="spelling_check", use_container_width=True):
                        spelling_result = correct_spelling(input_text)
                        if spelling_result.get("is_corrected", False):
                            st.write("**Corrected Text:**")
                            st.text_area("", value=spelling_result.get("corrected", input_text), height=100, disabled=True)
                        else:
                            st.success("✓ No spelling errors found!")


        if st.button("📋 Copy Input", key="in_copy", use_container_width=True):
            if input_text.strip():
                st.toast("Copied input!")
                safe_js_val = json.dumps(input_text.strip())
                js = f"<script>navigator.clipboard.writeText({safe_js_val});</script>"
                components.html(js, height=0)

    with main_col2:
        st.markdown(f"""
        <div style='background:white; border-radius:16px; border:2px solid var(--border); padding:15px; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.02);'>
            <span style='font-size:16px; font-weight:900; color:var(--accent); letter-spacing:1px; text-transform:uppercase;'>🌐 Translation</span>
        </div>
        """, unsafe_allow_html=True)
        
        output_val = st.session_state.translation_result if st.session_state.translation_result else ""
        
        st.text_area(
            "Output text",
            value=output_val,
            height=200,
            disabled=True,
            label_visibility="collapsed",
            placeholder="Translation will appear here..."
        )
        
        st.markdown(f"<div style='text-align:right; margin-top:4px;'><span style='font-size:10px; color:#94A3B8;'>{len(output_val)} characters</span></div>", unsafe_allow_html=True)

        r_act_cols = st.columns([1, 1, 1])
        with r_act_cols[0]:
            if st.button("🔊 Listen", key="out_listen", use_container_width=True):
                if st.session_state.translation_result:
                    audio = text_to_speech(st.session_state.translation_result, st.session_state.tgt_lang)
                    if audio:
                        st.session_state.audio_to_play = audio
                        st.rerun()
        with r_act_cols[1]:
            if st.button("📋 Copy Result", key="out_copy", use_container_width=True):
                if st.session_state.translation_result:
                    st.toast("Copied translation!")
                    safe_js_val = json.dumps(st.session_state.translation_result.strip())
                    js = f"<script>navigator.clipboard.writeText({safe_js_val});</script>"
                    components.html(js, height=0)
        with r_act_cols[2]:
            if st.button("🔖 Save", key="out_bookmark", use_container_width=True):
                if st.session_state.translation_result:
                    st.session_state.phrasebook.append({
                        "input": st.session_state.input_text,
                        "output": st.session_state.translation_result,
                        "lang": st.session_state.tgt_lang,
                        "date": datetime.datetime.now().isoformat()
                    })
                    save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                    st.toast("Saved!")

    # Audio Output Player
    if 'audio_to_play' in st.session_state and st.session_state.audio_to_play:
        try:
            st.audio(st.session_state.audio_to_play, autoplay=True)
        except TypeError:
            st.audio(st.session_state.audio_to_play)
        st.session_state.audio_to_play = None

    if st_clicked:
        if input_text.strip():
            with st.spinner("Translating..."):
                translation, detected_lang = detect_and_translate(input_text, st.session_state.tgt_lang, st.session_state.src_lang)
                st.session_state.translation_result = translation
                st.session_state.translated_detected = detected_lang
                if st.session_state.authenticated:
                    st.session_state.history.append({
                        "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                        "src": SUPPORTED_LANGS.get(detected_lang if st.session_state.src_lang == "auto" else st.session_state.src_lang),
                        "tgt": SUPPORTED_LANGS[st.session_state.tgt_lang],
                        "input": input_text,
                        "output": translation
                    })
                    save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                st.rerun()

    # Translation History Section
    if st.session_state.authenticated:
        st.markdown("<div style='margin-top:48px;'></div>", unsafe_allow_html=True)
        h_row = st.columns([1, 1])
        with h_row[0]:
            st.markdown("### 🕒 Translation History")
        with h_row[1]:
            if st.button("Clear all", key="clear_all_dash"):
                st.session_state.history = []
                save_data([], st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                st.rerun()
        
        if st.session_state.history:
            for idx, entry in enumerate(reversed(st.session_state.history[-10:])):
                with st.container():
                    st.markdown(f"""
                    <div style='background:var(--panel); border:1px solid var(--border); border-radius:20px; padding:24px; margin-bottom:16px; box-shadow:0 4px 15px rgba(0,0,0,0.02);'>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;'>
                            <div style='display:flex; align-items:center; gap:12px;'>
                                <span style='font-size:11px; color:var(--text-secondary); opacity:0.6; font-weight:700;'>{entry['Time']}</span>
                                <span style='background:var(--accent)15; color:var(--accent); padding:4px 10px; border-radius:8px; font-size:10px; font-weight:800;'>{entry['src'].upper()}</span>
                                <span style='color:var(--text-secondary); opacity:0.5;'>→</span>
                                <span style='background:var(--accent-secondary)15; color:var(--accent-secondary); padding:4px 10px; border-radius:8px; font-size:10px; font-weight:800;'>{entry['tgt'].upper()}</span>
                            </div>
                        </div>
                        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:30px;'>
                            <div>
                                <p style='font-size:9px; font-weight:800; color:var(--text-secondary); opacity:0.6; margin-bottom:6px; text-transform:uppercase;'>Original Text</p>
                                <p style='font-size:13px; color:var(--text-primary); font-weight:600; overflow-wrap: break-word;'>{entry['input'][:300]}</p>
                            </div>
                            <div>
                                <p style='font-size:9px; font-weight:800; color:var(--text-secondary); opacity:0.6; margin-bottom:6px; text-transform:uppercase;'>Translation Result</p>
                                <p style='font-size:13px; color:var(--accent); font-weight:700; overflow-wrap: break-word;'>{entry['output'][:300]}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"⚡ Restore this Session", key=f"hist_rest_{idx}", use_container_width=True):
                        st.session_state.input_text = entry['input']
                        st.session_state.translation_result = entry['output']
                        st.rerun()
        else:
            st.caption("No recent translations to show.")
    else:
        st.markdown("---")
        st.info("🕒 Sign in to view and persist your translation history.")

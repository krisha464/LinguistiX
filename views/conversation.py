import streamlit as st
from utils.translator import detect_and_translate, SUPPORTED_LANGS
from utils.speech import text_to_speech
from utils.nlp_advanced import analyze_sentiment, detect_intent
from streamlit_mic_recorder import speech_to_text

def get_sentiment_color(sentiment):
    """Return color based on sentiment."""
    if sentiment == "POSITIVE":
        return "#10B981"  # Green
    elif sentiment == "NEGATIVE":
        return "#EF4444"  # Red
    else:
        return "#F59E0B"  # Yellow

def get_intent_icon(intent):
    """Return emoji icon for intent."""
    intent_icons = {
        "greeting": "👋",
        "farewell": "👋",
        "question": "❓",
        "gratitude": "🙏",
        "apology": "😔",
        "affirmation": "✅",
        "negation": "❌",
        "request": "🙏",
        "statement": "💬",
        "emotion": "😊"
    }
    return intent_icons.get(intent, "💭")

def render_conversation(target_options):
    st.markdown("""
        <div style='text-align:center; margin-bottom:30px;'>
            <h3 style='margin:0; font-weight:800; color:var(--accent);'><i class='fas fa-comments'></i> Live Duo Translate</h3>
            <p style='opacity:0.6; font-size:13px;'>Real-time bilingual dialogue powered by AI</p>
        </div>
    """, unsafe_allow_html=True)

    # --- TOP CONTROL PANEL ---
    with st.container():
        st.markdown("<div style='background:var(--panel); border:1.5px solid var(--border); border-radius:24px; padding:20px; box-shadow:0 10px 30px rgba(0,0,0,0.03); margin-bottom:24px;'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 0.5, 2])
        
        with c1:
            st.session_state.conv_lang_a = st.selectbox("Person A", options=target_options, format_func=lambda x: SUPPORTED_LANGS[x], key="conv_a_sel", index=target_options.index(st.session_state.conv_lang_a) if st.session_state.conv_lang_a in target_options else 0)
        with c2:
            st.markdown("<h3 style='text-align:center; padding-top:28px; color:var(--accent);'>⇆</h3>", unsafe_allow_html=True)
        with c3:
            st.session_state.conv_lang_b = st.selectbox("Person B", options=target_options, format_func=lambda x: SUPPORTED_LANGS[x], key="conv_b_sel", index=target_options.index(st.session_state.conv_lang_b) if st.session_state.conv_lang_b in target_options else 1)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- CHAT HISTORY ---
    st.markdown('<div class="conv-container" style="background:rgba(255,255,255,0.05); border-radius:30px; padding:20px; margin-bottom:20px; border:1px solid var(--border); min-height:300px;">', unsafe_allow_html=True)
    if not st.session_state.conv_history:
        st.markdown("<div style='text-align:center; padding: 60px; opacity:0.3;'><i class='fas fa-microphone-lines' style='font-size:40px; margin-bottom:15px; display:block;'></i><p style='font-weight:600;'>Tap a microphone below to start talking</p></div>", unsafe_allow_html=True)
    
    for msg in st.session_state.conv_history:
        side = "left" if msg['role'] == "A" else "right"
        justify = "flex-start" if side == "left" else "flex-end"
        
        # Analyze sentiment and intent
        sentiment = analyze_sentiment(msg['text'])
        intent = detect_intent(msg['text'])
        sentiment_color = get_sentiment_color(sentiment['sentiment'])
        intent_icon = get_intent_icon(intent['primary_intent'])
        
        st.markdown(f"""
        <div style='display:flex; justify-content:{justify}; margin-bottom:24px;'>
            <div class='bubble bubble-{side}' style='max-width:80%;'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; opacity:0.7;'>
                    <div style='display:flex; gap:8px; align-items:center;'>
                        <span style='font-size:9px; font-weight:900; letter-spacing:1px;'>{SUPPORTED_LANGS[msg['lang']].upper()}</span>
                        <span style='font-size:9px; font-weight:900;'>PERSON {msg['role']}</span>
                    </div>
                    <div style='display:flex; gap:6px; align-items:center;'>
                        <span style='background:{sentiment_color}; color:white; padding:2px 8px; border-radius:12px; font-size:9px; font-weight:700;'>{sentiment["sentiment"]}</span>
                        <span style='font-size:14px;' title='{intent["primary_intent"]}'>{intent_icon}</span>
                    </div>
                </div>
                <p style='margin:0; font-size:15px; font-weight:500; line-height:1.4;'>{msg['text']}</p>
                <div class='bubble-trans' style='margin-top:12px; padding-top:12px;'>
                    <p style='margin:0; font-size:16px; font-weight:800;'>{msg['translated']}</p>
                </div>
                <div style='margin-top:8px; opacity:0.6; font-size:11px;'>
                    📊 Confidence: {sentiment["score"]:.0%} | Intent: {intent["primary_intent"].title()} ({intent["confidence"]:.0%})
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTOM ACTION PANEL ---
    mic_col1, mic_col2 = st.columns(2, gap="medium")
    
    with mic_col1:
        st.markdown(f"<div style='background:var(--panel); border-radius:20px; padding:15px; border:1px solid var(--border); text-align:center;'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight:800; font-size:12px; color:var(--accent); margin-bottom:10px;'>SPEAKER A ({SUPPORTED_LANGS[st.session_state.conv_lang_a]})</p>", unsafe_allow_html=True)
        voice_a = speech_to_text(language=st.session_state.conv_lang_a, use_container_width=True, just_once=True, key='mic_conv_a_btn')
        if voice_a:
            with st.spinner("A is speaking..."):
                translated_a, _ = detect_and_translate(voice_a, st.session_state.conv_lang_b, st.session_state.conv_lang_a)
                st.session_state.conv_history.append({"role": "A", "lang": st.session_state.conv_lang_a, "text": voice_a, "translated": translated_a})
                audio = text_to_speech(translated_a, st.session_state.conv_lang_b)
                if audio: st.session_state.conv_audio = audio
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with mic_col2:
        st.markdown(f"<div style='background:var(--panel); border-radius:20px; padding:15px; border:1px solid var(--border); text-align:center;'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight:800; font-size:12px; color:var(--accent-secondary); margin-bottom:10px;'>SPEAKER B ({SUPPORTED_LANGS[st.session_state.conv_lang_b]})</p>", unsafe_allow_html=True)
        voice_b = speech_to_text(language=st.session_state.conv_lang_b, use_container_width=True, just_once=True, key='mic_conv_b_btn')
        if voice_b:
            with st.spinner("B is speaking..."):
                translated_b, _ = detect_and_translate(voice_b, st.session_state.conv_lang_a, st.session_state.conv_lang_b)
                st.session_state.conv_history.append({"role": "B", "lang": st.session_state.conv_lang_b, "text": voice_b, "translated": translated_b})
                audio = text_to_speech(translated_b, st.session_state.conv_lang_a)
                if audio: st.session_state.conv_audio = audio
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.conv_history:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Conversation", use_container_width=True, key='conv_reset_btn', type="secondary"):
            st.session_state.conv_history = []
            st.rerun()

    # Audio Output
    if 'conv_audio' in st.session_state and st.session_state.conv_audio:
        try:
            st.audio(st.session_state.conv_audio, autoplay=True)
        except TypeError:
            st.audio(st.session_state.conv_audio)
        del st.session_state.conv_audio

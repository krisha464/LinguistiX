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
    st.markdown("<div class='translator-page'>", unsafe_allow_html=True)
    st.markdown("""
    <style>
      .translator-page {
        width: 100% !important;
        padding: 0 !important;
      }
      .home-hero-card {
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 32px !important;
        padding: 30px !important;
        margin-bottom: 28px !important;
        box-shadow: 0 30px 60px rgba(15,23,42,0.08) !important;
        backdrop-filter: blur(18px) !important;
      }
      .hero-eyebrow {
        color: #2563EB !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 1.4px !important;
        text-transform: uppercase !important;
        margin-bottom: 16px !important;
      }
      .hero-heading {
        font-size: 42px !important;
        font-weight: 900 !important;
        line-height: 1.05 !important;
        color: #0F172A !important;
        margin: 0 0 18px 0 !important;
      }
      .hero-text {
        font-size: 16px !important;
        color: #475569 !important;
        line-height: 1.72 !important;
        margin: 0 !important;
      }
      .hero-pill-wrap {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 12px !important;
        margin-top: 24px !important;
      }
      .hero-pill {
        background: rgba(37,99,235,0.08) !important;
        color: #2563EB !important;
        border-radius: 999px !important;
        padding: 10px 16px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
      }
      .translator-card {
        background: rgba(255,255,255,0.98) !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 32px !important;
        padding: 28px !important;
        box-shadow: 0 35px 90px rgba(15,23,42,0.08) !important;
        margin-bottom: 32px !important;
      }
      .workspace-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: flex-start !important;
        gap: 20px !important;
        margin-bottom: 24px !important;
      }
      .workspace-label {
        color: #2563EB !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 1.4px !important;
        text-transform: uppercase !important;
        margin-bottom: 10px !important;
      }
      .workspace-title {
        font-size: 26px !important;
        font-weight: 900 !important;
        margin: 0 !important;
        color: #0F172A !important;
      }
      .workspace-note {
        color: #64748B !important;
        font-size: 14px !important;
        line-height: 1.75 !important;
        margin-top: 10px !important;
      }
      .translator-topbar {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 16px !important;
        align-items: flex-end !important;
        margin-bottom: 24px !important;
      }
      .translator-topbar .lang-group {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 14px !important;
        flex: 1 1 540px !important;
      }
      .translator-topbar .lang-group > div {
        min-width: 220px !important;
        width: 100% !important;
      }
      .translator-topbar .action-group {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 14px !important;
      }
      .translate-button .stButton > button {
        background: linear-gradient(135deg, #2563EB, #60A5FA) !important;
        color: #FFFFFF !important;
        border-radius: 18px !important;
        min-height: 54px !important;
        box-shadow: 0 18px 30px rgba(37,99,235,0.18) !important;
      }
      .translator-panel {
        display: flex !important;
        gap: 24px !important;
        flex-wrap: wrap !important;
      }
      .translator-column {
        background: #F8FBFF !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 28px !important;
        padding: 24px !important;
        box-shadow: 0 20px 40px rgba(15,23,42,0.06) !important;
      }
      .translator-column.wide {
        flex: 1 1 72% !important;
        min-width: 420px !important;
      }
      .translator-column.narrow {
        flex: 1 1 28% !important;
        min-width: 300px !important;
      }
      .field-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 24px !important;
        padding: 22px !important;
        box-shadow: 0 18px 36px rgba(15,23,42,0.05) !important;
      }
      .field-card .card-label {
        font-size: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 1.4px !important;
        color: #64748B !important;
        margin-bottom: 10px !important;
      }
      .field-card .card-title {
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin-bottom: 8px !important;
      }
      .field-card .card-copy {
        font-size: 13px !important;
        color: #475569 !important;
        line-height: 1.7 !important;
      }
      .translated-status {
        color: #64748B !important;
        font-size: 12px !important;
        margin-bottom: 10px !important;
      }
      .action-grid {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 12px !important;
        margin-top: 20px !important;
      }
      .action-grid .stButton > button {
        min-height: 48px !important;
      }
      .grammar-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 24px !important;
        padding: 22px !important;
        margin-top: 24px !important;
        box-shadow: 0 18px 36px rgba(15,23,42,0.05) !important;
      }
      .grammar-card .panel-title {
        font-size: 16px !important;
      }
      .grammar-card .panel-subtitle {
        margin-top: 6px !important;
      }
      .sidebar-card {
        background: #FFFFFF !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 24px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 18px 36px rgba(15,23,42,0.05) !important;
      }
      .sidebar-card .title {
        font-size: 18px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        margin-bottom: 10px !important;
      }
      .sidebar-card .description {
        font-size: 14px !important;
        color: #475569 !important;
        line-height: 1.75 !important;
        margin-bottom: 18px !important;
      }
      .sidebar-cta {
        background: linear-gradient(180deg, #2563EB 0%, #60A5FA 100%) !important;
        color: #FFFFFF !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 24px 60px rgba(37,99,235,0.18) !important;
      }
      .sidebar-cta .title {
        color: #FFFFFF !important;
      }
      .sidebar-cta .description {
        color: rgba(255,255,255,0.85) !important;
      }
      .sidebar-cta .feature-pill {
        background: rgba(255,255,255,0.18) !important;
        color: #FFFFFF !important;
      }
      .history-section {
        margin-top: 16px !important;
      }
      .section-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: flex-end !important;
        gap: 12px !important;
        margin-bottom: 18px !important;
      }
      .section-title {
        font-size: 22px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        margin: 0 !important;
      }
      .history-table {
        background: #FFFFFF !important;
        border: 1px solid rgba(226,232,240,0.95) !important;
        border-radius: 24px !important;
        overflow: hidden !important;
        box-shadow: 0 18px 36px rgba(15,23,42,0.06) !important;
      }
      .history-row {
        display: grid !important;
        grid-template-columns: 100px 100px minmax(260px, 1fr) 100px 120px !important;
        gap: 18px !important;
        align-items: center !important;
        padding: 18px 24px !important;
        border-bottom: 1px solid rgba(226,232,240,0.95) !important;
      }
      .history-row.header {
        background: #F8FBFF !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
      }
      .history-row:last-child {
        border-bottom: none !important;
      }
      .restore-btn {
        background: rgba(37,99,235,0.08) !important;
        color: #2563EB !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 10px 16px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
      }
      .history-empty {
        padding: 24px 0 !important;
        color: #64748B !important;
        font-size: 14px !important;
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
      <div class='home-hero-card'>
        <div class='hero-eyebrow'>Translator Workspace</div>
        <h1 class='hero-heading'>A polished translator homepage with a SaaS dashboard feel.</h1>
        <p class='hero-text'>Soft UI, clear hierarchy, and card-based feature grouping for fast translations, phrasebook previews, and compact history.</p>
        <div class='hero-pill-wrap'>
          <div class='hero-pill'>Modern dashboard layout</div>
          <div class='hero-pill'>Two-column workspace</div>
          <div class='hero-pill'>Sidebar CTA & preview</div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='translator-panel'>", unsafe_allow_html=True)
    main_col, side_col = st.columns([3, 1], gap="large")

    with main_col:
        st.markdown("<div class='translator-column wide'>", unsafe_allow_html=True)
        st.markdown("""
          <div class='workspace-header'>
            <div>
              <div class='workspace-label'>Language Selection</div>
              <div class='workspace-title'>Translate text with precision</div>
              <div class='workspace-note'>Select source and target languages, then translate in a polished side-by-side workspace.</div>
            </div>
          </div>
        """, unsafe_allow_html=True)

        top_cols = st.columns([2, 2, 0.8, 1], gap="medium")
        with top_cols[0]:
            st.markdown("<div class='card-label'>Source language</div>", unsafe_allow_html=True)
            st.session_state.src_lang = st.selectbox(
                "Source Language",
                options=list(SUPPORTED_LANGS.keys()),
                format_func=lambda x: SUPPORTED_LANGS[x],
                key="src_lang_dash",
                index=list(SUPPORTED_LANGS.keys()).index(st.session_state.src_lang),
                label_visibility="collapsed"
            )
        with top_cols[1]:
            st.markdown("<div class='card-label'>Target language</div>", unsafe_allow_html=True)
            st.session_state.tgt_lang = st.selectbox(
                "Target Language",
                options=target_options,
                format_func=lambda x: SUPPORTED_LANGS[x],
                key="tgt_lang_dash",
                index=target_options.index(st.session_state.tgt_lang) if st.session_state.tgt_lang in target_options else 0,
                label_visibility="collapsed"
            )
        with top_cols[2]:
            st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
            if st.button("⇄", key="swap_lang_btn", help="Swap source and target languages", use_container_width=True):
                swap_languages()
                st.rerun()
        with top_cols[3]:
            st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
            st_clicked = st.button("Translate", key="main_tr_dash", type="primary", use_container_width=True)

        st.markdown("<div class='translator-panel' style='margin-top:22px;'>", unsafe_allow_html=True)
        input_col, output_col = st.columns([1, 1], gap="large")

        with input_col:
            st.markdown("""
              <div class='field-card'>
                <div class='card-label'>Input</div>
                <div class='card-title'>Enter text to translate</div>
                <div class='card-copy'>Type or paste source text and keep the workspace visible.</div>
              </div>
            """, unsafe_allow_html=True)
            input_text = st.text_area(
                "Source text",
                value=st.session_state.input_text,
                placeholder="Good morning! Type your sentence here...",
                key="input_dash",
                height=320,
                label_visibility="collapsed"
            )
            st.markdown(f"<div style='text-align:right; margin-top:12px; font-size:12px; color:#64748B;'>Characters: {len(input_text)} / 5000</div>", unsafe_allow_html=True)
            if st.button("📋 Copy Input", key="copy_input_btn", use_container_width=True):
                if input_text.strip():
                    components.html(f"<script>navigator.clipboard.writeText({json.dumps(input_text.strip())});</script>", height=0)
                    st.toast("Copied input!")

        with output_col:
            st.markdown("""
              <div class='field-card'>
                <div class='card-label'>Output</div>
                <div class='card-title'>Translated result</div>
                <div class='card-copy'>Review translated text with the target language shown below.</div>
              </div>
            """, unsafe_allow_html=True)
            output_val = st.session_state.translation_result or ""
            target_label = SUPPORTED_LANGS.get(st.session_state.tgt_lang, "Target")
            st.markdown(f"<div class='translated-status'>Output language: <strong>{target_label}</strong></div>", unsafe_allow_html=True)
            st.text_area(
                "Translated text",
                value=output_val,
                height=320,
                disabled=True,
                label_visibility="collapsed",
                placeholder="Translation will appear here..."
            )
            st.markdown(f"<div style='text-align:right; margin-top:12px; font-size:12px; color:#64748B;'>Characters: {len(output_val)} / 5000</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='action-grid'>", unsafe_allow_html=True)
        action_cols = st.columns([1, 1, 1, 1], gap="small")
        with action_cols[0]:
            if st.button("📋 Copy Output", key="copy_output_btn", use_container_width=True):
                if output_val.strip():
                    components.html(f"<script>navigator.clipboard.writeText({json.dumps(output_val.strip())});</script>", height=0)
                    st.toast("Copied translation!")
        with action_cols[1]:
            if st.button("🔊 Listen", key="listen_output_btn", use_container_width=True):
                if output_val.strip():
                    audio = text_to_speech(output_val, st.session_state.tgt_lang)
                    if audio:
                        st.session_state.audio_to_play = audio
                        st.rerun()
        with action_cols[2]:
            if st.button("🔖 Save Phrase", key="save_phrase_btn", use_container_width=True):
                if not st.session_state.authenticated:
                    st.warning("Sign in to save phrases and unlock phrasebook.")
                elif output_val.strip():
                    st.session_state.phrasebook.append({
                        "input": input_text,
                        "output": output_val,
                        "lang": st.session_state.tgt_lang,
                        "date": datetime.datetime.now().isoformat()
                    })
                    save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                    st.toast("Phrase saved to your phrasebook!")
        with action_cols[3]:
            if st.button("❤️ Favorite", key="favorite_output_btn", use_container_width=True):
                if not st.session_state.authenticated:
                    st.warning("Sign in to favorite translations.")
                elif output_val.strip():
                    st.session_state.favorites.append({
                        "input": input_text,
                        "output": output_val,
                        "lang": st.session_state.tgt_lang,
                        "date": datetime.datetime.now().isoformat()
                    })
                    save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                    st.toast("Added to favorites!")
        st.markdown("</div>", unsafe_allow_html=True)

        if output_val.strip():
            st.markdown("<div class='grammar-card'>", unsafe_allow_html=True)
            st.markdown("""
              <div class='panel-header'>
                <div>
                  <div class='panel-title'>Grammar & Writing Tools</div>
                  <div class='panel-subtitle'>Improve your translated text with one tap.</div>
                </div>
              </div>
            """, unsafe_allow_html=True)
            grammar_cols = st.columns([1, 1], gap="small")
            with grammar_cols[0]:
                if st.button("✅ Check Grammar", key="check_grammar_btn", use_container_width=True):
                    grammar_result = check_grammar(output_val)
                    if grammar_result["error_count"] == 0:
                        st.success("No grammar issues found.")
                    else:
                        st.warning(f"Found {grammar_result['error_count']} suggestion(s).")
                        for error in grammar_result["suggestions"][:3]:
                            st.info(f"{error['original']} → {error['suggestion']}")
            with grammar_cols[1]:
                if st.button("✨ Fix Spelling", key="fix_spelling_btn", use_container_width=True):
                    correction = correct_spelling(output_val)
                    if correction.get("is_corrected"):
                        st.session_state.translation_result = correction["corrected"]
                        st.success("Spelling improvements applied.")
                        st.rerun()
                    else:
                        st.info("No spelling issues found.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with side_col:
        st.markdown("<div class='translator-column narrow'>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            st.markdown("""
              <div class='sidebar-card'>
                <div class='title'>Phrasebook preview</div>
                <div class='description'>Your latest saved phrases and quick reuse suggestions.</div>
              </div>
            """, unsafe_allow_html=True)
            if st.session_state.phrasebook:
                for item in reversed(st.session_state.phrasebook[-4:]):
                    st.markdown(f"""
                      <div class='sidebar-card'>
                        <div class='history-meta'>
                          <div class='history-chip'>{SUPPORTED_LANGS.get(item['lang'], item['lang']).upper()}</div>
                        </div>
                        <p class='history-text'><strong>{item['input'][:42]}</strong></p>
                        <p class='history-text' style='color:#2563eb; margin-top:8px;'>{item['output'][:42]}</p>
                      </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<div class='sidebar-card'><p class='history-text'>No saved phrases yet. Translate and save phrases to populate this preview.</p></div>", unsafe_allow_html=True)
            if st.button("View all phrases", key="view_phrasebook_btn", use_container_width=True, type="secondary"):
                st.session_state.show_dashboard = True
                st.rerun()

            st.markdown("""
              <div class='sidebar-card'>
                <div class='title'>Audio playback</div>
                <div class='description'>Listen to your translated result once rendering is complete.</div>
              </div>
            """, unsafe_allow_html=True)
            if output_val.strip():
                st.markdown("<div class='history-card'><p class='history-text'>Translation ready to listen. Use the Listen action above.</p></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='history-card'><p class='history-text'>Translate text to unlock audio playback cues.</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("""
              <div class='sidebar-cta'>
                <div class='title'>Unlock premium features</div>
                <div class='description'>Sign in to save history, favorites, and your phrasebook across devices.</div>
                <div class='feature-pill'>💾 Save translation history</div>
                <div class='feature-pill'>❤️ Favorite translations</div>
                <div class='feature-pill'>📚 Phrasebook preview</div>
                <div class='feature-pill'>☁️ Sync across devices</div>
              </div>
            """, unsafe_allow_html=True)
            if st.button("Sign in to unlock", key="signin_history_btn", use_container_width=True, type="primary"):
                st.session_state.page = "auth"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='history-section'>", unsafe_allow_html=True)
    st.markdown("""
      <div class='section-header'>
        <div>
          <div class='workspace-label'>Recent history</div>
          <div class='section-title'>Your latest translations</div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    if st.session_state.authenticated:
        if st.session_state.history:
            st.markdown("""
            <div class='history-table'>
              <div class='history-row header'>
                <div>From</div>
                <div>To</div>
                <div>Text</div>
                <div>Time</div>
                <div>Action</div>
              </div>
            """, unsafe_allow_html=True)
            for idx, entry in enumerate(reversed(st.session_state.history[-8:])):
                compact_input = entry['input'][:45] + ('...' if len(entry['input']) > 45 else '')
                compact_output = entry['output'][:45] + ('...' if len(entry['output']) > 45 else '')
                st.markdown(f"""
                <div class='history-row'>
                  <div>{entry['src']}</div>
                  <div>{entry['tgt']}</div>
                  <div><strong>{compact_input}</strong><br><span style='color:#64748B;'>{compact_output}</span></div>
                  <div>{entry['Time']}</div>
                  <div><button class='restore-btn'>Restore</button></div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Restore", key=f"hist_restore_{idx}", use_container_width=True):
                    st.session_state.input_text = entry['input']
                    st.session_state.translation_result = entry['output']
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='history-empty'>No recent translations yet. Translate to build your history.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='history-empty'>Sign in to view your translation history and favorite entries.</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st

# Page Config must be first
st.set_page_config(page_title="Linguistix", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

import datetime
import time

# Config & Styles
from config import WOTD_LIST, QUOTES, THEMES
from views.ui_styles import get_main_css

# Utilities
from utils.session import initialize_session_state, swap_languages
from utils.translator import SUPPORTED_LANGS
from utils.pdf import create_pdf
from utils.storage import save_data

# Views
from views.auth import render_auth_page
from views.sidebar import render_sidebar
from views.translator import render_translator
from views.conversation import render_conversation
from views.dictionary_view import render_dictionary
from views.offline_hub import render_offline_hub
from views.image_translate import render_image_translate
from views.doc_translate import render_doc_translate
from views.fun_zone import render_fun_zone
from views.games import render_word_games
from views.dashboard import show_dashboard_modal

# Initialize Session State
initialize_session_state()

# Global Theme setup
theme_choice = st.session_state.get("theme_selection_box", "cloud_fusion")
if theme_choice not in THEMES:
    theme_choice = "cloud_fusion"
active_theme = THEMES[theme_choice]

# CSS Injection
st.markdown(get_main_css(active_theme), unsafe_allow_html=True)

def main():
    if st.session_state.page == "auth":
        render_auth_page()
        return

    # Sidebar Rendering
    render_sidebar()


    # Header Section
    h_col1, h_col2, h_col3 = st.columns([1, 4, 1], gap="medium")
    with h_col2:
        st.markdown('<div class="hero-text"><h1 style="text-align:center !important; font-family: \'Poppins\', sans-serif !important; text-transform:uppercase; margin-bottom:4px; margin-top:0; padding:0; font-weight:900; font-size:56px; letter-spacing:-1.5px;">LINGUISTIX</h1></div>', unsafe_allow_html=True)
        st.markdown("<div class='hero-text'><p style='text-align:center !important; font-family: \'Inter\', sans-serif !important; opacity:0.85; font-size:16px; margin:0; padding:0; margin-top:4px; color:var(--text-secondary) !important;'>Translate Beyond Words</p></div>", unsafe_allow_html=True)
    with h_col3:
        st.markdown("<div class='auth-btn' style='text-align:right; padding-top:4px;'>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            col_profile, col_logout = st.columns([2, 1])
            with col_profile:
                if st.button(f"👤 {st.session_state.username}", key="nav_profile_btn", use_container_width=True):
                    st.session_state.show_dashboard = True
                    st.rerun()
            with col_logout:
                if st.button("Logout", key="nav_logout_btn", use_container_width=True):
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.session_state.show_dashboard = False
                    st.session_state.history = []
                    st.session_state.favorites = []
                    st.session_state.phrasebook = []
                    st.rerun()
        else:
            if st.button("🔑 Login / Sign Up", key="nav_login_btn"):
                st.session_state.page = "auth"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()

    # Tabs definition
    target_options = [l for l in SUPPORTED_LANGS.keys() if l != "auto"]
    tab_list = ["Translator", "🤝 Conversation", "Dictionary", "📲 Offline Hub"]
    if st.session_state.authenticated:
        tab_list += ["📸 Image Translate", "📄 Doc Translate", "🧩 Fun Zone"]
    else:
        tab_list += ["🔐 Image Translate", "🔐 Doc Translate", "🧩 Fun Zone"]

    tabs = st.tabs(tab_list)
    
    with tabs[0]:
        render_translator(target_options, create_pdf)
    with tabs[1]:
        render_conversation(target_options)
    with tabs[2]:
        render_dictionary(target_options)
    with tabs[3]:
        render_offline_hub()
    with tabs[4]:
        render_image_translate(target_options, create_pdf)
    with tabs[5]:
        render_doc_translate(target_options, create_pdf)
    with tabs[6]:
        render_fun_zone(render_word_games)

    # Dashboard Modal
    if st.session_state.show_dashboard and st.session_state.authenticated:
        show_dashboard_modal()

    # Footer Section
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.divider()
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown("**Your World, Translated.**")
        st.caption("Empowering global dialogue.")
    with f_col2:
        st.markdown("**Crafted for Clarity.**")
        st.caption("Clean code. Clean design.")
    with f_col3:
        st.markdown("**Always Evolving.**")
        st.caption("v1.0.0 | © 2026 Linguistix")

if __name__ == "__main__":
    main()
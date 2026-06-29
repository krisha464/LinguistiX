import streamlit as st
import time
import base64
import os
from utils.storage import load_users, verify_password, load_data, hash_password, save_users, find_user, get_remembered_user, set_remember_me

def handle_social_login(provider, users):
    """Mock social login handler"""
    mock_email = f"user@{provider.lower()}.com"
    username = f"{provider}User"
    
    # Register mock user if doesn't exist
    if username not in users:
        users[username] = {"password": hash_password("social_login_dummy"), "email": mock_email}
        save_users(users)
        
    st.session_state.authenticated = True
    st.session_state.username = username
    u_data = load_data(username)
    st.session_state.history = u_data.get("history", [])
    st.session_state.favorites = u_data.get("favorites", [])
    st.session_state.phrasebook = u_data.get("phrasebook", [])
    st.session_state.page = "main"
    st.toast(f"✅ Signed in with {provider}!", icon="🎉")
    time.sleep(0.5)
    st.rerun()

def render_auth_page():
    # State init
    if "auth_tab" not in st.session_state:
        remembered = get_remembered_user()
        if remembered:
            st.session_state.auth_tab = "login"
            st.session_state.prefill_user = remembered
        else:
            st.session_state.auth_tab = "login"
            st.session_state.prefill_user = ""
            
    users = load_users()

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

    .stApp {{
        background: linear-gradient(135deg, #F4FAFF 0%, #EAF7FF 40%, #FFFFFF 100%) !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        font-family: 'Inter', sans-serif !important;
        overflow-x: hidden;
        min-height: 100vh;
    }}

    .stMainBlockContainer {{
        background: transparent !important;
        padding: 0 !important;
        max-width: 100%;
    }}

    /* Top Navbar */
    .top-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.5);
    }}
    .nav-logo {{
        display: flex;
        align-items: center;
        gap: 10px;
        color: #1E293B;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 20px;
    }}
    .nav-links {{
        display: flex;
        gap: 30px;
        align-items: center;
    }}
    .nav-links span {{
        color: #1E293B;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .nav-links span:hover {{ color: #3B82F6; }}
    
    /* Center Branding */
    .brand-header {{
        text-align: center;
        margin-top: 100px;
        margin-bottom: 30px;
        animation: fadeInUp 1s ease-out;
    }}
    .ai-badge {{
        background: rgba(255, 255, 255, 0.95);
        color: #3B82F6;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #D9ECF7;
    }}
    .brand-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 64px;
        font-weight: 900;
        color: #1E293B;
        margin: 0;
        letter-spacing: -2px;
    }}
    .brand-subtitle {{
        color: #64748B;
        font-size: 16px;
        margin-top: 5px;
        font-weight: 500;
    }}

    /* Feature Badges */
    .feature-badges {{
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 20px 0;
        flex-wrap: wrap;
    }}
    .feature-badge {{
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid #D9ECF7;
        color: #3B82F6;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    /* Floating Blobs */
    .blob {{
        position: fixed;
        border-radius: 50%;
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
        filter: blur(40px);
    }}
    .blob-blue {{ background: #B6F4FF; }}
    .blob-cyan {{ background: #A7F3F0; }}
    .blob-light {{ background: #CFFAFE; }}

    /* The Glass Card */
    .auth-container-wrapper {{
        display: flex;
        justify-content: center;
        position: relative;
        z-index: 10;
        padding-bottom: 50px;
    }}
    [data-testid="column"]:nth-child(2) {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid #D9ECF7 !important;
        border-radius: 24px !important;
        padding: 40px !important;
        box-shadow: 0 20px 50px rgba(125,211,252,.15) !important;
        max-width: 440px !important;
        margin: 0 auto !important;
        animation: fadeInUp 0.8s ease-out;
    }}

    /* Card Headers */
    .card-icon {{
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }}
    .card-icon-inner {{
        background: linear-gradient(135deg, #3B82F6, #60A5FA);
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }}
    .card-title {{
        color: #1E293B;
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        margin: 0;
        font-family: 'Poppins', sans-serif;
    }}
    .card-subtitle {{
        color: #64748B;
        font-size: 14px;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 25px;
        line-height: 1.5;
    }}

    /* Inputs */
    .stTextInput input {{
        background: #FFFFFF !important;
        border: 1.5px solid #D9ECF7 !important;
        border-radius: 12px !important;
        color: #1E293B !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }}
    .stTextInput input:focus {{
        background: #FFFFFF !important;
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }}
    ::placeholder {{
        color: #94A3B8 !important;
    }}

    /* Primary Button */
    .stButton button[kind="primary"] {{
        background: linear-gradient(135deg, #3B82F6, #60A5FA) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        margin-top: 10px !important;
        width: 100% !important;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3) !important;
    }}
    .stButton button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 25px rgba(59, 130, 246, 0.4) !important;
        filter: brightness(1.1) !important;
    }}

    /* Divider */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin: 20px 0;
    }}
    .divider::before, .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid #D9ECF7;
    }}
    .divider::before {{ margin-right: .5em; }}
    .divider::after {{ margin-left: .5em; }}

    /* Social Buttons */
    .social-btn .stButton button {{
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid #D9ECF7 !important;
        border-radius: 12px !important;
        color: #1E293B !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 12px !important;
        width: 100% !important;
        margin-bottom: 10px !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .social-btn .stButton button:hover {{
        background: rgba(255, 255, 255, 0.9) !important;
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
    }}

    /* Checkbox */
    [data-testid="stCheckbox"] label span {{ color: #1E293B !important; font-size: 13px !important; }}
    [data-testid="stCheckbox"] div[role="checkbox"] {{ border-color: #D9ECF7 !important; background: transparent !important; }}
    [data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {{ background: #3B82F6 !important; border-color: #3B82F6 !important; }}

    /* Links */
    .text-link-btn .stButton button {{
        background: transparent !important;
        border: none !important;
        color: #3B82F6 !important;
        font-size: 13px !important;
        padding: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        box-shadow: none !important;
    }}
    .text-link-btn .stButton button:hover {{ text-decoration: underline !important; color: #2563EB !important; }}

    .element-container {{ margin-bottom: 0px !important; }}
    
    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    
    /* Floating Language Pills Animation */
    @keyframes floatPill {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-15px); }}
    }}
    
    .lang-pill {{
        position: fixed;
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid #D9ECF7;
        backdrop-filter: blur(8px);
        color: #3B82F6;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 700;
        z-index: 0;
        pointer-events: none;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    </style>
    """, unsafe_allow_html=True)

    # UI Elements (HTML Overlays)
    st.markdown("""
    <div class="top-nav">
        <div class="nav-logo">🗣️ LinguistiX</div>
        <div class="nav-links">
            <span>Home</span>
            <span>Features</span>
            <span>About</span>
            <span>Contact</span>
            <span style="background:linear-gradient(135deg, #3B82F6, #60A5FA); padding:8px 20px; border-radius:20px; color:white; font-weight:600;">Get Started</span>
        </div>
    </div>
    
    <div class="brand-header">
        <div class="ai-badge">✨ THE FUTURE OF AI 🚀</div>
        <h1 class="brand-title">LinguistiX</h1>
        <div class="brand-subtitle">Translate Beyond Words 🌎</div>
        <div class="feature-badges">
            <div class="feature-badge">🤖 AI Powered</div>
            <div class="feature-badge">🌐 100+ Languages</div>
            <div class="feature-badge">⚡ Real-Time Translation</div>
        </div>
    </div>

    <!-- Floating Blobs -->
    <div class="blob blob-blue" style="top: 15%; left: 10%; width: 300px; height: 300px;"></div>
    <div class="blob blob-cyan" style="top: 45%; right: 15%; width: 250px; height: 250px;"></div>
    <div class="blob blob-light" style="bottom: 10%; left: 20%; width: 200px; height: 200px;"></div>
    <div class="blob blob-blue" style="top: 60%; right: 5%; width: 280px; height: 280px;"></div>
    
    <!-- Floating Language Pills -->
    <div class="lang-pill" style="top: 20%; left: 8%; animation: floatPill 6s ease-in-out infinite 0s;">BONJOUR</div>
    <div class="lang-pill" style="top: 55%; left: 12%; animation: floatPill 6s ease-in-out infinite 1s;">नमस्ते</div>
    <div class="lang-pill" style="top: 30%; right: 10%; animation: floatPill 6s ease-in-out infinite 0.5s;">HELLO</div>
    <div class="lang-pill" style="top: 65%; right: 8%; animation: floatPill 6s ease-in-out infinite 1.5s;">HALLO</div>
    <div class="lang-pill" style="top: 40%; left: 18%; animation: floatPill 6s ease-in-out infinite 2s;">HOLA</div>
    <div class="lang-pill" style="top: 75%; right: 20%; animation: floatPill 6s ease-in-out infinite 2.5s;">你好</div>
    """, unsafe_allow_html=True)

    # 3 Column layout to center the card
    st.markdown("<div class='auth-container-wrapper'>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])

    with center_col:
        # Icon
        st.markdown("""
        <div class="card-icon">
            <div class="card-icon-inner">🗣️</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.auth_tab == "login":
            st.markdown("<div class='card-title'>Welcome Back</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-subtitle'>Continue your multilingual journey with LinguistiX</div>", unsafe_allow_html=True)

            u_in = st.text_input("Email", placeholder="✉️ Enter your email", key="page_u_in", value=st.session_state.prefill_user, label_visibility="collapsed")
            p_in = st.text_input("Password", type="password", placeholder="🔒 Enter your password", key="page_p_in", label_visibility="collapsed")
            
            rm_col, fp_col = st.columns([1.5, 1])
            with rm_col:
                remember = st.checkbox("Remember me", value=bool(st.session_state.prefill_user))
            with fp_col:
                st.markdown("<div class='text-link-btn' style='text-align: right; padding-top:6px;'>", unsafe_allow_html=True)
                if st.button("Forgot Password?", key="forgot_link_btn"):
                    st.session_state.auth_tab = "forgot"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
            if st.button("Sign In →", type="primary", use_container_width=True, key="sign_in_btn"):
                if not u_in or not p_in:
                    st.error("Please enter email and password")
                else:
                    with st.spinner("Authenticating..."):
                        time.sleep(0.5)
                        username, user_data = find_user(u_in, users)
                        if user_data and verify_password(p_in, user_data["password"]):
                            # Handle Remember Me
                            set_remember_me(username, remember)
                            
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            u_data = load_data(username)
                            st.session_state.history = u_data.get("history", [])
                            st.session_state.favorites = u_data.get("favorites", [])
                            st.session_state.phrasebook = u_data.get("phrasebook", [])
                            st.session_state.page = "main"
                            st.toast(f"✅ Welcome back, {username}!", icon="🎉")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Invalid credentials.")

            st.markdown("<div class='divider'>OR</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='social-btn'>", unsafe_allow_html=True)
            g_col, gh_col = st.columns(2)
            with g_col:
                if st.button("Continue with Google", use_container_width=True):
                    handle_social_login("Google", users)
            with gh_col:
                if st.button("Continue with GitHub", use_container_width=True):
                    handle_social_login("GitHub", users)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='text-align:center; margin-top:20px; color:#64748B; font-size:13px;'>Don't have an account?</div>", unsafe_allow_html=True)
            st.markdown("<div class='text-link-btn' style='text-align:center;'>", unsafe_allow_html=True)
            if st.button("Sign up", key="go_to_signup_link"):
                st.session_state.auth_tab = "signup"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.auth_tab == "signup":
            st.markdown("<div class='card-title'>Create Account</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-subtitle'>Join LinguistiX and explore the world without language barriers.</div>", unsafe_allow_html=True)

            nu_in = st.text_input("Username", placeholder="👤 Full Name", key="page_nu_in", label_visibility="collapsed")
            em_in = st.text_input("Email", placeholder="✉️ Enter your email", key="page_em_in", label_visibility="collapsed")
            np_in = st.text_input("Password", type="password", placeholder="🔒 Create a password", key="page_np_in", label_visibility="collapsed")
            cp_in = st.text_input("Confirm", type="password", placeholder="🔒 Confirm password", key="page_cp_in", label_visibility="collapsed")
            
            st.checkbox("I agree to the Terms of Service and Privacy Policy")

            if st.button("Sign Up →", type="primary", use_container_width=True, key="create_acc_btn"):
                if nu_in in users:
                    st.error("Username already taken")
                elif any(u.get("email") == em_in for u in users.values() if isinstance(u, dict)):
                    st.error("Email already registered")
                elif np_in != cp_in:
                    st.error("Passwords do not match")
                elif len(nu_in) < 3 or len(np_in) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    users[nu_in] = {"password": hash_password(np_in), "email": em_in}
                    save_users(users)
                    st.success("Account created!")
                    time.sleep(1)
                    st.session_state.auth_tab = "login"
                    st.rerun()

            st.markdown("<div class='divider'>OR</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='social-btn'>", unsafe_allow_html=True)
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                if st.button("Continue with Google", use_container_width=True, key="sg_btn"):
                    handle_social_login("Google", users)
            with s_col2:
                if st.button("Continue with GitHub", use_container_width=True, key="sh_btn"):
                    handle_social_login("GitHub", users)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='text-align:center; margin-top:20px; color:#64748B; font-size:13px;'>Already have an account?</div>", unsafe_allow_html=True)
            st.markdown("<div class='text-link-btn' style='text-align:center;'>", unsafe_allow_html=True)
            if st.button("Sign in", key="go_to_login_link"):
                st.session_state.auth_tab = "login"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.auth_tab == "forgot":
            st.markdown("<div class='card-title'>Reset Password</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-subtitle'>Get back into your account.</div>", unsafe_allow_html=True)

            f_u_in = st.text_input("Email", placeholder="✉️ Email or Username", key="forgot_u_in", label_visibility="collapsed")
            f_p_in = st.text_input("New Password", type="password", placeholder="🔒 New password", key="forgot_p_in", label_visibility="collapsed")
            f_cp_in = st.text_input("Confirm", type="password", placeholder="🔒 Confirm password", key="forgot_cp_in", label_visibility="collapsed")
            
            if st.button("Reset →", type="primary", use_container_width=True):
                username, user_data = find_user(f_u_in, users)
                if not user_data:
                    st.error("User not found")
                elif f_p_in != f_cp_in:
                    st.error("Passwords do not match")
                elif len(f_p_in) < 6:
                    st.error("Password too short")
                else:
                    users[username]["password"] = hash_password(f_p_in)
                    save_users(users)
                    st.success("Password updated!")
                    time.sleep(1)
                    st.session_state.auth_tab = "login"
                    st.rerun()

            st.markdown("<div style='text-align:center; margin-top:20px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='text-link-btn' style='text-align:center;'>", unsafe_allow_html=True)
            if st.button("Back to Login", key="back_to_login_btn"):
                st.session_state.auth_tab = "login"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

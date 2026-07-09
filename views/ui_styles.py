import streamlit as st
import base64
import os

@st.cache_data
def _get_bg_b64():
    """Load the background image as a base64 string (cached)."""
    img_path = os.path.join("images", "bg.png")
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

@st.cache_data
def get_main_css(theme):
    bg_b64 = _get_bg_b64()
    _bg_url = f"url('data:image/png;base64,{bg_b64}')" if bg_b64 else "none"
    
    # Extract primary accent color
    primary_accent = theme['accent']
    accent_light = theme.get('accent_secondary', primary_accent)
    
    return f"""

<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800;900&family=Outfit:wght@400;600;800&family=Inter:wght@400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

    /* ═══════════════════════════════════════════════════════════════
       COHESIVE COLOR SYSTEM - Primary Color with Depth Layering
       ═══════════════════════════════════════════════════════════════ */
    
    :root {{
        /* PRIMARY COLOR & ACCENTS */
        --primary: #2563EB;
        --primary-light: #60A5FA;
        --primary-dark: rgba(15, 23, 42, 0.12);
        
        /* COLOR TINTS FOR DEPTH & STATES */
        --primary-hover: rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.9);
        --primary-active: rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.85);
        --primary-disabled: rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.5);
        
        /* BACKGROUND TINTS - Lighter/Darker for visual hierarchy */
        --bg-lightest: rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.05);
        --bg-light: rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.1);
        --bg-lighter: rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.15);
        
        /* SHADOW SYSTEM - Elevation Depth */
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
        --shadow-xl: 0 12px 32px rgba(0, 0, 0, 0.15);
        --shadow-2xl: 0 20px 50px rgba(125, 211, 252, 0.15);
        --shadow-accent-sm: 0 2px 8px rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.2);
        --shadow-accent-md: 0 6px 20px rgba({int(primary_accent[1:3], 16)}, {int(primary_accent[3:5], 16)}, {int(primary_accent[5:7], 16)}, 0.3);
        
        /* TEXT COLORS */
        --text-primary: {theme.get('text', '#1E293B')};
        --text-secondary: {theme.get('text_muted', '#64748B')};
        --text-tertiary: #94A3B8;
        --text-inverse: {theme.get('text_inverse', '#ffffff')};
        
        /* ACCENT & BORDERS */
        --accent: #14B8A6;
        --accent-secondary: #60A5FA;
        --panel: #FFFFFF;
        --bg: #F8FAFC;
        --border: #E2E8F0;
        --glow: rgba(37, 99, 235, 0.14);
        
        /* TYPOGRAPHY */
        --font-heading: 'Outfit', sans-serif;
        --font-body: 'Inter', sans-serif;
        
        /* SPACING & SIZING */
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 12px;
        --spacing-lg: 16px;
        --spacing-xl: 24px;
        --spacing-2xl: 32px;
        
        /* TRANSITIONS */
        --transition-fast: 0.15s cubic-bezier(0.2, 0, 0.38, 0.9);
        --transition-base: 0.25s cubic-bezier(0.2, 0, 0.38, 0.9);
        --transition-slow: 0.4s cubic-bezier(0.2, 0, 0.38, 0.9);
        
        /* BORDER RADIUS */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --radius-2xl: 24px;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       LOADING STATES & SKELETON SCREENS - Smooth Transitions
       ═══════════════════════════════════════════════════════════════ */
    
    /* Loading spinner - Smooth rotation */
    @keyframes spinLoader {{
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Skeleton screen - Shimmer effect */
    @keyframes shimmerLoader {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    .loading-spinner {{
        display: inline-block;
        width: 24px;
        height: 24px;
        border: 3px solid var(--bg-light);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spinLoader 0.8s linear infinite;
    }}
    
    .skeleton {{
        background: linear-gradient(
            90deg,
            var(--bg-lightest) 0%,
            var(--bg-light) 50%,
            var(--bg-lightest) 100%
        );
        background-size: 1000px 100%;
        animation: shimmerLoader 2s infinite;
        border-radius: var(--radius-md);
    }}
    
    .skeleton-text {{
        height: 16px;
        margin-bottom: 12px;
        border-radius: var(--radius-sm);
    }}
    
    .skeleton-text.large {{
        height: 24px;
    }}
    
    /* Button loading state */
    .stButton button:disabled {{
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        box-shadow: var(--shadow-sm) !important;
    }}
    
    /* Smooth transition for modals, drawers, tooltips */
    @keyframes slideInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeInScale {{
        from {{
            opacity: 0;
            transform: scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    /* Modal-like elements */
    [data-testid="stModalBody"] {{
        animation: fadeInScale var(--transition-base) ease-out !important;
    }}
    
    /* Drawer-like elements */
    [data-testid="stSidebar"] {{
        animation: slideInDown 0.3s ease-out !important;
    }}

    /* GLOBAL RESET - Clean and minimal */
    #MainMenu, footer, [data-testid="stDecoration"] {{visibility: hidden; display: none !important;}}
    header, [data-testid="stHeader"] {{
        background: transparent !important;
        height: 0px !important;
    }}
    [data-testid="stHeader"] > div {{visibility: visible !important;}}
    
    /* ═══════════════════════════════════════════════════
       BACKGROUND - Clean, soft gradient  
    ═══════════════════════════════════════════════════ */
    .stApp {{
        background-image: radial-gradient(circle at top left, #EEF6FF 0%, #F8FBFF 36%, #FFFFFF 100%) !important;
        background-color: #F8FBFF !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    /* Force global text color — using theme text colors */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp .stMarkdown div, .stApp .stCaption,
    [data-testid="stWidgetLabel"] p, [data-testid="stHeader"] *, .stMarkdown p,
    .stSelectbox div, .stTextInput div, .stTextArea div,
    h2, h3, h4, h5, h6, li, td, th, strong, em, b {{
        color: var(--text-primary) !important;
    }}
    
    /* Input field text color stabilization */
    input, textarea, select {{
        color: var(--text-primary) !important;
    }}
    
    /* Ensure inputs have a solid, soft card surface */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {{
        background: #F8FBFF !important;
        color: var(--text-primary) !important;
        border: 1.5px solid rgba(148, 163, 184, 0.35) !important;
        border-radius: 20px !important;
        box-shadow: inset 0 1px 3px rgba(15, 23, 42, 0.06) !important;
        transition: border-color var(--transition-fast) !important, box-shadow var(--transition-fast) !important;
    }}

    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12) !important;
    }}

    textarea[aria-label="Output text"] {{
        animation: fadeInText 0.35s ease both !important;
    }}
    
    /* Muted/secondary text — using theme text_muted */
    .secondary-text, [data-testid="stCaption"], .stCaption {{
        color: var(--text-secondary) !important;
        opacity: 0.85 !important;
    }}

    /* Sidebar — white glassmorphism panel */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-right: 1px solid {theme.get('border', '#D9ECF7')} !important;
    }}
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: var(--text-primary) !important;
    }}

    [data-testid="stSidebar"] [data-testid="stExpander"] > div:first-child,
    [data-testid="stSidebar"] [data-testid="stExpander"] > div:nth-child(2),
    [data-testid="stExpander"] {{
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1.5px solid {theme.get('border', '#D9ECF7')} !important;
        border-radius: 14px !important;
        color: var(--text-primary) !important;
    }}

    /* Global Expander Header Fix */
    [data-testid="stExpander"] summary {{
        background: rgba(255, 255, 255, 0.7) !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }}

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] {{
        background: var(--panel) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }}
    .stSelectbox [data-baseweb="select"] * {{
        background: transparent !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    /* GLOBAL — Selectbox floating dropdown (FORCE LIGHT) */
    [data-baseweb="popover"], [role="listbox"], [data-baseweb="menu"] {{
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1px solid #D9ECF7 !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.12) !important;
        border-radius: 12px !important;
    }}
    [role="option"], [data-baseweb="menu"] li {{
        background: #FFFFFF !important;
        color: var(--text-primary) !important;
        padding: 10px 16px !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }}
    [role="option"]:hover, [data-baseweb="menu"] li:hover {{
        background: rgba(91,181,224,0.15) !important;
        color: var(--accent) !important;
    }}
    
    .result-card {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid #D9ECF7 !important;
        box-shadow: 0 20px 50px rgba(125,211,252,.15) !important;
        color: var(--text-primary) !important;
        padding: 24px;
        border-radius: 20px;
    }}

    /* FILE UPLOADER - Comprehensive Cloud Fusion Pastel Styling */
    .stFileUploader section, 
    [data-testid="stFileUploadDropzone"], 
    .stFileUploader {{
        background: #F8FAFC !important;
        border: 2.2px dashed rgba(59, 130, 246, 0.25) !important;
        border-radius: 18px !important;
        transition: all 0.3s ease !important;
        color: #1E293B !important;
        padding: 24px !important;
        min-height: 120px !important;
    }}
    
    .stFileUploader section:hover, 
    [data-testid="stFileUploadDropzone"]:hover {{
        background: #EFF6FF !important;
        border-color: #2563EB !important;
        border-width: 2.5px !important;
        box-shadow: 0 8px 30px rgba(37, 99, 235, 0.12) !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Force text/icon colors inside uploader dropzone only */
    [data-testid="stFileUploadDropzone"] * {{
        color: #1E293B !important;
        background: transparent !important;
        fill: #3B82F6 !important;
    }}

    /* Uploaded file name chip — must stay readable */
    [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploaderFileName"],
    .stFileUploader [data-testid="stFileUploaderDeleteBtn"] ~ span,
    .stFileUploader li,
    .stFileUploader li span,
    .stFileUploader li p,
    [data-testid="stFileUploader"] li,
    [data-testid="stFileUploader"] li span,
    [data-testid="stFileUploader"] li p {{
        color: #1E293B !important;
        background: #FFFFFF !important;
    }}

    /* File name pill/chip wrapper */
    .stFileUploader [class*="fileInfo"],
    .stFileUploader [class*="UploadedFile"],
    [data-testid="stFileUploaderFile"] {{
        background: #FFFFFF !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 10px !important;
        color: #1E293B !important;
        padding: 6px 12px !important;
    }}

    /* Filename text specifically */
    [data-testid="stFileUploaderFileName"] span,
    [data-testid="stFileUploaderFileName"] p,
    [data-testid="stFileUploaderFileName"] {{
        color: #1E293B !important;
        background: transparent !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    /* Browse Button Inside Uploader specifically */
    .stFileUploader button, 
    [data-testid="stFileUploadDropzone"] button {{
        background: #FFFFFF !important;
        border: 1.5px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #3B82F6 !important;
        font-weight: 800 !important;
        padding: 10px 24px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }}
    [role="option"][aria-selected="true"] {{
        background: {theme['accent']}22 !important;
        color: {theme['accent']} !important;
        font-weight: 700 !important;
    }}


    /* MAIN CONTAINER - Proper alignment and spacing */
    .stMainBlockContainer {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.75rem 1.5rem 2rem 1.5rem !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        width: 100% !important;
        max-width: 1400px !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        position: relative !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       MOBILE RESPONSIVE - Tap Targets & Prioritized Actions
       ═══════════════════════════════════════════════════════════════ */
    
    /* Ensure all interactive elements have minimum 48x48px tap target */
    @media (max-width: 768px) {{
        .stMainBlockContainer {{
            padding: 1rem 0.75rem !important;
        }}
        
        h1 {{ 
            font-size: 32px !important; 
        }}
        
        /* Stack horizontal blocks vertically on mobile */
        [data-testid="stHorizontalBlock"] {{
            flex-direction: column !important;
            gap: 12px !important;
        }}
        
        /* Ensure buttons are tap-friendly on mobile */
        .stButton button {{
            min-height: 48px !important;
            padding: 14px 20px !important;
            font-size: 0.95rem !important;
        }}
        
        /* Input fields - tap-friendly */
        .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {{
            min-height: 48px !important;
            padding: 14px 16px !important;
            font-size: 16px !important;
        }}
        
        /* CTA button - larger on mobile */
        .cta-btn-wrap .stButton button {{
            min-height: 56px !important;
            font-size: 1.1rem !important;
            padding: 16px 24px !important;
        }}
        
        /* Cards - reduced padding on mobile */
        .result-card, .sidebar-card, .game-v2-card {{
            padding: 16px !important;
            margin: 12px 0 !important;
        }}
        
        /* Hide non-essential content on mobile */
        .mobile-hide {{
            display: none !important;
        }}
        
        /* Badges - larger on mobile */
        .badge {{
            padding: 8px 16px !important;
            font-size: 12px !important;
        }}
        
        /* Content grouping - single column on mobile */
        .grouped-row {{
            grid-template-columns: 1fr !important;
            gap: 12px !important;
        }}
        
        /* Sidebar - less padding on mobile */
        [data-testid="stSidebar"] {{
            padding: 8px !important;
        }}
    }}
    
    /* Extra small devices */
    @media (max-width: 480px) {{
        h1 {{ font-size: 24px !important; }}
        h2 {{ font-size: 20px !important; }}
        h3 {{ font-size: 16px !important; }}
        
        .stButton button {{
            padding: 12px 16px !important;
            font-size: 0.9rem !important;
        }}
        
        .cta-btn-wrap .stButton button {{
            min-height: 52px !important;
        }}
        
        .stMainBlockContainer {{
            padding: 0.75rem 0.5rem !important;
        }}
        
        /* Single column layout */
        [data-testid="stHorizontalBlock"] {{
            gap: 8px !important;
        }}
    }}

    /* TYPOGRAPHY - Clean and consistent */
    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes spin {{ 100% {{ transform:rotate(360deg); }} }}
    @keyframes pulseGlow {{ 0%, 100% {{ box-shadow: 0 0 10px var(--accent)40, 0 0 20px var(--accent)20; transform: scale(1); }} 50% {{ box-shadow: 0 0 25px var(--accent)60, 0 0 45px var(--accent)30; transform: scale(1.03); }} }}
    @keyframes shimmer {{ 0% {{ background-position: -200% 0; }} 100% {{ background-position: 200% 0; }} }}
    @keyframes globalShimmer {{ 0% {{ background-position: -100% center; }} 100% {{ background-position: 100% center; }} }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
    h1 {{
        background: linear-gradient(90deg, var(--text-primary), var(--accent), var(--text-primary));
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: globalShimmer 5s linear infinite;
        font-family: var(--font-heading) !important;
        font-size: 64px !important;
        font-weight: 800 !important;
        letter-spacing: -2.5px !important;
        text-align: center !important;
        margin-bottom: 4px !important;
        margin-top: 0 !important;
    }}
    
    h2, h3, h4 {{
        color: {theme.get('text', '#1E293B')} !important;
        font-family: var(--font-heading) !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
    }}
    
    .tagline {{
        text-align: center;
        color: #475569;
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 0;
        margin-top: 0;
        opacity: 0.75;
        letter-spacing: 0.2px;
    }}

    /* LAYOUT SECTIONS - Clear spacing */
    [data-testid="column"] {{
        padding: 0 !important;
    }}
    
    [data-testid="stHorizontalBlock"] {{
        gap: 16px !important;
        align-items: stretch !important;
    }}

    /* TABS - Clean style */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.9) !important;
        padding: 10px 14px !important;
        border: 1px solid var(--border) !important;
        border-radius: 999px !important;
        margin-bottom: 26px !important;
        display: flex !important;
        gap: 16px !important;
        flex-wrap: wrap !important;
        box-shadow: var(--shadow-sm) !important;
    }}

    button[data-baseweb="tab"] {{
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: none !important;
        border-radius: 999px !important;
        margin: 0 !important;
        padding: 10px 18px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all var(--transition-fast) !important;
        opacity: 0.9 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        background: var(--primary) !important;
        color: #ffffff !important;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18) !important;
        opacity: 1 !important;
    }}
    
    button[data-baseweb="tab"]:hover {{
        color: var(--text-primary) !important;
        opacity: 1 !important;
        background: rgba(37, 99, 235, 0.08) !important;
    }}


    /* ═══════════════════════════════════════════════════════
       BUTTON SYSTEM — 3-Tier: Primary | Ghost | Danger
    ═══════════════════════════════════════════════════════ */

    /* ═══════════════════════════════════════════════════════════════
       BUTTON SYSTEM - Three-Tier with Depth & Mobile Support
       ═══════════════════════════════════════════════════════════════ */
    
    /* Base button styles - CONSISTENT across all buttons */
    .stButton button {{
        font-family: var(--font-heading) !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.8px !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.75rem 1.5rem !important;
        transition: all var(--transition-fast) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        border: none !important;
        min-height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transform: translateZ(0) !important;
    }}

    /* PRIMARY BUTTON - Bold & Easy to Find */
    .stButton button[kind="primary"],
    .stButton button:not([kind="secondary"]) {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
        color: var(--text-inverse) !important;
        box-shadow: var(--shadow-accent-md), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }}
    
    /* PRIMARY HOVER - Elevated with depth */
    .stButton button:not([kind="secondary"]):hover {{
        transform: scale(1.02) translateY(-2px) !important;
        box-shadow: 
            var(--shadow-accent-md),
            0 14px 36px rgba(15, 23, 42, 0.16),
            0 0 18px var(--primary),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        filter: brightness(1.08) !important;
    }}
    
    /* PRIMARY ACTIVE - Pressed state with immediate feedback */
    .stButton button:not([kind="secondary"]):active {{
        transform: scale(0.98) translateY(-1px) !important;
        box-shadow: var(--shadow-sm), inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        filter: brightness(0.95) !important;
    }}

    /* SECONDARY BUTTON - Lighter, outline-based */
    .stButton button[kind="secondary"] {{
        background: linear-gradient(135deg, var(--primary)12, var(--primary)06) !important;
        color: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        box-shadow: var(--shadow-sm), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        font-weight: 700 !important;
    }}
    
    /* SECONDARY HOVER - Depth increase */
    .stButton button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, var(--primary)18, var(--primary)12) !important;
        border-color: var(--primary) !important;
        transform: scale(1.02) translateY(-1px) !important;
        box-shadow: var(--shadow-accent-md), inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
        filter: brightness(1.05) !important;
    }}
    
    /* SECONDARY ACTIVE */
    .stButton button[kind="secondary"]:active {{
        transform: scale(0.98) translateY(0px) !important;
        box-shadow: var(--shadow-sm), inset 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }}

    /* Error button */
    .error-btn .stButton button, .error-btn button {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.08)) !important;
        color: #ef4444 !important;
        border: 2px solid rgba(239, 68, 68, 0.5) !important;
        box-shadow: 
            0 2px 8px rgba(239, 68, 68, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
    }}
    
    .error-btn .stButton button:hover, .error-btn button:hover {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(239, 68, 68, 0.15)) !important;
        border-color: #ef4444 !important;
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 
            0 4px 15px rgba(239, 68, 68, 0.35),
            0 8px 25px rgba(239, 68, 68, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        filter: brightness(1.08) !important;
    }}

    /* Warning button */
    .warning-btn .stButton button {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.08)) !important;
        color: #f59e0b !important;
        border: 2px solid rgba(245, 158, 11, 0.5) !important;
        box-shadow: 
            0 2px 8px rgba(245, 158, 11, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
    }}
    
    .warning-btn .stButton button:hover {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(245, 158, 11, 0.15)) !important;
        border-color: #f59e0b !important;
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 
            0 4px 15px rgba(245, 158, 11, 0.35),
            0 8px 25px rgba(245, 158, 11, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        filter: brightness(1.08) !important;
    }}

    /* Success button */
    .success-btn .stButton button {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.08)) !important;
        color: #10b981 !important;
        border: 2px solid rgba(16, 185, 129, 0.5) !important;
        box-shadow: 
            0 2px 8px rgba(16, 185, 129, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
    }}
    
    .success-btn .stButton button:hover {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(16, 185, 129, 0.15)) !important;
        border-color: #10b981 !important;
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 
            0 4px 15px rgba(16, 185, 129, 0.35),
            0 8px 25px rgba(16, 185, 129, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        filter: brightness(1.08) !important;
    }}

    /* Download button */
    [data-testid="stDownloadButton"] button {{
        background: linear-gradient(135deg, rgba(100, 116, 139, 0.15), rgba(100, 116, 139, 0.08)) !important;
        color: #64748b !important;
        border: 2px solid rgba(100, 116, 139, 0.45) !important;
        border-radius: 12px !important;
        font-size: 0.82rem !important;
        padding: 0.5rem 1rem !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        box-shadow: 
            0 2px 8px rgba(100, 116, 139, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }}
    
    [data-testid="stDownloadButton"] button:hover {{
        background: linear-gradient(135deg, rgba(100, 116, 139, 0.25), rgba(100, 116, 139, 0.15)) !important;
        border-color: #94a3b8 !important;
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 
            0 4px 15px rgba(100, 116, 139, 0.3),
            0 8px 25px rgba(100, 116, 139, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        filter: brightness(1.08) !important;
    }}

    /* Sidebar button */
    [data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.08)) !important;
        color: #ef4444 !important;
        border: 2px solid rgba(239, 68, 68, 0.45) !important;
        font-size: 0.82rem !important;
        padding: 0.45rem 1rem !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        box-shadow: 
            0 2px 8px rgba(239, 68, 68, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }}
    
    [data-testid="stSidebar"] .stButton button:hover {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(239, 68, 68, 0.15)) !important;
        border-color: #ef4444 !important;
        transform: scale(1.03) translateY(-1px) !important;
        box-shadow: 
            0 3px 12px rgba(239, 68, 68, 0.3),
            0 6px 20px rgba(239, 68, 68, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        filter: brightness(1.08) !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       INPUT FIELDS & FORM ELEMENTS - Consistent Depth & Mobile Support
       ═══════════════════════════════════════════════════════════════ */
    
    /* TEXT INPUTS - Solid, Elevated, Tap-Friendly */
    .stTextInput input, .stTextArea textarea {{
        background: #FFFFFF !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-base) !important;
        box-shadow: var(--shadow-sm) !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    /* INPUT FOCUS STATE - Depth increase on interaction */
    .stTextInput input:focus, .stTextArea textarea:focus {{
        background: #FFFFFF !important;
        border-color: var(--primary) !important;
        box-shadow: 
            var(--shadow-accent-sm),
            0 0 0 3px var(--bg-light) !important;
        outline: none !important;
    }}
    
    /* INPUT HOVER STATE - Subtle depth indicator */
    .stTextInput input:hover, .stTextArea textarea:hover {{
        border-color: var(--primary-light) !important;
        box-shadow: var(--shadow-md) !important;
    }}
    
    /* SELECTBOX - Consistent with input fields */
    .stSelectbox [data-baseweb="select"] {{
        background: #FFFFFF !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 0 16px !important;
        min-height: 50px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: border-color var(--transition-base) !important, box-shadow var(--transition-base) !important;
        color: var(--text-primary) !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    .stSelectbox [data-baseweb="select"]:hover {{
        border-color: var(--primary-light) !important;
        box-shadow: var(--shadow-md) !important;
    }}
    
    .stSelectbox [data-baseweb="select"]:focus {{
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-accent-sm), 0 0 0 3px var(--bg-light) !important;
    }}

    .translator-card {{
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        border-radius: 28px !important;
        padding: 28px !important;
        margin-bottom: 36px !important;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.06) !important;
    }}

    .stTextArea textarea::placeholder {{
        color: rgba(15, 23, 42, 0.45) !important;
    }}
    
    /* DROPDOWN MENU - Light, Grouped Content */
    [data-baseweb="popover"], [role="listbox"], [data-baseweb="menu"] {{
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-xl) !important;
        border-radius: var(--radius-lg) !important;
    }}
    
    [role="option"], [data-baseweb="menu"] li {{
        background: #FFFFFF !important;
        color: var(--text-primary) !important;
        padding: 10px 16px !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.95rem !important;
        transition: all var(--transition-fast) !important;
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    /* OPTION HOVER - Highlight with accent */
    [role="option"]:hover, [data-baseweb="menu"] li:hover {{
        background: var(--bg-light) !important;
        color: var(--primary) !important;
        padding-left: 20px !important;
    }}
    
    /* OPTION SELECTED - Bold and colored */
    [role="option"][aria-selected="true"] {{
        background: var(--bg-lighter) !important;
        color: var(--primary) !important;
        font-weight: 700 !important;
        border-left: 3px solid var(--primary) !important;
        padding-left: 16px !important;
    }}

    /* EXPANDERS - Transparent containers */
    [data-testid="stExpander"] {{
        background: transparent !important;
        border: none !important;
    }}
    
    [data-testid="stExpander"] > div:first-child {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        border: 1.5px solid #D9ECF7 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stExpander"] > div:first-child:hover {{
        background: rgba(255, 255, 255, 0.80) !important;
        border-color: #B0D9F0 !important;
    }}
    
    [data-testid="stExpander"] > div:last-child {{
        background: transparent !important;
        border: none !important;
    }}

    /* RADIO BUTTONS */
    div[data-testid="stRadio"] label div[role="radio"] > div {{
        background-color: var(--accent) !important;
    }}
    
    div[data-testid="stRadio"] label div[role="radio"][aria-checked="true"] {{
        border-color: var(--accent) !important;
    }}

    /* ═══════════════════════════════════════════════════════════════
       CARDS & CONTENT GROUPING - Visual Hierarchy & Scannability
       ═══════════════════════════════════════════════════════════════ */
    
    /* Glass card base styles - consistent depth system */
    .result-card {{
        background: var(--panel) !important;
        border-radius: var(--radius-xl) !important;
        padding: 24px !important;
        border: 1px solid var(--border) !important;
        margin: 16px 0 !important;
        box-shadow: var(--shadow-lg) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        transition: all var(--transition-base) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Card hover state - lift with increased depth */
    .result-card:hover {{
        border-color: var(--primary) !important;
        box-shadow: 
            var(--shadow-xl),
            0 0 20px var(--primary),
            inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-4px) scale(1.005) !important;
    }}

    /* Content Group - For organizing similar items together */
    .content-group {{
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
        margin-bottom: var(--spacing-xl);
    }}
    
    .content-group-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-bottom: var(--spacing-md);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
    }}
    
    .content-group-title::before {{
        content: '';
        width: 4px;
        height: 24px;
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        border-radius: var(--radius-sm);
    }}

    /* BADGES - Consistent with color system */
    .badge {{
        background: linear-gradient(135deg, var(--primary)30, var(--primary)15) !important;
        color: var(--primary) !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        border: 1.5px solid var(--primary)50 !important;
        display: inline-block !important;
        box-shadow: 
            var(--shadow-accent-sm),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(4px) !important;
        transition: all var(--transition-fast) !important;
    }}
    
    .badge:hover {{
        transform: scale(1.05);
        box-shadow: var(--shadow-accent-md), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
    }}

    /* ═══════════════════════════════════════════════════
       CONVERSATION BUBBLES
    ═══════════════════════════════════════════════════ */
    
    .conv-container {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 16px 0;
        max-height: 500px;
        overflow-y: auto;
        scroll-behavior: smooth;
    }}
    
    .bubble {{
        max-width: 80%;
        padding: 14px 16px;
        border-radius: 16px;
        font-size: 0.95rem;
        position: relative;
        line-height: 1.5;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        word-wrap: break-word;
        backdrop-filter: blur(8px) !important;
        transition: all 0.2s ease !important;
    }}
    
    .bubble-left {{
        align-self: flex-start;
        background: linear-gradient(135deg, #B6F4FF 0%, #8DEBFF 100%) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid #A7F3F0 !important;
    }}
    
    .bubble-right {{
        align-self: flex-end;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%) !important;
        color: white !important;
        box-shadow: 
            0 6px 20px var(--accent)40,
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }}
    
    .bubble:hover {{
        transform: translateY(-2px) !important;
    }}
    
    .bubble-info {{
        font-size: 10px;
        opacity: 0.7;
        margin-bottom: 8px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .bubble-trans {{
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid rgba(0,0,0,0.08);
        font-weight: 600;
        font-size: 0.9rem;
    }}
    
    .bubble-right .bubble-trans {{
        border-top: 1px solid rgba(255,255,255,0.2);
    }}
    .roll-container {{
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        padding: 5px 0 20px 0 !important;
        gap: 16px !important;
        scroll-snap-type: x mandatory !important;
        -webkit-overflow-scrolling: touch !important;
    }}
    .roll-container::-webkit-scrollbar {{
        height: 6px !important;
    }}
    .roll-container::-webkit-scrollbar-track {{
        background: rgba(0,0,0,0.05) !important;
        border-radius: 10px !important;
    }}
    .roll-container::-webkit-scrollbar-thumb {{
        background: var(--accent)50 !important;
        border-radius: 10px !important;
    }}
    .roll-item {{
        flex: 0 0 280px !important;
        scroll-snap-align: start !important;
        margin: 0 !important;
    }}

    /* DROPDOWNS & SELECTS — solid white, text from theme */
    .stSelectbox [data-baseweb="select"], .stSelectbox div[role="button"] {{
        background: #FFFFFF !important;
        border: 1px solid #D9ECF7 !important;
        border-radius: 14px !important;
        padding: 8px 12px !important;
        box-shadow: 0 4px 15px rgba(91, 181, 224, 0.08) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    /* ═══════════════════════════════════════════════════
       RECENT DOCS CAROUSEL (SIDEBAR)
    ═══════════════════════════════════════════════════ */
    .recent-doc-card {{
        position: relative;
        background: rgba(255, 255, 255, 0.65) !important;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        border: 1.5px solid #D9ECF7 !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        align-items: center;
        gap: 12px;
        overflow: hidden;
    }}
    
    .recent-doc-card:hover {{
        transform: translateX(8px) scale(1.02);
        border-color: var(--accent) !important;
        box-shadow: 
            -4px 0 0 var(--accent),
            0 10px 25px rgba(0, 0, 0, 0.05);
    }}
    
    .doc-icon-box {{
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 10px;
        flex-shrink: 0;
    }}
    
    .doc-icon-pdf {{ background: #FEE2E2; color: #DC2626; }}
    .doc-icon-img {{ background: #DBEAFE; color: #0284C7; }}
    
    .recent-doc-card .info {{
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }}
    
    .recent-doc-card .name {{
        font-size: 12px;
        font-weight: 700;
        color: var(--text-primary) !important;
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
    }}
    
    .recent-doc-card .meta {{
        font-size: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 2px;
    }}
    
    .lang-pill {{ background: rgba(255, 255, 255, 0.7); color: #2563EB; padding: 2px 6px; border: 1px solid #D9ECF7; border-radius: 4px; font-weight: 800; text-transform: uppercase; }}
    
    /* ═══════════════════════════════════════════════════════════════
       PRIMARY ACTION AREAS - CTA Buttons (Bold & Easy to Find)
       ═══════════════════════════════════════════════════════════════ */
    
    /* Translation Panels - Container for CTAs */
    .translate-panel {{
        background: rgba(255, 255, 255, 0.65) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-xl);
        padding: 28px 24px 20px 24px;
        margin-bottom: 20px;
        box-shadow: var(--shadow-xl);
        transition: all var(--transition-base) !important;
    }}
    
    .translate-panel:hover {{
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-2xl) !important;
    }}
    
    /* CTA BUTTON - Bold, High Contrast, Mobile Tap-Friendly */
    .cta-btn-wrap .stButton button {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        padding: 12px 24px !important;
        border-radius: var(--radius-lg) !important;
        border: none !important;
        box-shadow: var(--shadow-accent-md), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all var(--transition-base) !important;
        min-height: 52px !important;
        letter-spacing: 0.5px !important;
    }}
    
    .cta-btn-wrap .stButton button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 
            var(--shadow-accent-md),
            0 12px 32px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        filter: brightness(1.1) !important;
    }}
    
    .cta-btn-wrap .stButton button:active {{
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-accent-sm), inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }}
    
    .visual-btn-wrap .stButton button {{
        background: var(--bg) !important;
        color: var(--primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        transition: all var(--transition-base) !important;
        min-height: 48px !important;
    }}
    
    .visual-btn-wrap .stButton button:hover {{
        border-color: var(--primary) !important;
        background: var(--bg-light) !important;
        box-shadow: var(--shadow-accent-sm) !important;
    }}

    /* Learning & Activity Styles */
    .game-v2-card {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-2xl) !important;
        padding: 24px !important;
        position: relative;
        box-shadow: var(--shadow-lg) !important;
        transition: all var(--transition-base) !important;
        height: 100%; display: flex; flex-direction: column;
    }}
    .game-v2-card:hover {{ 
        transform: translateY(-8px) !important; 
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-xl) !important; 
    }}
    .game-v2-icon-box {{ 
        width: 64px; 
        height: 64px; 
        border-radius: var(--radius-lg); 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: 32px; 
        margin-bottom: 24px; 
        transition: transform var(--transition-base); 
    }}
    .game-v2-icon-box:hover {{ transform: scale(1.1) rotate(5deg); }}
    .game-v2-title {{ 
        font-size: 20px; 
        font-weight: 800; 
        color: var(--text-primary) !important; 
        margin-bottom: 8px; 
        letter-spacing: -0.5px; 
    }}
    .game-v2-desc {{ 
        font-size: 14px; 
        color: var(--text-secondary) !important; 
        line-height: 1.5; 
        margin-bottom: 24px; 
        min-height: 42px; 
    }}
    .flashcard {{ 
        min-width: 200px; 
        max-width: 200px; 
        background: var(--panel); 
        border: 1.5px solid var(--border); 
        border-radius: var(--radius-lg); 
        padding: 16px; 
        flex-shrink: 0; 
        cursor: pointer; 
        box-shadow: var(--shadow-sm); 
        transition: all var(--transition-base); 
    }}
    .flashcard:hover {{ 
        border-color: var(--primary); 
        box-shadow: var(--shadow-lg); 
        transform: translateY(-4px) scale(1.02); 
    }}

    /* Global Glowy Panel Style */
    .sidebar-card, .result-card {{
        background: rgba(255, 255, 255, 0.65) !important;
        padding: 30px !important;
        border-radius: var(--radius-2xl) !important;
        margin-bottom: 24px !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-xl) !important;
        transition: all var(--transition-slow) !important;
        animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) backwards;
    }}
    .sidebar-card:hover, .result-card:hover {{
        box-shadow: 0 20px 40px var(--glow) !important;
        transform: translateY(-8px) scale(1.02) !important;
        border-color: var(--accent) !important;
    }}

    /* ═══════════════════════════════════════════════════
       ALIGNMENT & SPACING IMPROVEMENTS
    ═══════════════════════════════════════════════════ */

    /* Columns - vertically align children to center */
    [data-testid="column"] {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        gap: 0 !important;
        padding: 0 8px !important;
    }}

    /* First column has no left padding */
    [data-testid="column"]:first-child {{
        padding-left: 0 !important;
    }}

    /* Last column has no right padding */
    [data-testid="column"]:last-child {{
        padding-right: 0 !important;
    }}

    /* Row containers — consistent vertical alignment */
    [data-testid="stHorizontalBlock"] {{
        align-items: flex-end !important;
        gap: 12px !important;
    }}

    /* All Streamlit buttons — uniform sizing and consistent look */
    .stButton {{
        display: flex !important;
        width: 100% !important;
    }}
    .stButton > button {{
        width: 100% !important;
        min-height: 46px !important;
        height: 46px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 12px !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        padding: 0 1.2rem !important;
        letter-spacing: 0.3px !important;
        white-space: nowrap !important;
        box-sizing: border-box !important;
    }}

    /* Inputs and Selects — same height so they line up in rows */
    .stTextInput input,
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] {{
        min-height: 46px !important;
        height: 46px !important;
        box-sizing: border-box !important;
        border-radius: 12px !important;
        padding: 0 14px !important;
        font-size: 0.92rem !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* TextArea — consistent padding */
    .stTextArea textarea {{
        border-radius: 14px !important;
        padding: 14px 16px !important;
        font-size: 0.93rem !important;
        line-height: 1.6 !important;
        resize: vertical !important;
    }}

    /* Widget labels — consistent spacing above inputs */
    [data-testid="stWidgetLabel"] {{
        margin-bottom: 4px !important;
        margin-top: 0 !important;
    }}
    [data-testid="stWidgetLabel"] p {{
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.4px !important;
        text-transform: uppercase !important;
        color: #000000 !important;
        margin: 0 0 4px 0 !important;
    }}

    /* Selectbox arrow and text vertical centering */
    .stSelectbox [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    .stSelectbox [data-baseweb="select"] > div > div {{
        display: flex !important;
        align-items: center !important;
    }}

    /* File uploader — clean and consistent */
    .stFileUploader section, [data-testid="stFileUploadDropzone"] {{
        border-radius: 14px !important;
        padding: 16px 20px !important;
        min-height: 80px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }}

    /* Dividers — subtle */
    hr {{
        border: none !important;
        border-top: 1.5px solid rgba(59, 130, 246, 0.1) !important;
        margin: 20px 0 !important;
    }}

    /* Download button — match button height */
    [data-testid="stDownloadButton"] button {{
        min-height: 46px !important;
        height: 46px !important;
        border-radius: 12px !important;
        font-size: 0.88rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }}

    /* Checkbox alignment */
    [data-testid="stCheckbox"] {{
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}

    /* Radio button alignment */
    [data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        gap: 12px !important;
        flex-wrap: wrap !important;
    }}

    /* Tabs label padding and alignment */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.9) !important;
        padding: 10px 12px !important;
        gap: 16px !important;
        border: 1px solid var(--border) !important;
        border-radius: 999px !important;
        margin-bottom: 26px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        box-shadow: var(--shadow-sm) !important;
    }}

    button[data-baseweb="tab"] {{
        padding: 10px 18px !important;
        border-radius: 999px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        min-width: fit-content !important;
        background: transparent !important;
        color: var(--text-secondary) !important;
        transition: all var(--transition-fast) !important;
        opacity: 0.92 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        background: var(--primary) !important;
        color: #ffffff !important;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18) !important;
        opacity: 1 !important;
    }}

    button[data-baseweb="tab"]:hover {{
        background: rgba(37, 99, 235, 0.08) !important;
        color: var(--text-primary) !important;
        opacity: 1 !important;
    }}

    /* Expander header alignment */
    [data-testid="stExpander"] summary {{
        display: flex !important;
        align-items: center !important;
        padding: 12px 16px !important;
        min-height: 50px !important;
        font-weight: 600 !important;
        font-size: 0.93rem !important;
    }}

    /* st.columns gap standardization */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
        box-sizing: border-box !important;
    }}

    /* Reduce excessive top/bottom spacers Streamlit generates */
    .element-container {{
        margin-bottom: 8px !important;
    }}

    /* Subheader and text spacing */
    h2 {{ margin-top: 24px !important; margin-bottom: 12px !important; }}
    h3 {{ margin-top: 16px !important; margin-bottom: 8px !important; }}

    /* ─── BACKGROUND IMAGE (user-supplied glassmorphism PNG) ─── */
    /* Background is set above in the main .stApp block — no duplicate needed */

    /* Input boxes & textareas — solid white, text from theme */
    .stTextInput input,
    .stSelectbox [data-baseweb="select"],
    .stTextArea textarea {{
        background: #FFFFFF !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        color: var(--text-primary) !important;
        border: 1.5px solid #D9ECF7 !important;
    }}

    /* Dropdown popover — solid white, text from theme */
    [data-baseweb="popover"], [role="listbox"], [data-baseweb="menu"] {{
        background: #FFFFFF !important;
        color: var(--text-primary) !important;
        border: 1px solid #D9ECF7 !important;
    }}
    [role="option"], [data-baseweb="menu"] li {{
        background: #FFFFFF !important;
        color: var(--text-primary) !important;
    }}

    /* Glass cards — semi-transparent white with premium blur */
    [data-testid="stExpander"] > div:first-child,
    .result-card, .sidebar-card, .translate-panel, .game-v2-card, .flashcard {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        color: var(--text-primary) !important;
        border: 1px solid #D9ECF7 !important;
    }}

    /* Text areas — solid white */
    .stTextArea textarea {{
        background: #FFFFFF !important;
        border: 1.5px solid #D9ECF7 !important;
        color: var(--text-primary) !important;
    }}
    .stTextArea textarea:focus {{
        background: #FFFFFF !important;
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(91, 181, 224, 0.2) !important;
    }}

    /* File uploader — light semi-transparent */
    .stFileUploader section, [data-testid="stFileUploadDropzone"] {{
        background: rgba(255, 255, 255, 0.65) !important;
        border: 2px dashed #D9ECF7 !important;
        color: var(--text-primary) !important;
    }}

    /* Compact Dictionary Search Box — solid white */
    .dictionary-search-wrap .stTextInput input {{
        background: #FFFFFF !important;
        border: 1.5px solid #D9ECF7 !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        height: 48px !important;
        box-shadow: none !important;
    }}

    .context-card {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 14px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        border: 1px solid #D9ECF7 !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }}

    .context-card:hover {{
        background: rgba(255, 255, 255, 0.80) !important;
        transform: translateY(-2px);
    }}

    /* Unified Search Bar styling */
    .unified-search-box {{
        display: flex !important;
        align-items: stretch !important;
        background: rgba(255, 255, 255, 0.65) !important;
        border-radius: 16px !important;
        border: 1.5px solid #D9ECF7 !important;
        overflow: hidden !important;
        box-shadow: 0 20px 50px rgba(125,211,252,.15) !important;
        margin-bottom: 30px !important;
    }}

    .unified-search-box [data-testid="column"] {{
        padding: 0 !important;
    }}
    
    .unified-search-box [data-testid="stHorizontalBlock"] {{
        gap: 0 !important;
    }}

    .unified-search-box .stTextInput {{
        flex: 1 !important;
        margin-bottom: 0 !important;
    }}

    .unified-search-box .stTextInput input {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        height: 52px !important;
        padding-left: 20px !important;
    }}

    .unified-search-box .stButton {{
        width: auto !important;
    }}

    .unified-search-box .stButton button {{
        border-radius: 0 !important;
        height: 52px !important;
        border: none !important;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%) !important;
        padding: 0 25px !important;
        font-weight: 800 !important;
        color: white !important;
        margin: 0 !important;
    }}

    .unified-search-box:focus-within {{
        border-color: var(--accent) !important;
        box-shadow: 0 8px 25px rgba(91, 181, 224, 0.20) !important;
        background: rgba(255, 255, 255, 0.65) !important;
    }}

    .dictionary-search-wrap .stTextInput input:focus {{
        border-color: var(--accent) !important;
        background: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(91, 181, 224, 0.22) !important;
    }}

    .dictionary-search-wrap {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    .dict-meaning-card {{
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(10px) !important;
        border-left: 4px solid var(--accent) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        border: 1px solid rgba(120, 190, 230, 0.45);
        border-left-width: 4px !important;
        color: #000000 !important;
        transition: transform 0.3s ease !important;
    }}

    .dict-meaning-card:hover {{
        transform: translateX(10px) !important;
        background: rgba(255, 255, 255, 0.62) !important;
    }}
    /* ─── NEW UI EFFECTS & BLOBS ─── */
    .hero-text {{
        animation: fadeInUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) both;
    }}

    @keyframes fadeInText {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes floatSlightly {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-8px); }}
    }}
    
    .result-card, .sidebar-card, .game-v2-card {{
        animation: floatSlightly 4s ease-in-out infinite !important;
    }}
    
    /* Background Blobs */
    @keyframes slowMoveBlob1 {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        33% {{ transform: translate(40px, -60px) scale(1.1); }}
        66% {{ transform: translate(-30px, 30px) scale(0.9); }}
    }}
    @keyframes slowMoveBlob2 {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        33% {{ transform: translate(-50px, 40px) scale(0.9); }}
        66% {{ transform: translate(30px, -30px) scale(1.1); }}
    }}
    
    .stApp::before {{
        display: none !important;
    }}
    
    .stApp::after {{
        content: '';
        position: fixed;
        bottom: 14%;
        right: 12%;
        width: 420px;
        height: 420px;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.12) 0%, transparent 62%);
        border-radius: 50%;
        filter: blur(44px);
        z-index: -1;
        animation: slowMoveBlob2 18s ease-in-out infinite;
        pointer-events: none;
    }}

    /* ═══════════════════════════════════════════════════════════════
       Z-INDEX LAYERING SYSTEM - Visual Hierarchy & Key Areas
       ═══════════════════════════════════════════════════════════════ */
    
    /* Background layers */
    .stApp {{ z-index: 1; }}
    .stApp::before {{ z-index: 0; }}
    .stApp::after {{ z-index: 0; }}
    
    /* Main content layers */
    [data-testid="stSidebar"] {{ z-index: 100; }}
    [data-testid="stMainBlockContainer"] {{ z-index: 10; }}
    
    /* Elevated components */
    [data-baseweb="popover"], [role="listbox"], [data-baseweb="menu"] {{ z-index: 1000; }}
    [data-testid="stModalBody"] {{ z-index: 1001; }}
    
    /* Floating elements */
    .cta-btn-wrap {{ z-index: 50; }}
    .floating-action {{ z-index: 50; }}
    
    /* Tooltips and popovers */
    [data-testid="stTooltip"] {{ z-index: 999; }}
    
    /* ═══════════════════════════════════════════════════════════════
       ACCESSIBILITY & FOCUS STATES - Better Navigation
       ═══════════════════════════════════════════════════════════════ */
    
    /* Visible focus indicators for keyboard navigation */
    .stButton button:focus {{
        outline: 2px solid var(--primary) !important;
        outline-offset: 2px !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox [data-baseweb="select"]:focus {{
        outline: 2px solid var(--primary) !important;
        outline-offset: 2px !important;
    }}
    
    /* High contrast focus state for accessibility */
    *:focus-visible {{
        outline: 2px solid var(--primary) !important;
        outline-offset: 2px !important;
        border-radius: var(--radius-md) !important;
    }}
    
    /* Skip to content link */
    .skip-to-content {{
        position: absolute;
        top: -40px;
        left: 0;
        background: var(--primary);
        color: white;
        padding: 8px 16px;
        z-index: 100;
        border-radius: var(--radius-md);
    }}
    
    .skip-to-content:focus {{
        top: 0;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       ICON SYSTEM - Consistent Style & Weight
       ═══════════════════════════════════════════════════════════════ */
    
    /* Icon container - ensures consistent size and alignment */
    .icon-container {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: var(--radius-md);
        background: var(--bg-light);
        transition: all var(--transition-fast);
    }}
    
    .icon-container:hover {{
        background: var(--bg-lighter);
        transform: scale(1.1);
    }}
    
    .icon-lg {{
        width: 48px;
        height: 48px;
    }}
    
    .icon-sm {{
        width: 24px;
        height: 24px;
    }}
    
    /* Icon weight consistency */
    .icon, [class*="icon"] {{
        font-weight: 600 !important;
        line-height: 1 !important;
    }}
    
    /* ═══════════════════════════════════════════════════════════════
       SMOOTH TRANSITIONS & ANIMATION UTILITIES
       ═══════════════════════════════════════════════════════════════ */
    
    /* Fade in animation for new content */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    /* Smooth scale animation */
    @keyframes scaleIn {{
        from {{
            opacity: 0;
            transform: scale(0.9);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    /* Utility classes for animations */
    .animate-fade-in {{
        animation: fadeIn var(--transition-base) ease-out !important;
    }}
    
    .animate-scale-in {{
        animation: scaleIn var(--transition-base) ease-out !important;
    }}
    
    .animate-slide-up {{
        animation: slideInUp var(--transition-base) ease-out !important;
    }}

</style>

"""

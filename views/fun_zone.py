import streamlit as st


def render_fun_zone(render_word_games):
    st.session_state.setdefault("fun_zone_confetti", False)

    username = st.session_state.get("username") or "there"
    is_logged_in = bool(st.session_state.get("authenticated"))
    display_name = username if is_logged_in else "guest"
    streak_value = 7 if is_logged_in else 3
    xp_value = 420 if is_logged_in else 180
    xp_target = 600 if is_logged_in else 300
    challenge_count = 6 if is_logged_in else 5

    st.markdown("""
    <style>
        @keyframes float-soft {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        @keyframes drift-glow {
            0%, 100% { transform: translate3d(0,0,0) scale(1); opacity: 0.6; }
            50% { transform: translate3d(10px,-12px,0) scale(1.06); opacity: 0.95; }
        }

        @keyframes float-symbol {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
            50% { transform: translateY(-12px) rotate(6deg); opacity: 1; }
        }

        @keyframes confetti-fall {
            0% { transform: translateY(-20px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(140px) rotate(540deg); opacity: 0; }
        }

        .fun-zone-shell {
            position: relative;
            margin: 6px 0 28px;
            padding: 0;
        }

        .fun-zone-hero-grid {
            display: grid;
            gap: 14px;
            align-items: stretch;
        }

        .fun-zone-ambient {
            position: absolute;
            inset: 0;
            pointer-events: none;
            overflow: hidden;
            border-radius: 28px;
        }

        .fun-zone-blob {
            position: absolute;
            border-radius: 999px;
            filter: blur(46px);
            opacity: 0.55;
            animation: drift-glow 9s ease-in-out infinite;
        }

        .fun-zone-blob.one { width: 180px; height: 180px; left: -30px; top: 10px; background: rgba(59,130,246,0.22); }
        .fun-zone-blob.two { width: 220px; height: 220px; right: -40px; top: -20px; background: rgba(16,185,129,0.16); animation-delay: 1.2s; }
        .fun-zone-blob.three { width: 150px; height: 150px; right: 120px; bottom: -40px; background: rgba(236,72,153,0.14); animation-delay: 2.2s; }

        .fun-zone-symbol {
            position: absolute;
            font-size: 1.15rem;
            color: rgba(37,99,235,0.35);
            animation: float-symbol 5.5s ease-in-out infinite;
            font-weight: 800;
            user-select: none;
        }

        .fun-zone-symbol.a { left: 10%; top: 24%; animation-delay: 0.3s; }
        .fun-zone-symbol.b { right: 18%; top: 34%; animation-delay: 1.1s; }
        .fun-zone-symbol.c { left: 45%; bottom: 15%; animation-delay: 1.6s; }
        .fun-zone-symbol.d { right: 8%; bottom: 20%; animation-delay: 0.8s; }

        .fun-zone-hero {
            position: relative;
            overflow: hidden;
            padding: 32px 32px 28px;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(255,255,255,0.97), rgba(240,247,255,0.95));
            border: 1px solid rgba(37, 99, 235, 0.16);
            box-shadow: 0 18px 44px rgba(15, 23, 42, 0.07);
            margin-bottom: 18px;
        }

        .fun-zone-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top left, rgba(59,130,246,0.12), transparent 42%), radial-gradient(circle at bottom right, rgba(16,185,129,0.12), transparent 36%);
            pointer-events: none;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }

        .fun-zone-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(255,255,255,0.88);
            color: #2563EB;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 10px;
            box-shadow: 0 6px 16px rgba(37,99,235,0.08);
        }

        .fun-zone-kicker .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #12B886;
            box-shadow: 0 0 0 3px rgba(18,184,134,0.16);
        }

        .fun-zone-title {
            font-size: 2.2rem;
            font-weight: 900;
            color: var(--text-primary);
            margin: 0 0 10px;
            letter-spacing: -0.04em;
        }

        .fun-zone-title span {
            color: #2563EB;
        }

        .fun-zone-subtitle {
            font-size: 1rem;
            color: var(--text-secondary);
            margin: 0 auto 14px;
            line-height: 1.7;
            max-width: 780px;
        }

        .fun-zone-cta-row {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 14px;
        }

        .fun-zone-cta {
            padding: 10px 16px;
            border-radius: 999px;
            border: none;
            background: linear-gradient(135deg, #2563EB, #3B82F6);
            color: white;
            font-weight: 800;
            box-shadow: 0 10px 24px rgba(37,99,235,0.16);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        }

        .fun-zone-cta:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 14px 28px rgba(37,99,235,0.24);
        }

        .fun-zone-pill-row {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 14px;
        }

        .fun-zone-pill {
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.78);
            color: #334155;
            font-size: 0.82rem;
            font-weight: 700;
            border: 1px solid rgba(148, 163, 184, 0.22);
        }

        .fun-zone-stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin: 16px 0 8px;
        }

        @media (max-width: 900px) {
            .fun-zone-stats {
                grid-template-columns: 1fr;
            }
        }

        .fun-zone-stat-box {
            padding: 12px 10px;
            border-radius: 16px;
            background: rgba(255,255,255,0.78);
            border: 1px solid rgba(148,163,184,0.16);
            box-shadow: 0 8px 20px rgba(15,23,42,0.04);
            text-align: center;
        }

        .fun-zone-stat-box strong {
            display: block;
            font-size: 1rem;
            color: #0F172A;
            margin-bottom: 3px;
        }

        .fun-zone-stat-box span {
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .fun-zone-card {
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            min-height: 240px;
            padding: 18px 18px 16px;
            border-radius: 20px;
            border: 1px solid rgba(148,163,184,0.18);
            background: linear-gradient(145deg, rgba(255,255,255,0.97), rgba(248,250,252,0.92));
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            animation: float-soft 4.8s ease-in-out infinite;
        }

        .fun-zone-tier-section {
            margin-bottom: 24px;
        }

        .fun-zone-tier-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }

        .fun-zone-tier-title {
            font-size: 1.02rem;
            font-weight: 800;
            color: var(--text-primary);
        }

        .fun-zone-tier-subtitle {
            font-size: 0.84rem;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .fun-zone-card:hover {
            transform: translateY(-6px) scale(1.01);
            box-shadow: 0 16px 38px rgba(37, 99, 235, 0.12);
        }

        .fun-zone-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.45) 50%, transparent 100%);
            transform: translateX(-120%);
            transition: transform 0.7s ease;
            pointer-events: none;
        }

        .fun-zone-card:hover::before {
            transform: translateX(120%);
        }

        .fun-zone-illustration {
            width: 54px;
            height: 54px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            font-size: 1.35rem;
            margin-bottom: 12px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.55);
            animation: float-soft 4.2s ease-in-out infinite;
        }

        .fun-zone-card-body {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
        }

        .fun-zone-title-small {
            font-size: 1.02rem;
            font-weight: 800;
            color: var(--text-primary);
            margin: 0;
        }

        .fun-zone-desc {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin: 0;
            line-height: 1.5;
            min-height: 44px;
        }

        .fun-zone-badges {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: auto;
            margin-bottom: 10px;
        }

        .fun-zone-badges .fun-zone-badge:nth-child(2) {
            background: rgba(255,255,255,0.9);
        }

        .fun-zone-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 5px 9px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 800;
            background: rgba(248,250,252,0.92);
            color: #475569;
            border: 1px solid rgba(148,163,184,0.16);
        }

        .fun-zone-progress {
            height: 7px;
            width: 100%;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(226,232,240,0.9);
            margin: 10px 0 8px;
        }

        .fun-zone-progress > span {
            display: block;
            height: 100%;
            border-radius: inherit;
        }

        .fun-zone-meta {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(248,250,252,0.9);
            color: #475569;
            font-size: 0.8rem;
            font-weight: 700;
            border: 1px solid rgba(148,163,184,0.16);
        }

        .fun-zone-card-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            margin-top: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            color: #475569;
        }

        .fun-zone-card-footer-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(148,163,184,0.16);
        }

        .fun-zone-sticker {
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 1.55rem;
            opacity: 0.16;
            transform: rotate(-12deg);
            animation: drift-glow 5s ease-in-out infinite;
        }

        .fun-zone-card button, .fun-zone-card .stButton > button {
            margin-top: 10px;
            width: 100%;
            border-radius: 999px !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        .fun-zone-card button:hover, .fun-zone-card .stButton > button:hover {
            transform: translateY(-2px) scale(1.01) !important;
        }

        .fun-zone-footer-note {
            text-align: center;
            margin-top: 8px;
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 600;
        }

        .confetti-layer {
            position: relative;
            height: 0;
            overflow: visible;
            pointer-events: none;
        }

        .confetti-piece {
            position: absolute;
            top: 0;
            left: 50%;
            width: 8px;
            height: 14px;
            border-radius: 2px;
            animation: confetti-fall 1.2s ease-out forwards;
            opacity: 0;
        }

        .confetti-piece.one { background: #2563EB; animation-delay: 0s; }
        .confetti-piece.two { background: #38BDF8; animation-delay: 0.06s; }
        .confetti-piece.three { background: #34D399; animation-delay: 0.12s; }
        .confetti-piece.four { background: #F59E0B; animation-delay: 0.18s; }
        .confetti-piece.five { background: #F472B6; animation-delay: 0.24s; }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.fun_zone_confetti:
        st.markdown("""
        <div class="confetti-layer" aria-hidden="true">
            <div class="confetti-piece one"></div>
            <div class="confetti-piece two"></div>
            <div class="confetti-piece three"></div>
            <div class="confetti-piece four"></div>
            <div class="confetti-piece five"></div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.fun_zone_confetti = False

    st.markdown(f"""
    <div class="fun-zone-shell">
        <div class="fun-zone-ambient" aria-hidden="true">
            <div class="fun-zone-blob one"></div>
            <div class="fun-zone-blob two"></div>
            <div class="fun-zone-blob three"></div>
            <div class="fun-zone-symbol a">文</div>
            <div class="fun-zone-symbol b">α</div>
            <div class="fun-zone-symbol c">न</div>
            <div class="fun-zone-symbol d">ß</div>
        </div>
        <div class="fun-zone-hero">
            <div class="hero-content">
                <div class="fun-zone-kicker"><span class="dot"></span>Interactive practice lounge</div>
                <h2 class="fun-zone-title">Welcome back, <span>{display_name}</span><br>ready for your next challenge?</h2>
                <p class="fun-zone-subtitle">A refined game space built to feel energetic and rewarding for {display_name}, while staying polished for the rest of Linguistix.</p>
                <div class="fun-zone-cta-row">
                    <button class="fun-zone-cta" type="button">Explore Games →</button>
                </div>
                <div class="fun-zone-pill-row">
                    <span class="fun-zone-pill">Professional look</span>
                    <span class="fun-zone-pill">Calm color palette</span>
                    <span class="fun-zone-pill">Smooth motion</span>
                </div>
                <div class="fun-zone-stats">
                    <div class="fun-zone-stat-box"><strong>{challenge_count}</strong><span>Challenge modes</span></div>
                    <div class="fun-zone-stat-box"><strong>{xp_value}</strong><span>XP in your streak</span></div>
                    <div class="fun-zone-stat-box"><strong>{streak_value} day</strong><span>Current streak</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

    game_cards = [
        {"id": "word_quest", "icon": "🧠", "label": "Word Quest", "desc": "Vocabulary quiz with quick translation choices", "cta": "🚀 Start Quest", "tier": "Beginner", "accent": "#EF9F27", "accent_bg": "#FFF5E4", "accent_chip": "#FDE7C3", "tag_a": "Quick quiz", "tag_b": "Vocabulary", "progress": 72, "footer": "Warm-up ready"},
        {"id": "picture_match", "icon": "🖼️", "label": "Picture Match", "desc": "Match the image cue to the correct word", "cta": "🖼️ Match", "tier": "Beginner", "accent": "#1D9E75", "accent_bg": "#EAF8F2", "accent_chip": "#D0EEE1", "tag_a": "Visual", "tag_b": "Confidence", "progress": 64, "footer": "First steps"},
        {"id": "lightning_blitz", "icon": "⚡", "label": "Lightning Blitz", "desc": "Beat the clock with rapid-fire prompts", "cta": "⚡ Go Blitz", "tier": "Beginner", "accent": "#D85A30", "accent_bg": "#FCEEE7", "accent_chip": "#F9D7C9", "tag_a": "Speed", "tag_b": "Recall", "progress": 58, "footer": "Fast lane"},
        {"id": "story_master", "icon": "📖", "label": "Story Master", "desc": "Fill the blank with the best context-based word", "cta": "📖 Try Story", "tier": "Intermediate", "accent": "#7F77DD", "accent_bg": "#F2EEFF", "accent_chip": "#D9D3FF", "tag_a": "Reading", "tag_b": "Context", "progress": 81, "footer": "Story flow"},
        {"id": "sentence_scramble", "icon": "🧩", "label": "Sentence Scramble", "desc": "Rebuild the sentence by ordering shuffled chips", "cta": "🧩 Scramble", "tier": "Intermediate", "accent": "#639922", "accent_bg": "#F1F8E8", "accent_chip": "#DDEEC6", "tag_a": "Grammar", "tag_b": "Order", "progress": 77, "footer": "Pattern play"},
        {"id": "listening_ear", "icon": "🎧", "label": "Listening Ear", "desc": "Listen and choose the translation you hear", "cta": "🎧 Listen", "tier": "Intermediate", "accent": "#D4537E", "accent_bg": "#FCECF2", "accent_chip": "#F8D6E2", "tag_a": "Listening", "tag_b": "Audio", "progress": 69, "footer": "Ear training"},
        {"id": "word_detective", "icon": "🕵️", "label": "Word Detective", "desc": "Use clues to solve the hidden word", "cta": "🕵️ Solve", "tier": "Advanced", "accent": "#185FA5", "accent_bg": "#EAF4FC", "accent_chip": "#CFE3F6", "tag_a": "Reasoning", "tag_b": "Clues", "progress": 86, "footer": "Deep dive"},
        {"id": "grammar_gauntlet", "icon": "📝", "label": "Grammar Gauntlet", "desc": "Spot the error and pick the correction", "cta": "📝 Test Grammar", "tier": "Advanced", "accent": "#E24B4A", "accent_bg": "#FDEDED", "accent_chip": "#F8C9C9", "tag_a": "Precision", "tag_b": "Fixes", "progress": 91, "footer": "Master mode"},
    ]

    for tier_name in ["Beginner", "Intermediate", "Advanced"]:
        tier_cards = [card for card in game_cards if card["tier"] == tier_name]
        if not tier_cards:
            continue
        st.markdown(f"""
        <div class="fun-zone-tier-section">
            <div class="fun-zone-tier-heading">
                <div>
                    <div class="fun-zone-tier-title">{tier_name}</div>
                    <div class="fun-zone-tier-subtitle">{len(tier_cards)} focused practice modes</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        for start in range(0, len(tier_cards), 3):
            row_cards = tier_cards[start:start + 3]
            columns = st.columns(3)
            for column, card in zip(columns, row_cards):
                with column:
                    st.markdown(f"""
                    <div class="fun-zone-card" style="border-top: 3px solid {card['accent']}; margin-bottom: 14px;">
                        <div class="fun-zone-card-body">
                            <div class="fun-zone-illustration" style="background: {card['accent_bg']}; color: {card['accent']};">{card['icon']}</div>
                            <div class="fun-zone-title-small">{card['label']}</div>
                            <div class="fun-zone-desc">{card['desc']}</div>
                            <div class="fun-zone-badges">
                                <span class="fun-zone-badge">{card['tag_a']}</span>
                                <span class="fun-zone-badge">{card['tag_b']}</span>
                            </div>
                            <div class="fun-zone-progress"><span style="background: linear-gradient(90deg, {card['accent']}, {card['accent_chip']}); width: {card['progress']}%;"></span></div>
                            <div class="fun-zone-card-footer">
                                <span class="fun-zone-card-footer-chip">📈 {card['progress']}%</span>
                                <span>{card['footer']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(card['cta'], key=f"game_fun_{card['id']}", use_container_width=True):
                        st.session_state.word_games_selected = card['id']
                        st.session_state.fun_zone_confetti = True
                        render_word_games()

    footer_copy = "Keep the streak alive and make today count." if is_logged_in else "Log in to unlock your personal streak and progress history."
    st.markdown(f"<div class='fun-zone-footer-note'>{footer_copy}</div>", unsafe_allow_html=True)

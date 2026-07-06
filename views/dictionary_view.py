import streamlit as st
import random
import datetime
from utils.dictionary import get_word_info
from utils.storage import save_data

def render_dictionary(target_options=None):
    st.markdown("<h3 style='margin-bottom:12px; color:var(--text-primary);'><i class='fas fa-book'></i> Visual Dictionary</h3>", unsafe_allow_html=True)
    
    # 1. Compact Search Box
    st.markdown('<div style="border: 1.5px solid var(--border); background: white; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border-radius: 12px; padding: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
    c_search, c_btn, c_clr = st.columns([4, 1, 1], gap="small")
    with c_search:
        word_input = st.text_input("Search word", placeholder="Search word...", key="dict_search_input", label_visibility="collapsed")
    with c_btn:
        do_search = st.button("🔍 Search", key="dict_search_btn", use_container_width=True, type="primary")
    with c_clr:
        if st.button("🗑️ Clear", key="dict_clear_btn", use_container_width=True):
            st.session_state.dict_results = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    current_search = word_input.strip()
    if do_search and current_search:
        with st.spinner(f"Finding '{current_search}'..."):
            word_info = get_word_info(current_search)
            if word_info:
                st.session_state.dict_results = word_info
            else:
                st.session_state.dict_results = None
                st.error(f"'{current_search}' not found.")

    if st.session_state.dict_results:
        word_info = st.session_state.dict_results
        
        # Header (No Image)
        st.markdown(f"""
        <div style="margin-bottom:20px;">
            <h1 style="margin:0; font-size:56px; font-weight:900; color:var(--text-primary); letter-spacing:-2px; line-height:1;">{word_info['word'].capitalize()}</h1>
            <p style="color:var(--accent); font-size:22px; font-weight:600; margin-top:4px;">/{word_info['phonetic'].strip('/') if word_info['phonetic'] else '---'}/</p>
            <div style="display:flex; gap:8px; margin-top:12px;">
                <span style="background:var(--accent)10; color:var(--accent); padding:4px 10px; border-radius:8px; font-size:10px; font-weight:800; border:1px solid var(--accent)20;">SYNCED</span>
                <span style="background:var(--accent-secondary)10; color:var(--accent-secondary); padding:4px 10px; border-radius:8px; font-size:10px; font-weight:800; border:1px solid var(--accent-secondary)20;">THESAURUS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

        # Definitions & Thesaurus
        def_col, the_col = st.columns([3, 2], gap="medium")

        with def_col:
            for meaning in word_info['meanings']:
                st.markdown(f"""
                <div style="background:white; border:1.5px solid var(--border); border-radius:16px; padding:20px; margin-bottom:16px;">
                    <div style="margin-bottom:12px;"><span style="background:var(--accent); color:white; padding:4px 12px; border-radius:8px; font-size:9px; font-weight:900; text-transform:uppercase;">{meaning['partOfSpeech']}</span></div>
                """, unsafe_allow_html=True)
                for d_idx, d in enumerate(meaning['definitions'][:2]):
                    st.markdown(f"<p style='font-weight:700; font-size:15px; color:#1e293b; margin-bottom:6px;'>{d_idx+1}. {d['definition']}</p>", unsafe_allow_html=True)
                    if d.get('example'):
                        st.markdown(f"<p style='margin:0 0 12px 0; font-style:italic; font-size:13px; color:#64748b; border-left:3px solid var(--accent)50; padding-left:10px;'>“{d['example']}”</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with the_col:
            # Synonyms & Antonyms in smaller cards
            if word_info['synonyms']:
                st.markdown("<div style='background:white; border:1.5px solid var(--border); border-radius:16px; padding:15px; margin-bottom:16px;'>", unsafe_allow_html=True)
                st.markdown("<p style='font-weight:900; color:var(--accent); font-size:11px; margin-bottom:10px;'>SYNONYMS</p>", unsafe_allow_html=True)
                syns_html = "".join([f"<span style='display:inline-block; background:var(--accent)08; color:var(--accent); padding:4px 10px; border-radius:8px; font-size:11px; font-weight:700; margin:3px; border:1px solid var(--accent)15;'>{s}</span>" for s in word_info['synonyms'][:8]])
                st.markdown(f"<div style='display:flex; flex-wrap:wrap;'>{syns_html}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if word_info['antonyms']:
                st.markdown("<div style='background:white; border:1.5px solid var(--border); border-radius:16px; padding:15px; margin-bottom:16px;'>", unsafe_allow_html=True)
                st.markdown("<p style='font-weight:900; color:#f43f5e; font-size:11px; margin-bottom:10px;'>ANTONYMS</p>", unsafe_allow_html=True)
                ants_html = "".join([f"<span style='display:inline-block; background:#fff1f2; color:#f43f5e; padding:4px 10px; border-radius:8px; font-size:11px; font-weight:700; margin:3px; border:1px solid #fecdd3;'>{a}</span>" for a in word_info['antonyms'][:8]])
                st.markdown(f"<div style='display:flex; flex-wrap:wrap;'>{ants_html}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Save to Phrasebook
            st.markdown("<div style='background:var(--accent); border-radius:16px; padding:15px; color:white;'>", unsafe_allow_html=True)
            if st.button("💾 Save to Phrasebook", key="dict_save_btn", use_container_width=True):
                st.session_state.phrasebook.append({
                    "input": word_info['word'], 
                    "output": word_info['meanings'][0]['definitions'][0]['definition'] if word_info['meanings'] and word_info['meanings'][0]['definitions'] else word_info['word'],
                    "lang": "en",
                    "date": datetime.datetime.now().isoformat()
                })
                save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                st.toast("💾 Saved to Phrasebook!")
            st.markdown("</div>", unsafe_allow_html=True)


    # Inspiration section
    st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
    st.divider()
    ins_col1, ins_col2 = st.columns(2, gap="large")
    with ins_col1:
        st.markdown(f"""
        <div class="sidebar-card" style="width:100%; border-top: 6px solid var(--accent); position:relative; overflow:hidden; animation: float 4s ease-in-out infinite;">
            <div style="position:absolute; bottom:-20px; right:-20px; font-size:120px; opacity:0.04; color:var(--accent); pointer-events:none;"><i class="fas fa-book-open"></i></div>
            <div style="position:relative; z-index:1;">
                <p style="font-size:11px; font-weight:800; color:var(--accent); text-transform:uppercase; letter-spacing:2px; margin-bottom:16px; display:flex; align-items:center; gap:8px;">
                    <i class="fas fa-sparkles" style="animation: spin 3s linear infinite;"></i> Word of the Day
                </p>
                <h3 style="margin:0; color:var(--text-primary); font-size:36px; font-weight:900; font-family:'Outfit', sans-serif; letter-spacing:-1.5px;">{st.session_state.wotd['word']}</h3>
                <p style="font-size:15px; margin-top:10px; color:var(--text-secondary); font-weight:600;">{st.session_state.wotd['meaning']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with ins_col2:
        st.markdown(f"""
        <div class="sidebar-card" style="width:100%; border-top: 6px solid var(--accent-secondary); position:relative; overflow:hidden; animation: float 5s ease-in-out infinite;">
            <div style="position:absolute; top:-20px; left:-20px; font-size:120px; opacity:0.04; color:var(--accent-secondary); pointer-events:none;"><i class="fas fa-quote-right"></i></div>
            <div style="position:relative; z-index:1;">
                <p style="font-size:11px; font-weight:800; color:var(--accent-secondary); text-transform:uppercase; letter-spacing:2px; margin-bottom:16px; display:flex; align-items:center; gap:8px;">
                    <i class="fas fa-lightbulb"></i> Daily Wisdom
                </p>
                <p style="font-size:20px; font-style:italic; margin:0; color:var(--text-primary); font-weight:600;">“{st.session_state.quote.split('—')[0].strip()}”</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

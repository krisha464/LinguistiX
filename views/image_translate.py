import streamlit as st
import datetime
import io
from utils.ocr_logic import extract_text_from_image, translate_image_content
from utils.translator import detect_and_translate, SUPPORTED_LANGS
from utils.storage import save_data
from utils.speech import text_to_speech

def render_image_translate(target_options, create_pdf):
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="result-card" style="text-align:center; padding: 40px 20px;">
            <h2 style="color:var(--accent) !important; margin-bottom:10px;"><i class="fas fa-crown"></i> Go Pro</h2>
            <p style="font-size:1.1rem; opacity:0.9;">Professional translation tools for images are reserved for members.</p>
            <div style="margin: 25px 0; text-align:left; display:inline-block; border-left: 2px solid var(--border); padding-left: 20px;">
                <p style="margin-bottom:8px;"><i class="fas fa-check-circle" style="color:var(--state-success);"></i> <b>Instant OCR</b> - Read text from signs and photos</p>
                <p style="margin-bottom:8px;"><i class="fas fa-check-circle" style="color:var(--state-success);"></i> <b>AI Refinement</b> - Polish extracted text with GPT power</p>
                <p style="margin-bottom:8px;"><i class="fas fa-check-circle" style="color:var(--state-success);"></i> <b>Persistent History</b> - Access your captures later</p>
            </div>
            <p style="font-weight:600; color:var(--text-secondary) !important;">Use the button in the top-right corner to unlock!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Unlock Instant OCR", width='stretch', key='unlock_ocr_btn'):
            st.session_state.page = "auth"
            st.rerun()
    else:
        st.markdown("<p style='font-size:0.9rem; opacity:0.7; margin-top:-8px;'>Capture and translate text from any image — signs, menus, documents, or photos.</p>", unsafe_allow_html=True)
        st.markdown('<div class="translate-panel">', unsafe_allow_html=True)
        uploaded_image = st.file_uploader("📂 Upload an image (JPG, PNG)", type=['jpg', 'jpeg', 'png'], key="ocr_upload")

        if uploaded_image:
            st.image(uploaded_image, caption=f"📸  {uploaded_image.name}", width='stretch')
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

            # Improved Controls Layout
            st.markdown("<p style='font-size:11px; font-weight:800; color:#94A3B8; margin-bottom:8px;'>TRANSLATION OPTIONS</p>", unsafe_allow_html=True)
            
            ctrl_row = st.columns([2, 1.2, 1.2], gap="medium")
            with ctrl_row[0]:
                st.markdown("<p style='font-size:10px; font-weight:700; color:var(--text-primary); margin-bottom:6px;'>Target Language</p>", unsafe_allow_html=True)
                img_tgt = st.selectbox("Select target language", options=target_options, format_func=lambda x: SUPPORTED_LANGS[x], key="img_lang_select", label_visibility="collapsed")
            with ctrl_row[1]:
                st.markdown("<p style='font-size:10px; font-weight:700; color:var(--text-primary); margin-bottom:6px;'>Extract & Translate</p>", unsafe_allow_html=True)
                ocr_clicked = st.button("🚀 Translate", key="ocr_main_btn", type="primary", use_container_width=True)
            with ctrl_row[2]:
                st.markdown("<p style='font-size:10px; font-weight:700; color:var(--text-primary); margin-bottom:6px;'>Visual Redraw</p>", unsafe_allow_html=True)
                visual_clicked = st.button("🖼️ Redraw", key="visual_tr_btn", help="Redraw image with translated text", use_container_width=True)

            if ocr_clicked:
                with st.spinner("🔍 Reading and translating..."):
                    raw_text = extract_text_from_image(uploaded_image)
                    if raw_text and raw_text.startswith("ERROR:"):
                        st.error(raw_text.replace("ERROR:", ""))
                    elif raw_text and raw_text != "No readable text found.":
                        translation, detected = detect_and_translate(raw_text, img_tgt, "auto")
                        st.session_state.ocr_result = translation
                        st.session_state.ocr_detected = detected
                        st.session_state.ocr_raw = raw_text
                        st.session_state.history.append({
                            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                            "src": f"📸 {SUPPORTED_LANGS.get(detected, detected)}",
                            "tgt": SUPPORTED_LANGS[img_tgt],
                            "input": raw_text[:30] + "...",
                            "output": translation,
                            "filename": uploaded_image.name,
                            "type": "image"
                        })
                        save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                        st.rerun()
                    else:
                        st.warning("No readable text was found in this image.")

            if visual_clicked:
                with st.spinner("🎨 Redrawing image with translated text..."):
                    translated_img, err = translate_image_content(uploaded_image, img_tgt, detect_and_translate)
                    if err:
                        st.error(f"Visual translation failed: {err}")
                    else:
                        st.session_state.visual_ocr_img = translated_img
                        st.success("Image translated visually!", icon="🎨")

        st.markdown('</div>', unsafe_allow_html=True)

        # Visual OCR Display
        if st.session_state.visual_ocr_img:
            st.markdown("""
            <div style="margin-top:20px;">
                <h3 style="color:var(--accent); margin-bottom:12px;">🎨 Translated Image</h3>
            </div>
            """, unsafe_allow_html=True)
            st.image(st.session_state.visual_ocr_img, caption="Visual Translation Result", width="stretch")
            
            st.markdown("<p style='font-size:11px; font-weight:800; color:#94A3B8; margin:16px 0 12px 0;'>DOWNLOAD OPTIONS</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                buf = io.BytesIO()
                st.session_state.visual_ocr_img.save(buf, format="PNG")
                st.download_button("📥 Download PNG", data=buf.getvalue(), file_name="translated_image.png", mime="image/png", use_container_width=True)
            with col2:
                if st.button("🗑️ Clear", key="clear_visual", use_container_width=True):
                    st.session_state.visual_ocr_img = None
                    st.rerun()

        # Persisted OCR Result
        if st.session_state.ocr_result:
            translation = st.session_state.ocr_result
            detected = st.session_state.ocr_detected
            raw_text = st.session_state.ocr_raw
            img_tgt_display = st.session_state.get('img_lang_select', target_options[0] if target_options else 'es')

            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                    <h3 style="margin:0; color:var(--accent) !important; font-size:1.3rem;">📸 Image Translation</h3>
                    <span class="badge" style="background:var(--accent)15; color:var(--accent); padding:6px 12px; border-radius:8px; font-size:11px; font-weight:800; border:1px solid var(--accent)30;">
                        {detected.upper() if detected else 'OCR'} → {img_tgt_display.upper()}
                    </span>
                </div>
                <p style="font-size:12px; margin:10px 0; color:var(--text-secondary); font-style:italic; padding:8px; background:var(--bg); border-radius:6px; border-left:3px solid var(--accent);">
                    <strong>Extracted:</strong> {raw_text[:100]}...
                </p>
                <hr style="opacity:0.1; margin: 16px 0;">
                <div style="background:rgba(255,255,255,0.3); padding:16px; border-radius:8px; border-left:4px solid var(--accent);">
                    <p style="font-size: 1.05rem; line-height: 1.7; margin:0; color:var(--text-primary);">{translation}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons with better alignment
            st.markdown("<p style='font-size:11px; font-weight:800; color:#94A3B8; margin:20px 0 12px 0;'>ACTIONS</p>", unsafe_allow_html=True)
            act_img = st.columns(4, gap="medium")
            with act_img[0]:
                if st.button("🔊 Listen", key="img_pron_btn", use_container_width=True):
                    audio_bytes = text_to_speech(translation, img_tgt_display)
                    if audio_bytes:
                        st.session_state.audio_to_play = audio_bytes
                        st.rerun()
            with act_img[1]:
                if st.button("⭐ Favorite", key="img_star", use_container_width=True):
                    st.session_state.favorites.append({"input": f"Image OCR: {raw_text[:30]}...", "output": translation})
                    save_data(st.session_state.history, st.session_state.favorites, st.session_state.phrasebook, username=st.session_state.username)
                    st.toast("✅ Saved to favorites!")
            with act_img[2]:
                pdf_data = create_pdf(translation)
                st.download_button("📄 PDF", data=pdf_data, file_name="image_tr.pdf", use_container_width=True)
            with act_img[3]:
                st.download_button("📝 TXT", data=translation, file_name="linguistix_tr.txt", use_container_width=True)

            if 'refined_output_img' in st.session_state and st.session_state.refined_output_img:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(168, 85, 247, 0.1)); border: 1.5px solid var(--accent)30; padding:16px; border-radius:12px; margin:16px 0;">
                    <p style="font-size:11px; font-weight:800; color:var(--accent); text-transform:uppercase; margin-bottom:8px;">✨ AI Refined Version</p>
                    <p style="font-size:14px; color:var(--text-primary); margin:0; line-height:1.6;">{st.session_state.refined_output_img}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("✅ Use Refined", key="use_refined_img", use_container_width=True):
                    st.session_state.ocr_result = st.session_state.refined_output_img
                    del st.session_state.refined_output_img
                    st.rerun()
            
            if st.button("🗑️ Clear Result", key="img_clear_final", use_container_width=True):
                st.session_state.ocr_result = None
                st.rerun()
        else:
            st.markdown("""
            <div style='background:var(--panel); border:1.5px dashed var(--border); border-radius:20px; padding:80px 40px; text-align:center;'>
                <div style='font-size:3rem; margin-bottom:16px;'>📸</div>
                <h3 style='color:var(--text-primary) !important; margin:0 0 8px 0; font-size:1.2rem;'>No Translation Yet</h3>
                <p style='font-size:14px; opacity:0.7; margin:0;'>Upload an image to extract and translate text instantly</p>
            </div>
            """, unsafe_allow_html=True)

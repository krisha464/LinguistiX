import io

import streamlit as st

try:
    from gtts import gTTS
except Exception:  # pragma: no cover - exercised when dependency is absent
    gTTS = None


@st.cache_data(show_spinner=False)
def text_to_speech(text, lang='en'):
    """
    Converts text to speech and returns the audio bytes.
    """
    try:
        if not text.strip():
            return None

        if gTTS is None:
            return None

        # gTTS uses slightly different lang codes sometimes, 
        # but for core langs like 'en', 'es', 'fr' etc it matches.
        # We'll normalize zh-CN to zh
        tts_lang = lang.split('-')[0]

        tts = gTTS(text=text, lang=tts_lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

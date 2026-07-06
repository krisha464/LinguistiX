import streamlit as st
from utils.nlp_advanced import analyze_sentiment, detect_intent, extract_entities


def render_nlp_analyzer():
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <h3 style='margin:0; color:var(--accent);'>🧠 NLP Analyzer</h3>
        <p style='margin:6px 0 0; color:var(--text-secondary);'>Quickly inspect sentiment, intent, and named entities in text.</p>
    </div>
    """, unsafe_allow_html=True)

    text_input = st.text_area(
        "Analyze text",
        placeholder="Type a sentence or paragraph to inspect...",
        height=160,
        key="nlp_analyzer_input",
    )

    if text_input.strip():
        sentiment = analyze_sentiment(text_input)
        intent = detect_intent(text_input)
        entities = extract_entities(text_input)

        st.markdown("### Insights")
        cols = st.columns(3)
        with cols[0]:
            st.metric("Sentiment", sentiment["sentiment"], delta=None)
        with cols[1]:
            st.metric("Intent", intent["primary_intent"].title(), delta=None)
        with cols[2]:
            st.metric("Entities", entities["entity_count"], delta=None)

        st.markdown("### Details")
        st.write(f"**Sentiment score:** {sentiment['score']:.2f}")
        st.write(f"**Intent confidence:** {intent['confidence']:.2f}")

        if entities["entity_count"] > 0:
            st.write("**Entities:**")
            st.write(entities["by_label"])
        else:
            st.info("No entities detected.")
    else:
        st.info("Enter some text to analyze it.")

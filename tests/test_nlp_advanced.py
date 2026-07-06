from utils.nlp_advanced import (
    analyze_sentiment,
    check_grammar,
    correct_spelling,
    detect_intent,
    extract_entities,
)


def test_nlp_helpers_return_expected_shapes():
    grammar_result = check_grammar("I am go to school yesterday")
    assert grammar_result["error_count"] >= 1
    assert isinstance(grammar_result["suggestions"], list)

    spelling_result = correct_spelling("teh")
    assert spelling_result["is_corrected"] is True

    sentiment_result = analyze_sentiment("I love this app")
    assert sentiment_result["sentiment"] in {"POSITIVE", "NEGATIVE", "NEUTRAL"}

    intent_result = detect_intent("Can you help me with this?")
    assert intent_result["primary_intent"] in {
        "greeting",
        "question",
        "request",
        "statement",
        "gratitude",
    }

    entity_result = extract_entities("Barack Obama visited Paris in 2024")
    assert entity_result["entity_count"] >= 2

from views.nlp_analyzer import render_nlp_analyzer


def test_nlp_analyzer_view_is_available():
    assert callable(render_nlp_analyzer)

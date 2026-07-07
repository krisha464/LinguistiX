from views.games import GAME_LIBRARY


def test_game_library_contains_all_requested_modes():
    game_ids = {game["id"] for game in GAME_LIBRARY}

    expected_ids = {
        "word_quest",
        "story_master",
        "lightning_blitz",
        "word_detective",
        "sentence_scramble",
        "listening_ear",
        "grammar_gauntlet",
        "picture_match",
    }

    assert game_ids == expected_ids
    assert all("label" in game and "description" in game for game in GAME_LIBRARY)


def test_games_are_grouped_by_skill_level():
    levels = {game["id"]: game["level"] for game in GAME_LIBRARY}

    assert levels["word_quest"] == "beginner"
    assert levels["story_master"] == "intermediate"
    assert levels["word_detective"] == "advanced"
    assert levels["picture_match"] == "beginner"

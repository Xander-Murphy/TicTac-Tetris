from elements.eventManager import EventManager


def test_quit_game_calls_every_listener_in_order(quit_calls):
    EventManager.onQuitGame.append(lambda: quit_calls.append("second"))
    EventManager.quitGame()
    assert quit_calls == ["quit", "second"]

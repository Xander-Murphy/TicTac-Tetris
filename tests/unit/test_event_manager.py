from elements.eventManager import EventManager


def test_quit_game_calls_every_listener_in_order(quit_calls):
    EventManager.onQuitGame.append(lambda: quit_calls.append("second"))
    EventManager.quitGame()
    assert quit_calls == ["quit", "second"]


def test_quit_game_with_no_listeners_does_nothing():
    EventManager.quitGame()  # must not raise


def test_change_scene_passes_both_scenes_to_every_listener(scene_changes):
    others = []
    EventManager.onSceneChange.append(lambda current, nxt: others.append(nxt))
    EventManager.changeScene("startScene", "missionTestScene")
    assert scene_changes == [("startScene", "missionTestScene")]
    assert others == ["missionTestScene"]


def test_change_scene_with_no_listeners_does_nothing():
    EventManager.changeScene("startScene", "testScene")  # must not raise

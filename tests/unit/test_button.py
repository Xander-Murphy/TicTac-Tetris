import pygame
import pytest

from elements.UI.button import Button, ImageButton
from elements.scenes.startScene import highlight


@pytest.fixture
def mouse(monkeypatch):
    state = {"pos": (0, 0), "down": False}
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: state["pos"])
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda *a: (state["down"], False, False))
    return state


@pytest.mark.parametrize("pos, down, clicked", [
    ((25, 40), True, True),     # inside, pressed
    ((40, 60), True, True),     # on the bottom-right edge
    ((25, 40), False, False),   # inside, not pressed
    ((41, 40), True, False),    # just outside, pressed
])
def test_button_is_clicked_only_when_pressed_over_it(screen, mouse, pos, down, clicked):
    button = Button(10, 20, 30, 40, screen, "red")  # x 10..40, y 20..60
    mouse["pos"], mouse["down"] = pos, down
    assert button.is_clicked() is clicked


def test_image_button_scales_image_and_click_area(screen, mouse):
    button = ImageButton(50, 60, pygame.Surface((4, 3)), screen, scale=2)
    assert button.image.get_size() == (8, 6)
    assert button.collisionBox == pygame.Rect(50, 60, 8, 6)


def test_highlight_draws_two_pixel_red_border(screen):
    button = ImageButton(10, 20, pygame.Surface((6, 6)), screen)
    screen.fill("black")

    highlight(button)

    assert screen.get_at((10, 20)) == pygame.Color("red")
    assert screen.get_at((11, 21)) == pygame.Color("red")
    assert screen.get_at((12, 22)) == pygame.Color("black")

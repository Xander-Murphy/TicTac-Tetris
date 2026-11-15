"""Unit tests for UI/textures.py - tile colors and drawing a cell."""

import pygame
import pytest

from elements.UI.textures import Texture
from elements.gameLogic.piece import PIECE_COLORS


def test_empty_tile_is_gray():
    assert Texture.getTileTexture(0) == (128, 128, 128)


def test_every_piece_color_has_a_texture():
    for color in PIECE_COLORS.values():
        assert len(Texture.getTileTexture(color)) == 3


def test_piece_textures_are_all_different():
    textures = [Texture.getTileTexture(color) for color in PIECE_COLORS.values()]
    assert len(set(textures)) == len(textures)


def test_unknown_texture_index_raises():
    with pytest.raises(IndexError):
        Texture.getTileTexture(8)


def test_set_cell_texture_fills_inside_a_one_pixel_border():
    surface = pygame.Surface((10, 10))
    surface.fill((0, 0, 0))
    Texture.setCellTexture(surface, 4)
    assert surface.get_at((5, 5))[:3] == Texture.getTileTexture(4)
    assert surface.get_at((0, 0))[:3] == (0, 0, 0)  # border left alone

import pygame
from .scene import Scene
from ..gameLogic.game import Game
from ..UI.gameUI import UIMenu


class TestScene(Scene):
    def __init__(self, screen: pygame.Surface, name: str = "TestScene"):
        super().__init__(screen, name)

    def enter(self):
        self.counter : int = 0
        self.game = Game(20, 10)
        self.ui = UIMenu(self.SCREEN)
        self.FPS = 25
    
    def update(self):
        self.counter += 1

        if self.counter > 100000:
            self.counter = 0

        if self.game.state == "start" and (self.counter % (self.FPS // 2) == 0 or self.ui.pressing_down):
            self.game.soft_drop()

        self.ui.handle_input(self.game)

        if self.game.state == "start":
            self.ui.draw_board(self.game.board)
            self.ui.draw_piece(self.game.current_piece)

        self.ui.draw_hud(self.game.score, self.game.high_score)

        if self.game.state == "gameover":
            self.ui.draw_game_over_screen()

    def exit(self):
        pass

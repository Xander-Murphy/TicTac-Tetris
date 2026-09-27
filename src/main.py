import pygame

from game import Game
from ui import UIMenu

SIZE = (400, 500)
FPS = 25


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    game = Game(20, 10)
    ui = UIMenu(screen)

    counter = 0
    done = False
    while not done:
        counter += 1
        if counter > 100000:
            counter = 0

        if game.state == "start" and (counter % (FPS // 2) == 0 or ui.pressing_down):
            game.soft_drop()

        if ui.handle_input(game):
            done = True

        if game.state == "start":
            ui.draw_board(game.board)
            ui.draw_piece(game.current_piece)

        ui.draw_hud(game.score, game.high_score)

        if game.state == "gameover":
            ui.draw_game_over_screen()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

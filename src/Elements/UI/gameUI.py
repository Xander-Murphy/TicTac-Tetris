"""
UIMenu is the only file in this project that imports pygame. It knows
how to draw a Board/Piece/HUD and how to translate pygame events into
calls on a Game object - it does not make any gameplay decisions
itself. That split is what makes Board/Piece/Game testable without a
display attached.
"""

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

Colors = (
    (0, 0, 0),
    (241, 239, 47),
    (136, 44, 237),
    (138, 234, 40),
    (207, 54, 22),
    (0, 0, 240),
    (221, 164, 34),
    (0, 240, 240),
)


class UIMenu:
    def __init__(self, screen, start_x=100, start_y=60, zoom=20):
        self.screen = screen
        self.start_x = start_x
        self.start_y = start_y
        self.zoom = zoom
        self.font = pygame.font.SysFont("Calibri", 25, True, False)
        self.pressing_down = False  # tracked here since it's input state, not game state

    # -- Drawing -----------------------------------------------------

    def draw_board(self, board):
        self.screen.fill(WHITE)
        x, y, zoom = self.start_x, self.start_y, self.zoom
        for i in range(board.height):
            for j in range(board.width):
                pygame.draw.rect(
                    self.screen, GRAY, [x + zoom * j, y + zoom * i, zoom, zoom], 1
                )
                if board.is_cell_occupied(i, j):
                    pygame.draw.rect(
                        self.screen,
                        Colors[board.grid[i][j]],
                        [x + zoom * j + 1, y + zoom * i + 1, zoom - 2, zoom - 1],
                    )

    def draw_piece(self, piece):
        x, y, zoom = self.start_x, self.start_y, self.zoom
        for i in range(4):
            for j in range(4):
                if i * 4 + j in piece.image():
                    pygame.draw.rect(
                        self.screen,
                        Colors[piece.color],
                        [
                            x + zoom * (piece.x + j) + 1,
                            y + zoom * (piece.y + i) + 1,
                            zoom - 2,
                            zoom - 2,
                        ],
                    )

    def draw_hud(self, score, high_score):
        text = self.font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(text, [0, 0])
        text_hi = self.font.render(f"High Score: {high_score}", True, BLACK)
        self.screen.blit(text_hi, [0, 24])

    def draw_game_over_screen(self):
        lines = [
            "Press Q to quit",
            "Press S for endless mode",
            "Press M for mission mode",
        ]
        for offset, line in enumerate(lines):
            text = self.font.render(line, True, (255, 215, 0))
            self.screen.blit(text, [25, 265 + offset * 35])

    # -- Input ---------------------------------------------------------

    def handle_input(self, game):
        """
        Reads pygame events and calls the matching Game method.
        Returns True if the player asked to quit the program entirely.
        """
        quit_requested = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_requested = True

            if event.type == pygame.KEYDOWN:
                if game.state == "start":
                    quit_requested |= self._handle_playing_key(event, game)
                elif game.state == "gameover":
                    quit_requested |= self._handle_end_screen_key(event, game)

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.pressing_down = False

        return quit_requested

    def _handle_playing_key(self, event, game):
        if event.key == pygame.K_UP:
            game.rotate_current_piece()
        elif event.key == pygame.K_LEFT:
            game.move_left()
        elif event.key == pygame.K_RIGHT:
            game.move_right()
        elif event.key == pygame.K_SPACE:
            game.hard_drop()
        elif event.key == pygame.K_DOWN:
            self.pressing_down = True
        return False

    def _handle_end_screen_key(self, event, game):
        if event.key == pygame.K_q:
            return True
        elif event.key == pygame.K_s:
            game.reset(20, 10, is_mission=False)
            self.pressing_down = False
        elif event.key == pygame.K_m:
            game.reset(20, 10, is_mission=True)
            self.pressing_down = False
        return False

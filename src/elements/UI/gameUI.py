"""
UIMenu is the only file in this project that imports pygame. It knows
how to draw a Board/Piece/HUD and how to translate pygame events into
calls on a Game object - it does not make any gameplay decisions
itself. That split is what makes Board/Piece/Game testable without a
display attached.
"""

import pygame
from ..eventManager import EventManager
from ..gameLogic.game import Game
from ..gameLogic.cell import Cell
from ..gameLogic.board import Board
from ..config import Config
from .textures import Texture

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

Colors = (
    (0, 0, 0),        # White
    (241, 239, 47),   # Yellow
    (136, 44, 237),   # Purple
    (138, 234, 40),   # Green
    (207, 54, 22),    # Red
    (0, 0, 240),      # Blue
    (221, 164, 34),   # Orange
    (0, 240, 240),    # Cyan
)


class GameUI:
    def __init__(self, screen, board_size=(200,500), score_data_size=(100,50)):
        self.screen = screen
        self.font = pygame.font.SysFont("Calibri", 25, True, False)
        self.pressing_down = False  # tracked here since it's input state, not game state
        self.UI_surface = pygame.Surface(Config.SCREEN_SIZE)
        self.board_surface : pygame.Surface = pygame.Surface(board_size)
        self.score_surface : pygame.surface = pygame.Surface(score_data_size)

    # -- Drawing -----------------------------------------------------

    def create_board_cell_surfaces(self, board : Board, cell_size : int):
        cell_dimentions = (cell_size, cell_size)
        cells = []

        for row in range(board.height):
            cell_row = []
            
            for col in range(board.width):
                board_cell = pygame.Surface(cell_dimentions)
                cell_row.append(board_cell)
            
            cells.append(cell_row)
        
        return cells

    
    def draw_board(self, board : Board):
        board_surface = self.board_surface
        board_size = board_surface.get_size()
        cell_size = board_size // board.width
        cell_surfaces = self.create_board_cell_surfaces(board, cell_size)

        # Background of board
        board_surface.fill(WHITE)
        
        # Center the board
        x = (Config.SCREEN_SIZE[0] // 2) - (board_size[0] // 2)
        y = (Config.SCREEN_SIZE[1] // 2) - (board_size[1] // 2)

        # Draw lines
        # Draw vertical lines
        for col in range(1, board.width):
            line_x = col * cell_size
            pygame.draw.line(
                board_surface,
                BLACK,
                (line_x, 0),
                (line_x, board_size[1]),
                2
            )

        # Draw horizontal lines
        for row in range(1, board.height):
            line_y = row * cell_size
            pygame.draw.line(
                board_surface,
                BLACK,
                (0, line_y),
                (board_size[0], line_y),
                2
            )

        # Draw Cells
        for row_index, row in enumerate(cell_surfaces):
            for col_index, cell_surface in enumerate(row):
                
                # Get the texture value from the cell on the board
                board_cell : Cell = board.get_cell(row_index, col_index)
                cell_texture_value = board_cell.tileTexture
                
                # Get the drawn surface from the value
                cell_surface = Texture.getCellTexture(cell_surface, cell_texture_value)
                
                # Put the cell surface on the board surface
                board_surface.blit(cell_surface, (col_index*cell_size, row_index*cell_size))
        

    
        
    
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
            "Press R to restart",
            "Press M to go back to main menu",
        ]
        for offset, line in enumerate(lines):
            text = self.font.render(line, True, (255, 215, 0))
            self.screen.blit(text, [25, 265 + offset * 35])

    # -- Input ---------------------------------------------------------

    def handle_input(self, game, scene="errorScene"):
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
                    quit_requested |= self._handle_end_screen_key(event, game, scene)

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.pressing_down = False

        if quit_requested:
            EventManager.quitGame()

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

    def _handle_end_screen_key(self, event, game : Game, scene="errorScene"):
        if event.key == pygame.K_q:
            return True
        elif event.key == pygame.K_r:
            is_mission = game.is_mission
            game.reset(20, 10, is_mission)
            self.pressing_down = False
        elif event.key == pygame.K_m:
            EventManager.changeScene(scene, "startScene")
            self.pressing_down = False
        return False

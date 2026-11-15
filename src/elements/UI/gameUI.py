"""
UIMenu is the only file in this project that imports pygame. It knows
how to draw a Board/Piece/HUD and how to translate pygame events into
calls on a Game object - it does not make any gameplay decisions
itself. That split is what makes Board/Piece/Game testable without a
display attached.
"""

# Think about text class for handling rendered text

import pygame
from ..eventManager import EventManager
from ..gameLogic.game import Game
from ..gameLogic.cell import Cell
from ..gameLogic.board import Board
from ..config import Config
from ..missionData.mission_data import MISSION_BOARDS
from .textures import Texture
from .dataDisplay import DataDisplay

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

class GameUI:
    def __init__(self, screen, cell_size = 30,score_data_size=(100,50)):
        self.screen : pygame.Surface = screen
        self.font = pygame.font.SysFont("Calibri", 25, True, False)
        self.pressing_down = False  # tracked here since it's input state, not game state
        self.UI_surface = pygame.Surface(Config.SCREEN_SIZE)
        self.cell_size = cell_size
        self.is_board_initialized = False
        self.score_data_size = score_data_size
        self.is_data_displays_initialized = False
        self.mission_selected = 0  # which mission layout R restarts with

    # -- Drawing -----------------------------------------------------

    def update_UI(self, board : Board, piece, score, high_score, goal_row=None):
        self.UI_surface.fill(WHITE)
        self.draw_board(board, goal_row)
        self.draw_piece(piece, board)
        self.draw_hud(score, high_score)
    
    def initialize_board(self, board : Board):
        self.board_size = (
            self.cell_size * board.width,
            self.cell_size * board.height,
        )
        self.board_position = (
            (Config.SCREEN_SIZE[0] - self.board_size[0]) // 2,
            (Config.SCREEN_SIZE[1] - self.board_size[1]) // 2,
        )
        self.board_surface : pygame.Surface = pygame.Surface(self.board_size)
        self.is_board_initialized = True
        self.initialize_data_displays()

    def initialize_data_displays(self):
        score_size = (
            max(self.score_data_size[0], self.screen.get_width()),
            self.score_data_size[1],
        )
        self.score_data_display = DataDisplay(score_size, (0, 0))

        next_piece_size = self.board_size[1] // 3
        self.next_piece_data_display = DataDisplay(
            (next_piece_size, next_piece_size),
            (
                self.board_position[0] + self.board_size[0] + self.cell_size,
                self.board_position[1],
            ),
        )
        self.is_data_displays_initialized = True
    
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

    def draw_board(self, board : Board, goal_row=None):
        if not self.is_board_initialized:
            self.initialize_board(board)

        board_surface = self.board_surface
        board_size = board_surface.get_size()
        cell_size = self.cell_size
        cell_surfaces = self.create_board_cell_surfaces(board, cell_size)

        # Background of board
        board_surface.fill(WHITE)
        
        # Draw lines
        # Draw vertical lines
        for col in range(1, board.width):
            line_x = col * cell_size
            pygame.draw.line(
                board_surface,
                BLACK,
                (line_x, 0),
                (line_x, board_size[1]),
                1
            )

        # Draw horizontal lines
        for row in range(1, board.height):
            line_y = row * cell_size
            pygame.draw.line(
                board_surface,
                BLACK,
                (0, line_y),
                (board_size[0], line_y),
                1
            )

        # Draw Cells
        for row_index, row in enumerate(cell_surfaces):
            for col_index, cell_surface in enumerate(row):
                
                # Get the texture value from the cell on the board
                board_cell : Cell = board.get_cell(row_index, col_index)
                cell_texture_value = board_cell.tileTexture
                
                # Set the surface of the cell to the texture given the value
                Texture.setCellTexture(cell_surface, cell_texture_value)
                
                # Put the cell surface on the board surface
                board_surface.blit(cell_surface, (col_index*cell_size, row_index*cell_size))

        # Outline the mission goal row in red
        if goal_row is not None:
            pygame.draw.rect(
                board_surface,
                RED,
                [0, goal_row * cell_size, board_size[0], cell_size],
                2,
            )

        self.screen.blit(board_surface, self.board_position)
        
    def draw_piece(self, piece, board: Board):
        cell_size = self.cell_size
        color = Texture.getTileTexture(piece.color)

        for i in range(4):
            for j in range(4):
                if i * 4 + j in piece.image():
                    pygame.draw.rect(
                        self.board_surface,
                        color,
                        [
                            cell_size * (piece.x + j) + 1,
                            cell_size * (piece.y + i) + 1,
                            cell_size - 2,
                            cell_size - 2,
                        ],
                    )

        self.screen.blit(self.board_surface, self.board_position)

    def draw_hud(self, score, high_score):
        if not self.is_data_displays_initialized:
            raise RuntimeError("The board must be initialized before drawing the HUD")

        self.score_data_display.clear()
        text = self.font.render(f"Score: {score}", True, BLACK)
        self.score_data_display.add_surface(text, (0, 0))
        text_hi = self.font.render(f"High Score: {high_score}", True, BLACK)
        self.score_data_display.add_surface(text_hi, (0, 24))
        self.score_data_display.display(self.screen)
        self.next_piece_data_display.display(self.screen)

    def draw_game_over_screen(self, is_mission=False):
        lines = [
            "Press Q to quit",
            "Press R to restart",
            "Press M to go back to main menu",
        ]
        if is_mission:
            lines.append(f"Left/Right: mission board {self.mission_selected + 1}/{len(MISSION_BOARDS)}")

        # Clear behind the text so a changed line doesn't draw over the old one
        pygame.draw.rect(self.screen, BLACK, [15, 255, 460, len(lines) * 35 + 10])
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
            game.reset(20, 10, is_mission=game.is_mission, mission_board=self.mission_selected)
            self.pressing_down = False
        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and game.is_mission:
            step = 1 if event.key == pygame.K_RIGHT else -1
            self.mission_selected = (self.mission_selected + step) % len(MISSION_BOARDS)
        elif event.key == pygame.K_m:
            EventManager.changeScene(scene, "startScene")
            self.pressing_down = False
        return False
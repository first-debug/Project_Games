import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, GRIT_COLOR,
                                 (self.left + col * self.cell_size,
                                  self.top + row * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        col = (mouse_pos[0] - self.left) // self.cell_size
        row = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= col < self.width and 0 <= row < self.height:
            return row, col

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos.pos)
        self.on_click(cell)

    @staticmethod
    def _value_cell(board, row, col):
        w = len(board[0])
        h = len(board)
        return board[row % h][col % w]


GRIT_COLOR = pygame.Color('white')

import pygame


class Board:
    # создание поля
    def __init__(self, width, height, value=None):
        self.width = width
        self.height = height
        self.board = [[value] * height for _ in range(width)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                self.draw_cell(x, y, screen)

    def draw_cell(self, x, y, screen):
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), self.cell_rect(x, y), 1)

    def cell_rect(self, x, y):
        return pygame.Rect(x * self.cell_size + self.left, y * self.cell_size + self.top,
                          self.cell_size, self.cell_size)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and cell < (self.width, self.height):
            self.on_click(cell)

import pygame
from gena.gameboard import Board

pygame.init()
size = 820, 620
screen = pygame.display.set_mode(size)


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height, 0)

    def on_click(self, cell):
        x, y = cell
        val = self.board[x][y]
        self.board[x][y] = 0 if val else 1

    def draw_cell(self, x, y, screen):
        val = self.board[x][y]
        rect = self.cell_rect(x, y)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), rect, 0 if val else 1)
        font = pygame.font.Font(None, 40)
        text = font.render(str(self.around(x, y)), 1, (128, 128, 128))
        screen.blit(text, rect)  # вычисленная длина пути до клетки

    def around(self, x, y):
        total = 0
        low = y - 1
        if low < 0:
            low = 0
        else:
            total += self.board[x][low]
        top = y + 1
        if top >= self.height:
            top = y
        else:
            total += self.board[x][top]
        top += 1
        if x > 0:
            total += sum(self.board[x-1][low:top])
        if x < self.width - 1:
            total += sum(self.board[x+1][low:top])
        return total


board = Life(10, 10)
board.set_view(10, 10, 40)

running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
    # clock.tick(10)

pygame.quit()
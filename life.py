import pygame
from gena.gameboard import Board

pygame.init()
size = 820, 620
screen = pygame.display.set_mode(size)


class Life(Board):
    def on_click(self, cell):
        x, y = cell
        val = self.board[x][y]
        self.board[x][y] = 0 if val else 1

    def draw_cell(self, x, y, screen):
        val = self.board[x][y]
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), self.cell_rect(x, y),
                         0 if val else 1)


board = Life(40, 30)
board.set_view(10, 10, 20)

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
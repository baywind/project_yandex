import pygame
from gena.gameboard import Board

pygame.init()
size = 420, 420
screen = pygame.display.set_mode(size)
# clock = pygame.time.Clock()


class Lines(Board):
    BALL = 'ball'
    active = None
    target = None
    paths = None

    def on_click(self, cell):
        x, y = cell
        if self.active:
            if cell == self.active:
                self.active = None
            elif self.board[x][y] == Lines.BALL:
                self.active = cell
            else:
                self.target = cell
        else:
            if self.board[x][y] == Lines.BALL:
                self.active = cell
            else:
                self.board[x][y] = Lines.BALL

    def draw_cell(self, x, y, screen):
        rect = self.cell_rect(x, y)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), rect, 1)  # рисуем клетку
        if self.board[x][y] == Lines.BALL:  # если в клетке шарик
            c = pygame.Color("yellow")
            if self.active == (x, y):  # если шарик активен, меняем цвет
                c = pygame.Color("red")
            pygame.draw.circle(screen, c, rect.center, self.cell_size // 3)
        if self.target == (x, y):  # если клетка назначена целевой
            pygame.draw.circle(screen, pygame.Color("white"), rect.center, self.cell_size // 3, 1)
        if self.paths:  # если мы в процессе поиска пути
            if (x, y) == self.curr:
                pygame.draw.rect(screen, pygame.Color("green"), rect)
            elif (x, y) in self.todo:
                pygame.draw.rect(screen, pygame.Color("yellow"), rect)
            if (x, y) in self.paths:
                font = pygame.font.Font(None, 30)
                text = font.render(str(len(self.paths[(x, y)])), 1, (128, 128, 128))
                screen.blit(text, rect)  # вычисленная длина пути до клетки

    def update(self):
        if self.target is None:
            return
        if self.paths is None:  # подготовим переменные для хранения маршрутов
            self.paths = {self.active: []}
            self.todo = []
            self.curr = self.active  #
            return
        if self.target in self.paths:  # если нашли дорогу
            if self.curr != self.target:  #
                self.curr = self.target  #
                self.todo = self.paths[self.target][:]  # сохраняем маршрут для визуализации
                self.paths[self.active] = self.todo  #
            x, y = self.active
            self.board[x][y] = None
            if self.todo:  # пока маршрут не закончился, переставляем активный шарик
                self.active = self.todo.pop(0)
                x, y = self.active
                self.board[x][y] = Lines.BALL
            else:          # завершаем перемещение
                x, y = self.target
                self.board[x][y] = Lines.BALL
                self.paths = self.active = self.target = None  # удаляем все переменные поиска пути
                del self.todo, self.curr
                return
            return
        if self.curr is None:
            if len(self.todo) == 0:  # если все доступные клетки просмотрены
                self.paths = self.target = None    # прекращаем искать дорогу
                del self.todo
                return
            self.curr = self.todo.pop(0)  # берём первую непросмотренную клетку
            return
        x, y = self.curr
        self.curr = None  #
        path = self.paths[(x, y)] + [(x, y)]  # записываем маршрут до неё
        for xx, yy in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):  # рассматриваем все соседние
            if not (0 <= xx < self.width and 0 <= yy < self.height):  # исключаем клетки вне доски
                continue
            if (xx, yy) in self.paths:  # исключаем ранее просмотренные
                continue
            if self.board[xx][yy] == Lines.BALL:  # исключаем занятые шариками
                continue
            self.paths[(xx, yy)] = path  # добавляем пути до клеток
            self.todo.append((xx, yy))  # добавляем к списку для просмотра



board = Lines(10, 10)
board.set_view(10, 10, 40)

running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.update()
    board.render(screen)
    pygame.display.flip()
    # clock.tick(10)

pygame.quit()
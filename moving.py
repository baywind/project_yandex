import pygame

pygame.init()
size = width, height = 800, 600
g = 5
screen = pygame.display.set_mode(size)
pygame.display.flip()
clock = pygame.time.Clock();


class Ball:
    def __init__(self, pos, r=1, color=pygame.Color('white'), v=(0, 0)):
        self.x = pos[0]
        self.y = pos[1]
        self.r = r
        self.color = color
        self.vx = v[0]
        self.vy = v[1]

    def pos(self):
        return int(self.x), int(self.y)

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos(), self.r)

    def update(self, tick):
        self.x += tick * self.vx / 1000
        self.y += tick * self.vy / 1000
        self.vy += tick * g / self.r
        if self.y >= 580:
            self.vy = 0


balls = []
ball = None
running = True
while running:
    tick = clock.tick(30)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball = Ball(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            balls.append(ball)
            ball = None
    if ball:
        ball.r += tick // 30
        ball.draw()
    for b in balls:
        b.update(tick)
        b.draw()
    pygame.display.flip()

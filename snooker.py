import pygame


def distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx ** 2 + dy ** 2)**0.5


class Ball(pygame.sprite.Sprite):
    def __init__(self, center, r, color=pygame.Color('white'), vx=0, vy=0, m=None):
        super().__init__(all_sprites)
        self.image = pygame.Surface([r * 2, r * 2], pygame.SRCALPHA)
        self.rect = pygame.Rect(center[0] - r, center[1] - r, r * 2, r * 2)
        self.radius = r
        pygame.draw.circle(self.image, color, (r, r), r)
        self.vx = vx
        self.vy = vy
        self.cx = center[0]
        self.cy = center[1]
        self.m = m
        self.used = []

    def center(self):
        return self.cx, self.cy

    def punch(self, pos):
        self.vx += self.cx - pos[0]
        self.vy += self.cy - pos[1]

    def update(self):
        self.cx += self.vx * tick / 1000
        self.cy += self.vy * tick / 1000
        self.rect.centerx = int(self.cx)
        self.rect.centery = int(self.cy)
        collisions = pygame.sprite.spritecollide(self, all_sprites, 0, pygame.sprite.collide_circle)
        collisions.remove(self)
        for other in collisions:
            self.collide(other)
        self.used.clear()
        if self.rect.x > screen.get_width() or self.rect.y > screen.get_height() \
                or self.rect.x < -self.rect.width or self.rect.y < -self.rect.height:
            self.kill()

    def collide(self, other):
        if self.m is None or other in self.used:
            return
        dx = other.cx - self.cx
        dy = other.cy - self.cy
        r = (dx ** 2 + dy ** 2)**0.5

        vr = (dx * self.vx + dy * self.vy) / r
        vt = (dy * self.vx - dx * self.vy) / r
        o_vr = (dx * other.vx + dy * other.vy) / r
        if other.m is None:
            vr = 2 * o_vr - abs(vr)
        else:
            o_vt = (dy * other.vx - dx * other.vy) / r

            e = self.m * vr**2 + other.m * o_vr**2
            p = self.m * vr + other.m * o_vr
            # a*V**2 - 2*b*V + c == 0
            a = self.m * (self.m + other.m)
            b = self.m * p
            c = p**2 - e * other.m
            d = b**2 - a*c
            if d < 0:
                raise ValueError
            vr = (b - d**0.5) / a
            o_vr = (p - self.m * vr) / other.m
            other.used.append(self)
            other.vx = (dx * o_vr + dy * o_vt) / r
            other.vy = (dy * o_vr - dx * o_vt) / r

        self.vx = (dx * vr + dy * vt) / r
        self.vy = (dy * vr - dx * vt) / r


class Line:
    def __init__(self, point, color=(128, 128, 128)):
        self.point = point
        self.color = color
        self.p1 = self.p2 = (-1, -1)

    def update(self, p):
        dx = self.point[0] - p[0]
        dy = self.point[1] - p[1]
        mul = 0
        if dx < 0:
            mul = p[0] // abs(dx)
        elif dx > 0:
            mul = (screen.get_width() - p[0]) // dx
        if dy < 0:
            mul = max(mul, p[1] // abs(dy))
        elif dy > 0:
            mul = max(mul, (screen.get_height() - p[1]) // dy)
        self.p1 = p
        self.p2 = (p[0] + mul * dx, p[1] + mul * dy)

    def draw(self):
        pygame.draw.line(screen, self.color, self.p1, self.p2)


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.flip()
clock = pygame.time.Clock()

running = True
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
obstacle = None
r = 1
line = None
ball = None

while running:
    tick = clock.tick(30)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            for s in all_sprites:
                if event.key == pygame.K_SPACE:
                    s.vx = s.vy = 0
                elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_ESCAPE):
                    s.kill()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                obstacle = event.pos
            elif event.button == 1:
                for s in all_sprites:
                    if distance(s.center(), event.pos) < s.radius:
                        ball = s
                        ball.vx = ball.vy = 0
                        ball.cx = event.pos[0]
                        ball.cy = event.pos[1]
                        break
                else:
                    ball = Ball(event.pos, 10, pygame.Color('red'), m=1)
                line = Line(ball.center())
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if type(obstacle) == tuple:
                    r = int(distance(obstacle, pygame.mouse.get_pos()))
                    if r > 0:
                        obstacle = Ball(obstacle, r, pygame.Color('yellow'))
                        obstacles.add(obstacle)
                    obstacle = None
            elif event.button == 1:
                if line:
                    line = None
                if ball:
                    balls.add(ball)
                    ball.punch(event.pos)
                    ball = None
        if event.type == pygame.MOUSEMOTION:
            if line:
                line.update(event.pos)
    if type(obstacle) == tuple:
        r = int(distance(obstacle, pygame.mouse.get_pos()))
        if r > 0:
            pygame.draw.circle(screen, pygame.Color('yellow'), obstacle, r, 1)
    all_sprites.update()
    all_sprites.draw(screen)
    if line:
        line.draw()
    pygame.display.flip()

import pygame
pygame.init()
from pygame import *
FPS = 60
SPEED_FACTOR = 10
GAME_TIME_MS = 2 * 60 * 1000
HIT_COOLDOWN_MS = 600
START_X, START_Y = 15, 500
class Proekt(sprite.Sprite):
    def __init__(self, x, y, speed, mg):
        """
        Создаёт базовый игровой объект (спрайт) с картинкой, скоростью и позицией.
        Объект хранит координаты двумя способами:
        - ``fx``/``fy`` (float) — для плавного перемещения (можно прибавлять дробные значения).
        - ``rect`` (pygame.Rect) — для отрисовки и столкновений (pygame работает с целыми).
        :param x: Начальная координата X (левый верхний угол спрайта).
        :type x: int | float
        :param y: Начальная координата Y (левый верхний угол спрайта).
        :type y: int | float
        :param speed: Базовая скорость объекта (множится на ``SPEED_FACTOR`` и ``dt``).
        :type speed: int | float
        :param mg: Путь к файлу изображения объекта.
        :type mg: str
        :raises pygame.error: Если изображение не удаётся загрузить (не найден файл или неверный формат).
        """
        sprite.Sprite.__init__(self)
        self.speed = speed
        mg = image.load(mg)
        self.image = transform.scale(mg, (50, 50))
        self.rect = self.image.get_rect()
        self.fx = float(x)
        self.fy = float(y)
        self.rect.x = int(self.fx)
        self.rect.y = int(self.fy)
    def see(self):
        """
        Отрисовывает спрайт на главном окне ``window``.
        Использует текущие координаты ``self.rect.x`` и ``self.rect.y``.
        Предполагается, что перед вызовом была выполнена синхронизация ``sync_rect()``
        (если ``fx/fy`` менялись).
        :returns: Ничего не возвращает.
        :rtype: None
        """
        window.blit(self.image,(self.rect.x, self.rect.y))
    def sync_rect(self):
        """
        Синхронизирует ``pygame.Rect`` (целые координаты) с float-координатами ``fx/fy``.
        Нужна для корректной отрисовки и столкновений после движения, выполненного
        с использованием ``fx/fy``.
        :returns: Ничего не возвращает.
        :rtype: None
        """
        self.rect.x = int(round(self.fx))
        self.rect.y = int(round(self.fy))
class Caracters(Proekt):
    def smena(self, dt):
        """
        Обрабатывает управление игроком и перемещает персонажа.
        Управление:
        - влево: ``LEFT`` или ``A``
        - вправо: ``RIGHT`` или ``D``
        - вверх: ``UP`` или ``W``
        - вниз: ``DOWN`` или ``S``
        Перемещение делается во float-координатах через ``fx/fy`` и зависит от времени кадра:
        ``step = self.speed * SPEED_FACTOR * dt``
        :param dt: Время, прошедшее с прошлого кадра (в секундах).
        :type dt: float
        :returns: Ничего не возвращает.
        :rtype: None
        """
        keys = key.get_pressed()
        step = self.speed * SPEED_FACTOR * dt
        if keys[K_LEFT] or keys[K_a]:
            self.fx -= step
        if keys[K_RIGHT] or keys[K_d]:
            self.fx += step
        if keys[K_UP] or keys[K_w]:
            self.fy -= step
        if keys[K_DOWN] or keys[K_s]:
            self.fy += step
        self.sync_rect()
class Eneny(Proekt):
    side = "left"
    def vrag_smena1(self, dt):
        """
        Движение врага №1: патрулирование по вертикали между заданными границами.
        Логика:
        - если враг поднялся до ``y <= 170`` → направление становится ``down``
        - если опустился до ``y >= 420`` → направление становится ``up``
        - затем двигается на шаг ``step`` вверх или вниз.
        :param dt: Время, прошедшее с прошлого кадра (в секундах).
        :type dt: float
        :returns: Ничего не возвращает.
        :rtype: None
        """
        step = self.speed * SPEED_FACTOR * dt
        if self.rect.y <= 170:
            self.side2 = "down"
        if self.rect.y >= 420:
            self.side2 = "up"
        if self.side2 == "up":
            self.fy -= step
        else:
            self.fy += step
        self.sync_rect()
    side2 = "down"
    def vrag_smena2(self, dt):
        """
        Движение врага №2: патрулирование по горизонтали между заданными границами.
        Логика:
        - если враг ушёл влево до ``x <= 20`` → направление становится ``right``
        - если ушёл вправо до ``x >= 730`` → направление становится ``left``
        - затем двигается на шаг ``step`` влево или вправо.
        :param dt: Время, прошедшее с прошлого кадра (в секундах).
        :type dt: float
        :returns: Ничего не возвращает.
        :rtype: None
        """
        step = self.speed * SPEED_FACTOR * dt
        if self.rect.x <= 20:
            self.side = "right"
        if self.rect.x >= 730:
            self.side = "left"
        if self.side == "left":
            self.fx -= step
        else:
            self.fx += step
        self.sync_rect()
    def vrag_smena3(self, dt):
        """
        Движение врага №3: движение по маршруту (список точек) туда-обратно.
        При первом запуске метод инициализирует:
        - ``self.route`` — список точек маршрута ``[(x1, y1), (x2, y2), ...]``
        - ``self._route_i`` — индекс текущей целевой точки
        - ``self._route_dir`` — направление изменения индекса (``+1`` вперёд, ``-1`` назад)
        Затем каждый кадр враг перемещается от текущей позиции к целевой точке.
        Если достиг точки — выбирает следующую (в конце маршрута разворачивается обратно).
        Метод учитывает ``dt`` и использует float-координаты.
        :param dt: Время, прошедшее с прошлого кадра (в секундах).
        :type dt: float
        :returns: Ничего не возвращает. Может завершиться досрочно, если скорость нулевая или маршрут слишком короткий.
        :rtype: None
        """
        if not hasattr(self, "route"):
            self.route = [(740, 345), (740, 95), (660, 95), (660, 160), (585, 160),(585, 95), (510, 95), (510, 15), (740, 15)]
            self._route_i = 0
            self._route_dir = 1
            self.fx, self.fy = map(float, self.route[0])
            self.sync_rect()
            self._route_i = 1
        if self.speed <= 0 or len(self.route) < 2:
            return
        step = self.speed * SPEED_FACTOR * dt
        tx, ty = self.route[self._route_i]
        tx, ty = float(tx), float(ty)
        x, y = self.fx, self.fy
        dx, dy = tx - x, ty - y
        if dx == 0 and dy == 0:
            if self._route_i == len(self.route) - 1:
                self._route_dir = -1
            elif self._route_i == 0:
                self._route_dir = 1
            self._route_i += self._route_dir
            return
        dist = (dx * dx + dy * dy) ** 0.5
        move = min(step, dist)
        self.fx = x + dx / dist * move
        self.fy = y + dy / dist * move
        self.sync_rect()
class Wall(sprite.Sprite):
    """
    Создаёт прямоугольную стену (препятствие) заданного размера и цвета.
    Стена хранит параметры цвета и размера, а также прямоугольник ``rect``
    для отрисовки и столкновений.
    :param x: Координата X (левый верхний угол стены).
    :type x: int
    :param y: Координата Y (левый верхний угол стены).
    :type y: int
    :param heig: Высота стены (в пикселях).
    :type heig: int
    :param wid: Ширина стены (в пикселях).
    :type wid: int
    :param r: Красная составляющая цвета (0..255).
    :type r: int
    :param g: Зелёная составляющая цвета (0..255).
    :type g: int
    :param b: Синяя составляющая цвета (0..255).
    :type b: int
    """ 
    def __init__(self, x, y, heig, wid, r, g, b):
        sprite.Sprite.__init__(self)
        self.r = r
        self.g = g
        self.b = b
        self.width = wid
        self.height = heig
        self.image = Surface([self.width, self.height])
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, self.width, self.height)

    def picture_wall(self):
        """
        Отрисовывает стену на главном окне ``window`` в виде прямоугольника.
        Использует сохранённые цвет (r, g, b) и параметры ``rect``/``width``/``height``.
        :returns: Ничего не возвращает.
        :rtype: None
        """
        draw.rect(window, (self.r, self.g, self.b), (self.rect.x, self.rect.y, self.width, self.height))
class Door(sprite.Sprite):
    """
    Создаёт прямоугольную "дверь" (зону выхода).
    Дверь используется для проверки столкновения игрока с выходом:
    ``sprite.collide_rect(geroy, door_rect)``.
    :param x: Координата X (левый верхний угол двери).
    :type x: int
    :param y: Координата Y (левый верхний угол двери).
    :type y: int
    :param heig: Высота двери (в пикселях).
    :type heig: int
    :param wid: Ширина двери (в пикселях).
    :type wid: int
    """
    def __init__(self, x, y, heig, wid):
        sprite.Sprite.__init__(self)
        self.width = wid
        self.height = heig
        self.image = Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, self.width, self.height)
window = display.set_mode((810, 800))
display.set_caption("Лабиринт")
background = image.load("фон1.jpg")
background = transform.scale(background, (810, 800))
welcome_image = image.load("Welcome.png")
welcome_image = transform.scale(welcome_image, (810, 800))
window.blit(welcome_image, (0, 0))
display.update()
welcome = True
while welcome:
    for e in event.get():
        if e.type == QUIT:
            pygame.quit()
            exit()
        if e.type == KEYDOWN or e.type == MOUSEBUTTONDOWN:
            welcome = False
    time.delay(20)
geroy = Caracters(START_X, START_Y, 15, "geroy.png")
zvezda1 = Proekt(15, 90, 0, "zvezda.png")
zvezda2 = Proekt(740, 15, 0, "zvezda.png")
zvezda3 = Proekt(420, 400, 0, "zvezda.png")
vrag1 = Eneny(92, 160, 15, "vrag.png")
vrag2 = Eneny(20, 731, 15, "vrag.png")
vrag3 = Eneny(740, 345, 15, "vrag.png")
lage = Wall(0, 0, 800, 10, 100, 0,235 )
lage2 = Wall(0, 0, 10, 800, 100, 0, 235)
lage3 = Wall(800, 0, 130, 10, 100, 0, 235)
lage4 = Wall(800, 200, 600, 10, 100, 0, 235)
lage5 = Wall(0, 790, 100, 800, 100, 0, 235)
lage6 = Wall(75, 0, 80, 10, 100, 0, 235)
lage7 = Wall(150, 80, 80, 10, 100, 0, 235)
lage8 = Wall(75, 150, 10, 80, 100, 0, 235)
lage9 = Wall(75, 150, 80, 10, 100, 0, 235)
lage10 = Wall(0, 220, 10, 80, 100, 0, 235)
lage11 = Wall(235, 0, 230, 10, 100, 0, 235)
lage12 = Wall(160, 220, 10, 160, 100, 0, 235)
lage13 = Wall(150, 220, 270, 10, 100, 0, 235)
lage14 = Wall(75, 480, 10, 80, 100, 0, 235)
lage15 = Wall(75, 300, 430, 10, 100, 0, 235)
lage16 = Wall(75, 720, 10, 415, 100, 0, 235)
lage17 = Wall(320, 220, 190, 10, 100, 0, 235)
lage18 = Wall(235, 300, 270, 10, 100, 0, 235)
lage19 = Wall(160, 570, 10, 330, 100, 0, 235)
lage20 = Wall(150, 570, 80, 10, 100, 0, 235)
lage21 = Wall(320, 570, 80, 10, 100, 0, 235)
lage22 = Wall(490, 570, 80, 10, 100, 0, 235)
lage23 = Wall(235, 650, 80, 10, 100, 0, 235)
lage24 = Wall(400, 650, 80, 10, 100, 0, 235)
lage25 = Wall(490, 640, 10, 80, 100, 0, 235)
lage26 = Wall(560, 640, 90, 10, 100, 0, 235)
lage27 = Wall(560, 720, 10, 170, 100, 0, 235)
lage28 = Wall(720, 650, 80, 10, 100, 0, 235)
lage29 = Wall(640, 570, 80, 10, 100, 0, 235)
lage30 = Wall(570, 570, 10, 230, 100, 0, 235)
lage31 = Wall(570, 480, 90, 10, 100, 0, 235)
lage32 = Wall(570, 480, 10, 80, 100, 0, 235)
lage33 = Wall(720, 410, 80, 10, 100, 0, 235)
lage34 = Wall(640, 410, 10, 160, 100, 0, 235)
lage35 = Wall(640, 220, 200, 10, 100, 0, 235)
lage36 = Wall(570, 300, 10, 80, 100, 0, 235)
lage37 = Wall(570, 220, 10, 160, 100, 0, 235)
lage38 = Wall(720, 150, 80, 10, 100, 0, 235)
lage39 = Wall(570, 150, 80, 10, 100, 0, 235)
lage40 = Wall(500, 150, 10, 80, 100, 0, 235)
lage41 = Wall(490, 80, 80, 10, 100, 0, 235)
lage42 = Wall(640, 80, 80, 10, 100, 0, 235)
lage43 = Wall(570, 80, 10, 240, 100, 0, 235)
lage44 = Wall(320, 80, 10, 180, 100, 0, 235)
lage45 = Wall(320, 80, 80, 10, 100, 0, 235)
lage46 = Wall(320, 150, 10, 80, 100, 0, 235)
lage47 = Wall(400, 150, 160, 10, 100, 0, 235)
lage48 = Wall(410, 300, 10, 80, 100, 0, 235)
lage49 = Wall(490, 220, 270, 10, 100, 0, 235)
lage50 = Wall(235, 480, 10, 260, 100, 0, 235)
lage51 = Wall(320, 410, 10, 80, 100, 0, 235)
lage52 = Wall(490, 410, 10, 80, 100, 0, 235)
walls = [lage, lage2, lage3, lage4, lage5, lage6, lage7, lage8, lage9, lage10,
         lage11, lage12, lage13, lage14, lage15, lage16, lage17, lage18, lage19, lage20,
         lage21, lage22, lage23, lage24, lage25, lage26, lage27, lage28, lage29, lage30,
         lage31, lage32, lage33, lage34, lage35, lage36, lage37, lage38, lage39, lage40,
         lage41, lage42, lage43, lage44, lage45, lage46, lage47, lage48, lage49, lage50,
         lage51, lage52]
stars = [zvezda1, zvezda2, zvezda3]
vrags = [vrag1, vrag2, vrag3]
font_obj = font.Font(None, 36)
score = 0
all_collected = False
door_rect = Door(800, 130, 100, 10)
door_open = False
lives = 3
last_hit_time = -HIT_COOLDOWN_MS
clock = time.Clock()
start_time = time.get_ticks()
run = True
while run:
    dt = clock.tick(FPS) / 1000.0
    for e in event.get():
        if e.type == QUIT:
            run = False
    now = time.get_ticks()
    elapsed = now - start_time
    remaining = GAME_TIME_MS - elapsed
    if remaining <= 0:
        background1 = image.load("game_over.png")
        background1 = transform.scale(background1, (810, 800))
        window.blit(background1, (0, 0))
        msg = font_obj.render("Время вышло!", True, (255, 0, 0))
        window.blit(msg, (300, 20))
        display.update()
        time.delay(2000)
        break
    if len(stars) == 0:
        door_open = True
    if door_open and sprite.collide_rect(geroy, door_rect):
        background1 = image.load("win.jpg")
        background1 = transform.scale(background1, (810, 800))
        window.blit(background1, (0, 0))
        display.update()
        time.delay(3000)
        break
    window.blit(background, (0, 0))
    window.blit(background, (0, 0))
    lage.picture_wall()
    lage2.picture_wall()
    lage3.picture_wall()
    lage4.picture_wall()
    lage5.picture_wall()
    lage6.picture_wall()
    lage7.picture_wall()
    lage8.picture_wall()
    lage9.picture_wall()
    lage10.picture_wall()
    lage11.picture_wall()
    lage12.picture_wall()
    lage13.picture_wall()
    lage14.picture_wall()
    lage15.picture_wall()
    lage16.picture_wall()
    lage17.picture_wall()
    lage18.picture_wall()
    lage19.picture_wall()
    lage20.picture_wall()
    lage21.picture_wall()
    lage22.picture_wall()
    lage23.picture_wall()
    lage24.picture_wall()
    lage25.picture_wall()
    lage26.picture_wall()
    lage27.picture_wall()
    lage28.picture_wall()
    lage29.picture_wall()
    lage30.picture_wall()
    lage31.picture_wall()
    lage32.picture_wall()
    lage33.picture_wall()
    lage34.picture_wall()
    lage35.picture_wall()
    lage36.picture_wall()
    lage37.picture_wall()
    lage38.picture_wall()
    lage39.picture_wall()
    lage40.picture_wall()
    lage41.picture_wall()
    lage42.picture_wall()
    lage43.picture_wall()
    lage44.picture_wall()
    lage45.picture_wall()
    lage46.picture_wall()
    lage47.picture_wall()
    lage48.picture_wall()
    lage49.picture_wall()
    lage50.picture_wall()
    lage51.picture_wall()
    lage52.picture_wall()
    old_fx, old_fy = geroy.fx, geroy.fy
    geroy.smena(dt)
    if any(sprite.collide_rect(geroy, wall) for wall in walls):
        geroy.fx, geroy.fy = old_fx, old_fy
        geroy.sync_rect()
    vrag1.vrag_smena1(dt)
    vrag2.vrag_smena2(dt)
    vrag3.vrag_smena3(dt)
    hit_enemy = any(sprite.collide_rect(geroy, v) for v in vrags)
    if hit_enemy and (now - last_hit_time) >= HIT_COOLDOWN_MS:
        lives -= 1
        last_hit_time = now
        geroy.fx, geroy.fy = float(START_X), float(START_Y)
        geroy.sync_rect()
        if lives <= 0:
            background1 = image.load("game_over.png")
            background1 = transform.scale(background1, (810, 800))
            window.blit(background1, (0, 0))
            display.update()
            time.delay(2000)
            break
    geroy.see()
    vrag1.see()
    vrag2.see()
    vrag3.see()
    for star in stars:
        star.see()
    for star in stars[:]:
        if sprite.collide_rect(geroy, star):
            stars.remove(star)
            star.kill()
            score += 1
    score_text = font_obj.render(f"Звезд: {score}", True, (255, 0, 0))
    lives_text = font_obj.render(f"Жизни: {lives}", True, (255, 0, 0))
    sec = max(0, remaining // 1000)
    mm = sec // 60
    ss = sec % 60
    timer_text = font_obj.render(f"Время: {mm:02d}:{ss:02d}", True, (255, 0, 0))
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, 45))
    window.blit(timer_text, (10, 80))
    if not door_open:
        draw.rect(window, (255, 0, 0), door_rect.rect)
    else:
        draw.rect(window, (255, 255, 255), door_rect.rect)
    display.update()
pygame.quit()
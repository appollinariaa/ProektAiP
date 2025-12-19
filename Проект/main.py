import pygame
pygame.init()
from pygame import *
class Proekt(sprite.Sprite):
    def __init__(self, x, y, speed, mg):
        sprite.Sprite.__init__(self)
        self.speed = speed
        mg = image.load(mg)
        self.image = transform.scale(mg, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def see(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Caracters(Proekt):
    def smena(self):
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x = self.rect.x + self.speed
        if keys[K_UP] or keys[K_w]:
            self.rect.y = self.rect.y - self.speed
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y = self.rect.y + self.speed
class Eneny(Proekt):
    side = "left"
    def smena(self):
        if self.rect.x <= 0:
            self.side = "right"
        if self.rect.x >= 700:
            self.side = "left"
        if self.side == "left":
            self.rect.x = self.rect.x - self.speed
        else:
            self.rect.x = self.rect.x + self.speed
    side2 = "down"
    def smena2(self):
        if self.rect.y <= 30:
             self.side2 = "down"
        if self.rect.y >= 500:
            self.side2 = "up"
        if self.side2 == "up":
            self.rect.y = self.rect.y - self.speed
        else:
            self.rect.y = self.rect.y + self.speed

class Wall(sprite.Sprite):
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
        draw.rect(window, (self.r, self.g, self.b), (self.rect.x, self.rect.y, self.width, self.height))

class Door(sprite.Sprite):
    def __init__(self, x, y, heig, wid):
        sprite.Sprite.__init__(self)
        self.width = wid
        self.height = heig
        self.image = Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, self.width, self.height)

window = display.set_mode((810, 800))
display.set_caption("Лабиринт")
background = image.load("static/фон1.jpg")
background = transform.scale(background, (810, 800))
geroy = Caracters(15, 500, 15, "static/geroy.png")
zvezda1 = Proekt(15, 90, 0, "static/zvezda.png")
zvezda2 = Proekt(740, 15, 0, "static/zvezda.png")
zvezda3 = Proekt(420, 400, 0, "static/zvezda.png")
vrag1 = Eneny(0, 70, 20, "static/vrag.png")
vrag2 = Eneny(100, 650, 15, "static/vrag.png")
vrag3 = Eneny(750, 0, 15, "static/vrag.png")
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
run = True
while run:
    time.delay(100)
    for e in event.get():
        if e.type == QUIT:
            run = False
    if sprite.collide_rect(geroy, vrag1):
        background1 = image.load("static/game_over.png")
        background1 = transform.scale(background1, (810, 800))
        window.blit(background1, (0, 0))
        display.update()
        time.delay(1000)
        run = False
    if sprite.collide_rect(geroy, vrag2):
        background1 = image.load("static/game_over.png")
        background1 = transform.scale(background1, (810, 800))
        window.blit(background1, (0, 0))
        display.update()
        time.delay(1000)
        run = False
    if sprite.collide_rect(geroy, vrag3):
        background1 = image.load("static/game_over.png")
        background1 = transform.scale(background1, (810, 800))
        window.blit(background1, (0, 0))
        display.update()
        time.delay(1000)
        run = False
    if len(stars) == 0:
        all_collected = True
        door_open = True
    if door_open and sprite.collide_rect(geroy, door_rect):
        background1 = image.load("static/win.jpg")
        background1 = transform.scale(background1, (810, 800))
        window.blit(background1, (0, 0))
        display.update()
        time.delay(3000)
        run = False
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
    old_x, old_y = geroy.rect.x, geroy.rect.y
    geroy.smena()
    if any(sprite.collide_rect(geroy, wall) for wall in walls):
        geroy.rect.x, geroy.rect.y = old_x, old_y
    geroy.see()
    vrag1.smena()
    vrag1.see()
    vrag2.smena()
    vrag2.see()
    vrag3.smena2()
    vrag3.see()
    for star in stars:
        star.see()
    for star in stars[:]:
        if sprite.collide_rect(geroy, star):
            stars.remove(star)
            star.kill()
            score += 1
    score_text = font_obj.render(f"Звезд: {score}", True, (255, 0, 0))
    window.blit(score_text, (10, 10))

    if not door_open:
        draw.rect(window, (255, 0, 0), door_rect)
    else:
        draw.rect(window, (255, 255, 255), door_rect)
    display.update()



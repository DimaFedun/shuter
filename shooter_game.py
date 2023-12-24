#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed, player_x, player_y, size_x,size_y ):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y) )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >=5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',10, self.rect.centerx, self.rect.top, 15,20)
        bullets.add(bullet)

lost = 0


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y>500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"), (700,500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOY WIN!', True, (255,255,255))
lose = font1.render('YOU LOST!', True, (255,255,255))

finish = False

font.init()
font2 = font.SysFont(None, 36)

player = Player('rocket.png', 5, 400, 400, 80, 100)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(1,2),randint(80, 620), -40,80,50 )
    monsters.add(monster)

bullets = sprite.Group()
max_lost = 5
score = 0
goal = 10


asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(1,5), randint(30, 670), -40, 80, 50)
    asteroids.add(asteroid)

run = True
life = 3
rel_time = False
num_fire = 0
FPS = 60
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<5 and rel_time == False:
                    num_fire+=1
                    player.fire()
                    fire_sound.play()
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        
        window.blit(background, (0,0))
        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('wait,reload.....', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        Collide_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in Collide_list:
            score +=1
            monster = Enemy('ufo.png', 2,randint(80, 620), -40,80,50 )
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or lost>= max_lost or life == 0:
            finish = True
            window.blit(lose, (200,250))
        if score >= goal:
            finish = True
            window.blit(win, (200,250))
        if sprite.spritecollide(player, asteroids, False):
            life -= 1
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)    
        
        text = font2.render('Счёт'+str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))
        text_lost = font2.render('Пропущено '+str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10,50))
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
           life_color = (150,0,0)
        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650,10))
        display.update()
    else:
        rel_time = False
        num_fire = 0
        finish = False
        score = 0
        lost = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        for i in range(1,6):
            monster = Enemy('ufo.png',2,randint(80, 620), -40,80,50)
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy('asteroid.png', randint(1,5), randint(30, 670), -40, 80, 50)
            asteroids.add(asteroid)

    display.update()
    clock.tick(FPS)

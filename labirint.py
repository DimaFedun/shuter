from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed, player_x, player_y ):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65) )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<680:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y<480:
            self.rect.y += self.speed
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >=620:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -=self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_wight, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_wight
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
Kick = mixer.Sound('Kick.ogg')
Kick.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (120,67,35))
lose = font.render('YOU LOSE', True, (45,78,125))

finish = False

#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load("background.jpg"), (700,500))

player = Player('hero.png', 5, 50, 50)
monster = Enemy('cyborg.png', 2, 600, 250)
final = GameSprite('treasure.png', 0, 600, 400)
wall1 = Wall(100, 180, 180, 25, 56, 25, 600)
wall2 = Wall(100, 180, 180, 150, 56, 25, 356)
wall3 = Wall(100, 180, 180, 150, 412, 125, 25)
wall4 = Wall(100, 180, 180, 350, 120, 25, 380)
wall5 = Wall(100, 180, 180, 250, 20, 25, 392)
wall6 = Wall(100, 180, 180, 250, 20, 425, 25)
wall7 = Wall(100, 180, 180, 350, 120, 150, 25)
wall8 = Wall(100, 180, 180, 500, 120, 25, 380)
wall9 = Wall(100, 180, 180, 675, 20, 25, 480)


game = True
FPS = 60
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
     
        window.blit(background,(0, 0))
        monster.update()
        player.update()
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()
        wall8.draw_wall()
        wall9.draw_wall()
        player.reset()
        monster.reset()
        final.reset()

    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (200,200))
        money.play()

    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall4) or sprite.collide_rect(player, wall5) or sprite.collide_rect(player, wall6) or sprite.collide_rect(player, wall7) or sprite.collide_rect(player, wall8) or sprite.collide_rect(player, wall9):
        finish = True
        window.blit(lose, (200,200))
        kick.play()
    display.update()
    clock.tick(FPS)
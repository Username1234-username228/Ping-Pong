#Создай собственный Шутер!

from pygame import *

from random import randint

from time import time as timer

font.init()

mixer.init()


class GameSprite(sprite.Sprite):
    
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < 645:
            self.rect.x += self.speed
    

    def fire(self):
        
        Sprite_center_x = self.rect.centerx
        Sprite_top = self.rect.top

        bullet = Bullet("bullet.png", Sprite_center_x, Sprite_top, 20)
        bullets.add(bullet)

        fire.play()


class Enemy(GameSprite):
    
    def update(self):
        
        if self.rect.y <= 500:
            self.direction = "down"

        if self.direction == "down":
            self.rect.y += self.speed

        if self.rect.y == 495:
            self.rect.y = 0
            self.rect.x = randint(0, 655)
            self.rect.y = randint(0, 40)

        self.rect.y +=self.speed
        
        global lost

        if self.rect.y > 485:
            self.rect.x = randint(0, 655)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    
    def update(self):
        
        self.rect.y -= self.speed
        
        if self.rect.y <= 0:
            self.kill()

mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')

lost = 0
score = 0

bullets = sprite.Group()

rocket = Player("rocket.png", 275, 435, 10)

ufo1 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo2 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo3 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo4 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo5 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo6 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo7 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo8 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo9 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo10 = Enemy("ufo.png", randint(0, 655), randint(0, 40),1)
ufo11 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
ufo12 = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)

monsters = sprite.Group()
monsters.add(ufo1)
monsters.add(ufo2)
monsters.add(ufo3)
monsters.add(ufo4)
monsters.add(ufo5)
monsters.add(ufo6)
monsters.add(ufo7)
monsters.add(ufo8)
monsters.add(ufo9)
monsters.add(ufo10)
monsters.add(ufo11)
monsters.add(ufo12)


window = display.set_mode((700, 500))
display.set_caption('Galaxy')

background = transform.scale(image.load("galaxy.jpg"),(700, 500))

clock = time.Clock()
FPS = 60 

game = True
finish = False

reloading = False

num_fire = 0

font = font.SysFont("Arial", 40)

win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (255, 0, 0))
draws = font.render('DRAWS!', True, (0, 255, 127))

while game:
    
    for e in event.get():
        
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            
            if e.key == K_SPACE:
                
                    if num_fire < 8 and reloading == False:
                        num_fire = num_fire + 1
                        fire.play()
                        rocket.fire()

                    if num_fire >= 8 and reloading == False:
                        last_time = timer()
                        reloading = True

    if finish != True:
        
        window.blit(background, (0, 0))
        clock.tick(FPS)

        if score == 10 and sprite.spritecollide(rocket, monsters, False) or score >= 20 and lost >= 7:
            window.blit(draws, (290, 230))
            finish = True

        elif score >= 15:
            window.blit(win, (290, 230))
            finish = True

        elif lost >= 7 or sprite.spritecollide(rocket, monsters, False):
            window.blit(lose, (290, 230))
            finish = True

        rocket.reset()
        
        monsters.draw(window)
        bullets.draw(window)
        
        if reloading == True:
            now_time = timer()

            if now_time - last_time < 0.4:
                reloading2 = font.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reloading2, (260, 460))
            else:
                num_fire = 0
                reloading = False

        #rocket.fire()
        
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        
        for s in sprite_list:
            score = score + 1
            m = Enemy("ufo.png", randint(0, 655), randint(0, 40), 1)
            monsters.add(m)

        rocket.update()
        monsters.update()
        bullets.update()

        text_lose = font.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (1, 60))

        text_score = font.render("Счёт:" + str(score), 1, (255, 255, 255))
        window.blit(text_score, (1, 25))

        display.update()
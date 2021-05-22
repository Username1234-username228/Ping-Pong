from pygame import *

from random import randint

from time import time as timer

font.init()



class GameSprite(sprite.Sprite):
    
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = player_width
        self.height = player_height


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    
    def update1(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys_pressed[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed
    
    def update2(self):
        self.rect.y = ball.rect.y


racket1 = Player("rocket.png", 5, 250, 5, 50, 150)
racket2 = Player("rocket.png", 645, 250, 5, 50, 150)

ball = GameSprite("ball.png", 330, 230, 8, 40, 40)

window = display.set_mode((700, 500))
display.set_caption('Ping-Pong')

background = transform.scale(image.load("Ping-Pong.jpg"),(700, 500))

clock = time.Clock()
FPS = 60 

game = True
finish = False

font = font.SysFont("Arial", 40)

win1 = font.render('Player 1 wins!', True, (255, 0, 0))
win2 = font.render('Player 2 wins!', True, (255, 0, 0))

speed_x = 3
speed_y = 3
score = 0

while game:
    
    for e in event.get():
        
        if e.type == QUIT:
            game = False

    if finish != True:
        
        window.blit(background, (0, 0))
        clock.tick(FPS)

        if ball.rect.x < 0:
            window.blit(win2, (290, 230))
            finish = True

        elif ball.rect.x > 700:
            window.blit(win1, (290, 230))
            finish = True

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if ball.rect.y > 470 or ball.rect.y < 0:
            speed_y *= -1

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            score += 1

        if score >= 3 and speed_x > 0:
            speed_x += 3
            score = 0

        racket1.reset()
        racket2.reset()
        ball.reset()

        racket1.update2()
        racket2.update1()
        ball.update()

        display.update()

from pygame import *

#*класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #*конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#*класс-наследник для спрайта-игрока (управляется стрелками)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

#*класс-наследник для спрайта-врага (перемещается сам)

class Enemy(GameSprite):
   direction = "left"
   def update(self):
       if self.rect.x <= 470:
           self.direction = "right"
       if self.rect.x >= win_width - 85:
           self.direction = "left"
 
       if self.direction == "left":
           self.rect.x -= self.speed
       else:
           self.rect.x += self.speed
#Класс стены
class Wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width,wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        #*Карна стены
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1,color_2,color_3))
        #*Каждый спрайт хранит свойство rect
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
        #*draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))
 
#TODO Игровая сцена:
win_width = 700
win_height = 500
#!Цвета
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#TODO Дисплей
window = display.set_mode((win_width, win_height))
display.set_caption("My First Game!")
background = transform.scale(image.load("background.png"), (win_width, win_height))
#?Стены
w1 = Wall(242,243,244,110,20,350,10)
w2 = Wall(242,243,244,100,20,10,350)
w3 = Wall(242,243,244,200,120,10,400)
w4 = Wall(242,243,244,0,369,110,10)
w5 = Wall(242,243,244,450,150,10,350)
w6 = Wall(242,243,244,325,20,10,350)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
#*Персонажи игры:
player = Player('player.png', 5, win_height - 80, 4)
monster = Enemy('enemy.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', 550, 450, 0)
#*Концовки игры
win = transform.scale(image.load('win_1.jpg'), (700,500))
lose = transform.scale(image.load('lose_1.png'), (700,500))
#*музыка
mixer.init()
mixer.music.load('StreetLove.ogg')
mixer.music.play()

#!      САМА ИГРА И ЕЁ НАСТРОЙКИ        !#

#*Игровой цикл
game = True
finish = False
clock = time.Clock()
FPS = 60
#*Игра
while game:
   for e in event.get():
       if e.type == QUIT:
           game = False  
   if finish != True:
        window.blit(background,(0, 0))
        player.update()
        monster.update()
        final.reset()      
        player.reset()
        monster.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win,(0,0))
            game = False
        if sprite.collide_rect(player, monster):
            window.blit(lose,(0,0))
            mixer.music.stop()           
        for wall in barriers:
            if sprite.collide_rect(player, wall):
                mixer.music.stop()   
                window.blit(lose,(0,0))                 
        display.update()
        clock.tick(FPS)

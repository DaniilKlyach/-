from pygame import *
import time as t 
init()
mixer.init()
font.init()

#aaa
class  GameSprite(sprite.Sprite):
    def __init__ (self, image_file, x,y,speed):
        self.image = transform.scale(image.load(image_file), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player1(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0 + 150:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0 + 150:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 150:
            self.rect.x += self.speed


class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0 + 150:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 0 + 150:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 150:
            self.rect.x += self.speed
        
class Wall(sprite.Sprite):
    def __init__ (self, color, x, y, width, height,image_file=None):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if image_file != None:
            self.image = transform.scale(image.load(image_file), (width, height))
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Ball(GameSprite):
    def __init__(self, image_file, x,y,speedx,speedy,xmin, xmax,ymin,ymax):
        super().__init__(image_file, x,y, speedx)
        self.speedy = speedy
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
    
    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speedy

        if self.rect.x > self.xmax:
            self.speed = -abs(self.speed)
        if self.rect.x < self.xmin:
            self.speed = abs(self.speed)
        if self.rect.y > self.ymax:
            self.speedy = -abs(self.speedy)
        if self.rect.y < self.ymin:
            self.speedy = abs(self.speedy)




window = display.set_mode((0, 0), FULLSCREEN)
win_width,win_height = display.get_surface().get_size()
display.set_caption('Футбол')

lastshot_time = 0
lastshot_time2 = 0
win_time = time.Clock()
win_FPS = 60
win_game = True
win_finish = False
score1 = 0 
score2 = 0
begin_time = t.time()

music = mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
mixer.music.play()

font1 = font.SysFont('Arial', 200)
font2 = font.SysFont('Arial', 50)

win_image1 = font1.render('Победа левого!', True, (0, 255, 0))
win_image2 = font1.render("Победа правого!",  True, (255, 0, 0))
win_image3 = font1.render("Ничья!",  True, (255, 0, 0))
klavishi = font2.render('ESC - выйти, R - перезапуск',   True, (255, 0, 0))

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

player1 = Player1('ufo.png', 500, 400,10)
player2 = Player2('ufo.png', 900 ,400,10)
ball = Ball('ball.png', win_width//2, win_height//2, 5, 3, 150, win_width-150, 150, win_height-150 )
walls = sprite.Group()
walls.add(Wall((255,0,0), 0+150,win_height//2 -75+37, 100,10))
walls.add(Wall((255,0,0), 0+150,win_height//2 +75+37, 100,10))
walls.add(Wall((255,0,0), win_width - 150-36,win_height//2-75+37, 100,10))
walls.add(Wall((255,0,0), win_width - 150-36,win_height//2 + 75+37, 100,10))
walls.add(Wall((0,0,0), 150,150, 10,win_height-300+65))
walls.add(Wall((0,0,0), win_width-150+65,150, 10,win_height-300+65))
walls.add(Wall((0,0,0), 150,150, win_width-300+65,10))
walls.add(Wall((0,0,0), 150,win_height-150+65, win_width-300+65,10))

wall1 = Wall((255,0,0), 0+150-100+10,win_height//2 -75+37, 10+100,160, 'left.png')
wall2 = Wall((255,0,0), win_width - 150-36+100-10,win_height//2-75+37, 10+100,160, 'right.png')

while win_game:
    display.update()  
    win_time.tick(win_FPS) 


    
    for e in event.get():
        if (e.type == QUIT) or (e.type == KEYDOWN and e.key == K_ESCAPE) :
            win_game = False
        elif (e.type == KEYDOWN and e.key == K_r):
            player1 = Player1('ufo.png', 500, 400,10)
            player2 = Player2('ufo.png', 900 ,400,10)
            begin_time = t.time()
            score1 = 0 
            score2 = 0
            win_finish = False
    

    if not(win_finish):
        player1.update()
        player2.update()
        ball.update()
        now_time = t.time()
        if sprite.collide_rect(player1,ball):
            if now_time - lastshot_time > 1:
                if ball.speed > 0:
                    ball.speedy = -ball.speedy
                else: 
                    ball.speed = - ball.speed
                fire.play()
                lastshot_time = now_time
        if sprite.collide_rect(player2,ball):
            if now_time - lastshot_time2 > 1:
                if ball.speed < 0:
                    ball.speedy = -ball.speedy
                else: 
                    ball.speed = - ball.speed
                fire.play()
                lastshot_time2 = now_time
        


        if sprite.collide_rect(ball, wall1):
            score2 += 1
            player1 = Player1('ufo.png', 500, 400,10)
            player2 = Player2('ufo.png', 900 ,400,10)
            ball = Ball('ball.png', win_width//2, win_height//2, 5, 3, 150, win_width-150, 150, win_height-150 )


        if sprite.collide_rect(ball, wall2):
            score1 += 1
            player1 = Player1('ufo.png', 500, 400,10)
            player2 = Player2('ufo.png', 900 ,400,10)
            ball = Ball('ball.png', win_width//2, win_height//2, 5, 3, 150, win_width-150, 150, win_height-150 )

        image_score = font2.render('Счет: '+str(score1)  +':'+str(score2), True, (0,255,0) )
        tim = 30-int(now_time - begin_time)
        image_time = font2.render('Осталось: '+str(tim) +' секунд.', True, (0,255,0) )
        

        if tim <= 0:
            if score1 > score2:
                window.blit(win_image1, (200, 200))
            elif score2 > score1:
                window.blit(win_image2, (200, 200))
            elif score1 == score2:
                window.blit(win_image3, (500,200))

                
            win_finish = True
            
        if win_finish:
            continue


        window.blit(background, (0,0))
            
        walls.draw(window) 
        wall1.reset()
        wall2.reset()

        player1.reset()
        player2.reset()
        ball.reset()
        window.blit(image_score, (600, 100))
        window.blit(image_time, (200,100))
        window.blit(klavishi, (300,700))
        
        




    





import pygame
from pygame.locals import *
import time
import random
size = 40 
class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("images/apple.jpg")
        self.x = size*3
        self.y = size*3
    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.x = random.randint(0,24)*size
        self.y = random.randint(0,14)*size

class Snake:
    def __init__(self,parent_screen,length):
        self.length = length 
        self.block = pygame.image.load("images/block.jpg")
        self.x = [size]*length
        self.y = [size]*length
        self.parent_screen = parent_screen
        self.direction = "down"

    def incre_len(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)
    def draw(self):
        self.parent_screen.fill((21, 147, 163))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    def move_left(self):
        self.direction ="left"
    def move_right(self):
        self.direction="right"
    def move_up(self):
        self.direction ="up"
    def move_down(self):
       self.direction="down"
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=="down":
            self.y[0] +=size
            self.draw()
        if self.direction=="up":
            self.y[0] -=size
            self.draw()
        if self.direction=="left":
            self.x[0] -=size
            self.draw()
        if self.direction=="right":
            self.x[0] +=size
            self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.background_music()
        self.surface = pygame.display.set_mode((1000,600))
        self.surface.fill((73, 205, 245))
        self.snake =Snake(self.surface,1) 
        self.apple = Apple(self.surface)
        self.snake.draw()
        self.apple.draw()
    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+size:
            if y1>=y2 and y1<y2+size:
                return True
        return False
    def background_music(self):
        pygame.mixer.music.load("sounds/music.mp3")
        pygame.mixer.music.play()
    def play_sound(self,s):
        sound = pygame.mixer.Sound(f"sounds/{s}.mp3")
        pygame.mixer.Sound.play(sound)
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("bite")
            self.snake.incre_len()
            self.apple.move()
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "game over"
        if not (0 <= self.snake.x[0] <= 990 and 0 <= self.snake.y[0] <= 590):
            self.play_sound('crash')
            raise "Hit the boundry error"        
    def reset(self):
        self.snake =Snake(self.surface,1)
        self.apple = Apple(self.surface)
    def show_game_over(self):
        self.surface.fill((73, 205, 245))
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"total score:{self.snake.length-1}",True,(255,255,255))
        self.surface.blit(line1,(300,250))
        line2 = font.render("To play press Enter!!! ,To exit press Escape",True,(255,255,255))
        self.surface.blit(line2,(300,300))
        pygame.display.flip()
        pygame.mixer.music.pause()
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"score:{self.snake.length-1}",True,(255,255,255))
        self.surface.blit(score,(850,10))
    def run(self):
        self.running = True
        pause = False
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()
            

                elif event.type == QUIT:
                    self.running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_game_over()
                self.reset()
            time.sleep(0.2)

if __name__ =="__main__":
    game = Game()
    game.run()
    
    
    
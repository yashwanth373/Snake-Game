import pygame
import time
import random

class Environment:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        pygame.display.set_caption('Snake Game')
        self.display=pygame.display.set_mode((width,height))
        self.bg=pygame.transform.scale(pygame.image.load("media/background.jpg"),(width,height))
        self.display.blit(self.bg,(0,0))
        pygame.display.update()

# class Player:
#     def __init__(self):
#         self.x=
#         self.body =[]

class Food:
    def __init__(self,env):
        self.x_food=200
        self.y_food=300
        pygame.draw.rect(env.display,(0,255,0),[self.x_food,self.y_food,10,10])
        pygame.display.update()
    def new_spawn(self,env):
        env.display.fill((255,255,255))
        pygame.display.update()
        self.x_food=random.randint(10,env.width-20)
        self.y_food=random.randint(10,env.height-20)
        env.display.blit(env.bg,(0,0))
        pygame.display.update()
        pygame.draw.rect(env.display,(0,255,0),[self.x_food,self.y_food,10,10])
        pygame.display.update()

         



if __name__ == '__main__':
    pygame.init()
    env = Environment(600,400)
    game_over = False
    food=Food(env)
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
        if random.random()<=0.5:
            food.new_spawn(env)

                
    pygame.quit()
    quit()



        


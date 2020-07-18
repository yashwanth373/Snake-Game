import pygame
import time
import random

class Environment:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        pygame.display.set_caption('Snake Game')
        self.display=pygame.display.set_mode((width,height))
        self.bg=pygame.transform.scale(pygame.image.load("media/background.jpg"),(width-50,height-50))
        self.display.fill((255,255,255))
        self.display.blit(self.bg,(25,5))
        pygame.display.update()
        self.player=Player()
        self.food=Food(self)

class Player:
    def __init__(self):
        self.x=200
        self.y=200
        self.body =[]
        self.body.append([self.x,self.y])
        self.score=1
        self.crash=False

    def display(self,env):
        for i in range(0,self.score):
            pygame.draw.rect(env.display,(0,0,0),[self.body[i][0],self.body[i][1],10,10])

    def move(self):
        pass
    


class Food:
    def __init__(self,env):
        self.x_food=200
        self.y_food=300
        pygame.draw.rect(env.display,(0,255,0),[self.x_food,self.y_food,10,10])
        pygame.display.update()
    def new_spawn(self,env):
        env.display.fill((255,255,255))
        pygame.display.update()
        self.x_food=random.randrange(35,env.width-45,10)
        self.y_food=random.randrange(15,env.height-65,10)
        if [self.x_food,self.y_food] in env.player.body:
            self.new_spawn(env)
        else:
            env.display.blit(env.bg,(25,5))
            pygame.display.update()
            pygame.draw.rect(env.display,(0,255,0),[self.x_food,self.y_food,10,10])
            pygame.display.update()

         



if __name__ == '__main__':
    pygame.init()
    env = Environment(600,400)
    player=env.player
    food=env.food
    player.display(env)
    pygame.display.update()
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
        if random.random()<=0.5:
            food.new_spawn(env)
            player.display(env)
            pygame.display.update()
        time.sleep(1)

                
    pygame.quit()
    quit()



        


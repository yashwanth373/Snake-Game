import pygame
import time
import random
import numpy as np
from keras.utils import to_categorical

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
        self.end=False

class Player:
    def __init__(self):
        self.x=200
        self.y=200
        self.body =[]
        self.body.append([self.x,self.y])
        self.body.append([self.x-10,self.y])
        self.body.append([self.x-20,self.y])
        self.body.append([self.x-30,self.y])
        self.body.append([self.x-40,self.y])
        self.body.append([self.x-50,self.y])
        self.score=1
        self.crash=False
        self.dir="right"

    def display(self,env):
        for i in range(0,len(self.body)):
            pygame.draw.rect(env.display,(0,0,0),[self.body[i][0],self.body[i][1],10,10])
            pygame.display.update()
    
    def update_body(self,head_x,head_y,env):
        if [head_x,head_y] in self.body:
            env.end=True
        else:
            self.body.pop()
            self.body.insert(0,[head_x,head_y])
        

    def move(self,direction,env):
        if self.dir=="right":
            if np.array_equal(direction,[0,1,0]): #right turn
                self.update_body(self.body[0][0],self.body[0][1] + 10,env)  
                self.dir="down"              
            elif np.array_equal(direction,[0,0,1]): #left turn
                self.update_body(self.body[0][0],self.body[0][1] - 10,env)
                self.dir="up"
            elif np.array_equal(direction,[1,0,0]): #gng straight
                self.update_body(self.body[0][0] + 10,self.body[0][1],env)
                self.dir="right"
        elif self.dir=="left":
            if np.array_equal(direction,[0,1,0]): #right turn
                self.update_body(self.body[0][0],self.body[0][1] - 10,env)  
                self.dir="up"             
            elif np.array_equal(direction,[0,0,1]): #left turn
                self.update_body(self.body[0][0],self.body[0][1] + 10,env)
                self.dir="down"
            elif np.array_equal(direction,[1,0,0]): #gng straight
                self.update_body(self.body[0][0] - 10,self.body[0][1],env)
                self.dir="left"
        elif self.dir=="up":
            if np.array_equal(direction,[0,1,0]): #right turn
                self.update_body(self.body[0][0] + 10,self.body[0][1],env)  
                self.dir="right"              
            elif np.array_equal(direction,[0,0,1]): #left turn
                self.update_body(self.body[0][0] - 10,self.body[0][1],env)
                self.dir="left"
            elif np.array_equal(direction,[1,0,0]): #gng straight
                self.update_body(self.body[0][0],self.body[0][1]-10,env)
                self.dir="up"
        elif self.dir=="down":
            if np.array_equal(direction,[0,1,0]): #right turn
                self.update_body(self.body[0][0] - 10,self.body[0][1],env)  
                self.dir="left"              
            elif np.array_equal(direction,[0,0,1]): #left turn
                self.update_body(self.body[0][0] + 10,self.body[0][1],env)
                self.dir="right"
            elif np.array_equal(direction,[1,0,0]): #gng straight
                self.update_body(self.body[0][0],self.body[0][1] + 10,env)
                self.dir="down"
    
        if self.body[0][0]>env.width-45:
            env.end=True
        
        
        
        
        
        
        
    


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
            screen_update(env)


def screen_update(env):
    env.display.blit(env.bg,(25,5))
    pygame.display.update()
    pygame.draw.rect(env.display,(0,255,0),[env.food.x_food,env.food.y_food,10,10])
    pygame.display.update()
    env.player.display(env)





if __name__ == '__main__':
    pygame.init()
    env = Environment(600,400)
    player=env.player
    food=env.food
    player.display(env)
    pygame.display.update()
    while not env.end:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                env.end=True
        direction=to_categorical(random.randint(0,2),num_classes=3)
        player.move(direction,env)
        screen_update(env)
        time.sleep(0.2)
    if(env.end):
        print("game over")
        print("head loc is ",player.body[0])

    pygame.quit()
    quit()



        


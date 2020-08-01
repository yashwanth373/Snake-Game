import pygame
import time
import random
import numpy as np
from keras.utils import to_categorical

# Global Paramters
episodes_count=50
epsilon=1
epsilon_decay=0.001




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
        elif head_x==env.food.x_food and head_y==env.food.y_food:
            self.body.insert(0,[head_x,head_y])
            self.score += 1
            env.food.new_spawn(env)
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
    
        if self.body[0][0]>env.width-45 or self.body[0][0]<35 or self.body[0][1]>env.height-65 or self.body[0][1]<15:
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
    game_count=0
    highscore=0
    break_out=False
    while game_count<episodes_count:
        env = Environment(600,400)
        player=env.player
        food=env.food
        player.display(env)
        pygame.display.update()
        direction=[]
        while not env.end:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    env.end=True
                    break_out=True
            if random.randint(0,1)<epsilon:
                #do a random movement
                direction=to_categorical(random.randint(0,2),num_classes=3)
            else:
                #get movement from the NN
                pass
            player.move(direction,env)
            screen_update(env)
            time.sleep(0.1)
        if break_out:
            break
        epsilon=epsilon-epsilon_decay
        if player.score-1>highscore:
            highscore=player.score-1
        game_count += 1
        print("game number ",game_count)
        print("head loc is ",player.body[0], "score is ",player.score-1, " and highscore is ",highscore)

    pygame.quit()
    quit()



        


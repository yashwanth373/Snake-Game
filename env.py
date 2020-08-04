import pygame
import time
import random
import numpy as np
from keras.utils import to_categorical
from DQN import Agent

# Global Paramters
episodes_count=150
epsilon=0
epsilon_decay=1/75
batch_size=500





class Environment:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        # pygame.display.set_caption('Snake Game')
        # self.display=pygame.display.set_mode((width,height))
        # self.bg=pygame.transform.scale(pygame.image.load("media/background.jpg"),(width-50,height-50))
        # self.display.fill((255,255,255))
        # self.display.blit(self.bg,(25,5))
        # pygame.display.update()
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
        self.eaten=False

    # def display(self,env):
    #     for i in range(0,len(self.body)):
    #         pygame.draw.rect(env.display,(0,0,0),[self.body[i][0],self.body[i][1],10,10])
    #         pygame.display.update()
    
    def update_body(self,head_x,head_y,env):      
        
        if [head_x,head_y] in self.body:
            env.end=True
        elif head_x==env.food.x_food and head_y==env.food.y_food:
            self.body.insert(0,[head_x,head_y])
            self.score += 1
            self.eaten=True
            env.food.new_spawn(env)
            self.eaten=False
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
    
        if self.body[0][0]>env.width-40 or self.body[0][0]<20 or self.body[0][1]>env.height-40 or self.body[0][1]<20:
            env.end=True
        
        
        
        
        
        
        
    


class Food:
    def __init__(self,env):
        self.x_food=200
        self.y_food=300
        # pygame.draw.rect(env.display,(0,255,0),[self.x_food,self.y_food,10,10])
        # pygame.display.update()
    def new_spawn(self,env):
        # env.display.fill((255,255,255))
        # pygame.display.update()
        self.x_food=random.randrange(20,env.width-40,10)
        self.y_food=random.randrange(20,env.height-40,10)
        if [self.x_food,self.y_food] in env.player.body:
            self.new_spawn(env)
        # else:
        #     screen_update(env)


# def screen_update(env):
#     env.display.blit(env.bg,(25,5))
#     pygame.display.update()
#     pygame.draw.rect(env.display,(0,255,0),[env.food.x_food,env.food.y_food,10,10])
#     pygame.display.update()
#     env.player.display(env)


def initialise(env,agent):
    init_state1=agent.get_state(env)
    action = [1,0,0]
    env.player.move(action,env)
    init_state2=agent.get_state(env)
    reward = agent.set_reward(env)
    agent.remember(init_state1,action,reward,init_state2,env.end)
    agent.replay(agent.memory,batch_size)






if __name__ == '__main__':
    pygame.init()
    game_count=0
    agent=Agent()
    highscore=0
    break_out=False
    while game_count<episodes_count:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        env = Environment(440,440)
        player=env.player
        food=env.food

        #Initialising game
        initialise(env,agent)

        # player.display(env)
        # pygame.display.update()
        direction=[]
        while not env.end:
            old_state = agent.get_state(env)

            if random.randint(0,1)<epsilon:
                #do a random movement
                direction=to_categorical(random.randint(0,2),num_classes=3)
            else:
                #get movement from the NN
                prediction = agent.NN.predict(old_state.reshape((1,11)))
                direction = to_categorical(np.argmax(prediction[0]),num_classes=3)
            
            player.move(direction,env)
            new_state = agent.get_state(env)
            reward =agent.set_reward(env)
            agent.train_short_memory(old_state,direction,reward,new_state,env.end)
            agent.remember(old_state,direction,reward,new_state,env.end)
            player.eaten=False
            # screen_update(env)
            # for better display
            # time.sleep(0.1)
        agent.replay(agent.memory,batch_size)

        epsilon=epsilon-epsilon_decay
        if player.score-1>highscore:
            highscore=player.score-1
        game_count += 1
        print("game number ",game_count, "score is ",player.score-1, " and highscore is ",highscore)
    agent.NN.save_weights('weights/weights.hdf5')

    pygame.quit()
    quit()



        


from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import Adam
from operator import add
import numpy as np
import random
import collections

class Agent:
    def __init__(self):
        self.reward=0
        self.first_layer= 150
        self.second_layer=150
        self.memory_size=2500
        self.third_layer=150
        self.memory=collections.deque(maxlen=self.memory_size)
        self.gamma = 0.9
        self.learning_rate=0.00001
        self.NN=self.network()

    
    # Sequential Neural Network
    def network(self):
        nn=Sequential()
        nn.add(Dense(self.first_layer,activation='relu',input_dim=11))
        nn.add(Dense(self.second_layer,activation='relu'))
        nn.add(Dense(self.third_layer,activation='relu'))
        nn.add(Dense(3,activation='softmax'))
        opt=Adam(self.learning_rate)
        nn.compile(loss='mse',optimizer=opt)
        return nn

    def get_state(self,env):
        player=env.player
        
        state=[



            (player.dir=="right" and ((list(map(add, player.body[-1], [10, 0])) in player.body) or
            player.body[-1][0] + 10 >= (env.width - 40))) or (player.dir=="left" and ((list(map(add, player.body[-1], [-10, 0])) in player.body) or
            player.body[-1][0] - 10 < 20)) or (player.dir=="up" and ((list(map(add, player.body[-1], [0, -10])) in player.body) or
            player.body[-1][-1] - 10 < 20)) or (player.dir=="down" and ((list(map(add, player.body[-1], [0, 10])) in player.body) or
            player.body[-1][-1] + 10 >= (env.height-40))),  # danger straight

            (player.dir=="up" and ((list(map(add,player.body[-1],[10, 0])) in player.body) or
            player.body[ -1][0] + 10 > (env.width-40))) or (player.dir=="down" and ((list(map(add,player.body[-1],[-10,0])) in player.body) or
            player.body[-1][0] - 10 < 20)) or (player.dir=="left" and ((list(map(add,player.body[-1],[0,-10])) in player.body) or 
            player.body[-1][-1] - 10 < 20)) or (player.dir=="right" and ((list(map(add,player.body[-1],[0,10])) in player.body) or 
            player.body[-1][-1] + 10 >= (env.height-40))),  # danger right

             (player.dir=="down" and ((list(map(add,player.body[-1],[10,0])) in player.body) or
             player.body[-1][0] + 10 > (env.width-40))) or (player.dir=="up" and ((list(map(add, player.body[-1],[-10,0])) in player.body) or
             player.body[-1][0] - 10 < 20)) or (player.dir=="right" and ((list(map(add,player.body[-1],[0,-10])) in player.body) or 
             player.body[-1][-1] - 10 < 20)) or (player.dir=="left" and ((list(map(add,player.body[-1],[0,10])) in player.body) or
             player.body[-1][-1] + 10 >= (env.height-40))), #danger left


            env.player.dir=="right", #moving right
            env.player.dir=="left",  #moving left
            env.player.dir=="up",    #moving up
            env.player.dir=="down",  #moving down

            env.food.x_food<env.player.body[0][0], #food to the left
            env.food.x_food>env.player.body[0][0], #food to the right
            env.food.y_food<env.player.body[0][1], #food to the up
            env.food.y_food<env.player.body[0][1]  #food to the down 

        ]

        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0 

        return np.asarray(state)
    
    def set_reward(self,env):
        self.reward=0
        if env.end:
            self.reward = -10
            return self.reward
        if env.player.eaten:
            self.reward= 10 
        return self.reward



    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))
    



    def replay(self,memory,batch_size):
        if len(memory) > batch_size:
            minibatch=random.sample(memory,batch_size)
        else:
            minibatch = memory
        for state,action,reward,next_state,done in minibatch:
            target= reward
            if not done:
                target = reward + self.gamma*np.amax(self.NN.predict(np.array([next_state]))[0])
            target_f = self.NN.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.NN.fit(np.array([state]),target_f,epochs=1,verbose=0)
    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.NN.predict(next_state.reshape((1, 11)))[0])
        target_f = self.NN.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.NN.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)






















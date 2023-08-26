import gymnasium as gym 
from gymnasium import spaces 
from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController  
import random 
import numpy as np
import time 
from collections import deque


MAX_LEN = 50


class WorldEnv(gym.Env):

    def __init__(self):
        super(WorldEnv,self).__init__()

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-500, high=500,shape=(6,), dtype=np.float32)
    
    def step(self,action):
        self.action = action
        self.app.step()
        self.update()
        return self.observation, self.reward, self.done, False, {}

    def update(self):
        action = self.action
        # self.prev_actions.append(action)
        self.player.y += held_keys["space"]*0.1 
        self.player.y -= held_keys["shift"]*0.1
        prevp1 = np.array((self.lander.x,self.lander.z))
        prevp2 = np.array((self.target.x,self.target.z))
        reward = 0
        if not self.lander.intersects(self.ground).hit:
            self.lander.y -= 0.2
            if action == 0:
                self.lander.x += 0.2
            if action == 1:
                self.lander.z -= 0.2
            if action == 2:
                self.lander.z += 0.2
            if action == 3:
                self.lander.x -= 0.2
        else:
            self.done = True 
        
        if held_keys["q"]:
            self.done = True 
            quit()
        
        p1 = np.array((self.lander.x,self.lander.z))
        p2 = np.array((self.target.x,self.target.z))
        distprev = np.linalg.norm(prevp1 - prevp2)
        dist = np.linalg.norm(p1 - p2)

        if dist < 2:
            reward += 200

        if dist < distprev:
            reward += 10
        else:
            reward -= 100

        observation = [self.lander.x,self.lander.y,self.lander.z,self.target.x,self.target.y,self.target.z] 
        self.observation = np.array(observation,dtype = np.float32)
        self.reward = reward
        
        
    
    def reset(self, seed = 0 ):
        self.app = Ursina() 
        self.landerPos = (5,25,5)
        self.targetPos = (random.randint(0,15),1,random.randint(0,15))
        
        try:
            if self.target:
                self.target.position = self.targetPos
            else:
                self.target = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = self.targetPos)
            if self.ground:
                pass 
            else:
                self.ground = Entity(model = "plane", texture = "grass", collider = "box", scale = (100,1,100))
            if self.lander:
                self.lander.position = self.landerPos
            else:
                self.lander = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = self.landerPos)

            if self.player:
                pass 
            else:
                self.player = FirstPersonController()

        except:
            self.target = Entity(model = "cube", color = color.rgb(255,255,255), collider = "box", scale =(2), position = self.targetPos)
            self.ground = Entity(model = "plane", texture = "grass", collider = "box", scale = (100,1,100))
            self.lander = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = self.landerPos)
            self.player = FirstPersonController()

        self.player.gravity = 0
        self.done = False
        landerPos = self.landerPos
        targetPos = self.targetPos
        self.prev_actions = deque(maxlen = MAX_LEN)  # however long we aspire the snake to be
        for i in range(MAX_LEN):
            self.prev_actions.append(-1) # to create history
        observation = [landerPos[0], landerPos[1], landerPos[2],targetPos[0],targetPos[1],targetPos[2]]
        self.observation = np.array(observation,dtype = np.float32)
        self.reward = -1000
        return self.observation

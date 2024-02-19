import gymnasium as gym 
from gymnasium import spaces 
from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController  
import random 
import numpy as np
import time 
from collections import deque
from threading import Timer



MAX_LEN = 500
GRAVITY = -9.8 *0.3
LANDER_SPEED_Y = 0
LANDER_SPEED_Z = 0
LANDER_SPEED_X = 0
LANDER_ROTATE_X_SPEED = 0 
LANDER_ROTATE_Y_SPEED = 0 
LANDER_ROTATE_Z_SPEED = 0 

LANDER_BOOSTER_ACC = 200

particles = []

def destroy_entity(entity):
    global particles
    try:
        particles.remove(entity)
    except:
        pass
    destroy(entity)

class WorldEnv(gym.Env):

    def __init__(self):
        super(WorldEnv,self).__init__()

        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low=-500, high=500,shape=(12,), dtype=np.float32)
    
    def step(self,action):
        self.action = action
        self.app.step()
        self.update()
        return self.observation, self.reward, self.done, False, {}

    def update(self):
        action = self.action
        self.prev_actions.append(action)
        reward =  0
        # self.prev_actions.append(action)
        prevh = self.lander.y
        prevp1 = np.array((self.lander.x,self.lander.z,self.lander.y))
        prevp2 = np.array((self.target.x,self.target.z,self.target.y))
        global GRAVITY,LANDER_SPEED_Y,LANDER_BOOSTER_ACC,LANDER_ROTATE_X_SPEED,LANDER_ROTATE_Y_SPEED,LANDER_ROTATE_Z_SPEED,LANDER_SPEED_X,LANDER_SPEED_Z
        player = self.player
        lander = self.lander
        player.y += held_keys["space"]*0.1 
        player.y -= held_keys["shift"]*0.1
        reward = 0
        if action == 0:
            # reward -= 10
            LANDER_ROTATE_X_SPEED += LANDER_BOOSTER_ACC*time.dt
            leftThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x-1, (lander.y),lander.z))
            r = Timer(0.05, destroy_entity, (leftThrust,))
            particles.append(leftThrust)
            r.start()
        

        if action == 1:
            # reward -= 10
            LANDER_ROTATE_X_SPEED -= LANDER_BOOSTER_ACC*time.dt
            rightThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x+1, (lander.y),lander.z))
            r = Timer(0.05, destroy_entity, (rightThrust,))
            particles.append(rightThrust)
            r.start()
        # else:
        #     LANDER_ROTATE_X_SPEED = min((LANDER_ROTATE_X_SPEED + 5),0)
        
        if action == 2:
            # reward -= 10
            LANDER_ROTATE_Z_SPEED += LANDER_BOOSTER_ACC*time.dt
            upThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x, (lander.y),lander.z - 1))
            r = Timer(0.05, destroy_entity, (upThrust,))
            particles.append(upThrust)
            r.start()
        # else:
        #     LANDER_ROTATE_Z_SPEED = max((LANDER_ROTATE_Z_SPEED - 5),0)
        
        if action == 3:
            # reward -= 10
            LANDER_ROTATE_Z_SPEED -= LANDER_BOOSTER_ACC*time.dt
            downThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x, (lander.y),lander.z + 1))
            r = Timer(0.05, destroy_entity, (downThrust,))
            particles.append(downThrust)
            r.start()
        # else:
        #     LANDER_ROTATE_Z_SPEED = min((LANDER_ROTATE_Z_SPEED + 5),0)
        
        LANDER_SPEED_Y += GRAVITY*time.dt
        if LANDER_SPEED_Y > 0:
            lander.y += LANDER_SPEED_Y*time.dt
        if lander.intersects(self.ground).hit:
            LANDER_SPEED_Y = 0
        lander.y += LANDER_SPEED_Y*time.dt
        lander.x += LANDER_SPEED_X*time.dt
        lander.z += LANDER_SPEED_Z*time.dt
        # lander.y += LANDER_SPEED * time.dt
        if abs(lander.rotation_x) < 20:
            lander.rotation_x -= LANDER_ROTATE_X_SPEED*time.dt
        else:
            if(lander.rotation_x) < 0:
                lander.rotation_x = -19
            else:
                lander.rotation_x = 19
            LANDER_ROTATE_X_SPEED = 0

        if abs(lander.rotation_z) < 20:
            lander.rotation_z -= LANDER_ROTATE_Z_SPEED*time.dt 
        else:
            if(lander.rotation_z) < 0:
                lander.rotation_z = -19
            else:
                lander.rotation_z = 19
            LANDER_ROTATE_Z_SPEED = 0
        
        if action == 4:
            # reward -= 10
            direction = Vec3(
            lander.forward * (1) + lander.up * (1)
            ).normalized()

            vector1 = np.array(direction)
            vector2 = np.array([0, 0.707107, 0.707107])
            angle_rad = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
            angle_deg = np.degrees(angle_rad)
            LANDER_SPEED_Y += cos((angle_deg * 3.14)/180)*5*time.dt*15
            direction = Vec3(
            lander.forward * (1)
            ).normalized()
            vector1 = np.array(direction)
            vector2 = np.array([0,1.0,0])
            angle_rad = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
            angle_deg = np.degrees(angle_rad)
            LANDER_SPEED_Z -= (cos((angle_deg * 3.14)/180))*time.dt*30
            direction = Vec3(
            lander.up * (1) 
            ).normalized()
            vector1 = np.array(direction)
            vector2 = np.array([1.0,0,0])
            angle_rad = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
            angle_deg = np.degrees(angle_rad)
            LANDER_SPEED_X += (cos((angle_deg * 3.14)/180))*time.dt*30
     
            downYThrust = Entity(model = "cube", color = color.rgb(255,255,0), collider = "box", scale =(1), position = (lander.x, lander.y-1,lander.z ))
            r = Timer(0.05, destroy_entity, (downYThrust,))
            r.start()
            
        lander.y += LANDER_SPEED_Y*time.dt
        lander.x += LANDER_SPEED_X*time.dt
        lander.z += LANDER_SPEED_Z*time.dt
        if lander.intersects(self.target).hit:
            self.done = True 

        if not lander.intersects(self.ground).hit:
            LANDER_SPEED_Y += GRAVITY*time.dt
            # lander.y += LANDER_SPEED * time.dt
            # lander.rotation_x -= LANDER_ROTATE_X_SPEED*time.dt
            # lander.rotation_z -= LANDER_ROTATE_Z_SPEED*time.dt 
            
        else:
            self.done = True
        
        if lander.y < 0 or lander.y > 40:
            reward -= 10000
            self.done = True
        
        if abs(lander.x) > 100:
            reward = -10000
            self.done = True
        if abs(lander.z) > 100:
            reward = -10000
            self.done = True
        
        p1 = np.array((self.lander.x,self.lander.z,self.lander.y))
        p2 = np.array((self.target.x,self.target.z,self.target.y))
        distprev = np.linalg.norm(prevp1 - prevp2)
        dist = np.linalg.norm(p1 - p2)
        
        
        if abs(LANDER_SPEED_Y)  > 3:
            reward -= 10

        if abs(LANDER_SPEED_Y) > 7:
            reward -= 100
        

        if LANDER_SPEED_Y > 2:
            reward -= 100

        t1 = distprev-dist
        if t1 < 0:
            reward -= 100
        else:
            reward += 10

        # observation = [self.lander.x,self.lander.y,self.lander.z,self.target.x,self.target.y,self.target.z,self.lander.rotation_x,self.lander.rotation_y,self.lander.rotation_z] + list(self.prev_actions)
        observation = [self.lander.x,self.lander.y,self.lander.z,self.target.x,self.target.y,self.target.z,self.lander.rotation_x,self.lander.rotation_y,self.lander.rotation_z, LANDER_SPEED_X,LANDER_SPEED_Y,LANDER_SPEED_Z] 
        self.observation = np.array(observation,dtype = np.float32)
        self.Info.text = str(int(reward)) + " " + str(int(LANDER_SPEED_Y))
        self.reward = reward
        
        
       
    def reset(self, seed = 0 ):
        global GRAVITY,LANDER_SPEED_Y,LANDER_BOOSTER_ACC,LANDER_ROTATE_X_SPEED,LANDER_ROTATE_Y_SPEED,LANDER_ROTATE_Z_SPEED,LANDER_SPEED_X,LANDER_SPEED_Z

        GRAVITY = -9.8 *0.5
        LANDER_SPEED_Y = 0
        LANDER_SPEED_Z = 0
        LANDER_SPEED_X = 0
        LANDER_ROTATE_X_SPEED = 0 
        LANDER_ROTATE_Y_SPEED = 0 
        LANDER_ROTATE_Z_SPEED = 0 

        LANDER_BOOSTER_ACC = 200
        
        self.landerPos = (5,25,5)
        self.targetPos = (random.randint(0,15),1,random.randint(0,15))
        
        try:
            if self.app:
                pass 
                
            if self.target:
                self.target.position = self.targetPos
            else:
                self.target = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2,1,2), position = self.targetPos)
            if self.ground:
                pass 
            else:
                self.ground = Entity(model = "plane", texture = "grass", collider = "box", scale = (100,1,100))
            if self.lander:
                self.lander.position = self.landerPos
                self.lander.rotation = (0,0,0)
            else:
                self.lander = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = self.landerPos)

            if self.player:
                pass 
            else:
                self.player = FirstPersonController()

            if self.Info:
                pass 
            else:
                self.Info = Text(text = '', x = -0.8, y = 0.35)

        except:
            self.app = Ursina() 
            self.target = Entity(model = "cube", color = color.rgb(255,255,255), collider = "box", scale =(2), position = self.targetPos)
            self.ground = Entity(model = "plane", texture = "grass", collider = "box", scale = (100,1,100))
            self.lander = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = self.landerPos)
            self.player = FirstPersonController()
            self.Info = Text(text = '', x = -0.8, y = 0.35)

        self.player.gravity = 0
        self.done = False
        landerPos = self.landerPos
        targetPos = self.targetPos
        self.prev_actions = deque(maxlen = MAX_LEN)  # however long we aspire the snake to be
        for i in range(MAX_LEN):
            self.prev_actions.append(-1) # to create history

        self.prev_actions = deque(maxlen = MAX_LEN)  # however long we aspire the snake to be
        for i in range(MAX_LEN):
            self.prev_actions.append(-1)
        # observation = [landerPos[0], landerPos[1], landerPos[2],targetPos[0],targetPos[1],targetPos[2],self.lander.rotation_x,self.lander.rotation_y,self.lander.rotation_z] + list(self.prev_actions)
        observation = [landerPos[0], landerPos[1], landerPos[2],targetPos[0],targetPos[1],targetPos[2],self.lander.rotation_x,self.lander.rotation_y,self.lander.rotation_z, LANDER_SPEED_X,LANDER_SPEED_Y,LANDER_SPEED_Z]

        self.observation = np.array(observation,dtype = np.float32)
        return self.observation,{}
from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController  
import random 
import time 
import math

import numpy as np

app = Ursina() 
ground = Entity(model = "plane", texture = "grass", collider = "box", scale = (100,1,100))

lander = Entity(model = "cube", texture = "grass", collider = "box", scale =(2), position = (5,20,5))
target = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = (random.randint(0,15),1,random.randint(0,15)))

GRAVITY = -9.8 *0.2
LANDER_SPEED_Y = 0
LANDER_SPEED_Z = 0
LANDER_SPEED_X = 0
LANDER_ROTATE_X_SPEED = 0 
LANDER_ROTATE_Y_SPEED = 0 
LANDER_ROTATE_Z_SPEED = 0 

LANDER_BOOSTER_ACC = 200


def update():
    global GRAVITY,LANDER_SPEED_Y,LANDER_BOOSTER_ACC,LANDER_ROTATE_X_SPEED,LANDER_ROTATE_Y_SPEED,LANDER_ROTATE_Z_SPEED,LANDER_SPEED_X,LANDER_SPEED_Z
    player.y += held_keys["space"]*0.1 
    player.y -= held_keys["shift"]*0.1
    if held_keys["r"]:
        lander.y = 20
    if held_keys["j"]:
        LANDER_ROTATE_X_SPEED += LANDER_BOOSTER_ACC*time.dt
    # else:
    #     LANDER_ROTATE_X_SPEED = max((LANDER_ROTATE_X_SPEED - 5),0)

    if held_keys["i"]:
        LANDER_ROTATE_X_SPEED -= LANDER_BOOSTER_ACC*time.dt
    # else:
    #     LANDER_ROTATE_X_SPEED = min((LANDER_ROTATE_X_SPEED + 5),0)
    
    if held_keys["k"]:
        LANDER_ROTATE_Z_SPEED += LANDER_BOOSTER_ACC*time.dt
    # else:
    #     LANDER_ROTATE_Z_SPEED = max((LANDER_ROTATE_Z_SPEED - 5),0)
    
    if held_keys["l"]:
        LANDER_ROTATE_Z_SPEED -= LANDER_BOOSTER_ACC*time.dt
    # else:
    #     LANDER_ROTATE_Z_SPEED = min((LANDER_ROTATE_Z_SPEED + 5),0)
    
    if not lander.intersects(ground).hit:
        LANDER_SPEED_Y += GRAVITY*time.dt
        lander.y += LANDER_SPEED_Y*time.dt
        lander.x += LANDER_SPEED_X*time.dt
        lander.z += LANDER_SPEED_Z*time.dt
        # lander.y += LANDER_SPEED * time.dt
        lander.rotation_x -= LANDER_ROTATE_X_SPEED*time.dt
        lander.rotation_z -= LANDER_ROTATE_Z_SPEED*time.dt 
        if held_keys["i"] or held_keys["j"] or held_keys["k"] or held_keys["l"]:
            direction = Vec3(
            lander.forward * (1) + lander.up * (1)
            ).normalized()

            vector1 = np.array(direction)
            vector2 = np.array([0, 0.707107, 0.707107])
            angle_rad = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
            angle_deg = np.degrees(angle_rad)
            LANDER_SPEED_Y += cos((angle_deg * 3.14)/180)*5*time.dt
            direction = Vec3(
            lander.forward * (1)
            ).normalized()
            vector1 = np.array(direction)
            vector2 = np.array([0,1.0,0])
            angle_rad = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
            angle_deg = np.degrees(angle_rad)
            LANDER_SPEED_Z -= (cos((angle_deg * 3.14)/180))*time.dt*5
            direction = Vec3(
            lander.up * (1) 
            ).normalized()
            vector1 = np.array(direction)
            vector2 = np.array([1.0,0,0])
            angle_rad = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))
            angle_deg = np.degrees(angle_rad)
            LANDER_SPEED_X += (cos((angle_deg * 3.14)/180))*time.dt*5
     

    else:
        LANDER_SPEED = 0 
    
    if lander.intersects(target):
        print("Reward")
    
  
 
player = FirstPersonController()
player.gravity = 0

while not held_keys["q"]:
    # if lander.intersects(ground).hit:
    #     break
    app.step() 
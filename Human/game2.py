from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController  
import random 
import time 
import math
from threading import Timer

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
particles = []

def destroy_entity(entity):
    global particles
    try:
        particles.remove(entity)
    except:
        pass
    destroy(entity)

def update():
    global GRAVITY,LANDER_SPEED_Y,LANDER_BOOSTER_ACC,LANDER_ROTATE_X_SPEED,LANDER_ROTATE_Y_SPEED,LANDER_ROTATE_Z_SPEED,LANDER_SPEED_X,LANDER_SPEED_Z,particles
    player.y += held_keys["space"]*0.1 
    player.y -= held_keys["shift"]*0.1
    if held_keys["r"]:
        lander.y = 20
    if held_keys["j"]:
        LANDER_SPEED_X += LANDER_BOOSTER_ACC*time.dt/10
        leftThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x-1, (lander.y),lander.z))
        r = Timer(0.2, destroy_entity, (leftThrust,))
        particles.append(leftThrust)
        r.start()
    # else:
    #     LANDER_ROTATE_X_SPEED = max((LANDER_ROTATE_X_SPEED - 5),0)

    if held_keys["i"]:
        LANDER_SPEED_X -= LANDER_BOOSTER_ACC*time.dt/10
        rightThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x+1, (lander.y),lander.z))
        r = Timer(0.2, destroy_entity, (rightThrust,))
        particles.append(rightThrust)
        r.start()
    # else:
    #     LANDER_ROTATE_X_SPEED = min((LANDER_ROTATE_X_SPEED + 5),0)
    
    if held_keys["k"]:
        LANDER_SPEED_Z += LANDER_BOOSTER_ACC*time.dt/10
        upThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x, (lander.y),lander.z - 1))
        r = Timer(0.2, destroy_entity, (upThrust,))
        particles.append(upThrust)
        r.start()
    # else:
    #     LANDER_ROTATE_Z_SPEED = max((LANDER_ROTATE_Z_SPEED - 5),0)
    
    if held_keys["l"]:
        LANDER_SPEED_Z -= LANDER_BOOSTER_ACC*time.dt/10
        downThrust = Entity(model = "cube", color = color.rgb(255,0,0), collider = "box", scale =(0.5), position = (lander.x, (lander.y),lander.z + 1))
        r = Timer(0.2, destroy_entity, (downThrust,))
        particles.append(downThrust)
        r.start()
    # else:
    #     LANDER_ROTATE_Z_SPEED = min((LANDER_ROTATE_Z_SPEED + 5),0)
    if held_keys["g"]:
        LANDER_SPEED_Y += LANDER_BOOSTER_ACC*time.dt/10
        downYThrust = Entity(model = "cube", color = color.rgb(255,255,0), collider = "box", scale =(0.5), position = (lander.x, lander.y-1,lander.z ))
        r = Timer(0.2, destroy_entity, (downYThrust,))
        r.start()
        
    lander.y += LANDER_SPEED_Y*time.dt
    for i in particles:
        print(particles)
        i.y = lander.y
    lander.x += LANDER_SPEED_X*time.dt
    lander.z += LANDER_SPEED_Z*time.dt
    if not lander.intersects(ground).hit:
        LANDER_SPEED_Y += GRAVITY*time.dt
        # lander.y += LANDER_SPEED * time.dt
        # lander.rotation_x -= LANDER_ROTATE_X_SPEED*time.dt
        # lander.rotation_z -= LANDER_ROTATE_Z_SPEED*time.dt 
        
    else:
        LANDER_SPEED_Y = 0
        
    
    if lander.intersects(target):
        print("Reward")
    
  
 
player = FirstPersonController()
player.gravity = 0

while not held_keys["q"]:
    # if lander.intersects(ground).hit:
    #     break
    app.step() 
from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController  
import random 
import time 

app = Ursina() 
ground = Entity(model = "plane", texture = "grass", collider = "box", scale = (100,1,100))

lander = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = (5,20,5))
target = Entity(model = "cube", color = color.rgb(0,0,0), collider = "box", scale =(2), position = (random.randint(0,15),1,random.randint(0,15)))

GRAVITY = -9.8 * 0.03
LANDER_SPEED = 0
LANDER_ROTATE_X_SPEED = 0 
LANDER_BOOSTER_ACC = 200


def update():
    global GRAVITY,LANDER_SPEED,LANDER_BOOSTER_ACC,LANDER_ROTATE_X_SPEED
    player.y += held_keys["space"]*0.1 
    player.y -= held_keys["shift"]*0.1
    if held_keys["r"]:
        lander.y = 20
    if held_keys["j"]:
        LANDER_ROTATE_X_SPEED += LANDER_BOOSTER_ACC*time.dt
    else:
        LANDER_ROTATE_X_SPEED = max((LANDER_ROTATE_X_SPEED - 5),0)

    if not lander.intersects(ground).hit:
        # LANDER_SPEED += GRAVITY
        # lander.y += LANDER_SPEED * time.dt
        lander.rotation_x -= LANDER_ROTATE_X_SPEED*time.dt
        lander.x += held_keys["l"]*0.1
        lander.z -= held_keys["k"]*0.1
        lander.z += held_keys["i"]*0.1
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
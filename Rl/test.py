from env import WorldEnv
from stable_baselines3 import PPO 
import gymnasium as gym 


env = WorldEnv()
env.reset()

model_path = "model_V2.zip"
model = PPO.load(model_path, env = env)

episode = 500 

for ep in range(episode):
    obs = env.reset()
    done = False 
    while not done:
        t  = model.predict(obs)
        action,_states = t
        obs, rewards, done, truncated, info = env.step(action)

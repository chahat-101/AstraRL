from game_obj import Player, Enemy
from rl_env import SpaceDuelEnv, NUM_ACTIONS
import numpy as np


player = Player((640, 360))

enemy = Enemy((960, 360), level=1)

env = SpaceDuelEnv(player, enemy)
obs = env.reset()

for i in range(100):
    action = np.random.randint(0, NUM_ACTIONS)
    obs, reward, done = env.step(action)
    # print(f"step={i} action={action} reward={reward:.2f} done={done} \n {obs}")
    print(f"step = {i} reward:{reward}")
if done:
    obs = env.reset()
    print("Episode ended — resetting\n")

import gymnasium as gym
from gymnasium import spaces
import numpy as np

from game_obj import Player, Enemy
from rl_env import SpaceDuelEnv, NUM_ACTIONS


class SpaceDuelGymEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self):
        super().__init__()

        self.player = Player((640, 360))
        self.enemy = Enemy((960, 360), level=1)

        self.env = SpaceDuelEnv(self.player, self.enemy)

        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(9,),
            dtype=np.float32,
        )

        self.action_space = spaces.Discrete(NUM_ACTIONS)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        obs = self.env.reset()
        info = {}
        return obs, info

    def step(self, action):
        obs, reward, done = self.env.step(action)

        terminated = done
        truncated = False

        info = {}
        return obs, reward, terminated, truncated, info

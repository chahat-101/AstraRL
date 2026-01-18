from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from space_duel_gym_env import SpaceDuelGymEnv
import torch

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
env = DummyVecEnv([lambda: SpaceDuelGymEnv()])


model = DQN(
    "MlpPolicy",
    env,
    learning_rate=1e-4,
    buffer_size=100_000,
    learning_starts=10_000,
    batch_size=64,
    gamma=0.99,
    train_freq=4,
    target_update_interval=1000,
    exploration_fraction=0.2,
    exploration_final_eps=0.05,
    verbose=1,
)


model.learn(total_timesteps=500_000)

model.save("space_duel_dqn")

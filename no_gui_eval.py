from stable_baselines3 import DQN
from space_duel_gym_env import SpaceDuelGymEnv
import time

def evaluate_no_gui():
    # Load the trained model
    model = DQN.load("space_duel_dqn")

    # Create the environment
    env = SpaceDuelGymEnv()

    print("Starting no-GUI evaluation...")

    # Run the simulation for a few episodes
    num_episodes = 5
    for episode in range(num_episodes):
        obs, info = env.reset()
        done = False
        episode_reward = 0
        step_count = 0

        print(f"\n--- Episode {episode + 1}/{num_episodes} ---")

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            episode_reward += reward
            step_count += 1

            # Optional: Print some stats to see progress
            # print(f"Step: {step_count}, Reward: {reward:.2f}, Player HP: {obs[7]:.2f}, Enemy HP: {obs[8]:.2f}")

        print(f"Episode {episode + 1} finished after {step_count} steps with total reward: {episode_reward:.2f}")

    print("\nNo-GUI evaluation finished.")

if __name__ == "__main__":
    evaluate_no_gui()

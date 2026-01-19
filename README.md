# Space Duel: Pygame Shooter with RL Agent

This project is a 2D space combat game built with Pygame. It features a classic arcade-style shooter where a player-controlled ship battles an enemy ship. The project has two modes: a manual mode where you can play the game yourself, and an AI mode where a Reinforcement Learning agent controls the player's ship.

## Features

- Classic 2D space shooter gameplay.
- An AI agent trained using Deep Q-Networks (DQN) with `stable-baselines3`.
- A modular and extensible code structure that allows for easy implementation and testing of different RL algorithms (e.g., PPO, A2C).

## File Structure

- `main.py`: The main game loop for human players.
- `game_obj.py`: Defines all core game objects (Player, Enemy, Bullet), constants, and drawing functions.
- `rl_env.py`: Contains the core logic for the custom reinforcement learning environment.
- `space_duel_gym_env.py`: A wrapper that makes the environment compatible with the `gymnasium` API, allowing it to be used with libraries like `stable-baselines3`.
- `train_dqn.py`: A script to train the DQN agent. The trained model is saved as `space_duel_dqn.zip`.
- `evaluate_agent.py`: A script to load the trained model and watch the AI agent play the game.
- `requirements.txt`: A list of all Python dependencies for the project.

## Installation

1.  **Clone the repository (optional):**
    ```bash
    git clone https://github.com/chahat-101/AstraRL/
    cd AstraRL
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Make sure you have activated your virtual environment before running the scripts.

### Human Player Mode

To play the game yourself, run `main.py`.

```bash
python main.py
```
**Controls:**
- `W`: Thrust forward
- `S`: Thrust backward
- `A`: Rotate left
- `D`: Rotate right
- `SPACE`: Shoot

### Training the AI Agent

To train the AI agent, run the training script. This will run for a set number of timesteps and save the resulting model to `space_duel_dqn.zip`.

```bash
python train_dqn.py
```

### Evaluating the AI Agent

To watch the trained agent play, run the evaluation script. This will load `space_duel_dqn.zip` and render the game with the AI in control.

```bash
python evaluate_agent.py
```

## Extending with Other Algorithms

Thanks to the modular structure, you can easily train the agent with a different algorithm from the `stable-baselines3` library. For example, to use Proximal Policy Optimization (PPO), you could create a new `train_ppo.py` script and simply replace the `DQN` model with the `PPO` model. No changes to the environment files (`rl_env.py`, `space_duel_gym_env.py`) would be necessary.

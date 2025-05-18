from tensorforce.agents import Agent
from reinforcement.rl_environment import TradingEnvironment
import pandas as pd
import joblib

df = joblib.load("data/processed_df.pkl")  # আপনার feature যুক্ত CSV pickle

env = TradingEnvironment(df)

agent = Agent.create(
    agent='ppo',
    environment=env,
    batch_size=10,
    learning_rate=1e-3,
    exploration=0.2,
    max_episode_timesteps=200,
)

for episode in range(100):
    states = env.reset()
    terminal = False
    episode_reward = 0

    while not terminal:
        actions = agent.act(states=states)
        states, terminal, reward = env.execute(actions)
        agent.observe(terminal=terminal, reward=reward)
        episode_reward += reward

    print(f"Episode {episode}: Reward = {episode_reward}")

agent.save(directory='models/tensorforce', filename='trading-agent')

from tensorforce.environments import Environment
import numpy as np
import pandas as pd

class TradingEnvironment(Environment):
    def __init__(self, df):
        self.df = df.reset_index(drop=True)
        self.current_step = 0
        self.balance = 100000
        self.position = 0
        self.entry_price = 0

    def states(self):
        return dict(type='float', shape=(6,))  # RSI, MACD, MA, etc.

    def actions(self):
        return dict(type='int', num_values=3)  # 0 = Hold, 1 = Buy, 2 = Sell

    def reset(self):
        self.current_step = 0
        self.balance = 100000
        self.position = 0
        return self._get_state()

    def execute(self, action):
        done = False
        reward = 0

        current_price = self.df.loc[self.current_step, 'close']

        if action == 1 and self.position == 0:  # Buy
            self.position = 1
            self.entry_price = current_price

        elif action == 2 and self.position == 1:  # Sell
            reward = current_price - self.entry_price
            self.balance += reward
            self.position = 0

        self.current_step += 1
        if self.current_step >= len(self.df) - 1:
            done = True

        return self._get_state(), done, reward

    def _get_state(self):
        row = self.df.iloc[self.current_step]
        return np.array([
            row['rsi'], row['macd'], row['ma_20'], row['ma_50'],
            row['bb_upper'], row['bb_lower']
        ])

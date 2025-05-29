import torch
import torch.nn as nn
import torch.optim as optim
import os
import pickle
import random
from collections import defaultdict


# CFRNet: Simple feedforward NN for MCCFR value approximation
class CFRNet(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super(CFRNet, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, x):
        return self.model(x)

# MCCFR Agent
class MCCFR:
    def __init__(self, input_size, save_path="mccfr_model.pt"):
        self.regret_net = CFRNet(input_size)
        self.strategy_net = CFRNet(input_size)
        self.optimizer = optim.Adam(self.regret_net.parameters(), lr=0.01)
        self.strategy_optimizer = optim.Adam(self.strategy_net.parameters(), lr=0.01)
        self.save_path = save_path

    def get_state_representation(self, player_info, hand):
        return torch.tensor([player_info[0], player_info[2]] + [hash(card) % 100 for card in hand], dtype=torch.float32)

    def get_strategy(self, state):
        return torch.sigmoid(self.strategy_net(state)).item()

    def update_regret(self, state, reward):
        prediction = self.regret_net(state)
        loss = (prediction - reward) ** 2
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_strategy(self, state, reward):
        prediction = self.strategy_net(state)
        loss = (prediction - reward) ** 2
        self.strategy_optimizer.zero_grad()
        loss.backward()
        self.strategy_optimizer.step()

    def draw_with_policy(self, core, player_index):
        player_info = core.players[player_index].getInfo()
        hand = core.deal[player_index]
        state = self.get_state_representation(player_info, hand)
        strategy = self.get_strategy(state)
        draw_count = int(strategy * 3)
        draw_indices = random.sample(range(5), draw_count)
        core.draw(player_index, draw_indices)

    def simulate_game(self, core):
        core.reset()
        for i in range(len(core.players)):
            player_info = core.players[i].getInfo()
            hand = core.deal[i]
            state = self.get_state_representation(player_info, hand)
            strategy = self.get_strategy(state)
            draw_count = int(strategy * 3)
            draw_indices = random.sample(range(5), draw_count)
            core.draw(i, draw_indices)

        points = core.evaluate()
        for i in range(len(core.players)):
            player_info = core.players[i].getInfo()
            hand = core.deal[i]
            state = self.get_state_representation(player_info, hand)
            reward = torch.tensor([points[i]], dtype=torch.float32)
            self.update_regret(state, reward)
            self.update_strategy(state, reward)

    def train(self, core, iterations=1000):
        for _ in range(iterations):
            self.simulate_game(core)

    def save(self):
        torch.save({
            'regret_net': self.regret_net.state_dict(),
            'strategy_net': self.strategy_net.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'strategy_optimizer': self.strategy_optimizer.state_dict()
        }, self.save_path)

    def load(self):
        if os.path.exists(self.save_path):
            checkpoint = torch.load(self.save_path)
            self.regret_net.load_state_dict(checkpoint['regret_net'])
            self.strategy_net.load_state_dict(checkpoint['strategy_net'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            self.strategy_optimizer.load_state_dict(checkpoint['strategy_optimizer'])
            print("Model loaded successfully.")
        else:
            print("No saved model found.")

# ------------------ Playable Terminal Game ------------------ #
if __name__ == "__main__":
    from Controller import CorePoker
    players = [["You"], ["AI"]]
    core = CorePoker(players)
    mccfr = MCCFR(input_size=7)
    mccfr.load()

    core.reset()
    print("\nYour hand:", core.deal[0])
    cards = []
    print("Choose up to 3 cards to draw (indexes 0–4), one per line. Type any non-digit to finish:")
    for _ in range(3):
        choice = input("> ")
        if choice.isdigit() and 0 <= int(choice) <= 4:
            cards.append(int(choice))
        else:
            break
    core.draw(0, cards)

    print("\nAI is thinking...")
    mccfr.draw_with_policy(core, player_index=1)

    points = core.evaluate()
    for i, player in enumerate(core.players):
        print(f"{player.nick} final hand: {core.deal[i]} -> Points: {points[i]}")

    winner = points.index(max(points))
    print(f"\nWinner: {core.players[winner].nick}!")

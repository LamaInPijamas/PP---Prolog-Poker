import torch
import torch.nn as nn
import torch.optim as optim
import os
import random
from tqdm import tqdm
from typing import List, Any, Optional

# [TODO] Fix this pice of shit

MODEL_PATH_PREFIX = "../AI/Models/"

class CFRNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 128):
        super(CFRNet, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 1:
            x = x.unsqueeze(0)  # batch dimension
        return self.model(x).squeeze(-1)

class MCCFR:
    def __init__(self, input_size: int, device: Optional[torch.device] = None, save_path: str = "mccfr_model.pt"):
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        self.regret_net = CFRNet(input_size).to(self.device)
        self.strategy_net = CFRNet(input_size).to(self.device)
        self.optimizer = optim.Adam(self.regret_net.parameters(), lr=0.01)
        self.strategy_optimizer = optim.Adam(self.strategy_net.parameters(), lr=0.01)
        if not os.path.isdir(MODEL_PATH_PREFIX):
            os.makedirs(MODEL_PATH_PREFIX)
        self.save_path = MODEL_PATH_PREFIX + save_path
        self.input_size = input_size

    def get_state_representation(self, player_info: List[Any], hand: List[Any]) -> torch.Tensor:
        """
        Convert player info and hand into a normalized feature tensor.
        """
        # Defensive numeric extraction with default fallback
        p0 = float(player_info[0]) if len(player_info) > 0 and isinstance(player_info[0], (int, float)) else 0.0
        p2 = float(player_info[2]) if len(player_info) > 2 and isinstance(player_info[2], (int, float)) else 0.0

        # Hash cards, mod 100, pad/truncate to length 5
        hand_features = [hash(card) % 100 for card in hand]
        hand_features = (hand_features + [0]*5)[:5]

        features = [p0, p2] + hand_features
        tensor = torch.tensor(features, dtype=torch.float32, device=self.device)
        # Normalize features: example simple normalization
        tensor /= 100.0  # scale card hashes
        return tensor

    def get_strategy(self, state: torch.Tensor) -> float:
        """
        Predict the strategy probability from the strategy network.
        """
        self.strategy_net.eval()
        with torch.no_grad():
            out = self.strategy_net(state)
            strategy = torch.sigmoid(out).clamp(0.0, 1.0).item()
        return strategy

    def update_regret(self, state: torch.Tensor, reward: torch.Tensor) -> None:
        self.regret_net.train()
        pred = self.regret_net(state)
        loss = (pred - reward) ** 2
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_strategy(self, state: torch.Tensor, reward: torch.Tensor) -> None:
        self.strategy_net.train()
        pred = self.strategy_net(state)
        loss = (pred - reward) ** 2
        self.strategy_optimizer.zero_grad()
        loss.backward()
        self.strategy_optimizer.step()

    def draw_with_policy(self, core: Any, player_index: int) -> None:
        player_info = core.players[player_index].getInfo()
        hand = core.deal[player_index]
        state = self.get_state_representation(player_info, hand)
        strategy = self.get_strategy(state)

        draw_count = max(0, min(int(strategy * core.max_draw), core.max_draw))
        draw_indices = random.sample(range(len(hand)), draw_count) if draw_count > 0 else []
        core.draw(player_index, draw_indices)

    def simulate_game(self, core: Any, num_rounds: int = 1) -> None:
        for _ in range(num_rounds):
            core.reset()
            num_players = len(core.players)

            # Drawing phase for all players
            for i in range(num_players):
                player_info = core.players[i].getInfo()
                hand = core.deal[i]
                state = self.get_state_representation(player_info, hand)
                strategy = self.get_strategy(state)

                draw_count = max(0, min(int(strategy * core.max_draw), core.max_draw))
                draw_indices = random.sample(range(len(hand)), draw_count) if draw_count > 0 else []
                core.draw(playerId=i, cardsIndex=draw_indices)

            # Evaluation and learning
            points = core.evaluate()
            for i in range(num_players):
                player_info = core.players[i].getInfo()
                hand = core.deal[i]
                state = self.get_state_representation(player_info, hand)
                reward = torch.tensor(points[i], dtype=torch.float32, device=self.device)
                self.update_regret(state, reward)
                self.update_strategy(state, reward)


    def train(self, core: Any, iterations: int = 1000, rounds: int = 1) -> None:
        for _ in tqdm(range(iterations), desc="Training MCCFR"):
            self.simulate_game(core, rounds)

    def save(self) -> None:
        torch.save({
            'regret_net': self.regret_net.state_dict(),
            'strategy_net': self.strategy_net.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'strategy_optimizer': self.strategy_optimizer.state_dict()
        }, self.save_path)

    def load(self) -> None:
        if os.path.exists(self.save_path):
            checkpoint = torch.load(self.save_path, map_location=self.device)
            self.regret_net.load_state_dict(checkpoint['regret_net'])
            self.strategy_net.load_state_dict(checkpoint['strategy_net'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            self.strategy_optimizer.load_state_dict(checkpoint['strategy_optimizer'])
            print(f"Model loaded successfully from {self.save_path} on {self.device}.")
        else:
            print("No saved model found.")

if __name__ == "__main__":
    import random
    from Controller import CorePoker

    random.seed(42)
    torch.manual_seed(42)

    players = [["You"], ["AI"]]
    core = CorePoker(players)
    mccfr = MCCFR(input_size=7)
    mccfr.load()

    core.reset()
    print("\nYour hand:", core.deal[0])

    cards = []
    print(f"Choose up to {self.core.max_draw} cards to draw (indexes 0–4), one per line. Type any non-digit to finish:")
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

  # --------------- [Include] --------------- #
from Core.Core import Core
from Variants.MCCFRAIPoker import MCCFRAIPoker
from Variants.ClassicTerminalPoker import ClassicTerminalPoker
from AI.MCCFR import MCCFR

# --------------- [GUI] --------------- #
mode = 0
print("Chose Mode")
print("1: Normal")
print("2: MCCFR 5000 AI")
print("3: Visualization of AI")
mode = input()

if mode == "1":
  # --------------- [Normal] --------------- #
  players = [["Daniel"], ["Ruslan"]]
  core = Core(players, 3)
  easy_poker = ClassicTerminalPoker(core)
  easy_poker.run()

if mode == "2":
  # --------------- [AI] --------------- #
  players = [["Daniel"], ["FraniuBot"]]
  core = Core(players, 3)
  mccfr = MCCFR(input_size=7, save_path="monte_carlos_5000.pt")
  mccfr.load()
  poker_ai = MCCFRAIPoker(core, mccfr)
  poker_ai.run()

  # --------------- [Visualization] --------------- #
if mode == "3":
  import matplotlib.pyplot as plt
  from tqdm import tqdm
  import random
  import torch
  random.seed(42)
  torch.manual_seed(42)

  players = [["You"], ["AI"]]
  core = Core(players)
  mccfr = MCCFR(input_size=7)

  NUMBER_OF_GAMES = 100

  iteration_steps = [10, 50, 500, 1000]
  win_rates = []

  def evaluate_win_rate(mccfr, num_games=100):
      wins = 0
      for _ in range(num_games):
          core.reset()
          mccfr.draw_with_policy(core, player_index=1)
          points = core.evaluate()
          winner = points.index(max(points))
          if winner == 1:
              wins += 1
      return wins / num_games

  prev_iters = 0
  for iters in tqdm(iteration_steps, desc="Incremental Training"):
      to_train = iters - prev_iters
      if to_train > 0:
          mccfr.train(core, iterations=to_train, rounds=3)
      win_rate = evaluate_win_rate(mccfr, num_games=NUMBER_OF_GAMES)
      win_rates.append(win_rate)
      prev_iters = iters

  plt.figure(figsize=(10, 6))
  plt.plot(iteration_steps, win_rates, marker='o')
  plt.title("MCCFR Training Iterations vs AI Win Rate")
  plt.xlabel("Training Iterations")
  plt.ylabel("Win Rate (AI)")
  plt.grid(True)
  plt.ylim(0, 1)
  plt.show()

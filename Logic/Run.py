from Controller import CorePoker, PokerAI, EasyPoker
from MCCFR import MCCFR

mode = "Vizualization"

if mode == "AI":
  # --------------- [AI] --------------- #
  players = [["You"], ["AI"]]
  core = CorePoker(players)

  mccfr = MCCFR(input_size=7)
  mccfr.load()

  poker_ai = PokerAI(core, mccfr, rounds=3)
  poker_ai.run()

if mode == "Normal":
  # --------------- [Normal] --------------- #
  players = [["Daniel"], ["Ruslan"]]
  core = CorePoker(players)
  easy_poker = EasyPoker(core, 3)
  easy_poker.run()

  # --------------- [Vizualization] --------------- #
if mode == "Vizualization":
  import matplotlib.pyplot as plt
  from tqdm import tqdm
  import random
  import torch
  random.seed(42)
  torch.manual_seed(42)

  players = [["You"], ["AI"]]
  core = CorePoker(players)
  mccfr = MCCFR(input_size=7)

  iteration_steps = [500, 5000]
  win_rates = []

  def evaluate_win_rate(mccfr, num_games=100):
      wins = 0
      for _ in range(num_games):
          core.reset()
          core.draw(0, [])
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
          mccfr.train(core, iterations=to_train)
      win_rate = evaluate_win_rate(mccfr, num_games=100)
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

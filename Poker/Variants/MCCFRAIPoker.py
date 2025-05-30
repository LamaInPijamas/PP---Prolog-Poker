# ------------------ [ Include ] ------------------ # 
from Core.Core import Core
import os

# ------------------ [ AI Poker class ] ------------------ # 
class MCCFRAIPoker:
  def __init__(self, core: Core, mccfr_agent):
    self.core = core
    self.mccfr = mccfr_agent

  def clear_terminal(self):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

  def run(self):
    self.clear_terminal()
    for round_no in range(self.core.rounds):
      print(f"--- Round {round_no + 1} ---")
      self.core.reset()

      # Human or first player move
      print(f"{self.core.players[0].nick}, your hand: {self.core.deal[0]}")
      cards_to_draw = []
      print(f"Choose up to {self.core.max_draw} cards to draw (indexes 0–4), one per line. Type any non-digit to finish:")
      for _ in range(self.core.max_draw):
        choice = input("> ")
        if choice.isdigit() and 0 <= int(choice) <= 4:
          cards_to_draw.append(int(choice))
        else:
          break
      self.core.draw(0, cards_to_draw)

      # MCCFR AI move (assumed player index 1)
      print("\nAI is thinking...")
      self.mccfr.draw_with_policy(self.core, player_index=1)

    # Evaluate hands
    points = self.core.evaluate()
    for i, player in enumerate(self.core.players):
      print(f"{player.nick} final hand: {self.core.deal[i]} -> Points: {points[i]}")

    winner = points.index(max(points))
    print(f"\nWinner: {self.core.players[winner].nick}!\n")

    if round_no < self.core.rounds - 1:
      input("Press Enter to continue to next round...")
      self.clear_terminal()